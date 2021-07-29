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

from pyreach import color_camera
from pyreach import core
from pyreach.common.python import types_gen
from pyreach.impl import color_camera_impl
from pyreach.impl import test_utils
from pyreach.impl import thread_util


class TestPyReachCamera(unittest.TestCase):

  def test_test_camera(self) -> None:
    test_color_camera = TestColorCamera("test-type", "test-name", "uvc")
    test_utils.run_test_client_test([test_color_camera], [
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1,
                device_type="test-type",
                device_name="test-name",
                data_type="frame-request"), (types_gen.DeviceData(
                    ts=1,
                    device_type="test-type",
                    device_name="test-name",
                    data_type="color",
                    color=test_utils.get_test_image_file(
                        "test_images/uvc/color.jpg")),)),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1,
                device_type="test-type",
                device_name="test-name",
                data_type="frame-request",
                tag="test-tag"), (
                    types_gen.DeviceData(
                        ts=1,
                        device_type="test-type",
                        device_name="test-name",
                        data_type="color",
                        color=test_utils.get_test_image_file(
                            "test_images/uvc/color.jpg"),
                        tag="test-tag"),
                    types_gen.DeviceData(
                        ts=1,
                        device_type="test-type",
                        device_name="test-name",
                        data_type="cmd-status",
                        tag="test-tag",
                        status="done"),
                )),
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

  def test_test_camera_untagged(self) -> None:
    test_utils.run_test_client_test([TestColorCamera("uvc", "", "uvc")], [
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1,
                device_type="uvc",
                device_name="",
                data_type="frame-request"), (types_gen.DeviceData(
                    ts=1,
                    device_type="uvc",
                    device_name="",
                    data_type="color",
                    color=test_utils.get_test_image_file(
                        "test_images/uvc/color.jpg")),)),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1,
                device_type="uvc",
                device_name="",
                data_type="frame-request"), (types_gen.DeviceData(
                    ts=1,
                    device_type="uvc",
                    device_name="",
                    data_type="color",
                    color=test_utils.get_test_image_file(
                        "test_images/uvc/color.jpg")),)),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1,
                device_type="uvc",
                device_name="test",
                data_type="frame-request"), ()),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1,
                device_type="test",
                device_name="",
                data_type="frame-request"), ()),
    ])

  def test_camera_tagged(self) -> None:
    ## Setup, ensure no cached image, and that tagged requests will be used.
    rdev, dev = color_camera_impl.ColorCameraDevice("test-type",
                                                    "test-name").get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      global_callbacks: ("thread_util.CallbackCapturer[color_camera.ColorFrame]"
                        ) = thread_util.CallbackCapturer()
      stop_callback = dev.add_update_callback(
          global_callbacks.callback_false, global_callbacks.finished_callback)
      assert dev.supports_tagged_request()
      assert dev.image() is None
      test_device.set_responder(
          TestColorCamera("test-type", "test-name", "uvc"))
      ## Get the first image
      frame = dev.fetch_image()
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="test-type",
              tag="tag-1")
      ])
      self._verify_uvc(frame, "test-type", "test-name")
      self._verify_uvc(dev.image(), "test-type", "test-name")
      ## ensure cached is the first image
      assert dev.image() == frame
      ## Use callbacks to get the next images
      callback: ("thread_util.DoubleCallbackCapturer[color_camera.ColorFrame, "
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
      self._verify_uvc(frames[0][0], "test-type", "test-name")
      assert frames[0][1] is None
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

  def test_camera_untagged(self) -> None:
    ## Setup, ensure no cached image, and that tagged requests will be used.
    rdev, dev = color_camera_impl.ColorCameraDevice("uvc", "").get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      global_callbacks: ("thread_util.CallbackCapturer[color_camera.ColorFrame]"
                        ) = thread_util.CallbackCapturer()
      stop_callback = dev.add_update_callback(
          global_callbacks.callback_false, global_callbacks.finished_callback)
      assert not dev.supports_tagged_request()
      assert dev.image() is None
      test_device.set_responder(TestColorCamera("uvc", "", "uvc"))
      ## Get the first image
      frame = dev.fetch_image()
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request", device_name="", device_type="uvc")
      ])
      self._verify_uvc(frame, "uvc", "")
      self._verify_uvc(dev.image(), "uvc", "")
      ## ensure cached is the first image
      assert dev.image() == frame
      ## Use callbacks to get the next images
      callback: ("thread_util.DoubleCallbackCapturer["
                 "Optional[color_camera.ColorFrame], core.PyReachStatus]"
                ) = thread_util.DoubleCallbackCapturer()
      dev.async_fetch_image(
          callback=callback.first_callback_finish,
          error_callback=callback.second_callback_finish)
      frames = callback.wait()
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request", device_name="", device_type="uvc")
      ])
      assert len(frames) == 1
      assert frames[0][1] is None
      self._verify_uvc(frames[0][0], "uvc", "")
      ## image is cached, and ensure second image is not the first
      assert dev.image() == frames[0][0]
      assert frame != frames[0]
      ## clear the callback to test timeouts
      test_device.set_callback(None)
      assert dev.fetch_image(timeout=0) is None
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request", device_name="", device_type="uvc")
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
              data_type="frame-request", device_name="", device_type="uvc")
      ])
      stop_callback()
      global_frames = global_callbacks.wait()
      assert len(global_frames) == 2
      assert global_frames[0] == frame
      assert global_frames[1] == frames[0][0]

  def test_camera_untagged_request(self) -> None:
    ## Setup, ensure no cached image, and that tagged requests will be used.
    rdev, dev = color_camera_impl.ColorCameraDevice("uvc", "").get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      global_callbacks: "thread_util.CallbackCapturer[color_camera.ColorFrame]" = thread_util.CallbackCapturer(
      )
      stop_callback = dev.add_update_callback(
          global_callbacks.callback_false, global_callbacks.finished_callback)
      assert not dev.supports_tagged_request()
      assert dev.image() is None
      test_device.set_responder(TestColorCamera("uvc", "", "uvc"))
      dev.start_streaming(1.0)
      while True:
        if dev.image() is not None:
          break
      self._verify_uvc(dev.image(), "uvc", "")
      dev.stop_streaming()
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request", device_name="", device_type="uvc")
      ])
      stop_callback()
      global_frames = global_callbacks.wait()
      assert len(global_frames) == 1
      assert global_frames[0] == dev.image()

  def _verify_uvc(self, frame: Optional[color_camera.ColorFrame],
                  device_type: str, device_name: str) -> None:
    assert frame is not None
    assert frame.device_type == device_type
    assert frame.device_name == device_name
    assert frame.color_image is not None
    test_utils.assert_image_equal(frame.color_image,
                                  "test_images/uvc/color.jpg")

  def _is_timeout(self, status: Optional[core.PyReachStatus]) -> None:
    assert status is not None
    assert status.status == "done"
    assert status.error == "timeout"


class TestColorCamera(test_utils.TestResponder):
  """Represents a Camera for use in a test suite."""

  def __init__(self, device_type: str, device_name: str,
               directory: str) -> None:
    """Initialize a Test Camera.

    Args:
      device_type: The JSON device type for the camera.
      device_name: The JSON device name for the camera.
      directory: The directory to store the camera frames into.
    """
    self._device_type = device_type
    self._device_name = device_name
    self._directory = directory

  def _response(self, ts: int, tag: str) -> List[types_gen.DeviceData]:
    """Generate a test response."""
    if (self._device_type, self._device_name) in {("uvc", "")}:
      tag = ""
    output = [
        types_gen.DeviceData(
            device_type=self._device_type,
            device_name=self._device_name,
            ts=ts,
            tag=tag,
            data_type="color",
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
