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
from typing import Optional
from pyreach.snapshot import Snapshot


class Playback:
  """Playback is a playback object that manages playback of snapshots."""

  def next_snapshot(self) -> Optional[Snapshot]:
    """Get the next command-data snapshot."""
    raise NotImplementedError

  def seek_snapshot(self, gym_run_id: Optional[str], gym_episode: Optional[int],
                    gym_step: Optional[int]) -> Optional[Snapshot]:
    """Seek the oldest snapshot that matches the given criteria.

    Args:
      gym_run_id: The gym_run_id of the snapshot to seek.
      gym_episode: The gym_episode of the snapshot to seek.
      gym_step: The gym_step of the snapshot to seek.

    Returns:
      The snapshot, or None if there is no matching snapshot.
    """
    raise NotImplementedError

  def first_snapshot(self) -> Optional[Snapshot]:
    """Seek the first snapshot.

    Returns:
      The snapshot, or None if there is no matching snapshot.
    """
    return self.seek_snapshot(None, None, None)

  def replay_snapshot(self, snapshot: Snapshot) -> Snapshot:
    """Replay snapshot replays all device data from a snapshot.

    Args:
      snapshot: The snapshot to replay.

    Returns:
      The snapshot, with all of the snapshot responses loaded.
    """
    raise NotImplementedError
