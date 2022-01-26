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

"""Implementation of PyReach Gym Server Device."""

import sys
from typing import Any, Dict, Tuple

import gym  # type: ignore

import pyreach
from pyreach import snapshot as lib_snapshot
from pyreach.gyms import core as gyms_core
from pyreach.gyms import server_element
from pyreach.gyms.devices import reach_device


class ReachDeviceServer(reach_device.ReachDevice):
  """Represents a Reach Server.

  Attributes:
    observation_space: A Gym Dict Space that specifies a "latest_ts" value and
      "server_ts" value. These attributes are read only.
  """

  def __init__(self, server_config: server_element.ReachServer) -> None:
    """Initialize a Reach Server.

    Args:
      server_config: The server configuration information.
    """
    reach_name: str = server_config.reach_name
    is_synchronous: bool = server_config.is_synchronous

    self._latest_ts: float = 0.0

    action_space: gym.spaces.Dict = gym.spaces.Dict({})
    observation_space: gym.spaces.Dict = gym.spaces.Dict({
        "latest_ts": gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
        "server_ts": gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
    })
    super().__init__(reach_name, action_space, observation_space,
                     is_synchronous)

  def __str__(self) -> str:
    """Return a string representation of ReachDeviceServer."""
    return "ReachDeviceServer('{0}':'{1}', latest_ts={2})".format(
        self.config_name, self._reach_name, self._latest_ts)

  def get_observation(self,
                      host: pyreach.Host) -> reach_device.ObservationSnapshot:
    """Return the Reach Server Gym Observation as Dict.

    Args:
      host: The host to get the observation from.

    Returns:
      Returns a Tuple containing the Gym Observation, a tuple of
      SnapshotReference objects and a tuple of SnapshotResponse objects.
      The observation is Dict with the "latest_ts" set.

    """
    # The latest timestamps are updated up in ReachDevice _get_observation().
    # Set to zero here so that it is bogus if the update does not happen.
    latest_ts: Any = gyms_core.Timestamp.new(0.0)
    server_ts: Any = gyms_core.Timestamp.new(0.0)
    server_observation: Dict[str, Any] = {
        "latest_ts": latest_ts,
        "server_ts": server_ts
    }
    return server_observation, (), ()

  def synchronize(self) -> None:
    """Synchronously the server."""
    pass

  def do_action(
      self, action: gyms_core.Action,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Do nothing for an action.

    Args:
      action: Gym action space to process.  Should be empty
      host: The pyreach.Host connect to.

    Returns:
        The list of gym action snapshots.
    """
    return ()

  def validate(self, host: pyreach.Host) -> str:
    """Validate that server device is operable."""
    return ""  # Pseudo device is always there.
