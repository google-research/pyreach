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

"""Benchmark environment for the T-Shirt Folding challenge."""

import collections
import enum
import re
import sys
import time
from typing import Any, Dict, Tuple, Optional

import numpy as np  # type: ignore

from pyreach.gyms import core
from pyreach.gyms import reach_env


def _log(msg: str) -> None:
  """Helper method to log with time."""
  sys.stderr.write(f"{time.time():.4f}:ENV: {msg}\n")


class _InternalState(enum.Enum):
  INACTIVE = 1
  SCRAMBLE_NOW = 2
  FOLD_NOW = 3


class BenchmarkFoldingEnv(reach_env.ReachEnv):
  """Benchmark environment for the T-Shirt Folding challenge.

  For more information on the benchmark challenge and evaluation protocol,
  see pyreach/gyms/g3doc/benchmark_folding_challenge.md.

  For more information on the Gym API and action/observation spaces,
  see pyreach/gyms/g3doc/gym_api.md.
  """

  SAFE_JOINT_ANGLES: np.ndarray = (
      np.array([1.369, -0.944, 1.666, -2.300, 4.675, -0.270]))
  CLEAR_FOV_JOINT_ANGLES: np.ndarray = (
      np.array([1.618, -1.444, 2.164, -2.403, 5.270, -0.259]))

  CENTER_GRAB_POSE = np.array([0.0, -0.6, -0.04, -0.308, -2.943, -0.035])
  CENTER_LIFT_POSE = CENTER_GRAB_POSE + [0, 0, 0.55, 0, 0, 0]

  MIN_JOINT_ANGLES = SAFE_JOINT_ANGLES - 5.0
  MAX_JOINT_ANGLES = SAFE_JOINT_ANGLES + 5.0

  MAX_JOINT_DEGREES_PER_SECOND = 80.0

  TSHIRT_TOSSING_CYCLES = 3
  TIMEOUT_PER_INSTRUCTION_SECONDS = 600.0

  def __init__(self, **kwargs: Any) -> None:
    self._internal_state = _InternalState.INACTIVE
    self._inactive_reason = ""  # Only valid if state is INACTIVE.
    self._timer_running: bool = False
    self.deadline: float = 0.0
    self.last_joint_move_observation: Optional[core.Observation] = None

    task_params: Dict[str, str] = {"task-code": "142"}
    pyreach_config: Dict[str, reach_env.ReachElement] = {
        "arm":
            reach_env.ReachArm(
                "",
                self.MIN_JOINT_ANGLES,
                self.MAX_JOINT_ANGLES,
                response_queue_length=1),
        "realsense0":
            reach_env.ReachColorCamera("realsense0", (360, 640)),
        "realsense1":
            reach_env.ReachColorCamera("realsense1", (360, 640)),
        "realsense2":
            reach_env.ReachColorCamera("realsense2", (360, 640)),
        "realsense3":
            reach_env.ReachColorCamera("realsense3", (360, 640)),
        "depth_camera":
            reach_env.ReachDepthCamera("", (360, 640), color_enabled=True),
        "server":
            reach_env.ReachServer("Server"),
        "vacuum":
            reach_env.ReachVacuum(""),
        "text_instructions":
            reach_env.ReachTextInstructions("instruction-generator"),
    }
    super().__init__(
        pyreach_config=pyreach_config, task_params=task_params, **kwargs)

  def _inactivate(self, reason: str) -> None:
    """Mark state as inactive, with a reason."""
    self._internal_state = _InternalState.INACTIVE
    self._inactive_reason = reason

  def _movej(self,
             joints: np.ndarray) -> Tuple[core.Observation, float, bool, Any]:
    action = {
        "arm": {
            "command": 1,
            "joint_angles": joints,
            "synchronous": 1,
            "velocity": 1.04,
            "acceleration": 1.2
        }
    }
    return super().step(action)

  def _movepose(self,
                pose: np.ndarray) -> Tuple[core.Observation, float, bool, Any]:
    action = {
        "arm": {
            "command": 2,
            "pose": pose,
            "synchronous": 1,
            "velocity": 1.04,
            "acceleration": 1.2
        }
    }
    return super().step(action)

  def _grab(self) -> Tuple[core.Observation, float, bool, Any]:
    action = {"vacuum": {"state": reach_env.ReachVacuumState.VACUUM}}
    return super().step(action)

  def _release(self) -> Tuple[core.Observation, float, bool, Any]:
    action = {"vacuum": {"state": reach_env.ReachVacuumState.OFF}}
    return super().step(action)

  def _end_instruction(self) -> Tuple[core.Observation, float, bool, Any]:
    # Move the robot arm clear of the camera and turn off vacuum
    self._stow_workcell()

    _log("Waiting 1 sec for workcell to settle and capture end of task image")

    # Give logs a chance to take a photo of workcell before ending task
    time.sleep(1)

    # End task
    action = collections.OrderedDict(
        {"text_instructions": collections.OrderedDict({"task_enable": 0})})
    super().step(action)

    # Move to a safe position before returning control
    return self._movej(self.SAFE_JOINT_ANGLES)

  def scramble(self) -> core.Observation:
    """Scramble the t-shirt with prescripted moves.

    An agent can use this instead of creating its own policy.
    The agent must still call scramble_done() even if it uses this method.

    This will cause the workcell to make three attempts to jumble the t-shirt
    randomly by grabbing at random points in the workspace. The arm will be
    returned to a safe joint position at the end of the jumble sequence.

    Returns:
      Observation after moving arm to safe joint position.
    """

    _log("Scrambling the t-shirt with scripted moves")

    # Move to a safe position
    obs, _, _, _ = self._movej(self.SAFE_JOINT_ANGLES)

    for i in range(1, self.TSHIRT_TOSSING_CYCLES + 1):
      # Toss t-shirt toward the center of the table
      _log(f"Tossing t-shirt {i} of {self.TSHIRT_TOSSING_CYCLES} times")
      offset = np.concatenate((np.random.rand(2,) * 0.2 - 0.1, np.zeros(4,)))

      self._movepose(self.CENTER_GRAB_POSE + offset)
      self._grab()
      time.sleep(0.1)

      self._movepose(self.CENTER_LIFT_POSE)
      self._release()
      time.sleep(0.25)

    # Move to a safe position before returning control
    obs, _, _, _ = self._movej(self.SAFE_JOINT_ANGLES)

    return obs

  def _stow_workcell(self) -> core.Observation:
    """Stow the workcell arm clear of the FOV of the camera.

    This will move the workcell arm to a safe joint position and turn off the
    vacuum gripper.

    Returns:
      Observation after moving arm to safe joint position.
    """

    _log("Stowing workcell arm and turning off vacuum gripper")

    obs, _, _, _ = self._release()
    obs, _, _, _ = self._movej(self.CLEAR_FOV_JOINT_ANGLES)

    return obs

  def _clamp_joint_velocity_limits(self, q_target: np.ndarray,
                                   obs: core.Observation) -> np.ndarray:
    """Clamp joint angles based on joint speed limits and last observed joints.

    The joint velocity is computed based on the timestamp and joint angles from
    the provided reference observation.

    The maximum joint velocity is self.MAX_JOINT_DEGREES_PER_SECOND.

    Args:
      q_target: Target joint angles.
      obs: Observation used as reference for prior state.

    Returns:
      q_clamp: Target joint angles clamped for joint velocities.

    """
    assert obs is not None
    assert isinstance(obs, (dict, collections.OrderedDict))

    try:
      q_obs = obs["arm"]["joint_angles"]
      ts_obs = obs["arm"]["ts"]
    except KeyError:
      raise KeyError("Unable to read joint_angles or timestamp in obs")

    q_delta = q_target - q_obs

    # Should we use fixed ts_delta or compute from actual observation?
    # Observations do not always happen on schedule, so ts_delta may be variable
    # Defer this decision to the caller to pass in appropriate observation
    ts_delta = time.time() - ts_obs
    q_dot = q_delta / ts_delta

    max_q_dot = np.deg2rad(self.MAX_JOINT_DEGREES_PER_SECOND)
    max_q_delta = max_q_dot * ts_delta

    if (np.abs(q_dot) > max_q_dot).any():
      q_clamp = q_obs + np.clip(q_delta, -max_q_delta, max_q_delta)
      _log(f"Joint velocity {max_q_dot} rad/s exceeded! "
           f"Predicted velocities: {q_dot}")
      _log(f"Last observation ts was {ts_obs}, " f"{ts_delta} seconds ago.")
      _log(f"Desired joints angles were: {q_target}")
      _log(f"Clamping target joints to:  {q_clamp}")
    else:
      q_clamp = q_target

    return q_clamp

  def parse_instruction(self, obs: core.Observation) -> Optional[str]:
    """Parse PyReach Gym Instructions into UTF-8 strings.

    PyReach Gym environments provide text instructions in a weird format.

    Args:
      obs: the current observation containing the instruction

    Returns:
      UTF-8 formatted string of the text instruction, or None if no text
      instruction is found in observation
    """

    assert isinstance(obs, (dict, collections.OrderedDict))
    text_instructions: Any = obs["text_instructions"]
    assert isinstance(obs, (dict, collections.OrderedDict))
    instruction: Any = text_instructions["instruction"]
    assert isinstance(instruction, np.ndarray)

    utf_string: str = bytes([x for x in instruction if x != 0]).decode("utf-8")
    return utf_string

  def _ensure_instruction(self, regex: str) -> None:
    """Ensures that a task is active with instruction matching regex.

    If we time out waiting for a new instruction, that means that
    we have completed all instructions, and we return None,
    otherwise we return the latest observation.

    Args:
      regex: A regular expression identifying the instruction we want.

    Raises:
      RuntimeError: If the desired instruction could not be obtained.
    """
    _log("Asking for a new text instruction")

    def instruction_achieved(parent_env: Any) -> bool:
      # Ensure task is started (if not, start a new task).
      action = collections.OrderedDict(
          {"text_instructions": collections.OrderedDict({"task_enable": 1})})
      obs, _, _, _ = parent_env.step(action)

      # Give time for Reach serve to produce a new instruction
      time.sleep(1)
      obs, _, _, _ = parent_env.step({})

      # Confirm that the instruction is what we want.
      text = self.parse_instruction(obs)
      if text is not None and re.match(regex, text):
        return True
      else:
        _log(f"Current instruction is {text}, but want {regex!r}")
        return False

    if instruction_achieved(super()):
      return

    # This instruction is not what we want. End current task and try again.
    _log("Ending this task to request a new task / instruction.")
    action = collections.OrderedDict(
        {"text_instructions": collections.OrderedDict({"task_enable": 0})})
    _, _, _, _ = super().step(action)

    # Enable a task and check if instruction is achieved.
    if instruction_achieved(super()):
      return

    # Unexpected condition. May be the task codes are not set up correctly?
    raise RuntimeError(
        f"Instruction matching {regex!r} was not obtained from Reach.")

  def reset(self) -> core.Observation:
    """Resets the benchmark.

    This will cause the environment to start a new challenge.

    Returns:
          Initial observation.
    """

    _log("Resetting the benchmark environment")

    # End any current task with reset
    super().reset()
    _log("Wait 1 second for environment to settle")
    time.sleep(1)

    obs, _, _, _ = self._movej(self.SAFE_JOINT_ANGLES)

    # Reset timer.
    self._timer_running = False

    # Start a task and ensure the instruction is to scramble.
    self._ensure_instruction(regex=r"^Scramble the t-shirt$")
    self._internal_state = _InternalState.SCRAMBLE_NOW

    # Get updated joint angles
    obs, _, _, _ = super().step({})
    self.last_joint_move_observation = obs
    return obs

  def scramble_done(self) -> None:
    _log("Agent reports scramble_done()")
    if self._internal_state != _InternalState.SCRAMBLE_NOW:
      self._inactivate("scramble_done() when it wasn't expected")
      return
    self._end_instruction()
    self._ensure_instruction(regex=r"^Fold the t-shirt$")
    self._internal_state = _InternalState.FOLD_NOW
    self._timer_running = False

  def fold_done(self) -> None:
    _log("Agent reports fold_done()")
    if self._internal_state != _InternalState.FOLD_NOW:
      self._inactivate("fold_done() when it wasn't expected")
      return
    # We should be all done now.
    # End task so that a crowd-compute is triggered.
    self._end_instruction()

    self._internal_state = _InternalState.INACTIVE
    self._timer_running = False

  def close(self) -> None:
    _log("Closing gym and Reach connect")
    self._stow_workcell()
    super().close()

  def step(self,
           action: core.Action) -> Tuple[core.Observation, float, bool, Any]:
    """Perform one step."""
    observation: core.Observation
    reward: float
    done: bool
    info: Any

    assert isinstance(action, (dict, collections.OrderedDict))

    # Clamp joint angles q based on joint velocity limits
    q_action: Optional[np.ndarray] = None

    if "arm" in action:
      if "joint_angles" in action["arm"]:
        q_action = action["arm"]["joint_angles"]

        q_clamped = self._clamp_joint_velocity_limits(
            q_action, self.last_joint_move_observation)
        action["arm"]["joint_angles"] = q_clamped

    observation, reward, done, info = super().step(action)

    # Only record the last observation if joint action was taken, such that
    # joint velocity calculations are based on the prior joint move.
    # Alternatively, we can update the observation every step, but the delta_t
    # between observations could vary greatly. This approach will store the
    # observation at approximately the agent action rate (e.g. 10 Hz, 100 Hz).
    if q_action is not None:
      self.last_joint_move_observation = observation

    # Start timer if necessary (timeout is per instruction)
    if not self._timer_running:
      self._timer_running = True
      self.deadline = time.time() + self.TIMEOUT_PER_INSTRUCTION_SECONDS
      _log(f"Instruction is '{self.parse_instruction(observation)}'")
      _log(f"You have {self.TIMEOUT_PER_INSTRUCTION_SECONDS} seconds until "
           f"{self.deadline} to complete your instruction. Good luck.")

    # Perform any checks for terminating the instruction
    if self._internal_state == _InternalState.INACTIVE:
      _log(f"Ended with reason {self._inactive_reason}")
      observation, reward, done, info = self._end_instruction()
      done = True
    elif time.time() >= self.deadline:
      _log("You ran out of time! "
           "Please env.reset() to start a new instruction.")
      observation, reward, done, info = self._end_instruction()
      done = True
      reward = -1.0
    elif done:
      _log("Parent env reported done, unexpectedly")
      observation, reward, done, info = self._end_instruction()
      done = True

    return (observation, reward, done, info)
