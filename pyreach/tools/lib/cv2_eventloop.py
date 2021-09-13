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

"""OpenCV eventloop for thread-safe access to opencv GUI.

 Makes it possible for multiple threads to interact with cv2 UI.

 This gets rid of the problem here: https://github.com/opencv/opencv/issues/8407

 Normally cv2 insists that the thread which invokes waitKey, must also be the
 one to perform other UI operations such as imshow, namedWindow, etc.

 This module frees the developer from ensuring it for a multi-threaded
 application. Hence UI and waitKey can now be manipulated by two different,
 independent, threads.

 Example -
   cv2e = cv2_threadsafe.get_instance()

   # User thread 1: Get keys.
   for key in cv2e.key_iterator():
     print(key)

   # User thread 2: Can independently get the same keys.
   for key in cv2e.key_iterator():
     print(key)

   # User thread 3: Can modify cv UI without blocking.
   cv2e.call(cv2.namedWindow, "my window")

   cv2e.stop()  # To stop the event loop.

 NOTE: Non UI opencv methods, e.g. image manipulation etc. are safe to be called
 directly without requiring this module.
"""

import collections
import threading
from typing import Any, Callable, Deque, List, Optional, Tuple
import cv2  # type: ignore  # type: ignore


# How long to wait on cv2.waitKey() for the main event loop.
_CV2_EVENTLOOP_MS = 100

# Key on which the event loop will stop.
_STOP_KEY = 27  # Esc


class _KeyIterator:
  """Is really an iterator that returns keys as int's.

  Used as the return type for cv2e.key_iterator().
  Iteration ends when the cv2e object stops.
  """

  def __init__(self,
               add_key_listener: Callable[[Callable[[Optional[int]], None]],
                                          None], stop: Callable[[], None],
               timeout: Optional[float]) -> None:
    """Create the _KeyIterator.

    Args:
      add_key_listener: the key listener, called when a key is pressed.
      stop: the stop callback, called when the loop is stopped.
      timeout: timeout for each loop of the iterator.
    """
    self._keys: Deque[int] = collections.deque()
    self._event = threading.Event()
    self._lock = threading.Lock()
    self._timeout = timeout
    self._stopped = False
    self._stop = stop

    # Use the passed function to add the key listener.
    add_key_listener(self._on_key)

  def _on_key(self, c: Optional[int]) -> None:
    """Called on key press.

    Args:
      c: the key that was pressed. None if is stopping of the iterator.
    """
    if c is None:
      self._stopped = True
    if self._stopped:
      with self._lock:
        self._event.set()
      return
    with self._lock:
      self._event.set()
      assert c is not None  # To appease pytype.
      self._keys.append(c)

  def __iter__(self) -> '_KeyIterator':
    return self

  def __next__(self) -> int:
    while True:
      try:
        if not self._event.wait(self._timeout):
          # Timed out.
          return -1
        break
      except KeyboardInterrupt:
        self._stop()
    with self._lock:
      if self._stopped:
        raise StopIteration()
      c = self._keys.popleft()
      if not self._keys:
        self._event.clear()
      return c


class _SafeCv2:
  """Global thread-safe CV2 access object."""

  _key_listeners: List[Callable[[Optional[int]], None]]
  _command_queue: Deque[Tuple[Callable[..., None], Any, Any]]
  _running: bool
  _thread: threading.Thread

  def __init__(self) -> None:
    """Initialize the object."""
    # Methods to be called on a new key. Currently used internally for
    # key_iterator(). The method gets a None when the event loop ends.
    self._key_listeners = []

    # OpenCV function calls to be processed.
    self._command_queue = collections.deque()

    # Used to request the thread to stop.
    self._running = True

    self._thread = threading.Thread(target=self._run)
    self._thread.start()

  def call(self, fn: Callable[..., None], *args: Any, **kwargs: Any) -> None:
    """Queues an opencv method to be called.

    Note that the method will not be called immediately. If the args change by
    the time the method is called, it will use the modified arguments.

    Args:
      fn: An opencv function, e.g. cv2.namedWindow
      *args: Arguments to the method.
      **kwargs: Keyword args.
    """
    self._command_queue.append((fn, args, kwargs))

  def stop(self) -> None:
    """Stop the iterators."""
    self._command_queue.append((self._stop, [], {}))

  def _add_key_listener(self, listener: Callable[[Optional[int]],
                                                 None]) -> None:
    """Add a key listener.

    Args:
      listener: the listener.
    """
    if not self._running:
      listener(None)
    else:
      self._key_listeners.append(listener)

  def key_iterator(self, timeout_secs: Optional[float] = None) -> _KeyIterator:
    """Iterates keys.

    Does not generate -1.

    Multiple threads can use it if needed.

    Args:
      timeout_secs: How long to wait for key press in seconds. If None, will
        wait indefinitely. Will yield -1 whenever it times out.

    Returns:
      the key iterator.
    """
    return _KeyIterator(self._add_key_listener, self._stop, timeout_secs)

  def _stop(self) -> None:
    print('Stopping cv2 event loop.')
    self._running = False
    while self._key_listeners:
      listener = self._key_listeners.pop()
      listener(None)
    cv2.destroyAllWindows()

  def _run(self) -> None:
    """Run the openCV event loop."""
    while True:
      c = None
      try:
        c = cv2.waitKey(_CV2_EVENTLOOP_MS)
      except KeyboardInterrupt:
        c = _STOP_KEY
      if not self._running:
        break
      if c != -1:
        for handler in self._key_listeners:
          handler(c)
      while self._command_queue:
        fn, args, kwargs = self._command_queue.popleft()
        fn(*args, **kwargs)
      if c == _STOP_KEY:
        self._stop()


# Singleton instance.
_INSTANCE: Optional[_SafeCv2] = None


def get_instance() -> _SafeCv2:
  """Lazy initializes instance, and returns it."""
  global _INSTANCE  # pylint: disable=global-statement
  if _INSTANCE is None:
    _INSTANCE = _SafeCv2()
  return _INSTANCE
