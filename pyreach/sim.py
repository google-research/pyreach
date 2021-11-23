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
"""Interface for controlling the reach sim console."""

from typing import Callable, Optional

from pyreach import core


class Sim(object):
  """Interface for controlling the reach sim console."""

  def reset(self, timeout: Optional[float] = None) -> core.PyReachStatus:
    """Reset resets the simulator.

    Args:
      timeout: The time in seconds to wait for the simulator reset.

    Returns:
      PyReachStatus representing the result of the command.
    """
    raise NotImplementedError

  def async_reset(self,
                  callback: Optional[Callable[[core.PyReachStatus],
                                              None]] = None,
                  finished_callback: Optional[Callable[[], None]] = None,
                  timeout: Optional[float] = None) -> None:
    """Asynchronously reset the simulator.

    Args:
      callback: callback when message is delivered.
      finished_callback: called when the reset is finished.
      timeout: The time in seconds to wait for the simulator reset.
    """
    raise NotImplementedError
