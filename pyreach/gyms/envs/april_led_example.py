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
"""A basic environment for toggling an AprilLED."""

import time

from typing import Any, Dict, Tuple
from pyreach.gyms import core as gyms_core
from pyreach.gyms import io_element
from pyreach.gyms import reach_env


class PyReachAprilLEDExampleEnv(reach_env.ReachEnv):
  """An OpenAI PyReach Gym Example Environment."""

  def __init__(self, **kwargs: Any):
    """Initialize the Singulation environment."""

    print("=>PyReachAprilLEDExample.__init()")
    pyreach_config = {
        "io":
            io_element.ReachIO(
                reach_name="april-led",
                is_synchronous=True,
                digital_outputs={
                    "gym-april-led":
                        io_element.ReachIODigitalOutput(
                            reach_name="april-led",
                            capability_type="april-led",
                            pin_name="")
                }),
        "server":
            reach_env.ReachServer("Server"),
    }
    if "robot_types" not in kwargs:
      kwargs["robot_types"] = {}
    kwargs["robot_types"]["april-led"] = "april-led.urdf"
    print("=>ReachEnv.__init__()")
    super().__init__(
        pyreach_config=pyreach_config, task_params={}, timeout=15.0, **kwargs)
    print("<=ReachEnv.__init__()")
    print("<=PyReachAprilLEDExample.__init()")

    self._led_state = True

  def reset(self) -> gyms_core.Observation:
    """Resets the environment."""
    self._led_state = True
    observation: gyms_core.Observation = super().reset()
    print(f"{time.time():.4f}: Reset called.")
    return observation

  def step(
      self, action: gyms_core.Action
  ) -> Tuple[gyms_core.Observation, float, bool, Any]:
    """Perform one step."""
    time.sleep(1.0)
    self._led_state = not self._led_state
    observation: gyms_core.Observation
    reward: float
    done: bool
    info: Dict[str, Any]
    action = {
        "io": {
            "digital_outputs": {
                "gym-april-led": int(self._led_state),
            },
        },
    }
    observation, reward, done, info = super().step(action)
    print(f"{time.time():.4f}: Step called: led_state={self._led_state}.")
    return observation, reward, done, info
