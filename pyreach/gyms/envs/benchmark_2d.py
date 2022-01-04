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
import enum
import math
import os
import queue
import signal
import socket
import sys
import tempfile
import threading
import time
from typing import Any, Dict, List, Optional, Tuple, cast, TYPE_CHECKING
from typing import Callable

from absl import app  # type: ignore
from absl import flags  # type: ignore
import gym  # type: ignore
import gym.core  # type: ignore
from gym.utils import seeding  # type: ignore
import numpy as np  # type: ignore
from google.protobuf import timestamp_pb2
from pyreach.common.proto_gen import logs_pb2
from pyreach.core import Pose
from pyreach.gyms import core
from pyreach.gyms import reach_env
from pyreach.gyms.arm_element import ReachArmCommand
from pyreach.gyms.task_element import ReachAction as ReachTaskAction

# The type of the return from step.
StepReturn = Tuple[core.Observation, float, bool, Any]

# The benchmark environment ID. This corresponds to the id in
# gyms/__init__.py.
ENV_ID = "benchmark-2d-v1"

# The official 2d benchmark task code.
TASK_CODE_2D = "128"

# The number of bytes expected in each chat transaction. This is the maximum
# size of a short- or long-horizon instruction.
CHAT_LEN_BYTES = 256
# The file in the os temp dir containing the chat port number.
CHAT_PORT_FILE = "benchmark_2d_chat_port.txt"

# The orientation for the tool to point straight down.
TOOL_ORIENTATION_RADS = (1.27, -2.845, -0.054)

# The rough limits for the workspace. This is based on the end effector tip.
# It's a bit sloppy, because there may be some areas which can't be reached,
# especially close to the robot base and close to the far corners.
BOARD_X_LIMITS_METERS = (0.200, 0.610)   # near, far w.r.t. base
BOARD_Y_LIMITS_METERS = (-0.297, 0.335)  # right, left w.r.t. base
BOARD_Z_LIMITS_METERS = (0.1, 0.5)

# Safe z-height. This is above the blocks, so movement at this height will
# not impact against any blocks.
SAFE_Z_METERS = 0.262

# z-height where the end-effector can push the blocks around.
PUSH_Z_METERS = 0.184

# Maximum allowed linear distance (meters) between (i) desired cartesian pose,
# and (ii) measured cartesian pose.
SAFE_SERVO_DIST_METERS = 0.071

# Resting corner x,y coordinates (upper right with respect to a camera
# facing the base from the far side of the board, or near left with respect to
# the base) where the arm goes after a test case.
CORNER_X_METERS = 0.200
CORNER_Y_METERS = 0.335

# The number of seconds to complete a long-horizon instruction.
TIMEOUT_PER_TASK_SECONDS = 4 * 60.0

RESPONSE_DONE: int = 1
RESPONSE_FAILED: int = 2  # Done with error other than timeout
RESPONSE_ABORTED: int = 3
RESPONSE_REJECTED: int = 4
RESPONSE_TIMEOUT: int = 5  # Done with timeout error.

# The path to the file containing the instructions. The file is expected to have
# one string per line, the long-horizon text instruction to carry out. It must
# be no more than 256 bytes long when encoded as UTF-8.
INSTRUCTIONS_PATH: str = "benchmark_2d_long_horizon_instrs.txt"

# The maximum number of test cases to present.
NUM_TEST_CASES: int = 3

# Required for mypy to pass typechecking.
if TYPE_CHECKING:
  SimpleQueue = queue.SimpleQueue
else:
  class FakeGenericMeta(type):

    def __getitem__(cls, item):
      return cls

  class SimpleQueue(queue.Queue, metaclass=FakeGenericMeta):
    pass


class Instruction:
  """Represents a single long-horizon instruction to test the agent against."""

  def __init__(self, instruction: str):
    self.instruction = instruction


class SetupState(enum.Enum):
  """The state of the environment."""
  # The environment needs the human to reset the environment.
  AWAIT_CLIENT = enum.auto()
  # The agent is attempting to follow the instruction.
  ATTEMPTING_INSTRUCTION = enum.auto()


class TextInstruction:
  """Text instruction class for holding text instruction data.

  Attributes:
    name: The name of the corresponding device.
    ts: The timestamp when the instruction was created.
    instr: The UTF-8 encoded text instruction.
  """

  name: str
  ts: float
  instr: np.ndarray
  _lock: threading.Lock

  def __init__(self, name: str):
    assert name, "TextInstruction name cannot be empty"
    self.name = name
    self.ts = 0
    self.instr = self._str_to_nparray("")
    self._lock = threading.Lock()

  def set(self, instr: str) -> None:
    """Sets this instruction's data.

    Thread-safe.

    Args:
      instr: The instruction to set.
    """
    self._lock.acquire()
    self.ts = time.time()
    self.instr = self._str_to_nparray(instr)
    self._lock.release()

  def inject(self, obs: core.Observation) -> None:
    """Injects this instruction into the observation.

    Thread safe.

    Args:
      obs: The observation to inject the instruction into.
    """
    obs = cast(Dict[str, Any], obs)
    self._lock.acquire()
    obs[self.name] = {
        "ts": self.ts,
        "instruction": self.instr,
    }
    self._lock.release()

  def _str_to_nparray(self, s: str) -> np.ndarray:
    """Encodes the string as UTF-8, returning the data as an ndarray.

    If the string encodes to more than CHAT_LEN_BYTES, the array is
    truncated to CHAT_LEN_BYTES.

    Args:
      s: The string to encode.
    Returns:
      The UTF-8 encoded string in an np.ndarray of floats.
    """
    bs = s.encode("utf-8")[:CHAT_LEN_BYTES]
    buff = bytearray([0] * CHAT_LEN_BYTES)
    buff[:len(bs)] = bs
    return np.array(list(buff), dtype=np.float)


class ChatServer:
  """Sets up a socket at a random port to receive chat messages.

  The port number chosen is stored in /{TMPDIR}/{CHAT_PORT_FILE}.

  Upon initial connection, it will send the long-horizon text instruction over
  to the connecting client. Then it will wait for CHAT_LEN_BYTES length
  messages and notify the environment for each message. When the client closes
  the connection, we assume the task is done.
  """

  instruction: str
  server: socket.socket
  sock: socket.socket
  thread: threading.Thread
  chatport: int

  def __init__(self, instruction: str,
               notify: Callable[[bytearray], None]):
    self.instruction = instruction
    self.notify = notify

    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.server.bind((socket.gethostname(), 0))
    self.chatport = self.server.getsockname()[1]
    with open(f"{tempfile.gettempdir()}/{CHAT_PORT_FILE}", "w") as f:
      f.write(f"{self.chatport}")
    self.server.listen(1)
    print(f"{time.time()}: Waiting for chat client to connect")
    (self.sock, _) = self.server.accept()
    self.thread = threading.Thread(target=self.go)
    self.thread.start()

  def go(self) -> None:
    """Handles the connection.

    First sends the long-horizon text instruction. Then awaits low-level text
    instructions, until the client closes the connection.
    """
    bs = self.instruction.encode("utf-8")[:CHAT_LEN_BYTES]
    buff = bytearray([0] * CHAT_LEN_BYTES)
    buff[:len(bs)] = bs
    total = 0
    while total < CHAT_LEN_BYTES:
      sent = self.sock.send(buff[total:])
      if sent == 0:
        print("")
        print(f"{time.time()}: Chat client closed connection.")
        return
      total = total + sent

    while True:
      data = bytearray()
      while len(data) < CHAT_LEN_BYTES:
        chunk = self.sock.recv(CHAT_LEN_BYTES - len(data))
        if not chunk:
          print("")
          print(f"{time.time()}: Chat client closed connection.")
          self.stop()
          return
        data.extend(chunk)
      self.notify(data)

  def stop(self) -> None:
    """Stops the server."""
    print("Stopping chat server...")
    fname = f"{tempfile.gettempdir()}/{CHAT_PORT_FILE}"
    try:
      os.remove(fname)
    except FileNotFoundError:
      pass
    try:
      self.sock.shutdown(socket.SHUT_RD)
    except OSError:
      pass  # This is okay.
    self.sock.close()
    try:
      self.server.shutdown(socket.SHUT_RD)
    except OSError:
      pass  # This is okay.
    self.server.close()

  def is_alive(self) -> bool:
    return self.thread.is_alive()


class ChatClient:
  """Connects to the server to send low-level text instructions.

  Upon connection, waits for the long-horizon text instruction from the server.
  Then waits for input, and sends each message as a CHAT_LEN_BYTES-length
  low-level text instruction to the server.

  If the user ctrl-C's out of the input, we send that ctrl-C to the server
  as an indication that the user claims the long-horizon instruction is done.

  If the server disconnects, we either ran out of time or the agent claims
  the long-horizon instruction is done.

  This happens as many as NUM_TEST_CASES times.
  """

  client: socket.socket

  def __init__(self) -> None:
    for _ in range(NUM_TEST_CASES):
      print("-------------------- RESET --------------------------------")
      print("1. E-stop the robot.")
      print("2. Roughly bunch all the blocks in the center.")
      print("3. Separate them all a bit.")
      print("4. Release the e-stop.")
      print("5. Hit return.")
      _ = input("> ")

      if not self.connect():
        print("The agent never became ready. Probably a bug.")
        return

      if not self.await_instruction():
        return
      thread = threading.Thread(target=self.await_server_termination)
      thread.start()
      while self.getline():
        pass
      while thread.is_alive():
        try:
          time.sleep(1)
        except KeyboardInterrupt:
          pass  # This is expected if client hits ctrl-C.
      time.sleep(1)  # Enough time for the server to delete its port file.
    print("No more test cases.")

  def connect(self) -> bool:
    """Gets the port number from the server's port file."""
    port = -1
    for _ in range(30):
      try:
        fname = f"{tempfile.gettempdir()}/{CHAT_PORT_FILE}"
        with open(fname, "r") as f:
          port = int(f.readline())
      except FileNotFoundError:
        print("The agent is not ready (no port file)... sleeping 1 second")
        time.sleep(1)
        continue

      if port == -1:
        print("The agent never became ready. Probably a bug.")
        return False

      print(f"Connecting to port {port}")
      try:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((socket.gethostname(), port))
        break

      except ConnectionRefusedError:
        print("The agent is not ready: connection refused... sleeping 1 second")
        time.sleep(1)
        continue

    print("Connected to agent.")

    return True

  def await_server_termination(self) -> None:
    """Blocks until server terminates."""
    _ = self.client.recv(CHAT_LEN_BYTES)
    os.kill(os.getpid(), signal.SIGINT)
    print("")
    print("Server closed connection. Please wait for agent cleanup.")

  def getline(self) -> bool:
    """Gets a short-horizon instruction from the user."""
    buff = bytearray([0] * CHAT_LEN_BYTES)
    line = "\u0003"  # ctrl-C

    try:
      line = input("> ")
    except KeyboardInterrupt:
      print("Completion indicated!")
      pass

    bs = line.encode("utf-8")[:CHAT_LEN_BYTES]
    buff[:len(bs)] = bs
    total = 0
    while total < CHAT_LEN_BYTES:
      sent = self.client.send(buff[total:])
      if sent == 0:
        print("")
        print("Completion or time limit indicated by "
              "agent (server closed connection).")
        return False
      total = total + sent
    if line == "\u0003":
      print("Completion indication sent to agent. "
            "Please wait for agent cleanup.")
      return False
    return True

  def await_instruction(self) -> bool:
    """Waits for a long-horizon instruction from the server."""
    data = bytearray()
    while len(data) < CHAT_LEN_BYTES:
      chunk = self.client.recv(CHAT_LEN_BYTES - len(data))
      if not chunk:
        print("")
        print("Server closed connection.")
        return False
      data.extend(chunk)
    print("------------------ INSTRUCTION -----------------------------")
    print("")
    print("Give the robot instructions to help it complete the following")
    print("task. End each instruction with a return. If you see that the robot")
    print("completed the entire task, hit ctrl-C to tell it that it finished.")
    print("You've got four minutes from now!")
    print("")
    print(data.decode("utf-8", "ignore"))
    print("")
    print("------------------------------------------------------------")
    return True


class Benchmark2DEnv(reach_env.ReachEnv):
  """Benchmark environment for the Instruction Following/2D benchmark.

  See go/robotics-benchmark-2d and gym_api.md.

  Briefly, the agent controls the robot, and a human (the "instructor")
  gives the agent short-horizon instructions with the goal of completing
  a long-horizon instruction. The agent is given the long-horizon
  instruction also, but is not required to understand it or use it.

  Procedure:
  1. Run the gym; the gym connects to the evaluation cell. When the instructor
     is ready, the instructor runs the chat client, which connects to the gym.
  2. The 100 long-horizon instructions in the INSTRUCTIONS_PATH file are
     shuffled by the gym.
     * Each long-horizon instruction is no more than 256 bytes long when
       encoded in UTF-8.
  3. For each of the first three (shuffled) instructions:
    a. The arm is moved up and out of the way of the board.
    b. The gym tells the instructor to e-stop the robot, bunch all the blocks
       together in the center, separate them a bit, and un-e-stop the robot.
    c. When the instructor tells the gym this was done, the gym:
       i. Sends a task start.
       ii. Moves the arm down to an appropriate z-height to push the blocks.
       iii. Gives the long-horizon instruction to the agent as an array of 256
            floats. Each float is one byte of UTF-8 encoded text. Bytes beyond
            the length of the encoded text are zero.
       iv. Gives the long-horizon instruction to the instructor as text.
       v. Starts a timer for four minutes.
       vi. Sends an annotation for the beginning of the episode.
       vii. Sends an annotation for the long-horizon instruction.
    d. The instructor gives the gym short-horizon instructions which are passed
       through to the agent verbatim.
       * Each short-horizon instruction may be no more than 256 bytes long.
       * Short-horizon instructions longer than 256 bytes are truncated to 256
         bytes.
       * Short-horizon instructions have no limit for their frequency of
         submission.
       * Short-horizon instructions are also sent in annotations.
    e. The agent attempts to carry out the instructor's short-horizon
       instructions.
    f. The episode ends in any of these cases:
       i. The instructor declares that the long-horizon instruction is done, by
          hitting ctrl-C in the chat client.
       ii. The agent declares that the long-horizon instruction is done, by
           setting the "done" action to 1.
       iii. The four-minute timer elapses.
    g. The gym sends an annotation to mark the end of the episode.
    h. The arm is moved up and out of the way of the board.
    i. The gym sends a task end.
  4. The gym disconnects from the robot.

  From a logs perspective, the data is as follows:
    * Gym connects to robot.
    * Repeat 3 times:
      * Robot arm moves out of the way.
      * Task start (task code 128)
      * Robot arm moves to ready position.
      * Annotation: begin test case:
            annotation.point_measurement.space = "benchmark-2d-v1",
            annotation.point_measurement.name = "test_case_begin_ts",
            annotation.point_measurement.value.seconds = timestamp
        * Annotation: long-horizon instruction:
              long_horizon_instruction.text = long-horizon instruction
        * Robot arm moves, with short-horizon instruction annotations when
          issued:
              short_horizon_instruction.text = short-horizon instruction
      * Annotation: end test case:
            annotation.point_measurement.space = "benchmark-2d-v1",
            annotation.point_measurement.name = "test_case_begin_ts",
            annotation.point_measurement.value.seconds = time from
                test_case_begin_ts
      * Robot arm moves out of the way.
      * Task end (task code 128)
    * Gym disconnects from robot.
  """

  def __init__(self, **kwargs: Any) -> None:
    """Initializes the environment.

    Arguments:
      **kwargs: Keyword arguments.

    Keyword args accepted:

    tc (str): The task code to override the standard task code with.
    disable_time_limit (bool): Whether to disable the standard time limit.
    """
    self._low_level_queue: SimpleQueue[str] = SimpleQueue()
    self._timer_running: bool = False
    self._deadline: float = 0.0
    # The full list of long-horizon instructions.
    self._long_horizon_instructions: List[Instruction] = self._load_test_cases()
    # The random number generator for the environment.
    self._np_random: np.random.RandomState = np.random.RandomState()
    # The long-horizon instruction number to attempt
    self._instr_num: int = 0
    # The environment state.
    self._setup_state: SetupState = SetupState.AWAIT_CLIENT
    # The last observed server timestamp, for sending annotations.
    self._last_server_ts: float = 0.0
    # The last observed pose, for checking for unsafe actions.
    self._last_pose: Optional[np.ndarray] = None
    # The time at which the long-horizon instruction begins, defined as just
    # before the arm drops to the pushing z-height before the long-horizon
    # instruction is annotated. See _start_test_case() for details.
    self._test_case_begin_ts: float = 0.0

    # Memoized action space, with done space injected.
    self._action_space: Optional[core.Space] = None
    # Memoized observation space, with instruction spaces injected.
    self._observation_space: Optional[core.Space] = None
    # The text instruction data.
    self._high_level_instruction = TextInstruction("long_horizon_instruction")
    self._low_level_instruction = TextInstruction("short_horizon_instruction")
    # The chat server.
    self._chat_server: Optional[ChatServer] = None
    # Whether the chat client sent a ctrl-C to indicate test case completed.
    self._chat_client_indicated_end: bool = False

    self._task_code = TASK_CODE_2D
    if "tc" in kwargs:
      self._task_code = str(kwargs["tc"])

    self._disable_time_limit = False
    if "disable_time_limit" in kwargs:
      self._disable_time_limit = bool(kwargs["disable_time_limit"])

    self.seed()

    low_joint_angles = tuple([-6.283, -2.059, -3.926, -3.141, -1.692, -6.283])
    high_joint_angles = tuple([6.283, 2.094, 0.191, 3.141, 3.141, 6.283])

    task_params: Dict[str, str] = {"task-code": self._task_code}

    pyreach_config: Dict[str, reach_env.ReachElement] = {
        "arm":
            reach_env.ReachArm("", low_joint_angles, high_joint_angles,
                               response_queue_length=1, is_synchronous=False),
        "color_camera":  # realsense
            reach_env.ReachColorCamera("", shape=(360, 640),
                                       initial_stream_request_period=0.03),
        "server":
            reach_env.ReachServer("Server"),
        "task":
            reach_env.ReachTask("Task"),
        "annotation":
            reach_env.ReachAnnotation("",
                                      is_synchronous=False,
                                      maximum_size=1024),
    }
    super().__init__(
        pyreach_config=pyreach_config, task_params=task_params, **kwargs)

  @property
  def action_space(self) -> core.Space:
    """Returns the action space.

    This memoizes the ReachEnv action space, adds the done space, and
    hides the task space.
    """
    if self._action_space is not None:
      return self._action_space

    a = super().action_space
    a["done"] = gym.spaces.Discrete(2)
    del a["task"]
    self._action_space = a

    return self._action_space

  def _strip_action(self, action: core.Action) -> core.Action:
    """Removes the 'done' action for passing to the base step()."""
    action = cast(Dict[str, Any], action)

    a = action.copy()
    if "done" in a:
      del a["done"]
    return a

  @property
  def observation_space(self) -> core.Space:
    """Returns the observation space.

    This memoizes the ReachEnv observation space, and then adds the
    text instruction spaces.
    """
    if self._observation_space is not None:
      return self._observation_space

    s = super().observation_space
    s[self._high_level_instruction.name] = gym.spaces.Dict({
        "ts": gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
        "instruction": gym.spaces.MultiDiscrete(CHAT_LEN_BYTES * [255]),
    })
    s[self._low_level_instruction.name] = gym.spaces.Dict({
        "ts": gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
        "instruction": gym.spaces.MultiDiscrete(CHAT_LEN_BYTES * [255]),
    })
    self._observation_space = s

    return self._observation_space

  def _update_observation(self, obs: core.Observation) -> None:
    """Injects the high- and low-level text instructions into the observation.

    They are injected into the observation passed in.

    Also records the last server timestamp for annotations, and the
    last pose for checking unsafe moves.

    Args:
      obs: The observation to inject the instructions into.
    """
    obs = cast(Dict[str, Any], obs)
    self._high_level_instruction.inject(obs)
    self._low_level_instruction.inject(obs)
    self._last_server_ts = obs["server"]["latest_ts"]
    self._last_pose = obs["arm"]["pose"]

  def _load_test_cases(self) -> List[Instruction]:
    """Loads the long horizon instructions from this directory."""
    test_cases = []

    instr_dir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(instr_dir, INSTRUCTIONS_PATH)
    with open(path) as f:
      lines = f.readlines()
      test_cases = [Instruction(instruction=line.strip()) for line in lines]

    return test_cases

  def seed(self, seed: Optional[int] = None) -> List[Any]:
    """Sets the seed for this env's random number generator(s).

    Note:
        Some environments use multiple pseudorandom number generators.
        We want to capture all such seeds used in order to ensure that
        there aren't accidental correlations between multiple generators.

    Args:
      seed: A seed to be passed to np_random. If None, a random seed is used.

    Returns:
        list<bigint>: Returns the list of seeds used in this env's random
          number generators. The first value in the list should be the
          "main" seed, or the value which a reproducer should pass to
          'seed'. Often, the main seed equals the provided 'seed', but
          this won't be true if seed=None, for example.
    """
    self._np_random, seed = seeding.np_random(seed)
    return [seed]

  def reset(self) -> core.Observation:
    """Resets the benchmark.

    Returns:
      Initial observation.
    """

    self._high_level_instruction.set("")
    self._low_level_instruction.set("")
    super().reset()

    print(f"{time.time()}: Resetting environment.")
    observation, reward, _, info = self._end_test_case(reward=0, reset=True)

    # Shuffle the test cases.
    self._np_random.shuffle(self._long_horizon_instructions)
    self._setup_state = SetupState.AWAIT_CLIENT
    self._instr_num = 0

    print(f"{time.time()}: Reset complete.")
    return (observation, reward, False, info)

  def _super_step(self, action: core.Action) -> StepReturn:
    """Calls super step and injects instructions into returned observation."""
    observation, reward, done, info = super().step(action)
    self._update_observation(observation)
    return (observation, reward, done, info)

  def step(self, action: core.Action) -> StepReturn:
    """Perform one step.

    The observation will be None to indicate that the agent should exit.

    Args:
      action: The action to perform.

    Returns:
      A StepReturn tuple.
    """
    observation: core.Observation = None
    reward: float = 0.0
    instr_done: bool = False
    info: Any = None

    # This is just the action, without the done action in it, and with a
    # don't-change-task action in it.
    stripped_action: core.Action = self._strip_action(action)
    stripped_action = cast(Dict[str, Any], stripped_action)
    stripped_action["task"] = {}
    stripped_action["task"]["action"] = ReachTaskAction.NO_CHANGE

    if self._setup_state == SetupState.AWAIT_CLIENT:
      return self._start_test_case(reward, info)

    # Check for various termination criteria.
    reward, instr_done = self._check_for_done(action)

    # instr_done is only set when the agent runs out of time or the agent
    # indicates done, or the human at the chat client indicates done.
    if instr_done:
      self._setup_state = SetupState.AWAIT_CLIENT
      self._instr_num += 1
      print(f"{time.time()}: "
            "Task completion criteria reached; closing out task.")
      return self._end_test_case(reward, reset=False)

    # If there's a new low-level instruction, issue an annotation for it
    # and include it in the observation.
    self._process_low_level_instr()

    # Check the agent's action for board bounds or huge moves. Give a
    # negative reward for such a move.
    if not self._is_safe_move(stripped_action):
      observation, _, _, info = self._super_step({})
      return (observation, -1, False, info)

    # Finally, issue the agent's action.
    observation, reward, _, info = self._super_step(stripped_action)
    return (observation, reward, False, info)

  def _is_safe_move(self, action: core.Action) -> bool:
    """Determines if a servo move is a safe move."""
    action = cast(Dict[str, Any], action)
    pose: Optional[Pose]

    if self._last_pose is None:
      return True
    if "arm" not in action:
      return True
    if "command" not in action["arm"]:
      return True
    if "servo" not in action["arm"]:
      return True
    if action["arm"]["servo"] != 1:
      return True

    if action["arm"]["command"] == ReachArmCommand.POSE:
      p = action["arm"]["pose"]
      if isinstance(p, list):
        pose = Pose.from_list(p)
      elif isinstance(p, tuple):
        p = cast(Tuple[float, float, float, float, float, float], p)
        pose = Pose.from_tuple(p)
      elif isinstance(p, np.ndarray):
        p = cast(np.ndarray, p)
        pose = Pose.from_list(p.tolist())
      else:
        print(f"Warning: Unknown type for arm/pose: {type(p)}, "
              "treating as safe.")
        return True
    elif action["arm"]["command"] == ReachArmCommand.JOINTS:
      pose = self.fk("", action["arm"]["joints"])

    if pose is None:
      print("Warning: FK returned None, treating move as safe.")
      return True

    tr = pose.position
    distx = (tr.x - self._last_pose[0])
    dist = distx * distx
    disty = (tr.y - self._last_pose[1])
    dist += disty * disty
    distz = (tr.z - self._last_pose[2])
    dist += distz * distz
    dist = math.sqrt(dist)
    if dist > SAFE_SERVO_DIST_METERS:
      print("Unsafe move denied: servo move would be "
            f"{dist} > {SAFE_SERVO_DIST_METERS}")
      return False

    fudge = 0.01
    if (tr.x < BOARD_X_LIMITS_METERS[0] - fudge or
        tr.x > BOARD_X_LIMITS_METERS[1] + fudge):
      print("Unsafe move denied: X position {tr.x} exceeds board limits")
      return False
    if (tr.y < BOARD_Y_LIMITS_METERS[0] - fudge or
        tr.y > BOARD_Y_LIMITS_METERS[1] + fudge):
      print("Unsafe move denied: Y position {tr.y} exceeds board limits")
      return False
    if (tr.z < BOARD_Z_LIMITS_METERS[0] - fudge or
        tr.z > BOARD_Z_LIMITS_METERS[1] + fudge):
      print("Unsafe move denied: Z position {tr.z} exceeds board limits")
      return False

    return True

  def _check_for_done(self, action: core.Action) -> Tuple[float, bool]:
    """Checks for various termination criteria."""
    # Did the agent indicate it's done?
    action = cast(Dict[str, Any], action)

    if "done" in action and action["done"] == 1:
      print(f"{time.time()}: Agent indicated completion.")
      self._timer_running = False
      return (1.0, True)

    # Did we run out of time?
    if not self._disable_time_limit and time.time() >= self._deadline:
      print(f"{time.time()}: You ran out of time!")
      self._timer_running = False
      return (-1.0, True)

    # Did the chat client disconnect? The server is not alive if the client
    # disconnected.
    if self._chat_server and not self._chat_server.is_alive():
      print(f"{time.time()}: Chat client disconnected, indicating completion.")
      self._timer_running = False
      return (1.0, True)

    # Did the chat client send a ctrl-C?
    if self._chat_client_indicated_end:
      self._chat_client_indicated_end = False
      print(f"{time.time()}: Chat client sent ctrl-C, indicating completion.")
      self._timer_running = False
      return (1.0, True)

    return (0, False)

  def _notify_low_level_instr(self, data: bytearray) -> None:
    """Puts a received low-level instruction onto the queue."""
    self._low_level_queue.put(data.decode("utf-8", "ignore").rstrip("\x00"))

  def _process_low_level_instr(self) -> None:
    """Handles a low-level instruction.

    If a low-level instruction is present in the queue, pop if off, include
    it in the observation, and send an annotation for it.
    """

    low_level_instr: Optional[str] = None
    try:
      low_level_instr = self._low_level_queue.get_nowait()
    except queue.Empty:
      pass

    if low_level_instr is not None:
      if low_level_instr and ord(low_level_instr[0]) == 3:  # ctrl-C
        self._chat_client_indicated_end = True
        return

      self._low_level_instruction.set(low_level_instr)
      self._annotate_short_horizon_instr(low_level_instr)

  def _end_test_case(self, reward: float, reset: bool) -> StepReturn:
    """Runs cleanup after a test case is done.

    The task is stopped, the arm is moved up and out of the way, the chat
    server is stopped (if still running), the end of the test case is annotated,
    and 'done' is set based on whether we need to run another test case or not.

    Args:
      reward: The reward to give to the agent.
      reset: Whether we are ending the test case due to a reset.

    Returns:
      A StepReturn tuple.
    """

    # Annotate the end of the test case (if this isn't total reset).
    if not reset:
      observation, _, _, info = self._annotate_end_of_test_case()
    else:
      observation, _, _, info = self._super_step({})
    observation = cast(Dict[str, Any], observation)

    # Move the arm up and out of the way:
    # Get the current pose, set the z-height to the safe z-height, and
    # synchronously move.
    pose = observation["arm"]["pose"]
    pose[2] = SAFE_Z_METERS
    pose[3:] = TOOL_ORIENTATION_RADS
    self._go_to(pose, preemptive=True)

    # Move the arm to one corner.
    pose[0] = CORNER_X_METERS
    pose[1] = CORNER_Y_METERS
    self._go_to(pose)

    # Shut down the chat server if started.
    if self._chat_server is not None:
      self._chat_server.stop()
      self._chat_server = None

    observation, _, _, info = self._stop_task()

    # Any more long-horizon instructions?
    if self._instr_num == NUM_TEST_CASES:
      return (observation, reward, True, info)

    # Ignore what the agent wanted to do prior to done.
    observation, _, _, info = self._super_step({})
    return (observation, reward, False, info)

  def _start_test_case(self, reward: float, info: Any) -> StepReturn:
    """Runs setup for a new test case.

    Effectively suspends the agent until the blocks are placed in
    their initial state. When the human is ready to go, issue the
    long-horizon instruction.

    The arm is moved up and out of the way first.

    Args:
      reward: The reward to give to the agent.
      info: Any info to be passed to the agent.

    Returns:
      A StepReturn tuple.
    """

    # See where the arm currently is.
    observation, _, _, _ = self._super_step({})
    observation = cast(Dict[str, Any], observation)

    # Get the long-horizon instruction to work on.
    instr = self._long_horizon_instructions[self._instr_num].instruction
    # print(f"{time.time()}: Long-horizon instruction: {instr}")

    # Start a chat server and await a connection.
    self._chat_server = ChatServer(instr, self._notify_low_level_instr)

    self._start_task()

    # Drop the arm close to the table.
    pose = observation["arm"]["pose"]
    pose[2] = PUSH_Z_METERS
    pose[3:] = TOOL_ORIENTATION_RADS
    self._go_to(pose)

    # Set the starting time for this test case.
    self._test_case_begin_ts = time.time()
    self._annotate_start_of_test_case()

    self._annotate_long_horizon_instr(instr)

    # Set the long-horizon instruction and clear the low-level queue.
    self._high_level_instruction.set(instr)
    self._low_level_instruction.set("")
    while not self._low_level_queue.empty():
      try:
        _ = self._low_level_queue.get_nowait()
      except queue.Empty:
        pass

    # Ignore what the agent wanted to do prior to setup.
    observation, reward, done, info = self._super_step({})

    # Start the timer running.
    self._timer_running = True
    self._deadline = time.time() + TIMEOUT_PER_TASK_SECONDS

    self._setup_state = SetupState.ATTEMPTING_INSTRUCTION

    return (observation, reward, done, info)

  def _start_task(self) -> StepReturn:
    """Starts a task."""
    task_action = collections.OrderedDict(
        {"task": collections.OrderedDict(
            {"action": ReachTaskAction.START})})
    return self._super_step(task_action)

  def _stop_task(self) -> StepReturn:
    """Stops a task."""
    task_action = collections.OrderedDict(
        {"task": collections.OrderedDict(
            {"action": ReachTaskAction.STOP})})
    return self._super_step(task_action)

  def _annotate_long_horizon_instr(self, instr: str) -> StepReturn:
    """Sends an annotation for a long-horizon instruction.

    The instruction is stripped of null bytes at the end, in case
    there were any.

    Args:
      instr: The instruction to put in the annotation.

    Returns:
      A StepReturn tuple.
    """
    annotation = logs_pb2.ClientAnnotation()
    annotation.long_horizon_instruction.text = instr.rstrip("\x00")
    return self._annotate(annotation)

  def _annotate_short_horizon_instr(self, instr: str) -> StepReturn:
    """Sends an annotation for a short-horizon instruction.

    The instruction is stripped of null bytes at the end, in case
    there were any.

    Args:
      instr: The instruction to put in the annotation.

    Returns:
      A StepReturn tuple.
    """
    annotation = logs_pb2.ClientAnnotation()
    annotation.short_horizon_instruction.text = instr.rstrip("\x00")
    return self._annotate(annotation)

  def _annotate_start_of_test_case(self) -> StepReturn:
    """Sends an annotation for the start of the test case."""
    annotation = logs_pb2.ClientAnnotation()
    self._set_proto_timestamp(annotation.point_measurement.timestamp,
                              time.time())
    annotation.point_measurement.space = ENV_ID
    annotation.point_measurement.name = "test_case_begin_ts"
    annotation.point_measurement.value.seconds = self._test_case_begin_ts
    return self._annotate(annotation)

  def _annotate_end_of_test_case(self) -> StepReturn:
    """Sends an annotation for the end of the test case.

    Defined as when the arm moves out of the way, so that the
    most recent image can show the board unoccluded.

    Returns:
      A StepReturn tuple.
    """
    t = time.time() - self._test_case_begin_ts
    annotation = logs_pb2.ClientAnnotation()
    self._set_proto_timestamp(annotation.point_measurement.timestamp,
                              time.time())
    annotation.point_measurement.space = ENV_ID
    annotation.point_measurement.name = "test_case_time"
    annotation.point_measurement.value.seconds = t
    return self._annotate(annotation)

  def _annotate(self, proto: logs_pb2.ClientAnnotation) -> StepReturn:
    """Sends an annotation using an action."""
    self._set_proto_timestamp(proto.associated_server_ts, self._last_server_ts)

    annotation_size = self.action_space["annotation"]["data"].shape[0]
    bs = proto.SerializeToString()
    enc = annotation_size * [256]
    enc[:len(bs)] = bs
    enc_ndarray = np.array(enc, dtype=np.int)
    action = {
        "annotation": {
            "disable": 0,
            "data": enc_ndarray
        }
    }
    return self._super_step(action)

  def _set_proto_timestamp(self, ts: timestamp_pb2.Timestamp,
                           t: float) -> None:
    """Sets the timestamp in a proto."""
    ts.seconds = int(t)
    ts.nanos = int((t % 1) * 1e9)

  def _go_to(self, pose: List[float], preemptive: bool = False) -> StepReturn:
    """Moves the arm synchronously to the given pose."""
    action = collections.OrderedDict({
        "arm":
            collections.OrderedDict({
                "command": 2,
                "pose": pose,
                "synchronous": 1,
                "use_linear": 1,
                "velocity": 0.7,
                "preemptive": 1 if preemptive else 0,
            })
    })
    return self._super_step(action)

  def _go_to_joints(self, joints: List[float]) -> StepReturn:
    """Moves the arm synchronously to the given joint angles."""
    action = collections.OrderedDict({
        "arm":
            collections.OrderedDict({
                "command": 1,
                "joint_angles": np.array(joints),
                "synchronous": 1,
                "use_linear": 1,
                "velocity": 0.5,
            })
    })
    return self._super_step(action)


def main(_: Any) -> None:
  if flags.FLAGS.instructor:
    ChatClient()

if __name__ == "__main__":
  flags.DEFINE_bool("instructor", False, "Run as the instructor.")
  app.run(main)
