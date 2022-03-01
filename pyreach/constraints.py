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
"""Constraints of the configuration and task space.

PyReach only provides bare minimum support for the constraints right now.
"""

import dataclasses
from typing import Optional, Sequence, Tuple, Union

import numpy as np

from pyreach import core


@dataclasses.dataclass(frozen=True)
class JointLimit:
  """A single joint limit in radians.

  Attributes:
    min: The smallest joint angle in radian.
    max: The largest joint angle in radian.
  """

  min: float
  max: float


@dataclasses.dataclass(frozen=True)
class Geometry:
  """Base class for Geometries."""


@dataclasses.dataclass(frozen=True)
class Box(Geometry):
  """A geometry with the shape of a box.

  Attributes:
    pose: the pose of the box.
    scale: the scale of the box.
  """

  pose: core.Pose
  scale: core.Scale


@dataclasses.dataclass(frozen=True)
class Interactable:
  """An interactable is a geometry that a user can interact within its volume.

  Attributes:
    name: the name of the interactable.
    geometry: the geometry user can interact within.
  """

  name: str
  geometry: Geometry


@dataclasses.dataclass(frozen=True)
class ReferencePose:
  """Represents a reference pose for constraints robots.

  Attributes:
    name: The name of the reference pose.
    pose_type: The "type" field of the reference pose.
    pose: The actual reference pose.
  """
  name: str
  pose_type: str
  pose: core.Pose


class Constraints(object):
  """Interface for checking constraints."""

  def is_point_in_object(self, point: Union[Sequence[Union[int, float]],
                                            Sequence[int], Sequence[float],
                                            np.ndarray],
                         device_name: str) -> bool:
    """Check if a 3D point is colliding with a named device.

    Args:
      point: [x, y, z] coordinate of the point.
      device_name: name of the object to check.

    Returns:
      True if the point is inside the object.

    """
    raise NotImplementedError

  def get_joint_limits(self,
                       device_name: str) -> Optional[Tuple[JointLimit, ...]]:
    """Get the joint limits for the named arm device.

    Args:
      device_name: name of the arm.

    Returns:
      Limits of all the joints if available.

    """
    raise NotImplementedError

  def get_interactables(self) -> Tuple[Interactable, ...]:
    """Get the list of interactable geometries.

    Returns:
      Limits of all the interactable geometries if available.

    """
    raise NotImplementedError

  def get_reference_poses(
      self,
      device_name: str) -> Optional[core.ImmutableDictionary[ReferencePose]]:
    """Get the reference poses for a given robot.

    Args:
      device_name: the name of the robot device to load from.

    Returns:
      The reference poses as tuple of tuple of poses.
    """
    raise NotImplementedError
