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

"""Compute undistortion fields for images."""

from typing import Tuple

import cv2  # type: ignore  # type: ignore
import numpy as np


def _get_undistortion_shifts(
    depth_image: np.ndarray, intrinsics: Tuple[float, ...],
    distortion: Tuple[float, ...]) -> Tuple[np.ndarray, np.ndarray]:
  """Returns difference between using and not using distortion.

  Args:
    depth_image: Opencv Image.
    intrinsics: [fx, fy, cx, cy].
    distortion: [k1, k2, p1, p2, k3].

  Returns:
    Sampling points [(u, v), ...], and
    deltas [(dx, dy), ...] in pixel units.
  """
  stride = 10
  x_axis, y_axis = np.mgrid[stride // 2:depth_image.shape[1]:stride,
                            stride // 2:depth_image.shape[0]:stride]
  valid = np.ones_like(x_axis).astype(bool).T
  x_axis = x_axis.T[valid]
  y_axis = y_axis.T[valid]
  x_and_y = np.vstack([x_axis, y_axis]).astype(float)
  x_and_y = x_and_y[:, ::20]
  fx, fy, cx, cy = intrinsics
  camera_matrix = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
  no_undistort = cv2.undistortPoints(x_and_y, camera_matrix,
                                     np.array([0, 0, 0, 0, 0]))
  with_undistort = cv2.undistortPoints(x_and_y, camera_matrix,
                                       np.array(distortion))
  # Difference focal-length cooridnates.
  diff = with_undistort - no_undistort
  # Reshape, and convert to pixel units.
  diff = diff.reshape((diff.shape[0], diff.shape[2])) * [[fx, fy]]
  return x_and_y.T, diff


def _draw_arrow(image: np.ndarray, center: np.ndarray, uv: np.ndarray,
                delta: float) -> None:
  """Draw an arrow on an image.

  Args:
    image: the image to render the arrow onto.
    center: the center point of the image.
    uv: the direction of the arrow.
    delta: the length of the arrow.
  """
  if np.abs(delta).max() < 1:
    return
  original_rad = np.linalg.norm(uv - center)
  new_rad = np.linalg.norm(uv + delta - center)
  cv2.arrowedLine(
      image,
      tuple(uv.astype(int).tolist()),
      tuple((uv + delta).astype(int).tolist()),
      color=(0, 255, 0) if new_rad > original_rad else (0, 0, 255),
      thickness=2,
      tipLength=0.2)


def render_onto(orig_image: np.ndarray, intrinsics: Tuple[float, ...],
                distortion: Tuple[float, ...]) -> None:
  """Render an undistortion field onto an image.

  Args:
    orig_image: the image to render the field onto.
    intrinsics: the intrinsics for undistortion.
    distortion: the distrortion field.
  """
  image = orig_image.copy()
  uv_coords, deltas = _get_undistortion_shifts(image, intrinsics, distortion)
  center = np.array(intrinsics[2:4], dtype=float)
  for index in range(uv_coords.shape[0]):
    uv = uv_coords[index, :]
    delta = deltas[index, :]
    _draw_arrow(image, center, uv, delta)
  cv2.addWeighted(orig_image, 0.5, image, 0.5, 0, dst=orig_image)
