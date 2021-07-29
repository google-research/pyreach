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

"""Template for a t-shirt folding benchmark agent.

This template demonstrates the basic usage of the t-shirt folding benchmark Gym
environment.
"""
import collections
import time

import gym  # type: ignore
import numpy as np  # type: ignore
from pyreach.gyms import core
from pyreach.gyms import experiment_assigner
from pyreach.gyms.envs.benchmark_folding import BenchmarkFoldingEnv


class JointsFoldingAgent:
  """Example agent for the wrapped T-Shirt Folding benchmark environment using joint moves."""
  ACTION_TIME_INCREMENT_SECONDS = 1.0

  def __init__(self) -> None:
    # Store anything that needs to be preserved, such as models.
    self._action_id = 0
    pass

  def _calculate_action(self, obs: core.Observation,
                        env: BenchmarkFoldingEnv) -> core.Action:
    """Do something based on the observation.

    Currently generates random moves around current joint position.

    Args:
      obs: the current observation
      env: the environment on which calculations are to be performed

    Raises:
      Exception: if the observation is not valid
    Returns:
      Next action of the agent
    """
    assert isinstance(obs, (dict, collections.OrderedDict))

    # Example of how to fetch joints and camera images from observation space
    joints: np.ndarray = obs["arm"]["joint_angles"]
    image: np.ndarray = obs["depth_camera"]["color"]

    assert isinstance(joints, np.ndarray)
    assert isinstance(image, np.ndarray)

    new_joints = env.SAFE_JOINT_ANGLES + np.random.uniform(-0.005, 0.005, 6)
    new_vacuum = np.random.randint(2)

    print(f"{time.time():.4f}:AGENT: Random joint move to {new_joints} "
          f"and vacuum to {new_vacuum}")

    self._action_id += 1

    action = {
        "arm": {
            "joint_angles": new_joints,
            "command": 1,
            "id": self._action_id
        },
        "vacuum": {
            "state": new_vacuum
        }
    }

    return action

  def single_attempt(self, env: BenchmarkFoldingEnv) -> None:
    """Runs the agent loop."""
    env.set_agent_id("sample-folding-agent-v0")

    # env.reset() will swirl the t-shirt into a random configuration
    obs = env.reset()

    print(f"{time.time():.4f}:AGENT: Starting policy")

    while True:
      loop_start_time = time.time()

      # Get up-to-date observation after we slept
      obs, _, done, _ = env.step({})

      # Check if environment says we are done
      if done:
        print(f"{time.time():.4f}:AGENT: Step returned done")
        break

      # Agents are welcome to attempt unfolding, but it is not required.
      if env.parse_instruction(obs) == "Unfold the t-shirt":
        print(f"{time.time():.4f}:AGENT: Cheating. Just say you are done.")
        env.finish_instruction()
        # Unfolding is done, let's continue for the 'Fold' instruction.
        continue

      # If no special cases or timeouts, perform normal obs -> action -> step
      action = self._calculate_action(obs, env)
      obs, _, done, _ = env.step(action)

      # Check if environment says we are done
      if done:
        print(f"{time.time():.4f}:AGENT: Step returned done")
        break

      # Attempt to operate with delta t of ACTION_TIME_INCREMENT_SECONDS
      loop_end_time = time.time()
      loop_elapsed_secs = loop_end_time - loop_start_time
      loop_slack_secs = self.ACTION_TIME_INCREMENT_SECONDS - loop_elapsed_secs

      if loop_slack_secs > 0:
        time.sleep(loop_slack_secs)
      else:
        print(f"{time.time():.4f}:AGENT: Did not hit "
              f"{1.0/self.ACTION_TIME_INCREMENT_SECONDS} Hz target action rate")
        print(f"{time.time():.4f}:AGENT: Missed target deadline by "
              f"{loop_slack_secs*1000.0} ms")

    print(f"{time.time():.4f}:AGENT: An attempt has ended")


def main() -> None:
  agent = JointsFoldingAgent()

  with gym.make("benchmark-folding-v0") as env:
    # To compare multiple agents, pass more than one agents below.
    experiment_assigner.randomized_run(env, [agent.single_attempt], [1.0])


if __name__ == "__main__":
  main()
