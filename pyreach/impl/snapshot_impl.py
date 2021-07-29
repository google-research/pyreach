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

"""Implementation for snapshot conversion."""
import logging
from typing import List, Optional

from pyreach.common.python import types_gen
from pyreach.core import PyReachStatus
from pyreach.impl import utils
from pyreach.snapshot import Snapshot
from pyreach.snapshot import SnapshotGymAction
from pyreach.snapshot import SnapshotGymArmAction
from pyreach.snapshot import SnapshotGymLoggerAction
from pyreach.snapshot import SnapshotGymVacuumAction
from pyreach.snapshot import SnapshotReference
from pyreach.snapshot import SnapshotResponse


def reverse_snapshot(
    snapshot: Optional[types_gen.Snapshot]) -> Optional[Snapshot]:
  """Convert a types_gen Snapshot to a PyReach Snapshot.

  Args:
    snapshot: The input types_gen Snapshot to convert.

  Returns:
    The PyReach Snapshot, or None if the input is None.
  """
  if snapshot is None:
    return None
  device_data_refs: List[SnapshotReference] = []
  for ref in snapshot.device_data_refs:
    device_data_refs.append(
        SnapshotReference(
            time=utils.time_at_timestamp(ref.ts), sequence=ref.seq))
  responses: List[SnapshotResponse] = []
  for resp in snapshot.responses:
    if (resp.status and
        (not resp.device_data_ref or resp.device_data_ref.seq <= 0)):
      time: float = 0.0
      if resp.device_data_ref:
        time = utils.time_at_timestamp(resp.device_data_ref.ts)
      responses.append(
          SnapshotResponse(
              resp.cid, resp.gym_element_type, resp.gym_config_name,
              utils.reverse_pyreach_status(resp.status, timestamp=time)))
    elif resp.device_data_ref:
      responses.append(
          SnapshotResponse(
              resp.cid, resp.gym_element_type, resp.gym_config_name,
              SnapshotReference(
                  time=utils.time_at_timestamp(resp.device_data_ref.ts),
                  sequence=resp.device_data_ref.seq)))
  gym_actions: List[SnapshotGymAction] = []
  for action in snapshot.gym_actions:
    if action.arm_action_params is not None:
      if action.vacuum_action_params is not None:
        logging.warning(
            "Gym action snapshot contains bot armActionParams "
            "and vacuumActionParams: %s", str(action.to_json()))
      gym_actions.append(
          SnapshotGymArmAction(
              device_type=action.device_type,
              device_name=action.device_name,
              synchronous=action.synchronous,
              command=action.arm_action_params.command,
              cid=action.arm_action_params.cid,
              joint_angles=tuple(action.arm_action_params.joint_angles),
              use_linear=action.arm_action_params.use_linear,
              velocity=action.arm_action_params.velocity,
              acceleration=action.arm_action_params.acceleration,
              pose=tuple(action.arm_action_params.pose),
              action_name=action.arm_action_params.action_name,
              use_unity_ik=action.arm_action_params.use_unity_ik,
              intent=action.arm_action_params.intent,
              success_type=action.arm_action_params.success_type,
              pick_id=action.arm_action_params.pick_id,
              apply_tip_adjust_transform=action.arm_action_params
              .apply_tip_adjust_transform,
              servo=action.arm_action_params.servo,
              servo_time_seconds=action.arm_action_params.servo_t_secs,
              servo_lookahead_time_seconds=action.arm_action_params
              .servo_lookahead_time_secs,
              servo_gain=action.arm_action_params.servo_gain,
              allow_uncalibrated=action.arm_action_params.allow_uncalibrated,
              timeout_sec=action.arm_action_params.timeout_sec))
    elif action.vacuum_action_params is not None:
      gym_actions.append(
          SnapshotGymVacuumAction(
              device_type=action.device_type,
              device_name=action.device_name,
              synchronous=action.synchronous,
              state=action.vacuum_action_params.state))
    elif action.logger_action_params is not None:
      gym_actions.append(
          SnapshotGymLoggerAction(
              device_type=action.device_type,
              device_name=action.device_name,
              synchronous=action.synchronous,
              is_start=action.logger_action_params.is_start,
              event_params=dict([
                  (data.key, data.value)
                  for data in action.logger_action_params.event_params
              ]),
          ))
    else:
      gym_actions.append(
          SnapshotGymAction(
              device_type=action.device_type,
              device_name=action.device_name,
              synchronous=action.synchronous))
  return Snapshot(
      source=snapshot.source,
      gym_env_id=snapshot.gym_env_id,
      gym_run_id=snapshot.gym_run_id,
      gym_episode=snapshot.gym_episode,
      gym_step=snapshot.gym_step,
      gym_reward=snapshot.gym_reward,
      gym_done=snapshot.gym_done,
      device_data_refs=tuple(device_data_refs),
      responses=tuple(responses),
      gym_actions=tuple(gym_actions))


def convert_snapshot(
    snapshot: Optional[Snapshot]) -> Optional[types_gen.Snapshot]:
  """Convert a PyReach Snapshot to a types_gen Snapshot.

  Args:
    snapshot: The input PyReach Snapshot to convert.

  Returns:
    The types_gen Snapshot, or None if the input is None.
  """
  if snapshot is None:
    return None
  device_data_refs = []
  for ref in snapshot.device_data_refs:
    device_data_refs.append(
        types_gen.DeviceDataRef(
            ts=utils.timestamp_at_time(ref.time), seq=ref.sequence))
  responses = []
  for resp in snapshot.responses:
    if isinstance(resp.reference,
                  PyReachStatus) and resp.reference.sequence <= 0:
      responses.append(
          types_gen.SnapshotResponse(
              cid=resp.cid,
              gym_element_type=resp.gym_element_type,
              gym_config_name=resp.gym_config_name,
              device_data_ref=types_gen.DeviceDataRef(
                  ts=utils.timestamp_at_time(resp.reference.time)),
              status=utils.convert_pyreach_status(resp.reference)))
    elif isinstance(resp.reference, (SnapshotReference, PyReachStatus)):
      responses.append(
          types_gen.SnapshotResponse(
              cid=resp.cid,
              gym_element_type=resp.gym_element_type,
              gym_config_name=resp.gym_config_name,
              device_data_ref=types_gen.DeviceDataRef(
                  ts=utils.timestamp_at_time(resp.reference.time),
                  seq=resp.reference.sequence)))
  gym_actions = []
  for action in snapshot.gym_actions:
    arm_params = None
    vacuum_params = None
    logger_params = None
    if isinstance(action, SnapshotGymArmAction):
      arm_params = types_gen.ArmActionParams(
          command=action.command,
          cid=action.cid,
          joint_angles=list(action.joint_angles),
          use_linear=action.use_linear,
          velocity=action.velocity,
          acceleration=action.acceleration,
          pose=list(action.pose),
          action_name=action.action_name,
          use_unity_ik=action.use_unity_ik,
          intent=action.intent,
          success_type=action.success_type,
          pick_id=action.pick_id,
          apply_tip_adjust_transform=action.apply_tip_adjust_transform,
          servo=action.servo,
          servo_t_secs=action.servo_time_seconds,
          servo_lookahead_time_secs=action.servo_lookahead_time_seconds,
          servo_gain=action.servo_gain,
          allow_uncalibrated=action.allow_uncalibrated,
          timeout_sec=action.timeout_sec)
    elif isinstance(action, SnapshotGymVacuumAction):
      vacuum_params = types_gen.VacuumActionParams(state=action.state)
    elif isinstance(action, SnapshotGymLoggerAction):
      logger_params = types_gen.LoggerActionParams(
          is_start=action.is_start,
          event_params=[
              types_gen.KeyValue(key=key, value=value)
              for key, value in sorted(action.event_params.items())
          ])
    gym_actions.append(
        types_gen.GymAction(
            device_type=action.device_type,
            device_name=action.device_name,
            synchronous=action.synchronous,
            arm_action_params=arm_params,
            vacuum_action_params=vacuum_params,
            logger_action_params=logger_params))
  return types_gen.Snapshot(
      source=snapshot.source,
      gym_env_id=snapshot.gym_env_id,
      gym_run_id=snapshot.gym_run_id,
      gym_episode=snapshot.gym_episode,
      gym_step=snapshot.gym_step,
      gym_reward=snapshot.gym_reward,
      gym_done=snapshot.gym_done,
      device_data_refs=device_data_refs,
      responses=responses,
      gym_actions=gym_actions)
