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
"""Provide a local TCP client."""

import json
import logging
import multiprocessing
import queue  # pylint: disable=unused-import
import socket
import threading
import time
from typing import Any, Dict, Optional  # pylint: disable=unused-import

from pyreach import host
from pyreach.common.python import types_gen
from pyreach.core import PyReachError
from pyreach.impl import client as cli
from pyreach.impl import host_impl


class _PingManager:
  """Manage reading from a ping queue.."""
  _ping_queue: "queue.Queue[None]"
  _time_time: float

  def __init__(self, ping_queue: "queue.Queue[None]") -> None:
    """Send thread sends data to a socket until it is closed.

    Args:
      ping_queue: ping queue stores pings from the main process.
    """
    self._ping_queue = ping_queue
    self._ping_time = time.time()

  def update(self) -> bool:
    """Flush ping queue, return true if should continue."""
    while True:
      try:
        self._ping_queue.get(block=False)
        self._ping_time = time.time()
      except queue.Empty:
        break
    if time.time() - self._ping_time > 1.0:
      return False
    return True


def _send_thread(sock: socket.socket,
                 input_queue: "queue.Queue[Optional[bytes]]",
                 ping_queue: "queue.Queue[None]") -> None:
  """Send thread sends data to a socket until it is closed.

  Args:
    sock: the socket to send to.
    input_queue: the input data queue of bytes. Exits if None.
    ping_queue: ping queue stores pings from the main process.
  """
  ping_manager = _PingManager(ping_queue)
  try:
    while True:
      if not ping_manager.update():
        logging.warning(
            "sending thread and socket process are due to lack of ping from "
            "the main process")
        break
      data: Optional[bytes] = None
      try:
        data = input_queue.get(block=True, timeout=0.5)
      except queue.Empty:
        continue
      if data is None:
        break
      try:
        sock.send(data)
      except OSError:
        break
  finally:
    try:
      sock.shutdown(socket.SHUT_RD)
    except OSError:
      pass
    try:
      sock.close()
    except OSError:
      pass


def _read_process(hostname: str, port: int,
                  q: "queue.Queue[Optional[types_gen.DeviceData]]",
                  input_queue: "queue.Queue[Optional[bytes]]",
                  started: "queue.Queue[bool]",
                  ping_queue: "queue.Queue[None]") -> None:
  """Process for reading from a socket and writing to the socket.

  Args:
    hostname: the hostname to connect to.
    port: the TCP port number.
    q: stream of DeviceData from the socket. None is sent on close.
    input_queue: the input data queue. Sending None closes the thread.
    started: Queue is sent at startup, True if socket is started successfully,
      False otherwise. If false, no data will be sent to other queues.
    ping_queue: ping queue stores pings from the main process.
  """
  sender: Optional[threading.Thread] = None
  sock: Optional[socket.socket] = None
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # See end of: https://docs.python.org/3/library/socket.html
    # For description on SE_REUSEADDR.
    # Note this may mean we need to ensure we don't collide sockets.
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # TCP_NODELAY ensures that Nagle's algorithm is disabled,
    # which otherwise will cause buffering.
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    sock.settimeout(60.0)  # Seconds
    sock.connect((hostname, port))
    started.put(True)
    sender = threading.Thread(
        target=_send_thread, args=(sock, input_queue, ping_queue))
    sender.start()
    pb = ""
    while True:
      packet = b""
      try:
        packet = sock.recv(8)
      except OSError:
        break
      if not packet:
        break
      try:
        pb += packet.decode("utf-8")
      except UnicodeError:
        logging.warning("packet could not be decoded to utf-8")
        break
      while True:
        next_pos = pb.find("\n")
        if next_pos < 0:
          break
        try:
          msg = json.loads(pb[0:next_pos])
          data = types_gen.DeviceData.from_json(msg)
          q.put(data)
        except json.JSONDecodeError as e:
          logging.warning("packet could not be decoded from JSON: %s", e)
        pb = pb[next_pos + 1:]
    try:
      sock.shutdown(socket.SHUT_RD)
    except OSError:
      pass
  finally:
    try:
      if sock:
        try:
          sock.close()
        except OSError:
          pass
    finally:
      if sender:
        sender.join()


def _serialize_process(
    input_queue: "queue.Queue[Optional[types_gen.CommandData]]",
    output_queue: "queue.Queue[Optional[bytes]]",
    ping_queue: "queue.Queue[None]") -> None:
  """Serializes a stream of command data into a packet stream.

  Args:
    input_queue: input stream of command data, ends with None.
    output_queue: output stream of bytes, ends with None.
      ping_queue: ping queue stores pings from the main process.
  """
  ping_manager = _PingManager(ping_queue)
  while True:
    if not ping_manager.update():
      logging.warning(
          "serialization process closing due to lack of ping from the "
          "main process")
      break
    try:
      cmd = input_queue.get(block=True, timeout=0.5)
      if cmd is None:
        break
      output_queue.put((json.dumps(cmd.to_json()) + "\n").encode("utf-8"))
    except queue.Empty:
      pass
    except KeyboardInterrupt:
      pass


class LocalTCPClient(cli.Client):
  """Class to implement a local TCP client."""

  _stop: threading.Event
  _lock: threading.Lock
  _queue: "queue.Queue[Optional[types_gen.DeviceData]]"
  _input_queue: "queue.Queue[Optional[types_gen.CommandData]]"
  _ping_reader_queue: "queue.Queue[None]"
  _ping_serialize_queue: "queue.Queue[None]"
  _cmd_data_queue: "queue.Queue[Optional[bytes]]"
  _started_queue: "queue.Queue[bool]"
  _ping_thread: Optional[threading.Thread]
  _process: Optional[multiprocessing.Process]
  _serialize: Optional[multiprocessing.Process]
  _close_reader_thread: Optional[threading.Thread]
  _close_serialize_thread: Optional[threading.Thread]

  def __init__(self, hostname: str = "localhost", port: int = 50008):
    """Init a LocalTCPClient.

    Args:
      hostname: The local host to connect to as a string. This argument is
        optional and defaults to "localhost".
      port: The port number to connect to.  This argument is optional and
        defaults to 50008.

    Raises:
       PyReachError: if connection fails.
    """
    super().__init__()
    self._stop = threading.Event()
    self._lock = threading.Lock()
    self._queue = multiprocessing.Queue()
    self._input_queue = multiprocessing.Queue()
    self._ping_reader_queue = multiprocessing.Queue()
    self._ping_serialize_queue = multiprocessing.Queue()
    self._cmd_data_queue = multiprocessing.Queue()
    self._started_queue = multiprocessing.Queue()
    self._ping_thread = None
    self._process = None
    self._serialize = None
    self._close_reader_thread = None
    self._close_serialize_thread = None
    success = False
    try:
      self._ping_thread = threading.Thread(target=self._send_pings, args=())
      self._ping_thread.start()
      self._process = multiprocessing.Process(
          target=_read_process,
          args=(hostname, port, self._queue, self._cmd_data_queue,
                self._started_queue, self._ping_reader_queue))
      self._process.start()
      self._serialize = multiprocessing.Process(
          target=_serialize_process,
          args=(self._input_queue, self._cmd_data_queue,
                self._ping_serialize_queue))
      self._serialize.start()
      self._close_reader_thread = threading.Thread(
          target=self._wait_for_close_reader)
      self._close_reader_thread.start()
      self._close_serialize_thread = threading.Thread(
          target=self._wait_for_close_serialize)
      self._close_serialize_thread.start()
      if not self._started_queue.get(block=True):
        self.close()
        raise PyReachError("Failed to connect")
      success = True
    finally:
      if not success:
        self.close()

  def _send_pings(self) -> None:
    """Ping the processes."""
    while not self._stop.wait(timeout=0.1):
      self._ping_reader_queue.put(None)
      self._ping_serialize_queue.put(None)

  def _wait_for_close_reader(self) -> None:
    """Wait for the reader process to close."""
    if self._process:
      self._process.join()
    self._queue.put(None)
    self._started_queue.put(False)
    self._close()

  def _wait_for_close_serialize(self) -> None:
    """Wait for the serialize process to close."""
    if self._serialize:
      self._serialize.join()
    self._cmd_data_queue.put(None)
    self._close()

  def get_queue(self) -> "queue.Queue[Optional[types_gen.DeviceData]]":
    """Get the queue for the LocalTCPClient."""
    return self._queue

  def send_cmd(self, cmd: types_gen.CommandData) -> None:
    """Send a command to the client.

    Args:
      cmd: The CommandData to send to the client.
    """
    self._input_queue.put(cmd)

  def _close(self) -> None:
    with self._lock:
      if self._stop.is_set():
        return
      self._stop.set()
    self._input_queue.put(None)

  def close(self) -> None:
    """Close the connection to the local client."""
    self._close()
    for p in [
        self._ping_thread, self._process, self._serialize,
        self._close_reader_thread, self._close_serialize_thread
    ]:
      if p:
        p.join()


def connect_local_tcp(hostname: str, port: int, kwargs: Dict[str,
                                                             Any]) -> host.Host:
  """Connect to Reach using TCP on specific host:port.

  Args:
    hostname: host name or IP address.
    port: TCP port to connect to.
    kwargs: additional argument.

  Returns:
    Host interface if successful.
  """
  return host_impl.HostImpl(LocalTCPClient(hostname, port), **kwargs)


if __name__ == "__main__":
  pass
