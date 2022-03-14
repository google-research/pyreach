# Copyright 2022 Google LLC
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
"""Tests for LoggerMock."""

from typing import Dict, List, Optional, Tuple
import unittest

from pyreach import playback
from pyreach import snapshot
from pyreach.mock import playback_mock


class TestPlaybackMock(unittest.TestCase):
  """Test the TestLogger."""

  def test_playback_types(self) -> None:
    """Test the MockVacuum."""
    mock_playback: playback_mock.PlaybackMock = playback_mock.PlaybackMock()
    assert isinstance(mock_playback, playback_mock.PlaybackMock)
    assert isinstance(mock_playback, playback.Playback)

  def test_playback_methods(self) -> None:
    """Test the MockVacuum."""
    mock_playback: playback_mock.PlaybackMock = playback_mock.PlaybackMock()
    assert isinstance(mock_playback, playback_mock.PlaybackMock)
    assert isinstance(mock_playback, playback.Playback)

    # Create some snapshots and stuff them into a mock_playback.
    source: str = "source"
    device_data_refs: Tuple[snapshot.SnapshotReference, ...] = ()
    responses: Tuple[snapshot.SnapshotResponse, ...] = ()
    actions: Tuple[snapshot.SnapshotGymAction, ...] = ()
    server_time: float = 1.0
    run_id: str
    snapshots_table: Dict[str, snapshot.Snapshot] = {}
    snapshots: List[snapshot.Snapshot] = []
    env_id: str = "Env"
    for run_id in ("Run0", "Run1", "Run2"):
      episode: int
      for episode in range(3):
        step: int
        for step in range(3):
          server_time += 1.0
          reward: float = float(step + 1)
          done: bool = step == 3
          key: str = f"{run_id}.{episode}.{step}"
          snap_shot: snapshot.Snapshot = snapshot.Snapshot(
              source, device_data_refs, responses, server_time, env_id, run_id,
              episode, step, reward, done, actions)
          snapshots.append(snap_shot)
          snapshots_table[key] = snap_shot
          server_time += 1.0
    mock_playback = playback_mock.PlaybackMock(tuple(snapshots))

    # Iterate through the snapshots:
    assert mock_playback.next_snapshot() is snapshots_table["Run0.0.0"]
    assert mock_playback.next_snapshot() is snapshots_table["Run0.0.1"]
    assert mock_playback.next_snapshot() is snapshots_table["Run0.0.2"]
    assert mock_playback.next_snapshot() is snapshots_table["Run0.1.0"]
    assert mock_playback.next_snapshot() is snapshots_table["Run0.1.1"]
    assert mock_playback.next_snapshot() is snapshots_table["Run0.1.2"]
    assert mock_playback.next_snapshot() is snapshots_table["Run0.2.0"]
    assert mock_playback.next_snapshot() is snapshots_table["Run0.2.1"]
    assert mock_playback.next_snapshot() is snapshots_table["Run0.2.2"]
    assert mock_playback.next_snapshot() is snapshots_table["Run1.0.0"]
    assert mock_playback.next_snapshot() is snapshots_table["Run1.0.1"]
    assert mock_playback.next_snapshot() is snapshots_table["Run1.0.2"]
    assert mock_playback.next_snapshot() is snapshots_table["Run1.1.0"]
    assert mock_playback.next_snapshot() is snapshots_table["Run1.1.1"]
    assert mock_playback.next_snapshot() is snapshots_table["Run1.1.2"]
    assert mock_playback.next_snapshot() is snapshots_table["Run1.2.0"]
    assert mock_playback.next_snapshot() is snapshots_table["Run1.2.1"]
    assert mock_playback.next_snapshot() is snapshots_table["Run1.2.2"]
    assert mock_playback.next_snapshot() is snapshots_table["Run2.0.0"]
    assert mock_playback.next_snapshot() is snapshots_table["Run2.0.1"]
    assert mock_playback.next_snapshot() is snapshots_table["Run2.0.2"]
    assert mock_playback.next_snapshot() is snapshots_table["Run2.1.0"]
    assert mock_playback.next_snapshot() is snapshots_table["Run2.1.1"]
    assert mock_playback.next_snapshot() is snapshots_table["Run2.1.2"]
    assert mock_playback.next_snapshot() is snapshots_table["Run2.2.0"]
    assert mock_playback.next_snapshot() is snapshots_table["Run2.2.1"]
    assert mock_playback.next_snapshot() is snapshots_table["Run2.2.2"]
    assert mock_playback.next_snapshot() is None

    # Do a seek.
    seek: Optional[snapshot.Snapshot] = (
        mock_playback.seek_snapshot("Run2", 2, None))
    assert seek is snapshots_table["Run2.2.0"], (seek,
                                                 snapshots_table["Run2.2.0"])


if __name__ == "__main__":
  unittest.main()
