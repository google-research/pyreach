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

"""Implementation of the PyReach Logger interface."""
import logging  # type: ignore
import queue  # pylint: disable=unused-import
import threading
from typing import Callable, Dict, Optional, Tuple

from pyreach import core
from pyreach import logger
from pyreach.common.python import types_gen
from pyreach.impl import requester
from pyreach.impl import snapshot_impl
from pyreach.impl import thread_util
from pyreach.impl import utils
from pyreach.snapshot import Snapshot


class LoggerDevice(requester.Requester[core.PyReachStatus]):
  """Device for logger."""

  _time_lock: threading.Lock
  _task_time_lock: threading.Lock
  _start_times: Dict[str, int]
  _task_start_ts: int
  _task_end_ts: int

  def __init__(self) -> None:
    """Construct a logger."""
    super().__init__()
    self._time_lock = threading.Lock()
    self._task_time_lock = threading.Lock()
    self._start_times = {}
    self._task_start_ts: int = 0
    self._task_end_ts: int = 0

  def get_message_supplement(
      self, msg: types_gen.DeviceData) -> Optional[core.PyReachStatus]:
    """Get additional message."""
    if (msg.device_type == "client-annotation" and not msg.device_name and
        msg.data_type == "cmd-status"):
      return utils.pyreach_status_from_message(msg)
    return None

  def get_wrapper(self) -> Tuple["LoggerDevice", "logger.Logger"]:
    """Get wrapper for the device that should be shown to the user."""
    return self, LoggerImpl(self)

  def start_annotation_interval(
      self,
      name: str,
      log_channel_id: str = ""
  ) -> ("queue.Queue[Optional[Tuple[types_gen.DeviceData, "
        "Optional[core.PyReachStatus]]]]"):
    """Generate an event marking the start of an interval.

    Args:
      name: name of the interval.
      log_channel_id: log channel of the interval.

    Returns:
      A queue of response.
    """
    with self._time_lock:
      self._start_times[log_channel_id] = utils.timestamp_now()
    return self.send_tagged_request(
        types_gen.CommandData(
            ts=utils.timestamp_now(),
            tag=utils.generate_tag(),
            device_type="client-annotation",
            data_type="client-annotation",
            client_annotation=types_gen.ClientAnnotation(
                interval_start=types_gen.IntervalStart(name=name))),
        timeout=30)

  def end_annotation_interval(
      self,
      name: str,
      log_channel_id: str = "",
      start_time: Optional[float] = None,
      end_time: Optional[float] = None
  ) -> ("queue.Queue[Optional[Tuple[types_gen.DeviceData, "
        "Optional[core.PyReachStatus]]]]"):
    """Generate an event marking the end of an interval.

    Args:
      name: name of the interval.
      log_channel_id: log channel of the interval.
      start_time: the start time of the interval.
      end_time: the end time of the interval.

    Returns:
      A queue of response.
    """
    with self._time_lock:
      if start_time is None:
        start_timestamp = self._start_times.get(log_channel_id,
                                                utils.timestamp_now())
      else:
        start_timestamp = utils.timestamp_at_time(start_time)
    end_timestamp = utils.timestamp_now(
    ) if end_time is None else utils.timestamp_at_time(end_time)
    return self.send_tagged_request(
        types_gen.CommandData(
            ts=utils.timestamp_now(),
            tag=utils.generate_tag(),
            device_type="client-annotation",
            data_type="client-annotation",
            client_annotation=types_gen.ClientAnnotation(
                interval_end=types_gen.IntervalEnd(
                    name=name, start_ts=start_timestamp,
                    end_ts=end_timestamp))),
        timeout=30)

  def start_task(self, event_params: Dict[str, str]) -> None:
    """Start a task.

    Args:
      event_params: custom parameters of the event.
    """
    with self._task_time_lock:
      self._task_start_ts = utils.timestamp_now()

      self.send_cmd(
          types_gen.CommandData(
              ts=self._task_start_ts,
              device_type="operator",
              data_type="event-start",
              event_params=sorted([
                  types_gen.KeyValue(key=key, value=value)
                  for key, value in event_params.items()
              ],
                                  key=lambda obj: obj.key)))

  def end_task(self, event_params: Dict[str, str]) -> None:
    """End a task.

    Args:
      event_params: custom parameters of the event.
    """
    with self._task_time_lock:
      self._task_end_ts = utils.timestamp_now()

      self.send_cmd(
          types_gen.CommandData(
              ts=self._task_end_ts,
              device_type="operator",
              data_type="event",
              event_name="pick",
              event_duration=float(self._task_end_ts - self._task_start_ts) /
              1e3,
              event_params=sorted([
                  types_gen.KeyValue(key=key, value=value)
                  for key, value in event_params.items()
              ],
                                  key=lambda obj: obj.key)))

  def send_snapshot(self, snapshot: Snapshot) -> None:
    """Send a snapshot.

    Args:
      snapshot: The snapshot to send.
    """
    self.send_cmd(
        types_gen.CommandData(
            ts=utils.timestamp_now(),
            device_type="client-annotation",
            data_type="client-annotation",
            snapshot=snapshot_impl.convert_snapshot(snapshot)))


class LoggerImpl(logger.Logger):
  """A class for accessing logs."""

  _device: LoggerDevice

  def __init__(self, device: LoggerDevice) -> None:
    """Construct a logger implementation.

    Args:
      device: The device to log to.
    """
    self._device = device

  def start_task(self, event_params: Dict[str, str]) -> None:
    """Start a task.

    Args:
      event_params: custom parameters of the event.
    """
    self._device.start_task(event_params)

  def end_task(self, event_params: Dict[str, str]) -> None:
    """End a task.

    Args:
      event_params: custom parameters of the event.
    """
    self._device.end_task(event_params)

  def send_snapshot(self, snapshot: Snapshot) -> None:
    """Send a snapshot.

    Args:
      snapshot: The snapshot to send.
    """
    self._device.send_snapshot(snapshot)

  def start_annotation_interval(self,
                                name: str,
                                log_channel_id: str = "") -> core.PyReachStatus:
    """Start an annotation interval.

    Args:
      name: Name of the annotation interval.
      log_channel_id: channel ID of the log.

    Returns:
      Return status of the call.

    """
    q = self._device.start_annotation_interval(name, log_channel_id)
    msgs = thread_util.extract_all_from_queue(q)
    if not msgs:
      return core.PyReachStatus(
          utils.timestamp_now(), status="rejected", error="timeout")
    if len(msgs) != 1:
      logging.warning("expected single message, got %d", len(msgs))
    result = msgs[0][1]
    if result is None:
      return core.PyReachStatus(
          utils.timestamp_now(), status="rejected", error="timeout")
    return result

  def async_start_annotation_interval(
      self,
      name: str,
      log_channel_id: str = "",
      callback: Optional[Callable[[core.PyReachStatus], None]] = None) -> None:
    """Generate a message that marks the start of an annotation interval.

    Non-blocking.

    Args:
      name: the interval name.
      log_channel_id: channel id for this log entry.
      callback: callback when status is received.
    """
    q = self._device.start_annotation_interval(name, log_channel_id)
    self._device.queue_to_error_callback(q, callback, callback)

  def end_annotation_interval(
      self,
      name: str,
      log_channel_id: str = "",
      start_time: Optional[float] = None,
      end_time: Optional[float] = None) -> core.PyReachStatus:
    """Generate a message that marks the end of an annotation interval.

    Non-blocking version.

    Args:
      name: Name of the interval.
      log_channel_id: logging channel of the interval.
      start_time: start time of the interval.
      end_time: end time of the interval.

    Returns:
      Status of the command.
    """
    q = self._device.end_annotation_interval(name, log_channel_id, start_time,
                                             end_time)
    msgs = thread_util.extract_all_from_queue(q)
    if not msgs:
      return core.PyReachStatus(
          utils.timestamp_now(), status="rejected", error="timeout")
    if len(msgs) != 1:
      logging.warning("expected single message, got %d", len(msgs))
    result = msgs[0][1]
    if result is None:
      return core.PyReachStatus(
          utils.timestamp_now(), status="rejected", error="timeout")
    return result

  def async_end_annotation_interval(
      self,
      name: str,
      log_channel_id: str = "",
      start_time: Optional[float] = None,
      end_time: Optional[float] = None,
      callback: Optional[Callable[[core.PyReachStatus], None]] = None) -> None:
    """Generate a message that marks the end of an annotation interval.

    Non-blocking version.

    Args:
      name: Name of the interval.
      log_channel_id: logging channel of the interval.
      start_time: start time of the interval.
      end_time: end time of the interval.
      callback: callback when the request is complete.
    """
    q = self._device.end_annotation_interval(name, log_channel_id, start_time,
                                             end_time)
    self._device.queue_to_error_callback(q, callback, callback)
