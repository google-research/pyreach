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
"""Template for a Kitting agent using the PyReach Gym.

This template demonstrates basic usage of the Kitting Gym environment. It
implements essentially a random policy, performing small moves with a
50% chance. The essence of the policy is in the agent's calculate_action()
function.

== Creating the environment ==

As with all OpenAI Gyms, the Kitting environment is created like this:

with gym.make("benchmark-kitting-v0") as env:
  your_code_here(env)

== About the environment ==

The environment provides two functions:

obs = env.reset()
obs, reward, done, info = env.step(action)

The reset() function should be called at the beginning of an episode and will
reset the scene in SIM only.

=== The agent loop ===

See the run() function.
"""

import collections
import time
from typing import Any, Optional, Tuple

import gym  # type: ignore

from pyreach.gyms import core
from pyreach.gyms.envs.benchmark_kitting import BenchmarkKittingWrapper

MAX_ATTEMPTS_KITTING = 7
MAX_ATTEMPTS_DEKITTING = 8


class KittingAgent:
  """Example agent for the wrapped Kitting environment."""
  env: Optional[gym.Env]

  def __init__(self) -> None:
    self.env = None

  # pylint: disable=unused-argument
  def kitting_reward_function(
      self, action: core.Action,
      observation: core.Observation) -> Tuple[float, bool]:
    """Reward function for environment.

    A function that the environment uses when step() is called, to compute the
    reward value and done flag that step() should return. Pass this to the
    gym.make function when making a new environment.

    Args:
      action: the action taken via step.
      observation: the current observation.

    Returns:
      A tuple of (reward, done) to return from step().
    """
    assert isinstance(observation, dict)
    if "oracle" in observation:
      if "response" in observation["oracle"]:
        metric: int = observation["oracle"]["response"]
        if metric == 1:
          return 1.0, True
        return 0.0, False

    # All other cases indicate something going wrong.
    return -1.0, False

  # pylint: disable=unused-argument
  def calculate_action(self, observation: core.Observation,
                       current_instruction: str) -> core.Action:
    """Do something based on the observation and the current instruction.

    This is random for now.
    Fill me in!

    Args:
      observation: the current observation.
      current_instruction: the current instruction the agent is working on.

    Raises:
      Exception: if the observation is not valid.

    Returns:
      The next action of the agent.
    """
    assert isinstance(self.env, BenchmarkKittingWrapper)
    kitting_mode: int = self.env.set_mode(current_instruction)

    action = collections.OrderedDict(
        {"oracle": collections.OrderedDict({"request": kitting_mode})})

    return action

  def run(self, env: gym.Env) -> None:
    """Runs the agent loop."""
    self.env = env
    self.env.set_agent_id("kitting-example-v0")

    prev_instruction = None
    current_instruction: str = ""
    done = False

    print(f"{time.time()}: Resetting environment, please wait")
    obs = self.env.reset()

    print(f"{time.time()}: Running policy")
    while obs is not None:

      if prev_instruction and not done:
        obs, _, _, _ = env.ask_for_new_instruction(obs)

      done = False
      text_instructions: Any = obs["text_instructions"]
      instruction: Any = text_instructions["instruction"]

      text = bytes([x for x in instruction if x != 0]).decode("utf-8")
      if text != prev_instruction:
        print(f"{time.time()}: New instruction to handle: '{text}'")
        prev_instruction = text
        step = 0

        if "Empty" in text:
          current_instruction = "dekitting"
        elif "Complete" in text:
          current_instruction = "kitting"

      # done will get set when time for the instruction runs out.
      while ((current_instruction == "dekitting" and
              step < MAX_ATTEMPTS_DEKITTING) or
             (current_instruction == "kitting" and
              step < MAX_ATTEMPTS_KITTING)) and not done:

        next_action = self.calculate_action(obs, current_instruction)

        obs, _, done, _ = self.env.step(next_action)
        step += 1

        if done:
          print(f"{time.time()}: Step returned done")


def main() -> None:

  agent = KittingAgent()

  with gym.make(
      "benchmark-kitting-v0",
      reward_done_function=agent.kitting_reward_function) as env:

    agent.run(BenchmarkKittingWrapper(env))


if __name__ == "__main__":
  main()