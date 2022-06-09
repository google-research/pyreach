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

from typing import Optional
import unittest

from pyreach.common.proto_gen import workcell_io_pb2 as workcell_io
from pyreach.impl import device_base
from pyreach.impl import workcell_io_impl

WORKCELL_IO_JSON = (
    '{"Proto":'
    '"ChoKBnZhY3V1bRoCdXIoAjoKEghzdGFuZGFyZAolCg92YWN1dW0tcHJlc3N1c'
    'mUaAnVyKAE6DBIIc3RhbmRhcmQgAwogCgx2YWN1dW0tZ2F1Z2UaAnVyKAM6ChII'
    'c3RhbmRhcmQSCHN0YW5kYXJkEgxjb25maWd1cmFibGUSBHRvb2waDgoIc3RhbmR'
    'hcmQQASAHGg4KCHN0YW5kYXJkEAIgBxoSCgxjb25maWd1cmFibGUQASAHGhIKDG'
    'NvbmZpZ3VyYWJsZRACIAcaDgoIc3RhbmRhcmQQAyABGg4KCHN0YW5kYXJkEAQgA'
    'RoKCgR0b29sEAEgARoKCgR0b29sEAIgARoKCgR0b29sEAMgASIhChp2YWN1dW0t'
    'Z2F1Z2UtbWluLXRocmVzaG9sZB0AAPpEIhwKFXF1YWxpdHktbWluLXRocmVzaG9'
    'sZB0zMzM/IiIKG3NlbnNvci1oZWFsdGgtbWluLXRocmVzaG9sZB0zMzM/",'
    '"created":"2020-12-01T02:06:23.684718Z",'
    '"createdBy":"ytkj76DHYZbsjBVPObfm6dA8rPx1"'
    '}')


class TestPyReachWorkcellIO(unittest.TestCase):

  def test_workcell_io(self) -> None:
    device = workcell_io_impl.WorkcellIoDevice()
    key = device_base.KeyValueKey(
        device_type='settings-engine', device_name='', key='workcell_io.json')
    device.on_set_key_value(key, WORKCELL_IO_JSON)
    io_config: Optional[workcell_io.IOConfig] = device.get()
    self.assertIsNotNone(io_config)
    assert io_config
    self.assertEqual(
        io_config.io_space,
        ['standard', 'configurable', 'tool'])
    device.close()


if __name__ == '__main__':
  unittest.main()
