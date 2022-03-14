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
"""Interface for logs playback in the PyReach Host API."""
from typing import Optional, Tuple
from pyreach import playback
from pyreach import snapshot


class PlaybackMock(playback.Playback):
  """Playback is a playback object that manages playback of snapshots."""

  _snapshots: Tuple[snapshot.Snapshot, ...]
  _current_index: int = 0

  def __init__(self, snapshots: Tuple[snapshot.Snapshot, ...] = ()) -> None:
    """Initialize PlaybackMock."""

    super().__init__()
    self._snapshots = snapshots
    self._current_index = -1

  def next_snapshot(self) -> Optional[snapshot.Snapshot]:
    """Get the next command-data snapshot."""
    self._current_index += 1
    snapshots: Tuple[snapshot.Snapshot, ...] = self._snapshots
    return (snapshots[self._current_index]
            if 0 <= self._current_index < len(snapshots) else None)

  def seek_snapshot(self, gym_run_id: Optional[str], gym_episode: Optional[int],
                    gym_step: Optional[int]) -> Optional[snapshot.Snapshot]:
    """Seek the oldest snapshot that matches the given criteria.

    Args:
      gym_run_id: The gym_run_id of the snapshot to seek.
      gym_episode: The gym_episode of the snapshot to seek.
      gym_step: The gym_step of the snapshot to seek.

    Returns:
      The snapshot, or None if there is no matching snapshot.
    """
    snap_shot: Optional[snapshot.Snapshot] = None
    index: int
    for index, snap_shot in enumerate(self._snapshots):
      match_run_id: bool = (
          gym_run_id is None or snap_shot.gym_run_id == gym_run_id)
      match_episode: bool = (
          gym_episode is None or snap_shot.gym_episode == gym_episode)
      match_step: bool = (gym_step is None or snap_shot.gym_step == gym_step)
      if match_run_id and match_episode and match_step:
        self._current_index = index
        break
    else:
      snap_shot = None
    return snap_shot

  def first_snapshot(self) -> Optional[snapshot.Snapshot]:
    """Seek the first snapshot.

    Returns:
      The snapshot, or None if there is no matching snapshot.
    """
    return self.seek_snapshot(None, None, None)

  def replay_snapshot(self, snap_shot: snapshot.Snapshot) -> snapshot.Snapshot:
    """Replay snapshot replays all device data from a snapshot.

    Args:
      snap_shot: The snapshot to replay.

    Returns:
      The snapshot, with all of the snapshot responses loaded.
    """
    raise NotImplementedError
