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

from pyreach import core  # pylint: disable=unused-import
from pyreach import vacuum  # pylint: disable=unused-import
from pyreach.common.python import types_gen
from pyreach.impl import arm_impl
from pyreach.impl import calibration_impl
from pyreach.impl import test_utils
from pyreach.impl import thread_util
from pyreach.impl import vacuum_impl
from pyreach.common.proto_gen import workcell_io_pb2 as workcell_io


class TestPyreachVacuum(unittest.TestCase):

  def test_test_vacuum(self) -> None:
    test_utils.run_test_client_test(
        [TestVacuum("test-name", False, False, False, 0.0)], [
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=1,
                    device_type="vacuum",
                    device_name="test-name",
                    data_type="frame-request"), (types_gen.DeviceData(
                        ts=1,
                        device_type="vacuum",
                        device_name="test-name",
                        data_type="output-state"),)),
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=2,
                    tag="test-tag",
                    device_type="vacuum",
                    device_name="test-name",
                    data_type="frame-request"), (
                        types_gen.DeviceData(
                            ts=2,
                            tag="test-tag",
                            device_type="vacuum",
                            device_name="test-name",
                            data_type="output-state"),
                        types_gen.DeviceData(
                            ts=2,
                            tag="test-tag",
                            device_type="vacuum",
                            device_name="test-name",
                            data_type="cmd-status",
                            status="done"),
                    )),
        ])
    test_utils.run_test_client_test(
        [TestVacuum("test-name", True, False, False, 0.0)], [
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=1,
                    device_type="vacuum",
                    device_name="test-name",
                    data_type="frame-request"), (types_gen.DeviceData(
                        ts=1,
                        device_type="vacuum",
                        device_name="test-name",
                        data_type="output-state",
                        state=[types_gen.CapabilityState(int_value=1)]),)),
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=2,
                    tag="test-tag",
                    device_type="vacuum",
                    device_name="test-name",
                    data_type="frame-request"), (
                        types_gen.DeviceData(
                            ts=2,
                            tag="test-tag",
                            device_type="vacuum",
                            device_name="test-name",
                            data_type="output-state",
                            state=[types_gen.CapabilityState(int_value=1)]),
                        types_gen.DeviceData(
                            ts=2,
                            tag="test-tag",
                            device_type="vacuum",
                            device_name="test-name",
                            data_type="cmd-status",
                            status="done"),
                    )),
        ])

    test_utils.run_test_client_test(
        [TestVacuum("test-name", False, False, False, 0.0)], [
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=1,
                    device_type="blowoff",
                    device_name="test-name",
                    data_type="frame-request"), (types_gen.DeviceData(
                        ts=1,
                        device_type="blowoff",
                        device_name="test-name",
                        data_type="output-state"),)),
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=2,
                    tag="test-tag",
                    device_type="blowoff",
                    device_name="test-name",
                    data_type="frame-request"), (
                        types_gen.DeviceData(
                            ts=2,
                            tag="test-tag",
                            device_type="blowoff",
                            device_name="test-name",
                            data_type="output-state"),
                        types_gen.DeviceData(
                            ts=2,
                            tag="test-tag",
                            device_type="blowoff",
                            device_name="test-name",
                            data_type="cmd-status",
                            status="done"),
                    )),
        ])
    test_utils.run_test_client_test(
        [TestVacuum("test-name", False, True, False, 0.0)], [
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=1,
                    device_type="blowoff",
                    device_name="test-name",
                    data_type="frame-request"), (types_gen.DeviceData(
                        ts=1,
                        device_type="blowoff",
                        device_name="test-name",
                        data_type="output-state",
                        state=[types_gen.CapabilityState(int_value=1)]),)),
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=2,
                    tag="test-tag",
                    device_type="blowoff",
                    device_name="test-name",
                    data_type="frame-request"), (
                        types_gen.DeviceData(
                            ts=2,
                            tag="test-tag",
                            device_type="blowoff",
                            device_name="test-name",
                            data_type="output-state",
                            state=[types_gen.CapabilityState(int_value=1)]),
                        types_gen.DeviceData(
                            ts=2,
                            tag="test-tag",
                            device_type="blowoff",
                            device_name="test-name",
                            data_type="cmd-status",
                            status="done"),
                    )),
        ])

    test_utils.run_test_client_test(
        [TestVacuum("test-name", False, False, False, 0.0)], [
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=1,
                    device_type="vacuum-pressure",
                    device_name="test-name",
                    data_type="frame-request"), (types_gen.DeviceData(
                        ts=1,
                        device_type="vacuum-pressure",
                        device_name="test-name",
                        data_type="sensor-state"),)),
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=2,
                    tag="test-tag",
                    device_type="vacuum-pressure",
                    device_name="test-name",
                    data_type="frame-request"), (
                        types_gen.DeviceData(
                            ts=2,
                            tag="test-tag",
                            device_type="vacuum-pressure",
                            device_name="test-name",
                            data_type="sensor-state"),
                        types_gen.DeviceData(
                            ts=2,
                            tag="test-tag",
                            device_type="vacuum-pressure",
                            device_name="test-name",
                            data_type="cmd-status",
                            status="done"),
                    )),
        ])
    test_utils.run_test_client_test(
        [TestVacuum("test-name", False, False, True, 0.0)], [
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=1,
                    device_type="vacuum-pressure",
                    device_name="test-name",
                    data_type="frame-request"), (types_gen.DeviceData(
                        ts=1,
                        device_type="vacuum-pressure",
                        device_name="test-name",
                        data_type="sensor-state",
                        state=[types_gen.CapabilityState(int_value=1)]),)),
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=2,
                    tag="test-tag",
                    device_type="vacuum-pressure",
                    device_name="test-name",
                    data_type="frame-request"), (
                        types_gen.DeviceData(
                            ts=2,
                            tag="test-tag",
                            device_type="vacuum-pressure",
                            device_name="test-name",
                            data_type="sensor-state",
                            state=[types_gen.CapabilityState(int_value=1)]),
                        types_gen.DeviceData(
                            ts=2,
                            tag="test-tag",
                            device_type="vacuum-pressure",
                            device_name="test-name",
                            data_type="cmd-status",
                            status="done"),
                    )),
        ])

    test_utils.run_test_client_test(
        [TestVacuum("test-name", False, False, False, 0.0)], [
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=1,
                    device_type="vacuum-gauge",
                    device_name="test-name",
                    data_type="frame-request"), (types_gen.DeviceData(
                        ts=1,
                        device_type="vacuum-gauge",
                        device_name="test-name",
                        data_type="sensor-state"),)),
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=2,
                    tag="test-tag",
                    device_type="vacuum-gauge",
                    device_name="test-name",
                    data_type="frame-request"), (
                        types_gen.DeviceData(
                            ts=2,
                            tag="test-tag",
                            device_type="vacuum-gauge",
                            device_name="test-name",
                            data_type="sensor-state"),
                        types_gen.DeviceData(
                            ts=2,
                            tag="test-tag",
                            device_type="vacuum-gauge",
                            device_name="test-name",
                            data_type="cmd-status",
                            status="done"),
                    )),
        ])
    test_utils.run_test_client_test(
        [TestVacuum("test-name", False, False, False, 12.0)], [
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=1,
                    device_type="vacuum-gauge",
                    device_name="test-name",
                    data_type="frame-request"), (types_gen.DeviceData(
                        ts=1,
                        device_type="vacuum-gauge",
                        device_name="test-name",
                        data_type="sensor-state",
                        state=[types_gen.CapabilityState(float_value=12.0)]),)),
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=2,
                    tag="test-tag",
                    device_type="vacuum-gauge",
                    device_name="test-name",
                    data_type="frame-request"),
                (
                    types_gen.DeviceData(
                        ts=2,
                        tag="test-tag",
                        device_type="vacuum-gauge",
                        device_name="test-name",
                        data_type="sensor-state",
                        state=[types_gen.CapabilityState(float_value=12.0)]),
                    types_gen.DeviceData(
                        ts=2,
                        tag="test-tag",
                        device_type="vacuum-gauge",
                        device_name="test-name",
                        data_type="cmd-status",
                        status="done"),
                )),
        ])

  def test_vacuum(self) -> None:
    ## Setup, ensure no cached image, and that tagged requests will be used.
    calibration_device = calibration_impl.CalDevice()
    armdev, constraints_device, arm_wrapper = arm_impl.ArmDevice(
        arm_impl.ArmTypeImpl.from_urdf_file("ur5e.urdf"), calibration_device,
        None, None, "test-name").get_wrapper()
    workcell_io_config = workcell_io.IOConfig()  # type: ignore
    pressure_io = workcell_io_config.capability.add()
    pressure_io.device_type = "ur"
    pressure_io.device_name = "test-name"
    pressure_io.type = "vacuum-pressure"
    pressure_io.io_type = workcell_io.DIGITAL_INPUT  # type: ignore
    pressure_io = workcell_io_config.capability.add()
    pressure_io.device_type = "ur"
    pressure_io.device_name = "test-name"
    pressure_io.type = "vacuum-gauge"
    pressure_io.io_type = workcell_io.ANALOG_INPUT  # type: ignore
    rdev, dev = vacuum_impl.VacuumDevice(workcell_io_config,
                                         arm_wrapper).get_wrapper()
    calibration_device.close()
    constraints_device.close()
    armdev.close()
    with test_utils.TestDevice(rdev) as test_device:
      assert not dev.support_blowoff
      assert dev.support_pressure
      assert dev.support_gauge
      vacuum_state_callbacks: \
        "thread_util.CallbackCapturer[vacuum.VacuumState]" = \
        thread_util.CallbackCapturer()
      stop_vacuum_state_callback = dev.add_state_callback(
          vacuum_state_callbacks.callback_false,
          vacuum_state_callbacks.finished_callback)
      vacuum_blowoff_state_callbacks: \
        "thread_util.CallbackCapturer[vacuum.BlowoffState]" = \
        thread_util.CallbackCapturer()
      stop_vacuum_blowoff_state_callback = dev.add_blowoff_state_callback(
          vacuum_blowoff_state_callbacks.callback_false,
          vacuum_blowoff_state_callbacks.finished_callback)
      vacuum_pressure_state_callbacks: \
        "thread_util.CallbackCapturer[vacuum.VacuumPressure]" = \
        thread_util.CallbackCapturer()
      stop_vacuum_pressure_state_callback = dev.add_pressure_state_callback(
          vacuum_pressure_state_callbacks.callback_false,
          vacuum_pressure_state_callbacks.finished_callback)
      vacuum_gauge_state_callbacks: \
        "thread_util.CallbackCapturer[vacuum.VacuumGauge]" = \
        thread_util.CallbackCapturer()
      stop_vacuum_gauge_state_callback = dev.add_gauge_state_callback(
          vacuum_gauge_state_callbacks.callback_false,
          vacuum_gauge_state_callbacks.finished_callback)

      # Test vacuum false
      assert not dev.state
      test_device.set_responder(TestVacuum("test-name", False, False, False, 0))
      state = dev.fetch_state()
      assert state
      assert not state.state
      assert dev.state
      state = dev.state
      assert state
      assert not state.state
      state_callbacks: ("thread_util.DoubleCallbackCapturer[vacuum.VacuumState,"
                        " core.PyReachStatus]")
      state_callbacks = thread_util.DoubleCallbackCapturer()
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="vacuum")
      ])
      dev.async_fetch_state(
          callback=state_callbacks.first_callback_finish,
          error_callback=state_callbacks.second_callback_finish)
      states = state_callbacks.wait()
      assert len(states) == 1
      assert states[0][0]
      assert not states[0][0].state  # type: ignore
      assert not states[0][1]
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="vacuum")
      ])

      # Test vacuum true
      test_device.set_responder(TestVacuum("test-name", True, False, False, 0))
      state = dev.fetch_state()
      assert state
      assert state.state
      state = dev.state
      assert state
      assert state.state
      state_callbacks = thread_util.DoubleCallbackCapturer()
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="vacuum")
      ])
      dev.async_fetch_state(
          callback=state_callbacks.first_callback_finish,
          error_callback=state_callbacks.second_callback_finish)
      states = state_callbacks.wait()
      assert len(states) == 1
      assert states[0][0]
      assert states[0][0].state  # type: ignore
      assert not states[0][1]
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="vacuum")
      ])

      # Test blowoff false
      assert not dev.blowoff_state
      test_device.set_responder(TestVacuum("test-name", False, False, False, 0))
      blowoff_state = dev.fetch_blowoff_state()
      assert blowoff_state
      assert not blowoff_state.state
      assert dev.state
      blowoff_state = dev.blowoff_state
      assert blowoff_state
      assert not blowoff_state.state
      blowoff_state_callbacks: ("thread_util.DoubleCallbackCapturer["
                                "vacuum.BlowoffState, core.PyReachStatus]")
      blowoff_state_callbacks = thread_util.DoubleCallbackCapturer()
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="blowoff")
      ])
      dev.async_fetch_blowoff_state(
          callback=blowoff_state_callbacks.first_callback_finish,
          error_callback=blowoff_state_callbacks.second_callback_finish)
      blowoff_states = blowoff_state_callbacks.wait()
      assert len(blowoff_states) == 1
      assert blowoff_states[0][0]
      assert not blowoff_states[0][0].state  # type: ignore
      assert not blowoff_states[0][1]
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="blowoff")
      ])

      # Test blowoff true
      test_device.set_responder(TestVacuum("test-name", False, True, False, 0))
      blowoff_state = dev.fetch_blowoff_state()
      assert blowoff_state
      assert blowoff_state.state
      blowoff_state = dev.blowoff_state
      assert blowoff_state
      assert blowoff_state.state
      blowoff_state_callbacks = thread_util.DoubleCallbackCapturer()
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="blowoff")
      ])
      dev.async_fetch_blowoff_state(
          callback=blowoff_state_callbacks.first_callback_finish,
          error_callback=blowoff_state_callbacks.second_callback_finish)
      blowoff_states = blowoff_state_callbacks.wait()
      assert len(blowoff_states) == 1
      assert blowoff_states[0][0]
      assert blowoff_states[0][0].state  # type: ignore
      assert not blowoff_states[0][1]
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="blowoff")
      ])

      # Test vacuum-pressure false
      assert not dev.pressure_state
      test_device.set_responder(TestVacuum("test-name", False, False, False, 0))
      pressure_state = dev.fetch_pressure_state()
      assert pressure_state
      assert not pressure_state.state
      pressure_state1 = dev.pressure_state
      assert pressure_state1
      assert not pressure_state1.state
      pressure_callbacks: (
          "thread_util.DoubleCallbackCapturer[vacuum.VacuumPressure,"
          " core.PyReachStatus]")
      pressure_callbacks = thread_util.DoubleCallbackCapturer()
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="vacuum-pressure")
      ])
      dev.async_fetch_pressure_state(
          callback=pressure_callbacks.first_callback_finish,
          error_callback=pressure_callbacks.second_callback_finish)
      states2 = pressure_callbacks.wait()
      assert len(states2) == 1
      assert states2[0][0]
      assert not states2[0][0].state  # type: ignore
      assert not states2[0][1]
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="vacuum-pressure")
      ])

      # Test vacuum-pressure true
      test_device.set_responder(TestVacuum("test-name", False, False, True, 0))
      pressure_state = dev.fetch_pressure_state()
      assert pressure_state
      assert pressure_state.state
      pressure_state1 = dev.pressure_state
      assert pressure_state1
      assert pressure_state1.state
      pressure_callbacks = thread_util.DoubleCallbackCapturer()
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="vacuum-pressure")
      ])
      dev.async_fetch_pressure_state(
          callback=pressure_callbacks.first_callback_finish,
          error_callback=pressure_callbacks.second_callback_finish)
      states2 = pressure_callbacks.wait()
      assert len(states2) == 1
      assert states2[0][0]
      assert states2[0][0].state  # type: ignore
      assert not states2[0][1]
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="vacuum-pressure")
      ])

      # Test vacuum-gauge 0
      assert dev.gauge_state is None
      test_device.set_responder(TestVacuum("test-name", False, False, False, 0))
      gauge_state = dev.fetch_gauge_state()
      assert gauge_state is not None
      assert gauge_state.state == 0.0
      gauge_state1 = dev.gauge_state
      assert gauge_state1 is not None
      assert gauge_state1.state == 0.0
      gauge_callbacks: ("thread_util.DoubleCallbackCapturer[vacuum.VacuumGauge,"
                        " core.PyReachStatus]")
      gauge_callbacks = thread_util.DoubleCallbackCapturer()
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="vacuum-gauge")
      ])
      dev.async_fetch_gauge_state(
          callback=gauge_callbacks.first_callback_finish,
          error_callback=gauge_callbacks.second_callback_finish)
      gauge_states = gauge_callbacks.wait()
      assert len(gauge_states) == 1
      assert gauge_states[0][0].state == 0
      assert gauge_states[0][1] is None
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="vacuum-gauge")
      ])

      # Test vacuum-gauge 12
      test_device.set_responder(
          TestVacuum("test-name", False, False, False, 12))
      gauge_state = dev.fetch_gauge_state()
      assert gauge_state
      assert gauge_state.state == 12.0
      gauge_state1 = dev.gauge_state
      assert gauge_state1
      assert gauge_state1.state == 12.0
      gauge_callbacks = thread_util.DoubleCallbackCapturer()
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="vacuum-gauge")
      ])
      dev.async_fetch_gauge_state(
          callback=gauge_callbacks.first_callback_finish,
          error_callback=gauge_callbacks.second_callback_finish)
      gauge_states = gauge_callbacks.wait()
      assert len(gauge_states) == 1
      assert gauge_states[0][0].state == 12
      assert gauge_states[0][1] is None
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="frame-request",
              device_name="test-name",
              device_type="vacuum-gauge")
      ])

      # Stop callbacks and test values
      stop_vacuum_state_callback()
      stop_vacuum_blowoff_state_callback()
      stop_vacuum_pressure_state_callback()
      stop_vacuum_gauge_state_callback()
      assert [state.state for state in vacuum_state_callbacks.wait()
             ] == [False, False, True, True]
      assert [
          blowoff_state.state
          for blowoff_state in vacuum_blowoff_state_callbacks.wait()
      ] == [False, False, True, True]
      assert [
          pressure_state.state
          for pressure_state in vacuum_pressure_state_callbacks.wait()
      ] == [False, False, True, True]
      assert [
          gauge_state.state
          for gauge_state in vacuum_gauge_state_callbacks.wait()
      ] == [0, 0, 12, 12]


class TestVacuum(test_utils.TestResponder):
  """Represents a Vacuum for use in a test suite."""
  _device_name: str
  _output: bool
  _blowoff: bool
  _pressure: bool
  _gauge: float

  def __init__(self, device_name: str, output: bool, blowoff: bool,
               pressure: bool, gauge: float) -> None:
    """Construct a Test Vacuum.

    Args:
      device_name: The device name for the camera.
      output: If the vacuum output value is true.
      blowoff: If the blowoff output value is true.
      pressure: If the vacuum pressure output is true.
      gauge: The vacuum gaute value.
    """
    self._device_name = device_name
    self._output = output
    self._blowoff = blowoff
    self._pressure = pressure
    self._gauge = gauge

  def _respond(
      self, cmd: types_gen.CommandData, device_type: str, response_type: str,
      states: List[types_gen.CapabilityState]) -> List[types_gen.DeviceData]:
    if not test_utils.is_frame_request_for(cmd, device_type, self._device_name):
      return []
    out = [
        types_gen.DeviceData(
            ts=cmd.ts,
            tag=cmd.tag,
            device_type=device_type,
            device_name=cmd.device_name,
            data_type=response_type,
            state=[
                state for state in states
                if state.int_value != 0 or state.float_value != 0
            ])
    ]
    if cmd.tag:
      out.append(
          types_gen.DeviceData(
              ts=cmd.ts,
              tag=cmd.tag,
              device_type=device_type,
              device_name=self._device_name,
              data_type="cmd-status",
              status="done"))
    return out

  def step(self, cmd: types_gen.CommandData) -> List[types_gen.DeviceData]:
    """Test step, generates a response for testing framework data."""
    output = self._respond(
        cmd, "vacuum", "output-state",
        [types_gen.CapabilityState(int_value=1 if self._output else 0)])
    blowff = self._respond(
        cmd, "blowoff", "output-state",
        [types_gen.CapabilityState(int_value=1 if self._blowoff else 0)])
    pressure = self._respond(
        cmd, "vacuum-pressure", "sensor-state",
        [types_gen.CapabilityState(int_value=1 if self._pressure else 0)])
    gauge = self._respond(cmd, "vacuum-gauge", "sensor-state",
                          [types_gen.CapabilityState(float_value=self._gauge)])
    return output + blowff + pressure + gauge

  def start(self) -> List[types_gen.DeviceData]:
    return []


if __name__ == "__main__":
  unittest.main()
