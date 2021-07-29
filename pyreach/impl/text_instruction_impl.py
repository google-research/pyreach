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

"""Implementation of the PyReach TextInstruction interface."""
import logging  # type: ignore
from typing import Callable, Optional, Tuple

from pyreach import core
from pyreach import text_instruction
from pyreach.common.python import types_gen
from pyreach.impl import requester
from pyreach.impl import thread_util
from pyreach.impl import utils


class TextInstructionDevice(
    requester.Requester[text_instruction.TextInstruction]):
  """Represents the text instruction device."""

  def get_message_supplement(
      self,
      msg: types_gen.DeviceData) -> Optional[text_instruction.TextInstruction]:
    """Get getting supplementary information for the request manager.

    Args:
      msg: Device data message.

    Returns:
      Loads the TextInstruction from the message.
    """
    if (msg.device_type == "instruction-generator" and not msg.device_name and
        msg.data_type == "text-instruction" and msg.text_instruction):
      return text_instruction.TextInstruction(
          time=utils.time_at_timestamp(msg.ts),
          sequence=msg.seq,
          intent=msg.text_instruction.intent,
          success_type=msg.text_instruction.success_type,
          instruction=msg.text_instruction.instruction,
          success_detection=msg.text_instruction.success_detection,
          uid=msg.text_instruction.uid)
    return None

  def get_wrapper(
      self
  ) -> Tuple["TextInstructionDevice", "text_instruction.TextInstructions"]:
    """Get the wrapper for the device that should be shown to the user."""
    return self, TextInstructionImpl(self)


class TextInstructionImpl(text_instruction.TextInstructions):
  """Interface for text instructions."""

  _device: TextInstructionDevice

  def __init__(self, device: TextInstructionDevice):
    self._device = device

  def add_update_callback(
      self,
      callback: Callable[[text_instruction.TextInstruction], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback to be invoked when a new text instruction is available.

    Args:
      callback: function to be invoked when a new text instruction is available.
        Returns False to continue receiving new instructions. Returns True to
        stop further update.
      finished_callback: Optional callback, called when the callback is stopped
        or if the camera is closed.

    Returns:
      A function that when called stops the callback.
    """
    return self._device.add_update_callback(callback, finished_callback)

  def fetch_text_instruction(
      self,
      timeout: float = 15.0) -> Optional[text_instruction.TextInstruction]:
    """Fetch a the text instruction or possibly times out.

    Args:
      timeout: The number number of seconds to wait before timing out. This
        defaults to 15 seconds if not specified.

    Returns:
      Newly received text instruction.
    """
    q = self._device.send_tagged_request(
        types_gen.CommandData(
            device_type="instruction-generator",
            data_type="text-instruction-request",
            ts=utils.timestamp_now(),
            tag=utils.generate_tag()),
        timeout=timeout,
        expect_messages=1)
    msgs = thread_util.extract_all_from_queue(q)
    if not msgs:
      return None
    if (len(msgs) == 1 and msgs[0][0].data_type == "cmd-status" and
        (msgs[0][0].status in {"rejected", "aborted"} or msgs[0][0].error)):
      return None
    if len(msgs) != 2:
      logging.warning("expected a single message and status: %s", msgs)
    return msgs[0][1]

  def async_fetch_text_instruction(
      self,
      callback: Optional[Callable[[text_instruction.TextInstruction],
                                  None]] = None,
      error_callback: Optional[Callable[[core.PyReachStatus], None]] = None,
      timeout: float = 30) -> None:
    """Fetch a new text instruction asynchronously.

    The callback will be invoked when new text instruction is available.

    Args:
      callback: callback called when the instruction arrives. If the device
        fails to load an instruction, callback will not be called.
      error_callback: optional callback called if there is an error.
      timeout: timeout for the process, defaults to 30 seconds.
    """
    q = self._device.send_tagged_request(
        types_gen.CommandData(
            device_type="instruction-generator",
            data_type="text-instruction-request",
            ts=utils.timestamp_now(),
            tag=utils.generate_tag()),
        timeout=timeout,
        expect_messages=1)
    self._device.queue_to_error_callback(q, callback, error_callback)

  @property
  def text_instruction(self) -> Optional[text_instruction.TextInstruction]:
    """Return the latest text instruction if it exists."""
    return self._device.get_cached()
