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

"""Implementation of PyReach Gym Arm Device."""

import copy
import dataclasses
import logging
import sys
import threading
import time
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

import gym  # type: ignore
import numpy as np  # type: ignore

import pyreach
from pyreach import arm as pyreach_arm
from pyreach import core
from pyreach import snapshot as lib_snapshot
from pyreach.gyms import arm_element
from pyreach.gyms import core as gyms_core
from pyreach.gyms.devices import reach_device

IKLibType = pyreach.arm.IKLibType


class ReachDeviceArm(reach_device.ReachDevice):
  """Represents a Reach Arm.

  Attributes:
    action_space: A Gym action space represented as a Gym Dict Space with
      "command", "joint_angles", "pose", "synchronous", "id", "controller"
      and "command" should be 0 for do nothing, 1 for set joint angles and 2
      for set pose. "joint_angles" should be the desired joint angles in
      radians. "pose" should be the desired arm pose. "synchronous" is only
      valid when the arm is configured as asynchronous. When set to 1, a
      synchronous move is performed. When set to 0 (or not present), an
      asynchronous move occurs.  "id" is used to keep track of asynchronous
      move status. When id is present and positive, each asynchronous move
      can be given a unique id (simple counter bumping adequate) to keep
      track of the returned status for the move.  The most recent returned
      statuses are put into the "responses" portion of the arm observation.
    observation_space: A Gym observation space represented as a Gym Dict Space
      with "ts", "joint_angles", and "pose" fields.
  """

  def __init__(self, arm_config: arm_element.ReachArm) -> None:
    """Initialize a Reach Arm.

    Args:
      arm_config: An arm configuration.
    """
    reach_name: str = arm_config.reach_name
    low_joint_angles: Tuple[float, ...] = arm_config.low_joint_angles
    high_joint_angles: Tuple[float, ...] = arm_config.high_joint_angles
    apply_tip_adjust_transform: bool = arm_config.apply_tip_adjust_transform
    is_synchronous: bool = arm_config.is_synchronous
    response_queue_length: int = arm_config.response_queue_length
    controllers: Tuple[str, ...] = arm_config.controllers
    ik_lib: Optional[str] = arm_config.ik_lib
    e_stop_mode: int = arm_config.e_stop_mode
    p_stop_mode: int = arm_config.p_stop_mode
    # For unit testing only.
    test_states: Optional[List[pyreach_arm.ArmState]] = arm_config.test_states
    if not test_states:
      test_states = []

    if not controllers:
      raise pyreach.PyReachError("At least one controller must be specified")
    if response_queue_length < 0:
      raise pyreach.PyReachError(
          "response length queue must be non-negative: {0}".format(
              response_queue_length))

    action_dict: Dict[str, gyms_core.Action] = {
        "command":
            gym.spaces.Discrete(4),
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
        "controller":
            gym.spaces.Discrete(len(controllers))
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
            gym.spaces.Discrete(arm_element.ReachResponse.RESPONSE_MAX + 1),
    }
    if response_queue_length:
      response_space: gym.spaces.Dict = gym.spaces.Dict({
          "ts":
              gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
          "id":
              gym.spaces.Discrete(1 << 30),
          "status":
              gym.spaces.Discrete(arm_element.ReachResponse.RESPONSE_MAX + 1),
          "finished":
              gym.spaces.Discrete(2),
      })
      observation_dict["responses"] = gym.spaces.Tuple(
          (response_space,) * response_queue_length)
    observation_space: gym.spaces.Dict = gym.spaces.Dict(observation_dict)

    super().__init__(reach_name, action_space, observation_space,
                     is_synchronous)
    self._arm: Optional[pyreach.Arm] = None
    self._arm_state_capturer: _ArmStateCapturer = _ArmStateCapturer()
    self._controllers: Tuple[str, ...] = controllers
    self._early_done: bool = False
    self._high_joint_angles: Tuple[float, ...] = high_joint_angles
    self._low_joint_angles: Tuple[float, ...] = low_joint_angles
    self._joints: np.ndarray = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    self._pose: np.ndarray = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
    self._pyreach_status: Optional[pyreach.PyReachStatus] = None
    self._response_queue_length: int = response_queue_length
    self._apply_tip_adjust_transform: bool = apply_tip_adjust_transform
    self._last_command: int = 0
    self._ik_lib: Optional[str] = ik_lib
    self._e_stop_mode: int = e_stop_mode
    self._p_stop_mode: int = p_stop_mode

  def __str__(self) -> str:
    """Return string representation of Arm."""
    return "ReachDeviceArm('{0}':'{1}')".format(self.config_name,
                                                self._reach_name)

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

  def get_early_done(self) -> bool:
    """Return an early Done flag.

    Returns:
        Return True when the arm to shut done Gym session immediately.
    """
    return self._early_done

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

  def get_observation(self,
                      host: pyreach.Host) -> reach_device.ObservationSnapshot:
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
        response = arm_element.ReachResponse.RESPONSE_NONE
        responses.append(
            lib_snapshot.SnapshotResponse(
                0, "arm", self.config_name,
                lib_snapshot.SnapshotReference(0.0, 0)))
      else:
        # Get last cached value ArmState, which should be good enough to figure
        # out if either E-Stop or P-Stop has occurred.
        # Snapshot this?
        responses.append(
            lib_snapshot.SnapshotResponse(0, "arm", self.config_name,
                                          pyreach_status))
        status: str = pyreach_status.status
        error: str = pyreach_status.error
        if status == "done":
          if error == "timeout":
            response = arm_element.ReachResponse.RESPONSE_TIMEOUT
          elif error:
            response = arm_element.ReachResponse.RESPONSE_FAILED
          else:
            response = arm_element.ReachResponse.RESPONSE_DONE
        elif status == "aborted":
          response = arm_element.ReachResponse.RESPONSE_ABORTED
        else:
          logging.warning("Internal Error: Unexpected response '%s' '%s'",
                          status, error)
          response = arm_element.ReachResponse.RESPONSE_FAILED
        if not 0 <= response <= arm_element.ReachResponse.RESPONSE_MAX:
          raise pyreach.PyReachError(
              f"Internal Error: Bad Arm response {response}")

      arm_state: Optional[pyreach.ArmState]
      with self._timers.select({"!agent*", "!gym*", "host.arm.state"}):
        arm_state = arm.fetch_state() if self._is_synchronous else arm.state()

      if arm_state is not None:
        # Deal with E-stop and P-Stop.
        if arm_state.is_emergency_stopped:
          e_stop_mode: int = self._e_stop_mode
          if e_stop_mode == arm_element.ReachStopMode.STOP_ERROR:
            raise pyreach.PyReachError("Robot is in Protective-Stop mode")
          response = arm_element.ReachResponse.RESPONSE_ESTOP
          if e_stop_mode == arm_element.ReachStopMode.STOP_DONE:
            self._early_done = True

        if arm_state.is_protective_stopped:
          p_stop_mode: int = self._p_stop_mode
          if p_stop_mode == arm_element.ReachStopMode.STOP_ERROR:
            raise pyreach.PyReachError("Robot is in Protective-Stop mode")
          if p_stop_mode == arm_element.ReachStopMode.STOP_DONE:
            response = arm_element.ReachResponse.RESPONSE_PSTOP
            self._early_done = True
          else:
            response = arm_element.ReachResponse.RESPONSE_PSTOP

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

    Digs through the _ArmStateCapturer state and returns a Gym observation
    that contains the most recent N arm states. N is set by the
    response queue length specified at configuration time. Old information
    is culled from _ArmStateCapturer.
    """
    response_queue_length: int = self._response_queue_length
    response_spaces: Tuple[gyms_core.Observation, ...] = ()
    arm_state_capturer: _ArmStateCapturer = self._arm_state_capturer
    with self._timers.select({"!agent*", "!gym*", "host.arm.status"}):
      storage: Dict[int, _ArmResponse] = arm_state_capturer.get_storage()

    arm_response: _ArmResponse
    action_id: int
    done: bool

    active_ids: Dict[int, List[_ArmResponse]] = {}
    for arm_response in storage.values():
      action_id = arm_response.action_id
      if action_id not in active_ids:
        active_ids[action_id] = []
      active_ids[action_id].append(arm_response)

    def get_timestamp(arm_responses: List[_ArmResponse]) -> float:
      """Returns the timestamp for an _ArmResponse list.

      Args:
          arm_responses: The list to get the timestamp from.

      Returns:
          The timestamp of the first element in the list.

      Assumes _ArmResponses are presorted with highest timestamp first.
      """
      return arm_responses[0].timestamp

    arm_responses_list: List[List[_ArmResponse]] = list(active_ids.values())
    arm_responses_list.sort(key=get_timestamp, reverse=True)
    arm_responses_list = arm_responses_list[:response_queue_length]
    arm_responses_list_size: int = len(arm_responses_list)

    responses: List[lib_snapshot.SnapshotResponse] = []

    index: int
    active_counts: Set[int] = set()
    for index in range(response_queue_length):
      timestamp: float = 0.0
      action_id = 0
      status: int = arm_element.ReachResponse.RESPONSE_NONE
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
      if not (isinstance(command, int) and (0 <= command <= 3)):
        raise pyreach.PyReachError("Invalid arm command -- must be 0 - 3")

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
      controller_index: int = action_dict.get("controller", 0)
      controllers: Tuple[str, ...] = self._controllers
      controller_size: int = len(controllers)
      if not 0 <= controller_index < controller_size:
        raise pyreach.PyReachError(
            f"Invalid controller index (={controller_index}) is too big; "
            f"it must be less than {controller_size}")
      controller_name: str = controllers[controller_index]
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
        raise pyreach.PyReachError("id is required for non-synchronous moves")
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
      finished_callback: Optional[reach_device.FinishedCallback]

      if command == 0:
        # Do nothing
        return (lib_snapshot.SnapshotGymArmAction(
            device_type="robot",
            device_name=arm.device_name,
            command=command,
            controller_name=controller_name,
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
            controller_name=controller_name,
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
                    controller_name=controller_name,
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
              controller_name=controller_name,
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
            controller_name=controller_name,
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
                controller_name=controller_name,
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
              controller_name=controller_name,
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

      if command == 3:
        # Stop the arm:

        cmd_tuple = (lib_snapshot.SnapshotGymArmAction(
            device_type="robot",
            device_name=arm.device_name,
            cid=action_id,
            command=command,
            controller_name=controller_name,
            velocity=velocity,
            acceleration=acceleration,
            timeout_sec=timeout if timeout else 0.0,
            synchronous=self._is_synchronous or synchronous),)
        if self._is_synchronous or synchronous:
          with self._timers.select({"!agent*", "!gym*", "host.arm.stop"}):
            arm.stop(deceleration=acceleration, preemptive=True)
        else:
          arm.async_stop(deceleration=acceleration, preemptive=True)
        return cmd_tuple

      raise pyreach.PyReachError(
          f"Invalid Arm command {command} (must be 0, 1, 2, or 3)")

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
class _ArmResponse:
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


class _ArmStateCapturer(object):
  """A class to keep track of asynchronous ArmState responses."""

  def __init__(self) -> None:
    """Initializes the ArmState object."""
    self._lock = threading.Lock()
    self._counter: int = 0
    self._storage: Dict[int, _ArmResponse] = {}

  def start(self, action_id: int) -> int:
    """Starts a new arm state."""
    with self._lock:
      assert action_id >= 0
      self._counter += 1
      self._storage[self._counter] = _ArmResponse(
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
        arm_response: _ArmResponse = self._storage[count]
        timestamp: float = arm_response.timestamp
        action_id: int = arm_response.action_id
        done: bool = arm_response.done
        arm_response = _ArmResponse(timestamp, count, action_id, done, status)
        self._storage[count] = arm_response

  def finished_callback(self, count: int) -> None:
    """Finished callback for an ArmState."""
    with self._lock:
      if count in self._storage:
        arm_response: _ArmResponse = self._storage[count]
        timestamp: float = arm_response.timestamp
        action_id: int = arm_response.action_id
        status: Optional[pyreach.PyReachStatus] = arm_response.status
        arm_response = _ArmResponse(timestamp, count, action_id, True, status)
        self._storage[count] = arm_response

  def get_storage(self) -> Dict[int, _ArmResponse]:
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
