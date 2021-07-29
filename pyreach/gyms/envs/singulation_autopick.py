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

"""Initialize singulation autopick Pyreach Gym Environment."""

from typing import Any, Dict, List, Tuple

from pyreach.gyms import core
from pyreach.gyms import reach_env

LEFT_BIN = 1
RIGHT_BIN = 2
UNSET = 0


class SingulationAutopickEnv(reach_env.ReachEnv):  # type: ignore
  """OpenAI Gym Reach Environment for the singulation autopicking agent."""

  def __init__(self, **kwargs: Any) -> None:
    """Initialize the Singulation environment."""
    center_joint_angles: List[float] = [3.06, -1.66, -1.57, -1.10, 1.7, 0.0]
    low_joint_angles: Tuple[float, ...] = tuple(
        [cja - 5.0 for cja in center_joint_angles])
    high_joint_angles: Tuple[float, ...] = tuple(
        [cja + 5.0 for cja in center_joint_angles])
    self._bin: int = UNSET

    task_params: Dict[str, str] = {
        "task-code": "110",
        "intent": "pick",
        "success_type": "vacuum-pressure-sensor"
    }

    pyreach_config: Dict[str, reach_env.ReachElement] = {
        "arm":
            reach_env.ReachArm("", low_joint_angles, high_joint_angles),
        "camera":
            reach_env.ReachColorCamera("", (576, 1024), is_synchronous=True),
        "depth_camera":
            reach_env.ReachDepthCamera(
                "", (720, 1280), True, is_synchronous=True),
        "oracle":
            reach_env.ReachOracle(
                "oracle",
                task_params["task-code"],
                task_params["intent"],
                task_params["success_type"],
                is_synchronous=True),
        "server":
            reach_env.ReachServer("Server"),
        "vacuum":
            reach_env.ReachVacuum(""),
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

    return (observation, reward, done, info)

  def switch_bins(self) -> int:
    """Switch between bins."""
    if self._bin == UNSET or self._bin == RIGHT_BIN:
      self._bin = LEFT_BIN
    else:
      self._bin = RIGHT_BIN
    return self._bin
