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
"""Example of PyReach singulation autopicking agent."""

import collections
import logging
from typing import Dict, List, Tuple

from absl import app  # type: ignore
from absl import flags  # type: ignore
import gym  # type: ignore
import numpy as np

from pyreach.gyms import core


# To control the reward, done returns from the step method,
# provide a function computes those value from the action and observation.
# Pass this to the gym.make function when making a new environment.
# pylint: disable=unused-argument
def singulation_reward_function(
    action: core.Action, observation: core.Observation) -> Tuple[float, bool]:
  """Place holder reward/done function."""
  assert isinstance(observation, dict)
  if "oracle" in observation:
    if "pick_point" in observation["oracle"]:
      pick_point_chosen: np.ndarray = observation["oracle"]["pick_point"]
      metric: int = observation["oracle"]["response"]
      bogus_pick_point: np.ndarray = np.array([-1.0, -1.0])
      if np.array_equal(pick_point_chosen, bogus_pick_point):
        if metric == 0:
          # No pick point and no response: reached the end of a bin.
          return 3.0, True
        # No pick point but got metrics should never happen -
        # indicates something wrong.
        return -1.0, False
      if np.any(pick_point_chosen) and metric != 0:
        # Valid pick point and proper metrics: return the metric value
        return float(metric), False
  # All other cases indicate something going wrong.
  return -1.0, False


def main(unused_argv: List[str]) -> None:
  logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Starting")
  with gym.make(
      "singulation-autopick-v0",
      reward_done_function=singulation_reward_function,
      connection_string=flags.FLAGS.connection_string) as env:

    env.set_agent_id("singulation-autopick-example-v0")

    # Iterate over episodes and steps.
    failure_count: int = 0

    logging.info("================================> Reset environment")
    _ = env.reset()
    observation = None
    for i_episode in range(1000):
      logging.info("================================> Started episode %d",
                   i_episode)
      # Reset to the initial state for the simulation.
      # On a real robot, this forces everything into known positions/states.
      done = False
      episode_bin: int = env.switch_bins()

      # Start a task.
      action = collections.OrderedDict(
          {"text_instructions": collections.OrderedDict({"task_enable": 1})})
      _, _, _, _ = env.step(action)

      # Run through a fixed number of steps
      t = 0
      while not done:
        t += 1
        logging.info("================================> i_episode=%d, step=%d",
                     i_episode, t)

        # Create an action from the observation received.
        action = collections.OrderedDict(
            {"oracle": collections.OrderedDict({"request": episode_bin})})
        k: str

        logging.info("JM's action: %s", action)
        # The step function takes current action and creates a new
        # observation, etc. This is where the ML agent code is run.
        observation, reward, done, _ = env.step(action)
        xobservation: Dict[str, core.Observation] = {
            k: v
            for (k, v) in observation.items()
            if k not in ("camera", "depth_camera")
        }
        logging.info("JM's xobservation: %s", xobservation)

        if reward == 2.0:
          failure_count += 1
          if failure_count == 2:
            failure_count = 0
            done = True
            # End a task.
            action = collections.OrderedDict({
                "text_instructions": collections.OrderedDict({"task_enable": 0})
            })
            _, _, _, _ = env.step(action)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  flags.DEFINE_string(
      "connection_string", None,
      "Connect using a PyReach connection string (see "
      "connection_string.md for examples and documentation).")
  app.run(main)
