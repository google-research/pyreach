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

from typing import Callable, Optional

import numpy as np

from pyreach import core
from pyreach import depth_camera
from pyreach.calibration import CalibrationCamera


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
    translation: core.Translation = core.Translation(1.0, 2.0, 3.0)
    orientation: core.Rotation = core.Rotation(core.AxisAngle())
    mock_pose: core.Pose = core.Pose(translation, orientation)
    depth_frame: depth_camera.DepthFrame = depth_camera.DepthFrame(
        1.0,
        0,
        "device_type",
        "device_name",
        np.zeros((3, 5, 3), dtype=np.uint8),  # Color image
        np.zeros((3, 5), dtype=np.uint16),  # Depth image
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
            link_name=None),
        mock_pose)
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
