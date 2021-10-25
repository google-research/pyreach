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
"""Tests for client_annotation_impl."""

from typing import List
import unittest

from pyreach.common.proto_gen import logs_pb2
from pyreach import core
from pyreach.common.python import types_gen
from pyreach.impl import client_annotation_impl
from pyreach.impl import test_utils
from pyreach.impl import thread_util


class TestClientAnnotation(test_utils.TestResponder):
  """Class to test client annotation."""

  def step(self, cmd: types_gen.CommandData) -> List[types_gen.DeviceData]:
    """Step function of testing client annotation."""
    if (cmd.device_type == "client-annotation" and not cmd.device_name and
        cmd.data_type == "client-annotation"):
      return [
          types_gen.DeviceData(
              ts=cmd.ts,
              device_type="client-annotation",
              data_type="cmd-status",
              status="done",
              tag=cmd.tag)
      ]
    return []

  def start(self) -> List[types_gen.DeviceData]:
    return []


class TestPyReachClientAnnotation(unittest.TestCase):

  def test_test_client_annotation(self) -> None:
    test_utils.run_test_client_test([TestClientAnnotation()], [
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1,
                device_type="client-annotation",
                device_name="",
                data_type="client-annotation"), (types_gen.DeviceData(
                    ts=1,
                    device_type="client-annotation",
                    device_name="",
                    data_type="cmd-status",
                    status="done"),)),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1, device_type="operator", data_type="event-start"), ()),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1,
                device_type="operator",
                data_type="event",
                event_name="pick",
            ), ()),
    ])

  def test_client_annotation(self) -> None:
    rdev, dev = client_annotation_impl.ClientAnnotationDevice().get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      test_device.set_responder(TestClientAnnotation())
      self.assertRaises(
          core.PyReachError, dev.annotate,
          logs_pb2.ClientAnnotation(
              interval_start=logs_pb2.IntervalStart(name="test")))
      self.assertRaises(
          core.PyReachError, dev.async_annotate,
          logs_pb2.ClientAnnotation(
              interval_start=logs_pb2.IntervalStart(name="test")))
      self.assertRaises(
          core.PyReachError, dev.annotate,
          logs_pb2.ClientAnnotation(
              interval_end=logs_pb2.IntervalEnd(name="test")))
      self.assertRaises(
          core.PyReachError, dev.async_annotate,
          logs_pb2.ClientAnnotation(
              interval_end=logs_pb2.IntervalEnd(name="test")))
      status = dev.annotate(
          logs_pb2.ClientAnnotation(
              text_annotation=logs_pb2.TextAnnotation(
                  category="test-category", text="test-text")))
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="client-annotation",
              device_name="",
              device_type="client-annotation",
              tag="tag-1",
              client_annotation=types_gen.ClientAnnotation(
                  text_annotation=types_gen.TextAnnotation(
                      category="test-category", text="test-text")))
      ])
      self.assertEqual(status.status, "done")
      self.assertTrue(status.is_last_status())
      self.assertFalse(status.is_error())
      callbacks = thread_util.CallbackCapturer[core.PyReachStatus]()
      dev.async_annotate(
          logs_pb2.ClientAnnotation(
              text_annotation=logs_pb2.TextAnnotation(
                  category="test-category", text="test-text")),
          callback=callbacks.callback_and_then_finish)
      statuses = callbacks.wait()
      self.assertEqual(len(statuses), 1)
      status = statuses[0]
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="client-annotation",
              device_name="",
              device_type="client-annotation",
              tag="tag-2",
              client_annotation=types_gen.ClientAnnotation(
                  text_annotation=types_gen.TextAnnotation(
                      category="test-category", text="test-text")))
      ])
      self.assertEqual(status.status, "done")
      self.assertTrue(status.is_last_status())
      self.assertFalse(status.is_error())


if __name__ == "__main__":
  unittest.main()
