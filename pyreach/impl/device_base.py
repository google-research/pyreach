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

"""DeviceBase is the base class for all PyReach Device classes.

Device classes manage interaction with Reach devices. One Device instance
manages interaction with a single Reach device.

Each DeviceBase instance has its own thread pool that processes DeviceData
messages.
"""

import queue
import threading
from typing import Any, Callable, Dict, Optional, Set, Tuple
import dataclasses

from pyreach import core
from pyreach.common.python import types_gen
from pyreach.impl import thread_util


@dataclasses.dataclass(frozen=True)
class KeyValueKey:
  device_type: str
  device_name: str
  key: str


class DeviceBase:
  """DeviceBase is the base class for all Reach Devices.

  A Reach Device manages interaction with a single Reach device.

  Each Reach Device has an independent thread pool and manages key-value for
  the device to operate. By default, there is a single thread running in the
  pool: the DeviceData thread. This thread intercepts key-value messages and
  pass along DeviceData to the on_device_data function. The thread pool can
  be used for data streaming and other processing by the subclasses.

  The transport is provided by the set_send_cmd and enqueue_device_data
  functions. The set_send_cmd function is usually called at initialization.
  The enqueue_device_data function is called continuously by an external thread.
  """

  _condition: threading.Condition
  _thread_collection: thread_util.ThreadCollection
  _key_values: Dict[KeyValueKey, str]
  _key_value_lock: threading.Lock
  _send_cmd: Tuple[Optional[Callable[[types_gen.CommandData], None]]]
  _queue: "queue.Queue[Optional[types_gen.DeviceData]]"
  _closed: bool

  def __init__(self) -> None:
    """Construct a Device instance.

    The constructor initializes instance states and kickoff device data thread.
    """
    self._condition = threading.Condition()
    self._key_values = {}
    self._key_value_lock = threading.Lock()
    self._send_cmd = (None,)
    self._closed = False
    self._queue = queue.Queue()
    self._thread_collection = thread_util.ThreadCollection("Device")

  def _device_data_thread(self) -> None:
    """Read data from the queue."""
    active = True
    while active:
      try:
        msg = self._queue.get(block=True)
        if msg is None:
          active = False
        else:
          self.sync_device_data(msg)
      finally:
        self._queue.task_done()

  def flush(self) -> None:
    """Flush all data from the queues."""
    self._queue.join()

  def sync_device_data(self, msg: types_gen.DeviceData) -> None:
    """Process a device-data message.

    Args:
      msg: the message to process.
    """
    if msg.data_type == "key-value":
      key = KeyValueKey(
          device_type=msg.device_type,
          device_name=msg.device_name,
          key=msg.key)
      with self._key_value_lock:
        self._key_values[key] = msg.value
      self.on_set_key_value(key, msg.value)
    self.on_device_data(msg)

  def poll(self, period: float, f: "Callable[..., bool]", *args: Any,
           **kwargs: Any) -> None:
    """Poll a device periodically in the Device thread collection.

    Args:
      period: The period between function calls.
      f: The function to call.
      *args: The arguments to pass to the function.
      **kwargs: The keyword arguments to pass to the function.
    """
    self._thread_collection.poll(self.wait, period, f, *args, **kwargs)

  def run(self, f: "Callable[..., None]", *args: Any, **kwargs: Any) -> None:
    """Run a function thread in the Device thread collection.

    Args:
      f: The function to call.
      *args: The arguments to pass to the function.
      **kwargs: The keyword arguments to pass to the function.
    """
    self._thread_collection.run(f, *args, **kwargs)

  def get_key_values(self) -> Set[KeyValueKey]:
    """Return the key/values for a Device.

    Returns:
      Returns nothing by default. This function expects the subclass to return
    meaningful value.
    """
    return set()

  def get_key_value(self, key: KeyValueKey) -> Optional[str]:
    """Get the value associated with KeyValueKey.

    Args:
      key: The KeyValueKey to lookup.

    Returns:
      Returns a string upon success and None otherwise.
    """
    with self._key_value_lock:
      return self._key_values.get(key, None)

  # pylint: disable=unused-argument
  def on_set_key_value(self, key: KeyValueKey, value: str) -> None:
    """Invoke after a new key-value is just set.

    Args:
      key: The KeyValueKey to use.
      value: The value to set it to.
    """
    return

  def on_start(self) -> None:
    """Invoke when a device is started."""
    return

  def on_close(self) -> None:
    """Invoke when the device is closing at shutdown."""
    return

  def on_message(self, msg: types_gen.DeviceData) -> None:
    """Invoke when a device data message is received."""
    return

  def on_device_data(self, msg: types_gen.DeviceData) -> None:
    """Invoke when a device data is received.

    Args:
      msg: The DeviceData message that is received.
    """
    self.on_message(msg)

  def enqueue_device_data(self, msg: types_gen.DeviceData) -> None:
    """Enqueue a DeviceData message.

    This is supposed to be called by an external thread for injecting new
    DeviceData message into the queue.

    Args:
      msg: The DeviceData message.
    """
    self._queue.put(msg)

  def start(self) -> None:
    """Start the device."""
    self._thread_collection.start()
    self.run(self._device_data_thread)
    self.on_start()

  def set_send_cmd(self, cmd: Callable[[types_gen.CommandData], None]) -> None:
    """Set the command to use send a CommandData.

    Args:
        cmd: A function to call to send a command.
    """
    self._send_cmd = (cmd,)

  def send_cmd(self, msg: types_gen.CommandData) -> None:
    """Send CommandData to the host.

    Args:
      msg: The CommandData message to send.

    Raises:
      PyReachError if the send command function was not previously set.

    """
    if self._send_cmd[0] is None:
      raise core.PyReachError(
          "send_cmd used is not set - commands used before startup")
    self._send_cmd[0](msg)

  def close(self) -> None:
    """Close the device."""
    with self._condition:
      self._closed = True
      self._condition.notify_all()
    self._queue.put(None)
    self._thread_collection.join()
    self.on_close()

  def is_closed(self) -> bool:
    """Return whether the Device is closed."""
    with self._condition:
      return self._closed

  def wait(self, timeout: Optional[float]) -> bool:
    """Wait a while.

    Args:
      timeout: The amount to wait in seconds. Specifying 0 will check if the
        device is closed without waiting. Specifying None will wait until the
        device is closed.

    Returns:
      Returns True if the device is closed and False otherwise.
    """
    with self._condition:
      if self._closed:
        return True
      if timeout is None or timeout > 0.0:
        self._condition.wait(timeout=timeout)
      return self._closed
