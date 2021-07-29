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

import unittest
import numpy as np  # type: ignore
from pyreach.ik_pybullet import ik_pybullet


class IkPybulletTest(unittest.TestCase):

  def test_ikpybullet_xarm6(self) -> None:
    resolver = ik_pybullet.IKPybullet()
    tranlation_tolerance = 1e-3
    rad_tolerance = 0.035
    num_start_poses = 10

    np.random.seed(0)
    for _ in range(num_start_poses):
      joints = np.random.randn(6)

      pose = resolver.fk(joints)
      target_joints = resolver.ik_search(pose, joints)
      target_pose = resolver.fk(target_joints)
      translation_error = np.linalg.norm(pose[0:3] - target_pose[0:3])
      rotation_error = np.linalg.norm(pose[3:] - target_pose[3:])

      self.assertIsNotNone(joints)
      self.assertIsNotNone(target_joints)

      self.assertTrue(np.allclose(joints, target_joints, atol=2e-3))
      self.assertLess(translation_error, tranlation_tolerance)
      self.assertLess(rotation_error, rad_tolerance)


if __name__ == "__main__":
  unittest.main()
