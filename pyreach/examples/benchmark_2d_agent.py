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
"""Template for a 2D benchmark agent using only servo joint moves.

This template demonstrates basic usage of the 2D benchmark Gym environment. It
implements essentially a random policy, performing small moves with a
50% chance. The essence of the policy is in the agent's calculate_action()
function.

== Creating the environment ==

As with all OpenAI Gyms, the 2D environment is created like this:

with gym.make("benchmark-2d-v0") as env:
  your_code_here(env)

== About the environment ==

The environment provides two functions:

obs = env.reset()
obs, reward, done, info = env.step(action)

The reset() function should be called once and once only. Thereafter, you can
use the observation returned by reset and every step to determine what the
next action should be.

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
from typing import Any, Dict, List, Optional, Union, cast

from absl import app  # type: ignore
from absl import flags  # type: ignore
import gym  # type: ignore
import matplotlib.axes as pltaxes  # type: ignore
import matplotlib.image as pltimage  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore

from pyreach.gyms import core
from pyreach.gyms.envs import benchmark_2d

# How long to wait for an instruction before realizing that no more instructions
# are going to come.
FINAL_INSTRUCTION_TIMEOUT_SECONDS = 10.0

# How long to wait between actions.
ACTION_TIME_INCREMENT_SECONDS = 0.1


class ServoJoints2DAgent:
  """Example agent for the wrapped 2D benchmark environment for servo moves."""
  env: Optional[gym.Env]

  def __init__(self) -> None:
    self.env: Optional[gym.Env] = None
    self.figure: Any = None
    self.color_plt: Dict[str, Optional[plt]] = {"axis": None, "img": None}

  # pylint: disable=unused-argument
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
    arm: Any = observation["arm"]
    assert isinstance(observation, (dict, collections.OrderedDict))
    robot_joints: Any = arm["joint_angles"]
    assert isinstance(robot_joints, np.ndarray)

    rnd_offset: np.ndarray = np.random.uniform(
        low=-0.002, high=0.002, size=(6,))
    new_robot_joints: np.ndarray = robot_joints + rnd_offset

    action: core.Action = collections.OrderedDict(
        {"arm": collections.OrderedDict({
            "joint_angles": new_robot_joints,
        })})
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
    assert isinstance(color_data, np.ndarray)
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
    self.env.set_agent_id("2d-example-random-v0")

    prev_instruction: Optional[str] = None

    # reset() causes the robot to run a cleanup pass around the edge of the
    # board, in an attempt to move any blocks on the edge more towards the
    # working area of the board.
    print(f"{time.time()}: Resetting environment, please wait")
    obs: core.Observation = self.env.reset()
    assert isinstance(obs, (dict, collections.OrderedDict))
    arm: Any = obs["arm"]
    assert isinstance(arm, (dict, collections.OrderedDict))
    joint_angles: Any = arm["joint_angles"]
    assert isinstance(joint_angles, np.ndarray)

    print(f"{time.time()} Arm at: {joint_angles}")

    self.init_image_plot()
    self.handle_image(obs)

    print(f"{time.time()}: Moving to center")

    self.env.go_to_center()
    obs, _, _, _ = self.env.step({})
    print(f"{time.time()} Arm at joints {obs['arm']['joint_angles']} "
          f"pose {obs['arm']['pose']}")

    print(f"{time.time()}: Running policy")
    while obs is not None:
      done: bool = False
      new_instruction_deadline: Optional[float] = (
          time.time() + FINAL_INSTRUCTION_TIMEOUT_SECONDS)

      # done will get set when time for the instruction runs out.
      while obs is not None and not done:

        start_time: float = time.time()

        # Get up-to-date observation after we slept
        obs, _, done, _ = self.env.step({})
        if done:
          print(f"{time.time()}: Step returned done")
          break

        assert isinstance(obs, (dict, collections.OrderedDict))
        text_instructions: Any = obs["text_instructions"]
        assert isinstance(text_instructions, (dict, collections.OrderedDict))
        instruction: Any = text_instructions["instruction"]
        assert isinstance(instruction, np.ndarray)

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

        # Displaying the image could take some time, so commenting this out
        # or updating only periodically could make things faster.
        self.handle_image(obs)

        if done:
          print(f"{time.time()}: Step returned done")
          break

        end_time: float = time.time()
        loop_time: float = end_time - start_time
        slack_time: float = ACTION_TIME_INCREMENT_SECONDS - loop_time

        if slack_time > 0:
          # Send actions at 10 Hz
          time.sleep(slack_time)


def main(unused_argv: List[str]) -> None:
  agent: ServoJoints2DAgent = ServoJoints2DAgent()

  with gym.make(
      "benchmark-2d-v0",
      connection_string=flags.FLAGS.connection_string) as env:
    agent.run(benchmark_2d.Benchmark2DServoJointsWrapper(env))


if __name__ == "__main__":
  flags.DEFINE_string(
      "connection_string", None,
      "Connect using a PyReach connection string (see "
      "connection_string.md for examples and documentation).")
  app.run(main)
