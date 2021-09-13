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

"""Tests for logs_directory_client."""

import json
import os
import queue
import tempfile
from typing import Callable, Optional, List, Union
import unittest

from pyreach import core
from pyreach.common.python import types_gen
from pyreach.impl import logs_directory_client
from pyreach.impl import playback_client
from pyreach.impl import playback_client_test
from pyreach.impl import snapshot_impl
from pyreach.impl import utils


class LogsDirectoryClientTest(unittest.TestCase):
  _device_data: List[types_gen.DeviceData] = [
      types_gen.DeviceData(
          device_type="robot", data_type="robot-state", ts=2, seq=1),
      types_gen.DeviceData(
          device_type="robot",
          data_type="robot-state",
          ts=3,
          seq=2,
          inhibit_frame_send=True),
      types_gen.DeviceData(
          device_type="session-manager",
          data_type="connected-clients",
          ts=4,
          seq=3,
          connected_clients=types_gen.ConnectedClients([
              types_gen.ConnectedClient(
                  control_session_active=True, uid="test-1"),
              types_gen.ConnectedClient(uid="test-2"),
          ])),
      types_gen.DeviceData(
          device_type="robot",
          data_type="robot-state",
          ts=5,
          seq=4,
          send_to_clients=[types_gen.SendToClient("test-tag-1", "test-1")]),
      types_gen.DeviceData(
          device_type="robot",
          data_type="robot-state",
          ts=6,
          seq=5,
          send_to_clients=[types_gen.SendToClient("test-tag-2", "test-2")]),
      types_gen.DeviceData(
          device_type="robot",
          data_type="robot-state",
          ts=7,
          seq=6,
          send_to_clients=[
              types_gen.SendToClient("test-tag-3", "test-1"),
              types_gen.SendToClient("test-tag-4", "test-2")
          ]),
      types_gen.DeviceData(
          device_type="depth-camera",
          data_type="color-depth",
          ts=8,
          seq=7,
          color="color-8.jpg",
          depth="depth-8.pgm",
          send_to_clients=[types_gen.SendToClient("test-req-1", "test-1")]),
      types_gen.DeviceData(
          device_type="depth-camera",
          data_type="color-depth",
          ts=9,
          seq=8,
          color="depth-camera/color-9.jpg",
          depth="depth-camera/depth-9.pgm",
          send_to_clients=[types_gen.SendToClient("test-req-2", "test-1")]),
      types_gen.DeviceData(
          device_type="depth-camera",
          data_type="color-depth",
          ts=10,
          seq=9,
          color="/tmp/log/depth-camera/color-10.jpg",
          depth="/tmp/log/depth-camera/depth-10.pgm",
          send_to_clients=[types_gen.SendToClient("test-req-3", "test-1")]),
      types_gen.DeviceData(
          tag="test-in-tag-1",
          device_type="robot",
          data_type="cmd-status",
          ts=11,
          seq=10),
      types_gen.DeviceData(
          tag="test-in-tag-2",
          device_type="robot",
          data_type="cmd-status",
          ts=12,
          seq=11),
      types_gen.DeviceData(
          device_type="session-manager",
          data_type="connected-clients",
          ts=13,
          seq=12,
          connected_clients=types_gen.ConnectedClients([])),
      types_gen.DeviceData(
          device_type="robot", data_type="robot-state", ts=14, seq=13),
  ]

  _device_data_client_1: List[types_gen.DeviceData] = [
      types_gen.DeviceData(
          device_type="session-manager",
          data_type="connected-clients",
          ts=4,
          seq=3,
          connected_clients=types_gen.ConnectedClients([
              types_gen.ConnectedClient(
                  control_session_active=True, is_current=True, uid="test-1"),
              types_gen.ConnectedClient(uid="test-2"),
          ])),
      types_gen.DeviceData(
          tag="test-tag-1",
          device_type="robot",
          data_type="robot-state",
          ts=5,
          seq=4),
      types_gen.DeviceData(
          tag="test-tag-3",
          device_type="robot",
          data_type="robot-state",
          ts=7,
          seq=6),
      types_gen.DeviceData(
          tag="test-req-1",
          device_type="depth-camera",
          data_type="color-depth",
          ts=8,
          seq=7,
          color="color-8.jpg",
          depth="depth-8.pgm"),
      types_gen.DeviceData(
          tag="test-req-2",
          device_type="depth-camera",
          data_type="color-depth",
          ts=9,
          seq=8,
          color="depth-camera/color-9.jpg",
          depth="depth-camera/depth-9.pgm"),
      types_gen.DeviceData(
          tag="test-req-3",
          device_type="depth-camera",
          data_type="color-depth",
          ts=10,
          seq=9,
          color="/tmp/log/depth-camera/color-10.jpg",
          depth="/tmp/log/depth-camera/depth-10.pgm"),
      types_gen.DeviceData(
          tag="test-in-tag-1",
          device_type="robot",
          data_type="cmd-status",
          ts=11,
          seq=10),
  ]

  _device_data_client_2: List[types_gen.DeviceData] = [
      types_gen.DeviceData(
          device_type="session-manager",
          data_type="connected-clients",
          ts=4,
          seq=3,
          connected_clients=types_gen.ConnectedClients([
              types_gen.ConnectedClient(
                  control_session_active=True, uid="test-1"),
              types_gen.ConnectedClient(is_current=True, uid="test-2"),
          ])),
      types_gen.DeviceData(
          tag="test-tag-2",
          device_type="robot",
          data_type="robot-state",
          ts=6,
          seq=5),
      types_gen.DeviceData(
          tag="test-tag-4",
          device_type="robot",
          data_type="robot-state",
          ts=7,
          seq=6),
      types_gen.DeviceData(
          tag="test-in-tag-2",
          device_type="robot",
          data_type="cmd-status",
          ts=12,
          seq=11),
  ]

  _cmd_data: List[types_gen.CommandData] = [
      types_gen.CommandData(
          ts=2,
          seq=1,
          origin_client="test-1",
          tag="test-in-tag-1",
          device_type="robot",
          data_type="reach-script",
          snapshot=types_gen.Snapshot(
              gym_run_id="test-gym-1",
              gym_episode=2,
              gym_step=1,
          ),
      ),
      types_gen.CommandData(
          ts=3,
          seq=2,
          origin_client="test-2",
          tag="test-in-tag-2",
          device_type="robot",
          data_type="reach-script",
          snapshot=types_gen.Snapshot(
              gym_run_id="test-gym-2",
              gym_episode=2,
              gym_step=1,
          ),
      ),
      types_gen.CommandData(
          ts=4,
          seq=3,
          origin_client="test-1",
          tag="test-req-1",
          device_type="robot",
          data_type="reach-script",
          snapshot=types_gen.Snapshot(
              gym_run_id="test-gym-1",
              gym_episode=2,
              gym_step=2,
          ),
      ),
      types_gen.CommandData(
          ts=5,
          seq=4,
          origin_client="test-1",
          tag="test-req-2",
          device_type="robot",
          data_type="reach-script",
          snapshot=types_gen.Snapshot(
              gym_run_id="test-gym-1",
              gym_episode=3,
              gym_step=1,
          ),
      ),
      types_gen.CommandData(
          ts=5,
          seq=4,
          origin_client="test-1",
          device_type="robot",
          data_type="reach-script",
          snapshot=types_gen.Snapshot(
              gym_run_id="test-gym-3",
              gym_episode=2,
              gym_step=1,
          ),
      ),
  ]

  def test_empty(self) -> None:
    with tempfile.TemporaryDirectory() as tempdir:
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    False, None, False)
      try:
        self.assertIsNone(c.client_id)
        self.assertIsNone(c.gym_run_id)
        self._test_empty(c)
      finally:
        c.close()
      for client_id in ["test-invalid", None]:
        for select_client in [True, False]:
          for gym_run_id in ["test-invalid-gym", None]:
            for select_gym in [True, False]:
              if (not client_id and not select_client and not gym_run_id and
                  not select_gym):
                continue
              self.assertRaises(core.PyReachError,
                                logs_directory_client.LogsDirectoryClient,
                                "test-robot", tempdir, client_id, select_client,
                                gym_run_id, select_gym)

  def _test_empty(self, c: logs_directory_client.LogsDirectoryClient) -> None:
    self.assertFalse(c.device_data_available())
    self.assertIsNone(c.next_device_data())
    self.assertRaises(
        NotImplementedError, c.send_cmd,
        types_gen.CommandData(
            data_type="frame-request", device_type="robot", ts=1))
    self.assertFalse(c.device_data_available())
    self.assertRaises(queue.Empty, c.get_queue().get, False, 0.0)
    self.assertRaises(core.PyReachError, c.seek_device_data, None, None)
    self.assertRaises(queue.Empty, c.get_queue().get, False, 0.0)
    self.assertIsNone(c.seek_device_data(1.0, None))
    self.assertRaises(queue.Empty, c.get_queue().get, False, 0.0)
    self.assertIsNone(c.seek_device_data(1.0, 1))
    self.assertRaises(queue.Empty, c.get_queue().get, False, 0.0)
    self.assertIsNone(c.seek_device_data(None, 1))
    self.assertRaises(queue.Empty, c.get_queue().get, False, 0.0)
    self.assertIsNone(c.next_snapshot())
    self.assertIsNone(c.seek_snapshot(None, None, None))
    self.assertIsNone(c.seek_snapshot("test", None, None))
    self.assertIsNone(c.seek_snapshot(None, 1, None))
    self.assertIsNone(c.seek_snapshot(None, 0, 1))
    self.assertRaises(queue.Empty, c.get_queue().get, False, 0.0)
    c.close()
    self.assertIsNone(c.get_queue().get(True, 1.0))
    self.assertRaises(queue.Empty, c.get_queue().get, False, 0.0)

  def test_client_1(self) -> None:
    with tempfile.TemporaryDirectory() as tempdir:
      cmd_data = [
          utils.copy_command_data(cmd)
          for cmd in self._cmd_data
          if cmd.origin_client == "test-1"
      ]
      tags = set([cmd.tag for cmd in cmd_data])
      for cmd in cmd_data:
        cmd.origin_client = ""
      self._write_data(tempdir, self._device_data_client_1, cmd_data)
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    False, None, False)
      try:
        self.assertIsNone(c.client_id)
        self.assertIsNone(c.gym_run_id)
        self._test_client(c, tempdir,
                          self._remove_current(self._device_data_client_1),
                          cmd_data)
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    True, None, False)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertIsNone(c.gym_run_id)
        self._test_client(c, tempdir, [
            data for data in self._device_data_client_1
            if data.tag in tags or not data.tag
        ], cmd_data)
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir,
                                                    "test-1", False, None,
                                                    False)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertIsNone(c.gym_run_id)
        self._test_client(c, tempdir, [
            data for data in self._device_data_client_1
            if data.tag in tags or not data.tag
        ], cmd_data)
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir,
                                                    "test-1", True, None, False)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertIsNone(c.gym_run_id)
        self._test_client(c, tempdir, [
            data for data in self._device_data_client_1
            if data.tag in tags or not data.tag
        ], cmd_data)
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    False, None, True)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertEqual(c.gym_run_id, "test-gym-1")
        self._test_client(c, tempdir, [
            data for data in self._device_data_client_1
            if data.tag in tags or not data.tag
        ], [
            cmd for cmd in cmd_data
            if cmd.snapshot is None or cmd.snapshot.gym_run_id == "test-gym-1"
        ])
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    False, "test-gym-1", True)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertEqual(c.gym_run_id, "test-gym-1")
        self._test_client(c, tempdir, [
            data for data in self._device_data_client_1
            if data.tag in tags or not data.tag
        ], [
            cmd for cmd in cmd_data
            if cmd.snapshot is None or cmd.snapshot.gym_run_id == "test-gym-1"
        ])
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    False, "test-gym-1", False)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertEqual(c.gym_run_id, "test-gym-1")
        self._test_client(c, tempdir, [
            data for data in self._device_data_client_1
            if data.tag in tags or not data.tag
        ], [
            cmd for cmd in cmd_data
            if cmd.snapshot is None or cmd.snapshot.gym_run_id == "test-gym-1"
        ])
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    False, "test-gym-3", False)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertEqual(c.gym_run_id, "test-gym-3")
        self._test_client(c, tempdir, [
            data for data in self._device_data_client_1
            if data.tag in tags or not data.tag
        ], [
            cmd for cmd in cmd_data
            if cmd.snapshot is None or cmd.snapshot.gym_run_id == "test-gym-3"
        ])
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    False, "test-gym-3", True)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertEqual(c.gym_run_id, "test-gym-3")
        self._test_client(c, tempdir, [
            data for data in self._device_data_client_1
            if data.tag in tags or not data.tag
        ], [
            cmd for cmd in cmd_data
            if cmd.snapshot is None or cmd.snapshot.gym_run_id == "test-gym-3"
        ])
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir,
                                                    "test-1", False,
                                                    "test-gym-3", False)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertEqual(c.gym_run_id, "test-gym-3")
        self._test_client(c, tempdir, [
            data for data in self._device_data_client_1
            if data.tag in tags or not data.tag
        ], [
            cmd for cmd in cmd_data
            if cmd.snapshot is None or cmd.snapshot.gym_run_id == "test-gym-3"
        ])
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir,
                                                    "test-1", True,
                                                    "test-gym-3", False)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertEqual(c.gym_run_id, "test-gym-3")
        self._test_client(c, tempdir, [
            data for data in self._device_data_client_1
            if data.tag in tags or not data.tag
        ], [
            cmd for cmd in cmd_data
            if cmd.snapshot is None or cmd.snapshot.gym_run_id == "test-gym-3"
        ])
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    True, "test-gym-3", False)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertEqual(c.gym_run_id, "test-gym-3")
        self._test_client(c, tempdir, [
            data for data in self._device_data_client_1
            if data.tag in tags or not data.tag
        ], [
            cmd for cmd in cmd_data
            if cmd.snapshot is None or cmd.snapshot.gym_run_id == "test-gym-3"
        ])
      finally:
        c.close()

  def test_client_2(self) -> None:
    with tempfile.TemporaryDirectory() as tempdir:
      cmd_data = [
          utils.copy_command_data(cmd)
          for cmd in self._cmd_data
          if cmd.origin_client == "test-2"
      ]
      tags = set([cmd.tag for cmd in cmd_data])
      for cmd in cmd_data:
        cmd.origin_client = ""
      self._write_data(tempdir, self._device_data_client_2, cmd_data)
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    False, None, False)
      try:
        self.assertIsNone(c.client_id)
        self.assertIsNone(c.gym_run_id)
        self._test_client(c, tempdir,
                          self._remove_current(self._device_data_client_2),
                          cmd_data)
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    True, None, False)
      try:
        self.assertEqual(c.client_id, "test-2")
        self.assertIsNone(c.gym_run_id)
        self._test_client(c, tempdir, [
            data for data in self._device_data_client_2
            if data.tag in tags or not data.tag
        ], cmd_data)
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir,
                                                    "test-2", False, None,
                                                    False)
      try:
        self.assertEqual(c.client_id, "test-2")
        self.assertIsNone(c.gym_run_id)
        self._test_client(c, tempdir, [
            data for data in self._device_data_client_2
            if data.tag in tags or not data.tag
        ], cmd_data)
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir,
                                                    "test-2", True, None, False)
      try:
        self.assertEqual(c.client_id, "test-2")
        self.assertIsNone(c.gym_run_id)
        self._test_client(c, tempdir, [
            data for data in self._device_data_client_2
            if data.tag in tags or not data.tag
        ], cmd_data)
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    False, None, True)
      try:
        self.assertEqual(c.client_id, "test-2")
        self.assertEqual(c.gym_run_id, "test-gym-2")
        self._test_client(c, tempdir, [
            data for data in self._device_data_client_2
            if data.tag in tags or not data.tag
        ], [
            cmd for cmd in cmd_data
            if cmd.snapshot is None or cmd.snapshot.gym_run_id == "test-gym-2"
        ])
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    False, "test-gym-2", True)
      try:
        self.assertEqual(c.client_id, "test-2")
        self.assertEqual(c.gym_run_id, "test-gym-2")
        self._test_client(c, tempdir, [
            data for data in self._device_data_client_2
            if data.tag in tags or not data.tag
        ], [
            cmd for cmd in cmd_data
            if cmd.snapshot is None or cmd.snapshot.gym_run_id == "test-gym-2"
        ])
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    False, "test-gym-2", False)
      try:
        self.assertEqual(c.client_id, "test-2")
        self.assertEqual(c.gym_run_id, "test-gym-2")
        self._test_client(c, tempdir, [
            data for data in self._device_data_client_2
            if data.tag in tags or not data.tag
        ], [
            cmd for cmd in cmd_data
            if cmd.snapshot is None or cmd.snapshot.gym_run_id == "test-gym-2"
        ])
      finally:
        c.close()

  def test_serverside(self) -> None:
    with tempfile.TemporaryDirectory() as tempdir:
      self._write_data(tempdir, self._device_data, self._cmd_data)
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    False, None, False)
      try:
        self.assertIsNone(c.client_id)
        self.assertIsNone(c.gym_run_id)
        self._test_client(c, tempdir, self._device_data, self._cmd_data)
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    True, None, False)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertIsNone(c.gym_run_id)
        self._test_client(c, tempdir, self._device_data_client_1,
                          self._filter_cmd(self._cmd_data, "test-1", None))
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir,
                                                    "test-1", True, None, False)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertIsNone(c.gym_run_id)
        self._test_client(c, tempdir, self._device_data_client_1,
                          self._filter_cmd(self._cmd_data, "test-1", None))
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir,
                                                    "test-1", False, None,
                                                    False)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertIsNone(c.gym_run_id)
        self._test_client(c, tempdir, self._device_data_client_1,
                          self._filter_cmd(self._cmd_data, "test-1", None))
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir,
                                                    "test-1", False,
                                                    "test-gym-1", False)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertEqual(c.gym_run_id, "test-gym-1")
        self._test_client(
            c, tempdir, self._device_data_client_1,
            self._filter_cmd(self._cmd_data, "test-1", "test-gym-1"))
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir,
                                                    "test-1", False,
                                                    "test-gym-1", True)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertEqual(c.gym_run_id, "test-gym-1")
        self._test_client(
            c, tempdir, self._device_data_client_1,
            self._filter_cmd(self._cmd_data, "test-1", "test-gym-1"))
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir,
                                                    "test-1", False, None, True)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertEqual(c.gym_run_id, "test-gym-1")
        self._test_client(
            c, tempdir, self._device_data_client_1,
            self._filter_cmd(self._cmd_data, "test-1", "test-gym-1"))
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    False, "test-gym-1", False)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertEqual(c.gym_run_id, "test-gym-1")
        self._test_client(
            c, tempdir, self._device_data_client_1,
            self._filter_cmd(self._cmd_data, "test-1", "test-gym-1"))
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    False, "test-gym-1", True)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertEqual(c.gym_run_id, "test-gym-1")
        self._test_client(
            c, tempdir, self._device_data_client_1,
            self._filter_cmd(self._cmd_data, "test-1", "test-gym-1"))
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    False, None, True)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertEqual(c.gym_run_id, "test-gym-1")
        self._test_client(
            c, tempdir, self._device_data_client_1,
            self._filter_cmd(self._cmd_data, "test-1", "test-gym-1"))
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    True, "test-gym-1", False)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertEqual(c.gym_run_id, "test-gym-1")
        self._test_client(
            c, tempdir, self._device_data_client_1,
            self._filter_cmd(self._cmd_data, "test-1", "test-gym-1"))
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    True, "test-gym-1", True)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertEqual(c.gym_run_id, "test-gym-1")
        self._test_client(
            c, tempdir, self._device_data_client_1,
            self._filter_cmd(self._cmd_data, "test-1", "test-gym-1"))
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir, None,
                                                    True, None, True)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertEqual(c.gym_run_id, "test-gym-1")
        self._test_client(
            c, tempdir, self._device_data_client_1,
            self._filter_cmd(self._cmd_data, "test-1", "test-gym-1"))
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir,
                                                    "test-2", True, None, False)
      try:
        self.assertEqual(c.client_id, "test-2")
        self.assertIsNone(c.gym_run_id)
        self._test_client(c, tempdir, self._device_data_client_2,
                          self._filter_cmd(self._cmd_data, "test-2", None))
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir,
                                                    "test-2", False, None,
                                                    False)
      try:
        self.assertEqual(c.client_id, "test-2")
        self.assertIsNone(c.gym_run_id)
        self._test_client(c, tempdir, self._device_data_client_2,
                          self._filter_cmd(self._cmd_data, "test-2", None))
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir,
                                                    "test-2", False,
                                                    "test-gym-2", True)
      try:
        self.assertEqual(c.client_id, "test-2")
        self.assertEqual(c.gym_run_id, "test-gym-2")
        self._test_client(
            c, tempdir, self._device_data_client_2,
            self._filter_cmd(self._cmd_data, "test-2", "test-gym-2"))
      finally:
        c.close()
      c = logs_directory_client.LogsDirectoryClient("test-robot", tempdir,
                                                    "test-1", False,
                                                    "test-gym-3", True)
      try:
        self.assertEqual(c.client_id, "test-1")
        self.assertEqual(c.gym_run_id, "test-gym-3")
        self._test_client(
            c, tempdir, self._device_data_client_1,
            self._filter_cmd(self._cmd_data, "test-1", "test-gym-3"))
      finally:
        c.close()
      self.assertRaises(core.PyReachError,
                        logs_directory_client.LogsDirectoryClient, "test-robot",
                        tempdir, "test-3", False, None, False)
      self.assertRaises(core.PyReachError,
                        logs_directory_client.LogsDirectoryClient, "test-robot",
                        tempdir, "test-3", False, None, True)
      self.assertRaises(core.PyReachError,
                        logs_directory_client.LogsDirectoryClient, "test-robot",
                        tempdir, "test-3", False, None, True)
      self.assertRaises(core.PyReachError,
                        logs_directory_client.LogsDirectoryClient, "test-robot",
                        tempdir, "test-2", False, "test-gym-1", False)
      self.assertRaises(core.PyReachError,
                        logs_directory_client.LogsDirectoryClient, "test-robot",
                        tempdir, "test-1", False, "test-gym-2", False)
      self.assertRaises(core.PyReachError,
                        logs_directory_client.LogsDirectoryClient, "test-robot",
                        tempdir, "test-1", True, "test-gym-2", False)
      self.assertRaises(core.PyReachError,
                        logs_directory_client.LogsDirectoryClient, "test-robot",
                        tempdir, "test-2", True, "test-gym-1", True)
      self.assertRaises(core.PyReachError,
                        logs_directory_client.LogsDirectoryClient, "test-robot",
                        tempdir, "test-2", True, "test-gym-1", False)
      self.assertRaises(core.PyReachError,
                        logs_directory_client.LogsDirectoryClient, "test-robot",
                        tempdir, "test-1", False, "test-gym-2", True)

  def _remove_current(
      self,
      device_data: List[types_gen.DeviceData]) -> List[types_gen.DeviceData]:
    d = [utils.copy_device_data(data) for data in device_data]
    for data in d:
      if data.connected_clients and data.connected_clients.clients:
        for c in data.connected_clients.clients:
          c.is_current = False
    return d

  def _filter_cmd(self, command_data: List[types_gen.CommandData],
                  client_id: Optional[str],
                  gym_run_id: Optional[str]) -> List[types_gen.CommandData]:
    output = []
    for cmd in command_data:
      if ((client_id is None or not cmd.origin_client or
           cmd.origin_client == client_id) and
          (gym_run_id is None or cmd.snapshot is None or
           cmd.snapshot.gym_run_id == gym_run_id)):
        output.append(cmd)
    return output

  def _test_client(self, c: logs_directory_client.LogsDirectoryClient,
                   tempdir: str, device_data: List[types_gen.DeviceData],
                   command_data: List[types_gen.CommandData]) -> None:
    iteration = 0
    while True:
      have_data = c.device_data_available()
      data = c.next_device_data()
      if not data:
        self.assertFalse(have_data)
        self.assertEqual(iteration, len(device_data))
        break
      self.assertTrue(have_data)
      if iteration >= len(device_data):
        self.assertIsNone(data.to_json())
      self._assert_data(c, tempdir, data, device_data[iteration])
      iteration += 1
    for iteration in range(len(device_data) - 1, -1, -1):
      data = c.seek_device_data(
          utils.time_at_timestamp(device_data[iteration].ts), None)
      assert data
      self._assert_data(c, tempdir, data, device_data[iteration])
    for iteration in range(len(device_data) - 1, -1, -1):
      data = c.seek_device_data(
          utils.time_at_timestamp(device_data[iteration].ts),
          device_data[iteration].seq)
      assert data
      self._assert_data(c, tempdir, data, device_data[iteration])
    for iteration in range(len(device_data) - 1, -1, -1):
      data = c.seek_device_data(
          utils.time_at_timestamp(device_data[iteration].ts),
          device_data[iteration].seq + 1000)
      self.assertIsNone(data)
      self.assertRaises(queue.Empty, c.get_queue().get, False, 0.0)
    for cmd in command_data:
      if cmd.snapshot:
        snapshot = c.next_snapshot()
        self.assertEqual(snapshot, snapshot_impl.reverse_snapshot(cmd.snapshot))
    for iteration in range(len(command_data) - 1, -1, -1):
      cmd = command_data[iteration]
      if cmd.snapshot:
        snapshot = c.seek_snapshot(cmd.snapshot.gym_run_id,
                                   cmd.snapshot.gym_episode,
                                   cmd.snapshot.gym_step)
        self.assertEqual(snapshot, snapshot_impl.reverse_snapshot(cmd.snapshot))
    snapshot = c.seek_snapshot(None, None, None)
    self.assertEqual(snapshot,
                     snapshot_impl.reverse_snapshot(command_data[0].snapshot))
    self.assertIsNone(c.seek_device_data(1.0, None))
    self.assertRaises(queue.Empty, c.get_queue().get, False, 0.0)
    c.close()
    self.assertIsNone(c.get_queue().get(True, 1.0))
    self.assertRaises(queue.Empty, c.get_queue().get, False, 0.0)

  def _write_data(self, tempdir: str, device_data: List[types_gen.DeviceData],
                  cmd_data: List[types_gen.CommandData]) -> None:
    os.mkdir(os.path.join(tempdir, "device-data"))
    with open(os.path.join(tempdir, "device-data", "00000.json"), "w") as f:
      for data in device_data:
        f.write(json.dumps(data.to_json()) + "\n")
    os.mkdir(os.path.join(tempdir, "command-data"))
    with open(os.path.join(tempdir, "command-data", "00000.json"), "w") as f:
      for cmd in cmd_data:
        f.write(json.dumps(cmd.to_json()) + "\n")

  def _assert_data(self, c: logs_directory_client.LogsDirectoryClient,
                   tempdir: str, data: types_gen.DeviceData,
                   expect_data: types_gen.DeviceData) -> None:
    expect_data = utils.copy_device_data(expect_data)
    if expect_data.depth:
      expect_data.depth = os.path.join(tempdir, "depth-camera",
                                       "depth-" + str(expect_data.ts) + ".pgm")
    if expect_data.color:
      expect_data.color = os.path.join(tempdir, "depth-camera",
                                       "color-" + str(expect_data.ts) + ".jpg")
    playback_client_test.log_data_equal(self, data, expect_data)
    self.assertEqual(c.get_queue().get(True, 1.0), data)
    self.assertRaises(queue.Empty, c.get_queue().get, False, 0.0)

  def test_data_reader(self) -> None:
    device_data = [
        types_gen.DeviceData(
            ts=1000,
            seq=2,
            data_type="robot-state",
            device_type="robot",
            device_name="test"),
        types_gen.DeviceData(
            ts=2001,
            seq=1,
            data_type="robot-state",
            device_type="robot",
            device_name="test"),
        types_gen.DeviceData(
            ts=2000,
            seq=3,
            data_type="robot-state",
            device_type="robot",
            device_name="test"),
    ]

    def factory(
        working_directory: str) -> logs_directory_client._DeviceDataReader:
      return logs_directory_client._DeviceDataReader(working_directory,
                                                     working_directory)

    self._test_directory_iterator(device_data, factory)

  def test_command_reader(self) -> None:
    command_data = [
        types_gen.CommandData(
            ts=1000,
            seq=2,
            data_type="frame-request",
            device_type="robot",
            device_name="test"),
        types_gen.CommandData(
            ts=2001,
            seq=1,
            data_type="frame-request",
            device_type="robot",
            device_name="test"),
        types_gen.CommandData(
            ts=2000,
            seq=3,
            data_type="frame-request",
            device_type="robot",
            device_name="test"),
    ]
    self._test_directory_iterator(command_data,
                                  logs_directory_client._CommandDataReader)

  def test_empty_data_reader(self) -> None:

    def factory(
        working_directory: str) -> logs_directory_client._DeviceDataReader:
      return logs_directory_client._DeviceDataReader(working_directory,
                                                     working_directory)

    empty_data: List[types_gen.DeviceData] = []
    self._test_directory_iterator(empty_data, factory)

  def test_empty_command_reader(self) -> None:
    empty_cmd: List[types_gen.CommandData] = []
    self._test_directory_iterator(empty_cmd,
                                  logs_directory_client._CommandDataReader)

  def _test_directory_iterator(
      self, data: Union[List[types_gen.DeviceData],
                        List[types_gen.CommandData]],
      factory: Callable[[str],
                        Union[playback_client.Iterator[types_gen.DeviceData],
                              playback_client.Iterator[types_gen.CommandData]]]
  ) -> None:
    test_invalid_seqs = [
        (0.0, 0),
        (1.0, 0),
        (1.0, 1),
        (2.001, 3),
        (2.0, 2),
        (1.001, None),
        (1.2, None),
        (None, 4),
        (None, 0),
        (0.0, None),
    ]

    with tempfile.TemporaryDirectory() as tempdir:
      if data:
        self.assertGreater(len(data), 2)
        with open(os.path.join(tempdir, "00000.json"), "w") as f:
          for element in data[0:2]:
            f.write(json.dumps(element.to_json()) + "\n")
        with open(os.path.join(tempdir, "00001.json"), "w") as f:
          for element in data[2:]:
            f.write(json.dumps(element.to_json()) + "\n")

      def factory_wrapper(
      ) -> Union[playback_client.Iterator[types_gen.DeviceData],
                 playback_client.Iterator[types_gen.CommandData]]:
        return factory(tempdir)

      if data:
        playback_client_test.log_iterator_test(self, data, test_invalid_seqs,
                                               factory_wrapper, False)
      else:
        playback_client_test.empty_log_iterator_test(self, factory_wrapper)


if __name__ == "__main__":
  unittest.main()
