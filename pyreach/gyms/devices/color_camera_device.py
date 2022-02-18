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

"""Implementation of PyReach Gym Color Camera Device."""

import sys
from typing import Any, Dict, List, Optional, Tuple

import gym  # type: ignore
import numpy as np  # type: ignore

import pyreach
from pyreach import calibration
from pyreach import color_camera
from pyreach import snapshot as lib_snapshot
from pyreach.gyms import color_camera_element
from pyreach.gyms import core as gyms_core
from pyreach.gyms.devices import reach_device


class ReachDeviceColorCamera(reach_device.ReachDevice):
  """Represents a Reach Color Camera.

  Attributes:
    observation_space: This is a Gym Dict Space that contains a "ts" and "color"
      options.  This attribute is read only.
  """

  def __init__(
      self, color_camera_config: color_camera_element.ReachColorCamera) -> None:
    """Initialize a Reach Color Camera.

    Initializes the Gym interface to a reach color camera.

    Args:
      color_camera_config: A color camera configuration.
    """
    reach_name: str = color_camera_config.reach_name
    shape: Tuple[int, int] = color_camera_config.shape
    force_fit: bool = color_camera_config.force_fit
    is_synchronous: bool = color_camera_config.is_synchronous
    calibration_enable: bool = color_camera_config.calibration_enable
    lens_model: Optional[str] = color_camera_config.lens_model
    link_name: Optional[str] = color_camera_config.link_name
    initial_stream_request_period: float = (
        color_camera_config.initial_stream_request_period)

    if len(shape) != 2:
      raise pyreach.PyReachError("ColorCamera shape is {shape}, not (DX,DY)")
    color_shape: Tuple[int, int, int] = shape + (3,)
    observation_dict: Dict[str, Any] = {
        "ts":
            gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
        "color":
            gym.spaces.Box(low=0, high=255, shape=color_shape, dtype=np.uint8),
    }
    if calibration_enable:
      lens_models: Tuple[str, ...] = ("fisheye", "pinhole")
      if lens_model not in lens_models:
        raise pyreach.PyReachError(
            f"Lens modle ('{lens_model}' not one of {lens_models}")
      calibration_space: gym.space.Dict = gym.spaces.Dict({
          "distortion":
              gym.spaces.Box(low=-sys.maxsize, high=sys.maxsize, shape=(5,)),
          "distortion_depth":
              gym.spaces.Box(low=-sys.maxsize, high=sys.maxsize, shape=(7,)),
          "extrinsics":
              gym.spaces.Box(low=-sys.maxsize, high=sys.maxsize, shape=(6,)),
          "intrinsics":
              gym.spaces.Box(low=-sys.maxsize, high=sys.maxsize, shape=(4,))
      })
      observation_dict["calibration"] = calibration_space
    action_space: gym.spaces.Dict = gym.spaces.Dict({})
    observation_space: gym.spaces.Dict = gym.spaces.Dict(observation_dict)

    super().__init__(reach_name, action_space, observation_space,
                     is_synchronous)
    self._color_camera: Optional[pyreach.ColorCamera] = None
    self._force_fit: bool = force_fit
    self._shape: Tuple[int, int, int] = color_shape
    self._calibration_enable: bool = calibration_enable
    self._lens_model: str = lens_model if lens_model else ""
    self._link_name: str = link_name if link_name else ""
    self._initial_stream_request_period: float = initial_stream_request_period

  def __str__(self) -> str:
    """Return string representation of a Reach Color Camera."""
    return f"ReachDeviceColorCamera('{self.config_name}','{self._reach_name}')"

  def do_action(
      self, action: gyms_core.Action,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Do nothing for an action.

    Args:
      action: Gym action space to process.  Should be empty.
      host: The PyReach host connect to.

    Returns:
        The list of gym action snapshots.
    """
    return ()

  def _get_color_camera(self, host: pyreach.Host) -> pyreach.ColorCamera:
    """Return the ColorCamera or raise a PyReach exception."""
    reach_name: str = self._reach_name
    if self._color_camera is None:
      with self._timers.select({"!agent*", "!gym*", "host.color"}):
        if reach_name not in host.color_cameras:
          camera_names: List[str] = list(host.color_cameras.keys())
          raise pyreach.PyReachError(
              "Color camera '{0}' needs to be one of {1}".format(
                  reach_name, camera_names))
        self._color_camera = host.color_cameras[reach_name]
        self._color_camera.start_streaming(self._initial_stream_request_period)
    return self._color_camera

  def validate(self, host: pyreach.Host) -> str:
    """Validate that color camera is operable."""
    try:
      _ = self._get_color_camera(host)
    except pyreach.PyReachError as pyreach_error:
      return str(pyreach_error)
    return ""

  def get_observation(self,
                      host: pyreach.Host) -> reach_device.ObservationSnapshot:
    """Return the Reach Color Camera Gym observation.

    Args:
      host: The reach host to use.

    Returns:
      Returns a Tuple containing the Gym Observation, a tuple of
      SnapshotReference objects and a tuple of SnapshotResponse objects.
      The Gym camera observation consists of dictionary with
      "ts" and "color", where "color" contains a 3-dimensional
      array (dx, dy, 3) containing the pixel values.

    Raises:
      pyreach.PyReachError when an image does not match the specified shape.

    """
    camera: pyreach.ColorCamera = self._get_color_camera(host)
    with self._timers_select({"!agent*", "!gym*", "host.color"}):
      color_frame: Optional[color_camera.ColorFrame] = camera.image()
    with self._timers_select({"!agent*", "gym.color"}):
      image: np.ndarray
      ts: float = 0.0
      if color_frame is None:
        image = np.zeros(self._shape, dtype=np.uint8)
      else:
        image = color_frame.color_image
        ts = color_frame.time
      if image.shape != self._shape:
        if self._force_fit:
          image = self._reshape_image(image, self._shape)
        else:
          raise pyreach.PyReachError(
              "Internal Error: Returned color camera image for "
              f"'{self.config_name}' is {image.shape}, "
              f"not desired {self._shape}")

      calibration_camera: calibration.CalibrationCamera
      if self._calibration_enable:
        if not color_frame:
          raise pyreach.PyReachError(
              "Internal Error: Missing image needed for calibration.")
        camera_calibration: Optional[calibration.Calibration] = (
            color_frame.calibration)
        if not camera_calibration:
          raise pyreach.PyReachError(
              "Internal Error: Image does not have camera calibration.")

        # Some mypy dancing here:
        calibration_device: Any = camera_calibration.get_device(
            color_frame.device_type, color_frame.device_name)
        assert isinstance(calibration_device, calibration.CalibrationCamera)
        calibration_camera = calibration_device

        if not calibration_camera:
          raise pyreach.PyReachError(
              "Internal Error: Image does not have a calibration device.")
        if not isinstance(calibration_camera, calibration.CalibrationCamera):
          raise pyreach.PyReachError(
              "Internal Error: Image does not have a calibration camera")
        if calibration_camera.width != self._shape[1]:
          raise pyreach.PyReachError(
              f"Internal Error: Width {calibration_camera.width} "
              f"!= {self._shape[1]}")
        if calibration_camera.height != self._shape[0]:
          raise pyreach.PyReachError(
              f"Internal Error: Width {calibration_camera.height} "
              f"!= {self._shape[0]}")
        if calibration_camera.lens_model != self._lens_model:
          raise pyreach.PyReachError(
              f"Internal Error: Width ''{calibration_camera.lens_model}' "
              f"!= '{self._lens_model}'")
        if calibration_camera.link_name != self._link_name:
          raise pyreach.PyReachError(
              f"Internal Error: Width '{calibration_camera.link_name}' "
              f"!= '{self._link_name}'")

      # mypy treats observation as immutable, disallowing incremental changes.
      observation: gyms_core.Observation
      if self._calibration_enable:
        assert isinstance(calibration_camera, calibration.CalibrationCamera)
        observation = {
            "ts": gyms_core.Timestamp.new(ts),
            "color": image,
            "calibration": {
                "distortion": np.array(calibration_camera.distortion),
                "distortion_depth":
                    (np.array(calibration_camera.distortion_depth)),
                "extrinsics": np.array(calibration_camera.extrinsics),
                "intrinsics": np.array(calibration_camera.intrinsics),
            }
        }
      else:
        observation = {
            "ts": gyms_core.Timestamp.new(ts),
            "color": image,
        }

      snapshot_reference: Tuple[lib_snapshot.SnapshotReference, ...] = ()
      if color_frame:
        snapshot_reference = (lib_snapshot.SnapshotReference(
            ts, color_frame.sequence),)
      return observation, snapshot_reference, ()

  def synchronize(self, host: pyreach.Host) -> None:
    """Synchronously fetch an image."""
    if self._color_camera:
      _ = self._color_camera.fetch_image()

  def start_observation(self, host: pyreach.Host) -> bool:
    """Start a synchronous observation."""
    camera: pyreach.ColorCamera = self._get_color_camera(host)
    with self._timers.select({"!agent*", "gym.color"}):
      self._add_update_callback(camera.add_update_callback)
    return True
