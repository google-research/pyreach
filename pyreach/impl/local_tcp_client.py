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
from typing import Any, Dict, Optional  # pylint: disable=unused-import

from pyreach import host
from pyreach.common.python import types_gen
from pyreach.core import PyReachError
from pyreach.impl import client as cli
from pyreach.impl import host_impl


def _send_thread(sock: socket.socket,
                 input_queue: "queue.Queue[Optional[bytes]]") -> None:
  """Send thread sends data to a socket until it is closed.

  Args:
    sock: the socket to send to.
    input_queue: the input data queue of bytes. Exits if None.
  """
  while True:
    data = input_queue.get(block=True)
    if data is None:
      break
    try:
      sock.send(data)
    except OSError:
      break
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
                  close: "queue.Queue[None]",
                  started: "queue.Queue[bool]") -> None:
  """Process for reading from a socket and writing to the socket.

  Args:
    hostname: the hostname to connect to.
    port: the TCP port number.
    q: stream of DeviceData from the socket. None is sent on close.
    input_queue: the input data queue. Sending None closes the thread.
    close: Queue is sent when the socket closes.
    started: Queue is sent at startup, True if socket is started successfully,
             False otherwise. If false, no data will be sent to other queues.
  """
  sender: Optional[threading.Thread] = None
  started_value = False
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
    started_value = True
  finally:
    started.put(started_value)
  try:
    sender = threading.Thread(target=_send_thread, args=(sock, input_queue))
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
    sock.close()
  finally:
    close.put(None)
    if sender:
      sender.join()
    q.put(None)


def _serialize_process(
    input_queue: "queue.Queue[Optional[types_gen.CommandData]]",
    output_queue: "queue.Queue[Optional[bytes]]") -> None:
  """Serializes a stream of command data into a packet stream.

  Args:
    input_queue: input stream of command data, ends with None.
    output_queue: output stream of bytes, ends with None.
  """
  while True:
    try:
      cmd = input_queue.get(block=True)
      if cmd is None:
        output_queue.put(None)
        break
      output_queue.put((json.dumps(cmd.to_json()) + "\n").encode("utf-8"))
    except KeyboardInterrupt:
      pass


class LocalTCPClient(cli.Client):
  """Class to implement a local TCP client."""

  _stop: bool
  _lock: threading.Lock
  _queue: "queue.Queue[Optional[types_gen.DeviceData]]"
  _input_queue: "queue.Queue[Optional[types_gen.CommandData]]"
  _close_queue: "queue.Queue[None]"
  _process: multiprocessing.Process
  _serialize: multiprocessing.Process
  _close_thread: threading.Thread

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
    self._stop = False
    self._lock = threading.Lock()
    self._queue = multiprocessing.Queue()
    self._input_queue = multiprocessing.Queue()
    self._close_queue = multiprocessing.Queue()
    cmd_data_queue: "queue.Queue[Optional[bytes]]" = multiprocessing.Queue()
    started: "queue.Queue[bool]" = multiprocessing.Queue()
    self._process = multiprocessing.Process(
        target=_read_process,
        args=(hostname, port, self._queue, cmd_data_queue, self._close_queue,
              started))
    self._process.start()
    self._serialize = multiprocessing.Process(
        target=_serialize_process,
        args=(self._input_queue, cmd_data_queue))
    self._serialize.start()
    if not started.get(block=True):
      self._input_queue.put(None)
      raise PyReachError("Failed to connect")
    self._close_thread = threading.Thread(target=self._wait_for_close)
    self._close_thread.start()

  def _wait_for_close(self) -> None:
    """Wait for the process to close."""
    self._close_queue.get(block=True)
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
      if self._stop:
        return
      self._stop = True
    self._input_queue.put(None)

  def close(self) -> None:
    """Close the connection to the local client."""
    self._close()
    self._process.join()
    self._serialize.join()
    self._close_thread.join()


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
