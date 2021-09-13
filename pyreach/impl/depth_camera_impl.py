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
import logging  # type: ignore
from typing import Callable, Optional, Tuple, cast

import numpy as np  # type: ignore

from pyreach import calibration as cal
from pyreach import core
from pyreach import depth_camera
from pyreach.common.base import transform_util
from pyreach.common.python import types_gen
from pyreach.impl import calibration_impl
from pyreach.impl import requester
from pyreach.impl import thread_util
from pyreach.impl import utils


class DepthFrameImpl(depth_camera.DepthFrame):
  """Implementation of a DepthFrame."""

  def __init__(self, time: float, sequence: int,
               device_type: str, device_name: str,
               color_data: np.ndarray, depth_data: np.ndarray,
               calibration: Optional[cal.Calibration]) -> None:
    """Construct a DepthFrameImpl."""
    self._time: float = time
    self._sequence: int = sequence
    self._device_type: str = device_type
    self._device_name: str = device_name
    self._color_data: np.ndarray = color_data
    self._depth_data: np.ndarray = depth_data
    self._calibration: Optional[cal.Calibration] = calibration

  @property
  def time(self) -> float:
    """Return timestamp of the ColorFrame."""
    return self._time

  @property
  def sequence(self) -> int:
    """Sequence number of the ColorFrame."""
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
    return self._color_data

  @property
  def depth_data(self) -> np.ndarray:
    """Return the color image as a (DX,DY)."""
    return self._depth_data

  @property
  def calibration(self) -> Optional[cal.Calibration]:
    """Return the Calibration for for the ColorFrame."""
    return self._calibration

  def pose(self) -> Optional[core.Pose]:
    """Return the pose of the camera when the image is taken."""
    if self.calibration is None:
      return None
    c = self.calibration
    device = c.get_device(self.device_type, self.device_name)
    if device is None:
      return None
    if not isinstance(device, cal.CalibrationCamera):
      return None
    device = cast(cal.CalibrationCamera, device)

    if len(device.extrinsics) != 6:
      logging.warning("Camera extrinisics not a 6-element list.")
      return None
    parent_id = device.tool_mount
    if parent_id is None:
      return core.Pose.from_list(list(device.extrinsics))

    logging.warning("Camera had a parent ID. Currently unsupported.")
    return None

  def get_point_normal(self, x: int,
                       y: int) -> Optional[Tuple[np.array, np.array, np.array]]:
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

    c = self.calibration
    camera_device = c.get_device(self.device_type, self.device_name)

    if camera_device is None:
      return None
    if not isinstance(camera_device, cal.CalibrationCamera):
      return None

    intrinsics = transform_util.intrinsics_to_matrix(camera_device.intrinsics)
    distortion = np.array(camera_device.distortion, np.float64)
    distortion_depth = np.array(camera_device.distortion_depth, np.float64)
    camera_transform = self.pose()
    if not camera_transform:
      return None
    pose = transform_util.inverse_pose(camera_transform.as_list())
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
  _calibration: Optional[calibration_impl.CalDevice]

  def __init__(
      self,
      device_type: str,
      device_name: str = "",
      calibration: Optional[calibration_impl.CalDevice] = None) -> None:
    """Initialize a depth camera.

    Args:
      device_type: The JSON device type for the camera.
      device_name: The JSON device name for the camera.
      calibration: Calibration of the camera.
    """
    super().__init__()
    self._device_type = device_type
    self._device_name = device_name
    self._calibration = calibration

  def get_message_supplement(
      self, msg: types_gen.DeviceData) -> Optional[depth_camera.DepthFrame]:
    """Get the depth camera image if it is available."""
    if (msg.data_type == "color-depth" and
        msg.device_type == self._device_type and
        msg.device_name == self._device_name):

      return self._depth_frame_from_message(msg, self.get_calibration())
    return None

  def get_wrapper(
      self) -> Tuple["DepthCameraDevice", "depth_camera.DepthCamera"]:
    """Get the wrapper for the device that should be shown to the user."""
    return self, DepthCameraImpl(self)

  def get_calibration(self) -> Optional[cal.Calibration]:
    """Get the Calibration if it is available."""
    if self._calibration is None:
      return None
    return self._calibration.get()

  @classmethod
  def _depth_frame_from_message(
      cls, msg: types_gen.DeviceData, calibration: Optional[cal.Calibration]
  ) -> "Optional[depth_camera.DepthFrame]":
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
    return DepthFrameImpl(
        utils.time_at_timestamp(msg.ts), msg.seq,
        msg.device_type, msg.device_name,
        color, depth, calibration)

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
    c = self._device.get_calibration()
    if c is None:
      return None
    device = c.get_device(self._device.device_type(),
                          self._device.device_name())
    if device is None:
      return None
    if not isinstance(device, cal.CalibrationCamera):
      return None
    if len(device.extrinsics) != 6:
      logging.warning("Camera extrinisics not a 6-element list.")
      return None
    parent_id = device.tool_mount
    if parent_id is None:
      return core.Pose.from_list(list(device.extrinsics))
    logging.warning("Camera had a parent ID. Currently unsupported.")
    return None
