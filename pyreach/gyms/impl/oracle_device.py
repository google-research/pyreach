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

"""Implementation of PyReach Gym Oracle Device."""

import logging
import sys
from typing import Callable, List, Optional, Tuple

import gym  # type: ignore
import numpy as np  # type: ignore

import pyreach
from pyreach import snapshot as lib_snapshot
from pyreach.gyms import core as gyms_core
from pyreach.gyms import oracle_element
from pyreach.gyms.impl import reach_device

TaggedRequest = Tuple[str, str, str, str, str]


class ReachDeviceOracle(reach_device.ReachDevice):
  """Represents a Reach Oracle.

  A Reach Oracle takes a depth image and returns a list of pick points.
  Only the first pick point is returned.

  Attributes:
    observation_space: The Gym observation space for the Oracle. This consists
      of a Gym Dict Space with "ts", "request", and "pick_point" sub Spaces.
      This attribute is read-only.
    action_space: A Gym Dict Space with a "request" entry. This attribute is
      read only. observation_space> A Gym Dict Space with "ts", "request" and
      "pick_point" entries.
  """

  EMPTY_TAGGED_REQUEST: TaggedRequest = ("", "", "", "", "")

  # Valid  "request" values:
  REQUEST_NONE: int = 0
  REQUEST_LEFT_BIN: int = 1
  REQUEST_RIGHT_BIN: int = 2
  REQUEST_MAX: int = max(REQUEST_NONE, REQUEST_LEFT_BIN, REQUEST_RIGHT_BIN)

  # Valid "response" values:
  RESPONSE_NONE: int = 0
  RESPONSE_SUCCESS: int = 1
  RESPONSE_FAIL: int = 2
  RESPONSE_MAX: int = max(RESPONSE_NONE, RESPONSE_SUCCESS, RESPONSE_FAIL)

  def __init__(self, oracle_config: oracle_element.ReachOracle) -> None:
    """Initialize a Reach Oracle.

    Args:
      oracle_config: The Oracle configuration information.
    """
    # Note a Box can store floats, but pixel indices are actually ints.
    reach_name: str = oracle_config.reach_name
    task_code: str = oracle_config.task_code
    intent: str = oracle_config.intent
    success_type: str = oracle_config.success_type
    is_synchronous: bool = oracle_config.is_synchronous

    action_space: gym.spaces.Dict = gym.spaces.Dict(
        {"request": gym.spaces.Discrete(ReachDeviceOracle.REQUEST_MAX + 1)})
    observation_space: gym.spaces.Dict = gym.spaces.Dict({
        "ts":
            gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
        "pick_point":
            gym.spaces.Box(low=-sys.maxsize, high=sys.maxsize, shape=(2,)),
        "request":
            gym.spaces.Discrete(ReachDeviceOracle.REQUEST_MAX + 1),
        "response":
            gym.spaces.Discrete(ReachDeviceOracle.RESPONSE_MAX + 1)
    })

    super().__init__(reach_name, action_space, observation_space,
                     is_synchronous)
    self._oracle: Optional[pyreach.Oracle] = None
    self._label: str = ""
    self._last_ts: float = -1.0
    self._request: int = ReachDeviceOracle.REQUEST_NONE
    self._tagged_request: TaggedRequest = ReachDeviceOracle.EMPTY_TAGGED_REQUEST
    self._pick_status: Optional[Callable[[], List[pyreach.Metric]]] = None
    self._prediction: Optional[pyreach.Prediction] = None
    self._task_code: str = task_code
    self._intent: str = intent
    self._success_type: str = success_type
    self._execute_action_status: Optional[pyreach.PyReachStatus] = None
    self._selected_point: Optional[pyreach.PredictionPoint] = None
    self._selected_pick_place_point: Optional[
        pyreach.PredictionPickPlacePoint] = None
    self._rejected_pick_points: List[pyreach.PredictionPoint] = []

  def __str__(self) -> str:
    """Return a string represenation of Reach Oracle."""
    return "ReachDeviceOracle('{0}:{1}')".format(self.config_name,
                                                 self._reach_name)

  # pylint: disable=unused-argument
  def reset(self,
            host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Called when the gym is reset."""
    self.disable_tagged_request()
    self._rejected_pick_points = []
    self._execute_action_status = None
    self._selected_point = None
    self._request = ReachDeviceOracle.REQUEST_NONE
    return ()

  def disable_tagged_request(self) -> None:
    """End sending tagged requests."""
    empty_tagged_request: TaggedRequest = ReachDeviceOracle.EMPTY_TAGGED_REQUEST
    if self._tagged_request:
      self._tagged_request = empty_tagged_request
      self._label = ""

  def _enable_tagged_request(self, label: str) -> None:
    """Start tagged requests."""
    tagged_request: TaggedRequest = ("pick", "pick", "sparse", self._task_code,
                                     label)
    if self._tagged_request != tagged_request:
      self._tagged_request = tagged_request
      self._label = label

  def _get_oracle(self, host: pyreach.Host) -> pyreach.Oracle:
    """Return the Color Camera.

    Args:
      host: The pyreach.Host to use for getting the camera.

    Returns:
      Returns the Oracle object.

    Raises:
      pyreach.PyReachError if the color camera is not available.

    """
    if self._oracle is None:
      if host.oracle is None:
        raise pyreach.PyReachError("There is no Oracle configured for host.")
      self._oracle = host.oracle
    return self._oracle

  def _get_latest_prediction(self, host: pyreach.Host) -> pyreach.Prediction:
    """Return a the most recent prediction.

    This code works around:
    * Multiple Images Using the Same Device-Data: PIPE-2552
    Args:
      host: Reach host.

    Raises:
      pyreach.PyReachError when neither oracle nor prediction is found.

    Returns:
      Requested prediction.
    """
    oracle: pyreach.Oracle = self._get_oracle(host)
    with self._timers.select({"!agent*", "!gym*", "host.oracle"}):
      prediction: Optional[pyreach.Prediction] = None
      prediction = oracle.prediction()

    prediction_try: int
    for prediction_try in range(3):
      tagged_request: TaggedRequest = self._tagged_request
      if tagged_request == ReachDeviceOracle.EMPTY_TAGGED_REQUEST:
        raise pyreach.PyReachError(
            "Internal Error: Oracle tagged request not set")

      with self._timers.select({"!agent*", "!gym*", "host.oracle"}):
        prediction = oracle.fetch_prediction(*tagged_request, timeout=30.0)
      if prediction:
        logging.debug(">>>>>>>>>>>>>>>>Got 'prediction' message @ %f",
                      prediction.time)
        break

    if not prediction:
      raise pyreach.PyReachError(
          "Internal Error: No Oracle prediction after {0} trys.".format(
              prediction_try + 1))
    if not prediction:
      raise pyreach.PyReachError(
          "Internal Error: Unable to get Oracle Prediction")
    return prediction

  def get_observation(self,
                      host: pyreach.Host) -> reach_device.ObservationSnapshot:
    """Return the Oracle Gym observation.

    Args:
      host: Reach host.

    Returns:
      Returns a Tuple containing the Gym Observation, a tuple of
      SnapshotReference objects and a tuple of SnapshotResponse objects.
      The observation is a Gym Dict Space with "ts", "pick_point",
      and "request" values.
    """
    # TODO(gramlich): the oracle does not return snapshots.
    with self._timers_select({"!agent*", "gym.oracle"}):
      ts: float = 0.0
      if self._request != ReachDeviceOracle.REQUEST_NONE:
        if not self._label:
          raise pyreach.PyReachError(
              "Internal Error: No bin selected for Oracle")
        tagged_request: TaggedRequest = self._tagged_request
        if tagged_request == ReachDeviceOracle.EMPTY_TAGGED_REQUEST:
          raise pyreach.PyReachError(
              "Internal Error: No tagged request for Oracle")
        try:
          prediction = self._get_latest_prediction(host)
          self._prediction = prediction
          assert prediction
        except pyreach.PyReachError as reach_error:
          raise pyreach.PyReachError from reach_error
        ts = prediction.time

      if not self._selected_point:
        pick_point = np.array([-1.0, -1.0])
      else:
        pick_point = np.array([self._selected_point.x, self._selected_point.y])

      execute_action_status: Optional[
          pyreach.PyReachStatus] = self._execute_action_status
      response: int = ReachDeviceOracle.RESPONSE_NONE
      if (execute_action_status and
          execute_action_status.status not in ("rejected", "aborted")):
        metrics: List[pyreach.Metric] = (
            self._pick_status() if self._pick_status else [])
        self._pick_status = None
        metric: pyreach.Metric
        for metric in metrics:
          key: str = metric.key
          if key == "operator/success":
            response = ReachDeviceOracle.RESPONSE_SUCCESS
          elif key == "operator/failure":
            response = ReachDeviceOracle.RESPONSE_FAIL
          elif key == "operator/attempt":
            pass
          else:
            logging.error("Gym Oracle: Unhandled metric: '%s'", key)
      elif self._selected_point:
        self._rejected_pick_points.append(self._selected_point)

      observation: gyms_core.Observation = {
          "ts": gyms_core.Timestamp.new(ts),
          "pick_point": pick_point,
          "request": self._request,
          "response": response,
      }
      return observation, (), ()

  def start_observation(self, host: pyreach.Host) -> bool:
    """Start a synchronous observation."""
    # The gym gets gets the first observation before getting the first action.
    # So, the first time through, there is no tagged request.
    # Thus, there is nothing to do if there is no tagged request.
    tagged_request: TaggedRequest = self._tagged_request
    if tagged_request == ReachDeviceOracle.EMPTY_TAGGED_REQUEST:
      return False
    return True

  def do_action(
      self, action: gyms_core.Action,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Perform an action for the Gym Oracle.

    Args:
      action: An Gym Dict Space with an "request" value. The "request" value is
        tagged to the return oracle request.
      host: Reach host.

    Returns:
        The list of gym action snapshots.
    """
    # TODO(gramlich): the oracle does not store actions.
    with self._timers_select({"!agent*", "gym.oracle"}):
      oracle: pyreach.Oracle
      if self._oracle is None:
        if host.oracle is None:
          raise pyreach.PyReachError("There is no Oracle configured for host.")
        self._oracle = host.oracle
      oracle = self._oracle
      assert oracle is not None

      if not isinstance(host.arm, pyreach.Arm):
        raise pyreach.PyReachError("Internal Error: Arm not found.")
      arm: pyreach.Arm = host.arm
      if not isinstance(host.depth_camera, pyreach.DepthCamera):
        raise pyreach.PyReachError("Internal Error: Oracle not found.")
      depth_camera: pyreach.DepthCamera = host.depth_camera

      try:
        action_dict: gyms_core.ActionDict = self._get_action_dict(action)
      except pyreach.PyReachError as runtime_error:
        raise pyreach.PyReachError from runtime_error

      with self._timers.select({"!agent*", "!gym*", "host.depth"}):
        color_depth = depth_camera.image()
        if color_depth is None:
          color_depth = depth_camera.fetch_image()

      if not color_depth:
        logging.warning("Failed to receive depth image. Ignoring.")
        return ()

      calibration = host.config.calibration
      if not calibration:
        logging.warning("Calibration is missing. Ignoring.")
        return ()

      constraints = host.config.constraint
      if not constraints:
        logging.warning("Constraints are missing. Ignoring.")
        return ()

      label: str = ""
      bin_name: str = ""
      request: int
      if "request" in action_dict:
        request = int(action_dict["request"])
        if request == ReachDeviceOracle.REQUEST_LEFT_BIN:
          label = "SingulateLeftBin"
          bin_name = "left"
        elif request == ReachDeviceOracle.REQUEST_RIGHT_BIN:
          label = "SingulateRightBin"
          bin_name = "right"
      if not label:
        return ()
      self._request = request
      self._enable_tagged_request(label)

      prediction: Optional[pyreach.Prediction] = self._prediction
      if not prediction:
        try:
          prediction = self._get_latest_prediction(host)
        except pyreach.PyReachError as reach_error:
          raise pyreach.PyReachError from reach_error
      assert prediction

      self._selected_point = None
      self._selected_pick_place_point = None
      self._execute_action_status = None
      selected_point_3d: Optional[List[pyreach.ActionInput]] = None
      if prediction:
        prediction_points = prediction.points
        prediction_pick_place_points = prediction.pick_place_points
        # Singulation support
        if prediction_points:
          inputs_3d: List[Tuple[np.ndarray, np.ndarray, np.ndarray]] = []
          for pt in prediction_points:
            point_normal = color_depth.get_point_normal(int(pt.x), int(pt.y))
            if point_normal is None:
              continue
            inputs_3d.append(
                (point_normal[2], point_normal[0], point_normal[1]))
          if not inputs_3d:
            logging.warning("Converting pick points to 3D failed. Ignoring.")
            return ()
          for i, point in enumerate(inputs_3d):
            pick_point: np.ndarray = point[1]
            if prediction_points[i] in self._rejected_pick_points:
              continue
            if constraints.is_point_in_object(pick_point, bin_name):
              self._selected_point = prediction_points[i]
              selected_point_3d = [
                  pyreach.ActionInput(
                      prediction_point=point, position=None, rotation=None)
              ]
              break
            self._selected_point = None
            self._execute_action_status = None
        # Kitting support
        elif prediction_pick_place_points:
          pick_place_pt: pyreach.PredictionPickPlacePoint
          pick_place_pt = prediction_pick_place_points[0]
          selected_point_3d = [
              pyreach.ActionInput(
                  prediction_point=None,
                  position=pick_place_pt.pick_position_3d,
                  rotation=pick_place_pt.pick_rotation_quat_3d),
              pyreach.ActionInput(
                  prediction_point=None,
                  position=pick_place_pt.place_position_3d,
                  rotation=pick_place_pt.place_rotation_quat_3d),
          ]
          self._selected_pick_place_point = pick_place_pt

      if ((self._selected_point or self._selected_pick_place_point) and
          self._intent == "pick"):
        metrics: pyreach.Metrics = host.metrics
        pick_id: str
        read_status: Callable[[], List[pyreach.Metric]]
        pick_id, read_status = metrics.start_pick()

        if not isinstance(selected_point_3d, list):
          raise pyreach.PyReachError(
              "Internal Error: Oracle no selected 3D point")
        with self._timers.select({"!agent*", "!gym*", "host.arm.execute"}):
          self._execute_action_status = arm.execute_action(
              label,
              selected_point_3d,
              intent=self._intent,
              success_type=self._success_type,
              pick_id=pick_id,
              use_unity_ik=True)
          self._pick_status = read_status
    return ()
