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
"""Shared utility functions for PyReach implementation."""

import bz2
import io
import logging
import time
from typing import Any, Optional, Union
import uuid

import numpy as np
import PIL  # type: ignore
from PIL import Image  # type: ignore

from google.protobuf import duration_pb2
from google.protobuf import timestamp_pb2
from pyreach.common.proto_gen import logs_pb2
from pyreach import core
from pyreach.common.python import types_gen
import cv2  # type: ignore


def copy_device_data(data: types_gen.DeviceData) -> types_gen.DeviceData:
  """Copy a device data, including images.

  Args:
    data: the device-data to copy.

  Returns:
    The new device-data.
  """
  if isinstance(data, ImagedDeviceData):
    image_data: ImagedDeviceData = data
    return ImagedDeviceData.with_images(image_data, image_data.color_image,
                                        image_data.depth_image)
  return types_gen.DeviceData.from_json(data.to_json())


def copy_command_data(cmd: types_gen.CommandData) -> types_gen.CommandData:
  """Copy a command data, including images.

  Args:
    cmd: the command-data to copy.

  Returns:
    The new command-data.
  """
  return types_gen.CommandData.from_json(cmd.to_json())


class ImagedDeviceData(types_gen.DeviceData):
  """DeviceData with images included in the object."""
  _color_image: Optional[bytes]
  _depth_image: Optional[bytes]

  def __init__(self,
               *args: Any,
               color_image: Optional[bytes] = None,
               depth_image: Optional[bytes] = None,
               **kwargs: Any) -> None:
    """Create the ImagedDeviceData from a DeviceData.

    Args:
      *args: arguments for types_gen.DeviceData.__init__
      color_image: the color image data, if available.
      depth_image: the depth image data, if available.
      **kwargs: keyword arguments for types_gen.DeviceData.__init__
    """
    super().__init__(*args, **kwargs)
    self._color_image = color_image
    self._depth_image = depth_image

  @property
  def color_image(self) -> Optional[bytes]:
    """Get the color image data."""
    return self._color_image

  @property
  def depth_image(self) -> Optional[bytes]:
    """Get the depth image data."""
    return self._depth_image

  @staticmethod
  def with_images(data: types_gen.DeviceData, color_image: Optional[bytes],
                  depth_image: Optional[bytes]) -> "ImagedDeviceData":
    kvdata = (data.__dict__).copy()
    kvdata["color_image"] = color_image
    kvdata["depth_image"] = depth_image
    if "_color_image" in kvdata:
      del kvdata["_color_image"]
    if "_depth_image" in kvdata:
      del kvdata["_depth_image"]
    return ImagedDeviceData(**kvdata)

  def to_proto(self) -> logs_pb2.DeviceData:
    """Convert AcquireImageArgs to proto."""
    proto = super().to_proto()
    if self._color_image is not None:
      if proto.HasField("color"):
        proto.color.color_data = self._color_image
      elif proto.HasField("color_depth"):
        proto.color_depth.color_data = self._color_image
      elif proto.HasField("prediction"):
        proto.prediction.color_data = self._color_image
      else:
        logging.warning("Could not write color data to proto for %s",
                        str(self.to_json()))
    if self._depth_image is not None:
      if proto.HasField("color_depth"):
        proto.color_depth.depth_data = self._depth_image
      else:
        logging.warning("Could not write depth data to proto for %s",
                        str(self.to_json()))
    return proto

  @staticmethod
  def from_proto(proto: logs_pb2.DeviceData) -> Optional[types_gen.DeviceData]:
    """Convert DeviceData proto to type object."""
    msg = types_gen.DeviceData.from_proto(proto)
    if not msg:
      return None
    color_data = None
    if proto.HasField("color") and proto.color.HasField(
        "color_data") and proto.color.color_data:
      color_data = proto.color.color_data
    if proto.HasField("color_depth") and proto.color_depth.HasField(
        "color_data") and proto.color_depth.color_data:
      color_data = proto.color_depth.color_data
    if proto.HasField("prediction") and proto.prediction.HasField(
        "color_data") and proto.prediction.color_data:
      color_data = proto.prediction.color_data
    depth_data = None
    if proto.HasField("color_depth") and proto.color_depth.HasField(
        "depth_data") and proto.color_depth.depth_data:
      depth_data = proto.color_depth.depth_data
    if color_data or depth_data:
      return ImagedDeviceData.with_images(msg, color_data, depth_data)
    return msg


def load_color_image_from_data(
    msg: Union[types_gen.DeviceData, logs_pb2.DeviceData]) -> np.ndarray:
  """Load the color image from a device-data.

  Args:
    msg: the data message to load from.

  Raises:
    FileNotFoundError: if the image file is not found.

  Returns:
    The image loaded into an-unwritable np.ndarray.
  """
  if isinstance(msg, logs_pb2.DeviceData):
    msg_from_proto = ImagedDeviceData.from_proto(msg)
    assert msg_from_proto
    msg = msg_from_proto
  assert isinstance(msg, types_gen.DeviceData)
  if not msg.color:
    raise FileNotFoundError
  fp: Union[str, io.BytesIO] = msg.color
  if isinstance(msg, ImagedDeviceData):
    imaged_msg: ImagedDeviceData = msg
    if imaged_msg.color_image is not None:
      fp = io.BytesIO(imaged_msg.color_image)
  try:
    with Image.open(fp) as image_file:
      color = np.array(image_file)
      if len(color.shape) == 2:
        color = np.tile(color[..., None], (1, 1, 3))  # grey to rgb.
      if color is None:
        raise FileNotFoundError
      color.flags.writeable = False
      return color
  except PIL.UnidentifiedImageError as error:
    logging.warning("Unidentified (incorrect format?) image: %s", str(error))
    raise FileNotFoundError from error


def load_depth_image_from_data(
    msg: Union[types_gen.DeviceData, logs_pb2.DeviceData]) -> np.ndarray:
  """Load the depth image from a device-data.

  Args:
    msg: the data message to load from.

  Raises:
    FileNotFoundError: if the image file is not found.

  Returns:
    The image loaded into an-unwritable np.ndarray.
  """
  if isinstance(msg, logs_pb2.DeviceData):
    msg_from_proto = ImagedDeviceData.from_proto(msg)
    assert msg_from_proto
    msg = msg_from_proto
  assert isinstance(msg, types_gen.DeviceData)
  if not msg.depth:
    raise FileNotFoundError
  if isinstance(msg, ImagedDeviceData):
    imaged_msg: ImagedDeviceData = msg
    if imaged_msg.depth_image is not None:
      nparray = np.asarray(bytearray(imaged_msg.depth_image), dtype="uint8")
      depth = cv2.imdecode(nparray, cv2.IMREAD_ANYDEPTH)
      if depth is None:
        raise FileNotFoundError
      depth.flags.writeable = False
      return depth
  if msg.depth.endswith(".bz2"):
    try:
      with bz2.open(msg.depth, "rb") as f:
        content = f.read()
        nparray = np.asarray(bytearray(content), dtype="uint8")
        depth = cv2.imdecode(nparray, cv2.IMREAD_ANYDEPTH)
        if depth is None:
          raise FileNotFoundError
        depth.flags.writeable = False
        return depth
    except OSError:
      raise FileNotFoundError from OSError
  depth = cv2.imread(msg.depth, cv2.IMREAD_ANYDEPTH)
  if depth is None:
    raise FileNotFoundError
  depth.flags.writeable = False
  return depth


def time_at_timestamp(timestamp_ms: int) -> float:
  """Convert millisecond Epoch timestamp to Python float time value.

  Args:
    timestamp_ms: Epoch timestamp in milliseconds.

  Returns:
    Python time value in float.

  """
  return float(timestamp_ms) / 1000.0


def timestamp_at_time(time_sec: float) -> int:
  """Convert Python float time value to millisecond Epoch timestamp.

  Args:
    time_sec: Python time value in seconds.

  Returns:
    Epoch timestamp in milliseconds.

  """
  return int(time_sec * 1000)


def timestamp_now() -> int:
  """Return the current epoch time in milliseconds."""
  return timestamp_at_time(time.time())


def generate_tag() -> str:
  """Generate a unique random tag."""
  return str(uuid.uuid4())


def pyreach_status_from_message(
    msg: types_gen.DeviceData) -> core.PyReachStatus:
  """Extract PyReachStatus from a DeviceData message.

  Args:
    msg: The source DeviceData instance.

  Returns:
    The decoded PyReachStatus object.

  """
  return core.PyReachStatus(
      time=time_at_timestamp(msg.ts),
      sequence=msg.seq,
      status=msg.status,
      script=msg.script,
      error=msg.error,
      progress=msg.progress,
      message=msg.message,
      code=msg.code)


def convert_pyreach_status(status: core.PyReachStatus) -> types_gen.Status:
  """Convert a PyReachStatus to a types_gen Status.

  Args:
    status: The PyReachStatus.

  Returns:
    The types_gen status.
  """
  return types_gen.Status(
      code=status.code,
      error=status.error,
      message=status.message,
      progress=status.progress,
      script=status.script,
      status=status.status)


def reverse_pyreach_status(status: types_gen.Status,
                           timestamp: float = 0.0,
                           sequence: int = 0) -> core.PyReachStatus:
  """Convert a PyReachStatus from a types_gen Status.

  Args:
    status: The types_gen Status.
    timestamp: The time this status is generated.
    sequence: the sequence number for the status.

  Returns:
    The PyReachStatus.
  """
  return core.PyReachStatus(
      time=timestamp,
      sequence=sequence,
      code=status.code,
      error=status.error,
      message=status.message,
      progress=status.progress,
      script=status.script,
      status=status.status)


def get_time_at_timestamp(timestamp: timestamp_pb2.Timestamp) -> float:
  """Get the time stored within a protobuf timestamp.

  Args:
    timestamp: the protobuf timestamp.

  Returns:
    The python float time value.
  """
  return float(timestamp.seconds) + (float(timestamp.nanos) / 1e9)


def set_timestamp_to_time(timestamp: timestamp_pb2.Timestamp,
                          ts: float) -> None:
  """Set the time stored within a protobuf timestamp.

  Args:
    timestamp: the protobuf timestamp.
    ts: the python float time value to set.
  """
  timestamp.seconds = int(ts)
  timestamp.nanos = int(ts * 1000000000) % 1000000000


def get_seconds_from_duration(duration: duration_pb2.Duration) -> float:
  """Get the duration stored within a protobuf duration.

  Args:
    duration: the protobuf duration.

  Returns:
    The python float time value.
  """
  return float(duration.seconds) + (float(duration.nanos) / 1e9)


def set_duration_to_seconds(duration: duration_pb2.Duration,
                            seconds: float) -> None:
  """Set the duration stored within a protobuf duration.

  Args:
    duration: the protobuf duration.
    seconds: the python float time value to set.
  """
  duration.seconds = int(seconds)
  duration.nanos = int(seconds * 1000000000) % 1000000000
