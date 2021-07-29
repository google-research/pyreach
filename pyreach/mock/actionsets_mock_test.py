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

"""Tests for ActionsMock."""

import unittest

from pyreach import actionsets
from pyreach.mock import actionsets_mock


class TestActionsMock(unittest.TestCase):
  """Test the TestLogger."""

  def test_actions(self) -> None:
    """Test the ActionsMock."""
    mock_actions: actionsets_mock.ActionsMock = actionsets_mock.ActionsMock()
    assert isinstance(mock_actions, actionsets.Actions)
    assert isinstance(mock_actions, actionsets_mock.ActionsMock)


if __name__ == "__main__":
  unittest.main()
