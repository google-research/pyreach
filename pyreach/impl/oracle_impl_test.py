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

import os
from typing import List
from typing import Optional
import unittest
from pyreach import core
from pyreach import oracle
from pyreach.common.python import types_gen
from pyreach.impl import oracle_impl
from pyreach.impl import test_utils
from pyreach.impl import thread_util


class TestPyreachOracle(unittest.TestCase):

  def test_test_oracle(self) -> None:
    test_utils.run_test_client_test(
        [TestOracle("test-type", "test-name", "oracle-pick-points")], [
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=1,
                    device_type="test-type",
                    device_name="test-name",
                    data_type="inference-request"),
                (types_gen.DeviceData(
                    ts=1,
                    device_type="test-type",
                    device_name="test-name",
                    data_type="prediction",
                    pick_points=[
                        types_gen.PickPoint(369, 275),
                        types_gen.PickPoint(270, 344),
                        types_gen.PickPoint(414, 346),
                        types_gen.PickPoint(348, 425),
                        types_gen.PickPoint(238, 391),
                        types_gen.PickPoint(467, 373),
                        types_gen.PickPoint(302, 382),
                        types_gen.PickPoint(248, 431),
                        types_gen.PickPoint(469, 423),
                        types_gen.PickPoint(318, 246),
                        types_gen.PickPoint(526, 375),
                        types_gen.PickPoint(363, 320),
                        types_gen.PickPoint(404, 257),
                        types_gen.PickPoint(398, 304),
                        types_gen.PickPoint(424, 410),
                        types_gen.PickPoint(328, 353),
                        types_gen.PickPoint(488, 318),
                        types_gen.PickPoint(437, 328),
                        types_gen.PickPoint(310, 447),
                        types_gen.PickPoint(252, 305),
                        types_gen.PickPoint(457, 260),
                        types_gen.PickPoint(433, 440),
                    ],
                    color=test_utils.get_test_image_file(
                        "test_images/oracle-pick-points/color.jpg")),),
            ),
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=1,
                    device_type="test-type",
                    device_name="test-name",
                    data_type="frame-request",
                    tag="test-tag"),
                (types_gen.DeviceData(
                    ts=1,
                    device_type="test-type",
                    device_name="test-name",
                    data_type="prediction",
                    pick_points=[
                        types_gen.PickPoint(369, 275),
                        types_gen.PickPoint(270, 344),
                        types_gen.PickPoint(414, 346),
                        types_gen.PickPoint(348, 425),
                        types_gen.PickPoint(238, 391),
                        types_gen.PickPoint(467, 373),
                        types_gen.PickPoint(302, 382),
                        types_gen.PickPoint(248, 431),
                        types_gen.PickPoint(469, 423),
                        types_gen.PickPoint(318, 246),
                        types_gen.PickPoint(526, 375),
                        types_gen.PickPoint(363, 320),
                        types_gen.PickPoint(404, 257),
                        types_gen.PickPoint(398, 304),
                        types_gen.PickPoint(424, 410),
                        types_gen.PickPoint(328, 353),
                        types_gen.PickPoint(488, 318),
                        types_gen.PickPoint(437, 328),
                        types_gen.PickPoint(310, 447),
                        types_gen.PickPoint(252, 305),
                        types_gen.PickPoint(457, 260),
                        types_gen.PickPoint(433, 440),
                    ],
                    color=test_utils.get_test_image_file(
                        "test_images/oracle-pick-points/color.jpg"),
                    tag="test-tag"),),
            ),
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=1,
                    device_type="test-type",
                    device_name="test",
                    data_type="frame-request"), ()),
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=1,
                    device_type="test-type",
                    device_name="",
                    data_type="frame-request"), ()),
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=1,
                    device_type="test",
                    device_name="test-name",
                    data_type="frame-request"), ()),
        ])

  def test_oracle_tagged(self) -> None:
    ## Setup, ensure no cached image, and that tagged requests will be used.
    rdev, dev = oracle_impl.OracleDevice("test-type", "test-name").get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      global_callbacks: "thread_util.CallbackCapturer[oracle.Prediction]" = thread_util.CallbackCapturer(
      )
      stop_callback = dev.add_update_callback(
          global_callbacks.callback_false, global_callbacks.finished_callback)
      assert dev.prediction() is None
      test_device.set_responder(
          TestOracle("test-type", "test-name", "oracle-pick-points"))
      ## Get the first image
      frame = dev.fetch_prediction("pick", "pick", "sparse", "122",
                                   "SingulateLeftBin")
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="inference-request",
              device_name="test-name",
              device_type="test-type",
              intent="pick",
              prediction_type="pick",
              request_type="sparse",
              task_code="122",
              label="SingulateLeftBin",
              tag="tag-1")
      ])
      self._verify_oracle_pick_points(frame, "test-type", "test-name")
      ## Use callbacks to get the next images
      callback: ("thread_util.DoubleCallbackCapturer"
                 "[oracle.Prediction, core.PyReachStatus]")
      callback = thread_util.DoubleCallbackCapturer()
      dev.async_fetch_prediction(
          "pick",
          "pick",
          "sparse",
          "122",
          "SingulateLeftBin",
          callback=callback.first_callback_finish,
          error_callback=callback.second_callback_finish)
      frames = callback.wait()
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="inference-request",
              device_name="test-name",
              device_type="test-type",
              intent="pick",
              prediction_type="pick",
              request_type="sparse",
              task_code="122",
              label="SingulateLeftBin",
              tag="tag-2")
      ])
      assert len(frames) == 1
      self._verify_oracle_pick_points(frames[0][0], "test-type", "test-name")
      ## image is cached, and ensure second image is not the first
      assert frame != frames[0][0]
      assert frames[0][1] is None
      ## set the callback to None to test timeouts
      test_device.set_callback(None)
      with self.assertRaises(core.PyReachError):
        dev.fetch_prediction(
            "pick", "pick", "sparse", "122", "SingulateLeftBin", timeout=0)
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="inference-request",
              device_name="test-name",
              device_type="test-type",
              intent="pick",
              prediction_type="pick",
              request_type="sparse",
              task_code="122",
              label="SingulateLeftBin",
              tag="tag-3")
      ])
      callback = thread_util.DoubleCallbackCapturer()
      dev.async_fetch_prediction(
          "pick",
          "pick",
          "sparse",
          "122",
          "SingulateLeftBin",
          callback=callback.first_callback_finish,
          error_callback=callback.second_callback_finish,
          timeout=0)
      frames = callback.wait()
      assert len(frames) == 1
      assert frames[0][0] is None
      self._is_timeout(frames[0][1])
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="inference-request",
              device_name="test-name",
              device_type="test-type",
              intent="pick",
              prediction_type="pick",
              request_type="sparse",
              task_code="122",
              label="SingulateLeftBin",
              tag="tag-4")
      ])
      ## set the reject responder
      test_device.set_responder(test_utils.RejectResponder())
      with self.assertRaises(core.PyReachError):
        dev.fetch_prediction("pick", "pick", "sparse", "122",
                             "SingulateLeftBin")
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="inference-request",
              device_name="test-name",
              device_type="test-type",
              intent="pick",
              prediction_type="pick",
              request_type="sparse",
              task_code="122",
              label="SingulateLeftBin",
              tag="tag-5")
      ])
      callback = thread_util.DoubleCallbackCapturer()
      dev.async_fetch_prediction(
          "pick",
          "pick",
          "sparse",
          "122",
          "SingulateLeftBin",
          callback=callback.first_callback_finish,
          error_callback=callback.second_callback_finish,
          timeout=0)
      frames = callback.wait()
      self.assertEqual(len(frames), 1)
      self.assertIsNone(frames[0][0])
      status = frames[0][1]
      self.assertIsNotNone(status)
      if status:
        self.assertEqual(status.status, "rejected")
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="inference-request",
              device_name="test-name",
              device_type="test-type",
              intent="pick",
              prediction_type="pick",
              request_type="sparse",
              task_code="122",
              label="SingulateLeftBin",
              tag="tag-6")
      ])
      self.assertIsNone(dev.prediction())
      stop_callback()
      self.assertEqual(len(global_callbacks.wait()), 0)

  def _verify_oracle_pick_points(self, frame: Optional[oracle.Prediction],
                                 device_type: str, device_name: str) -> None:
    self.assertIsNotNone(frame)
    if not frame:
      return
    self.assertEqual(frame.device_type, device_type)
    self.assertEqual(frame.device_name, device_name)
    self.assertIsNotNone(frame.image)
    self.assertEqual(frame.intent, "pick")
    self.assertEqual(frame.prediction_type, "pick")
    self.assertEqual(frame.request_type, "sparse")
    self.assertEqual(frame.task_code, "122")
    self.assertEqual(frame.label, "SingulateLeftBin")
    test_utils.assert_image_equal(frame.image,
                                  "test_images/oracle-pick-points/color.jpg")

  def _is_timeout(self, status: Optional[core.PyReachStatus]) -> None:
    self.assertIsNotNone(status)
    if not status:
      return
    self.assertEqual(status.status, "done")
    self.assertEqual(status.error, "timeout")


class TestOracle(test_utils.TestResponder):
  """A test oracle for the test suite."""

  def __init__(self, device_type: str, device_name: str,
               directory: str) -> None:
    """Init a test Oracle.

    Args:
      device_type: The JSON device type for the test Oracle.
      device_name: The JSON device name for the test Oracle.
      directory:   The directory for test image files.
    """
    self._device_type = device_type
    self._device_name = device_name
    self._directory = directory

  def _response(self, ts: int, tag: str) -> List[types_gen.DeviceData]:
    """Generate a test response.

    Args:
      ts: the timestamp.
      tag: the tag.

    Returns:
      A list of device data.
    """
    # Note: the oracle does not return cmd-status.
    return [
        types_gen.DeviceData(
            device_type=self._device_type,
            device_name=self._device_name,
            ts=ts,
            tag=tag,
            data_type="prediction",
            pick_points=[
                types_gen.PickPoint(369, 275),
                types_gen.PickPoint(270, 344),
                types_gen.PickPoint(414, 346),
                types_gen.PickPoint(348, 425),
                types_gen.PickPoint(238, 391),
                types_gen.PickPoint(467, 373),
                types_gen.PickPoint(302, 382),
                types_gen.PickPoint(248, 431),
                types_gen.PickPoint(469, 423),
                types_gen.PickPoint(318, 246),
                types_gen.PickPoint(526, 375),
                types_gen.PickPoint(363, 320),
                types_gen.PickPoint(404, 257),
                types_gen.PickPoint(398, 304),
                types_gen.PickPoint(424, 410),
                types_gen.PickPoint(328, 353),
                types_gen.PickPoint(488, 318),
                types_gen.PickPoint(437, 328),
                types_gen.PickPoint(310, 447),
                types_gen.PickPoint(252, 305),
                types_gen.PickPoint(457, 260),
                types_gen.PickPoint(433, 440),
            ],
            color=os.path.join(self.test_image_dir, "test_images",
                               self._directory, "color.jpg"))
    ]

  def step(self, cmd: types_gen.CommandData) -> List[types_gen.DeviceData]:
    """Test step, generates a response for testing framework data."""
    if (self._device_type == cmd.device_type and
        self._device_name == cmd.device_name and
        cmd.data_type == "inference-request"):
      return self._response(cmd.ts, cmd.tag)
    if (self._device_type == cmd.device_type and
        self._device_name == cmd.device_name and
        cmd.data_type == "frame-request"):
      return self._response(cmd.ts, cmd.tag)
    return []

  def start(self) -> List[types_gen.DeviceData]:
    return []


if __name__ == "__main__":
  unittest.main()
