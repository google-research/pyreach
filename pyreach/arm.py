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
"""Interface for interacting with a single robot arm.

Supported features
  - State reporting
  - Constraints such as joint limits
  - Commands: joint move and Cartesian move.
  - Action template: execute a predefined action.
  - Streaming control
"""
import dataclasses
import enum
from typing import Callable, List, Optional, Tuple, Union

import numpy as np

from pyreach import constraints
from pyreach import core
from pyreach import digital_output


class IKLibType(enum.Enum):
  """IK library enumeration type."""

  IKFAST = "ikfast"
  IKPYBULLET = "ik_pybullet"


class RobotMode(enum.Enum):
  """Robot mode type."""

  DEFAULT = ""
  NORMAL = "normal"
  LOCAL = "local"

  @classmethod
  def from_string(cls, robot_mode: str) -> "RobotMode":
    for option in cls:
      if option.value == robot_mode:
        return option
    raise ValueError("Invalid robot mode: " + robot_mode)


class ArmType:
  """ArmType defines a type of arm for a robot."""

  @property
  def urdf_file(self) -> str:
    """Converts an arm_type to an associate URDF."""
    raise NotImplementedError

  @property
  def joint_count(self) -> int:
    """Get the joint count of the arm."""
    raise NotImplementedError


@dataclasses.dataclass(frozen=True)
class ActionInput:
  """The action input to be used only for oracle actions.

  Attributes:
    prediction_point: Used for singulation oracle.
    position: position used for kitting oracle.
    rotation: rotation used for kitting oracle.
  """

  prediction_point: Optional[Tuple[np.ndarray, np.ndarray, np.ndarray]]
  position: Optional[core.Translation]
  rotation: Optional[core.Quaternion]


@dataclasses.dataclass(frozen=True)
class ArmControllerDescription:
  """The description of an arm controller.

  Attributes:
    name: The name of the controller.
  """
  name: str


@dataclasses.dataclass(frozen=True)
class ArmState:
  """The state of a robot Arm at a specific time.

  Attributes:
    time: The timestamp when the arm state is measured.
    sequence: The sequence number of the arm state.
    device_type: The device type of the arm..
    device_name: The device name of the arm.
    joint_angles: The arm joint angles in radians.
    pose: The pose of the arm (alias for flange_t_base).
    flange_t_base: The pose of the robot flange relative to the base of the arm.
    force: The arm joint force values in Newton-meters.  Robot specific.
    is_protective_stopped: True if the robot is protective stopped.
    is_emergency_stopped: True if the robot is emergency stopped.
    is_safeguard_stopped: True if the robot is safeguard stopped.
    is_reduced_mode: True if the robot is in reduced mode.
    safety_message: Safety state message from the robot.
    is_program_running: True if a program is running on the robot.
    is_robot_power_on: True if the robot power is on.
    robot_mode: Mode of operation of the robot.
    tip_adjust_t_flange: Adjust transform for the tooltip.
    tip_adjust_t_base: Pose with the tip adjust applied relative to the base of
      the arm.
  """

  time: float = 0.0
  sequence: int = 0
  device_type: str = "robot"
  device_name: str = ""
  joint_angles: Tuple[float, ...] = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
  pose: core.Pose = core.Pose(
      core.Translation(0.0, 0.0, 0.0), core.AxisAngle.from_tuple(
          (0.0, 0.0, 0.0)))
  flange_t_base: core.Pose = core.Pose(
      core.Translation(0.0, 0.0, 0.0), core.AxisAngle.from_tuple(
          (0.0, 0.0, 0.0)))
  force: Tuple[float, ...] = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
  is_protective_stopped: bool = False
  is_emergency_stopped: bool = False
  is_safeguard_stopped: bool = False
  is_reduced_mode: bool = False
  safety_message: str = ""
  is_program_running: bool = False
  is_robot_power_on: bool = False
  robot_mode: RobotMode = RobotMode.DEFAULT
  tip_adjust_t_flange: Optional[core.Pose] = None
  tip_adjust_t_base: Optional[core.Pose] = None


class Arm(object):
  """Interface of a multi-joint Arm."""

  @property
  def device_name(self) -> str:
    """Return the Arm device name."""
    raise NotImplementedError

  def state(self) -> Optional[ArmState]:
    """Return the latest state of the arm."""
    raise NotImplementedError

  @property
  def arm_type(self) -> ArmType:
    """Return the arm type of the arm."""
    raise NotImplementedError

  @property
  def digital_outputs(
      self
  ) -> core.ImmutableDictionary[core.ImmutableDictionary[
      digital_output.DigitalOutput]]:
    """Get the digital outputs for this arm device."""
    raise NotImplementedError

  @property
  def supported_controllers(
      self) -> Optional[Tuple[ArmControllerDescription, ...]]:
    """The supported controllers, or None if not loaded."""
    raise NotImplementedError

  def set_ik_lib(self, ik_lib: IKLibType) -> None:
    """Set the IK library to be used.

    Args:
      ik_lib: str, name for the IK library to use (ikfast or ik_pybullet
        supported).
    """
    raise NotImplementedError

  def add_update_callback(
      self,
      callback: Callable[[ArmState], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback for the arm state.

    Args:
      callback: Callback called when a new arm state arrives. The callback
        function should return False for continuous state update. When the
        callback function returns True, it will stop receiving future updates.
      finished_callback: Optional callback, called when the callback is stopped
        or if the arm is stopped.

    Returns:
      A function that when called stops the callback.

    """
    raise NotImplementedError

  def start_streaming(self, request_period: float = 0.1) -> None:
    """Start streaming of arm state.

    Args:
      request_period: The number of seconds between arm states. Defaults to .1
        seconds between arm states.
    """
    raise NotImplementedError

  def stop_streaming(self) -> None:
    """Stop streaming arm states."""
    raise NotImplementedError

  @property
  def joint_limits(self) -> Optional[Tuple[constraints.JointLimit, ...]]:
    """Return the joint limits of the arm. None if not available."""
    raise NotImplementedError

  def fetch_state(self, timeout: float = 15.0) -> Optional[ArmState]:
    """Fetch a new arm state.

    Block until a new arm state is available or timeout.

    Args:
      timeout: The number of seconds to wait before giving up.

    Returns:
      Return the latest state or None for a timeout.

    """
    raise NotImplementedError

  def async_fetch_state(
      self,
      timeout: float = 15.0,
      callback: Optional[Callable[[ArmState], None]] = None,
      error_callback: Optional[Callable[[core.PyReachStatus], None]] = None
  ) -> None:
    """Fetch a new arm state.

    Non-blocking.

    Args:
      timeout: The number of seconds to wait before giving up.
      callback: Optional callback when a new arm state arrives.
      error_callback: Optional callback called if there is an error.
    """
    raise NotImplementedError

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
    """Move the arm to a target joint configuration synchronously.

    Args:
      joints: The list of joint angles in radians.
      use_linear: Whether to move in linear space. (Default: False)
      servo: Use servoing. (Default: False)
      intent: The intent of the command. (Default: no intent)
      pick_id: The pick_id of the command. (Default: no pick id)
      success_type: The success_type of the command. (Default; no success type)
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
      timeout: The amount time to wait before giving up. (Default: no timeout)

    Returns:
      Return the status of the move arm command.

    """
    raise NotImplementedError

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
    """Move the arm to a target joint configuration asynchronously.

    Args:
      joints: The joint angles in radians.
      use_linear: Whether to move in linear space. (Default: False)
      servo: Use servoing. (Default: False)
      intent: The intent of the command. (Default: no intent)
      pick_id: The pick_id of the command. (Default: no pick id)
      success_type: The success_type of the command. (Default: no success type)
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
      timeout: The amount time to wait before giving up. (Default: no timeout)
      callback: An optional callback routine call upon completion.
      finished_callback: An optional callback when done.
    """
    raise NotImplementedError

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
              timeout: Optional[float] = None) -> core.PyReachStatus:
    """Move the arm to a target pose synchronously.

    Args:
      pose: The target pose of the arm in [x, y, z, rx, ry, rz]. Rotation in
        axis-angle.
      use_linear: True if a linear translation is required.
      servo: Use servoing. (Default: False)
      intent: The intent of the command. (Default: no intent)
      pick_id: The pick_id of the command. (Default: no pick id)
      success_type: The success_type of the command. (Default: no success type)
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
      timeout: The amount time to wait before giving up. (Default: no timeout)

    Returns:
       Return the Status

    """
    raise NotImplementedError

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
      timeout: Optional[float] = None,
      callback: Optional[Callable[[core.PyReachStatus], None]] = None,
      finished_callback: Optional[Callable[[], None]] = None) -> None:
    """Move the arm to a target pose asynchronously.

    Args:
      pose: The target pose of the arm in [x, y, z, rx, ry, rz]. Rotation is in
        axis-angle format.
      use_linear: True if a linear translation is required.
      servo: Use servoing. (Default: False)
      intent: The intent of the command. (Default: no intent)
      pick_id: The pick_id of the command. (Default: no pick id)
      success_type: The success_type of the command. (Default; no success type)
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
      timeout: The amount time to wait before giving up. (Default: no timeout)
      callback: An optional callback routine call upon completion.
      finished_callback: An optional callback when done.

    Returns:
      Return the Status on success and None on timeout.

    """
    raise NotImplementedError

  def async_execute_action(
      self,
      action_name: str,
      inputs: List[ActionInput],
      intent: str = "",
      pick_id: str = "",
      success_type: str = "",
      use_unity_ik: bool = False,
      allow_uncalibrated: bool = False,
      preemptive: bool = False,
      timeout: Optional[float] = None,
      callback: Optional[Callable[[core.PyReachStatus], None]] = None,
      finished_callback: Optional[Callable[[], None]] = None) -> None:
    """Execute an action template asynchronously.

    Args:
      action_name: Name of the action template.
      inputs: Input to the action template.
      intent: The intent of the command. (Default: no intent)
      pick_id: The pick_id of the command. (Default: no pick id)
      success_type: The success_type of the command. (Default: no success type)
      use_unity_ik: Whether to follow the Unity convention.
      allow_uncalibrated: Allow motion when uncalibrated (unsafe, should only be
        set in calibration code).
      preemptive: True to preempt existing scripts.
      timeout: An optional timeout measured in seconds.
      callback: An optional callback routine call upon completion.
      finished_callback: An optional callback when done.

    Returns:
      Status of the request.

    """
    raise NotImplementedError

  def execute_action(self,
                     action_name: str,
                     inputs: List[ActionInput],
                     intent: str = "",
                     pick_id: str = "",
                     success_type: str = "",
                     use_unity_ik: bool = False,
                     allow_uncalibrated: bool = False,
                     preemptive: bool = False,
                     timeout: Optional[float] = None) -> core.PyReachStatus:
    """Execute an action template synchronously.

    Args:
      action_name: Name of the action template.
      inputs: Input to the action template.
      intent: The intent of the command. (Default: no intent)
      pick_id: The pick_id of the command. (Default: no pick id)
      success_type: The success_type of the command. (Default: no success type)
      use_unity_ik: Whether to follow the Unity convention.
      allow_uncalibrated: Allow motion when uncalibrated (unsafe, should only be
        set in calibration code).
      preemptive: True to preempt existing scripts.
      timeout: An optional timeout measured in seconds.

    Returns:
      Status of the request.

    """
    raise NotImplementedError

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
    raise NotImplementedError

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
    raise NotImplementedError

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
    raise NotImplementedError

  def wait_constraints(self, timeout: Optional[float] = None) -> bool:
    """Wait for the arm constraints to load.

    Args:
      timeout: the optional maximum time to wait for loading.

    Returns:
      True if the constraints loaded, otherwise false.
    """
    raise NotImplementedError
