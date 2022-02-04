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

import logging
import time
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
import uuid

import gym  # type: ignore
import numpy as np  # type: ignore

import pyreach
from pyreach import arm as pyreach_arm
from pyreach import factory
from pyreach import internal
from pyreach import snapshot as lib_snapshot
from pyreach.gyms import annotation_element
from pyreach.gyms import arm_element
from pyreach.gyms import color_camera_element
from pyreach.gyms import constraints_element
from pyreach.gyms import core as gyms_core
from pyreach.gyms import depth_camera_element
from pyreach.gyms import force_torque_sensor_element
from pyreach.gyms import oracle_element
from pyreach.gyms import reach_element
from pyreach.gyms import server_element
from pyreach.gyms import task_element
from pyreach.gyms import text_instructions_element
from pyreach.gyms import vacuum_element
from pyreach.gyms.annotation_element import ReachAnnotation  # pylint: disable=unused-import
from pyreach.gyms.arm_element import ReachArm  # pylint: disable=unused-import
from pyreach.gyms.color_camera_element import ReachColorCamera  # pylint: disable=unused-import
from pyreach.gyms.constraints_element import ReachConstraints  # pylint: disable=unused-import
from pyreach.gyms.depth_camera_element import ReachDepthCamera  # pylint: disable=unused-import
from pyreach.gyms.devices.annotation_device import ReachDeviceAnnotation
from pyreach.gyms.devices.arm_device import ReachDeviceArm
from pyreach.gyms.devices.color_camera_device import ReachDeviceColorCamera
from pyreach.gyms.devices.constraints_device import ReachDeviceConstraints
from pyreach.gyms.devices.depth_camera_device import ReachDeviceDepthCamera
from pyreach.gyms.devices.force_torque_sensor_device import ReachDeviceForceTorqueSensor
from pyreach.gyms.devices.oracle_device import ReachDeviceOracle
from pyreach.gyms.devices.reach_device import ReachDevice
from pyreach.gyms.devices.reach_device import ReachDeviceSynchronous
from pyreach.gyms.devices.server_device import ReachDeviceServer
from pyreach.gyms.devices.task_device import ReachDeviceTask
from pyreach.gyms.devices.text_instructions_device import ReachDeviceTextInstructions
from pyreach.gyms.devices.vacuum_device import ReachDeviceVacuum

from pyreach.gyms.force_torque_sensor_element import ReachForceTorqueSensor  # pylint: disable=unused-import
from pyreach.gyms.oracle_element import ReachOracle  # pylint: disable=unused-import
from pyreach.gyms.reach_element import ReachElement
from pyreach.gyms.server_element import ReachServer  # pylint: disable=unused-import
from pyreach.gyms.task_element import ReachTask  # pylint: disable=unused-import
from pyreach.gyms.text_instructions_element import ReachTextInstructions  # pylint: disable=unused-import
from pyreach.gyms.vacuum_element import ReachVacuum  # pylint: disable=unused-import
from pyreach.gyms.vacuum_element import ReachVacuumState  # pylint: disable=unused-import

TaggedRequest = Tuple[str, str, str, str, str]
Callback = Callable[[Any], bool]
FinishedCallback = Optional[Callable[[], None]]
Stop = Callable[[], None]
AddUpdateCallback = Callable[[Callback, FinishedCallback], Stop]
IKLibType = pyreach.arm.IKLibType
ObservationSnapshot = Tuple[gyms_core.Observation,
                            Tuple[lib_snapshot.SnapshotReference, ...],
                            Tuple[lib_snapshot.SnapshotResponse, ...]]


# ReachEnv:
class ReachEnv(gym.Env):  # type: ignore
  """Reach compatible OpenAI/Gym.

  Attributes:
    action_space: A Gym Dict Space that specifies the entire action Space for
      the environment.  This attribute is read only.
    observation_space: A Gym Dict space that specifies the entire observation
      space for the environment.
    info: An initially empty Dict of Any's.  This is available for user
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
  def info(self) -> Dict[str, Any]:
    """Return the meta data dictionary."""
    return self._info

  @property
  def task_params(self) -> Dict[str, str]:
    return self._task_params

  def __init__(self,
               pyreach_config: Optional[Dict[str, ReachElement]] = None,
               task_params: Optional[Dict[str, str]] = None,
               timeout: Optional[float] = None,
               host: Optional[pyreach.Host] = None,
               gym_env_id: Optional[str] = None,
               connection_string: Optional[str] = None,
               **kwargs: Any) -> None:
    """Initialize a Reach Gym Environment.

    Args:
      pyreach_config: A dictionary of named ReachDevices. (Default: {}.)
      task_params: Additional parameters for the task. (Default: {}.)
      timeout: A timeout in seconds to set for synchronous gym. (Default: None.)
      host: A host to use. (Default: None.)
      gym_env_id: ID used to create this gym. Must be specified.
      connection_string: the connection string (see connection_string.md).
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
        "gym.constraints",
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
        "host.arm.to_joints.async",
        "host.arm.to_joints.sync",
        "host.arm.stop",
        "host.arm.to_pose.async",
        "host.arm.to_pose.sync",
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
      # Verify that task_params is Dict[str, str]:
      key: str
      value: str
      for key, value in task_params.items():
        if not isinstance(key, str):
          raise pyreach.PyReachError(
              "task_params dict has key that is not a str")
        if not isinstance(value, str):
          raise pyreach.PyReachError(
              f"task_params['{key}'] does not specify a str")

      # Prescan pyreach_config for inverse kinematics library selection.
      # It must be determined before connecting to the host..
      arm_default_ik_types: Dict[str, pyreach_arm.IKLibType] = {}
      config_name: str
      config_element: reach_element.ReachElement
      for config_name, config_element in pyreach_config.items():
        if isinstance(config_element, arm_element.ReachArm):
          ik_lib: Optional[pyreach_arm.IKLibType] = config_element.ik_lib
          if not ik_lib:
            # Historically defaults to IKFast.
            ik_lib = pyreach_arm.IKLibType.IKFAST
          arm_default_ik_types[config_element.reach_name] = ik_lib
      host_kwargs: Dict[str, Any] = {
          "enable_streaming": True,
          "arm_default_ik_types": arm_default_ik_types,
      }

      if not host:
        if not connection_string:
          connection_string = ""
        host = factory.ConnectionFactory(
            connection_string=connection_string, **host_kwargs).connect()

      reach_synchronous: ReachDeviceSynchronous = (
          ReachDeviceSynchronous(host, self._timers, timeout=timeout))

      # Create the composite action space from the configuration.
      element: Optional[ReachDevice] = None
      action_space_dict: Dict[str, gyms_core.Space] = {}
      config_names: Set[str] = set()
      arm_elements: List[ReachDeviceArm] = []
      elements: Dict[str, ReachDevice] = {}

      for config_name, config_element in pyreach_config.items():
        if isinstance(config_element, annotation_element.ReachAnnotation):
          element = ReachDeviceAnnotation(config_element)
        elif isinstance(config_element, arm_element.ReachArm):
          element = ReachDeviceArm(config_element)
          arm_elements.append(element)
        elif isinstance(config_element, color_camera_element.ReachColorCamera):
          element = ReachDeviceColorCamera(config_element)
        elif isinstance(config_element, constraints_element.ReachConstraints):
          element = ReachDeviceConstraints(config_element)
        elif isinstance(config_element, depth_camera_element.ReachDepthCamera):
          element = ReachDeviceDepthCamera(config_element)
        elif isinstance(config_element,
                        force_torque_sensor_element.ReachForceTorqueSensor):
          element = ReachDeviceForceTorqueSensor(config_element)
        elif isinstance(config_element, oracle_element.ReachOracle):
          element = ReachDeviceOracle(config_element)
        elif isinstance(config_element, server_element.ReachServer):
          element = ReachDeviceServer(config_element)
        elif isinstance(config_element, task_element.ReachTask):
          element = ReachDeviceTask(config_element)
        elif isinstance(config_element, task_element.ReachTask):
          element = ReachDeviceTask(config_element)
        elif isinstance(config_element,
                        text_instructions_element.ReachTextInstructions):
          element = ReachDeviceTextInstructions(config_element)
        elif isinstance(config_element, vacuum_element.ReachVacuum):
          element = ReachDeviceVacuum(config_element)

        if not isinstance(element, ReachDevice):
          raise pyreach.PyReachError(
              f"Unexpected configuration element {config_name}:{element}")
        elements[config_name] = element

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

      # Validate that each device is correctly configured.
      validation_errors: List[str] = []
      for name, element in elements.items():
        validation_error: str = element.validate(host)
        if validation_error:
          validation_errors.append(f"{name}: {validation_error}")
      if validation_errors:
        raise pyreach.PyReachError(f"Validation Error: "
                                   f"environment:{self.__class__.__name__}: "
                                   f"connection_string={connection_string} "
                                   f"validation_errors={validation_errors}")

      # Register task_synchronize() for devices that need to trigger
      # a global synchronize operation.  All other devices will ignore.
      for element in elements.values():
        assert isinstance(element, ReachDevice), element
        element.set_task_synchronize(self.task_synchronize)

      # Create the composite observation space from the configuration.
      observation_space_dict: Dict[str, gyms_core.Space] = {}
      for name, element in elements.items():
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
      self._info: Dict[str, Any] = {}  # Explicitly for agent debugging
      self._reach_synchronous = reach_synchronous
      self._reward_range: Tuple[float, float] = (-float("inf"), float("inf"))
      self._arm_elements: Tuple[ReachDeviceArm, ...] = tuple(arm_elements)
      self._elements: Dict[str, ReachDevice] = elements
      self._pyreach_config: Dict[str, ReachElement] = pyreach_config
      self._text_instruction: Optional[ReachDeviceTextInstructions] = None
      for element in self._elements.values():
        if isinstance(element, ReachDeviceTextInstructions):
          if self._text_instruction:
            raise pyreach.PyReachError(
                "Can have at most one ReachDeviceTextInstructions "
                "in the gym configuration")
          self._text_instruction = element
      self._episode = 0
      self._step = 0
      self._host = host
      self._reward_done_function: gyms_core.RewardDoneFunction = (
          self._nop_reward_done_function)
      self._task_started: bool = False
      self._task_params: Dict[str, str] = task_params

      # Allow overwride of reward/done/info function from kwargs.
      if "reward_done_function" in kwargs:
        self._reward_done_function = kwargs["reward_done_function"]

      # Synchronize all devices
      for element in self._elements.values():
        element.synchronize()

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
      # Perform the actual action for each sub device.
      with self._timers.select({"gym.action"}):
        assert isinstance(action, Dict)
        elements: Dict[str, ReachDevice] = self._elements
        name: str
        element: ReachDevice
        for name, element in elements.items():
          if name in action:
            action_list.extend(element.do_action(action[name], self._host))

      # Get the next observation.
      observation: Dict[str, gyms_core.Observation]
      snapshot_references: Tuple[lib_snapshot.SnapshotReference, ...]
      snapshot_responses: Tuple[lib_snapshot.SnapshotResponse, ...]
      server_time: float
      observation, snapshot_references, snapshot_responses, server_time = (
          self._get_observation(self._host))

      # Compute and reward/done return values.
      reward: float
      done: bool
      reward, done = self._reward_done_function(action, observation)

      # E-stop and P-stop in the arms can force an early done:
      arm_device: ReachDeviceArm
      for arm_device in self._arm_elements:
        done |= arm_device.get_early_done()

      # Snapshot the observation here.
      self._step += 1

      snapshot: lib_snapshot.Snapshot = lib_snapshot.Snapshot(
          source="pyreach_gym",
          device_data_refs=tuple(snapshot_references),
          responses=tuple(snapshot_responses),
          gym_server_time=server_time,
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
    return self._reach_reset(False)

  def _reach_reset(self, close: bool) -> gyms_core.Observation:
    """Reset for a new episode and return an initial observation.

    Args:
      close: if true, gym is closing.

    Returns:
      Returns the next Gym Observation as a Gym Dict Space.
    """
    with self._timers.select({"!agent*", "gym.reset"}):
      action_list: List[lib_snapshot.SnapshotGymAction] = []

      element: ReachDevice
      for element in self._elements.values():
        action_list.extend(element.reset(self._host))

      observation: Dict[str, gyms_core.Observation] = {}
      snapshot_references: Tuple[lib_snapshot.SnapshotReference, ...] = ()
      snapshot_responses: Tuple[lib_snapshot.SnapshotResponse, ...] = ()
      if close:
        server_time = time.time() + (self._host.get_server_offset_time() or 0.0)
        server_time = round(server_time, 3)
      else:
        self._host.reset()
        self.task_params["reset_id"] = str(uuid.uuid4())

        # Do element specific waiting for reset.
        for element in self._elements.values():
          element.reset_wait(self._host)

        observation, snapshot_references, snapshot_responses, server_time = (
            self._get_observation(self._host))

      self._episode += 1
      self._step = 0
      snapshot: lib_snapshot.Snapshot = lib_snapshot.Snapshot(
          source="pyreach_gym",
          device_data_refs=tuple(snapshot_references),
          responses=tuple(snapshot_responses),
          gym_server_time=server_time,
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
                                                  ...], float]:
    """Return the latest observation for the ReachEnv.

    Args:
      host: The reach host to use.

    Returns:
      The a tuple of next Gym Observation as Gym Dict Space and
      the snapshot references.

    """
    with self._timers.select({"!agent*", "gym.obs"}):
      # Wait for synchronous elements to respond.
      reach_synchronous: ReachDeviceSynchronous
      reach_synchronous = self._reach_synchronous
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
      elements: Dict[str, ReachDevice] = self._elements
      name: str
      element: ReachDevice
      for name, element in elements.items():
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

      server_time = time.time() + (self._host.get_server_offset_time() or 0.0)
      server_time = round(server_time, 3)
      if "server" in observations:
        server_observation: gyms_core.Observation = observations["server"]
        if isinstance(server_observation, dict):
          if "latest_ts" in server_observation:
            server_observation["latest_ts"] = gyms_core.Timestamp.new(latest_ts)
          if "server_ts" in server_observation:
            server_observation["server_ts"] = gyms_core.Timestamp.new(
                server_time)

      element_names = set(elements.keys())
      observation_names = set(observations.keys())
      if element_names != observation_names:
        raise pyreach.PyReachError(
            "Internal error: elements({0}) != observation_names({1})".format(
                element_names, observation_names))

      return observations, tuple(snapshot_references), tuple(
          snapshot_responses), server_time

  def task_synchronize(self) -> None:
    """Synchronize all of the devices."""
    for element in self._elements.values():
      element.synchronize()

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
    self._reach_reset(True)
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
    arm = self._elements.get(element)
    if arm is None or not isinstance(arm, ReachDeviceArm):
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
