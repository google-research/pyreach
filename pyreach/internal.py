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

"""Internal functions used only by the Reach team for experimentation purpose.

WARNING: Please do not use the internal functions in the PyReach application
         code. Specifically, there is no commitment to maintain backward
         compatibility for CommandData and DeviceData structure. They are
         considered Reach system's internal data structure, which could be
         changed at any time without notification.
"""
import os
import threading
import time
from typing import Any, Callable, Dict, FrozenSet, List, Optional, Set, TextIO, Tuple

import numpy as np  # type: ignore

from pyreach import core
from pyreach.common.python import types_gen

# There are three timer classes used for collecting performance information.
#
# * Timer:
#   This class behaves like a stop watch and can be turned on and off.
#   It counts the number of times it has been started and stopped.
#
# * TimersSet:
#   This is a set of timers that can be enabled/disabled together
#   via a Ptyhon `with` statement.
#
# * Timers:
#   This is the top level class that creates all of the counter timers.
#   This is where all of the counters get a unique name.
#   Counter names are hierarchical separated by periods.
#
# The basic usage through out the code is:
#
#   # Define all of the timers once.
#   counter_timers = Timers({"gym", "host", "init", "arm", ...})
#
#   # Within a `with` statement.
#   with counter_timers.select({"arm"}):
#      # Do some Gym Arm stuff here.
#
#   Timer selects can be inside nested `with` statements.  At each nesting
#   level it is possible to start/stop a new collection of timers.  Upon
#   exiting the with statement, the if there is attempt to start a timer
#   that is already running.  In addition, it possible temporarly disable
#   a timer at a lower nesting level:
#
#   Example:
#
#     timers = Timers("gym", "step", "reset", "host", "arm", ...)
#     ...
#     with timers.select({"gym.arm"}):
#       # Only "gym" and "gym.arm" are on here.
#       with timers.select({"!gym*", "host.arm"}):
#         # "gym"/"gym.arm" are off and "host"/"host.arm" are on.
#         pass
#       # "gym"/"gym.arm" are resumed and "host"/"host.arm" are off.


class Timer(object):
  """A stop watch class that can be enabled/disabled."""

  def __init__(self,
               name: str,
               get_time: Callable[[], float] = time.time) -> None:
    """Init a Timer."""
    self.name: str = name
    self._calls: int = 0
    self._duration: float = 0.0
    self._lock: threading.Lock = threading.Lock()
    self._start_time: float = 0.0
    self._get_time: Callable[[], float] = get_time
    self.parent: Optional[Timer] = None

  @property
  def calls(self) -> int:
    """Return the number of timer calls."""
    with self._lock:
      return self._calls

  @property
  def enabled(self) -> bool:
    """Return whether the timer is enabled."""
    with self._lock:
      enabled: bool = self._start_time > 0.0
      return enabled

  def start(self, resume: bool = False) -> bool:
    """Start a timer.

    Args:
      resume: Optional argument that is set to True to indicate that the timer
        is being resumed.  This means that the call count is not incremented.

    Returns:
      Returns True if the counter transitions from stopped to running and
       False otherwise.

    """
    with self._lock:
      if self._start_time == 0.0:
        self._start_time = self._get_time()
        if not resume:
          self._calls += 1
        return True
      return False

  def stop(self) -> bool:
    """Stop a timer.

    Returns:
      Returns True if the counter transitions from running to stopped and
       False otherwise.

    """
    with self._lock:
      if self._start_time > 0.0:
        now: float = self._get_time()
        self._duration += now - self._start_time
        self._start_time = 0.0
        return True
      return False

  def result(self, now: float) -> Tuple[str, int, float]:
    """Return a result tuple.

    Args:
      now: The current time to use for running timers.

    Returns:
      Returns a 3-tuple containing the timer name, current number of calls, and
      current total duration.

    """
    with self._lock:
      delta: float = 0.0 if self._start_time == 0.0 else now - self._start_time
      return (self.name, self._calls, self._duration + delta)


class TimersSet(object):
  """A set of ReachTimers that can be enabled/disabled as a group."""

  def __init__(self,
               timer_ops: Tuple[Tuple[Timer, bool], ...],
               trace: str = "") -> None:
    """Init a ReachTimerSet.

    Args:
      timer_ops: A list of 2-tuples containing a timer and a start/stop flag.
      trace: Optional tracing string for debugging only.
    """
    self._timer_ops: Tuple[Tuple[Timer, bool], ...] = timer_ops
    self._trace = trace
    self._restore: List[Tuple[Timer, bool]] = []

  def __enter__(self) -> None:
    """Enable/disable a set of timers."""
    restore: List[Tuple[Timer, bool]] = self._restore
    del restore[:]
    trace: str = self._trace
    if trace:
      print(f"{trace}:=>__enter__()")
    for timer, enable in self._timer_ops:
      if enable:
        if trace:
          print(f"{trace}:start({timer.name})")
        if timer.start():
          restore.append((timer, True))
      else:
        if trace:
          print(f"{trace}:stop({timer.name})")
        if timer.stop():
          restore.append((timer, False))
    if trace:
      print(f"{trace}:<=__enter__()")

  def __exit__(self, exception_type: Any, exception_value: Any,
               trace_back: Any) -> None:
    """Restore a timers set to its previous state.."""
    trace: str = self._trace
    if trace:
      print(f"{trace}:=>__exit__()")
    for timer, enable in self._restore:
      if enable:
        if trace:
          print(f"{trace}::stop({timer.name})")
        timer.stop()
      else:
        if trace:
          print(f"{trace}::start({timer.name})")
        timer.start(resume=True)
    del self._restore[:]
    if trace:
      print(f"{trace}:<=__exit__()")


class Timers(object):
  """Performance measurement timers class."""

  def __init__(self,
               names: Set[str],
               get_time: Callable[[], float] = time.time) -> None:
    """Initialize a set of timers.

    Args:
      names: The timer names of all of the passed in as a Python set (see
        below.)
      get_time: Function to call to get the next time.  (Default: time.time()).
        A timer name is hierarchical with separated with a period ("."). The
        names set specifies a the leaf nodes specifies the leaf nodes of all of
        the timers in the tree.  All interior tree nodes are automatically
        created.
    """
    # Flesh out the timer tree and ensure each timer has a parent.
    counter_timers: Dict[str, Timer] = {}
    for name in names:
      name_parts: List[str] = name.split(".")
      for index in range(len(name_parts)):
        sub_name: str = ".".join(name_parts[:index + 1])
        if sub_name not in counter_timers:
          timer: Timer = Timer(sub_name, get_time=get_time)
          counter_timers[sub_name] = timer

    # Ensure that the parent pointers are all in place.
    for name, timer in counter_timers.items():
      index = name.rfind(".")
      if index > 0:
        parent_name: str = name[:index]
        parent: Timer = counter_timers[parent_name]
        timer.parent = parent

    empty_timer_ops: Tuple[Tuple[Timer, bool], ...] = ()
    self._cache: Dict[FrozenSet[str], TimersSet] = {}
    self._counter_timers: Dict[str, Timer] = counter_timers
    self._empty_counter_timers_set: TimersSet = (TimersSet(empty_timer_ops))
    self._enabled: bool = "PYREACH_PERF" in os.environ
    self._get_time: Callable[[], float] = get_time
    self._last_results: List[Tuple[str, int, float]] = []
    self._last_results_time: float = get_time()
    self._names: Set[str] = names
    self._start_time: float = get_time()

  def __getitem__(self, name: str) -> Timer:
    return self._counter_timers[name]

  def enabled(self) -> Set[str]:
    """Return the currently enabled timers."""
    return set([
        timer.name for timer in self._counter_timers.values() if timer.enabled
    ])

  def select(self, timers_patterns: Set[str], trace: str = "") -> TimersSet:
    """Return a list of timer operations derived from a set of timer patterns.

    Args:
      timers_patterns: A set of timer patterns, which each pattern of the form
        "[!]TIMER[*]".  A '!' means deactivate and a "*" matches all timers that
        start with "TIMER".
      trace: A tracing string used for debugging. (Default is "" to disable.)

    Returns:
      Returns a TimerSet containing the desired timers to
      activate/deactivate.

    Raises:
      PyReachError: if there are any conflicts or misssing timers.

    """
    if not self._enabled:
      return self._empty_counter_timers_set

    # Dump every 30 seconds if enabled.
    now: float = self._get_time()
    if now - self._last_results_time > 30.0:
      self.dump()
      self._last_results_time = now

    timer_patterns: FrozenSet[str] = frozenset(timers_patterns)
    if timer_patterns in self._cache:
      return self._cache[timer_patterns]

    counter_timers: Dict[str, Timer] = self._counter_timers
    activate_names: Set[str] = set()
    deactivate_names: Set[str] = set()

    timer_name: str
    timer_pattern: str
    for timer_pattern in timer_patterns:
      # Extract the timer name from a timer pattern of the form "[!]NAME[*]".
      deactivate: bool = timer_pattern.startswith("!")
      timer_name = timer_pattern[1:] if deactivate else timer_pattern
      wild_card: bool = timer_name.endswith("*")
      timer_name = timer_name[:-1] if wild_card else timer_name
      if timer_name not in counter_timers:
        raise core.PyReachError(f"'{timer_pattern}' is not a valid.")
      timer_names: Set[str] = {timer_name}

      # Find all of the matching wild card names.
      if wild_card:
        prefix_name: str = timer_name + "."
        key: str
        timer_names = timer_names.union({
            key for key in counter_timers.keys()
            if key.startswith(prefix_name) or key == timer_name
        })

      # Expand timer names to include all parents.
      all_timer_names: Set[str] = set()
      for timer_name in timer_names:
        timer: Optional[Timer] = counter_timers[timer_name]
        while timer:
          all_timer_names.add(timer.name)
          timer = timer.parent

      if deactivate:
        deactivate_names |= all_timer_names
      else:
        activate_names |= all_timer_names

    # Die if the pattern names conflict.
    name_conflicts: Set[str] = activate_names.intersection(deactivate_names)
    if name_conflicts:
      raise core.PyReachError(
          f"{timer_patterns} has timer conflicts of {name_conflicts}")

    timer_ops: List[Tuple[Timer, bool]] = []
    for timer_name in activate_names:
      timer_ops.append((counter_timers[timer_name], True))
    for timer_name in deactivate_names:
      timer_ops.append((counter_timers[timer_name], False))

    reach_counter_timers_set: TimersSet = TimersSet(
        tuple(timer_ops), trace=trace)
    self._cache[timer_patterns] = reach_counter_timers_set
    return reach_counter_timers_set

  def results(self, now: float = -1.0) -> List[Tuple[str, int, float]]:
    """Return the results of all the counters.

    Args:
      now: The current time to use for timers that are still running.

    Returns:
      Return a sorted list of Tuples that contain the counter name,
      number of calls, and counter duration.

    """
    if now < 0.0:
      now = self._get_time()
    results: List[Tuple[str, int, float]] = sorted([
        counter_timer.result(now)
        for counter_timer in self._counter_timers.values()
    ])
    return sorted(results)

  def dump(self) -> None:
    """Dump the current results."""

    def count_periods(name: str) -> int:
      """Count the number of periods in a name."""
      count: int = 0
      for c in name:
        if c == ".":
          count += 1
      return count

    if "PYREACH_PERF" in os.environ:
      pyreach_performance: str = os.environ["PYREACH_PERF"]

      now: float = self._get_time()
      total_time: float = now - self._start_time
      lines: List[str] = [f"PyReach Performance:  100% = {total_time:.9f} sec"]
      results: List[Tuple[str, int, float]] = self.results(now)

      max_name_length: int = 0
      result: Tuple[str, int, float]
      periods: int = 0
      for result in results:
        name, calls, duration = result
        periods = count_periods(name)
        max_name_length = max(max_name_length, len(name) + periods)

      padding: str = max_name_length * " "
      index: int
      for index, result in enumerate(results):
        name, calls, duration = result

        periods = count_periods(name)
        name_text: str = padding[:periods] + name + padding
        name_text = name_text[:max_name_length]

        percentage: float = 100.0 * duration / total_time
        percentage_text: str = f"        {percentage:.2f}%"[-8:]
        calls_text: str = f"        {calls}"[-6:]
        duration_text: str = f"        {duration:.9f} sec"[-17:]

        delta_calls: int = 0
        delta_duration: float = 0.0
        last_results: List[Tuple[str, int, float]] = self._last_results
        if last_results:
          result = last_results[index]
          delta_calls = calls - result[1]
          delta_duration = duration - result[2]

        delta_calls_text: str = f"        {delta_calls}"[-6:]
        delta_duration_text: str = f"        {delta_duration:.9f} sec"[-17:]

        lines.append(f"{name_text} {percentage_text} "
                     f"{calls_text} => {duration_text} "
                     f"{delta_calls_text} => {delta_duration_text}")
      self._last_results = results

      lines.append("")
      performance_text: str = "\n".join(lines)
      if pyreach_performance:
        performance_file: TextIO
        with open(pyreach_performance, "w") as performance_file:
          performance_file.write(performance_text)
      else:
        print(performance_text)


class InternalPlayback:
  """Playback is a playback object that manages playback of data."""

  def next_device_data(self) -> Optional[types_gen.DeviceData]:
    """Playback the next device-data object.

    Returns:
      Returns the DeviceData object loaded, if available.
    """
    raise NotImplementedError

  def device_data_available(self) -> bool:
    """Get if device-data is available.

    Returns:
      Returns if a further device-data object is available.
    """
    raise NotImplementedError

  def seek_device_data(
      self, timestamp: Optional[float],
      sequence: Optional[int]) -> Optional[types_gen.DeviceData]:
    """Seek the given device data and output it, if available.

    Args:
      timestamp: the timestamp to seek. If sequence number is not specified,
        will not return any data from before the specified time.
      sequence: the sequence number to seek. If specified, the exact sequence
        number, or any data after it will be returned.

    Returns:
      Returns the DeviceData object loaded, if found.
    """
    raise NotImplementedError


class Internal(object):
  """Internal interfance for the Reach system."""

  _timers: Timers = Timers(set(), time.time)  # Empty timers.

  @classmethod
  def set_timers(cls, timers: Timers) -> None:
    """Set the global timers."""
    cls._timers = timers

  @classmethod
  def get_timers(cls) -> Timers:
    """Get the global timers."""
    return cls._timers

  @property
  def playback(self) -> Optional[InternalPlayback]:
    """Get the playback object, if available."""
    raise NotImplementedError

  def load_color_image_from_data(self, msg: types_gen.DeviceData) -> np.ndarray:
    """Load the color image from a device-data.

    Args:
      msg: the data message to load from.

    Raises:
      FileNotFoundError: if the image file is not found.

    Returns:
      The image loaded into an-unwritable np.ndarray.
    """
    raise NotImplementedError

  def load_depth_image_from_data(self, msg: types_gen.DeviceData) -> np.ndarray:
    """Load the depth image from a device-data.

    Args:
      msg: the data message to load from.

    Raises:
      FileNotFoundError: if the image file is not found.

    Returns:
      The image loaded into an-unwritable np.ndarray.
    """
    raise NotImplementedError

  def async_send_command_data(
      self,
      command_data: types_gen.CommandData,
      callback: Optional[Callable[[types_gen.DeviceData], bool]] = None,
      finished_callback: Optional[Callable[[], None]] = None) -> None:
    """Send a command data asynchronously.

    Args:
      command_data: The command data to send.
      callback: The callback for tagged response messages. The command data
        message must be tagged if specified. The callback will stop if it
        returns true.
      finished_callback: Callback called after the callback is called.
    """
    raise NotImplementedError

  def send_key_value_request(self,
                             device_type: str,
                             device_name: str,
                             key: str,
                             tag: Optional[str] = None) -> str:
    """Send a key-value-request command data message to the host.

    Args:
      device_type: The device type of the message.
      device_name: The device name of the message.
      key: The key to request in the message.
      tag: Optional, if not set will be generated.

    Returns:
      The tag for the message.

    """
    raise NotImplementedError

  def add_device_data_callback(
      self,
      callback: Callable[[types_gen.DeviceData], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a listener to the DeviceData stream.

    Args:
      callback: Optional[Callable[[PyReachStatus], None]] = None,
      finished_callback: Optional[Callable[[], None]] = None

    Returns:
      A function that when called stops the callback.

    """
    raise NotImplementedError
