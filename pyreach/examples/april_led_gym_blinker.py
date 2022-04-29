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

from typing import Any, Dict, List
from absl import app  # type: ignore
from absl import flags  # type: ignore
import gym  # type: ignore

from pyreach.gyms import core as gyms_core


def main(unused_argv: List[str]) -> None:
  env: Any
  with gym.make("april-led-example-v0") as env:
    print("Perform LED Environment reset.")
    observation: gyms_core.Observation = env.reset()
    _ = observation
    action: Dict[str, Any] = {"digital_outputs": ()}
    done: bool = False
    print("Iteration until step count exceded.")
    while not done:
      print("Do next step")
      observation, _, done, _ = env.step(action)
    print("Exit April LED Environment.")
  print("Closed")


if __name__ == "__main__":
  flags.DEFINE_string(
      "connection_string", None,
      "Connect using a PyReach connection string (see"
      "connections_string.md for examples and documentation")
  app.run(main)
