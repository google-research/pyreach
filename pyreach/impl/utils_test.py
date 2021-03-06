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

import unittest

from pyreach import core
from pyreach.common.python import types_gen
from pyreach.impl import test_utils
from pyreach.impl import utils


class UtilsTest(unittest.TestCase):

  def test_time_at_timestamp(self) -> None:
    self.assertEqual(utils.time_at_timestamp(100), 0.1)

  def test_timestamp_at_time(self) -> None:
    self.assertEqual(utils.timestamp_at_time(0.1), 100)

  def test_generate_tag(self) -> None:
    self.assertIsNotNone(utils.generate_tag())

  def test_data_copy(self) -> None:

    def copy_test(data: types_gen.DeviceData) -> None:
      self.assertTrue(
          test_utils.device_data_equal(data, utils.copy_device_data(data)))

    copy_test(
        utils.ImagedDeviceData(
            ts=1,
            seq=1,
            device_type="depth-camera",
            data_type="color-depth",
            color_image=bytes([1, 2]),
            depth_image=bytes([3, 4])))
    copy_test(
        types_gen.DeviceData(
            ts=1, seq=1, device_type="robot", data_type="robot-state"))

  def test_proto_loop(self) -> None:

    def proto_loop_test(data: types_gen.DeviceData) -> None:
      loop = utils.ImagedDeviceData.from_proto(data.to_proto())
      assert loop is not None
      self.assertTrue(test_utils.device_data_equal(data, loop))

    proto_loop_test(
        utils.ImagedDeviceData(
            ts=1,
            seq=1,
            device_type="depth-camera",
            data_type="color-depth",
            color="test_color.jpg",
            depth="test_depth.pgm",
            color_image=bytes([1, 2]),
            depth_image=bytes([3, 4])))
    proto_loop_test(
        utils.ImagedDeviceData(
            ts=1,
            seq=1,
            device_type="color-camera",
            data_type="color",
            color="test_color.jpg",
            color_image=bytes([1, 2])))
    proto_loop_test(
        utils.ImagedDeviceData(
            ts=1,
            seq=1,
            device_type="oracle",
            device_name="pick-points",
            data_type="prediction",
            color="test_color.jpg",
            color_image=bytes([1, 2])))
    proto_loop_test(
        utils.ImagedDeviceData(
            ts=1, seq=1, device_type="robot", data_type="robot-state"))

  def test_color_image_loader(self) -> None:

    def read_file(fn: str) -> bytes:
      with open(fn, "rb") as f:
        return f.read()

    for data_type, filename in [
        ("prediction", "test_images/oracle-pick-points/color.jpg"),
        ("color", "test_images/uvc/color.jpg"),
        ("color", "test_images/vnc/color.jpg"),
        ("color", "test_images/realsense_invoice/color.jpg"),
        ("color-depth", "test_images/photoneo/color.jpg"),
        ("color-depth", "test_images/realsense/color.jpg"),
    ]:
      for source in [
          types_gen.DeviceData(
              ts=1,
              device_type="test-type",
              device_name="test-name",
              data_type=data_type),
          utils.ImagedDeviceData(
              ts=1,
              device_type="test-type",
              device_name="test-name",
              data_type=data_type),
          utils.ImagedDeviceData(
              ts=1,
              device_type="test-type",
              device_name="test-name",
              data_type=data_type,
              color=test_utils.get_test_image_file(filename) + "invalid",
              color_image=b"12"),
          utils.ImagedDeviceData(
              ts=1,
              device_type="test-type",
              device_name="test-name",
              data_type=data_type,
              color_image=read_file(test_utils.get_test_image_file(filename))),
      ]:
        self.assertRaises(FileNotFoundError, utils.load_color_image_from_data,
                          source)
        self.assertRaises(FileNotFoundError, utils.load_color_image_from_data,
                          source.to_proto())
        loop = utils.ImagedDeviceData.from_proto(source.to_proto())
        assert loop
        self.assertRaises(FileNotFoundError, utils.load_color_image_from_data,
                          loop)
        self.assertRaises(FileNotFoundError, utils.load_color_image_from_data,
                          loop.to_proto())
      for source in [
          types_gen.DeviceData(
              ts=1,
              device_type="test-type",
              device_name="test-name",
              data_type=data_type,
              color=test_utils.get_test_image_file(filename)),
          utils.ImagedDeviceData(
              ts=1,
              device_type="test-type",
              device_name="test-name",
              data_type=data_type,
              color=test_utils.get_test_image_file(filename)),
          utils.ImagedDeviceData(
              ts=1,
              device_type="test-type",
              device_name="test-name",
              data_type=data_type,
              color=test_utils.get_test_image_file(filename),
              color_image=read_file(test_utils.get_test_image_file(filename))),
      ]:
        test_utils.assert_image_equal(
            utils.load_color_image_from_data(source), filename)
        test_utils.assert_image_equal(
            utils.load_color_image_from_data(source.to_proto()), filename)
        loop = utils.ImagedDeviceData.from_proto(source.to_proto())
        assert loop
        test_utils.assert_image_equal(
            utils.load_color_image_from_data(loop), filename)
        test_utils.assert_image_equal(
            utils.load_color_image_from_data(loop.to_proto()), filename)

  def test_depth_image_loader(self) -> None:

    def read_file(fn: str) -> bytes:
      with open(fn, "rb") as f:
        return f.read()

    for data_type, filename in [
        ("color-depth", "test_images/photoneo/depth.pgm"),
        ("color-depth", "test_images/realsense/depth.pgm"),
    ]:
      for source in [
          types_gen.DeviceData(
              ts=1,
              device_type="test-type",
              device_name="test-name",
              data_type=data_type),
          utils.ImagedDeviceData(
              ts=1,
              device_type="test-type",
              device_name="test-name",
              data_type=data_type),
          utils.ImagedDeviceData(
              ts=1,
              device_type="test-type",
              device_name="test-name",
              data_type=data_type,
              depth_image=read_file(test_utils.get_test_image_file(filename))),
      ]:
        self.assertRaises(FileNotFoundError, utils.load_depth_image_from_data,
                          source)
        self.assertRaises(FileNotFoundError, utils.load_depth_image_from_data,
                          source.to_proto())
        loop = utils.ImagedDeviceData.from_proto(source.to_proto())
        assert loop
        self.assertRaises(FileNotFoundError, utils.load_depth_image_from_data,
                          loop)
        self.assertRaises(FileNotFoundError, utils.load_depth_image_from_data,
                          loop.to_proto())
      for source in [
          types_gen.DeviceData(
              ts=1,
              device_type="test-type",
              device_name="test-name",
              data_type=data_type,
              depth=test_utils.get_test_image_file(filename)),
          utils.ImagedDeviceData(
              ts=1,
              device_type="test-type",
              device_name="test-name",
              data_type=data_type,
              depth=test_utils.get_test_image_file(filename)),
          utils.ImagedDeviceData(
              ts=1,
              device_type="test-type",
              device_name="test-name",
              data_type=data_type,
              depth=test_utils.get_test_image_file(filename),
              depth_image=read_file(test_utils.get_test_image_file(filename))),
      ]:
        test_utils.assert_image_depth_equal(
            utils.load_depth_image_from_data(source), filename)
        test_utils.assert_image_depth_equal(
            utils.load_depth_image_from_data(source.to_proto()), filename)
        loop = utils.ImagedDeviceData.from_proto(source.to_proto())
        assert loop
        test_utils.assert_image_depth_equal(
            utils.load_depth_image_from_data(loop), filename)
        test_utils.assert_image_depth_equal(
            utils.load_depth_image_from_data(loop.to_proto()), filename)

  def test_command_copy(self) -> None:

    def copy_test(data: types_gen.CommandData) -> None:
      self.assertTrue(
          test_utils.command_data_equal(data, utils.copy_command_data(data)))

    copy_test(
        types_gen.CommandData(
            ts=1, seq=1, device_type="robot", data_type="reach-script"))

  def test_pyreach_status_from_message(self) -> None:
    device_data = types_gen.DeviceData()
    device_data.ts = 12000
    device_data.status = "done"
    device_data.script = "ur"
    device_data.error = "error"
    device_data.progress = 0.2
    device_data.message = "error message"
    device_data.code = 1

    status = utils.pyreach_status_from_message(device_data)
    self.assertEqual(status.time, 12)
    self.assertEqual(status.status, "done")
    self.assertEqual(status.script, "ur")
    self.assertEqual(status.error, "error")
    self.assertEqual(status.progress, 0.2)
    self.assertEqual(status.message, "error message")
    self.assertEqual(status.code, 1)

  def convert_pyreach_status(self) -> None:
    converted = utils.convert_pyreach_status(
        core.PyReachStatus(
            time=1.0,
            sequence=2,
            status="test-status",
            script="test-script",
            error="test-error",
            progress=3.0,
            message="test-message",
            code=4))
    self.assertIsInstance(converted, types_gen.Status)
    self.assertEqual(converted.status, "test-status")
    self.assertEqual(converted.script, "test-script")
    self.assertEqual(converted.error, "test-error")
    self.assertEqual(converted.progress, 3.0)
    self.assertEqual(converted.message, "test-message")
    self.assertEqual(converted.code, 4)

  def reverse_pyreach_status(self) -> None:
    converted = utils.reverse_pyreach_status(
        types_gen.Status(
            status="test-status",
            script="test-script",
            error="test-error",
            progress=3.0,
            message="test-message",
            code=4),
        timestamp=1.0,
        sequence=2)
    self.assertIsInstance(converted, core.PyReachStatus)
    self.assertEqual(converted.time, 1.0)
    self.assertEqual(converted.sequence, 2)
    self.assertEqual(converted.status, "test-status")
    self.assertEqual(converted.script, "test-script")
    self.assertEqual(converted.error, "test-error")
    self.assertEqual(converted.progress, 3.0)
    self.assertEqual(converted.message, "test-message")
    self.assertEqual(converted.code, 4)
    converted = utils.reverse_pyreach_status(
        types_gen.Status(
            status="test-1-status",
            script="test-1-script",
            error="test-1-error",
            progress=5.0,
            message="test-1-message",
            code=6))
    self.assertIsInstance(converted, core.PyReachStatus)
    self.assertEqual(converted.time, 0.0)
    self.assertEqual(converted.sequence, 0)
    self.assertEqual(converted.status, "test-1-status")
    self.assertEqual(converted.script, "test-1-script")
    self.assertEqual(converted.error, "test-1-error")
    self.assertEqual(converted.progress, 5.0)
    self.assertEqual(converted.message, "test-1-message")
    self.assertEqual(converted.code, 6)

  def quaternion_almost_equal(self, quaternion1: core.Quaternion,
                              quaternion2: core.Quaternion) -> None:
    """Check if two quaternions are almost the same."""
    self.assertAlmostEqual(quaternion1.x, quaternion2.x)
    self.assertAlmostEqual(quaternion1.y, quaternion2.y)
    self.assertAlmostEqual(quaternion1.z, quaternion2.z)
    self.assertAlmostEqual(quaternion1.w, quaternion2.w)

  def axis_angle_almost_equal(self, axis_angle1: core.AxisAngle,
                              axis_angle2: core.AxisAngle) -> None:
    """Check if two axis-angles are almost the same."""
    self.assertAlmostEqual(axis_angle1.rx, axis_angle2.rx)
    self.assertAlmostEqual(axis_angle1.ry, axis_angle2.ry)
    self.assertAlmostEqual(axis_angle1.rz, axis_angle2.rz)

  def test_rotation_conversion(self) -> None:
    expect_quaternion = core.Quaternion(
        x=0.049708843324859475,
        y=0.09941768664971895,
        z=0.14912652997457843,
        w=0.9825509821552589)
    axis_angle = core.AxisAngle(0.1, 0.2, 0.3)
    axis_angle_rotation = core.Rotation(axis_angle)
    self.axis_angle_almost_equal(axis_angle_rotation.axis_angle, axis_angle)
    quaternion = axis_angle_rotation.quaternion
    quaternion_rotation = core.Rotation(quaternion)
    self.quaternion_almost_equal(quaternion_rotation.quaternion, quaternion)
    self.axis_angle_almost_equal(quaternion_rotation.axis_angle, axis_angle)
    back_axis_angle = quaternion_rotation.axis_angle
    self.axis_angle_almost_equal(back_axis_angle, axis_angle)
    self.axis_angle_almost_equal(
        core.Rotation(back_axis_angle).axis_angle, axis_angle)
    self.quaternion_almost_equal(
        core.Rotation(back_axis_angle).quaternion, expect_quaternion)


if __name__ == "__main__":
  unittest.main()
