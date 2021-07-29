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

"""A basic singulation Gym environment used as an example."""

from typing import Any, Dict, List, Tuple

from pyreach.gyms import reach_env


class PyReachGymExampleEnv(reach_env.ReachEnv):
  """An OpenAI PyReach Gym Example Environment."""

  def __init__(self, **kwargs: Any):
    """Initialize the Singulation environment."""
    center_joint_angles: List[float] = [5.06, -1.66, -1.57, -1.10, 1.7, 0.0]
    low_joint_angles: Tuple[float, ...] = tuple(
        [cja - 0.1 for cja in center_joint_angles])
    high_joint_angles: Tuple[float, ...] = tuple(
        cja + 0.1 for cja in center_joint_angles)
    timeout: float = 15.0

    pyreach_config: Dict[str, reach_env.ReachElement] = {
        "arm":
            reach_env.ReachArm(
                "", low_joint_angles, high_joint_angles, is_synchronous=True),
        "camera":
            reach_env.ReachColorCamera(
                "", (772, 1032), force_fit=True, is_synchronous=True),
        "depth_camera":
            reach_env.ReachDepthCamera(
                "", (720, 1280), True, force_fit=True, is_synchronous=True),
        "server":
            reach_env.ReachServer("Server"),
        "text_instruction":
            reach_env.ReachTextInstructions("text", is_synchronous=True),
        "vacuum":
            reach_env.ReachVacuum(""),
    }

    task_params: Dict[str, str] = {
        "task_code": "122",
        "intent": "pick",
        "success_type": "vacuum-pressure-sensor"
    }

    super().__init__(
        pyreach_config=pyreach_config,
        task_params=task_params,
        timeout=timeout,
        **kwargs)
