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

"""Lightweight client to reach for point clouds and camera development."""

from typing import Optional, Tuple, cast

from pyreach import DepthFrame
from pyreach.calibration import CalibrationCamera
from pyreach.factory import LocalTCPHostFactory
from pyreach.tools.lib import view_rgbd
import cv2  # type: ignore


class View3dOverReach:
  """Streams a 3d view over Reach."""

  def __init__(self) -> None:
    """Initialize the 3D viewer."""
    self._viewer = view_rgbd.RgbdViewer()
    self._host = LocalTCPHostFactory(
        take_control_at_start=False,
        enable_streaming=False).connect()
    camera = self._host.depth_camera
    if camera is None:
      self._host.close()
      raise RuntimeError("Robot does not support depth-camera")
    camera.add_update_callback(self._on_image)
    camera.start_streaming()

  def _camera_params(self) -> Tuple[
      Optional[Tuple[float, float, float, float]],
      Optional[Tuple[float, ...]]]:
    """Get the current camera parameters.

    Returns:
      The intrinsics and distortion.
    """
    calibration = self._host.config.calibration
    if calibration is None:
      return None, None
    device = calibration.get_device("depth-camera", "")
    if device is None:
      return None, None
    if not isinstance(device, CalibrationCamera):
      return None, None
    intrinsics = device.intrinsics
    if len(intrinsics) != 4:
      return None, None
    return cast(Tuple[float, float, float, float],
                device.intrinsics), device.distortion

  def _on_image(self, frame: DepthFrame) -> bool:
    """On image received.

    Args:
      frame: the depth frame.

    Returns:
      False to continue operation of the callback.
    """
    intrinsics, distortion = self._camera_params()
    if intrinsics is None or distortion is None:
      return False
    self._viewer.set_calibration(intrinsics, list(distortion))
    color = cv2.cvtColor(frame.color_data, cv2.COLOR_RGB2BGR)
    self._viewer.update_image_frames(frame.depth_data, color)
    return False

  def run_until_closed(self) -> None:
    """Start listening until the windows is closed."""
    try:
      self._viewer.wait_until_closed()
    except KeyboardInterrupt:
      self._host.close()
      raise
    self._host.close()

