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

"""Interface for interacting with an Oracle device.

An Oracle device is a ML model that runs on the Reach host. This is considered
the legacy way of integrating ML model with Reach. Because the ML model
is tightly coupled with Reach internal data structure.

The recommended way of integrating new ML model with Reach is to run ML model
as an Agent that talks to the Reach host through the PyReach API.

The existing Oracle models will continue to be supported, specifically, the
pick point model and kitting model.

Any new Oracle model is strongly discouraged. Please discuss with the Reach
infrastructure team first before developing any new Oracle models.
"""

import dataclasses
from typing import Callable, Optional, Tuple

import numpy

from pyreach import core


@dataclasses.dataclass(frozen=True)
class PredictionPoint:
  """A predicted pixel coordinate in the camera frame.

  Attributes:
    x: Pixel x-coordinate.
    y: Pixel y-coordinate.

  """

  x: float
  y: float


@dataclasses.dataclass(frozen=True)
class PredictionPickPlacePoint:
  """A predicted pick and place point in the camera frame.

  Attributes:
    pick_position_3d: Position 3D for pick point.
    pick_rotation_quat_3d: Rotation 3D in quaternions for pick point.
    place_position_3d: Position 3D for place point.
    place_rotation_quat_3d: Rotation 3D in quaternions for place point.
  """

  pick_position_3d: core.Translation
  pick_rotation_quat_3d: core.Quaternion
  place_position_3d: core.Translation
  place_rotation_quat_3d: core.Quaternion


@dataclasses.dataclass(frozen=True)
class Prediction:
  """A set of pick points.

  Attributes:
    time: The time the prediction is made.
    sequence: The sequence number of the oracle frame.
    device_type: The device type of the oracle.
    device_name: The device name of the oracle.
    points: A list of pick points rated where the "best" pick points are listed
      first.
    pick_place_points: A list of pick and place points used for pick and place.
    image: The depth image used by the pick points as a (DX,DY)
    intent: The intent of the oracle.
    prediction_type: The prediction type for the oracle.
    request_type: The request type for the oracle.
    task_code: The task code for the oracle.
    label: The label for the oracle.

  """

  time: float
  sequence: int
  device_type: str
  device_name: str
  points: Tuple[PredictionPoint, ...]
  pick_place_points: Tuple[PredictionPickPlacePoint, ...]
  image: numpy.ndarray
  intent: str
  prediction_type: str
  request_type: str
  task_code: str
  label: str


class Oracle(object):
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

  def prediction(self) -> Optional[Prediction]:
    """Return the latest prediction if available."""
    raise NotImplementedError

  def add_update_callback(
      self,
      callback: Callable[[Prediction], bool],
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
                       timeout: float = 15.0) -> Prediction:
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
                             callback: Optional[Callable[[Prediction],
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
