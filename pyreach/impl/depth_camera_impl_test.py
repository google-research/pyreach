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

import os.path
from typing import List, Optional
import unittest

from pyreach import core
from pyreach import depth_camera
from pyreach.common.python import types_gen
from pyreach.impl import depth_camera_impl
from pyreach.impl import test_utils
from pyreach.impl import thread_util


class TestPyReachDepthCamera(unittest.TestCase):

  def test_test_depth_camera(self) -> None:
    test_utils.run_test_client_test(
        [TestDepthCamera("test-type", "test-name", "photoneo")], [
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=1,
                    device_type="test-type",
                    device_name="test-name",
                    data_type="frame-request"), (types_gen.DeviceData(
                        ts=1,
                        device_type="test-type",
                        device_name="test-name",
                        data_type="color-depth",
                        color=test_utils.get_test_image_file(
                            "test_images/photoneo/color.jpg"),
                        depth=test_utils.get_test_image_file(
                            "test_images/photoneo/depth.pgm")),)),
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=1,
                    device_type="test-type",
                    device_name="test-name",
                    data_type="frame-request",
                    tag="test-tag"), (types_gen.DeviceData(
                        ts=1,
                        device_type="test-type",
                        device_name="test-name",
                        data_type="color-depth",
                        color=test_utils.get_test_image_file(
                            "test_images/photoneo/color.jpg"),
                        depth=test_utils.get_test_image_file(
                            "test_images/photoneo/depth.pgm"),
                        tag="test-tag"),
                                      types_gen.DeviceData(
                                          ts=1,
                                          device_type="test-type",
                                          device_name="test-name",
                                          data_type="cmd-status",
                                          tag="test-tag",
                                          status="done"))),
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

  def test_depth_camera_tagged(self) -> None:
    ## Setup, ensure no cached image, and that tagged requests will be used.
    rdev, dev = depth_camera_impl.DepthCameraDevice("test-type",
                                                    "test-name").get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      global_callbacks: "thread_util.CallbackCapturer[depth_camera.DepthFrame]" = thread_util.CallbackCapturer(
      )
      stop_callback = dev.add_update_callback(
          global_callbacks.callback_false, global_callbacks.finished_callback)
      assert dev.image() is None
      test_device.set_responder(
          TestDepthCamera("test-type", "test-name", "photoneo"))
      ## Get the first image
      frame = dev.fetch_image()
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="test-type",
              tag="tag-1")
      ])
      self._verify_photoneo(frame, "test-type", "test-name")
      self._verify_photoneo(dev.image(), "test-type", "test-name")
      ## ensure cached is the first image
      assert dev.image() == frame
      ## Use callbacks to get the next images
      callback: ("thread_util.DoubleCallbackCapturer[depth_camera.DepthFrame, "
                 "core.PyReachStatus]") = thread_util.DoubleCallbackCapturer()
      dev.async_fetch_image(
          callback=callback.first_callback_finish,
          error_callback=callback.second_callback_finish)
      frames = callback.wait()
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="test-type",
              tag="tag-2")
      ])
      assert len(frames) == 1
      self._verify_photoneo(frames[0][0], "test-type", "test-name")
      ## image is cached, and ensure second image is not the first
      cached_image = frames[0][0]
      assert dev.image() == cached_image
      assert frame != frames[0][0]
      ## set the callback to None to test timeouts
      test_device.set_callback(None)
      assert dev.fetch_image(timeout=0) is None
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="test-type",
              tag="tag-3")
      ])
      callback = thread_util.DoubleCallbackCapturer()
      dev.async_fetch_image(
          callback=callback.first_callback_finish,
          error_callback=callback.second_callback_finish,
          timeout=0)
      empty_frames = callback.wait()
      assert len(empty_frames) == 1
      assert empty_frames[0][0] is None
      self._is_timeout(empty_frames[0][1])
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="test-type",
              tag="tag-4")
      ])
      ## set the reject responder
      test_device.set_responder(test_utils.RejectResponder())
      assert dev.fetch_image() is None
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="test-type",
              tag="tag-5")
      ])
      callback = thread_util.DoubleCallbackCapturer()
      dev.async_fetch_image(
          callback=callback.first_callback_finish,
          error_callback=callback.second_callback_finish,
          timeout=0)
      empty_frames = callback.wait()
      assert len(empty_frames) == 1
      assert empty_frames[0][0] is None
      status = empty_frames[0][1]
      assert status is not None
      assert status.status == "rejected"
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="test-type",
              tag="tag-6")
      ])
      assert dev.image() == cached_image
      stop_callback()
      global_frames = global_callbacks.wait()
      assert len(global_frames) == 2
      assert global_frames[0] == frame
      assert global_frames[1] == frames[0][0]

  def _verify_photoneo(self, frame: Optional[depth_camera.DepthFrame],
                       device_type: str, device_name: str) -> None:
    assert frame is not None
    assert frame.device_type == device_type
    assert frame.device_name == device_name
    assert frame.color_data is not None
    assert frame.depth_data is not None
    test_utils.assert_image_equal(
        frame.color_data,
        test_utils.get_test_image_file("test_images/photoneo/color.jpg"))
    test_utils.assert_image_depth_equal(
        frame.depth_data,
        test_utils.get_test_image_file("test_images/photoneo/depth.pgm"))

  def _is_timeout(self, status: Optional[core.PyReachStatus]) -> None:
    assert status is not None
    assert status.status == "done"
    assert status.error == "timeout"


class TestDepthCamera(test_utils.TestResponder):
  """Represents a fake depth camera used for testing."""

  def __init__(self, device_type: str, device_name: str,
               directory: str) -> None:
    """Init a test depth camera."""
    self._device_type = device_type
    self._device_name = device_name
    self._directory = directory

  def _response(self, ts: int, tag: str) -> List[types_gen.DeviceData]:
    """Generate a test response."""
    output = [
        types_gen.DeviceData(
            device_type=self._device_type,
            device_name=self._device_name,
            ts=ts,
            tag=tag,
            data_type="color-depth",
            depth=os.path.join(self.test_image_dir, "test_images",
                               self._directory, "depth.pgm"),
            color=os.path.join(self.test_image_dir, "test_images",
                               self._directory, "color.jpg"))
    ]
    if tag:
      output.append(
          types_gen.DeviceData(
              device_type=self._device_type,
              device_name=self._device_name,
              ts=ts,
              tag=tag,
              data_type="cmd-status",
              status="done"))
    return output

  def step(self, cmd: types_gen.CommandData) -> List[types_gen.DeviceData]:
    """Test step, generates a response for testing framework data."""
    if test_utils.is_frame_request_for(cmd, self._device_type,
                                       self._device_name):
      return self._response(cmd.ts, cmd.tag)
    return []

  def start(self) -> List[types_gen.DeviceData]:
    return []


if __name__ == "__main__":
  unittest.main()
