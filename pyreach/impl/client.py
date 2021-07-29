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

"""Client is the lowest level abstraction for interacting with a Reach Host.

A Reach host client consumes CommandData and produces a queue of DeviceData.
"""
import queue  # pylint: disable=unused-import
from typing import Callable, Optional

from pyreach.common.python import types_gen
from pyreach.snapshot import Snapshot


class Client:
  """Interface for interacting with a Reach host."""

  def get_queue(self) -> "queue.Queue[Optional[types_gen.DeviceData]]":
    """Get a queue of DeviceData from the Reach host.

    None is inserted to close the queue.
    """
    raise NotImplementedError

  def send_cmd(self, cmd: types_gen.CommandData) -> None:
    """Send a command to the Reach host."""
    raise NotImplementedError

  def close(self) -> None:
    """Close the connection to the Reach host."""
    raise NotImplementedError


class PlaybackClient(Client):
  """Client that supports playback of logged data."""

  def with_queue_lock(self, callback: Callable[[], None]) -> None:
    """Run the callback under the send lock, preventing queue.put().

    Args:
      callback: the callback function.
    """
    raise NotImplementedError

  def next_device_data(self) -> Optional[types_gen.DeviceData]:
    """Playback the next device-data object.

    Returns:
      Returns the DeviceData object loaded, if available.
    """
    raise NotImplementedError

  def device_data_available(self) -> bool:
    """Returns true if the client has additional device data."""
    raise NotImplementedError

  def seek_device_data(
      self, time: Optional[float],
      sequence: Optional[int]) -> Optional[types_gen.DeviceData]:
    """Seek the given device data and output it, if available.

    Args:
      time: the timestamp to seek. If sequence number is not specified, will not
        return any data from before the specified time.
      sequence: the sequence number to seek. If specified, the exact sequence
        number, or any data after it will be returned.

    Returns:
      Returns the DeviceData object loaded, if found.
    """
    raise NotImplementedError

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
