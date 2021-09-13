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

"""Handle registeration within the gym."""

import importlib
from typing import Any

import gym  # type: ignore


# pylint: disable=redefined-builtin
def register(id: str, entry_point: str, **kwargs: Any) -> None:
  """Register a gym environment for gym.make.

  Note: this is a special wrapper for pyreach that stores the "id" field in the
  kwarg "gym_env_id" parameter, which is used for reach snapshot logging.

  Args:
    id: the gym id (specified in call to gym.make).
    entry_point: the entry_point in the format "module name: class name".
    **kwargs: optional key-word arguments to the class.
  """

  def wrapped(**wrapper_args: Any) -> Any:
    args_update = wrapper_args.copy()
    args_update['gym_env_id'] = id
    mod_name, attr_name = entry_point.split(':')
    mod = importlib.import_module(mod_name)
    fn = getattr(mod, attr_name)
    return fn(**args_update)

  gym.register(id=id, entry_point=wrapped, **kwargs)
