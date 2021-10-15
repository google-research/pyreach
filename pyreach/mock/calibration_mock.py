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

  def __init__(self, device_type: str, device_name: str,
               link_name: str) -> None:
    """Initialize CalibrationMock.

    Args:
      device_type: The device type for the calibration device.
      device_name: The device name for the calibration device.
      link_name: The URDF link name associated with the calibration device.
    """
    super().__init__()
    self._device_type: str = device_type
    self._device_name: str = device_name
    self._link_name: str = link_name

  def get_device(self, device_type: str,
                 device_name: str) -> Optional[calibration.CalibrationDevice]:
    """Get the device by type/name pair.

    Args:
      device_type: The device type for the calibration device.
      device_name: The device name for the calibration device.

    Returns:
      The device on success and None otherwise

    """
    return calibration.CalibrationCamera(
        device_type=self._device_type,
        device_name=self._device_name,
        tool_mount=None,
        sub_type=None,
        distortion=(1.0, 2.0, 3.0, 4.0, 5.0),
        distortion_depth=(11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0),
        extrinsics=(21.0, 22.0, 23.0, 24.0, 25.0, 26.0),
        intrinsics=(31.0, 32.0, 33.0, 34.0),
        height=3,
        width=5,
        extrinsics_residual=None,
        intrinsics_residual=None,
        lens_model="fisheye",
        link_name=self._link_name)

  def get_all_devices(self) -> Tuple[calibration.CalibrationDevice, ...]:
    """Get all devices in the calibration.

    Returns:
      The a tuple of all devices in the calibration.
    """
    raise NotImplementedError
