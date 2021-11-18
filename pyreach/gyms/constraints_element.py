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
"""Reach arm element used for configuration."""

import dataclasses
from typing import Tuple

from pyreach.gyms import reach_element


@dataclasses.dataclass(frozen=True)
class ReachConstraint(object):
  """One constrainte object.

  Attributes:
    name: The constraint name (e.g. "left_bin", "right_bin", etc.)
    geometry: The constraint geometry (currently must be "box".)
  """
  name: str
  geometry: str


@dataclasses.dataclass(frozen=True)
class ReachConstraints(reach_element.ReachElement):
  """Task configuration class.

  Attributes:
    reach_name: The name of the corresponding device on the Reach server. This
      name can be empty.
    is_synchronous: If True, the next Gym observation will synchronize all
      observactions elements that have this flag set otherwise the next
      observation is asynchronous.  This argument is optional and defaults to
      False.
    constraints: A tuple of ReachConstraint objects.
  """
  is_synchronous: bool = False
  constraints: Tuple[ReachConstraint, ...] = ()
