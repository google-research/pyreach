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

"""Implementation of Open AI Gym interface for PyReach."""

import collections
import logging
import queue
import sys
import threading
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

import numpy as np  # type: ignore

import pyreach
from pyreach import internal
from pyreach import snapshot as lib_snapshot
from pyreach.gyms import core as gyms_core

Callback = Callable[[Any], bool]
FinishedCallback = Optional[Callable[[], None]]
Stop = Callable[[], None]
AddUpdateCallback = Callable[[Callback, FinishedCallback], Stop]
ObservationSnapshot = Tuple[gyms_core.Observation,
                            Tuple[lib_snapshot.SnapshotReference, ...],
                            Tuple[lib_snapshot.SnapshotResponse, ...]]


class ReachDevice(object):
  """Base class for all Reach Gym devices."""

  def __init__(self, reach_name: str, action_space: gyms_core.Space,
               observation_space: gyms_core.Space,
               is_synchronous: bool) -> None:
    """Initialize a Reach Element base class.

    Args:
      reach_name: The name of the corresponding device on the Reach server.
        Sometimes this name is empty.
      action_space: The Gym action space to use.
      observation_space: The Gym observation space to use.
      is_synchronous: If True, the next Gym observation will synchronize all
        observations elements that have this flag set otherwise the next
        observation is asynchronous.  This argument is optional and defaults to
        False.
    """
    self._reach_name: str = reach_name
    self._action_space: gyms_core.Space = action_space
    self._observation_space: Optional[gyms_core.Space] = observation_space
    self._config_name: str = ""  # Filled in during registration (never empty)
    self._is_synchronous: bool = is_synchronous
    self._reach_synchronous: Optional[ReachDeviceSynchronous] = None
    self._timers: internal.Timers = internal.Timers(set())
    self._task_params: Dict[str, str] = {}

  @property
  def action_space(self) -> gyms_core.Space:
    """Get the action space."""
    return self._action_space

  @property
  def observation_space(self) -> gyms_core.Space:
    """Get the observation space."""
    return self._observation_space

  @property
  def config_name(self) -> str:
    """Get the configuration name."""
    return self._config_name

  @property
  def is_synchronous(self) -> bool:
    """Get the synchronous flag."""
    return self._is_synchronous

  def _timers_select(self, timer_names: Set[str]) -> internal.TimersSet:
    """Select timers to enable/disable for a block of code.

    Args:
      timer_names: A set of timer name strings.  (Must be a Python set).

    Returns:
      Returns the CounterTimerSet for selected timers.

    """
    timers: Optional[internal.Timers] = self._timers
    if not timers:
      raise pyreach.PyReachError(
          f"No performance timers for Reach Element {self._reach_name} found.")
    return timers.select(timer_names)

  def _add_update_callback(self,
                           add_update_callback: AddUpdateCallback) -> None:
    """Cause and update callback to occur.

    Args:
      add_update_callback: A function in the standard `add_updata_callback` form
        from the PyReach API.

    Raises:
      pyreach.PyReachError for internal errors only.

    """

    reach_synchronous: Optional[ReachDeviceSynchronous] = (
        self._reach_synchronous)
    if reach_synchronous is None:
      raise pyreach.PyReachError(
          "Internal Error: No ReachDeviceSynchronous object")
    reach_synchronous.add_update_callback(add_update_callback, self)

  def set_task_synchronize(self, task_synchronize: Callable[[], None]) -> None:
    """Provide a global task synchronize function."""
    pass  # Most devices will ignore this.

  def do_action(
      self, action: gyms_core.Action,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Perform an action with the Element."""
    # Must be implemented in sub class.
    raise pyreach.PyReachError(
        "Internal Error: Unable to do '{0}' action.".format(self.config_name))

  # pylint: disable=unused-argument
  def reset(self,
            host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Called when the gym is reset."""
    return ()

  def get_observation(self, host: pyreach.Host) -> ObservationSnapshot:
    """Return the Reach element Gym observation."""
    # Must be implemented in sub class.
    raise pyreach.PyReachError(
        "Internal Error: Unable to get '{0}' observation".format(
            self.config_name))

  def reset_wait(self, host: pyreach.Host) -> None:
    """Wait for reset to complete."""
    # Sub-class this method to deal with waiting for reset to complete.
    pass

  def start_observation(self, host: pyreach.Host) -> bool:
    """Start a synchronous observation."""
    # Must be implemented in sub class.
    raise pyreach.PyReachError(
        "Internal Error: Unable to start '{0}' observation".format(
            self.config_name))

  def get_task_params(self) -> Dict[str, str]:
    """Get the environment task parameters."""
    key: str
    value: str
    for key, value in self._task_params.items():
      if not isinstance(key, str):
        raise pyreach.PyReachError("task_params dict has key that is not a str")
      if not isinstance(value, str):
        raise pyreach.PyReachError(
            f"task_params['{key}'] does not specify a str")
    return self._task_params

  def set_task_params(self, task_params: Dict[str, str]) -> None:
    """Store the environment task parameters."""
    self._task_params = task_params

  def set_reach_synchronous(
      self, reach_synchronous: "ReachDeviceSynchronous") -> None:
    """Set the ReachDeviceSynchronous for the Reach Element."""
    self._reach_synchronous = reach_synchronous

  def _get_action_dict(self, action: Any) -> gyms_core.ActionDict:
    """Verify that an action dictionary is a valid (or fail)."""
    if isinstance(action, (dict, collections.OrderedDict)):
      return action
    raise pyreach.PyReachError(
        "Action {0} is neither a Dict nor an collections.OrderedDict".format(
            action))

  def set_timers(self, timers: internal.Timers) -> None:
    """Set the reach environment."""
    self._timers = timers

  def synchronize(self) -> None:
    """Force the device synchronize its observations."""
    raise NotImplementedError(f"Device {self._reach_name}; no synchronize()")

  def _reshape_image(self, old_image: np.ndarray,
                     new_shape: Tuple[int, ...]) -> np.ndarray:
    """Return a reshaped image.

    Args:
      old_image: The image to reshape.
      new_shape: The new shape of the image.

    Returns:
      Return a cropped image that is padded with zeros.

    """
    if old_image.shape == new_shape:
      return old_image

    dimensions: int = len(old_image.shape)
    assert len(new_shape) == dimensions
    assert 2 <= dimensions <= 3

    index: int
    old_shape: Tuple[int, ...] = old_image.shape
    overlap_shape: Tuple[int, ...] = tuple([
        min(old_shape[index], new_shape[index]) for index in range(dimensions)
    ])

    reshaped_image: np.ndarray = np.zeros(new_shape, dtype=old_image.dtype)
    dx: int = overlap_shape[0]
    dy: int = overlap_shape[1]
    if dimensions == 2:
      reshaped_image[:dx, :dy] = old_image[:dx, :dy]
    else:
      dz: int = overlap_shape[2]
      reshaped_image[:dx, :dy, :dz] = old_image[:dx, :dy, :dz]
    return reshaped_image

  def validate(self, host: pyreach.Host) -> str:
    """Validate that device is operable."""
    raise pyreach.PyReachError(
        f"validate(): not implemented for {self.__class__.__name__}")


class ReachDeviceSynchronous(object):
  """A class to synchronous observations from ReachDevice's."""

  def __init__(self,
               host: pyreach.Host,
               timers: internal.Timers,
               timeout: Optional[float] = 15.0) -> None:
    """Init the Reach Synchronous object."""
    self._add_update_callbacks: Dict[str, AddUpdateCallback] = {}
    self.elements: Dict[str, ReachDevice] = {}
    self._host: pyreach.Host = host
    self._lock: threading.Lock = threading.Lock()
    self._pending_actions: Set[str] = set()
    self._q: queue.Queue[str] = queue.Queue()
    self._stops: Dict[str, Callable[[], None]] = {}
    self._timeout: Optional[float] = timeout
    self._timers: internal.Timers = timers

  def _register_element(self, element: ReachDevice) -> None:
    """Register a ReachDevice for synchronous observations.

    Args:
      element: The ReachDevice to register.
    """
    element.set_reach_synchronous(self)
    with self._lock:
      self.elements[element.config_name] = element

  def add_update_callback(self, add_update_callback: AddUpdateCallback,
                          element: ReachDevice) -> None:
    """Add an update callback for an element.

    Args:
      add_update_callback: A standard PyReach method that registers a couple of
        callback routines when the update shows up. This function always returns
        a function that can be called at any time to shut down any callback
        requests.
      element: Target element.
    """
    with self._lock:
      config_name: str = element.config_name
      if config_name not in self._add_update_callbacks:
        self._add_update_callbacks[config_name] = add_update_callback
      self._register_stop(element)

  def _register_stop(self, element: ReachDevice) -> None:
    """Register a stop assuming the lock is held."""
    config_name: str = element.config_name
    if config_name not in self._add_update_callbacks:
      raise pyreach.PyReachError(
          "Internal error: no add_update_callback found '{0}'".format(
              config_name))
    if config_name in self._stops:
      raise pyreach.PyReachError(
          "Internal error: Duplicate callback '{0}'".format(config_name))

    add_update_callback: AddUpdateCallback = (
        self._add_update_callbacks[config_name])
    stop: Callable[[], None] = (
        add_update_callback(lambda msg: True, lambda: self._q.put(config_name)))

    self._stops[config_name] = stop
    if element.action_space:
      self._pending_actions.add(config_name)

  def synchronize_observations(
      self, observations: Dict[str, gyms_core.Observation]
  ) -> Tuple[float, List[lib_snapshot.SnapshotReference],
             List[lib_snapshot.SnapshotResponse]]:
    """Wait for the synchronized observations to complete.

    Args:
      observations: set of observations that need to be synced.

    Raises:
      pyreach.PyReachError for internal errors.

    Returns:
      The latest timestamp among all observations.
    """

    snapshot_references: Dict[str, Tuple[Tuple[lib_snapshot.SnapshotReference,
                                               ...],
                                         Tuple[lib_snapshot.SnapshotResponse,
                                               ...]]] = {}
    with self._timers.select({"!agent*", "gym.sync"}):

      def stops_clear() -> None:
        """Clear out the stops table."""
        # Done with the lock held.
        config_name: str
        stop: Callable[[], None]
        for config_name, stop in stops.items():
          stop()
          del stops[config_name]

      latest_ts: float = 0.0
      minimum_ts: float = 0.0
      with self._lock:
        elements: Dict[str, ReachDevice] = self.elements
        element: ReachDevice
        host: pyreach.Host = self._host
        pending_actions: Set[str] = self._pending_actions
        stops: Dict[str, Callable[[], None]] = self._stops
        stop: Callable[[], None]
        q: queue.Queue[str] = self._q
        config_name: str
        if pending_actions:
          minimum_ts = sys.float_info.max
        while stops:
          # Get the stop and clear it.
          try:
            config_name = q.get(block=True, timeout=self._timeout)
          except queue.Empty:
            stops_clear()
            raise pyreach.PyReachError(
                "Internal Error: Observation timeout: waiting for {0}".format(
                    list(stops.keys())))
          stop = stops[config_name]
          stop()
          del stops[config_name]

          # Get the observation timestamp:
          if config_name not in elements:
            raise pyreach.PyReachError(
                "Internal Error: '{0}' not found".format(config_name))
          element = elements[config_name]
          observation: gyms_core.Observation
          references: Tuple[lib_snapshot.SnapshotReference, ...]
          responses: Tuple[lib_snapshot.SnapshotResponse, ...]
          observation, references, responses = element.get_observation(host)
          if not isinstance(observation, dict):
            raise pyreach.PyReachError(
                "Internal Error: No observation dictionary")
          if "ts" not in observation:
            raise pyreach.PyReachError(
                "Internal Error: No timestamp for '{0}'".format(
                    element.config_name))
          observation_ts: float = observation["ts"]
          latest_ts = max(latest_ts, observation_ts)
          logging.debug(
              ">>>>>>>>>>>>>>>>Got message from '%s' message @ %f} "
              "Waiting for %s Pending Actions: %s", config_name, observation_ts,
              list(stops.keys()), pending_actions)
          observations[config_name] = observation
          snapshot_references[config_name] = references, responses

          if element.action_space:
            # Action and Observation:
            if minimum_ts >= sys.float_info.max:
              minimum_ts = observation_ts
            else:
              minimum_ts = max(minimum_ts, observation_ts)
            logging.debug(">>>>>>>>>>>>>>>>minimum_ts: %f", minimum_ts)
            pending_actions.discard(config_name)
          elif pending_actions or observation_ts < minimum_ts:
            # Observation only:
            logging.debug(">>>>>>>>>>>>>>>>Retrigger '%s'", config_name)
            self._register_stop(element)

        if stops:
          stops_clear()
          raise pyreach.PyReachError("Internal Error: "
                                     "Non-empty ReachSynchronize stops table")

        # Sometimes a synchronous request makes no sense, in which case
        # we need to back fill the missing ones:
        for element in elements.values():
          config_name = element.config_name
          if config_name not in observations:
            observation, references, responses = element.get_observation(host)
            observations[config_name] = observation
            snapshot_references[config_name] = (references, responses)

        observation_names: Set[str] = set(observations.keys())
        element_names: Set[str] = set(elements.keys())
        if observation_names != element_names:
          raise pyreach.PyReachError(
              "observation_names{0} != element_names{1}".format(
                  observation_names, element_names))

      list_references: List[lib_snapshot.SnapshotReference] = []
      list_responses: List[lib_snapshot.SnapshotResponse] = []
      for refs, resps in snapshot_references.values():
        list_references.extend(refs)
        list_responses.extend(resps)

      return latest_ts, list_references, list_responses

  def start_observations(self, host: pyreach.Host) -> None:
    """Start a synchronized observations.

    Args:
      host: The host to start the observation on.

    Raises:
      pyreach.PyReachError for internal errors.

    """
    with self._timers.select({"!agent*", "gym.sync"}):
      with self._lock:
        stops: Dict[str, Callable[[], Any]] = self._stops
        named_elements: List[Tuple[str, ReachDevice]] = (
            list(self.elements.items()))

      actions_started: int = 0
      observations_started: int = 0
      element: ReachDevice
      config_name: str
      for config_name, element in named_elements:
        if config_name in stops:
          raise pyreach.PyReachError(
              "Internal Error: Duplicate stop {0}".format(config_name))
        if element.start_observation(host):
          observations_started += 1
          if element.action_space:
            actions_started += 1


if __name__ == "__main__":
  pass
