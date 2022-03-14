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
"""Provide a client to play back a logs directory."""

import json
import os
import queue  # pylint: disable=unused-import
from typing import Any, Dict, Optional, TextIO, Tuple, TypeVar

from pyreach import host
from pyreach.common.python import types_gen
from pyreach.impl import host_impl
from pyreach.impl import playback_client
from pyreach.impl import utils

T = TypeVar("T")


class _DirectoryReader(playback_client.Iterator[T]):
  """Read from a logged directory (e.g. command-data) in sequence."""
  _working_directory: str
  _file: Optional[TextIO]
  _index: int
  _overflow: bool
  _started: bool
  _closed: bool
  _value: Optional[Tuple[T, float, int]]

  def valid(self) -> bool:
    """Get if the current value is valid."""
    return self._value is not None

  def value(self) -> Optional[Tuple[T, float, int]]:
    """Get the current value."""
    return self._value

  def __init__(self, working_directory: str) -> None:
    """Create the directory reader, for reading files in a reach log directory.

    Args:
      working_directory: path to the directory containing files.
    """
    self._working_directory = working_directory
    self._file = None
    self._index = 0
    self._overflow = False
    self._started = False
    self._closed = False
    self._value = None

  def start(self) -> None:
    """Start the directory reader."""
    assert not self._closed
    self._started = True
    while not self.value() and not self._overflow:
      self.step()

  def transform(self, line: str) -> Optional[Tuple[T, float, int]]:
    """Transform a line of data into the correct data type.

    Args:
      line: line from the file.

    Returns:
      The converted data object.
    """
    raise NotImplementedError

  def step(self) -> bool:
    """Load the next device data."""
    self._value = self._next_data()
    return self.valid()

  def reset(self) -> bool:
    """Reset the iterator back to the start."""
    if self._file:
      self._file.close()
      self._file = None
    self._value = None
    self._index = 0
    self._overflow = False
    return self.step()

  def _next_data(self) -> Optional[Tuple[T, float, int]]:
    """Read the next data item from the stream."""
    assert self._started
    assert not self._closed
    while True:
      if self._overflow:
        return None
      if self._file is None:
        try:
          self._file = open(
              os.path.join(self._working_directory, "%05d.json" % self._index))
        except FileNotFoundError:
          self._overflow = True
          return None
      line = self._file.readline()
      if not line:
        self._file.close()
        self._file = None
        self._index += 1
      else:
        data = self.transform(line)
        if data is not None:
          return data

  def close(self) -> None:
    """Close the object."""
    self._closed = True
    if self._file is not None:
      self._file.close()
    self._value = None


class _DeviceDataReader(_DirectoryReader[types_gen.DeviceData]):
  """Read from a logged device-data directory."""

  def __init__(self, working_directory: str, abs_path: str) -> None:
    """Create the directory reader, for reading files in a reach log directory.

    Args:
      working_directory: path to the directory containing files.
      abs_path: absolute path for image files.
    """
    super().__init__(working_directory)
    self._abs_path = abs_path

  def transform(self,
                line: str) -> Optional[Tuple[types_gen.DeviceData, float, int]]:
    """Convert a line to device data."""
    try:
      data = json.loads(line)
    except json.JSONDecodeError:
      return None
    msg = types_gen.DeviceData.from_json(data)
    if msg.color or msg.depth:
      dev_key = msg.device_type
      if msg.device_name:
        dev_key += "-" + msg.device_name
      if msg.color:
        abs_path, filename = os.path.split(msg.color)
        _, dir_key = os.path.split(abs_path)
        if not dir_key:
          dir_key = dev_key
        msg.color = os.path.join(self._abs_path, dir_key, filename)
      if msg.depth:
        abs_path, filename = os.path.split(msg.depth)
        _, dir_key = os.path.split(abs_path)
        if not dir_key:
          dir_key = dev_key
        msg.depth = os.path.join(self._abs_path, dir_key, filename)
        if not os.path.exists(msg.depth) and msg.upload_depth:
          abs_path, filename = os.path.split(msg.upload_depth)
          _, dir_key = os.path.split(abs_path)
          if not dir_key:
            dir_key = dev_key
          msg.depth = os.path.join(self._abs_path, dir_key, filename)
    return msg, utils.time_at_timestamp(msg.ts), msg.seq


class _CommandDataReader(_DirectoryReader[types_gen.CommandData]):
  """Read from a logged command-data directory."""

  def transform(
      self, line: str) -> Optional[Tuple[types_gen.CommandData, float, int]]:
    """Convert a line to command data."""
    try:
      data = json.loads(line)
    except json.JSONDecodeError:
      return None
    if "experimentFlags" in data:
      del data["experimentFlags"]
    msg = types_gen.CommandData.from_json(data)
    return msg, utils.time_at_timestamp(msg.ts), msg.seq


class LogsDirectoryClient(playback_client.PlaybackClient):
  """Class to implement a logs directory client."""

  def __init__(self, robot_id: str, working_directory: str,
               client_id: Optional[str], select_client_id: bool,
               gym_run_id: Optional[str], select_gym_run: bool) -> None:
    """Init a LogsDirectoryClient.

    Args:
      robot_id: the robot id to connect to.
      working_directory: optional directory to run within.
      client_id: the client ID to simulate (e.g. 00005.json vs 00000.json).
      select_client_id: if client ID is None, will select first client.
      gym_run_id: if specified, will select the given snapshot by gym_run_id.
      select_gym_run: if specified, but gym_run_id is None, will select first
        snapshot.

    Raises:
       PyReachError: if connection fails.
    """
    super().__init__()

    started = False
    device_iterator = _DeviceDataReader(
        os.path.join(working_directory, "device-data"),
        os.path.abspath(working_directory))
    command_iterator = _CommandDataReader(
        os.path.join(working_directory, "command-data"))
    try:
      device_iterator.start()
      command_iterator.start()
      self.start_playback(device_iterator, command_iterator, client_id,
                          select_client_id, gym_run_id, select_gym_run, True)
      started = True
    finally:
      if not started:
        device_iterator.close()
        command_iterator.close()


def connect_logs_directory(robot_id: str, working_directory: str,
                           client_id: Optional[str], select_client_id: bool,
                           gym_run_id: Optional[str], select_gym_run: bool,
                           kwargs: Dict[str, Any]) -> host.Host:
  """Connect to Reach using TCP on specific host:port.

  Args:
    robot_id: the robot id to connect to.
    working_directory: optional directory to run within.
    client_id: the client ID to simulate.
    select_client_id: if client ID is None, will select first client.
    gym_run_id: if specified, will select the given snapshot by gym_run_id.
    select_gym_run: if specified, but gym_run_id is None, will select first
      snapshot.
    kwargs: additional argument.

  Returns:
    Host interface if successful.
  """
  return host_impl.HostImpl(
      LogsDirectoryClient(robot_id, working_directory, client_id,
                          select_client_id, gym_run_id, select_gym_run),
      **kwargs)
