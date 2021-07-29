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

"""Program to run agent connected to robot/simulator."""

import pathlib
import queue
import signal
import subprocess
import sys
import threading
import time
from typing import Any, BinaryIO, cast, Dict, List, Optional, Tuple

from pyreach import core

Event = Tuple[str, Optional[str]]


def main() -> None:
  """Run the Agent Runner."""

  arguments: Tuple[str, ...] = tuple(sys.argv)
  if len(arguments) < 3:
    print("usage: python run_agent.py AGENT ROBOT_OR_SIM")
    print("where:")
    print("  AGENT is 2D, AUTOPICK, KIT, FOLD, ALL or explicit agent .py file")
    print("  ROBOT_SIM is SIM, ROBOT, BOTH, or explicit robot/sim name")
    return

  agent_argument: str = arguments[1]
  robot_sim_argument: str = arguments[2]
  print(f"agent_argument='{agent_argument}'")
  print(f"robot_argmuent='{robot_sim_argument}'")

  current_directory: pathlib.Path = pathlib.Path(".").absolute()
  agents: Dict[str, pathlib.Path] = {}
  if agent_argument in ("ALL", "AUTOPICK"):
    agents["singulate"] = (
        current_directory / "examples" / "singulation_autopick_agent.py")
  if agent_argument in ("ALL", "2D"):
    agents["2d"] = current_directory / "examples" / "benchmark_2d_agent.py"
  if agent_argument in ("ALL", "KIT"):
    agents["kit"] = (
        current_directory / "examples" / "benchmark_kitting_agent.py")
  if agent_argument in ("ALL", "FOLD"):
    agents["fold"] = (
        current_directory / "examples" / "benchmark_folding_agent.py")
  if agent_argument.endswith(".py"):
    agents["other"] = current_directory / pathlib.Path(agent_argument)
  if not agents:
    print(f"'{agent_argument}' is not 2D, KIT, FOLD, ALL, or a .py file")
    sys.exit(1)

  # Find out what robots and simulators are available.
  exact_match: str = ("" if robot_sim_argument in ("SIM", "ROBOT", "BOTH") else
                      robot_sim_argument)
  print(f"exact_match:'{exact_match}'")
  matches: Dict[str, List[str]] = find_matches(agents, exact_match)
  print(f"matches={matches}")

  # Determine whether to run the robot, simulator or both.
  workcell_modes: Tuple[bool, ...] = ()
  if robot_sim_argument == "BOTH":
    workcell_modes = (True, False)
  elif robot_sim_argument == "SIM":
    workcell_modes = (True,)
  elif robot_sim_argument == "ROBOT":
    workcell_modes = (False,)
  else:
    # When there is an exact match for the robot/simulator name, the value of
    # workcell_mode needs to be a tuple of length 1 to execution of the
    # appropriate robot/simulator.
    workcell_modes = (True,)

  agent_runner: AgentRunner
  if "other" in agents and exact_match:
    # Run just one explicit instance.
    try:
      agent_runner = AgentRunner(agent_argument, robot_sim_argument)
      agent_runner.run()
    except core.PyReachError as error:
      print(f"AgentRunner Exception: {error}")

  else:
    # First time: check for robot/simulator availability.
    # Second time: actually run robot/simulator.
    check_run: str
    for check_run in ("check", "run"):
      # Sweep through all of the agents that were specified on command line.
      agent_name: str
      agent_path: pathlib.Path
      is_sim: bool
      for is_sim in workcell_modes:
        workcell_type: str = "simulator" if is_sim else "robot"
        for agent_name, agent_path in agents.items():
          # See which simulators and robot match.
          match: List[str] = matches[agent_name]
          robot_sim: str = match[int(is_sim)]
          if check_run == "check":
            # Check only.
            if robot_sim:
              print(f"{agent_name}: will be run on {workcell_type} "
                    f"'{robot_sim}'")
            else:
              print(f"{agent_name}: {workcell_type} is not available!!!!!!!!!!")
          else:
            # Run robot/simulator.
            print(f"{agent_name}: Run on '{robot_sim}' {workcell_type}")
            try:
              agent_runner = AgentRunner(str(agent_path), robot_sim)
              agent_runner.run()
            except core.PyReachError as error:
              print(f"AgentRunner Exception: {error}")
      print("================")


def find_matches(agents: Dict[str, pathlib.Path],
                 exact_name: str) -> Dict[str, List[str]]:
  """Find available robots and simulators.

  Args:
    agents: The dictionary of agents to agent paths.
    exact_name: If a non-empty string, the exact simulator added to the search.

  Returns:
    Return a dictionary containing the available simulators and robots
    for all of the benchmarks.  If exact_name is matched, it is inserted
    into the returned dictionary with a key of "EXACT".

  """

  stdout_bytes: bytes = subprocess.check_output(["reach", "ls"])
  stdout_str: str = stdout_bytes.decode("utf-8")
  platforms: List[str] = stdout_str.split("\n")

  matches: Dict[str, List[str]] = {
      agent_name: ["", ""] for agent_name in agents.keys()
  }
  platform: str
  for platform in platforms:
    fields: List[str] = platform.split("\t")
    if len(fields) == 3:
      name: str = fields[0][5:].strip()
      is_sim: bool = name.find("sim") >= 0
      access: str = fields[1]
      accessible: bool = (
          access == "everyone/" or access.startswith("reach-lab/"))
      available: bool = fields[2].startswith("available")

      match: str
      for match in matches.keys():
        if accessible and available:
          if name.find(match) >= 0 or access.find(match) >= 0:
            # Stick with the first simulator that matches.
            if not matches[match][int(is_sim)]:
              matches[match][int(is_sim)] = name
          if exact_name and name == exact_name:
            matches[match][0] = exact_name
            matches[match][1] = name

  return matches


class AgentRunner:
  """Class for running an agent."""

  def __init__(self, agent_name: str, robot_name: str) -> None:
    """Initialize the AgentRunner class.

    Args:
      agent_name: The name of the program that implements the agent.
      robot_name: The name of the robot/simulator to run.

    Raises:
      core.PyReachError when an initialization error occurs.

    """
    # File path hacking.  This must be run from `pyreach` directory.
    pyreach_dir: pathlib.Path = pathlib.Path(".").absolute()
    if pyreach_dir.name != "pyreach":
      raise core.PyReachError(f"This program is in {pyreach_dir} directory, "
                              "not the '.../pyreach' directory")
    go_dir: pathlib.Path = pyreach_dir.parent / "go"
    if not go_dir.exists():
      raise core.PyReachError(f"Reach go directory '{go_dir}' does not exit")

    viewer_dir: pathlib.Path = pyreach_dir / "tools"
    if not go_dir.exists():
      raise core.PyReachError(f"Reach viewer directory '{viewer_dir}' "
                              "does not exit")

    viewer_main: pathlib.Path = viewer_dir / "async_viewer.py"
    if not viewer_main.exists():
      raise core.PyReachError(f"Viewer program '{viewer_main}' "
                              "does not exist.")

    self._agent_path: pathlib.Path = pathlib.Path(agent_name)
    self._agent_process: Optional[subprocess.Popen[Any]] = None
    self._agent_thread: Optional[threading.Thread] = None
    self._events: "queue.Queue[Tuple[str, Optional[str]]]" = queue.Queue()
    self._go_dir: pathlib.Path = go_dir
    self._lock: threading.Lock = threading.Lock()
    self._connect_process: Optional[subprocess.Popen[Any]] = None
    self._connect_thread_stderr: Optional[threading.Thread] = None
    self._connect_thread_stdout: Optional[threading.Thread] = None
    self._robot_name: str = robot_name
    self._viewer_dir: pathlib.Path = viewer_dir
    self._viewer_main: pathlib.Path = viewer_main
    self._viewer_process: Optional[subprocess.Popen[Any]] = None
    self._viewer_thread_stderr: Optional[threading.Thread] = None
    self._viewer_thread_stdout: Optional[threading.Thread] = None

  def run(self) -> None:
    """Run the robot/simulator, viewer, and agent."""

    signal.signal(signal.SIGINT, self.signal_catcher)

    self.connect_begin()
    self.events_process()
    self.shutdown()

  def signal_catcher(self, signal_number: int, _: Any) -> None:
    """Catch a signal.

    Args:
      signal_number: The signal number (e.g. SIGTERM.)
    """
    self._events.put(("signal", str(signal_number)))

  def events_process(self) -> None:
    """Process events in events queue."""

    # Process events from the events queue.
    while True:
      with self._lock:
        if (self._agent_process is None and self._connect_process is None and
            self._viewer_process is None):
          break

      event: Event = self._events.get()
      label: str
      value: Optional[str]
      label, value = event

      if label == "connect":
        if value is None:
          break
        self.viewer_begin()
        self.agent_begin()

      elif label == "viewer":
        pass

      elif label == "agent":
        break

      elif label == "signal":
        print(f"Signal {value} occurred")
        break

      else:
        assert False, f"Unexpected label '{label}'."

  def shutdown(self) -> None:
    """Shutdown all of the processes."""

    self.agent_shutdown()
    self.viewer_shutdown()
    self.connect_shutdown()

  def connect_begin(self) -> None:
    """Begin a connection."""
    with self._lock:
      commands: List[str] = ["reach", "connect", self._robot_name]
      self._connect_process = subprocess.Popen(
          commands,
          cwd=self._go_dir,
          stderr=subprocess.PIPE,
          stdout=subprocess.PIPE)

      self._connect_thread_stderr = threading.Thread(
          target=self.connect_events, args=(self._connect_process.stderr, True))
      self._connect_thread_stderr.daemon = True  # Shut down on program exit

      self._connect_thread_stdout = threading.Thread(
          target=self.connect_events,
          args=(self._connect_process.stdout, False))
      self._connect_thread_stdout.daemon = True  # Shut down on program exit

    self._connect_thread_stderr.start()
    self._connect_thread_stdout.start()

  def connect_events(self, pipe: BinaryIO, is_stderr: bool) -> None:
    """Generate a connect event when a simulator actually connects.

    Args:
      pipe: The pipe to read input from.
      is_stderr: True of the pipe is stderr, otherwiser stdout.
    """
    assert pipe is not None
    waiting: bool = True
    while True:
      line_bytes: Optional[bytes] = pipe.readline()
      if line_bytes is None:
        break
      line: str = line_bytes.decode("utf-8")
      if not line:
        break
      if line.endswith("\n"):
        line = line[:-1]
      if waiting:
        print(f"<<<<{line}>>>>" if is_stderr else f"[[[[{line}]]]]")
      if line.find("Connected to") >= 0:
        self._events.put(("connect", line))
        waiting = False
    self._events.put(("connect", None))

  def connect_shutdown(self) -> None:
    """Shutdown reach server connection."""
    with self._lock:
      connect_process: Optional[subprocess.Popen[Any]] = self._connect_process

    if connect_process:
      print("Sending SIGTERM to reach connect")
      connect_process.send_signal(signal.SIGINT)
      print("Waiting for reach connect to terminate")
      connect_process.wait()

    with self._lock:
      self._connect_process = None
      self._connect_thread_stderr = None
      self._connect_thread_stdout = None

  def viewer_begin(self) -> None:
    """Start the viewer."""
    with self._lock:
      viewer_process: Optional[subprocess.Popen[Any]] = self._viewer_process

    if not viewer_process:

      viewer_process = subprocess.Popen(
          ["python", str(self._viewer_main), "--reqfps=0"],
          cwd=self._viewer_dir,
          stdin=subprocess.PIPE,
          stderr=subprocess.PIPE,
          stdout=subprocess.PIPE)
      viewer_thread_stderr = threading.Thread(
          target=self.viewer_events, args=(viewer_process.stderr, True))
      viewer_thread_stderr.daemon = True
      viewer_thread_stdout = threading.Thread(
          target=self.viewer_events, args=(viewer_process.stdout, False))
      viewer_thread_stdout.daemon = True

      with self._lock:
        self._viewer_process = viewer_process
        self._viewer_thread_stderr = viewer_thread_stderr
        self._viewer_thread_stdout = viewer_thread_stdout

      viewer_thread_stderr.start()
      viewer_thread_stdout.start()

  def viewer_events(self, pipe: BinaryIO, is_stderr: bool) -> None:
    """Generate a viewer event when the viewer appears to be up.

    Args:
      pipe: The pipe to read input from.
      is_stderr: True of the pipe is stderr, otherwiser stdout.
    """
    assert pipe is not None
    waiting: bool = True
    while True:
      line_bytes: Optional[bytes] = pipe.readline()
      if line_bytes is None:
        break
      line: str = line_bytes.decode("utf-8")
      if not line:
        break
      if line.endswith("\n"):
        line = line[:-1]
      if True or waiting:
        s: bool = is_stderr
        print(f"<<<<{line}>>>> {s}" if is_stderr else f"[[[[{line}]]]] {s}")
      if line.startswith("CameraType:"):
        self._events.put(("viewer", line))
        waiting = False
    self._events.put(("viewer", None))

  def viewer_shutdown(self) -> None:
    """Shutdown the viewer."""

    with self._lock:
      viewer_process: Optional[subprocess.Popen[Any]] = self._viewer_process
      if viewer_process:
        assert isinstance(viewer_process, subprocess.Popen)
        # Send an escape character first, then try SIGINT.
        stdin = cast(BinaryIO, viewer_process.stdin)
        escape: bytes = b"\x1b"
        stdin.write(escape)
        time.sleep(1.0)
        viewer_process.send_signal(signal.SIGINT)
        viewer_process.wait()
      self._viewer_process = None
      self._viewer_thread_stderr = None
      self._viewer_thread_stdout = None

  def agent_begin(self) -> None:
    """Start the agent."""
    with self._lock:
      agent_path: pathlib.Path = self._agent_path
      agent_process: Optional[subprocess.Popen[Any]] = self._agent_process
      agent_thread: Optional[threading.Thread] = self._agent_thread

    if not agent_process:
      agent_process = subprocess.Popen(["python", agent_path])

    if not agent_thread:
      agent_thread = threading.Thread(target=self.agent_events, args=())
      agent_thread.daemon = True

    with self._lock:
      self._agent_process = agent_process
      self._agent_thread = agent_thread

    agent_thread.start()

  def agent_events(self) -> None:
    """Generate a agent event when the agent exits."""
    with self._lock:
      agent_process: Optional[subprocess.Popen[Any]] = self._agent_process
      events: "queue.Queue[Tuple[str, Optional[str]]]" = self._events

    assert isinstance(agent_process, subprocess.Popen), agent_process
    agent_process.wait()

    events.put(("agent", None))

  def agent_shutdown(self) -> None:
    """Shutdown the agent."""
    with self._lock:
      agent_process: Optional[subprocess.Popen[Any]] = self._agent_process

    if agent_process:
      agent_process.send_signal(signal.SIGINT)
      agent_process.wait()

    with self._lock:
      self._agent_process = None


if __name__ == "__main__":
  main()
