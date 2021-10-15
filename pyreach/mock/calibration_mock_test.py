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

from pyreach import calibration
from pyreach.mock import calibration_mock


class TestLoggerMock(unittest.TestCase):
  """Test the TestLogger."""

  def test_logger(self) -> None:
    """Test the MockLogger."""
    mock_calibration: calibration_mock.CalibrationMock
    mock_calibration = calibration_mock.CalibrationMock("device_type",
                                                        "device_name",
                                                        "link_name")
    assert isinstance(mock_calibration, calibration_mock.CalibrationMock)
    assert isinstance(mock_calibration, calibration.Calibration)


if __name__ == "__main__":
  unittest.main()
