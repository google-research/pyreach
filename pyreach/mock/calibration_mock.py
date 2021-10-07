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

"""Robot mock calibration module."""

from typing import Optional, Tuple

from pyreach import calibration


class CalibrationMock(calibration.Calibration):
  """A collection of devices that is calibrated together."""

  def get_device(self, device_type: str,
                 device_name: str) -> Optional[calibration.CalibrationDevice]:
    """Get the device by type/name pair.

    Args:
      device_type: The device type for the calibration device.
      device_name: The device name for the calibartion device.

    Returns:
      The device on success and None otherwise

    """
    raise NotImplementedError

  def get_all_devices(self) -> Tuple[calibration.CalibrationDevice, ...]:
    """Get all devices in the calibration.

    Returns:
      The a tuple of all devices in the calibration.
    """
    raise NotImplementedError
