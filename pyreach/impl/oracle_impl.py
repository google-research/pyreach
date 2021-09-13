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

"""Internal structure for Oracle."""
import logging
import threading
from typing import Callable, Optional, Set, Tuple
from pyreach import core
from pyreach import oracle
from pyreach.common.python import types_gen
from pyreach.impl import device_base
from pyreach.impl import requester
from pyreach.impl import thread_util
from pyreach.impl import utils


class OracleDevice(requester.Requester[oracle.Prediction]):
  """Represents the Oracle pick point."""

  _device_type: str
  _device_name: str
  _request_lock: threading.Lock
  _request_enable: bool
  _request_in_progress: bool
  _request_intent: str
  _request_predication_type: str
  _request_request_type: str
  _request_task_code: str
  _request_label: str

  def __init__(self, device_type: str, device_name: str = "") -> None:
    """Init the Oracle.

    Args:
      device_type: The JSON device type.
      device_name: The JSON device name.
    """
    super().__init__()
    self._device_type = device_type
    self._device_name = device_name
    self._request_lock = threading.Lock()
    self._request_enable = False
    self._request_in_progress = False
    self._request_intent = ""
    self._request_prediction_type = ""
    self._request_request_type = ""
    self._request_task_code = ""
    self._request_label = ""

  def start_tagged_requests(self, intent: str, prediction_type: str,
                            request_type: str, task_code: str,
                            label: str) -> None:
    """Start tagged requests for the Oracle.

    Args:
      intent: The intent for the oracle.
      prediction_type: The prediction_type for the oracle.
      request_type: The request_type for the oracle.
      task_code: The task_code for the oracle.
      label: The label for the oracle.
    """
    with self._request_lock:
      self._request_enable = True
      self._request_intent = intent
      self._request_prediction_type = prediction_type
      self._request_request_type = request_type
      self._request_task_code = task_code
      self._request_label = label
    self._request_update()

  def stop_tagged_requests(self) -> None:
    """Stop tagged requests for the Oracle."""
    with self._request_lock:
      self._request_enable = False

  def get_cached_prediction(self) -> Optional[oracle.Prediction]:
    """Return a cached prediction if it is available."""
    with self._request_lock:
      cached_prediction = self.get_cached()
      if cached_prediction is None:
        return None
      if self._request_intent != cached_prediction.intent:
        return None
      if self._request_prediction_type != cached_prediction.prediction_type:
        return None
      if self._request_request_type != cached_prediction.request_type:
        return None
      if self._request_task_code != cached_prediction.task_code:
        return None
      if self._request_label != cached_prediction.label:
        return None
      return cached_prediction

  def _request_update(self) -> None:
    """Request an Oracle update.

    Handles streaming requests by requesting again after completion of a
    request.
    """
    with self._request_lock:
      if self.is_closed():
        return
      if not self._request_enable:
        return
      if self._request_in_progress:
        return
      self._request_in_progress = True
      self.get_prediction_callback(self._request_intent,
                                   self._request_prediction_type,
                                   self._request_request_type,
                                   self._request_task_code, self._request_label,
                                   self._on_request_completed,
                                   self._on_request_error)

  def _on_request_completed(self, prediction: oracle.Prediction) -> None:
    """Finish the on-going Oracle request."""
    self.set_cached(prediction)
    with self._request_lock:
      self._request_in_progress = False
    self._request_update()

  def _on_request_error(self, status: core.PyReachStatus) -> None:
    """Finish the on-going Oracle request with error."""
    with self._request_lock:
      self._request_in_progress = False
    self._request_update()

  def get_key_values(self) -> Set[device_base.KeyValueKey]:
    """Get the key-value keys that should be loaded from the server."""
    return set([device_base.KeyValueKey("settings-engine", "", "robot-name")])

  def get_prediction(self,
                     intent: str,
                     prediction_type: str,
                     request_type: str,
                     task_code: str,
                     label: str,
                     timeout: float = 15.0) -> Optional[oracle.Prediction]:
    """Return a current prediction (if available).

    Args:
      intent: The intent for the oracle.
      prediction_type: The prediction_type for the oracle.
      request_type: The request_type for the oracle.
      task_code: The task_code for the oracle.
      label: The label for the oracle.
      timeout: The optional maximum time to wait for the prediction. If not
        specified, it defaults to 15 seconds.

    Returns:
      The latest prediction, if available.
    """
    robot_id = self.get_key_value(
        device_base.KeyValueKey("settings-engine", "", "robot-name"))
    if robot_id is None:
      robot_id = ""
    q = self.send_tagged_request(
        types_gen.CommandData(
            ts=utils.timestamp_now(),
            device_type=self._device_type,
            device_name=self._device_name,
            data_type="inference-request",
            tag=utils.generate_tag(),
            intent=intent,
            prediction_type=prediction_type,
            request_type=request_type,
            task_code=task_code,
            label=label,
            robot_id=robot_id),
        timeout=timeout,
        expect_messages=1,
        expect_cmd_status=False)
    msgs = thread_util.extract_all_from_queue(q)
    if not msgs:
      return None
    if (msgs[0][0].data_type == "cmd-status" and
        msgs[0][0].status in {"rejected", "aborted"}):
      return None
    if len(msgs) != 1:
      logging.warning("expected a single message: %s", msgs)
    return self._prediction_from_message(msgs[0][0], intent, prediction_type,
                                         request_type, task_code, label)

  def get_prediction_callback(self,
                              intent: str,
                              prediction_type: str,
                              request_type: str,
                              task_code: str,
                              label: str,
                              callback: Optional[Callable[[oracle.Prediction],
                                                          None]] = None,
                              error_callback: Optional[Callable[
                                  [core.PyReachStatus], None]] = None,
                              timeout: float = 30) -> None:
    """Get a prediction via a callback.

    Args:
      intent: The intent for the oracle.
      prediction_type: The prediction_type for the oracle.
      request_type: The request_type for the oracle.
      task_code: The task_code for the oracle.
      label: The label for the oracle.
      callback: callback called when an image arrives. If the camera fails to
        load an image, callback will not be called.
      error_callback: optional callback called if there is an error.
      timeout: the timeout of the callback (default 30 seconds).
    """
    robot_id = self.get_key_value(
        device_base.KeyValueKey("settings-engine", "", "robot-name"))
    if robot_id is None:
      robot_id = ""
    q = self.send_tagged_request(
        types_gen.CommandData(
            ts=utils.timestamp_now(),
            device_type=self._device_type,
            device_name=self._device_name,
            data_type="inference-request",
            tag=utils.generate_tag(),
            intent=intent,
            prediction_type=prediction_type,
            request_type=request_type,
            task_code=task_code,
            label=label,
            robot_id=robot_id),
        timeout=timeout,
        expect_messages=1,
        expect_cmd_status=False)

    def transform(
        msg: types_gen.DeviceData,
        unused_supplement: Optional[oracle.Prediction]
    ) -> Optional[oracle.Prediction]:
      if msg.device_type != self._device_type:
        return None
      if msg.device_name != self._device_name:
        return None
      if msg.data_type != "prediction":
        return None
      return self._prediction_from_message(msg, intent, prediction_type,
                                           request_type, task_code, label)

    self.queue_to_error_callback(q, callback, error_callback, transform)

  def get_wrapper(self) -> Tuple["OracleDevice", "oracle.Oracle"]:
    """Get the wrapper for the device that should be shown to the user."""
    return self, OracleImpl(self)

  @classmethod
  def _prediction_from_message(cls, msg: types_gen.DeviceData, intent: str,
                               prediction_type: str, request_type: str,
                               task_code: str,
                               label: str) -> "Optional[oracle.Prediction]":
    """Convert JSON message into a Prediction.

    Args:
      msg: The device data message to convert.
      intent: The intent value from the inference-request.
      prediction_type: The prediction type value from the inference-request.
      request_type: The request_type for the inference-request.
      task_code: The task code value from the inference-request.
      label: The label value from the inference-request.

    Returns:
      Returns the oracle Prediction.

    """
    try:
      color = utils.load_color_image_from_data(msg)
    except FileNotFoundError:
      ts = msg.local_ts if msg.local_ts > 0 else msg.ts
      delta = utils.timestamp_now() - ts
      logging.warning(
          "oracle message missing file at %d ms time delta, file %s", delta,
          msg.color)
      return None
    color.flags.writeable = False
    pick_points = [
        oracle.PredictionPoint(point.x, point.y) for point in msg.pick_points
    ]
    pick_place_points = []
    compare_lengths = [
        len(msg.quaternion_3d),
        len(msg.place_position_3d),
        len(msg.place_quaternion_3d),
    ]
    if all([length == len(msg.position_3d) for length in compare_lengths]):
      for i in range(len(msg.position_3d)):
        point = oracle.PredictionPickPlacePoint(
            pick_position_3d=core.Translation(msg.position_3d[i].x,
                                              msg.position_3d[i].y,
                                              msg.position_3d[i].z),
            pick_rotation_quat_3d=core.Quaternion(msg.quaternion_3d[i].x,
                                                  msg.quaternion_3d[i].y,
                                                  msg.quaternion_3d[i].z,
                                                  msg.quaternion_3d[i].w),
            place_position_3d=core.Translation(msg.place_position_3d[i].x,
                                               msg.place_position_3d[i].y,
                                               msg.place_position_3d[i].z),
            place_rotation_quat_3d=core.Quaternion(
                msg.place_quaternion_3d[i].x, msg.place_quaternion_3d[i].y,
                msg.place_quaternion_3d[i].z, msg.place_quaternion_3d[i].w))
        pick_place_points.append(point)

    return oracle.Prediction(
        utils.time_at_timestamp(msg.ts), msg.seq,
        msg.device_type, msg.device_name, tuple(pick_points),
        tuple(pick_place_points), color, intent, prediction_type, request_type,
        task_code, label)


class OracleImpl(oracle.Oracle):
  """Represents the Oracle pick point."""

  _device: OracleDevice

  def __init__(self, device: OracleDevice) -> None:
    """Init the Oracle."""
    self._device = device

  def enable_tagged_request(self, intent: str, prediction_type: str,
                            request_type: str, task_code: str,
                            label: str) -> None:
    """Start tagged requests for the Oracle.

    Args:
      intent: The intent for the oracle.
      prediction_type: The prediction_type for the oracle.
      request_type: The request_type for the oracle.
      task_code: The task_code for the oracle.
      label: The label for the oracle.
    """
    self._device.start_tagged_requests(intent, prediction_type, request_type,
                                       task_code, label)

  def disable_tagged_request(self) -> None:
    """Stop tagged requests for the Oracle."""
    self._device.stop_tagged_requests()

  def prediction(self) -> Optional[oracle.Prediction]:
    """Return a cached prediction if it is available."""
    return self._device.get_cached_prediction()

  def add_update_callback(
      self,
      callback: Callable[[oracle.Prediction], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback for cached frames.

    Args:
      callback: Callback called when a prediction arrives. If it returns True,
        the callback will be stopped.
      finished_callback: Optional callback, called when the callback is stopped
        or if the oracle is closed.

    Returns:
      A function that when called stops the callback.

    """
    return self._device.add_update_callback(callback, finished_callback)

  def fetch_prediction(self,
                       intent: str,
                       prediction_type: str,
                       request_type: str,
                       task_code: str,
                       label: str,
                       timeout: float = 15.0) -> oracle.Prediction:
    """Fetch a new prediction.

    Args:
      intent: The intent for the oracle.
      prediction_type: The prediction_type for the oracle.
      request_type: The request_type for the oracle.
      task_code: The task_code for the oracle.
      label: The label for the oracle.
      timeout: The optional maximum time to wait for the prediction. If not
        specified, it defaults to 15 seconds.

    Raises:
      PyReachError if timeout.

    Returns:
      A new prediction.
    """
    result = self._device.get_prediction(intent, prediction_type, request_type,
                                         task_code, label, timeout)
    if result is None:
      raise core.PyReachError("Timeout")

    return result

  def async_fetch_prediction(self,
                             intent: str,
                             prediction_type: str,
                             request_type: str,
                             task_code: str,
                             label: str,
                             callback: Optional[Callable[[oracle.Prediction],
                                                         None]] = None,
                             error_callback: Optional[Callable[
                                 [core.PyReachStatus], None]] = None,
                             timeout: float = 30) -> None:
    """Get a Prediction via callback.

    Args:
      intent: The intent for the oracle.
      prediction_type: The prediction_type for the oracle.
      request_type: The request_type for the oracle.
      task_code: The task_code for the oracle.
      label: The label for the oracle.
      callback: callback called when an image arrives. If the camera fails to
        load an image, callback will not be called.
      error_callback: optional callback called if there is an error.
      timeout: the timeout of the callback (default 30 seconds).
    """
    self._device.get_prediction_callback(intent, prediction_type, request_type,
                                         task_code, label, callback,
                                         error_callback, timeout)
