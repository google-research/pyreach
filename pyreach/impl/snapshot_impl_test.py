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
"""Tests for snapshot_impl."""

import json
import unittest

from pyreach import snapshot
from pyreach.common.python import types_gen
from pyreach.core import PyReachStatus
from pyreach.impl import snapshot_impl


class SnapshotImpl(unittest.TestCase):

  def test_reverse_snapshot(self) -> None:
    self.assertIsNone(snapshot_impl.reverse_snapshot(None))
    snapshot_cmd = snapshot_impl.reverse_snapshot(
        types_gen.Snapshot(
            source="pyreach-test",
            device_data_refs=[types_gen.DeviceDataRef(ts=2000, seq=1)],
            responses=[
                types_gen.SnapshotResponse(
                    cid=5,
                    gym_element_type="vacuum",
                    gym_config_name="test-vacuum",
                    device_data_ref=types_gen.DeviceDataRef(ts=3000, seq=4)),
                types_gen.SnapshotResponse(
                    cid=6,
                    gym_element_type="arm",
                    gym_config_name="test-arm",
                    device_data_ref=types_gen.DeviceDataRef(ts=7000, seq=0),
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
                    device_data_ref=types_gen.DeviceDataRef(ts=11000, seq=12),
                    status=types_gen.Status(
                        status="test-status",
                        script="test-script",
                        error="test-error",
                        progress=13.0,
                        message="test-message",
                        code=14)),
            ],
            gym_server_ts=1,
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
                    device_type="test-logger",
                    device_name="logger",
                    synchronous=False,
                    logger_action_params=types_gen.LoggerActionParams([
                        types_gen.KeyValue(key="1", value="2"),
                        types_gen.KeyValue(key="3", value="4")
                    ], True)),
                types_gen.GymAction(
                    device_type="test-arm",
                    device_name="arm",
                    synchronous=True,
                    arm_action_params=types_gen.ArmActionParams(
                        command=1,
                        cid=2,
                        joint_angles=[1.1, 2.2, 3.3, 4.4, 5.5, 6.6],
                        pose=[1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
                        reach_action=3,
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
                        allow_uncalibrated=True,
                        controller_name="test-controller"))
            ],
            gym_env_id="test-env-id",
            gym_run_id="test-run-id",
            gym_episode=1,
            gym_step=2,
            gym_reward=3.0,
            gym_done=True))
    assert snapshot_cmd is not None
    expect_snapshot = snapshot.Snapshot(
        source="pyreach-test",
        device_data_refs=(snapshot.SnapshotReference(2.0, 1),),
        responses=(snapshot.SnapshotResponse(5, "vacuum", "test-vacuum",
                                             snapshot.SnapshotReference(3.0,
                                                                        4)),
                   snapshot.SnapshotResponse(
                       6, "arm", "test-arm",
                       PyReachStatus(
                           time=7.0,
                           status="test-status",
                           script="test-script",
                           error="test-error",
                           progress=8.0,
                           message="test-message",
                           code=9)),
                   snapshot.SnapshotResponse(
                       10, "oracle", "test-oracle",
                       snapshot.SnapshotReference(11.0, 12))),
        gym_server_time=0.001,
        gym_env_id="test-env-id",
        gym_run_id="test-run-id",
        gym_episode=1,
        gym_step=2,
        gym_reward=3.0,
        gym_done=True,
        gym_actions=(snapshot.SnapshotGymAction("test-type", "test-name", True),
                     snapshot.SnapshotGymVacuumAction("test-vacuum", "vacuum",
                                                      True, 1),
                     snapshot.SnapshotGymLoggerAction("test-logger", "logger",
                                                      False, True, {
                                                          "1": "2",
                                                          "3": "4"
                                                      }),
                     snapshot.SnapshotGymArmAction(
                         "test-arm", "arm", True, 1, 2,
                         (1.1, 2.2, 3.3, 4.4, 5.5, 6.6),
                         (1.0, 2.0, 3.0, 4.0, 5.0, 6.0), True, 4.0, 5.0, 6.0,
                         "test-action", True, "test-intent", "success",
                         "test-id", True, True, 7.0, 8.0, 9.0, True,
                         "test-controller")))
    self.assertEqual(expect_snapshot, snapshot_cmd)

  def test_convert_snapshot(self) -> None:
    self.assertIsNone(snapshot_impl.convert_snapshot(None))
    snapshot_cmd = snapshot_impl.convert_snapshot(
        snapshot.Snapshot(
            source="pyreach-test",
            device_data_refs=(snapshot.SnapshotReference(2.0, 1),),
            responses=(snapshot.SnapshotResponse(
                5, "vacuum", "test-vacuum", snapshot.SnapshotReference(3.0, 4)),
                       snapshot.SnapshotResponse(
                           6, "arm", "test-arm",
                           PyReachStatus(
                               time=7.0,
                               status="test-status",
                               script="test-script",
                               error="test-error",
                               progress=8.0,
                               message="test-message",
                               code=9)),
                       snapshot.SnapshotResponse(
                           10, "oracle", "test-oracle",
                           PyReachStatus(
                               time=11.0,
                               sequence=12,
                               status="test-status",
                               script="test-script",
                               error="test-error",
                               progress=13.0,
                               message="test-message",
                               code=14))),
            gym_server_time=0.001,
            gym_env_id="test-env-id",
            gym_run_id="test-run-id",
            gym_episode=1,
            gym_step=2,
            gym_reward=3.0,
            gym_done=True,
            gym_actions=(snapshot.SnapshotGymAction("test-type", "test-name",
                                                    True),
                         snapshot.SnapshotGymVacuumAction(
                             "test-vacuum", "vacuum", True, 1),
                         snapshot.SnapshotGymLoggerAction(
                             "test-logger", "logger", False, True, {
                                 "1": "2",
                                 "3": "4"
                             }),
                         snapshot.SnapshotGymArmAction(
                             "test-arm", "arm", True, 1, 2,
                             (1.1, 2.2, 3.3, 4.4, 5.5, 6.6),
                             (1.0, 2.0, 3.0, 4.0, 5.0, 6.0), True, 4.0, 5.0,
                             6.0, "test-action", True, "test-intent", "success",
                             "test-id", True, True, 7.0, 8.0, 9.0, True,
                             "test-controller"))))
    self.assertIsNotNone(snapshot_cmd)
    expect_snapshot = types_gen.Snapshot(
        source="pyreach-test",
        device_data_refs=[types_gen.DeviceDataRef(ts=2000, seq=1)],
        responses=[
            types_gen.SnapshotResponse(
                cid=5,
                gym_element_type="vacuum",
                gym_config_name="test-vacuum",
                device_data_ref=types_gen.DeviceDataRef(ts=3000, seq=4)),
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
                device_data_ref=types_gen.DeviceDataRef(ts=11000, seq=12))
        ],
        gym_server_ts=1,
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
                device_type="test-logger",
                device_name="logger",
                synchronous=False,
                logger_action_params=types_gen.LoggerActionParams([
                    types_gen.KeyValue(key="1", value="2"),
                    types_gen.KeyValue(key="3", value="4")
                ], True)),
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
                    allow_uncalibrated=True,
                    controller_name="test-controller"))
        ],
        gym_env_id="test-env-id",
        gym_run_id="test-run-id",
        gym_episode=1,
        gym_step=2,
        gym_reward=3.0,
        gym_done=True)
    assert snapshot_cmd is not None
    self.assertEqual(
        json.dumps(snapshot_cmd.to_json(), indent="  "),
        json.dumps(expect_snapshot.to_json(), indent="  "))


if __name__ == "__main__":
  unittest.main()
