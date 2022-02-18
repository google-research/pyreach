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

"""Implementation of PyReach Gym Vacuum Device."""

import sys
import threading
from typing import Any, Dict, List, Optional, Tuple

import gym  # type: ignore
import numpy as np  # type: ignore

import pyreach
from pyreach import snapshot as lib_snapshot
from pyreach import vacuum as pyreach_vacuum
from pyreach.gyms import core as gyms_core
from pyreach.gyms import vacuum_element
from pyreach.gyms.devices import reach_device


class ReachDeviceVacuum(reach_device.ReachDevice):
  """Represents a Reach Vacuum system."""

  def __init__(self, vacuum_config: vacuum_element.ReachVacuum) -> None:
    """Initialize a Vacuum actuator.

    Args:
      vacuum_config: The vacuum configuration information.
    """
    reach_name: str = vacuum_config.reach_name
    is_synchronous: bool = vacuum_config.is_synchronous
    blowoff_ignore: bool = vacuum_config.blowoff_ignore
    state_enable: bool = vacuum_config.state_enable
    detect_enable: bool = vacuum_config.vacuum_detect_enable
    gauge_enable: bool = vacuum_config.vacuum_gauge_enable

    # 0=>Vacuum off, 1=>Vacuum on, and 2=>Blow Off on.
    action_space: gym.spaces.Dict = gym.spaces.Dict({
        "state": gym.spaces.Discrete(3),
    })
    observation_space_config: Dict[str, gyms_core.Space] = {
        "ts": gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
        "state": gym.spaces.Discrete(3),
    }
    if detect_enable:
      observation_space_config["vacuum_detect"] = gym.spaces.Discrete(2)
    if gauge_enable:
      observation_space_config["vacuum_gauge"] = (
          gym.spaces.Box(low=-1.0, high=101325.0, shape=()))
    observation_space: gym.spaces.Dict = (
        gym.spaces.Dict(observation_space_config))

    super().__init__(reach_name, action_space, observation_space,
                     is_synchronous)
    self._vacuum: Optional[pyreach.Vacuum] = None
    self._blowoff_ignore: bool = blowoff_ignore
    self._state_enable: bool = state_enable
    self._detect_enable: bool = detect_enable
    self._gauge_enable: bool = gauge_enable
    self._state: int = vacuum_element.ReachVacuumState.OFF
    self._desired_state: int = vacuum_element.ReachVacuumState.OFF
    self._last_send_lock: threading.Lock = threading.Lock()
    self._last_send_count: int = 0
    self._last_send_state: Optional[int] = None

  def __str__(self) -> str:
    """Return string representation of Vacuum."""
    return "ReachVacuum('{0}':'{1}', {2})".format(self.config_name,
                                                  self._reach_name, self._state)

  def _get_vacuum(self, host: pyreach.Host) -> Optional[pyreach.Vacuum]:
    """Return the vacuum device."""
    if self._vacuum is None:
      with self._timers.select({"!agent*", "!gym*", "host.vacuum"}):
        if self._reach_name not in host.vacuums:
          vacuum_names: List[str] = list(host.vacuums.keys())
          raise pyreach.PyReachError("Vacuum '{0}' is not one of {1}".format(
              self._reach_name, vacuum_names))
        self._vacuum = host.vacuums[self._reach_name]
        self._vacuum.start_streaming()
        if self._vacuum.support_blowoff:
          self._vacuum.start_blowoff_streaming()
    return self._vacuum

  def validate(self, host: pyreach.Host) -> str:
    """Validate that vacuum is operable."""
    try:
      _ = self._get_vacuum(host)
    except pyreach.PyReachError as pyreach_error:
      return str(pyreach_error)
    return ""

  def get_observation(self,
                      host: pyreach.Host) -> reach_device.ObservationSnapshot:
    """Return the Reach Vacuum actuator Gym observation.

    Args:
      host: The reach host to use.

    Returns:
      Returns a Tuple containing the Gym Observation, a tuple of
      SnapshotReference objects and a tuple of SnapshotResponse objects.
      The next observation is a Gym Dict Space with "ts" and "state" values.

    """
    with self._timers_select({"!agent*", "gym.vacuum"}):
      is_synchronous: bool = self._is_synchronous

      vacuum: Optional[pyreach.Vacuum] = self._get_vacuum(host)
      if vacuum is None:
        raise pyreach.PyReachError("Vacuum is not set")

      ts: float = 0.0
      snapshots: List[lib_snapshot.SnapshotReference] = []

      state: int = self._desired_state
      state_enable: bool = self._state_enable
      if state_enable:
        vacuum_state: Optional[pyreach_vacuum.VacuumState] = ((
            vacuum.fetch_state() if is_synchronous else vacuum.state))
        if vacuum_state:
          ts = vacuum_state.time
          if vacuum_state.state:
            state = vacuum_element.ReachVacuumState.VACUUM
            snapshots.append(
                lib_snapshot.SnapshotReference(
                    time=vacuum_state.time, sequence=vacuum_state.sequence))

        if vacuum.support_blowoff:
          blowoff_state: Optional[pyreach_vacuum.BlowoffState] = ((
              vacuum.fetch_blowoff_state()
              if is_synchronous else vacuum.blowoff_state))
          if blowoff_state:
            ts = max(ts, blowoff_state.time)
            if blowoff_state.state:
              state = vacuum_element.ReachVacuumState.BLOWOFF
              snapshots.append(
                  lib_snapshot.SnapshotReference(
                      time=blowoff_state.time, sequence=blowoff_state.sequence))

      detect_state: int = 0
      detect_enable: bool = self._detect_enable
      if vacuum.support_pressure:
        vacuum_pressure: Optional[pyreach_vacuum.VacuumPressure] = ((
            vacuum.fetch_pressure_state()
            if is_synchronous else vacuum.pressure_state))
        if vacuum_pressure:
          ts = max(ts, vacuum_pressure.time)
          if vacuum_pressure.state:
            detect_state = 1
          snapshots.append(
              lib_snapshot.SnapshotReference(
                  time=vacuum_pressure.time, sequence=vacuum_pressure.sequence))

      gauge_state: float = -1.0
      gauge_enable: bool = self._gauge_enable
      if gauge_enable and vacuum.support_gauge:
        vacuum_gauge: Optional[pyreach_vacuum.VacuumGauge] = ((
            vacuum.fetch_gauge_state()
            if is_synchronous else vacuum.gauge_state))
        if vacuum_gauge:
          ts = max(ts, vacuum_gauge.time)
          gauge_state = vacuum_gauge.state
          snapshots.append(
              lib_snapshot.SnapshotReference(
                  time=vacuum_gauge.time, sequence=vacuum_gauge.sequence))

      self._state = state
      observation: gyms_core.Observation = {
          "ts": gyms_core.Timestamp.new(ts),
      }
      assert isinstance(observation, dict)
      if state_enable:
        observation["state"] = state
      if detect_enable:
        observation["vacuum_detect"] = detect_state
      if gauge_enable:
        observation["vacuum_gauge"] = np.array(gauge_state)
      return observation, tuple(snapshots), ()

  def synchronize(self, host: pyreach.Host) -> None:
    """Synchronously update the vacuum state."""
    vacuum: Optional[pyreach.Vacuum] = self._vacuum
    if vacuum is None:
      raise pyreach.PyReachError("Vacuum is not set")

    if self._state_enable:
      _ = vacuum.fetch_state()
      if vacuum.support_blowoff:
        _ = vacuum.fetch_blowoff_state()
    if vacuum.support_pressure:
      _ = vacuum.fetch_pressure_state()
    if self._gauge_enable:
      _ = vacuum.fetch_gauge_state()

  def do_action(
      self, action: gyms_core.Action,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Set/Clear the vacuum.

    Args:
      action: The Gym Action Space to process as a Gym Dict Space with a "state"
        field (0=Off, 1=Vacuum, 2=BlowOff).
      host: The reach host to use.

    Returns:
        The list of gym action snapshots.
    """

    with self._timers_select({"!agent*", "gym.vacuum"}):
      try:
        action_dict: gyms_core.ActionDict = self._get_action_dict(action)
      except pyreach.PyReachError as runtime_error:
        raise pyreach.PyReachError from runtime_error

      desired_state: int = 0
      if "state" in action_dict:
        requested_state: Any = action_dict["state"]
        if isinstance(requested_state, int) and 0 <= requested_state <= 2:
          desired_state = requested_state
      vacuum: Optional[pyreach.Vacuum] = self._vacuum
      if self._vacuum is None:
        raise pyreach.PyReachError("Internal error: Vacuum is not set")
      assert isinstance(vacuum, pyreach.Vacuum)
      last_send_state: Optional[int] = self._last_send_state
      if desired_state == self._state:
        pass  # Do not send requests if state is already set
      elif (last_send_state is not None and last_send_state == desired_state and
            not self._is_synchronous):
        pass  # Do not send requests for a given state if it is requested
      else:
        send_count = 0
        with self._last_send_lock:
          self._last_send_count += 1
          send_count = self._last_send_count
          self._last_send_state = desired_state

        def completed_callback() -> None:
          with self._last_send_lock:
            if self._last_send_count == send_count:
              self._last_send_state = None

        if desired_state == vacuum_element.ReachVacuumState.OFF:
          with self._timers_select({"!agent*", "!gym*", "host.vacuum"}):
            if self._is_synchronous:
              vacuum.off()
              completed_callback()
            else:
              vacuum.async_off(finished_callback=completed_callback)
        elif desired_state == vacuum_element.ReachVacuumState.VACUUM:
          with self._timers_select({"!agent*", "!gym*", "host.vacuum"}):
            if self._is_synchronous:
              vacuum.on()
              completed_callback()
            else:
              vacuum.async_on(finished_callback=completed_callback)
        elif desired_state == vacuum_element.ReachVacuumState.BLOWOFF:
          with self._timers_select({"!agent*", "!gym*", "host.vacuum"}):
            if not self._vacuum.support_blowoff:
              if not self._blowoff_ignore:
                raise pyreach.PyReachError(
                    "Blow off is not supported by this vacuum device.")
            else:
              if self._is_synchronous:
                vacuum.blowoff()
                completed_callback()
              else:
                vacuum.async_blowoff(finished_callback=completed_callback)
        else:
          raise pyreach.PyReachError(
              "Invalid Vacuum state request {0}".format(desired_state))
      self._desired_state = desired_state
      return (lib_snapshot.SnapshotGymVacuumAction(
          device_type="robot",
          device_name=vacuum.device_name,
          state=desired_state,
          synchronous=self._is_synchronous),)

  def start_observation(self, host: pyreach.Host) -> bool:
    """Start a synchronous observation."""
    return True
