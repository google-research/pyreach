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

"""Implementation of the PyReach VNC interface."""

import queue  # pylint: disable=unused-import
import time
from typing import Optional, Tuple, Callable
from pyreach import color_camera
from pyreach import core
from pyreach import vnc
from pyreach.common.python import types_gen
from pyreach.impl import color_camera_impl
from pyreach.impl import thread_util
from pyreach.impl import utils


class VNCDevice(color_camera_impl.ColorCameraDevice):
  """Represents a VNC Device."""

  _device_type: str
  _device_name: str

  def __init__(self, device_type: str, device_name: str = "") -> None:
    """Initialize a VNC device.

    Args:
      device_type: The JSON device type to use.
      device_name: The JSON device name to use.
    """
    super().__init__(device_type, device_name, None)
    self._device_type = device_type
    self._device_name = device_name

  def get_wrapper(self) -> Tuple["VNCDevice", "vnc.VNC"]:
    """Get the wrapper for the device that should be shown to the user."""
    return self, VNCImpl(self)

  @property
  def device_name(self) -> str:
    """Return device name."""
    return self._device_name

  @property
  def device_type(self) -> str:
    """Return device type."""
    return self._device_type

  def send_pointer_event(
      self, x: float, y: float, event_type: vnc.PointerEventType, timeout: float
  ) -> ("Tuple[Optional[queue.Queue[Optional[Tuple[types_gen.DeviceData, "
        "Optional[color_camera.ColorFrame]]]]], Optional[core.PyReachStatus]]"):
    """Send a pointer event to the VNC device.

    Args:
      x: the x position of the mouse pointer.
      y: the y position of the mouse pointer.
      event_type: the type of pointer event.
      timeout: the timeout.

    Returns:
      The status message associated with the event.
    """
    if x < 0.0 or x > 1.0:
      return None, core.PyReachStatus(
          time=time.time(),
          status="rejected",
          error="bad-input",
          message="x must be between 0 and 1")
    if y < 0.0 or y > 1.0:
      return None, core.PyReachStatus(
          time=time.time(),
          status="rejected",
          error="bad-input",
          message="y must be between 0 and 1")
    return self.send_tagged_request(
        types_gen.CommandData(
            ts=utils.timestamp_now(),
            tag=utils.generate_tag(),
            device_type=self.device_type,
            device_name=self.device_name,
            data_type="pointer-event",
            cmd=event_type.value,
            x=x,
            y=y),
        timeout=timeout), None


class VNCImpl(vnc.VNC, color_camera_impl.ColorCameraImpl):
  """Represents a color Camera."""

  _device: VNCDevice

  def __init__(self, device: VNCDevice) -> None:
    """Initialize a VNC around a device.

    Args:
      device: VNC device.
    """
    color_camera_impl.ColorCameraImpl.__init__(self, device)
    self._device = device

  def send_pointer_event(
      self, x: float, y: float,
      event_type: vnc.PointerEventType,
      timeout: float = 30) -> core.PyReachStatus:
    """Send a pointer event to the VNC device.

    Args:
      x: the x position of the mouse pointer.
      y: the y position of the mouse pointer.
      event_type: the type of pointer event.
      timeout: the timeout.

    Returns:
      The status message associated with the event.
    """
    q, status = self._device.send_pointer_event(x, y, event_type, timeout)
    if status:
      return status
    assert q
    for msg in thread_util.extract_all_from_queue(q):
      if msg[0].data_type == "cmd-status":
        status = utils.pyreach_status_from_message(msg[0])
        if status.is_last_status():
          return status
    return core.PyReachStatus(time=time.time(), status="done", error="timeout")

  def async_send_pointer_event(
      self,
      x: float,
      y: float,
      event_type: vnc.PointerEventType,
      callback: Optional[Callable[[core.PyReachStatus], None]] = None,
      timeout: float = 30) -> None:
    """Send a pointer event to the VNC device.

    Args:
      x: the x position of the mouse pointer.
      y: the y position of the mouse pointer.
      event_type: the type of pointer event.
      callback: optional callback for status from the command.
      timeout: the timeout.
    """
    q, status = self._device.send_pointer_event(x, y, event_type, timeout)
    if not callback:
      return
    if status:
      self._device.run(callback, status)
      return
    assert q

    def transform(
        msg: types_gen.DeviceData,
        unused_supplement: Optional[color_camera.ColorFrame]
    ) -> Optional[core.PyReachStatus]:
      if msg.data_type != "cmd-status":
        return None
      status = utils.pyreach_status_from_message(msg)
      if status.is_last_status():
        return status
      return None

    self._device.queue_to_error_callback_transform(q, callback, callback,
                                                   transform)

  @property
  def pose(self) -> Optional[core.Pose]:
    """Pose is not meaningful for VNC."""
    raise NotImplementedError
