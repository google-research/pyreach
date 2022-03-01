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

"""RGBD viewer."""

import threading
import time
from typing import List, Optional, Tuple

import cv2  # type: ignore  # type: ignore
import numpy as np

import google3.third_party.open3d.open3d as o3d  # type: ignore


_DEPTH_SCALE = 0.1


# Fast conversion of rgbd images to point cloud.
# TODO(hirak): Include depthDistortions.
# TODO(hirak): May be this should be moved to transform_utils.py.
def pgm_to_pointcloud(
    depth_image: np.ndarray, color_image: Optional[np.ndarray],
    intrinsics: Tuple[float, float, float, float],
    distortion: List[float]) -> Tuple[np.ndarray, Optional[np.ndarray]]:
  """Fast conversion of opencv images to pointcloud.

  Takes ~7 ms per 1280x720 RGBD on my corp laptop (hirak).

  Args:
    depth_image: OpenCV image.
    color_image: Corresponding color image, if colors for each point is desired.
    intrinsics: fx, fy, cx, cy.
    distortion: Standard distoriton params k1, k2, p1, p2, [k3, [k4, k5, k6]].

  Returns:
    points: Nx3 array of points in space.
    colors: Nx3 array of colors, each row an RGB. None if color_image is None.
  """
  # The code below is optimized for speed, further optimizations may also be
  # possible.
  x_axis, y_axis = np.mgrid[0:depth_image.shape[1], 0:depth_image.shape[0]]
  valid = ~np.isnan(depth_image)
  x_axis = x_axis.T[valid]
  y_axis = y_axis.T[valid]
  depth = depth_image[valid] * _DEPTH_SCALE
  x_and_y = np.vstack([x_axis, y_axis]).astype(float)
  fx, fy, cx, cy = intrinsics
  camera_matrix = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
  x_and_y = cv2.undistortPoints(x_and_y, camera_matrix, np.array(distortion))
  x_and_y = x_and_y.T.reshape(2, -1)
  points = np.vstack([x_and_y * depth, depth]).T
  colors = None
  if color_image is not None:
    colors = color_image[valid]
    if len(colors.shape) > 1 and colors.shape[1] == 3:
      # OpenCV uses BGR. Point cloud libraries like to use RGB.
      colors[:, [0, 2]] = colors[:, [2, 0]]
    else:
      colors = np.vstack([colors, colors, colors]).T
  return points, colors


# TODO(hirak): Correct for extrinsics (useful to test multiple depth cams).
def _pgm_to_pcd(depth_raw: np.ndarray, color_raw: np.ndarray,
                intrinsics: Tuple[float, float, float, float],
                distortion: List[float]) -> o3d.geometry.PointCloud:
  """Obtain an Open3d pointcloud from RGBD data."""
  points, colors = pgm_to_pointcloud(depth_raw, color_raw, intrinsics,
                                     distortion)
  pcd = o3d.geometry.PointCloud()
  pcd.points = o3d.utility.Vector3dVector(points)
  # This is to appease pytype.
  # colors must be populated, since we passed color to pgm_to_pointcloud.
  assert colors is not None
  pcd.colors = o3d.utility.Vector3dVector(colors / 256)
  # Flip it, otherwise the pointcloud will be upside down.
  pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
  return pcd


class RgbdViewer:
  """Allows viewing 3d images."""

  def __init__(self) -> None:
    """Initialize the visualizer."""
    self._vis = o3d.visualization.Visualizer()
    self._lock = threading.Lock()
    self._refresh_lock = threading.Lock()
    self._frame_count = 0
    self._intrinsics: Optional[Tuple[float, float, float, float]] = None
    self._distortion: Optional[List[float]] = None
    self._thread: Optional[threading.Thread] = None
    self._thread_created = threading.Event()

  def _setup_vis(self) -> None:
    """Setup the visualizer."""
    self._vis.create_window()
    opt = self._vis.get_render_option()
    opt.background_color = np.asarray([0, 0, 0])
    opt.point_size = 2

    def o3d_viz() -> None:
      while True:
        with self._refresh_lock:
          if not self._vis.poll_events():
            print("Stopped")
            self._vis.close()
            self._vis.destroy_window()
            break
          self._vis.update_renderer()
        time.sleep(0.05)

    self._thread = threading.Thread(target=o3d_viz, daemon=True)
    self._thread.start()
    self._thread_created.set()

  def set_calibration(self, intrinsics: Tuple[float, float, float, float],
                      distortion: List[float]) -> None:
    """Updates the calibration parameters.

    Args:
      intrinsics: the camera intrinsics.
      distortion: the camera distortion.
    """
    self._intrinsics = intrinsics
    self._distortion = distortion

  def update_image(self, depth_fname: str, color_fname: str) -> None:
    """Update image updates the image.

    Args:
      depth_fname: the depth filename.
      color_fname: the color filename.
    """
    if self._intrinsics is None or self._distortion is None:
      print("Invalid intrinsics or distortion")
      return
    if self._lock.locked():
      print("Skipping image...")
      return
    with self._lock:
      depth_raw = cv2.imread(depth_fname, cv2.IMREAD_ANYDEPTH)
      if depth_raw is None:
        return
      color_raw = cv2.imread(color_fname, cv2.IMREAD_ANYCOLOR)

      # Get the point cloud from depth and color images.
      pcd = _pgm_to_pcd(depth_raw, color_raw, self._intrinsics,
                        self._distortion)
      if self._frame_count == 0:
        self._setup_vis()
      with self._refresh_lock:
        self._vis.clear_geometries()
        self._vis.add_geometry(pcd, reset_bounding_box=self._frame_count == 0)
      self._frame_count += 1

  def update_image_frames(self, depth_raw: np.ndarray,
                          color_raw: np.ndarray) -> None:
    """Update image updates the image frames.

    Args:
      depth_raw: the depth image.
      color_raw: the color image.
    """
    if self._intrinsics is None or self._distortion is None:
      print("Invalid intrinsics or distortion")
      return
    if self._lock.locked():
      print("Skipping image...")
      return
    with self._lock:
      # Get the point cloud from depth and color images.
      pcd = _pgm_to_pcd(depth_raw, color_raw, self._intrinsics,
                        self._distortion)
      if self._frame_count == 0:
        self._setup_vis()
      with self._refresh_lock:
        self._vis.clear_geometries()
        self._vis.add_geometry(pcd, reset_bounding_box=self._frame_count == 0)
      self._frame_count += 1

  def is_alive(self) -> bool:
    """Returns True until the user closes the UI."""
    if self._frame_count == 0:
      return True
    return self._thread is not None and self._thread.is_alive()

  def wait_until_closed(self) -> None:
    """Blocks the thread and wait till the user closes the UI."""
    self._thread_created.wait()
    assert self._thread is not None
    self._thread.join()
