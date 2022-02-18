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
from typing import Dict

from pyreach.gyms import reach_element


class ReachDigitalIOState:
  """ReachDigitalIOState maps the various vacuum states to int values."""

  OFF = 0
  ON = 1
  NO_CHANGE = 2


@dataclasses.dataclass(frozen=True)
class ReachIODigitalOutput:
  """Reach I/O Digital Output specification.

  In general, operations is going to have the provide these triples to
  provide successful configuration.

  Attributes:
    reach_name: The reach name of the robot that sponsors the digital output.
    capability_type: The capability type name (e.g "blowoff", "vacuum", etc.)
    pin_name: The internal pin name required by the capability type.
  """
  reach_name: str
  capability_type: str
  pin_name: str


@dataclasses.dataclass(frozen=True)
class ReachIO(reach_element.ReachElement):
  """Reach digital/analog input/output configuration class.

  Attributes:
    reach_name: The Reach name of the io device.  May be empty.
    is_synchronous: True synchronous I/O and False otherwise.
    digital_outputs: A dictionary that maps the user defined Gym pin name to a
      tuple of ("reach_name", "capability_type_name", "reach_pin_name") .
  """
  reach_name: str
  is_synchronous: bool
  digital_outputs: Dict[str, ReachIODigitalOutput]
