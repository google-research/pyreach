# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Implementation of Open AI Gym interface for PyReach."""

import collections
import copy
import logging
import queue
import sys
import threading
import time
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
import uuid
import dataclasses
import gym  # type: ignore
import numpy as np  # type: ignore

import pyreach
from pyreach import core
from pyreach import factory
from pyreach import force_torque_sensor
from pyreach import internal
from pyreach import snapshot as lib_snapshot
from pyreach.gyms import core as gyms_core

TaggedRequest = Tuple[str, str, str, str, str]
Callback = Callable[[Any], bool]
FinishedCallback = Optional[Callable[[], None]]
Stop = Callable[[], None]
AddUpdateCallback = Callable[[Callback, FinishedCallback], Stop]
IKLibType = pyreach.arm.IKLibType
ObservationSnapshot = Tuple[gyms_core.Observation,
                            Tuple[lib_snapshot.SnapshotReference, ...],
                            Tuple[lib_snapshot.SnapshotResponse, ...]]


class ReachVacuumState:
  """ReachVacuumState maps the various vacuum states to int values."""

  OFF = 0
  VACUUM = 1
  BLOWOFF = 2


class ReachElement(object):
  """Base class for all Reach Gym elements."""

  def __init__(self, reach_name: str, action_space: gyms_core.Space,
               observation_space: gyms_core.Space,
               is_synchronous: bool) -> None:
    """Initialize a Reach Element base class.

    Args:
      reach_name: The name of the corresponding device on the Reach server.
        Sometimes this name is empty.
      action_space: The Gym action space to use.
      observation_space: The Gym observation space to use.
      is_synchronous: If True, the next Gym observation will synchronize all
        observations elements that have this flag set otherwise the next
        observation is asynchronous.  This argument is optional and defaults to
        False.
    """
    self._reach_name: str = reach_name
    self._action_space: gyms_core.Space = action_space
    self._observation_space: Optional[gyms_core.Space] = observation_space
    self._config_name: str = ""  # Filled in during registration (never empty)
    self._is_synchronous: bool = is_synchronous
    self._reach_synchronous: Optional[ReachSynchronous] = None
    self._timers: internal.Timers = internal.Timers(set())
    self._task_params: Dict[str, str] = {}

  @property
  def action_space(self) -> gyms_core.Space:
    """Get the action space."""
    return self._action_space

  @property
  def observation_space(self) -> gyms_core.Space:
    """Get the observation space."""
    return self._observation_space

  @property
  def config_name(self) -> str:
    """Get the configuration name."""
    return self._config_name

  @property
  def is_synchronous(self) -> bool:
    """Get the synchronous flag."""
    return self._is_synchronous

  def _timers_select(self, timer_names: Set[str]) -> internal.TimersSet:
    """Select timers to enable/disable for a block of code.

    Args:
      timer_names: A set of timer name strings.  (Must be a Python set).

    Returns:
      Returns the CounterTimerSet for selected timers.

    """
    timers: Optional[internal.Timers] = self._timers
    if not timers:
      raise pyreach.PyReachError(
          f"No performance timers for Reach Element {self._reach_name} found.")
    return timers.select(timer_names)

  def _add_update_callback(self,
                           add_update_callback: AddUpdateCallback) -> None:
    """Cause and update callback to occur.

    Args:
      add_update_callback: A function in the standard `add_updata_callback` form
        from the PyReach API.

    Raises:
      pyreach.PyReachError for internal errors only.

    """
    reach_synchronous: Optional[ReachSynchronous] = self._reach_synchronous
    if reach_synchronous is None:
      raise pyreach.PyReachError("Internal Error: No ReachSynchronous object")
    reach_synchronous.add_update_callback(add_update_callback, self)

  def do_action(
      self, action: gyms_core.Action,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Perform an action with the Element."""
    # Must be implemented in sub class.
    raise pyreach.PyReachError(
        "Internal Error: Unable to do '{0}' action.".format(self.config_name))

  def get_observation(self, host: pyreach.Host) -> ObservationSnapshot:
    """Return the Reach element Gym observation."""
    # Must be implemented in sub class.
    raise pyreach.PyReachError(
        "Internal Error: Unable to get '{0}' observation".format(
            self.config_name))

  def reset_wait(self, host: pyreach.Host) -> None:
    """Wait for reset to complete."""
    # Sub-class this method to deal with waiting for reset to complete.
    pass

  def start_observation(self, host: pyreach.Host) -> bool:
    """Start a synchronous observation."""
    # Must be implemented in sub class.
    raise pyreach.PyReachError(
        "Internal Error: Unable to start '{0}' observation".format(
            self.config_name))

  def get_task_params(self) -> Dict[str, str]:
    """Store the environment task parameters."""
    return self._task_params

  def set_task_params(self, task_params: Dict[str, str]) -> None:
    """Store the environment task parameters."""
    self._task_params = task_params

  def set_reach_synchronous(self,
                            reach_synchronous: "ReachSynchronous") -> None:
    """Set the ReachSynchronous for the Reach Element."""
    self._reach_synchronous = reach_synchronous

  def _get_action_dict(self, action: Any) -> gyms_core.ActionDict:
    """Verify that an action dictionary is a valid (or fail)."""
    if isinstance(action, (dict, collections.OrderedDict)):
      return action
    raise pyreach.PyReachError(
        "Action {0} is neither a Dict nor an collections.OrderedDict".format(
            action))

  def set_timers(self, timers: internal.Timers) -> None:
    """Set the reach environment."""
    self._timers = timers

  def _reshape_image(self, old_image: np.ndarray,
                     new_shape: Tuple[int, ...]) -> np.ndarray:
    """Return a reshaped image.

    Args:
      old_image: The image to reshape.
      new_shape: The new shape of the image.

    Returns:
      Return a cropped image that is padded with zeros.

    """
    if old_image.shape == new_shape:
      return old_image

    dimensions: int = len(old_image.shape)
    assert len(new_shape) == dimensions
    assert 2 <= dimensions <= 3

    index: int
    old_shape: Tuple[int, ...] = old_image.shape
    overlap_shape: Tuple[int, ...] = tuple([
        min(old_shape[index], new_shape[index]) for index in range(dimensions)
    ])

    reshaped_image: np.ndarray = np.zeros(new_shape, dtype=old_image.dtype)
    dx: int = overlap_shape[0]
    dy: int = overlap_shape[1]
    if dimensions == 2:
      reshaped_image[:dx, :dy] = old_image[:dx, :dy]
    else:
      dz: int = overlap_shape[2]
      reshaped_image[:dx, :dy, :dz] = old_image[:dx, :dy, :dz]
    return reshaped_image


class ReachArm(ReachElement):
  """Represents a Reach Arm.

  Attributes:a
    action_space: A Gym action space represented as a Gym Dict Space with
      "command", "joint_angles", "pose", "synchronous", and "id" fields.
      "command" should be 0 for do nothing, 1 for set joint angles and 2 for set
      pose. "joint_angles" should be the desired joint angles in radians. "pose"
      should be the desired arm pose. "synchronous" is only valid when the arm
      is configured as asynchronous. When set to 1, a synchronous move is
      performed. When set to 0 (or not present), an asynchronous move occurs.
      "id" is used to keep track of asynchronous move status. When id is present
      and positive, each asynchronous move can be given a unique id (simple
      counter bumping adequate) to keep track of the returned status for the
      move.  The most recent returned statuses are put into the "responses"
      portion of the arm observation.
    observation_space: A Gym observation space represented as a Gym Dict Space
      with "ts", "joint_angles", and "pose" fields.
  """

  # Valid "response" values:
  RESPONSE_NONE: int = 0
  RESPONSE_DONE: int = 1
  RESPONSE_FAILED: int = 2  # Done with error other than timeout
  RESPONSE_ABORTED: int = 3
  RESPONSE_REJECTED: int = 4
  RESPONSE_TIMEOUT: int = 5  # Done with timeout error.
  RESPONSE_MAX: int = max(RESPONSE_NONE, RESPONSE_DONE, RESPONSE_FAILED,
                          RESPONSE_ABORTED, RESPONSE_REJECTED, RESPONSE_TIMEOUT)

  def __init__(self,
               reach_name: str,
               low_joint_angles: Tuple[float, ...] = (),
               high_joint_angles: Tuple[float, ...] = (),
               apply_tip_adjust_transform: bool = False,
               is_synchronous: bool = False,
               response_queue_length: int = 0,
               ik_lib: Optional[str] = None) -> None:
    """Initialize a Reach Arm.

    The arm may be moved either synchronously or asynchronously.
    In synchronous mode, the follow on observation is delayed until
    the arm stops moving.  In asynchronous mode, the follow on observation
    is performed immediately without waiting for the arm to stop moving.

    There are two ways to put the arm in synchronous mode:
    1. Set is_synchronous to True when the arm is initially configured.
    2. Set is_synchronous to False for initial configuration, but set the
       "synchronous" flag in the arm action space to 1 during a step() call.
       Whenever the "synchronous" flag is set, the arm will move synchronously.
    If the arm is not in synchronous mode, it is moved asynchronously.

    All reach elements that are configured in synchronous mode (arm, vacuum,
    text instructions, etc.) are moved as a group.  The step() call initiates
    all of these synchronous together and waits for them all to complete before
    returning the final observation.

    The other non synchronous reach elements are being continuously polled
    by the PyReach Gym.  Whenever at least one element is in synchronous mode
    (i.e. the arm), the PyReach Gym will also wait for the polled information
    to have timestamps after all of the synchronous operations completed.
    For the arm, this means is that the color camera(s) and depth camera(s)
    will contain images after arm has stopped moving.

    Args:
      reach_name: The Reach name of the arm.
      low_joint_angles : The minimum values for the joint angles in radians. Use
        an empty list if no low limits are specified.
      high_joint_angles: The maximum values for the joint angles in radians. Use
        an empty list if no high limits are specified.
      apply_tip_adjust_transform: If True and a tip adjustment transform is
        available, apply the transform for each arm movement operation.
      is_synchronous: If True, the arm is always moved synchronously; otherwise
        it is typically moved asynchronously.  (For further details see above.)
      response_queue_length: When positive, the PyReach Gym returns the last N
        arm status values for asynchronous moves.
      ik_lib: Whether to use IKFast or IK PyBullet for inverse kinematics.
    """

    if response_queue_length < 0:
      raise pyreach.PyReachError(
          "response length queue must be non-negative: {0}".format(
              response_queue_length))

    action_dict: Dict[str, gyms_core.Action] = {
        "command":
            gym.spaces.Discrete(3),
        "id":
            gym.spaces.Discrete(1 << 30),
        "joint_angles":
            gym.spaces.Box(
                low=np.array(low_joint_angles),
                high=np.array(high_joint_angles),
                dtype=np.dtype(float)),
        "pose":
            gym.spaces.Box(low=-100, high=100, shape=(6,)),
        "reach_action":
            gym.spaces.Discrete(3),
        "use_linear":
            gym.spaces.Discrete(2),
        "preemptive":
            gym.spaces.Discrete(2),
        "velocity":
            gym.spaces.Box(low=0, high=10, shape=()),
        "acceleration":
            gym.spaces.Box(low=0, high=10, shape=()),
        "timeout":
            gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
    }
    if not is_synchronous and response_queue_length:
      action_dict["synchronous"] = gym.spaces.Discrete(2)
    action_space: gym.spaces.Dict = gym.spaces.Dict(action_dict)

    observation_dict: Dict[str, gyms_core.Observation] = {
        "ts":
            gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
        "joint_angles":
            gym.spaces.Box(
                low=np.array(low_joint_angles),
                high=np.array(high_joint_angles),
                dtype=np.dtype(float)),
        "pose":
            gym.spaces.Box(low=-100, high=100, shape=(6,)),
        "status":
            gym.spaces.Discrete(ReachArm.RESPONSE_MAX + 1),
    }
    if response_queue_length:
      response_space: gym.spaces.Dict = gym.spaces.Dict({
          "ts": gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
          "id": gym.spaces.Discrete(1 << 30),
          "status": gym.spaces.Discrete(ReachArm.RESPONSE_MAX + 1),
          "finished": gym.spaces.Discrete(2),
      })
      observation_dict["responses"] = gym.spaces.Tuple(
          (response_space,) * response_queue_length)
    observation_space: gym.spaces.Dict = gym.spaces.Dict(observation_dict)

    super().__init__(reach_name, action_space, observation_space,
                     is_synchronous)
    self._arm: Optional[pyreach.Arm] = None
    self._arm_state_capturer: ArmStateCapturer = ArmStateCapturer()
    self._high_joint_angles: Tuple[float, ...] = high_joint_angles
    self._low_joint_angles: Tuple[float, ...] = low_joint_angles
    self._joints: np.ndarray = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    self._pose: np.ndarray = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    self._pyreach_status: Optional[pyreach.PyReachStatus] = None
    self._response_queue_length: int = response_queue_length
    self._apply_tip_adjust_transform: bool = apply_tip_adjust_transform
    self._last_command: int = 0
    self._ik_lib: Optional[str] = ik_lib

  def __str__(self) -> str:
    """Return string representation of Arm."""
    return "ReachArm('{0}':'{1}')".format(self.config_name, self._reach_name)

  def _joints_ok(self, joints: Tuple[float, ...]) -> bool:
    """Validate that the joint angles are OK.

    Args:
      joints: A list of joint angles to validate.

    Returns:
      True is returned if the joint angles are OK.

    """
    high_joint_angles: Tuple[float, ...] = self._high_joint_angles
    low_joint_angles: Tuple[float, ...] = self._low_joint_angles
    high_size: int = len(high_joint_angles)
    low_size: int = len(low_joint_angles)
    for i, joint in enumerate(joints):
      if i < low_size and joint < low_joint_angles[i]:
        return False
      if i < high_size and joint > high_joint_angles[i]:
        return False
    return True

  def _get_arm(self, host: pyreach.Host) -> pyreach.Arm:
    """Return the Arm or raise a PyReach exception."""
    if self._arm is None:
      with self._timers.select({"!gym*", "host.arm"}):
        reach_name: str = self._reach_name
        if reach_name not in host.arms:
          config_name: str = self.config_name
          arm_names: List[str] = list(host.arms.keys())
          raise pyreach.PyReachError(
              "Arm '{0}' specifies '{1}' which is not one of {2}".format(
                  config_name, reach_name, arm_names))
        self._arm = host.arms[reach_name]
        if self._ik_lib:
          self._arm.set_ik_lib(IKLibType(self._ik_lib))
        self._arm.start_streaming()
    return self._arm

  def fk(self,
         host: Optional[pyreach.Host],
         joints: Union[Tuple[float, ...], List[float], np.ndarray],
         apply_tip_adjust_transform: bool = False) -> Optional[pyreach.Pose]:
    """Uses forward kinematics to get the pose from the joint angles.

    Args:
      host: The host to get the pose from.
      joints: The robot joints.
      apply_tip_adjust_transform: If True, will use the data in the calibration
        file for the robot to change the returned pose from the end of the arm
        to the tip of the end-effector.

    Returns:
      The pose for the end of the arm, or if apply_tip_adjust_transform was
      set to True, the pose for the tip of the end-effector. If the IK library
      was not yet initialized, this will return None.

    """
    if host is None:
      return None
    arm: pyreach.Arm = self._get_arm(host)
    with self._timers.select({"!agent*", "!gym*", "host.arm.fk"}):
      return arm.fk(joints, apply_tip_adjust_transform)

  def get_observation(self, host: pyreach.Host) -> ObservationSnapshot:
    """Return the Reach Arm Gym observation.

    Args:
        host: The host to get the observation from.

    Returns:
        Returns a Tuple containing the Gym Observation, a tuple of
        SnapshotReference objects and a tuple of SnapshotResponse objects.
        The observation that is returned a dictionary with "ts",
        "joint_angles" and "pose" fields.  If the response queue length
        is positive, a tuple of response dictionaries is present as well.
        Each response has consisting of "ts", "id", "status", and "finished".
        "ts" is the status timestamp, "id" is the user specified id
        for the asynchronous arm movement, "status" is the arm status value,
        and "finished" is 0 or 1 for whether the arm action is complete.

    Raises:
        pyreach.PyReachError when there is no observation available.

    """
    with self._timers_select({"!agent*", "gym.arm"}):
      observation: gyms_core.Observation = {}
      try:
        arm: pyreach.Arm = self._get_arm(host)
      except pyreach.PyReachError as runtime_error:
        raise pyreach.PyReachError from runtime_error
      ts: float = 0.0

      responses: List[lib_snapshot.SnapshotResponse] = []

      pyreach_status: Optional[pyreach.PyReachStatus] = self._pyreach_status
      response: int = -1
      if pyreach_status is None:
        response = ReachArm.RESPONSE_NONE
        responses.append(
            lib_snapshot.SnapshotResponse(
                0, "arm", self.config_name,
                lib_snapshot.SnapshotReference(0.0, 0)))
      else:
        responses.append(
            lib_snapshot.SnapshotResponse(0, "arm", self.config_name,
                                          pyreach_status))
        status: str = pyreach_status.status
        error: str = pyreach_status.error
        if status == "done":
          if error == "timeout":
            response = ReachArm.RESPONSE_TIMEOUT
          elif error:
            response = ReachArm.RESPONSE_FAILED
          else:
            response = ReachArm.RESPONSE_DONE
        elif status == "aborted":
          response = ReachArm.RESPONSE_ABORTED
        else:
          logging.warning("Internal Error: Unexpected response '%s' '%s'",
                          status, error)
          response = ReachArm.RESPONSE_FAILED
        if not 0 <= response <= ReachArm.RESPONSE_MAX:
          raise pyreach.PyReachError(
              f"Internal Error: Bad Arm response {response}")

      arm_state: Optional[pyreach.ArmState]
      with self._timers.select({"!agent*", "!gym*", "host.arm.state"}):
        arm_state = arm.fetch_state() if self._is_synchronous else arm.state()

      if arm_state is not None:
        ts = arm_state.time
        joints: Tuple[float, ...] = arm_state.joint_angles
        if self._joints_ok(joints):
          self._joints = np.array(joints)
        elif self._last_command != 0:
          logging.info("++++++++++++++++ Invalid joint angles: %s", joints)
        self._pose = np.array(
            pyreach.Pose.as_list(arm_state.pose), dtype=np.float_)
        observation = {
            "ts": gyms_core.Timestamp.new(ts),
            "joint_angles": self._joints,
            "pose": self._pose,
            "status": response,
        }
        if self._response_queue_length:
          observation["responses"], queue_responses = self._get_response_queue()
          responses.extend(queue_responses)

      if not observation:
        raise pyreach.PyReachError("Unable to get observation for Arm")
      snapshot_reference: Tuple[lib_snapshot.SnapshotReference, ...] = ()
      if arm_state:
        snapshot_reference = (lib_snapshot.SnapshotReference(
            ts, arm_state.sequence),)
      return observation, snapshot_reference, tuple(responses)

  def _get_response_queue(
      self
  ) -> Tuple[gyms_core.Observation, List[lib_snapshot.SnapshotResponse]]:
    """Returns the response queue and a list of snapshot responses.

    Digs through the ArmStateCapturer state and returns a Gym observation
    that contains the most recent N arm states. N is set by the
    response queue length specified at configuration time. Old information
    is culled from ArmStateCapturer.
    """
    response_queue_length: int = self._response_queue_length
    response_spaces: Tuple[gyms_core.Observation, ...] = ()
    arm_state_capturer: ArmStateCapturer = self._arm_state_capturer
    with self._timers.select({"!agent*", "!gym*", "host.arm.status"}):
      storage: Dict[int, ArmResponse] = arm_state_capturer.get_storage()

    arm_response: ArmResponse
    action_id: int
    done: bool

    active_ids: Dict[int, List[ArmResponse]] = {}
    for arm_response in storage.values():
      action_id = arm_response.action_id
      if action_id not in active_ids:
        active_ids[action_id] = []
      active_ids[action_id].append(arm_response)

    def get_timestamp(arm_responses: List[ArmResponse]) -> float:
      """Returns the timestamp for an ArmResponse list.

      Args:
          arm_responses: The list to get the timestamp from.

      Returns:
          The timestamp of the first element in the list.

      Assumes ArmResponses are presorted with highest timestamp first.
      """
      return arm_responses[0].timestamp

    arm_responses_list: List[List[ArmResponse]] = list(active_ids.values())
    arm_responses_list.sort(key=get_timestamp, reverse=True)
    arm_responses_list = arm_responses_list[:response_queue_length]
    arm_responses_list_size: int = len(arm_responses_list)

    responses: List[lib_snapshot.SnapshotResponse] = []

    index: int
    active_counts: Set[int] = set()
    for index in range(response_queue_length):
      timestamp: float = 0.0
      action_id = 0
      status: int = ReachArm.RESPONSE_NONE
      arm_response_status: Optional[core.PyReachStatus] = None
      done = False

      if index < arm_responses_list_size:
        arm_response = arm_responses_list[index][0]
        action_id = arm_response.action_id
        done = arm_response.done
        arm_response_status = arm_response.status
        if arm_response_status:
          status = arm_response_status.code
        timestamp = arm_response.timestamp
        active_counts.add(arm_response.count)

      responses.append(
          lib_snapshot.SnapshotResponse(
              action_id, "arm-" + str(index) + ("-done" if done else ""),
              self._config_name, arm_response_status or
              lib_snapshot.SnapshotReference(0.0, 0)))

      response_space: gyms_core.Observation = {
          "ts": gyms_core.Timestamp.new(timestamp),
          "id": action_id,
          "status": status,
          "finished": int(done),
      }
      response_spaces += (response_space,)

    # Clean out stale counts.
    arm_state_capturer.remove_inactive_counts(active_counts)

    return response_spaces, responses

  def do_action(
      self, action: gyms_core.Action,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Move the Arm to specified joint angles or pose.

    Args:
        action: The Gym Action to perform for the Arm represented a dictionary.
          "command" must be specified as an integer where 0 means do nothing, 1
          means set the joint angles, and 2 means set the pose.  "joint_angles"
          and "pose" must be present depending on the value of "command".
          "joint_angles" or "pose", only one at a time, must be present.
          "use_linear" (0 or 1) indicates to use a linear move. "servo" (0 or 1)
          indicates to do a servo move. "preemptive" indicates that the action
          will preempt existing scripts. "velocity" specifies the joints
          velocity limit in radians per second. "acceleration" specifies a
          joints acceleration limit in radians per second squared. "synchronous"
          specifies that synchronous arm movement needs to be performed when the
          arm is configured in asynchronous mode.  It is ignored if then arm is
          configured in synchronous mode. "timeout" specifies the timeout for
          any synchronous arm move. A negative timeout specifies that there is
          no timeout and a timeout of 0.0 specifies an immediate timeout (which
          is not very useful.)  The timeout is ignored in asynchronous mode.
        host: The host to use to perform the action.

    Raises:
        pyreach.PyReachError when no command or an invalid command
          specified, bad joint angles are specified, a bad pose
          is specified, or there is no Arm actually available.

    Returns:
        The list of gym action snapshots.
    """
    with self._timers_select({"!agent*", "gym.arm"}):
      try:
        arm: pyreach.Arm = self._get_arm(host)
        action_dict: gyms_core.ActionDict = self._get_action_dict(action)
      except pyreach.PyReachError as runtime_error:
        raise pyreach.PyReachError from runtime_error

      if "command" not in action_dict:
        raise pyreach.PyReachError("No command specified in Arm Action.")
      command: Any = action_dict["command"]
      if not (isinstance(command, int) and (0 <= command <= 2)):
        raise pyreach.PyReachError("Invalid arm command -- must be 0, 1, or 2")

      use_linear: bool = action_dict.get("use_linear", 0) == 1
      servo: bool = action_dict.get("servo", 0) == 1
      servo_time_seconds: float = action_dict.get("servo_time_seconds", 0.0)
      servo_lookahead_time_seconds: float = action_dict.get(
          "servo_lookahead_time_seconds", 0.0)
      servo_gain: float = float(action_dict.get("servo_gain", 0.0))
      if not servo:
        if "servo_time_seconds" in action_dict:
          raise pyreach.PyReachError(
              "servo_time_seconds specified without servo set to 1")
        if "servo_lookahead_time_seconds" in action_dict:
          raise pyreach.PyReachError(
              "servo_lookahead_time_seconds specified without servo set to 1")
        if "servo_gain" in action_dict:
          raise pyreach.PyReachError(
              "servo_gain specified without servo set to 1")
      preemptive: bool = action_dict.get("preemptive", 0) == 1
      velocity = float(action_dict.get("velocity", 0.0))
      acceleration = float(action_dict.get("acceleration", 0.0))
      synchronous: bool = action_dict.get("synchronous", 0) == 1
      timeout: Optional[float] = None
      timeout = float(action_dict.get("timeout", -1.0))
      if timeout < 0.0:
        timeout = None
      action_id: int = -1
      if (not self._is_synchronous and not synchronous and
          "id" not in action_dict):
        raise pyreach.PyReachError("id is required for nonsynchronous moves")
      if "id" in action_dict:
        if not isinstance(action_dict["id"], int):
          raise pyreach.PyReachError("id is not an integer: {0}".format(
              action_dict["id"]))
        action_id = action_dict["id"]
        if action_id <= 0:
          raise pyreach.PyReachError(f"id is not positive: {action_id}")

      self._last_command = command
      self._pyreach_status = None

      count: int
      callback: Optional[Callable[[pyreach.PyReachStatus], None]]
      finished_callback: Optional[FinishedCallback]

      if command == 0:
        # Do nothing
        return (lib_snapshot.SnapshotGymArmAction(
            device_type="robot",
            device_name=arm.device_name,
            command=command,
            cid=action_id,
            synchronous=self._is_synchronous or synchronous),)

      if command == 1:
        # Move using joint angles.
        if "joint_angles" not in action_dict:
          raise pyreach.PyReachError("No joint_angles in Arm Action "
                                     "(command == 1)")
        joints: Tuple[float, ...] = tuple(action_dict["joint_angles"].tolist())
        if not self._joints_ok(joints):
          raise pyreach.PyReachError("Bad joint angles {0}".format(joints))

        cmd_tuple = (lib_snapshot.SnapshotGymArmAction(
            device_type="robot",
            device_name=arm.device_name,
            command=command,
            cid=action_id,
            joint_angles=joints,
            use_linear=use_linear,
            velocity=velocity,
            acceleration=acceleration,
            timeout_sec=timeout if timeout else 0.0,
            servo=servo,
            servo_gain=servo_gain,
            servo_lookahead_time_seconds=servo_lookahead_time_seconds,
            synchronous=self._is_synchronous or synchronous),)

        if self._is_synchronous or synchronous:
          with self._timers.select({"!agent*", "!gym*", "host.arm.to_joints"}):
            self._pyreach_status = (
                arm.to_joints(
                    joints,
                    use_linear=use_linear,
                    servo=servo,
                    servo_time_seconds=servo_time_seconds,
                    servo_lookahead_time_seconds=servo_lookahead_time_seconds,
                    servo_gain=servo_gain,
                    preemptive=preemptive,
                    velocity=velocity,
                    acceleration=acceleration,
                    timeout=timeout))
          return cmd_tuple

        # Keep track of the callbacks:
        count = self._arm_state_capturer.start(action_id)

        def arm_state_callback(arm_state: pyreach.PyReachStatus) -> None:
          """Track asynchronous arm state callbacks."""
          self._arm_state_capturer.callback(count, arm_state)

        def arm_state_finished_callback() -> None:
          """Track finished arm state callback."""
          self._arm_state_capturer.finished_callback(count)

        callback = arm_state_callback
        finished_callback = arm_state_finished_callback
        with self._timers.select({"!agent*", "!gym*", "host.arm.to_joints"}):
          arm.async_to_joints(
              joints,
              use_linear=use_linear,
              servo=servo,
              servo_time_seconds=servo_time_seconds,
              servo_lookahead_time_seconds=servo_lookahead_time_seconds,
              servo_gain=servo_gain,
              preemptive=preemptive,
              velocity=velocity,
              acceleration=acceleration,
              callback=callback,
              finished_callback=finished_callback)
        return cmd_tuple

      if command == 2:
        # Move using pose.
        if "pose" not in action_dict:
          raise pyreach.PyReachError("No pose in Arm Action (command == 2)")
        pose: np.ndarray = action_dict["pose"]
        pose_values: List[float] = pose.tolist()
        tip_adjust: bool = self._apply_tip_adjust_transform

        cmd_tuple = (lib_snapshot.SnapshotGymArmAction(
            device_type="robot",
            device_name=arm.device_name,
            command=command,
            cid=action_id,
            pose=tuple(pose.tolist()),
            use_linear=use_linear,
            velocity=velocity,
            acceleration=acceleration,
            apply_tip_adjust_transform=tip_adjust,
            timeout_sec=timeout if timeout else 0.0,
            synchronous=self._is_synchronous or synchronous),)

        if self._is_synchronous or synchronous:
          with self._timers.select({"!agent*", "!gym*", "host.arm.to_pose"}):
            self._pyreach_status = arm.to_pose(
                pyreach.Pose.from_list(pose_values),
                use_linear=use_linear,
                servo=servo,
                servo_time_seconds=servo_time_seconds,
                servo_lookahead_time_seconds=servo_lookahead_time_seconds,
                servo_gain=servo_gain,
                preemptive=preemptive,
                velocity=velocity,
                apply_tip_adjust_transform=tip_adjust,
                acceleration=acceleration,
                timeout=timeout)
          return cmd_tuple

        # Keep track of the callbacks:
        count = self._arm_state_capturer.start(action_id)

        def arm_state_callback2(arm_state: pyreach.PyReachStatus) -> None:
          """Track asynchronous arm state callbacks."""
          self._arm_state_capturer.callback(count, arm_state)

        def arm_state_finished_callback2() -> None:
          """Track finished arm state callback."""
          self._arm_state_capturer.finished_callback(count)

        callback = arm_state_callback2
        finished_callback = arm_state_finished_callback2

        with self._timers.select({"!agent*", "!gym*", "host.arm.to_pose"}):
          arm.async_to_pose(
              pyreach.Pose.from_list(pose_values),
              use_linear=use_linear,
              servo=servo,
              servo_time_seconds=servo_time_seconds,
              servo_lookahead_time_seconds=servo_lookahead_time_seconds,
              servo_gain=servo_gain,
              preemptive=preemptive,
              callback=callback,
              velocity=velocity,
              apply_tip_adjust_transform=tip_adjust,
              acceleration=acceleration,
              finished_callback=finished_callback)
        return cmd_tuple

      raise pyreach.PyReachError(
          "Invalid Arm command {0} (must be 0, 1, or 2)".format(command))

  def start_observation(self, host: pyreach.Host) -> bool:
    """Start a synchronous observation."""
    arm: pyreach.Arm = self._get_arm(host)
    with self._timers.select({"!agent*", "!gym*", "host.arm"}):
      self._add_update_callback(arm.add_update_callback)
    return True

  def reset_wait(self, host: pyreach.Host) -> None:
    """Wait for arm to stop moving after a reset."""

    arm: pyreach.Arm = self._get_arm(host)
    previous_joint_angles: Optional[Tuple[float, ...]] = None
    current_joint_angles: Optional[Tuple[float, ...]] = None
    while True:
      with self._timers.select({"!agent*", "!gym*", "host.arm.state"}):
        current_state: Optional[pyreach.ArmState] = arm.fetch_state()
        if current_state:
          current_joint_angles = current_state.joint_angles
      if previous_joint_angles and current_joint_angles:
        change: float = 0.0
        index: int
        current_joint_angle: float
        for index, current_joint_angle in enumerate(current_joint_angles):
          change += abs(previous_joint_angles[index] - current_joint_angle)
        if change < .01:
          break
      time.sleep(0.25)
      previous_joint_angles = current_joint_angles


@dataclasses.dataclass(frozen=True, order=True)
class ArmResponse:
  """An immutable Arm response class.

  Attributes:
    timestamp: The timestamp of the response in seconds.
    action_id: The positive action id assigned by the agent.
    count: The unique count assigned to the action.
    done: True if this is the last response.
    status: The PyReachStatus or None if no status received yet.
  """
  timestamp: float  # First for sorting purposes.
  count: int
  action_id: int
  done: bool
  status: Optional[pyreach.PyReachStatus]


class ArmStateCapturer(object):
  """A class to keep track of asynchronous ArmState responses."""

  def __init__(self) -> None:
    """Initializes the ArmState object."""
    self._lock = threading.Lock()
    self._counter: int = 0
    self._storage: Dict[int, ArmResponse] = {}

  def start(self, action_id: int) -> int:
    """Starts a new arm state."""
    with self._lock:
      assert action_id >= 0
      self._counter += 1
      self._storage[self._counter] = ArmResponse(
          0.0,
          count=self._counter,
          action_id=action_id,
          done=False,
          status=None)
      return self._counter

  def callback(self, count: int, status: pyreach.PyReachStatus) -> None:
    """A progress callback for an ArmState."""
    with self._lock:
      if count in self._storage:
        arm_response: ArmResponse = self._storage[count]
        timestamp: float = arm_response.timestamp
        action_id: int = arm_response.action_id
        done: bool = arm_response.done
        arm_response = ArmResponse(timestamp, count, action_id, done, status)
        self._storage[count] = arm_response

  def finished_callback(self, count: int) -> None:
    """Finished callback for an ArmState."""
    with self._lock:
      if count in self._storage:
        arm_response: ArmResponse = self._storage[count]
        timestamp: float = arm_response.timestamp
        action_id: int = arm_response.action_id
        status: Optional[pyreach.PyReachStatus] = arm_response.status
        arm_response = ArmResponse(timestamp, count, action_id, True, status)
        self._storage[count] = arm_response

  def get_storage(self) -> Dict[int, ArmResponse]:
    """Return the storage dictionary."""
    with self._lock:
      return copy.deepcopy(self._storage)

  def remove_count(self, count: int) -> None:
    """Delete a value from the storage dictionary."""
    with self._lock:
      if count in self._storage:
        del self._storage[count]

  def remove_inactive_counts(self, active_counts: Set[int]) -> None:
    """Delete inactive values from the storage dictionary."""
    with self._lock:
      all_counts: Set[int] = set(self._storage.keys())
      old_count: int
      for old_count in all_counts - active_counts:
        del self._storage[old_count]


class ReachColorCamera(ReachElement):
  """Represents a Reach Color Camera.

  Attributes:
    observation_space: This is a Gym Dict Space that contains a "ts" and "color"
      options.  This attribute is read only.
  """

  def __init__(self,
               reach_name: str,
               shape: Tuple[int, int],
               force_fit: bool = False,
               is_synchronous: bool = False) -> None:
    """Initialize a Reach Color Camera.

    Initializes the Gym interface to a reach color camera.

    Args:
      reach_name: Reach name of the color camera.  This name must match the name
        used by the remote robot host (e.g. "uvc", ...)
      shape: The shape (dx, dy) of the color image.  The ndarray shape is
        extended to (dx, dy, 3).  The pixel values are unit8.
      force_fit: If True, any misconfigured cameras are simply cropped to shape.
        must match shape.  A PyReachError is raised for
      is_synchronous: If True, the next Gym observation will synchronize all
        observactions element that have this flag set otherwise the next
        observation is asynchronous.  This argument is optional and defaults to
        False.  There is no way to validate the image shape at initialization
        time. Instead, a PyReach exception is raised when the shape mismatch is
        first detected.  Setting force_fit to True avoids the exception and
        simply crops the image to shape.
    """
    if len(shape) != 2:
      raise pyreach.PyReachError("ColorCamera shape is {shape}, not (DX,DY)")
    color_shape: Tuple[int, int, int] = shape + (3,)
    observation_space: gym.spaces.Dict = gym.spaces.Dict({
        "ts":
            gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
        "color":
            gym.spaces.Box(low=0, high=255, shape=color_shape, dtype=np.uint8),
    })
    action_space: gym.spaces.Dict = gym.spaces.Dict({})

    super().__init__(reach_name, action_space, observation_space,
                     is_synchronous)
    self._color_camera: Optional[pyreach.ColorCamera] = None
    self._force_fit: bool = force_fit
    self._shape: Tuple[int, int, int] = color_shape

  def __str__(self) -> str:
    """Return string representation of a Reach Color Camera."""
    return f"ReachColorCamera('{self.config_name}','{self._reach_name}')"

  def do_action(
      self, action: gyms_core.Action,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Do nothing for an action.

    Args:
      action: Gym action space to process.  Should be empty.
      host: The PyReach host connect to.

    Returns:
        The list of gym action snapshots.
    """
    return ()

  def _get_color_camera(self, host: pyreach.Host) -> pyreach.ColorCamera:
    """Return the ColorCamera or raise a PyReach exception."""
    reach_name: str = self._reach_name
    if self._color_camera is None:
      with self._timers.select({"!agent*", "!gym*", "host.color"}):
        if reach_name not in host.color_cameras:
          camera_names: List[str] = list(host.color_cameras.keys())
          raise pyreach.PyReachError(
              "Color camera '{0}' needs to be one of {1}".format(
                  reach_name, camera_names))
        self._color_camera = host.color_cameras[reach_name]
        self._color_camera.start_streaming(1.0)
    return self._color_camera

  def get_observation(self, host: pyreach.Host) -> ObservationSnapshot:
    """Return the Reach Color Camera Gym observation.

    Args:
      host: The reach host to use.

    Returns:
      Returns a Tuple containing the Gym Observation, a tuple of
      SnapshotReference objects and a tuple of SnapshotResponse objects.
      The Gym camera observation consists of dictionary with
      "ts" and "color", where "color" contains a 3-dimensional
      array (dx, dy, 3) containing the pixel values.

    Raises:
      pyreach.PyReachError when an image does not match the specified shape.

    """
    color_camera: pyreach.ColorCamera = self._get_color_camera(host)
    with self._timers_select({"!agent*", "!gym*", "host.color"}):
      color_frame: Optional[pyreach.ColorFrame] = color_camera.image()
    with self._timers_select({"!agent*", "gym.color"}):
      image: np.ndarray
      ts: float = 0.0
      if color_frame is None:
        image = np.zeros(self._shape, dtype=np.uint8)
      else:
        image = color_frame.color_image
        ts = color_frame.time
      if image.shape != self._shape:
        if self._force_fit:
          image = self._reshape_image(image, self._shape)
        else:
          raise pyreach.PyReachError(
              "Internal Error: Returned color camera image for "
              f"'{self.config_name}' is {image.shape}, "
              f"not desired {self._shape}")
      observation: gyms_core.Observation = {
          "ts": gyms_core.Timestamp.new(ts),
          "color": image,
      }
      snapshot_reference: Tuple[lib_snapshot.SnapshotReference, ...] = ()
      if color_frame:
        snapshot_reference = (lib_snapshot.SnapshotReference(
            ts, color_frame.sequence),)
      return observation, snapshot_reference, ()

  def start_observation(self, host: pyreach.Host) -> bool:
    """Start a synchronous observation."""
    color_camera: pyreach.ColorCamera = self._get_color_camera(host)
    with self._timers.select({"!agent*", "gym.color"}):
      self._add_update_callback(color_camera.add_update_callback)
    return True


class ReachDepthCamera(ReachElement):
  """Represents a Reach Depth Camera.

  Attributes:
    observation_space: The Gym observation Space for the depth camera as
      dictionary with "ts", "depth" and (optionally) "color" fields. The depth
      is an 2D array (dx, dy) of unit16's.  If present, the color image is a 3D
      array (dx, dy, 3) of uint8's.  There is no action_space attribute set.
  """

  def __init__(self,
               reach_name: str,
               shape: Tuple[int, int],
               color_enabled: bool,
               force_fit: bool = False,
               is_synchronous: bool = False) -> None:
    """Initialize a Reach Depth Camera.

    Initializes the Gym interface to a Reach depth camera.

    Args:
      reach_name: Name of the depth camera.  This name must match the name used
        by the remote robot host (e.g. "photoneo", "realsense", etc.)
      shape: The shape (dx, dy) of the depth image.  The ndarray shape is
        extended to (dx, dy, 3).  The depth image has values of np.uint16.
      color_enabled: If True, color images are enabled.  The ndarray shape same
        as the depth camera shape (i.e.  (dx, dy, 3).) The pixel values are
        np.uint8.
      force_fit: If True, any misconfigured cameras are simply cropped to shape.
        must match shape.  A PyReachError is raised for
      is_synchronous: If True, the next Gym observation will synchronize all
        observactions element that have this flag set otherwise the next
        observation is asynchronous.  This argument is optional and defaults to
        False.  There is no way to validate the image shape at initialization
        time. Instead, a PyReach exception is raised when the shape mismatch is
        first detected.  Setting force_fit to True avoids the exception and
        simply crops the image to shape.
    """
    if len(shape) != 2:
      raise pyreach.PyReachError(f"Depth camera has shape {shape}, not (DX,DY)")
    depth_shape: Tuple[int, int] = shape
    color_shape: Tuple[int, int, int] = shape + (3,)

    observation_space_dict: Dict[str, gym.spaces.Space]
    observation_space_dict = {
        "ts":
            gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
        "depth":
            gym.spaces.Box(
                low=0,
                high=65535,
                shape=depth_shape,
                dtype=np.uint16,
            )
    }
    if color_enabled:
      observation_space_dict["color"] = gym.spaces.Box(
          low=0, high=255, shape=color_shape, dtype=np.uint8)
    action_space: gym.spaces.Dict = gym.spaces.Dict({})
    observation_space: gym.spaces.Dict = gym.spaces.Dict(observation_space_dict)

    super().__init__(reach_name, action_space, observation_space,
                     is_synchronous)
    self._depth_shape: Tuple[int, int] = depth_shape
    self._depth_camera: Optional[pyreach.DepthCamera] = None
    self._force_fit: bool = force_fit
    self._color_shape: Tuple[int, int, int] = color_shape
    self._color_enabled: bool = color_enabled

  def __str__(self) -> str:
    """Return a string representation of ReachDepthCamera."""
    return "ReachDepthCamera('{0}':'{1}', {2}, {3}')".format(
        self.config_name, self._reach_name, self._depth_shape,
        self._color_enabled)

  def _get_depth_camera(self, host: pyreach.Host) -> pyreach.DepthCamera:
    """Return the DepthCamera.

    Args:
      host: The pyreach.Host to use for getting the camera.

    Returns:
      Returns the appropriate ColorCamera object.

    Raises:
      pyreach.PyReachError if the color camera is not available.

    """
    reach_name: str = self._reach_name
    if self._depth_camera is None:
      with self._timers.select({"!agent*", "!gym*", "host.depth"}):
        if reach_name not in host.depth_cameras:
          depth_camera_names: List[str] = list(host.depth_cameras.keys())
          raise pyreach.PyReachError(
              "Depth camera '{0}' needs to specify one of '{1}'".format(
                  reach_name, depth_camera_names))
        self._depth_camera = host.depth_cameras[reach_name]
        self._depth_camera.start_streaming(1.0)
    return self._depth_camera

  def do_action(
      self, action: gyms_core.Action,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Do nothing for an action.

    Args:
      action: Gym action space to process.  Should be empty
      host: The pyreach.Host connect to.

    Returns:
        The list of gym action snapshots.
    """
    return ()

  def get_observation(self, host: pyreach.Host) -> ObservationSnapshot:
    """Fetch the Reach Depth Camera Gym observation.

    Args:
      host: The host to get the observation from.

    Returns:
      Returns a Tuple containing the Gym Observation, a tuple of
      SnapshotReference objects and a tuple of SnapshotResponse objects.
      The observation space is a Gym Dict Space with
      "ts", "depth", and (if requested) "color" entries.
      If the depth image is not available yet, a zero timestamp
      is returned with no "depth" entry.

    Raises:
      pyreach.PyReachError if there are any mismatches between the specified
        color/depth image shapes and the actual ones obtained.

    """
    depth_camera: pyreach.DepthCamera = self._get_depth_camera(host)
    with self._timers_select({"!agent*", "gym.depth"}):
      reach_name: str = self._reach_name
      force_fit: bool = self._force_fit
      depth_shape: Tuple[int, ...] = self._depth_shape
      color_shape: Tuple[int, ...] = self._color_shape

      ts: float = 0.0
      color_image: Optional[np.ndarray] = None
      depth_image: np.ndarray
      with self._timers.select({"!agent*", "!gym*", "host.depth"}):
        depth_frame: Optional[pyreach.DepthFrame] = depth_camera.image()
      snapshot_reference: Tuple[lib_snapshot.SnapshotReference, ...] = ()
      if depth_frame is None:
        depth_image = np.zeros(shape=self._depth_shape, dtype=np.uint16)
        if self._color_enabled:
          color_image = np.zeros(shape=self._color_shape, dtype=np.uint8)
      else:
        ts = depth_frame.time
        depth_image = depth_frame.depth_data
        if self._color_enabled:
          color_image = depth_frame.color_data
        snapshot_reference = (lib_snapshot.SnapshotReference(
            ts, depth_frame.sequence),)

      if depth_image.shape != depth_shape:
        if force_fit:
          depth_image = self._reshape_image(depth_image, depth_shape)
        else:
          raise pyreach.PyReachError(
              f"Returned depth camera image for '{reach_name}' "
              f"is {depth_image.shape}, not desired {depth_shape}")

      if color_image is not None and color_image.shape != color_shape:
        if force_fit:
          color_image = self._reshape_image(color_image, color_shape)
        else:
          raise pyreach.PyReachError(
              f"Returned color camera image for '{reach_name}' "
              f"is {color_image.shape}, not desired {color_shape}")

      result: Dict[str, np.ndarray] = {
          "ts": gyms_core.Timestamp.new(ts),
          "depth": depth_image,
      }
      if color_image is not None:
        result["color"] = color_image
      return result, snapshot_reference, ()

  def start_observation(self, host: pyreach.Host) -> bool:
    """Start a synchronous observation."""
    depth_camera: pyreach.DepthCamera = self._get_depth_camera(host)
    with self._timers.select({"!agent*", "gym.depth"}):
      self._add_update_callback(depth_camera.add_update_callback)
    return True


class ReachForceTorqueSensor(ReachElement):
  """Represents a Reach Force Torque Sensor.

  A Reach force torque sensor that returns force and torque values.

  Attributes:
    observation_space: The Gym observation space for the Reach force torque
      sensor.  This consists of a Gym Dict Space with "force", "torque", and
      "ts" sub Spaces. This attribute is read-only.
    action_space: A Gym Dict Space that is empty.
  """

  def __init__(self, reach_name: str, is_synchronous: bool = False) -> None:
    """Init a ReachForceTorqueSensor.

    Args:
      reach_name: The underlying Reach device type name of the force torque
        sensor.  May be empty.
      is_synchronous: If True, the next Gym observation will synchronize all
        observations element that have this flag set otherwise the next
        observation is asynchronous.  This argument is optional and defaults to
        False.
    """
    action_space: gym.spaces.Dict = gym.spaces.Dict({})
    observation_space: gym.spaces.Dict = gym.spaces.Dict({
        "force": gym.spaces.Box(low=0, high=sys.maxsize, shape=(3,)),
        "torque": gym.spaces.Box(low=0, high=sys.maxsize, shape=(3,)),
        "ts": gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
    })

    super().__init__(reach_name, action_space, observation_space,
                     is_synchronous)
    self._force_torque_sensor_state: Optional[
        force_torque_sensor.ForceTorqueSensorState] = None
    self._force_torque_sensor: Optional[
        force_torque_sensor.ForceTorqueSensor] = None

  def __str__(self) -> str:
    """Return a string representation of ReachForceToqueSensor."""
    return f"ReachForceTorqueSensor({self.config_name}, {self._reach_name})"

  def get_observation(self, host: pyreach.Host) -> ObservationSnapshot:
    """Return the Reach Force Torque Sensor actuator Gym observation.

    Args:
      host: The reach host to use.

    Returns:
      Returns a Tuple containing the Gym Observation, a tuple of
      SnapshotReference objects and a tuple of SnapshotResponse objects.
      The observation is Gym Dict Space with "force", "torque" and "ts" values.

    """
    if self._force_torque_sensor is None:
      with self._timers_select({"!agent*", "!gym*", "arm.force_torque_sensor"}):
        if self._reach_name not in host.force_torque_sensors:
          force_torque_sensor_names: List[str] = list(
              host.force_torque_sensors.keys())
          raise pyreach.PyReachError(
              f"Force Torque Sensor '{self._reach_name}' "
              f"is not one of {force_torque_sensor_names}")
        self._force_torque_sensor = host.force_torque_sensors[self._reach_name]

    with self._timers_select({"!agent*", "!gym*", "arm.force_torque_sensor"}):
      self._force_torque_sensor_state = (
          self._force_torque_sensor.fetch_state()
          if self._is_synchronous else self._force_torque_sensor.state)

    force: core.Force = (
        self._force_torque_sensor_state.force
        if self._force_torque_sensor_state else core.Force(0.0, 0.0, 0.0))
    torque: core.Torque = (
        self._force_torque_sensor_state.torque
        if self._force_torque_sensor_state else core.Torque(0.0, 0.0, 0.0))
    ts: float = (
        self._force_torque_sensor_state.time
        if self._force_torque_sensor_state else 0.0)
    sequence: int = (
        self._force_torque_sensor_state.sequence
        if self._force_torque_sensor_state else 0)
    observation: gyms_core.Observation = {
        "force": np.array([force.x, force.y, force.z], dtype=np.float_),
        "torque": np.array([torque.x, torque.y, torque.z], dtype=np.float_),
        "ts": gyms_core.Timestamp.new(ts),
    }
    snapshot_reference: Tuple[lib_snapshot.SnapshotReference, ...] = ()
    if sequence:
      snapshot_reference = (lib_snapshot.SnapshotReference(ts, sequence),)

    return observation, snapshot_reference, ()

  def do_action(
      self, action: gyms_core.Action,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Do any necessary work for force/torque sensor.

    Args:
      action: The action dictionary, ignored.
      host: Reach host.

    Returns:
        The list of gym action snapshots.
    """
    return ()

  def start_observation(self, host: pyreach.Host) -> bool:
    """Start a synchronous_observation."""
    return True


class ReachOracle(ReachElement):
  """Represents an Reach Oracle.

  A Reach Oracle takes a depth image and returns a list of pick points.
  Only the first pick point is returned.

  Attributes:
    observation_space: The Gym observation space for the Oracle. This consists
      of a Gym Dict Space with "ts", "request", and "pick_point" sub Spaces.
      This attribute is read-only.
    action_space: A Gym Dict Space with a "request" entry. This attribute is
      read only. observation_space> A Gym Dict Space with "ts", "request" and
      "pick_point" entries.
  """

  EMPTY_TAGGED_REQUEST: TaggedRequest = ("", "", "", "", "")

  # Valid  "request" values:
  REQUEST_NONE: int = 0
  REQUEST_LEFT_BIN: int = 1
  REQUEST_RIGHT_BIN: int = 2
  REQUEST_MAX: int = max(REQUEST_NONE, REQUEST_LEFT_BIN, REQUEST_RIGHT_BIN)

  # Valid "response" values:
  RESPONSE_NONE: int = 0
  RESPONSE_SUCCESS: int = 1
  RESPONSE_FAIL: int = 2
  RESPONSE_MAX: int = max(RESPONSE_NONE, RESPONSE_SUCCESS, RESPONSE_FAIL)

  def __init__(self,
               reach_name: str,
               task_code: str,
               intent: str = "",
               success_type: str = "",
               is_synchronous: bool = False) -> None:
    """Initialize a Reach Oracle.

    Args:
      reach_name: The name of the Oracle.
      task_code: The task code string.
      intent: The intention of the task.
      success_type: The type of success.
      is_synchronous: If True, the next Gym observation will synchronize all
        observation elements that have this flag set otherwise the next
        observation is asynchronous.  This argument is optional and defaults to
        False.
    """
    # Note a Box can store floats, but pixel indices are actually ints.
    action_space: gym.spaces.Dict = gym.spaces.Dict(
        {"request": gym.spaces.Discrete(ReachOracle.REQUEST_MAX + 1)})
    observation_space: gym.spaces.Dict = gym.spaces.Dict({
        "ts":
            gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
        "pick_point":
            gym.spaces.Box(low=-sys.maxsize, high=sys.maxsize, shape=(2,)),
        "request":
            gym.spaces.Discrete(ReachOracle.REQUEST_MAX + 1),
        "response":
            gym.spaces.Discrete(ReachOracle.RESPONSE_MAX + 1)
    })

    super().__init__(reach_name, action_space, observation_space,
                     is_synchronous)
    self._oracle: Optional[pyreach.Oracle] = None
    self._label: str = ""
    self._last_ts: float = -1.0
    self._request: int = ReachOracle.REQUEST_NONE
    self._tagged_request: TaggedRequest = ReachOracle.EMPTY_TAGGED_REQUEST
    self._pick_status: Optional[Callable[[], List[pyreach.Metric]]] = None
    self._prediction: Optional[pyreach.Prediction] = None
    self._task_code: str = task_code
    self._intent: str = intent
    self._success_type: str = success_type
    self._execute_action_status: Optional[pyreach.PyReachStatus] = None
    self._selected_point: Optional[pyreach.PredictionPoint] = None
    self._selected_pick_place_point: Optional[
        pyreach.PredictionPickPlacePoint] = None
    self._rejected_pick_points: List[pyreach.PredictionPoint] = []

  def __str__(self) -> str:
    """Return a string represenation of Reach Oracle."""
    return "ReachOracle('{0}:{1}')".format(self.config_name, self._reach_name)

  def end_task(self) -> None:
    """End the task."""
    self.disable_tagged_request()
    self._rejected_pick_points = []
    self._execute_action_status = None
    self._selected_point = None
    self._request = ReachOracle.REQUEST_NONE

  def disable_tagged_request(self) -> None:
    """End sending tagged requests."""
    empty_tagged_request: TaggedRequest = ReachOracle.EMPTY_TAGGED_REQUEST
    if self._tagged_request:
      self._tagged_request = empty_tagged_request
      self._label = ""

  def _enable_tagged_request(self, label: str) -> None:
    """Start tagged requests."""
    tagged_request: TaggedRequest = ("pick", "pick", "sparse", self._task_code,
                                     label)
    if self._tagged_request != tagged_request:
      self._tagged_request = tagged_request
      self._label = label

  def _get_oracle(self, host: pyreach.Host) -> pyreach.Oracle:
    """Return the Color Camera.

    Args:
      host: The pyreach.Host to use for getting the camera.

    Returns:
      Returns the Oracle object.

    Raises:
      pyreach.PyReachError if the color camera is not available.

    """
    if self._oracle is None:
      if host.oracle is None:
        raise pyreach.PyReachError("There is no Oracle configured for host.")
      self._oracle = host.oracle
    return self._oracle

  def _get_latest_prediction(self, host: pyreach.Host) -> pyreach.Prediction:
    """Return a the most recent prediction.

    This code works around:
    * Multiple Images Using the Same Device-Data:
    Args:
      host: Reach host.

    Raises:
      pyreach.PyReachError when neither oracle nor prediction is found.

    Returns:
      Requested prediction.
    """
    oracle: pyreach.Oracle = self._get_oracle(host)
    with self._timers.select({"!agent*", "!gym*", "host.oracle"}):
      prediction: Optional[pyreach.Prediction] = None
      prediction = oracle.prediction()

    prediction_try: int
    for prediction_try in range(3):
      tagged_request: TaggedRequest = self._tagged_request
      if tagged_request == ReachOracle.EMPTY_TAGGED_REQUEST:
        raise pyreach.PyReachError(
            "Internal Error: Oracle tagged request not set")

      with self._timers.select({"!agent*", "!gym*", "host.oracle"}):
        prediction = oracle.fetch_prediction(*tagged_request, timeout=30.0)
      if prediction:
        logging.debug(">>>>>>>>>>>>>>>>Got 'prediction' message @ %f",
                      prediction.time)
        break

    if not prediction:
      raise pyreach.PyReachError(
          "Internal Error: No Oracle prediction after {0} trys.".format(
              prediction_try + 1))
    if not prediction:
      raise pyreach.PyReachError(
          "Internal Error: Unable to get Oracle Prediction")
    return prediction

  def get_observation(self, host: pyreach.Host) -> ObservationSnapshot:
    """Return the Oracle Gym observation.

    Args:
      host: Reach host.

    Returns:
      Returns a Tuple containing the Gym Observation, a tuple of
      SnapshotReference objects and a tuple of SnapshotResponse objects.
      The observation is a Gym Dict Space with "ts", "pick_point",
      and "request" values.
    """
    # TODO: the oracle does not return snapshots.
    with self._timers_select({"!agent*", "gym.oracle"}):
      ts: float = 0.0
      if self._request != ReachOracle.REQUEST_NONE:
        if not self._label:
          raise pyreach.PyReachError(
              "Internal Error: No bin selected for Oracle")
        tagged_request: TaggedRequest = self._tagged_request
        if tagged_request == ReachOracle.EMPTY_TAGGED_REQUEST:
          raise pyreach.PyReachError(
              "Internal Error: No tagged request for Oracle")
        try:
          prediction = self._get_latest_prediction(host)
          self._prediction = prediction
          assert prediction
        except pyreach.PyReachError as reach_error:
          raise pyreach.PyReachError from reach_error
        ts = prediction.time

      if not self._selected_point:
        pick_point = np.array([-1.0, -1.0])
      else:
        pick_point = np.array([self._selected_point.x, self._selected_point.y])

      execute_action_status: Optional[
          pyreach.PyReachStatus] = self._execute_action_status
      response: int = ReachOracle.RESPONSE_NONE
      if (execute_action_status and
          execute_action_status.status not in ("rejected", "aborted")):
        metrics: List[pyreach.Metric] = (
            self._pick_status() if self._pick_status else [])
        self._pick_status = None
        metric: pyreach.Metric
        for metric in metrics:
          key: str = metric.key
          if key == "operator/success":
            response = ReachOracle.RESPONSE_SUCCESS
          elif key == "operator/failure":
            response = ReachOracle.RESPONSE_FAIL
          elif key == "operator/attempt":
            pass
          else:
            logging.error("Gym Oracle: Unhandled metric: '%s'", key)
      elif self._selected_point:
        self._rejected_pick_points.append(self._selected_point)

      observation: gyms_core.Observation = {
          "ts": gyms_core.Timestamp.new(ts),
          "pick_point": pick_point,
          "request": self._request,
          "response": response,
      }
      return observation, (), ()

  def start_observation(self, host: pyreach.Host) -> bool:
    """Start a synchronous observation."""
    # The gym gets gets the first observation before getting the first action.
    # So, the first time through, there is no tagged request.
    # Thus, there is nothing to do if there is no tagged request.
    tagged_request: TaggedRequest = self._tagged_request
    if tagged_request == ReachOracle.EMPTY_TAGGED_REQUEST:
      return False
    return True

  def do_action(
      self, action: gyms_core.Action,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Perform an action for the Gym Oracle.

    Args:
      action: An Gym Dict Space with an "request" value. The "request" value is
        tagged to the return oracle request.
      host: Reach host.

    Returns:
        The list of gym action snapshots.
    """
    # TODO: the oracle does not store actions.
    with self._timers_select({"!agent*", "gym.oracle"}):
      oracle: pyreach.Oracle
      if self._oracle is None:
        if host.oracle is None:
          raise pyreach.PyReachError("There is no Oracle configured for host.")
        self._oracle = host.oracle
      oracle = self._oracle
      assert oracle is not None

      if not isinstance(host.arm, pyreach.Arm):
        raise pyreach.PyReachError("Internal Error: Arm not found.")
      arm: pyreach.Arm = host.arm
      if not isinstance(host.depth_camera, pyreach.DepthCamera):
        raise pyreach.PyReachError("Internal Error: Oracle not found.")
      depth_camera: pyreach.DepthCamera = host.depth_camera

      try:
        action_dict: gyms_core.ActionDict = self._get_action_dict(action)
      except pyreach.PyReachError as runtime_error:
        raise pyreach.PyReachError from runtime_error

      with self._timers.select({"!agent*", "!gym*", "host.depth"}):
        color_depth = depth_camera.image()
        if color_depth is None:
          color_depth = depth_camera.fetch_image()

      if not color_depth:
        logging.warning("Failed to receive depth image. Ignoring.")
        return ()

      calibration = host.config.calibration
      if not calibration:
        logging.warning("Calibration is missing. Ignoring.")
        return ()

      constraints = host.config.constraint
      if not constraints:
        logging.warning("Constraints are missing. Ignoring.")
        return ()

      label: str = ""
      bin_name: str = ""
      request: int
      if "request" in action_dict:
        request = int(action_dict["request"])
        if request == ReachOracle.REQUEST_LEFT_BIN:
          label = "SingulateLeftBin"
          bin_name = "left"
        elif request == ReachOracle.REQUEST_RIGHT_BIN:
          label = "SingulateRightBin"
          bin_name = "right"
      if not label:
        return ()
      self._request = request
      self._enable_tagged_request(label)

      prediction: Optional[pyreach.Prediction] = self._prediction
      if not prediction:
        try:
          prediction = self._get_latest_prediction(host)
        except pyreach.PyReachError as reach_error:
          raise pyreach.PyReachError from reach_error
      assert prediction

      self._selected_point = None
      self._selected_pick_place_point = None
      self._execute_action_status = None
      selected_point_3d: Optional[List[pyreach.ActionInput]] = None
      if prediction:
        prediction_points = prediction.points
        prediction_pick_place_points = prediction.pick_place_points
        # Singulation support
        if prediction_points:
          inputs_3d: List[Tuple[np.ndarray, np.ndarray, np.ndarray]] = []
          for pt in prediction_points:
            point_normal = color_depth.get_point_normal(int(pt.x), int(pt.y))
            if point_normal is None:
              continue
            inputs_3d.append(
                (point_normal[2], point_normal[0], point_normal[1]))
          if not inputs_3d:
            logging.warning("Converting pick points to 3D failed. Ignoring.")
            return ()
          for i, point in enumerate(inputs_3d):
            pick_point: np.ndarray = point[1]
            if prediction_points[i] in self._rejected_pick_points:
              continue
            if constraints.is_point_in_object(pick_point, bin_name):
              self._selected_point = prediction_points[i]
              selected_point_3d = [
                  pyreach.ActionInput(
                      prediction_point=point, position=None, rotation=None)
              ]
              break
            self._selected_point = None
            self._execute_action_status = None
        # Kitting support
        elif prediction_pick_place_points:
          pick_place_pt: pyreach.PredictionPickPlacePoint
          pick_place_pt = prediction_pick_place_points[0]
          selected_point_3d = [
              pyreach.ActionInput(
                  prediction_point=None,
                  position=pick_place_pt.pick_position_3d,
                  rotation=pick_place_pt.pick_rotation_quat_3d),
              pyreach.ActionInput(
                  prediction_point=None,
                  position=pick_place_pt.place_position_3d,
                  rotation=pick_place_pt.place_rotation_quat_3d),
          ]
          self._selected_pick_place_point = pick_place_pt

      if ((self._selected_point or self._selected_pick_place_point) and
          self._intent == "pick"):
        metrics: pyreach.Metrics = host.metrics
        pick_id: str
        read_status: Callable[[], List[pyreach.Metric]]
        pick_id, read_status = metrics.start_pick()

        if not isinstance(selected_point_3d, list):
          raise pyreach.PyReachError(
              "Internal Error: Oracle no selected 3D point")
        with self._timers.select({"!agent*", "!gym*", "host.arm.execute"}):
          self._execute_action_status = arm.execute_action(
              label,
              selected_point_3d,
              intent=self._intent,
              success_type=self._success_type,
              pick_id=pick_id,
              use_unity_ik=True)
          self._pick_status = read_status
    return ()


class ReachServer(ReachElement):
  """Represents a Reach Server.

  Attributes:
    observation_space: A Gym Dict Space that specifies a "latest_ts" value. This
      attribute is read only.
  """

  def __init__(self, reach_name: str, is_synchronous: bool = False) -> None:
    """Initialize a Reach Server.

    Args:
      reach_name: The reach name of the reach server device. (Not used.)
      is_synchronous: If True, the next Gym observation will synchronize all
        observactions element that have this flag set otherwise the next
        observation is asynchronous.  This argument is optional and defaults to
        False.
    """
    self._latest_ts: float = 0.0

    action_space: gym.spaces.Dict = gym.spaces.Dict({})
    observation_space: gym.spaces.Dict = gym.spaces.Dict({
        "latest_ts": gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
    })
    super().__init__(reach_name, action_space, observation_space,
                     is_synchronous)

  def __str__(self) -> str:
    """Return a string representation of ReachServer."""
    return "ReachServer('{0}':'{1}', latest_ts={2})".format(
        self.config_name, self._reach_name, self._latest_ts)

  def get_observation(self, host: pyreach.Host) -> ObservationSnapshot:
    """Return the Reach Server Gym Observation as Dict.

    Args:
      host: The host to get the observation from.

    Returns:
      Returns a Tuple containing the Gym Observation, a tuple of
      SnapshotReference objects and a tuple of SnapshotResponse objects.
      The observation is Dict with the "latest_ts" set.

    """
    # The latest timestamp is updated up in ReachElement _get_observation().
    # Set to zero here so that it is bogus if the update does not happen.
    latest_ts: Any = gyms_core.Timestamp.new(0.0)
    server_observation: Dict[str, Any] = {"latest_ts": latest_ts}
    return server_observation, (), ()

  def do_action(
      self, action: gyms_core.Action,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Do nothing for an action.

    Args:
      action: Gym action space to process.  Should be empty
      host: The pyreach.Host connect to.

    Returns:
        The list of gym action snapshots.
    """
    return ()


class ReachTextInstructions(ReachElement):
  """Represents some text instructions.

  Attributes:
    action_space: An empty dictionary which is obviously ignored.
    observation_space: A Gym observation space with "ts" and "text" fields. The
      text field is a Gym MultiDiscrete space that is 1024 long with each
      element capable of holding in a value from 0-127.  The text instruction is
      encoded in UTF-8 and null padded to fill out the buffer.
    task_enable: Integer flag indicating if task is enabled.
  """

  def __init__(self, reach_name: str, is_synchronous: bool = False) -> None:
    """Init a Text Instruction element.

    Args:
      reach_name: The name of the corresponding device on the Reach server. This
        name can be empty.
      is_synchronous: If True, the next Gym observation will synchronize all
        observactions elements that have this flag set otherwise the next
        observation is asynchronous.  This argument is optional and defaults to
        False.
    """
    action_space: gym.spaces.Dict = gym.spaces.Dict({})
    observation_space: gym.spaces.Dict = gym.spaces.Dict({
        "ts": gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
        "instruction": gym.spaces.MultiDiscrete(1024 * [255]),
    })

    super().__init__(reach_name, action_space, observation_space,
                     is_synchronous)
    self._text_instruction: Optional[pyreach.TextInstruction] = None
    self._text_instructions: Optional[pyreach.TextInstructions] = None
    self._counter: int = 0
    self.task_enable: int = -1

  def __str__(self) -> str:
    """Return string representation of Arm."""
    return "ReachTextInstructions('{0}':'{1}')".format(self.config_name,
                                                       self._reach_name)

  def get_observation(self, host: pyreach.Host) -> ObservationSnapshot:
    """Return the Reach Server Gym Observation as an empty Dict.

    Args:
      host: The host to get the observation from.

    Returns:
      Returns a Tuple containing the Gym Observation, a tuple of
      SnapshotReference objects and a tuple of SnapshotResponse objects.
      The TextInstructions Observation is a dictionary containing a "ts",
      "counter" and "instruction" value.  The counter is incremented each
      time a new instruction is received.  The "instruction" value is a
      1024 byte null padded array with encoded text instructions in UTF-8
      format.

    Raises:
      pyreach.PyReachError when there is not observation available.

    """
    with self._timers_select({"!agent*", "gym.text"}):
      last_text_instruction: Optional[pyreach.TextInstruction] = (
          self._text_instruction)
      text_instructions_device: pyreach.TextInstructions = (
          self._get_text_instructions_device(host))
      current_text_instruction: Optional[pyreach.TextInstruction]

      device: pyreach.TextInstructions = text_instructions_device
      with self._timers.select({"!agent*", "!gym*", "host.text"}):
        current_text_instruction = (
            device.fetch_text_instruction()
            if self._is_synchronous else device.text_instruction)

      instruction_bytes: List[int] = 1024 * [0]
      ts: float = 0.0
      seq: int = 0
      counter: int = self._counter

      if current_text_instruction:
        if last_text_instruction:
          if current_text_instruction.uid != last_text_instruction.uid:
            counter += 1
        else:
          counter += 1
        ts = gyms_core.Timestamp.new(current_text_instruction.time)
        seq = current_text_instruction.sequence

        self._text_instruction = current_text_instruction
        self._counter = counter

        instruction: str = current_text_instruction.instruction
        instruction_bytes = list(bytes(instruction, "utf-8"))[:1024]
        pad_size: int = 1024 - len(instruction_bytes)
        instruction_bytes.extend(pad_size * [0])

      observation: gyms_core.Observation = {
          "counter": counter,
          "ts": ts,
          "instruction": np.array(instruction_bytes),
      }
      return observation, (), (lib_snapshot.SnapshotResponse(
          counter, "text-instruction", self.config_name,
          lib_snapshot.SnapshotReference(ts, seq)),)

  def do_action(
      self, action: gyms_core.Action,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Start/stop the action.

    Args:
      action: The Gym Action Space to process as a Gym Dict Space with a
        "task_enable" field (0=End, 1=Start).
      host: The reach host to use.

    Returns:
        The list of gym action snapshots.
    """
    with self._timers_select({"!agent*", "gym.text"}):
      action_dict: gyms_core.ActionDict = self._get_action_dict(action)
      if "task_enable" in action_dict:
        task_enable: int = int(action_dict["task_enable"])
        if self.task_enable != task_enable:
          # State needs to change.
          task_params: Dict[str, str] = self.get_task_params()
          if task_enable:
            # Send a start task message.
            host.logger.start_task(task_params)
          else:
            # Send an end task message.
            host.logger.end_task(task_params)
          self.task_enable = task_enable
          return (lib_snapshot.SnapshotGymLoggerAction("operator", "", False,
                                                       task_enable != 0,
                                                       task_params),)
    return ()

  def start_observation(self, host: pyreach.Host) -> bool:
    """Start a synchronous observation."""
    return False

  def end_task(
      self, host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """End the task.

    Args:
      host: the PyReach Host.

    Returns:
        The list of gym action snapshots.
    """
    if self.task_enable == 1:
      task_params: Dict[str, str] = self.get_task_params()
      host.logger.end_task(task_params)
      self.task_enable = 0
      self._executate_action_status = None
      self._prediction = 0
      return (lib_snapshot.SnapshotGymLoggerAction("operator", "", False, False,
                                                   task_params),)
    return ()

  def _get_text_instructions_device(
      self, host: pyreach.Host) -> pyreach.TextInstructions:
    """Return the pyreach.TextInstructions device."""
    if self._text_instructions is None:
      if host.text_instructions is None:
        raise pyreach.PyReachError(
            "Internal Error: There is no pyreach.TextInstructions "
            "configured for host.")
      self._text_instructions = host.text_instructions
    return self._text_instructions


class ReachVacuum(ReachElement):
  """Represents a Reach Actuator."""

  def __init__(self, reach_name: str, is_synchronous: bool = False) -> None:
    """Initialize a Vacuum actuator.

    Args:
      reach_name: The Reach name of the vacuum.  May be empty.
      is_synchronous: If True, the next Gym observation will synchronize all
        observations element that have this flag set otherwise the next
        observation is asynchronous.  This argument is optional and defaults to
        False.
    """
    # 0=>Vacuum off and 1=>Vacuum on.
    action_space: gym.spaces.Dict = gym.spaces.Dict({
        "state": gym.spaces.Discrete(3),
    })
    observation_space: gym.spaces.Dict = gym.spaces.Dict({
        "ts": gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
        "state": gym.spaces.Discrete(3),
    })

    super().__init__(reach_name, action_space, observation_space,
                     is_synchronous)
    self._vacuum: Optional[pyreach.Vacuum] = None
    self._state: int = ReachVacuumState.OFF
    self._last_send_lock: threading.Lock = threading.Lock()
    self._last_send_count: int = 0
    self._last_send_state: Optional[int] = None

  def __str__(self) -> str:
    """Return string representation of Vacuum."""
    return "ReachVacuum('{0}':'{1}', {2})".format(self.config_name,
                                                  self._reach_name, self._state)

  def get_observation(self, host: pyreach.Host) -> ObservationSnapshot:
    """Return the Reach Vacuum actuator Gym observation.

    Args:
      host: The reach host to use.

    Returns:
      Returns a Tuple containing the Gym Observation, a tuple of
      SnapshotReference objects and a tuple of SnapshotResponse objects.
      The next observation is a Gym Dict Space with "ts" and "state" values.

    """
    with self._timers_select({"!agent*", "gym.vacuum"}):
      reach_name: str = self._reach_name
      if self._vacuum is None:
        with self._timers.select({"!agent*", "!gym*", "host.vacuum"}):
          if reach_name not in host.vacuums:
            vacuum_names: List[str] = list(host.vacuums.keys())
            raise pyreach.PyReachError("Vacuum '{0}' is not one of {1}".format(
                reach_name, vacuum_names))
          self._vacuum = host.vacuums[reach_name]
      vacuum: Optional[pyreach.Vacuum] = self._vacuum
      if vacuum is None:
        raise pyreach.PyReachError("Vacuum is not set")

      ts: float = 0.0
      state = ReachVacuumState.OFF
      vacuum_state = vacuum.state
      snapshots: List[lib_snapshot.SnapshotReference] = []
      if vacuum_state:
        ts = vacuum_state.time
        if vacuum_state.state:
          state = ReachVacuumState.VACUUM
        snapshots.append(
            lib_snapshot.SnapshotReference(
                time=vacuum_state.time, sequence=vacuum_state.sequence))
      blowoff_state = vacuum.support_blowoff and vacuum.blowoff_state
      if blowoff_state:
        ts = max(ts, blowoff_state.time)
        if blowoff_state.state:
          state = ReachVacuumState.BLOWOFF
        snapshots.append(
            lib_snapshot.SnapshotReference(
                time=blowoff_state.time, sequence=blowoff_state.sequence))

      self._state = state
      observation: gyms_core.Observation = {
          "ts": gyms_core.Timestamp.new(ts),
          "state": state,
      }
      return observation, tuple(snapshots), ()

  def do_action(
      self, action: gyms_core.Action,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Set/Clear the vacuum.

    Args:
      action: The Gym Action Space to process as a Gym Dict Space with a "state"
        field (0=Off, 1=Vacuum, 2=BlowOff).
      host: The reach host to use.

    Returns:
        The list of gym action snapshots.
    """

    with self._timers_select({"!agent*", "gym.vacuum"}):
      try:
        action_dict: gyms_core.ActionDict = self._get_action_dict(action)
      except pyreach.PyReachError as runtime_error:
        raise pyreach.PyReachError from runtime_error

      if "state" not in action_dict:
        raise pyreach.PyReachError("Invalid Vacuum action {0}.".format(action))
      desired_state: int = action_dict["state"]
      vacuum: Optional[pyreach.Vacuum] = self._vacuum
      if vacuum is None:
        raise pyreach.PyReachError("Vacuum is not set")
      last_send_state = self._last_send_state
      if desired_state == self._state:
        pass  # Do not send requests if state is already set
      elif (last_send_state is not None and last_send_state == desired_state and
            not self._is_synchronous):
        pass  # Do not send requests for a given state if it is requested
      else:
        send_count = 0
        with self._last_send_lock:
          self._last_send_count += 1
          send_count = self._last_send_count
          self._last_send_state = desired_state

        def completed_callback() -> None:
          with self._last_send_lock:
            if self._last_send_count == send_count:
              self._last_send_state = None

        if desired_state == ReachVacuumState.OFF:
          with self._timers_select({"!agent*", "!gym*", "host.vacuum"}):
            if self._is_synchronous:
              vacuum.off()
              completed_callback()
            else:
              vacuum.async_off(finished_callback=completed_callback)
        elif desired_state == ReachVacuumState.VACUUM:
          with self._timers_select({"!agent*", "!gym*", "host.vacuum"}):
            if self._is_synchronous:
              vacuum.on()
              completed_callback()
            else:
              vacuum.async_on(finished_callback=completed_callback)
        elif desired_state == ReachVacuumState.BLOWOFF:
          with self._timers_select({"!agent*", "!gym*", "host.vacuum"}):
            if self._is_synchronous:
              vacuum.blowoff()
              completed_callback()
            else:
              vacuum.async_blowoff(finished_callback=completed_callback)
        else:
          raise pyreach.PyReachError(
              "Invalid Vacuum state request {0}".format(desired_state))
      return (lib_snapshot.SnapshotGymVacuumAction(
          device_type="robot",
          device_name=vacuum.device_name,
          state=desired_state,
          synchronous=self._is_synchronous),)

  def start_observation(self, host: pyreach.Host) -> bool:
    """Start a synchronous observation."""
    return True


class ReachSynchronous(object):
  """A class to synchronous observations from ReachElement's."""

  def __init__(self,
               host: pyreach.Host,
               timers: internal.Timers,
               timeout: Optional[float] = 15.0) -> None:
    """Init the Reach Synchronous object."""
    self._add_update_callbacks: Dict[str, AddUpdateCallback] = {}
    self.elements: Dict[str, ReachElement] = {}
    self._host: pyreach.Host = host
    self._lock: threading.Lock = threading.Lock()
    self._pending_actions: Set[str] = set()
    self._q: queue.Queue[str] = queue.Queue()
    self._stops: Dict[str, Callable[[], None]] = {}
    self._timeout: Optional[float] = timeout
    self._timers: internal.Timers = timers

  def _register_element(self, element: ReachElement) -> None:
    """Register a ReachElement for synchronous observations.

    Args:
      element: The ReachElement to register.
    """
    element.set_reach_synchronous(self)
    with self._lock:
      self.elements[element.config_name] = element

  def add_update_callback(self, add_update_callback: AddUpdateCallback,
                          element: ReachElement) -> None:
    """Add an update callback for an element.

    Args:
      add_update_callback: A standard PyReach method that registers a couple of
        callback routines when the update shows up. This function always returns
        a function that can be called at any time to shut down any callback
        requests.
      element: Target element.
    """
    with self._lock:
      config_name: str = element.config_name
      if config_name not in self._add_update_callbacks:
        self._add_update_callbacks[config_name] = add_update_callback
      self._register_stop(element)

  def _register_stop(self, element: ReachElement) -> None:
    """Register a stop assuming the lock is held."""
    config_name: str = element.config_name
    if config_name not in self._add_update_callbacks:
      raise pyreach.PyReachError(
          "Internal error: no add_update_callback found '{0}'".format(
              config_name))
    if config_name in self._stops:
      raise pyreach.PyReachError(
          "Internal error: Duplicate callback '{0}'".format(config_name))

    add_update_callback: AddUpdateCallback = (
        self._add_update_callbacks[config_name])
    stop: Callable[[], None] = (
        add_update_callback(lambda msg: True, lambda: self._q.put(config_name)))

    self._stops[config_name] = stop
    if element.action_space:
      self._pending_actions.add(config_name)

  def synchronize_observations(
      self, observations: Dict[str, gyms_core.Observation]
  ) -> Tuple[float, List[lib_snapshot.SnapshotReference],
             List[lib_snapshot.SnapshotResponse]]:
    """Wait for the synchronized observations to complete.

    Args:
      observations: set of observations that need to be synced.

    Raises:
      pyreach.PyReachError for internal errors.

    Returns:
      The latest timestamp among all observations.
    """

    snapshot_references: Dict[str, Tuple[Tuple[lib_snapshot.SnapshotReference,
                                               ...],
                                         Tuple[lib_snapshot.SnapshotResponse,
                                               ...]]] = {}
    with self._timers.select({"!agent*", "gym.sync"}):

      def stops_clear() -> None:
        """Clear out the stops table."""
        # Done with the lock held.
        config_name: str
        stop: Callable[[], None]
        for config_name, stop in stops.items():
          stop()
          del stops[config_name]

      latest_ts: float = 0.0
      minimum_ts: float = 0.0
      with self._lock:
        elements: Dict[str, ReachElement] = self.elements
        element: ReachElement
        host: pyreach.Host = self._host
        pending_actions: Set[str] = self._pending_actions
        stops: Dict[str, Callable[[], None]] = self._stops
        stop: Callable[[], None]
        q: queue.Queue[str] = self._q
        config_name: str
        if pending_actions:
          minimum_ts = sys.float_info.max
        while stops:
          # Get the stop and clear it.
          try:
            config_name = q.get(block=True, timeout=self._timeout)
          except queue.Empty:
            stops_clear()
            raise pyreach.PyReachError(
                "Internal Error: Observation timeout: waiting for {0}".format(
                    list(stops.keys())))
          stop = stops[config_name]
          stop()
          del stops[config_name]

          # Get the observation timestamp:
          if config_name not in elements:
            raise pyreach.PyReachError(
                "Internal Error: '{0}' not found".format(config_name))
          element = elements[config_name]
          observation: gyms_core.Observation
          references: Tuple[lib_snapshot.SnapshotReference, ...]
          responses: Tuple[lib_snapshot.SnapshotResponse, ...]
          observation, references, responses = element.get_observation(host)
          if not isinstance(observation, dict):
            raise pyreach.PyReachError(
                "Internal Error: No observation dictionary")
          if "ts" not in observation:
            raise pyreach.PyReachError(
                "Internal Error: No timestamp for '{0}'".format(
                    element.config_name))
          observation_ts: float = observation["ts"]
          latest_ts = max(latest_ts, observation_ts)
          logging.debug(
              ">>>>>>>>>>>>>>>>Got message from '%s' message @ %f} "
              "Waiting for %s Pending Actions: %s", config_name, observation_ts,
              list(stops.keys()), pending_actions)
          observations[config_name] = observation
          snapshot_references[config_name] = references, responses

          if element.action_space:
            # Action and Observation:
            if minimum_ts >= sys.float_info.max:
              minimum_ts = observation_ts
            else:
              minimum_ts = max(minimum_ts, observation_ts)
            logging.debug(">>>>>>>>>>>>>>>>minimum_ts: %f", minimum_ts)
            pending_actions.discard(config_name)
          elif pending_actions or observation_ts < minimum_ts:
            # Observation only:
            logging.debug(">>>>>>>>>>>>>>>>Retrigger '%s'", config_name)
            self._register_stop(element)

        if stops:
          stops_clear()
          raise pyreach.PyReachError("Internal Error: "
                                     "Non-empty ReachSynchronize stops table")

        # Sometimes a synchronous request makes no sense, in which case
        # we need to back fill the missing ones:
        for element in elements.values():
          config_name = element.config_name
          if config_name not in observations:
            observation, references, responses = element.get_observation(host)
            observations[config_name] = observation
            snapshot_references[config_name] = (references, responses)

        observation_names: Set[str] = set(observations.keys())
        element_names: Set[str] = set(elements.keys())
        if observation_names != element_names:
          raise pyreach.PyReachError(
              "observation_names{0} != element_names{1}".format(
                  observation_names, element_names))

      list_references: List[lib_snapshot.SnapshotReference] = []
      list_responses: List[lib_snapshot.SnapshotResponse] = []
      for refs, resps in snapshot_references.values():
        list_references.extend(refs)
        list_responses.extend(resps)

      return latest_ts, list_references, list_responses

  def start_observations(self, host: pyreach.Host) -> None:
    """Start a synchronized observations.

    Args:
      host: The host to start the observation on.

    Raises:
      pyreach.PyReachError for internal errors.

    """
    with self._timers.select({"!agent*", "gym.sync"}):
      with self._lock:
        stops: Dict[str, Callable[[], Any]] = self._stops
        named_elements: List[Tuple[str, ReachElement]] = (
            list(self.elements.items()))

      actions_started: int = 0
      observations_started: int = 0
      element: ReachElement
      config_name: str
      for config_name, element in named_elements:
        if config_name in stops:
          raise pyreach.PyReachError(
              "Internal Error: Duplicate stop {0}".format(config_name))
        if element.start_observation(host):
          observations_started += 1
          if element.action_space:
            actions_started += 1


# ReachEnv:
class ReachEnv(gym.Env):  # type: ignore
  """Reach compatibale OpenAI/Gym.

  Attributes:
    action_space: A Gym Dict Space that specifies the entire action Space for
      the environment.  This attribute is read only.
    observation_space: A Gym Dict space that specifies the entire observation
      space for the environment.
    metadata: An initialy empty Dict of Any's.  This is available for user
      debugging.
    reward_range: Specifies maximum and minimum value for rewards as a two
      floats in a tuple.
  """

  @property
  def action_space(self) -> gyms_core.Space:
    """Return the action space."""
    return self._action_space

  @property
  def observation_space(self) -> gyms_core.Space:
    """Return the observation space."""
    return self._observation_space

  @property
  def reward_range(self) -> Tuple[float, float]:
    """Return the reward range."""
    return self._reward_range

  @property
  def metadata(self) -> Dict[str, Any]:
    """Return the meda data dictionary."""
    return self._metadata

  def __init__(self,
               pyreach_config: Optional[Dict[str, ReachElement]] = None,
               task_params: Optional[Dict[str, str]] = None,
               timeout: Optional[float] = None,
               host: Optional[pyreach.Host] = None,
               gym_env_id: Optional[str] = None,
               **kwargs: Any) -> None:
    """Initialize a Reach Gym Environment.

    Args:
      pyreach_config: A dictionary of named ReachElements. (Default: {}.)
      task_params: Additional parameters for the task. (Default: {}.)
      timeout: A timeout in seconds to set for synchronous gym. (Default: None.)
      host: A host to use. (Default: None.)
      gym_env_id: ID used to create this gym. Must be specified.
      **kwargs: Additional keyword arguments.

    Raises:
      pyreach.PyReachError for configuration errors.

    """
    super().__init__()
    assert gym_env_id, (
        "The gym_env_id argument must be specified. Please ensure the gym was "
        "using the pyreach gym register wrapper function and that gym_env_id "
        "is passed through any subclass __init__().")
    self._gym_env_id: str = gym_env_id
    self._timers = internal.Timers({
        "agent",
        "gym.action",
        "gym.arm",
        "gym.color",
        "gym.depth",
        "gym.force_torque_sensor",
        "gym.init",
        "gym.obs",
        "gym.oracle",
        "gym.reset",
        "gym.step",
        "gym.sync",
        "gym.text",
        "gym.vacuum",
        "host.arm.execute",
        "host.arm.fk",
        "host.arm.state",
        "host.arm.status",
        "host.arm.to_joints",
        "host.arm.to_pose",
        "host.color",
        "host.depth",
        "host.force_torque_sensor",
        "host.oracle",
        "host.text",
        "host.vacuum",
    })

    # Create the run ID
    self._run_id: str = str(uuid.uuid4())

    # Relay timers the host via the Internal class.
    internal.Internal.set_timers(self._timers)

    # Assign all non-gym and non-host activity to the "agent" timer.
    agent_timer: internal.Timer = self._timers["agent"]
    agent_timer.start()

    with self._timers.select({"!agent*", "gym.init"}):
      if not pyreach_config:
        pyreach_config = {}
      if not task_params:
        task_params = {}
      host_kwargs: Dict[str, Any] = {}
      if not host:
        host = factory.LocalTCPHostFactory(**host_kwargs).connect()
      reach_synchronous: ReachSynchronous = (
          ReachSynchronous(host, self._timers, timeout=timeout))

      # Create the composite action space from the configuration.
      element: ReachElement
      action_space_dict: Dict[str, gyms_core.Space] = {}
      config_names: Set[str] = set()
      config_name: str
      for config_name, element in pyreach_config.items():
        element.set_task_params(task_params)
        if not config_name:
          raise pyreach.PyReachError("Configuration name must be non empty")
        if config_name in config_names:
          raise pyreach.PyReachError(
              "Duplicate configuration name '{0}'".format(config_name))
        config_names.add(config_name)
        element._config_name = config_name
        element.set_timers(self._timers)

        is_synchronous: bool = element.is_synchronous
        if is_synchronous:
          reach_synchronous._register_element(element)

        element_action_space: Optional[gyms_core.Space] = element.action_space
        is_action_space: bool = element_action_space is not None
        if is_action_space:
          action_space_dict[config_name] = element_action_space

        logging.info("Element: %15s synchronous=%d action=%d", config_name,
                     int(is_synchronous), int(is_action_space))
      action_space: gyms_core.Space = gym.spaces.Dict(action_space_dict)

      # Create the composite observation space from the configuration.
      observation_space_dict: Dict[str, gyms_core.Space] = {}
      for name, element in pyreach_config.items():
        element_observation_space: Optional[gyms_core.Space] = (
            element.observation_space)
        if element_observation_space is not None:
          observation_space_dict[name] = element_observation_space

      observation_space: gyms_core.Space = gym.spaces.Dict(
          observation_space_dict)
      observation_space_names: Set[str] = set(observation_space_dict.keys())
      if config_names != observation_space_names:
        raise pyreach.PyReachError(
            "Internal Error: incomplete observation space "
            f"{config_names} != {observation_space_names}")

      # A top level gym.Env requires these 4 fields.
      self._action_space: gyms_core.Space = action_space
      self._observation_space: gyms_core.Space = observation_space
      self._metadata: Dict[str, Any] = {}  # Explicitly for agent debugging
      self._reach_synchronous = reach_synchronous
      self._reward_range: Tuple[float, float] = (-float("inf"), float("inf"))
      self._pyreach_config: Dict[str, ReachElement] = pyreach_config
      self._episode = 0
      self._step = 0
      self._host = host
      self._reward_done_function: gyms_core.RewardDoneFunction = (
          self._nop_reward_done_function)
      self._task_started: bool = False
      self.task_params = task_params

      # Allow overwride of reward/done/info function from kwargs.
      if "reward_done_function" in kwargs:
        self._reward_done_function = kwargs["reward_done_function"]

  @staticmethod
  def _nop_reward_done_function(
      action: gyms_core.Action,
      observation: gyms_core.Observation) -> Tuple[float, bool]:
    """Do nothing reward/done/info function."""
    return 0.0, False

  def step(
      self, action: gyms_core.Action
  ) -> Tuple[gyms_core.Observation, float, bool, Any]:
    """Perform one Gym step.

    Args:
      action: The Gym action Space as Gym Dict Space.

    Returns:
      A 4-tuple of:
        observation: The next observation as a Gym Dict Space.
        reward: A the reward value as a float.
        done: A boolean that is True if the episode is done.
        info: Some miscellaneous information for debugging.

    """
    action_list: List[lib_snapshot.SnapshotGymAction] = []
    with self._timers.select({"!agent*", "gym.step"}):
      if not self._task_started:
        self._host.logger.start_task(self.task_params)
        action_list.append(
            lib_snapshot.SnapshotGymLoggerAction("operator", "", False, True,
                                                 self.task_params),)
        self._task_started = True

      # Perform the actual action for each sub device.
      with self._timers.select({"gym.action"}):
        assert isinstance(action, Dict)
        pyreach_config: Dict[str, ReachElement] = self._pyreach_config
        name: str
        element: ReachElement
        for name, element in pyreach_config.items():
          if name in action:
            action_list.extend(element.do_action(action[name], self._host))

      # Get the next observation.
      observation: Dict[str, gyms_core.Observation]
      snapshot_references: Tuple[lib_snapshot.SnapshotReference, ...]
      snapshot_responses: Tuple[lib_snapshot.SnapshotResponse, ...]
      observation, snapshot_references, snapshot_responses = (
          self._get_observation(self._host))

      # Compute and reward/done return values.
      reward: float
      done: bool
      reward, done = self._reward_done_function(action, observation)

      # Snapshot the observation here.
      self._step += 1

      snapshot: lib_snapshot.Snapshot = lib_snapshot.Snapshot(
          source="pyreach_gym",
          device_data_refs=tuple(snapshot_references),
          responses=tuple(snapshot_responses),
          gym_env_id=self._gym_env_id,
          gym_run_id=self._run_id,
          gym_episode=self._episode,
          gym_step=self._step,
          gym_reward=reward,
          gym_done=done,
          gym_actions=tuple(action_list))
      self._host.logger.send_snapshot(snapshot)

      return observation, reward, done, {}

  def reset(self) -> gyms_core.Observation:
    """Reset for a new episode and return an initial observation.

    Returns:
      Returns the next Gym Observation as a Gym Dict Space.
    """
    with self._timers.select({"!agent*", "gym.reset"}):
      action_list: List[lib_snapshot.SnapshotGymAction] = []
      oracle: Optional[ReachOracle] = None
      text_instructions: Optional[ReachTextInstructions] = None
      element: ReachElement
      for element in self._pyreach_config.values():
        if isinstance(element, ReachOracle):
          oracle = element
        if isinstance(element, ReachTextInstructions):
          text_instructions = element

      if text_instructions:
        if text_instructions.task_enable == 1:
          action_list.extend(text_instructions.end_task(self._host))
          if oracle:
            oracle.end_task()

      self._host.reset()
      self.task_params["reset_id"] = str(uuid.uuid4())

      # Do element specific waiting for reset.
      for element in self._pyreach_config.values():
        element.reset_wait(self._host)

      observation: Dict[str, gyms_core.Observation]
      snapshot_references: Tuple[lib_snapshot.SnapshotReference, ...]
      snapshot_responses: Tuple[lib_snapshot.SnapshotResponse, ...]
      observation, snapshot_references, snapshot_responses = self._get_observation(
          self._host)

      self._episode += 1
      self._step = 0
      snapshot: lib_snapshot.Snapshot = lib_snapshot.Snapshot(
          source="pyreach_gym",
          device_data_refs=tuple(snapshot_references),
          responses=tuple(snapshot_responses),
          gym_env_id=self._gym_env_id,
          gym_run_id=self._run_id,
          gym_episode=self._episode,
          gym_step=self._step,
          gym_reward=0.0,
          gym_done=False,
          gym_actions=tuple(action_list))
      self._host.logger.send_snapshot(snapshot)

      if not isinstance(observation, dict):
        raise pyreach.PyReachError("Internal Error: non-dictionary observation")

      return observation

  def _get_observation(
      self, host: pyreach.Host
  ) -> Tuple[Dict[str, gyms_core.Observation], Tuple[
      lib_snapshot.SnapshotReference, ...], Tuple[lib_snapshot.SnapshotResponse,
                                                  ...]]:
    """Return the latest observation for the ReachEnv.

    Args:
      host: The reach host to use.

    Returns:
      The a tuple of next Gym Observation as Gym Dict Space and
      the snapshot references.

    """
    with self._timers.select({"!agent*", "gym.obs"}):
      # Wait for synchronous elements to respond.
      reach_synchronous: ReachSynchronous = self._reach_synchronous
      observations: Dict[str, gyms_core.Observation] = {}
      reach_synchronous.start_observations(host)
      latest_ts: float
      snapshot_references: List[lib_snapshot.SnapshotReference]
      snapshot_responses: List[lib_snapshot.SnapshotResponse]
      latest_ts, snapshot_references, snapshot_responses = (
          reach_synchronous.synchronize_observations(observations))

      element_names: Set[str] = set(reach_synchronous.elements.keys())
      observation_names: Set[str] = set(observations.keys())
      if observation_names != element_names:
        raise pyreach.PyReachError(
            "Internal Error: observations({0}) != synchronous_elements({1})"
            .format(observation_names, element_names))

      # Collect the non-synchronous observations:
      pyreach_config: Dict[str, ReachElement] = self._pyreach_config
      name: str
      element: ReachElement
      for name, element in pyreach_config.items():
        if not element.is_synchronous:
          observation: gyms_core.Observation
          references: Tuple[lib_snapshot.SnapshotReference, ...]
          responses: Tuple[lib_snapshot.SnapshotResponse, ...]
          observation, references, responses = element.get_observation(
              self._host)
          snapshot_references.extend(references)
          snapshot_responses.extend(responses)
          observations[name] = observation
          if isinstance(observation, dict) and "ts" in observation:
            latest_ts = max(latest_ts, float(observation["ts"]))

      if "server" in observations:
        server_observation: gyms_core.Observation = observations["server"]
        if isinstance(server_observation, dict):
          if "latest_ts" in server_observation:
            server_observation["latest_ts"] = gyms_core.Timestamp.new(latest_ts)

      element_names = set(pyreach_config.keys())
      observation_names = set(observations.keys())
      if element_names != observation_names:
        raise pyreach.PyReachError(
            "Internal error: elements({0}) != observation_names({1})".format(
                element_names, observation_names))

      return observations, tuple(snapshot_references), tuple(snapshot_responses)

  def set_reward_done_function(
      self, reward_done_function: gyms_core.RewardDoneFunction) -> None:
    """Set the reward/done function.

    Args:
      reward_done_function: Override of the default reward function. (See
        compute_reward()) for arguments.
    """
    self._reward_done_function = reward_done_function

  def render(self, mode: str = "human") -> None:
    """Render the current state."""
    pass

  def close(self) -> None:
    """Close the Reach Gym environment."""
    super().close()
    pyreach_config: Dict[str, ReachElement] = self._pyreach_config
    text_instructions: Optional[ReachTextInstructions] = None
    oracle: Optional[ReachOracle] = None
    element: ReachElement
    for element in pyreach_config.values():
      if isinstance(element, ReachTextInstructions):
        text_instructions = element
      if isinstance(element, ReachOracle):
        oracle = element

    if text_instructions:
      if text_instructions.task_enable == 1:
        text_instructions.end_task(self._host)
        if oracle:
          oracle.disable_tagged_request()
      text_instructions.task_enable = -1
    self._host.close()
    self._timers.dump()

  def fk(self,
         element: str,
         joints: Union[Tuple[float, ...], List[float], np.ndarray],
         apply_tip_adjust_transform: bool = False) -> Optional[pyreach.Pose]:
    """Uses forward kinematics to get the pose from the joint angles.

    Args:
      element: The name of the arm element.
      joints: The robot joints.
      apply_tip_adjust_transform: If True, will use the data in the calibration
        file for the robot to change the returned pose from the end of the arm
        to the tip of the end-effector.

    Returns:
      The pose for the end of the arm, or if apply_tip_adjust_transform was
      set to True, the pose for the tip of the end-effector. If the IK library
      was not yet initialized, this will return None.
    """
    arm = self._pyreach_config.get(element)
    if arm is None or not isinstance(arm, ReachArm):
      return None
    return arm.fk(self._host, joints, apply_tip_adjust_transform)

  def set_agent_id(self, agent_id: str) -> None:
    """Sets the agent ID for the environment.

    This must be called before calling reset(). This will differentiate
    between logs in the same environment but for different agents.

    Args:
      agent_id: The name of the agent to mark logs with.
    """
    self.task_params["agent_id"] = agent_id


if __name__ == "__main__":
  pass
