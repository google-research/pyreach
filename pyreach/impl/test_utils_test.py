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

import json
import os
import queue
import tempfile
from typing import List
import unittest
import numpy  # type: ignore
from PIL import Image  # type: ignore
from pyreach.common.python import types_gen
from pyreach.impl import device_base
from pyreach.impl import test_utils


class _MockDeviceBase(device_base.DeviceBase):

  def __init__(self) -> None:
    super().__init__()
    self._message_queue: "queue.Queue[types_gen.DeviceData]" = queue.Queue()

  def on_message(self, msg: types_gen.DeviceData) -> None:
    """Invoke when a device data message is received."""
    self._message_queue.put(msg)

  def send_ping(self, tag: str) -> None:
    """Invoke when a device data message is received."""
    self.send_cmd(
        types_gen.CommandData(device_type="ping", data_type="ping", tag=tag))

  @property
  def message_queue(self) -> "queue.Queue[types_gen.DeviceData]":
    return self._message_queue


class TestUtilsTest(unittest.TestCase):

  def test_test_responder(self) -> None:
    responder = test_utils.TestResponder()
    self.assertEqual(responder.test_image_dir, "")
    responder.set_test_image_dir("testdir")
    self.assertEqual(responder.test_image_dir, "testdir")
    self.assertRaises(NotImplementedError, responder.start)
    self.assertRaises(
        NotImplementedError, responder.step,
        types_gen.CommandData(device_type="ping", data_type="ping"))

  def test_test_responder_step(self) -> None:
    test_command = types_gen.CommandData(device_type="ping", data_type="ping")
    test_data_0 = types_gen.DeviceData(
        device_type="ping", data_type="cmd-status")
    test_data_1 = types_gen.DeviceData(
        device_type="ping", data_type="cmd-status")
    test_responder_step = test_utils.TestResponderStep(command=test_command)
    self.assertEqual(test_responder_step.command, test_command)
    self.assertEqual(len(test_responder_step.data), 0)
    test_responder_step = test_utils.TestResponderStep(
        command=test_command, data=(test_data_0,))
    self.assertEqual(test_responder_step.command, test_command)
    self.assertEqual(len(test_responder_step.data), 1)
    self.assertEqual(test_responder_step.data[0], test_data_0)
    test_responder_step = test_utils.TestResponderStep(
        command=test_command, data=(test_data_0, test_data_1))
    self.assertEqual(test_responder_step.command, test_command)
    self.assertEqual(len(test_responder_step.data), 2)
    self.assertEqual(test_responder_step.data[0], test_data_0)
    self.assertEqual(test_responder_step.data[1], test_data_1)

  def test_reject_responder(self) -> None:
    test_command = types_gen.CommandData(device_type="ping", data_type="ping")
    test_command_tag = types_gen.CommandData(
        device_type="ping", data_type="ping", tag="test-tag")
    responder = test_utils.RejectResponder()
    self.assertEqual(len(responder.start()), 0)
    self.assertEqual(len(responder.step(test_command)), 0)
    response = responder.step(test_command_tag)
    self.assertEqual(len(response), 1)
    self.assertEqual(response[0].device_type, "ping")
    self.assertEqual(response[0].device_name, "")
    self.assertEqual(response[0].data_type, "cmd-status")
    self.assertEqual(response[0].tag, "test-tag")
    self.assertEqual(response[0].status, "rejected")

  def test_assert_image_equal(self) -> None:
    with tempfile.TemporaryDirectory() as tempdir:
      filename = os.path.join(tempdir, "test.bmp")
      im = numpy.array([[[1, 2, 3], [4, 5, 6]], [[11, 12, 13], [14, 15, 16]]],
                       dtype=numpy.dtype("|u1"))
      Image.fromarray(im).save(filename)
      test_utils.assert_image_equal(im, filename)

  def test_assert_image_depth_equal(self) -> None:
    with tempfile.TemporaryDirectory() as tempdir:
      filename = os.path.join(tempdir, "test.pgm")
      im = numpy.array([[1, 2], [3, 4]], dtype=numpy.dtype("|u1"))
      Image.fromarray(im).save(filename)
      test_utils.assert_image_depth_equal(im, filename)

  def test_run_test_client_test(self) -> None:
    test_command = types_gen.CommandData(device_type="ping", data_type="ping")
    test_command_tag = types_gen.CommandData(
        device_type="ping", data_type="ping", tag="test-tag")
    device_data = types_gen.DeviceData(
        device_type="ping",
        data_type="cmd-status",
        tag="test-tag",
        status="rejected")
    test_utils.run_test_client_test([test_utils.RejectResponder()], [
        test_utils.TestResponderStep(command=test_command),
        test_utils.TestResponderStep(
            command=test_command_tag, data=(device_data,))
    ])

  def test_test_client(self) -> None:
    with test_utils.TestClient([]) as test_client:
      test_utils._verify_download(test_client._data_downloader.test_image_dir)
      client_queue = test_client.get_queue()
      device_data: List[types_gen.DeviceData] = []
      while True:
        try:
          data = client_queue.get(block=False)
          self.assertIsNotNone(data)
          if data:
            device_data.append(data)
        except queue.Empty:
          break
      self.assertEqual(len(device_data), 6)

      def mk_key_value(device_type: str, device_name: str,
                       key: str) -> types_gen.DeviceData:
        with test_client._lock:
          return types_gen.DeviceData(
              device_type=device_type,
              device_name=device_name,
              data_type="key-value",
              key=key,
              value=test_client._key_values[device_base.KeyValueKey(
                  device_type=device_type, device_name=device_name, key=key)])

      expect_elements = [
          mk_key_value("settings-engine", "", "robot-name"),
          mk_key_value("settings-engine", "", "display-name"),
          mk_key_value("settings-engine", "", "calibration.json"),
          mk_key_value("settings-engine", "", "actionsets.json"),
          mk_key_value("settings-engine", "", "workcell_constraints.json"),
          mk_key_value("settings-engine", "", "workcell_io.json"),
      ]
      for expect_element, data in zip(expect_elements, device_data):
        expect_json = json.dumps(expect_element.to_json())
        data_json = json.dumps(data.to_json())
        self.assertEqual(data_json, expect_json,
                         "Got %s data, expected %s" % (data_json, expect_json))
      for expect_element in expect_elements:
        test_client.send_cmd(
            types_gen.CommandData(
                device_type=expect_element.device_type,
                device_name=expect_element.device_name,
                data_type="key-value-request",
                key=expect_element.key))
        data = client_queue.get(block=False)
        self.assertIsNotNone(data)
        if data:
          expect_json = json.dumps(expect_element.to_json())
          data_json = json.dumps(data.to_json())
          self.assertEqual(
              data_json, expect_json,
              "Got %s data, expected %s" % (data_json, expect_json))
    terminate = client_queue.get(block=False)
    self.assertIsNone(terminate)
    self.assertRaises(queue.Empty, client_queue.get, False)

  def test_test_device(self) -> None:
    dev = _MockDeviceBase()

    def test_callback(cmd: types_gen.CommandData) -> List[types_gen.DeviceData]:
      if cmd.device_type == "ping" and cmd.data_type == "ping":
        return [
            types_gen.DeviceData(
                device_type="ping",
                device_name=cmd.device_name,
                data_type="cmd-status",
                ts=cmd.ts,
                tag=cmd.tag,
                status="done")
        ]
      return []

    with test_utils.TestDevice(dev) as test_dev:
      test_utils._verify_download(test_dev._data_downloader.test_image_dir)
      test_dev.send_cmd(
          types_gen.CommandData(device_type="ping", data_type="ping"))
      dev.send_ping("")
      test_dev.set_callback(test_callback)
      test_dev.send_cmd(
          types_gen.CommandData(device_type="ping", data_type="ping"))
      ping = dev.message_queue.get(block=True, timeout=1)
      self.assertRaises(queue.Empty, dev.message_queue.get, False)
      self.assertIsNotNone(ping)
      self.assertEqual(
          json.dumps(ping.to_json()),
          "{\"dataType\": \"cmd-status\", \"deviceType\": "
          "\"ping\", \"status\": \"done\"}")
      test_dev.set_responder(test_utils.RejectResponder())
      test_dev.send_cmd(
          types_gen.CommandData(
              device_type="ping", data_type="ping", tag="test-reject-1"))
      ping = dev.message_queue.get(block=True, timeout=1)
      self.assertRaises(queue.Empty, dev.message_queue.get, False)
      self.assertIsNotNone(ping)
      self.assertEqual(
          json.dumps(ping.to_json()),
          "{\"dataType\": \"cmd-status\", \"deviceType\": "
          "\"ping\", \"status\": \"rejected\", "
          "\"tag\": \"test-reject-1\"}")
      dev.send_ping("test-reject-2")
      ping = dev.message_queue.get(block=True, timeout=1)
      self.assertRaises(queue.Empty, dev.message_queue.get, False)
      self.assertIsNotNone(ping)
      self.assertEqual(
          json.dumps(ping.to_json()),
          "{\"dataType\": \"cmd-status\", \"deviceType\": "
          "\"ping\", \"status\": \"rejected\", "
          "\"tag\": \"test-reject-2\"}")
      test_dev.set_callback(None)
      test_dev.send_cmd(
          types_gen.CommandData(device_type="ping", data_type="ping"))
      dev.send_ping("")
      self.assertRaises(queue.Empty, dev.message_queue.get, False)
    self.assertTrue(dev.is_closed())
    self.assertRaises(queue.Empty, dev.message_queue.get, False)


if __name__ == "__main__":
  unittest.main()
