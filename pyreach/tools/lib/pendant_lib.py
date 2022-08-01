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
"""Library for the pendant GUI."""
import os
import subprocess
import threading
from typing import Any, Callable, List, Optional, Tuple

import cv2  # type: ignore  # type: ignore
import numpy as np

from pyreach.arm import Arm
from pyreach.arm import ArmControllerDescription
from pyreach.common.base import transform_util
from pyreach.core import AxisAngle
from pyreach.core import Pose
from pyreach.core import PyReachError
from pyreach.core import PyReachStatus
from pyreach.core import Translation
from pyreach.factory import ConnectionFactory
from pyreach.host import Host
from pyreach.host import SessionState
from pyreach.vacuum import Vacuum

ContinuousControlThread = Callable[
    [List["Pendant"], Callable[[float], bool], float], None]

_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
_DEBUG = False
_MAX_JOINT_ANGULAR_DIST = 0.5
_POSITION_STEP_DEFAULT = 0.05
_ROTATION_STEP_DEFAULT = 0.1

_POSITION_STEP_MIN = 0.001
_POSITION_STEP_MAX = 0.10
_ROTATION_STEP_MIN = 0.001
_ROTATION_STEP_MAX = 0.1

_RADIAL_VELOCITY_RAD_PER_SEC = 1
_RADIAL_ACCELERATION_RAD_PER_SEC2 = 1

_XARM_HOMEJ = [0.0, -1.0, 0.0, 0.0, 0.0,
               0.0]  # shoulder back a bit to prevent tool crashing
_XARM_HOMEJ_VELOCITY = 1.5

# 50Hz.  100Hz causes some stuttering on the reach serve side
_CONTINUOUS_CONTROL_INTERVAL_DELAY_SECONDS = 0.02

_COLOR_DISABLED = (128, 128, 128)
_COLOR_ENABLED = (128, 200, 128)
_COLOR_TEXT = (0, 0, 0)
_COLOR_WARNING_TEXT = (0, 0, 255)
_COLOR_CLEARSTOP = _COLOR_DISABLED
_TEXT_THICKNESS = 1
_TEXT_Y = 15
_TEXT_YINC = 15

_TEXT_SIZE = 0.8
_TEXT_FONT = cv2.FONT_HERSHEY_PLAIN

_BUTTON_XP = (98, 134, 144, 168)
_BUTTON_XN = (9, 133, 45, 161)
_BUTTON_YP = (58, 117, 94, 143)
_BUTTON_YN = (49, 157, 98, 189)
_BUTTON_ZP = (20, 70, 65, 110)
_BUTTON_ZN = (83, 68, 134, 114)

_BUTTON_RXP = (58, 289, 93, 317)
_BUTTON_RXN = (58, 233, 92, 265)
_BUTTON_RYP = (104, 212, 139, 253)
_BUTTON_RYN = (9, 210, 48, 248)
_BUTTON_RZP = (88, 258, 118, 294)
_BUTTON_RZN = (31, 258, 63, 297)

_BUTTON_J0N = (162, 68, 193, 104)
_BUTTON_J0P = (302, 72, 330, 102)
_BUTTON_J1N = (163, 112, 192, 144)
_BUTTON_J1P = (300, 113, 330, 144)
_BUTTON_J2N = (161, 157, 193, 187)
_BUTTON_J2P = (300, 158, 330, 190)
_BUTTON_J3N = (161, 196, 192, 232)
_BUTTON_J3P = (301, 199, 329, 231)
_BUTTON_J4N = (163, 242, 191, 272)
_BUTTON_J4P = (302, 241, 330, 276)
_BUTTON_J5N = (163, 286, 192, 321)
_BUTTON_J5P = (300, 286, 328, 319)

CARTESIAN_CONTROLS = [7, 60, 150, 318]

_BUTTON_STOP = (13, 365, 134, 390)
_BUTTON_VACUUM = (160, 335, 234, 365)
_BUTTON_CONTINUOUS = (160, 370, 234, 400)
_BUTTON_BLOWOFF = (258, 335, 325, 365)
_BUTTON_HOMEJ = (258, 370, 325, 400)
_BUTTON_HOMEJ_Y = (258, 370, 278, 400)
_BUTTON_HOMEJ_N = (288, 370, 310, 400)

_BUTTON_COLOR = (15, 329, 65, 354)
_BUTTON_DEPTH = (80, 329, 130, 354)

_BUTTON_SESSION = (13, 401, 134, 426)
_HOME_WARNING_TEXT = (140, 410)

_BUTTON_CONTROLLER = (160, 405, 325, 435)


def _contains(rect: Tuple[int, int, int, int], pt: Tuple[int, int]) -> bool:
  return rect[0] < pt[0] < rect[2] and rect[1] < pt[1] < rect[3]


def _bound(v: float, min_value: float, max_value: float) -> float:
  if v < min_value:
    return min_value
  if v > max_value:
    return max_value
  return v


class Button:
  """BUtton represents a clickable button within the pendant."""
  _text: str
  _active_text: str
  _rect: Tuple[int, int, int, int]
  _bg_color: Tuple[int, int, int]
  _text_color: Tuple[int, int, int]
  _active_color: Tuple[int, int, int]
  _active: bool
  _enabled: bool

  def __init__(self,
               text: str,
               rect: Tuple[int, int, int, int],
               bg_color: Tuple[int, int, int] = (128, 128, 128),
               text_color: Tuple[int, int, int] = (0, 0, 0),
               active_color: Tuple[int, int, int] = (128, 200, 128),
               active_text: Optional[str] = None,
               active: bool = False,
               enabled: bool = True) -> None:
    """Initialize the button.

    Args:
      text: The text for the button.
      rect: The button rectangle in (start x, start y, end x, end y) format.
      bg_color: The (red, green, blue) format color for the button background.
      text_color: The (red, green, blue) format color for the button text.
      active_color: The (red, green, blue) format color for active background.
      active_text: Text for active button, if None, inactive text will be used.
      active: Initial active state.
      enabled: Initial enabled state.
    """
    self._text = text
    self._active_text = text if active_text is None else active_text
    self._rect = rect
    self._bg_color = bg_color
    self._text_color = text_color
    self._active_color = active_color
    self._active = active
    self._enabled = enabled

  def set_text(self, text: str) -> None:
    """Set the text of the button.

    Args:
      text: the new button text.
    """
    self._text = text

  def hit(self, pt: Tuple[int, int]) -> bool:
    """Determine if the button is hit.

    Args:
      pt: The point to test in (x, y) format.

    Returns:
      True if point is within the button.
    """
    if _contains(self._rect, pt):
      return True
    else:
      return False

  @property
  def enabled(self) -> bool:
    """Returns true if the button is enabled."""
    return self._enabled

  @property
  def active(self) -> bool:
    """Returns true if the button is active."""
    return self._active

  def set_enabled(self, enabled: bool) -> None:
    """Set if the button is enabled.

    Args:
      enabled: If true, the button will be enabled.
    """
    self._enabled = enabled

  def set_active(self, active: bool) -> None:
    """Set if the button is active.

    Args:
      active: If true, the button will be active.
    """
    self._active = active

  def draw(self, img: np.ndarray) -> None:
    """Draw draws the button.

    Args:
      img: the image to draw the button upon.
    """
    text = self._active_text if self._active else self._text
    if self._active and self._enabled:
      cv2.rectangle(img, (self._rect[0], self._rect[1]),
                    (self._rect[2], self._rect[3]), self._active_color, -1)
    else:
      cv2.rectangle(img, (self._rect[0], self._rect[1]),
                    (self._rect[2], self._rect[3]), self._bg_color, -1)
    size = cv2.getTextSize(text, _TEXT_FONT, _TEXT_SIZE, _TEXT_THICKNESS)[0]
    cv2.putText(img, text,
                (int((self._rect[0] + self._rect[2]) / 2 - size[0] / 2),
                 int((self._rect[1] + self._rect[3]) / 2 + size[1] / 2)),
                _TEXT_FONT, _TEXT_SIZE, self._text_color, _TEXT_THICKNESS)


class Pendant(object):
  """Pendant for controlling a single robot."""
  _host: Host
  _device_name: str
  _window_name: str
  _bg_img: np.ndarray
  _active_axis: int
  _pos_step: float
  _rot_step: float
  _stop_button: Button
  _vacuum_button: Button
  _blowoff_button: Button
  _homej_button: Button
  _homej_y_button: Button
  _homej_n_button: Button
  _continuous_control_button: Button
  _color_button: Button
  _depth_button: Button
  _session_button: Button
  _controller_button: Button
  _target_pose: Optional[np.ndarray]
  _home_warning_active: bool
  _arm: Arm
  _vacuum: Optional[Vacuum]
  _controllers: Tuple[ArmControllerDescription, ...]
  _controller_name: str

  def __init__(self, device_name: str, bg_img: np.ndarray, host: Host,
               have_continuous_control: bool) -> None:
    """Initialize the pendant.

    Args:
      device_name: The device name for the robot.
      bg_img: The background pendant image.
      host: The PyReach host for the pendant.
      have_continuous_control: If true, can enable continuous control.

    Raises:
      core.PyReachError when an initialization error occurs.
    """
    self._host = host
    self._device_name = device_name
    self._window_name = f"pendant {self._device_name}"
    self._bg_img = bg_img
    # used when adjusting a single axis at a time with controller such as
    # shuttlexpress
    self._active_axis = -1
    self._pos_step = _POSITION_STEP_DEFAULT
    self._rot_step = _ROTATION_STEP_DEFAULT
    cv2.namedWindow(self._window_name)
    cv2.setMouseCallback(self._window_name, self._on_mouse)

    if device_name not in host.arms:
      raise PyReachError(
          f"Can't find robot '{device_name}' in the config, the following "
          f"options are available: {list(host.arms.keys())}, that can usually "
          "be changed by providing --robot_id=<robot-name>")
    self._arm = host.arms[device_name]
    self._vacuum = host.vacuums.get(device_name)
    controllers = self._arm.supported_controllers
    if controllers is None:
      print("Warning failed to load controllers")
      self._controllers = ()
    else:
      self._controllers = controllers
    self._controller_name = ""
    self._arm.start_streaming(0.1)
    if self._arm.fetch_state(timeout=2.0) is None:
      print(
          f"Did not receive state from robot '{device_name}' within two seconds."
      )
    if self._arm.fetch_state(timeout=2.0) is None:
      print(
          f"Did not receive state from robot '{device_name}' within two seconds."
      )

    urdf = self._arm.arm_type.urdf_file
    is_xarm = "XArm6.urdf" in urdf

    self._stop_button = Button("Stop", _BUTTON_STOP, active_color=(0, 0, 220))
    self._vacuum_button = Button(
        "Vacuum", _BUTTON_VACUUM, enabled=(self._vacuum is not None))
    self._blowoff_button = Button(
        "Blowoff",
        _BUTTON_BLOWOFF,
        enabled=(self._vacuum is not None and self._vacuum.support_blowoff))
    self._homej_button = Button(
        "HomeJ",
        _BUTTON_HOMEJ,
        enabled=is_xarm,
        active=is_xarm,
        active_color=(0, 0, 220))
    self._homej_y_button = Button(
        "Y", _BUTTON_HOMEJ_Y, enabled=False, active=False, bg_color=(0, 0, 220))
    self._homej_n_button = Button(
        "N", _BUTTON_HOMEJ_N, enabled=False, active=False, bg_color=(220, 0, 0))
    self._continuous_control_button = Button(
        "ContCtl",
        _BUTTON_CONTINUOUS,
        enabled=is_xarm and have_continuous_control)
    self._color_button = Button("Color", _BUTTON_COLOR)
    self._depth_button = Button("Depth", _BUTTON_DEPTH)
    self._session_button = Button(
        "Take Control", _BUTTON_SESSION, active_text="Release Control")
    self._controller_button = Button("Controller:", _BUTTON_CONTROLLER)
    self._target_pose = None

    self._home_warning_active = False

    print(f"Connecting Robot name '{device_name}'")

  @property
  def device_name(self) -> str:
    return self._device_name

  def on_continuous_control(self, transform: Optional[np.ndarray],
                            toggle_vacuum: bool) -> None:
    """Called when a continuous control update is generated.

    Args:
      transform: the transform to move the arm by.
      toggle_vacuum: if true, toggle the vacuum state.
    """
    if not self._continuous_control_button.active:
      return

    if toggle_vacuum and self._vacuum:
      vacuum_state = self._vacuum.state
      if vacuum_state is not None:
        if vacuum_state.state:
          self._vacuum.async_off()
        else:
          self._vacuum.async_on()

    state = self._arm.state()
    if state is None:
      return

    if state.joint_angles is None:
      return

    if self._target_pose is None:
      self._target_pose = np.array(state.pose.as_list())

    if transform is not None:
      rot = np.zeros(6, dtype=np.dtype(float))
      rot[3:] = self._target_pose[3:]
      self._target_pose[3:] = transform[3:]
      self._target_pose = transform_util.multiply_pose(self._target_pose, rot)
      self._target_pose[:3] += transform[:3]

    self._arm.async_to_pose(
        Pose.from_list(self._target_pose.tolist()),
        servo=True,
        allow_uncalibrated=True,
        controller_name=self._controller_name)

  def inc_pos_step(self) -> None:
    """Increment the value of the position step."""
    self._pos_step = _bound(self._pos_step * 2, _POSITION_STEP_MIN,
                            _POSITION_STEP_MAX)

  def dec_pos_step(self) -> None:
    """Decrement the value of the position step."""
    self._pos_step = _bound(self._pos_step / 2, _POSITION_STEP_MIN,
                            _POSITION_STEP_MAX)

  def inc_rot_step(self) -> None:
    """Increment the value of the rotation step."""
    self._rot_step = _bound(self._rot_step * 2, _ROTATION_STEP_MIN,
                            _ROTATION_STEP_MAX)

  def dec_rot_step(self) -> None:
    """Decrement the value of the rotation step."""
    self._rot_step = _bound(self._rot_step / 2, _ROTATION_STEP_MIN,
                            _ROTATION_STEP_MAX)

  def draw(self) -> Tuple[bool, bool]:
    """Draw the pendant.

    Returns:
      Tuple of (continuous_control_state, window_closed)
    """
    img = self._bg_img.copy()

    if self._vacuum:
      vacuum_state = self._vacuum.state
      self._vacuum_button.set_active(vacuum_state is not None and
                                     vacuum_state.state)
      blowoff_state = self._vacuum.blowoff_state
      self._blowoff_button.set_active(blowoff_state is not None and
                                      blowoff_state.state)

    state = self._arm.state()
    if state:
      x = 10
      y = _TEXT_Y

      pose = state.pose.as_list()
      color = (0, 0, 255) if self._active_axis == 0 else _COLOR_TEXT
      cv2.putText(img, "X:{:.3f}".format(pose[0]), (x, y), _TEXT_FONT,
                  _TEXT_SIZE, color, _TEXT_THICKNESS)
      y += _TEXT_YINC
      color = (0, 0, 255) if self._active_axis == 1 else _COLOR_TEXT
      cv2.putText(img, "Y:{:.3f}".format(pose[1]), (x, y), _TEXT_FONT,
                  _TEXT_SIZE, color, _TEXT_THICKNESS)
      y += _TEXT_YINC
      color = (0, 0, 255) if self._active_axis == 2 else _COLOR_TEXT
      cv2.putText(img, "Z:{:.3f}".format(pose[2]), (x, y), _TEXT_FONT,
                  _TEXT_SIZE, color, _TEXT_THICKNESS)
      y += _TEXT_YINC

      x = 95
      y = _TEXT_Y
      color = (0, 0, 255) if self._active_axis == 3 else _COLOR_TEXT
      cv2.putText(img, "Rx:{:.3f}".format(pose[3]), (x, y), _TEXT_FONT,
                  _TEXT_SIZE, color, _TEXT_THICKNESS)
      y += _TEXT_YINC
      color = (0, 0, 255) if self._active_axis == 4 else _COLOR_TEXT
      cv2.putText(img, "Ry:{:.3f}".format(pose[4]), (x, y), _TEXT_FONT,
                  _TEXT_SIZE, color, _TEXT_THICKNESS)
      y += _TEXT_YINC
      color = (0, 0, 255) if self._active_axis == 5 else _COLOR_TEXT
      cv2.putText(img, "Rz:{:.3f}".format(pose[5]), (x, y), _TEXT_FONT,
                  _TEXT_SIZE, color, _TEXT_THICKNESS)
      y += _TEXT_YINC

      x = 195
      y = _TEXT_Y
      ping_interval = self._host.get_ping_time()
      ping_interval_value = "Ping: ---"
      if ping_interval is not None:
        ping_interval_millis = int(ping_interval * 1000)
        ping_interval_value = f"Ping: {ping_interval_millis:3d} ms"
      cv2.putText(img, ping_interval_value, (x, y), _TEXT_FONT, _TEXT_SIZE,
                  _COLOR_TEXT, _TEXT_THICKNESS)

      y += _TEXT_YINC
      cv2.putText(img, f"PosStep: {self._pos_step:0.3f} ,/.", (x, y),
                  _TEXT_FONT, _TEXT_SIZE, _COLOR_TEXT, _TEXT_THICKNESS)
      y += _TEXT_YINC
      cv2.putText(img, f"RotStep: {self._rot_step:0.3f} [/]", (x, y),
                  _TEXT_FONT, _TEXT_SIZE, _COLOR_TEXT, _TEXT_THICKNESS)
      y += _TEXT_YINC
      cv2.putText(img, f"URDF: {self._arm.arm_type.urdf_file}", (x, y),
                  _TEXT_FONT, _TEXT_SIZE, _COLOR_TEXT, _TEXT_THICKNESS)

      x = 195
      y = 90
      text_joint_y_inc = 43

      joints = list(state.joint_angles)
      while len(joints) < 6:
        joints.append(0.0)

      cv2.putText(img, "Base:   {:.3f}".format(joints[0]), (x, y), _TEXT_FONT,
                  _TEXT_SIZE, _COLOR_TEXT, _TEXT_THICKNESS)
      y += text_joint_y_inc
      cv2.putText(img, "Shlder: {:.3f}".format(joints[1]), (x, y), _TEXT_FONT,
                  _TEXT_SIZE, _COLOR_TEXT, _TEXT_THICKNESS)
      y += text_joint_y_inc
      cv2.putText(img, "Elbow:  {:.3f}".format(joints[2]), (x, y), _TEXT_FONT,
                  _TEXT_SIZE, _COLOR_TEXT, _TEXT_THICKNESS)
      y += text_joint_y_inc
      cv2.putText(img, "Wrist1: {:.3f}".format(joints[3]), (x, y), _TEXT_FONT,
                  _TEXT_SIZE, _COLOR_TEXT, _TEXT_THICKNESS)
      y += text_joint_y_inc
      cv2.putText(img, "Wrist2: {:.3f}".format(joints[4]), (x, y), _TEXT_FONT,
                  _TEXT_SIZE, _COLOR_TEXT, _TEXT_THICKNESS)
      y += text_joint_y_inc
      cv2.putText(img, "Wrist3: {:.3f}".format(joints[5]), (x, y), _TEXT_FONT,
                  _TEXT_SIZE, _COLOR_TEXT, _TEXT_THICKNESS)
      y += text_joint_y_inc

    self._stop_button.set_active(True)
    self._stop_button.draw(img)
    self._vacuum_button.draw(img)
    self._blowoff_button.draw(img)
    self._continuous_control_button.draw(img)
    if not self._home_warning_active:
      self._homej_button.draw(img)
      self._controller_button.set_text("Controller: " + self._controller_name)
      self._controller_button.draw(img)
    else:
      self._homej_y_button.draw(img)
      self._homej_n_button.draw(img)
    self._color_button.set_active(True)
    self._color_button.draw(img)
    self._depth_button.set_active(True)
    self._depth_button.draw(img)
    session_state = self._host.get_session_state()
    self._session_button.set_enabled(session_state == SessionState.EVICTABLE or
                                     session_state == SessionState.INACTIVE or
                                     session_state == SessionState.ACTIVE)
    self._session_button.set_active(session_state == SessionState.ACTIVE)
    self._session_button.draw(img)

    if self._home_warning_active:
      cv2.putText(img, "The home action may be dangerous.", _HOME_WARNING_TEXT,
                  _TEXT_FONT, _TEXT_SIZE * 0.8, _COLOR_WARNING_TEXT,
                  _TEXT_THICKNESS)
      cv2.putText(img, "Click 'Y' to continue.",
                  (_HOME_WARNING_TEXT[0], _HOME_WARNING_TEXT[1] + 10),
                  _TEXT_FONT, _TEXT_SIZE * 0.8, _COLOR_WARNING_TEXT,
                  _TEXT_THICKNESS)
      cv2.putText(img, "Click 'N' to cancel.",
                  (_HOME_WARNING_TEXT[0], _HOME_WARNING_TEXT[1] + 20),
                  _TEXT_FONT, _TEXT_SIZE * 0.8, _COLOR_WARNING_TEXT,
                  _TEXT_THICKNESS)

    cv2.imshow(self._window_name, img)

    closed = cv2.getWindowProperty(self._window_name, cv2.WND_PROP_VISIBLE) == 0
    return self._continuous_control_button.active, closed

  def _command_callback(self, status: PyReachStatus) -> None:
    """Callback for PyReach commands.

    Args:
      status: the status of the command.
    """
    if status.is_error():
      print("Command:", status)

  def _command_finished_callback(self) -> None:
    pass

  def _move_home(self) -> None:
    """Moves the robot to the Home position."""
    if self._homej_button.enabled:
      self._continuous_control_button.set_active(False)
      self._homej_button.set_active(True)
      self._arm.async_to_joints(
          _XARM_HOMEJ,
          velocity=_XARM_HOMEJ_VELOCITY,
          allow_uncalibrated=True,
          controller_name=self._controller_name,
          callback=self._command_callback,
          finished_callback=self._command_finished_callback)
      print(f"Homing... {self._arm.arm_type.urdf_file}")
    else:
      print(f"HomeJ not enabled for {self._arm.arm_type.urdf_file}")

  def _on_mouse(self, event: int, x: int, y: int, unused_flags: int,
                unused_param: Any) -> None:
    """Callback for mouse clicks from OpenCV.

    Args:
      event: The OpenCV event.
      x: The X position for the click.
      y: The X position for the click.
      unused_flags: The flags from OpenCV, unused.
      unused_param: Parameters from OpenCV, unused.
    """
    if event == cv2.EVENT_LBUTTONDOWN:
      if _DEBUG:
        print(x, y)
        return
      state = self._arm.state()
      if state is None:
        return
      joints = list(state.joint_angles)
      pose = state.pose

      if _contains(_BUTTON_ZP, (x, y)):
        self._continuous_control_button.set_active(False)
        self._arm.async_to_pose(
            Pose(
                Translation(pose.position.x, pose.position.y,
                            pose.position.z + self._pos_step),
                pose.orientation),
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)
      elif _contains(_BUTTON_ZN, (x, y)):
        self._continuous_control_button.set_active(False)
        self._arm.async_to_pose(
            Pose(
                Translation(pose.position.x, pose.position.y,
                            pose.position.z - self._pos_step),
                pose.orientation),
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)
      elif _contains(_BUTTON_YP, (x, y)):
        self._continuous_control_button.set_active(False)
        self._arm.async_to_pose(
            Pose(
                Translation(pose.position.x, pose.position.y + self._pos_step,
                            pose.position.z), pose.orientation),
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)
      elif _contains(_BUTTON_YN, (x, y)):
        self._continuous_control_button.set_active(False)
        self._arm.async_to_pose(
            Pose(
                Translation(pose.position.x, pose.position.y - self._pos_step,
                            pose.position.z), pose.orientation),
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)
      elif _contains(_BUTTON_XP, (x, y)):
        self._continuous_control_button.set_active(False)
        self._arm.async_to_pose(
            Pose(
                Translation(pose.position.x + self._pos_step, pose.position.y,
                            pose.position.z), pose.orientation),
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)
      elif _contains(_BUTTON_XN, (x, y)):
        self._continuous_control_button.set_active(False)
        self._arm.async_to_pose(
            Pose(
                Translation(pose.position.x - self._pos_step, pose.position.y,
                            pose.position.z), pose.orientation),
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)
      elif _contains(_BUTTON_RXP, (x, y)):
        self._continuous_control_button.set_active(False)
        self._arm.async_to_pose(
            Pose(
                pose.position,
                AxisAngle(pose.orientation.axis_angle.rx + self._rot_step,
                          pose.orientation.axis_angle.ry,
                          pose.orientation.axis_angle.rz)),
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)
      elif _contains(_BUTTON_RXN, (x, y)):
        self._continuous_control_button.set_active(False)
        self._arm.async_to_pose(
            Pose(
                pose.position,
                AxisAngle(pose.orientation.axis_angle.rx - self._rot_step,
                          pose.orientation.axis_angle.ry,
                          pose.orientation.axis_angle.rz)),
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)
      elif _contains(_BUTTON_RYP, (x, y)):
        self._continuous_control_button.set_active(False)
        self._arm.async_to_pose(
            Pose(
                pose.position,
                AxisAngle(pose.orientation.axis_angle.rx,
                          pose.orientation.axis_angle.ry + self._rot_step,
                          pose.orientation.axis_angle.rz)),
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)
      elif _contains(_BUTTON_RYN, (x, y)):
        self._continuous_control_button.set_active(False)
        self._arm.async_to_pose(
            Pose(
                pose.position,
                AxisAngle(pose.orientation.axis_angle.rx,
                          pose.orientation.axis_angle.ry - self._rot_step,
                          pose.orientation.axis_angle.rz)),
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)
      elif _contains(_BUTTON_RZP, (x, y)):
        self._continuous_control_button.set_active(False)
        self._arm.async_to_pose(
            Pose(
                pose.position,
                AxisAngle(pose.orientation.axis_angle.rx,
                          pose.orientation.axis_angle.ry,
                          pose.orientation.axis_angle.rz + self._rot_step)),
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)
      elif _contains(_BUTTON_RZN, (x, y)):
        self._continuous_control_button.set_active(False)
        self._arm.async_to_pose(
            Pose(
                pose.position,
                AxisAngle(pose.orientation.axis_angle.rx,
                          pose.orientation.axis_angle.ry,
                          pose.orientation.axis_angle.rz - self._rot_step)),
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)

      # joint control
      elif _contains(_BUTTON_J0N, (x, y)):
        self._continuous_control_button.set_active(False)
        joints[0] -= self._rot_step
        self._arm.async_to_joints(
            joints,
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)

      elif _contains(_BUTTON_J0P, (x, y)):
        self._continuous_control_button.set_active(False)
        joints[0] += self._rot_step
        self._arm.async_to_joints(
            joints,
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)

      elif _contains(_BUTTON_J1N, (x, y)):
        self._continuous_control_button.set_active(False)
        joints[1] -= self._rot_step
        self._arm.async_to_joints(
            joints,
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)

      elif _contains(_BUTTON_J1P, (x, y)):
        self._continuous_control_button.set_active(False)
        joints[1] += self._rot_step
        self._arm.async_to_joints(
            joints,
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)

      elif _contains(_BUTTON_J2N, (x, y)):
        self._continuous_control_button.set_active(False)
        joints[2] -= self._rot_step
        self._arm.async_to_joints(
            joints,
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)

      elif _contains(_BUTTON_J2P, (x, y)):
        self._continuous_control_button.set_active(False)
        joints[2] += self._rot_step
        self._arm.async_to_joints(
            joints,
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)

      elif _contains(_BUTTON_J3N, (x, y)):
        self._continuous_control_button.set_active(False)
        joints[3] -= self._rot_step
        self._arm.async_to_joints(
            joints,
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)

      elif _contains(_BUTTON_J3P, (x, y)):
        self._continuous_control_button.set_active(False)
        joints[3] += self._rot_step
        self._arm.async_to_joints(
            joints,
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)

      elif _contains(_BUTTON_J4N, (x, y)):
        self._continuous_control_button.set_active(False)
        joints[4] -= self._rot_step
        self._arm.async_to_joints(
            joints,
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)

      elif _contains(_BUTTON_J4P, (x, y)):
        self._continuous_control_button.set_active(False)
        joints[4] += self._rot_step
        self._arm.async_to_joints(
            joints,
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)

      elif _contains(_BUTTON_J5N, (x, y)):
        self._continuous_control_button.set_active(False)
        joints[5] -= self._rot_step
        self._arm.async_to_joints(
            joints,
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)

      elif _contains(_BUTTON_J5P, (x, y)):
        self._continuous_control_button.set_active(False)
        joints[5] += self._rot_step
        self._arm.async_to_joints(
            joints,
            velocity=_RADIAL_VELOCITY_RAD_PER_SEC,
            acceleration=_RADIAL_ACCELERATION_RAD_PER_SEC2,
            allow_uncalibrated=True,
            controller_name=self._controller_name,
            callback=self._command_callback,
            finished_callback=self._command_finished_callback)

      if self._stop_button.hit((x, y)):
        self._continuous_control_button.set_active(False)
        print("stop")
        if self._arm:
          self._arm.stop(preemptive=True)

      if self._color_button.hit((x, y)):
        print("open color-camera")
        viewer_path = os.path.join(_DIR_PATH,
                                   "../../../scripts/async_viewer/main.py")
        subprocess.Popen(["python", viewer_path, "--cameras", "color-camera"])

      if self._depth_button.hit((x, y)):
        print("open depth camera")
        viewer_path = os.path.join(_DIR_PATH,
                                   "../../../scripts/async_viewer/main.py")
        subprocess.Popen(["python", viewer_path, "--cameras", "depth-camera"])

      if self._session_button.hit((x, y)):
        print("trigger session")
        self._host.set_should_take_control(not self._session_button.active,
                                           True)

      if self._vacuum_button.hit(
          (x, y)) and self._vacuum_button.enabled and self._vacuum:
        if not self._vacuum_button.active:
          self._vacuum.async_on(
              callback=self._command_callback,
              finished_callback=self._command_finished_callback)
        else:
          self._vacuum.async_off(
              callback=self._command_callback,
              finished_callback=self._command_finished_callback)

      if self._blowoff_button.hit(
          (x, y)) and self._blowoff_button.enabled and self._vacuum:
        if not self._blowoff_button.active:
          self._vacuum.async_blowoff(
              callback=self._command_callback,
              finished_callback=self._command_finished_callback)
        else:
          self._vacuum.async_off(
              callback=self._command_callback,
              finished_callback=self._command_finished_callback)

      if not self._home_warning_active:
        if self._homej_button.hit((x, y)):
          self._home_warning_active = True

          # Print warning to terminal in bold.
          print("\033[1m"
                "The Home action may be dangerous. "
                "Click Y to continue or click N to cancel."
                "\033[0m")
        if self._controller_button.hit((x, y)):
          if not self._controller_name:
            if self._controllers:
              self._controller_name = self._controllers[0].name
          else:
            idx = 0
            for ctl in self._controllers:
              if ctl.name == self._controller_name:
                break
              idx += 1
            idx += 1
            if idx >= len(self._controllers):
              self._controller_name = ""
            else:
              self._controller_name = self._controllers[idx].name
      else:
        if self._homej_y_button.hit((x, y)):
          self._home_warning_active = False
          self._move_home()

        if self._homej_n_button.hit((x, y)):
          print("Cancelled home action")
          self._home_warning_active = False

      if self._continuous_control_button.hit((x, y)):
        if not self._continuous_control_button.enabled:
          self._continuous_control_button.set_active(False)
          print("Continuous control input not enabled")
        else:
          self._continuous_control_button.set_active(
              not self._continuous_control_button.active)


def _clean_device_name(device_name: str) -> str:
  """Clean device name (remove an preceding : from name).

  Args:
    device_name: The name of the device.

  Returns:
    The device name.
  """
  pos = device_name.find(":")
  if pos < 0:
    return device_name
  return device_name[pos + 1:]


def run_pendants(device_names: List[str],
                 continuous_control: Optional[ContinuousControlThread] = None,
                 connection_string: str = "",
                 user_uid: Optional[str] = None) -> None:
  """Run a set of pendants.

  Args:
    device_names: The device_names for the robots.
    continuous_control: Function for the continuous control thread.
    connection_string: The PyReach connection string.
    user_uid: The user UID for the connection.
  """
  device_names = [
      _clean_device_name(device_name) for device_name in device_names
  ]
  should_exit_condition = threading.Condition()
  should_exit = False
  continuous_control_thread: Optional[threading.Thread] = None

  def wait(delay: float) -> bool:
    with should_exit_condition:
      should_exit_condition.wait(delay)
      return should_exit

  def set_exit() -> None:
    nonlocal should_exit
    with should_exit_condition:
      should_exit = True
      should_exit_condition.notify_all()

  with ConnectionFactory(
      enable_streaming=False,
      connection_string=connection_string,
      user_uid=user_uid).connect() as host:
    pendant_img_filename = os.path.join(_DIR_PATH, "pendant.jpg")
    bg_img = cv2.imread(pendant_img_filename)
    pendants = [
        Pendant(device_name, bg_img.copy(), host, continuous_control
                is not None) for device_name in device_names
    ]

    if continuous_control is not None:
      continuous_control_thread = threading.Thread(
          target=continuous_control,
          args=(pendants, wait, _CONTINUOUS_CONTROL_INTERVAL_DELAY_SECONDS))
      continuous_control_thread.start()

    while not host.is_closed() and not should_exit:
      continuous_control_enabled = False
      for pendant in pendants:
        pendant_continuous, window_closed = pendant.draw()
        if pendant_continuous:
          continuous_control_enabled = True
        if window_closed:
          set_exit()

      # if continuous control enabled, slow down GUI thread
      if continuous_control_enabled and not should_exit:
        c = cv2.waitKey(1000)
      elif not should_exit:
        c = cv2.waitKey(30)
      else:
        c = 0

      # needed for different UI toolkit installs
      if c > 0x100000:
        c -= 0x100000

      if c == ord(" "):
        print("stop")
        for device_name in device_names:
          if device_name in host.arms:
            host.arms[device_name].async_stop()
      elif c == ord(","):
        for pendant in pendants:
          pendant.dec_pos_step()
      elif c == ord("."):
        for pendant in pendants:
          pendant.inc_pos_step()
      elif c == ord("["):
        for pendant in pendants:
          pendant.dec_rot_step()
      elif c == ord("]"):
        for pendant in pendants:
          pendant.inc_rot_step()
      elif c == 27:
        break

  set_exit()
  if continuous_control_thread is not None:
    continuous_control_thread.join()
