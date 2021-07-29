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

  == Evaluation Protocol ==

    1.  The agent connects to the evaluation cell. The agent should write a
        single_attempt() method which does the following.

    2.  Reset: The agent must call reset to start each attempt.

    3.  Scramble: The workcell provides instruction "Scramble the t-shirt".
    4.  The agent may use its own policy, or call the pre-programmed
        env.scramble() method.
    5.  The agent must call scramble_done().

    6.  Fold: The workcell will provide the instruction "Fold the t-shirt".
    7.  The agent uses its own policy to fold.
    8.  The agent calls env.fold_done().

    9.  At this point, an attempt to solve has finished.

  === Observation Space ===

  The observation is a dictionary whose keys are the devices that the
  environment supports observations on, which are:

  * "arm"
  * "camera"
  * "depth_camera"
  * "workcell_camera"
  * "server"
  * "text_instructions"

  Each of these is a dictionary with the following observation space:

  obs["arm"]:
  "ts":
      # The UNIX timestamp in seconds (floating point) of the state.
      gym.spaces.Box(low=0, high=sys.maxsize, shape=())

  "joint_angles":
      # The 6 joint angles of the arm, in radians.
      gym.spaces.Box(
          low=np.array(low_joint_angles),
          high=np.array(high_joint_angles),
          dtype=np.float)

  "pose":
      # The X, Y, Z, Rx, Ry, Rz pose of the arm, in meters and radians.
      # Rx, Ry, and Rz are in axis-angle form.
      gym.spaces.Box(low=-100, high=100, shape=(6,))

  "status":
      # The state of the command:
      #  0 = no command, or not done yet
      #  1 = done, no error
      #  2 = failed
      #  3 = aborted by another command
      #  4 = rejected by the server
      #  5 = timed out
      gym.spaces.Discrete(6),

  "responses":
      # A tuple of the most recent command responses.
      gym.spaces.Tuple((ResponseElement,))

      ResponseElement: gym.spaces.Dict({
          "ts":
              # The UNIX timestamp in seconds (floating point) of the status.
              gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
          "id":
              # The ID of the command this status belongs to.
              gym.spaces.Discrete(1 << 30),
          "status":
              # The state of the command:
              #  0 = no command, or not done yet
              #  1 = done, no error
              #  2 = failed
              #  3 = aborted by another command
              #  4 = rejected by the server
              #  5 = timed out
              gym.spaces.Discrete(6),
          "finished":
              gym.spaces.Discrete(2)
      })

  obs["camera"]:
  "ts":
      # The UNIX timestamp in seconds (floating point) of the camera image.
      gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
  "color":
      # An ndarray of type uint8, with shape (height=240, width=424, depth=3)
      # (red, green, and blue channels).
      gym.spaces.Box(low=0, high=255, shape=(240, 424, 3), dtype=np.uint8),

  obs["depth_camera"]:
  "ts":
      # The UNIX timestamp in seconds (floating point) of the camera image.
      gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
  "color":
      # An ndarray of type uint8, with shape (height=240, width=426, depth=3)
      # (red, green, and blue channels).
      gym.spaces.Box(low=0, high=255, shape=(240, 426, 3), dtype=np.uint8),

  obs["workcell_camera"]:
  "ts":
      # The UNIX timestamp in seconds (floating point) of the camera image.
      gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
  "color":
      # An ndarray of type uint8, with shape (height=240, width=427, depth=3)
      # (red, green, and blue channels).
      gym.spaces.Box(low=0, high=255, shape=(240, 427, 3), dtype=np.uint8),

  obs["server"]:
  "ts":
      # The UNIX timestamp in seconds (floating point) of the most recent
      # message received.
      gym.spaces.Box(low=0, high=sys.maxsize, shape=())

  obs["text_instructions"]:
  "ts":
      # The UNIX timestamp in seconds (floating point) of the most recent
      # instruction received.
      gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
  "instruction":
      # The most recent instruction received, as a UTF-8 encoded string.
      # The end of the string is marked by a 0 byte. All bytes after that are
      # also 0.
      gym.spaces.MultiDiscrete(1024 * [255])

  === Action Space ===

  An action is a dictionary whose keys are the devices that the environment
  supports actions on. Zero, one, or any of these keys may be present. The keys
  are:

  * "arm"
  * "vacuum"
  * "text_instructions"

  Each of these is a dictionary with the following action space:

  action["arm"]:
  "command":
      # The command to perform. 0 means do nothing (although you can leave out
      # the arm action entirely if you want that), 1 means move specifying
      # joint angles, and 2 means move specifying a pose.
      gym.spaces.Discrete(3),
  "id:":
      # A unique ID to identify this command in the arm responses observation.
      # Not necessary if "synchronous" is set to 1.
      gym.spaces.Discrete(1 << 30),
  "joint_angles":
      # With command 1, the joint angles to move to.
      gym.spaces.Box(
          low=np.array((-6.283, -2.059, -3.926, -3.141, 1.692, -6.283)),
          high=np.array((6.283, 2.094, 0.191, 3.141, 3.141, 6.283)),
          dtype=np.dtype(float)),
  "pose":
      # With command 2, the X, Y, Z, Rx, Ry, Rz pose to move to, in meters and
      # radians. Rx, Ry, and Rz are in axis-angle form.
      gym.spaces.Box(low=-100, high=100, shape=(6,)),
  "use_linear":
      # 0 = move in joint space. 1 = move in cartesian space (i.e. linearly).
      gym.spaces.Discrete(2),
  "velocity":
      # The max velocity to move the arm. 0 means use whatever velocity was
      # previously used. If specifying the move by joint_angles, this is the
      # maximum velocity of any joint in rad/s. If specifying the move by
      # pose, this is the desired velocity in m/s.
      gym.spaces.Box(low=0, high=10, shape=()),
  "acceleration":
      # The max acceleration to move the arm. 0 means use whatever acceleration
      # was previously used. If specifying the move by joint_angles, this is the
      # maximum acceleration of any joint in rad/s/s. If specifying the move by
      # pose, this is the desired acceleration in m/s/s.
      gym.spaces.Box(low=0, high=10, shape=()),
  "servo":
      # 0 = move normally. 1 = move as fast as possible.
      gym.spaces.Discrete(2),
  "synchronous":
      # 0 = return an observation immediately. 1 = block until done.
      gym.spaces.Discrete(2),
  "timeout":
      # The amount of time, in seconds, to wait for the arm to complete its
      # movement. If the arm does not complete its motion by the end of the
      # timeout period, the status in the observation will be 5 (timed out).
      gym.spaces.Box(low=0, high=sys.maxsize, shape=()),

  action["vacuum"]:
  "state":
      # 0 = open gripper. 1 = close gripper.
      gym.spaces.Discrete(2)

  action["text_instructions"]:
  "task_enable":
      # 0 = end current task. 1 = start a new task.
      gym.spaces.Discrete(2)

  When an action is given to step(), it will immediately return, unless you had
  an arm action that was synchronous, in which case step() will return once the
  arm action is finished.
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
        "camera":
            reach_env.ReachColorCamera("realsense", (240, 424)),
        "depth_camera":
            reach_env.ReachDepthCamera("", (240, 426), color_enabled=True),
        "workcell_camera":
            reach_env.ReachColorCamera("g3flex", (240, 427)),
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
            "velocity": 0.5
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
            "velocity": 0.5
        }
    }
    return super().step(action)

  def _grab(self) -> Tuple[core.Observation, float, bool, Any]:
    action = {"vacuum": {"state": reach_env.ReachVacuumState.VACUUM}}
    return super().step(action)

  def _release(self) -> Tuple[core.Observation, float, bool, Any]:
    action = {"vacuum": {"state": reach_env.ReachVacuumState.OFF}}
    return super().step(action)

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
      _log(f"Last observation ts was {ts_obs}, "
           f"{ts_delta} seconds ago.")
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

  def _ensure_instruction(
      self,
      regex: str) -> None:
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
    _log("Wait 2 seconds for sim to settle")
    time.sleep(2)

    obs, _, _, _ = self._movej(self.SAFE_JOINT_ANGLES)

    # Reset timer.
    self._timer_running = False

    # Start a task and ensur the instruction is to scramble.
    self._ensure_instruction(regex=r"^Scramble the t-shirt$")
    self._internal_state = _InternalState.SCRAMBLE_NOW

    # Give time for Reach serve to produce a new instruction
    time.sleep(1)

    self.last_joint_move_observation = obs
    return obs

  def scramble_done(self) -> None:
    _log("Agent reports scramble_done()")
    if self._internal_state != _InternalState.SCRAMBLE_NOW:
      self._inactivate("scramble_done() when it wasn't expected")
      return
    self._ensure_instruction(regex=r"^Fold the t-shirt$")
    self._internal_state = _InternalState.FOLD_NOW
    # Timer will start on first step().
    self._timer_running = True

  def fold_done(self) -> None:
    _log("Agent reports fold_done()")
    if self._internal_state != _InternalState.FOLD_NOW:
      self._inactivate("fold_done() when it wasn't expected")
      return
    # We should be all done now.
    # End task so that a crowd-compute is triggered.
    action = collections.OrderedDict(
        {"text_instructions": collections.OrderedDict({"task_enable": 0})})
    _, _, _, _ = super().step(action)

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

    if not self._timer_running:
      self._timer_running = True
      self.deadline = time.time() + self.TIMEOUT_PER_INSTRUCTION_SECONDS
      _log(f"Instruction is '{self.parse_instruction(observation)}'")
      _log(
          f"You have {self.TIMEOUT_PER_INSTRUCTION_SECONDS} seconds until "
          f"{self.deadline} to complete your instruction. Good luck."
      )

    if self._internal_state == _InternalState.INACTIVE:
      _log(f"Ended with reason {self._inactive_reason}")
      done = True
    elif time.time() >= self.deadline:
      _log("You ran out of time! "
           "Please env.reset() to start a new instruction.")
      done = True
      reward = -1.0
    elif done:
      _log("Parent env reported done, unexpectedly")

    return (observation, reward, done, info)
