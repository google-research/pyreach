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

"""Support Pipeline Descriptions."""

import logging
import threading
import time
from typing import Callable, List, Optional, Tuple
from pyreach.common.python import types_gen
from pyreach.impl import device_base
from pyreach.impl import machine_interfaces
from pyreach.impl import thread_util
from pyreach.impl import utils


class MachineInterfacesDevice(device_base.DeviceBase):
  """Gets and stores the machine interfaces of a connection."""
  _machine_interfaces_lock: threading.Lock
  _machine_interfaces: Optional[machine_interfaces.MachineInterfaces]
  _callbacks: thread_util.CallbackManager[Optional[
      machine_interfaces.MachineInterfaces]]

  def __init__(self) -> None:
    super().__init__()
    self._machine_interfaces_lock = threading.Lock()
    self._machine_interfaces = None
    self._callbacks = thread_util.CallbackManager()

  def add_update_callback(
      self,
      callback: Callable[[Optional[machine_interfaces.MachineInterfaces]],
                         bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback to the MachineInterfacesDevice.

    Args:
      callback: A function to be called whenever there is a new message.
      finished_callback: A function to be called when done.

    Returns:
      A function that when called stops the callback.
    """
    return self._callbacks.add_callback(callback, finished_callback)

  def on_start(self) -> None:
    """Start the state machine."""
    self.poll(15.0, self._request_pipeline)

  def get_wrapper(
      self) -> Tuple["MachineInterfacesDevice", "MachineInterfacesWrapper"]:
    """Gets the wrapper for the device that should be shown to the user."""
    return self, MachineInterfacesWrapper(self)

  def _request_pipeline(self) -> bool:
    """Request the pipeline from the server."""
    with self._machine_interfaces_lock:
      if self._machine_interfaces is not None:
        return True
    self.send_cmd(
        types_gen.CommandData(
            device_type="discovery-aggregator",
            ts=utils.timestamp_at_time(time.time()),
            tag=utils.generate_tag(),
            data_type="machine-interfaces-request"))
    return False

  def on_device_data(self, msg: types_gen.DeviceData) -> None:
    """Capture responses."""
    if msg.device_type != "discovery-aggregator":
      return
    if msg.device_name:
      return
    if msg.data_type != "machine-interfaces":
      return
    with self._machine_interfaces_lock:
      interfaces: List[machine_interfaces.MachineInterface] = []
      if msg.machine_interfaces is not None:
        for mi in msg.machine_interfaces.interfaces:
          try:
            interface_type = machine_interfaces.InterfaceType.from_string(
                mi.py_type)
          except ValueError:
            logging.warning("interface type invalid: %s", mi.to_json())
            continue
          interfaces.append(
              machine_interfaces.MachineInterface(
                  interface_type=interface_type,
                  device_type=mi.device_type,
                  device_name=mi.device_name,
                  data_type=mi.data_type,
                  keys=tuple(mi.keys.copy())))
      self._machine_interfaces = machine_interfaces.MachineInterfaces(
          time=utils.time_at_timestamp(msg.ts),
          machine_interfaces=tuple(interfaces))
    self._callbacks.call(self.get())

  def get(self) -> Optional[machine_interfaces.MachineInterfaces]:
    """Get gets the currently loaded MachineInterfaces."""
    with self._machine_interfaces_lock:
      return self._machine_interfaces

  def close(self) -> None:
    """Close the machine interface device."""
    self._callbacks.close()
    super().close()


class MachineInterfacesWrapper:
  """Wrapper for machine interfaces."""
  _device: MachineInterfacesDevice

  def __init__(self, device: "MachineInterfacesDevice"):
    self._device = device

  def get(self) -> Optional[machine_interfaces.MachineInterfaces]:
    """Get gets the currently loaded MachineInterfaces."""
    return self._device.get()

  def add_update_callback(
      self,
      callback: Callable[[Optional[machine_interfaces.MachineInterfaces]],
                         bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback to the MachineInterfacesDevice.

    Args:
      callback: A function to be called whenever there is a new message.
      finished_callback: A function to be called when done.

    Returns:
      A function that when called stops the callback.
    """
    return self._device.add_update_callback(callback, finished_callback)
