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

"""Implementation for metrics devices."""
import queue
import threading
import time
from typing import Callable, Dict, List, Optional, Tuple
import uuid
from pyreach import metrics
from pyreach.common.python import types_gen
from pyreach.impl import requester
from pyreach.impl import thread_util
from pyreach.impl import utils


class MetricDevice(requester.Requester[metrics.Metric]):
  """Device for getting metrics."""

  _metrics_lock: threading.Lock
  _cached_metrics: Dict[str, metrics.Metric]

  def __init__(self) -> None:
    """Init the device."""
    super().__init__()
    self._metrics_lock = threading.Lock()
    self._cached_metrics = {}

  def get_wrapper(self) -> Tuple["MetricDevice", "metrics.Metrics"]:
    """Get the wrapper for the device that should be shown to the user."""
    return self, MetricsImpl(self)

  def get_message_supplement(
      self, msg: types_gen.DeviceData) -> Optional[metrics.Metric]:
    """Get getting supplementary information for the request manager.

    Loads the metric and caches it.

    Args:
      msg: the message to convert.

    Returns:
      The message converted to a metrics.Metric.
    """
    if (msg.device_type == "server" and not msg.device_name and
        msg.data_type == "metric"):
      with self._metrics_lock:
        metric = self._metric_from_message(msg)
        self._cached_metrics[metric.key] = metric
        return metric
    return None

  def get_cached_metric(self, key: str) -> Optional[metrics.Metric]:
    """Get a cached metric value.

    Args:
      key: the key to read.

    Returns:
      Returns the Metric (if available).

    """
    with self._metrics_lock:
      return self._cached_metrics.get(key)

  def start_pick(
      self,
      timeout: Optional[float] = None,
      callback: Optional[Callable[[metrics.Metric], bool]] = None,
      finished_callback: Optional[Callable[[], None]] = None
  ) -> Tuple[str, Callable[[], List[metrics.Metric]]]:
    """Start listening for data from a pick event.

    Args:
      timeout: Optional, timeout for the metric response.
      callback: Optional, will be called when a metric arrives.
      finished_callback: Optional, will be called when the last metric for the
        pick arrives.

    Returns:
      A tuple of the pick id and a function that will wait until all metrics for
      the pick arrive.

    """
    q: "queue.Queue[Optional[metrics.Metric]]" = queue.Queue()
    pick_id = str(uuid.uuid4())
    callback_wrapper: Callable[
        [metrics.Metric],
        bool] = lambda metric: self._pick_callback(q, pick_id, metric, callback)
    finished_callback_wrapper: Callable[
        [], None] = lambda: self._pick_finished_callback(q, finished_callback)
    stop_func = self.add_update_callback(callback_wrapper,
                                         finished_callback_wrapper)
    if timeout is not None:
      self.run(self._pick_timeout, timeout, stop_func)
    return pick_id, lambda: thread_util.extract_all_from_queue(q)

  def _pick_callback(
      self, q: "queue.Queue[Optional[metrics.Metric]]", pick_id: str,
      metric: metrics.Metric, callback: Optional[Callable[[metrics.Metric],
                                                          bool]]) -> bool:
    if metric.get_label("pick_id") == pick_id:
      q.put(metric)
      if callback is not None:
        if callback(metric):
          return True
      if metric.key in {
          "operator/success", "operator/pick_success", "operator/failure",
          "operator/pick_failure"
      }:
        return True
    return False

  def _pick_finished_callback(
      self, q: "queue.Queue[Optional[metrics.Metric]]",
      finished_callback: Optional[Callable[[], None]]) -> None:
    q.put(None)
    if finished_callback is not None:
      finished_callback()

  def _pick_timeout(self, timeout: float, stop_func: Callable[[],
                                                              None]) -> None:
    start = time.time()
    while True:
      delta = time.time() - start
      if delta >= timeout:
        break
      if self.wait(timeout - delta):
        break
    stop_func()

  @classmethod
  def _metric_from_message(cls, msg: types_gen.DeviceData) -> "metrics.Metric":
    """Convert JSON message into a Metric."""
    key = ""
    float_value = 0.0
    if msg.metric_value is not None:
      key = msg.metric_value.key
      float_value = msg.metric_value.float_value
    labels = [(label.key, label.value) for label in msg.labels]
    event_params = [
        (event_param.key, event_param.value) for event_param in msg.event_params
    ]
    return metrics.Metric(
        utils.time_at_timestamp(msg.ts), msg.seq, key, float_value,
        tuple(labels), tuple(event_params))


class MetricsImpl(metrics.Metrics):
  """A class for managing Metrics."""

  _device: MetricDevice

  def __init__(self, device: MetricDevice):
    """Init the wrapper.

    Args:
      device: The device.
    """
    self._device = device

  def add_update_callback(
      self,
      callback: Callable[[metrics.Metric], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback for metrics.

    Args:
      callback: Callback called when a metric arrives. If it returns True, the
        callback will be stopped.
      finished_callback: Optional callback, called when the callback is stopped
        or if the camera is closed.

    Returns:
      A function that when called stops the callback.

    """
    return self._device.add_update_callback(callback, finished_callback)

  def get_metric(self, key: str) -> Optional[metrics.Metric]:
    """Get a cached metric value.

    Args:
      key: the key to read.

    Returns:
      Get the metrics.
    """
    return self._device.get_cached_metric(key)

  def start_pick(
      self,
      timeout: Optional[float] = None,
      callback: Optional[Callable[[metrics.Metric], bool]] = None,
      finished_callback: Optional[Callable[[], None]] = None
  ) -> Tuple[str, Callable[[], List[metrics.Metric]]]:
    """Start listening for data from a pick event.

    Args:
      timeout: Optional, timeout for the metric response.
      callback: Optional, will be called when a metric arrives.
      finished_callback: Optional, will be called when the last metric for the
        pick arrives.

    Returns:
      A tuple of the pick id and a function that will wait until all metrics for
      the pick arrive.

    """
    return self._device.start_pick(timeout, callback, finished_callback)
