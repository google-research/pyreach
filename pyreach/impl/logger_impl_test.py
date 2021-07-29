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

"""Test the Logger."""

from typing import List, cast
import unittest

from pyreach import core
from pyreach import snapshot
from pyreach.common.python import types_gen
from pyreach.impl import logger_impl
from pyreach.impl import test_utils
from pyreach.impl import thread_util


class TestLogger(test_utils.TestResponder):
  """Class to test logger."""

  def step(self, cmd: types_gen.CommandData) -> List[types_gen.DeviceData]:
    """Step function of testing logger."""
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


class TestPyReachLogger(unittest.TestCase):

  def test_test_logger(self) -> None:
    test_utils.run_test_client_test([TestLogger()], [
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

  def test_start_annotation_interval(self) -> None:
    rdev, dev = logger_impl.LoggerDevice().get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      test_device.set_responder(TestLogger())
      status = dev.start_annotation_interval("task")
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="client-annotation",
              device_name="",
              device_type="client-annotation",
              tag="tag-1",
              client_annotation=types_gen.ClientAnnotation(
                  interval_start=types_gen.IntervalStart(name="task")))
      ])
      self.assertEqual(status.status, "done")

  def test_end_annotation_interval(self) -> None:
    rdev, dev = logger_impl.LoggerDevice().get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      test_device.set_responder(TestLogger())
      status = dev.end_annotation_interval("task", start_time=100, end_time=200)
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="client-annotation",
              device_name="",
              device_type="client-annotation",
              tag="tag-1",
              client_annotation=types_gen.ClientAnnotation(
                  interval_end=types_gen.IntervalEnd(
                      name="task", start_ts=100000, end_ts=200000)))
      ])
      self.assertEqual(status.status, "done")

  def test_start_task(self) -> None:
    rdev, dev = logger_impl.LoggerDevice().get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      test_device.set_responder(TestLogger())
      dev.start_task({})
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="event-start",
              device_type="operator",
          )
      ])

  def test_end_task(self) -> None:
    rdev, dev = logger_impl.LoggerDevice().get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      test_device.set_responder(TestLogger())
      dev.end_task({})
      dev_impl = cast(logger_impl.LoggerImpl, dev)
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="event",
              device_type="operator",
              event_name="pick",
              event_duration=float(dev_impl._device._task_end_ts -
                                   dev_impl._device._task_start_ts) / 1e3)
      ])

  def test_send_snapshot(self) -> None:
    rdev, dev = logger_impl.LoggerDevice().get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      test_device.set_responder(TestLogger())
      dev.send_snapshot(
          snapshot=snapshot.Snapshot(
              source="pyreach-test",
              device_data_refs=(snapshot.SnapshotReference(2.0, 1),),
              responses=(
                  snapshot.SnapshotResponse(5, "vacuum", "test-vacuum",
                                            snapshot.SnapshotReference(3.0, 4)),
                  snapshot.SnapshotResponse(
                      6, "arm", "test-arm",
                      core.PyReachStatus(
                          time=7.0,
                          status="test-status",
                          script="test-script",
                          error="test-error",
                          progress=8.0,
                          message="test-message",
                          code=9)),
                  snapshot.SnapshotResponse(
                      10, "oracle", "test-oracle",
                      core.PyReachStatus(
                          time=11.0,
                          sequence=12,
                          status="test-status",
                          script="test-script",
                          error="test-error",
                          progress=13.0,
                          message="test-message",
                          code=14))),
              gym_env_id="test-env-id",
              gym_run_id="test-run-id",
              gym_episode=1,
              gym_step=2,
              gym_reward=3.0,
              gym_done=True,
              gym_actions=(
                  snapshot.SnapshotGymAction("test-type", "test-name", True),
                  snapshot.SnapshotGymVacuumAction("test-vacuum", "vacuum",
                                                   True, 1),
                  snapshot.SnapshotGymArmAction(
                      "test-arm", "arm", True, 1, 2, (1.1, 2.2, 3.3, 4.4, 5.5,
                                                      6.6), (1.0, 2.0, 3.0, 4.0,
                                                             5.0, 6.0), True,
                      4.0, 5.0, 6.0, "test-action", True, "test-intent",
                      "success", "test-id", True, True, 7.0, 8.0, 9.0, True))))
      test_device.expect_command_data([
          types_gen.CommandData(
              device_type="client-annotation",
              data_type="client-annotation",
              snapshot=types_gen.Snapshot(
                  source="pyreach-test",
                  device_data_refs=[types_gen.DeviceDataRef(ts=2000, seq=1)],
                  responses=[
                      types_gen.SnapshotResponse(
                          cid=5,
                          gym_element_type="vacuum",
                          gym_config_name="test-vacuum",
                          device_data_ref=types_gen.DeviceDataRef(
                              ts=3000, seq=4)),
                      types_gen.SnapshotResponse(
                          cid=6,
                          gym_element_type="arm",
                          gym_config_name="test-arm",
                          device_data_ref=types_gen.DeviceDataRef(ts=7000),
                          status=types_gen.Status(
                              status="test-status",
                              script="test-script",
                              error="test-error",
                              progress=8.0,
                              message="test-message",
                              code=9)),
                      types_gen.SnapshotResponse(
                          cid=10,
                          gym_element_type="oracle",
                          gym_config_name="test-oracle",
                          device_data_ref=types_gen.DeviceDataRef(
                              ts=11000, seq=12))
                  ],
                  gym_actions=[
                      types_gen.GymAction(
                          device_type="test-type",
                          device_name="test-name",
                          synchronous=True),
                      types_gen.GymAction(
                          device_type="test-vacuum",
                          device_name="vacuum",
                          synchronous=True,
                          vacuum_action_params=types_gen.VacuumActionParams(1)),
                      types_gen.GymAction(
                          device_type="test-arm",
                          device_name="arm",
                          synchronous=True,
                          arm_action_params=types_gen.ArmActionParams(
                              command=1,
                              cid=2,
                              joint_angles=[1.1, 2.2, 3.3, 4.4, 5.5, 6.6],
                              pose=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
                              timeout_sec=6.0,
                              use_linear=True,
                              velocity=4.0,
                              acceleration=5.0,
                              action_name="test-action",
                              use_unity_ik=True,
                              intent="test-intent",
                              success_type="success",
                              pick_id="test-id",
                              apply_tip_adjust_transform=True,
                              servo=True,
                              servo_t_secs=7.0,
                              servo_lookahead_time_secs=8.0,
                              servo_gain=9.0,
                              allow_uncalibrated=True))
                  ],
                  gym_env_id="test-env-id",
                  gym_run_id="test-run-id",
                  gym_episode=1,
                  gym_step=2,
                  gym_reward=3.0,
                  gym_done=True))
      ])

  def test_async_start_annotation_interval(self) -> None:
    rdev, dev = logger_impl.LoggerDevice().get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      test_device.set_responder(TestLogger())
      callbacks = thread_util.CallbackCapturer[core.PyReachStatus]()
      dev.async_start_annotation_interval(
          "task", callback=callbacks.callback_and_then_finish)
      results: List[core.PyReachStatus] = callbacks.wait()
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="client-annotation",
              device_name="",
              device_type="client-annotation",
              tag="tag-1",
              client_annotation=types_gen.ClientAnnotation(
                  interval_start=types_gen.IntervalStart(name="task")))
      ])
      self.assertEqual(len(results), 1)
      self.assertEqual(results[0].status, "done")

  def test_async_end_annotation_interval(self) -> None:
    rdev, dev = logger_impl.LoggerDevice().get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      test_device.set_responder(TestLogger())
      callbacks = thread_util.CallbackCapturer[core.PyReachStatus]()
      dev.async_end_annotation_interval(
          "task",
          start_time=100,
          end_time=200,
          callback=callbacks.callback_and_then_finish)
      results: List[core.PyReachStatus] = callbacks.wait()
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="client-annotation",
              device_name="",
              device_type="client-annotation",
              tag="tag-1",
              client_annotation=types_gen.ClientAnnotation(
                  interval_end=types_gen.IntervalEnd(
                      name="task", start_ts=100000, end_ts=200000)))
      ])
      self.assertEqual(len(results), 1)
      self.assertEqual(results[0].status, "done")


if __name__ == "__main__":
  unittest.main()
