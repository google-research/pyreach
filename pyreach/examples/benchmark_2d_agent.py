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
implements essentially a random policy, performing small moves. The essence of
the policy is in the agent's calculate_action() function.

== Creating the environment ==

As with all OpenAI Gyms, the 2D environment is created like this:

with gym.make("benchmark-2d-v1") as env:
  your_code_here(env)

== About the environment ==

The environment provides two functions:

obs = env.reset()
obs, reward, done, info = env.step(action)

The reset() function should be called once and once only. Thereafter, you can
use the observation returned by reset and then from every step to determine what
the next action should be.

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

from absl import app  # type: ignore
from absl import flags  # type: ignore
import gym  # type: ignore
import matplotlib.axes as pltaxes  # type: ignore
import matplotlib.image as pltimage  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore

from pyreach.gyms import core
from pyreach.gyms.envs import benchmark_2d  # pylint: disable=unused-import

# The type of the return from step.
StepReturn = Tuple[core.Observation, float, bool, Any]

# The type of an observation. More strict than core.Observation.
ObservationDict = Union[dict, collections.OrderedDict]

# The center x,y coordinates that the agent goes to at the beginning of a task,
# so that jiggling around won't hit joint limits.
CENTER_X_METERS = 0.39
CENTER_Y_METERS = 0

# How long to wait between actions.
ACTION_TIME_INCREMENT_SECONDS = 0.1


class ServoJoints2DRandomAgent:
  """Example agent for the wrapped 2D benchmark environment for servo moves."""
  env: Optional[gym.Env]
  new_long_horizon_instr: bool
  new_short_horizon_instr: bool

  def __init__(self) -> None:
    self.env: Optional[gym.Env] = None
    self.figure: Any = None
    self.color_plt: Dict[str, Any] = {"axis": None, "img": None}
    self.short_horizon_instr: Optional[np.ndarray] = None
    self.long_horizon_instr: Optional[np.ndarray] = None
    self.new_long_horizon_instr = False
    self.new_short_horizon_instr = False

  def calculate_action(self, observation: core.Observation) -> core.Action:
    """Does something based on the observation.

    This is a random policy.
    Fill me in!

    Args:
      observation: the current observation.

    Raises:
      Exception: if the observation is not valid.

    Returns:
      The next action of the agent.
    """
    observation = cast(Dict[str, Any], observation)
    arm: ObservationDict = observation["arm"]
    pose: np.ndarray = arm["pose"]

    rnd_offset: np.ndarray = np.random.uniform(
        low=-0.002, high=0.002, size=(2,))
    pose[0] += rnd_offset[0]
    pose[1] += rnd_offset[1]

    print(f"Desired pose: {pose}")

    action: core.Action = collections.OrderedDict(
        {"arm": collections.OrderedDict({
            "command": 2,
            "pose": pose,
            "synchronous": 1,
            "use_linear": 1,
            "velocity": 0.5,
            "preemptive": 1,
        })})
    return action

  def go_to_center(self, observation: core.Observation) -> core.Action:
    """Goes to the center synchronously."""
    print("Going to center")
    observation = cast(Dict[str, Any], observation)
    arm: ObservationDict = observation["arm"]
    pose: np.ndarray = arm["pose"]

    pose[0] = CENTER_X_METERS
    pose[1] = CENTER_Y_METERS

    action: core.Action = collections.OrderedDict(
        {"arm": collections.OrderedDict({
            "command": 2,
            "pose": pose,
            "synchronous": 1,
            "use_linear": 1,
            "velocity": 0.4,
            "preemptive": 1,
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
      self.figure.canvas.draw()
      self.figure.canvas.flush_events()

    else:
      raise SystemError(f"Unknown image type received: {img.dtype}")

  def handle_image(self, observation: core.Observation) -> None:
    """Shows the images in the observation."""
    assert isinstance(observation, (dict, collections.OrderedDict))

    color_camera: ObservationDict = observation["color_camera"]
    assert isinstance(color_camera, (dict, collections.OrderedDict))

    color_data: np.ndarray = color_camera["color"]
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

  def instr_str(self, data: np.ndarray) -> str:
    """Decodes the data array into a string."""
    buff = bytearray([int(x) for x in data.tolist()])
    return buff.decode("utf-8").rstrip("\x00")

  def extract_instructions(self, obs: core.Observation) -> None:
    """Extracts the long- and short-horizon instructions from the obs."""
    obs = cast(Dict[str, Any], obs)
    long_horizon_instr = obs["long_horizon_instruction"]["instruction"]
    short_horizon_instr = obs["short_horizon_instruction"]["instruction"]

    if not all(long_horizon_instr == self.long_horizon_instr):
      print(f"{time.time()}: New long horizon instruction: "
            f"{self.instr_str(long_horizon_instr)}")
      self.long_horizon_instr = long_horizon_instr
      # Up to agent to clear this.
      self.new_long_horizon_instr = True

    if not all(short_horizon_instr == self.short_horizon_instr):
      print(f"{time.time()}: New short horizon instruction: "
            f"{self.instr_str(short_horizon_instr)}")
      self.short_horizon_instr = short_horizon_instr
      # Up to agent to clear this.
      self.new_short_horizon_instr = True

  def run(self, env: gym.Env) -> None:
    """Runs the agent loop."""
    self.env = env
    self.env.set_agent_id("2d-example-random-v1")

    print(f"{time.time()}: Resetting environment, please wait")

    obs, _, _, _ = self.env.reset()
    arm: ObservationDict = obs["arm"]
    joint_angles: np.ndarray = arm["joint_angles"]
    pose: np.ndarray = arm["pose"]

    print(f"{time.time()} Arm at: {joint_angles}, pose {pose}")

    self.init_image_plot()
    self.handle_image(obs)

    obs, _, done, _ = self.env.step({})
    print(f"{time.time()} Arm at joints {obs['arm']['joint_angles']} "
          f"pose {obs['arm']['pose']}")
    self.extract_instructions(obs)

    print(f"{time.time()}: Running policy")
    while not done:
      start_time: float = time.time()

      # Get up-to-date observation after we slept
      obs, _, done, _ = self.env.step({})
      self.extract_instructions(obs)
      if done:
        print(f"{time.time()}: Step returned done")
        break

      next_action: core.Action = ()

      if self.new_long_horizon_instr:
        next_action = self.go_to_center(obs)
        self.new_long_horizon_instr = False
      else:
        next_action = self.calculate_action(obs)

      obs, _, done, _ = self.env.step(next_action)
      self.extract_instructions(obs)
      if done:
        print(f"{time.time()}: Step returned done")
        break

      # Displaying the image could take some time, so commenting this out
      # or updating only periodically could make things faster.
      self.handle_image(obs)

      end_time: float = time.time()
      loop_time: float = end_time - start_time
      slack_time: float = ACTION_TIME_INCREMENT_SECONDS - loop_time

      if slack_time > 0:
        # Send actions at 10 Hz
        time.sleep(slack_time)


def main(_: Any) -> None:
  agent: ServoJoints2DRandomAgent = ServoJoints2DRandomAgent()

  with gym.make("benchmark-2d-v1",
                connection_string=flags.FLAGS.connection_string) as env:
    agent.run(env)


if __name__ == "__main__":
  flags.DEFINE_string(
      "connection_string", None,
      "Connect using a PyReach connection string (see "
      "connection_string.md for examples and documentation).")
  app.run(main)
