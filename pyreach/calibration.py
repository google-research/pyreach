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

"""Robot calibration module.

The calibration object captures information as described in the
Calibration 20190103 Design Doc.

Many parameters in this class inherits its meaning from OpenCV documentation:
  https://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html
"""

import dataclasses
from typing import Optional, Tuple, List


@dataclasses.dataclass(frozen=True)
class CalibrationDevice(object):
  """Base class for various calibration device.

  Attributes:
    device_type: Type of the device such as color-camera or robot.
    device_name: Name of the device being calibrated.
    tool_mount: Tool this device is mounted on.
    sub_type: Subtype of the device being calibrated.
  """

  device_type: str
  device_name: str
  tool_mount: Optional[str]
  sub_type: Optional[str]


@dataclasses.dataclass(frozen=True)
class CalibrationRobot(CalibrationDevice):
  """Calibration information of a robot.

  Attributes:
    calibration_action: The actions that are used to produce the calibration
      result.
    calibration_pose_cartesian: The Cartesian pose used for calibration.
    calibration_pose_joints: The joint configuration used for calibration.
    extrinsics: 6-DOF transform origin_T_robot or tool_T_robot if toolMount
      exists.
    extrinsics_residual: The residual cost of extrinsics calculation.
    urdf: URDF of the robot if available. Non-null value signals joint_space
      calibration.
    link_name: The URDF link name. If mounted on an intermediate joint.
      Otherwise assumed to be mounted at tool link.
  """

  calibration_action: Optional[Tuple[Tuple[float, ...], ...]]
  calibration_pose_cartesian: Optional[Tuple[float, ...]]
  calibration_pose_joints: Optional[Tuple[float, ...]]
  extrinsics: Tuple[float, ...]
  extrinsics_residual: Optional[float]
  urdf: str
  link_name: Optional[str]


@dataclasses.dataclass(frozen=True)
class CalibrationCamera(CalibrationDevice):
  """Calibration information of a camera device.

  Attributes:
    distortion: [k1, k2, p1, p2, k3] as in the OpenCV documentation.
    distortion_depth: Camera depth distortion [d1, d2, d3, d4, d5, d6, d7] as in
      the Calibration Design Doc.
    extrinsics: 6-DOF transform origin_T_camera or link_T_camera if
      toolMount/linkName exists
    intrinsics: [fx fy cx cy] as in OpenCV documentation.
    height: Image height, in pixels.
    width: Image width, in pixels.
    extrinsics_residual: Residual cost of extrinsics calculation.
    intrinsics_residual: Residual cost of intrinsics calculation.
    lens_model: pinhole or fisheye
    link_name: refers to URDF link, if mounted on an intermediate joint.
      Otherwise assumed to be mounted at "tool" link
  """

  distortion: Tuple[float, ...]
  distortion_depth: Optional[Tuple[float, ...]]
  extrinsics: Tuple[float, ...]
  intrinsics: Tuple[float, ...]
  height: float
  width: float
  extrinsics_residual: Optional[float]
  intrinsics_residual: Optional[float]
  lens_model: str
  link_name: Optional[str]


@dataclasses.dataclass(frozen=True)
class CalibrationObject(CalibrationDevice):
  """Calibration information of an object such as an April tag.

  Attributes:
    extrinsics: The extrinsics of the calibration object.
    extrinsics_residual: The residual cost of extrinsics calculation.
    intrinsics: The intrinsics of the calibration object. [x, y, z] which are
      width, height, and depth in meters.
    object_id: ID of the tag.
    link_name: The URDF link name. If mounted on an intermediate joint.
      Otherwise assumed to be mounted at tool linkLink name of the object.
  """

  extrinsics: Tuple[float, ...]
  extrinsics_residual: Optional[float]
  intrinsics: Tuple[float, ...]
  object_id: Optional[int]
  link_name: Optional[str]


class Calibration:
  """A collection of devices that is calibrated together."""

  def get_device(self, device_type: str,
                 device_name: str) -> Optional[CalibrationDevice]:
    """Get the device by type/name pair.

    Args:
      device_type: The device type for the calibration device.
      device_name: The device name for the calibartion device.

    Returns:
      The device on success and None otherwise

    """
    raise NotImplementedError

  def get_all_devices(self) -> List[CalibrationDevice]:
    """Get all devices in the calibration.

    Returns:
      The a list of all devices in the calibration.
    """
    raise NotImplementedError
