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
r"""Tests for transform_util.
"""

import json
import math
from typing import List, Tuple
import unittest

import numpy as np  # type: ignore

from pyreach.common.base import transform_util
from pyreach.common.base.transform_util import ZERO_VECTOR3

PI_2 = np.pi / 2.0

INTRINSICS_VEC = [2, 3, 4, 5]
INTRINSICS_MAT = [[INTRINSICS_VEC[0], 0, INTRINSICS_VEC[2]],
                  [0, INTRINSICS_VEC[1], INTRINSICS_VEC[3]], [0, 0, 1]]

CALIBRATION_PARAMS_JSON = ('{"distortion": [0.0868454530527644, '
                           '-0.041556557071665, -0.0036213716513449996, '
                           '-0.002464057758741828, 0.009632712012404352], '
                           '"distortionDepth": [0, 0.0001, 0, 0, 0, 0, 0, 0], '
                           '"extrinsics": [0.771388657109181, '
                           '0.17577610571716462, 0.15234885843422027, '
                           '-2.123275042042772, -1.0424501266418418, '
                           '0.5194726200971432], "extrinsicsResidual": '
                           '0.38495038660108105, "height": 720, "intrinsics": '
                           '[610.8792086394648, 609.0695965301111, '
                           '634.6380135355435, 360.95356629834873], '
                           '"intrinsicsResidual": 1.0650387279125357, '
                           '"lensModel": "pinhole", "width": 1280}')


class TransformTest(unittest.TestCase):

  def test_identity(self) -> None:
    """Test identity transform."""
    for pnt in np.array([[0, 0, 0], [1, 1, 1], [-1, -1, -1]], np.float64):
      pnt_t = transform_util.transform(pnt, ZERO_VECTOR3, ZERO_VECTOR3)
      self.assertLess(np.abs(pnt.reshape(3, 1) - pnt_t).max(), 1e-7)

  def test_translation(self) -> None:
    """Test simple translations."""
    for pnt in np.array([[0, 0, 0], [1, 1, 1], [-1, -1, -1]], np.float64):
      for trans in np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 1, 1]],
                            np.float64):
        pnt_t = transform_util.transform(pnt, trans, ZERO_VECTOR3)
        self.assertLess(np.abs((pnt + trans).reshape(3, 1) - pnt_t).max(), 1e-7)

  def test_rotation(self) -> None:
    """Test simple 90deg rotations."""
    pnt = np.array([1, 1, 1], np.float64)
    rot_vals = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], np.float64) * PI_2
    pnt_t_vals = np.array([[1, -1, 1], [1, 1, -1], [-1, 1, 1]], np.float64)
    for (rot, pnt_t_expected) in zip(rot_vals, pnt_t_vals):
      pnt_t = transform_util.transform(pnt, ZERO_VECTOR3, rot)
      self.assertLess(np.abs(pnt_t_expected.reshape(3, 1) - pnt_t).max(), 1e-7)

  def test_transform_inv(self) -> None:
    pnt = np.array([1, 1, 1], np.float64)
    trans = np.array([-1, 0.25, -0.5], np.float64)
    rot = np.array([-0.5, 0.25, 1.0], np.float64)
    pnt_t = transform_util.transform(pnt, trans, rot)
    self.assertGreater(np.linalg.norm(pnt - pnt_t), 1e-2)
    pnt_t_t = transform_util.transform_inv(pnt_t, trans, rot)
    self.assertLess(np.abs(pnt - pnt_t_t).max(), 1e-6)


class IntrinsicsTest(unittest.TestCase):

  def test_intrinsics_to_matrix(self) -> None:
    self.assertTrue(
        np.all(
            np.array(INTRINSICS_MAT) == transform_util.intrinsics_to_matrix(
                INTRINSICS_VEC)))

  def test_intrinsics_to_list(self) -> None:
    self.assertEqual(
        tuple(INTRINSICS_VEC),
        tuple(transform_util.intrinsics_to_list(np.array(INTRINSICS_MAT))))


class ProjectionTest(unittest.TestCase):

  @staticmethod
  def _load_cal_params() -> Tuple[np.ndarray, np.ndarray, np.ndarray, int, int]:
    cal_params = json.loads(CALIBRATION_PARAMS_JSON)
    intrinsics = transform_util.intrinsics_to_matrix(cal_params['intrinsics'])
    distortion = np.array(cal_params['distortion'])
    distortion_depth = np.array(cal_params['distortionDepth'])
    height = cal_params['height']
    width = cal_params['width']
    return intrinsics, distortion, distortion_depth, height, width

  def test_project2int(self) -> None:
    """Test simple projection (with identity extrinsics)."""
    intrinsics, distortion, _, _, _ = self._load_cal_params()

    def proj(p: Tuple[int, int, int]) -> np.ndarray:
      return transform_util.project_2d_int(
          p=p,
          extrinsics=np.zeros((6)),
          intrinsics=intrinsics,
          distortion=distortion,
          clip_range=1000)

    self.assertIsNone(proj((0, 0, -1)))  # Behind the camera.
    self.assertIsNone(proj((100, 0, 1)))  # Off the frame (clip range).
    self.assertIsNone(proj((-100, 0, 1)))  # Off the frame (clip range).
    self.assertIsNone(proj((0, 100, 1)))  # Off the frame (clip range).
    self.assertIsNone(proj((0, -100, 1)))  # Off the frame (clip range).

    proj_pix = proj((0, 0, 1))
    self.assertIs(type(proj_pix), tuple)
    self.assertEqual(len(proj_pix), 2)

  def test_project(self) -> None:
    """Test simple projection (with identity extrinsics)."""
    intrinsics, distortion, _, _, _ = self._load_cal_params()

    def proj(p: Tuple[int, int, int]) -> np.ndarray:
      return transform_util.project(
          p=np.array(p, np.float64).reshape((1, 1, 3)),
          extrinsics=np.zeros(6),
          intrinsics=intrinsics,
          distortion=distortion)

    proj_pix = proj((0, 0, 1))
    self.assertIs(type(proj_pix), np.ndarray)
    self.assertEqual(proj_pix.shape, (1, 1, 2))

  def test_unproject_depth_sample(self) -> None:
    """Test simple unprojection."""
    intrinsics, distortion, distortion_depth, _, _ = self._load_cal_params()

    xyz = transform_util.unproject_depth_sample((1, 1), 0, distortion_depth,
                                                intrinsics, distortion)
    self.assertIs(type(xyz), np.ndarray)
    self.assertEqual(xyz.shape, (1, 3))
    # Check that 0 depth maps to (0, 0, 0).
    self.assertLess(np.abs(xyz).max(), 1e-6)

    xyz = transform_util.unproject_depth_sample((1, 1), 1, distortion_depth,
                                                intrinsics, distortion)
    # Should be in front of the camera.
    self.assertGreater(xyz[0, 2], 0)

  def test_unproject_depth_vectorized(self) -> None:
    """Test simple depth image unprojection."""
    intrinsics, distortion, distortion_depth, _, _ = self._load_cal_params()

    for width, height in [(11, 7), (1, 1)]:
      height = 7
      width = 11
      im_depth = np.random.rand(height, width)
      im_depth[0, 0] = 0  # Add in an invalid depth.

      im_xyz = transform_util.unproject_depth_vectorized(im_depth,
                                                         distortion_depth,
                                                         intrinsics,
                                                         distortion)
      self.assertIs(type(im_xyz), np.ndarray)
      self.assertEqual(im_xyz.shape, (height * width, 3))
      # Check that 0 depth maps to (0, 0, 0).
      self.assertLess(np.abs(im_xyz[0, :]).max(), 1e-6)

      # Check consistency with the single sample version.
      im_xyz = im_xyz.reshape(height, width, 3)
      for v in range(height):
        for u in range(width):
          xyz = transform_util.unproject_depth_sample(
              (u, v), im_depth[v, u], distortion_depth, intrinsics, distortion)
          self.assertLess(np.linalg.norm(xyz - im_xyz[v, u, :]), 1e-6)

  def test_unproject_depth_sample_vectorized(self) -> None:
    """Test simple unprojection."""
    (intrinsics, distortion, distortion_depth, height,
     width) = self._load_cal_params()
    npnts = 11
    uvs = np.stack([np.random.randint(low=0, high=width, size=(npnts,)),
                    np.random.randint(low=0, high=height, size=(npnts,))],
                   axis=1).astype(np.float64)
    depths = np.random.rand(npnts) * 1000.00
    depths[0] = 0  # Add in an invalid depth.

    xyz = transform_util.unproject_depth_sample_vectorized(
        uvs, depths, distortion_depth, intrinsics, distortion)
    self.assertIs(type(xyz), np.ndarray)
    self.assertEqual(xyz.shape, (npnts, 3))
    # Check that 0 depth maps to (0, 0, 0).
    self.assertLess(np.abs(xyz[0]).max(), 1e-6)

    # Check against non-vectorized version.
    for ipnt in range(npnts):
      cur_xyz = transform_util.unproject_depth_sample(
          uvs[ipnt], depths[ipnt], distortion_depth, intrinsics, distortion)
      self.assertLess(np.abs(cur_xyz - xyz[ipnt]).max(), 1e-6)


class ConversionTest(unittest.TestCase):

  @staticmethod
  def _get_random_pose() -> List[float]:
    pose = [.0, .0, .0, .0, .0, .0]
    pose[0:3] = np.random.random(3) - 0.5
    axis_angle = np.random.random(3) - 0.5
    old_angle = np.linalg.norm(axis_angle)
    new_angle = (np.random.random() - 0.5) * math.pi
    pose[3:] = axis_angle * new_angle / old_angle
    return pose

  def test_pose_matrix_conversion(self) -> None:
    pose = self._get_random_pose()
    m = transform_util.pose_to_matrix(pose)
    pose2 = transform_util.matrix_to_pose(m)
    self.assertTrue(np.allclose(pose, pose2))

  def test_pose_inversion(self) -> None:
    pose = self._get_random_pose()
    inverted_pose = transform_util.inverse_pose(pose)
    result = transform_util.multiply_pose(pose, inverted_pose)
    self.assertTrue(np.allclose(np.zeros(6), result))

  def test_quaternion_conversion(self) -> None:
    unit_vector_z = [0., 0., 1.]
    x_90degree_quaternion = [math.sqrt(2) / 2, 0, 0, math.sqrt(2) / 2]
    x_90degree_pose = transform_util.unity_pos_quaternion_to_pose(
        unit_vector_z, x_90degree_quaternion)
    self.assertTrue(np.allclose([0., 1., 0.], x_90degree_pose[:3]))
    self.assertTrue(np.allclose([-math.pi / 2, 0., 0.], x_90degree_pose[3:]))

  def test_angular_mod_pose(self) -> None:
    pose = np.array(self._get_random_pose())
    axis_angle = pose[3:]
    angle = np.linalg.norm(axis_angle)
    angle_plus_2pi = pose
    new_axis_angle = axis_angle * ((angle + 2. * math.pi) / angle)
    angle_plus_2pi[3:] = new_axis_angle
    angle_plus_2pi_mod = transform_util.angular_mod_pose(angle_plus_2pi)
    self.assertTrue(np.allclose(pose, angle_plus_2pi_mod))

  def test_transform_between_two_vectors(self) -> None:
    translation1 = np.array([1., 1., 1.])
    unit_vector_y = np.array([0., 1., 0.])
    translation2 = np.array([2., 2., 2.])
    unit_vector_z = np.array([0., 0., 1.])
    transform = transform_util.transform_between_two_vectors(
        translation1, unit_vector_y, translation2, unit_vector_z)
    expected_transform = [1, 1, 1, math.pi / 2, 0, 0]
    self.assertTrue(np.allclose(transform, expected_transform))

  def test_transform_between_two_vectors_degenerate(self) -> None:
    # Both vectors have the same direction.
    translation1 = np.array([1., 1., 1.])
    translation2 = np.array([2., 2., 2.])
    unit_vector_x = np.array([1., 0., 0.])
    unit_vector_y = np.array([0., 1., 0.])
    unit_vector_z = np.array([0., 0., 1.])
    expected_transform = [1, 1, 1, 0, 0, 0]

    transform = transform_util.transform_between_two_vectors(
        translation1, unit_vector_x, translation2, unit_vector_x)
    self.assertTrue(np.allclose(transform, expected_transform))

    transform = transform_util.transform_between_two_vectors(
        translation1, unit_vector_y, translation2, unit_vector_y)
    self.assertTrue(np.allclose(transform, expected_transform))

    transform = transform_util.transform_between_two_vectors(
        translation1, unit_vector_z, translation2, unit_vector_z)
    self.assertTrue(np.allclose(transform, expected_transform))

  def test_raycast_into_depth_image(self) -> None:
    # Solid wall 1 meter in front of the depth camera.
    depth_img = np.ones([1000, 1000]) * 10000

    # Camera parameters.
    intrinsics = transform_util.intrinsics_to_matrix([615., 613., 638., 369.])
    distortion = np.array([0., 0., 0., 0., 0.])
    distortion_depth = np.array([0., 0.0001, 0., 0., 0., 0., 0., 0.])
    extrinsics = np.array([0.20, -0.73, 0.55, -2.91, 0., 0.])

    # Viewing from (0, -1, 1) and looking straight down the z-axis.
    origin = [0., -1., 1.]
    direction = [0., 0., -1.]
    direction /= np.linalg.norm(direction)

    raycast = transform_util.raycast_into_depth_image(origin, direction,
                                                      depth_img, intrinsics,
                                                      distortion,
                                                      distortion_depth,
                                                      extrinsics)
    if raycast is None:
      self.fail('raycast was None')
      return
    point, normal = raycast
    expected_point = [0., -0.999031368, -0.540874302]
    expected_normal = [0, -0.229527947, 0.97330207]
    self.assertTrue(np.allclose(expected_point, point))
    self.assertTrue(np.allclose(expected_normal, normal))

  def test_is_point_in_rectangle(self) -> None:
    rectangle = [10, 20, 30, 40]
    self.assertFalse(transform_util.is_point_in_rectangle(None, rectangle))
    self.assertTrue(transform_util.is_point_in_rectangle((20, 30), rectangle))
    self.assertFalse(transform_util.is_point_in_rectangle((0, 0), rectangle))

  def test_pose_quaternion_to_pose(self) -> None:
    unit_vector_z = [0., 0., 1.]
    x_90degree_quaternion = [math.sqrt(2) / 2, 0, 0, math.sqrt(2) / 2]
    x_90degree_pose = transform_util.pos_quaternion_to_pose(
        unit_vector_z, x_90degree_quaternion)
    self.assertTrue(np.allclose([0., 0., 1.], x_90degree_pose[:3]))
    self.assertTrue(np.allclose([math.pi / 2, 0., 0.], x_90degree_pose[3:]))

  def test_get_z_direction(self) -> None:
    pose = [1., 1., 1., 0., 0., 1.]
    z_direction = transform_util.get_z_direction(pose)
    self.assertTrue(np.allclose([0, 0, 1], z_direction))

  def test_random_xy_offset_within_radius(self) -> None:
    pose = transform_util.random_xy_offset_within_radius(2)
    self.assertEqual(len(pose), 6)
    x = pose[0]
    y = pose[1]
    self.assertLessEqual(x * x + y * y, 4)
    self.assertEqual(pose[2:], [0, 0, 0, 0])

  def test_axis_angle_to_quaternion(self) -> None:
    axis_angle = [0, 0, 0]
    quaternion = transform_util.axis_angle_to_quaternion(axis_angle)
    self.assertTrue(np.allclose([0, 0, 0, 1], quaternion))

  def test_quaternion_to_axis_angle(self) -> None:
    quaternion = [0, 0, 0, 1]
    axis_angle = transform_util.quaternion_to_axis_angle(quaternion)
    self.assertTrue(np.allclose([0, 0, 0], axis_angle))


class UtilTest(unittest.TestCase):

  def test_angular_distance(self) -> None:
    joints1 = [0., 1., 2.]
    joints2 = [1., 2., 3.]
    distance = transform_util.angular_distance(joints1, joints2)
    assert isinstance(distance, float)
    self.assertAlmostEqual(distance, 3)

  def test_euler_to_axis_angle(self) -> None:
    axis_angle = transform_util.euler_to_axis_angle(1., 1., 1.)
    self.assertTrue(np.allclose([0.3611812, 1.23098623, 0.3611812], axis_angle))


if __name__ == '__main__':
  unittest.main()
