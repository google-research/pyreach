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
"""Benchmark environment for the Kitting benchmark."""

import collections
import time
from typing import Tuple, Any, Dict, List
import gym  # type: ignore

from pyreach.gyms import core
from pyreach.gyms import reach_env
from pyreach.gyms.devices.text_instructions_device import ReachDeviceTextInstructions

KITTING = 3
DEKITTING = 4
UNSET = 0

INSTRUCTION_TIMEOUT_SEC = 20


class KittingBenchmarkEnv(reach_env.ReachEnv):  # type: ignore
  """Benchmark environment for the Kitting benchmark.

  Evaluation (see go/robotics-benchmark-kitting)

  1. The agent connects to the evaluation cell.
  2. The instruction "match this image" is given for the first task along with
     an image of the filled shell. This is the "kit" task. Then the instruction
     "match this image" is given for the second task along with an image of the
     empty shell. This is the "dekit" task. A total of 2 tasks
     (1 kit and 1 dekit) are presented.
  3. For each instruction:
       a. The instruction is given to the agent as text and image.
       b. The agent has 60 seconds from transmission of instruction to complete
          the instruction. If the agent completes the instruction in less time,
          it must signal the cell that the instruction is complete.
       c. The cell takes a picture of the table.
       d. The instruction, along with the picture, are stored.
  4. The agent is allowed to disconnect from the evaluation cell. If the agent
     does not disconnect within five seconds, the agent is forcefully
     disconnected.
  5. Each instruction/picture pair is evaluated for success. The instruction is
     graded as a success if all products are within <= 1cm & <= 15 deg of
     expected positions relative to package.
  6. The evaluation is graded a success if 100% of instructions are graded as
     a success.
  """

  def __init__(self, **kwargs: Any) -> None:
    """Initialize the Singulation environment."""
    center_joint_angles: List[float] = [3.06, -1.66, -1.57, -1.10, 1.7, 0.0]
    low_joint_angles: Tuple[float, ...] = tuple(
        [cja - 5.0 for cja in center_joint_angles])
    high_joint_angles: Tuple[float, ...] = tuple(
        [cja + 5.0 for cja in center_joint_angles])

    task_params: Dict[str, str] = {
        "task-code": "130",
        "intent": "pick",
        "success_type": "vacuum-pressure-sensor"
    }

    pyreach_config: Dict[str, reach_env.ReachElement] = {
        "arm":
            reach_env.ReachArm(
                "", low_joint_angles, high_joint_angles, is_synchronous=True),
        "camera":
            reach_env.ReachColorCamera("", (576, 1024), is_synchronous=True),
        "depth_camera":
            reach_env.ReachDepthCamera(
                "", (720, 1280), True, is_synchronous=True),
        "workcell_camera":
            reach_env.ReachColorCamera("realsense", (480, 640)),
        "server":
            reach_env.ReachServer("Server"),
        "vacuum":
            reach_env.ReachVacuum(""),
        "oracle":
            reach_env.ReachOracle(
                "oracle",
                task_params["task-code"],
                task_params["intent"],
                task_params["success_type"],
                is_synchronous=True),
        "text_instructions":
            reach_env.ReachTextInstructions("instruction-generator"),
    }

    super().__init__(
        pyreach_config=pyreach_config, task_params=task_params, **kwargs)

  def step(self,
           action: core.Action) -> Tuple[core.Observation, float, bool, Any]:
    """Perform one step."""
    observation: core.Observation
    reward: float
    done: bool
    info: Any

    observation, reward, done, info = super().step(action)

    if done:
      observation, _, _, info = self.ask_for_new_instruction(observation)
      return (observation, reward, done, info)

    return (observation, reward, done, info)

  def ask_for_new_instruction(
      self, current_observation: core.Observation
  ) -> Tuple[core.Observation, float, bool, Any]:
    """Asks for a new instruction.

    If we time out waiting for a new instruction, that means that
    we have completed all instructions, and we return None,
    otherwise we return the latest observation.

    Args:
      current_observation: the current observation.

    Returns:
      The observation when the instruction is received.
    """
    print(f"{time.time()}: Asking for a new text instruction")

    # End current task
    action = collections.OrderedDict(
        {"text_instructions": collections.OrderedDict({"task_enable": 0})})

    _, _, _, _ = super().step(action)

    # Start a new task
    return self._start_new_task()

  def reset(self) -> core.Observation:
    """Resets the benchmark.

    On SIM, this resets the scene and returns an observation. On real, it only
    returns an observation.

    Returns:
      Initial observation.
    """

    # End any current task
    action = collections.OrderedDict(
        {"text_instructions": collections.OrderedDict({"task_enable": 0})})
    _, _, _, _ = super().step(action)
    super().reset()

    # Start a new task
    obs, _, _, _ = self._start_new_task()
    return obs

  def _start_new_task(self) -> Tuple[core.Observation, float, bool, Any]:
    text_instr_device = self._elements["text_instructions"]
    assert isinstance(text_instr_device, ReachDeviceTextInstructions)
    instr_obs, _, _ = text_instr_device.get_observation(self._host)
    assert isinstance(instr_obs, dict) and "counter" in instr_obs
    start_instr_counter = instr_obs["counter"]
    action = collections.OrderedDict(
        {"text_instructions": collections.OrderedDict({"task_enable": 1})})
    start_time = time.time()
    while True:
      (obs, reward, done, info) = super().step(action)
      assert isinstance(obs, dict)
      text_instructions = obs["text_instructions"]
      assert isinstance(text_instructions, dict)
      if text_instructions["counter"] != start_instr_counter:
        break
      if time.time() - start_time > INSTRUCTION_TIMEOUT_SEC:
        raise ValueError("Timeout waiting for valid instruction.")

    return obs, reward, done, info


class BenchmarkKittingWrapper(gym.Wrapper):
  """A wrapper for the 2D Benchmark environment for servoing joints only.

  This environment is a stripped-down environment which provides actions for
  servo moves of joints only.

  == Actions ==

  action["arm"]:
    "pose":
        # The pose to move to, in radians.
        gym.spaces.Box(
            low=np.array((-6.283, -2.059, -3.926, -3.141, 1.692, -6.283)),
            high=np.array((6.283, 2.094, 0.191, 3.141, 3.141, 6.283)),
            dtype=np.dtype(float)),

  == Observations ==

    No filters! See KittingBenchmarkEnv!
  """

  def __init__(self, env: KittingBenchmarkEnv) -> None:
    super().__init__(env)

    self.env = env
    self._mode: int = UNSET

    self.action_space: core.Space = gym.spaces.Dict({
        "arm": gym.spaces.Dict({
            "pose": self.env.action_space["arm"]["pose"],
        })
    })
    self.observation_space: core.Space = self.env.observation_space

  def step(self,
           action: core.Action) -> Tuple[core.Observation, float, bool, Any]:
    assert isinstance(action, (dict, collections.OrderedDict))
    return self.env.step(action)

  def set_mode(self, instruction: str) -> int:
    """Set mode of Kitting task."""
    if instruction == "dekitting":
      self._mode = DEKITTING
    elif instruction == "kitting":
      self._mode = KITTING
    return self._mode
