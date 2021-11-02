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
"""Provide a reach connect client."""

import json
import logging
import pathlib
import queue
import subprocess
import threading
from typing import Any, Dict, List, Optional

from pyreach import host
from pyreach.common.python import types_gen
from pyreach.impl import client as cli
from pyreach.impl import host_impl
from pyreach.impl import local_tcp_client
from pyreach.impl import reach_tools_impl

_is_running_on_google3 = False


class ReachConnectClient(cli.Client):
  """Class to implement a local TCP client."""

  _stop: bool
  _lock: threading.Lock
  _process: "Optional[subprocess.Popen[bytes]]"
  _queue: "queue.Queue[Optional[types_gen.DeviceData]]"
  _client: Optional[local_tcp_client.LocalTCPClient]
  _stdout_thread: Optional[threading.Thread]
  _stderr_thread: Optional[threading.Thread]

  def __init__(self,
               robot_id: str,
               working_directory: Optional[pathlib.Path] = None,
               download_reach_tool: bool = True,
               download_webrtc_headless: bool = True,
               use_webrtc_headless: bool = True,
               reach_connect_arguments: Optional[List[str]] = None) -> None:
    """Init a ReachConnectClient.

    Args:
      robot_id: the robot id to connect to.
      working_directory: optional directory to run within.
      download_reach_tool: if true, will download the reach tool.
      download_webrtc_headless: if true, will download webtrc_headless.
      use_webrtc_headless: if true, will add webrtc_headless path.
      reach_connect_arguments: optional list of arguments to reach connect.
    """
    super().__init__()
    self._lock = threading.Lock()
    self._stop = False
    self._client = None
    self._stdout_thread = None
    self._stderr_thread = None
    self._process = None
    if not reach_connect_arguments:
      reach_connect_arguments = []
    if not working_directory:
      try:
        working_directory = reach_tools_impl.create_reach_workspace()
      finally:
        if working_directory is None:
          self.close()
          self._queue = queue.Queue()
          self._queue.put(None)
    assert working_directory is not None
    if not working_directory.is_dir():
      logging.error("Working directory %s does not exist.", working_directory)
      self.close()
      self._queue = queue.Queue()
      self._queue.put(None)
      return
    reach_path, _ = reach_tools_impl.download_reach_tool(
        working_directory if download_reach_tool else None)
    webrtc_arguments = []
    if use_webrtc_headless:
      webrtc_arguments = [
          "-webrtc_headless",
          str(
              reach_tools_impl.download_webrtc_headless(
                  working_directory if download_webrtc_headless else None))
      ]
    try:
      try:
        self._process = subprocess.Popen(
            [str(reach_path), "connect"] + webrtc_arguments +
            reach_connect_arguments + [
                "-start_control_session=false",
                robot_id,
            ],
            cwd=working_directory,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
      except FileNotFoundError:
        logging.error("Reach binary is not in your path. Did you install/build"
                      " reach tool and source setenv.sh?")
      if not self._process:
        self.close()
        self._queue = queue.Queue()
        self._queue.put(None)
        return
      self._stderr_thread = threading.Thread(target=self._read_stderr_pipe)
      self._stderr_thread.start()
      while True:
        if not self._process.stdout:
          logging.error("Output is None")
          self.close()
          break
        line = self._process.stdout.readline()
        if not line:
          logging.error("Output terminated before connecting")
          self.close()
          break
        try:
          data = json.loads(line.decode("utf-8"))
        except UnicodeError:
          logging.warning("Stdout line could not be decoded to utf-8")
        except json.JSONDecodeError:
          logging.warning("Packet could not be decoded from JSON: %s",
                          line.decode("utf-8"))
        if (isinstance(data, dict) and
            data.get("msg-type") == "device-data-server"):
          self._stdout_thread = threading.Thread(target=self._read_stdout_pipe)
          self._stdout_thread.start()
          hostname = data.get("hostname", "localhost")
          port = data.get("port", 50008)
          if not isinstance(hostname, str):
            logging.error("Hostname is not a string")
            self.close()
            break
          if not isinstance(port, int):
            logging.error("Port is not an int")
            self.close()
            break
          self._client = local_tcp_client.LocalTCPClient(
              hostname=hostname, port=port)
          break
        else:
          logging.warning("Invalid message: %s", data)
    except KeyboardInterrupt:
      self.close()
    if self._client:
      self._queue = self._client.get_queue()
    else:
      self._queue = queue.Queue()
      self._queue.put(None)

  def _read_stderr_pipe(self) -> None:
    assert self._process
    if not self._process.stderr:
      logging.error("Reach connect stderr is None")
      return
    while True:
      line = self._process.stderr.readline()
      if not line:
        break
      try:
        logging.info("Reach connect: %s", line.decode("utf8").strip())
      except UnicodeError:
        logging.error("Reach connect stderr line not unicode")
    self._process.stderr.close()

  def _read_stdout_pipe(self) -> None:
    assert self._process
    if not self._process.stdout:
      logging.error("Reach connect stdout is None")
      return
    while True:
      line = self._process.stdout.readline()
      if not line:
        break
      try:
        logging.error("Reach connect spurious stdout: %s",
                      line.decode("utf8").strip())
      except UnicodeError:
        logging.error("Reach connect stdout line not unicode")
    self._process.stdout.close()

  def get_queue(self) -> "queue.Queue[Optional[types_gen.DeviceData]]":
    """Get the queue for the LocalTCPClient."""
    return self._queue

  def send_cmd(self, cmd: types_gen.CommandData) -> None:
    """Send a command to the client.

    Args:
      cmd: The CommandData to send to the client.
    """
    if self._client:
      self._client.send_cmd(cmd)

  def _close(self) -> None:
    with self._lock:
      if self._stop:
        return
      self._stop = True
    if self._client:
      self._client.close()
    if self._process:
      self._stop_process()
    if self._stderr_thread:
      self._stderr_thread.join()
    if self._stdout_thread:
      self._stdout_thread.join()

  def _stop_process(self) -> None:
    if not self._process:
      return
    self._process.send_signal(2)
    try:
      self._process.wait(timeout=10.0)
      return
    except subprocess.TimeoutExpired:
      pass

    logging.warning(
        "Closing reach connect process is taking too long, sending SIGTERM...")
    self._process.terminate()
    try:
      self._process.wait(timeout=10.0)
      return
    except subprocess.TimeoutExpired:
      pass

    logging.warning(
        "Closing reach connect process is taking too long, sending SIGKILL...")
    self._process.kill()
    try:
      self._process.wait(timeout=10.0)
    except subprocess.TimeoutExpired:
      logging.error("reach connect failed - did not respond to SIGKILL")

  def close(self) -> None:
    """Close the connection to the local client."""
    self._close()


def reach_connect_webrtc(robot_id: str,
                         working_directory: Optional[pathlib.Path] = None,
                         download_reach_tool: bool = True,
                         download_webrtc_headless: bool = True,
                         reach_connect_arguments: Optional[List[str]] = None,
                         kwargs: Optional[Dict[str, Any]] = None) -> host.Host:
  """Connect to a remote robot.

  Args:
    robot_id: the robot id to connect to.
    working_directory: optional directory to run within.
    download_reach_tool: if true, will download the reach tool.
    download_webrtc_headless: if true, will automatically download
      webtrc_headless.
    reach_connect_arguments: optional list of arguments to the reach connect
      tool.
    kwargs: the optional kwargs to the connect host.

  Returns:
    Host interface if successful.
  """
  if not kwargs:
    kwargs = {}
  return host_impl.HostImpl(
      ReachConnectClient(robot_id, working_directory, download_reach_tool,
                         download_webrtc_headless, True,
                         reach_connect_arguments), **kwargs)


def reach_connect_remote_tcp(
    robot_id: str,
    connect_host: Optional[str] = None,
    connect_port: Optional[int] = 50009,
    working_directory: Optional[pathlib.Path] = None,
    download_reach_tool: bool = True,
    reach_connect_arguments: Optional[List[str]] = None,
    kwargs: Optional[Dict[str, Any]] = None) -> host.Host:
  """Connect to a remote robot.

  Args:
    robot_id: the robot id to connect to.
    connect_host: the host to connect to. Defaults to <robot_id>.local
    connect_port: the port to connect to. Defaults to 50009.
    working_directory: optional directory to run within.
    download_reach_tool: if true, will download the reach tool.
    reach_connect_arguments: optional list of arguments to the reach connect
      tool.
    kwargs: the optional kwargs to the connect host.

  Returns:
    Host interface if successful.
  """
  if not reach_connect_arguments:
    reach_connect_arguments = []
  if not connect_host:
    connect_host = robot_id + ".local"
  if not kwargs:
    kwargs = {}
  reach_connect_arguments += [
      "-connect_host", connect_host, "-connect_port",
      str(connect_port)
  ]
  return host_impl.HostImpl(
      ReachConnectClient(robot_id, working_directory, download_reach_tool,
                         False, False, reach_connect_arguments), **kwargs)
