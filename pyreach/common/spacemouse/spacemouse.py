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

"""Spacemouse utility."""

import time
from typing import Sequence

from absl import app  # type: ignore

from pyreach.common.spacemouse import spacemouse_lib


def main(unused_args: Sequence[str]) -> None:
  spacemouse_lib.rspnav_open()
  time.sleep(0.5)
  spacemouse_lib.rspnav_remove_events(0)

  while True:
    event = spacemouse_lib.rspnav_wait_event()
    if event and isinstance(event, spacemouse_lib.RSpnavMotionEvent):
      print(
          f"MOTION {event.device}: x {event.translation[0]} y "
          f"{event.translation[1]} z {event.translation[2]} rx "
          f"{event.rotation[0]} ry {event.rotation[1]} rz {event.rotation[2]}")
    elif event and isinstance(event, spacemouse_lib.RSpnavButtonEvent):
      press = "released"
      if event.press:
        press = "pressed"
      print(f"BUTTON {event.device}: {event.bnum} {press}")


if __name__ == "__main__":
  try:
    app.run(main)
  finally:
    spacemouse_lib.rspnav_kill()
