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
"""Interface for generating client annotations."""

import logging  # type: ignore
import queue  # pylint: disable=unused-import
from typing import Callable, Optional, Tuple

from pyreach.common.proto_gen import logs_pb2
from pyreach import client_annotation
from pyreach import core
from pyreach.common.python import types_gen
from pyreach.impl import requester
from pyreach.impl import thread_util
from pyreach.impl import utils


class ClientAnnotationDevice(requester.Requester[core.PyReachStatus]):
  """Device for client annotations."""

  def get_message_supplement(
      self, msg: types_gen.DeviceData) -> Optional[core.PyReachStatus]:
    """Get additional message."""
    if (msg.device_type == "client-annotation" and not msg.device_name and
        msg.data_type == "cmd-status"):
      return utils.pyreach_status_from_message(msg)
    return None

  def get_wrapper(
      self
  ) -> Tuple["ClientAnnotationDevice", "client_annotation.ClientAnnotation"]:
    """Get the wrapper for the device that should be shown to the user."""
    return self, ClientAnnotationImpl(self)

  def send_annotation(
      self, annotation: logs_pb2.ClientAnnotation
  ) -> ("queue.Queue[Optional[Tuple[types_gen.DeviceData, "
        "Optional[core.PyReachStatus]]]]"):
    """Annotate the logs with the given client annotation.

    Args:
      annotation: The annotation to log.

    Raises:
      PyReachError: if an interval annotation is sent.

    Returns:
      A queue of response.
    """
    data_annotation = types_gen.ClientAnnotation.from_proto(annotation)
    assert data_annotation
    if data_annotation.interval_start or data_annotation.interval_end:
      raise core.PyReachError(
          "Interval annotations must be sent via the logger device")
    return self.send_tagged_request(
        types_gen.CommandData(
            ts=utils.timestamp_now(),
            tag=utils.generate_tag(),
            device_type="client-annotation",
            data_type="client-annotation",
            client_annotation=data_annotation),
        timeout=30)


class ClientAnnotationImpl(client_annotation.ClientAnnotation):
  """ClientAnnotation generates annotations of the logs from the client."""
  _device: ClientAnnotationDevice

  def __init__(self, device: ClientAnnotationDevice) -> None:
    """Create the client annotation implementation.

    Args:
      device: The device implementation.
    """
    self._device = device

  def annotate(self,
               annotation: logs_pb2.ClientAnnotation) -> core.PyReachStatus:
    """Annotate the logs with the given client annotation.

    Args:
      annotation: The annotation to log.

    Raises:
      PyReachError: if an interval annotation is sent.

    Returns:
      The annotation PyReachStatus.
    """
    q = self._device.send_annotation(annotation)
    msgs = thread_util.extract_all_from_queue(q)
    if not msgs:
      return core.PyReachStatus(
          utils.timestamp_now(), status="rejected", error="timeout")
    if len(msgs) != 1:
      logging.warning("expected single message, got %d", len(msgs))
    result = msgs[len(msgs) - 1][1]
    if result is None:
      return core.PyReachStatus(
          utils.timestamp_now(), status="rejected", error="timeout")
    return result

  def async_annotate(
      self,
      annotation: logs_pb2.ClientAnnotation,
      callback: Optional[Callable[[core.PyReachStatus], None]] = None) -> None:
    """Annotate the logs with the given client annotation.

    Args:
      annotation: The annotation to log.
      callback: callback when status is received.

    Raises:
      PyReachError: if an interval annotation is sent.

    Returns:
      The annotation PyReachStatus.
    """
    q = self._device.send_annotation(annotation)
    self._device.queue_to_error_callback(q, callback, callback)
