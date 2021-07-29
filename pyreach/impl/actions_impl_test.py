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

from pyreach.impl import actions_impl
from pyreach.impl import device_base
from pyreach.impl import test_data


class TestActionsImpl(unittest.TestCase):

  def test_actions_impl(self) -> None:
    rdev, dev = actions_impl.ActionDevice().get_wrapper()
    try:
      key = device_base.KeyValueKey(
          device_type="settings-engine", device_name="", key="actionsets.json")
      rdev.on_set_key_value(key, test_data.get_actionsets_json())
      actionsets: Optional[actions_impl.ActionsImpl] = dev.get()
      self.assertIsNotNone(actionsets)
      names = actionsets.action_names()  # type: ignore
      self.assertIsNotNone(names)
      self.assertEqual(names, ("FixedCalibration", "SingulateLeftBin",
                               "SingulateRightBin", "StowSuction1"))
    finally:
      rdev.close()


if __name__ == "__main__":
  unittest.main()
