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

"""Mock Interface for interacting with a single robot arm."""

from typing import List, Optional, Callable, Tuple, Union

import numpy as np

from pyreach import arm
from pyreach import constraints
from pyreach import core
from pyreach import digital_output
from pyreach.gyms import arm_element
from pyreach.gyms import reach_element
from pyreach.mock import digital_output_mock

# Type hint appreviations:
DigOutput = digital_output.DigitalOutput
DigOutputMock = digital_output_mock.DigitalOutputMock
DigOutState = digital_output.DigitalOutputState
DigOutPinState = digital_output.DigitalOutputPinState
ImmutableDict = core.ImmutableDictionary


class ArmMock(arm.Arm):
  """Interface of a multi-joint Arm."""

  arm_config: arm_element.ReachArm

  def __init__(self, arm_config: reach_element.ReachElement) -> None:
    """Initialize Mock Arm."""
    super().__init__()
    assert isinstance(arm_config, arm_element.ReachArm), (
        f"Got {type(arm_config)} instead of arm_element.ReachArm")
    self.arm_config = arm_config

  @property
  def device_name(self) -> str:
    """Return the Arm device name."""
    return ""

  def state(self) -> Optional[arm.ArmState]:
    """Return the latest state of the arm."""
    arm_config: arm_element.ReachArm = self.arm_config
    test_states: Optional[List[arm.ArmState]] = arm_config.test_states
    arm_state: Optional[arm.ArmState] = None
    if test_states:
      arm_state = test_states.pop(0)
      assert isinstance(
          arm_state,
          arm.ArmState), (f"Found {type(arm_state)} instead of arm.ArmState")
    if not arm_state:
      arm_state = arm.ArmState()
    return arm_state

  @property
  def arm_type(self) -> arm.ArmType:
    """Return the arm type of the arm."""
    raise NotImplementedError

  @property
  def digital_outputs(self) -> ImmutableDict[ImmutableDict[DigOutput]]:
    """Get the digital outputs for this arm device."""
    # time: float = 1.0
    # sequence: int = 1
    # robot_name: str = "robot_robot_name"
    # capability_name: str = "capability_name"
    # pin_states: Tuple[DigOutPinState, ...] = ()  # TODO(gramlich): fix
    dig_output: DigOutput = DigOutputMock()
    pin_outputs: ImmutableDict[DigOutput] = ImmutableDict({
        "pin_name": dig_output,
    })
    capabilities: ImmutableDict[ImmutableDict[DigOutput]] = ImmutableDict({
        "capability_type": pin_outputs,
    })
    return capabilities

  def set_ik_lib(self, ik_lib: arm.IKLibType) -> None:
    """Set the IK library to be used.

    Args:
      ik_lib: str, name for the IK library to use (ikfast or ik_pybullet
        supported).
    """

  def add_update_callback(
      self,
      callback: Callable[[arm.ArmState], bool],
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
    # arm_state: arm.ArmState = arm.ArmState(
    #     time=1.0,
    #     sequence=1
    # )
    # _ = callback(arm_state)

    # def stop_callback() -> None:
    #   assert False  # Fail hard

    raise NotImplementedError("arm_mock.py:add_update_callback()")
    # return stop_callback

  def start_streaming(self, request_period: float = 0.1) -> None:
    """Start streaming of arm state.

    Args:
      request_period: The number of seconds between arm states. Defaults to .1
        seconds between arm states.
    """
    pass

  def stop_streaming(self) -> None:
    """Stop streaming arm states."""
    raise NotImplementedError

  @property
  def joint_limits(self) -> Optional[Tuple[constraints.JointLimit, ...]]:
    """Return the joint limits of the arm. None if not available."""
    raise NotImplementedError

  def fetch_state(self, timeout: float = 15.0) -> Optional[arm.ArmState]:
    """Fetch a new arm state.

    Block until a new arm state is available or timeout.

    Args:
      timeout: The number of seconds to wait before giving up.

    Returns:
      Return the latest state or None for a timeout.

    """
    time: float = 0.0
    sequence: int = 0
    joint_angles: Tuple[float, ...] = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    pose: core.Pose = core.Pose.from_tuple((0.0, 0.0, 0.0, 1.0, 0.0, 0.0))
    force: Tuple[float, ...] = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    return arm.ArmState(time, sequence, "robot", "", joint_angles, pose, pose,
                        force, False, False, False, False, "", False, False,
                        arm.RobotMode.DEFAULT)

  def async_fetch_state(
      self,
      timeout: float = 15.0,
      callback: Optional[Callable[[arm.ArmState], None]] = None,
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
    if callback:
      pyreach_status: core.PyReachStatus = core.PyReachStatus(
          time=1.0,
          status="status",
          script="script",
          error="error",
          progress=1.0,
          message="message",
          code=0)
      callback(pyreach_status)
    if finished_callback:
      finished_callback()

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
                     inputs: List[arm.ActionInput],
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
