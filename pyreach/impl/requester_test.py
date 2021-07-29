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

from typing import Optional
import unittest

from pyreach.common.python import types_gen
from pyreach.impl import requester
from pyreach.impl import thread_util


class _MockRequester(requester.Requester[str]):

  def get_message_supplement(self, msg: types_gen.DeviceData) -> Optional[str]:
    if msg.device_type == "robot" and msg.device_name == "test" and \
        msg.data_type == "key-value" and msg.key == "robot_constraints.json":
      return msg.value
    return None

  def send_key_value(self, tag: str, value: str) -> None:
    self.enqueue_device_data(
        types_gen.DeviceData(
            tag=tag,
            device_type="robot",
            device_name="test",
            data_type="key-value",
            key="robot_constraints.json",
            value=value))

  def send_wrong_key(self, tag: str) -> None:
    self.enqueue_device_data(
        types_gen.DeviceData(
            tag=tag,
            device_type="robot",
            device_name="test",
            data_type="key-value",
            key="kill",
            value="{}"))


class TestPyreachRequester(unittest.TestCase):
  """Test the Request and Requester classes."""

  def test_request_untagged_no_timeout(self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera", "left", "color", None, None)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertIsNone(request.tag)
    terminate, send = request.on_poll()
    self.assertFalse(terminate)
    self.assertIsNone(send)
    terminate, send = request.on_message(
        types_gen.DeviceData(
            device_type="color-camera", device_name="right", data_type="color"),
        "test-1")
    self.assertFalse(terminate)
    self.assertIsNone(send)
    request._resend_time = 0.0  # Force resend for test
    terminate, send = request.on_message(
        types_gen.DeviceData(
            device_type="color-camera", device_name="right", data_type="color"),
        "test-2")
    self.assertFalse(terminate)
    self.assertIsNotNone(send)
    if send is not None:
      self.assertEqual(send.device_type, "color-camera")
      self.assertEqual(send.device_name, "left")
      self.assertEqual(send.data_type, "frame-request")
      self.assertEqual(send.tag, "")
    pass_data = types_gen.DeviceData(
        device_type="color-camera", device_name="left", data_type="color")
    terminate, send = request.on_message(pass_data, "test-3")
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 1)
    self.assertEqual(messages[0][0], pass_data)
    self.assertEqual(messages[0][1], "test-3")
    request.close()

  def test_request_untagged_without_timeout(self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera", "left", "color", None, 100.0)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertIsNone(request.tag)
    terminate, send = request.on_poll()
    self.assertFalse(terminate)
    self.assertIsNone(send)
    terminate, send = request.on_message(
        types_gen.DeviceData(
            device_type="color-camera", device_name="right", data_type="color"),
        "test-1")
    self.assertFalse(terminate)
    self.assertIsNone(send)
    request._resend_time = 0.0  # Force resend for test
    terminate, send = request.on_message(
        types_gen.DeviceData(
            device_type="color-camera", device_name="right", data_type="color"),
        "test-2")
    self.assertFalse(terminate)
    self.assertNotEqual(send, None)
    if send is not None:
      self.assertEqual(send.device_type, "color-camera")
      self.assertEqual(send.device_name, "left")
      self.assertEqual(send.data_type, "frame-request")
      self.assertEqual(send.tag, "")
    pass_data = types_gen.DeviceData(
        device_type="color-camera", device_name="left", data_type="color")
    terminate, send = request.on_message(pass_data, "test-3")
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 1)
    self.assertEqual(messages[0][0], pass_data)
    self.assertEqual(messages[0][1], "test-3")
    request.close()

  def test_request_untagged_with_timeout(self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera", "left", "color", None, 0.0)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertIsNone(request.tag)
    terminate, send = request.on_poll()
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 0)
    request.close()

  def test_request_untagged_with_timeout_message(self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera", "left", "color", None, 0.0)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertIsNone(request.tag)
    pass_data = types_gen.DeviceData(
        device_type="color-camera", device_name="left", data_type="color")
    terminate, send = request.on_message(pass_data, "test-1")
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 1)
    self.assertEqual(messages[0][0], pass_data)
    self.assertEqual(messages[0][1], "test-1")
    request.close()

  def test_request_untagged_with_timeout_wrong_message(self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera", "left", "color", None, 0.0)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertIsNone(request.tag)
    pass_data = types_gen.DeviceData(
        device_type="color-camera", device_name="right", data_type="color")
    terminate, send = request.on_message(pass_data, "test-1")
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 0)
    request.close()

  def test_request_tagged_no_timeout(self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera", "left", "color", "test-tag", None)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertEqual(request.tag, "test-tag")
    terminate, send = request.on_poll()
    self.assertFalse(terminate)
    self.assertIsNone(send)
    terminate, send = request.on_message(
        types_gen.DeviceData(
            device_type="color-camera",
            device_name="left",
            data_type="color",
            tag="ignore"), "test-1")
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_0 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="cmd-status",
        data_type="color",
        tag="test-tag",
        status="executing")
    terminate, send = request.on_message(pass_data_0, None)
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_1 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="color",
        tag="test-tag")
    self.assertIsNone(send)
    terminate, send = request.on_message(pass_data_1, "test-2")
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_2 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="cmd-status",
        tag="test-tag",
        status="executing")
    terminate, send = request.on_message(pass_data_2, None)
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_3 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="cmd-status",
        tag="test-tag",
        status="done")
    terminate, send = request.on_message(pass_data_3, None)
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 4)
    self.assertEqual(messages[0][0], pass_data_0)
    self.assertIsNone(messages[0][1])
    self.assertEqual(messages[1][0], pass_data_1)
    self.assertEqual(messages[1][1], "test-2")
    self.assertEqual(messages[2][0], pass_data_2)
    self.assertIsNone(messages[2][1])
    self.assertEqual(messages[3][0], pass_data_3)
    self.assertIsNone(messages[3][1])
    request.close()

  def test_request_tagged_no_timeout_swap(self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera", "left", "color", "test-tag", None)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertEqual(request.tag, "test-tag")
    terminate, send = request.on_poll()
    self.assertFalse(terminate)
    self.assertIsNone(send)
    terminate, send = request.on_message(
        types_gen.DeviceData(
            device_type="color-camera",
            device_name="left",
            data_type="color",
            tag="ignore"), "test-1")
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_0 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="cmd-status",
        data_type="color",
        tag="test-tag",
        status="executing")
    terminate, send = request.on_message(pass_data_0, None)
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_1 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="cmd-status",
        tag="test-tag",
        status="done")
    terminate, send = request.on_message(pass_data_1, None)
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 2)
    self.assertEqual(messages[0][0], pass_data_0)
    self.assertIsNone(messages[0][1])
    self.assertEqual(messages[1][0], pass_data_1)
    self.assertIsNone(messages[1][1])
    request.close()

  def test_request_tagged_no_timeout_expect_messages(self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera", "left", "color", "test-tag", None, expect_messages=1)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertEqual(request.tag, "test-tag")
    terminate, send = request.on_poll()
    self.assertFalse(terminate)
    self.assertIsNone(send)
    terminate, send = request.on_message(
        types_gen.DeviceData(
            device_type="color-camera",
            device_name="left",
            data_type="color",
            tag="ignore"), "test-0")
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_0 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="color",
        tag="test-tag")
    terminate, send = request.on_message(pass_data_0, "test-1")
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_1 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="cmd-status",
        tag="test-tag",
        status="done")
    terminate, send = request.on_message(pass_data_1, None)
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 2)
    self.assertEqual(messages[0][0], pass_data_0)
    self.assertEqual(messages[0][1], "test-1")
    self.assertEqual(messages[1][0], pass_data_1)
    self.assertIsNone(messages[1][1])
    request.close()

  def test_request_tagged_no_timeout_expect_messages_swap(self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera", "left", "color", "test-tag", None, expect_messages=1)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertEqual(request.tag, "test-tag")
    terminate, send = request.on_poll()
    self.assertFalse(terminate)
    self.assertIsNone(send)
    terminate, send = request.on_message(
        types_gen.DeviceData(
            device_type="color-camera",
            device_name="left",
            data_type="color",
            tag="ignore"), "test-0")
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_0 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="cmd-status",
        tag="test-tag",
        status="done")
    terminate, send = request.on_message(pass_data_0, None)
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_1 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="color",
        tag="test-tag")
    terminate, send = request.on_message(pass_data_1, "test-1")
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 2)
    self.assertEqual(messages[0][0], pass_data_1)
    self.assertEqual(messages[0][1], "test-1")
    self.assertEqual(messages[1][0], pass_data_0)
    self.assertIsNone(messages[1][1])
    request.close()

  def test_request_tagged_no_timeout_expect_messages_error(self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera", "left", "color", "test-tag", None, expect_messages=1)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertEqual(request.tag, "test-tag")
    terminate, send = request.on_poll()
    self.assertFalse(terminate)
    self.assertIsNone(send)
    terminate, send = request.on_message(
        types_gen.DeviceData(
            device_type="color-camera",
            device_name="left",
            data_type="color",
            tag="ignore"), "test-0")
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_0 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="cmd-status",
        tag="test-tag",
        status="done",
        error="died")
    terminate, send = request.on_message(pass_data_0, None)
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 1)
    self.assertEqual(messages[0][0], pass_data_0)
    self.assertIsNone(messages[0][1])
    request.close()

  def test_request_tagged_no_timeout_expect_messages_skip_status(self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera",
        "left",
        "color",
        "test-tag",
        None,
        expect_messages=1,
        expect_cmd_status=False)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertEqual(request.tag, "test-tag")
    terminate, send = request.on_poll()
    self.assertFalse(terminate)
    self.assertIsNone(send)
    terminate, send = request.on_message(
        types_gen.DeviceData(
            device_type="color-camera",
            device_name="left",
            data_type="color",
            tag="ignore"), "test-0")
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_0 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="color",
        tag="test-tag")
    terminate, send = request.on_message(pass_data_0, "test-1")
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 1)
    self.assertEqual(messages[0][0], pass_data_0)
    self.assertEqual(messages[0][1], "test-1")
    request.close()

  def test_request_tagged_no_timeout_expect_messages_skip_status_error(
      self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera",
        "left",
        "color",
        "test-tag",
        None,
        expect_messages=1,
        expect_cmd_status=False)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertEqual(request.tag, "test-tag")
    terminate, send = request.on_poll()
    self.assertFalse(terminate)
    self.assertIsNone(send)
    terminate, send = request.on_message(
        types_gen.DeviceData(
            device_type="color-camera",
            device_name="left",
            data_type="color",
            tag="ignore"), "test-0")
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_0 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="cmd-status",
        tag="test-tag",
        status="done",
        error="died")
    terminate, send = request.on_message(pass_data_0, None)
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 1)
    self.assertEqual(messages[0][0], pass_data_0)
    self.assertIsNone(messages[0][1])
    request.close()

  def test_request_tagged_without_timeout(self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera", "left", "color", "test-tag", 100.0)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertEqual(request.tag, "test-tag")
    terminate, send = request.on_poll()
    self.assertFalse(terminate)
    self.assertIsNone(send)
    terminate, send = request.on_message(
        types_gen.DeviceData(
            device_type="color-camera",
            device_name="left",
            data_type="color",
            tag="ignore"), "test-1")
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_0 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="cmd-status",
        data_type="color",
        tag="test-tag",
        status="executing")
    terminate, send = request.on_message(pass_data_0, None)
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_1 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="color",
        tag="test-tag")
    self.assertIsNone(send)
    terminate, send = request.on_message(pass_data_1, "test-2")
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_2 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="cmd-status",
        tag="test-tag",
        status="executing")
    terminate, send = request.on_message(pass_data_2, None)
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_3 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="cmd-status",
        tag="test-tag",
        status="done")
    terminate, send = request.on_message(pass_data_3, None)
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 4)
    self.assertEqual(messages[0][0], pass_data_0)
    self.assertIsNone(messages[0][1])
    self.assertEqual(messages[1][0], pass_data_1)
    self.assertEqual(messages[1][1], "test-2")
    self.assertEqual(messages[2][0], pass_data_2)
    self.assertIsNone(messages[2][1])
    self.assertEqual(messages[3][0], pass_data_3)
    self.assertIsNone(messages[3][1])
    request.close()

  def test_request_tagged_without_timeout_swap(self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera", "left", "color", "test-tag", 100.0)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertEqual(request.tag, "test-tag")
    terminate, send = request.on_poll()
    self.assertFalse(terminate)
    self.assertIsNone(send)
    terminate, send = request.on_message(
        types_gen.DeviceData(
            device_type="color-camera",
            device_name="left",
            data_type="color",
            tag="ignore"), "test-1")
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_0 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="cmd-status",
        data_type="color",
        tag="test-tag",
        status="executing")
    terminate, send = request.on_message(pass_data_0, None)
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_1 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="cmd-status",
        tag="test-tag",
        status="done")
    terminate, send = request.on_message(pass_data_1, None)
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 2)
    self.assertEqual(messages[0][0], pass_data_0)
    self.assertIsNone(messages[0][1])
    self.assertEqual(messages[1][0], pass_data_1)
    self.assertIsNone(messages[1][1])
    request.close()

  def test_request_tagged_without_timeout_expect_messages(self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera", "left", "color", "test-tag", 100.0, expect_messages=1)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertEqual(request.tag, "test-tag")
    terminate, send = request.on_poll()
    self.assertFalse(terminate)
    self.assertIsNone(send)
    terminate, send = request.on_message(
        types_gen.DeviceData(
            device_type="color-camera",
            device_name="left",
            data_type="color",
            tag="ignore"), "test-0")
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_0 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="color",
        tag="test-tag")
    terminate, send = request.on_message(pass_data_0, "test-1")
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_1 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="cmd-status",
        tag="test-tag",
        status="done")
    terminate, send = request.on_message(pass_data_1, None)
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 2)
    self.assertEqual(messages[0][0], pass_data_0)
    self.assertEqual(messages[0][1], "test-1")
    self.assertEqual(messages[1][0], pass_data_1)
    self.assertIsNone(messages[1][1])
    request.close()

  def test_request_tagged_without_timeout_expect_messages_swap(self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera", "left", "color", "test-tag", 100.0, expect_messages=1)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertEqual(request.tag, "test-tag")
    terminate, send = request.on_poll()
    self.assertFalse(terminate)
    self.assertIsNone(send)
    terminate, send = request.on_message(
        types_gen.DeviceData(
            device_type="color-camera",
            device_name="left",
            data_type="color",
            tag="ignore"), "test-0")
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_0 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="cmd-status",
        tag="test-tag",
        status="done")
    terminate, send = request.on_message(pass_data_0, None)
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_1 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="color",
        tag="test-tag")
    terminate, send = request.on_message(pass_data_1, "test-1")
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 2)
    self.assertEqual(messages[0][0], pass_data_1)
    self.assertEqual(messages[0][1], "test-1")
    self.assertEqual(messages[1][0], pass_data_0)
    self.assertIsNone(messages[1][1])
    request.close()

  def test_request_tagged_without_timeout_expect_messages_error(self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera", "left", "color", "test-tag", 100.0, expect_messages=1)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertEqual(request.tag, "test-tag")
    terminate, send = request.on_poll()
    self.assertFalse(terminate)
    self.assertIsNone(send)
    terminate, send = request.on_message(
        types_gen.DeviceData(
            device_type="color-camera",
            device_name="left",
            data_type="color",
            tag="ignore"), "test-0")
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_0 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="cmd-status",
        tag="test-tag",
        status="done",
        error="died")
    terminate, send = request.on_message(pass_data_0, None)
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 1)
    self.assertEqual(messages[0][0], pass_data_0)
    self.assertIsNone(messages[0][1])
    request.close()

  def test_request_tagged_without_timeout_expect_messages_skip_status(
      self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera",
        "left",
        "color",
        "test-tag",
        100.0,
        expect_messages=1,
        expect_cmd_status=False)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertEqual(request.tag, "test-tag")
    terminate, send = request.on_poll()
    self.assertFalse(terminate)
    self.assertIsNone(send)
    terminate, send = request.on_message(
        types_gen.DeviceData(
            device_type="color-camera",
            device_name="left",
            data_type="color",
            tag="ignore"), "test-0")
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_0 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="color",
        tag="test-tag")
    terminate, send = request.on_message(pass_data_0, "test-1")
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 1)
    self.assertEqual(messages[0][0], pass_data_0)
    self.assertEqual(messages[0][1], "test-1")
    request.close()

  def test_request_tagged_without_timeout_expect_messages_skip_status_error(
      self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera",
        "left",
        "color",
        "test-tag",
        100.0,
        expect_messages=1,
        expect_cmd_status=False)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertEqual(request.tag, "test-tag")
    terminate, send = request.on_poll()
    self.assertFalse(terminate)
    self.assertIsNone(send)
    terminate, send = request.on_message(
        types_gen.DeviceData(
            device_type="color-camera",
            device_name="left",
            data_type="color",
            tag="ignore"), "test-0")
    self.assertFalse(terminate)
    self.assertIsNone(send)
    pass_data_0 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="cmd-status",
        tag="test-tag",
        status="done",
        error="died")
    terminate, send = request.on_message(pass_data_0, None)
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 1)
    self.assertEqual(messages[0][0], pass_data_0)
    self.assertIsNone(messages[0][1])
    request.close()

  def test_request_tagged_with_timeout(self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera", "left", "color", "test-tag", 0)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertEqual(request.tag, "test-tag")
    pass_data_0 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="cmd-status",
        data_type="color",
        tag="test-tag",
        status="executing")
    terminate, send = request.on_message(pass_data_0, None)
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 1)
    self.assertEqual(messages[0][0], pass_data_0)
    self.assertIsNone(messages[0][1])
    request.close()

  def test_request_tagged_with_timeout_swap(self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera", "left", "color", "test-tag", 0)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertEqual(request.tag, "test-tag")
    pass_data_0 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="cmd-status",
        data_type="color",
        tag="test-tag",
        status="executing")
    terminate, send = request.on_message(pass_data_0, None)
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 1)
    self.assertEqual(messages[0][0], pass_data_0)
    self.assertIsNone(messages[0][1])
    request.close()

  def test_request_tagged_with_timeout_expect_messages(self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera", "left", "color", "test-tag", 0, expect_messages=1)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertEqual(request.tag, "test-tag")
    pass_data_0 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="color",
        tag="test-tag")
    terminate, send = request.on_message(pass_data_0, "test-1")
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 1)
    self.assertEqual(messages[0][0], pass_data_0)
    self.assertEqual(messages[0][1], "test-1")
    request.close()

  def test_request_tagged_with_timeout_expect_messages_swap(self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera", "left", "color", "test-tag", 0, expect_messages=1)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertEqual(request.tag, "test-tag")
    pass_data_0 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="cmd-status",
        tag="test-tag",
        status="done")
    terminate, send = request.on_message(pass_data_0, None)
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 0)
    request.close()

  def test_request_tagged_with_timeout_expect_messages_error(self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera", "left", "color", "test-tag", 0, expect_messages=1)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertEqual(request.tag, "test-tag")
    pass_data_0 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="cmd-status",
        tag="test-tag",
        status="done",
        error="died")
    terminate, send = request.on_message(pass_data_0, None)
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 1)
    self.assertEqual(messages[0][0], pass_data_0)
    self.assertIsNone(messages[0][1])
    request.close()

  def test_request_tagged_with_timeout_expect_messages_skip_status(
      self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera",
        "left",
        "color",
        "test-tag",
        0,
        expect_messages=1,
        expect_cmd_status=False)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertEqual(request.tag, "test-tag")
    pass_data_0 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="color",
        tag="test-tag")
    terminate, send = request.on_message(pass_data_0, "test-1")
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 1)
    self.assertEqual(messages[0][0], pass_data_0)
    self.assertEqual(messages[0][1], "test-1")
    request.close()

  def test_request_tagged_with_timeout_expect_messages_skip_status_error(
      self) -> None:
    request: "requester.DeviceRequest[str]" = requester.DeviceRequest(
        "color-camera",
        "left",
        "color",
        "test-tag",
        0,
        expect_messages=1,
        expect_cmd_status=False)
    self.assertEqual(request.device_type, "color-camera")
    self.assertEqual(request.device_name, "left")
    self.assertEqual(request.tag, "test-tag")
    pass_data_0 = types_gen.DeviceData(
        device_type="color-camera",
        device_name="left",
        data_type="cmd-status",
        tag="test-tag",
        status="done",
        error="died")
    terminate, send = request.on_message(pass_data_0, None)
    self.assertTrue(terminate)
    self.assertIsNone(send)
    messages = thread_util.extract_all_from_queue(request.queue)
    self.assertEqual(len(messages), 1)
    self.assertEqual(messages[0][0], pass_data_0)
    self.assertIsNone(messages[0][1])
    request.close()

  def test_requester(self) -> None:
    callback_capturer: "thread_util.CallbackCapturer[str]" = (
        thread_util.CallbackCapturer())
    device = _MockRequester()
    device.add_update_callback(callback_capturer.callback_false,
                               callback_capturer.finished_callback)
    device.start()
    self.assertIsNone(device.get_cached())

    device.send_key_value("", "{}")
    device.send_wrong_key("")

    device.close()

    self.assertEqual(device.get_cached(), "{}")
    states = callback_capturer.wait()
    self.assertEqual(len(states), 0)


if __name__ == "__main__":
  unittest.main()
