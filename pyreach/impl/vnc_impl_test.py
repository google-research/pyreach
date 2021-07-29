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

from typing import List
import unittest

from pyreach import core  # pylint: disable=unused-import
from pyreach import vnc
from pyreach.common.python import types_gen
from pyreach.impl import test_utils
from pyreach.impl import thread_util
from pyreach.impl import vnc_impl


class TestPyReachVNCImpl(unittest.TestCase):

  def test_test_vnc(self) -> None:
    test_vnc = TestVNC("test-type", "test-name")
    test_utils.run_test_client_test([test_vnc], [
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1,
                device_type="test-type",
                device_name="test-name",
                tag="test-tag",
                data_type="pointer-event"), (types_gen.DeviceData(
                    ts=1,
                    tag="test-tag",
                    device_type="test-type",
                    device_name="test-name",
                    data_type="cmd-status",
                    status="executing"),
                                             types_gen.DeviceData(
                                                 ts=1,
                                                 tag="test-tag",
                                                 device_type="test-type",
                                                 device_name="test-name",
                                                 data_type="cmd-status",
                                                 status="done"))),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1,
                device_type="test-type",
                device_name="test-name",
                data_type="pointer-event"), ()),
    ])

  def test_send_pointer(self) -> None:
    rdev, dev = vnc_impl.VNCDevice("test-type", "test-name").get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      assert dev.supports_tagged_request()
      assert dev.image() is None

      test_device.set_responder(TestVNC("test-type", "test-name"))
      status = dev.send_pointer_event(0.5, 0.6, vnc.PointerEventType.SEND_CLICK)
      self.assertEqual(status.status, "done")
      self.assertEqual(status.error, "")
      test_device.expect_command_data([
          types_gen.CommandData(
              device_type="test-type",
              device_name="test-name",
              data_type="pointer-event",
              tag="tag-1",
              cmd=vnc.PointerEventType.SEND_CLICK.value,
              x=0.5,
              y=0.6)
      ])

      callbacks: ("thread_util.CallbackCapturer[core.PyReachStatus]"
                 ) = thread_util.CallbackCapturer()
      dev.async_send_pointer_event(0.4, 0.3,
                                   vnc.PointerEventType.SEND_LEFT_MOUSE_DOWN,
                                   callbacks.callback_and_then_finish)
      statuses = callbacks.wait()
      self.assertEqual(len(statuses), 1)
      status = statuses[0]
      self.assertEqual(status.status, "done")
      self.assertEqual(status.error, "")
      test_device.expect_command_data([
          types_gen.CommandData(
              device_type="test-type",
              device_name="test-name",
              data_type="pointer-event",
              tag="tag-2",
              cmd=vnc.PointerEventType.SEND_LEFT_MOUSE_DOWN.value,
              x=0.4,
              y=0.3)
      ])

      test_device.set_responder(test_utils.RejectResponder())
      status = dev.send_pointer_event(0.5, 0.6, vnc.PointerEventType.SEND_CLICK)
      self.assertEqual(status.status, "rejected")
      self.assertEqual(status.error, "")
      test_device.expect_command_data([
          types_gen.CommandData(
              device_type="test-type",
              device_name="test-name",
              data_type="pointer-event",
              tag="tag-3",
              cmd=vnc.PointerEventType.SEND_CLICK.value,
              x=0.5,
              y=0.6)
      ])

      callbacks = thread_util.CallbackCapturer()
      dev.async_send_pointer_event(0.4, 0.3,
                                   vnc.PointerEventType.SEND_LEFT_MOUSE_DOWN,
                                   callbacks.callback_and_then_finish)
      statuses = callbacks.wait()
      self.assertEqual(len(statuses), 1)
      status = statuses[0]
      self.assertEqual(status.status, "rejected")
      self.assertEqual(status.error, "")
      test_device.expect_command_data([
          types_gen.CommandData(
              device_type="test-type",
              device_name="test-name",
              data_type="pointer-event",
              tag="tag-4",
              cmd=vnc.PointerEventType.SEND_LEFT_MOUSE_DOWN.value,
              x=0.4,
              y=0.3)
      ])

      test_device.set_callback(None)
      status = dev.send_pointer_event(
          0.5, 0.6, vnc.PointerEventType.SEND_CLICK, timeout=0.0)
      self.assertEqual(status.status, "done")
      self.assertEqual(status.error, "timeout")
      test_device.expect_command_data([
          types_gen.CommandData(
              device_type="test-type",
              device_name="test-name",
              data_type="pointer-event",
              tag="tag-5",
              cmd=vnc.PointerEventType.SEND_CLICK.value,
              x=0.5,
              y=0.6)
      ])

      callbacks = thread_util.CallbackCapturer()
      dev.async_send_pointer_event(
          0.4,
          0.3,
          vnc.PointerEventType.SEND_LEFT_MOUSE_DOWN,
          callbacks.callback_and_then_finish,
          timeout=0.0)
      statuses = callbacks.wait()
      self.assertEqual(len(statuses), 1)
      status = statuses[0]
      self.assertEqual(status.status, "done")
      self.assertEqual(status.error, "timeout")
      test_device.expect_command_data([
          types_gen.CommandData(
              device_type="test-type",
              device_name="test-name",
              data_type="pointer-event",
              tag="tag-6",
              cmd=vnc.PointerEventType.SEND_LEFT_MOUSE_DOWN.value,
              x=0.4,
              y=0.3)
      ])


class TestVNC(test_utils.TestResponder):
  """Represents a VNC for use in a test suite."""

  def __init__(self, device_type: str, device_name: str) -> None:
    """Initialize a Test VNC.

    Args:
      device_type: The JSON device type for the VNC.
      device_name: The JSON device name for the VNC.
    """
    self._device_type = device_type
    self._device_name = device_name

  def step(self, cmd: types_gen.CommandData) -> List[types_gen.DeviceData]:
    """Test step, generates a response for testing framework data."""
    if (cmd.device_type == self._device_type and
        cmd.device_name == self._device_name and
        cmd.data_type == "pointer-event" and cmd.tag):
      return [
          types_gen.DeviceData(
              device_type=self._device_type,
              device_name=self._device_name,
              ts=cmd.ts,
              tag=cmd.tag,
              data_type="cmd-status",
              status="executing"),
          types_gen.DeviceData(
              device_type=self._device_type,
              device_name=self._device_name,
              ts=cmd.ts,
              tag=cmd.tag,
              data_type="cmd-status",
              status="done")
      ]
    return []

  def start(self) -> List[types_gen.DeviceData]:
    return []


if __name__ == "__main__":
  unittest.main()
