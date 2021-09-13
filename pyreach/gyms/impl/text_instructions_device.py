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

"""Implementation of PyReach Gym Vacuum Device."""

import sys
from typing import Dict, List, Optional, Tuple

import gym  # type: ignore
import numpy as np  # type: ignore

import pyreach
from pyreach import snapshot as lib_snapshot
from pyreach.gyms import core as gyms_core
from pyreach.gyms import text_instructions_element
from pyreach.gyms.impl import reach_device


class ReachDeviceTextInstructions(reach_device.ReachDevice):
  """Represents some text instructions.

  Attributes:
    action_space: An empty dictionary which is obviously ignored.
    observation_space: A Gym observation space with "ts" and "text" fields. The
      text field is a Gym MultiDiscrete space that is 1024 long with each
      element capable of holding in a value from 0-127.  The text instruction is
      encoded in UTF-8 and null padded to fill out the buffer.
    task_enable: Integer flag indicating if task is enabled.
  """

  def __init__(
      self,
      text_instructions_config: text_instructions_element.ReachTextInstructions
  ) -> None:
    """Init a Text Instruction element.

    Args:
      text_instructions_config: The text instructions configuration information.
    """
    reach_name: str = text_instructions_config.reach_name
    is_synchronous: bool = text_instructions_config.is_synchronous

    action_space: gym.spaces.Dict = gym.spaces.Dict({})
    observation_space: gym.spaces.Dict = gym.spaces.Dict({
        "ts": gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
        "instruction": gym.spaces.MultiDiscrete(1024 * [255]),
    })

    super().__init__(reach_name, action_space, observation_space,
                     is_synchronous)
    self._text_instruction: Optional[pyreach.TextInstruction] = None
    self._text_instructions: Optional[pyreach.TextInstructions] = None
    self._counter: int = 0
    self._task_enable: bool = False

  def __str__(self) -> str:
    """Return string representation of Arm."""
    return "ReachDeviceTextInstructions('{0}':'{1}')".format(
        self.config_name, self._reach_name)

  def get_observation(self,
                      host: pyreach.Host) -> reach_device.ObservationSnapshot:
    """Return the Reach Server Gym Observation as an empty Dict.

    Args:
      host: The host to get the observation from.

    Returns:
      Returns a Tuple containing the Gym Observation, a tuple of
      SnapshotReference objects and a tuple of SnapshotResponse objects.
      The TextInstructions Observation is a dictionary containing a "ts",
      "counter" and "instruction" value.  The counter is incremented each
      time a new instruction is received.  The "instruction" value is a
      1024 byte null padded array with encoded text instructions in UTF-8
      format.

    Raises:
      pyreach.PyReachError when there is not observation available.

    """
    with self._timers_select({"!agent*", "gym.text"}):
      last_text_instruction: Optional[pyreach.TextInstruction] = (
          self._text_instruction)
      text_instructions_device: pyreach.TextInstructions = (
          self._get_text_instructions_device(host))
      current_text_instruction: Optional[pyreach.TextInstruction]

      device: pyreach.TextInstructions = text_instructions_device
      with self._timers.select({"!agent*", "!gym*", "host.text"}):
        current_text_instruction = (
            device.fetch_text_instruction()
            if self._is_synchronous else device.text_instruction)

      instruction_bytes: List[int] = 1024 * [0]
      ts: float = 0.0
      seq: int = 0
      counter: int = self._counter

      if current_text_instruction:
        if last_text_instruction:
          if current_text_instruction.uid != last_text_instruction.uid:
            counter += 1
        else:
          counter += 1
        ts = gyms_core.Timestamp.new(current_text_instruction.time)
        seq = current_text_instruction.sequence

        self._text_instruction = current_text_instruction
        self._counter = counter

        instruction: str = current_text_instruction.instruction
        instruction_bytes = list(bytes(instruction, "utf-8"))[:1024]
        pad_size: int = 1024 - len(instruction_bytes)
        instruction_bytes.extend(pad_size * [0])

      observation: gyms_core.Observation = {
          "counter": counter,
          "ts": ts,
          "instruction": np.array(instruction_bytes),
      }
      return observation, (), (lib_snapshot.SnapshotResponse(
          counter, "text-instruction", self.config_name,
          lib_snapshot.SnapshotReference(ts, seq)),)

  def do_action(
      self, action: gyms_core.Action,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Start/stop the action.

    Args:
      action: The Gym Action Space to process as a Gym Dict Space with a
        "task_enable" field (0=End, 1=Start).
      host: The reach host to use.

    Returns:
        The list of gym action snapshots.
    """
    with self._timers_select({"!agent*", "gym.text"}):
      action_dict: gyms_core.ActionDict = self._get_action_dict(action)
      if "task_enable" in action_dict:
        task_enable: bool = bool(int(action_dict["task_enable"]))
        if self._task_enable != task_enable:
          # State needs to change.
          task_params: Dict[str, str] = self.get_task_params()
          if task_enable:
            # Send a start task message.
            host.logger.start_task(task_params)
          else:
            # Send an end task message.
            host.logger.end_task(task_params)
          self._task_enable = task_enable
          return (lib_snapshot.SnapshotGymLoggerAction("operator", "", False,
                                                       task_enable,
                                                       task_params),)
      return ()

  def start_observation(self, host: pyreach.Host) -> bool:
    """Start a synchronous observation."""
    return False

  # pylint: disable=unused-argument
  def reset(self,
            host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Called when the gym is reset."""
    if self._task_enable:
      task_params: Dict[str, str] = self.get_task_params()
      host.logger.end_task(task_params)
      self._task_enable = False
      self._executate_action_status = None
      self._prediction = 0
      return (lib_snapshot.SnapshotGymLoggerAction("operator", "", False, False,
                                                   task_params),)
    return ()

  def _get_text_instructions_device(
      self, host: pyreach.Host) -> pyreach.TextInstructions:
    """Return the pyreach.TextInstructions device."""
    if self._text_instructions is None:
      if host.text_instructions is None:
        raise pyreach.PyReachError(
            "Internal Error: There is no pyreach.TextInstructions "
            "configured for host.")
      self._text_instructions = host.text_instructions
    return self._text_instructions
