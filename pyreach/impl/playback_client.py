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

"""Shared utilities for playback clients."""

import queue
import threading
from typing import Callable, Generic, Optional, Set, Tuple, TypeVar

from pyreach import core
from pyreach.common.python import types_gen
from pyreach.impl import client
from pyreach.impl import snapshot_impl
from pyreach.impl import utils
from pyreach.snapshot import Snapshot

T = TypeVar("T")


class Iterator(Generic[T]):
  """Iterator for reading device-data or command-data."""

  def valid(self) -> bool:
    """Get if the current value is valid."""
    raise NotImplementedError

  def value(self) -> Optional[Tuple[T, float, int]]:
    """Get the current value."""
    raise NotImplementedError

  def start(self) -> None:
    """Start the directory reader."""
    raise NotImplementedError

  def step(self) -> bool:
    """Load the next device data."""
    raise NotImplementedError

  def reset(self) -> bool:
    """Reset the iterator back to the start."""
    raise NotImplementedError

  def seek(self, time: Optional[float], sequence: Optional[int]) -> bool:
    """Seek the given data and output it, if available.

    Args:
      time: the timestamp to seek. If sequence number is not specified, the
        exact time will be returned.
      sequence: the sequence number to seek. If specified, the exact sequence
        number will be returned.

    Returns:
      Returns if the data object was found and played.
    """
    # Default implementation is very inefficient, simply iterate through all
    # data elements to find the requested value.
    if time is None and sequence is None:
      raise core.PyReachError("Must specify either timestamp or sequence")
    while self.valid():
      value = self.value()
      if (value and (time is None or value[1] == time) and
          (sequence is None or value[2] == sequence)):
        return True
      self.step()
    self.reset()
    while self.valid():
      value = self.value()
      if (value and (time is None or value[1] == time) and
          (sequence is None or value[2] == sequence)):
        return True
      self.step()
    return False

  def close(self) -> None:
    """Close the object."""
    raise NotImplementedError


class ClientSimulator:
  """ClientSimulator filters and transforms data to simulate a client session."""
  _start: Optional[Tuple[float, int]]
  _end: Optional[Tuple[float, int]]
  _start_time: int
  _end_time: Optional[int]
  _client_id: str
  _tags: Set[str]
  _allow_client_logs: bool

  def __init__(self, client_id: Optional[str],
               device_iterator: Iterator[types_gen.DeviceData],
               command_iterator: Iterator[types_gen.CommandData],
               allow_client_logs: bool) -> None:
    """Initialize the ClientSimulator.

    Args:
      client_id: the client ID to simulate. If the client ID is None, will find
        the first client, using the connected client if possible.
      device_iterator: iterator used to establish the connection state. Will not
        be used after init is completed.
      command_iterator: iterator used to load tags. Will not be used after init
        is completed.
      allow_client_logs: allow parsing client logs.
    """
    device_iterator.reset()
    self._start = None
    self._end = None
    self._allow_client_logs = allow_client_logs
    # Iterate until we find the session.
    while not client_id or not self._start:
      if not device_iterator.valid():
        raise core.PyReachError("specified client not found within dataset")
      step = device_iterator.value()
      assert step
      data = step[0]
      if (data.device_type == "session-manager" and not data.device_name and
          data.data_type == "connected-clients" and data.connected_clients and
          data.connected_clients.clients):
        if client_id is None:
          best_client = data.connected_clients.clients[0]
          for connected_client in data.connected_clients.clients:
            if connected_client.uid and connected_client.is_current:
              best_client = connected_client
              break
          if best_client:
            client_id = best_client.uid
            self._start = (step[1], step[2])
        else:
          for connected_client in data.connected_clients.clients:
            if connected_client.uid == client_id:
              self._start = (step[1], step[2])
              break
      device_iterator.step()
    self._start_time = utils.timestamp_at_time(self._start[0])
    # Iterate until we find the end of the session.
    while device_iterator.valid() and not self._end:
      step = device_iterator.value()
      assert step
      data = step[0]
      if (data.device_type == "session-manager" and not data.device_name and
          data.data_type == "connected-clients" and data.connected_clients and
          data.ts > self._start_time):
        found_client = False
        for connected_client in data.connected_clients.clients:
          if connected_client.uid == client_id:
            found_client = True
            break
        if not found_client:
          self._end = (step[1], step[2])
      device_iterator.step()
    # Save the client ID.
    assert client_id
    assert self._start
    self._client_id = client_id
    self._end_time = None
    if self._end:
      self._end_time = utils.timestamp_at_time(self._end[0])
    # Load all the tags from the file.
    self._tags = set()
    command_iterator.reset()
    while command_iterator.valid():
      command_step = command_iterator.value()
      if command_step:
        cmd = self.transform_command(command_step[0])
        if cmd and cmd.tag:
          self._tags.add(cmd.tag)
      command_iterator.step()

  @property
  def client_id(self) -> str:
    """Get the client ID of the system."""
    return self._client_id

  def transform_command(
      self, data: types_gen.CommandData) -> Optional[types_gen.CommandData]:
    """Transform a command-data message to simulate the client.

    Args:
      data: the data to transform.

    Returns:
      The command-data message transformed, or None if not sent from the client.
      The data will be copied before it is modified.
    """
    if not self._allow_client_logs and not data.origin_client:
      return None
    if data.origin_client and data.origin_client != self._client_id:
      return None
    return data

  def transform_data(
      self, data: types_gen.DeviceData) -> Optional[types_gen.DeviceData]:
    """Transform a device-data message to simulate the client.

    Args:
      data: the data to transform.

    Returns:
      The device-data message transformed, or None if not sent to the client.
      The data will be copied before it is modified.
    """
    if data.inhibit_frame_send:
      return None
    force = False
    copied = False
    if data.send_to_clients:
      have_client = False
      tag = ""
      for test_client in data.send_to_clients:
        if test_client.uid == self._client_id:
          have_client = True
          tag = test_client.tag
          break
      if not have_client:
        return None
      if not copied:
        data = utils.copy_device_data(data)
        copied = True
      data.tag = tag
      data.send_to_clients = []
      force = True
    if data.tag and not force:
      if data.tag not in self._tags:
        return None
      force = True
    if (data.device_type == "session-manager" and not data.device_name and
        data.data_type == "connected-clients" and data.connected_clients):
      if not copied:
        data = utils.copy_device_data(data)
        copied = True
      have_client = False
      assert data.connected_clients
      for connected_client in data.connected_clients.clients:
        connected_client.is_current = (connected_client.uid == self._client_id)
        have_client = connected_client.is_current or have_client
      if not have_client:
        return None
    if not force and (data.ts < self._start_time or
                      (self._end_time and data.ts > self._end_time)):
      return None
    return data


class PlaybackClient(client.PlaybackClient):
  """Implements a playback client by wrapping iterators."""

  _lock: threading.Lock
  _device_data_iterator: Optional[Iterator[types_gen.DeviceData]]
  _command_data_iterator: Optional[Iterator[types_gen.CommandData]]
  _closed: bool
  _allow_client_logs: bool
  _client_simulator: Optional[ClientSimulator]
  _gym_run_id: Optional[str]
  _queue: "queue.Queue[Optional[types_gen.DeviceData]]"

  def __init__(self, lock: Optional[threading.Lock] = None) -> None:
    """Create the playback client.

    Args:
      lock: optional, lock to use as lock.
    """
    self._lock = lock if lock else threading.Lock()
    self._device_data_iterator = None
    self._command_data_iterator = None
    self._client_simulator = None
    self._gym_run_id = None
    self._queue = queue.Queue()
    self._closed = False
    self._allow_client_logs = False

  @property
  def client_id(self) -> Optional[str]:
    """Get the client ID we are currently simulating."""
    sim = self._client_simulator
    return sim.client_id if sim else None

  @property
  def gym_run_id(self) -> Optional[str]:
    """Get the current gym run id."""
    return self._gym_run_id

  def get_queue(self) -> "queue.Queue[Optional[types_gen.DeviceData]]":
    """Get a queue of DeviceData from the Reach host.

    None is inserted to close the queue.

    Returns:
      The queue.
    """
    return self._queue

  def start_playback(self, device_data_iterator: Iterator[types_gen.DeviceData],
                     command_data_iterator: Iterator[types_gen.CommandData],
                     client_id: Optional[str], select_client: bool,
                     gym_run_id: Optional[str], select_gym_run: bool,
                     allow_client_logs: bool) -> None:
    """Start a PlaybackClient.

    Args:
      device_data_iterator: opened iterator for device-data.
      command_data_iterator: opened iterator for command-data.
      client_id: the client ID to simulate.
      select_client: if client ID is None, will select first client.
      gym_run_id: if specified, will select the given snapshot by gym_run_id.
      select_gym_run: if specified, but gym_run_id is None, will select first
        snapshot.
      allow_client_logs: must be set if the log could be a client-side log.

    Raises:
       PyReachError: if the session or client could not be found.
    """
    with self._lock:
      self._allow_client_logs = allow_client_logs
      if self._closed:
        return None
      if select_gym_run or gym_run_id is not None:
        command_data_iterator.reset()
        while True:
          if not command_data_iterator.valid():
            raise core.PyReachError("gym session not found within dataset")
          step = command_data_iterator.value()
          assert step
          if step[0].snapshot:
            if step[0].snapshot.gym_run_id == gym_run_id or gym_run_id is None:
              gym_run_id = step[0].snapshot.gym_run_id
              assert step[0].origin_client or allow_client_logs
              if step[0].origin_client:
                if client_id is not None and client_id != step[0].origin_client:
                  raise core.PyReachError("gym session has wrong client ID")
                client_id = step[0].origin_client
              elif client_id is None:
                # In client data logs, origin_client == "", so we have to find
                # the correct client.
                select_client = True
              break
          command_data_iterator.step()
      if select_client or client_id is not None:
        self._client_simulator = ClientSimulator(client_id,
                                                 device_data_iterator,
                                                 command_data_iterator,
                                                 allow_client_logs)
      self._gym_run_id = gym_run_id
      device_data_iterator.reset()
      self._device_data_iterator = device_data_iterator
      command_data_iterator.reset()
      self._command_data_iterator = command_data_iterator
      while device_data_iterator.valid() and not self._current_data(False):
        device_data_iterator.step()

  def next_snapshot(self) -> Optional[Snapshot]:
    """Get the next command-data snapshot."""
    with self._lock:
      return self._next_snapshot()

  def _next_snapshot(self) -> Optional[Snapshot]:
    """Get the next command-data snapshot."""
    if self._closed or not self._command_data_iterator:
      return None
    while self._command_data_iterator.valid():
      step = self._command_data_iterator.value()
      assert step
      cmd: Optional[types_gen.CommandData] = step[0]
      if self._client_simulator and cmd:
        cmd = self._client_simulator.transform_command(cmd)
      if cmd and cmd.snapshot and (
          (not cmd.origin_client and self._allow_client_logs) or
          not self._client_simulator or
          self._client_simulator.client_id == cmd.origin_client) and (
              self._gym_run_id is None or
              self._gym_run_id == cmd.snapshot.gym_run_id):
        snap = snapshot_impl.reverse_snapshot(cmd.snapshot)
        if snap:
          self._command_data_iterator.step()
          return snap
      self._command_data_iterator.step()
    return None

  def seek_snapshot(self, gym_run_id: Optional[str], gym_episode: Optional[int],
                    gym_step: Optional[int]) -> Optional[Snapshot]:
    """Seek the oldest snapshot that matches the given criteria.

    Args:
      gym_run_id: The gym_run_id of the snapshot to seek.
      gym_episode: The gym_episode of the snapshot to seek.
      gym_step: The gym_step of the snapshot to seek.

    Returns:
      The snapshot, or None if there is no matching snapshot.
    """
    with self._lock:
      if self._closed or not self._command_data_iterator:
        return None
      self._command_data_iterator.reset()
      while True:
        snap = self._next_snapshot()
        if snap is None:
          return None
        if ((gym_run_id is None or snap.gym_run_id == gym_run_id) and
            (gym_episode is None or snap.gym_episode == gym_episode) and
            (gym_step is None or snap.gym_step == gym_step)):
          return snap
    return None

  def next_device_data(self) -> Optional[types_gen.DeviceData]:
    """Playback the next device-data object.

    Returns:
      Returns the DeviceData object loaded, if available.
    """
    with self._lock:
      if self._closed or not self._device_data_iterator:
        return None
      data = self._current_data(True)
      while self._device_data_iterator.valid():
        self._device_data_iterator.step()
        if self._current_data(False):
          break
      return data

  def device_data_available(self) -> bool:
    """Returns true if the client has additional device data."""
    with self._lock:
      return self._current_data(False) is not None

  def seek_device_data(
      self, time: Optional[float],
      sequence: Optional[int]) -> Optional[types_gen.DeviceData]:
    """Seek the given device data and output it, if available.

    Args:
      time: the timestamp to seek. If sequence number is not specified, will not
        return any data from before the specified time.
      sequence: the sequence number to seek. If specified, the exact sequence
        number, or any data after it will be returned.

    Returns:
      Returns the DeviceData object loaded, if found.
    """
    with self._lock:
      if self._closed or not self._device_data_iterator:
        return None
      if not self._device_data_iterator.seek(time, sequence):
        return None
      data = self._current_data(True)
      while self._device_data_iterator.valid():
        self._device_data_iterator.step()
        if self._current_data(False):
          break
      return data

  def _current_data(self, publish: bool) -> Optional[types_gen.DeviceData]:
    if not self._device_data_iterator:
      return None
    step = self._device_data_iterator.value()
    data = step[0] if step else None
    if data and self._client_simulator:
      data = self._client_simulator.transform_data(data)
    elif data and data.connected_clients and data.connected_clients.clients:
      data = utils.copy_device_data(data)
      assert data.connected_clients
      for connected_client in data.connected_clients.clients:
        connected_client.is_current = False
    if data and publish:
      self._queue.put(data)
    return data

  def with_queue_lock(self, callback: Callable[[], None]) -> None:
    with self._lock:
      callback()

  def close(self) -> None:
    with self._lock:
      closed = self._closed
      self._closed = True
      try:
        if self._device_data_iterator:
          self._device_data_iterator.close()
      finally:
        try:
          if self._command_data_iterator:
            self._command_data_iterator.close()
        finally:
          if not closed:
            self._queue.put(None)
