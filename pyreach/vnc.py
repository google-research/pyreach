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

"""Interface for interacting with VNC device."""

import enum
from typing import Optional, Callable
from pyreach import ColorCamera
from pyreach import core


class PointerEventType(enum.Enum):
  """Type of event for pointer events."""
  SEND_CLICK = "send-click"
  SEND_LEFT_MOUSE_DOWN = "send-left-mouse-down"
  SEND_LEFT_MOUSE_UP = "send-left-mouse-up"


class VNC(ColorCamera):
  """Interface for VNC."""

  def send_pointer_event(self, x: float, y: float,
                         event_type: PointerEventType,
                         timeout: float = 30) -> core.PyReachStatus:
    """Send a pointer event to the VNC device.

    Args:
      x: the x position of the mouse pointer.
      y: the y position of the mouse pointer.
      event_type: the type of pointer event.
      timeout: the timeout.

    Returns:
      The status message associated with the event.
    """
    raise NotImplementedError

  def async_send_pointer_event(
      self,
      x: float,
      y: float,
      event_type: PointerEventType,
      callback: Optional[Callable[[core.PyReachStatus], None]] = None,
      timeout: float = 30
  ) -> None:
    """Send a pointer event to the VNC device.

    Args:
      x: the x position of the mouse pointer.
      y: the y position of the mouse pointer.
      event_type: the type of pointer event.
      callback: optional callback for status from the command.
      timeout: the timeout.
    """
    raise NotImplementedError

  @property
  def pose(self) -> Optional[core.Pose]:
    """Pose is not meaningful for VNC."""
    raise NotImplementedError
