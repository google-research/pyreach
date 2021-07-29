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

"""Tests for ForceTorqueSensorMock."""

import unittest

from pyreach import force_torque_sensor
from pyreach.mock import force_torque_sensor_mock


class TestForceTorqueSensorMock(unittest.TestCase):

  def test_force_torque_sense(self) -> None:
    """Test the ForceTorqueSensorMock."""
    mock_force_torque_sensor: force_torque_sensor_mock.ForceTorqueSensorMock
    mock_force_torque_sensor = force_torque_sensor_mock.ForceTorqueSensorMock()
    assert isinstance(mock_force_torque_sensor,
                      force_torque_sensor_mock.ForceTorqueSensorMock)
    assert isinstance(mock_force_torque_sensor,
                      force_torque_sensor.ForceTorqueSensor)


if __name__ == "__main__":
  unittest.main()
