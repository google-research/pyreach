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

from pyreach import core
from pyreach.common.python import types_gen
from pyreach.force_torque_sensor import ForceTorqueSensorState
from pyreach.impl import force_torque_sensor_impl
from pyreach.impl import test_utils
from pyreach.impl import thread_util


class ForceTorqueSensorImplTest(unittest.TestCase):

  def test_test_force_torque_sensor(self) -> None:
    test_utils.run_test_client_test([TestForceTorqueSensor("test-name")], [
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1,
                device_type="force-torque-sensor",
                device_name="test-name",
                data_type="frame-request"), (types_gen.DeviceData(
                    ts=1,
                    device_type="force-torque-sensor",
                    device_name="test-name",
                    data_type="sensor-state",
                    state=[
                        types_gen.CapabilityState(pin="fx", float_value=1.0),
                        types_gen.CapabilityState(pin="fy", float_value=2.0),
                        types_gen.CapabilityState(pin="fz", float_value=3.0),
                        types_gen.CapabilityState(pin="tx", float_value=4.0),
                        types_gen.CapabilityState(pin="ty", float_value=5.0),
                        types_gen.CapabilityState(pin="tz", float_value=6.0),
                    ]),)),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1,
                device_type="force-torque-sensor",
                device_name="test-name",
                data_type="frame-request",
                tag="test-tag"), (types_gen.DeviceData(
                    ts=1,
                    tag="test-tag",
                    device_type="force-torque-sensor",
                    device_name="test-name",
                    data_type="sensor-state",
                    state=[
                        types_gen.CapabilityState(pin="fx", float_value=1.0),
                        types_gen.CapabilityState(pin="fy", float_value=2.0),
                        types_gen.CapabilityState(pin="fz", float_value=3.0),
                        types_gen.CapabilityState(pin="tx", float_value=4.0),
                        types_gen.CapabilityState(pin="ty", float_value=5.0),
                        types_gen.CapabilityState(pin="tz", float_value=6.0),
                    ]),
                                  types_gen.DeviceData(
                                      ts=1,
                                      device_type="force-torque-sensor",
                                      device_name="test-name",
                                      data_type="cmd-status",
                                      tag="test-tag",
                                      status="done"))),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1,
                device_type="force-torque-sensor",
                device_name="test",
                data_type="frame-request"), ()),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1,
                device_type="force-torque-sensor",
                device_name="",
                data_type="frame-request"), ()),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1,
                device_type="test",
                device_name="test-name",
                data_type="frame-request"), ()),
    ])

  def test_force_torque_sensor(self) -> None:
    ## Setup, ensure no cached frame, and that tagged requests will be used.
    rdev, dev = force_torque_sensor_impl.ForceTorqueSensorDevice(
        "test-name").get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      global_callbacks: "thread_util.CallbackCapturer[ForceTorqueSensorState]" = thread_util.CallbackCapturer(
      )
      stop_callback = dev.add_update_callback(
          global_callbacks.callback_false, global_callbacks.finished_callback)
      assert dev.state is None
      test_device.set_responder(TestForceTorqueSensor("test-name"))
      ## Get the first state
      frame = dev.fetch_state()
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_type="force-torque-sensor",
              device_name="test-name")
      ])
      self._verify_state(frame, "test-name")
      self._verify_state(dev.state, "test-name")
      ## ensure cached is the first frame
      assert dev.state == frame
      ## Use callbacks to get the next frames
      callback: ("thread_util.DoubleCallbackCapturer[ForceTorqueSensorState, "
                 "core.PyReachStatus]") = thread_util.DoubleCallbackCapturer()
      dev.async_fetch_state(
          callback=callback.first_callback_finish,
          error_callback=callback.second_callback_finish)
      frames = callback.wait()
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_type="force-torque-sensor",
              device_name="test-name")
      ])
      assert len(frames) == 1
      self._verify_state(frames[0][0], "test-name")
      ## frame is cached
      cached_frame = frames[0][0]
      assert dev.state == cached_frame
      ## set the callback to None to test timeouts
      test_device.set_callback(None)
      self.assertRaises(core.PyReachError, dev.fetch_state, timeout=0)
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_type="force-torque-sensor",
              device_name="test-name")
      ])
      callback = thread_util.DoubleCallbackCapturer()
      dev.async_fetch_state(
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
              device_type="force-torque-sensor",
              device_name="test-name")
      ])
      assert dev.state == cached_frame
      stop_callback()
      global_frames = global_callbacks.wait()
      assert len(global_frames) == 2
      assert global_frames[0] == frame
      assert global_frames[1] == frames[0][0]

  def _verify_state(self, state: Optional[ForceTorqueSensorState],
                    name: str) -> None:
    self.assertIsNotNone(state)
    if not state:
      return
    self.assertEqual(state.device_name, name)
    self.assertEqual(state.force.x, 1.0)
    self.assertEqual(state.force.y, 2.0)
    self.assertEqual(state.force.z, 3.0)
    self.assertEqual(state.torque.x, 4.0)
    self.assertEqual(state.torque.y, 5.0)
    self.assertEqual(state.torque.z, 6.0)

  def _is_timeout(self, status: Optional[core.PyReachStatus]) -> None:
    assert status is not None
    assert status.status == "done"
    assert status.error == "timeout"


class TestForceTorqueSensor(test_utils.TestResponder):
  """Represents a fake force torque sensor used for testing."""

  _device_name: str

  def __init__(self, device_name: str) -> None:
    """Init a test depth camera."""
    self._device_name = device_name

  def _response(self, ts: int, tag: str) -> List[types_gen.DeviceData]:
    """Generate a test response."""
    output = [
        types_gen.DeviceData(
            device_type="force-torque-sensor",
            device_name=self._device_name,
            ts=ts,
            tag=tag,
            data_type="sensor-state",
            state=[
                types_gen.CapabilityState(pin="fx", float_value=1.0),
                types_gen.CapabilityState(pin="fy", float_value=2.0),
                types_gen.CapabilityState(pin="fz", float_value=3.0),
                types_gen.CapabilityState(pin="tx", float_value=4.0),
                types_gen.CapabilityState(pin="ty", float_value=5.0),
                types_gen.CapabilityState(pin="tz", float_value=6.0),
            ])
    ]
    if tag:
      output.append(
          types_gen.DeviceData(
              device_type="force-torque-sensor",
              device_name=self._device_name,
              ts=ts,
              tag=tag,
              data_type="cmd-status",
              status="done"))
    return output

  def step(self, cmd: types_gen.CommandData) -> List[types_gen.DeviceData]:
    """Test step, generates a response for testing framework data."""
    if test_utils.is_frame_request_for(cmd, "force-torque-sensor",
                                       self._device_name):
      return self._response(cmd.ts, cmd.tag)
    return []

  def start(self) -> List[types_gen.DeviceData]:
    return []


if __name__ == "__main__":
  unittest.main()
