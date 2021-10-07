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

from typing import Dict, Tuple

import gym  # type: ignore

import pyreach
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
    observation_space: gym.spaces.Dict = gym.spaces.Dict({})

    super().__init__(reach_name, action_space, observation_space,
                     is_synchronous)
    self._active: bool = False
    self._action_id: int = 0

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
    observation: gyms_core.Observation = {}
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
    """
    with self._timers_select({"!agent*", "gym.text"}):
      action_dict: gyms_core.ActionDict = self._get_action_dict(action)
      if "action" in action_dict:
        action_request: bool = bool(int(action_dict["action"]))
        active: bool = self._active
        task_params: Dict[str, str] = self.get_task_params()
        changed: bool = True
        if action_request == task_element.ReachAction.START and not active:
          host.logger.start_task(task_params)
          self._active = True
          self._action_id += 1
          changed = True
        elif action_request == task_element.ReachAction.STOP and active:
          host.logger.end_task(task_params)
          self._active = False
          changed = True
        if changed:
          return (lib_snapshot.SnapshotGymLoggerAction("operator", "", False,
                                                       active, task_params),)
      return ()

  def start_observation(self, host: pyreach.Host) -> bool:
    """Start a synchronous observation."""
    return False

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
