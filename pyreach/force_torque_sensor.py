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

"""Interface for interacting with the force torque sensor."""

from typing import Optional, Callable
import dataclasses

from pyreach import core


@dataclasses.dataclass(frozen=True)
class ForceTorqueSensorState:
  """Represents the state of the force torque sensor device.

  Attributes:
    time: The time when the state is measured.
    sequence: The sequence number of the force torque state.
    device_name: The name of the device.
    force: The force.
    torque: The torque.
  """

  time: float
  sequence: int
  device_name: str
  force: core.Force
  torque: core.Torque


class ForceTorqueSensor(object):
  """Interface for interacting with a force torque sensor device."""

  @property
  def device_name(self) -> str:
    """Return the force torque sensor device name."""
    raise NotImplementedError

  @property
  def state(self) -> Optional[ForceTorqueSensorState]:
    """Return the latest force torque sensor state."""
    raise NotImplementedError

  def add_update_callback(
      self,
      callback: Callable[[ForceTorqueSensorState], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback for force torque sensor state.

    Args:
      callback: Callback called when a new sensor state arrives. The callback
        function should return False for continuous state update. When the
        callback function returns True, it will stop receiving future updates.
      finished_callback: Optional callback, called when the callback is stopped.

    Returns:
      A function that when called stops the callback.

    """
    raise NotImplementedError

  def fetch_state(self,
                  timeout: float = 15.0) -> Optional[ForceTorqueSensorState]:
    """Fetch a new force torque sensor state.

    Args:
      timeout: The number of seconds to wait before giving up.

    Raises:
      PyReachError: if timeout.

    Returns:
      The latest sensor state.

    """
    raise NotImplementedError

  def async_fetch_state(self,
                        callback: Optional[Callable[[ForceTorqueSensorState],
                                                    None]] = None,
                        error_callback: Optional[Callable[[core.PyReachStatus],
                                                          None]] = None,
                        timeout: float = 15.0) -> None:
    """Fetch a new force torque sensor state asynchronously.

    Args:
      callback: Optional callback when a new force torque sensor state arrives.
      error_callback: Optional callback called if there is an error.
      timeout: The number of seconds to wait before giving up.
    """
    raise NotImplementedError
