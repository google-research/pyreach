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

"""Implementation of the playback API."""
import dataclasses
import logging
from typing import Optional

from pyreach.core import PyReachStatus
from pyreach.impl import client as cli
from pyreach.impl import reach_host
from pyreach.impl import utils
from pyreach.internal import InternalPlayback
from pyreach.playback import Playback
from pyreach.snapshot import Snapshot
from pyreach.snapshot import SnapshotResponse


class PlaybackDevice:
  """PlaybackDevice is a playback object that manages playback of data."""
  _internal: InternalPlayback
  _host: reach_host.ReachHost
  _client: cli.PlaybackClient

  def __init__(self, internal: InternalPlayback, host: reach_host.ReachHost,
               client: cli.Client) -> None:
    self._internal = internal
    self._host = host
    assert isinstance(client, cli.PlaybackClient)
    self._client = client

  def next_snapshot(self) -> Optional[Snapshot]:
    """Get the next command-data snapshot."""
    return self._client.next_snapshot()

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
    return self._client.seek_snapshot(gym_run_id, gym_episode, gym_step)

  def replay_snapshot(self, snapshot: Snapshot) -> Snapshot:
    """Replay snapshot replays all device data from a snapshot.

    Args:
      snapshot: The snapshot to replay.

    Returns:
      The snapshot, with all of the snapshot responses loaded.
    """
    for reference in sorted(
        snapshot.device_data_refs, key=lambda ref: (ref.time, ref.sequence)):
      self._internal.seek_device_data(reference.time, reference.sequence)
    responses = []
    for response in snapshot.responses:
      if not isinstance(response.reference, PyReachStatus):
        kv = dataclasses.asdict(response)
        data = self._internal.seek_device_data(response.reference.time,
                                               response.reference.sequence)
        if data is None:
          logging.warning("DeviceData missing for snapshot response: %s",
                          str(response))
          continue
        if data.status is None:
          logging.warning(
              "DeviceData has no status for snapshot response: %s: %s",
              str(response), str(data.to_json()))
          continue
        if data.device_type != "cmd-status":
          logging.warning(
              "DeviceData is not command status for snapshot response: %s: %s",
              str(snapshot), str(data.to_json()))
        kv["reference"] = utils.pyreach_status_from_message(data)
        response = SnapshotResponse(**kv)
      responses.append(response)
    kv = dataclasses.asdict(snapshot)
    kv["responses"] = tuple(responses)
    return Snapshot(**kv)


class PlaybackImpl(Playback):
  """PlaybackImpl is a playback object that manages playback of data."""
  _device: PlaybackDevice

  def __init__(self, internal: InternalPlayback, host: reach_host.ReachHost,
               client: cli.Client) -> None:
    self._device = PlaybackDevice(internal, host, client)

  def next_snapshot(self) -> Optional[Snapshot]:
    """Get the next command-data snapshot."""
    return self._device.next_snapshot()

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
    return self._device.seek_snapshot(gym_run_id, gym_episode, gym_step)

  def replay_snapshot(self, snapshot: Snapshot) -> Snapshot:
    """Replay snapshot replays all device data from a snapshot.

    Args:
      snapshot: The snapshot to replay.

    Returns:
      The snapshot, with all of the snapshot responses loaded.
    """
    return self._device.replay_snapshot(snapshot)
