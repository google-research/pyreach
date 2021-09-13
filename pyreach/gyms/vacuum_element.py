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

"""Reach vacuum element used for configuration."""

import dataclasses

from pyreach.gyms import reach_element


class ReachVacuumState:
  """ReachVacuumState maps the various vacuum states to int values."""

  OFF = 0
  VACUUM = 1
  BLOWOFF = 2


@dataclasses.dataclass(frozen=True)
class ReachVacuum(reach_element.ReachElement):
  """Reach vacuum actuator configuration class.

  Attributes:
    reach_name: The Reach name of the vacuum.  May be empty.
    is_synchronous: If True, the next Gym observation will synchronize all
      observations element that have this flag set otherwise the next
      observation is asynchronous.  This argument is optional and defaults to
      False.
    state_enable: If True, the `state` entry is in the observation space.
    vacuum_detect_enable: If True, the `vacuum_detect` entry is in the
      observation space.
    vacuum_gauge_enable: If True, the `vacuum_gauge` entry is present in
      observation space.  The vacuum gauge pressure is measured in inverse
      Pascals where 0.0 means 1 atmosphere and 101325.0 means a hard vacuum.
      -1.0 is returned if no valid vacuum gauge pressure is present.
  """
  is_synchronous: bool = False
  state_enable: bool = True  # Backwards compatibility => True
  vacuum_detect_enable: bool = True  # Backwards compatibility => True
  vacuum_gauge_enable: bool = False
