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

"""Requester provides streaming capability for a DeviceBase."""

import queue
import threading
import time
from typing import Callable, Dict, Generic, List, Optional, Set, Tuple, TypeVar

from pyreach import core
from pyreach.common.python import types_gen
from pyreach.impl import device_base
from pyreach.impl import machine_interfaces
from pyreach.impl import thread_util
from pyreach.impl import utils

T = TypeVar("T")
U = TypeVar("U")


class DeviceRequest(Generic[T]):
  """Represents a request message."""

  _queue: "queue.Queue[Optional[Tuple[types_gen.DeviceData, Optional[T]]]]"
  _device_type: str
  _device_name: str
  _data_type: str
  _tag: Optional[str]
  _resend_time: Optional[float]
  _timeout: Optional[float]
  _expected_messages: Optional[int]
  _expect_cmd_status: bool
  _messages: int
  _cmd_status: Optional[Tuple[types_gen.DeviceData, Optional[T]]]
  _terminated: bool

  def __init__(self,
               device_type: str,
               device_name: str,
               data_type: str,
               tag: Optional[str],
               timeout: Optional[float],
               expect_messages: Optional[int] = None,
               expect_cmd_status: bool = True) -> None:
    """Construct a DeviceRequest.

    Args:
      device_type: The device type string (or DEVICE_ANY.)
      device_name: The device name string (or DEVICE_ANY.)
      data_type: The data type string.
      tag: The tag string or None for no tag.
      timeout: The timeout for the request in seconds or None for no timeout.
      expect_messages: Optional, if not specified, the request will complete
        after getting "rejected", "aborted", or "done" status. If specified, the
        request will complete after getting "rejected" or "aborted" status, or
        the number of messages is >= expect_messages and getting "done" status.
        Specifying "expect_messages" is required in the case of out-of-order
        messages.
      expect_cmd_status: True if a command status message is expected.
    """
    self._queue = queue.Queue()
    self._device_type = device_type
    self._device_name = device_name
    self._data_type = data_type
    self._tag = tag
    self._timeout = timeout
    self._resend_time = None
    self._expect_cmd_status = expect_cmd_status
    if tag is None:
      self._resend_time = time.time() + 1.0
    self._expect_messages = expect_messages
    if self._timeout is not None:
      self._timeout += time.time()
    self._messages = 0
    self._cmd_status = None
    self._terminated = False

  @property
  def tag(self) -> Optional[str]:
    """Return the tag."""
    return self._tag

  @property
  def device_type(self) -> str:
    """Return the device type."""
    return self._device_type

  @property
  def device_name(self) -> str:
    """Return the device name."""
    return self._device_name

  @property
  def queue(
      self
  ) -> "queue.Queue[Optional[Tuple[types_gen.DeviceData, Optional[T]]]]":
    """Return the request queue."""
    return self._queue

  def close(self) -> None:
    """Close the request."""
    if self._terminated:
      return
    self._queue.put(None)
    self._terminated = True

  def flush(self) -> None:
    """Flush the request queue."""
    self._queue.join()

  def on_poll(self) -> Tuple[bool, Optional[types_gen.CommandData]]:
    """Poll to determine in requester should be terminated.

    Should be called once per second to resend requests or determine if
    the requester should be terminated.

    Returns:
      Return (True, None) if the request is terminated and
      (False, CommandData(...)) otherwise.

    """
    if self._terminated:
      return self._terminated, None
    if self._timeout is not None and self._timeout <= time.time():
      self.close()
      return self._terminated, None
    if self._resend_time is not None and self._resend_time <= time.time():
      self._resend_time = time.time() + 1.0
      return False, types_gen.CommandData(
          device_type=self._device_type,
          device_name=self._device_name,
          ts=utils.timestamp_at_time(time.time()),
          tag="",
          data_type="frame-request")
    return self._terminated, None

  def _process_msg(self, msg: types_gen.DeviceData,
                   supplement: Optional[T]) -> None:
    """Process a DeviceData message.

    Args:
      msg: DeviceData message to process.
      supplement: Supplemental information generating by transforming the
        DeviceData (e.g. loading image).
    """
    if self._tag is not None and msg.tag == self._tag:
      if (self._expect_messages is not None and
          msg.data_type == "cmd-status" and msg.status == "done" and
          not msg.error and self._messages < self._expect_messages):
        self._cmd_status = (msg, supplement)
        return
      self._messages += 1
      self._queue.put((msg, supplement))
      if (self._expect_messages is not None and
          self._messages >= self._expect_messages and
          (self._cmd_status is not None or not self._expect_cmd_status)):
        if self._cmd_status is not None:
          self._queue.put(self._cmd_status)
        self.close()
        return
      if (msg.data_type == "cmd-status" and
          msg.status in set(["aborted", "done", "rejected"])):
        self.close()
      return
    elif self._tag is not None:
      return
    if (self._device_type == msg.device_type and
        self._device_name == msg.device_name and
        self._data_type == msg.data_type):
      self._queue.put((msg, supplement))
      self.close()

  def on_message(
      self, msg: types_gen.DeviceData,
      supplement: Optional[T]) -> Tuple[bool, Optional[types_gen.CommandData]]:
    """Call when a message is received.

    Args:
      msg: DeviceData message to process.
      supplement: Supplemental information generating by transforming the
        DeviceData (e.g. loading image).

    Returns:
      Return (True, None) if the request is terminated and
      (False, CommandData(...)) otherwise.
    """
    self._process_msg(msg, supplement)
    return self.on_poll()


class Requester(device_base.DeviceBase, Generic[T]):
  """Class to request a result."""

  _lock: threading.Lock
  _cached: Optional[T]
  _callback_manager: "thread_util.CallbackManager[T]"
  _requests: List["DeviceRequest[T]"]
  _last_request: Dict[Tuple[str, str], float]
  _untagged_request_period: Dict[Tuple[str, str], float]
  _untagged_request_counter: Dict[Tuple[str, str], int]
  _enable_tagged_requests: Set[Tuple[str, str]]
  _interfaces: Optional[machine_interfaces.MachineInterfaces]

  def __init__(self) -> None:
    """Init a Requester."""
    super().__init__()
    self._lock = threading.Lock()
    self._cached = None
    self._callback_manager = thread_util.CallbackManager()
    self._requests = []
    self._last_request = {}
    self._untagged_request_counter = {}
    self._untagged_request_period = {}
    self._enable_tagged_requests = set()
    self._interfaces = None

  def get_message_supplement(self, msg: types_gen.DeviceData) -> Optional[T]:
    """Allow subclass to provide custom transformation.

    Args:
      msg: DeviceData that needs to be transformed.

    Returns:
      Device specific transformed object. By default, None.
    """
    return None

  def get_cached(self) -> Optional[T]:
    """Get the latest cached value from Requester.

    Returns:
      Returns the latest cached value (if present) and None otherwise.
    """
    with self._lock:
      return self._cached

  def start(self) -> None:
    """Start a Requester."""
    device_base.DeviceBase.start(self)
    self.poll(1.0, self._on_poll)

  def set_machine_interfaces(
      self, interfaces: Optional[machine_interfaces.MachineInterfaces]) -> None:
    """Set the machine interface settings.

    Args:
      interfaces: the machine interfaces discovered.
    """
    super().set_machine_interfaces(interfaces)
    with self._lock:
      self._interfaces = interfaces

  def set_untagged_request_period(self, device_type: str, device_name: str,
                                  data_type: str,
                                  period: Optional[float]) -> None:
    """Set the untagged request period for a Requester.

    Args:
      device_type: The device type as a string.
      device_name: The device name as a string.
      data_type: The data name as a string.
      period: The polling period in sec.
    """
    if period is not None and period <= 0:
      raise core.PyReachError("Request period must be greater than zero")
    with self._lock:
      request_type = (
          self._interfaces and self._interfaces.get_request_strategy(
              device_type, device_name, data_type))
      if request_type == machine_interfaces.InterfaceType.PUBLISH:
        self._set_untagged_request_period(device_type, device_name, None)
      else:
        self._set_untagged_request_period(device_type, device_name, period)

  def _set_untagged_request_period(self, device_type: str, device_name: str,
                                   period: Optional[float]) -> None:
    device_pair = (device_type, device_name)
    if period is None:
      if device_pair in self._untagged_request_period:
        self._untagged_request_counter[device_pair] = (
            self._untagged_request_counter.get(device_pair, 0) + 1)
        del self._untagged_request_period[device_pair]
    elif (device_pair not in self._untagged_request_period or
          self._untagged_request_period[device_pair] != period):
      self._untagged_request_period[device_pair] = period
      self._untagged_request_counter[
          device_pair] = self._untagged_request_counter.get(device_pair, 0) + 1
      self.poll(period, self._untagged_poll, device_type, device_name,
                self._untagged_request_counter[device_pair])

  def _untagged_poll(self, device_type: str, device_name: str,
                     counter: int) -> bool:
    """Retrigger a poll based a counter for a Requester.

    Args:
      device_type: The device type as a string.
      device_name: The device name as a string.
      counter: Expected counter value.

    Returns:
      True to stop the request.
    """
    with self._lock:
      if self._untagged_request_counter[(device_type, device_name)] != counter:
        return True
    self.send_frame_request(device_type, device_name)
    return False

  def set_enable_tagged_request(self, device_type: str, device_name: str,
                                enable_tagged_requests: bool) -> None:
    """Set the enable tagged request flag.

    Args:
      device_type: The device type as a string.
      device_name: The device name as a string.
      enable_tagged_requests: True for enable tagged request.
    """
    with self._lock:
      if enable_tagged_requests:
        self._enable_tagged_requests.add((device_type, device_name))
      elif (device_type, device_name) in self._enable_tagged_requests:
        self._enable_tagged_requests.remove((device_type, device_name))
    self._on_poll()

  def _on_poll(self) -> bool:
    tagged: Set[Tuple[str, str]] = set()
    with self._lock:
      active = []
      for req in self._requests:
        terminated, resend = req.on_poll()
        if not terminated:
          active.append(req)
        if resend is not None:
          self.send_cmd(resend)
      self._requests = active
      for key in self._enable_tagged_requests:
        tagged.add(key)
      for request in self._requests:
        key = (request.device_type, request.device_name)
        if request.tag is not None and key in tagged:
          tagged.remove(key)
    for key in tagged:
      self.request_tagged(key[0], key[1], 20.0)
    return False

  def set_cached(self, supplement: Optional[T]) -> None:
    """Set the Device cache for a Requester.

    Args:
      supplement: The value to cache or None if no new value is present.
    """
    if supplement is not None:
      with self._lock:
        self._cached = supplement
      self._callback_manager.call(supplement)

  def on_device_data(self, msg: types_gen.DeviceData) -> None:
    """Invoke when a device data is received.

    Args:
      msg: The DeviceData message that is received.
    """
    # pylint: disable=assignment-from-none
    supplement = self.get_message_supplement(msg)
    self.set_cached(supplement)
    with self._lock:
      active = []
      for req in self._requests:
        terminated, resend = req.on_message(msg, supplement)
        if not terminated:
          active.append(req)
        if resend is not None:
          self.send_cmd(resend)
      self._requests = active
    self._on_poll()
    device_base.DeviceBase.on_device_data(self, msg)

  def flush(self) -> None:
    """Flush all data from the queues."""
    super().flush()
    with self._lock:
      reqs = self._requests.copy()
    for req in reqs:
      req.flush()

  def request_untagged(
      self,
      device_type: str,
      device_name: str,
      data_type: str,
      timeout: Optional[float] = None
  ) -> "queue.Queue[Optional[Tuple[types_gen.DeviceData, Optional[T]]]]":
    """Return a queue that gets untagged requests from Requester.

    Args:
      device_type: The devcie type as a string.
      device_name: The device name as a string.
      data_type: The data type as a string.
      timeout: The timeout in seconds or None for no timeout.

    Returns:
      Returns a Queue of the untagged DeviceData messages.
    """
    assert device_type
    assert data_type
    r: "DeviceRequest[T]" = DeviceRequest(device_type, device_name, data_type,
                                          None, timeout)
    with self._lock:
      self._requests.append(r)
    self.send_frame_request(device_type, device_name)
    self._on_poll()
    return r.queue

  def send_frame_request(self, device_type: str, device_name: str) -> None:
    """Send a frame request to a Requester.

    Args:
      device_type: The type of the device.
      device_name: The name of the device.
    """
    self.send_cmd(
        types_gen.CommandData(
            device_type=device_type,
            device_name=device_name,
            ts=utils.timestamp_at_time(time.time()),
            tag="",
            data_type="frame-request"))

  def request_tagged(
      self,
      device_type: str,
      device_name: str,
      timeout: Optional[float] = None,
      expect_messages: Optional[int] = None,
      expect_cmd_status: bool = True,
  ) -> "queue.Queue[Optional[Tuple[types_gen.DeviceData, Optional[T]]]]":
    """Request a tagged request Queue from a Requester.

    Args:
      device_type: The device type as a string.
      device_name: The device name as a string.
      timeout: The number of seconds before timing out or None for no timeout.
      expect_messages: The number of expected messages or None for the request
        to complete after getting "rejected", "aborted", or "done" status.
      expect_cmd_status: True if command status message are expected and False
        otherwise.

    Returns:
      Returns a queue containing the matching DeviceData messages.
    """
    assert device_type
    tag = utils.generate_tag()
    r: "DeviceRequest[T]" = DeviceRequest(device_type, device_name, "", tag,
                                          timeout, expect_messages,
                                          expect_cmd_status)
    with self._lock:
      self._requests.append(r)
    self.send_cmd(
        types_gen.CommandData(
            device_type=device_type,
            device_name=device_name,
            ts=utils.timestamp_at_time(time.time()),
            tag=tag,
            data_type="frame-request"))
    self._on_poll()
    return r.queue

  def send_tagged_request(
      self,
      cmd: types_gen.CommandData,
      timeout: Optional[float] = None,
      expect_messages: Optional[int] = None,
      expect_cmd_status: bool = True,
  ) -> "queue.Queue[Optional[Tuple[types_gen.DeviceData, Optional[T]]]]":
    """Send a tagged request.

    Args:
      cmd: The CommandData to use for the device type and name.
      timeout: The amount to wait before timing out or None for no timeout.
      expect_messages: The number of expected messages or None for the request
        to complete after getting "rejected", "aborted", or "done" status.
      expect_cmd_status: True if command status message are expected and False
        otherwise.

    Returns:
      Returns a queue for containing the requested DeviceData messages.
    """
    assert cmd.device_type
    assert cmd.tag
    r: "DeviceRequest[T]" = DeviceRequest(cmd.device_type, cmd.device_name, "",
                                          cmd.tag, timeout, expect_messages,
                                          expect_cmd_status)
    with self._lock:
      self._requests.append(r)
    self.send_cmd(cmd)
    self._on_poll()
    return r.queue

  def queue_to_callback(
      self,
      q: "queue.Queue[Optional[Tuple[types_gen.DeviceData, Optional[T]]]]",
      callback: Callable[[Tuple[types_gen.DeviceData, Optional[T]]],
                         None], finished_callback: Callable[[], None]) -> None:
    """Convert a queue of DeviceData into callbacks.

    The callback is executed on the thread pool of the device.

    Args:
      q: The DeviceData queue to use.
      callback: callback function for each DeviceData.
      finished_callback: callback when processing of DeviceData is done.
    """
    self.run(thread_util.queue_to_callback, q, callback, finished_callback)

  def queue_to_error_callback(
      self,
      q: "queue.Queue[Optional[Tuple[types_gen.DeviceData, Optional[T]]]]",
      callback: Optional[Callable[[T], None]],
      error_callback: Optional[Callable[[core.PyReachStatus], None]],
      transform: Optional[Callable[[types_gen.DeviceData, Optional[T]],
                                   Optional[T]]] = None
  ) -> None:
    """Queue to single state callback or error_callback.

    Args:
      q: The DeviceData queue to use.
      callback: The callback.
      error_callback: The error callback.
      transform: Override conversion of supplement.
    """
    if transform is None:
      # pylint: disable=unused-argument
      def identity_transform(msg: types_gen.DeviceData,
                             supplement: Optional[T]) -> Optional[T]:
        return supplement

      transform = identity_transform
    self.queue_to_error_callback_transform(q, callback, error_callback,
                                           transform)

  def queue_to_error_callback_transform(
      self,
      q: "queue.Queue[Optional[Tuple[types_gen.DeviceData, Optional[T]]]]",
      callback: Optional[Callable[[U], None]],
      error_callback: Optional[Callable[[core.PyReachStatus], None]],
      transform: Callable[[types_gen.DeviceData, Optional[T]], Optional[U]]
  ) -> None:
    """Queue to single state callback or error_callback.

    Args:
      q: The DeviceData queue to use.
      callback: The callback.
      error_callback: The error callback.
      transform: Override conversion of supplement.
    """
    self.run(self._queue_to_error_callback_transform, q, callback,
             error_callback, transform)

  def _queue_to_error_callback_transform(
      self,
      q: "queue.Queue[Optional[Tuple[types_gen.DeviceData, Optional[T]]]]",
      callback: Optional[Callable[[U], None]],
      error_callback: Optional[Callable[[core.PyReachStatus], None]],
      transform: Callable[[types_gen.DeviceData, Optional[T]], Optional[U]]
  ) -> None:
    """Queue to single state callback or error callback.

    Args:
      q: The DeviceData queue to use.
      callback: The callback.
      error_callback: The error callback.
      transform: Override conversion of supplement.
    """
    data = thread_util.extract_all_from_queue(q)
    msg = None
    status = None
    for step in data:
      if step[0].data_type == "cmd-status":
        status = utils.pyreach_status_from_message(step[0])
      transformed = transform(step[0], step[1])
      if transformed is not None:
        msg = transformed
    if msg is not None:
      if callback is not None:
        callback(msg)
    elif status is None:
      if error_callback is not None:
        error_callback(
            core.PyReachStatus(
                time=time.time(), status="done", error="timeout"))
    else:
      if error_callback is not None:
        error_callback(status)

  def add_update_callback(
      self,
      callback: Callable[[T], bool],
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

  def close(self) -> None:
    """Close the Requester."""
    with self._lock:
      reqs = self._requests.copy()
    for req in reqs:
      req.close()
    self._on_poll()
    self._on_poll()
    self._callback_manager.close()
    device_base.DeviceBase.close(self)
