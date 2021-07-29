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

"""Controller for the async viewer."""

import threading
from typing import Dict, List, Optional, Set, Tuple

import numpy as np  # type: ignore

from pyreach import ColorFrame
from pyreach import DepthFrame
from pyreach import Host
from pyreach import PointerEventType
from pyreach import Prediction
from pyreach.calibration import CalibrationCamera
from pyreach.common.python import types_gen
from pyreach.factory import LocalTCPHostFactory
from pyreach.tools.lib import cv2_eventloop
from pyreach.tools.lib import image_display
from pyreach.utils import load_image

# Directory to store snapshots in.
_SNAPSHOT_DIR = "snapshots"

# Separator for camera device type and device name, e.g. uvc.cam1.
# Using '.', since '-' is already used in 'pick-points'.
_TYPE_NAME_SEP = "."


def parse_cameras(cameras_arg: str) -> List[Tuple[str, Optional[str]]]:
  """Parses cameras from command line.

  Args:
    cameras_arg: A comma delimited string of cameras. For example,
      'depth-camera+oracle.pick-points,color-camera'.

  Returns:
    A list of tuple of the form -
    [('depth-camera', 'oracle.pick-points'), ('color-camera', )]
    Each entry in the tuple has a source, and a possible overlay.
  """
  result: List[Tuple[str, Optional[str]]] = []
  if not cameras_arg:
    # Empty string - return before splitting with ','.
    return []
  for camera in cameras_arg.split(","):
    modes = camera.split("+")
    actual = modes[0]
    overlay = modes[1] if len(modes) > 1 else None
    result.append((actual, overlay))
  return result


class Controller:
  """Controller for the async viewer."""
  _host: Host
  _overlay_target: Dict[str, str]
  _color_camera_windows: Optional[Dict[str, List[Tuple[str, bool]]]]
  _depth_camera_windows: Optional[Dict[str, List[Tuple[str, bool]]]]
  _oracle_windows: Optional[Dict[str, List[Tuple[str, bool]]]]
  _vnc_windows: Optional[Dict[str, List[Tuple[str, bool]]]]
  _unrequested_oracles: Set[str]
  _show_undistortion: bool
  _show_detections: bool
  _quiet: bool

  def __init__(self, camera_names: List[Tuple[str,
                                              Optional[str]]], reqfps: float,
               uwidth: int, show_undistortion: bool, use_tags: bool,
               show_detections: bool, quiet: bool):
    """Instantiate a controller for multiple cameras.

    Args:
      camera_names: A list of tuples of (device type, device name) for the
        cameras to view. If empty, all cameras will be viewed.
      reqfps: the request rate for cameras.
      uwidth: the window width in pixels. If zero, will autoscale.
      show_undistortion: if true, calibration undistortion will be displayed.
      use_tags: if true, will use tagged requests.
      show_detections: if true, will show object detections.
      quiet: if true, will not print help text.
    """
    # If true, will render the undistortion field as red / green arrows.
    self._show_undistortion = show_undistortion
    self._show_detections = show_detections
    self._quiet = quiet

    self._host = LocalTCPHostFactory(
        take_control_at_start=False, enable_streaming=False).connect()

    self._overlay_target = {}

    self._cv2e = cv2_eventloop.get_instance()

    # Image displayer using OpenCV windows.
    self._image_display = image_display.ImageDisplay(uwidth=uwidth)
    self._image_display.add_click_listener(self._on_mouse)

    # These "windows" variables hold the names of the windows for each camera to
    # be written to. The attached boolean represents if it should be an overlay
    # or not. If the dictionary is None, then the camera will be written only to
    # the window derived from its device type and device name.
    self._color_camera_windows = None
    self._depth_camera_windows = None
    self._oracle_windows = None
    self._vnc_windows = None

    # If an oracle is in this list, it is not requested, and must be processed
    # manually by the viewer.
    self._unrequested_oracles = set()

    if camera_names:
      self._color_camera_windows = {}
      self._depth_camera_windows = {}
      self._oracle_windows = {}
      self._vnc_windows = {}
      cameras_by_type: Dict[str, Dict[str, List[Tuple[str, bool]]]] = {
          "uvc": self._color_camera_windows,
          "color-camera": self._color_camera_windows,
          "photoneo": self._depth_camera_windows,
          "depth-camera": self._depth_camera_windows,
          "oracle": self._oracle_windows,
          "vnc": self._vnc_windows,
      }
      for cam_id, overlay_id in camera_names:
        type_name = cam_id.split(_TYPE_NAME_SEP)
        camera_name = type_name[1] if len(type_name) > 1 else ""
        if type_name[0] in cameras_by_type:
          cameras = cameras_by_type[type_name[0]]
          if camera_name not in cameras:
            cameras[camera_name] = []
          window_name = self._device_to_key(type_name[0], camera_name)
          cameras[camera_name].append((window_name, False))
          if overlay_id:
            overlay_type_name = overlay_id.split(_TYPE_NAME_SEP)
            overlay_camera_name = ""
            if len(overlay_type_name) > 1:
              overlay_camera_name = overlay_type_name[1]
            if overlay_type_name[0] in cameras_by_type:
              overlay_cameras = cameras_by_type[overlay_type_name[0]]
              if overlay_camera_name not in overlay_cameras:
                overlay_cameras[overlay_camera_name] = []
              overlay_cameras[overlay_camera_name].append((window_name, True))
            else:
              print("Invalid camera overlay:", overlay_id)
        else:
          print("Invalid camera:", cam_id)

    for name, color_camera in self._host.color_cameras.items():
      if not self._quiet:
        print("Discovered --cameras=color-camera" +
              (("." + name) if name else ""))
      if (self._color_camera_windows is not None and
          name not in self._color_camera_windows):
        continue
      color_camera.add_update_callback(self._color_camera_callback)
      if use_tags and color_camera.supports_tagged_request:
        color_camera.enable_tagged_request()
      elif reqfps > 0:
        color_camera.start_streaming(1.0 / reqfps)

    for name, depth_camera in self._host.depth_cameras.items():
      if not self._quiet:
        print("Discovered --cameras=depth-camera" +
              (("." + name) if name else ""))
      if (self._depth_camera_windows is not None and
          name not in self._depth_camera_windows):
        continue
      depth_camera.add_update_callback(self._depth_camera_callback)
      if use_tags:
        depth_camera.enable_tagged_request()
      elif reqfps > 0:
        depth_camera.start_streaming(1.0 / reqfps)

    for name, oracle in self._host.oracles.items():
      if not self._quiet:
        print("Discovered --cameras=oracle" + (("." + name) if name else ""))
      if self._oracle_windows is not None and name not in self._oracle_windows:
        continue
      oracle.add_update_callback(self._oracle_callback)
      if use_tags or reqfps > 0:
        oracle.enable_tagged_request(
            intent="",
            prediction_type="",
            request_type="",
            task_code="",
            label="")
      else:
        self._unrequested_oracles.add(name)

    for name, vnc in self._host.vncs.items():
      if not self._quiet:
        print("Discovered --cameras=vnc" + (("." + name) if name else ""))
      if self._vnc_windows is not None and name not in self._vnc_windows:
        continue
      vnc.add_update_callback(self._vnc_callback)
      if use_tags:
        vnc.enable_tagged_request()
      elif reqfps > 0:
        vnc.start_streaming(1.0 / reqfps)

    internal = self._host.internal
    if internal:
      internal.add_device_data_callback(self._internal_callback)

    name_lock = threading.Lock()
    with name_lock:

      def host_id_callback(host_id: str) -> bool:
        with name_lock:
          # The host name is only used for unified view.
          self._image_display.update_host_name(host_id)
        return False

      self._host.add_host_id_callback(host_id_callback)
      host_id = self._host.host_id
      if host_id:
        self._image_display.update_host_name(host_id)

  def _image_callback(self, listeners: Optional[Dict[str, List[Tuple[str,
                                                                     bool]]]],
                      device_type: str, device_name: str,
                      color_image: np.ndarray,
                      depth_image: Optional[np.ndarray]) -> None:
    """Image callback is called when a new image is loaded.

    Args:
      listeners: the list of listener window names for this device type. If
        None, a single window (device_type.device_name) will be displayed. Else,
        the windows in listeners[device_name] will be updated with the image,
        the booleans specifying to update the overlay.
      device_type: the device type for the image.
      device_name: the device name for the image.
      color_image: the color image.
      depth_image: optional depth image.
    """
    if listeners is None:
      self._image_listener(
          self._device_to_key(device_type, device_name), False, device_type,
          device_name, color_image, depth_image)
    elif device_name in listeners:
      for window_name, overlay in listeners[device_name]:
        self._image_listener(window_name, overlay, device_type, device_name,
                             color_image, depth_image)

  def _color_camera_callback(self, msg: ColorFrame) -> bool:
    self._image_callback(self._color_camera_windows, "color-camera",
                         msg.device_name, msg.color_image, None)
    return False

  def _depth_camera_callback(self, msg: DepthFrame) -> bool:
    self._image_callback(self._depth_camera_windows, "depth-camera",
                         msg.device_name, msg.color_data, msg.depth_data)
    return False

  def _oracle_callback(self, msg: Prediction) -> bool:
    self._image_callback(self._oracle_windows, "oracle", msg.device_name,
                         msg.image, None)
    return False

  def _vnc_callback(self, msg: ColorFrame) -> bool:
    self._image_callback(self._vnc_windows, "vnc", msg.device_name,
                         msg.color_image, None)
    return False

  @staticmethod
  def _split_key(device_key: str) -> Tuple[str, str]:
    values = device_key.split(_TYPE_NAME_SEP)
    if len(values) == 1:
      return values[0], ""
    return values[0], values[1]

  @staticmethod
  def _device_to_key(dtype: str, dname: str) -> str:
    if not dname:
      return dtype
    return dtype + _TYPE_NAME_SEP + dname

  def _internal_callback(self, msg: types_gen.DeviceData) -> bool:
    if msg.detection:
      self._object_detector_listener(msg)
    self._unrequested_oracle_listener(msg)
    return False

  def _unrequested_oracle_listener(self, msg: types_gen.DeviceData) -> None:
    """Called when a new device data is received to update unrequested oracles.

    Args:
      msg: The device data message.
    """
    if msg.device_type != "oracle":
      return
    if msg.data_type != "prediction":
      return
    if msg.device_name not in self._unrequested_oracles:
      return
    try:
      image = load_image(msg.color)
    except FileNotFoundError:
      print("oracle message missing file %s", msg.color)
      return
    self._image_callback(self._oracle_windows, "oracle", msg.device_name,
                         image, None)

  def _object_detector_listener(self, msg: types_gen.DeviceData) -> None:
    """Called when a new device data is received to update object detector.

    Args:
      msg: The device data message.
    """
    if not self._show_detections:
      return
    data = msg.detection
    if not data:
      return
    source = data.source
    if not source:
      return
    window_name, unused_is_overlay = self._device_to_window(
        source.device_type, source.device_name)
    polygons: List[image_display.NamedPolygonT] = []
    for det in data.detections:
      if not det.corners:
        # AprilGroup detections may not have corners.
        continue
      corners: List[float] = det.corners
      coords = [(corners[i], corners[i + 1]) for i in range(0, len(corners), 2)]
      polygons.append((det.py_type + "-" + det.py_id, coords))
    self._image_display.update_detections(window_name, polygons)

  def _device_to_window(self, dtype: str, dname: str) -> Tuple[str, bool]:
    """Returns (virtual) window name assgined for device, and bool indicating overlay."""
    is_overlay = False

    device_key = self._device_to_key(dtype, dname)
    if device_key in self._overlay_target:
      is_overlay = True
      dtype, dname = self._split_key(self._overlay_target[device_key])

    window_name = dtype
    if dname:
      window_name += _TYPE_NAME_SEP + dname
    return window_name, is_overlay

  def _image_listener(self, window_name: str, is_overlay: bool,
                      device_type: str, device_name: str, color: np.ndarray,
                      depth: Optional[np.ndarray]) -> None:
    """Image listener is called when a window is to be updated.

    Args:
      window_name: the window name to be updated.
      is_overlay: if true, window should be overlay.
      device_type: the device type.
      device_name: the device name.
      color: the color image.
      depth: the optional depth image.
    """
    calibration_intrinsics: Optional[Tuple[float, ...]] = None
    calibration_distortion: Optional[Tuple[float, ...]] = None
    calibration = self._host.config.calibration
    if self._show_undistortion and calibration:
      device = calibration.get_device(device_type, device_name)
      if device and isinstance(device, CalibrationCamera):
        calibration_intrinsics = device.intrinsics
        calibration_distortion = device.distortion

    self._image_display.update_image(
        window_name,
        color,
        intrinsics=calibration_intrinsics,
        distortion=calibration_distortion,
        overlay=is_overlay,
        depth=False)
    if depth is not None:
      self._image_display.update_image(
          window_name + "_depth",
          depth,
          intrinsics=calibration_intrinsics,
          distortion=calibration_distortion,
          overlay=False,
          depth=True)

  def _on_mouse(self, window_name: str, x: float, y: float, wx: float,
                wy: float) -> None:
    """Handles mouse, to send vnc commands."""
    if not window_name.startswith("vnc.") and window_name != "vnc":
      return
    vnc = self._host.vncs.get("" if window_name ==
                              "vnc" else window_name[len("vnc."):])
    if vnc is None:
      return
    frac_x = x / wx
    frac_y = y / wy
    vnc.async_send_pointer_event(frac_x, frac_y, PointerEventType.SEND_CLICK)
    print("Sent click over vnc.")

  def _wait_close_thread(self) -> None:
    """Wait for the host the close, then stop."""
    self._host.wait()
    self._cv2e.stop()

  def run(self) -> None:
    """Run runs the viewer until the window is closed or exit key is pressed."""
    thread = threading.Thread(target=self._wait_close_thread)
    thread.start()
    try:
      for c in self._cv2e.key_iterator():
        # needed for different UI toolkit installs.
        if c > 0x100000:
          c -= 0x100000

        if c == ord(" "):
          self._image_display.take_snapshots()
      print("Controller shutting down.")
    finally:
      self._host.close()
      thread.join()
