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

"""LoggerMock unit tests."""

from typing import Callable, Dict, Optional

from pyreach import core
from pyreach import logger
from pyreach import snapshot as snapshot_lib


class LoggerMock(logger.Logger):
  """Interface for generating special log entries in the Reach server log."""

  def __init__(self) -> None:
    """Initialize the MockLogger."""
    # super().__init()
    pass

  def start_task(self, event_params: Dict[str, str]) -> None:
    """Indicate a task has started.

    Args:
      event_params: additional session information in name-value pair.
    """
    pass

  def end_task(self, event_params: Dict[str, str]) -> None:
    """Indicate a task has ended.

    Args:
      event_params: additional session information in name-value pair.
    """
    raise NotImplementedError

  def send_snapshot(self, snapshot: snapshot_lib.Snapshot) -> None:
    """Send a snapshot.

    Args:
      snapshot: The snapshot to send.
    """
    pass

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
    raise NotImplementedError

  def async_start_annotation_interval(
      self,
      name: str,
      log_channel_id: str = "",
      callback: Optional[Callable[[core.PyReachStatus], None]] = None,
  ) -> None:
    """Start an annotation interval asynchronously.

    Args:
      name: Name of the annotation interval.
      log_channel_id: Channel ID of the annotation.
      callback: callback when message is delivered.
    """
    raise NotImplementedError

  def end_annotation_interval(
      self,
      name: str,
      log_channel_id: str = "",
      start_time: Optional[float] = None,
      end_time: Optional[float] = None) -> core.PyReachStatus:
    """End an annotation interval.

    Args:
      name: Name of the internal.
      log_channel_id: Channel ID of this internal.
      start_time: interval start time.
      end_time: interval end time.
    """
    raise NotImplementedError

  def async_end_annotation_interval(
      self,
      name: str,
      log_channel_id: str = "",
      start_time: Optional[float] = None,
      end_time: Optional[float] = None,
      callback: Optional[Callable[[core.PyReachStatus], None]] = None) -> None:
    """End an asynchronous annotation interval asynchronously.

    Args:
      name: Name of this annotation.
      log_channel_id: Channel ID of the annotation.
      start_time: Annotation start time.
      end_time: Annotation end time.
      callback: callback when the annotation is done.
    """
    raise NotImplementedError
