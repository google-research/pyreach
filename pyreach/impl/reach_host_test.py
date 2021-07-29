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

from pyreach.common.python import types_gen
from pyreach.impl.test_utils import TestResponder


class TestPingResponder(TestResponder):

  def step(self, cmd: types_gen.CommandData) -> List[types_gen.DeviceData]:
    if (cmd.device_type == "ping" and not cmd.device_name and
        cmd.data_type == "ping"):
      return [
          types_gen.DeviceData(
              device_type="ping",
              data_type="cmd-status",
              status="done",
              ts=cmd.ts,
              local_ts=cmd.ts,
              tag=cmd.tag)
      ]
    return []

  def start(self) -> List[types_gen.DeviceData]:
    return []


class TestSessionManager(TestResponder):
  _active: bool = False

  def _get_state(self, ts: int, tag: str) -> types_gen.DeviceData:
    return types_gen.DeviceData(
        ts=ts,
        tag=tag,
        device_type="session-manager",
        data_type="connected-clients",
        connected_clients=types_gen.ConnectedClients(clients=[
            types_gen.ConnectedClient(
                uid="ac375ffb-601a-4f4f-a7b8-a0cd20c09f64",
                is_current=True,
                control_session_active=self._active)
        ]))

  def step(self, cmd: types_gen.CommandData) -> List[types_gen.DeviceData]:
    if (cmd.device_type == "session-info" and not cmd.device_name and
        cmd.data_type == "session-info"):
      self._active = False
      return [self._get_state(cmd.ts, "")]
    if cmd.device_type == "operator" and cmd.data_type == "session-info":
      self._active = True
      return [self._get_state(cmd.ts, "")]
    if (cmd.device_type == "session-manager" and not cmd.device_name and
        cmd.data_type == "connected-clients-request"):
      return [self._get_state(cmd.ts, "")]
    return []

  def start(self) -> List[types_gen.DeviceData]:
    return []


class TestPipelineDescription(TestResponder):

  def step(self, cmd: types_gen.CommandData) -> List[types_gen.DeviceData]:
    """Generate one pipeline description.

    Args:
      cmd: The CommandData to get the device type/name from.

    Returns:
      A list containing a rejected Device Data message if
      the cmd is untagged; otherwise an empty list is returned.
    """
    if (cmd.device_type == "discovery-aggregator" and not cmd.device_name and
        cmd.data_type == "machine-interfaces-request"):
      return [
          types_gen.DeviceData(
              ts=cmd.ts,
              tag=cmd.tag,
              device_type="discovery-aggregator",
              data_type="machine-interfaces",
              machine_interfaces=types_gen.MachineInterfaces(interfaces=[
                  types_gen.MachineInterface(
                      data_type="prediction",
                      device_type="oracle",
                      device_name="pick-points",
                      py_type="inference-request"),
                  types_gen.MachineInterface(
                      data_type="color-depth",
                      device_type="photoneo",
                      py_type="frame-request"),
                  types_gen.MachineInterface(
                      data_type="color-depth",
                      device_name="wrist",
                      device_type="realsense",
                      py_type="frame-request"),
                  types_gen.MachineInterface(
                      data_type="color",
                      device_name="invoice",
                      device_type="realsense",
                      py_type="frame-request"),
                  types_gen.MachineInterface(
                      data_type="color",
                      device_type="uvc",
                      py_type="frame-request"),
                  types_gen.MachineInterface(
                      data_type="color",
                      device_name="vnc0",
                      device_type="vnc",
                      py_type="frame-request"),
                  types_gen.MachineInterface(
                      data_type="ur-state", device_type="ur", py_type="publish")
              ]))
      ]
    return []

  def start(self) -> List[types_gen.DeviceData]:
    return []
