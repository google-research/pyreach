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

"""Frame counter for display."""

import collections
import time

from typing import Deque

# At least this much time will be kept for fps.
_FPS_SECS = 3
# At least this many frames will be kept for fps.
_FPS_FRAMES = 10


class FrameCounter:
  """Count frames displayed within a window."""

  def __init__(self) -> None:
    """Initialize the frame counter."""
    self.frames = 0
    self._times: Deque[float] = collections.deque()

  def incr(self) -> None:
    """Increment upon a frame arriving."""
    self.frames += 1
    curtime = time.time()
    self._times.append(curtime)
    while (len(self._times) > _FPS_FRAMES and
           (curtime - self._times[0] > _FPS_SECS)):
      self._times.popleft()

  @property
  def fps(self) -> float:
    """Get the FPS of the frame counter.

    Returns:
      The frames per second as a float.
    """
    if len(self._times) <= 1:
      return 0
    fps = (len(self._times) - 1) / (self._times[-1] - self._times[0])
    return fps
