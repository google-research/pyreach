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

"""Implementation of PyReach Gym Depth Camera Device."""

import sys
from typing import Any, Dict, List, Optional, Tuple, Union

import gym  # type: ignore
import numpy as np

import pyreach
from pyreach import calibration
from pyreach import core
from pyreach import depth_camera
from pyreach import snapshot as lib_snapshot
from pyreach.gyms import core as gyms_core
from pyreach.gyms import depth_camera_element
from pyreach.gyms.devices import reach_device


class ReachDeviceDepthCamera(reach_device.ReachDevice):
  """Represents a Reach Depth Camera.

  Attributes:
    observation_space: The Gym observation Space for the depth camera as
      dictionary with "ts", "depth" and (optionally) "color" fields. The depth
      is an 2D array (dx, dy) of unit16's.  If present, the color image is a 3D
      array (dx, dy, 3) of uint8's.  There is no action_space attribute set.
  """

  def __init__(
      self, depth_camera_config: depth_camera_element.ReachDepthCamera) -> None:
    """Initialize a Reach Depth Camera.

    Initializes the Gym interface to a Reach depth camera.
    Args:
      depth_camera_config: A the depth camera configuration information.
    """
    reach_name: str = depth_camera_config.reach_name
    shape: Tuple[int, int] = depth_camera_config.shape
    color_enabled: bool = depth_camera_config.color_enabled
    color_frame_rate: float = depth_camera_config.color_frame_rate
    depth_frame_rate: float = depth_camera_config.depth_frame_rate
    force_fit: bool = depth_camera_config.force_fit
    is_synchronous: bool = depth_camera_config.is_synchronous
    calibration_enable: bool = depth_camera_config.calibration_enable
    lens_model: Optional[str] = depth_camera_config.lens_model
    link_name: Optional[str] = depth_camera_config.link_name
    pose_enable: bool = depth_camera_config.pose_enable
    if depth_frame_rate <= 0.0:
      depth_frame_rate = 1.0
    if color_frame_rate <= 0.0:
      color_frame_rate = 10.0
    frame_rate: float = max(depth_frame_rate, color_frame_rate)

    if len(shape) != 2:
      raise pyreach.PyReachError(f"Depth camera has shape {shape}, not (DX,DY)")
    depth_shape: Tuple[int, int] = shape
    color_shape: Tuple[int, int, int] = shape + (3,)

    observation_dict: Dict[str, Any] = {
        "ts":
            gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
        "depth":
            gym.spaces.Box(
                low=0,
                high=65535,
                shape=depth_shape,
                dtype=np.uint16,
            ),
        "color_frame_rate":
            gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
        "depth_frame_rate":
            gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
    }
    if color_enabled:
      observation_dict["color"] = gym.spaces.Box(
          low=0, high=255, shape=color_shape, dtype=np.uint8)

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
    if pose_enable:
      observation_dict["pose"] = gym.spaces.Box(
          low=-sys.maxsize, high=sys.maxsize, shape=(6,))
    action_space: gym.spaces.Dict = gym.spaces.Dict({})
    observation_space: gym.spaces.Dict = gym.spaces.Dict(observation_dict)

    super().__init__(reach_name, action_space, observation_space,
                     is_synchronous, set())
    self._depth_shape: Tuple[int, int] = depth_shape
    self._depth_camera: Optional[pyreach.DepthCamera] = None
    self._force_fit: bool = force_fit
    self._color_shape: Tuple[int, int, int] = color_shape
    self._color_enabled: bool = color_enabled
    self._calibration_enable: bool = calibration_enable
    self._lens_model: str = lens_model if lens_model else ""
    self._link_name: str = link_name if link_name else ""
    self._color_frame_rate = color_frame_rate
    self._depth_frame_rate = depth_frame_rate
    self._frame_rate: float = frame_rate
    self._pose_enable: bool = pose_enable

  def __str__(self) -> str:
    """Return a string representation of ReachDeviceDepthCamera."""
    return "ReachDeviceDepthCamera('{0}':'{1}', {2}, {3}')".format(
        self.config_name, self._reach_name, self._depth_shape,
        self._color_enabled)

  def _get_depth_camera(self, host: pyreach.Host) -> pyreach.DepthCamera:
    """Return the DepthCamera.

    Args:
      host: The pyreach.Host to use for getting the camera.

    Returns:
      Returns the appropriate ColorCamera object.

    Raises:
      pyreach.PyReachError if the color camera is not available.

    """
    reach_name: str = self._reach_name
    if self._depth_camera is None:
      with self._timers.select({"!agent*", "!gym*", "host.depth"}):
        if reach_name not in host.depth_cameras:
          depth_camera_names: List[str] = list(host.depth_cameras.keys())
          raise pyreach.PyReachError(
              "Depth camera '{0}' needs to specify one of '{1}'".format(
                  reach_name, depth_camera_names))
        self._depth_camera = host.depth_cameras[reach_name]
        if host.playback is None:
          self._depth_camera.start_streaming(1.0 / self._frame_rate)
    return self._depth_camera

  def validate(self, host: pyreach.Host) -> str:
    """Validate that depth camera is operable."""
    try:
      _ = self._get_depth_camera(host)
    except pyreach.PyReachError as pyreach_error:
      return str(pyreach_error)
    return ""

  def do_action(
      self, action: gyms_core.Action,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Do nothing for an action.

    Args:
      action: Gym action space to process.  Should be empty
      host: The pyreach.Host connect to.

    Returns:
        The list of gym action snapshots.
    """
    return ()

  def get_observation(self,
                      host: pyreach.Host) -> reach_device.ObservationSnapshot:
    """Fetch the Reach Depth Camera Gym observation.

    Args:
      host: The host to get the observation from.

    Returns:
      Returns a Tuple containing the Gym Observation, a tuple of
      SnapshotReference objects and a tuple of SnapshotResponse objects.
      The observation space is a Gym Dict Space with
      "ts", "depth", and (if requested) "color" entries.
      If the depth image is not available yet, a zero timestamp
      is returned with no "depth" entry.

    Raises:
      pyreach.PyReachError if there are any mismatches between the specified
        color/depth image shapes and the actual ones obtained.

    """
    camera: pyreach.DepthCamera = self._get_depth_camera(host)
    with self._timers_select({"!agent*", "gym.depth"}):
      reach_name: str = self._reach_name
      force_fit: bool = self._force_fit
      depth_shape: Tuple[int, ...] = self._depth_shape
      color_shape: Tuple[int, ...] = self._color_shape

      ts: float = 0.0
      color_image: Optional[np.ndarray] = None
      depth_image: np.ndarray
      with self._timers.select({"!agent*", "!gym*", "host.depth"}):
        depth_frame: Optional[depth_camera.DepthFrame] = camera.image()

      snapshot_reference: Tuple[lib_snapshot.SnapshotReference, ...] = ()
      if depth_frame is None:
        depth_image = np.zeros(shape=self._depth_shape, dtype=np.uint16)
        if self._color_enabled:
          color_image = np.zeros(shape=self._color_shape, dtype=np.uint8)
      else:
        ts = depth_frame.time
        depth_image = depth_frame.depth_data
        if self._color_enabled:
          color_image = depth_frame.color_data
        snapshot_reference = (lib_snapshot.SnapshotReference(
            ts, depth_frame.sequence),)

      if depth_image.shape != depth_shape:
        if force_fit:
          depth_image = self._reshape_image(depth_image, depth_shape)
        else:
          raise pyreach.PyReachError(
              f"Returned depth camera image for '{reach_name}' "
              f"is {depth_image.shape}, not desired {depth_shape}")

      if color_image is not None and color_image.shape != color_shape:
        if force_fit:
          color_image = self._reshape_image(color_image, color_shape)
        else:
          raise pyreach.PyReachError(
              f"Returned color camera image for '{reach_name}' "
              f"is {color_image.shape}, not desired {color_shape}")

      observation: Dict[str, Any] = {
          "ts": gyms_core.Timestamp.new(ts),
          "color_frame_rate": np.array(self._color_frame_rate),
          "depth": depth_image,
          "depth_frame_rate": np.array(self._depth_frame_rate),
      }
      if color_image is not None:
        observation["color"] = color_image

      if self._calibration_enable:
        if not depth_frame:
          raise pyreach.PyReachError(
              "Internal Error: Missing image needed for calibration.")
        camera_calibration: Optional[calibration.Calibration] = (
            depth_frame.calibration)
        if not camera_calibration:
          raise pyreach.PyReachError(
              "Internal Error: Image does not have camera calibration.")
        calibration_camera: Union[None, calibration.CalibrationDevice,
                                  calibration.CalibrationCamera]
        calibration_camera = camera_calibration.get_device(
            depth_frame.device_type, depth_frame.device_name)

        if not calibration_camera:
          raise pyreach.PyReachError(
              "Internal Error: Image does not have a calibration device.")
        if not isinstance(calibration_camera, calibration.CalibrationCamera):
          raise pyreach.PyReachError(
              "Internal Error: Image does not have a calibration camera")
        if calibration_camera.width != depth_shape[1]:
          raise pyreach.PyReachError(
              f"Internal Error: Width {calibration_camera.width} "
              f"!= {depth_shape[1]}")
        if calibration_camera.height != depth_shape[0]:
          raise pyreach.PyReachError(
              f"Internal Error: Width {calibration_camera.height} "
              f"!= {depth_shape[0]}")
        if calibration_camera.lens_model != self._lens_model:
          raise pyreach.PyReachError(
              f"Internal Error: Width ''{calibration_camera.lens_model}' "
              f"!= '{self._lens_model}'")
        if calibration_camera.link_name != self._link_name:
          raise pyreach.PyReachError(
              f"Internal Error: Width '{calibration_camera.link_name}' "
              f"!= '{self._link_name}'")

        observation["calibration"] = {
            "distortion": np.array(calibration_camera.distortion),
            "distortion_depth": np.array(calibration_camera.distortion_depth),
            "extrinsics": np.array(calibration_camera.extrinsics),
            "intrinsics": np.array(calibration_camera.intrinsics),
        }
      if self._pose_enable:
        observation_pose: np.ndarray
        if isinstance(depth_frame, depth_camera.DepthFrame):
          pose: Optional[core.Pose] = depth_frame.pose()
          if isinstance(pose, core.Pose):
            observation_pose = np.array(pose.as_list())
          else:
            raise pyreach.PyReachError(
                f"DepthCamera {self.config_name} does not have a pose")
        else:
          raise pyreach.PyReachError(
              f"DepthCamera {self.config_name} does not have an image"
              "to extract a pose from")
        observation["pose"] = observation_pose

    return observation, snapshot_reference, ()

  def synchronize(self, host: pyreach.Host) -> None:
    """Synchronously fetch an image."""
    if self._depth_camera:
      _ = self._depth_camera.fetch_image()

  def start_observation(self, host: pyreach.Host) -> bool:
    """Start a synchronous observation."""
    camera: pyreach.DepthCamera = self._get_depth_camera(host)
    with self._timers.select({"!agent*", "gym.depth"}):
      self._add_update_callback(camera.add_update_callback)
    return True
