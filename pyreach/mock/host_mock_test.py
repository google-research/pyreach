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

"""Tests for HostMock."""

import unittest

# import numpy as np  # type: ignore

from pyreach import host
from pyreach.mock import host_mock


class TestMockHost(unittest.TestCase):
  """Test the MockHost class."""

  def test_host(self) -> None:
    """Test the host."""
    pyreach_host: host.Host = host_mock.HostMock()
    assert isinstance(pyreach_host, host.Host)


if __name__ == "__main__":
  unittest.main()