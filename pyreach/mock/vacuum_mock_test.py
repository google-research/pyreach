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

"""Tests for LoggerMock."""

import unittest

from pyreach import vacuum
from pyreach.mock import vacuum_mock


class TestVacuumMock(unittest.TestCase):
  """Test the TestLogger."""

  def test_vacuum(self) -> None:
    """Test the MockVacuum."""
    mock_vacuum: vacuum_mock.VacuumMock = vacuum_mock.VacuumMock()
    assert isinstance(mock_vacuum, vacuum_mock.VacuumMock)
    assert isinstance(mock_vacuum, vacuum.Vacuum)
    assert isinstance(mock_vacuum.device_name, str)
    assert isinstance(mock_vacuum.state, vacuum.VacuumState)
    assert isinstance(mock_vacuum.blowoff_state, vacuum.BlowoffState)
    assert isinstance(mock_vacuum.pressure_state, vacuum.VacuumPressure)
    assert isinstance(mock_vacuum.gauge_state, vacuum.VacuumGauge)
    assert mock_vacuum.support_blowoff
    assert mock_vacuum.support_gauge
    assert mock_vacuum.support_pressure


if __name__ == "__main__":
  unittest.main()
