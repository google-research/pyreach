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

"""Calibration implementation."""
import json
import logging
import threading
from typing import List, Optional, Set, Tuple, Dict, Any

from pyreach import calibration
from pyreach.impl import device_base


class CalDevice(device_base.DeviceBase):
  """Calibration device that loads and caches the latest Calibration."""

  _calibration: Optional[calibration.Calibration]
  _calibration_lock: threading.Lock

  def __init__(self) -> None:
    """Construct a calibration device."""
    super().__init__()
    self._calibration = None
    self._calibration_lock = threading.Lock()

  def get_key_values(self) -> Set[device_base.KeyValueKey]:
    """Return the key used to load a calibration from the settings engine."""
    return {
        device_base.KeyValueKey(
            device_type="settings-engine",
            device_name="",
            key="calibration.json")
    }

  def get(self) -> Optional[calibration.Calibration]:
    """Get the latest calibration."""
    with self._calibration_lock:
      return self._calibration

  def on_set_key_value(self, key: device_base.KeyValueKey, value: str) -> None:
    """Process the calibration JSON to create a new Calibration object.

    Args:
      key: The key for the key/value pair as a KeyValueKey.
      value: The value of the key/value pair.
    """
    if key.device_type != "settings-engine" or key.device_name:
      return None
    if key.key != "calibration.json":
      return None
    if not value:
      with self._calibration_lock:
        self._calibration = None
      return None
    try:
      calibration_json = json.loads(value)
    except json.decoder.JSONDecodeError as decode_error:
      logging.warning("WARNING: calibration JSON invalid: %s", decode_error)
      return None
    if not isinstance(calibration_json, dict):
      logging.warning("calibration JSON was not a dictionary")
      return None
    if not isinstance(calibration_json.get("devices", []), list):
      logging.warning("calibration JSON 'devices' was not a list")
      return None
    devices: List[calibration.CalibrationDevice] = []
    for dev in calibration_json.get("devices", []):
      if not isinstance(dev, dict):
        logging.warning("calibration JSON device is not a dictionary")
        return None
      for key in dev:
        if key not in {"deviceType", "deviceName", "parameters"}:
          logging.warning("calibration JSON extra key:%s in %s", key, dev)
          return None
      if (not isinstance(dev.get("deviceType", ""), str) or
          not dev.get("deviceType", "")):
        logging.warning("calibration JSON deviceType invalid in %s", dev)
        return None
      if not isinstance(dev.get("deviceName", ""), str):
        logging.warning("calibration JSON deviceName invalid in %s", dev)
        return None
      if not isinstance(dev.get("parameters", {}), dict):
        logging.warning("calibration JSON parameters invalid in %s", dev)
        return None
      if dev.get("deviceType", "") in {"ur", "robot"}:
        robot = CalDevice._robot_device_from_json(
            dev.get("deviceType", ""), dev.get("deviceName", ""),
            dev.get("parameters", {}))
        if robot is None:
          return None
        devices.append(robot)
      elif dev.get("deviceType",
                   "") in {"photoneo", "uvc", "color-camera", "depth-camera"}:
        camera = CalDevice._camera_device_from_json(
            dev.get("deviceType", ""), dev.get("deviceName", ""),
            dev.get("parameters", {}))
        if camera is None:
          return None
        devices.append(camera)
      elif dev.get("deviceType", "") in {"object"}:
        obj = CalDevice._calibration_object_from_json(
            dev.get("deviceType", ""), dev.get("deviceName", ""),
            dev.get("parameters", {}))
        if obj is None:
          return None
        devices.append(obj)
      else:
        logging.warning("calibration contains invalid device in %s", dev)
        return None
    with self._calibration_lock:
      self._calibration = CalibrationImpl(devices)

  @classmethod
  def _robot_device_from_json(
      cls, device_type: str, device_name: str,
      json_data: Dict[str, Any]) -> Optional["calibration.CalibrationRobot"]:
    """Unmarshal Robot object from JSON.

    Args:
      device_type: device type
      device_name: device name
      json_data: JSON message for a robot calibration.

    Returns:
      Robot object or None.

    """
    dev = {
        "device_type": device_type,
        "device_name": device_name,
        "parameters": json_data
    }
    calibration_action: Optional[Tuple[Tuple[float, ...], ...]] = None
    if "calibrationAction" in json_data:
      if not isinstance(json_data["calibrationAction"], list):
        logging.warning(
            "calibrationAction is not a list of "
            "lists of floats in: %s", dev)
        return None
      for element_list in json_data["calibrationAction"]:
        if not isinstance(element_list, list):
          logging.warning(
              "calibrationAction is not list of "
              "lists of floats in: %s", dev)
          return None
        for element in element_list:
          if not isinstance(element, (int, float)):
            logging.warning(
                "calibrationAction is not a list of "
                "lists of floats in: %s", dev)
            return None
      calibration_action_list: List[List[float]] = (
          json_data["calibrationAction"])
      calibration_action = tuple(
          [tuple(floats) for floats in calibration_action_list])
    calibration_pose_cartesian: Optional[Tuple[float, ...]] = None
    calibration_pose_joints: Optional[Tuple[float, ...]] = None
    if "calibrationPose" in json_data:
      if not isinstance(json_data["calibrationPose"], dict):
        logging.warning("calibrationPose is not dictionary in: %s", dev)
        return None
      if "cartesian" not in json_data["calibrationPose"]:
        logging.warning("cartesian not in calibrationPose "
                        "dictionary in: %s", dev)
        return None
      if "joints" not in json_data["calibrationPose"]:
        logging.warning("joints not in calibrationPose dictionary in: %s", dev)
        return None
      if not isinstance(json_data["calibrationPose"]["cartesian"], list):
        logging.warning(
            "calibrationPose cartesian is not a list "
            "of floats in: %s", dev)
        return None
      if len(json_data["calibrationPose"]["cartesian"]) != 6:
        logging.warning(
            "calibrationPose cartesian is not a 6-element list "
            "of floats in: %s", dev)
        return None
      for element in json_data["calibrationPose"]["cartesian"]:
        if not isinstance(element, (float, int)):
          logging.warning(
              "calibrationPose cartesian is not a list of "
              "floats in: %s", dev)
          return None
      if not isinstance(json_data["calibrationPose"]["joints"], list):
        logging.warning(
            "calibrationPose joints is not a list of "
            "floats in: %s", dev)
        return None
      if len(json_data["calibrationPose"]["joints"]) != 6:
        logging.warning(
            "calibrationPose joints is not a 6-element list of "
            "floats in: %s", dev)
        return None
      for element in json_data["calibrationPose"]["joints"]:
        if not isinstance(element, (float, int)):
          logging.warning(
              "calibrationPose joints is not a list of "
              "floats in: %s", dev)
          return None
      floats: List[float] = (json_data["calibrationPose"]["cartesian"])
      calibration_pose_cartesian = tuple(floats)
      calibration_pose_joints_list: List[float] = (
          json_data["calibrationPose"]["joints"])
      calibration_pose_joints = tuple(calibration_pose_joints_list)

    if "extrinsics" not in json_data:
      logging.warning("extrinsics not in: %s", dev)
      return None
    if not isinstance(json_data["extrinsics"], list):
      logging.warning("extrinsics is not a list of floats in: %s", dev)
      return None
    if len(json_data["extrinsics"]) != 6:
      logging.warning("extrinsics is not a 6-element list of "
                      "floats in: %s", dev)
      return None
    for element in json_data["extrinsics"]:
      if not isinstance(element, (float, int)):
        logging.warning("extrinsics is not a list of floats in: %s", dev)
        return None
    if ("extrinsicsResidual" in json_data and
        not isinstance(json_data["extrinsicsResidual"], (float, int))):
      logging.warning("extrinsicsResidual is not a float in: %s", dev)
      return None
    if "urdf" not in json_data:
      logging.warning("urdf not in %s", dev)
      return None
    if not isinstance(json_data["urdf"], str):
      logging.warning("urdf not string in %s", dev)
      return None
    if ("toolMount" in json_data and
        not isinstance(json_data.get("toolMount", ""), str)):
      logging.warning("toolMount not string in %s", dev)
      return None
    if ("linkName" in json_data and
        not isinstance(json_data.get("linkName", ""), str)):
      logging.warning("linkName not string in: %s", dev)
      return None
    return calibration.CalibrationRobot(
        device_type,
        device_name,
        calibration_action=calibration_action,
        calibration_pose_cartesian=calibration_pose_cartesian,
        calibration_pose_joints=calibration_pose_joints,
        extrinsics=tuple(json_data["extrinsics"]),
        extrinsics_residual=json_data.get("extrinsicsResidual"),
        urdf=json_data["urdf"],
        tool_mount=json_data.get("toolMount"),
        link_name=json_data.get("linkName"),
        sub_type=json_data.get("subType"))

  @classmethod
  def _camera_device_from_json(
      cls, device_type: str, device_name: str,
      json_data: Dict[str, Any]) -> Optional["calibration.CalibrationCamera"]:
    """Unmarshal Camera object from JSON.

    Args:
      device_type: device type
      device_name: device name
      json_data: JSON message for a camera calibration.

    Returns:
      Camera object or None.
    """
    dev = {
        "device_type": device_type,
        "device_name": device_name,
        "parameters": json_data
    }
    distortion_depth: Optional[List[float]] = None
    if "distortionDepth" in json_data:
      if not isinstance(json_data["distortionDepth"], list):
        logging.warning("distortionDepth is not a list of floats in: %s", dev)
        return None
      for element in json_data["distortionDepth"]:
        if not isinstance(element, (float, int)):
          logging.warning("distortionDepth is not a list of floats in: %s", dev)
          return None
      distortion_depth = json_data["distortionDepth"]
    if "extrinsics" not in json_data:
      logging.warning("extrinsics not in: %s", dev)
      return None
    if not isinstance(json_data["extrinsics"], list):
      logging.warning("extrinsics is not a list of floats in: %s", dev)
      return None
    if len(json_data["extrinsics"]) != 6:
      logging.warning("extrinsics is not a 6-element list of "
                      "floats in: %s", dev)
      return None
    for element in json_data["extrinsics"]:
      if not isinstance(element, (float, int)):
        logging.warning("extrinsics is not a list of floats in: %s", dev)
        return None
    if "intrinsics" not in json_data:
      logging.warning("intrinsics not in: %s", dev)
      return None
    if not isinstance(json_data["intrinsics"], list):
      logging.warning("intrinsics is not a list of floats in: %s", dev)
      return None
    if len(json_data["intrinsics"]) != 4:
      logging.warning("intrinsics is not a 4-element list of "
                      "floats in: %s", dev)
      return None
    for element in json_data["intrinsics"]:
      if not isinstance(element, (float, int)):
        logging.warning("intrinsics is not a list of floats in: %s", dev)
        return None
    if "distortion" not in json_data:
      logging.warning("distortion not in: %s", dev)
      return None
    if not isinstance(json_data["distortion"], list):
      logging.warning("distortion is not a list of floats in: %s", dev)
      return None
    if len(json_data["distortion"]) != 5:
      logging.warning("distortion is not a 5-element list of "
                      "floats in: %s", dev)
      return None
    for element in json_data["distortion"]:
      if not isinstance(element, (float, int)):
        logging.warning("distortion is not a list of floats in: %s", dev)
        return None
    if ("extrinsicsResidual" in json_data and
        not isinstance(json_data["extrinsicsResidual"], (float, int))):
      logging.warning("extrinsicsResidual is not a float in: %s", dev)
      return None
    if ("intrinsicsResidual" in json_data and
        not isinstance(json_data["intrinsicsResidual"], (float, int))):
      logging.warning("intrinsicsResidual is not a float in: %s", dev)
      return None
    if ("toolMount" in json_data and
        not isinstance(json_data.get("toolMount", ""), str)):
      logging.warning("toolMount not string in: %s", dev)
      return None
    if ("linkName" in json_data and
        not isinstance(json_data.get("linkName", ""), str)):
      logging.warning("linkName not string in: %s", dev)
      return None
    if json_data.get("lensModel") not in {"pinhole"}:
      logging.warning("lensModel not string in: %s", dev)
      return None
    if "height" not in json_data or not isinstance(json_data["height"], int):
      logging.warning("height not int in: %s", dev)
      return None
    if "width" not in json_data or not isinstance(json_data["width"], int):
      logging.warning("width not int in: %s", dev)
      return None
    return calibration.CalibrationCamera(
        device_type,
        device_name,
        distortion=tuple(json_data["distortion"]),
        distortion_depth=tuple(distortion_depth) if distortion_depth else None,
        extrinsics=tuple(json_data["extrinsics"]),
        intrinsics=tuple(json_data["intrinsics"]),
        height=json_data["height"],
        width=json_data["width"],
        extrinsics_residual=json_data.get("extrinsicsResidual"),
        intrinsics_residual=json_data.get("instrinsicsResidual"),
        lens_model=json_data["lensModel"],
        tool_mount=json_data.get("toolMount"),
        link_name=json_data.get("linkName"),
        sub_type=json_data.get("subType"))

  @classmethod
  def _calibration_object_from_json(
      cls, device_type: str, device_name: str,
      json_data: Dict[str, Any]) -> Optional["calibration.CalibrationObject"]:
    """Unmarshal Object from JSON.

    Args:
      device_type: device type
      device_name: device name
      json_data: JSON message for an object calibration.

    Returns:
      Object or None.

    """
    dev = {
        "device_type": device_type,
        "device_name": device_name,
        "parameters": json_data
    }
    if "extrinsics" not in json_data:
      logging.warning("extrinsics not in %s", dev)
      return None
    if not isinstance(json_data["extrinsics"], list):
      logging.warning("extrinsics is not a list of floats in %s", dev)
      return None
    if len(json_data["extrinsics"]) != 6:
      logging.warning("extrinsics is not a 6-element list of floats in %s", dev)
      return None
    for element in json_data["extrinsics"]:
      if not isinstance(element, (float, int)):
        logging.warning("extrinsics is not a list of floats in %s", dev)
        return None
    if ("extrinsicsResidual" in json_data and
        not isinstance(json_data["extrinsicsResidual"], (float, int))):
      logging.warning("extrinsicsResidual is not a float in %s", dev)
      return None
    if "intrinsics" not in json_data:
      logging.warning("intrinsics not in %s", dev)
      return None
    if not isinstance(json_data["intrinsics"], list):
      logging.warning("intrinsics is not a list of floats in %s", dev)
      return None
    if len(json_data["intrinsics"]) != 3:
      logging.warning("intrinsics is not a 3-element list of floats in %s", dev)
      return None
    for element in json_data["intrinsics"]:
      if not isinstance(element, (float, int)):
        logging.warning("intrinsics is not a list of floats in %s", dev)
        return None
    if "toolMount" in json_data and not isinstance(json_data["toolMount"], str):
      logging.warning("toolMount not string in %s", dev)
      return None
    if ("linkName" in json_data and
        not isinstance(json_data.get("linkName", ""), str)):
      logging.warning("linkName not string in %s", dev)
      return None
    if "id" in json_data and not isinstance(json_data.get("id", ""), int):
      logging.warning("id not int in %s", dev)
      return None
    extrinsics_list: List[float] = json_data["extrinsics"]
    intrinsics_list: List[float] = json_data["intrinsics"]
    return calibration.CalibrationObject(
        device_type,
        device_name,
        extrinsics=tuple(extrinsics_list),
        extrinsics_residual=float(json_data.get("extrinsicsResidual", 0)),
        intrinsics=tuple(intrinsics_list),
        object_id=json_data.get("id", None),
        link_name=json_data.get("linkName", None),
        tool_mount=json_data.get("toolMount", None),
        sub_type=json_data.get("subType"))


class CalibrationImpl(calibration.Calibration):
  """A collection of devices that is calibrated together."""

  def __init__(self, devices: List[calibration.CalibrationDevice]) -> None:
    """Init the Calibration.

    Args:
      devices: A list of calibration devices.
    """
    self._devices = devices

  def get_device(self, device_type: str,
                 device_name: str) -> Optional[calibration.CalibrationDevice]:
    """Get the device by type/name pair.

    Args:
      device_type: The device type for the calibration device.
      device_name: The device name for the calibartion device.

    Returns:
      The device on success and None otherwise

    """
    for device in self._devices:
      if (device.device_type == device_type and
          device.device_name == device_name):
        return device
    return None

  def get_all_devices(self) -> List[calibration.CalibrationDevice]:
    """Get all devices in the calibration.

    Returns:
      The a list of all devices in the calibration.
    """
    return self._devices.copy()
