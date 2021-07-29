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

from typing import List, Tuple, Callable, Optional

from pyreach import metrics


class MetricsMock(metrics.Metrics):
  """Interface for metrics."""

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
    raise NotImplementedError

  def get_metric(self, key: str) -> Optional[metrics.Metric]:
    """Get a cached metric value.

    Args:
      key: the key to read.
    """
    raise NotImplementedError

  def start_pick(
      self,
      timeout: Optional[float] = None,
      callback: Optional[Callable[[metrics.Metric], bool]] = None,
      finished_callback: Optional[Callable[[], None]] = None
  ) -> Tuple[str, Callable[[], List[metrics.Metric]]]:
    """Start listening for data from a pick event.

    Args:
      timeout: Optional.
      callback: Optional, will be called when a metric arrives.
      finished_callback: Optional, will be called when the last metric for the
        pick arrives.

    Returns:
      A tuple of the pick id and a function that will wait until all metrics for
      the pick arrive.

    """
    raise NotImplementedError
