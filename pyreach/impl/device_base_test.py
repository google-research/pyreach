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

"""Tests for device_base.py."""

from typing import List, Optional, TypeVar
import unittest

from pyreach import core
from pyreach.common.python import types_gen
from pyreach.impl import device_base

T = TypeVar("T")


class MockDeviceBase(device_base.DeviceBase):

  def __init__(self) -> None:
    super().__init__()
    self._run_called = False
    self._poll_called = False
    self._wait_output = False
    self._wait_output_closed = False
    self._on_start_called = False
    self._on_close_called = False
    self._messages: List[types_gen.DeviceData] = []
    self._key_value_key: Optional[device_base.KeyValueKey] = None
    self._key_value_value: Optional[str] = None

  def on_message(self, msg: types_gen.DeviceData) -> None:
    """Invoke when a device data message is received."""
    self._messages.append(msg)

  def on_start(self) -> None:
    self._on_start_called = True
    self.run(self._wait_runner)
    self.run(self._set_run_called, True)
    self.poll(1000000, self._set_poll_called, True)
    self.send_cmd(
        types_gen.CommandData(
            device_type="startup-test", data_type="ping", tag="test-tag"))

  def on_set_key_value(self, key: device_base.KeyValueKey, value: str) -> None:
    self._key_value_key = key
    self._key_value_value = value

  def on_close(self) -> None:
    self._on_close_called = True

  def _wait_runner(self) -> None:
    self._wait_output = self.wait(1000000)
    self._wait_output_closed = self.wait(1000000)

  def _set_run_called(self, value: bool) -> None:
    self._run_called = value

  def _set_poll_called(self, value: bool) -> bool:
    self._poll_called = value
    return False


class TestPyReachDeviceBase(unittest.TestCase):
  """Test the DeviceBase class."""

  def test_device_base(self) -> None:
    """Test with callbacks overridden."""
    command_data: List[types_gen.CommandData] = []

    def send_cmd(cmd: types_gen.CommandData) -> None:
      nonlocal command_data
      command_data.append(cmd)

    device = MockDeviceBase()
    self.assertRaises(
        core.PyReachError, device.send_cmd,
        types_gen.CommandData(
            device_type="startup-test", data_type="ping", tag="test-tag"))
    device.set_send_cmd(send_cmd)
    device.start()

    self.assertIsInstance(device.get_key_values(), set)
    self.assertEqual(len(device.get_key_values()), 0)

    device.enqueue_device_data(
        types_gen.DeviceData(
            device_type="startup-test", data_type="cmd-status"))

    device.enqueue_device_data(
        types_gen.DeviceData(
            device_type="robot",
            device_name="test",
            data_type="key-value",
            key="robot_constraints.json",
            value="{}"))

    device.close()

    self.assertTrue(device._poll_called)
    self.assertTrue(device._run_called)
    self.assertTrue(device._wait_output)
    self.assertTrue(device._wait_output_closed)
    self.assertTrue(device.is_closed())
    self.assertTrue(device._on_close_called)
    self.assertTrue(device._on_start_called)

    self.assertEqual(
        device.get_key_value(
            device_base.KeyValueKey("robot", "test", "robot_constraints.json")),
        "{}")

    self.assertEqual(
        device._key_value_key,
        device_base.KeyValueKey("robot", "test", "robot_constraints.json"))
    self.assertEqual(device._key_value_value, "{}")

    self.assertEqual(len(command_data), 1)
    self.assertEqual(command_data[0].device_type, "startup-test")
    self.assertEqual(command_data[0].data_type, "ping")

  def test_device_base_no_callbacks(self) -> None:
    """Test without overriding callbacks."""
    command_data: List[types_gen.CommandData] = []

    def send_cmd(cmd: types_gen.CommandData) -> None:
      nonlocal command_data
      command_data.append(cmd)

    device = device_base.DeviceBase()
    self.assertRaises(
        core.PyReachError, device.send_cmd,
        types_gen.CommandData(
            device_type="startup-test", data_type="ping", tag="test-tag"))
    device.set_send_cmd(send_cmd)
    device.start()

    self.assertIsInstance(device.get_key_values(), set)
    self.assertEqual(len(device.get_key_values()), 0)

    device.send_cmd(
        types_gen.CommandData(
            device_type="startup-test", data_type="ping", tag="test-tag"))

    device.enqueue_device_data(
        types_gen.DeviceData(
            device_type="startup-test", data_type="cmd-status"))

    device.enqueue_device_data(
        types_gen.DeviceData(
            device_type="robot",
            device_name="test",
            data_type="key-value",
            key="robot_constraints.json",
            value="{}"))

    device.close()

    self.assertTrue(device.is_closed())
    self.assertEqual(
        device.get_key_value(
            device_base.KeyValueKey("robot", "test", "robot_constraints.json")),
        "{}")

    self.assertEqual(len(command_data), 1)
    self.assertEqual(command_data[0].device_type, "startup-test")
    self.assertEqual(command_data[0].data_type, "ping")


if __name__ == "__main__":
  unittest.main()
