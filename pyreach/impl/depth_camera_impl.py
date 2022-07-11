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
"""Implementation for the PyReach DepthCamera interface."""

import dataclasses
import logging  # type: ignore
from typing import Callable, Optional, Tuple

import numpy as np

from pyreach import core
from pyreach import depth_camera
from pyreach.calibration import CalibrationCamera
from pyreach.common.base import transform_util
from pyreach.common.python import types_gen
from pyreach.impl import requester
from pyreach.impl import thread_util
from pyreach.impl import utils


@dataclasses.dataclass(frozen=True)
class DepthFrameImpl(depth_camera.DepthFrame):
  """Implementation of a DepthFrame."""

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
    if self.calibration is None:
      return None

    intrinsics = transform_util.intrinsics_to_matrix(
        list(self.calibration.intrinsics))
    distortion = np.array(self.calibration.distortion, np.float64)
    distortion_depth = np.array(self.calibration.distortion_depth, np.float64)
    camera_transform = self.pose()
    if not camera_transform:
      return None
    pose = transform_util.inverse_pose(
        np.array(camera_transform.as_list(), dtype=float))
    inv_pose = transform_util.inverse_pose(pose)

    ray = transform_util.unproject(
        np.array([x, y], dtype=np.float64), 1, intrinsics, distortion)
    ray = transform_util.transform_by_pose(ray, inv_pose).reshape(
        (1, 3)) - inv_pose[:3]
    ray /= np.linalg.norm(ray)

    origin = inv_pose[:3]
    direction = ray[0]

    res = transform_util.raycast_into_depth_image(
        origin,
        direction,
        self.depth_data,
        intrinsics,
        distortion,
        distortion_depth,
        np.array(camera_transform.as_list()),
        radius=5,
        max_ray_dist=4,
        init_ray_step_size=0.05,
    )
    if res is None:
      return None

    pick_pt, pick_normal = res
    if pick_pt is None or pick_normal is None:
      return None

    pick_transform = transform_util.transform_between_two_vectors(
        np.array([0.0, 0.0, 0.0]),
        np.array([0.0, 0.0, 1.0]),
        pick_pt,
        pick_normal,
    )
    return (pick_pt, pick_normal, pick_transform)


class DepthCameraDevice(requester.Requester[depth_camera.DepthFrame]):
  """Device for a depth camera."""

  _device_type: str
  _device_name: str

  def __init__(self, device_type: str, device_name: str = "") -> None:
    """Initialize a depth camera.

    Args:
      device_type: The JSON device type for the camera.
      device_name: The JSON device name for the camera.
    """
    super().__init__()
    self._device_type = device_type
    self._device_name = device_name

  def get_message_supplement(
      self, msg: types_gen.DeviceData) -> Optional[depth_camera.DepthFrame]:
    """Get the depth camera image if it is available."""
    if (msg.data_type == "color-depth" and
        msg.device_type == self._device_type and
        msg.device_name == self._device_name):

      return self._depth_frame_from_message(msg)
    return None

  def get_wrapper(
      self) -> Tuple["DepthCameraDevice", "depth_camera.DepthCamera"]:
    """Get the wrapper for the device that should be shown to the user."""
    return self, DepthCameraImpl(self)

  @classmethod
  def _depth_frame_from_message(
      cls, msg: types_gen.DeviceData) -> "Optional[depth_camera.DepthFrame]":
    """Convert a JSON message into a camera frame."""
    try:
      color: np.ndarray = utils.load_color_image_from_data(msg)
    except FileNotFoundError:
      ts = msg.local_ts if msg.local_ts > 0 else msg.ts
      delta = utils.timestamp_now() - ts
      logging.warning(
          "depth color message missing file a %d ms time delta, file %s", delta,
          msg.color)
      return None
    try:
      depth: np.ndarray = utils.load_depth_image_from_data(msg)
    except FileNotFoundError:
      ts = msg.local_ts if msg.local_ts > 0 else msg.ts
      delta = utils.timestamp_now() - ts
      logging.warning("depth message missing file at %d ms time delta, file %s",
                      delta, msg.depth)
      return None
    pose: Optional[core.Pose] = None
    calibration: Optional[CalibrationCamera] = None
    if msg.camera_calibration:
      calibration = CalibrationCamera(
          device_type=msg.device_type,
          device_name=msg.device_name,
          tool_mount=None,
          sub_type=None,
          distortion=tuple(msg.camera_calibration.distortion),
          distortion_depth=tuple(msg.camera_calibration.distortion_depth),
          extrinsics=tuple(msg.camera_calibration.extrinsics),
          intrinsics=tuple(msg.camera_calibration.intrinsics),
          height=msg.camera_calibration.calibrated_height,
          width=msg.camera_calibration.calibrated_width,
          extrinsics_residual=msg.camera_calibration.extrinsics_residual,
          intrinsics_residual=msg.camera_calibration.intrinsics_residual,
          lens_model=msg.camera_calibration.lens_model,
          link_name=None)
      if msg.camera_calibration.camera_t_origin:
        pose = core.Pose.from_list(msg.camera_calibration.camera_t_origin)
    return DepthFrameImpl(  # pylint: disable=unexpected-keyword-arg
        time=utils.time_at_timestamp(msg.ts),
        sequence=msg.seq,
        device_type=msg.device_type,
        device_name=msg.device_name,
        color_data=color,
        depth_data=depth,
        calibration=calibration,
        camera_t_origin=pose)

  def device_type(self) -> str:
    """Return the type of device."""
    return self._device_type

  def device_name(self) -> str:
    """Return the name of device."""
    return self._device_name


class DepthCameraImpl(depth_camera.DepthCamera):
  """Represents a depth camera."""

  _device: DepthCameraDevice

  def __init__(self, device: DepthCameraDevice) -> None:
    """Initialize a DepthCamera around a device.

    Args:
      device: DepthCamera device.
    """
    self._device = device

  def start_streaming(self, request_period: float = 1.0) -> None:
    """Start depth camera streaming.

    Args:
      request_period: The optional period between depth camera image quests.  If
        not specified, it defaults to a period of 1.0 seconds.
    """
    self._device.set_untagged_request_period(self._device.device_type(),
                                             self._device.device_name(),
                                             "color-depth", request_period)

  def stop_streaming(self) -> None:
    """Stop depth camera streaming."""
    self._device.set_untagged_request_period(self._device.device_type(),
                                             self._device.device_name(),
                                             "color-depth", None)

  def enable_tagged_request(self) -> None:
    """Enable tagged depth camare image requests."""
    self._device.set_enable_tagged_request(self._device.device_type(),
                                           self._device.device_name(), True)

  def disable_tagged_request(self) -> None:
    """Disable tagged requests."""
    self._device.set_enable_tagged_request(self._device.device_type(),
                                           self._device.device_name(), False)

  def image(self) -> Optional[depth_camera.DepthFrame]:
    """Get the cached depth camera image if it is available."""
    return self._device.get_cached()

  def fetch_image(self,
                  timeout: float = 15.0) -> Optional[depth_camera.DepthFrame]:
    """Get the next depth camera image if it is available.

    Args:
      timeout: The number number of seconds to wait before timing out. This
        defaults to 15 seconds if not specified.

    Returns:
      Return newly acquired image.
    """
    q = self._device.request_tagged(
        self._device.device_type(),
        self._device.device_name(),
        timeout=timeout,
        expect_messages=1)
    msgs = thread_util.extract_all_from_queue(q)
    if not msgs:
      return None
    if (len(msgs) == 1 and msgs[0][0].data_type == "cmd-status" and
        (msgs[0][0].status in {"rejected", "aborted"} or msgs[0][0].error)):
      return None
    if len(msgs) != 2:
      logging.warning("expected a single message and status: %s", msgs)
    return msgs[0][1]

  def async_fetch_image(self,
                        callback: Optional[Callable[[depth_camera.DepthFrame],
                                                    None]] = None,
                        error_callback: Optional[Callable[[core.PyReachStatus],
                                                          None]] = None,
                        timeout: float = 30) -> None:
    """Get an image via a callback.

    Args:
      callback: callback called when an image arrives. If the camera fails to
        load an image, callback will not be called.
      error_callback: optional callback called if there is an error.
      timeout: Time to wait until giving up.
    """
    q = self._device.request_tagged(
        self._device.device_type(),
        self._device.device_name(),
        timeout=timeout,
        expect_messages=1)

    self._device.queue_to_error_callback(q, callback, error_callback)

  def add_update_callback(
      self,
      callback: Callable[[depth_camera.DepthFrame], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback for cached frames.

    Args:
      callback: Callback called when a frame arrives. If it returns True, the
        callback will be stopped.
      finished_callback: Optional callback, called when the callback is stopped
        or if the camera is closed.

    Returns:
      A function that when called stops the callback.

    """
    return self._device.add_update_callback(callback, finished_callback)

  @property
  def pose(self) -> Optional[core.Pose]:
    """Return the latest pose of the camera."""
    current_image = self.image()
    if current_image:
      return current_image.pose()
    return None
