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

"""Factory interface and concrete factory for connecting to Reach host."""

import importlib
from typing import Dict, Any, Optional, List

import pyreach


class HostFactory(object):
  """Factory for creating a host object to interact with a Reach host."""

  def connect(self) -> pyreach.Host:
    """Connect to a Reach host.

    Returns:
      An implementation of the Host interface.
    """
    raise NotImplementedError


class LocalTCPHostFactory(HostFactory):
  """Factory for connecting to Reach using local TCP."""

  _host: str
  _port: int
  _kwargs: Dict[str, Any]

  def __init__(self,
               hostname: str = 'localhost',
               port: int = 50008,
               **kwargs: Any):
    """Construct a LocalTCPHostFactory object."""
    self._host = hostname
    self._port = port
    if kwargs is None:
      self._kwargs = {}
    else:
      self._kwargs = kwargs

  def connect(self) -> pyreach.Host:
    """Connect to a Reach host.

    Returns:
      An implementation of the Host interface.
    """
    mod = importlib.import_module(
        'pyreach.impl.local_tcp_client'
    )
    if not hasattr(mod, 'connect_local_tcp'):
      raise pyreach.PyReachError()

    fn = getattr(mod, 'connect_local_tcp')
    return fn(self._host, self._port, self._kwargs)


class WebRTCHostFactory(HostFactory):
  """Factory for connecting to Reach using webrtc."""

  _robot_id: str
  _working_directory: Optional[str]
  _kwargs: Any

  def __init__(self,
               robot_id: str,
               working_directory: Optional[str] = None,
               reach_connect_arguments: Optional[List[str]] = None,
               **kwargs: Any) -> None:
    """Construct a WebRTCHostFactory object.

    Args:
      robot_id: the robot id to connect to.
      working_directory: optional directory to run within.
      reach_connect_arguments: optional list of arguments to the reach connect
        tool.
      **kwargs: the optional kwargs to the connect host.
    """
    self._robot_id = robot_id
    self._working_directory = working_directory
    self._reach_connect_arguments = reach_connect_arguments
    if kwargs is None:
      self._kwargs = {}
    else:
      self._kwargs = kwargs

  def connect(self) -> pyreach.Host:
    """Connect to a Reach host.

    Returns:
      An implementation of the Host interface.
    """
    mod = importlib.import_module(
        'pyreach.impl.reach_connect_client'
    )
    if not hasattr(mod, 'reach_connect_webrtc'):
      raise pyreach.PyReachError()

    fn = getattr(mod, 'reach_connect_webrtc')
    return fn(self._robot_id, self._working_directory, True,
              self._reach_connect_arguments, self._kwargs)


class RemoteTCPHostFactory(HostFactory):
  """Factory for connecting to Reach using remote tcp."""

  _robot_id: str
  _working_directory: Optional[str]
  _connect_host: Optional[str]
  _connect_port: Optional[int]
  _kwargs: Any

  def __init__(self,
               robot_id: str,
               connect_host: Optional[str] = None,
               connect_port: Optional[int] = 50009,
               working_directory: Optional[str] = None,
               reach_connect_arguments: Optional[List[str]] = None,
               **kwargs: Any) -> None:
    """Construct a RemoteTCPHostFactory object.

    Args:
      robot_id: the robot id to connect to.
      connect_host: the host to connect to. Defaults to <robot_id>.local
      connect_port: the port to connect to. Defaults to 50009.
      working_directory: optional directory to run within.
      reach_connect_arguments: optional list of arguments to the reach connect
        tool.
      **kwargs: the optional kwargs to the connect host.
    """
    self._robot_id = robot_id
    self._working_directory = working_directory
    self._connect_host = connect_host
    self._connect_port = connect_port
    self._reach_connect_arguments = reach_connect_arguments
    if kwargs is None:
      self._kwargs = {}
    else:
      self._kwargs = kwargs

  def connect(self) -> pyreach.Host:
    """Connect to a Reach host.

    Returns:
      An implementation of the Host interface.
    """
    mod = importlib.import_module(
        'pyreach.impl.reach_connect_client'
    )
    if not hasattr(mod, 'reach_connect_remote_tcp'):
      raise pyreach.PyReachError()

    fn = getattr(mod, 'reach_connect_remote_tcp')
    return fn(self._robot_id, self._connect_host, self._connect_port,
              self._working_directory, self._reach_connect_arguments,
              self._kwargs)


class LocalPlaybackHostFactory(HostFactory):
  """Factory for local playback of a robot's log session."""

  _working_directory: str
  _robot_id: str
  _client_id: Optional[str]
  _select_client: bool
  _snapshot_run_id: Optional[str]
  _select_snapshot_run_id: bool
  _kwargs: Any

  def __init__(self,
               robot_id: str,
               working_directory: str,
               client_id: Optional[str] = None,
               select_client: bool = False,
               snapshot_run_id: Optional[str] = None,
               select_snapshot_run_id: bool = False,
               **kwargs: Any) -> None:
    """Construct a LocalPlaybackHostFactory object.

    Args:
      robot_id: the robot id to connect to.
      working_directory: optional directory to run within.
      client_id: the client ID to simulate.
      select_client: if client ID is None, will select first client.
      snapshot_run_id: if specified, will select the given snapshot by
        gym_run_id.
      select_snapshot_run_id: if specified, but snapshot_run_id is None, will
        select first snapshot.
      **kwargs: the optional kwargs to the connect host.
    """
    self._robot_id = robot_id
    self._working_directory = working_directory
    self._client_id = client_id
    self._select_client = select_client
    self._snapshot_run_id = snapshot_run_id
    self._select_snapshot_run_id = select_snapshot_run_id
    if kwargs is None:
      self._kwargs = {}
    else:
      self._kwargs = kwargs

  def connect(self) -> pyreach.Host:
    """Connect to a log directory, simulating a reach host.

    Returns:
      An implementation of the Host interface.
    """
    mod = importlib.import_module('pyreach.impl.logs_directory_client')
    if not hasattr(mod, 'connect_logs_directory'):
      raise pyreach.PyReachError()

    fn = getattr(mod, 'connect_logs_directory')
    return fn(self._robot_id, self._working_directory, self._client_id,
              self._select_client, self._snapshot_run_id,
              self._select_snapshot_run_id, self._kwargs)
