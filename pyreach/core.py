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
"""Basic types for PyReach."""

import dataclasses
import json
import math
from typing import Dict, Generic, ItemsView, Iterator, KeysView, TypeVar
from typing import List, Optional, Tuple, Union, ValuesView, cast

T = TypeVar("T")


class PyReachError(Exception):
  """Standard exception error for Pyreach."""

  pass


@dataclasses.dataclass(frozen=True)
class PyReachStatus:
  """Represents a status message.

  Attributes:
    time: The time this status is generated.
    sequence: the sequence number for the status.
    status: The status code such as rejected, done, executing, aborted.
    script: The name of the script/cmd/downlink that the status refers to.
    error: The error message.
    progress: The progress percentage between 0 and 100.
    message: The message for this status.
    code: The numerical status code.
  """

  time: float
  sequence: int = 0
  status: str = ""
  script: str = ""
  error: str = ""
  progress: float = 0.0
  message: str = ""
  code: int = 0

  def __str__(self) -> str:
    """Convert Status to a string."""
    return "Status(" + json.dumps({
        "time": self.time,
        "sequence": self.sequence,
        "status": self.status,
        "script": self.script,
        "error": self.error,
        "progress": self.progress,
        "message": self.message,
        "code": self.code
    }) + ")"

  def is_last_status(self) -> bool:
    """Returns true if the last status in a series of status messages."""
    return self.status in {"done", "rejected", "aborted"}

  def is_error(self) -> bool:
    """Returns true if the status is an error status."""
    if self.error:
      return True
    return self.status in {"rejected", "aborted"}


class ImmutableDictionary(Generic[T]):
  """Represents an Immutable Dictionary."""

  _data: Dict[str, T]

  def __init__(self, data: Dict[str, T]):
    """Init the Immutable dictionary."""
    self._data = data

  def __contains__(self, key: str) -> bool:
    """Determine if a key is in the Immutable Dictionary."""
    return key in self._data

  def __iter__(self) -> Iterator[str]:
    """Return an iterator for the Immutable Dictionary."""
    return self._data.__iter__()

  def __getitem__(self, key: str) -> T:
    """Return the value associated with the key."""
    return self._data[key]

  def get(self, key: str, default: Optional[T] = None) -> Optional[T]:
    """Return the Key value if present, otherwise the default."""
    return self._data.get(key, default)

  def values(self) -> ValuesView[T]:
    """Return the data values."""
    return self._data.values()

  def items(self) -> ItemsView[str, T]:
    """Return the data items."""
    return self._data.items()

  def keys(self) -> KeysView[str]:
    """Return the dictionary keys."""
    return self._data.keys()

  def __len__(self) -> int:
    """Get the length of the dictionary."""
    return len(self._data)


@dataclasses.dataclass(frozen=True)
class Translation(object):
  """A data class that represents a 3D translation.

  Values in meters. Default to no translation.
  """
  x: float = 0
  y: float = 0
  z: float = 0

  def as_tuple(self) -> Tuple[float, float, float]:
    """Return the translation as a tuple.

    Returns:
      The translation as a three-element (x, y, z) tuple.
    """
    return (self.x, self.y, self.z)

  def as_list(self) -> List[float]:
    """Return the translation as a list.

    Returns:
      The translation as a three-element (x, y, z) list.
    """
    return list(self.as_tuple())

  @classmethod
  def from_tuple(cls, translation: Tuple[float, float, float]) -> "Translation":
    """Return translation from a tuple.

    Args:
      translation: The translation as a three-element (x, y, z) tuple.

    Returns:
      The translation.
    """
    return Translation(x=translation[0], y=translation[1], z=translation[2])

  @classmethod
  def from_list(cls, translation: List[float]) -> "Translation":
    """Return translation from a list.

    Args:
      translation: The translation as a three-element (x, y, z) list.

    Raises:
      ValueError: if the list is not a three-element list.

    Returns:
      The translation.
    """
    if len(translation) != 3:
      raise ValueError("Translation must be three elements.")
    translation_tuple: Tuple[float, float,
                             float] = cast(Tuple[float, float, float],
                                           tuple(translation))
    return cls.from_tuple(translation_tuple)


@dataclasses.dataclass(frozen=True)
class AxisAngle(object):
  """Rodriguez axis-angle representation of an orientation.

  The axis is the direction of the vector. The angle is the norm of the vector
  in radians. Rotation uses the right-hand rule. The angle can be any value,
  not restricted between [-pi, pi).

  Default to no rotation.
  """
  rx: float = 0
  ry: float = 0
  rz: float = 0

  def as_tuple(self) -> Tuple[float, float, float]:
    """Return the axis-angle rotation as a tuple.

    Returns:
      The rotation as a three-element (rx, ry, rz) tuple.
    """
    return (self.rx, self.ry, self.rz)

  def as_list(self) -> List[float]:
    """Return the axis-angle rotation as a list.

    Returns:
      The rotation as a three-element (rx, ry, rz) list.
    """
    return list(self.as_tuple())

  @classmethod
  def from_tuple(cls, rotation: Tuple[float, float, float]) -> "AxisAngle":
    """Return rotation from a tuple.

    Args:
      rotation: The rotation as a three-element (rx, ry, rz) tuple.

    Returns:
      The rotation.
    """
    return AxisAngle(rx=rotation[0], ry=rotation[1], rz=rotation[2])

  @classmethod
  def from_list(cls, rotation: List[float]) -> "AxisAngle":
    """Return rotation from a list.

    Args:
      rotation: The rotation as a three-element (rx, ry, rz) list.

    Raises:
      ValueError: if the list is not a three-element list.

    Returns:
      The rotation.
    """
    if len(rotation) != 3:
      raise ValueError("Rotation must be three elements.")
    rotation_tuple: Tuple[float, float,
                          float] = cast(Tuple[float, float, float],
                                        tuple(rotation))
    return cls.from_tuple(rotation_tuple)


@dataclasses.dataclass(frozen=True)
class Quaternion(object):
  """Quaternion representation of an orientation.

  Default to no rotation.
  """
  x: float = 0
  y: float = 0
  z: float = 0
  w: float = 1

  @property
  def normalized(self) -> "Quaternion":
    """Return a normalizaed version of the quaternion."""
    length = math.sqrt(self.x**2 + self.y**2 + self.z**2 + self.w**2)
    if length == 0:
      return Quaternion(0, 0, 0, 1)
    return Quaternion(self.x / length, self.y / length, self.z / length,
                      self.w / length)

  def as_tuple(self) -> Tuple[float, float, float, float]:
    """Return the quaternion as a tuple.

    Returns:
      The rotation as a four-element (x, y, z, w) tuple.
    """
    return (self.x, self.y, self.z, self.w)

  def as_list(self) -> List[float]:
    """Return the quaternion rotation as a list.

    Returns:
      The rotation as a four-element (x, y, z, w) list.
    """
    return list(self.as_tuple())

  @classmethod
  def from_tuple(cls, rotation: Tuple[float, float, float,
                                      float]) -> "Quaternion":
    """Return rotation from a tuple.

    Args:
      rotation: The rotation as a four-element (x, y, z, w) tuple.

    Returns:
      The rotation.
    """
    return Quaternion(
        x=rotation[0], y=rotation[1], z=rotation[2], w=rotation[3])

  @classmethod
  def from_list(cls, rotation: List[float]) -> "Quaternion":
    """Return rotation from a list.

    Args:
      rotation: The rotation as a four-element (x, y, z, w) list.

    Raises:
      ValueError: if the list is not a three-element list.

    Returns:
      The rotation.
    """
    if len(rotation) != 4:
      raise ValueError("Rotation must be four elements.")
    rotation_tuple: Tuple[float, float, float,
                          float] = cast(Tuple[float, float, float, float],
                                        tuple(rotation))
    return cls.from_tuple(rotation_tuple)


@dataclasses.dataclass(frozen=True)
class Scale(object):
  """A data class that represents a 3D scale.

  Values in meters. Default to 1 meter.
  """
  x: float = 1.0
  y: float = 1.0
  z: float = 1.0

  def as_tuple(self) -> Tuple[float, float, float]:
    """Return the scale as a tuple.

    Returns:
      The scale as a three-element (x, y, z) tuple.
    """
    return (self.x, self.y, self.z)

  def as_list(self) -> List[float]:
    """Return the scale as a list.

    Returns:
      The scale as a three-element (x, y, z) list.
    """
    return list(self.as_tuple())

  @classmethod
  def from_tuple(cls, scale: Tuple[float, float, float]) -> "Scale":
    """Return scale from a tuple.

    Args:
      scale: The scale as a three-element (x, y, z) tuple.

    Returns:
      The scale.
    """
    return Scale(x=scale[0], y=scale[1], z=scale[2])

  @classmethod
  def from_list(cls, scale: List[float]) -> "Scale":
    """Return scale from a list.

    Args:
      scale: The scale as a three-element (x, y, z) list.

    Raises:
      ValueError: if the list is not a three-element list.

    Returns:
      The scale.
    """
    if len(scale) != 3:
      raise ValueError("Scale must be three elements.")
    return Scale(x=scale[0], y=scale[1], z=scale[2])


class Rotation(object):
  """A interface that represents a particular rotation in 3D space."""

  _rotation: Union[AxisAngle, Quaternion]

  def __init__(self, rotation: Union[AxisAngle, Quaternion]) -> None:
    """Create a rotation object.

    Args:
      rotation: The AxisAngle or Quaternion rotation.
    """
    self._rotation = rotation

  @property
  def axis_angle(self) -> "AxisAngle":
    """Return rotation in the Rodriguez axis-angle format."""
    if isinstance(self._rotation, AxisAngle):
      return cast(AxisAngle, self._rotation)
    norm = cast(Quaternion, self._rotation).normalized
    angle = 2 * math.atan2(math.sqrt(norm.x**2 + norm.y**2 + norm.z**2), norm.w)
    if angle <= 1e-3:
      scale = (2 + angle**2 / 12 + 7 * angle**4 / 2880)
    else:
      scale = angle / math.sin(angle / 2)
    return AxisAngle(norm.x * scale, norm.y * scale, norm.z * scale)

  @property
  def quaternion(self) -> "Quaternion":
    """Return rotation in the quaternion format."""
    if isinstance(self._rotation, Quaternion):
      return cast(Quaternion, self._rotation)
    aa = cast(AxisAngle, self._rotation)
    angle = math.sqrt(aa.rx * aa.rx + aa.ry * aa.ry + aa.rz * aa.rz)
    return Quaternion(aa.rx / angle * math.sin(angle / 2),
                      aa.ry / angle * math.sin(angle / 2),
                      aa.rz / angle * math.sin(angle / 2), math.cos(angle / 2))


@dataclasses.dataclass(frozen=True, init=False)
class Pose(object):
  """Represents a location and orientation in physical space.

  Attributes:
    position: the translational offset of this pose.
    orientation: the rotational offset of this pose.
  """
  position: Translation = Translation()
  orientation: Rotation = Rotation(AxisAngle())

  def __init__(self,
               position: Optional[Translation] = None,
               orientation: Optional[Union[Rotation, AxisAngle,
                                           Quaternion]] = None):
    """Represents a location and orientation in physical space.

    Args:
      position: the translational offset of this pose.
      orientation: the rotational offset of this pose.
    """
    if position is None:
      object.__setattr__(self, "position", Translation())
    else:
      object.__setattr__(self, "position", position)
    if orientation is None:
      object.__setattr__(self, "orientation", Rotation(AxisAngle()))
    elif isinstance(orientation, Rotation):
      object.__setattr__(self, "orientation", orientation)
    else:
      object.__setattr__(self, "orientation", Rotation(orientation))

  def as_tuple(self) -> Tuple[float, float, float, float, float, float]:
    """Return pose as a tuple.

    Returns:
      The position and axis-angle rotation as a six-element (x, y, z, rx, ry,
      rz) tuple.
    """
    return self.position.as_tuple() + self.orientation.axis_angle.as_tuple()

  def as_list(self) -> List[float]:
    """Return pose as a list.

    Returns:
      The position and axis-angle rotation as a six-element (x, y, z, rx, ry,
      rz) list.
    """
    return list(self.as_tuple())

  @classmethod
  def from_tuple(
      cls, pose: Tuple[float, float, float, float, float, float]) -> "Pose":
    """Return a pose from a tuple.

    Args:
      pose: a six-element (x, y, z, rx, ry, rz) tuple.

    Returns:
      The pose.
    """
    return Pose(
        Translation.from_tuple(pose[0:3]), AxisAngle.from_tuple(pose[3:]))

  @classmethod
  def from_list(cls, pose: List[float]) -> "Pose":
    """Return a pose from a list.

    Args:
      pose: a six-element (x, y, z, rx, ry, rz) list.

    Raises:
      ValueError: if the list is not six elements.

    Returns:
      The pose.
    """
    if len(pose) != 6:
      raise ValueError("Pose must be six elements.")
    pose_tuple: Tuple[float, float, float, float, float, float] = cast(
        Tuple[float, float, float, float, float, float], tuple(pose))
    return cls.from_tuple(pose_tuple)


@dataclasses.dataclass(frozen=True)
class Force:
  """Represents a torque.

  Attributes:
    x: The X-axis force in Newtons.
    y: The Y-axis force in Newtons.
    z: The Z-axis force in Newtons.
  """

  x: float
  y: float
  z: float


@dataclasses.dataclass(frozen=True)
class Torque:
  """Represents a torque.

  Attributes:
    x: The X-axis torque in Newton-Meters.
    y: The Y-axis torque in Newton-Meters.
    z: The Z-axis torque in Newton-Meters.
  """

  x: float
  y: float
  z: float
