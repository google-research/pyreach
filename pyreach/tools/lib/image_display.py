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

"""Manages the abstraction for showing windows.

Can show in a single unified window, or in multiple windows.
"""
import math
import os
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

import cv2  # type: ignore  # type: ignore
import numpy as np

from pyreach.tools.lib import cv2_eventloop
from pyreach.tools.lib import frame_counter
from pyreach.tools.lib import undistortion_field

# Directory where image snapshots will be saved.
_SNAPSHOT_DIR = "snapshots"

# Aspect ratio used for the unified window.
_UNIFIED_ASPECT_RATIO = 16 / 9

# Color in which the crosshair is drawn, in the form (B, G, R).
_CROSSHAIR_COLOR = (255, 0, 255)

# Fraction of the image height which the crosshair should take up.
_CROSSHAIR_LENGTH_FRAC = 0.25

# The crosshair thickness in pixels.
_CROSSHAIR_THICKNESS = 2

# Type denoting tuple of (object name, coordinates).
NamedPolygonT = Tuple[str, List[Tuple[float, float]]]


def _draw_crosshair(img: np.ndarray, color: Tuple[int, int, int],
                    length_frac: float, thickness: int) -> None:
  """Draw a crosshair at the centre of each image.

  Args:
    img: The image to draw the crosshair on. This image is edited in place.
    color: Color in which the crosshair is drawn, in the form (B, G, R).
    length_frac: Fraction of the image height which the crosshair should take
      up. This value should be in the range 0 to 1.
    thickness: The crosshair thickness in pixels.
  """

  assert 0. < length_frac <= 1.

  length = int(length_frac * img.shape[0])
  centre_x = int(img.shape[1] / 2)
  centre_y = int(img.shape[0] / 2)

  # Draw a vertical line
  cv2.line(img, (centre_x, centre_y - int(length / 2)),
           (centre_x, centre_y + int(length / 2)), color, thickness)

  # Draw a horizontal line
  cv2.line(img, (centre_x - int(length / 2), centre_y),
           (centre_x + int(length / 2), centre_y), color, thickness)


def _get_image_to_show(img: Optional[np.ndarray],
                       overlay_img: Optional[np.ndarray] = None,
                       show_crosshair: bool = True) -> Optional[np.ndarray]:
  """Get the image to show in the viewer.

  Args:
    img: the image.
    overlay_img: optional overlay image.
    show_crosshair: if true, the crosshair at the centre of each image will be
      drawn.

  Raises:
    RuntimeError: if the image format is unexpected.

  Returns:
    The image to display.
  """
  if img is None:
    return None
  if img.dtype == np.uint16:
    img = cv2.applyColorMap((img / 64).astype(np.uint8), cv2.COLORMAP_JET)
  elif img.dtype == np.uint8:
    if overlay_img is not None:
      if img.shape[0] == overlay_img.shape[0] and img.shape[
          1] == overlay_img.shape[1]:
        if overlay_img.dtype == np.uint16:
          o2 = cv2.applyColorMap((overlay_img / 64).astype(np.uint8),
                                 cv2.COLORMAP_JET)
          img = cv2.addWeighted(img, 0.5, o2, 0.5, 0)
        else:
          img = cv2.addWeighted(img, 0.5, overlay_img, 0.5, 0)
      else:
        print("Img has size {} and overlay has size {}".format(
            img.shape, overlay_img.shape))
  else:
    raise RuntimeError(f"Unexpected image format {img.dtype!r}")

  if show_crosshair and img is not None:
    _draw_crosshair(img, _CROSSHAIR_COLOR, _CROSSHAIR_LENGTH_FRAC,
                    _CROSSHAIR_THICKNESS)
  return img


class ImageDisplay:
  """ImageDisplay displays images."""

  def __init__(self, uwidth: int = 0, show_crosshair: bool = True) -> None:
    """Initialize the image display.

    Args:
      uwidth: the width of the display, if zero, will autoscale.
      show_crosshair: if true, the crosshair at the centre of each image will be
        displayed.
    """
    # Threadsafe cv2.
    self._cv2e = cv2_eventloop.get_instance()
    # Stores the latest image file and overlay displayed, per window.
    self._last_shown: Dict[str, Tuple[np.ndarray, Optional[np.ndarray],
                                      bool]] = {}
    self._last_detected_objects: Dict[str, List[NamedPolygonT]] = {}
    # Counts number of frames per window.
    self._frames: Dict[str, frame_counter.FrameCounter] = {}
    # If true, will draw everything in one window.
    self._uwidth = uwidth
    # If true, the crosshair at the center of each image will be displayed.
    self._show_crosshair = show_crosshair
    # Callback for mouse clicks. Must take (window_name, x, y, width, height).
    self._click_listeners: List[Callable[[str, float, float, float, float],
                                         None]] = []

    # Following are used only for unified view.
    # Connected host name, used for unified window title.
    self._host_name: Optional[str] = None
    # Unified window shape.
    self._unified_shape = (int(uwidth // _UNIFIED_ASPECT_RATIO), uwidth)
    # Last known window boundaries.
    self._window_rects: List[Tuple[str, Tuple[int, int, int, int],
                                   Tuple[int, int]]] = []
    # Unified window name.
    self._unified_window_name = "Unified View"
    if self._is_unified():
      self._cv2e.call(cv2.namedWindow, self._unified_window_name)
      self._cv2e.call(cv2.setMouseCallback, self._unified_window_name,
                      self._cv2_on_mouse)

  def _is_unified(self) -> bool:
    """Get if the display is unified together in a single display.

    Returns:
      True if the display is unified together.
    """
    return self._uwidth > 0

  def add_click_listener(
      self, listener: Callable[[str, float, float, float, float],
                               None]) -> None:
    """Add a listener that is called when a click is generated.

    Args:
      listener: the listener to add.
    """
    self._click_listeners.append(listener)

  def _cv2_on_mouse(self, event: int, x: float, y: float, unused_flags: int,
                    params: str) -> None:
    """Called when a mouse click is registered.

    Args:
      event: the OpenCV event type.
      x: the X position of the click, as a fraction of the window.
      y: the Y position of the click, as a fraction of the window.
      unused_flags: flags passed by OpenCV, ignored.
      params: the name of the window.
    """
    if event != cv2.EVENT_LBUTTONDOWN:
      return
    if self._is_unified():
      window_rects = self._window_rects  # Copy over for thread safety.
      for name, (x1, y1, x2, y2), (fx, fy) in window_rects:
        if x >= x1 and x <= x2 and y >= y1 and y <= y2:
          x = (x - x1) / (x2 - x1) * fx
          y = (y - y1) / (y2 - y1) * fy
          wname = name
          break
      else:
        # Click was not on any of the mapped images.
        print("Click detected outside any feed.")
        return
    else:
      wname = params
      if wname not in self._last_shown:
        return
      last_img = self._last_shown[wname][0]
      fx, fy = last_img.shape[1], last_img.shape[0]
    print(f"Click detected: {wname} ({x:0.1f}, {y:0.1f})")
    for listener in self._click_listeners:
      listener(wname, x, y, fx, fy)

  def _resize_image_to(self, texts: List[str], img: np.ndarray,
                       target_img: np.ndarray, target_start: Tuple[int, int],
                       target_extent: Tuple[int,
                                            int], window_name: str) -> None:
    """Resize the image to display.

    Args:
      texts: list of text to display on the image.
      img: the image to display.
      target_img: the target image.
      target_start: the start (x, y) tuple to paste the target.
      target_extent: the size (width, height) tuple to paste the image to.
      window_name: the name of the window.
    """
    # TODO: Height / width and x / y are swapped in this method. Should
    # be corrected.
    width, height = target_extent
    owidth, oheight = img.shape[0], img.shape[1]
    aspect = owidth / oheight
    if width / height > aspect:
      width = int(height * aspect)
    else:
      height = int(width / aspect)
    img = cv2.resize(img, (height, width))
    for line_no, line in enumerate(texts):
      cv2.putText(img, line, (21, 31 + 20 * line_no), cv2.FONT_HERSHEY_DUPLEX,
                  0.6, (64, 64, 64))
      cv2.putText(img, line, (20, 30 + 20 * line_no), cv2.FONT_HERSHEY_DUPLEX,
                  0.6, (0, 192, 256))
    x1 = target_start[0] + (target_extent[0] - width) // 2
    x2 = x1 + width
    y1 = target_start[1] + (target_extent[1] - height) // 2
    y2 = y1 + height
    if x1 < x2 and y1 < y2:
      target_img[x1:x2, y1:y2] = img
    # Store the window mapping so that we can retrieve original coordinates on
    # click.
    self._window_rects.append(
        (window_name, (y1, x1, y2, x2), (oheight, owidth)))

  def _draw_unified_view(self) -> None:
    """Draw unified view draws a unified view."""
    # Create a grid of number of images.
    n = len(self._last_shown)
    h = int(math.ceil(math.sqrt(n)))
    w = int(math.ceil(n / h))
    resize_to = (self._unified_shape[1] // w, self._unified_shape[0] // h)
    unified_image = np.zeros(
        (self._unified_shape[0], self._unified_shape[1], 3), np.uint8)
    self._window_rects = []
    for index, window_tuple in enumerate(sorted(self._last_shown.items())):
      wname, images_tuple = window_tuple
      raw_img, raw_ovl, _ = images_tuple
      img = _get_image_to_show(raw_img, raw_ovl, self._show_crosshair)
      if img is None:
        continue
      grid_j = index // h
      grid_i = index % h
      start_y = int(grid_i * self._unified_shape[0] / h)
      start_x = int(grid_j * self._unified_shape[1] / w)
      texts = [
          f"{wname} ({raw_img.shape[1]} x {raw_img.shape[0]})",
          f"Client fps: {self._frames[wname].fps:0.2f} "
          f"[{self._frames[wname].frames}]",
      ]
      self._resize_image_to(texts, img, unified_image, (start_y, start_x),
                            (resize_to[1], resize_to[0]), wname)
    self._cv2e.call(cv2.imshow, self._unified_window_name, unified_image)

  def update_host_name(self, host: str) -> None:
    if not host or self._host_name == host:
      return
    self._host_name = host
    if self._is_unified():
      # Ensures that the window exists.
      self._cv2e.call(cv2.namedWindow, self._unified_window_name)
      # Changes the title for the window.
      self._cv2e.call(cv2.setWindowTitle, self._unified_window_name,
                      self._unified_window_name + " - " + self._host_name)

  def _render(self, window_name: str, img: Any) -> None:
    if self._is_unified():
      self._draw_unified_view()
    else:
      if img is not None:
        self._cv2e.call(cv2.imshow, window_name, img)

  def update_detections(self, window_name: str,
                        polygons: List[NamedPolygonT]) -> None:
    self._last_detected_objects[window_name] = polygons

  def _draw_detections(self, img: np.ndarray, window_name: str) -> np.ndarray:
    """Draw the detections from the object detector.

    Args:
      img: the image to draw upon.
      window_name: the name of the window.

    Returns:
      The image with detections drawn.
    """
    if window_name not in self._last_detected_objects:
      return img
    polygons = self._last_detected_objects[window_name]
    all_pts: List[np.ndarray] = []
    color = (0, 0, 196)
    for desc, points in polygons:
      img = cv2.putText(
          img,
          desc, (int(points[0][0]), int(points[0][1])),
          cv2.FONT_HERSHEY_PLAIN,
          fontScale=1,
          thickness=2,
          color=color)
      all_pts.append(np.array(points, dtype=int).reshape((-1, 1, 2)))
    img = cv2.polylines(img, all_pts, isClosed=True, color=color, thickness=2)
    return img

  def update_image(self, window_name: str, img_input: np.ndarray,
                   intrinsics: Optional[Tuple[float, ...]],
                   distortion: Optional[Tuple[float, ...]], overlay: bool,
                   depth: bool) -> None:
    """Shows a cv2 color or depth image on a window_name.

    Args:
      window_name: the name of the window to update.
      img_input: the input image.
      intrinsics: the calibration intrinsics.
      distortion: the calibration distortion.
      overlay: if true, write the overlay image.
      depth: if true, write the depth image.

    Raises:
      RuntimeError: if the image fails to load.
    """
    if not self._is_unified():
      # Add callbacks if we encounter a window for the first time.
      if window_name not in self._last_shown:
        self._cv2e.call(cv2.namedWindow, window_name)
        self._cv2e.call(cv2.setMouseCallback, window_name, self._cv2_on_mouse,
                        window_name)
    if not depth:
      img_input = cv2.cvtColor(img_input, cv2.COLOR_RGB2BGR)
    img, ovl, _ = self._last_shown.get(window_name, (None, None, depth))
    if overlay:
      ovl = img_input
    else:
      img = img_input
    if intrinsics is not None and distortion is not None and img is not None:
      # Render undistortion field.
      undistortion_field.render_onto(img, intrinsics, distortion)
    if img is None:
      return
    self._last_shown[window_name] = (img, ovl, depth)
    if img is None:
      raise RuntimeError("Overlay received before original image")
    self._frames.setdefault(window_name, frame_counter.FrameCounter()).incr()

    # Optionally apply overlay (e.g. --cameras=depth-camera+oracle.pick-points).
    img = _get_image_to_show(img, ovl, self._show_crosshair)
    if img is None:
      return
    # If detections exist, render them.
    img = self._draw_detections(img, window_name)
    self._render(window_name, img)

  def take_snapshots(self) -> None:
    """Save the latest images to disk."""
    os.makedirs(_SNAPSHOT_DIR, exist_ok=True)

    ts = int(time.time() * 1000)

    def snap(window_name: str, img: np.ndarray, depth: bool) -> None:
      target = os.path.join(_SNAPSHOT_DIR, window_name + "_" + str(ts))
      if depth:
        target += ".pgm"
      else:
        target += ".jpg"
      cv2.imwrite(target, img)
      print(f"Saved {target}")

    for window, (img, overlay_img, depth) in self._last_shown.items():
      if img is not None:
        snap(window, img, depth)
      if overlay_img is not None:
        snap(window, overlay_img, depth)

    # Clear last images.
    self._last_shown = {}
