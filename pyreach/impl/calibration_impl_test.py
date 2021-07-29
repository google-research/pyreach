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

"""Tests for utils.py."""

from typing import Optional
import unittest

from pyreach import calibration
from pyreach.impl import calibration_impl as cal
from pyreach.impl import device_base
from pyreach.impl import test_data


class TestActionsImpl(unittest.TestCase):

  def test_actions_impl(self) -> None:
    calibration_device = cal.CalDevice()
    key = device_base.KeyValueKey(
        device_type="settings-engine", device_name="", key="calibration.json")
    calibration_device.on_set_key_value(key, test_data.get_calibration_json())
    cal_object: Optional[calibration.Calibration] = calibration_device.get()
    self.assertIsNotNone(cal_object)
    if not cal_object:
      return None
    self.assertIsNotNone(cal_object.get_device("photoneo", ""))
    self.assertIsNotNone(cal_object.get_device("uvc", ""))
    self.assertIsNotNone(cal_object.get_device("ur", ""))
    self.assertIsNotNone(cal_object.get_device("object", "bodyTag"))
    calibration_device.close()


if __name__ == "__main__":
  unittest.main()
