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
"""Tests for utils.py."""

from typing import Optional
import unittest

from pyreach import constraints
from pyreach.common.python import types_gen
from pyreach.impl import constraints_impl as impl
from pyreach.impl import test_data


class TestConstraintsImpl(unittest.TestCase):

  def test_constraints_impl(self) -> None:
    constraints_device = impl.ConstraintsDevice()
    try:
      constraints_device.start()
      self.assertIsNone(constraints_device.get())
      constraints_device.enqueue_device_data(
          types_gen.DeviceData(
              device_type="settings-engine",
              data_type="key-value",
              key="workcell_constraints.json",
              value=test_data.get_workcell_constraints_json()))
      constraints_device.wait(1)

      cs: Optional[impl.ConstraintsImpl] = constraints_device.get()
      self.assertIsNotNone(cs)
      assert cs
      self.assertIsNone(cs.get_joint_limits(""))
      interactables = cs.get_interactables()
      self.assertEqual(len(interactables), 2)
      self.assertEqual(interactables[0].name, "LeftBox")
      left_geometry = interactables[0].geometry
      self.assertIsInstance(left_geometry, constraints.Box)
      assert isinstance(left_geometry, constraints.Box)
      self.assertEqual(left_geometry.pose.as_tuple(),
                       (-0.246944084763527, -0.705296516418457,
                        -0.168291628360748, 0.0, 0.0, 0.0))
      self.assertEqual(
          left_geometry.scale.as_tuple(),
          (0.379999995231628, 0.259999990463257, 0.200000002980232))

      self.assertEqual(interactables[1].name, "RightBox")
      right_geometry = interactables[1].geometry
      self.assertIsInstance(right_geometry, constraints.Box)
      assert isinstance(right_geometry, constraints.Box)
      self.assertEqual(right_geometry.pose.as_tuple(),
                       (0.254177570343018, -0.711709439754486,
                        -0.174813330173492, -6.585575275907331e-05,
                        -0.006104793682704136, -0.021574200980967757))
      self.assertEqual(
          right_geometry.scale.as_tuple(),
          (0.370000004768372, 0.300000011920929, 0.200000002980232))

    finally:
      constraints_device.close()

  def test_robot_constraints_impl(self) -> None:
    constraints_device = impl.ConstraintsDevice("")
    try:
      constraints_device.start()
      self.assertIsNone(constraints_device.get())
      constraints_device.enqueue_device_data(
          types_gen.DeviceData(
              device_type="settings-engine",
              data_type="key-value",
              key="workcell_constraints.json",
              value=test_data.get_workcell_constraints_json()))
      self.assertIsNone(constraints_device.get())
      constraints_device.enqueue_device_data(
          types_gen.DeviceData(
              device_type="robot",
              data_type="key-value",
              key="robot_constraints.json",
              value=test_data.get_robot_constraints_json()))
      constraints_device.wait(1)

      cs: Optional[impl.ConstraintsImpl] = constraints_device.get()
      self.assertIsNotNone(cs)
      assert cs
      joints = cs.get_joint_limits("")
      self.assertIsNotNone(joints)
      assert joints is not None
      self.assertEqual(len(joints), 6)
      self.assertEqual(joints[0].min, -6.335545214359173)
      self.assertEqual(joints[0].max, 6.335545187179586)
      self.assertEqual(joints[1].min, -6.335545214359173)
      self.assertEqual(joints[1].max, 6.335545187179586)
      self.assertEqual(joints[2].min, -6.335545214359173)
      self.assertEqual(joints[2].max, 6.335545187179586)
      self.assertEqual(joints[3].min, -6.335545214359173)
      self.assertEqual(joints[3].max, 6.335545187179586)
      self.assertEqual(joints[4].min, -6.335545214359173)
      self.assertEqual(joints[4].max, 6.335545187179586)
      self.assertEqual(joints[5].min, -6.335545214359173)
      self.assertEqual(joints[5].max, 6.335545187179586)
      self.assertEqual(len(cs.get_interactables()), 2)
    finally:
      constraints_device.close()


if __name__ == "__main__":
  unittest.main()
