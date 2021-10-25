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
"""Interface for generating snapshots for client state logging."""

import dataclasses
from typing import Dict, Tuple, Union

from pyreach.common.proto_gen import logs_pb2
from pyreach.core import PyReachStatus


@dataclasses.dataclass(frozen=True)
class SnapshotReference:
  """Represents a snapshot device data reference.

  Attributes:
    time: the time referenced.
    sequence: the sequence number.
  """
  time: float
  sequence: int


@dataclasses.dataclass(frozen=True)
class SnapshotResponse:
  """Represents a snapshot response device data reference.

  Attributes:
    cid: the cid of the command.
    gym_element_type: the device type for the response.
    gym_config_name: the device name for the response.
    reference: the reference or the status for the data.
  """
  cid: int
  gym_element_type: str
  gym_config_name: str
  reference: Union[SnapshotReference, PyReachStatus]


@dataclasses.dataclass(frozen=True)
class SnapshotGymAction:
  """Represents the logger snapshot.

  Attributes:
    device_type: The device type for the logger action.
    device_name: The device name for the logger action.
    synchronous: If the action is synchronous.
  """
  device_type: str
  device_name: str
  synchronous: bool


@dataclasses.dataclass(frozen=True)
class SnapshotGymArmAction(SnapshotGymAction):
  """Represents the arm action.

  Attributes:
    command: the arm command.
    cid: the cid.
    joint_angles: the joint angles.
    pose: the pose.
    use_linear: True if a linear translation is required.
    velocity: The max velocity.
    acceleration: The max acceleration.
    timeout_sec: the timeout in seconds.
    action_name: the name of the action to execute.
    use_unity_ik: True to use Unity IK format.
    intent: pick intent for the action.
    success_type: success type for the action.
    pick_id: pick ID for the action.
    apply_tip_adjust_transform: Apply the transform of the tip adjust.
    servo: Use servo mode.
    servo_time_seconds: Time to block the robot for (servo + UR only).
    servo_lookahead_time_seconds: Lookahead time for trajectory smoothing (servo
      + UR only).
    servo_gain: Gain for the servoing - if zero, defaults to 300 (servo + UR
      only).
    allow_uncalibrated: Allow motion when uncalibrated (unsafe, should only be
      set in calibration code).
    controller_name: The name of the controller to send the command to.
  """
  command: int
  cid: int
  joint_angles: Tuple[float, ...] = ()
  pose: Tuple[float, ...] = ()
  use_linear: bool = False
  velocity: float = False
  acceleration: float = 0.0
  timeout_sec: float = 0.0
  action_name: str = ""
  use_unity_ik: bool = False
  intent: str = ""
  success_type: str = ""
  pick_id: str = ""
  apply_tip_adjust_transform: bool = False
  servo: bool = False
  servo_time_seconds: float = 0.0
  servo_lookahead_time_seconds: float = 0.0
  servo_gain: float = 0.0
  allow_uncalibrated: bool = False
  controller_name: str = ""


@dataclasses.dataclass(frozen=True)
class SnapshotGymVacuumAction(SnapshotGymAction):
  """Represents the vacuum action.

  Attributes:
    state: the vacuum state.
  """
  state: int


@dataclasses.dataclass(frozen=True)
class SnapshotGymLoggerAction(SnapshotGymAction):
  """Represents the logger action.

  Attributes:
    is_start: true if a start task for the logger.
    event_params: task event parameters.
  """
  is_start: bool
  event_params: Dict[str, str]


@dataclasses.dataclass(frozen=True)
class SnapshotGymClientAnnotationAction(SnapshotGymAction):
  """Represents the client annotation action.

  Attributes:
    annotation: the annotation written
  """
  annotation: logs_pb2.ClientAnnotation


@dataclasses.dataclass(frozen=True)
class Snapshot:
  """Represents the logger snapshot.

  Attributes:
    source: The application source that generates this snapshot.
    device_data_refs: The logger snapshot references.
    responses: The response snapshot references.
    gym_server_time: The estimated server-side time at snapshot creation.
    gym_env_id: The gym environment ID.
    gym_run_id: The gym run ID.
    gym_episode: The gym episode number starting with 1 for the first episode.
    gym_step: The gym step number for the current episode starting with 0.
    gym_reward: The reward returned by the gym step.
    gym_done: True if the gym is complete.
    gym_actions: The actions for the gym step.
  """
  source: str
  device_data_refs: Tuple[SnapshotReference, ...]
  responses: Tuple[SnapshotResponse, ...]
  gym_server_time: float
  gym_env_id: str
  gym_run_id: str
  gym_episode: int
  gym_step: int
  gym_reward: float
  gym_done: bool
  gym_actions: Tuple[SnapshotGymAction, ...]
