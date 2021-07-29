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

from pyreach.common.python import types_gen
from pyreach.impl import constraints_impl as impl
from pyreach.impl import test_data


class TestConstraintsImpl(unittest.TestCase):

  def test_constraints_impl(self) -> None:
    constraints_device = impl.ConstraintsDevice()
    try:
      constraints_device.start()
      constraints_device.enqueue_device_data(
          types_gen.DeviceData(
              device_type="settings-engine",
              data_type="key-value",
              key="workcell_constraints.json",
              value=test_data.get_workcell_constraints_json()))
      constraints_device.wait(1)

      constraints: Optional[impl.ConstraintsImpl] = constraints_device.get()
      self.assertIsNotNone(constraints)
    finally:
      constraints_device.close()


if __name__ == "__main__":
  unittest.main()
