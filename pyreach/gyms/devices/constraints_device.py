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
"""Implementation of PyReach gym Constraints Device."""

import sys
from typing import Dict, Optional, Tuple

import gym  # type: ignore
import numpy as np

import pyreach
from pyreach import constraints
from pyreach import host as pyreach_host
from pyreach import snapshot as lib_snapshot
from pyreach.gyms import constraints_element
from pyreach.gyms import core as gyms_core
from pyreach.gyms.devices import reach_device


class ReachDeviceConstraints(reach_device.ReachDevice):
  """Represents some text instructions.

  Attributes:
    action_space: The actions space is empty.
    observation_space: The observation space consists of a top level gym
      dictionary with a nested "constraint" dictionaries below for each
      configured constraint.
  """

  def __init__(
      self, constraints_config: constraints_element.ReachConstraints) -> None:
    """Initialize a Constraints device.

    Arguments:
      constraints_config: The constraints configuration information.

    Raises:
      PyReachError when there is a configuration error.
    """
    reach_name: str = constraints_config.reach_name
    is_synchronous: bool = constraints_config.is_synchronous

    allowed_geometries: Tuple[str, ...] = ("box",)
    config_constraint: constraints_element.ReachConstraint
    constraints_dict: Dict[str, gym.Spaces.Dict] = {}
    for config_constraint in constraints_config.constraints:
      geometry: str = config_constraint.geometry
      if geometry not in allowed_geometries:
        raise pyreach.PyReachError(
            f"Constraint geometry '{geometry}' is one of {allowed_geometries}")

      constraints_dict[config_constraint.name] = gym.spaces.Dict({
          "pose":
              gym.spaces.Box(low=-sys.maxsize, high=sys.maxsize, shape=(6,)),
          geometry:
              gym.spaces.Box(low=-sys.maxsize, high=sys.maxsize, shape=(3,)),
      })

    self._constraints: Optional[constraints.Constraints] = None
    action_space: gym.spaces.Dict = gym.spaces.Dict({})
    observation_space: gym.spaces.Dict = gym.spaces.Dict(constraints_dict)
    super().__init__(reach_name, action_space, observation_space,
                     is_synchronous)

    # Initialize other values here:
    self._constraint: Optional[constraints.Constraints] = None
    self._every_step: bool = False
    self._counter: int = 0

  def __str__(self) -> str:
    """Return string representation of Arm."""
    return "ReachDeviceConstraints('{0}':'{1}')".format(self.config_name,
                                                        self._reach_name)

  def get_observation(self,
                      host: pyreach.Host) -> reach_device.ObservationSnapshot:
    """Return the Reach Server gym Observation as an empty Dict.

    Args:
      host: The host to get the observation from.

    Returns:
      Returns a Tuple containing the gym Observation, a tuple of
      SnapshotReference objects and a tuple of SnapshotResponse objects.
      The Constraints Observation is a dictionary containing a "ts",
      "counter" and "instruction" value.  The counter is incremented each
      time a new instruction is received.  The "instruction" value is a
      1024 byte null padded array with encoded text instructions in UTF-8
      format.

    Raises:
       pyreach.PyReachError when there is not observation available.

    """
    with self._timers_select({"!agent*", "gym.constraints"}):
      observation: gyms_core.Observation = {}
      assert isinstance(observation, dict)  # Needed for mypy

      interactable: constraints.Interactable
      for interactable in self._get_constraint(host).get_interactables():
        geometry: constraints.Geometry = interactable.geometry
        if isinstance(geometry, constraints.Box):
          observation[interactable.name] = {
              "pose": np.array(geometry.pose.as_tuple()),
              "box": np.array(geometry.scale.as_tuple()),
          }
        else:
          raise pyreach.PyReachError(
              f"Internal Error: {geometry} is not a Box.")

      counter: int = self._counter
      self._counter = counter + 1
      return observation, (), (lib_snapshot.SnapshotResponse(
          self._counter, "constraints", self.config_name,
          lib_snapshot.SnapshotReference(0.0, counter)),)

  def synchronize(self, host: pyreach.Host) -> None:
    """Synchronously fetch constraints."""
    pass  # Currently constraints don't change.

  def do_action(
      self, action: gyms_core.Action,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Start/stop the action.

    Args:
      action: The gym Action Space to process as a gym Dict Space with a
        "task_enable" field (0=End, 1=Start).
      host: The reach host to use.

    Returns:
        The list of gym action snapshots.
    """
    return ()

  def start_observation(self, host: pyreach.Host) -> bool:
    """Start a synchronous observation."""
    return False

  # pylint: disable=unused-argument
  def reset(self,
            host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Called when the gym is reset."""
    return ()

  def _get_constraint(self, host: pyreach.Host) -> constraints.Constraints:
    """Get the constraints.

    Arguments:
      host: The host to fetch the constraints from.

    Returns:
      Return the constraints.

    Raises:
      Raises pyreach.PyReachError for errors.
    """
    if self._constraint is None:
      config: Optional[pyreach_host.Config] = host.config
      if not config:
        raise pyreach.PyReachError(
            "Internal Error: There is no host.config configured for host.")
      constraint: Optional[constraints.Constraints]
      constraint = config.constraint
      if not constraint:
        raise pyreach.PyReachError(
            "Internal Error: There is are no configured constraints.")
      self._constraint = constraint
    return self._constraint

  def validate(self, host: pyreach.Host) -> str:
    """Validate that is straints is operable."""
    try:
      _ = self._get_constraint(host)
    except pyreach.PyReachError as pyreach_error:
      return str(pyreach_error)
    return ""
