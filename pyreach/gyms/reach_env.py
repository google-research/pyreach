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

from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import gym  # type: ignore
import numpy as np  # type: ignore

import pyreach
from pyreach import snapshot as lib_snapshot
from pyreach.gyms import core as gyms_core
from pyreach.gyms.arm_element import ReachArm  # pylint: disable=unused-import
from pyreach.gyms.color_camera_element import ReachColorCamera  # pylint: disable=unused-import
from pyreach.gyms.depth_camera_element import ReachDepthCamera  # pylint: disable=unused-import
from pyreach.gyms.force_torque_sensor_element import ReachForceTorqueSensor  # pylint: disable=unused-import
from pyreach.gyms.impl import mirror_reach_env
from pyreach.gyms.oracle_element import ReachOracle  # pylint: disable=unused-import
from pyreach.gyms.reach_element import ReachElement
from pyreach.gyms.server_element import ReachServer  # pylint: disable=unused-import
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
    metadata: An initially empty Dict of Any's.  This is available for user
      debugging.
    reward_range: Specifies maximum and minimum value for rewards as a two
      floats in a tuple.
  """

  @property
  def action_space(self) -> gyms_core.Space:
    """Return the action space."""
    return self._gym_mirror.action_space

  @property
  def observation_space(self) -> gyms_core.Space:
    """Return the observation space."""
    return self._gym_mirror.observation_space

  @property
  def reward_range(self) -> Tuple[float, float]:
    """Return the reward range."""
    return self._gym_mirror.reward_range

  @property
  def metadata(self) -> Dict[str, Any]:
    """Return the meda data dictionary."""
    return self._gym_mirror.metadata

  @property
  def task_params(self) -> Dict[str, str]:
    return self._gym_mirror.task_params

  def __init__(self,
               pyreach_config: Optional[Dict[str, ReachElement]] = None,
               task_params: Optional[Dict[str, str]] = None,
               timeout: Optional[float] = None,
               host: Optional[pyreach.Host] = None,
               gym_env_id: Optional[str] = None,
               **kwargs: Any) -> None:
    """Initialize a Reach Gym Environment.

    Args:
      pyreach_config: A dictionary of named ReachDevices. (Default: {}.)
      task_params: Additional parameters for the task. (Default: {}.)
      timeout: A timeout in seconds to set for synchronous gym. (Default: None.)
      host: A host to use. (Default: None.)
      gym_env_id: ID used to create this gym. Must be specified.
      **kwargs: Additional keyword arguments.

    Raises:
      pyreach.PyReachError for configuration errors.

    """
    super().__init__()
    self._gym_mirror: gym.Env = mirror_reach_env.MirrorReachEnv(
        pyreach_config, task_params, timeout, host, gym_env_id, **kwargs)

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
    return self._gym_mirror.step(action)

  def reset(self) -> gyms_core.Observation:
    """Reset for a new episode and return an initial observation.

    Returns:
      Returns the next Gym Observation as a Gym Dict Space.
    """
    return self._gym_mirror.reset()

  def set_reward_done_function(
      self, reward_done_function: gyms_core.RewardDoneFunction) -> None:
    """Set the reward/done function.

    Args:
      reward_done_function: Override of the default reward function. (See
        compute_reward()) for arguments.
    """
    self._gym_mirror.set_reward_done_function(reward_done_function)

  def render(self, mode: str = "human") -> None:
    """Render the current state."""
    self._gym_mirror.render(mode)

  def close(self) -> None:
    """Close the Reach Gym environment."""
    self._gym_mirror.close()

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
    return self._gym_mirror.fk(element, joints, apply_tip_adjust_transform)

  def set_agent_id(self, agent_id: str) -> None:
    """Sets the agent ID for the environment.

    This must be called before calling reset(). This will differentiate
    between logs in the same environment but for different agents.

    Args:
      agent_id: The name of the agent to mark logs with.
    """
    self._gym_mirror.set_agent_id(agent_id)


if __name__ == "__main__":
  pass
