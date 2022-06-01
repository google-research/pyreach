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
"""Process that reads spacemouse commands."""

import dataclasses
import json
import logging
from multiprocessing import connection as mpc
import time
from typing import Any, Dict, Optional

from pyreach.common.spacemouse import spacemouse_lib

_SPACEMOUSE_X_INDEX: int = 0
_SPACEMOUSE_Y_INDEX: int = 1
_SPACEMOUSE_Z_INDEX: int = 2
_SPACEMOUSE_ROLL_INDEX: int = 0
_SPACEMOUSE_PITCH_INDEX: int = 1
_SPACEMOUSE_YAW_INDEX: int = 2
_X_FLIP: int = 1
_Y_FLIP: int = 1
_ROLL_FLIP: int = 1


@dataclasses.dataclass
class CartesianDeltaPositionAction:
  """Simple structured data, mutable, for the action."""
  # The state of the virtual gripper.
  gripper_open: bool  # no default value

  # Change in x, y, z, roll, pitch, yaw.
  delta_x: float = 0.0
  delta_y: float = 0.0
  delta_z: float = 0.0
  delta_roll: float = 0.0
  delta_pitch: float = 0.0
  delta_yaw: float = 0.0
  # Whether a button was pressed.
  button_press: bool = False
  # If a button was pressed, which one.
  bnum: int = 0


class EncodeAction(json.JSONEncoder):
  """Encoder definition for data classes."""

  def default(self, o: Any) -> Dict[Any, Any]:
    return o.__dict__


class SpacemouseDriver:
  """Driver for the Spacemouse translating events to actions.

  If the button is pressed, and the driver isn't configured for gripper use,
  then the button controls coarse/fine movement.

  If the driver is configured for gripper use, then the button controls
  opening/closing of the gripper. The gripper starts in closed position.

  If this is started with an mp.Pipe, then we just send actions over the
  pipe as serialized CartesianDeltaPositionAction. Otherwise, actions are
  printed to stdout as JSON.
  """
  _spacemouse_device_id: Optional[int] = 0
  _coarse_translation_scale: float = 0.0
  _fine_translation_scale: float = 0.0
  _coarse_rotation_scale: float = 0.0
  _fine_rotation_scale: float = 0.0
  _gripper_cooldown_time: float = 0.0
  _fine_adjust_mode: bool = False
  _use_gripper: bool = False
  _two_dof_mode: bool = False
  _gripper_open: bool = False
  _dt: float = 0.1
  _pipe: Optional[mpc.Connection] = None

  def __init__(self,
               pipe: Optional[mpc.Connection] = None,
               spacemouse_id: Optional[int] = None,
               two_dof_mode: bool = False,
               scale_up: float = 4,
               use_gripper: bool = False,
               dt: float = 0.1) -> None:
    ## --------- spacemouse config --------

    # of course needs tuning, for sensitivty
    self._coarse_translation_scale = 0.000006 * scale_up
    self._fine_translation_scale = 0.000003 * scale_up

    self._coarse_rotation_scale = 0.00001 * scale_up
    self._fine_rotation_scale = 0.000005 * scale_up
    ## --------- spacemouse config --------

    self._spacemouse_device_id = spacemouse_id
    self._fine_adjust_mode = False
    self._use_gripper = use_gripper
    self._two_dof_mode = two_dof_mode
    self._gripper_cooldown_time = time.time()
    self._gripper_open = False
    self._dt = dt
    self._pipe = pipe

  def run(self) -> None:
    """Polls the spacemouse every dt seconds."""
    try:
      spacemouse_lib.rspnav_open()
      # this removes events that were queued previously
      spacemouse_lib.rspnav_remove_events(spacemouse_lib.RSPNAV_EVENT_MOTION)
      while not self._pipe or not self._pipe.poll():
        start_loop_time = time.time()

        event: Optional[spacemouse_lib.RSpnavEvent] = None
        while True:
          next_event = spacemouse_lib.rspnav_poll_event()
          if next_event is None:
            break
          event = next_event

        action = self._get_action(event)
        if self._pipe and action is not None:
          self._pipe.send(action)

        sleep_time = self._dt - (time.time() - start_loop_time)
        if sleep_time > 0:
          time.sleep(sleep_time)

      logging.debug("-+-+-+-+-+-+-+ spacemouse driver received end signal")
      # Clear the pipe
      if self._pipe:
        _ = self._pipe.recv()
    finally:
      spacemouse_lib.rspnav_kill()
      logging.debug("-+-+-+-+-+-+-+ spacemouse driver quitting")

  def _get_action(
      self, event: Optional[spacemouse_lib.RSpnavEvent]
  ) -> Optional[CartesianDeltaPositionAction]:
    """Returns the action corresponding to a spacemouse event.

    Args:
      event: The event received from the spacemouse

    Returns:
      A CartesianDeltaPositionAction corresponding to the spacemouse event, or
      None if there was no event.
    """
    if event is None or (self._spacemouse_device_id is not None and
                         event.device != self._spacemouse_device_id):
      return None

    if isinstance(event, spacemouse_lib.RSpnavMotionEvent):
      action = CartesianDeltaPositionAction(gripper_open=self._gripper_open)
      scale_down = (
          self._fine_translation_scale
          if self._fine_adjust_mode else self._coarse_translation_scale)
      rot_scale = (
          self._fine_rotation_scale
          if self._fine_adjust_mode else self._coarse_rotation_scale)

      action.delta_x = event.translation[
          _SPACEMOUSE_X_INDEX] * scale_down * _X_FLIP
      action.delta_y = event.translation[
          _SPACEMOUSE_Y_INDEX] * scale_down * _Y_FLIP
      if not self._two_dof_mode:
        action.delta_z = event.translation[_SPACEMOUSE_Z_INDEX] * scale_down

      if not self._two_dof_mode:
        action.delta_roll = event.rotation[
            _SPACEMOUSE_ROLL_INDEX] * rot_scale * _ROLL_FLIP
        action.delta_pitch = event.rotation[_SPACEMOUSE_PITCH_INDEX] * rot_scale
        action.delta_yaw = event.rotation[_SPACEMOUSE_YAW_INDEX] * rot_scale

      # this prevents events from building up, which feels like lag
      spacemouse_lib.rspnav_remove_events(spacemouse_lib.RSPNAV_EVENT_MOTION)

      return action

    if isinstance(event, spacemouse_lib.RSpnavButtonEvent):
      action = CartesianDeltaPositionAction(gripper_open=self._gripper_open)
      if time.time() - self._gripper_cooldown_time > 0.3:
        self._gripper_cooldown_time = time.time()

        if event.press and not self._use_gripper:
          self._fine_adjust_mode = not self._fine_adjust_mode
        self._gripper_open = not self._gripper_open

      action.gripper_open = self._gripper_open
      action.bnum = event.bnum
      action.button_press = event.press

      return action

    return None
