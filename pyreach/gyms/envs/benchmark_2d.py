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

"""Benchmark environment for the Instruction Following/2D benchmark."""
import collections
import time
from typing import Any, Dict, List, Optional, Tuple, Union

import gym  # type: ignore
import numpy as np  # type: ignore

from pyreach.gyms import core
from pyreach.gyms import reach_env

# The z-height of a block.
BLOCK_HEIGHT_METERS = 0.035

# The z-height of the adapter plate between table and robot.
ADAPTER_PLATE_Z_ADJUST_METERS = 0.022

# The limits for the workspace. This is based on the end effector tip.
BOARD_X_LIMITS_METERS = (0.12, 0.502)
BOARD_Y_LIMITS_METERS = (-0.287, 0.287)
BOARD_Z_LIMITS_METERS = (0.03, 1.0)

SAFE_Z = 0.2
# There's a bit of a problem with sweeping directly in front of the robot base,
# so we do a little jig around it.
SWEEP_CORNERS = np.array([
    [0.502, -0.287, 0.114, 3.141, 0.0, 0.0],
    [0.502, 0.287, 0.114, 3.141, 0.0, 0.0],
    [0.12, 0.287, 0.114, 3.141, 0.0, 0.0],
    [0.177, 0.086, 0.114, 3.141, 0.0, 0.0],  # Jig
    [0.12, -0.287, 0.114, 3.141, 0.0, 0.0],
])
# The same, but precomputed in joint space so we don't have to rely on IK.
SWEEP_CORNERS_JOINTS = np.array([
    [-0.517, 0.753, -1.401, 0.0, 0.644, -0.516],
    [0.517, 0.753, -1.401, 0, 0.644, 0.521],
    [1.166, 0.179, -0.340, -0.019, 0.163, 1.184],
    [-0.372, 0.014, -0.249, 2.957, -0.236, -3.332],
    [-1.176, 0.187, -0.336, 0.003, 0.127, 0],
])
SWEEP_CORNER0_SAFE_Z_JOINTS = [-0.514, 0.582, -1.403, 0.0, 0.824, -0.518]
TIMEOUT_PER_TASK_SECONDS = 20.0
RESPONSE_DONE: int = 1
RESPONSE_FAILED: int = 2  # Done with error other than timeout
RESPONSE_ABORTED: int = 3
RESPONSE_REJECTED: int = 4
RESPONSE_TIMEOUT: int = 5  # Done with timeout error.


class Benchmark2DEnv(reach_env.ReachEnv):
  """Benchmark environment for the Instruction Following/2D benchmark.

  See go/robotics-benchmark-2d

  === Observations ===

  The observation is a dictionary whose keys are the devices that the
  environment supports observations on, which are:

  * "arm"
  * "color_camera"
  * "depth_camera"
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

  obs["color_camera"]:
  "ts":
      # The UNIX timestamp in seconds (floating point) of the camera image.
      gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
  "color":
      # An ndarray of type uint8, with shape (height=480, width=640, depth=3)
      # (red, green, and blue channels).
      gym.spaces.Box(low=0, high=255, shape=(480, 640, 3), dtype=np.uint8),

  obs["server"]:
  "latest_ts":
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

  === Actions ===

  An action is a dictionary whose keys are the devices that the environment
  supports actions on. Zero, one, or any of these keys may be present. The keys
  are:

  * "arm"
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

  action["text_instructions"]:
  "task_enable":
      # 0 = end current task. 1 = start a new task.
      gym.spaces.Discrete(2)

  When an action is given to step(), it will immediately return, unless you had
  an arm action that was synchronous, in which case step() will return once the
  arm action is finished.
  """

  def __init__(self, **kwargs: Any) -> None:
    self.timer_running: bool = False
    self.deadline: float = 0.0

    low_joint_angles = tuple([-6.283, -2.059, -3.926, -3.141, -1.692, -6.283])
    high_joint_angles = tuple([6.283, 2.094, 0.191, 3.141, 3.141, 6.283])

    task_params: Dict[str, str] = {"task-code": "128"}

    pyreach_config: Dict[str, reach_env.ReachElement] = {
        "arm":
            reach_env.ReachArm("", low_joint_angles, high_joint_angles,
                               response_queue_length=1),
        "color_camera":  # realsense
            reach_env.ReachColorCamera("", (360, 640)),
        "server":
            reach_env.ReachServer("Server"),
        "text_instructions":
            reach_env.ReachTextInstructions("instruction-generator"),
    }
    super().__init__(
        pyreach_config=pyreach_config, task_params=task_params, **kwargs)

  def _go_to(self, pose: List[float], timeout: float) -> None:
    """Moves the arm synchronously to the given pose."""
    action = collections.OrderedDict({
        "arm":
            collections.OrderedDict({
                "command": 2,
                "pose": pose,
                "synchronous": 1,
                "use_linear": 1,
                "velocity": 0.1,
            })
    })
    _, _, _, _ = super().step(action)

  def _go_to_joints(self, joints: List[float], timeout: float) -> None:
    """Moves the arm synchronously to the given joint angles."""
    action = collections.OrderedDict({
        "arm":
            collections.OrderedDict({
                "command": 1,
                "joint_angles": np.array(joints),
                "synchronous": 1,
                "use_linear": 1,
                "velocity": 0.1,
            })
    })
    _, _, _, _ = super().step(action)

  def _do_cleanup_pass(self, obs: core.Observation) -> None:
    # Lift to safe z
    # Go to corner 0
    # Lower
    # Go to corner 1
    # Go to corner 2
    # Go to corner 3
    # Go to corner 0
    # Lift to safe z

    assert isinstance(obs, (dict, collections.OrderedDict))
    arm: Any = obs["arm"]
    assert isinstance(arm, (dict, collections.OrderedDict))
    safe_pose: Any = arm["pose"]
    assert isinstance(safe_pose, np.ndarray)
    safe_pose = safe_pose.copy()
    safe_pose[2] = SAFE_Z
    print(f"{time.time()}: Go to safe z")
    self._go_to(pose=safe_pose, timeout=2.0)

    start_corner = SWEEP_CORNERS[0]
    start_corner[2] = SAFE_Z
    print(f"{time.time()}: Go to corner 0 at safe z: "
          f"{SWEEP_CORNER0_SAFE_Z_JOINTS}")
    self._go_to_joints(joints=SWEEP_CORNER0_SAFE_Z_JOINTS, timeout=5.0)

    for i, corner in enumerate(SWEEP_CORNERS_JOINTS):
      print(f"{time.time()}: Go to corner {i}: {corner}")
      self._go_to_joints(joints=corner, timeout=5.0)

    end_corner = SWEEP_CORNERS[0]
    end_corner[2] = SAFE_Z
    print(f"{time.time()}: go back to safe z: {SWEEP_CORNER0_SAFE_Z_JOINTS}")
    self._go_to_joints(joints=SWEEP_CORNER0_SAFE_Z_JOINTS, timeout=5.0)

    print(f"{time.time()}: done with sweep")

  def reset(self) -> core.Observation:
    """Resets the benchmark.

    This involves running a cleanup pass around the edge of the surface to push
    any blocks that are outside the working area into the working area. It also
    randomizes the list of instructions to present to the agent.

    Returns:
      Initial observation.
    """

    # End any current task
    action = collections.OrderedDict(
        {"text_instructions": collections.OrderedDict({"task_enable": 0})})
    _, _, _, _ = super().step(action)
    obs = super().reset()

    # There's a problem with IK, so we're skipping this for now.
    # self._do_cleanup_sweep(obs)

    # Start a new task
    action = collections.OrderedDict(
        {"text_instructions": collections.OrderedDict({"task_enable": 1})})
    obs, _, _, _ = super().step(action)

    return obs

  def step(self,
           action: core.Action) -> Tuple[core.Observation, float, bool, Any]:
    """Perform one step."""
    observation: core.Observation
    reward: float
    done: bool
    info: Any

    if not self.timer_running:
      self.timer_running = True
      self.deadline = time.time() + TIMEOUT_PER_TASK_SECONDS
      print(f"{time.time()}: You have until {self.deadline} "
            "to complete your task. Good luck.")

    observation, reward, done, info = super().step(action)

    if done:
      self.timer_running = False
      observation, reward, _, info = self._ask_for_new_instruction(observation)
      return (observation, reward, done, info)

    if time.time() >= self.deadline:
      print(f"{time.time()}: You ran out of time!")
      self.timer_running = False
      reward = -1.0
      done = True

    # done only gets set here when the agent runs out of time.
    if done:
      observation, reward, _, info = self._ask_for_new_instruction(observation)

    return (observation, reward, done, info)

  def _ask_for_new_instruction(
      self, current_observation: core.Observation) -> Tuple[core.Observation,
                                                            float, bool, Any]:
    """Asks for a new instruction.

    If we time out waiting for a new instruction, that means that
    we have completed all instructions, and we return None,
    otherwise we return the latest observation.

    Args:
      current_observation: the current observation.

    Returns:
      The observation when the instruction is received.
    """
    print(f"{time.time()}: Asking for a new text instruction")

    # End current task
    action = collections.OrderedDict(
        {"text_instructions": collections.OrderedDict({"task_enable": 0})})

    _, _, _, _ = super().step(action)

    # Start new task
    action = collections.OrderedDict(
        {"text_instructions": collections.OrderedDict({"task_enable": 1})})
    return super().step(action)


# Just to make things interesting, this is somewhere around the center,
# with z-height 86mm above the table.
START_JOINTS = np.array([0.0, 0.069, -0.797, 0.024, 0.838, 1.6], dtype=float)


class Benchmark2DServoJointsWrapper(gym.Wrapper):
  """A wrapper for the 2D Benchmark environment for servoing joints only.

  This environment is a stripped-down environment which provides actions for
  servo moves of joints only. It also checks any movement to ensure that it
  does not crash the end-effector into the table or move it outside the
  bounds of the board. If such a move happens, the action is skipped.

  We also provide a convenience method, go_to_center(), which moves
  synchronously to the center of the board at a safe Z-height.

  == Actions ==

  action["arm"]:
    "joint_angles":
        # The joint angles to move to, in radians.
        gym.spaces.Box(
            low=np.array((-6.283, -2.059, -3.926, -3.141, 1.692, -6.283)),
            high=np.array((6.283, 2.094, 0.191, 3.141, 3.141, 6.283)),
            dtype=np.dtype(float)),

  == Observations ==

    No filters! See Benchmark2DEnv!
  """

  def __init__(self, env: Benchmark2DEnv) -> None:
    super().__init__(env)

    self.env: gym.Env = env
    self.action_id: int = 1
    self.prev_observation: core.Observation = None

    self.action_space: core.Space = gym.spaces.Dict({
        "arm":
            gym.spaces.Dict({
                "joint_angles": self.env.action_space["arm"]["joint_angles"],
            })
    })
    self.observation_space: core.Space = self.env.observation_space

  def reset(self) -> core.Observation:
    self.prev_observation = self.env.reset()
    return self.prev_observation

  def step(self,
           action: core.Action) -> Tuple[core.Observation, float, bool, Any]:
    assert isinstance(action, (dict, collections.OrderedDict))

    new_action = {}

    if "arm" in action:
      arm: Any = action["arm"]
      assert isinstance(arm, (dict, collections.OrderedDict))
      joint_angles: Any = arm["joint_angles"]
      assert isinstance(joint_angles, np.ndarray)
      new_joint_angles: Optional[np.ndarray] = joint_angles

      if new_joint_angles is not None:
        new_action["arm"] = {
            "command": 1,
            "joint_angles": new_joint_angles,
            "servo": 1,
            "id": self.action_id,
        }
        self.action_id += 1

        if not self._is_move_safe(self.prev_observation, new_joint_angles):
          print(f"{time.time()}: Unsafe move")
          del new_action["arm"]

    self.prev_observation, reward, done, info = self.env.step(new_action)
    joints = self.prev_observation.get("arm", {}).get("joint_angles")
    if joints is not None:
      pose = self.env.fk("arm", joints, apply_tip_adjust_transform=True)

      pose_list = pose.as_list()
      # Add Z-height because of the adapter plate between the table and base.
      pose_list[2] += ADAPTER_PLATE_Z_ADJUST_METERS

      self.prev_observation["arm"]["pose"] = np.array(pose_list)
    return self.prev_observation, reward, done, info

  def _is_move_safe(
      self, obs: core.Observation, joints: Union[Tuple[float, ...], List[float],
                                                 np.ndarray]) -> bool:
    """Determines if the action will lead to a safe pose."""
    pose = self.env.fk("arm", joints, apply_tip_adjust_transform=True)
    if pose is None:
      print(f"{time.time()}: Pose for fk is None")
      return False

    # Add Z-height because of the adapter plate between the table and base.
    z = pose.position.z
    z += ADAPTER_PLATE_Z_ADJUST_METERS

    return (self._is_between_limits(pose.position.x, BOARD_X_LIMITS_METERS) and
            self._is_between_limits(pose.position.y, BOARD_Y_LIMITS_METERS) and
            self._is_between_limits(z, BOARD_Z_LIMITS_METERS))

  def _is_between_limits(self, val: float, limits: Tuple[float, float]) -> bool:
    """Determines if the value is between, inclusive of, the given limits."""
    return limits[0] <= val <= limits[1]

  def go_to_center(self) -> Tuple[core.Observation, float, bool, Any]:
    """Moves the arm to the center synchronously.

    Does not return until the move is complete.

    Returns:
      Observation, reward, done, info.

    """
    new_action = {}

    new_action["arm"] = {
        "command": 1,
        "joint_angles": START_JOINTS,
        "synchronous": 1,
        "velocity": 0.1,
    }

    print(f"{time.time()}: Moving to center")
    self.prev_observation, reward, done, info = self.env.step(new_action)
    print(f"{time.time()}: Center move complete")
    return self.prev_observation, reward, done, info
