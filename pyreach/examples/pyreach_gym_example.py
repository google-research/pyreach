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
"""Example PyReach Gym Agent.

This example demonstrates the basic usage of the PyReach Gym API based on
an generic example environment. The example environment and the example
agent code is not meant to be used for any practical purposes.
DO NOT try to collect data or train a model with it.

Before running this example, please make sure `reach connect` is running.
"""
from typing import List, Tuple

from absl import app  # type: ignore
from absl import flags  # type: ignore
import gym  # type: ignore

from pyreach.gyms import core


# Reward and done signal can be customized through a function. This function
# takes the action and observation at a given step, runs custom logic to
# produce a numerical reward value and a boolean done signal. These values will
# be returned without modification by the env.step() function.
#
# Custom reward and done function is passed to the gym.make() function when
# a gym environment is created.
def my_awesome_reward_done_function(
    action: core.Action, observation: core.Observation) -> Tuple[float, bool]:
  assert action and observation
  return 0.0, False


def main(unused_argv: List[str]) -> None:
  with gym.make(
      "pyreach_gym_example-v0",
      connection_string=flags.FLAGS.connection_string,
      reward_done_function=my_awesome_reward_done_function) as env:
    env.set_agent_id("my-unique-agent-id-v0")
    print(f"An example observation:\n{env.reset()}")
    # The observation space is a Dict. The keys are device keys, which follows
    # the format "device_type:device_name". The value is device type dependent.
    #
    # An example looks as follows:
    # {
    #   'arm': {
    #     'ts': 1605579534.046733,
    #     'joint_angles': array([0., 0., 0., 0., 0., 0., 0.]),
    #     'pose': array([0., 0., 0., 0., 0., 0.])
    #   },
    #   'camera': {
    #     'ts': 1605579534.046733,
    #     'image': array([
    #       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #       ...
    #       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    #   },
    #   'depth_camera': {
    #     'ts': 1605579534.046733,
    #     'image': array([
    #       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #       ...
    #       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    #   },
    #   'vacuum': {
    #     'ts': 1605579534.046733,
    #     'vacuums': array([0])
    #   }
    # }
    # Note: The timestamps specify when the observation actually occurs.
    # Hence, the timestamps should be close to one another, but not equal.
    #
    # Multiple devices of the same type will be distinguished by device key.
    # For example:
    # {
    #   'arm:left': {
    #      ...
    #   },
    #   'arm:right': {
    #      ...
    #   },
    #   'camera:overview': {
    #      ...
    #   },
    #   'camera:side': {
    #      ...
    #   },
    # }

    print(f"An example Action:\n{env.action_space.sample()}")
    # Action space is a Dict. The keys are device keys.
    # For example:
    # {
    #   'arm:left': {
    #     'pose': array([0, 0, 0, 0, 0, 0]),
    #   },
    # }

    # Iterate over episodes and steps.
    for i_episode in range(3):
      # Reset to the initial state for the simulation.
      # On a real robot, this forces everything into known positions/states.
      env.reset()

      # Run through a fixed number of steps
      for t in range(30):
        print(f"============================ episode={i_episode}, step={t} ")
        # On a real robot, the render() method does nothing.
        # For a simulation, the render() method updates the simulator.
        env.render()

        # Create a random action.
        action = env.action_space.sample()
        print(f"action={action}")

        # The step function takes current action and creates a new
        # observation, etc. This is where the ML agent code is run.
        # pylint: disable=unused-variable
        observation, reward, done, info = env.step(action)
        if done:
          break


if __name__ == "__main__":
  flags.DEFINE_string(
      "connection_string", None,
      "Connect using a PyReach connection string (see "
      "connection_string.md for examples and documentation).")
  app.run(main)
