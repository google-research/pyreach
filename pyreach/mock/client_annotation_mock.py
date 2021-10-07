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
"""Interface for interacting with text instructions."""

from typing import Callable, Optional
from pyreach.common.proto_gen import logs_pb2  # type: ignore
from pyreach import client_annotation
from pyreach import core


class ClientAnnotationMock(client_annotation.ClientAnnotation):
  """ClientAnnotation generates annotations of the logs from the client."""

  def annotate(
      self,
      annotation: logs_pb2.ClientAnnotation  # type: ignore
  ) -> core.PyReachStatus:
    """Annotate the logs with the given client annotation.

    Args:
      annotation: The annotation to log.

    Returns:
      The annotation PyReachStatus.
    """
    # TODO(gramlich): This is totally broken!
    return core.PyReachStatus(0.0)

  def async_annotate(
      self,
      annotation: logs_pb2.ClientAnnotation,  # type: ignore
      callback: Optional[Callable[[core.PyReachStatus], None]] = None
  ) -> None:
    """Annotate the logs with the given client annotation.

    Args:
      annotation: The annotation to log.
      callback: callback when status is received.

    Returns:
      The annotation PyReachStatus.
    """
    _ = self.annotate(annotation)
