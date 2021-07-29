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

"""Mock Constraints."""

from typing import Optional, Tuple

import numpy as np  # type: ignore
from pyreach import constraints


class ConstraintsMock(constraints.Constraints):
  """Interface for checking constraints."""

  def is_point_in_object(self, point: np.ndarray, device_name: str) -> bool:
    """Check if a 3D point is colliding with a named device.

    Args:
      point: [x, y, z] coordinate of the point.
      device_name: name of the object to check.

    Returns:
      True if the point is inside the object.

    """
    raise NotImplementedError

  def get_joint_limits(
      self, device_name: str) -> Optional[Tuple[constraints.JointLimit, ...]]:
    """Get the joint limits for the named arm device.

    Args:
      device_name: name of the arm.

    Returns:
      Limits of all the joints if available.

    """
    raise NotImplementedError
