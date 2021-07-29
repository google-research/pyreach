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

"""Interface for interacting with an OracleMock device."""
from typing import Optional, Callable

from pyreach import core
from pyreach import oracle


class OracleMock(oracle.Oracle):
  """Interface for the Oracle device."""

  def enable_tagged_request(self, intent: str, prediction_type: str,
                            request_type: str, task_code: str,
                            label: str) -> None:
    """Start tagged requests for the Oracle.

    Args:
      intent: The intent for the oracle.
      prediction_type: The prediction_type for the oracle.
      request_type: The request_type for the oracle.
      task_code: The task_code for the oracle.
      label: The label for the oracle.
    """
    raise NotImplementedError

  def disable_tagged_request(self) -> None:
    """Stop tagged requests for the Oracle."""
    raise NotImplementedError

  def prediction(self) -> Optional[oracle.Prediction]:
    """Return the latest prediction if available."""
    raise NotImplementedError

  def add_update_callback(
      self,
      callback: Callable[[oracle.Prediction], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback for frames.

    Args:
      callback: Callback called when a prediction arrives. If it returns True,
        the callback will be stopped.
      finished_callback: Optional callback, called when the callback is stopped
        or if the oracle is closed.

    Returns:
      A function that when called stops the callback.

    """
    raise NotImplementedError

  def fetch_prediction(self,
                       intent: str,
                       prediction_type: str,
                       request_type: str,
                       task_code: str,
                       label: str,
                       timeout: float = 15.0) -> oracle.Prediction:
    """Fetch a new prediction.

    Args:
      intent: The intent for the oracle.
      prediction_type: The prediction_type for the oracle.
      request_type: The request_type for the oracle.
      task_code: The task_code for the oracle.
      label: The label for the oracle.
      timeout: The optional maximum time to wait for the prediction. If not
        specified, it defaults to 15 seconds.

    Raises:
      PyReachError if timeout.

    Returns:
      A new prediction.

    """
    raise NotImplementedError

  def async_fetch_prediction(self,
                             intent: str,
                             prediction_type: str,
                             request_type: str,
                             task_code: str,
                             label: str,
                             callback: Optional[Callable[[oracle.Prediction],
                                                         None]] = None,
                             error_callback: Optional[Callable[
                                 [core.PyReachStatus], None]] = None,
                             timeout: float = 30) -> None:
    """Fetch a new prediction asynchronously.

    Args:
      intent: The intent for the oracle.
      prediction_type: The prediction_type for the oracle.
      request_type: The request_type for the oracle.
      task_code: The task_code for the oracle.
      label: The label for the oracle.
      callback: callback called when an image arrives. If the camera fails to
        load an image, callback will not be called.
      error_callback: optional callback called if there is an error.
      timeout: the timeout of the callback (default 30 seconds).
    """
    raise NotImplementedError
