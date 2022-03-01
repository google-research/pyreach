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

"""Implementation of PyReach Gym Text Instructions Device."""

import sys
from typing import List, Optional, Tuple

import gym  # type: ignore
import numpy as np

import pyreach
from pyreach import core
from pyreach import force_torque_sensor
from pyreach import snapshot as lib_snapshot
from pyreach.gyms import core as gyms_core
from pyreach.gyms import force_torque_sensor_element
from pyreach.gyms.devices import reach_device


class ReachDeviceForceTorqueSensor(reach_device.ReachDevice):
  """Represents a Reach Force Torque Sensor.

  A Reach force torque sensor that returns force and torque values.

  Attributes:
    observation_space: The Gym observation space for the Reach force torque
      sensor.  This consists of a Gym Dict Space with "force", "torque", and
      "ts" sub Spaces. This attribute is read-only.
    action_space: A Gym Dict Space that is empty.
  """

  def __init__(
      self, force_torque_sensor_config: force_torque_sensor_element
      .ReachForceTorqueSensor
  ) -> None:
    """Init a ReachDeviceForceTorqueSensor.

    Args:
      force_torque_sensor_config: The force torque sensor configuration.
    """
    reach_name: str = force_torque_sensor_config.reach_name
    is_synchronous: bool = force_torque_sensor_config.is_synchronous

    action_space: gym.spaces.Dict = gym.spaces.Dict({})
    observation_space: gym.spaces.Dict = gym.spaces.Dict({
        "force": gym.spaces.Box(low=0, high=sys.maxsize, shape=(3,)),
        "torque": gym.spaces.Box(low=0, high=sys.maxsize, shape=(3,)),
        "ts": gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
    })

    super().__init__(reach_name, action_space, observation_space,
                     is_synchronous, set())
    self._force_torque_sensor_state: Optional[
        force_torque_sensor.ForceTorqueSensorState] = None
    self._force_torque_sensor: Optional[
        force_torque_sensor.ForceTorqueSensor] = None

  def __str__(self) -> str:
    """Return a string representation of ReachForceToqueSensor."""
    return (
        f"ReachDeviceForceTorqueSensor({self.config_name}, {self._reach_name})")

  def _get_force_torque_sensor(self,
                               host: pyreach.Host) -> pyreach.ForceTorqueSensor:
    """Return the force torque sensor."""
    if self._force_torque_sensor is None:
      with self._timers_select({"!agent*", "!gym*", "arm.force_torque_sensor"}):
        if self._reach_name not in host.force_torque_sensors:
          force_torque_sensor_names: List[str] = list(
              host.force_torque_sensors.keys())
          raise pyreach.PyReachError(
              f"Force Torque Sensor '{self._reach_name}' "
              f"is not one of {force_torque_sensor_names}")
        self._force_torque_sensor = host.force_torque_sensors[self._reach_name]
        self._force_torque_sensor.start_streaming()
    return self._force_torque_sensor

  def validate(self, host: pyreach.Host) -> str:
    """Validate that force torque sensor is operable."""
    try:
      _ = self._get_force_torque_sensor(host)
    except pyreach.PyReachError as pyreach_error:
      return str(pyreach_error)
    return ""

  def get_observation(self,
                      host: pyreach.Host) -> reach_device.ObservationSnapshot:
    """Return the Reach Force Torque Sensor actuator Gym observation.

    Args:
      host: The reach host to use.

    Returns:
      Returns a Tuple containing the Gym Observation, a tuple of
      SnapshotReference objects and a tuple of SnapshotResponse objects.
      The observation is Gym Dict Space with "force", "torque" and "ts" values.

    """
    if self._force_torque_sensor is None:
      with self._timers_select({"!agent*", "!gym*", "arm.force_torque_sensor"}):
        if self._reach_name not in host.force_torque_sensors:
          force_torque_sensor_names: List[str] = list(
              host.force_torque_sensors.keys())
          raise pyreach.PyReachError(
              f"Force Torque Sensor '{self._reach_name}' "
              f"is not one of {force_torque_sensor_names}")
        self._force_torque_sensor = host.force_torque_sensors[self._reach_name]
        self._force_torque_sensor.start_streaming()

    with self._timers_select({"!agent*", "!gym*", "arm.force_torque_sensor"}):
      self._force_torque_sensor_state = (
          self._force_torque_sensor.fetch_state()
          if self._is_synchronous else self._force_torque_sensor.state)

    force: core.Force = (
        self._force_torque_sensor_state.force
        if self._force_torque_sensor_state else core.Force(0.0, 0.0, 0.0))
    torque: core.Torque = (
        self._force_torque_sensor_state.torque
        if self._force_torque_sensor_state else core.Torque(0.0, 0.0, 0.0))
    ts: float = (
        self._force_torque_sensor_state.time
        if self._force_torque_sensor_state else 0.0)
    sequence: int = (
        self._force_torque_sensor_state.sequence
        if self._force_torque_sensor_state else 0)
    observation: gyms_core.Observation = {
        "force": np.array([force.x, force.y, force.z], dtype=np.float_),
        "torque": np.array([torque.x, torque.y, torque.z], dtype=np.float_),
        "ts": gyms_core.Timestamp.new(ts),
    }
    snapshot_reference: Tuple[lib_snapshot.SnapshotReference, ...] = ()
    if sequence:
      snapshot_reference = (lib_snapshot.SnapshotReference(ts, sequence),)

    return observation, snapshot_reference, ()

  def synchronize(self, host: pyreach.Host) -> None:
    """Synchronously update the arm state."""
    if self._force_torque_sensor:
      self._force_torque_sensor.fetch_state()

  def do_action(
      self, action: gyms_core.Action,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Do any necessary work for force/torque sensor.

    Args:
      action: The action dictionary, ignored.
      host: Reach host.

    Returns:
        The list of gym action snapshots.
    """
    return ()

  def start_observation(self, host: pyreach.Host) -> bool:
    """Start a synchronous_observation."""
    return True
