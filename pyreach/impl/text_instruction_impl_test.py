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
from pyreach import text_instruction
from pyreach.common.python import types_gen
from pyreach.impl import test_utils
from pyreach.impl import text_instruction_impl
from pyreach.impl import thread_util


class TestPyReachTextInstruction(unittest.TestCase):

  def test_test_text_instruction(self) -> None:
    test_utils.run_test_client_test([TestTextInstructions()], [
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1, device_type="color-camera", data_type="frame-request"),
            (types_gen.DeviceData(
                ts=1,
                device_type="instruction-generator",
                data_type="text-instruction",
                text_instruction=types_gen.TextInstruction(
                    intent="pick",
                    success_type="test-type",
                    instruction="test instruction",
                    success_detection="test-detection",
                    uid="test-uid")),)),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=2, device_type="color-camera", data_type="frame-reqquest"),
            ()),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=3,
                tag="test-tag",
                device_type="instruction-generator",
                data_type="text-instruction-request"), (
                    types_gen.DeviceData(
                        ts=3,
                        tag="test-tag",
                        device_type="instruction-generator",
                        data_type="text-instruction",
                        text_instruction=types_gen.TextInstruction(
                            intent="pick",
                            success_type="test-type",
                            instruction="test instruction",
                            success_detection="test-detection",
                            uid="test-uid")),
                    types_gen.DeviceData(
                        ts=3,
                        tag="test-tag",
                        device_type="instruction-generator",
                        data_type="cmd-status",
                        status="done"),
                )),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=3,
                device_type="instruction-generator",
                data_type="text-instruction-request"), (types_gen.DeviceData(
                    ts=3,
                    device_type="instruction-generator",
                    data_type="text-instruction",
                    text_instruction=types_gen.TextInstruction(
                        intent="pick",
                        success_type="test-type",
                        instruction="test instruction",
                        success_detection="test-detection",
                        uid="test-uid")),))
    ])

  def test_text_instructions(self) -> None:
    ## Setup, ensure no cached image, and that tagged requests will be used.
    rdev, dev = text_instruction_impl.TextInstructionDevice().get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      global_callbacks: ("thread_util.CallbackCapturer["
                         "text_instruction.TextInstruction]") = (
                             thread_util.CallbackCapturer())
      stop_callback = dev.add_update_callback(
          global_callbacks.callback_false, global_callbacks.finished_callback)
      self.assertIsNone(dev.text_instruction)
      test_device.set_responder(TestTextInstructions())
      test_device.send_cmd(
          types_gen.CommandData(
              ts=1, device_type="color-camera", data_type="frame-request"))
      frame_0 = dev.text_instruction
      self._verify_frame(frame_0)
      frame_1 = dev.fetch_text_instruction()
      self._verify_frame(frame_1)
      self.assertNotEqual(frame_0, frame_1)

      callbacks: (
          "thread_util.DoubleCallbackCapturer["
          "text_instruction.TextInstruction,"
          " core.PyReachStatus]") = thread_util.DoubleCallbackCapturer()
      dev.async_fetch_text_instruction(
          callback=callbacks.first_callback_finish,
          error_callback=callbacks.second_callback_finish)
      frames = callbacks.wait()
      self.assertEqual(len(frames), 1)
      self.assertIsNone(frames[0][1])
      frame_2 = frames[0][0]
      self._verify_frame(frame_2)

      test_device.set_callback(None)

      self.assertIsNone(dev.fetch_text_instruction(timeout=0))
      dev.async_fetch_text_instruction(
          callback=callbacks.first_callback_finish,
          error_callback=callbacks.second_callback_finish,
          timeout=0)
      frames = callbacks.wait()
      self.assertEqual(len(frames), 1)
      self.assertIsNone(frames[0][0])
      status = frames[0][1]
      self.assertIsNotNone(status)
      if status:
        self.assertEqual(status.status, "done")
        self.assertEqual(status.error, "timeout")

      test_device.set_responder(test_utils.RejectResponder())

      self.assertIsNone(dev.fetch_text_instruction())
      dev.async_fetch_text_instruction(
          callback=callbacks.first_callback_finish,
          error_callback=callbacks.second_callback_finish)
      frames = callbacks.wait()
      self.assertEqual(len(frames), 1)
      self.assertIsNone(frames[0][0])
      status = frames[0][1]
      self.assertIsNotNone(status)
      if status:
        self.assertEqual(status.status, "rejected")
        self.assertEqual(status.error, "")

      stop_callback()
      global_frames = global_callbacks.wait()
      self.assertEqual(len(global_frames), 3)
      self.assertEqual(global_frames[0], frame_0)
      self.assertEqual(global_frames[1], frame_1)
      self.assertEqual(global_frames[2], frame_2)

  def _verify_frame(self,
                    frame: Optional[text_instruction.TextInstruction]) -> None:
    self.assertIsNotNone(frame)
    if frame:
      self.assertEqual(frame.intent, "pick")
      self.assertEqual(frame.success_type, "test-type")
      self.assertEqual(frame.instruction, "test instruction")
      self.assertEqual(frame.success_detection, "test-detection")
      self.assertEqual(frame.uid, "test-uid")


class TestTextInstructions(test_utils.TestResponder):
  """A test text instructions for the test suite."""
  _sent: bool

  def __init__(self) -> None:
    """Init a TestTextInstructions."""
    self._sent = False

  def _generate_message(self, ts: int, tag: str) -> types_gen.DeviceData:
    return types_gen.DeviceData(
        device_type="instruction-generator",
        tag=tag,
        ts=ts,
        data_type="text-instruction",
        text_instruction=types_gen.TextInstruction(
            intent="pick",
            success_type="test-type",
            instruction="test instruction",
            success_detection="test-detection",
            uid="test-uid"))

  def step(self, cmd: types_gen.CommandData) -> List[types_gen.DeviceData]:
    """Test step, generates a response for testing framework data."""
    output: List[types_gen.DeviceData] = []
    if not self._sent:
      self._sent = True
      output.append(self._generate_message(cmd.ts, ""))
    if (cmd.device_type == "instruction-generator" and not cmd.device_name and
        cmd.data_type == "text-instruction-request"):
      output.append(self._generate_message(cmd.ts, cmd.tag))
      if cmd.tag:
        output.append(
            types_gen.DeviceData(
                device_type="instruction-generator",
                tag=cmd.tag,
                ts=cmd.ts,
                data_type="cmd-status",
                status="done"))
    return output

  def start(self) -> List[types_gen.DeviceData]:
    return []


if __name__ == "__main__":
  unittest.main()
