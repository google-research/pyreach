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

"""Interface for interacting with a color camera device."""

import dataclasses
from typing import Callable, Optional

import numpy as np

from pyreach import core
from pyreach.calibration import CalibrationCamera


@dataclasses.dataclass(frozen=True)
class ColorFrame:
  """A single color camera frame taken at a specific time.

  Attributes:
    time: The time in seconds of the frame since 1970.
    sequence: The sequence number of the color frame.
    device_type: The JSON device type string.
    device_name: The JSON device name string.
    color_image: A color image as a (DX,DY,3) array of uint8's.
    calibration: The calibration when the image is captured.
    camera_t_origin: The camera pose with respect to the origin.
  """

  time: float
  sequence: int
  device_type: str
  device_name: str
  color_image: np.ndarray
  calibration: Optional[CalibrationCamera]
  camera_t_origin: Optional[core.Pose]

  def pose(self) -> Optional[core.Pose]:
    """Return the pose of the camera when the image is taken."""
    return self.camera_t_origin


class ColorCamera(object):
  """Interface for a color camera."""

  def add_update_callback(
      self,
      callback: Callable[[ColorFrame], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback function to be invoked when a new frame is available.

    Args:
      callback: A function to be invoked when a new frame is available. Returns
        False to continue receiving new images. Returns True to stop further
        update.
      finished_callback: Optional callback, called when the callback is stopped
        or if the camera is closed.

    Returns:
      A function that when called stops the callbacks.

    """
    raise NotImplementedError

  def start_streaming(self, request_period: float = 0.1) -> None:
    """Start streaming of camera images.

    Args:
      request_period: The number of seconds between frames. Defaults to .1
        second between frames.
    """
    raise NotImplementedError

  def stop_streaming(self) -> None:
    """Stop streaming camera images."""
    raise NotImplementedError

  def supports_tagged_request(self) -> bool:
    """Return True if tagged requests are supported."""
    raise NotImplementedError

  def enable_tagged_request(self) -> None:
    """Enable tagged requests."""
    raise NotImplementedError

  def disable_tagged_request(self) -> None:
    """Disable tagged requests."""
    raise NotImplementedError

  def image(self) -> Optional[ColorFrame]:
    """Return the latest image if it exists."""
    raise NotImplementedError

  def fetch_image(self, timeout: float = 15.0) -> Optional[ColorFrame]:
    """Fetch a new image or possibly times out.

    Args:
      timeout: The optional amount of time to wait for a camera frame. If not
        specified, 15 seconds is the default timeout.

    Returns:
      Returns the color image or None for a timeout.

    """
    raise NotImplementedError

  def async_fetch_image(self,
                        callback: Optional[Callable[[ColorFrame], None]] = None,
                        error_callback: Optional[Callable[[core.PyReachStatus],
                                                          None]] = None,
                        timeout: float = 30) -> None:
    """Fetch a new image asynchronously.

    The callback function will be invoked when new image is available.

    Args:
      callback: A callback function that is called when an image arrives.
        If the camera fails to load an image, the callback is not called.
      error_callback: Optional callback that is called if there is an error.
      timeout: Timeout for the fetch, defaults to 30 seconds.
    """
    raise NotImplementedError

  @property
  def pose(self) -> Optional[core.Pose]:
    """Return the latest pose of the camera."""
    raise NotImplementedError
