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

"""Implementation of PyReach Vacuum interface."""

import logging  # type: ignore
from typing import Callable, Optional, Tuple

from pyreach import core
from pyreach import vacuum
from pyreach.common.python import types_gen
from pyreach.impl import arm_impl
from pyreach.impl import machine_interfaces
from pyreach.impl import requester
from pyreach.impl import thread_util
from pyreach.impl import utils


class VacuumDevice(requester.Requester[None]):
  """VacuumDevice interacts with vacuum."""
  _arm: arm_impl.ArmImpl
  _vacuum_state: Optional[vacuum.VacuumState]
  _vacuum_state_callbacks: thread_util.CallbackManager[vacuum.VacuumState]
  _blowoff_state: Optional[vacuum.BlowoffState]
  _blowoff_state_callbacks: thread_util.CallbackManager[vacuum.BlowoffState]
  _vacuum_pressure_state: Optional[vacuum.VacuumPressure]
  _vacuum_pressure_state_callbacks: thread_util.CallbackManager[
      vacuum.VacuumPressure]
  _vacuum_gauge_state: Optional[vacuum.VacuumGauge]
  _vacuum_gauge_state_callbacks: thread_util.CallbackManager[vacuum.VacuumGauge]
  _support_blowoff: bool
  _support_gauge: bool
  _support_pressure: bool

  def __init__(self, interfaces: machine_interfaces.MachineInterfaces,
               arm: arm_impl.ArmImpl) -> None:
    have_vacuum = False
    have_blowoff = False
    have_gauge = False
    have_pressure = False
    for interface in interfaces.machine_interfaces:
      if interface.device_name != arm.device_name:
        continue
      if interface.interface_type not in {
          machine_interfaces.InterfaceType.PUBLISH,
          machine_interfaces.InterfaceType.FRAME_REQUEST,
          machine_interfaces.InterfaceType.STREAM_REQUEST
      }:
        continue
      if (interface.device_type == "vacuum" and
          interface.data_type == "output-state"):
        have_vacuum = True
      elif (interface.device_type == "blowoff" and
            interface.data_type == "output-state"):
        have_blowoff = True
      elif (interface.device_type == "vacuum-gauge" and
            interface.data_type == "sensor-state"):
        have_gauge = True
      elif (interface.device_type == "vacuum-pressure" and
            interface.data_type == "sensor-state"):
        have_pressure = True
    super().__init__()
    self.set_machine_interfaces(interfaces)
    if not have_vacuum:
      logging.error("Vacuum %s does not exist despite being in workcell IO",
                    arm.device_name)
    if arm.support_blowoff and not have_blowoff:
      logging.error(
          "Vacuum %s does not have blowoff state despite being in workcell IO",
          arm.device_name)
    self._arm = arm
    self._vacuum_state = None
    self._vacuum_state_callbacks = thread_util.CallbackManager()
    self._blowoff_state = None
    self._blowoff_state_callbacks = thread_util.CallbackManager()
    self._vacuum_pressure_state = None
    self._vacuum_pressure_state_callbacks = thread_util.CallbackManager()
    self._vacuum_gauge_state = None
    self._vacuum_gauge_state_callbacks = thread_util.CallbackManager()
    self._support_blowoff = arm.support_blowoff
    self._support_gauge = have_gauge
    self._support_pressure = have_pressure

  def vacuum_gauge_state_callbacks(
      self) -> thread_util.CallbackManager[vacuum.VacuumGauge]:
    """Return the vacuum gauge state callback manager."""
    return self._vacuum_gauge_state_callbacks

  def vacuum_pressure_state_callbacks(
      self) -> thread_util.CallbackManager[vacuum.VacuumPressure]:
    """Return the vacuum pressure state callback manager."""
    return self._vacuum_pressure_state_callbacks

  def vacuum_state_callbacks(
      self) -> thread_util.CallbackManager[vacuum.VacuumState]:
    """Return the vacuum state callback manager."""
    return self._vacuum_state_callbacks

  def blowoff_state_callbacks(
      self) -> thread_util.CallbackManager[vacuum.BlowoffState]:
    """Return the blowoff state callback manager."""
    return self._blowoff_state_callbacks

  def support_gauge(self) -> bool:
    """Return True if gauge is supported."""
    return self._support_gauge

  def support_blowoff(self) -> bool:
    """Return True if gauge is supported."""
    return self._support_blowoff

  def support_pressure(self) -> bool:
    """Return True if gauge is supported."""
    return self._support_pressure

  def vacuum_state(self) -> Optional[vacuum.VacuumState]:
    """Return the vacuum state."""
    return self._vacuum_state

  def blowoff_state(self) -> Optional[vacuum.BlowoffState]:
    """Return the blowoff state."""
    return self._blowoff_state

  def vacuum_pressure_state(self) -> Optional[vacuum.VacuumPressure]:
    """Return the vacuum pressure state."""
    return self._vacuum_pressure_state

  def vacuum_gauge_state(self) -> Optional[vacuum.VacuumGauge]:
    """Return the vacuum gauge state."""
    return self._vacuum_gauge_state

  def get_wrapper(self) -> Tuple["VacuumDevice", "vacuum.Vacuum"]:
    """Get the wrapper for the device that should be shown to the user."""
    return self, VacuumImpl(self, self._arm)

  def on_device_data(self, msg: types_gen.DeviceData) -> None:
    super().on_device_data(msg)
    if (msg.device_type == "vacuum" and
        msg.device_name == self._arm.device_name and
        msg.data_type == "output-state"):
      self._vacuum_state = vacuum.VacuumState(
          utils.time_at_timestamp(msg.ts), msg.seq,
          self.extract_bool_value(msg))
      self._vacuum_state_callbacks.call(self._vacuum_state)
    elif (msg.device_type == "blowoff" and
          msg.device_name == self._arm.device_name and
          msg.data_type == "output-state"):
      self._blowoff_state = vacuum.BlowoffState(
          utils.time_at_timestamp(msg.ts), msg.seq,
          self.extract_bool_value(msg))
      self._blowoff_state_callbacks.call(self._blowoff_state)
    if (msg.device_type == "vacuum-pressure" and
        msg.device_name == self._arm.device_name and
        msg.data_type == "sensor-state"):
      self._vacuum_pressure_state = vacuum.VacuumPressure(
          utils.time_at_timestamp(msg.ts), msg.seq,
          self.extract_bool_value(msg))
      self._vacuum_pressure_state_callbacks.call(self._vacuum_pressure_state)
    if (msg.device_type == "vacuum-gauge" and
        msg.device_name == self._arm.device_name and
        msg.data_type == "sensor-state"):
      self._vacuum_gauge_state = vacuum.VacuumGauge(
          utils.time_at_timestamp(msg.ts), msg.seq,
          self.extract_float_value(msg))
      self._vacuum_gauge_state_callbacks.call(self._vacuum_gauge_state)

  def extract_bool_value(self, msg: types_gen.DeviceData) -> bool:
    """Extract bool value from device data.

    Args:
      msg: message contains bool value based on state[0].int_value.

    Returns:
      True if the value is treated as bool.
    """
    if msg.state:
      return msg.state[0].int_value == 1
    return False

  def extract_float_value(self, msg: types_gen.DeviceData) -> float:
    """Extract float value from device data.

    Args:
      msg: message contains float value based on state[0].float_value.

    Returns:
      True if the value is treated as bool.
    """
    if msg.state:
      return msg.state[0].float_value
    return 0.0


class VacuumImpl(vacuum.Vacuum):
  """Represent a Vacuum effector for a robot."""

  _arm: arm_impl.ArmImpl

  def __init__(self, device: VacuumDevice, arm: arm_impl.ArmImpl) -> None:
    """Init an Arm vacuum effector.

    Args:
      device: The device for the vacuum.
      arm: The arm the vacuum effector is attached to.
    """
    self._device = device
    self._arm = arm

  @property
  def device_name(self) -> str:
    """Return the Arm name."""
    return self._arm.device_name

  @property
  def state(self) -> Optional[vacuum.VacuumState]:
    """Return the vacuum state."""
    return self._device.vacuum_state()

  @property
  def blowoff_state(self) -> Optional[vacuum.BlowoffState]:
    """Return the blowoff state."""
    return self._device.blowoff_state()

  @property
  def pressure_state(self) -> Optional[vacuum.VacuumPressure]:
    """Return the vacuum pressure state."""
    return self._device.vacuum_pressure_state()

  @property
  def gauge_state(self) -> Optional[vacuum.VacuumGauge]:
    """Return the vacuum gauge."""
    return self._device.vacuum_gauge_state()

  @property
  def support_blowoff(self) -> bool:
    """Return true if blowoff is supported."""
    return self._device.support_blowoff()

  @property
  def support_gauge(self) -> bool:
    """Return true if gauge is supported."""
    return self._device.support_gauge()

  @property
  def support_pressure(self) -> bool:
    """Return true if pressure is supported."""
    return self._device.support_pressure()

  def add_state_callback(
      self,
      callback: Callable[[vacuum.VacuumState], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback for vacuum states.

    Args:
      callback: Callback called when a vacuum state arrives. If it returns True,
        the callback will be stopped.
      finished_callback: Optional callback, called when the callback is stopped
        or if the vacuum state monitor is closed.

    Returns:
      A function that when called stops the callback.

    """
    return self._device.vacuum_state_callbacks().add_callback(
        callback, finished_callback)

  def add_blowoff_state_callback(
      self,
      callback: Callable[[vacuum.BlowoffState], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback for blowoff states.

    Args:
      callback: Callback called when a blowoff state arrives. If it returns
        True, the callback will be stopped.
      finished_callback: Optional callback, called when the callback is stopped
        or if the blowoff state monitor is closed.

    Returns:
      A function that when called stops the callback.

    """
    return self._device.blowoff_state_callbacks().add_callback(
        callback, finished_callback)

  def add_pressure_state_callback(
      self,
      callback: Callable[[vacuum.VacuumPressure], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback for vacuum pressure states.

    Args:
      callback: Callback called when a vacuum presure state arrives. If it
        returns True, the callback will be stopped.
      finished_callback: Optional callback, called when the callback is stopped
        or if the vacuum pressure state monitor is closed.

    Raises:
      PyReachError: if pressure state is not supported.

    Returns:
      A function that when called stops the callback.

    """
    if not self.support_pressure:
      raise core.PyReachError("pressure is not supported")
    return self._device.vacuum_pressure_state_callbacks().add_callback(
        callback, finished_callback)

  def add_gauge_state_callback(
      self,
      callback: Callable[[vacuum.VacuumGauge], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback for vacuum gauge states.

    Args:
      callback: Callback called when a vacuum gauge state arrives. If it returns
        True, the callback will be stopped.
      finished_callback: Optional callback, called when the callback is stopped
        or if the vacuum state monitor is closed.

    Raises:
      PyReachError: if gauge state is not supported.

    Returns:
      A function that when called stops the callback.

    """
    if not self.support_gauge:
      raise core.PyReachError("gauge is not supported")
    return self._device.vacuum_gauge_state_callbacks().add_callback(
        callback, finished_callback)

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
    result = self._arm.set_vacuum_state(arm_impl.ActionVacuumState.VACUUM,
                                        intent, pick_id, success_type)
    if result is None:
      return core.PyReachStatus(
          utils.timestamp_now(), status="rejected", error="timeout")
    return result

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
    result = self._arm.set_vacuum_state(arm_impl.ActionVacuumState.OFF, intent,
                                        pick_id, success_type)
    if result is None:
      return core.PyReachStatus(
          utils.timestamp_now(), status="rejected", error="timeout")

    return result

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
    if not self.support_blowoff:
      raise core.PyReachError("blowoff is not supported")
    result = self._arm.set_vacuum_state(arm_impl.ActionVacuumState.BLOWOFF,
                                        intent, pick_id, success_type)
    if result is None:
      return core.PyReachStatus(
          utils.timestamp_now(), status="rejected", error="timeout")

    return result

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
      timeout: the timeout for the call, defaults to no timeout.
      callback: callback called with the status response. If the robot does not
        respond, will not be called.
      finished_callback: callback called after operation is completed.
    """
    self._arm.async_set_vacuum_state(arm_impl.ActionVacuumState.VACUUM, intent,
                                     pick_id, success_type, "", timeout,
                                     callback, finished_callback)

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
      timeout: the timeout for the call, defaults to no timeout.
      callback: callback called with the status response. If the robot does not
        respond, will not be called.
      finished_callback: callback called after operation is completed.
    """
    self._arm.async_set_vacuum_state(arm_impl.ActionVacuumState.OFF, intent,
                                     pick_id, success_type, "", timeout,
                                     callback, finished_callback)

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
      timeout: the timeout for the call, defaults to no timeout.
      callback: callback called with the status response. If the robot does not
        respond, will not be called.
      finished_callback: callback called after operation is completed.

    Raises:
      PyReachError: if blowoff is not supported.

    """
    if not self.support_blowoff:
      raise core.PyReachError("blowoff is not supported")
    self._arm.async_set_vacuum_state(arm_impl.ActionVacuumState.BLOWOFF, intent,
                                     pick_id, success_type, "", timeout,
                                     callback, finished_callback)

  def fetch_state(self, timeout: float = 15.0) -> vacuum.VacuumState:
    """Fetch a new vacuum state.

    Args:
      timeout: The number of seconds to wait before giving up.

    Raises:
      PyReachError: on timeout.

    Returns:
      Latest vacuum state.

    """
    data = thread_util.extract_all_from_queue(
        self._device.request_untagged(
            "vacuum",
            self.device_name,
            data_type="output-state",
            timeout=timeout))
    if not data:
      raise core.PyReachError("Timeout")
    if len(data) != 1:
      logging.warning("too much data returned for vacuum state")
    return vacuum.VacuumState(
        utils.time_at_timestamp(data[0][0].ts), data[0][0].seq,
        self._device.extract_bool_value(data[0][0]))

  def async_fetch_state(self,
                        callback: Optional[Callable[[vacuum.VacuumState],
                                                    None]] = None,
                        error_callback: Optional[Callable[[core.PyReachStatus],
                                                          None]] = None,
                        timeout: float = 15.0) -> None:
    """Async fetch the state.

    Args:
      callback: The callback for the call.
      error_callback: Optional callback called if there is an error.
      timeout: The timeout for the call.
    """

    # pylint: disable=unused-argument
    def transform(msg: types_gen.DeviceData,
                  supplement: None) -> Optional[vacuum.VacuumState]:
      if msg.data_type == "output-state":
        return vacuum.VacuumState(
            utils.time_at_timestamp(msg.ts), msg.seq,
            self._device.extract_bool_value(msg))
      return None

    self._device.queue_to_error_callback_transform(
        self._device.request_untagged(
            "vacuum",
            self.device_name,
            data_type="output-state",
            timeout=timeout), callback, error_callback, transform)

  def fetch_blowoff_state(self, timeout: float = 15.0) -> vacuum.BlowoffState:
    """Fetch a new blowoff state.

    Args:
      timeout: The number of seconds to wait before giving up.

    Raises:
      PyReachError: on timeout.

    Returns:
      Latest blowoff state.

    """
    data = thread_util.extract_all_from_queue(
        self._device.request_untagged(
            "blowoff",
            self.device_name,
            data_type="output-state",
            timeout=timeout))
    if not data:
      raise core.PyReachError("Timeout")
    if len(data) != 1:
      logging.warning("too much data returned for blowoff state")
    return vacuum.BlowoffState(
        utils.time_at_timestamp(data[0][0].ts), data[0][0].seq,
        self._device.extract_bool_value(data[0][0]))

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

    # pylint: disable=unused-argument
    def transform(msg: types_gen.DeviceData,
                  supplement: None) -> Optional[vacuum.BlowoffState]:
      if msg.data_type == "output-state":
        return vacuum.BlowoffState(
            utils.time_at_timestamp(msg.ts), msg.seq,
            self._device.extract_bool_value(msg))
      return None

    self._device.queue_to_error_callback_transform(
        self._device.request_untagged(
            "blowoff",
            self.device_name,
            data_type="output-state",
            timeout=timeout), callback, error_callback, transform)

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
    if not self.support_pressure:
      raise core.PyReachError("pressure is not supported")
    data = thread_util.extract_all_from_queue(
        self._device.request_untagged(
            "vacuum-pressure",
            self.device_name,
            data_type="sensor-state",
            timeout=timeout))
    if not data:
      raise core.PyReachError("Timeout")
    if len(data) != 1:
      logging.warning("too much data returned for vacuum state")
    return vacuum.VacuumPressure(
        utils.time_at_timestamp(data[0][0].ts), data[0][0].seq,
        self._device.extract_bool_value(data[0][0]))

  def async_fetch_pressure_state(
      self,
      callback: Optional[Callable[[vacuum.VacuumPressure], None]] = None,
      error_callback: Optional[Callable[[core.PyReachStatus], None]] = None,
      timeout: float = 15.0) -> None:
    """Async fetch the vacuum pressure state.

    Args:
      callback: The callback for the call.
      error_callback: Optional callback called if there is an error.
      timeout: The timeout for the call.

    Raises:
      PyReachError: if pressure state is not supported.
    """
    if not self.support_pressure:
      raise core.PyReachError("pressure is not supported")

    # pylint: disable=unused-argument
    def transform(msg: types_gen.DeviceData,
                  supplement: None) -> Optional[vacuum.VacuumPressure]:
      if msg.data_type == "sensor-state":
        return vacuum.VacuumPressure(
            utils.time_at_timestamp(msg.ts), msg.seq,
            self._device.extract_bool_value(msg))
      return None

    self._device.queue_to_error_callback_transform(
        self._device.request_untagged(
            "vacuum-pressure",
            self.device_name,
            data_type="sensor-state",
            timeout=timeout), callback, error_callback, transform)

  def fetch_gauge_state(self, timeout: float = 15.0) -> vacuum.VacuumGauge:
    """Fetch the vacuum gauge state.

    Args:
      timeout: The number of seconds to wait before giving up.

    Raises:
      PyReachError: if gauge state is not supported or timeout.

    Returns:
      The latest vacuum gauge state.

    """
    if not self.support_gauge:
      raise core.PyReachError("gauge is not supported")
    data = thread_util.extract_all_from_queue(
        self._device.request_untagged(
            "vacuum-gauge",
            self.device_name,
            data_type="sensor-state",
            timeout=timeout))
    if not data:
      raise core.PyReachError("Timeout")
    if len(data) != 1:
      logging.warning("too much data returned for vacuum state")
    return vacuum.VacuumGauge(
        utils.time_at_timestamp(data[0][0].ts), data[0][0].seq,
        self._device.extract_float_value(data[0][0]))

  def async_fetch_gauge_state(self,
                              callback: Optional[Callable[[vacuum.VacuumGauge],
                                                          None]] = None,
                              error_callback: Optional[Callable[
                                  [core.PyReachStatus], None]] = None,
                              timeout: float = 15.0) -> None:
    """Fetch a new vacuum gauge state asynchronously.

    Args:
      callback: The callback for the call.
      error_callback: Optional callback called if there is an error.
      timeout: The number of seconds to wait before giving up.

    Raises:
      PyReachError: if gauge state is not supported.

    """
    if not self.support_gauge:
      raise core.PyReachError("gauge is not supported")

    # pylint: disable=unused-argument
    def transform(msg: types_gen.DeviceData,
                  supplement: None) -> Optional[vacuum.VacuumGauge]:
      if msg.data_type == "sensor-state":
        return vacuum.VacuumGauge(
            utils.time_at_timestamp(msg.ts), msg.seq,
            self._device.extract_float_value(msg))
      return None

    self._device.queue_to_error_callback_transform(
        self._device.request_untagged(
            "vacuum-gauge",
            self.device_name,
            data_type="sensor-state",
            timeout=timeout), callback, error_callback, transform)

  def start_streaming(self, request_period: float = 0.1) -> None:
    """Start streaming of vacuum output state.

    Args:
      request_period: The number of seconds between vacuum states. Defaults to
        .1 seconds between vacuum output states.
    """
    self._device.set_untagged_request_period("vacuum", self.device_name,
                                             "output-state", request_period)

  def stop_streaming(self) -> None:
    """Stop streaming vacuum output states."""
    self._device.set_untagged_request_period("vacuum", self.device_name,
                                             "output-state", None)

  def start_blowoff_streaming(self, request_period: float = 0.1) -> None:
    """Start streaming of blowoff output state.

    Args:
      request_period: The number of seconds between blowoff states. Defaults to
        .1 seconds between blowoff output states.
    """
    if not self.support_blowoff:
      raise core.PyReachError("blowoff is not supported")
    self._device.set_untagged_request_period("blowoff", self.device_name,
                                             "output-state", request_period)

  def stop_blowoff_streaming(self) -> None:
    """Stop streaming blowoff output states."""
    if not self.support_blowoff:
      raise core.PyReachError("blowoff is not supported")
    self._device.set_untagged_request_period("blowoff", self.device_name,
                                             "output-state", None)

  def start_gauge_streaming(self, request_period: float = 0.1) -> None:
    """Start streaming of blowoff output state.

    Args:
      request_period: The number of seconds between vacuum gauge states.
        Defaults to .1 seconds between vacuum gauge sensor states.
    """
    if not self.support_gauge:
      raise core.PyReachError("gauge is not supported")
    self._device.set_untagged_request_period("vacuum-gauge", self.device_name,
                                             "sensor-state", request_period)

  def stop_gauge_streaming(self) -> None:
    """Stop streaming vacuum gauge states."""
    if not self.support_gauge:
      raise core.PyReachError("gauge is not supported")
    self._device.set_untagged_request_period("vacuum-gauge", self.device_name,
                                             "sensor-state", None)

  def start_pressure_streaming(self, request_period: float = 0.1) -> None:
    """Start streaming of vacuum pressure states.

    Args:
      request_period: The number of seconds between vacuum pressure states.
        Defaults to .1 seconds between vacuum pressure sensor states.
    """
    if not self.support_pressure:
      raise core.PyReachError("pressure is not supported")
    self._device.set_untagged_request_period("vacuum-pressure",
                                             self.device_name, "sensor-state",
                                             request_period)

  def stop_pressure_streaming(self) -> None:
    """Stop streaming vacuum pressure states."""
    if not self.support_pressure:
      raise core.PyReachError("pressure is not supported")
    self._device.set_untagged_request_period("vacuum-pressure",
                                             self.device_name, "sensor-state",
                                             None)
