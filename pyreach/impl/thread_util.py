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

"""Threading utilities."""
import queue
import threading
import time
import traceback
from typing import Any, Callable, Dict, Generic, List, Optional, Set, Tuple, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class ThreadCollection:
  """Represents a set of threads."""

  _lock: threading.Lock
  _threads: Set[threading.Thread]
  _name: str

  def __init__(self, name: str) -> None:
    """Init a ThreadCollection.

    Args:
      name: The name of the TreadCollection.
    """
    self._lock = threading.Lock()
    self._threads = set()
    self._name = name
    self._started = False

  def start(self) -> None:
    """Start must be called to add threads to the collection."""
    with self._lock:
      self._started = True

  def run(self, f: "Callable[..., None]", *args: Any, **kwargs: Any) -> None:
    """Run a thread in the ThreadCollection.

    Args:
      f: the function to be run within the thread. Thread terminates when the
        function returns. Function can take arguments, but must return None.
      *args: the arguments to the function.
      **kwargs: the keyword arguments to the function.

    Raises:
      RuntimeError: if the thread connection is not started.
    """
    with self._lock:
      if not self._started:
        raise RuntimeError("ThreadCollection used before starting.")
    thread = threading.Thread(
        target=self._run_thread,
        args=(f, args, kwargs),
        name="run thread " + self._name + ": " +
        "".join(traceback.format_stack()))
    with self._lock:
      self._threads.add(thread)
    thread.start()

  def poll(self, wait: Callable[[float], bool], period: float,
           f: "Callable[..., bool]", *args: Any, **kwargs: Any) -> None:
    """Call a function at given rate in thread in the ThreadCollection.

    Args:
      wait: function that waits for a time or terminates early. Is passed a
        float number of seconds to wait, and must return true if the thread
        should terminate.
      period: the minimum period between calls to the function. Time is adjusted
        based on the runtime of the function.
      f: the function to be run within the thread. Thread terminates when the
        function returns. Function can take arguments. If the function returns
        True, the poll thread will terminate.
      *args: the arguments to the function.
      **kwargs: the keyword arguments to the function.

    Raises:
      RuntimeError: if the thread connection is not started.
    """
    self.run(self._poll_thread, wait, period, f, args, kwargs)

  def join(self) -> None:
    """Join all the threads within the ThreadCollection."""
    while True:
      thread: Optional[threading.Thread] = None
      with self._lock:
        for t in self._threads:
          thread = t
          break
      if thread is None:
        return
      thread.join()

  def _run_thread(self, f: "Callable[..., None]", args: List[Any],
                  kwargs: Dict[str, Any]) -> None:
    """Run a thread and then remove it from the ThreadCollection.

    Args:
      f: the function to be run within the thread. Thread terminates when the
        function returns. Function can take arguments, but must return None.
      args: the arguments to the function.
      kwargs: the keyword arguments to the function.  Returns
    """
    try:
      f(*args, **kwargs)
    finally:
      with self._lock:
        self._threads.remove(threading.current_thread())

  def _poll_thread(self, wait: Callable[[float], bool], period: float,
                   f: "Callable[..., bool]", args: List[Any],
                   kwargs: Dict[str, Any]) -> None:
    """Poll a function periodically in a TreadhCollection.

    Args:
      wait: function that waits for a time or terminates early. Is passed a
        float number of seconds to wait, and must return true if the thread
        should terminate.
      period: the minimum period between calls to the function. Time is adjusted
        based on the runtime of the function.
      f: the function to be run within the thread. Thread terminates when the
        function returns. Function can take arguments. If the function returns
        True, the poll thread will terminate.
      args: the arguments to the function.
      kwargs: the keyword arguments to the function.  Returns
    """
    while True:
      start = time.time()
      if f(*args, **kwargs):
        return
      while True:
        runtime = time.time() - start
        delay = period - runtime
        if wait(max(delay, 0)):
          return
        if delay <= 0:
          break


def extract_all_from_queue(q: "queue.Queue[Optional[T]]") -> List[T]:
  """Return the contents of a queue.

  The queue is expected to contain a series of elements, and then None as the
  last element.

  Args:
    q: The Queue to empty.

  Returns:
    The list of queue objects.

  """
  msgs = []
  while True:
    try:
      msg = q.get(block=True)
      if msg is None:
        break
      msgs.append(msg)
    except queue.Empty:
      continue
  for _ in msgs:
    q.task_done()
  q.task_done()
  return msgs


def queue_to_callback(q: "queue.Queue[Optional[T]]",
                      callback: Optional[Callable[[T], None]],
                      finished_callback: Callable[[], None]) -> None:
  """Convert a queue to a series of callbacks.

  The queue is expected to contain a series of elements, and then None as the
  last element.

  Args:
    q: The queue to attach the callbacks too.
    callback: function called for each element of the queue.
    finished_callback: function called when the queue finished.  Returns
  """
  while True:
    msg = None
    try:
      msg = q.get(block=True)
    except queue.Empty:
      continue
    if msg is None:
      try:
        finished_callback()
      finally:
        q.task_done()
      return
    if callback is None:
      q.task_done()
    else:
      exception = True
      try:
        callback(msg)
        exception = False
      finally:
        q.task_done()
        if exception:
          queue_to_callback(q, None, finished_callback)
      if exception:
        return


class CallbackCapturer(Generic[T]):
  """CallbackCapturer is a testing tool for a Requester.

  This class is used to extract all data from a "callback" and
  "finish_callback" interface, as commonly used within the requester.
  """

  _queue: "queue.Queue[Optional[T]]"

  def __init__(self) -> None:
    """Init CallbackCapturer."""
    self._queue = queue.Queue()

  def callback(self, msg: T) -> None:
    """Pass a message to the tested object as the "callback" function."""
    self._queue.put(msg)

  def callback_and_then_finish(self, msg: T) -> None:
    """Pass message to "callback" function and then finish."""
    self.callback(msg)
    self.finished_callback()

  def finished_callback(self) -> None:
    """Mark the tested object as the "finished_callback" function."""
    self._queue.put(None)

  def callback_false(self, msg: T) -> bool:
    """Pass a message  the tested object as the "callback" function.

    Args:
      msg: message to the callback.

    Returns:
      Returns False instead of None, which is required in some cases.

    """
    self.callback(msg)
    return False

  def wait(self) -> List[T]:
    """Wait for the finished_callback() function to be called.

    Returns:
      all objects saved by callbacks.
    """
    return extract_all_from_queue(self._queue)


class DoubleCallbackCapturer(Generic[T, U]):
  """DoubleCallbackCapturer is a testing tool for a Requester.

  This class is used to extract all data from two callbacks (e.g. a "callback"
  and "error_callback") and capture the data.
  """

  # The actual type of _capturer is the type:
  # "CallbackCapturer[Tuple[Optional[T], Optional[U]]]"
  # Unfortunately, pytype does not support this data type currently, so we
  # have to remove the arguments and add a type: ignore for mypy.
  _capturer: "CallbackCapturer"  # type: ignore

  def __init__(self) -> None:
    """Init DoubleCallbackCapturer."""
    self._capturer = CallbackCapturer()

  def first_callback(self, msg: T) -> None:
    """Pass the first message to the tested object as the "callback" function."""
    self._capturer.callback((msg, None))

  def second_callback(self, msg: U) -> None:
    """Pass the second message to the tested object as the "callback" function."""
    self._capturer.callback((None, msg))

  def finished_callback(self) -> None:
    """Mark the tested object as the "finished_callback" function."""
    self._capturer.finished_callback()

  def first_callback_finish(self, msg: T) -> None:
    """Pass the first message to the tested object as the "callback" function."""
    self.first_callback(msg)
    self.finished_callback()

  def second_callback_finish(self, msg: U) -> None:
    """Pass the second message to the tested object as the "callback" function."""
    self.second_callback(msg)
    self.finished_callback()

  def wait(self) -> List[Tuple[Optional[T], Optional[U]]]:
    """Wait for the finished_callback() function to be called.

    Returns:
      all objects saved by callbacks.
    """
    return self._capturer.wait()


class CallbackManager(Generic[T]):
  """Manages callbacks."""

  _lock: threading.Lock
  _callbacks: List[Tuple[Callable[[T], bool], Callable[[], None]]]

  def __init__(self) -> None:
    """Init the CallbackManager."""
    self._lock = threading.Lock()
    self._callbacks = []

  def add_callback(
      self, callback: Callable[[T], bool],
      finished_callback: Optional[Callable[[], None]]) -> Callable[[], None]:
    """Add a callback to the CallbackManager.

    Args:
      callback: A function to be called whenever there is a new message.
      finished_callback: A function to be called when done.

    Returns:
      Cleanup function.
    """
    if finished_callback is None:
      tup = ((callback, lambda: None))
    else:
      tup = (callback, finished_callback)
    with self._lock:
      self._callbacks.append(tup)
    return lambda: self._remove_callback(tup)

  def _remove_callback(
      self, tup: Tuple[Callable[[T], bool], Callable[[], None]]) -> None:
    """Remove a callback.

    Args:
      tup: A tuple containing a callback and finish call back function.
    """
    # TODO: Why not two arguments?
    with self._lock:
      if tup not in self._callbacks:
        return
      self._callbacks = [
          callback for callback in self._callbacks if callback != tup
      ]
    tup[1]()

  def close(self) -> None:
    """Close a CallbackManager."""
    with self._lock:
      cbs = self._callbacks.copy()
      self._callbacks = []
    for cb in cbs:
      cb[1]()

  def call(self, parameter: T) -> None:
    """Call the Callback manager with a single parameter."""
    with self._lock:
      cbs = self._callbacks.copy()
    for cb in cbs:
      if cb[0](parameter):
        self._remove_callback(cb)
