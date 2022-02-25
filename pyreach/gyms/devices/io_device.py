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
"""Implementation of PyReach Gym I/O Device."""

import collections.abc as collections_abc
import copy
import sys
from typing import Any, cast, Dict, List, Set, Tuple, Optional, Union

import gym  # type: ignore

import pyreach
from pyreach import arm as pyreach_arm
from pyreach import core as pyreach_core
from pyreach import digital_output as pyreach_digital_output
from pyreach import snapshot as lib_snapshot
from pyreach.gyms import core as gyms_core
from pyreach.gyms import io_element
from pyreach.gyms.devices import reach_device

# Common type hits:
DigOutput = pyreach_digital_output.DigitalOutput
DigOutState = pyreach_digital_output.DigitalOutputState
DigOutPinState = pyreach_digital_output.DigitalOutputPinState
ImmutableDict = pyreach_core.ImmutableDictionary
ReachDigitalOutput = io_element.ReachIODigitalOutput


class ReachDeviceIO(reach_device.ReachDevice):
  """Represents a Reach Io system."""

  def __init__(self, io_config: io_element.ReachIO) -> None:
    """Initialize a Io actuator.

    Args:
      io_config: The io configuration information.
    """
    reach_name: str = io_config.reach_name
    is_synchronous: bool = io_config.is_synchronous
    digital_outputs_config: Dict[str, ReachDigitalOutput] = {}

    io_action_config: Dict[str, gym.spaces.Space] = {}
    io_observation_config: Dict[str, gym.spaces.Space] = {}
    # Eventually, there will be "digital_inputs", "analog_inputs"
    # and "analog_outputs" as well.
    if hasattr(io_config, "digital_outputs"):
      # Make private copy that will not be accidentally changed.
      digital_outputs_config = cast(Dict[str, ReachDigitalOutput],
                                    getattr(io_config, "digital_outputs"))
      if not isinstance(digital_outputs_config, dict):
        raise pyreach.PyReachError("digital_outputs config is not a dict")
      digital_outputs_config = copy.deepcopy(digital_outputs_config)
      self._digital_outputs_config = digital_outputs_config

      # Verify digital_outputs_config types since it easy to make a mistake.
      action_digital_outputs: Dict[str, gym.spaces.Discrete] = {}
      observation_digital_outputs: Dict[str, gym.spaces.Dict] = {}
      pin_name: str
      digital_output_config: ReachDigitalOutput
      for pin_name, digital_output_config in digital_outputs_config.items():
        if pin_name in action_digital_outputs:
          raise pyreach.PyReachError(f"'{pin_name}' is a duplicate")
        if not isinstance(pin_name, str):
          raise pyreach.PyReachError(f"{pin_name} is not a str")
        if not isinstance(digital_output_config, ReachDigitalOutput):
          raise pyreach.PyReachError(
              f"{digital_output_config} is not a ReachDigitalOutput")

        # Each action can be 0=>set 0, 1=>set 1, or 2=> no_change.
        action_digital_outputs[pin_name] = gym.spaces.Discrete(3)
        # Each observation is a time stamp and a single boolean value:
        observation_digital_outputs[pin_name] = gym.spaces.Dict({
            "state": gym.spaces.Discrete(2),
            "ts": gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
        })
      io_action_config["digital_outputs"] = (
          gym.spaces.Dict(action_digital_outputs))
      io_observation_config["digital_outputs"] = (
          gym.spaces.Dict(observation_digital_outputs))

    # Do the final configuration.
    action_space: gym.spaces.Dict = gym.spaces.Dict(io_action_config)
    observation_space: gym.spaces.Dict = (
        gym.spaces.Dict(io_observation_config))
    super().__init__(reach_name, action_space, observation_space,
                     is_synchronous)
    self._digital_outputs_table: Optional[Dict[str, Tuple[DigOutput,
                                                          str]]] = None
    self._all_digital_outputs: Tuple[DigOutput, ...] = ()

  def _get_digital_outputs_table(
      self, host: pyreach.Host) -> Dict[str, Tuple[DigOutput, str]]:
    """Return "gym_pin_name" => (DigitalOutput, "pin_name") table."""
    with self._timers_select({"!agent*", "gym.io"}):
      all_digital_outputs: Dict[int, DigOutput] = {}  # Key is id(DigOutput)
      if not self._digital_outputs_table:
        # Be paranoid building this table since it is really easy to make a
        # configuration error.  Give diagnostice error messages.
        gym_pin_name: str
        # ("arm", "capability", "pin")
        digital_outputs_table: Dict[str, Tuple[DigOutput, str]] = {}

        reach_digital_output: ReachDigitalOutput
        for gym_pin_name, reach_digital_output in (
            self._digital_outputs_config.items()):
          if not isinstance(reach_digital_output, ReachDigitalOutput):
            raise pyreach.PyReachError(
                f"{reach_digital_output} is not a ReachIODigitalOutput")
          arm_name: str = reach_digital_output.reach_name
          capability_type: str = reach_digital_output.capability_type
          pin_name: str = reach_digital_output.pin_name

          if arm_name not in host.arms:
            raise pyreach.PyReachError(
                f"Arm '{arm_name}' is not one of {tuple(host.arms.keys())}")
          arm: pyreach_arm.Arm = host.arms[arm_name]

          digital_outputs: ImmutableDict[
              ImmutableDict[DigOutput]] = arm.digital_outputs
          if capability_type not in digital_outputs:
            raise pyreach.PyReachError(
                f"Capability type: '{capability_type}' is not one of "
                f"{tuple(digital_outputs.keys())}")

          capabilities: ImmutableDict[DigOutput] = (
              digital_outputs[capability_type])
          if pin_name not in capabilities:
            raise pyreach.PyReachError(
                f"Pin name '{pin_name}' "
                f"is not one of {tuple(capabilities.keys())}")
          digital_output: DigOutput = capabilities[pin_name]
          all_digital_outputs[id(digital_output)] = digital_output
          # TODO(gramlich): Should this be conditioned on is_synchronous?
          digital_output.start_streaming()

          digital_outputs_table[gym_pin_name] = (digital_output, pin_name)

        self._digital_outputs_table = digital_outputs_table
        self._all_digital_outputs = tuple(all_digital_outputs.values())
      return self._digital_outputs_table

  def validate(self, host: pyreach.Host) -> str:
    """Validate that io is operable."""
    with self._timers_select({"!agent*", "gym.io"}):
      try:
        _ = self._get_digital_outputs_table(host)
      except pyreach.PyReachError as pyreach_error:
        return str(pyreach_error)
      return ""

  def get_observation(self,
                      host: pyreach.Host) -> reach_device.ObservationSnapshot:
    """Return the Reach Io actuator Gym observation.

    Args:
      host: The reach host to use.

    Returns:
      Returns a Tuple containing the Gym Observation, a tuple of
      SnapshotReference objects and a tuple of SnapshotResponse objects.
      The next observation is a Gym Dict Space with "ts" and "state" values.

    """
    snapshots: List[lib_snapshot.SnapshotReference] = []
    with self._timers_select({"!agent*", "gym.io"}):
      # Fetch the state for each digital output.
      observation: gyms_core.Observation = {}
      digital_outputs_table: Dict[str, Tuple[DigOutput, str]] = (
          self._get_digital_outputs_table(host))

      # Eventually, there will be "digital_inputs", "analog_inputs"
      # and "analog_outputs" as well.
      if digital_outputs_table:
        state: Optional[DigOutState]
        pin_state: DigOutPinState
        # Key: (id(digital_output), "pin_name")
        states: Dict[Tuple[int, str], Tuple[DigOutState, DigOutPinState]] = {}
        digital_output: DigOutput
        for digital_output in self._all_digital_outputs:
          if self.is_synchronous:
            state = digital_output.fetch_state()
          else:
            state = digital_output.state
          if state is None:
            raise pyreach.PyReachError(
                "No state available for "
                f"{digital_output.robot_name}.{digital_output.type}")
          assert isinstance(state, DigOutState), state
          for pin_state in state.pin_states:
            # The cast should not be needed, but mypy is complaining, so...
            states[(id(digital_output),
                    pin_state.name)] = (cast(DigOutState, state), pin_state)
          snapshots.append(
              lib_snapshot.SnapshotReference(
                  time=state.time, sequence=state.sequence))

        # Construct the observation.
        digital_outputs_config: Dict[str, ReachDigitalOutput] = (
            self._digital_outputs_config)
        gym_pin_name: str
        digital_outputs: Dict[str, Dict[str, Union[int, Any]]] = {}
        reach_digital_output: ReachDigitalOutput
        for gym_pin_name, reach_digital_output in (
            digital_outputs_config.items()):
          pin_name: str = reach_digital_output.pin_name
          digital_output, pin_name = digital_outputs_table[gym_pin_name]
          state, pin_state = states[(id(digital_output), pin_name)]
          state_value: Optional[bool] = pin_state.state
          if not isinstance(state_value, bool):
            raise pyreach.PyReachError(
                f"Pin {gym_pin_name}.{pin_name} has no value.")
          digital_outputs[gym_pin_name] = {
              "state": int(state_value),
              "ts": gyms_core.Timestamp.new(state.time),
          }
        assert isinstance(observation, dict), observation
        observation["digital_outputs"] = digital_outputs
      return observation, tuple(snapshots), ()

  def synchronize(self, host: pyreach.Host) -> None:
    """Synchronously update the io state."""
    digital_output: DigOutput
    for digital_output in self._all_digital_outputs:
      digital_output.fetch_state()

  def do_action(
      self, action: gyms_core.Action,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Set/Clear the io.

    Args:
      action: The Gym Action Space to process to process.  (See API document.)
      host: The reach host to use.

    Returns:
        The list of gym action snapshots.
    """

    with self._timers_select({"!agent*", "gym.io"}):
      try:
        action_dict: gyms_core.ActionDict = self._get_action_dict(action)
      except pyreach.PyReachError as runtime_error:
        raise pyreach.PyReachError from runtime_error
      acceptable_types: Set[str] = set(("digital_outputs",))
      actual_types: Set[str] = set(action_dict.keys())
      extra_types: Set[str] = actual_types - acceptable_types
      if extra_types:
        raise pyreach.PyReachError(
            f"{extra_types} do not match {acceptable_types}")

      snapshots: Tuple[lib_snapshot.SnapshotGymAction, ...] = ()
      allowed_io_types: Tuple[str, ...] = ("digital_outputs",)
      if not isinstance(action, collections_abc.Mapping):
        raise pyreach.PyReachError(f"{action} is not a dict")
      io_type: Any
      io_dict: Any
      for io_type, io_dict in action.items():
        if io_type not in allowed_io_types:
          raise pyreach.PyReachError(
              f"io type {io_type} device key is one of {allowed_io_types}")
        if not isinstance(io_dict, collections_abc.Mapping):
          raise pyreach.PyReachError(f"{io_type} value is not a dict")

        if "digital_outputs" in action:
          digital_outputs_dict: Any = action["digital_outputs"]
          if not isinstance(digital_outputs_dict, collections_abc.Mapping):
            raise pyreach.PyReachError("io.digital_outputs is not dict")
          snapshots += self._do_digital_outputs_action(digital_outputs_dict,
                                                       host)
      return snapshots

  def _do_digital_outputs_action(
      self, digital_outputs_action: collections_abc.Mapping,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Perform digital outputs action."""
    digital_outputs_table: Dict[str, Tuple[DigOutput, str]] = (
        self._get_digital_outputs_table(host))

    # Collect all pin operations on the same DigOutput together:
    # Use id(DigOutput) as the key for this table:
    Operation = Tuple[DigOutput, str, bool]  # (DigOutput, "pin", True/False)
    arm_operations: Dict[int, List[Operation]] = {}

    digital_output: DigOutput
    gym_pin_name: Any
    pin_value: Any
    pin_name: str
    if not isinstance(digital_outputs_action, collections_abc.Mapping):
      raise pyreach.PyReachError(
          f"action is not a dictionary: {digital_outputs_action}")
    for gym_pin_name, pin_value in digital_outputs_action.items():
      if gym_pin_name not in digital_outputs_table:
        raise pyreach.PyReachError(
            f"io.digital_io: {gym_pin_name} is not a one of "
            f"{tuple(digital_outputs_table.keys())}")
      if not isinstance(pin_value, int) and 0 <= pin_value <= 2:
        raise pyreach.PyReachError(f"io.digital_io.{gym_pin_name}:"
                                   f"{pin_value} is not int in range 0-2")

      if pin_value < 2:
        digital_output, pin_name = digital_outputs_table[gym_pin_name]
        if id(digital_output) not in arm_operations:
          arm_operations[id(digital_output)] = []
        arm_operations[id(digital_output)].append(
            (digital_output, pin_name, pin_value == 1))

    # Perform pin operations on a per digital output basis:
    operations: List[Tuple[DigOutput, str, bool]]
    for operations in arm_operations.values():
      if operations:
        value: bool
        states_list: List[Tuple[str, bool]] = []
        for operation in operations:
          digital_output, pin_name, value = operation
          states_list.append((pin_name, value))
          if self._is_synchronous:
            digital_output.set_pin_states(tuple(states_list))
          else:
            digital_output.async_set_pin_states(tuple(states_list))

    return ()

  def start_observation(self, host: pyreach.Host) -> bool:
    """Start a synchronous observation."""
    return True
