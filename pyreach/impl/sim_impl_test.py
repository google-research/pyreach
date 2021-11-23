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

from typing import List, Optional
import unittest

from pyreach import core  # pylint: disable=unused-import
from pyreach.common.python import types_gen
from pyreach.impl import sim_impl
from pyreach.impl import test_utils
from pyreach.impl import thread_util


class TestSimImpl(unittest.TestCase):

  def test_sim_test(self) -> None:
    test_utils.run_test_client_test([TestSim()], [
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1, device_type="color-camera", data_type="frame-request"),
            ()),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=2,
                device_type="script-engine",
                data_type="run-script",
                script="sim reset"), ()),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=3,
                tag="test-tag-1",
                device_type="script-engine",
                data_type="run-script",
                script="sim reset"), (types_gen.DeviceData(
                    device_type="script-engine",
                    data_type="cmd-status",
                    ts=3,
                    local_ts=3,
                    tag="test-tag-1",
                    status="done",
                ),)),
    ])

  def test_sim_impl_reject(self) -> None:
    rdev, dev = sim_impl.SimDevice().get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:

      def test_cmd(tag: str) -> types_gen.CommandData:
        return types_gen.CommandData(
            tag=tag,
            device_type="script-engine",
            data_type="run-script",
            script="sim reset")

      # Test reject
      test_device.set_responder(test_utils.RejectResponder())
      self._is_rejected(dev.reset())
      test_device.expect_command_data([test_cmd("tag-1")])
      callback_capturer: thread_util.CallbackCapturer[core.PyReachStatus] = (
          thread_util.CallbackCapturer())
      dev.async_reset(callback_capturer.callback,
                      callback_capturer.finished_callback)
      test_device.expect_command_data([test_cmd("tag-2")])
      statuses = callback_capturer.wait()
      self.assertEqual(len(statuses), 1)
      self._is_rejected(statuses[0])
      # Test timeout
      test_device.set_callback(None)
      self._is_rejected(dev.reset(0.0), "timeout")
      test_device.expect_command_data([test_cmd("tag-3")])
      callback_capturer = thread_util.CallbackCapturer()
      dev.async_reset(callback_capturer.callback,
                      callback_capturer.finished_callback, 0.0)
      test_device.expect_command_data([test_cmd("tag-4")])
      statuses = callback_capturer.wait()
      self.assertEqual(len(statuses), 0)
      # Test accept
      test_device.set_responder(TestSim())
      self._is_done(dev.reset())
      test_device.expect_command_data([test_cmd("tag-5")])
      callback_capturer = thread_util.CallbackCapturer()
      dev.async_reset(callback_capturer.callback,
                      callback_capturer.finished_callback)
      test_device.expect_command_data([test_cmd("tag-6")])
      statuses = callback_capturer.wait()
      self.assertEqual(len(statuses), 1)
      self._is_done(statuses[0])

  def _is_rejected(self,
                   status: Optional[core.PyReachStatus],
                   error: str = "") -> None:
    self.assertIsNotNone(status)
    assert status
    self.assertEqual(status.status, "rejected")
    self.assertEqual(status.script, "")
    self.assertEqual(status.message, "")
    self.assertEqual(status.code, 0)
    self.assertEqual(status.error, error)
    self.assertEqual(status.progress, 0.0)

  def _is_done(self, status: Optional[core.PyReachStatus]) -> None:
    self.assertIsNotNone(status)
    assert status
    self.assertEqual(status.status, "done")
    self.assertEqual(status.script, "")
    self.assertEqual(status.message, "")
    self.assertEqual(status.code, 0)
    self.assertEqual(status.error, "")
    self.assertEqual(status.progress, 0.0)


class TestSim(test_utils.TestResponder):
  """A class for generating a regected DeviceData message."""

  def start(self) -> List[types_gen.DeviceData]:
    """Start the responder with no messages."""
    return []

  def step(self, cmd: types_gen.CommandData) -> List[types_gen.DeviceData]:
    """Generate one rejected message.

    Args:
      cmd: The CommandData to get the device type/name from.

    Returns:
      A list containing a rejected Device Data message if
      the cmd is untagged; otherwise an empty list is returned.

    """
    if (cmd.tag and cmd.device_type == "script-engine" and
        not cmd.device_name and cmd.data_type == "run-script"):
      return [
          types_gen.DeviceData(
              device_type="script-engine",
              data_type="cmd-status",
              ts=cmd.ts,
              local_ts=cmd.ts,
              tag=cmd.tag,
              status="done",
          )
      ]
    return []


if __name__ == "__main__":
  unittest.main()
