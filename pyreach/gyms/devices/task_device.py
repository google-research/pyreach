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
"""Implementation of PyReach Gym Task Device."""

from typing import Callable, Dict, Optional, Tuple

import gym  # type: ignore

import pyreach
from pyreach import logger
from pyreach import snapshot as lib_snapshot
from pyreach.gyms import core as gyms_core
from pyreach.gyms import task_element
from pyreach.gyms.devices import reach_device


class ReachDeviceTask(reach_device.ReachDevice):
  """Represents some a task management device.

  Attributes:
    action_space: A Gym dictionary the following fields:
      "action": A Gym Discrete(3) that can contain the value of 0 (no change), 1
        (Start Task), or 2 (Stop Task).
  """

  def __init__(self, task_config: task_element.ReachTask) -> None:
    """Init a Text Instruction element.

    Args:
      task_config: The task configuration information.
    """
    reach_name: str = task_config.reach_name
    is_synchronous: bool = task_config.is_synchronous

    action_space: gym.spaces.Dict = gym.spaces.Dict({
        "action": gym.spaces.Discrete(3),
    })
    observation_space: gym.spaces.Dict = gym.spaces.Dict({
        "active": gym.spaces.MultiBinary(1),
    })

    super().__init__(reach_name, action_space, observation_space,
                     is_synchronous, {"action"})
    self._active: bool = False
    self._action_id: int = 0
    self._task_synchronize: Optional[Callable[[pyreach.Host], None]] = None

  def __str__(self) -> str:
    """Return string representation of Arm."""
    return f"ReachDeviceTask('{self.config_name}':'{self._reach_name}')"

  def get_observation(self,
                      host: pyreach.Host) -> reach_device.ObservationSnapshot:
    """Return the Reach Server Gym Observation as an empty Dict.

    Args:
      host: The host to get the observation from.

    Returns:
      Returns a Tuple containing the Gym Observation, a tuple of
      SnapshotReference objects and a tuple of SnapshotResponse objects.
      The actual observation is empty.

    Raises:
      pyreach.PyReachError when there is not observation available.

    """
    observation: gyms_core.Observation = {"active": (self._active,)}
    return observation, (), ()

  def do_action(
      self, action: gyms_core.Action,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Start/stop the action.

    Args:
      action: The Gym Action Space to process as a Gym Dict Space with a
        "action" field (0=no change, 1=Start, and 2=Stop).
      host: The reach host to use.

    Returns:
      The list of gym action snapshots.

    Raises:
      PyReachError if the task parameters are not pure strings.
    """
    with self._timers_select({"!agent*", "gym.text"}):
      action_dict: gyms_core.ActionDict = self._get_action_dict(action)
      if "action" in action_dict:
        action_request: int = int(action_dict["action"])
        active: bool = self._active
        task_params: Dict[str, str]
        try:
          task_params = self.get_task_params()
        except pyreach.PyReachError as reach_error:
          raise reach_error
        if self._task_synchronize is None:
          raise pyreach.PyReachError("Internal Error: no task synchronize")

        changed: bool = True
        if action_request == task_element.ReachAction.START and not active:
          host.logger.start_task(task_params)
          host.logger.wait_for_task_state(logger.TaskState.TASK_STARTED)
          self._task_synchronize(host)
          self._active = True
          self._action_id += 1
          changed = True
        elif action_request == task_element.ReachAction.STOP and active:
          self._task_synchronize(host)
          host.logger.end_task(task_params)
          host.logger.wait_for_task_state(logger.TaskState.TASK_ENDED)
          self._active = False
          changed = True
        if changed:
          return (lib_snapshot.SnapshotGymLoggerAction("operator", "", False,
                                                       active, task_params),)
      return ()

  def start_observation(self, host: pyreach.Host) -> bool:
    """Start a synchronous observation."""
    return False

  def set_task_synchronize(
      self, task_synchronize: Callable[[pyreach.Host], None]) -> None:
    """Set the global task synchronize function."""
    self._task_synchronize = task_synchronize

  def synchronize(self, host: pyreach.Host) -> None:
    """Synchronously update the task device."""
    pass  # The task device does not have state to synchronize.

  # pylint: disable=unused-argument
  def reset(self,
            host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Called when the gym is reset."""
    if self._active:
      task_params: Dict[str, str] = self.get_task_params()
      host.logger.end_task(task_params)
      self._active = False
      return (lib_snapshot.SnapshotGymLoggerAction("operator", "", False, False,
                                                   task_params),)
    return ()

  def validate(self, host: pyreach.Host) -> str:
    """Validate that task device is operable."""
    return ""  # Task device is always there.
