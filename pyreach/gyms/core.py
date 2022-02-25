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

"""Useful type hints for working with Gyms."""

import collections
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import gym  # type: ignore
import numpy as np

from pyreach import core


class Timestamp(gym.spaces.Box):  # type: ignore
  """A Gym Space that holds a timestamp."""

  def __init__(self) -> None:
    """Initialize a Timestamp Gym Space."""
    super().__init__(low=0.0, high=np.inf, shape=(), dtype=np.dtype(float))

  @classmethod
  def new(cls, ts: Union[float, np.ndarray]) -> np.ndarray:
    """Return a new timestamp as numpy scalar for an observation."""
    # There are currently no type hints for numpy, which confuses the
    # Google3 Python type hints checker.  This solves the problem.
    if isinstance(ts, np.ndarray) and not isinstance(ts, float):
      size: int = len(ts.shape)
      if size:
        raise core.PyReachError(f"Timestamp ts={ts} is not scalar numpy array")
      ts = float(ts)
    if not isinstance(ts, float):
      raise core.PyReachError(f"Timestamp ts={ts} is type {type(ts)} "
                              "not float or numpy scalar")
    timestamp: np.ndarray = np.array(ts)
    return timestamp


Space = Union[Timestamp,
              gym.spaces.Box,  # N-dimensional array of bounded floats
              gym.spaces.Dict,  # Dictionary of other GymSpaces
              gym.spaces.Discrete,  # A single bounded integer from 0...N-1
              gym.spaces.MultiBinary,  # N-dimensional structure of Bool's
              gym.spaces.MultiDiscrete,  # List of discrete values
              gym.spaces.Tuple]  # Tuple of other GymSpaces
Action = Union[np.ndarray,  # Box/MultiBinary/MultiDiscreate observation
               Dict[str, Any],  # Dict observation (Any == Action)
               collections.OrderedDict,  # Treat the same as a Dict
               int,  # Discrete observation
               Tuple[Any, ...]]  # Tuple observation (Any == Action)
ActionDict = Union[Dict[str, Any], collections.OrderedDict]
Observation = Action
RewardDoneFunction = Callable[[Action, Observation], Tuple[float, bool]]

# Utilitiy functions for reading observations:


def get_path(observation: Observation, path: str) -> Tuple[Any, str]:
  """Return a sub-observation from a dictionary space observation.

  Args:
    observation: An observation dictionary that may contain nested dictionaries.
    path: A period separated path of dictionary names (e.g. "arm.pose").

  Returns:
    Upon success returns a tuple of (value, "").
    Upon failure returns a tuple of (None, "error_message")

  """
  current: Any = observation
  partial_path: List[str] = []
  key: str
  for key in path.split("."):
    if not key:
      return (None, f"Path ('{path}') has an empty key.")
    if not isinstance(current, (dict, collections.OrderedDict)):
      return (None, f"'{'.'.join(partial_path)}' is not a dictionary.")
    if key not in current:
      return (None, f"Dictionary key '{key}' is not present, "
              f"(try one of {list(current.keys())})")
    partial_path.append(key)
    current = current[key]
  return (current, "")


def path_exists(observation: Observation, path: str) -> bool:
  """Determine if a path exists.

  Args:
    observation: An observation dictionary that may contain nested dictionaries.
    path: A period separated path of dictionary names (e.g. "arm.pose").

  Returns:
    Return True if the path exists; otherwise False.

  """
  value: Any
  value, _ = get_path(observation, path)
  return value is not None


def get_ndarray(observation: Observation, path: str, dimensionality: int,
                dtype: np.dtype) -> Tuple[Optional[np.ndarray], str]:
  """Return a numpy array of the desired dimensionality and type.

  Args:
    observation: An observation dictionary that may contain nested dictionaries.
    path: A period separated path of dictionary names (e.g. "arm.pose").
    dimensionality: The required dimensionaility of the numpy ndarray.
    dtype: The required data type for the array.

  Returns:
    Return (numpy_array, "") if the array is found;
    otherwise return (None, "error message")

  """
  sub_observation: Optional[Observation]
  sub_observation, error = get_path(observation, path)
  if sub_observation is None:
    return (None, error)

  if not isinstance(sub_observation, np.ndarray):
    return (None, f"'{path}' is not a numpy.ndarray.")
  if sub_observation.dtype != dtype:
    return (None, f"'{path}' is type {sub_observation.dtype}, not {dtype}.")
  if len(sub_observation.shape) != dimensionality:
    return (None, f"Dimensionality of '{path}' is "
            f"{len(sub_observation.shape)}, not {dimensionality}")
  return (sub_observation, "")


def default_ndarray_check(default: Any, dimensionality: int,
                          dtype: np.dtype) -> str:
  """Check ndarray dimensionality and type.

  Args:
    default: The default ndarray to check.
    dimensionality: The desired dimensionality of ndarray.
    dtype: The desired type of ndarray.

  Returns:
    Empty string for success; otherwise, an error message is returned.

  """
  if not isinstance(default, np.ndarray):
    return f"default has type {str(default.dtype)}, not numpy.ndarray"
  if len(default.shape) != dimensionality:
    return (f"default has dimensionality of {len(default.shape)}, "
            f"not {dimensionality}")
  if default.dtype != dtype:
    return f"default has type {default.dtype} not {dtype}"
  return ""


def get_float0(observation: Observation,
               path: str,
               default: Optional[float] = None) -> float:
  """Return a float from an observation path.

  Args:
    observation: The observation to start with.
    path: The path to the desired float.
    default: The default float to return if path not found. If None, raise a
      core.PyReachError if path not found.

  Returns:
    Return float associated with Path or default if path not found.

  Raises:
    core.PyreachError for any path, dimensionality, or type errors.

  """
  ndarray: Optional[np.ndarray]
  error: str
  ndarray, error = get_ndarray(observation, path, 0, np.dtype(np.float_))
  if isinstance(ndarray, np.ndarray):
    value: Any = ndarray.flat[0]
    if isinstance(value, float):
      return value
  if isinstance(default, float):
    return default
  raise core.PyReachError(error)


def get_float1(observation: Observation,
               path: str,
               default: Optional[np.ndarray] = None) -> np.ndarray:
  """Return a list of floats from an observation path.

  Args:
    observation: The observation to start with.
    path: The path to the desired float.
    default: The default np.ndarray to return if path not found. If None, raise
      a core.PyreachError if path not found.

  Returns:
    Returns the np.ndarray specified by the path or the default if not found.

  Raises:
    core.PyreachError for any path, dimensionality, or type errors.

  """
  ndarray: Optional[np.ndarray]
  error: str
  ndarray, error = get_ndarray(observation, path, 1, np.dtype(np.float_))
  if isinstance(ndarray, np.ndarray):
    return ndarray
  if isinstance(default, np.ndarray):
    error = default_ndarray_check(default, 1, np.dtype(np.float_))
    if not error:
      return default
  raise core.PyReachError(error)


def get_int0(observation: Observation,
             path: str,
             default: Optional[int] = None) -> int:
  """Return a int from an observation path.

  Args:
    observation: The observation to start with.
    path: The path to the desired float.
    default: The

  Returns:
    Returns the selected float.  If default set, the default is returned.

  Raises:
    core.PyreachError for any path, dimensionality, or type errors.

  """
  error: str
  value, error = get_path(observation, path)
  if isinstance(value, int):
    return value
  if isinstance(default, int):
    return default
  raise core.PyReachError(error)


def get_int1(observation: Observation,
             path: str,
             default: Optional[np.ndarray] = None) -> np.ndarray:
  """Return a list of ints from an observation path.

  Args:
    observation: The observation to start with.
    path: The path to the desired float.
    default: The default np.ndarray to return if path not found. If None, raise
      a core.PyreachError if path not found.

  Returns:
    Returns the np.ndarray specified by the path or the default if not found.

  Raises:
    core.PyreachError for any path, dimensionality, or type errors.

  """
  ndarray: Optional[np.ndarray]
  error: str
  ndarray, error = get_ndarray(observation, path, 1, np.dtype(np.int64))
  if isinstance(ndarray, np.ndarray):
    return ndarray
  if isinstance(default, np.ndarray):
    error = default_ndarray_check(default, 1, np.dtype(np.int64))
    if not error:
      return default
  raise core.PyReachError(error)


def get_int2(observation: Observation,
             path: str,
             default: Optional[np.ndarray] = None) -> np.ndarray:
  """Return a 2-dimensional array of int's from an observation path.

  Args:
    observation: The observation to start with.
    path: The path to the desired float.
    default: The default float to return if path not found. If None, raise a
      core.PyreachError if path not found.

  Returns:
    Return float associated with Path or default if path not found.

  Raises:
    core.PyreachError for any path, dimensionality, or type errors.

  """
  ndarray: Optional[np.ndarray]
  error: str
  ndarray, error = get_ndarray(observation, path, 2, np.dtype(np.uint16))
  if isinstance(ndarray, np.ndarray):
    assert ndarray.dtype == np.uint16, ndarray.dtype
    return ndarray
  if isinstance(default, np.ndarray):
    error = default_ndarray_check(default, 2, np.dtype(np.uint16))
    if not error:
      return default
  raise core.PyReachError(error)


def get_int3(observation: Observation,
             path: str,
             default: Optional[np.ndarray] = None) -> np.ndarray:
  """Return a 3-dimensional array of int's from an observation path.

  Args:
    observation: The observation to start with.
    path: The path to the desired float.
    default: The default float to return if path not found. If None, raise a
      core.PyreachError if path not found.

  Returns:
    Return float associated with Path or default if path not found.

  Raises:
    core.PyreachError for any path, dimensionality, or type errors.


  """
  ndarray: Optional[np.ndarray]
  error: str
  ndarray, error = get_ndarray(observation, path, 3, np.dtype(np.uint8))
  if isinstance(ndarray, np.ndarray):
    return ndarray
  if isinstance(default, np.ndarray):
    error = default_ndarray_check(default, 3, np.dtype(np.uint8))
    if not error:
      return default
  raise core.PyReachError(error)
