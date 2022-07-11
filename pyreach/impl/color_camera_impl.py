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
"""Implementation of the PyReach ColorCamera interface."""
import logging
from typing import Callable, Optional, Tuple

import numpy as np

from pyreach import color_camera
from pyreach import core
from pyreach.calibration import CalibrationCamera
from pyreach.common.python import types_gen
from pyreach.impl import calibration_impl
from pyreach.impl import requester
from pyreach.impl import thread_util
from pyreach.impl import utils


class ColorCameraDevice(requester.Requester[color_camera.ColorFrame]):
  """Represents a Camera Device."""

  _device_type: str
  _device_name: str
  _display_device_type: str
  _display_device_name: str
  _calibration: Optional[calibration_impl.CalDevice]

  def __init__(self,
               device_type: str,
               device_name: str = "",
               display_device_type: Optional[str] = None,
               display_device_name: Optional[str] = None) -> None:
    """Initialize a Camera.

    Args:
      device_type: The JSON device type to use.
      device_name: The JSON device name to use.
      display_device_type: Override the device type to display to the user.
      display_device_name: Override the device name to display to the user.
    """
    super().__init__()
    self._device_type = device_type
    self._device_name = device_name
    self._display_device_type = device_type
    if display_device_type is not None:
      self._display_device_type = display_device_type
    self._display_device_name = device_name
    if display_device_name is not None:
      self._display_device_name = display_device_name

  def get_message_supplement(
      self, msg: types_gen.DeviceData) -> Optional[color_camera.ColorFrame]:
    """Get getting supplementary information for the request manager.

    Args:
      msg: device data message.

    Returns:
      Converted ColorFrame object.
    """
    if (self._device_type == msg.device_type and
        self._device_name == msg.device_name and msg.data_type == "color"):
      return self._color_frame_from_message(msg)
    return None

  def get_wrapper(
      self) -> Tuple["ColorCameraDevice", "color_camera.ColorCamera"]:
    """Get the wrapper for the device that should be shown to the user."""
    return self, ColorCameraImpl(self)

  @property
  def device_name(self) -> str:
    """Return device name."""
    return self._device_name

  @property
  def device_type(self) -> str:
    """Return device type."""
    return self._device_type

  def _color_frame_from_message(
      self, msg: types_gen.DeviceData) -> Optional[color_camera.ColorFrame]:
    """Convert JSON message into a ColorFrame."""
    pose: Optional[core.Pose] = None
    calibration: Optional[CalibrationCamera] = None
    if msg.camera_calibration:
      calibration = CalibrationCamera(
          device_type=msg.device_type,
          device_name=msg.device_name,
          tool_mount=None,
          sub_type=None,
          distortion=tuple(msg.camera_calibration.distortion),
          distortion_depth=None,
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
    try:
      color_image: np.ndarray = utils.load_color_image_from_data(msg)
      return color_camera.ColorFrame(
          utils.time_at_timestamp(msg.ts), msg.seq, self._display_device_type,
          self._display_device_name, color_image, calibration, pose)
    except FileNotFoundError:
      ts = msg.local_ts if msg.local_ts > 0 else msg.ts
      delta = utils.timestamp_now() - ts
      logging.warning("color message missing file at %d ms time delta, file %s",
                      delta, msg.color)
      return None


class ColorCameraImpl(color_camera.ColorCamera):
  """Represents a color Camera."""

  _device: ColorCameraDevice

  def __init__(self, device: ColorCameraDevice) -> None:
    """Initialize a Camera around a device.

    Args:
      device: Camera device.
    """
    self._device = device

  def add_update_callback(
      self,
      callback: Callable[[color_camera.ColorFrame], bool],
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

  def start_streaming(self, request_period: float = 0.1) -> None:
    """Start streaming of camera images.

    Args:
      request_period: The number of seconds between frames. Defaults to .1
        second between frames.
    """
    self._device.set_untagged_request_period(self._device.device_type,
                                             self._device.device_name, "color",
                                             request_period)

  def stop_streaming(self) -> None:
    """Stop streaming camera images."""
    self._device.set_untagged_request_period(self._device.device_type,
                                             self._device.device_name, "color",
                                             None)

  def supports_tagged_request(self) -> bool:
    """Return True if tagged requests are supported."""
    return (self._device.device_type, self._device.device_name) not in {("uvc",
                                                                         "")}

  def enable_tagged_request(self) -> None:
    """Enable tagged requests."""
    if not self.supports_tagged_request():
      raise Exception("Tagged requests not supported")
    self._device.set_enable_tagged_request(self._device.device_type,
                                           self._device.device_name, True)

  def disable_tagged_request(self) -> None:
    """Disable tagged requests."""
    self._device.set_enable_tagged_request(self._device.device_type,
                                           self._device.device_name, False)

  def image(self) -> Optional[color_camera.ColorFrame]:
    """Return cached image if it exists."""
    return self._device.get_cached()

  def fetch_image(self,
                  timeout: float = 15.0) -> Optional[color_camera.ColorFrame]:
    """Return an image or possibly times out.

    Args:
      timeout: The optional amount of time to wait for a camera frame. If not
        specified, 15 seconds is the default timeout.

    Returns:
      Newly fetched image.
    """
    if not self.supports_tagged_request():
      q = self._device.request_untagged(
          self._device.device_type,
          self._device.device_name,
          data_type="color",
          timeout=timeout)
      msgs = thread_util.extract_all_from_queue(q)
      if not msgs:
        return None
      if len(msgs) != 1:
        logging.warning("expected a single message: %s", msgs)
      return msgs[0][1]
    q = self._device.request_tagged(
        self._device.device_type,
        self._device.device_name,
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
                        callback: Optional[Callable[[color_camera.ColorFrame],
                                                    None]] = None,
                        error_callback: Optional[Callable[[core.PyReachStatus],
                                                          None]] = None,
                        timeout: float = 30) -> None:
    """Get an image via callback.

    Args:
      callback: callback called when an image arrives. If the camera fails to
        load an image, callback will not be called.
      error_callback: optional callback called if there is an error.
      timeout: timeout for the process, defaults to 30 seconds.
    """
    if not self.supports_tagged_request():
      q = self._device.request_untagged(
          self._device.device_type,
          self._device.device_name,
          data_type="color",
          timeout=timeout)
    else:
      q = self._device.request_tagged(
          self._device.device_type,
          self._device.device_name,
          timeout=timeout,
          expect_messages=1)

    self._device.queue_to_error_callback(q, callback, error_callback)

  @property
  def pose(self) -> Optional[core.Pose]:
    """Return the latest pose of the camera."""
    current_image = self.image()
    if current_image:
      return current_image.pose()
    return None
