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

"""Reach oracle element used for configuration."""

import dataclasses

from pyreach.gyms import reach_element


@dataclasses.dataclass(frozen=True)
class ReachOracle(reach_element.ReachElement):
  """A Reach Oracle configuration class.

  Attributes:
    reach_name: The name of the Oracle.
    task_code: The task code string.
    intent: The intention of the task.  This agument is optional and defaults to
      an empty string.
    success_type: The type of success.  This argument is optional and defaults
      to an empty string.
    is_synchronous: If True, the next Gym observation will synchronize all
      observation elements that have this flag set otherwise the next
      observation is asynchronous.  This argument is optional and defaults to
      False.
  """
  task_code: str
  intent: str = ""
  success_type: str = ""
  is_synchronous: bool = False
