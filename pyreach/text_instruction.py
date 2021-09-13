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

"""Interface for interacting with text instructions."""

import dataclasses
from typing import Callable, Optional

from pyreach import core


@dataclasses.dataclass(frozen=True)
class TextInstruction:
  """A single text instruction.

  Attributes:
    time: The time in seconds of the instruction since 1970.
    sequence: The sequence number of the text instruction.
    intent: The intent of the instruction.
    success_type: The success_type of the instruction.
    instruction: The instruction string itself.
    success_detection: The method of success detection used.
    uid: The UID for the text instruction.
  """

  time: float
  sequence: int
  intent: str
  success_type: str
  instruction: str
  success_detection: str
  uid: str = ""


class TextInstructions(object):
  """Interface for a text instructions."""

  def add_update_callback(
      self,
      callback: Callable[[TextInstruction], bool],
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
    raise NotImplementedError

  def fetch_text_instruction(
      self, timeout: float = 15.0) -> Optional[TextInstruction]:
    """Fetch a the text instruction or possibly times out.

    Args:
      timeout: The number number of seconds to wait before timing out. This
        defaults to 15 seconds if not specified.
    """
    raise NotImplementedError

  def async_fetch_text_instruction(
      self,
      callback: Optional[Callable[[TextInstruction], None]] = None,
      error_callback: Optional[Callable[[core.PyReachStatus], None]] = None,
      timeout: float = 30) -> None:
    """Fetch a new text instruction asynchronously.

    The callback function will be invoked when new text instruction is
    available.

    Args:
      callback: callback called when the instruction arrives. If the device
        fails to load an instruction, callback will not be called.
      error_callback: optional callback called if there is an error.
      timeout: timeout for the process, defaults to 30 seconds.
    """
    raise NotImplementedError

  @property
  def text_instruction(self) -> Optional[TextInstruction]:
    """Return the latest text instruction if it exists."""
    raise NotImplementedError
