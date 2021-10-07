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
"""Interface for generating metrics related log entries in the Reach server log.

This interface allows generation of special log records that is used for
metrics calculation.
"""

import dataclasses
from typing import Callable, Optional, Tuple


@dataclasses.dataclass(frozen=True)
class Metric:
  """A metric entry.

  Attributes:
    time: The time in seconds of the frame since 1970.
    sequence: The sequence number of the metric data.
    key: the metric key.
    float_value: The float value.
    labels: The labels list.
    event_params: The event params list.
  """

  time: float
  sequence: int
  key: str
  float_value: float
  labels: Tuple[Tuple[str, str], ...]
  event_params: Tuple[Tuple[str, str], ...]

  def get_label(self, name: str) -> Optional[str]:
    """Get the value of a label."""
    for key, value in self.labels:
      if key == name:
        return value
    return None

  def get_event_param(self, name: str) -> Optional[str]:
    """Get the value of a event param."""
    for key, value in self.event_params:
      if key == name:
        return value
    return None


class Metrics(object):
  """Interface for metrics."""

  def add_update_callback(
      self,
      callback: Callable[[Metric], bool],
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
    raise NotImplementedError

  def get_metric(self, key: str) -> Optional[Metric]:
    """Get a cached metric value.

    Args:
      key: the key to read.
    """
    raise NotImplementedError

  def start_pick(
      self,
      intent: Optional[str] = None,
      timeout: Optional[float] = None,
      callback: Optional[Callable[[Metric], bool]] = None,
      finished_callback: Optional[Callable[[], None]] = None
  ) -> Tuple[str, Callable[[], Tuple[Metric, ...]]]:
    """Start listening for data from a pick event.

    Args:
      intent: the intent for the last command. If None, will accept any.
      timeout: Optional.
      callback: Optional, will be called when a metric arrives.
      finished_callback: Optional, will be called when the last metric for the
        pick arrives.

    Returns:
      A tuple of the pick id and a function that will wait until all metrics for
      the pick arrive.

    """
    raise NotImplementedError
