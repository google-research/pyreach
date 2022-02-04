"""Tests for digital_output_impl."""

from typing import List
import unittest

from pyreach import core
from pyreach import digital_output  # pylint: disable=unused-import
from pyreach.common.python import types_gen
from pyreach.impl import digital_output_impl
from pyreach.impl import test_utils
from pyreach.impl import thread_util


class DigitalOutputImplTest(unittest.TestCase):

  def test_digital_output_test(self) -> None:
    test_utils.run_test_client_test([
        TestDigitalOutput("test-dev-type", "test-dev", "test-robot", "pin_name",
                          1)
    ], [
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1,
                device_type="test-dev-type",
                device_name="test-dev",
                data_type="frame-request"),
            (types_gen.DeviceData(
                ts=1,
                device_type="test-dev-type",
                device_name="test-dev",
                data_type="output-state",
                state=[types_gen.CapabilityState(pin="pin_name", int_value=1)
                      ]),))
    ])
    test_utils.run_test_client_test([
        TestDigitalOutput("test-dev-type", "test-dev", "test-robot", "pin_name",
                          1)
    ], [
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=2,
                tag="test-tag-1",
                device_type="test-dev-type",
                device_name="test-dev",
                data_type="frame-request"),
            (
                types_gen.DeviceData(
                    ts=2,
                    tag="test-tag-1",
                    device_type="test-dev-type",
                    device_name="test-dev",
                    data_type="output-state",
                    state=[
                        types_gen.CapabilityState(pin="pin_name", int_value=1)
                    ]),
                types_gen.DeviceData(
                    ts=2,
                    tag="test-tag-1",
                    device_type="test-dev-type",
                    device_name="test-dev",
                    data_type="cmd-status",
                    status="done"),
            ))
    ])
    test_utils.run_test_client_test(
        [TestDigitalOutput("test-dev-type", "test-dev", "test-robot")], [
            test_utils.TestResponderStep(
                types_gen.CommandData(
                    ts=5,
                    tag="test-tag-3",
                    device_type="robot",
                    device_name="test-robot",
                    data_type="reach-script"), (
                        types_gen.DeviceData(
                            device_type="robot",
                            data_type="cmd-status",
                            device_name="test-robot",
                            tag="test-tag-3",
                            ts=5,
                            status="executing"),
                        types_gen.DeviceData(
                            ts=5,
                            tag="test-tag-3",
                            device_type="robot",
                            device_name="test-robot",
                            data_type="cmd-status",
                            status="done"),
                    ))
        ])

  def test_digital_output(self) -> None:
    self._digital_output_fetch(False)
    self._digital_output_fetch(True)

  def _digital_output_fetch(self, fused_pins: bool) -> None:
    rdev, dev = digital_output_impl.DigitalOutputDevice(
        "test-dev-type", "test-dev", "test-robot", ("pin-name",),
        fused_pins).get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      self.assertEqual(dev.type, "test-dev-type")
      self.assertEqual(dev.name, "test-dev")
      self.assertEqual(dev.robot_name, "test-robot")
      if fused_pins:
        self.assertEqual(dev.pins, ("",))
      else:
        self.assertEqual(dev.pins, ("pin-name",))
      global_callbacks: (
          "thread_util.CallbackCapturer[digital_output.DigitalOutputState]"
      ) = thread_util.CallbackCapturer()
      stop = dev.add_state_callback(global_callbacks.callback_false,
                                    global_callbacks.finished_callback)
      self.assertIsNone(dev.state)
      returned_states = []
      for input_state, expect in [(1, True), (0, False), (-1, None)]:
        test_device.set_responder(
            TestDigitalOutput("test-dev-type", "test-dev", "test-robot",
                              "pin-name" if not fused_pins else "",
                              input_state))
        state = dev.fetch_state()
        test_device.expect_command_data([
            types_gen.CommandData(
                device_type="test-dev-type",
                device_name="test-dev",
                data_type="frame-request")
        ])
        self.assertIsNotNone(state)
        self.assertEqual(state, dev.state)
        assert state
        returned_states.append(state)
        self.assertEqual(state.type, "test-dev-type")
        self.assertEqual(state.name, "test-dev")
        self.assertEqual(state.robot_name, "test-robot")
        self.assertEqual(len(state.pin_states), 1)
        if fused_pins:
          self.assertEqual(state.pin_states[0].name, "")
        else:
          self.assertEqual(state.pin_states[0].name, "pin-name")
        self.assertEqual(state.pin_states[0].state, expect)
        capturer: ("thread_util.DoubleCallbackCapturer["
                   "digital_output.DigitalOutputState, core.PyReachStatus]"
                  ) = thread_util.DoubleCallbackCapturer()
        dev.async_fetch_state(
            callback=capturer.first_callback_finish,
            error_callback=capturer.second_callback_finish)
        test_device.expect_command_data([
            types_gen.CommandData(
                device_type="test-dev-type",
                device_name="test-dev",
                data_type="frame-request")
        ])
        states = capturer.wait()
        self.assertEqual(len(states), 1)
        self.assertIsNone(states[0][1])
        test_state = states[0][0]
        assert test_state
        returned_states.append(test_state)
        self.assertIsNotNone(test_state)
        self.assertEqual(test_state, dev.state)
        self.assertEqual(test_state.type, "test-dev-type")
        self.assertEqual(test_state.name, "test-dev")
        self.assertEqual(test_state.robot_name, "test-robot")
        self.assertEqual(len(test_state.pin_states), 1)
        if fused_pins:
          self.assertEqual(state.pin_states[0].name, "")
        else:
          self.assertEqual(state.pin_states[0].name, "pin-name")
        self.assertEqual(test_state.pin_states[0].state, expect)
      stop()
      global_states = global_callbacks.wait()
      self.assertEqual(len(returned_states), 6)
      self.assertEqual(len(global_states), len(returned_states))
      for returned_state, global_state in zip(returned_states, global_states):
        self.assertIsNotNone(global_state)
        self.assertIsNotNone(returned_state)
        self.assertEqual(returned_state, global_state)

  def test_digital_output_send(self) -> None:
    fused_pins = False
    rdev, dev = digital_output_impl.DigitalOutputDevice(
        "test-dev-type", "test-dev", "test-robot", ("pin-name",),
        fused_pins).get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      write_pin_name = ""
      if not fused_pins:
        write_pin_name = "pin-name"
      self.assertEqual(dev.type, "test-dev-type")
      self.assertEqual(dev.name, "test-dev")
      self.assertEqual(dev.robot_name, "test-robot")
      self.assertEqual(dev.pins, (write_pin_name,))
      global_callbacks: (
          "thread_util.CallbackCapturer[digital_output.DigitalOutputState]"
      ) = thread_util.CallbackCapturer()
      stop = dev.add_state_callback(global_callbacks.callback_false,
                                    global_callbacks.finished_callback)
      self.assertIsNone(dev.state)

      tag_count = 0

      def verify_write_commmand_data(write_state: int) -> None:
        nonlocal tag_count
        tag_count += 1
        test_device.expect_command_data([
            types_gen.CommandData(
                device_type="robot",
                device_name="test-robot",
                tag="tag-" + str(tag_count),
                data_type="reach-script",
                pick_id="test-pick-id",
                intent="test-intent",
                success_type="test-success",
                reach_script=types_gen.ReachScript(
                    calibration_requirement=types_gen
                    .ReachScriptCalibrationRequirement(allow_uncalibrated=True),
                    preemptive=True,
                    version=0,
                    commands=[
                        types_gen.ReachScriptCommand(
                            set_output=types_gen.SetOutput(
                                name="test-dev",
                                py_type="test-dev-type",
                                args=[
                                    types_gen.CapabilityState(
                                        pin=write_pin_name,
                                        int_value=write_state)
                                ]))
                    ]))
        ])

      # Test async_set_pin_state and set_pin_state timeouts

      state = dev.set_pin_state(write_pin_name, True, "test-intent",
                                "test-pick-id", "test-success", True, 0.0)
      self._verify_state(state, "done", "timeout")
      verify_write_commmand_data(1)

      state = dev.set_pin_state(write_pin_name, False, "test-intent",
                                "test-pick-id", "test-success", True, 0.0)
      self._verify_state(state, "done", "timeout")
      verify_write_commmand_data(0)

      callbacks: ("thread_util.CallbackCapturer[core.PyReachStatus]"
                 ) = thread_util.CallbackCapturer()
      dev.async_set_pin_state(
          write_pin_name,
          True,
          "test-intent",
          "test-pick-id",
          "test-success",
          timeout=0.0,
          callback=callbacks.callback,
          finished_callback=callbacks.finished_callback)
      self.assertEqual(0, len(callbacks.wait()))
      verify_write_commmand_data(1)
      callbacks = thread_util.CallbackCapturer()
      dev.async_set_pin_state(
          write_pin_name,
          False,
          "test-intent",
          "test-pick-id",
          "test-success",
          timeout=0.0,
          callback=callbacks.callback,
          finished_callback=callbacks.finished_callback)
      self.assertEqual(0, len(callbacks.wait()))
      verify_write_commmand_data(0)

      # Test async_set_pin_states and set_pin_states timeouts

      state = dev.set_pin_states(((write_pin_name, True),), "test-intent",
                                 "test-pick-id", "test-success", True, 0.0)
      self._verify_state(state, "done", "timeout")
      verify_write_commmand_data(1)

      state = dev.set_pin_states(((write_pin_name, False),), "test-intent",
                                 "test-pick-id", "test-success", True, 0.0)
      self._verify_state(state, "done", "timeout")
      verify_write_commmand_data(0)

      callbacks = thread_util.CallbackCapturer()
      dev.async_set_pin_states(((write_pin_name, True),),
                               "test-intent",
                               "test-pick-id",
                               "test-success",
                               timeout=0.0,
                               callback=callbacks.callback,
                               finished_callback=callbacks.finished_callback)
      self.assertEqual(0, len(callbacks.wait()))
      verify_write_commmand_data(1)
      callbacks = thread_util.CallbackCapturer()
      dev.async_set_pin_states(((write_pin_name, False),),
                               "test-intent",
                               "test-pick-id",
                               "test-success",
                               timeout=0.0,
                               callback=callbacks.callback,
                               finished_callback=callbacks.finished_callback)
      self.assertEqual(0, len(callbacks.wait()))
      verify_write_commmand_data(0)

      # Test success for set_pin_state and async_set_pin_state

      test_device.set_responder(
          TestDigitalOutput("test-dev-name", "test-dev", "test-robot",
                            "pin-name", 0))
      state = dev.set_pin_state(write_pin_name, True, "test-intent",
                                "test-pick-id", "test-success")
      self._verify_state(state, "done")
      verify_write_commmand_data(1)
      state = dev.set_pin_state(write_pin_name, False, "test-intent",
                                "test-pick-id", "test-success")
      self._verify_state(state, "done")
      verify_write_commmand_data(0)

      callbacks = thread_util.CallbackCapturer()
      dev.async_set_pin_state(
          write_pin_name,
          True,
          "test-intent",
          "test-pick-id",
          "test-success",
          callback=callbacks.callback,
          finished_callback=callbacks.finished_callback)
      states = callbacks.wait()
      self.assertEqual(2, len(states))
      self._verify_state(states[0], "executing")
      self._verify_state(states[1], "done")
      verify_write_commmand_data(1)
      callbacks = thread_util.CallbackCapturer()
      dev.async_set_pin_state(
          write_pin_name,
          False,
          "test-intent",
          "test-pick-id",
          "test-success",
          callback=callbacks.callback,
          finished_callback=callbacks.finished_callback)
      states = callbacks.wait()
      self.assertEqual(2, len(states))
      self._verify_state(states[0], "executing")
      self._verify_state(states[1], "done")
      verify_write_commmand_data(0)

      # Test success for set_pin_states and async_set_pin_states

      test_device.set_responder(
          TestDigitalOutput("test-dev-name", "test-dev", "test-robot",
                            "pin-name", 0))
      state = dev.set_pin_states(((write_pin_name, True),), "test-intent",
                                 "test-pick-id", "test-success")
      self._verify_state(state, "done")
      verify_write_commmand_data(1)
      state = dev.set_pin_states(((write_pin_name, False),), "test-intent",
                                 "test-pick-id", "test-success")
      self._verify_state(state, "done")
      verify_write_commmand_data(0)

      callbacks = thread_util.CallbackCapturer()
      dev.async_set_pin_states(((write_pin_name, True),),
                               "test-intent",
                               "test-pick-id",
                               "test-success",
                               callback=callbacks.callback,
                               finished_callback=callbacks.finished_callback)
      states = callbacks.wait()
      self.assertEqual(2, len(states))
      self._verify_state(states[0], "executing")
      self._verify_state(states[1], "done")
      verify_write_commmand_data(1)
      callbacks = thread_util.CallbackCapturer()
      dev.async_set_pin_states(((write_pin_name, False),),
                               "test-intent",
                               "test-pick-id",
                               "test-success",
                               callback=callbacks.callback,
                               finished_callback=callbacks.finished_callback)
      states = callbacks.wait()
      self.assertEqual(2, len(states))
      self._verify_state(states[0], "executing")
      self._verify_state(states[1], "done")
      verify_write_commmand_data(0)

      stop()
      global_states = global_callbacks.wait()
      self.assertEqual(len(global_states), 0)

  def _verify_state(self,
                    state: core.PyReachStatus,
                    status: str,
                    error: str = "") -> None:
    self.assertEqual(state.status, status)
    self.assertEqual(state.script, "")
    self.assertEqual(state.error, error)
    self.assertEqual(state.progress, 0.0)
    self.assertEqual(state.message, "")
    self.assertEqual(state.code, 0)


class TestDigitalOutput(test_utils.TestResponder):
  _device_type: str
  _device_name: str
  _robot_name: str
  _pin_name: str
  _pin_state: int

  def __init__(self,
               device_type: str,
               device_name: str,
               robot_name: str,
               pin_name: str = "",
               pin_state: int = 0) -> None:
    super().__init__()
    self._device_type = device_type
    self._device_name = device_name
    self._robot_name = robot_name
    self._pin_name = pin_name
    self._pin_state = pin_state

  def start(self) -> List[types_gen.DeviceData]:
    return []

  def step(self, cmd: types_gen.CommandData) -> List[types_gen.DeviceData]:
    if (cmd.device_type == "robot" and cmd.device_name == self._robot_name and
        cmd.data_type == "reach-script"):
      if not cmd.tag:
        return []
      return [
          types_gen.DeviceData(
              device_type="robot",
              data_type="cmd-status",
              device_name=self._robot_name,
              tag=cmd.tag,
              ts=cmd.ts,
              status="executing"),
          types_gen.DeviceData(
              device_type="robot",
              data_type="cmd-status",
              device_name=self._robot_name,
              tag=cmd.tag,
              ts=cmd.ts,
              status="done"),
      ]
    if test_utils.is_frame_request_for(cmd, self._device_type,
                                       self._device_name):
      output = [
          types_gen.DeviceData(
              device_type=self._device_type,
              data_type="output-state",
              device_name=self._device_name,
              tag=cmd.tag,
              ts=cmd.ts,
              state=[
                  types_gen.CapabilityState(
                      pin=self._pin_name, int_value=self._pin_state)
              ])
      ]
      if cmd.tag:
        output += [
            types_gen.DeviceData(
                device_type=self._device_type,
                data_type="cmd-status",
                device_name=self._device_name,
                tag=cmd.tag,
                ts=cmd.ts,
                status="done")
        ]
      return output
    return []


if __name__ == "__main__":
  unittest.main()
