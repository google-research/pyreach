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
import unittest
from pyreach.common.python import types_gen
from pyreach.impl import machine_interfaces
from pyreach.impl import machine_interfaces_impl
from pyreach.impl import test_utils

_test_machine_interfaces = types_gen.MachineInterfaces(interfaces=[
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
        data_type="color", device_type="uvc", py_type="frame-request"),
    types_gen.MachineInterface(
        data_type="color",
        device_name="vnc0",
        device_type="vnc",
        py_type="frame-request"),
    types_gen.MachineInterface(
        data_type="ur-state", device_type="ur", py_type="publish"),
    types_gen.MachineInterface(
        data_type="key-value",
        device_type="settings-engine",
        py_type="key-value-request",
        keys=["robot-name", "display-name"]),
])


class TestPipelineDescription(test_utils.TestResponder):
  """Test responder for pipeline descriptions."""

  def step(self, cmd: types_gen.CommandData) -> List[types_gen.DeviceData]:
    """Generate one pipeline description.

    Args:
      cmd: The CommandData to get the device type/name from.

    Returns:
      A list containing a rejected Device Data message if
      the cmd is untagged; otherwise an empty list is returned.
    """
    if cmd.device_type == "discovery-aggregator" and not cmd.device_name and cmd.data_type == "machine-interfaces-request":
      output = [
          types_gen.DeviceData(
              ts=cmd.ts,
              tag=cmd.tag,
              device_type="discovery-aggregator",
              data_type="machine-interfaces",
              machine_interfaces=_test_machine_interfaces)
      ]
      if cmd.tag:
        output.append(
            types_gen.DeviceData(
                ts=cmd.ts,
                tag=cmd.tag,
                device_type="discovery-aggregator",
                data_type="cmd-status",
                status="done"))
      return output
    return []

  def start(self) -> List[types_gen.DeviceData]:
    return []


class MachineInterfacesImplTest(unittest.TestCase):

  def test_machine_interface_test_responder(self) -> None:
    test_utils.run_test_client_test([TestPipelineDescription()], [
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1,
                tag="test",
                device_type="discovery-aggregator",
                data_type="machine-interfaces-request"), (
                    types_gen.DeviceData(
                        ts=1,
                        tag="test",
                        device_type="discovery-aggregator",
                        data_type="machine-interfaces",
                        machine_interfaces=_test_machine_interfaces),
                    types_gen.DeviceData(
                        ts=1,
                        tag="test",
                        device_type="discovery-aggregator",
                        data_type="cmd-status",
                        status="done"),
                )),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=2,
                device_type="discovery-aggregator",
                data_type="machine-interfaces-request"), (
                    types_gen.DeviceData(
                        ts=2,
                        device_type="discovery-aggregator",
                        data_type="machine-interfaces",
                        machine_interfaces=_test_machine_interfaces),
                )),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=3,
                tag="ignore-1",
                device_type="discovery-aggregator",
                device_name="invalid",
                data_type="machine-interfaces-request"), ()),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=4,
                tag="ignore-2",
                device_type="discovery-aggregator",
                data_type="ping"), ()),
    ])

  def test_machine_interface(self) -> None:
    tdev, rdev = machine_interfaces_impl.MachineInterfacesDevice().get_wrapper()
    with test_utils.TestDevice(tdev) as test_device:
      self.assertIsNone(rdev.get())
      test_device.set_responder(TestPipelineDescription())
      test_device.send_cmd(
          types_gen.CommandData(
              device_type="discovery-aggregator",
              data_type="machine-interfaces-request"))
      interfaces = rdev.get()
      self.assertIsNotNone(interfaces)
      if not interfaces:
        return
      self.assertEqual(interfaces.time, 0.0)
      self.assertEqual(len(interfaces.machine_interfaces), 7)
      self.assertEqual(
          interfaces.machine_interfaces[0],
          machine_interfaces.MachineInterface(
              data_type="color-depth",
              device_type="photoneo",
              device_name="",
              interface_type=machine_interfaces.InterfaceType.FRAME_REQUEST,
              keys=()))
      self.assertEqual(
          interfaces.machine_interfaces[1],
          machine_interfaces.MachineInterface(
              data_type="color-depth",
              device_type="realsense",
              device_name="wrist",
              interface_type=machine_interfaces.InterfaceType.FRAME_REQUEST,
              keys=()))
      self.assertEqual(
          interfaces.machine_interfaces[2],
          machine_interfaces.MachineInterface(
              data_type="color",
              device_name="invoice",
              device_type="realsense",
              interface_type=machine_interfaces.InterfaceType.FRAME_REQUEST,
              keys=()))
      self.assertEqual(
          interfaces.machine_interfaces[3],
          machine_interfaces.MachineInterface(
              data_type="color",
              device_type="uvc",
              device_name="",
              interface_type=machine_interfaces.InterfaceType.FRAME_REQUEST,
              keys=()))
      self.assertEqual(
          interfaces.machine_interfaces[4],
          machine_interfaces.MachineInterface(
              data_type="color",
              device_name="vnc0",
              device_type="vnc",
              interface_type=machine_interfaces.InterfaceType.FRAME_REQUEST,
              keys=()))
      self.assertEqual(
          interfaces.machine_interfaces[5],
          machine_interfaces.MachineInterface(
              data_type="ur-state",
              device_type="ur",
              device_name="",
              interface_type=machine_interfaces.InterfaceType.PUBLISH,
              keys=()))
      self.assertEqual(
          interfaces.machine_interfaces[6],
          machine_interfaces.MachineInterface(
              data_type="key-value",
              device_type="settings-engine",
              device_name="",
              interface_type=machine_interfaces.InterfaceType.KEY_VALUE_REQUEST,
              keys=("robot-name", "display-name")))


if __name__ == "__main__":
  unittest.main()
