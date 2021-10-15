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

"""Interface for interacting with a depth camera device."""

from typing import Optional, Callable, Tuple

import numpy as np  # type: ignore

from pyreach import calibration as cal
from pyreach import core
from pyreach import depth_camera
from pyreach.mock import calibration_mock as cal_mock


class DepthFrameMock(depth_camera.DepthFrame):
  """A single depth camera frame taken at a specific time.

  Attributes:
    time: The time the depth camera image was taken in seconds.
    sequence: The sequence number of the color frame.
    device_type: The JSON device type associated with the camera.
    device_name: The JSON device name associated with the camera.
    depth_image:  A (DX,DY) array of uint16's containing the depth data.
    color_image: A (DX,DY,3) array of uint8's containing the color image.
    calibration: The calibration when the image is captured.
  """

  def __init__(self, time: float, sequence: int, device_type: str,
               device_name: str, depth_image: np.ndarray,
               color_image: np.ndarray,
               calibration: Optional[cal.Calibration]) -> None:
    """Initialize a MockColorFrame."""
    assert len(depth_image.shape) == 2
    assert depth_image.dtype == np.uint16
    assert len(color_image.shape) == 3
    assert color_image.dtype == np.uint8
    assert depth_image.shape == color_image.shape[:2]

    self._time: float = time
    self._sequence = sequence
    self._device_type: str = device_type
    self._device_name: str = device_name
    self._depth_image: np.ndarray = depth_image
    self._color_image: np.ndarray = color_image
    self._calibration: Optional[cal.Calibration] = calibration

  @property
  def time(self) -> float:
    """Return timestamp of the DepthFrame."""
    return self._time

  @property
  def sequence(self) -> int:
    """Sequence number of the DepthFrame."""
    return self._sequence

  @property
  def device_type(self) -> str:
    """Return the reach device type."""
    return self._device_type

  @property
  def device_name(self) -> str:
    """Return the Reach device name."""
    return self._device_name

  @property
  def color_data(self) -> np.ndarray:
    """Return the color image as a (DX,DY,3)."""
    return self._color_image

  @property
  def depth_data(self) -> np.ndarray:
    """Return the color image as a (DX,DY)."""
    return self._depth_image

  @property
  def calibration(self) -> Optional[cal.Calibration]:
    """Return the Calibration for for the ColorFrame."""
    return self._calibration

  def pose(self) -> Optional[core.Pose]:
    """Return the pose of the camera when the image is taken."""
    raise NotImplementedError

  def get_point_normal(
      self, x: int,
      y: int) -> Optional[Tuple[np.ndarray, np.ndarray, np.ndarray]]:
    """Return hit point, surface normal and transform of a pixel.

    Cast a ray from the camera center to the point cloud. Found the 3D position
    of the hit point. Around the hit point, cut a small region and measure the
    surface normal. The third return value is the transformation matrix from
    the unit z-vector to the hit point, surface normal pair.

    Args:
      x: x index of the pixel.
      y: y index of the pixel.

    Returns:
      tuple (position, surface normal, transform)

    """
    raise NotImplementedError


class DepthCameraMock(depth_camera.DepthCamera):
  """Interface for a depth camera."""

  def start_streaming(self, request_period: float = 1.0) -> None:
    """Start depth camera streaming.

    Args:
      request_period: The optional period between depth camera image quests. If
        not specified, it defaults to a period of 1.0 seconds.
    """
    pass

  def stop_streaming(self) -> None:
    """Stop depth camera streaming."""
    raise NotImplementedError

  def enable_tagged_request(self) -> None:
    """Enable tagged depth camera image requests."""
    raise NotImplementedError

  def disable_tagged_request(self) -> None:
    """Disable tagged requests."""
    raise NotImplementedError

  def image(self) -> Optional[depth_camera.DepthFrame]:
    """Get the latest depth camera frame if it is available."""
    depth_frame: depth_camera.DepthFrame = DepthFrameMock(
        1.0,
        0,
        "device_type",
        "device_name",
        np.zeros((3, 5), dtype=np.uint16),  # Depth image
        np.zeros((3, 5, 3), dtype=np.uint8),  # Color image
        cal_mock.CalibrationMock("device_type", "device_name",
                                 "depth_camera_link_name"))
    return depth_frame

  def fetch_image(self,
                  timeout: float = 15.0) -> Optional[depth_camera.DepthFrame]:
    """Fetch a new image or possibly times out.

    Args:
      timeout: The number number of seconds to wait before timing out. This
        defaults to 15 seconds if not specified.

    Returns:
      Returns the latest image.

    """
    return self.image()

  def async_fetch_image(self,
                        callback: Optional[Callable[[depth_camera.DepthFrame],
                                                    None]] = None,
                        error_callback: Optional[Callable[[core.PyReachStatus],
                                                          None]] = None,
                        timeout: float = 30) -> None:
    """Fetch a new image asynchronously.

    The callback function will be invoked when new image is available.

    Args:
      callback: callback called when an image arrives. If the camera fails to
        load an image, callback will not be called.
      error_callback: optional callback called if there is an error.
      timeout: timeout for the process, defaults to 30 seconds.
    """
    raise NotImplementedError

  def add_update_callback(
      self,
      callback: Callable[[depth_camera.DepthFrame], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback function to be invoked when a new frame is available.

    Args:
      callback: function to be invoked when a new frame is available. Returns
        False to continue receiving new images. Returns True to stop further
        update.
      finished_callback: Optional callback, called when the callback is stopped
        or if the camera is closed.

    Returns:
      A function that when called stops the callback.

    """
    raise NotImplementedError

  @property
  def pose(self) -> Optional[core.Pose]:
    """Return the latest pose of the camera."""
    raise NotImplementedError
