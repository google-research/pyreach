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

import collections
from typing import Deque, List, Union  # pylint: disable=unused-import
import unittest
from unittest import mock

from pyreach.tools.lib import cv2_eventloop

# pylint: disable=protected-access


class TestCv2t(unittest.TestCase):
  """Test for CV2 event loop."""

  _keys_to_send: Deque[int]
  # pylint: disable=g-bare-generic
  _patchers: List  # type: ignore
  _waitkey_calls: int
  _cv2t: cv2_eventloop._SafeCv2

  def setUp(self) -> None:
    """Set up the test case."""
    super().setUp()
    self._keys_to_send = collections.deque()

    self._waitkey_calls = 0

    # Mock to replace cv2.waitKey().
    def mock_waitkey(unused_ms: int) -> int:
      self._waitkey_calls += 1
      if self._keys_to_send:
        return self._keys_to_send.popleft()
      return -1

    self._patchers = [mock.patch('cv2.waitKey', side_effect=mock_waitkey)]

    for m in self._patchers:
      m.start()

    self._cv2t = cv2_eventloop._SafeCv2()

  def tearDown(self) -> None:
    """Tear down the system."""
    super().tearDown()
    self._cv2t._stop()
    for m in self._patchers:
      m.stop()

  def _send_key(self, c: int) -> None:
    """Send a key.

    Args:
      c: the key to send.
    """
    # Simulates the eventloop getting a key from cv2.waitKey().
    self._keys_to_send.append(c)

  def test_key_iterator(self) -> None:
    """Test key iterator."""
    # Create some key iterators.
    iter1 = self._cv2t.key_iterator()
    iter2 = self._cv2t.key_iterator()
    # Wait to ensure the iterators are added.
    while len(self._cv2t._key_listeners) < 2:
      pass

    # Send some keys.
    self._send_key(97)
    self._send_key(98)
    self._send_key(99)

    # Check that they are received by both iterators.
    # Iterator 1 -
    self.assertEqual(next(iter1), 97)
    self.assertEqual(next(iter1), 98)
    self.assertEqual(next(iter1), 99)
    # Iterator 2 -
    self.assertEqual(next(iter2), 97)
    self.assertEqual(next(iter2), 98)
    self.assertEqual(next(iter2), 99)

    # Assert that Esc closes the interface and renders it inactive.
    self._send_key(27)
    while self._cv2t._key_listeners:
      pass

    # Since the event loop is now stopped, all iteraters including new ones,
    # will stop iteration.
    iter3 = self._cv2t.key_iterator()
    for iterator in [iter1, iter2, iter3]:
      with self.assertRaises(StopIteration):
        next(iterator)
    # The listeners list should still be empty, despite calling key_iterator.
    self.assertEqual(self._cv2t._key_listeners, [])

  def test_function_call(self) -> None:
    """Test function call."""
    fn = mock.Mock()
    # Queue a few function calls.
    self._cv2t.call(fn, 'Hello', param2='World')
    self._cv2t.call(fn, 'Hello there')
    for n in range(1000, 2000, 100):
      self._cv2t.call(fn, n=n)

    # Expected calls in order.
    expect_calls = [
        mock.call('Hello', param2='World'),
        mock.call('Hello there')
    ]
    for n in range(1000, 2000, 100):
      expect_calls.append(mock.call(n=n))

    while fn.call_count < len(expect_calls):
      # Give it time to make the actual calls.
      pass

    # Check that the calls happened in correct order.
    self.assertEqual(fn.call_args_list, expect_calls)
