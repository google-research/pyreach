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

"""ReachHost manages low level communication with a Reach Host."""

import queue
import threading
import time
from typing import List, Dict, Optional, Tuple, Set, TypeVar, Callable

from pyreach import host
from pyreach.common.python import types_gen
from pyreach.core import PyReachError
from pyreach.impl import client as cli
from pyreach.impl import device_base
from pyreach.impl import machine_interfaces
from pyreach.impl import thread_util
from pyreach.impl import utils

T = TypeVar("T")


class Ping(device_base.DeviceBase):
  """Device that manages Ping request."""

  _send_ts: Optional[int]
  _send_tag: Optional[str]
  _ping_time: Optional[float]
  _server_offset_time: Optional[float]
  _server_offset_time_store: List[float]
  _lock: threading.Lock

  def __init__(self) -> None:
    """Construct a ping device."""
    super().__init__()
    self._send_ts = None
    self._send_tag = None
    self._ping_time = None
    self._server_offset_time = None
    self._server_offset_time_store = []
    self._lock = threading.Lock()

  def on_start(self) -> None:
    """Invoke when ping device is started."""
    self.poll(1.0, self._on_poll)

  def _on_poll(self) -> bool:
    with self._lock:
      if self._send_ts is not None:
        if self._send_tag is None:
          if utils.timestamp_now() - self._send_ts < 1000:
            return False
        else:
          if utils.timestamp_now() - self._send_ts < 15000:
            return False
      self._send_ts = utils.timestamp_now()
      self._send_tag = utils.generate_tag()
      self.send_cmd(
          types_gen.CommandData(
              ts=self._send_ts,
              device_type="ping",
              data_type="ping",
              tag=self._send_tag))
    return False

  def on_message(self, data: types_gen.DeviceData) -> None:
    """Invoke when a device data message is received."""
    with self._lock:
      if self._send_tag and self._send_ts and self._send_tag == data.tag:
        # Read the receive timestamp as either the current clock value, or the
        # local_ts if the device data has a local_ts value which stores the
        # receive time upstream of PyReach, improving calculation accuracy.
        recv_ts = utils.timestamp_now()
        if data.local_ts <= 0:
          recv_ts = data.local_ts
        estimated_server_ts = int((recv_ts + self._send_ts) / 2)
        server_offset_time = (data.ts - estimated_server_ts) / 1000.0
        self._server_offset_time_store.append(server_offset_time)
        while len(self._server_offset_time_store) > 120:
          self._server_offset_time_store = self._server_offset_time_store[1:]
        self._server_offset_time = (
            sum(self._server_offset_time_store) /
            len(self._server_offset_time_store))
        self._ping_time = (self._send_ts - recv_ts) / 1000.0
        self._send_tag = None

  def get_ping_time(self) -> Optional[float]:
    """Return the latest ping time."""
    with self._lock:
      return self._ping_time

  def get_server_offset_time(self) -> Optional[float]:
    """Return the offset to the server time.

    Returns:
      The offset to the server-side time, or None if it could not be computed.
    """
    with self._lock:
      return self._server_offset_time


class SessionManager(device_base.DeviceBase):
  """A class manages a session with the client."""

  _lock: threading.Lock
  _state: host.SessionState
  _last_request: Optional[float]
  _last_request_start: Optional[float]
  _last_request_end: Optional[float]
  _should_take_control: bool
  _should_release_control: bool
  _callback_manager: "thread_util.CallbackManager[host.SessionState]"

  def __init__(self, should_take_control: bool,
               should_release_control: bool) -> None:
    """Init the SessionManager.

    Args:
      should_take_control: If true, will try to start a control session.
      should_release_control: If true, will force release of control session.
    """
    super().__init__()
    self._lock = threading.Lock()
    self._state = host.SessionState.UNKNOWN
    self._last_request = None
    self._last_request_start = None
    self._last_request_end = None
    self._should_take_control = should_take_control
    self._should_release_control = should_release_control
    self._callback_manager = thread_util.CallbackManager()

  def on_start(self) -> None:
    """Invoke on startup."""
    self.poll(1.0, self._on_poll)

  def _on_poll(self) -> bool:
    """Manage session state updates and requests for session states."""
    with self._lock:
      if self._state == host.SessionState.SHUTDOWN:
        return False
      if self._state == host.SessionState.UNKNOWN:
        if not self._last_request or (time.time() - self._last_request) > 15:
          self._last_request = time.time()
          self.send_cmd(
              types_gen.CommandData(
                  ts=utils.timestamp_at_time(self._last_request),
                  device_type="session-manager",
                  data_type="connected-clients-request"))
      elif (self._should_take_control and
            (self._state == host.SessionState.EVICTABLE or
             self._state == host.SessionState.INACTIVE)):
        if (not self._last_request_start or
            (time.time() - self._last_request_start) > 15):
          self._last_request_start = time.time()
          self.send_cmd(
              types_gen.CommandData(
                  ts=utils.timestamp_at_time(self._last_request_start),
                  device_type="operator",
                  data_type="session-info",
                  session_info=types_gen.SessionInfo()))
      elif ((not self._should_take_control) and self._should_release_control and
            self._state == host.SessionState.ACTIVE):
        if (not self._last_request_end or
            (time.time() - self._last_request_end) > 15):
          self._last_request_end = time.time()
          self.send_cmd(
              types_gen.CommandData(
                  ts=utils.timestamp_at_time(self._last_request_end),
                  device_type="session-info",
                  data_type="session-info",
                  session_info=types_gen.SessionInfo()))
    return False

  def set_should_take_control(self, should_take_control: bool,
                              should_release_control: bool) -> None:
    """Set the take control flag of the SessionManager.

    Args:
      should_take_control: If true, will try to start a control session.
      should_release_control: If true, will force release of control session.
    """
    with self._lock:
      if (self._should_take_control != should_take_control or
          self._should_release_control != should_release_control):
        self._last_request_start = None
        self._last_request_end = None
      self._should_take_control = should_take_control
      self._should_release_control = should_release_control
    self._on_poll()

  def get_session_state(self) -> host.SessionState:
    """Get the session state of the host.

    Returns:
      The session state.
    """
    with self._lock:
      return self._state

  def wait_state(self,
                 state: host.SessionState,
                 timeout: Optional[float] = None) -> bool:
    """Wait for a specific state."""
    q: "queue.Queue[bool]" = queue.Queue()

    def cb(current_state: host.SessionState) -> bool:
      if state == current_state:
        q.put(True)
        return True
      return False

    def fcb() -> None:
      q.put(False)

    stop = self.add_update_callback(cb, fcb)

    if self.get_session_state() == state:
      stop()
      return True

    try:
      s = q.get(block=True, timeout=timeout)
    except queue.Empty:
      s = False

    stop()
    return s

  def on_message(self, msg: types_gen.DeviceData) -> None:
    """Process DeviceData when it is received.

    Args:
      msg: The Device Data to process.
    """
    if (msg.device_type != "session-manager" or msg.device_name or
        msg.data_type != "connected-clients"):
      return
    if msg.connected_clients is None:
      return
    update_state: Optional[host.SessionState] = None
    with self._lock:
      if self._state == host.SessionState.SHUTDOWN:
        return
      start_state = self._state
      current_index: Optional[int] = None
      session_index: Optional[int] = None
      i = 0
      for client in msg.connected_clients.clients:
        if current_index is None and client.is_current:
          current_index = i
        if session_index is None and client.control_session_active:
          session_index = i
        i += 1
      if current_index is None:
        self._state = host.SessionState.UNKNOWN
      else:
        if session_index is None:
          self._state = host.SessionState.INACTIVE
        elif session_index < current_index:
          self._state = host.SessionState.BLOCKED
        elif session_index > current_index:
          self._state = host.SessionState.EVICTABLE
        else:
          self._state = host.SessionState.ACTIVE
      if self._state != start_state:
        update_state = self._state
    self._on_poll()
    if update_state:
      self._callback_manager.call(update_state)

  def add_update_callback(
      self,
      callback: Callable[[host.SessionState], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback when new data is received.

    Args:
      callback: triggers when new data is received.
      finished_callback: triggers when update is finished.

    Returns:
      Returns a function when called stops the callback.
    """
    return self._callback_manager.add_callback(callback, finished_callback)

  def on_close(self) -> None:
    """Invoke when the system is closed."""
    with self._lock:
      self._state = host.SessionState.SHUTDOWN
    self._callback_manager.call(host.SessionState.SHUTDOWN)
    self._callback_manager.close()


class KeyValueReader(device_base.DeviceBase):
  """Reads a key value of the robot."""
  _key: device_base.KeyValueKey
  _callback_manager: thread_util.CallbackManager[str]
  _value: Optional[str]

  def __init__(self, key: device_base.KeyValueKey) -> None:
    """Initialize the key-value reader.

    Args:
      key: The key to read from.
    """
    super().__init__()
    self._key = key
    self._value = None
    self._callback_manager = thread_util.CallbackManager()

  def get_key_values(self) -> Set[device_base.KeyValueKey]:
    """Return the key used to load a calibration from the settings engine."""
    return {self._key}

  def on_set_key_value(self, key: device_base.KeyValueKey, value: str) -> None:
    """Process the value to set the local value.

    Args:
      key: The key for the key/value pair as a KeyValueKey.
      value: The value of the key/value pair.
    """
    if key.device_type != self._key.device_type:
      return
    if key.device_name != self._key.device_name:
      return
    if key.key != self._key.key:
      return None
    self._value = value
    self._callback_manager.call(self._value)

  def add_update_callback(
      self,
      callback: Callable[[str], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback when new data is received.

    Args:
      callback: triggers when new data is received.
      finished_callback: triggers when update is finished.

    Returns:
      Returns a function when called stops the callback.
    """
    return self._callback_manager.add_callback(callback, finished_callback)

  @property
  def value(self) -> Optional[str]:
    """Name gets the current value.

    Returns:
      The current value, or none if it is not loaded.
    """
    return self._value

  def wait_for_value(self) -> Optional[str]:
    """Wait for value waits for the value to load.

    Returns:
      The current value, or none if it is not loaded.
    """
    q: "queue.Queue[None]" = queue.Queue()

    def drop_callback(unused_value: str) -> bool:
      return True

    def finished_callback() -> None:
      q.put(None)

    stop = self._callback_manager.add_callback(drop_callback, finished_callback)
    value = self.value
    if value is None:
      q.get()
      value = self.value
    stop()
    return value

  def on_close(self) -> None:
    """Invoke when the system is closed."""
    self._callback_manager.close()


class ReachHost:
  """A class that represents the Reach Host."""

  _devices: List[device_base.DeviceBase]
  _ping_device: Optional[Ping]
  _session_manager: Optional[SessionManager]
  _host_id_reader: KeyValueReader
  _display_name_reader: KeyValueReader
  _thread: threading.Thread
  _take_control_at_start: bool
  _is_closed: bool
  _is_playback: bool

  def __init__(
      self,
      client: cli.Client,
      devices: List[device_base.DeviceBase],
      take_control_at_start: bool = True,
      initial_messages: Optional[List[Optional[types_gen.DeviceData]]] = None
  ) -> None:
    """Construct a ReachHost instance.

    Args:
      client: The Client to use.
      devices: The list of Devices supported.
      take_control_at_start: If True, immediately take control.
      initial_messages: A list of initial request messages.
    """
    self._is_closed = False
    self._is_playback = isinstance(client, cli.PlaybackClient)
    self._client = client
    self._devices = devices.copy()
    self._take_control_at_start = take_control_at_start
    self._ping_device = None
    self._session_manager = None
    if not self._is_playback:
      self._ping_device = Ping()
      self._devices.append(self._ping_device)
      self._session_manager = SessionManager(take_control_at_start, False)
      self._devices.append(self._session_manager)
    self._host_id_reader = KeyValueReader(
        device_base.KeyValueKey(
            device_type="settings-engine", device_name="", key="robot-name"))
    self._devices.append(self._host_id_reader)
    self._display_name_reader = KeyValueReader(
        device_base.KeyValueKey(
            device_type="settings-engine", device_name="", key="display-name"))
    self._devices.append(self._display_name_reader)
    for device in self._devices:
      device.set_send_cmd(self._send_to_client)
    self._thread = threading.Thread(
        name="host_thread", target=self._run_thread, args=(initial_messages,))

  def start(self) -> None:
    """Start the host."""
    success = False
    self._thread.start()
    try:
      if self._take_control_at_start:
        self.wait_for_control()
      self._host_id_reader.wait_for_value()
      self._display_name_reader.wait_for_value()
      success = True
    finally:
      if not success:
        self.close()

  def set_machine_interfaces(
      self, interfaces: Optional[machine_interfaces.MachineInterfaces]) -> None:
    """Set the machine interface settings.

    Args:
      interfaces: the machine interfaces discovered.
    """
    for device in self._devices:
      device.set_machine_interfaces(interfaces)

  def get_ping_time(self) -> Optional[float]:
    """Return the latest ping time.

    Returns:
      Returns the latest ping time or None if no ping time is available.

    """
    if not self._ping_device:
      return None
    return self._ping_device.get_ping_time()

  def get_server_offset_time(self) -> Optional[float]:
    """Return the offset to the server time.

    Returns:
      The offset to the server-side time, or None if it could not be computed.
    """
    if not self._ping_device:
      return None
    return self._ping_device.get_server_offset_time()

  def set_should_take_control(self,
                              should_take_control: bool,
                              should_release_control: bool = False) -> None:
    """Set the should take control flag.

    Args:
      should_take_control: If true, will try to start a control session.
      should_release_control: If true, will force release of control session.
    """
    if self._session_manager:
      self._session_manager.set_should_take_control(should_take_control,
                                                    should_release_control)

  def wait_for_control(self, timeout: Optional[float] = None) -> bool:
    """Wait until the session becomes active.

    Args:
      timeout: timeout for time to wait for state.

    Returns:
      True if have taken control, false otherwise.
    """
    if self._session_manager:
      return self._session_manager.wait_state(
          host.SessionState.ACTIVE, timeout=timeout)
    return True

  def wait_for_session_state(self,
                             state: host.SessionState,
                             timeout: Optional[float] = None) -> bool:
    """Wait for a specific session state.

    Args:
      state: the state to wait for.
      timeout: timeout for time to wait for state.

    Returns:
      True if have entered the state, false otherwise.
    """
    if self._session_manager:
      return self._session_manager.wait_state(state, timeout=timeout)
    return True

  def get_session_state(self) -> host.SessionState:
    """Get the session state of the host.

    Returns:
      The session state.
    """
    if self._session_manager:
      return self._session_manager.get_session_state()
    return host.SessionState.PLAYBACK

  def add_session_state_callback(
      self,
      callback: Callable[[host.SessionState], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback when new a session state is received.

    Args:
      callback: triggers when new a session state is received.
      finished_callback: triggers when update is finished.

    Returns:
      Returns a function when called stops the callback.
    """
    if self._session_manager:
      return self._session_manager.add_update_callback(callback,
                                                       finished_callback)

    def empty_function() -> None:
      pass

    return empty_function

  def _send_to_client(self, msg: types_gen.CommandData) -> None:
    """Send CommandData message to client."""
    self._client.send_cmd(msg)

  def _read_from_client(
      self, timeout: float) -> Tuple[List[types_gen.DeviceData], bool, int]:
    """Read a Device Data from the client.

    Args:
      timeout: The number of seconds until timing out.

    Returns:
      Returns a Tuple containing a list of DeviceData messages a flag, and
      the number of tasks from the queue. The flag is True if client is still
      open and False if closed.
    """
    msgs: List[types_gen.DeviceData] = []
    tasks_to_complete = 0
    # Clear the queue of all messages
    while True:
      try:
        msg = self._client.get_queue().get(block=False)
        tasks_to_complete += 1
        if msg is None:
          return msgs, False, tasks_to_complete
        msgs.append(msg)
      except queue.Empty:
        break
    if timeout > 0 and not msgs:
      try:
        msg = self._client.get_queue().get(block=True, timeout=timeout)
        tasks_to_complete += 1
        if msg is None:
          return msgs, False, tasks_to_complete
        msgs.append(msg)
      except queue.Empty:
        pass
    return msgs, True, tasks_to_complete

  def _complete_tasks(self, tasks_to_complete: int) -> None:
    if self._is_playback:
      q = self._client.get_queue()
      for _ in range(tasks_to_complete):
        q.task_done()

  def _flush(self) -> None:
    self._client.get_queue().join()
    for dev in self._devices:
      dev.flush()

  def flush(self) -> None:
    """Flush all data from the queues."""
    if not self._is_playback:
      raise PyReachError("flush is only supported for playback clients.")
    client = self._client
    assert isinstance(client, cli.PlaybackClient)
    client.with_queue_lock(self._flush)

  def _run_thread(
      self,
      initial_messages: Optional[List[Optional[types_gen.DeviceData]]]) -> None:
    """Thread to run the host device processing loop."""
    active: bool = True
    for dev in self._devices:
      dev.start()
    last_key_value_requests: Dict[device_base.KeyValueKey, float] = {}
    is_first = True
    tasks_to_complete = 0
    while active:
      self._complete_tasks(tasks_to_complete)
      # Get messages
      messages, active, tasks_to_complete = self._read_from_client(
          0.0 if is_first else 1.0)
      if is_first:
        if initial_messages:
          tasks_to_complete += len(initial_messages)
          messages = [m for m in initial_messages if m is not None] + messages
          if None in initial_messages:
            active = False
        is_first = False
      # Send to devices
      for dev in self._devices:
        for message in messages:
          dev.enqueue_device_data(message)
      # Send any key-value requests
      request_keys: Set[device_base.KeyValueKey] = set()
      for dev in self._devices:
        for kv in dev.get_key_values():
          if dev.get_key_value(kv) is None:
            request_keys.add(kv)
      remove_keys = set()
      for kv, request_time in last_key_value_requests.items():
        if time.time() > request_time + 15:
          remove_keys.add(kv)
      for kv in remove_keys:
        del last_key_value_requests[kv]
      for kv in request_keys:
        if kv in last_key_value_requests:
          continue
        last_key_value_requests[kv] = time.time()
        if not self._is_playback:
          self._send_to_client(
              types_gen.CommandData(
                  ts=utils.timestamp_now(),
                  tag=utils.generate_tag(),
                  device_type=kv.device_type,
                  device_name=kv.device_name,
                  data_type="key-value-request",
                  key=kv.key))
    self._complete_tasks(tasks_to_complete)
    for dev in self._devices:
      dev.close()
    self._client.close()
    self._is_closed = True

  def add_host_id_callback(
      self,
      callback: Callable[[str], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback when new a host id is received.

    Args:
      callback: triggers when new host id is received.
      finished_callback: triggers when update is finished.

    Returns:
      Returns a function when called stops the callback.
    """
    return self._host_id_reader.add_update_callback(callback, finished_callback)

  @property
  def host_id(self) -> Optional[str]:
    """Name gets the current host id of the robot.

    Returns:
      The current id of the host, or none if it is not loaded.
    """
    return self._host_id_reader.value

  def add_display_name_callback(
      self,
      callback: Callable[[str], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback when new a display name is received.

    Args:
      callback: triggers when new display name is received.
      finished_callback: triggers when update is finished.

    Returns:
      Returns a function when called stops the callback.
    """
    return self._display_name_reader.add_update_callback(
        callback, finished_callback)

  @property
  def display_name(self) -> Optional[str]:
    """Name gets the current display name of the robot.

    Returns:
      The current display name of the robot, or none if it is not loaded.
    """
    return self._display_name_reader.value

  def close(self) -> None:
    """Close the connect to the Reach Host."""
    self._client.close()
    self._thread.join()
    self._is_closed = True

  def wait(self) -> None:
    """Wait for the host to close."""
    self._thread.join()
    self._is_closed = True

  def is_closed(self) -> bool:
    """Determine if the host is closed."""
    return self._is_closed
