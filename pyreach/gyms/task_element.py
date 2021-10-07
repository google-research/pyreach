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

from pyreach.gyms import reach_element


class ReachAction:
  """Reach task action values."""
  NO_CHANGE = 0
  START = 1
  STOP = 2


@dataclasses.dataclass(frozen=True)
class ReachTask(reach_element.ReachElement):
  """Task configuration class.

  Attributes:
    reach_name: The name of the corresponding device on the Reach server. This
      name can be empty.
    is_synchronous: If True, the next Gym observation will synchronize all
      observactions elements that have this flag set otherwise the next
      observation is asynchronous.  This argument is optional and defaults to
      False.
  """

  is_synchronous: bool = False
