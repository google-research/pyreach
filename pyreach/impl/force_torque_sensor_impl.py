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

"""Implementation of PyReach force torque interface."""

import logging  # type: ignore
from typing import Callable, Dict, Optional, Tuple

from pyreach import core
from pyreach.common.python import types_gen
from pyreach.force_torque_sensor import ForceTorqueSensor
from pyreach.force_torque_sensor import ForceTorqueSensorState
from pyreach.impl import requester
from pyreach.impl import thread_util
from pyreach.impl import utils


class ForceTorqueSensorDevice(requester.Requester[ForceTorqueSensorState]):
  """ForceTorqueSensor interacts with force torque sensor."""

  _device_name: str

  def __init__(self, device_name: str) -> None:
    """Initialize the device.

    Args:
      device_name: The name of the device.
    """
    super().__init__()
    self._device_name = device_name

  @property
  def device_name(self) -> str:
    """Return the force torque sensor device name."""
    return self._device_name

  def get_message_supplement(
      self, msg: types_gen.DeviceData) -> Optional[ForceTorqueSensorState]:
    """Get getting supplementary information for the request manager.

    Args:
      msg: device data message.

    Returns:
      Converted ForceTorqueSensorState object.
    """
    if (msg.device_type == "force-torque-sensor" and
        self._device_name == msg.device_name and
        msg.data_type == "sensor-state" and msg.state):
      states: Dict[str, float] = {}
      expect_states = {"fx", "fy", "fz", "tx", "ty", "tz"}
      for state in msg.state:
        states[state.pin] = state.float_value
        if state.pin not in expect_states:
          logging.warning("force-torque-sensor state for %s contains extra: %s",
                          self._device_name, state)
      for expect_state in expect_states:
        if expect_state not in states:
          logging.warning("force-torque-sensor state for %s is missing %s",
                          self._device_name, expect_state)
      return ForceTorqueSensorState(
          time=utils.time_at_timestamp(msg.ts),
          sequence=msg.seq,
          device_name=self._device_name,
          force=core.Force(
              states.get("fx", 0), states.get("fy", 0), states.get("fz", 0)),
          torque=core.Torque(
              states.get("tx", 0), states.get("ty", 0), states.get("tz", 0)))
    return None

  def get_wrapper(
      self) -> Tuple["ForceTorqueSensorDevice", "ForceTorqueSensor"]:
    """Get the wrapper for the device that should be shown to the user."""
    return self, ForceTorqueSensorImpl(self)


class ForceTorqueSensorImpl(ForceTorqueSensor):
  """Interface for interacting with a force torque sensor device."""

  _device: ForceTorqueSensorDevice

  def __init__(self, device: ForceTorqueSensorDevice) -> None:
    """Init a force torque sensor device.

    Args:
      device: The device for the force torque sensor.
    """
    self._device = device

  @property
  def device_name(self) -> str:
    """Return the force torque sensor device name."""
    return self._device.device_name

  @property
  def state(self) -> Optional[ForceTorqueSensorState]:
    """Return the latest force torque sensor state."""
    return self._device.get_cached()

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
    return self._device.add_update_callback(callback, finished_callback)

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
    data = thread_util.extract_all_from_queue(
        self._device.request_untagged(
            "force-torque-sensor",
            self._device.device_name,
            data_type="sensor-state",
            timeout=timeout))
    if not data:
      raise core.PyReachError("Timeout")
    if len(data) != 1:
      logging.warning("too much data returned for force torque sensor state")
    return data[0][1]

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
    self._device.queue_to_error_callback(
        self._device.request_untagged(
            "force-torque-sensor",
            self._device.device_name,
            data_type="sensor-state",
            timeout=timeout), callback, error_callback)

  def start_streaming(self, request_period: float = 0.1) -> None:
    """Start streaming of force torque sensor state.

    Args:
      request_period: The number of seconds between force torque sensor states.
        Defaults to .1 seconds between force torque sensor states.
    """
    self._device.set_untagged_request_period("force-torque-sensor",
                                             self._device.device_name,
                                             "sensor-state", request_period)

  def stop_streaming(self) -> None:
    """Stop streaming force torque sensor states."""
    self._device.set_untagged_request_period("force-torque-sensor",
                                             self._device.device_name,
                                             "sensor-state", None)
