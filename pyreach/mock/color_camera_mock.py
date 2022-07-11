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
"""Mock PyReach Color Camera."""

from typing import Callable, Optional

import numpy as np

from pyreach import color_camera
from pyreach import core
from pyreach.calibration import CalibrationCamera


class ColorCameraMock(color_camera.ColorCamera):
  """Mock ColorCamera class."""

  def __init__(self) -> None:
    """Init a MockColorCamera."""
    pass

  def add_update_callback(
      self,
      callback: Callable[[color_camera.ColorFrame], bool],
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
    pass

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

  def image(self) -> Optional[color_camera.ColorFrame]:
    """Return the latest image if it exists."""
    translation: core.Translation = core.Translation(1.0, 2.0, 3.0)
    orientation: core.Rotation = core.Rotation(core.AxisAngle())
    mock_pose: core.Pose = core.Pose(translation, orientation)
    color_frame_mock: color_camera.ColorFrame = color_camera.ColorFrame(
        1.0, 0, "device_type", "device_name", np.zeros((3, 5, 3),
                                                       dtype=np.uint8),
        CalibrationCamera(
            device_type="device_type",
            device_name="device_name",
            tool_mount=None,
            sub_type=None,
            distortion=(1.0, 2.0, 3.0, 4.0, 5.0),
            distortion_depth=(11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0),
            extrinsics=(21.0, 22.0, 23.0, 24.0, 25.0, 26.0),
            intrinsics=(31.0, 32.0, 33.0, 34.0),
            height=3,
            width=5,
            extrinsics_residual=None,
            intrinsics_residual=None,
            lens_model="fisheye",
            link_name=None), mock_pose)
    color_frame: color_camera.ColorFrame = color_frame_mock
    return color_frame

  def fetch_image(self,
                  timeout: float = 15.0) -> Optional[color_camera.ColorFrame]:
    """Fetch a new image or possibly times out.

    Args:
      timeout: The optional amount of time to wait for a camera frame. If not
        specified, 15 seconds is the default timeout.

    Returns:
      Returns the color image or None for a timeout.

    """
    return self.image()

  def async_fetch_image(self,
                        callback: Optional[Callable[[color_camera.ColorFrame],
                                                    None]] = None,
                        error_callback: Optional[Callable[[core.PyReachStatus],
                                                          None]] = None,
                        timeout: float = 30) -> None:
    """Fetch a new image asynchronously.

    The callback function will be invoked when new image is available.

    Args:
      callback: A callback function that is called when an image arrives. If the
        camera fails to load an image, the callback is not called.
      error_callback: Optional callback that is called if there is an error.
      timeout: Timeout for the fetch, defaults to 30 seconds.
    """
    raise NotImplementedError

  @property
  def pose(self) -> Optional[core.Pose]:
    """Return the latest pose of the camera."""
    raise NotImplementedError
