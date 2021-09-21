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
import numpy as np  # type: ignore

from pyreach.gyms import core
from pyreach.gyms.envs.benchmark_kitting import BenchmarkKittingWrapper

FINAL_INSTRUCTION_TIMEOUT_SECONDS = 15.0


class KittingAgent:
  """Example agent for the wrapped Kitting environment."""
  env: Optional[gym.Env]

  def __init__(self) -> None:
    self.env = None

  # pylint: disable=unused-argument
  def i_think_im_done_based_on(self, current_instruction: Optional[np.ndarray],
                               observation: core.Observation) -> bool:
    """Decides whether you're done with the current instruction.

    This is a completely random function right now.
    Fill me in!

    Args:
      current_instruction: the current instruction to follow.
      observation: the current observation.

    Returns:
      True if the episode is done.
    """
    if current_instruction is None:
      return False
    rnd_num = np.random.randint(0, 100) % 10
    if rnd_num > 4:
      return True
    return False

  def agent_reward_function(
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
    assert isinstance(observation, (dict, collections.OrderedDict))
    text_instructions: Any = observation["text_instructions"]
    assert isinstance(text_instructions, (dict, collections.OrderedDict))
    current_instruction: Any = text_instructions["instruction"]
    assert isinstance(current_instruction, np.ndarray)

    if self.i_think_im_done_based_on(current_instruction, observation):
      print("I think I'm done")
      return 1.0, True
    return 0.0, False

  def calculate_action(self, observation: core.Observation,
                       current_instruction: np.ndarray) -> core.Action:
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
    kitting_mode: int = self.env.switch_modes()

    action = collections.OrderedDict(
        {"oracle": collections.OrderedDict({"request": kitting_mode})})

    return action

  def run(self, env: gym.Env) -> None:
    """Runs the agent loop."""
    self.env = env
    self.env.set_agent_id("kitting-example-v0")

    prev_instruction = None

    print(f"{time.time()}: Resetting environment, please wait")
    obs = self.env.reset()

    print(f"{time.time()}: Running policy")
    while obs is not None:
      done = False
      new_instruction_deadline: Optional[float]
      new_instruction_deadline = time.time() + FINAL_INSTRUCTION_TIMEOUT_SECONDS

      # done will get set when time for the instruction runs out.
      while obs is not None and not done:
        text_instructions: Any = obs["text_instructions"]
        instruction: Any = text_instructions["instruction"]

        text = bytes([x for x in instruction if x != 0]).decode("utf-8")
        if text != prev_instruction:
          print(f"{time.time()}: New instruction to handle: '{text}'")
          prev_instruction = text
          new_instruction_deadline = None

        if new_instruction_deadline is not None:
          if time.time() > new_instruction_deadline:
            print(f"{time.time()}: No more instructions!")
            return

        next_action = self.calculate_action(obs, instruction)

        obs, _, done, _ = self.env.step(next_action)

        if done:
          print(f"{time.time()}: Step returned done")
          break


def main() -> None:

  agent = KittingAgent()

  with gym.make(
      "benchmark-kitting-v0",
      reward_done_function=agent.agent_reward_function) as env:

    agent.run(BenchmarkKittingWrapper(env))


if __name__ == "__main__":
  main()
