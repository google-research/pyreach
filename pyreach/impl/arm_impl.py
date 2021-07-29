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

"""Implementation of the PyReach Arm interface."""

import enum
import json
import logging  # type: ignore
import threading
from typing import Callable, Dict, List, Optional, Set, Tuple, Union, cast

import numpy as np  # type: ignore

from pyreach import arm
from pyreach import calibration
from pyreach import constraints
from pyreach import core
from pyreach import internal
from pyreach.common.base import transform_util
from pyreach.common.python import types_gen
from pyreach.ik_pybullet import ik_pybullet
from pyreach.ikfast import ikfast
from pyreach.impl import actions_impl
from pyreach.impl import calibration_impl
from pyreach.impl import constraints_impl
from pyreach.impl import device_base
from pyreach.impl import requester
from pyreach.impl import thread_util
from pyreach.impl import utils
from pyreach.common.proto_gen import workcell_io_pb2 as workcell_io


class ActionVacuumState(enum.Enum):
  """ActionVacuumState specifies the desired vacuum state in an action."""

  OFF = 0
  VACUUM = 1
  BLOWOFF = 2


class ArmTypeImpl(arm.ArmType):
  """Implementation for an arm type."""
  _urdf_file: str
  _joint_count: int

  def __init__(self, urdf_file: str, joint_count: int):
    """Create an ArmTypeImpl.

    Args:
      urdf_file: the urdf file.
      joint_count: the number of joints in the arm.
    """
    self._urdf_file = urdf_file
    self._joint_count = joint_count

  @property
  def urdf_file(self) -> str:
    """Converts an arm_type to an associate URDF."""
    return self._urdf_file

  @property
  def joint_count(self) -> int:
    """Get the joint count of the arm."""
    return self._joint_count

  @classmethod
  def from_urdf_file(cls, urdf_file: str) -> arm.ArmType:
    if urdf_file in {
        "ur5.urdf", "ur5e.urdf", "ur5e.urdf", "ur10e.urdf", "lrmate200ic.urdf",
        "lrmate200id.urdf", "FanucCR7ia.urdf", "FanucLrmate200id7l.urdf",
        "FanucR2000ia165f.urdf", "XArm6.urdf"
    }:
      return ArmTypeImpl(urdf_file, 6)
    raise ValueError("invalid URDF file: " + urdf_file)


class _Command:
  """Represents a Arm command.

  This is a base class from which all other Arm commands are
  sub-classed.  This this class basically just defines virtual methods
  that get implemented as needed by the sub-class.  It is used to
  convert Arm Commands to lower level Reach Script commands.
  """

  def __init__(self) -> None:
    """Init Arm Command base instance."""
    pass

  def to_reach_script(
      self,
      arm_type: arm.ArmType,
      support_vacuum: bool,
      support_blowoff: bool,
      ik_lib: Optional[Union[ikfast.IKFast, ik_pybullet.IKPybullet]],
      ik_hints: Dict[int, List[float]],
      state: arm.ArmState,
      arm_origin: Optional[np.ndarray],
      tip_adjust_transform: Optional[np.ndarray],
  ) -> List[types_gen.ReachScriptCommand]:
    """Generate Reach Script for an Arm command.

    Args:
      arm_type: The type of the arm.
      support_vacuum: True if vacuum is supported.
      support_blowoff: True if blowoff is supported.
      ik_lib: An optional inverse kinimatics module.
      ik_hints: The ik hints.
      state: The arm state.
      arm_origin: The origin of the arm.
      tip_adjust_transform: The transform of the adjusted tip.

    Returns:
      A list of Reach Script Commands is returned.
    """
    raise NotImplementedError


class _MoveJoints(_Command):
  """An Command used to arm joint angles."""

  _joints: List[float]
  _velocity: float
  _acceleration: float
  _servo: bool
  _servo_time_seconds: float
  _servo_lookahead_time_seconds: float
  _servo_gain: float

  def __init__(self,
               joints: List[float],
               velocity: float = 0.0,
               acceleration: float = 0.0,
               servo: bool = False,
               servo_time_seconds: float = 0.0,
               servo_lookahead_time_seconds: float = 0.0,
               servo_gain: float = 0.0) -> None:
    """Construct a move joints command.

    Args:
      joints: Desired joint angles.
      velocity: Max velocity.
      acceleration: Max acceleration.
      servo: Use servo mode.
      servo_time_seconds: Time to block the robot for (servo + UR only).
      servo_lookahead_time_seconds: Lookahead time for trajectory smoothing
        (servo + UR only).
      servo_gain: Gain for the servoing - if zero, defaults to 300 (servo + UR
        only).
    """
    super().__init__()
    self._joints = joints
    self._velocity = velocity
    self._acceleration = acceleration
    self._servo = servo
    self._servo_time_seconds = servo_time_seconds
    self._servo_lookahead_time_seconds = servo_lookahead_time_seconds
    self._servo_gain = servo_gain

  def to_reach_script(
      self,
      arm_type: arm.ArmType,
      support_vacuum: bool,
      support_blowoff: bool,
      ik_lib: Optional[Union[ikfast.IKFast, ik_pybullet.IKPybullet]],
      ik_hints: Dict[int, List[float]],
      state: arm.ArmState,
      arm_origin: Optional[np.ndarray],
      tip_adjust_transform: Optional[np.ndarray],
  ) -> List[types_gen.ReachScriptCommand]:
    """Convert Arm Move Joints to Reach Script.

    Args:
      arm_type: The type of the arm.
      support_vacuum: True if vacuum is supported.
      support_blowoff: True if blowoff is supported.
      ik_lib: An optional inverse kinimatics module.
      ik_hints: The ik hints.
      state: The arm state.
      arm_origin: The origin of the arm.
      tip_adjust_transform: The transform of the adjusted tip.

    Returns:
      Generated ReachScript command.
    """
    if arm_type.joint_count != len(self._joints):
      raise core.PyReachError("Invalid joint count in MoveJoints")
    return [
        types_gen.ReachScriptCommand(
            move_j_path=types_gen.MoveJPathArgs(waypoints=[
                types_gen.MoveJWaypointArgs(
                    rotation=self._joints,
                    velocity=self._velocity,
                    acceleration=self._acceleration,
                    servo=self._servo,
                    servo_t_secs=self._servo_time_seconds,
                    servo_lookahead_time_secs=self
                    ._servo_lookahead_time_seconds,
                    servo_gain=self._servo_gain)
            ]))
    ]


class _MoveLinear(_Command):
  """An Command to move 'linearly' to specified joint angles."""

  _joints: List[float]
  _velocity: float
  _acceleration: float
  _servo: bool

  def __init__(self,
               joints: List[float],
               velocity: float = 0.0,
               acceleration: float = 0.0,
               servo: bool = False) -> None:
    """Construct the Arm Move Linear command with its desired joints.

    Args:
      joints: Desired joints.
      velocity: Max velocity.
      acceleration: Max acceleration.
      servo: Use servo mode.
    """
    super().__init__()
    self._joints = joints
    self._velocity = velocity
    self._acceleration = acceleration
    self._servo = servo

  def to_reach_script(
      self,
      arm_type: arm.ArmType,
      support_vacuum: bool,
      support_blowoff: bool,
      ik_lib: Optional[Union[ikfast.IKFast, ik_pybullet.IKPybullet]],
      ik_hints: Dict[int, List[float]],
      state: arm.ArmState,
      arm_origin: Optional[np.ndarray],
      tip_adjust_transform: Optional[np.ndarray],
  ) -> List[types_gen.ReachScriptCommand]:
    """Convert an MoveLinear to Reach Script.

    Args:
      arm_type: The type of Arm being used.
      support_vacuum: True if vacuum is supported.
      support_blowoff: True if blowoff is supported.
      ik_lib: An optional inverse kinimatics module.
      ik_hints: The ik hints.
      state: The arm state.
      arm_origin: The origin of the arm.
      tip_adjust_transform: The transform of the adjusted tip.

    Returns:
      The Reach Script to perform the linear move.
    """
    if arm_type.joint_count != len(self._joints):
      raise core.PyReachError("Invalid joint count in MoveLinear")
    return [
        types_gen.ReachScriptCommand(
            move_l_path=types_gen.MoveLPathArgs(waypoints=[
                types_gen.MoveLWaypointArgs(
                    rotation=self._joints,
                    velocity=self._velocity,
                    acceleration=self._acceleration,
                    servo=self._servo)
            ]))
    ]


class _MovePose(_Command):
  """An Command to move an Arm to a specified Pose."""

  _translation: types_gen.Vec3d
  _rotation: types_gen.Vec3d
  _velocity: float
  _acceleration: float
  _use_linear: bool
  _servo: bool
  _use_unity_ik: bool
  _apply_tip_adjust_transform: bool
  _servo_time_seconds: float
  _servo_lookahead_time_seconds: float
  _servo_gain: float

  def __init__(self,
               translation: types_gen.Vec3d,
               rotation: types_gen.Vec3d,
               velocity: float = 0.0,
               acceleration: float = 0.0,
               use_linear: bool = False,
               servo: bool = False,
               use_unity_ik: bool = False,
               apply_tip_adjust_transform: bool = False,
               servo_time_seconds: float = 0.0,
               servo_lookahead_time_seconds: float = 0.0,
               servo_gain: float = 0.0) -> None:
    """Construct the MovePose object.

    Args:
      translation: The [X,Y,Z] location to translate to.
      rotation: The rotation represented in angle-axis notation, [AX, AY, AZ]
        specifying the rotation axis and the length of the axis specifying the
        rotation in radians.
      velocity: The max velocity.
      acceleration: The max acceleration.
      use_linear: True if a linear translation is required.
      servo: Use servo mode.
      use_unity_ik: True to use Unity IK format.
      apply_tip_adjust_transform: Apply the transform of the tip adjust.
      servo_time_seconds: Time to block the robot for (servo + UR only).
      servo_lookahead_time_seconds: Lookahead time for trajectory smoothing
        (servo + UR only).
      servo_gain: Gain for the servoing - if zero, defaults to 300 (servo + UR
        only).
    """
    super().__init__()
    self._translation = translation
    self._rotation = rotation
    self._velocity = velocity
    self._acceleration = acceleration
    self._use_linear = use_linear
    self._servo = servo
    self._use_unity_ik = use_unity_ik
    self._apply_tip_adjust_transform = apply_tip_adjust_transform
    self._servo_time_seconds = servo_time_seconds
    self._servo_lookahead_time_seconds = servo_lookahead_time_seconds
    self._servo_gain = servo_gain

  def to_reach_script(
      self, arm_type: arm.ArmType, support_vacuum: bool, support_blowoff: bool,
      ik_lib: Optional[Union[ikfast.IKFast, ik_pybullet.IKPybullet]],
      ik_hints: Dict[int, List[float]], state: arm.ArmState,
      arm_origin: Optional[np.ndarray],
      tip_adjust_transform: Optional[np.ndarray]
  ) -> List[types_gen.ReachScriptCommand]:
    """Convert ArmMovePost to Reach Script commands.

    Args:
      arm_type: The type of arm to use.
      support_vacuum: True if vacuum is supported.
      support_blowoff: True if blowoff is supported.
      ik_lib: An optional inverse kinimatics object.
      ik_hints: The ik hints.
      state: The arm state.
      arm_origin: The arm origin transform.
      tip_adjust_transform: The transform of the adjusted tip.

    Returns:
      A list Reach Commands to perform the translation.
    """
    pose = np.array([
        self._translation.x, self._translation.y, self._translation.z,
        self._rotation.x, self._rotation.y, self._rotation.z
    ])
    if self._apply_tip_adjust_transform:
      if tip_adjust_transform is not None:
        pose = transform_util.multiply_pose(pose, tip_adjust_transform)
      else:
        raise core.PyReachError("Calibration was not loaded")
    if ik_lib is not None:
      if not ik_hints:
        raise core.PyReachError("IKhints have not been loaded")

      if isinstance(ik_lib, ikfast.IKFast):
        if self._use_unity_ik:
          joints = ik_lib.unity_ik_solve_search(pose, list(state.joint_angles),
                                                ik_hints)
        else:
          joints = ik_lib.ik_search(pose, ik_hints)
      elif isinstance(ik_lib, ik_pybullet.IKPybullet):
        joints = ik_lib.ik_search(pose, np.array(state.joint_angles))
      else:
        raise core.PyReachError("Unsupported IK library")

      if joints is None:
        raise core.PyReachError("IK failed to find solution")
      if self._use_linear:
        return _MoveLinear(joints.tolist(), self._velocity,
                           self._acceleration, self._servo).to_reach_script(
                               arm_type, support_vacuum, support_blowoff,
                               ik_lib, ik_hints, state, arm_origin,
                               tip_adjust_transform)
      else:
        return _MoveJoints(
            joints.tolist(),
            self._velocity,
            self._acceleration,
            self._servo,
            servo_time_seconds=self._servo_time_seconds,
            servo_lookahead_time_seconds=self._servo_lookahead_time_seconds,
            servo_gain=self._servo_gain).to_reach_script(
                arm_type, support_vacuum, support_blowoff, ik_lib, ik_hints,
                state, arm_origin, tip_adjust_transform)
    else:
      return [
          types_gen.ReachScriptCommand(
              move_pose_path=types_gen.MovePosePathArgs(waypoints=[
                  types_gen.MovePoseWaypointArgs(
                      translation=types_gen.Vec3d(pose[0], pose[1], pose[2]),
                      rotation=types_gen.Vec3d(pose[3], pose[4], pose[5]),
                      velocity=self._velocity,
                      acceleration=self._acceleration)
              ]))
      ]


class _SetVacuumState(_Command):
  """An Arm Command to set the vacuum state."""

  _state: ActionVacuumState

  def __init__(self, state: ActionVacuumState) -> None:
    """Init the vacuum state for an Arm Command."""
    super().__init__()
    self._state = state

  # pylint: disable=unused-argument
  def to_reach_script(
      self,
      arm_type: arm.ArmType,
      support_vacuum: bool,
      support_blowoff: bool,
      ik_lib: Optional[Union[ikfast.IKFast, ik_pybullet.IKPybullet]],
      ik_hints: Dict[int, List[float]],
      state: arm.ArmState,
      arm_origin: Optional[np.ndarray],
      tip_adjust_transform: Optional[np.ndarray],
  ) -> List[types_gen.ReachScriptCommand]:
    """Convert an SetVacuumState into some ReachScript commands.

    Args:
      arm_type: The type of arm to use.
      support_vacuum: True if vacuum is supported.
      support_blowoff: True if blowoff is supported.
      ik_lib: An optional inverse kinematics object.
      ik_hints: The ik hints.
      state: The arm state.
      arm_origin: The origin of the arm.
      tip_adjust_transform: The transform of the adjusted tip.

    Returns:
      A list Reach Commands to perform the translation.
    """
    if not support_vacuum:
      raise core.PyReachError("Robot does not support vacuum")
    cmds = [
        types_gen.ReachScriptCommand(
            set_output=types_gen.SetOutput(
                py_type="vacuum",
                name="",
                args=[
                    types_gen.CapabilityState(
                        pin="",
                        int_value=int(self._state == ActionVacuumState.VACUUM))
                ]))
    ]
    if support_blowoff:
      cmds.append(
          types_gen.ReachScriptCommand(
              set_output=types_gen.SetOutput(
                  py_type="blowoff",
                  name="",
                  args=[
                      types_gen.CapabilityState(
                          pin="",
                          int_value=int(
                              self._state == ActionVacuumState.BLOWOFF))
                  ])))
    elif self._state == ActionVacuumState.BLOWOFF:
      raise core.PyReachError("Robot does not support blowoff")
    return cmds


class _SetDigitalOut(_Command):
  """An Arm Command to set digital out."""

  _output: int
  _value: bool

  def __init__(self, output: int, value: bool) -> None:
    """Init the output state for an Arm Command."""
    super().__init__()
    self._output = output
    self._value = value

  # pylint: disable=unused-argument
  def to_reach_script(
      self,
      arm_type: arm.ArmType,
      support_vacuum: bool,
      support_blowoff: bool,
      ik_lib: Optional[Union[ikfast.IKFast, ik_pybullet.IKPybullet]],
      ik_hints: Dict[int, List[float]],
      state: arm.ArmState,
      arm_origin: Optional[np.ndarray],
      tip_adjust_transform: Optional[np.ndarray],
  ) -> List[types_gen.ReachScriptCommand]:
    """Convert a SetDigitalOut into some ReachScript commands.

    Args:
      arm_type: The type of arm to use.
      support_vacuum: True if vacuum is supported.
      support_blowoff: True if blowoff is supported.
      ik_lib: An optional inverse kinematics object.
      ik_hints: The ik hints.
      state: The arm state.
      arm_origin: The origin of the arm.
      tip_adjust_transform: The transform of the adjusted tip.

    Returns:
      A list Reach Commands to perform the translation.
    """
    return [
        types_gen.ReachScriptCommand(
            set_digital_out=types_gen.SetDigitalOutArgs(
                output=self._output, value=self._value))
    ]


class _SetToolDigitalOut(_Command):
  """An Arm Command to set tool digital out."""

  _output: int
  _value: bool

  def __init__(self, output: int, value: bool) -> None:
    """Init the tool output state for an Arm Command."""
    super().__init__()
    self._output = output
    self._value = value

  # pylint: disable=unused-argument
  def to_reach_script(
      self,
      arm_type: arm.ArmType,
      support_vacuum: bool,
      support_blowoff: bool,
      ik_lib: Optional[Union[ikfast.IKFast, ik_pybullet.IKPybullet]],
      ik_hints: Dict[int, List[float]],
      state: arm.ArmState,
      arm_origin: Optional[np.ndarray],
      tip_adjust_transform: Optional[np.ndarray],
  ) -> List[types_gen.ReachScriptCommand]:
    """Convert a SetToolDigitalOut into some ReachScript commands.

    Args:
      arm_type: The type of arm to use.
      support_vacuum: True if vacuum is supported.
      support_blowoff: True if blowoff is supported.
      ik_lib: An optional inverse kinematics object.
      ik_hints: The ik hints.
      state: The arm state.
      arm_origin: The origin of the arm.
      tip_adjust_transform: The transform of the adjusted tip.

    Returns:
      A list Reach Commands to perform the translation.
    """
    return [
        types_gen.ReachScriptCommand(
            set_tool_digital_out=types_gen.SetDigitalOutArgs(
                output=self._output, value=self._value))
    ]


class _SetAnalogOut(_Command):
  """An Arm Command to set analog out."""

  _output: int
  _value: float

  def __init__(self, output: int, value: float) -> None:
    """Init the tool output state for an Arm Command."""
    super().__init__()
    self._output = output
    self._value = value

  # pylint: disable=unused-argument
  def to_reach_script(
      self,
      arm_type: arm.ArmType,
      support_vacuum: bool,
      support_blowoff: bool,
      ik_lib: Optional[Union[ikfast.IKFast, ik_pybullet.IKPybullet]],
      ik_hints: Dict[int, List[float]],
      state: arm.ArmState,
      arm_origin: Optional[np.ndarray],
      tip_adjust_transform: Optional[np.ndarray],
  ) -> List[types_gen.ReachScriptCommand]:
    """Convert a SetAnalogOut into some ReachScript commands.

    Args:
      arm_type: The type of arm to use.
      support_vacuum: True if vacuum is supported.
      support_blowoff: True if blowoff is supported.
      ik_lib: An optional inverse kinematics object.
      ik_hints: The ik hints.
      state: The arm state.
      arm_origin: The origin of the arm.
      tip_adjust_transform: The transform of the adjusted tip.

    Returns:
      A list Reach Commands to perform the translation.
    """
    return [
        types_gen.ReachScriptCommand(
            set_analog_out=types_gen.SetAnalogOutArgs(
                output=self._output, value=self._value))
    ]


class _SetOutput(_Command):
  """An Arm Command to set output."""

  _type: str
  _name: str
  _int_states: List[Tuple[str, int]]
  _float_states: List[Tuple[str, float]]

  def __init__(self, typ: str, name: str, int_states: List[Tuple[str, int]],
               float_states: List[Tuple[str, float]]):
    """Init the out state for an Arm Command.

    Args:
      typ: The type of the output.
      name: The name of the output.
      int_states: The initial integer states as a list of name/value pairs.
      float_states: The initial float states as a list of name/value pairs.
    """
    super().__init__()
    self._type = typ
    self._name = name
    self._int_states = int_states
    self._float_states = float_states

  # pylint: disable=unused-argument
  def to_reach_script(
      self,
      arm_type: arm.ArmType,
      support_vacuum: bool,
      support_blowoff: bool,
      ik_lib: Optional[Union[ikfast.IKFast, ik_pybullet.IKPybullet]],
      ik_hints: Dict[int, List[float]],
      state: arm.ArmState,
      arm_origin: Optional[np.ndarray],
      tip_adjust_transform: Optional[np.ndarray],
  ) -> List[types_gen.ReachScriptCommand]:
    """Convert a SetAnalogOut into some ReachScript commands.

    Args:
      arm_type: The type of arm to use.
      support_vacuum: True if vacuum is supported.
      support_blowoff: True if blowoff is supported.
      ik_lib: An optional inverse kinematics object.
      ik_hints: The ik hints.
      state: The arm state.
      arm_origin: The origin of the arm.
      tip_adjust_transform: The transform of the adjusted tip.

    Returns:
      A list Reach Commands to perform the translation.
    """
    return [
        types_gen.ReachScriptCommand(
            set_output=types_gen.SetOutput(
                py_type=self._type,
                name=self._name,
                args=[
                    types_gen.CapabilityState(pin=x[0], int_value=x[1])
                    for x in self._int_states
                ] + [
                    types_gen.CapabilityState(pin=x[0], float_value=x[1])
                    for x in self._float_states
                ]))
    ]


class _Stop(_Command):
  """An Stop Command stops the arm."""

  _deceleration: float

  def __init__(self, deceleration: float = 2.0) -> None:
    """Init Stop Arm Command.

    Args:
      deceleration: The deceleration rate in radians/second/second.
    """
    super().__init__()
    self._deceleration = deceleration

  # pylint: disable=unused-argument
  def to_reach_script(
      self,
      arm_type: arm.ArmType,
      support_vacuum: bool,
      support_blowoff: bool,
      ik_lib: Optional[Union[ikfast.IKFast, ik_pybullet.IKPybullet]],
      ik_hints: Dict[int, List[float]],
      state: arm.ArmState,
      arm_origin: Optional[np.ndarray],
      tip_adjust_transform: Optional[np.ndarray],
  ) -> List[types_gen.ReachScriptCommand]:
    """Convert a Stop into some ReachScript commands.

    Args:
      arm_type: The type of arm to use.
      support_vacuum: True if vacuum is supported.
      support_blowoff: True if blowoff is supported.
      ik_lib: An optional inverse kinematics object.
      ik_hints: The ik hints.
      state: The arm state.
      arm_origin: The origin of the arm.
      tip_adjust_transform: The transform of the adjusted tip.

    Returns:
      A list Reach Commands to perform the translation.
    """
    return [
        types_gen.ReachScriptCommand(
            stop_j=types_gen.StopJArgs(deceleration=self._deceleration)),
    ]


class _Commands:
  """A sequence of Commands."""

  _commands: List[_Command]

  def __init__(self, commands: List[_Command]) -> None:
    """Construct the Commands."""
    self._commands = commands

  def to_reach_script(
      self,
      device_name: str,
      tag: str,
      intent: str,
      pick_id: str,
      success_type: str,
      arm_type: arm.ArmType,
      support_vacuum: bool,
      support_blowoff: bool,
      allow_uncalibrated: bool,
      preemptive: bool,
      ik_lib: Optional[Union[ikfast.IKFast, ik_pybullet.IKPybullet]],
      ik_hints: Dict[int, List[float]],
      state: arm.ArmState,
      arm_origin: Optional[np.ndarray],
      tip_adjust_transform: Optional[np.ndarray],
  ) -> types_gen.CommandData:
    """Convert Commands into ReachScript.

    Args:
      device_name: The device name for the Arm.
      tag: The tag to use for the Reach Script.
      intent: The intent of the command.
      pick_id: The pick_id of the command.
      success_type: The success_type of the command.
      arm_type: The type of arm to use.
      support_vacuum: True for supporting vacuum.
      support_blowoff: True for supporting blowoff.
      allow_uncalibrated: Allow motion when uncalibrated (unsafe, should only be
        set in calibration code).
      preemptive: True to preempt existing scripts.
      ik_lib: An optional inverse kinematics object.
      ik_hints: The ik hints.
      state: The arm state.
      arm_origin: The origin of the arm.
      tip_adjust_transform: The transform of the adjusted tip.

    Returns:
      A single Reach CommandData to send to the robot.
    """
    cmds = []
    for x in self._commands:
      cmds.extend(
          x.to_reach_script(arm_type, support_vacuum, support_blowoff, ik_lib,
                            ik_hints, state, arm_origin, tip_adjust_transform))
    return types_gen.CommandData(
        ts=utils.timestamp_now(),
        device_type="robot",
        device_name=device_name,
        data_type="reach-script",
        pick_id=pick_id,
        intent=intent,
        success_type=success_type,
        tag=tag,
        reach_script=types_gen.ReachScript(
            preemptive=preemptive,
            version=0,
            commands=cmds,
            calibration_requirement=types_gen.ReachScriptCalibrationRequirement(
                allow_uncalibrated=allow_uncalibrated)))


class ArmDevice(requester.Requester[arm.ArmState]):
  """A Device represents all of the robot components."""

  _arm_type: arm.ArmType
  _device_name: str
  _ik_lib_lock: threading.Lock
  _ik_hints: Dict[int, List[float]]
  _ik_lib: Optional[Union[ikfast.IKFast, ik_pybullet.IKPybullet]]
  _constraints_device: constraints_impl.ConstraintsDevice
  _calibration: calibration_impl.CalDevice
  _actions: Optional[actions_impl.ActionDevice]
  _support_vacuum: bool
  _support_blowoff: bool
  _timers: internal.Timers

  def __init__(
      self,
      arm_type: arm.ArmType,
      calibration_device: calibration_impl.CalDevice,
      actions: Optional[actions_impl.ActionDevice] = None,
      workcell_io_config: Optional[workcell_io.IOConfig] = None,  # type: ignore
      device_name: str = "",
      ik_lib: Optional[Union[ikfast.IKFast, ik_pybullet.IKPybullet]] = None
  ) -> None:
    """Construct the Arm Device.

    Args:
      arm_type: The arm type.
      calibration_device: The Calibration device.
      actions: The Action device.
      workcell_io_config: Teh workcell IO config.
      device_name: The name of the device.
      ik_lib: Override creation of ikfast.
    """
    requester.Requester.__init__(self)
    self._arm_type = arm_type
    self._device_name = device_name
    self._ik_lib_lock = threading.Lock()
    self._ik_hints = {}
    self._ik_lib = ik_lib
    if not ik_lib:
      self._ik_lib = ikfast.IKFast(arm_type.urdf_file)
    self._constraints_device = constraints_impl.ConstraintsDevice(device_name)
    self._calibration = calibration_device
    self._actions = actions
    self._support_vacuum = False
    self._support_blowoff = False
    self._timers = internal.Timers(set())
    if workcell_io_config is None:
      return
    for capability in workcell_io_config.capability:
      if capability.device_type not in {"ur", "robot"}:
        continue
      if capability.device_name != device_name:
        continue
      if capability.io_type != workcell_io.DIGITAL_OUTPUT:  # type: ignore
        continue
      if capability.type == "vacuum":
        self._support_vacuum = True
      elif capability.type == "blowoff":
        self._support_blowoff = True

  @property
  def constraints(self) -> constraints_impl.ConstraintsDevice:
    """Return the Device constraints device."""
    return self._constraints_device

  def actions(self) -> Optional[actions_impl.ActionDevice]:
    """Return the action device."""
    return self._actions

  def calibration(self) -> calibration_impl.CalDevice:
    """Return the calibration device."""
    return self._calibration

  def support_vacuum(self) -> bool:
    """Return if vacuum is supported."""
    return self._support_vacuum

  def support_blowoff(self) -> bool:
    """Return if blowoff is supported."""
    return self._support_blowoff

  def set_ik_lib(self, ik_lib: arm.IKLibType) -> None:
    """Set the IK library to be used."""
    if ik_lib == arm.IKLibType.IKFAST:
      self._ik_lib = ikfast.IKFast(self._arm_type.urdf_file)
    elif ik_lib == arm.IKLibType.IKPYBULLET:
      self._ik_lib = ik_pybullet.IKPybullet()
    else:
      raise core.PyReachError("IK name not recognized.")

  def on_set_key_value(self, key: device_base.KeyValueKey, value: str) -> None:
    """Invoke on setting of a key-value pair.

    Args:
      key: The KeyValueKey to use.
      value: The value to set it to.
    """
    if (key.device_type != "settings-engine" or key.device_name or
        key.key != "document-config/ikhints"):
      return
    with self._ik_lib_lock:
      if self._ik_lib is not None and value:
        try:
          ikhints_dictionary = json.loads(value)
          ikhints_array = json.loads(ikhints_dictionary.get("hints"))
          if not isinstance(ikhints_array, list):
            raise core.PyReachError("Invalid ikhints")
          hints = {}
          for i, l in enumerate(ikhints_array):
            if not isinstance(l, list):
              raise core.PyReachError("a list within ikhints not a list")
            for v in l:
              if not isinstance(v, (int, float)):
                raise core.PyReachError()
            hints[i] = l
          self._ik_hints = hints
        except core.PyReachError as e:
          logging.warning("document-config/ikhints invalid: %s", str(e))
          self._ik_hints = {}
      elif self._ik_lib is not None:
        self._ik_hints = {}

  def get_message_supplement(
      self, msg: types_gen.DeviceData) -> Optional[arm.ArmState]:
    """Return the message state (if available) from a message.

    Args:
      msg: The message to scan.

    Returns:
      The device State if it is present in the message.

    """
    if self._device_name == msg.device_name and msg.device_type == "ur" and msg.data_type == "ur-state":
      return self._arm_state_from_message(self._arm_type, msg)
    if self._device_name == msg.device_name and msg.device_type == "robot" and msg.data_type == "robot-state":
      return self._arm_state_from_message(self._arm_type, msg)
    return None

  def get_key_values(self) -> Set[device_base.KeyValueKey]:
    """Return the current set of key/value pairs."""
    return {
        device_base.KeyValueKey(
            device_type="settings-engine",
            device_name="",
            key="document-config/ikhints")
    }

  @property
  def device_name(self) -> str:
    """Return the device name."""
    return self._device_name

  def reset_sim(self,
                callback: Optional[Callable[[core.PyReachStatus], None]] = None,
                finished_callback: Optional[Callable[[], None]] = None,
                timeout: Optional[float] = None) -> None:
    """Reset the simulator if it is present.

    Args:
        callback: An optional callback called when new status is available.
        finished_callback: A n optional function that is called when finished.
        timeout: The time in seconds to wait for the simulator reset.
    """
    tag = utils.generate_tag()
    script = types_gen.CommandData(
        ts=utils.timestamp_now(),
        device_type="script-engine",
        data_type="run-script",
        tag=tag,
        script="sim reset")
    _ = self.send_tagged_request(script)
    return None

  def fk(self,
         joints: Union[Tuple[float, ...], List[float], np.ndarray],
         apply_tip_adjust_transform: bool = False) -> Optional[core.Pose]:
    """Uses forward kinematics to get the pose from the joint angles.

    Args:
      joints: The robot joints.
      apply_tip_adjust_transform: If True, will use the data in the calibration
        file for the robot to change the returned pose from the end of the arm
        to the tip of the end-effector.

    Returns:
      The pose for the end of the arm, or if apply_tip_adjust_transform was
      set to True, the pose for the tip of the end-effector. If the IK library
      was not yet initialized, this will return None.
    """

    pose: Optional[np.ndarray] = None

    with self._ik_lib_lock:
      if isinstance(self._ik_lib, ikfast.IKFast):
        pose = self._ik_lib.fk(joints)
      elif isinstance(self._ik_lib, ik_pybullet.IKPybullet):
        pose = self._ik_lib.fk(np.ndarray(joints))

    if pose is None:
      return None

    if not apply_tip_adjust_transform:
      return core.Pose.from_list(pose.tolist())

    calib = self.calibration().get()
    if calib:
      tip_obj = None
      arm_end_t_tip = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
      for dev in calib.get_all_devices():
        if (dev.device_type == "object" and dev.sub_type == "tip" and
            dev.tool_mount in {"robot", "ur"} and
            isinstance(dev, calibration.CalibrationObject)):
          tip_obj = cast(calibration.CalibrationObject, dev)
          if tip_obj.extrinsics:
            arm_end_t_tip = np.array(tip_obj.extrinsics, dtype=np.float64)

      if tip_obj:
        for dev in calib.get_all_devices():
          if (dev.device_type == "object" and dev.sub_type == "tip" and
              dev.tool_mount == ("object-" + tip_obj.device_name) and
              isinstance(dev, calibration.CalibrationObject)):
            tip_adjust_obj = cast(calibration.CalibrationObject, dev)
            if tip_adjust_obj.extrinsics:
              arm_end_t_tip = transform_util.multiply_pose(
                  arm_end_t_tip,
                  np.array(tip_adjust_obj.extrinsics, dtype=np.float64))

      pose = transform_util.multiply_pose(pose, arm_end_t_tip)

    return core.Pose.from_list(pose.tolist())

  def run_command(self,
                  commands: _Commands,
                  intent: str = "",
                  pick_id: str = "",
                  success_type: str = "",
                  allow_uncalibrated: bool = False,
                  preemptive: bool = False,
                  callback: Optional[Callable[[core.PyReachStatus],
                                              None]] = None,
                  finished_callback: Optional[Callable[[], None]] = None,
                  timeout: Optional[float] = None) -> core.PyReachStatus:
    """Run some commands on the device.

    Args:
      commands: The sequence of Command's to run.
      intent: The intent of the command.
      pick_id: The pick_id of the command.
      success_type: The success_type of the command.
      allow_uncalibrated: Allow motion when uncalibrated (unsafe, should only be
        set in calibration code).
      preemptive: True to preempt existing scripts.
      callback: An optional status callback function.
      finished_callback: An optional callback called when done.
      timeout: The maximum amount of time allowed to run the commands.

    Returns:
      Status of the command.
    """

    calib = self.calibration().get()
    tip_adjust_transform = None
    arm_origin = None
    if calib:
      tip_dev = None
      tip_transform = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
      tip_adjust_transform = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
      for dev in calib.get_all_devices():
        if (dev.device_type == "object" and dev.sub_type == "tip" and
            dev.tool_mount in {"robot", "ur"} and
            isinstance(dev, calibration.CalibrationObject)):
          tip_dev = cast(calibration.CalibrationObject, dev)
          if tip_dev.extrinsics:
            tip_transform = np.array(tip_dev.extrinsics, dtype=np.float64)

      if tip_dev:
        tip_adjust_transform = tip_transform
        for dev in calib.get_all_devices():
          if (dev.device_type == "object" and dev.sub_type == "tip" and
              dev.tool_mount == ("object-" + tip_dev.device_name) and
              isinstance(dev, calibration.CalibrationObject)):
            tip_adjust_dev = cast(calibration.CalibrationObject, dev)
            if tip_adjust_dev.extrinsics:
              tip_adjust_transform = transform_util.multiply_pose(
                  tip_adjust_transform,
                  np.array(tip_adjust_dev.extrinsics, dtype=np.float64))

      tip_transform = transform_util.inverse_pose(tip_transform)
      tip_adjust_transform = transform_util.inverse_pose(tip_adjust_transform)

    tag = utils.generate_tag()
    try:
      state = self.get_cached()
      if not state:
        raise core.PyReachError("State has not yet been loaded")

      with self._ik_lib_lock:
        script = commands.to_reach_script(
            self._device_name, tag, intent, pick_id, success_type,
            self._arm_type, self._support_vacuum, self._support_blowoff,
            allow_uncalibrated, preemptive, self._ik_lib, self._ik_hints, state,
            arm_origin, tip_adjust_transform)
    except core.PyReachError as e:
      status = core.PyReachStatus(
          utils.timestamp_now(),
          status="rejected",
          error="killed",
          message=str(e))
      if callback is not None:

        def run_error(callback: Callable[[core.PyReachStatus], None],
                      finished_callback: Optional[Callable[[], None]],
                      status: core.PyReachStatus) -> None:
          callback(status)
          if finished_callback:
            finished_callback()

        self.run(run_error, callback, finished_callback, status)
      return status
    q = self.send_tagged_request(script, timeout=timeout)
    if callback:

      def cb(msg: Tuple[types_gen.DeviceData, Optional[arm.ArmState]]) -> None:
        if msg[0].data_type == "cmd-status" and callback is not None:
          callback(utils.pyreach_status_from_message(msg[0]))

      def fcb() -> None:
        if finished_callback is not None:
          finished_callback()

      self.queue_to_callback(q, cb, fcb)
      return core.PyReachStatus(
          utils.timestamp_now(), status="rejected", error="timeout")

    for msg in thread_util.extract_all_from_queue(q):
      if msg[0].data_type == "cmd-status":
        status = utils.pyreach_status_from_message(msg[0])
        if status.is_last_status():
          return status
    return core.PyReachStatus(
        utils.timestamp_now(), status="rejected", error="timeout")

  def get_wrapper(
      self) -> Tuple[device_base.DeviceBase, device_base.DeviceBase, "ArmImpl"]:
    """Return the Device, Constraints Device, and Arm."""
    return self, self._constraints_device, ArmImpl(self)

  @classmethod
  def _arm_state_from_message(cls, arm_type: arm.ArmType,
                              msg: types_gen.DeviceData) -> "arm.ArmState":
    """Return the State from a device data message.

    Args:
      arm_type: The type of the arm.
      msg: The device data to decode.

    Returns:
      The Arm state.

    """
    joints = list(msg.joints)
    joints = joints[0:arm_type.joint_count]
    if len(joints) < arm_type.joint_count:
      logging.warning("joints too short: %s", msg)
      while len(joints) < arm_type.joint_count:
        joints.append(0.0)
    pose = list(msg.pose)
    if len(pose) != 6:
      logging.warning("poses is not correct length")
      pose = [0.0] * 6
    force = list(msg.force)
    if len(force) != 6:
      # warning("force is not the correct length: {msg.to_json()"})
      force = [0.0] * 6
    analog_input: Dict[str, List[float]] = {}
    analog_output: Dict[str, List[float]] = {}
    for analog_bank in msg.analog_bank:
      if analog_bank.output:
        analog_output[analog_bank.space] = list(analog_bank.state)
      else:
        analog_input[analog_bank.space] = list(analog_bank.state)
    digital_input: Dict[str, List[bool]] = {}
    digital_output: Dict[str, List[bool]] = {}
    for digital_bank in msg.digital_bank:
      if digital_bank.output:
        digital_output[digital_bank.space] = list(digital_bank.state)
      else:
        digital_input[digital_bank.space] = list(digital_bank.state)
    try:
      robot_mode = arm.RobotMode.from_string(msg.robot_mode)
    except ValueError:
      robot_mode = arm.RobotMode.DEFAULT
    return arm.ArmState(
        utils.time_at_timestamp(msg.ts), msg.seq,
        msg.device_type, msg.device_name, tuple(joints),
        core.Pose.from_list(pose), tuple(force), msg.is_protective_stopped,
        msg.is_emergency_stopped, msg.is_safeguard_stopped, msg.is_reduced_mode,
        msg.safety_message, msg.is_program_running, msg.is_robot_power_on,
        robot_mode)

  @property
  def arm_type(self) -> arm.ArmType:
    """Return the arm type of the arm."""
    return self._arm_type


class ArmImpl(arm.Arm):
  """Represents a multi-joint Arm."""

  _device: ArmDevice
  _enable_randomization: bool

  def __init__(self, device: ArmDevice) -> None:
    """Init the Arm."""
    self._device = device
    self._enable_randomization = True

  @property
  def arm_type(self) -> arm.ArmType:
    """Return the arm type of the arm."""
    return self._device.arm_type

  def reset_sim(self) -> None:
    """Send reset sim command."""
    self._device.reset_sim()

  @property
  def device_name(self) -> str:
    """Return the Arm name."""
    return self._device.device_name

  def state(self) -> Optional[arm.ArmState]:
    """Return the cached state."""
    return self._device.get_cached()

  @property
  def support_blowoff(self) -> bool:
    """Return true if blowoff is supported."""
    return self._device.support_blowoff()

  @property
  def support_vacuum(self) -> bool:
    """Return true if vacuum is supported."""
    return self._device.support_vacuum()

  def set_ik_lib(self, ik_lib: arm.IKLibType) -> None:
    """Set the IK library to be used."""
    self._device.set_ik_lib(ik_lib)

  def add_update_callback(
      self,
      callback: Callable[[arm.ArmState], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback for cached frames.

    Args:
      callback: Callback called when a frame arrives. If it returns True, the
        callback will be stopped.
      finished_callback: Optional callback, called when the callback is stopped
        or if the camera is closed.

    Returns:
      A function that when called stops the callback.

    """
    return self._device.add_update_callback(callback, finished_callback)

  def start_streaming(self, request_period: float = 0.1) -> None:
    """Start streaming of arm state.

    Args:
      request_period: The number of seconds between states. Defaults to .1
        second between states.
    """
    self._device.set_untagged_request_period("robot", self.device_name,
                                             request_period)

  def stop_streaming(self) -> None:
    """Stop streaming arm states."""
    self._device.set_untagged_request_period("robot", self.device_name, None)

  @property
  def joint_limits(self) -> Optional[Tuple[constraints.JointLimit, ...]]:
    """Return the Joint Limits."""
    c = self._device.constraints.get()
    if c is None:
      return None
    joint_limits: Optional[Tuple[constraints.JointLimit, ...]] = (
        c.get_joint_limits(self.device_name))
    if joint_limits:
      return tuple(joint_limits)
    return None

  def fetch_state(self, timeout: float = 15.0) -> Optional[arm.ArmState]:
    """Return the Arm State.

    Args:
      timeout: The number of seconds to wait before timing out.

    Returns:
      Returns the latest state (if available.)

    """
    q = self._device.request_untagged(
        "robot", self.device_name, "robot-state", timeout=timeout)
    msgs = thread_util.extract_all_from_queue(q)
    if not msgs:
      return None
    if len(msgs) != 1:
      logging.warning("expected only a message: %s", msgs)
    return msgs[0][1]

  def async_fetch_state(
      self,
      timeout: float = 15.0,
      callback: Optional[Callable[[arm.ArmState], None]] = None,
      error_callback: Optional[Callable[[core.PyReachStatus], None]] = None
  ) -> None:
    """Async fetch the Arm State.

    Args:
      timeout: The number of seconds to wait before timing out.
      callback: An optional callback function to call when the state arrives.
      error_callback: An optional callback called if there is an error.

    Returns:
      Returns the latest state (if available.)

    """
    q = self._device.request_untagged(
        "robot", self.device_name, "robot-state", timeout=timeout)
    self._device.queue_to_error_callback(q, callback, error_callback)

  def to_joints(self,
                joints: Union[Tuple[float, ...], List[float], np.ndarray],
                use_linear: bool = False,
                servo: bool = False,
                intent: str = "",
                pick_id: str = "",
                success_type: str = "",
                velocity: float = 0.0,
                acceleration: float = 0.0,
                allow_uncalibrated: bool = False,
                servo_time_seconds: float = 0.0,
                servo_lookahead_time_seconds: float = 0.0,
                servo_gain: float = 0.0,
                preemptive: bool = False,
                timeout: Optional[float] = None) -> core.PyReachStatus:
    """Set the arm joints synchronously.

    Args:
      joints: The list of joint angles in radians.
      use_linear: Whether to move in linear space. (Default: False)
      servo: Use servoing. (Default: False)
      intent: The intent of the command. (Default: no intent)
      pick_id: The pick_id of the command. (Default: No pick id)
      success_type: The success_type of the command. (Default; No success type)
      velocity: Max velocity.
      acceleration: Max acceleration.
      allow_uncalibrated: Allow motion when uncalibrated (unsafe, should only be
        set in calibration code).
      servo_time_seconds: Time to block the robot for (servo + UR only).
      servo_lookahead_time_seconds: Lookahead time for trajectory smoothing
        (servo + UR only).
      servo_gain: Gain for the servoing - if zero, defaults to 300 (servo + UR
        only).
      preemptive: True to preempt existing scripts.
      timeout: The amount time to wait before giving up. (Default: No timeout)

    Returns:
      Return the latest Arm status upon success; othewise None.

    """
    move_command: Union[_MoveLinear, _MoveJoints]
    if use_linear:
      move_command = _MoveLinear(
          list(joints),
          servo=servo,
          acceleration=acceleration,
          velocity=velocity)
    else:
      move_command = _MoveJoints(
          list(joints),
          servo=servo,
          acceleration=acceleration,
          velocity=velocity,
          servo_time_seconds=servo_time_seconds,
          servo_lookahead_time_seconds=servo_lookahead_time_seconds,
          servo_gain=servo_gain)

    return self._device.run_command(
        _Commands([move_command]),
        intent=intent,
        pick_id=pick_id,
        success_type=success_type,
        allow_uncalibrated=allow_uncalibrated,
        timeout=timeout,
        preemptive=preemptive,
        callback=None,
        finished_callback=None)

  def async_to_joints(
      self,
      joints: Union[List[float], np.ndarray],
      use_linear: bool = False,
      servo: bool = False,
      intent: str = "",
      pick_id: str = "",
      success_type: str = "",
      velocity: float = 0.0,
      acceleration: float = 0.0,
      allow_uncalibrated: bool = False,
      servo_time_seconds: float = 0.0,
      servo_lookahead_time_seconds: float = 0.0,
      servo_gain: float = 0.0,
      preemptive: bool = False,
      timeout: Optional[float] = None,
      callback: Optional[Callable[[core.PyReachStatus], None]] = None,
      finished_callback: Optional[Callable[[], None]] = None) -> None:
    """Set the Arm joint asynchronously.

    Args:
      joints: The joint angles in radians.
      use_linear: Whether to move in linear space. (Default: False)
      servo: Use servoing.
      intent: The intent of the command.
      pick_id: The pick_id of the command.
      success_type: The success_type of the command.
      velocity: Max velocity.
      acceleration: Max acceleration.
      allow_uncalibrated: Allow motion when uncalibrated (unsafe, should only be
        set in calibration code).
      servo_time_seconds: Time to block the robot for (servo + UR only).
      servo_lookahead_time_seconds: Lookahead time for trajectory smoothing
        (servo + UR only).
      servo_gain: Gain for the servoing - if zero, defaults to 300 (servo + UR
        only).
      preemptive: True to preempt existing scripts.
      timeout: The number of seconds to wait before timing out.
      callback: An optional callback routine call upon completion.
      finished_callback: An optional callback when done.
    """
    path: Optional[types_gen.ReachScriptCommand] = None

    if use_linear:
      path = types_gen.ReachScriptCommand(
          move_l_path=types_gen.MoveLPathArgs(waypoints=[
              types_gen.MoveLWaypointArgs(
                  rotation=list(joints),
                  velocity=velocity,
                  acceleration=acceleration,
                  servo=servo)
          ]))
    else:
      path = types_gen.ReachScriptCommand(
          move_j_path=types_gen.MoveJPathArgs(waypoints=[
              types_gen.MoveJWaypointArgs(
                  rotation=list(joints),
                  velocity=velocity,
                  acceleration=acceleration,
                  servo=servo,
                  servo_t_secs=servo_time_seconds,
                  servo_lookahead_time_secs=servo_lookahead_time_seconds,
                  servo_gain=servo_gain)
          ]))

    cmd = types_gen.CommandData(
        ts=utils.timestamp_now(),
        device_type="robot",
        device_name=self.device_name,
        data_type="reach-script",
        pick_id=pick_id,
        intent=intent,
        success_type=success_type,
        tag=utils.generate_tag(),
        reach_script=types_gen.ReachScript(
            preemptive=preemptive, version=0, commands=[path]))

    if allow_uncalibrated and cmd.reach_script:
      cmd.reach_script.calibration_requirement = types_gen.ReachScriptCalibrationRequirement(
          allow_uncalibrated=True)

    if callback is None and finished_callback is None:
      self._device.send_cmd(cmd)
      return

    def cb(msg: Tuple[types_gen.DeviceData, Optional[arm.ArmState]]) -> None:
      if msg[0].data_type == "cmd-status" and callback is not None:
        callback(utils.pyreach_status_from_message(msg[0]))

    def fcb() -> None:
      return

    if finished_callback is None:
      finished_callback = fcb
    q = self._device.send_tagged_request(cmd)
    self._device.queue_to_callback(q, cb, finished_callback)

  def to_pose(self,
              pose: core.Pose,
              use_linear: bool = False,
              servo: bool = False,
              intent: str = "",
              pick_id: str = "",
              success_type: str = "",
              velocity: float = 0.0,
              acceleration: float = 0.0,
              apply_tip_adjust_transform: bool = False,
              allow_uncalibrated: bool = False,
              servo_time_seconds: float = 0.0,
              servo_lookahead_time_seconds: float = 0.0,
              servo_gain: float = 0.0,
              preemptive: bool = False,
              timeout: Optional[float] = None) -> core.PyReachStatus:
    """Set the pose synchronously.

    Args:
       pose: The desired pose.
       use_linear: True if a linear translation is required.
       servo: Use servoing.
       intent: The intent of the command.
       pick_id: The pick_id of the command.
       success_type: The success_type of the command.
       velocity: Max velocity.
       acceleration: Max acceleration.
       apply_tip_adjust_transform: Apply the transform of the tip adjust.
       allow_uncalibrated: Allow motion when uncalibrated (unsafe, should only
         be set in calibration code).
       servo_time_seconds: Time to block the robot for (servo + UR only).
       servo_lookahead_time_seconds: Lookahead time for trajectory smoothing
         (servo + UR only).
       servo_gain: Gain for the servoing - if zero, defaults to 300 (servo + UR
         only).
       preemptive: True to preempt existing scripts.
       timeout: The amount of time to wait until giving up.

    Returns:
       Return the Status on success and None on timeout.

    """
    return self._device.run_command(
        _Commands([
            _MovePose(
                types_gen.Vec3d(*pose.position.as_list()),
                types_gen.Vec3d(*pose.orientation.axis_angle.as_list()),
                use_linear=use_linear,
                servo=servo,
                acceleration=acceleration,
                velocity=velocity,
                apply_tip_adjust_transform=apply_tip_adjust_transform,
                servo_time_seconds=servo_time_seconds,
                servo_lookahead_time_seconds=servo_lookahead_time_seconds,
                servo_gain=servo_gain)
        ]),
        intent=intent,
        pick_id=pick_id,
        success_type=success_type,
        allow_uncalibrated=allow_uncalibrated,
        preemptive=preemptive,
        timeout=timeout)

  def async_to_pose(
      self,
      pose: core.Pose,
      use_linear: bool = False,
      servo: bool = False,
      intent: str = "",
      pick_id: str = "",
      success_type: str = "",
      velocity: float = 0.0,
      acceleration: float = 0.0,
      apply_tip_adjust_transform: bool = False,
      allow_uncalibrated: bool = False,
      servo_time_seconds: float = 0.0,
      servo_lookahead_time_seconds: float = 0.0,
      servo_gain: float = 0.0,
      preemptive: bool = False,
      timeout: Optional[float] = None,
      callback: Optional[Callable[[core.PyReachStatus], None]] = None,
      finished_callback: Optional[Callable[[], None]] = None) -> None:
    """Asynchronously set the Arm pose.

    Args:
      pose: The desired X/Y/Z position and angle-axis rotation.
      use_linear: True if a linear translation is required.
      servo: Use servo mode.
      intent: The intent of the command.
      pick_id: The pick_id of the command.
      success_type: The success_type of the command.
      velocity: Max velocity.
      acceleration: Max acceleration.
      apply_tip_adjust_transform: Apply the transform of the tip adjust.
      allow_uncalibrated: Allow motion when uncalibrated (unsafe, should only be
        set in calibration code).
      servo_time_seconds: Time to block the robot for (servo + UR only).
      servo_lookahead_time_seconds: Lookahead time for trajectory smoothing
        (servo + UR only).
      servo_gain: Gain for the servoing - if zero, defaults to 300 (servo + UR
        only).
      preemptive: True to preempt existing scripts.
      timeout: The amount of time to wait until giving up.
      callback: Optional function to call when done (None for fail.)
      finished_callback: Optional finish function to call when done.

    Returns:
      Return the Status on success and None on timeout.
    """

    def cb(msg: core.PyReachStatus) -> None:  # pylint: disable=unused-argument
      return None

    if callback is None:
      callback = cb
    self._device.run_command(
        _Commands([
            _MovePose(
                types_gen.Vec3d(*pose.position.as_list()),
                types_gen.Vec3d(*pose.orientation.axis_angle.as_list()),
                use_linear=use_linear,
                servo=servo,
                acceleration=acceleration,
                velocity=velocity,
                apply_tip_adjust_transform=apply_tip_adjust_transform,
                servo_time_seconds=servo_time_seconds,
                servo_lookahead_time_seconds=servo_lookahead_time_seconds,
                servo_gain=servo_gain)
        ]),
        intent=intent,
        pick_id=pick_id,
        success_type=success_type,
        allow_uncalibrated=allow_uncalibrated,
        preemptive=preemptive,
        timeout=timeout,
        callback=callback,
        finished_callback=finished_callback)

  def set_vacuum_state(
      self,
      vacuum_state: ActionVacuumState,
      intent: str = "",
      pick_id: str = "",
      success_type: str = "",
      timeout: Optional[float] = None,
  ) -> Optional[core.PyReachStatus]:
    """Set the vacuum state synchronously.

    Args:
      vacuum_state: The desired vacuum state.
      intent: The intent of the command.
      pick_id: The pick_id of the command.
      success_type: The success_type of the command.
      timeout: The time in seconds to wait until failing.

    Returns:
      The Arm status on success and None otherwise.
    """
    return self._device.run_command(
        _Commands([_SetVacuumState(vacuum_state)]),
        intent=intent,
        pick_id=pick_id,
        success_type=success_type,
        timeout=timeout)

  def async_set_vacuum_state(
      self,
      vacuum_state: ActionVacuumState,
      intent: str = "",
      pick_id: str = "",
      success_type: str = "",
      timeout: Optional[float] = None,
      callback: Optional[Callable[[core.PyReachStatus], None]] = None,
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> core.PyReachStatus:
    """Asynchronously set the Vacuum State.

    Args:
      vacuum_state: The VacuumState to set.
      intent: The intent string (or empty) for the request.
      pick_id: The pick id (or empty) for the request.
      success_type: The success type to return on success.
      timeout: An optional timeout measured in seconds.
      callback: A callback function to invoke when the vacuum state arrives.
      finished_callback: A callback function to call when done.

    Returns:
      Status of the command.
    """

    def cb(msg: core.PyReachStatus) -> None:  # pylint: disable=unused-argument
      return None

    if callback is None:
      callback = cb
    return self._device.run_command(
        _Commands([_SetVacuumState(vacuum_state)]),
        intent=intent,
        pick_id=pick_id,
        success_type=success_type,
        timeout=timeout,
        callback=callback,
        finished_callback=finished_callback)

  def _action_to_commands(self, action: actions_impl.Action,
                          inputs: List[arm.ActionInput],
                          use_unity_ik: bool) -> _Commands:
    global_acceleration = action.get_softstart_accel() if action.get_softstart(
    ) else action.get_max_accel()
    global_velocity = action.get_softstart_velocity() if action.get_softstart(
    ) else action.get_max_velocity()
    steps = action.get_steps().copy()
    if action.get_cyclic() and steps:
      steps.append(steps[0])

    calib = self._device.calibration().get()
    if calib is None:
      raise core.PyReachError("Calibration has not loaded yet.")
    arm_calibration_dev = calib.get_device("robot", self.device_name)
    if arm_calibration_dev is None:
      arm_calibration_dev = calib.get_device("ur", self.device_name)
    if arm_calibration_dev is None:
      raise core.PyReachError("Arm calibration was missing.")
    if not isinstance(arm_calibration_dev, calibration.CalibrationRobot):
      raise core.PyReachError("Arm calibration data was not Robot.")
    arm_calibration = cast(calibration.CalibrationRobot, arm_calibration_dev)
    arm_transform = np.array(arm_calibration.extrinsics, dtype=np.float64)

    step_pose: Dict[int, Tuple[types_gen.Vec3d, types_gen.Quaternion3d]] = {}
    commands: List[_Command] = []
    while len(step_pose) < len(steps):
      start_len = len(step_pose)
      for idx, step in enumerate(steps):
        if idx in step_pose:
          continue

        velocity = global_velocity if step.get_velocity(
        ) == 0 else step.get_velocity()
        accel = global_acceleration if step.get_acceleration(
        ) == 0 else step.get_acceleration()
        offset = np.zeros(6)

        # Calculate randomized offset as done by the ReachUI
        if step.get_randomized_offset() and self._enable_randomization:
          data = [
              x * 0.01 for x in transform_util.random_xy_offset_within_radius(
                  step.get_randomized_offset_radius_cm())
          ]
          offset = np.array(data, dtype=np.float64)

        step_pos = step.get_pos()
        step_rot = step.get_rot()
        np_pos = np.array([step_pos.x, step_pos.y, step_pos.z],
                          dtype=np.float64)
        np_rot = np.array([step_rot.x, step_rot.y, step_rot.z, step_rot.w],
                          dtype=np.float64)

        if step.get_parent_type() == actions_impl.ActionStepParentType.ABSOLUTE:
          target_tip_transform = transform_util.unity_pos_quaternion_to_pose(
              np_pos, np_rot)
          target_tip_transform = transform_util.multiply_pose(
              target_tip_transform, offset)

          if step.get_parent_step_idx() in step_pose:
            step_pose[idx] = step_pose[step.get_parent_step_idx()]
          else:
            step_pose[idx] = (types_gen.Vec3d(), types_gen.Quaternion3d())
        elif step.get_parent_type(
        ) == actions_impl.ActionStepParentType.TIP_INPUT:
          if step.get_tip_input_idx() >= len(inputs):
            raise core.PyReachError("Not enough inputs")

          input_data = inputs[step.get_tip_input_idx()]
          # Singulation
          if input_data.prediction_point:
            input_pose_normal = input_data.prediction_point
            np_pos = np_pos / 100
            target_tip_transform = transform_util.pos_quaternion_to_pose(
                np_pos, np_rot)
            target_tip_transform = transform_util.multiply_pose(
                input_pose_normal[0], target_tip_transform)
            target_tip_transform = transform_util.multiply_pose(
                target_tip_transform, offset)
            normal = transform_util.get_z_direction(target_tip_transform)

            if np.dot(normal, input_pose_normal[2]) > 0:
              flipz_trans = np.array([0.0, 0.0, 0.0])
              flipz_rot = np.array([-3.14159, 0.0, 0.0])
              flipz_t = transform_util.matrix_to_pose(
                  transform_util.convert_to_matrix(flipz_trans, flipz_rot))
              target_tip_transform = transform_util.multiply_pose(
                  target_tip_transform, flipz_t)
              target_tip_transform = transform_util.angular_mod_pose(
                  target_tip_transform)
          # Kitting
          elif input_data.position and input_data.rotation:
            np_pos = np_pos / 100
            target_tip_transform = transform_util.pos_quaternion_to_pose(
                np_pos, np_rot)
            position_list = [
                input_data.position.x, input_data.position.y,
                input_data.position.z
            ]
            rotation_list = [
                input_data.rotation.x, input_data.rotation.y,
                input_data.rotation.z, input_data.rotation.w
            ]
            input_transform = transform_util.pos_quaternion_to_pose(
                position_list, rotation_list)
            target_tip_transform = transform_util.multiply_pose(
                input_transform, target_tip_transform)

          if step.get_parent_step_idx() in step_pose:
            step_pose[idx] = step_pose[step.get_parent_step_idx()]
          else:
            step_pose[idx] = (types_gen.Vec3d(), types_gen.Quaternion3d())
        elif step.get_parent_type(
        ) == actions_impl.ActionStepParentType.OTHER_STEP:
          if step.get_parent_step_idx() in step_pose:
            step_pose[idx] = step_pose[step.get_parent_step_idx()]
            continue
        else:
          step_pose[idx] = (types_gen.Vec3d(), types_gen.Quaternion3d())
          continue

        arm_origin_transform = transform_util.inverse_pose(arm_transform)
        arm_tool_transform = transform_util.multiply_pose(
            arm_origin_transform, target_tip_transform)

        use_linear = False
        if step.get_use_process_mode():
          use_linear = True
        commands.append(
            _MovePose(
                translation=types_gen.Vec3d(arm_tool_transform[0],
                                            arm_tool_transform[1],
                                            arm_tool_transform[2]),
                rotation=types_gen.Vec3d(arm_tool_transform[3],
                                         arm_tool_transform[4],
                                         arm_tool_transform[5]),
                velocity=velocity,
                acceleration=accel,
                use_linear=use_linear,
                use_unity_ik=use_unity_ik,
                apply_tip_adjust_transform=True))

        if step.get_set_capability():
          if step.get_set_capability_io_type() == "DigitalOutput":
            if step.get_set_capability_type(
            ) == "vacuum" or step.get_set_capability_type() == "blowoff":
              commands.append(
                  _SetVacuumState(
                      ActionVacuumState(step.get_set_capability_value())))

      if len(step_pose) == start_len:
        raise core.PyReachError("Action invalid: contains infinite loop")
    return _Commands(commands)

  def _execute_action(
      self,
      action_name: str,
      inputs: List[arm.ActionInput],
      intent: str = "",
      pick_id: str = "",
      success_type: str = "",
      use_unity_ik: bool = False,
      allow_uncalibrated: bool = False,
      preemptive: bool = False,
      timeout: Optional[float] = None,
      callback: Optional[Callable[[core.PyReachStatus], None]] = None,
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> core.PyReachStatus:
    """Asynchronously execute an action.

    Args:
      action_name: Name of the action to execute.
      inputs: Inputs to the action template.
      intent: The intent string (or empty) for the request.
      pick_id: The pick id (or empty) for the request.
      success_type: The success type to return on success.
      use_unity_ik: True only for tasks that use Oracle and actionsets.
      allow_uncalibrated: Allow motion when uncalibrated (unsafe, should only be
        set in calibration code).
      preemptive: True to preempt existing scripts.
      timeout: An optional timeout measured in seconds.
      callback: A callback function to invoke when the vacuum state arrives.
      finished_callback: A callback function to call when done.

    Returns:
      Execution status.
    """
    action_device = self._device.actions()
    if not action_device:
      logging.warning("No actions set for the workcell. Ignoring.")
      return core.PyReachStatus(
          utils.timestamp_now(), status="rejected", error="Invalid")

    action_list = action_device.get_actions()
    if not action_list:
      logging.warning("No action list in action sets. Ignoring.")
      return core.PyReachStatus(
          utils.timestamp_now(), status="rejected", error="Invalid")

    selected_action = action_list.get_action(action_name)
    if not selected_action:
      logging.warning("Action selected is not supported. Ignoring.")
      return core.PyReachStatus(
          utils.timestamp_now(), status="rejected", error="Invalid")

    return self._device.run_command(
        self._action_to_commands(selected_action, inputs, use_unity_ik),
        intent=intent,
        pick_id=pick_id,
        success_type=success_type,
        allow_uncalibrated=allow_uncalibrated,
        preemptive=preemptive,
        timeout=timeout,
        callback=callback,
        finished_callback=finished_callback)

  def async_execute_action(
      self,
      action_name: str,
      inputs: List[arm.ActionInput],
      intent: str = "",
      pick_id: str = "",
      success_type: str = "",
      use_unity_ik: bool = False,
      allow_uncalibrated: bool = False,
      preemptive: bool = False,
      timeout: Optional[float] = None,
      callback: Optional[Callable[[core.PyReachStatus], None]] = None,
      finished_callback: Optional[Callable[[], None]] = None) -> None:
    """Asynchronously execute an action.

    Args:
      action_name: Name of the action to execute.
      inputs: Inputs to the action template.
      intent: The intent string (or empty) for the request.
      pick_id: The pick id (or empty) for the request.
      success_type: The success type to return on success.
      use_unity_ik: True only for tasks that use Oracle and actionsets.
      allow_uncalibrated: Allow motion when uncalibrated (unsafe, should only be
        set in calibration code).
      preemptive: True to preempt existing scripts.
      timeout: An optional timeout measured in seconds.
      callback: A callback function to invoke when the vacuum state arrives.
      finished_callback: A callback function to call when done.
    """

    def cb(msg: core.PyReachStatus) -> None:  # pylint: disable=unused-argument
      return None

    if callback is None:
      callback = cb

    self._execute_action(
        action_name,
        inputs,
        intent=intent,
        pick_id=pick_id,
        success_type=success_type,
        use_unity_ik=use_unity_ik,
        allow_uncalibrated=allow_uncalibrated,
        preemptive=preemptive,
        timeout=timeout,
        callback=callback,
        finished_callback=finished_callback)

  def execute_action(self,
                     action_name: str,
                     inputs: List[arm.ActionInput],
                     intent: str = "",
                     pick_id: str = "",
                     success_type: str = "",
                     use_unity_ik: bool = False,
                     allow_uncalibrated: bool = False,
                     preemptive: bool = False,
                     timeout: Optional[float] = None) -> core.PyReachStatus:
    """Execute an action synchronously.

    Args:
      action_name: Name of the action to execute.
      inputs: Inputs to the action template.
      intent: The intent string (or empty) for the request.
      pick_id: The pick id (or empty) for the request.
      success_type: The success type to return on success.
      use_unity_ik: True only for tasks that use Oracle and actionsets.
      allow_uncalibrated: Allow motion when uncalibrated (unsafe, should only be
        set in calibration code).
      preemptive: True to preempt existing scripts.
      timeout: An optional timeout measured in seconds.

    Returns:
      Success or failure status of the command.
    """
    if not inputs:
      logging.warning("No inputs provided. Ignoring.")
      return core.PyReachStatus(
          utils.timestamp_now(), status="rejected", error="Timeout")

    return self._execute_action(
        action_name,
        inputs,
        intent=intent,
        pick_id=pick_id,
        success_type=success_type,
        use_unity_ik=use_unity_ik,
        allow_uncalibrated=allow_uncalibrated,
        preemptive=preemptive,
        timeout=timeout)

  def stop(self,
           deceleration: float = 2.0,
           intent: str = "",
           pick_id: str = "",
           success_type: str = "",
           allow_uncalibrated: bool = False,
           preemptive: bool = False,
           timeout: Optional[float] = None) -> core.PyReachStatus:
    """Stop the robot arm synchronously.

    Args:
      deceleration: The rate of deceleration in radians/second/second.
      intent: The intent of the command. (Default: no intent)
      pick_id: The pick_id of the command. (Default: no pick id)
      success_type: The success_type of the command. (Default: no success type)
      allow_uncalibrated: Allow motion when uncalibrated (unsafe, should only be
        set in calibration code).
      preemptive: True to preempt existing scripts.
      timeout: An optional timeout measured in seconds.

    Returns:
      Status of the request.

    """
    return self._device.run_command(
        _Commands([_Stop(deceleration=deceleration)]),
        intent=intent,
        pick_id=pick_id,
        success_type=success_type,
        allow_uncalibrated=allow_uncalibrated,
        preemptive=preemptive,
        timeout=timeout)

  def async_stop(
      self,
      deceleration: float = 2.0,
      intent: str = "",
      pick_id: str = "",
      success_type: str = "",
      allow_uncalibrated: bool = False,
      preemptive: bool = False,
      timeout: Optional[float] = None,
      callback: Optional[Callable[[core.PyReachStatus], None]] = None,
      finished_callback: Optional[Callable[[], None]] = None) -> None:
    """Stop the robot arm synchronously.

    Args:
      deceleration: The rate of deceleration in radians/second/second.
      intent: The intent of the command. (Default: no intent)
      pick_id: The pick_id of the command. (Default: no pick id)
      success_type: The success_type of the command. (Default: no success type)
      allow_uncalibrated: Allow motion when uncalibrated (unsafe, should only be
        set in calibration code).
      preemptive: True to preempt existing scripts.
      timeout: An optional timeout measured in seconds.
      callback: An optional callback routine call upon completion.
      finished_callback: An optional callback when done.
    """

    def cb(msg: core.PyReachStatus) -> None:  # pylint: disable=unused-argument
      return None

    if callback is None:
      callback = cb

    self._device.run_command(
        _Commands([_Stop(deceleration=deceleration)]),
        intent=intent,
        pick_id=pick_id,
        success_type=success_type,
        allow_uncalibrated=allow_uncalibrated,
        preemptive=preemptive,
        timeout=timeout,
        callback=callback,
        finished_callback=finished_callback)

  def fk(self,
         joints: Union[Tuple[float, ...], List[float], np.ndarray],
         apply_tip_adjust_transform: bool = False) -> Optional[core.Pose]:
    """Uses forward kinematics to get the pose from the joint angles.

    Args:
      joints: The robot joints.
      apply_tip_adjust_transform: If True, will use the data in the calibration
        file for the robot to change the returned pose from the end of the arm
        to the tip of the end-effector.

    Returns:
      The pose for the end of the arm, or if apply_tip_adjust_transform was
      set to True, the pose for the tip of the end-effector. If the IK library
      was not yet initialized, this will return None.
    """

    return self._device.fk(joints, apply_tip_adjust_transform)
