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

"""Template for a "raw" 2D benchmark agent.

This template demonstrates "everything bagel" usage of the 2D benchmark Gym
environment, where no wrappers or observation filtering is done.

It implements essentially a random policy, performing small moves,
with a 5% chance of deciding the instruction is complete. The essence of the
policy is in the agent's calculate_action() function.

== Creating the environment ==

As with all OpenAI Gyms, the 2D environment is created like this:

with gym.make("benchmark-2d-v0",
                reward_done_function=agent.agent_reward_function) as env:
  your_code_here(env)

== About the environment ==

The environment provides two functions:

obs = env.reset()
obs, reward, done, info = env.step(action)

The reset() function should be called once and once only. Thereafter, you can
use the observation returned by reset and every step to determine what the
next action should be.

=== The reward_done_function function ===

Because there is nothing in the environment which can tell the agent when it
has completed an instruction, the agent is responsible for telling the
environment when it thinks it has completed the instruction. This is done via
the reward_done_function passed to the environment constructor.

This function is called on every call to step().

This function returns a tuple of (reward, done flag). The function should
return a done flag of True once it thinks it has completed the current
instruction. The reward and flag will be returned by step.

However, the environment also monitors how much time the agent is taking to
work on an instruction. If the agent runs out of time as defined by the
benchmark (see TIMEOUT_PER_TASK_SECONDS), the environment will return a
reward of -1 and a done flag of True.

=== Environment initialization ===

Upon calling reset(), the environment will run a sweep of the arm around the
edges of the board to try to get any blocks hanging out on the edge to move
towards the delineated working area. Once that is complete, the environment
starts a task. reset() returns with the current observation, and the agent can
perform its loop.

=== The agent loop ===

See the run() function.

=== Handling images ===

See the handle_image() function.

While the observation contains images which can be used to decide what action
to take, this template agent also displays them using matplotlib. This is not a
necessary thing for the agent to do, but could be useful in monitoring the
agent as it does its thing.
"""
import collections
import time
from typing import Any, Dict, Optional, Union, cast, Tuple

import gym  # type: ignore
import matplotlib.axes as pltaxes  # type: ignore
import matplotlib.image as pltimage  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore

from pyreach.gyms import core

# How long to wait for an instruction before realizing that no more instructions
# are going to come.
FINAL_INSTRUCTION_TIMEOUT_SECONDS = 10.0

# How long to wait between actions.
ACTION_TIME_INCREMENT_SECONDS = 0.1

# The z-coordinate for where the tip of the end-effector is above the table
# by half the height of a block.
HALF_BLOCK_HEIGHT_METERS = 0.2

# The x and y limits for the workspace.
BOARD_X_LIMITS_METERS = (0.12, 0.502)
BOARD_Y_LIMITS_METERS = (-0.287, 0.287)


class Raw2DAgent:
  """Example agent for the base 2D benchmark environment."""
  env: gym.Env
  awaiting_new_instruction: bool

  def __init__(self) -> None:
    self.env: Optional[gym.Env] = None
    self.awaiting_new_instruction: bool = True
    self.figure: Any = None
    self.color_plt: Dict[str, Optional[plt]] = {"axis": None, "img": None}
    self.action_id: int = 1

  # pylint: disable=unused-argument
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

    if self.awaiting_new_instruction:
      return 0.0, False

    if self.i_think_im_done_based_on(current_instruction, observation):
      self.awaiting_new_instruction = True
      print(f"{time.time()}: I think I'm done")
      return 1.0, True

    return 0.0, False

  # pylint: disable=unused-argument
  def i_think_im_done_based_on(self, current_instruction: Tuple[int, ...],
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
    # 0.7% chance per 100 msec. This means roughly a 50% chance of
    # finishing within 10 seconds
    rnd_num = np.random.randint(0, 1000)
    if rnd_num < 7:
      return True
    return False

  def calculate_action(self, observation: core.Observation,
                       current_instruction: np.ndarray) -> core.Action:
    """Does something based on the observation and the current instruction.

    This is a random policy.
    Fill me in!

    Args:
      observation: the current observation.
      current_instruction: the current instruction the agent is working on.

    Raises:
      Exception: if the observation is not valid.

    Returns:
      The next action of the agent.
    """
    assert isinstance(observation, (dict, collections.OrderedDict))
    arm_observation: Any = observation["arm"]
    assert isinstance(arm_observation, (dict, collections.OrderedDict))
    robot_pose: Any = arm_observation["pose"]
    assert isinstance(robot_pose, np.ndarray)

    rnd_offset_x = np.random.uniform(low=-0.001, high=0.001)
    rnd_offset_y = np.random.uniform(low=-0.001, high=0.001)
    new_robot_pose: np.ndarray = robot_pose
    new_robot_pose[0] += rnd_offset_x
    new_robot_pose[1] += rnd_offset_y

    # The environment should prevent movements outside the
    # X, Y bounds (returning done with a negative reward) so that we don't
    # knock blocks out of the working area, which would require operations
    # intervention. This isn't implemented yet, so for now we just restrict
    # the movement here.

    new_robot_pose[0] = np.minimum(
        np.maximum(new_robot_pose[0], BOARD_X_LIMITS_METERS[0]),
        BOARD_X_LIMITS_METERS[1])
    new_robot_pose[1] = np.minimum(
        np.maximum(new_robot_pose[1], BOARD_Y_LIMITS_METERS[0]),
        BOARD_Y_LIMITS_METERS[1])
    new_robot_pose[2] = HALF_BLOCK_HEIGHT_METERS
    action = collections.OrderedDict({
        "arm":
            collections.OrderedDict({
                "command": 2,
                "pose": new_robot_pose,
                "use_linear": 1,
                "servo": 1,
                "id": self.action_id,
            })
    })
    self.action_id += 1
    return action

  def move_to_center_carelessly(self,
                                observation: core.Observation) -> core.Action:
    """Moves to the center without caring about hitting blocks."""
    assert isinstance(observation, (dict, collections.OrderedDict))
    arm_observation: Any = observation["arm"]
    assert isinstance(arm_observation, (dict, collections.OrderedDict))
    robot_pose: Any = arm_observation["pose"]
    assert isinstance(robot_pose, np.ndarray)

    new_robot_pose: np.ndarray = robot_pose.copy()
    new_robot_pose[0] = 0.3
    new_robot_pose[1] = 0
    new_robot_pose[2] = 0.114
    action = collections.OrderedDict({
        "arm":
            collections.OrderedDict({
                "command": 2,
                "pose": new_robot_pose,
                "use_linear": 1,
                "velocity": 0.05,
                "synchronous": 1,
            })
    })
    return action

  #
  # Image handling functions
  #

  def show_image(self, plot: Dict[str, Optional[Union[pltaxes.Axes,
                                                      pltimage.AxesImage]]],
                 img: Optional[np.ndarray]) -> None:
    """Shows an image in the given plot area."""
    if img is None:
      print("No image")
      return
    img = cast(np.ndarray, img)
    plot = cast(Dict[str, Optional[Union[pltaxes.Axes, pltimage.AxesImage]]],
                plot)

    if img.dtype == np.uint8:
      # I can't figure out how to show a placeholder image of some
      # small size first, and then resize the axes once we have the
      # actual image. So this will have to do.
      if plot["img"] is None:
        axis = cast(pltaxes.Axes, plot["axis"])
        plot["img"] = axis.imshow(img)
      image = cast(pltimage.AxesImage, plot["img"])
      image.set_data(img)
      self.figure.canvas.flush_events()

    else:
      raise SystemError(f"Unknown image type received: {img.dtype}")

  def handle_image(self, observation: core.Observation) -> None:
    """Shows the images in the observation."""
    assert isinstance(observation, (dict, collections.OrderedDict))
    color_camera: Any = observation["color_camera"]
    assert isinstance(color_camera, (dict, collections.OrderedDict))
    color_data: Any = color_camera["color"]
    self.show_image(self.color_plt, color_data)

  def init_image_plot(self) -> None:
    """Initializes the matplotlib plots for displaying images."""
    plt.ion()
    axis: plt
    self.figure, axis = plt.subplots()
    self.figure.set_figheight(5)
    self.figure.set_figwidth(10)

    self.color_plt["axis"] = axis
    axis.set_title("color")

    self.figure.canvas.flush_events()

  def run(self, env: gym.Env) -> None:
    """Runs the agent loop."""
    self.env = env
    self.env.set_agent_id("2d-example-raw-random-v0")

    prev_instruction: Optional[str] = None

    # reset() causes the robot to run a cleanup pass around the edge of the
    # board, in an attempt to move any blocks on the edge more towards the
    # working area of the board.
    print(f"{time.time()}: Resetting environment, please wait")
    obs: core.Observation = self.env.reset()

    self.init_image_plot()
    self.handle_image(obs)

    print(f"{time.time()}: Running policy")
    while obs is not None:
      done: bool = False
      new_instruction_deadline: Optional[float]
      new_instruction_deadline = time.time() + FINAL_INSTRUCTION_TIMEOUT_SECONDS

      # done will get set when time for the instruction runs out.
      while obs is not None and not done:

        assert isinstance(obs, (dict, collections.OrderedDict))
        text_instructions: Any = obs["text_instructions"]
        assert isinstance(text_instructions, (dict, collections.OrderedDict))
        instruction: np.ndarray = text_instructions["instruction"]
        text: str = bytes([x for x in instruction if x != 0]).decode("utf-8")
        if text != prev_instruction:
          print(f"{time.time()}: New instruction to handle: '{text}'")
          prev_instruction = text
          new_instruction_deadline = None

        if new_instruction_deadline is not None:
          if time.time() > new_instruction_deadline:
            print(f"{time.time()}: No more instructions!")
            return

        next_action: core.Action = self.calculate_action(obs, instruction)

        obs, _, done, _ = self.env.step(next_action)

        # This could take some time, so commenting this out could make
        # things faster.
        self.handle_image(obs)

        if done:
          print(f"{time.time()}: Step returned done")
          break

        # Send actions at 10 Hz
        time.sleep(ACTION_TIME_INCREMENT_SECONDS)


def main() -> None:
  agent = Raw2DAgent()

  with gym.make("benchmark-2d-v0",
                reward_done_function=agent.agent_reward_function) as env:

    agent.run(env)


if __name__ == "__main__":
  main()
