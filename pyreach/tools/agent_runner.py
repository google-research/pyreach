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
"""Agent runner class."""

import pathlib
import queue
import signal
import subprocess
import threading
import time
from typing import Any, BinaryIO, List, Optional, Tuple, Union, cast

from pyreach import core
from pyreach.impl import reach_tools_impl

Event = Tuple[str, Optional[str]]


class AgentRunner:
  """Class for running an agent."""

  def __init__(self,
               agent_name: Union[str, pathlib.Path],
               robot_name: str,
               with_viewer: bool,
               port_num: Optional[int] = None) -> None:
    """Initialize the AgentRunner class.

    Args:
      agent_name: The name of the program that implements the agent.
      robot_name: The name of the robot/simulator to run.
      with_viewer: Whether to start up a viewer or not.
      port_num: Optionally, pass a non default port to reach connect to.

    Raises:
      core.PyReachError when an initialization error occurs.

    """
    # File path hacking.  This must be run from `pyreach` directory.
    self._with_viewer: bool = with_viewer
    self._port_num = port_num if port_num else 50008
    test_directories = []
    cwd: pathlib.Path = pathlib.Path(".").absolute()
    test_directories.append(cwd)
    test_directories.extend(cwd.parents)
    test_directories.extend(pathlib.Path(__file__).parents)

    try:
      reach_exe_path = reach_tools_impl.download_reach_tool(None)
      self._webrtc_headless_exe_path = (
          reach_tools_impl.download_webrtc_headless(None))
    except reach_tools_impl.DownloadError as error:
      raise core.PyReachError(str(error))

    self._agent_path: pathlib.Path = pathlib.Path(agent_name)
    self._agent_process: Optional[subprocess.Popen[Any]] = None
    self._agent_thread: Optional[threading.Thread] = None
    self._agent_exit_code: Optional[int] = None
    self._events: "queue.Queue[Tuple[str, Optional[str]]]" = queue.Queue()
    self._reach_exe_path: pathlib.Path = reach_exe_path[0]
    self._reach_start_path: pathlib.Path = reach_exe_path[1]
    self._lock: threading.Lock = threading.Lock()
    self._connect_process: Optional[subprocess.Popen[Any]] = None
    self._connect_thread_stderr: Optional[threading.Thread] = None
    self._connect_thread_stdout: Optional[threading.Thread] = None
    self._robot_name: str = robot_name

    if self._with_viewer:
      self._viewer_process: Optional[subprocess.Popen[Any]] = None
      self._viewer_thread_stderr: Optional[threading.Thread] = None
      self._viewer_thread_stdout: Optional[threading.Thread] = None

  def run(self) -> int:
    """Run the robot/simulator, viewer, and agent."""

    signal.signal(signal.SIGINT, self.signal_catcher)

    try:
      self.connect_begin()
      self.events_process()
      self.shutdown()
      if self._agent_exit_code is None or self._agent_exit_code != 0:
        return -2
      return 0
    except ValueError as e:
      print(e)
      return -1

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
        if self._with_viewer:
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
    if self._with_viewer:
      self.viewer_shutdown()

    self.connect_shutdown()

  def connect_begin(self) -> None:
    """Begin a connection."""
    with self._lock:
      commands: List[str] = [
          str(self._reach_exe_path), "connect", "--device_data_port",
          str(self._port_num), "--webrtc_headless",
          str(self._webrtc_headless_exe_path), self._robot_name
      ]
      self._connect_process = subprocess.Popen(
          commands,
          executable=str(self._reach_exe_path),
          cwd=str(self._reach_start_path),
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
          ["python3", "-m", "pyreach.tools.async_viewer", "--reqfps=0"],
          cwd=self._reach_start_path,
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
      agent_process = subprocess.Popen(["python3", agent_path])

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

    return_code = None
    if agent_process:
      agent_process.send_signal(signal.SIGINT)
      return_code = agent_process.wait()

    with self._lock:
      if return_code is not None:
        self._agent_exit_code = return_code
      self._agent_process = None
