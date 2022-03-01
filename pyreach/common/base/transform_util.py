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

# Lint as: python3
r"""A collection of math transform methods."""

import math
import random
import sys
from typing import List, Tuple, Union, Optional

import numpy as np
from scipy.spatial.transform.rotation import Rotation  # type: ignore
import cv2  # type: ignore

ZERO_VECTOR3 = np.array([0.0, 0.0, 0.0]).reshape(3, 1)
X_VECTOR3 = np.array([1.0, 0.0, 0.0]).reshape(3, 1)
Y_VECTOR3 = np.array([0.0, 1.0, 0.0]).reshape(3, 1)
Z_VECTOR3 = np.array([0.0, 0.0, 1.0]).reshape(3, 1)

_FloatOrInt = Union[float, int]
ArrayOrList = Union[List[_FloatOrInt], Tuple[_FloatOrInt], np.ndarray]
ArrayOrList2 = Union[List[_FloatOrInt], Tuple[_FloatOrInt, _FloatOrInt],
                     np.ndarray]
ArrayOrList3 = Union[List[_FloatOrInt], Tuple[_FloatOrInt, _FloatOrInt,
                                              _FloatOrInt], np.ndarray]
ArrayOrList4 = Union[List[_FloatOrInt], Tuple[_FloatOrInt, _FloatOrInt,
                                              _FloatOrInt, _FloatOrInt],
                     np.ndarray]
ArrayOrList8 = Union[List[_FloatOrInt],
                     Tuple[_FloatOrInt, _FloatOrInt, _FloatOrInt, _FloatOrInt,
                           _FloatOrInt, _FloatOrInt, _FloatOrInt, _FloatOrInt],
                     np.ndarray]


def transform(v: np.ndarray, translation: Optional[np.ndarray],
              rotation: Optional[np.ndarray]) -> np.ndarray:
  """Transforms a 3D point using translation and rotation vectors.

  This rotates in place before translation. This is the way Unity operates.

  Args:
    v: array containing (x, y, z) coords or numpy array of shape (3, N).
    translation: array containing input translation (t_x, t_y, t_z).
    rotation: array containing input rotation vector parameterized using
      OpenCV's Rodrigues parameterization: (r_x, r_y, r_z).

  Returns:
    array containing (x, y, z) points of shape (3, N).
  """
  npnts = v.size // 3
  v2 = v.reshape(3, npnts)
  if rotation is not None:
    r_mat, _ = cv2.Rodrigues(rotation.reshape(3, 1))
    v2 = r_mat.dot(v2)
  if translation is not None:
    v2 = np.add(v2, translation.reshape(3, 1))
  return v2


def transform_inv(v: np.ndarray, translation: Optional[np.ndarray],
                  rotation: Optional[np.ndarray]) -> np.ndarray:
  """Transforms a 3D point using the inverse translation and rotation vectors.

  Args:
    v: array containing (x, y, z) coords or numpy array of shape (3, N).
    translation: array containing input translation (t_x, t_y, t_z).
    rotation: array containing input rotation vector parameterized using
      OpenCV's Rodrigues parameterization: (r_x, r_y, r_z).

  Returns:
    array containing (x, y, z) points of shape (3, N).
  """
  npnts = v.size // 3
  v2 = v.reshape(3, npnts)
  if translation is not None:
    v2 = np.add(v2, -translation.reshape(3, 1))

  if rotation is not None:
    r_mat, _ = cv2.Rodrigues(rotation.reshape(3, 1))
    v2 = r_mat.transpose().dot(v2)

  return v2


def project_2d_int(p: ArrayOrList3,
                   extrinsics: np.ndarray,
                   intrinsics: np.ndarray,
                   distortion: np.ndarray,
                   clip_range: float = 100000) -> Optional[Tuple[int, int]]:
  """Computes the 2D projection of a 3D point p.

  Using a camera model using the extrinsincs, intrinsics, and distortion
  parameters.

  Args:
    p: numpy array of type np.float32 containing (x, y, z) coord.
    extrinsics: numpy array of length 6 containing [t_x, t_y, t_z, r_x, r_y,
      r_z].
    intrinsics: numpy array of shape (3, 3). This is typically the return value
      of intrinsics_to_matrix.
    distortion: camera distortion parameters of shape (5,).
    clip_range: Return None if pixel x or y is larger than clip_range.

  Returns:
    x, y: integer pixel coords, else returns None if point is outside clip
      range or behind the camera view.
  """
  p2 = np.array(p, dtype=np.float32).reshape((1, 3, 1))

  # opencv project points will project even if behind camera
  # so do transform and z check here.
  p2 = transform(p2, extrinsics[:3].reshape(3, 1), extrinsics[3:].reshape(3, 1))
  if p2[2] < sys.float_info.epsilon:
    return None

  p2, _ = cv2.projectPoints(
      np.array([p2]), ZERO_VECTOR3, ZERO_VECTOR3, intrinsics, distortion)
  x = int(p2[0][0][0])
  y = int(p2[0][0][1])
  if x > clip_range:
    return None
  if x < -clip_range:
    return None
  if y > clip_range:
    return None
  if y < -clip_range:
    return None

  return x, y


def project(p: ArrayOrList3, extrinsics: np.ndarray, intrinsics: np.ndarray,
            distortion: np.ndarray) -> np.ndarray:
  """Compute the 2D projection of a 3D point p.

  Using a camera model using the extrinsincs, intrinsics, and distortion
  parameters.

  Args:
    p: array of containing (x, y, z) coord.
    extrinsics: array of length 6 containing [t_x, t_y, t_z, r_x, r_y, r_z].
    intrinsics: array of shape (3, 3). This is typically the return value of
      intrinsics_to_matrix.
    distortion: camera distortion parameters of shape (5,).

  Returns:
    numpy array of shape (1, 1, 2) containing projected x, y.
  """
  p2, _ = cv2.projectPoints(p, extrinsics[3:].reshape(3, 1),
                            extrinsics[:3].reshape(3,
                                                   1), intrinsics, distortion)

  return p2


def intrinsics_to_matrix(
    v: ArrayOrList4, dtype: np.dtype = np.dtype(np.float64)) -> np.ndarray:
  """Convert a flattened list of intrinsics to 3x3 intrincis matrix."""
  return np.array([[v[0], 0, v[2]], [0, v[1], v[3]], [0, 0, 1]], dtype=dtype)


def intrinsics_to_list(v: np.ndarray) -> List[float]:
  """Convert a 3x3 intrinsics matrix to a flattened list of intrinsics."""
  return [v[0, 0], v[1, 1], v[0, 2], v[1, 2]]


def unproject(p: ArrayOrList2, z: float, intrinsic: np.ndarray,
              distortion: ArrayOrList) -> np.ndarray:
  """Unproject (u,v) pixel coordinate, with depth z, into x,y,z coordinate.

  Args:
    p: (u,v) pixel coordinate.
    z: depth at pixel (u,v).
    intrinsic: array of shape (3, 3). This is typically the return value of
      intrinsics_to_matrix.
    distortion: camera distortion parameters of shape (5,).

  Returns:
    numpy.ndarray of shape (3,) containing xyz coordinate in camera frame.
  """
  cam_mtx = intrinsic  # shape [3,3]
  cam_dist = np.array(distortion)  # shape [5]
  pts = np.array([np.array(p, dtype=np.float32).reshape(1, 2)])  # shape [1,2]

  point_undistorted = cv2.undistortPoints(pts, cam_mtx, cam_dist)
  x = point_undistorted[0][0][0] * z
  y = point_undistorted[0][0][1] * z
  return np.array([x, y, z])


def unproject_depth_sample(img_pt: ArrayOrList2, raw_depth: float,
                           depth_dist: ArrayOrList8, camera_mtx: np.ndarray,
                           camera_dist: np.ndarray) -> np.ndarray:
  """Convert (u,v) pixel coordinate, with depth, into an (x, y, z) coordinate.

  Args:
    img_pt: (u,v) pixel coordinate.
    raw_depth: depth value pre-calibration.
    depth_dist: depth distortion parameters of shape (8,)
    camera_mtx: intrinsics matrix of shape (3, 3). This is typically the return
      value of intrinsics_to_matrix.
    camera_dist: camera distortion parameters. numpy array of shape (5,).

  Returns:
    xyz coordinate in camera frame of shape (1, 3).
  """
  # ax = (img_pt[0] - camera_mtx[0][2]) / camera_mtx[0][0]
  # ay = (img_pt[1] - camera_mtx[1][2]) / camera_mtx[1][1]
  adjusted_depth = depth_dist[0] + raw_depth * depth_dist[1]
  # + \
  # ax * depth_dist[2] + \
  # ay * depth_dist[3] + \
  # ax * ay * depth_dist[4] + \
  # ax * raw_depth * depth_dist[5] + \
  # ay * raw_depth * depth_dist[6] + \
  # ax * ay * raw_depth * depth_dist[7]
  return unproject(img_pt, adjusted_depth, camera_mtx,
                   camera_dist).reshape(1, 3)


def unproject_vectorized(uv_coordinates: np.ndarray, depth_values: np.ndarray,
                         intrinsic: np.ndarray,
                         distortion: np.ndarray) -> np.ndarray:
  """Vectorized version of unproject(), for N points.

  Args:
    uv_coordinates: pixel coordinates to unproject of shape (n, 2).
    depth_values: depth values corresponding index-wise to the uv_coordinates of
      shape (n).
    intrinsic: array of shape (3, 3). This is typically the return value of
      intrinsics_to_matrix.
    distortion: camera distortion parameters of shape (5,).

  Returns:
    xyz coordinates in camera frame of shape (n, 3).
  """
  cam_mtx = intrinsic  # shape [3, 3]
  cam_dist = np.array(distortion)  # shape [5]

  # shape of points_undistorted is [N, 2] after the squeeze().
  points_undistorted = cv2.undistortPoints(
      uv_coordinates.reshape((-1, 1, 2)), cam_mtx, cam_dist).squeeze(axis=1)

  x = points_undistorted[:, 0] * depth_values
  y = points_undistorted[:, 1] * depth_values

  xyz = np.vstack((x, y, depth_values)).T
  return xyz


def unproject_depth_sample_vectorized(img_pts: np.ndarray,
                                      raw_depths: np.ndarray,
                                      depth_dist: ArrayOrList8,
                                      camera_mtx: np.ndarray,
                                      camera_dist: np.ndarray) -> np.ndarray:
  """Convert (u,v) pixel coordinate, with depth, into an (x, y, z) coordinate.

  Args:
    img_pts: (u,v) pixel coordinates of shape (n, 2).
    raw_depths: depth values pre-calibration of shape (n).
    depth_dist: depth distortion parameters of shape (8,)
    camera_mtx: intrinsics matrix of shape (3, 3). This is typically the return
      value of intrinsics_to_matrix.
    camera_dist: camera distortion parameters. numpy array of shape (5,).

  Returns:
    xyz coordinates in camera frame of shape (n, 3).
  """
  adjusted_depths = depth_dist[0] + raw_depths * depth_dist[1]
  return unproject_vectorized(img_pts, adjusted_depths, camera_mtx,
                              camera_dist).reshape(img_pts.shape[0], 3)


def unproject_depth_vectorized(im_depth: np.ndarray, depth_dist: np.ndarray,
                               camera_mtx: np.ndarray,
                               camera_dist: np.ndarray) -> np.ndarray:
  """Unproject depth image into 3D point cloud, using calibration.

  Args:
    im_depth: raw depth image, pre-calibration of shape (height, width).
    depth_dist: depth distortion parameters of shape (8,)
    camera_mtx: intrinsics matrix of shape (3, 3). This is typically the return
      value of intrinsics_to_matrix.
    camera_dist: camera distortion parameters shape (5,).

  Returns:
    numpy array of shape [3, H*W]. each column is xyz coordinates
  """
  h, w = im_depth.shape

  # shape of each u_map, v_map is [H, W].
  dtype = np.float64 if not isinstance(im_depth, np.ndarray) else im_depth.dtype
  u_map, v_map = np.meshgrid(
      np.linspace(0, w - 1, w, dtype=dtype),
      np.linspace(0, h - 1, h, dtype=dtype))

  adjusted_depth = depth_dist[0] + im_depth * depth_dist[1]

  # shape after stack is [N, 2], where N = H * W.
  uv_coordinates = np.stack((u_map.reshape(-1), v_map.reshape(-1)), axis=-1)

  return unproject_vectorized(uv_coordinates, adjusted_depth.reshape(-1),
                              camera_mtx, camera_dist)


def pose_to_matrix(pose: np.ndarray) -> np.ndarray:
  """Converts a pose to a homogeneous transformation matrix.

  A pose is a 6-element array. First three elements are the translations of the
  post, next three elements are the rotation of the pose in the axis-angle
  representation.

  Args:
    pose: convert from pose.

  Returns:
    two dimensional numpy array of a homogeneous transformation matrix.
    array([[R00, R01, R02, T0],
           [R10, R11, R12, T1],
           [R20, R21, R22, T2],
           [0.,  0.,  0.,  1.]])
  """
  return convert_to_matrix(pose[0:3], pose[3:6])


def convert_to_matrix(translation: ArrayOrList3,
                      rotation: ArrayOrList3) -> np.ndarray:
  """Converts 3D translation & rotation to a homogeneous transformation matrix.

  Args:
    translation: x, y, z position of the pose.
    rotation: axis/angle representation of the rotation.

  Returns:
    two dimensional numpy array of a homogeneous transformation matrix.
    array([[R00, R01, R02, T0],
           [R10, R11, R12, T1],
           [R20, R21, R22, T2],
           [0.,  0.,  0.,  1.]])
  """
  m = np.zeros((4, 4), dtype=float)
  m[:3, :3] = cv2.Rodrigues(np.array(rotation))[0]
  m[0, 3] = translation[0]
  m[1, 3] = translation[1]
  m[2, 3] = translation[2]
  m[3, 3] = 1
  return m


def multiply_pose(a: np.ndarray, b: np.ndarray) -> np.ndarray:
  """Combine two poses.

  A pose is a 6-element array. First three elements are the translations of the
  post, next three elements are the rotation of the pose in the axis-angle
  representation.

  Args:
    a: relative pose on top of the base pose.
    b: base pose

  Returns:
    combined pose.
  """
  ma = pose_to_matrix(a)
  mb = pose_to_matrix(b)
  return matrix_to_pose(np.matmul(ma, mb))


def inverse_pose(pose: np.ndarray) -> np.ndarray:
  """Inverse a pose.

  A pose is a 6-element array. First three elements are the translations of the
  post, next three elements are the rotation of the pose in the axis-angle
  representation.

  Args:
    pose: relative pose on top of the base pose.

  Returns:
    inverted pose.
  """
  transformation_matrix = pose_to_matrix(pose)

  inverse_translation = np.identity(4, dtype=np.float64)
  inverse_translation[:3, 3] = -transformation_matrix[:3, 3]

  inverse_rotation = np.transpose(transformation_matrix)
  inverse_rotation[3, :3] = [0., 0., 0.]

  inverse_transformation_matrix = np.matmul(inverse_rotation,
                                            inverse_translation)
  return matrix_to_pose(inverse_transformation_matrix)


def matrix_to_pose(matrix: np.ndarray) -> np.ndarray:
  """Convert a homogeneous transformation matrix to a pose.

  A pose is a 6-element array. First three elements are the translations of the
  post, next three elements are the rotation of the pose in the axis-angle
  representation.

  Args:
    matrix: a two dimension ndarray representation of a homogeneous
      transformation matrix

  Returns:
    equivalent pose.

  """
  matrix_float = np.array(matrix, dtype=np.float64, copy=False)
  translation = matrix[:3, 3]
  rotation_matrix = matrix_float[:3, :3]
  axis_angle = cv2.Rodrigues(rotation_matrix)[0]
  return np.append(translation, axis_angle)


def angular_mod(angle: np.ndarray) -> np.ndarray:
  """Mod an angle to within the range of (-pi, pi).

  Args:
    angle: input angle in radius.

  Returns:
    Resulting angle within (-pi, pi)
  """
  return (angle + math.pi) % (2 * math.pi) - math.pi


def angular_mod_vector(axis_angle: np.ndarray) -> np.ndarray:
  """Angular mod the magnitude of a Rodriguez axis-angle vector.

  Args:
    axis_angle: a rodriguez axis-angle vector.

  Returns:
    Equivalent rodriguez axis-angle vector with angle within (-pi, pi)
  """
  mag = np.linalg.norm(axis_angle)
  if mag < math.pi:
    return axis_angle
  mag2 = angular_mod(mag)
  return (mag2 / mag) * axis_angle


def angular_mod_pose(pose: np.ndarray) -> np.ndarray:
  """Angular mod the rotation component of a pose.

  Args:
    pose: a 6-elements pose ndarray with element 3 - 6 in the Rodriguez
      axis-angle format.

  Returns:
    equivalent pose vector with angle within (-pi, pi)

  """
  axis_angle = pose[3:]
  pose[3:] = angular_mod_vector(axis_angle)
  return pose


def transform_by_pose(point: np.ndarray, pose: np.ndarray) -> np.ndarray:
  """Transforms a list of 3D points by a pose.

  Args:
    point: array containing (x, y, z) coords or numpy array of shape (3, N).
    pose: pose for the transformation.

  Returns:
    array containing (x, y, z) points of shape (3, N).
  """
  return transform(point, pose[0:3], pose[3:6])


def transformed_depth_sample(point: ArrayOrList2, depth_image: np.ndarray,
                             distortion_depth: np.ndarray,
                             intrinsics: np.ndarray, distortion: np.ndarray,
                             origin_t_dev: np.ndarray) -> Optional[np.ndarray]:
  """Get the pose of a depth pixel.

  Args:
    point: index of the depth pixel.
    depth_image: two dimension array of the depth image.
    distortion_depth: depth distortion parameters of shape (8,)
    intrinsics: intrinsics matrix of shape (3, 3).
    distortion: camera distortion parameters. numpy array of shape (5,).
    origin_t_dev: pose vector representing origin to device transformation.

  Returns:
    pose of the depth sample.
  """
  if (point[0] < 0) or (point[0] >= depth_image.shape[1]):
    return None
  if (point[1] < 0) or (point[1] >= depth_image.shape[0]):
    return None
  d = depth_image[point[1], point[0]]
  if d == 0:
    return None
  p = unproject_depth_sample(point, d, distortion_depth, intrinsics, distortion)
  return transform_by_pose(p, origin_t_dev)


def transform_between_two_vectors(position_a: np.ndarray,
                                  direction_a: np.ndarray,
                                  position_b: np.ndarray,
                                  direction_b: np.ndarray) -> np.ndarray:
  """Calculating transform between two vectors.

  Vectors are represented as position and direction pair. Position is a 3 DOF
  [x, y, z] array. Direction is a 2 DOF ray represented in [x, y, z] vector. The
  direction of the vector represent the direction of the ray. The length of the
  vector is ignored, unless when the length is too small that causes numerical
  stability issues.

  Args:
    position_a: position of vector A.
    direction_a: rotation of vector A.
    position_b: position of vector B.
    direction_b: rotation of vector B.

  Returns:
    The relative pose of B based on A.
  """
  translation = position_b - position_a
  mag_a = np.linalg.norm(direction_a)
  mag_b = np.linalg.norm(direction_b)

  if mag_a * mag_b < sys.float_info.epsilon:
    return np.concatenate((translation, ZERO_VECTOR3))

  angle = math.acos(np.dot(direction_a, direction_b) / (mag_a * mag_b))
  axis = np.cross(direction_a.reshape(1, 3), direction_b.reshape(1, 3))
  axis_mag = np.linalg.norm(axis)
  if axis_mag > sys.float_info.epsilon:
    axis *= angle / axis_mag
  else:
    # cross product is zero, construct a perpendicular rotation vector.
    axis = np.array([1., 1., 1.])
    if math.fabs(direction_a[2]) > sys.float_info.epsilon:
      axis[2] = -(axis[0] * direction_a[0] +
                  axis[1] * direction_a[1]) / direction_a[2]
    elif math.fabs(direction_a[1]) > sys.float_info.epsilon:
      axis[1] = -(axis[0] * direction_a[0] +
                  axis[2] * direction_a[2]) / direction_a[1]
    elif math.fabs(direction_a[0]) > sys.float_info.epsilon:
      axis[0] = -(axis[1] * direction_a[1] +
                  axis[2] * direction_a[2]) / direction_a[0]
    axis *= angle / np.linalg.norm(axis)

  pose = matrix_to_pose(convert_to_matrix(translation, axis))
  return pose


def pt_normal_depth_sample(
    point: ArrayOrList2, direction: ArrayOrList3, depth_image: np.ndarray,
    radius: int, distortion_depth: np.ndarray, intrinsics: np.ndarray,
    distortion: np.ndarray,
    origin_t_dev: np.ndarray) -> Optional[Tuple[np.ndarray, np.ndarray]]:
  """Calculate the surface normal for a depth pixel.

  Args:
    point: x, y coordinate of depth image sample
    direction: [1,3] direction of observation of the point used for return
      correct normal
    depth_image: [N,M] of np.uint8 depth image to ray cast into
    radius: radius in pixels around projected point to compute normal
    distortion_depth: distortion of the depth camera. [1,8] of float
    intrinsics: intrinsics of the depth camera. [3, 3] of float
    distortion: intrinsics distortion of the depth camera. [1, 5] of float
    origin_t_dev: extrinsics for the camera. [1,6] of float

  Returns:
    point and normal for this intersection. both of shape [1, 3]
    None if not hit

  """
  center = transformed_depth_sample(point, depth_image, distortion_depth,
                                    intrinsics, distortion, origin_t_dev)
  if center is None:
    return None
  center_pt = center.reshape((1, 3))[0]

  # simple 4 point sample and cross product to get normal
  x1 = transformed_depth_sample((point[0] - radius, point[1]), depth_image,
                                distortion_depth, intrinsics, distortion,
                                origin_t_dev)
  x2 = transformed_depth_sample((point[0] + radius, point[1]), depth_image,
                                distortion_depth, intrinsics, distortion,
                                origin_t_dev)
  y1 = transformed_depth_sample((point[0], point[1] - radius), depth_image,
                                distortion_depth, intrinsics, distortion,
                                origin_t_dev)
  y2 = transformed_depth_sample((point[0], point[1] + radius), depth_image,
                                distortion_depth, intrinsics, distortion,
                                origin_t_dev)
  if x1 is None or x2 is None or y1 is None or y2 is None:
    return None

  vx = x2 - x1
  vy = y2 - y1

  normal = np.cross(vx.reshape(1, 3)[0], vy.reshape(1, 3)[0])
  normal /= np.linalg.norm(normal)

  # flip the normal to point back toward toward the camera
  if np.dot(normal, direction) > 0:
    normal *= -1

  return center_pt, normal


def raycast_into_depth_image(
    origin: np.ndarray,
    direction: np.ndarray,
    depth_img: np.ndarray,
    intrinsics: np.ndarray,
    distortion: np.ndarray,
    distortion_depth: np.ndarray,
    origin_t_cam: np.ndarray,
    radius: int = 5,
    max_ray_dist: float = 4,
    init_ray_step_size: float = 0.05
) -> Optional[Tuple[np.ndarray, np.ndarray]]:
  """Compute the intersection point between a ray and a depth image.

  Args:
    origin: origin of the ray [x, y, z] in the origin/robot frame.
    direction: direction of the ray [x, y, z] in the origin/robot frame
    depth_img: depth image to ray cast into. [N, M] of np.uint8
    intrinsics: intrinsics of the depth camera. (3, 3) of float
    distortion: intrinsics distortion of the depth camera. (5,) of float
    distortion_depth: depth distortion of the depth camera. (8,) of float
    origin_t_cam: extrinsics for the camera (6,) of float
    radius: radius in pixels around projected point to compute normal
    max_ray_dist: maximum distance to traverse the ray in meters
    init_ray_step_size: initial step size for the ray march

  Returns:
    point and normal for this intersection. both of shape (3,).
    None if no hit.

  """
  cam_t_origin = inverse_pose(origin_t_cam)

  prev_depth_delta = -1

  cam_forward = transform_by_pose(
      np.array([0, 0, 1]).reshape((3, 1)), origin_t_cam)
  cam_forward -= origin_t_cam[:3].reshape((3, 1))

  step = init_ray_step_size

  p1 = origin
  img_pt = None
  hit = None

  # march along ray using step size, project into depth image from camera
  # perspective, when the ray samples are farther than the depth image samples,
  # we have an intersection
  for _ in range(4):
    # march along ray cast until we have an intersection
    p2 = p1.copy()
    for _ in range(int(max_ray_dist / step)):
      p2 += step * direction

      # we are behind the target camera, bail early
      delta = p2 - origin_t_cam[:3]
      if np.dot(direction, delta) < sys.float_info.epsilon:
        continue

      # project into the target camera
      pt = project_2d_int(p2, cam_t_origin, intrinsics, distortion, 100000)
      if pt is None:
        continue
      if not is_point_in_rectangle(
          pt, [0, 0, depth_img.shape[1], depth_img.shape[0]]):
        continue

      z = depth_img[pt[1], pt[0]]
      if z == 0:
        continue

      # we are within camera bounds and have a valid depth point
      depth_pt = unproject_depth_sample(pt, z, distortion_depth, intrinsics,
                                        distortion)
      depth_diff = np.linalg.norm(delta) - np.linalg.norm(depth_pt)

      # got an intersection, break out of this loop and refine search
      if (depth_diff > 0) and (prev_depth_delta < 0):
        hit = p1.copy()
        img_pt = pt
        break

      # got a good sample still above surface, move anchor point forward to
      # this point
      prev_depth_delta = depth_diff
      p1 = p2.copy()

    # exited inner loop when we encourter a distance sign change
    # reduce the step size and start checking again from the pre-intersection
    # point
    step /= 5

  if hit is None or img_pt is None:
    return None

  return pt_normal_depth_sample(img_pt, direction, depth_img, radius,
                                distortion_depth, intrinsics, distortion,
                                origin_t_cam)


def is_point_in_rectangle(point: Optional[Tuple[int, int]],
                          rectangle: List[int]) -> bool:
  """Checks if a point is within a rectangle.

  Args:
    point: point to check. (x, y)
    rectangle: bounding rectangle [left, bottom, right, top].

  Returns:
    True if the point is within the rectangle.
  """
  if point is None:
    return False

  return point[0] >= rectangle[0] and point[1] >= rectangle[1] and point[
      0] < rectangle[2] and point[1] < rectangle[3]


def pos_quaternion_to_matrix(translation: List[float],
                             quaternion: List[float]) -> np.ndarray:
  """Converts a translation-quaternion pair to a transformation matrix.

  Args:
    translation: translation [x, y, z]
    quaternion: rotation in the form of a quaternion [x, y, z, w].

  Returns:
    two dimension numpy array of homogeneous transformation matrix.
    array([[R00, R01, R02, T0],
           [R10, R11, R12, T1],
           [R20, R21, R22, T2],
           [0.,  0.,  0.,  1.]])
  """
  qw = quaternion[3]
  qx = quaternion[0]
  qy = quaternion[1]
  qz = quaternion[2]
  sqx = qx * qx
  sqy = qy * qy
  sqz = qz * qz
  m = np.zeros((4, 4), dtype=float)
  m[0, 0] = 1.0 - 2.0 * sqy - 2.0 * sqz
  m[0, 1] = 2.0 * qx * qy - 2.0 * qz * qw
  m[0, 2] = 2.0 * qx * qz + 2.0 * qy * qw
  m[1, 0] = 2.0 * qx * qy + 2.0 * qz * qw
  m[1, 1] = 1.0 - 2.0 * sqx - 2.0 * sqz
  m[1, 2] = 2.0 * qy * qz - 2.0 * qx * qw
  m[2, 0] = 2.0 * qx * qz - 2.0 * qy * qw
  m[2, 1] = 2.0 * qy * qz + 2.0 * qx * qw
  m[2, 2] = 1.0 - 2.0 * sqx - 2.0 * sqy
  m[0, 3] = translation[0]
  m[1, 3] = translation[1]
  m[2, 3] = translation[2]
  m[3, 3] = 1.0
  return m


def pos_quaternion_to_pose(translation: List[float],
                           quaternion: List[float]) -> np.ndarray:
  """Convert a translation-quaternion pair to a pose.

  A pose is a 6-element array. First three elements are the translations of the
  post, next three elements are the rotation of the pose in the axis-angle
  representation.

  Args:
    translation: translation [x, y, z]
    quaternion: rotation in the Unity coordinate system [x, y, z, w].

  Returns:
    equivalent pose.

  """
  return matrix_to_pose(pos_quaternion_to_matrix(translation, quaternion))


def unity_pos_quaternion_to_pose(translation: List[float],
                                 quaternion: List[float]) -> np.ndarray:
  """Converts an Unity translation-quaternion pair to a pose.

  A pose is a 6-element array. First three elements are the translations of the
  post, next three elements are the rotation of the pose in the axis-angle
  representation.

  Args:
    translation: translation [x, y, z]
    quaternion: rotation in the Unity coordinate system [x, y, z, w].

  Returns:
    equivalent pose.

  """
  real_to_unity = np.zeros((4, 4), dtype=float)
  real_to_unity[0, 0] = 1.0
  real_to_unity[1, 2] = 1.0
  real_to_unity[2, 1] = 1.0
  real_to_unity[3, 3] = 1.0
  robot_mat = pos_quaternion_to_matrix(translation, quaternion)
  m = np.matmul(np.matmul(real_to_unity, robot_mat), real_to_unity)
  return matrix_to_pose(m)


def get_z_direction(pose: np.ndarray) -> List[float]:
  """Takes a pose and returns a 3x1 vector of the transformed z axis.

  A pose is a 6-element array. First three elements are the translations of the
  post, next three elements are the rotation of the pose in the axis-angle
  representation.

  Args:
    pose: input pose.

  Returns:
    3x1 vector of the transformed z axis

  """
  m = pose_to_matrix(np.array(pose))
  origin = np.array([[0.0], [0.0], [0.0], [1.0]])
  z = np.array([[0.0], [0.0], [1.0], [1.0]])
  t_origin = np.matmul(m, origin)
  t_z = np.matmul(m, z)
  normal = (t_z - t_origin)[:3]
  normal = normal / np.linalg.norm(normal)
  return np.squeeze(normal)


def random_xy_offset_within_radius(radius: float) -> List[float]:
  """Generate a random 2D point within a circle.

  The bounding circle is centered at the origin with the provided radius.

  Args:
    radius: radius of the circle.

  Returns:
    6-element array with the first two elements representing the x,y position
    of the point.

  """
  rand_angle = 2 * np.pi * random.random()
  rand_r = radius * np.sqrt(random.random())
  x = rand_r * np.cos(rand_angle)
  y = rand_r * np.sin(rand_angle)
  return [x, y, 0., 0., 0., 0.]


def axis_angle_to_quaternion(rotation: ArrayOrList3) -> np.ndarray:
  """Converts a Rodrigues axis-angle rotation to a quaternion.

  Args:
    rotation: axis-angle rotation in [x,y,z]

  Returns:
    equivalent quaternion in [x,y,z,w]
  """
  r = Rotation.from_rotvec(rotation)
  return r.as_quat()


def quaternion_to_axis_angle(rotation: ArrayOrList4) -> np.ndarray:
  """Converts a quaternion to a Rodrgiues axis-angle representation.

  Args:
    rotation: the quaternion in [x,y,z,w]

  Returns:
    [x,y,z]. Angles are in radians.

  """
  r = Rotation.from_quat(rotation)
  return r.as_rotvec()


def ik_diff_angle(hint_angle: float,
                  solution_angle: float) -> Tuple[float, float]:
  """Compares the hint angle to the solution angle.

  Adjusts the solution angle by 2*pi if necessary, and returns a tuple of the
  difference and the updated solution angle.

  Args:
    hint_angle: the angle of ik hint examined.
    solution_angle: the angle of the solution examined.

  Returns:
    a tuple of the difference between the two angles and the updated
  solution angle.
  """
  diff_to_ik_fast = solution_angle - hint_angle
  if diff_to_ik_fast < -np.pi:
    solution_angle = solution_angle + 2.0 * np.pi
    return solution_angle, np.absolute(diff_to_ik_fast + 2.0 * np.pi)
  if diff_to_ik_fast > np.pi:
    solution_angle = solution_angle - 2.0 * np.pi
    return solution_angle, np.absolute(diff_to_ik_fast - 2.0 * np.pi)
  return solution_angle, np.absolute(diff_to_ik_fast)


def angular_distance(
    joints1: ArrayOrList,
    joints2: ArrayOrList,
    cyclic: bool = False) -> Union[float, Tuple[float, List[float]]]:
  """Computes the angular distance between two joint configurations.

  If cyclic is enabled, it will also search integer +/- 2*pi offsets of joint2
  joints, and returns it.

  Args:
    joints1: first joint configuration.
    joints2: second joint configuration.
    cyclic: True if cyclic is enabled.

  Returns:
    Angular distance and closest joints2 configuration when cyclic is enabled.
  """
  distance = 0.0
  if cyclic:
    new_j2: List[_FloatOrInt] = list(joints2)
    for i in range(len(joints1)):
      raw_dist = joints1[i] - joints2[i]
      while raw_dist > math.pi:
        new_j2[i] += math.tau  # math.tau is 2*math.pi
        raw_dist -= math.tau
      while raw_dist < -math.pi:
        new_j2[i] -= math.tau
        raw_dist += math.tau
      distance += math.fabs(raw_dist)
    return distance, new_j2
  else:
    for i in range(len(joints1)):
      raw_dist = joints1[i] - joints2[i]
      distance += math.fabs(raw_dist)
    return distance


def euler_to_axis_angle(roll: float, pitch: float, yaw: float) -> np.ndarray:
  """Converts Euler angle to Axis-angle format.

  Args:
    roll: rotation angle.
    pitch: up/down angle.
    yaw: left/right angle.

  Returns:
    Equivalent Axis-angle format.
  """
  r = Rotation.from_euler('xyz', [roll, pitch, yaw])
  return r.as_rotvec()


def inverse_quat(quat: np.ndarray) -> np.ndarray:
  """Calculates the inverse of a quaternion.

  Args:
    quat: quaternion in (x, y, z, w).

  Returns:
    Inverse quaternion in (x, y, z, w).
  """
  x = quat[0]
  y = quat[1]
  z = quat[2]
  w = quat[3]

  q_norm = np.linalg.norm(quat)
  return np.array([-x / q_norm, -y / q_norm, -z / q_norm, w / q_norm])


def quaternion_multiply(quat1: np.ndarray, quat2: np.ndarray) -> np.ndarray:
  """Multiplies two quaternions.

  Args:
    quat1: first quaternion in (x, y, z, w).
    quat2: second quaternion in (x, y, z, w).

  Returns:
    The multiplication of the two quaternions in (x, y, z, w).
  """
  x1 = quat1[0]
  y1 = quat1[1]
  z1 = quat1[2]
  w1 = quat1[3]

  x2 = quat2[0]
  y2 = quat2[1]
  z2 = quat2[2]
  w2 = quat2[3]

  quat_mult_x = x1 * w2 + w1 * x2 + y1 * z2 - z1 * y2
  quat_mult_y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
  quat_mult_z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
  quat_mult_w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2

  return np.array([quat_mult_x, quat_mult_y, quat_mult_z, quat_mult_w])
