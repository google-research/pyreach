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
"""Pendant displays a control pendant for a Reach workcell.

Run with:
  python3 pendant.py
"""
import time
from typing import Callable, Dict, List, Optional
from absl import app  # type: ignore
from absl import flags  # type: ignore
import numpy as np
from pyreach.common.base import transform_util
from pyreach.common.spacemouse import spacemouse_lib
from pyreach.tools.lib import pendant_lib

flags.DEFINE_multi_string("robot_id", None, "The robot id to connect to.")
flags.DEFINE_boolean("spacecat", False, "enable Space Cat user-space driver")
flags.DEFINE_string(
    "connection_string", "", "Connect using a PyReach connection string (see "
    "connection_string.md for examples and documentation).")
flags.DEFINE_string("user_uid", None, "Set user UID to connect with.")

_spacemouse_position_sensitivity = 0.00002
_spacemouse_rotation_sensitivity = 0.0001


def _spacecat_thread(pendants: List[pendant_lib.Pendant],
                     wait: Callable[[float], bool], delay: float) -> None:
  """Function called by the spacecat thread.

  Args:
    pendants: lists of pendent.
    wait:
    delay:
  """
  device_names = [pendant.device_name for pendant in pendants]
  device_names.sort()
  name_to_spacemouse: Dict[str, int] = {}
  if spacemouse_lib.rspnav_howmany() == 1 and len(device_names) == 1:
    name_to_spacemouse[device_names[0]] = 0
  else:
    print()
    print("There is more than one name or more than one mouse. We will now")
    print("let you assign a space mouse to each name.")
    while True:
      print()
      print("Assignments:")
      print()
      print("Index Name            Assignment")
      print("===== ==============  ==========")
      for i in range(len(device_names)):
        assignment = name_to_spacemouse[
            device_names[i]] if device_names[i] in name_to_spacemouse else None
        print(f"{i:5d} {device_names[i]:15s} {assignment}")
      print()
      index = input("Index to assign or just hit enter if done: ")
      if not index:
        break
      try:
        i = int(index)
        if i < 0 or i >= len(device_names):
          continue
        print()
        print(f"Assign '{device_names[i]}'. "
              f"Press any button on the mouse you want")
        print("to use to control it, or don't do anything for five seconds to")
        print("delete assignment.")
        spacemouse_lib.rspnav_remove_events(spacemouse_lib.RSPNAV_EVENT_MOTION)
        begin = time.time()
        assigned = None
        while assigned is None:
          event = spacemouse_lib.rspnav_poll_event()
          if event is None:
            if wait(0.001):
              return
          elif isinstance(event, spacemouse_lib.RSpnavButtonEvent):
            assigned = event.device
            break
          if time.time() - begin > 5:
            break
        if assigned is None:
          print("Deleting assignment")
          if device_names[i] in name_to_spacemouse:
            del name_to_spacemouse[device_names[i]]
        else:
          print(f"Assigning mouse {assigned} to '{device_names[i]}'")
          name_to_spacemouse[device_names[i]] = assigned
      except ValueError:
        pass

  # this removes events that were queued previously
  spacemouse_lib.rspnav_remove_events(spacemouse_lib.RSPNAV_EVENT_MOTION)

  while not wait(0.0):
    start_loop_time = time.time()
    event = spacemouse_lib.rspnav_poll_event()

    new_pose: Dict[int, np.ndarray] = {}
    tool_io: Dict[int, bool] = {}

    while True:
      event = spacemouse_lib.rspnav_poll_event()
      if event is None:
        break
      if isinstance(event, spacemouse_lib.RSpnavMotionEvent):
        transform = np.zeros(6, dtype=np.dtype(float))
        transform[0:3] = _spacemouse_position_sensitivity * np.array(
            [event.translation[0], event.translation[1], event.translation[2]])
        euler = (
            _spacemouse_rotation_sensitivity *
            np.array([event.rotation[0], event.rotation[1], event.rotation[2]]))
        transform[3:] = transform_util.euler_to_axis_angle(*euler)
        new_pose[event.device] = transform
      if isinstance(event, spacemouse_lib.RSpnavButtonEvent) and event.press:
        tool_io[event.device] = not tool_io.get(event.device, False)

    for pendant in pendants:
      if pendant.device_name in name_to_spacemouse:
        device = name_to_spacemouse[pendant.device_name]
        pendant.on_continuous_control(
            new_pose.get(device), tool_io.get(device, False))
      else:
        pendant.on_continuous_control(None, False)

    sleep_time = delay - (time.time() - start_loop_time)
    if sleep_time > 0:
      wait(sleep_time)
    else:
      print("Heads up: On this iteration, didn't hit targeted rate of ",
            1 / delay, "Hz")
      print("Missed it by (seconds):", -sleep_time)

  spacemouse_lib.rspnav_kill()


def _main(argv: List[str]) -> None:
  """Run the main for the pendant."""
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")

  continuous_control: Optional[pendant_lib.ContinuousControlThread] = None

  try:
    if flags.FLAGS.spacecat:
      spacemouse_lib.rspnav_open()
      time.sleep(1)
      if spacemouse_lib.rspnav_howmany() == 0:
        print()
        print("--spacecat specified, but no space mice found.")
        print()
      else:
        continuous_control = _spacecat_thread

    pendant_lib.run_pendants(
        flags.FLAGS.robot_id if flags.FLAGS.robot_id else [""],
        continuous_control, flags.FLAGS.connection_string, flags.FLAGS.user_uid)

  finally:
    spacemouse_lib.rspnav_kill()


if __name__ == "__main__":
  app.run(_main)
