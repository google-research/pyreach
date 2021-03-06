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
import logging  # type: ignore
import math
import threading
from typing import Callable, Dict, List, Optional, Tuple, Union

import numpy as np

from pyreach.common.proto_gen import workcell_io_pb2 as workcell_io
from pyreach import arm
from pyreach import constraints
from pyreach import core
from pyreach import digital_output
from pyreach import internal
from pyreach.common.base import transform_util
from pyreach.common.python import types_gen
from pyreach.impl import actions_impl
from pyreach.impl import constraints_impl
from pyreach.impl import device_base
from pyreach.impl import digital_output_impl
from pyreach.impl import requester
from pyreach.impl import thread_util
from pyreach.impl import utils


class IKLib:
  """Internal class for an IK library."""

  def fk(self, joints: List[float]) -> Optional[List[float]]:
    """Convert joint angles to a pose.

    Args:
      joints: the joint angles.

    Returns:
      the pose.
    """
    raise NotImplementedError

  def ik_search(self, pose: List[float], current_joints: List[float],
                ik_hints: Dict[int, List[float]],
                use_unity_ik: bool) -> Optional[List[float]]:
    """Perform IK search and return a single joint pose.

    Args:
      pose: The pose.
      current_joints: the current joint state.
      ik_hints: The ik hints for the search.
      use_unity_ik: If true, use Unity IK.

    Returns:
      The joint position.
    """
    raise NotImplementedError

  def require_ikhints(self) -> bool:
    """Return if IKHints are required for this IK library."""
    raise NotImplementedError


class IKLibIKFast(IKLib):
  """Internal class for an IK library."""

  def __init__(self, urdf_file: str) -> None:
    """Init the IK lib."""
    from pyreach.ikfast import ikfast
    self._ik: ikfast.IKFast = ikfast.IKFast(urdf_file)

  def fk(self, joints: List[float]) -> Optional[List[float]]:
    """Convert joint angles to a pose.

    Args:
      joints: the joint angles.

    Returns:
      the pose.
    """
    pose = self._ik.fk(joints)
    if pose is not None:
      return pose.tolist()
    return None

  def ik_search(self, pose: List[float], current_joints: List[float],
                ik_hints: Dict[int, List[float]],
                use_unity_ik: bool) -> Optional[List[float]]:
    """Perform IK search and return a single joint pose.

    Args:
      pose: The pose.
      current_joints: the current joint state.
      ik_hints: The ik hints for the search.
      use_unity_ik: If true, use Unity IK.

    Returns:
      The joint position.
    """
    if use_unity_ik:
      joints = self._ik.unity_ik_solve_search(pose, current_joints, ik_hints)
      if joints is not None:
        return joints.tolist()
      return None
    joints = self._ik.ik_search(pose, ik_hints)
    if joints is not None:
      return joints.tolist()
    return None

  def require_ikhints(self) -> bool:
    """Return if IKHints are required for this IK library."""
    return True


class IKLibPyBullet(IKLib):
  """Internal class for an IK library."""

  def __init__(self) -> None:
    """Init the IK lib."""
    from pyreach.ik_pybullet import ik_pybullet
    self._ik: ik_pybullet.IKPybullet = ik_pybullet.IKPybullet()

  def fk(self, joints: List[float]) -> Optional[List[float]]:
    """Convert joint angles to a pose.

    Args:
      joints: the joint angles.

    Returns:
      the pose.
    """
    pose = self._ik.fk(np.array(joints, dtype=np.float64))
    if pose:
      return pose.tolist()
    return None

  def ik_search(self, pose: List[float], current_joints: List[float],
                ik_hints: Dict[int, List[float]],
                use_unity_ik: bool) -> Optional[List[float]]:
    """Perform IK search and return a single joint pose.

    Args:
      pose: The pose.
      current_joints: the current joint state.
      ik_hints: The ik hints for the search.
      use_unity_ik: If true, use Unity IK.

    Returns:
      The joint position.
    """
    joints = self._ik.ik_search(
        np.array(pose, dtype=np.float64),
        np.array(current_joints, dtype=np.float64))
    return joints.tolist()

  def require_ikhints(self) -> bool:
    """Return if IKHints are required for this IK library."""
    return False


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
        "ur3e.urdf", "ur5.urdf", "ur5e.urdf", "ur10e.urdf", "lrmate200ic.urdf",
        "lrmate200id.urdf", "FanucCR7ia.urdf", "FanucLrmate200id7l.urdf",
        "FanucR2000ia165f.urdf", "XArm6.urdf"
    }:
      return ArmTypeImpl(urdf_file, 6)
    if urdf_file == "april-led.urdf":
      return ArmTypeImpl(urdf_file, 0)
    raise ValueError("invalid URDF file: " + urdf_file)


class _Command:
  """Represents a Arm command.

  This is a base class from which all other Arm commands are
  sub-classed.  This this class basically just defines virtual methods
  that get implemented as needed by the sub-class.  It is used to
  convert Arm Commands to lower level Reach Script commands.
  """

  def __init__(self, controller_name: str) -> None:
    """Init Arm Command base instance.

    Args:
      controller_name: the name of the controller.
    """
    self._controller_name = controller_name

  @property
  def controller_name(self) -> str:
    return self._controller_name

  def to_reach_script(
      self,
      arm_type: arm.ArmType,
      support_vacuum: bool,
      support_blowoff: bool,
      ik_lib: Optional[IKLib],
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
               controller_name: str,
               joints: List[float],
               velocity: float = 0.0,
               acceleration: float = 0.0,
               servo: bool = False,
               servo_time_seconds: float = 0.0,
               servo_lookahead_time_seconds: float = 0.0,
               servo_gain: float = 0.0,
               blend_radius: float = 0.0) -> None:
    """Construct a move joints command.

    Args:
      controller_name: the name of the controller.
      joints: Desired joint angles.
      velocity: Max velocity.
      acceleration: Max acceleration.
      servo: Use servo mode.
      servo_time_seconds: Time to block the robot for (servo + UR only).
      servo_lookahead_time_seconds: Lookahead time for trajectory smoothing
        (servo + UR only).
      servo_gain: Gain for the servoing - if zero, defaults to 300 (servo + UR
        only).
      blend_radius: The blend radius.
    """
    super().__init__(controller_name)
    self._joints = joints
    self._velocity = velocity
    self._acceleration = acceleration
    self._servo = servo
    self._servo_time_seconds = servo_time_seconds
    self._servo_lookahead_time_seconds = servo_lookahead_time_seconds
    self._servo_gain = servo_gain
    self._blend_radius = blend_radius

  def to_reach_script(
      self,
      arm_type: arm.ArmType,
      support_vacuum: bool,
      support_blowoff: bool,
      ik_lib: Optional[IKLib],
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
            controller_name=self.controller_name,
            move_j_path=types_gen.MoveJPathArgs(waypoints=[
                types_gen.MoveJWaypointArgs(
                    rotation=self._joints,
                    velocity=self._velocity,
                    acceleration=self._acceleration,
                    servo=self._servo,
                    servo_t_secs=self._servo_time_seconds,
                    servo_lookahead_time_secs=self
                    ._servo_lookahead_time_seconds,
                    servo_gain=self._servo_gain,
                    blend_radius=self._blend_radius)
            ]))
    ]


class _MoveLinear(_Command):
  """An Command to move 'linearly' to specified joint angles."""

  _joints: List[float]
  _velocity: float
  _acceleration: float
  _servo: bool
  _blend_radius: float

  def __init__(self,
               controller_name: str,
               joints: List[float],
               velocity: float = 0.0,
               acceleration: float = 0.0,
               servo: bool = False,
               blend_radius: float = 0.0) -> None:
    """Construct the Arm Move Linear command with its desired joints.

    Args:
      controller_name: the name of the controller.
      joints: Desired joints.
      velocity: Max velocity.
      acceleration: Max acceleration.
      servo: Use servo mode.
      blend_radius: The blend radius.
    """
    super().__init__(controller_name)
    self._joints = joints
    self._velocity = velocity
    self._acceleration = acceleration
    self._servo = servo
    self._blend_radius = blend_radius

  def to_reach_script(
      self,
      arm_type: arm.ArmType,
      support_vacuum: bool,
      support_blowoff: bool,
      ik_lib: Optional[IKLib],
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
            controller_name=self.controller_name,
            move_l_path=types_gen.MoveLPathArgs(waypoints=[
                types_gen.MoveLWaypointArgs(
                    rotation=self._joints,
                    velocity=self._velocity,
                    acceleration=self._acceleration,
                    servo=self._servo,
                    blend_radius=self._blend_radius)
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
  _blend_radius: float
  _pose_in_world_coordinates: bool

  def __init__(self,
               controller_name: str,
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
               servo_gain: float = 0.0,
               blend_radius: float = 0.0,
               pose_in_world_coordinates: bool = False) -> None:
    """Construct the MovePose object.

    Args:
      controller_name: the name of the controller.
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
      blend_radius: The blend radius.
      pose_in_world_coordinates: If true, pose is in world coordinates,
        otherwise if false, pose is in arm base coordinates.
    """
    super().__init__(controller_name)
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
    self._blend_radius = blend_radius
    self._pose_in_world_coordinates = pose_in_world_coordinates

  def to_reach_script(
      self, arm_type: arm.ArmType, support_vacuum: bool, support_blowoff: bool,
      ik_lib: Optional[IKLib], ik_hints: Dict[int, List[float]],
      state: arm.ArmState, arm_origin: Optional[np.ndarray],
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
    if self._pose_in_world_coordinates:
      if arm_origin is None:
        raise core.PyReachError("arm origin was not loaded")
      pose = transform_util.multiply_pose(
          transform_util.inverse_pose(arm_origin), pose)
    if self._apply_tip_adjust_transform:
      if tip_adjust_transform is not None:
        if self._use_unity_ik:

          # Inverse of  Euler 90, -180, 0 in YXZ:
          # rotation to fix tip adjust in the case of Unity.
          quaternion_const = transform_util.inverse_quat(
              np.array([0.0, math.sqrt(2) / 2.0, -math.sqrt(2) / 2.0, 0.0]))

          # Convert tip adjust transform in Unity space.
          tip_adjust_unity = transform_util.unity_pos_quaternion_to_pose(
              tip_adjust_transform[:3],
              transform_util.axis_angle_to_quaternion(
                  tip_adjust_transform[3:]).tolist())
          tip_adjust_unity_translation = tip_adjust_unity[:3]
          tip_adjust_unity_rotation = tip_adjust_unity[3:]
          tip_adjust_unity_rotation_quat = transform_util.axis_angle_to_quaternion(
              tip_adjust_unity_rotation)

          # Apply the rotation adjustment.
          tip_adjust_unity_rotation = transform_util.quaternion_multiply(
              tip_adjust_unity_rotation_quat, quaternion_const)

          # Convert back to pose form in Unity space.
          tip_adjust_pose_unity = transform_util.pos_quaternion_to_pose(
              tip_adjust_unity_translation.tolist(),
              tip_adjust_unity_rotation.tolist())

          # Calculate the inverse matrix in Unity space.
          tip_adjust_pose_unity_matrix = np.linalg.inv(
              transform_util.pose_to_matrix(tip_adjust_pose_unity))

          # Calculate the pose in Unity space.
          pose_unity = transform_util.multiply_pose(
              pose, transform_util.matrix_to_pose(tip_adjust_pose_unity_matrix))

          # Convert back to pose in robot space before sending to IK solver.
          pose = transform_util.unity_pos_quaternion_to_pose(
              pose_unity[:3].tolist(),
              transform_util.axis_angle_to_quaternion(pose_unity[3:]).tolist())
        else:
          tip_adjust_transform = transform_util.inverse_pose(
              tip_adjust_transform)
          pose = transform_util.multiply_pose(pose, tip_adjust_transform)
      else:
        raise core.PyReachError("tip adjust transform was not loaded")
    if ik_lib is not None:
      if ik_lib.require_ikhints() and not ik_hints:
        raise core.PyReachError("IKhints have not been loaded")

      joints = ik_lib.ik_search(pose.tolist(), list(state.joint_angles),
                                ik_hints, self._use_unity_ik)
      if joints is None:
        raise core.PyReachError("IK failed to find solution")
      if self._use_linear:
        return _MoveLinear(self.controller_name, joints, self._velocity,
                           self._acceleration, self._servo,
                           self._blend_radius).to_reach_script(
                               arm_type, support_vacuum, support_blowoff,
                               ik_lib, ik_hints, state, arm_origin,
                               tip_adjust_transform)
      else:
        return _MoveJoints(
            self.controller_name,
            joints,
            self._velocity,
            self._acceleration,
            self._servo,
            servo_time_seconds=self._servo_time_seconds,
            servo_lookahead_time_seconds=self._servo_lookahead_time_seconds,
            servo_gain=self._servo_gain,
            blend_radius=self._blend_radius).to_reach_script(
                arm_type, support_vacuum, support_blowoff, ik_lib, ik_hints,
                state, arm_origin, tip_adjust_transform)
    else:
      return [
          types_gen.ReachScriptCommand(
              controller_name=self.controller_name,
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

  def __init__(self, controller_name: str, state: ActionVacuumState) -> None:
    """Init the vacuum state for an Arm Command.

    Args:
      controller_name: the name of the controller.
      state: the vacuum state.
    """
    super().__init__(controller_name)
    self._state = state

  # pylint: disable=unused-argument
  def to_reach_script(
      self,
      arm_type: arm.ArmType,
      support_vacuum: bool,
      support_blowoff: bool,
      ik_lib: Optional[IKLib],
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
            controller_name=self.controller_name,
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
              controller_name=self.controller_name,
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

  def __init__(self, controller_name: str, output: int, value: bool) -> None:
    """Init the output state for an Arm Command.

    Args:
      controller_name: the name of the controller.
      output: the output number to set.
      value: the value to set.
    """
    super().__init__(controller_name)
    self._output = output
    self._value = value

  # pylint: disable=unused-argument
  def to_reach_script(
      self,
      arm_type: arm.ArmType,
      support_vacuum: bool,
      support_blowoff: bool,
      ik_lib: Optional[IKLib],
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
            controller_name=self.controller_name,
            set_digital_out=types_gen.SetDigitalOutArgs(
                output=self._output, value=self._value))
    ]


class _SetToolDigitalOut(_Command):
  """An Arm Command to set tool digital out."""

  _output: int
  _value: bool

  def __init__(self, controller_name: str, output: int, value: bool) -> None:
    """Init the tool output state for an Arm Command.

    Args:
      controller_name: the name of the controller.
      output: the output number to set.
      value: the value to set.
    """
    super().__init__(controller_name)
    self._output = output
    self._value = value

  # pylint: disable=unused-argument
  def to_reach_script(
      self,
      arm_type: arm.ArmType,
      support_vacuum: bool,
      support_blowoff: bool,
      ik_lib: Optional[IKLib],
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
            controller_name=self.controller_name,
            set_tool_digital_out=types_gen.SetDigitalOutArgs(
                output=self._output, value=self._value))
    ]


class _SetAnalogOut(_Command):
  """An Arm Command to set analog out."""

  _output: int
  _value: float

  def __init__(self, controller_name: str, output: int, value: float) -> None:
    """Init the tool output state for an Arm Command.

    Args:
      controller_name: the name of the controller.
      output: the output number to set.
      value: the value to set.
    """
    super().__init__(controller_name)
    self._output = output
    self._value = value

  # pylint: disable=unused-argument
  def to_reach_script(
      self,
      arm_type: arm.ArmType,
      support_vacuum: bool,
      support_blowoff: bool,
      ik_lib: Optional[IKLib],
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
            controller_name=self.controller_name,
            set_analog_out=types_gen.SetAnalogOutArgs(
                output=self._output, value=self._value))
    ]


class _SetOutput(_Command):
  """An Arm Command to set output."""

  _type: str
  _name: str
  _int_states: List[Tuple[str, int]]
  _float_states: List[Tuple[str, float]]

  def __init__(self, controller_name: str, typ: str, name: str,
               int_states: List[Tuple[str, int]],
               float_states: List[Tuple[str, float]]) -> None:
    """Init the out state for an Arm Command.

    Args:
      controller_name: the name of the controller.
      typ: The type of the output.
      name: The name of the output.
      int_states: The initial integer states as a list of name/value pairs.
      float_states: The initial float states as a list of name/value pairs.
    """
    super().__init__(controller_name)
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
      ik_lib: Optional[IKLib],
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
            controller_name=self.controller_name,
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


class _AcquireImage(_Command):
  """An Arm Command to acquire image."""

  _type: str
  _name: str
  _mode: int
  _tag: str

  def __init__(self, controller_name: str, typ: str, name: str, mode: int,
               tag: str):
    """Init the acquire image for an Arm Command.

    Args:
      controller_name: the name of the controller.
      typ: The type of the camera to acquire image.
      name: The name of the camera to acquire image.
      mode: Whether to acquire image in blocking mode or not.
      tag: The tag for the acquire image command.
    """
    super().__init__(controller_name)
    self._type = typ
    self._name = name
    self._mode = mode
    self._tag = tag

  # pylint: disable=unused-argument
  def to_reach_script(
      self,
      arm_type: arm.ArmType,
      support_vacuum: bool,
      support_blowoff: bool,
      ik_lib: Optional[IKLib],
      ik_hints: Dict[int, List[float]],
      state: arm.ArmState,
      arm_origin: Optional[np.ndarray],
      tip_adjust_transform: Optional[np.ndarray],
  ) -> List[types_gen.ReachScriptCommand]:
    """Convert a Acquire Image into some ReachScript commands.

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
            acquire_image=types_gen.AcquireImageArgs(
                device_type=self._type,
                device_name=self._name,
                mode=self._mode,
                tag=self._tag))
    ]


class _Stop(_Command):
  """An Stop Command stops the arm."""

  _deceleration: float

  def __init__(self, controller_name: str, deceleration: float = 2.0) -> None:
    """Init Stop Arm Command.

    Args:
      controller_name: the name of the controller.
      deceleration: The deceleration rate in radians/second/second.
    """
    super().__init__(controller_name)
    self._deceleration = deceleration

  # pylint: disable=unused-argument
  def to_reach_script(
      self,
      arm_type: arm.ArmType,
      support_vacuum: bool,
      support_blowoff: bool,
      ik_lib: Optional[IKLib],
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
            controller_name=self.controller_name,
            stop_j=types_gen.StopJArgs(deceleration=self._deceleration)),
    ]


class _Sleep(_Command):
  """A Sleep Command pauses the arm."""

  _seconds: float

  def __init__(self, controller_name: str, seconds: float = 0.0) -> None:
    """Init Sleep Arm Command.

    Args:
      controller_name: the name of the controller.
      seconds: The seconds to sleep.
    """
    super().__init__(controller_name)
    self._seconds = seconds

  # pylint: disable=unused-argument
  def to_reach_script(
      self,
      arm_type: arm.ArmType,
      support_vacuum: bool,
      support_blowoff: bool,
      ik_lib: Optional[IKLib],
      ik_hints: Dict[int, List[float]],
      state: arm.ArmState,
      arm_origin: Optional[np.ndarray],
      tip_adjust_transform: Optional[np.ndarray],
  ) -> List[types_gen.ReachScriptCommand]:
    """Convert a Wait into some ReachScript commands.

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
            controller_name=self.controller_name,
            sleep=types_gen.SleepArgs(seconds=self._seconds)),
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
      ik_lib: Optional[IKLib],
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
    if len(cmds) > 1:
      optimized_cmds = [cmds[0]]
      for cmd in cmds[1:]:
        prev_cname = optimized_cmds[len(optimized_cmds) - 1].controller_name
        prev_move_j = optimized_cmds[len(optimized_cmds) - 1].move_j_path
        prev_move_l = optimized_cmds[len(optimized_cmds) - 1].move_l_path
        if (prev_move_j and cmd.move_j_path and
            prev_cname == cmd.controller_name):
          prev_move_j.waypoints.extend(cmd.move_j_path.waypoints)
        elif (prev_move_l and cmd.move_l_path and
              prev_cname == cmd.controller_name):
          prev_move_l.waypoints.extend(cmd.move_l_path.waypoints)
        else:
          optimized_cmds.append(cmd)
      cmds = optimized_cmds
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
  _cached_constraints: Optional[constraints.Constraints]
  _constraints_ik_hints: Optional[Dict[int, List[float]]]
  _ik_lib: Optional[IKLib]
  _ik_lib_type: arm.IKLibType
  _constraints_device: constraints_impl.ConstraintsDevice
  _internal_devices: List[device_base.DeviceBase]
  _digital_outputs: core.ImmutableDictionary[core.ImmutableDictionary[
      digital_output.DigitalOutput]]
  _actions: Optional[actions_impl.ActionDevice]
  _support_vacuum: bool
  _support_blowoff: bool
  _supported_controllers: Optional[Tuple[arm.ArmControllerDescription, ...]]
  _timers: internal.Timers

  def __init__(
      self,
      arm_type: arm.ArmType,
      actions: Optional[actions_impl.ActionDevice] = None,
      workcell_io_config: Optional[workcell_io.IOConfig] = None,
      device_name: str = "",
      ik_lib: Optional[IKLib] = None,
      support_controllers: bool = False,
      default_ik_lib_type: arm.IKLibType = arm.IKLibType.IKFAST) -> None:
    """Construct the Arm Device.

    Args:
      arm_type: The arm type.
      actions: The Action device.
      workcell_io_config: The workcell IO config.
      device_name: The name of the device.
      ik_lib: Override creation of ikfast.
      support_controllers: Robot supports controllers
      default_ik_lib_type: The default ik library.
    """
    requester.Requester.__init__(self)
    self._arm_type = arm_type
    self._device_name = device_name
    self._ik_lib_lock = threading.Lock()
    self._cached_constraints = None
    self._constraints_ik_hints = None
    self._ik_lib = ik_lib
    self._ik_lib_type = default_ik_lib_type
    if not ik_lib:
      self.set_ik_lib(self._ik_lib_type)
    self._constraints_device = constraints_impl.ConstraintsDevice(device_name)
    self._internal_devices = [self._constraints_device]
    self._actions = actions
    self._support_vacuum = False
    self._support_blowoff = False
    self._supported_controllers = None if support_controllers else ()
    self._timers = internal.Timers(set())
    self._digital_outputs = core.ImmutableDictionary({})
    if workcell_io_config is None:
      return
    digital_outputs: Dict[str, Dict[str, digital_output.DigitalOutput]] = {}
    for capability in workcell_io_config.capability:
      if capability.device_type not in {"ur", "robot"}:
        continue
      if capability.device_name != device_name:
        continue
      if capability.io_type == workcell_io.DIGITAL_OUTPUT:
        if capability.type == "vacuum":
          self._support_vacuum = True
        elif capability.type == "blowoff":
          self._support_blowoff = True
        elif not capability.fused_pins:
          if capability.type not in digital_outputs:
            digital_outputs[capability.type] = {}
          dev, wrapper = digital_output_impl.DigitalOutputDevice(
              capability.type, capability.name, device_name,
              tuple([pin.name for pin in capability.pin]),
              capability.fused_pins).get_wrapper()
          digital_outputs[capability.type][capability.name] = wrapper
          self._internal_devices.append(dev)
    digital_outputs_imm: Dict[
        str, core.ImmutableDictionary[digital_output.DigitalOutput]] = {}
    for name, digital_outputs_by_type in digital_outputs.items():
      digital_outputs_imm[name] = core.ImmutableDictionary(
          digital_outputs_by_type)
    self._digital_outputs = core.ImmutableDictionary(digital_outputs_imm)

  @property
  def digital_outputs(
      self
  ) -> core.ImmutableDictionary[core.ImmutableDictionary[
      digital_output.DigitalOutput]]:
    """Get the digital outputs for this arm device."""
    return self._digital_outputs

  @property
  def supported_controllers(
      self) -> Optional[Tuple[arm.ArmControllerDescription, ...]]:
    """The supported controllers, or None if not loaded."""
    return self._supported_controllers

  def fetch_supported_controllers(
      self) -> Optional[Tuple[arm.ArmControllerDescription, ...]]:
    """Fetch the supported controllers."""
    controllers = self.supported_controllers
    if controllers is not None:
      return controllers
    thread_util.extract_all_from_queue(
        self.send_tagged_request(
            types_gen.CommandData(
                tag=utils.generate_tag(),
                ts=utils.timestamp_now(),
                device_type="robot",
                device_name=self.device_name,
                data_type="controller-descriptions-request")))
    return self.supported_controllers

  @property
  def constraints(self) -> constraints_impl.ConstraintsDevice:
    """Return the Device constraints device."""
    return self._constraints_device

  def actions(self) -> Optional[actions_impl.ActionDevice]:
    """Return the action device."""
    return self._actions

  def support_vacuum(self) -> bool:
    """Return if vacuum is supported."""
    return self._support_vacuum

  def support_blowoff(self) -> bool:
    """Return if blowoff is supported."""
    return self._support_blowoff

  def set_ik_lib(self, ik_lib: arm.IKLibType) -> None:
    """Set the IK library to be used."""
    if self._arm_type.joint_count == 0:
      self._ik_lib = None
    elif ik_lib == arm.IKLibType.IKFAST:
      self._ik_lib = IKLibIKFast(self._arm_type.urdf_file)
    elif ik_lib == arm.IKLibType.IKPYBULLET:
      if self._arm_type.urdf_file != "XArm6.urdf":
        raise core.PyReachError("PyBullet is only supported on xarm, not: " +
                                self._arm_type.urdf_file)
      self._ik_lib = IKLibPyBullet()
    else:
      raise core.PyReachError("IK name not recognized.")

  def get_message_supplement(
      self, msg: types_gen.DeviceData) -> Optional[arm.ArmState]:
    """Return the message state (if available) from a message.

    Args:
      msg: The message to scan.

    Returns:
      The device State if it is present in the message.

    """
    if (self._device_name == msg.device_name and msg.device_type == "robot" and
        msg.data_type == "controller-descriptions"):
      descs = []
      if (msg.controller_descriptions and
          msg.controller_descriptions.descriptions):
        for desc in msg.controller_descriptions.descriptions:
          descs.append(arm.ArmControllerDescription(name=desc.name))
      self._supported_controllers = tuple(descs)
    if (self._device_name == msg.device_name and msg.device_type == "robot" and
        msg.data_type == "robot-state"):
      return self._arm_state_from_message(self._arm_type, msg)
    return None

  @property
  def device_name(self) -> str:
    """Return the device name."""
    return self._device_name

  def fk(self,
         joints: Union[Tuple[float, ...], List[float], np.ndarray],
         apply_tip_adjust_transform: bool = False,
         pose_in_world_coordinates: bool = False) -> Optional[core.Pose]:
    """Uses forward kinematics to get the pose from the joint angles.

    Args:
      joints: The robot joints.
      apply_tip_adjust_transform: If True, will use the data in the calibration
        file for the robot to change the returned pose from the end of the arm
        to the tip of the end-effector.
      pose_in_world_coordinates: If true, pose is in world coordinates,
        otherwise if false, pose is in arm base coordinates.

    Returns:
      The pose for the end of the arm, or if apply_tip_adjust_transform was
      set to True, the pose for the tip of the end-effector. If the IK library
      was not yet initialized, this will return None.
    """

    pose: Optional[List[float]] = None

    with self._ik_lib_lock:
      if not self._ik_lib:
        return None
      if isinstance(joints, tuple):
        pose = self._ik_lib.fk(list(joints))
      elif isinstance(joints, list):
        pose = self._ik_lib.fk(joints)
      else:
        pose = self._ik_lib.fk(joints.tolist())

    if pose is None:
      return None

    if not apply_tip_adjust_transform and not pose_in_world_coordinates:
      return core.Pose.from_list(pose)

    state = self.get_cached()
    if state is None:
      return None

    if apply_tip_adjust_transform:
      if state.tip_adjust_t_flange is None:
        return None
      pose = transform_util.multiply_pose(
          np.array(pose, dtype=np.float64),
          np.array(state.tip_adjust_t_flange.as_list(),
                   dtype=np.float64)).tolist()

    if pose_in_world_coordinates:
      if state.base_t_origin is None:
        return None
      pose = transform_util.multiply_pose(
          np.array(state.base_t_origin.as_list(), dtype=np.float64),
          np.array(pose, dtype=np.float64)).tolist()

    if pose is None:
      return None
    return core.Pose.from_list(pose)

  def wait_constraints(self, timeout: Optional[float]) -> bool:
    """Wait for the arm constraints to load.

    Args:
      timeout: the optional maximum time to wait for loading.

    Returns:
      True if the constraints loaded, otherwise false.
    """
    return self._constraints_device.wait_constraints(timeout) is not None

  def _update_ikhints(self) -> Dict[int, List[float]]:
    # Needs to be called in the ik lib lock.
    wc = self._constraints_device.get()
    if wc != self._cached_constraints:
      self._cached_constraints = wc
      if not wc:
        self._constraints_ik_hints = None
      else:
        self._constraints_ik_hints = None
        reference_poses = wc.get_reference_poses(self._device_name)
        if reference_poses:
          self._constraints_ik_hints = {}

          def sorter(named_pose: Tuple[str, constraints.ReferencePose]) -> str:
            return named_pose[0]

          for idx, named_pose in enumerate(
              sorted(reference_poses.items(), key=sorter)):
            self._constraints_ik_hints[idx] = named_pose[1].pose.as_list()
    if self._constraints_ik_hints:
      return self._constraints_ik_hints
    return {}

  def run_command(self,
                  run_async: bool,
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
      run_async: Run the command in a thread with callbacks.
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
    tag = utils.generate_tag()
    try:
      state = self.get_cached()
      if not state:
        raise core.PyReachError("State has not yet been loaded")

      with self._ik_lib_lock:
        script = commands.to_reach_script(
            self._device_name, tag, intent, pick_id, success_type,
            self._arm_type, self._support_vacuum,
            self._support_blowoff, allow_uncalibrated, preemptive, self._ik_lib,
            self._update_ikhints(), state,
            np.array(state.base_t_origin.as_list(), dtype=np.float64)
            if state.base_t_origin else None,
            np.array(state.tip_adjust_t_flange.as_list(), dtype=np.float64)
            if state.tip_adjust_t_flange else None)
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

    # Optimization for async without callbacks
    if run_async and callback is None and finished_callback is None:
      self.send_cmd(script)
      return core.PyReachStatus(
          utils.timestamp_now(), status="rejected", error="timeout")

    q = self.send_tagged_request(script, timeout=timeout)
    if run_async:

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
      self
  ) -> Tuple["ArmDevice", Tuple[device_base.DeviceBase, ...], "ArmImpl"]:
    """Return the Device, Constraints Device, and Arm."""
    return (self, tuple(self._internal_devices), ArmImpl(self))

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
      logging.warning("joints too short: %s", msg.to_json())
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
    analog_inputs: Dict[str, List[float]] = {}
    analog_outputs: Dict[str, List[float]] = {}
    for analog_bank in msg.analog_bank:
      if analog_bank.output:
        analog_outputs[analog_bank.space] = list(analog_bank.state)
      else:
        analog_inputs[analog_bank.space] = list(analog_bank.state)
    digital_inputs: Dict[str, List[bool]] = {}
    digital_outputs: Dict[str, List[bool]] = {}
    for digital_bank in msg.digital_bank:
      if digital_bank.output:
        digital_outputs[digital_bank.space] = list(digital_bank.state)
      else:
        digital_inputs[digital_bank.space] = list(digital_bank.state)
    try:
      robot_mode = arm.RobotMode.from_string(msg.robot_mode)
    except ValueError:
      robot_mode = arm.RobotMode.DEFAULT

    adjust_pose: Optional[core.Pose] = None
    tip_adjust_transform: Optional[core.Pose] = None
    if msg.tip_adjust_t_base:
      adjust_pose = core.Pose.from_list(msg.tip_adjust_t_base)
      tip_adjust_transform = core.Pose.from_list(
          transform_util.multiply_pose(
              transform_util.inverse_pose(np.array(pose, dtype=np.float64)),
              np.array(msg.tip_adjust_t_base, dtype=np.float64)).tolist())
    base_origin: Optional[core.Pose] = None
    pose_origin: Optional[core.Pose] = None
    adjust_pose_origin: Optional[core.Pose] = None
    if msg.base_t_origin:
      base_origin = core.Pose.from_list(msg.base_t_origin)
      pose_origin = core.Pose.from_list(
          transform_util.multiply_pose(
              np.array(msg.base_t_origin, dtype=np.float64),
              np.array(pose, dtype=np.float64)).tolist())
      if msg.tip_adjust_t_base:
        adjust_pose_origin = core.Pose.from_list(
            transform_util.multiply_pose(
                np.array(msg.base_t_origin, dtype=np.float64),
                np.array(msg.tip_adjust_t_base, dtype=np.float64)).tolist())
    pose_t = core.Pose.from_list(pose)
    return arm.ArmState(
        utils.time_at_timestamp(msg.ts), msg.seq,
        msg.device_type, msg.device_name, tuple(joints), pose_t, pose_t,
        tuple(force), msg.is_protective_stopped, msg.is_emergency_stopped,
        msg.is_safeguard_stopped, msg.is_reduced_mode, msg.safety_message,
        msg.is_program_running, msg.is_robot_power_on, robot_mode,
        tip_adjust_transform, adjust_pose, base_origin, pose_origin,
        adjust_pose_origin)

  @property
  def arm_type(self) -> arm.ArmType:
    """Return the arm type of the arm."""
    return self._arm_type


class ArmImpl(arm.Arm):
  """Represents a multi-joint Arm."""

  _device: ArmDevice
  _enable_randomization: bool
  _acquire_tag: Optional[int]

  def __init__(self, device: ArmDevice) -> None:
    """Init the Arm."""
    self._device = device
    self._enable_randomization = True
    self._acquire_tag = None

  @property
  def arm_type(self) -> arm.ArmType:
    """Return the arm type of the arm."""
    return self._device.arm_type

  @property
  def digital_outputs(
      self
  ) -> core.ImmutableDictionary[core.ImmutableDictionary[
      digital_output.DigitalOutput]]:
    """Get the digital outputs for this arm device."""
    return self._device.digital_outputs

  @property
  def supported_controllers(
      self) -> Optional[Tuple[arm.ArmControllerDescription, ...]]:
    """The supported controllers, or None if not loaded."""
    return self._device.supported_controllers

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
                                             "robot-state", request_period)

  def stop_streaming(self) -> None:
    """Stop streaming arm states."""
    self._device.set_untagged_request_period("robot", self.device_name,
                                             "robot-state", None)

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
                controller_name: str = "",
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
      controller_name: The name of the controller to send the command to.
      timeout: The amount time to wait before giving up. (Default: No timeout)

    Returns:
      Return the latest Arm status upon success; otherwise None.

    """
    move_command: Union[_MoveLinear, _MoveJoints]
    if use_linear:
      move_command = _MoveLinear(
          controller_name,
          list(joints),
          servo=servo,
          acceleration=acceleration,
          velocity=velocity)
    else:
      move_command = _MoveJoints(
          controller_name,
          list(joints),
          servo=servo,
          acceleration=acceleration,
          velocity=velocity,
          servo_time_seconds=servo_time_seconds,
          servo_lookahead_time_seconds=servo_lookahead_time_seconds,
          servo_gain=servo_gain)

    return self._device.run_command(
        False,
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
      joints: Union[List[float], Tuple[float, ...], np.ndarray],
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
      controller_name: str = "",
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
      controller_name: The name of the controller to send the command to.
      timeout: The number of seconds to wait before timing out.
      callback: An optional callback routine call upon completion.
      finished_callback: An optional callback when done.
    """
    move_command: Union[_MoveLinear, _MoveJoints]
    if use_linear:
      move_command = _MoveLinear(
          controller_name,
          list(joints),
          servo=servo,
          acceleration=acceleration,
          velocity=velocity)
    else:
      move_command = _MoveJoints(
          controller_name,
          list(joints),
          servo=servo,
          acceleration=acceleration,
          velocity=velocity,
          servo_time_seconds=servo_time_seconds,
          servo_lookahead_time_seconds=servo_lookahead_time_seconds,
          servo_gain=servo_gain)

    self._device.run_command(
        True,
        _Commands([move_command]),
        intent=intent,
        pick_id=pick_id,
        success_type=success_type,
        allow_uncalibrated=allow_uncalibrated,
        timeout=timeout,
        preemptive=preemptive,
        callback=callback,
        finished_callback=finished_callback)

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
              controller_name: str = "",
              pose_in_world_coordinates: bool = False,
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
       controller_name: The name of the controller to send the command to.
       pose_in_world_coordinates: If true, pose is in world coordinates,
         otherwise if false, pose is in arm base coordinates.
       timeout: The amount of time to wait until giving up.

    Returns:
       Return the Status on success and None on timeout.

    """
    return self._device.run_command(
        False,
        _Commands([
            _MovePose(
                controller_name,
                types_gen.Vec3d(*pose.position.as_list()),
                types_gen.Vec3d(*pose.orientation.axis_angle.as_list()),
                use_linear=use_linear,
                servo=servo,
                acceleration=acceleration,
                velocity=velocity,
                apply_tip_adjust_transform=apply_tip_adjust_transform,
                servo_time_seconds=servo_time_seconds,
                servo_lookahead_time_seconds=servo_lookahead_time_seconds,
                servo_gain=servo_gain,
                pose_in_world_coordinates=pose_in_world_coordinates)
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
      controller_name: str = "",
      pose_in_world_coordinates: bool = False,
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
      controller_name: The name of the controller to send the command to.
      pose_in_world_coordinates: If true, pose is in world coordinates,
        otherwise if false, pose is in arm base coordinates.
      timeout: The amount of time to wait until giving up.
      callback: Optional function to call when done (None for fail.)
      finished_callback: Optional finish function to call when done.

    Returns:
      Return the Status on success and None on timeout.
    """
    self._device.run_command(
        True,
        _Commands([
            _MovePose(
                controller_name,
                types_gen.Vec3d(*pose.position.as_list()),
                types_gen.Vec3d(*pose.orientation.axis_angle.as_list()),
                use_linear=use_linear,
                servo=servo,
                acceleration=acceleration,
                velocity=velocity,
                apply_tip_adjust_transform=apply_tip_adjust_transform,
                servo_time_seconds=servo_time_seconds,
                servo_lookahead_time_seconds=servo_lookahead_time_seconds,
                servo_gain=servo_gain,
                pose_in_world_coordinates=pose_in_world_coordinates)
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
      controller_name: str = "",
      timeout: Optional[float] = None,
  ) -> Optional[core.PyReachStatus]:
    """Set the vacuum state synchronously.

    Args:
      vacuum_state: The desired vacuum state.
      intent: The intent of the command.
      pick_id: The pick_id of the command.
      success_type: The success_type of the command.
      controller_name: The name of the controller to send the command to.
      timeout: The time in seconds to wait until failing.

    Returns:
      The Arm status on success and None otherwise.
    """
    return self._device.run_command(
        False,
        _Commands([_SetVacuumState(controller_name, vacuum_state)]),
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
      controller_name: str = "",
      timeout: Optional[float] = None,
      callback: Optional[Callable[[core.PyReachStatus], None]] = None,
      finished_callback: Optional[Callable[[], None]] = None) -> None:
    """Asynchronously set the Vacuum State.

    Args:
      vacuum_state: The VacuumState to set.
      intent: The intent string (or empty) for the request.
      pick_id: The pick id (or empty) for the request.
      success_type: The success type to return on success.
      controller_name: The name of the controller to send the command to.
      timeout: An optional timeout measured in seconds.
      callback: A callback function to invoke when the vacuum state arrives.
      finished_callback: A callback function to call when done.
    """
    self._device.run_command(
        True,
        _Commands([_SetVacuumState(controller_name, vacuum_state)]),
        intent=intent,
        pick_id=pick_id,
        success_type=success_type,
        timeout=timeout,
        callback=callback,
        finished_callback=finished_callback)

  def _action_to_commands(self, action: actions_impl.Action,
                          inputs: List[arm.ActionInput],
                          use_unity_ik: bool) -> _Commands:
    global_acceleration = action.get_max_accel()
    global_velocity = action.get_max_velocity()
    steps = action.get_steps().copy()
    if action.get_cyclic() and steps:
      steps.append(steps[0])

    step_pose: Dict[int, Tuple[types_gen.Vec3d, types_gen.Quaternion3d]] = {}
    commands: List[_Command] = []
    while len(step_pose) < len(steps):
      start_len = len(step_pose)
      for idx, step in enumerate(steps):
        if idx in step_pose:
          continue

        if step.get_wait() > 0:
          wait = step.get_wait()
          commands.append(_Sleep("", wait))
          if step.get_parent_step_idx() in step_pose:
            step_pose[idx] = step_pose[step.get_parent_step_idx()]
          else:
            step_pose[idx] = (types_gen.Vec3d(), types_gen.Quaternion3d())
          continue
        elif step.get_acquire_image_tag():
          acquire_tag: str
          if self._acquire_tag is not None:
            self._acquire_tag += 1
            acquire_tag = "tag-a-" + str(self._acquire_tag)
          else:
            acquire_tag = utils.generate_tag()
          commands.append(
              _AcquireImage("", step.get_set_capability_type(),
                            step.get_set_capability_name(),
                            step.get_acquire_image_mode(), acquire_tag))
          if step.get_parent_step_idx() in step_pose:
            step_pose[idx] = step_pose[step.get_parent_step_idx()]
          else:
            step_pose[idx] = (types_gen.Vec3d(), types_gen.Quaternion3d())
          continue
        elif step.get_set_capability():
          if step.get_set_capability_type(
          ) == "point-reached" and step.get_set_capability_name(
          ) == "place-point":
            commands.append(
                _SetOutput("", step.get_set_capability_type(),
                           step.get_set_capability_name(), [("", 0)], []))
          elif step.get_set_capability_io_type() == "DigitalOutput":
            commands.append(
                _SetOutput("", step.get_set_capability_type(),
                           step.get_set_capability_name(),
                           [("", int(step.get_set_capability_value()))], []))
          else:
            raise core.PyReachError("unsupported action statement: " +
                                    str(idx) + ": " + str(step.__dict__))
          if step.get_parent_step_idx() in step_pose:
            step_pose[idx] = step_pose[step.get_parent_step_idx()]
          else:
            step_pose[idx] = (types_gen.Vec3d(), types_gen.Quaternion3d())
          continue

        velocity = global_velocity
        accel = global_acceleration
        if step.get_individual_velocity_acceleration():
          velocity = step.get_velocity()
          accel = step.get_acceleration()
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

        apply_tip_adjust_transform = False
        if step.get_parent_type() == actions_impl.ActionStepParentType.ABSOLUTE:
          target_tip_transform = transform_util.unity_pos_quaternion_to_pose(
              np_pos.tolist(), np_rot.tolist())
          target_tip_transform = transform_util.multiply_pose(
              target_tip_transform, offset)

          if step.get_parent_step_idx() in step_pose:
            step_pose[idx] = step_pose[step.get_parent_step_idx()]
          else:
            step_pose[idx] = (types_gen.Vec3d(), types_gen.Quaternion3d())
        elif step.get_parent_type(
        ) == actions_impl.ActionStepParentType.TIP_INPUT:
          apply_tip_adjust_transform = True
          if step.get_tip_input_idx() >= len(inputs):
            raise core.PyReachError("Not enough inputs")

          input_data = inputs[step.get_tip_input_idx()]
          # Singulation
          if input_data.prediction_point:
            input_pose_normal = input_data.prediction_point
            np_pos = np_pos / 100
            target_tip_transform = transform_util.pos_quaternion_to_pose(
                np_pos.tolist(), np_rot.tolist())
            target_tip_transform = transform_util.multiply_pose(
                input_pose_normal[0], target_tip_transform)
            target_tip_transform = transform_util.multiply_pose(
                target_tip_transform, offset)
            normal = transform_util.get_z_direction(target_tip_transform)

            if np.dot(normal, input_pose_normal[2]) > 0:
              flipz_trans = np.array([0.0, 0.0, 0.0])
              flipz_rot = np.array([-np.pi, 0.0, 0.0])
              flipz_t = transform_util.matrix_to_pose(
                  transform_util.convert_to_matrix(flipz_trans, flipz_rot))
              target_tip_transform = transform_util.multiply_pose(
                  target_tip_transform, flipz_t)
              target_tip_transform = transform_util.angular_mod_pose(
                  target_tip_transform)
          # Kitting
          elif input_data.position and input_data.rotation:
            np_pos = np_pos / 100

            # This is already in Unity space.
            target_tip_transform = transform_util.pos_quaternion_to_pose(
                np_pos.tolist(), np_rot.tolist())
            position_list = [
                input_data.position.x, input_data.position.y,
                input_data.position.z
            ]
            rotation_list = [
                input_data.rotation.x, input_data.rotation.y,
                input_data.rotation.z, input_data.rotation.w
            ]

            # Convert to Unity space.
            input_transform = transform_util.unity_pos_quaternion_to_pose(
                position_list, rotation_list)

            # Apply rotation fix Euler 90, 180, 0 in YXZ on inputs as
            # per Unity implementation.
            quaternion_const = transform_util.inverse_quat(
                np.array(
                    [0.0, -1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0), 0.0]))
            input_matrix_unity_translation = input_transform[:3]
            input_matrix_unity_rotation = input_transform[3:]
            input_matrix_unity_rotation_quat = transform_util.axis_angle_to_quaternion(
                input_matrix_unity_rotation)
            input_matrix_unity_rotation = transform_util.quaternion_multiply(
                input_matrix_unity_rotation_quat, quaternion_const)

            # Adjusted input pose in Unity space.
            new_input_pose_unity = transform_util.pos_quaternion_to_pose(
                input_matrix_unity_translation.tolist(),
                input_matrix_unity_rotation.tolist())

            # Input and step pose in Unity space.
            target_tip_transform = transform_util.multiply_pose(
                new_input_pose_unity, target_tip_transform)

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

        use_linear = False
        if step.get_use_process_mode():
          use_linear = True
        commands.append(
            _MovePose(
                controller_name="",
                translation=types_gen.Vec3d(target_tip_transform[0],
                                            target_tip_transform[1],
                                            target_tip_transform[2]),
                rotation=types_gen.Vec3d(target_tip_transform[3],
                                         target_tip_transform[4],
                                         target_tip_transform[5]),
                velocity=velocity,
                acceleration=accel,
                blend_radius=step.get_radius(),
                use_linear=use_linear,
                use_unity_ik=use_unity_ik,
                apply_tip_adjust_transform=apply_tip_adjust_transform,
                pose_in_world_coordinates=True))

      if len(step_pose) == start_len:
        raise core.PyReachError("Action invalid: contains infinite loop")
    return _Commands(commands)

  def _execute_action(
      self,
      run_async: bool,
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
      run_async: Run the command in a thread with callbacks.
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
        run_async,
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
    self._execute_action(
        True,
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
        False,
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
           controller_name: str = "",
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
      controller_name: The name of the controller to send the command to.
      timeout: An optional timeout measured in seconds.

    Returns:
      Status of the request.

    """
    return self._device.run_command(
        False,
        _Commands(
            [_Stop(controller_name=controller_name,
                   deceleration=deceleration)]),
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
      controller_name: str = "",
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
      controller_name: The name of the controller to send the command to.
      timeout: An optional timeout measured in seconds.
      callback: An optional callback routine call upon completion.
      finished_callback: An optional callback when done.
    """
    self._device.run_command(
        True,
        _Commands(
            [_Stop(controller_name=controller_name,
                   deceleration=deceleration)]),
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
         apply_tip_adjust_transform: bool = False,
         pose_in_world_coordinates: bool = False) -> Optional[core.Pose]:
    """Uses forward kinematics to get the pose from the joint angles.

    Args:
      joints: The robot joints.
      apply_tip_adjust_transform: If True, will use the data in the calibration
        file for the robot to change the returned pose from the end of the arm
        to the tip of the end-effector.
      pose_in_world_coordinates: If true, pose is in world coordinates,
        otherwise if false, pose is in arm base coordinates.

    Returns:
      The pose for the end of the arm, or if apply_tip_adjust_transform was
      set to True, the pose for the tip of the end-effector. If the IK library
      was not yet initialized, this will return None.
    """

    return self._device.fk(joints, apply_tip_adjust_transform,
                           pose_in_world_coordinates)

  def wait_constraints(self, timeout: Optional[float] = None) -> bool:
    """Wait for the arm constraints to load.

    Args:
      timeout: the optional maximum time to wait for loading.

    Returns:
      True if the constraints loaded, otherwise false.
    """
    return self._device.wait_constraints(timeout)
