"""Tests for run_script_impl."""

from typing import List
import unittest

from pyreach import core
from pyreach.common.python import types_gen
from pyreach.impl import run_script_impl
from pyreach.impl import test_utils
from pyreach.impl import thread_util


class TestRunScript(test_utils.TestResponder):

  def start(self) -> List[types_gen.DeviceData]:
    """Start the TestResponder."""
    return []

  def step(self, cmd: types_gen.CommandData) -> List[types_gen.DeviceData]:
    """Step function of testing logger."""
    if (cmd.device_type == "delegated-client" and
        cmd.device_name == "run-script" and cmd.data_type == "run-script" and
        cmd.tag):
      if cmd.cmd == "cancel" or (cmd.cmd == "run-script" and cmd.args and
                                 cmd.args[0] == "good-script"):
        return [
            types_gen.DeviceData(
                ts=cmd.ts,
                device_type="delegated-client",
                device_name="run-script",
                data_type="cmd-status",
                status="done",
                tag=cmd.tag)
        ]
      return [
          types_gen.DeviceData(
              ts=cmd.ts,
              device_type="delegated-client",
              device_name="run-script",
              data_type="cmd-status",
              status="rejected",
              error="bad-input",
              message="unsupported command: " + str(cmd.args),
              tag=cmd.tag)
      ]
    return []


class RunScriptImplTest(unittest.TestCase):

  def test_test_run_script(self) -> None:
    test_utils.run_test_client_test([TestRunScript()], [
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1,
                tag="tag-1",
                device_type="delegated-client",
                device_name="run-script",
                data_type="run-script",
                cmd="cancel"), (types_gen.DeviceData(
                    ts=1,
                    tag="tag-1",
                    device_type="delegated-client",
                    device_name="run-script",
                    data_type="cmd-status",
                    status="done"),)),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=2,
                tag="tag-2",
                device_type="delegated-client",
                device_name="run-script",
                data_type="run-script",
                cmd="run-script",
                args=["good-script"]), (types_gen.DeviceData(
                    ts=2,
                    tag="tag-2",
                    device_type="delegated-client",
                    device_name="run-script",
                    data_type="cmd-status",
                    status="done"),)),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=3,
                tag="tag-3",
                device_type="delegated-client",
                device_name="run-script",
                data_type="run-script",
                cmd="run-script",
                args=["bad-script"]), (types_gen.DeviceData(
                    ts=3,
                    tag="tag-3",
                    device_type="delegated-client",
                    device_name="run-script",
                    data_type="cmd-status",
                    status="rejected",
                    error="bad-input",
                    message="unsupported command: ['bad-script']"),)),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=4,
                tag="tag-4",
                device_type="delegated-client",
                device_name="run-script",
                data_type="run-script",
                cmd="run-script",
                args=["bad-script", "invalid"]),
            (types_gen.DeviceData(
                ts=4,
                tag="tag-4",
                device_type="delegated-client",
                device_name="run-script",
                data_type="cmd-status",
                status="rejected",
                error="bad-input",
                message="unsupported command: ['bad-script', 'invalid']"),)),
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=5,
                tag="tag-5",
                device_type="delegated-client",
                device_name="run-script",
                data_type="run-script",
                cmd="invalid"), (types_gen.DeviceData(
                    ts=5,
                    tag="tag-5",
                    device_type="delegated-client",
                    device_name="run-script",
                    data_type="cmd-status",
                    status="rejected",
                    error="bad-input",
                    message="unsupported command: []"),)),
    ])

  def test_run_script(self) -> None:
    rdev, dev = run_script_impl.RunScriptDevice().get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      test_device.set_responder(TestRunScript())

      status = dev.cancel()
      self.assertEqual(status.status, "done")
      self.assertFalse(status.is_error())
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="run-script",
              device_name="run-script",
              device_type="delegated-client",
              tag="tag-1",
              cmd="cancel"),
      ])

      status = dev.run_script("good-script", [])
      self.assertEqual(status.status, "done")
      self.assertFalse(status.is_error())
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="run-script",
              device_name="run-script",
              device_type="delegated-client",
              tag="tag-2",
              cmd="run-script",
              args=["good-script"]),
      ])

      status = dev.run_script("bad-script", ["invalid"])
      self.assertEqual(status.status, "rejected")
      self.assertEqual(status.error, "bad-input")
      self.assertEqual(status.message,
                       "unsupported command: ['bad-script', 'invalid']")
      self.assertTrue(status.is_error())
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="run-script",
              device_name="run-script",
              device_type="delegated-client",
              tag="tag-3",
              cmd="run-script",
              args=["bad-script", "invalid"]),
      ])

      callbacks = thread_util.CallbackCapturer[core.PyReachStatus]()
      dev.async_cancel(None, callbacks.callback, callbacks.finished_callback)
      results = callbacks.wait()
      self.assertEqual(len(results), 1)
      self.assertEqual(results[0].status, "done")
      self.assertFalse(results[0].is_error())
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="run-script",
              device_name="run-script",
              device_type="delegated-client",
              tag="tag-4",
              cmd="cancel"),
      ])

      callbacks = thread_util.CallbackCapturer[core.PyReachStatus]()
      dev.async_run_script("good-script", [], None, callbacks.callback,
                           callbacks.finished_callback)
      results = callbacks.wait()
      self.assertEqual(len(results), 1)
      self.assertEqual(results[0].status, "done")
      self.assertFalse(results[0].is_error())
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="run-script",
              device_name="run-script",
              device_type="delegated-client",
              tag="tag-5",
              cmd="run-script",
              args=["good-script"]),
      ])

      callbacks = thread_util.CallbackCapturer[core.PyReachStatus]()
      dev.async_run_script("bad-script", ["invalid"], None, callbacks.callback,
                           callbacks.finished_callback)
      results = callbacks.wait()
      self.assertEqual(len(results), 1)
      self.assertEqual(results[0].status, "rejected")
      self.assertEqual(results[0].error, "bad-input")
      self.assertEqual(results[0].message,
                       "unsupported command: ['bad-script', 'invalid']")
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="run-script",
              device_name="run-script",
              device_type="delegated-client",
              tag="tag-6",
              cmd="run-script",
              args=["bad-script", "invalid"]),
      ])

  def test_run_script_reject(self) -> None:
    rdev, dev = run_script_impl.RunScriptDevice().get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      test_device.set_responder(test_utils.RejectResponder())

      status = dev.cancel()
      self.assertEqual(status.status, "rejected")
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="run-script",
              device_name="run-script",
              device_type="delegated-client",
              tag="tag-1",
              cmd="cancel"),
      ])

      status = dev.run_script("good-script", [])
      self.assertEqual(status.status, "rejected")
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="run-script",
              device_name="run-script",
              device_type="delegated-client",
              tag="tag-2",
              cmd="run-script",
              args=["good-script"]),
      ])

      status = dev.run_script("bad-script", ["invalid"])
      self.assertEqual(status.status, "rejected")
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="run-script",
              device_name="run-script",
              device_type="delegated-client",
              tag="tag-3",
              cmd="run-script",
              args=["bad-script", "invalid"]),
      ])

      callbacks = thread_util.CallbackCapturer[core.PyReachStatus]()
      dev.async_cancel(None, callbacks.callback, callbacks.finished_callback)
      results = callbacks.wait()
      self.assertEqual(len(results), 1)
      self.assertEqual(results[0].status, "rejected")
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="run-script",
              device_name="run-script",
              device_type="delegated-client",
              tag="tag-4",
              cmd="cancel"),
      ])

      callbacks = thread_util.CallbackCapturer[core.PyReachStatus]()
      dev.async_run_script("good-script", [], None, callbacks.callback,
                           callbacks.finished_callback)
      results = callbacks.wait()
      self.assertEqual(len(results), 1)
      self.assertEqual(results[0].status, "rejected")
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="run-script",
              device_name="run-script",
              device_type="delegated-client",
              tag="tag-5",
              cmd="run-script",
              args=["good-script"]),
      ])

      callbacks = thread_util.CallbackCapturer[core.PyReachStatus]()
      dev.async_run_script("bad-script", ["invalid"], None, callbacks.callback,
                           callbacks.finished_callback)
      results = callbacks.wait()
      self.assertEqual(len(results), 1)
      self.assertEqual(results[0].status, "rejected")
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="run-script",
              device_name="run-script",
              device_type="delegated-client",
              tag="tag-6",
              cmd="run-script",
              args=["bad-script", "invalid"]),
      ])

  def test_run_script_timeout(self) -> None:
    rdev, dev = run_script_impl.RunScriptDevice().get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      status = dev.cancel(timeout=0.0)
      self.assertEqual(status.status, "done")
      self.assertEqual(status.error, "timeout")
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="run-script",
              device_name="run-script",
              device_type="delegated-client",
              tag="tag-1",
              cmd="cancel"),
      ])

      status = dev.run_script("good-script", [], timeout=0.0)
      self.assertEqual(status.status, "done")
      self.assertEqual(status.error, "timeout")
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="run-script",
              device_name="run-script",
              device_type="delegated-client",
              tag="tag-2",
              cmd="run-script",
              args=["good-script"]),
      ])

      status = dev.run_script("bad-script", ["invalid"], timeout=0.0)
      self.assertEqual(status.status, "done")
      self.assertEqual(status.error, "timeout")
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="run-script",
              device_name="run-script",
              device_type="delegated-client",
              tag="tag-3",
              cmd="run-script",
              args=["bad-script", "invalid"]),
      ])

      callbacks = thread_util.CallbackCapturer[core.PyReachStatus]()
      dev.async_cancel(0.0, callbacks.callback, callbacks.finished_callback)
      results = callbacks.wait()
      self.assertEqual(len(results), 0)
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="run-script",
              device_name="run-script",
              device_type="delegated-client",
              tag="tag-4",
              cmd="cancel"),
      ])

      callbacks = thread_util.CallbackCapturer[core.PyReachStatus]()
      dev.async_run_script("good-script", [], 0.0, callbacks.callback,
                           callbacks.finished_callback)
      results = callbacks.wait()
      self.assertEqual(len(results), 0)
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="run-script",
              device_name="run-script",
              device_type="delegated-client",
              tag="tag-5",
              cmd="run-script",
              args=["good-script"]),
      ])

      callbacks = thread_util.CallbackCapturer[core.PyReachStatus]()
      dev.async_run_script("bad-script", ["invalid"], 0.0, callbacks.callback,
                           callbacks.finished_callback)
      results = callbacks.wait()
      self.assertEqual(len(results), 0)
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="run-script",
              device_name="run-script",
              device_type="delegated-client",
              tag="tag-6",
              cmd="run-script",
              args=["bad-script", "invalid"]),
      ])


if __name__ == "__main__":
  unittest.main()
