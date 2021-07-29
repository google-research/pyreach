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

"""Support Mock action sets."""
from typing import Tuple

from pyreach import actionsets


class ActionsMock(actionsets.Actions):
  """Interface for accessing action template related functionalities."""

  def action_names(self) -> Tuple[str, ...]:
    """Return the list of available action template names."""
    raise NotImplementedError
