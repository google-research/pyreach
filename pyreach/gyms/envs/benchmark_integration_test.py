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

"""Benchmark environment for benchmark integration testing."""

import collections
import time
from typing import Tuple, Any, Dict, List
import gym  # type: ignore
import numpy as np  # type: ignore

from pyreach.gyms import core
from pyreach.gyms import reach_env


class BenchmarkIntegrationEnv(reach_env.ReachEnv):  # type: ignore
  """Benchmark integration testing environment."""

  def __init__(self, **kwargs: Any) -> None:
    """Initialize the Singulation environment."""
    center_joint_angles: List[float] = [3.06, -1.66, -1.57, -1.10, 1.7, 0.0]
    low_joint_angles: Tuple[float, ...] = tuple(
        [cja - 5.0 for cja in center_joint_angles])
    high_joint_angles: Tuple[float, ...] = tuple(
        [cja + 5.0 for cja in center_joint_angles])

    task_params: Dict[str, str] = {
        "task-code": "9999999999",
    }

    pyreach_config: Dict[str, reach_env.ReachElement] = {
        "arm":
            reach_env.ReachArm(
                "", low_joint_angles, high_joint_angles, is_synchronous=True),
        # pylint: disable=g-bad-todo
        # TODO: These should be re-enabled and checked that there
        # is an observation in there.
        # "camera":
        #     reach_env.ReachColorCamera("", (576, 1024), is_synchronous=True),
        # "depth_camera":
        #     reach_env.ReachDepthCamera(
        #         "", (720, 1280), True, is_synchronous=True),
        "server":
            reach_env.ReachServer("Server"),
        "text_instructions":
            reach_env.ReachTextInstructions("instruction-generator"),
    }

    super().__init__(
        pyreach_config=pyreach_config, task_params=task_params, **kwargs)

  def step(self,
           action: core.Action) -> Tuple[core.Observation, float, bool, Any]:
    """Perform one step."""
    observation: core.Observation
    reward: float
    done: bool
    info: Any

    observation, reward, done, info = super().step(action)

    if done:
      observation, _, _, info = self._ask_for_new_instruction(observation)
      return (observation, reward, done, info)

    return (observation, reward, done, info)

  def _ask_for_new_instruction(
      self, current_observation: core.Observation
  ) -> Tuple[core.Observation, float, bool, Any]:
    """Asks for a new instruction.

    If we time out waiting for a new instruction, that means that
    we have completed all instructions, and we return None,
    otherwise we return the latest observation.

    Args:
      current_observation: the current observation.

    Returns:
      The observation when the instruction is received.
    """
    print(f"{time.time()}: Asking for a new text instruction")

    # End current task
    action = collections.OrderedDict(
        {"text_instructions": collections.OrderedDict({"task_enable": 0})})

    _, _, _, _ = super().step(action)

    # Start new task
    action = collections.OrderedDict(
        {"text_instructions": collections.OrderedDict({"task_enable": 1})})
    return super().step(action)

  def reset(self) -> core.Observation:
    """Resets the benchmark.

    On SIM, this resets the scene and returns an observation. On real, it only
    returns an observation.

    Returns:
      Initial observation.
    """

    # End any current task
    action = collections.OrderedDict(
        {"text_instructions": collections.OrderedDict({"task_enable": 0})})
    _, _, _, _ = super().step(action)
    obs = super().reset()

    # Start a new task
    action = collections.OrderedDict(
        {"text_instructions": collections.OrderedDict({"task_enable": 1})})
    obs, _, _, _ = super().step(action)

    return obs


class BenchmarkIntegrationWrapper(gym.Wrapper):
  """A wrapper for the Benchmark integration testing environment.

  This environment is a stripped-down environment which provides actions for
  moves of joints only.

  == Actions ==

  action["arm"]:
    "joint_angles":
        # The joints to move to, in radians.
        gym.spaces.Box(
            low=np.array((-6.283, -2.059, -3.926, -3.141, 1.692, -6.283)),
            high=np.array((6.283, 2.094, 0.191, 3.141, 3.141, 6.283)),
            dtype=np.dtype(float)),

  == Observations ==

    No filters! See BenchmarkIntegrationEnv!
  """

  def __init__(self, env: BenchmarkIntegrationEnv) -> None:
    super().__init__(env)

    self.env = env

    self.action_space: core.Space = gym.spaces.Dict({
        "arm":
            gym.spaces.Dict({
                "joint_angles": self.env.action_space["arm"]["joint_angles"],
            })
    })
    self.observation_space: core.Space = self.env.observation_space

  def step(self,
           action: core.Action) -> Tuple[core.Observation, float, bool, Any]:
    assert isinstance(action, (dict, collections.OrderedDict))
    arm: Any = action["arm"]
    assert isinstance(arm, (dict, collections.OrderedDict))
    pose: Any = arm["joint_angles"]
    assert isinstance(pose, np.ndarray)
    new_action = {
        "arm": {
            "command": 1,
            "joint_angles": action["arm"]["joint_angles"],
        },
    }

    return self.env.step(new_action)
