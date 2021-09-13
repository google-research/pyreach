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

"""Interface for interacting with a vacuum device."""

from typing import Optional, Callable

from pyreach import core
from pyreach import vacuum


class VacuumMock(vacuum.Vacuum):
  """Interface for interacting with a vacuum device."""

  @property
  def device_name(self) -> str:
    """Return the Vacuum device name."""
    return ""

  @property
  def state(self) -> Optional[vacuum.VacuumState]:
    """Return the latest vacuum on-off state."""
    return vacuum.VacuumState(time=0.0, sequence=0, state=True)

  @property
  def blowoff_state(self) -> Optional[vacuum.BlowoffState]:
    """Return the latest blowoff on-off state."""
    return vacuum.BlowoffState(time=0.0, sequence=0, state=True)

  @property
  def pressure_state(self) -> Optional[vacuum.VacuumPressure]:
    """Return the latest vacuum pressure state."""
    return vacuum.VacuumPressure(time=0.0, sequence=0, state=True)

  @property
  def gauge_state(self) -> Optional[vacuum.VacuumGauge]:
    """Return the latest vacuum gauge state."""
    return vacuum.VacuumGauge(time=0.0, sequence=0, state=123.456)

  @property
  def support_blowoff(self) -> bool:
    """Return true if blowoff is supported."""
    return True

  @property
  def support_gauge(self) -> bool:
    """Return true if gauge is supported."""
    return True

  @property
  def support_pressure(self) -> bool:
    """Return true if pressure is supported."""
    return True

  def add_state_callback(
      self,
      callback: Callable[[vacuum.VacuumState], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback for vacuum state.

    Args:
      callback: Callback called when a new vacuum state arrives. The callback
        function should return False for continuous state update. When the
        callback function returns True, it will stop receiving future updates.
      finished_callback: Optional callback, called when the callback is stopped.

    Returns:
      A function that when called stops the callback.

    """
    raise NotImplementedError

  def add_blowoff_state_callback(
      self,
      callback: Callable[[vacuum.BlowoffState], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback for blowoff state.

    Args:
      callback: Callback called when a new blowoff state arrives. The callback
        function should return False for continuous state update. When the
        callback function returns True, it will stop receiving future updates.
      finished_callback: Optional callback, called when the callback is stopped.

    Returns:
      A function that when called stops the callback.

    """
    raise NotImplementedError

  def add_pressure_state_callback(
      self,
      callback: Callable[[vacuum.VacuumPressure], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback for vacuum pressure state.

    Args:
      callback: Callback called when a new vacuum state arrives. The callback
        function should return False for continuous state update. When the
        callback function returns True, it will stop receiving future updates.
      finished_callback: Optional callback, called when the callback is stopped.

    Raises:
      PyReachError: if pressure state is not supported.

    Returns:
      A function that when called stops the callback.

    """
    raise NotImplementedError

  def add_gauge_state_callback(
      self,
      callback: Callable[[vacuum.VacuumGauge], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback for vacuum gauge state.

    Args:
      callback: Callback called when a new vacuum gauge state arrives. The
        callback function should return False for continuous state update. When
        the callback function returns True, it will stop receiving future
        updates.
      finished_callback: Optional callback, called when the callback is stopped.

    Raises:
      PyReachError: if gauge state is not supported.

    Returns:
      A function that when called stops the callback.

    """
    raise NotImplementedError

  def on(self,
         intent: str = "",
         pick_id: str = "",
         success_type: str = "") -> core.PyReachStatus:
    """Turn the vacuum suction on.

    Args:
      intent: The intent of the command.
      pick_id: The pick_id of the command.
      success_type: The success_type of the command.

    Returns:
      Status of the command.

    """
    raise NotImplementedError

  def off(self,
          intent: str = "",
          pick_id: str = "",
          success_type: str = "") -> core.PyReachStatus:
    """Turn the vacuum suction off.

    Args:
      intent: The intent of the command.
      pick_id: The pick_id of the command.
      success_type: The success_type of the command.

    Returns:
      Status of the command.

    """
    return core.PyReachStatus(time=1.0, status="done")

  def blowoff(self,
              intent: str = "",
              pick_id: str = "",
              success_type: str = "") -> core.PyReachStatus:
    """Reverse the vacuum to force a release/clear.

    Args:
      intent: The intent of the command.
      pick_id: The pick_id of the command.
      success_type: The success_type of the command.

    Raises:
      PyReachError: if blowoff is not supported.

    Returns:
      Status of the command.

    """
    raise NotImplementedError

  def async_on(self,
               intent: str = "",
               pick_id: str = "",
               success_type: str = "",
               timeout: Optional[float] = None,
               callback: Optional[Callable[[core.PyReachStatus], None]] = None,
               finished_callback: Optional[Callable[[], None]] = None) -> None:
    """Turn the vacuum suction on, asynchronously.

    Args:
      intent: The intent of the command.
      pick_id: The pick_id of the command.
      success_type: The success_type of the command.
      timeout: The number of seconds to wait before giving up.
      callback: Optional callback with the status response. If the robot does
        not respond, will not be called.
      finished_callback: Optional callback when finished.
    """
    raise NotImplementedError

  def async_off(self,
                intent: str = "",
                pick_id: str = "",
                success_type: str = "",
                timeout: Optional[float] = None,
                callback: Optional[Callable[[core.PyReachStatus], None]] = None,
                finished_callback: Optional[Callable[[], None]] = None) -> None:
    """Turn the vacuum suction off, asynchronously.

    Args:
      intent: The intent of the command.
      pick_id: The pick_id of the command.
      success_type: The success_type of the command.
      timeout: The number of seconds to wait before giving up.
      callback: Optional callback with the status response. If the robot does
        not respond, will not be called.
      finished_callback: Optional callback when finished.
    """
    raise NotImplementedError

  def async_blowoff(
      self,
      intent: str = "",
      pick_id: str = "",
      success_type: str = "",
      timeout: Optional[float] = None,
      callback: Optional[Callable[[core.PyReachStatus], None]] = None,
      finished_callback: Optional[Callable[[], None]] = None,
  ) -> None:
    """Reverse the vacuum to force a release/clear, asynchronously.

    Args:
      intent: The intent of the command.
      pick_id: The pick_id of the command.
      success_type: The success_type of the command.
      timeout: The number of seconds to wait before giving up.
      callback: Optional callback with the status response. If the robot does
        not respond, will not be called.
      finished_callback: Optional callback when finished.

    Raises:
      PyReachError: if blowoff is not supported.

    """
    raise NotImplementedError

  def fetch_state(self, timeout: float = 15.0) -> vacuum.VacuumState:
    """Fetch a new vacuum state.

    Args:
      timeout: The number of seconds to wait before giving up.

    Raises:
      PyReachError: on timeout.

    Returns:
      Latest vacuum state.

    """
    return vacuum.VacuumState(time=0.0, sequence=0, state=True)

  def async_fetch_state(self,
                        callback: Optional[Callable[[vacuum.VacuumState],
                                                    None]] = None,
                        error_callback: Optional[Callable[[core.PyReachStatus],
                                                          None]] = None,
                        timeout: float = 15.0) -> None:
    """Fetch a new vacuum state asynchronously.

    Args:
      callback: Optional callback when a new vacuum state arrives.
      error_callback: Optional callback called if there is an error.
      timeout: The number of seconds to wait before giving up.
    """
    raise NotImplementedError

  def fetch_blowoff_state(self,
                          timeout: float = 15.0
                         ) -> Optional[vacuum.BlowoffState]:
    """Fetch a new blowoff state.

    Args:
      timeout: The number of seconds to wait before giving up.

    Raises:
      PyReachError: on timeout.

    Returns:
      Latest blowoff state.

    """
    return vacuum.BlowoffState(time=0.0, sequence=0, state=True)

  def async_fetch_blowoff_state(
      self,
      callback: Optional[Callable[[vacuum.BlowoffState], None]] = None,
      error_callback: Optional[Callable[[core.PyReachStatus], None]] = None,
      timeout: float = 15.0) -> None:
    """Fetch a new blowoff state asynchronously.

    Args:
      callback: Optional callback when a new blowoff state arrives.
      error_callback: Optional callback called if there is an error.
      timeout: The number of seconds to wait before giving up.
    """
    raise NotImplementedError

  def fetch_pressure_state(self,
                           timeout: float = 15.0) -> vacuum.VacuumPressure:
    """Fetch a new vacuum pressure state.

    Args:
      timeout: The number of seconds to wait before giving up.

    Raises:
      PyReachError: if pressure state is not supported or timeout.

    Returns:
      The latest pressure state.

    """
    return vacuum.VacuumPressure(time=0.0, sequence=0, state=True)

  def async_fetch_pressure_state(
      self,
      callback: Optional[Callable[[vacuum.VacuumPressure], None]] = None,
      error_callback: Optional[Callable[[core.PyReachStatus], None]] = None,
      timeout: float = 15.0) -> None:
    """Fetch a new vacuum pressure state asynchronously.

    Args:
      callback: Optional callback when a new pressure state arrives.
      error_callback: Optional callback called if there is an error.
      timeout: The number of seconds to wait before giving up.

    Raises:
      PyReachError: if pressure state is not supported.

    """
    raise NotImplementedError

  def fetch_gauge_state(self, timeout: float = 15.0) -> vacuum.VacuumGauge:
    """Fetch a new vacuum gauge state.

    Args:
      timeout: The number of seconds to wait before giving up.

    Raises:
      PyReachError: if gauge state is not supported or timeout.

    Returns:
      The latest vacuum gauge state.

    """
    return vacuum.VacuumGauge(time=0.0, sequence=0, state=123.456)

  def async_fetch_gauge_state(self,
                              callback: Optional[Callable[[vacuum.VacuumGauge],
                                                          None]] = None,
                              error_callback: Optional[Callable[
                                  [core.PyReachStatus], None]] = None,
                              timeout: float = 15.0) -> None:
    """Fetch a new vacuum gauge state asynchronously.

    Args:
      callback: Optional callback when a new gauge state arrives.
      error_callback: Optional callback called if there is an error.
      timeout: The number of seconds to wait before giving up.

    Raises:
      PyReachError: if gauge state is not supported.

    """
    raise NotImplementedError

  def start_streaming(self, request_period: float = 0.1) -> None:
    """Start streaming of vacuum output state.

    Args:
      request_period: The number of seconds between vacuum states. Defaults to
        .1 seconds between vacuum output states.
    """
    pass

  def stop_streaming(self) -> None:
    """Stop streaming vacuum output states."""
    raise NotImplementedError

  def start_blowoff_streaming(self, request_period: float = 0.1) -> None:
    """Start streaming of blowoff output state.

    Args:
      request_period: The number of seconds between blowoff states. Defaults to
        .1 seconds between blowoff output states.
    """
    pass

  def stop_blowoff_streaming(self) -> None:
    """Stop streaming blowoff output states."""
    raise NotImplementedError

  def start_gauge_streaming(self, request_period: float = 0.1) -> None:
    """Start streaming of blowoff output state.

    Args:
      request_period: The number of seconds between vacuum gauge states.
        Defaults to .1 seconds between vacuum gauge sensor states.
    """
    raise NotImplementedError

  def stop_gauge_streaming(self) -> None:
    """Stop streaming vacuum gauge states."""
    raise NotImplementedError

  def start_pressure_streaming(self, request_period: float = 0.1) -> None:
    """Start streaming of vacuum pressure states.

    Args:
      request_period: The number of seconds between vacuum pressure states.
        Defaults to .1 seconds between vacuum pressure sensor states.
    """
    raise NotImplementedError

  def stop_pressure_streaming(self) -> None:
    """Stop streaming vacuum pressure states."""
    raise NotImplementedError
