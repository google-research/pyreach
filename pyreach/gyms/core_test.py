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

"""Tests for utils.py."""

import unittest
import gym  # type: ignore
import numpy as np  # type: ignore

from pyreach import core
from pyreach.gyms import core as gyms_core


class CoreTest(unittest.TestCase):

  def test_timestamp(self) -> None:
    timestamp_space = gyms_core.Timestamp()
    timestamp = gyms_core.Timestamp.new(1.0)
    self.assertTrue(timestamp_space.contains(timestamp))
    timestamp = gyms_core.Timestamp.new(np.array(2.0))
    self.assertTrue(timestamp_space.contains(timestamp))

    error_message: str = (
        "Timestamp ts=xyzzy is type <class 'str'> not float or numpy scalar")
    try:
      gyms_core.Timestamp.new("xyzzy")
      assert "missing exception"
    except core.PyReachError as error:
      assert error_message == str(error), f"Wrong error message '{error}'"

    error_message = "Timestamp ts=[1.23] is not scalar numpy array"
    try:
      gyms_core.Timestamp.new(np.array([1.23]))
      assert "missing exception"
    except core.PyReachError as error:
      assert error_message == str(error), f"Wrong error message '{error}'"


class TestObservationGet(unittest.TestCase):
  """Test the observation get functions."""

  def test_observation_get(self) -> None:
    """Test the observation get functions."""
    test_space: gym.spaces.Dict = gym.spaces.Dict({
        "box":
            gym.spaces.Dict({
                "f0":
                    gym.spaces.Box(
                        low=0.0, high=10.0, dtype=np.float_, shape=()),
                "f1":
                    gym.spaces.Box(
                        low=0.0, high=10.0, dtype=np.float_, shape=(6,)),
                "i0":
                    gym.spaces.Discrete(10),
                "i1":
                    gym.spaces.MultiDiscrete([2, 256, 1 << 16, 1 << 32]),
                "i2":
                    gym.spaces.Box(
                        low=0, high=65535, dtype=np.uint16, shape=(3, 5)),
                "i3":
                    gym.spaces.Box(
                        low=0, high=255, dtype=np.uint8, shape=(3, 5, 3)),
            }),
    })

    observation: gyms_core.Observation = test_space.sample()
    print(f"observation={observation}")

    # Test path_exits().
    assert gyms_core.path_exists(observation, "box")
    assert gyms_core.path_exists(observation, "box.f0")
    assert gyms_core.path_exists(observation, "box.f1")
    assert not gyms_core.path_exists(observation, "box.f2")
    assert gyms_core.path_exists(observation, "box.i0")
    assert gyms_core.path_exists(observation, "box.i1")
    assert gyms_core.path_exists(observation, "box.i2")
    assert gyms_core.path_exists(observation, "box.i3")
    assert not gyms_core.path_exists(observation, "box.i4")

    # Verify that bogus paths do not cause problems.
    assert not gyms_core.path_exists(observation, "")
    assert not gyms_core.path_exists(observation, ".")
    assert not gyms_core.path_exists(observation, "..")
    assert not gyms_core.path_exists(observation, ".a")
    assert not gyms_core.path_exists(observation, "a.")
    assert not gyms_core.path_exists(observation, "a..b")
    assert not gyms_core.path_exists(observation, "box.")
    assert not gyms_core.path_exists(observation, "box..")
    assert not gyms_core.path_exists(observation, "box.a")
    assert not gyms_core.path_exists(observation, "box.a.")

    # Test some exceptions.

    # Empty key.
    error_message: str
    try:
      gyms_core.get_float0(observation, "")
      assert False, "Missing exception"
    except core.PyReachError as py_reach_error:
      error_message = "Path ('') has an empty key."
      assert str(py_reach_error) == error_message, py_reach_error

    # Key not present:
    try:
      gyms_core.get_float0(observation, "boxy.f0")
      assert False, "Missing exception"
    except core.PyReachError as py_reach_error:
      error_message = ("Dictionary key 'boxy' is not present, "
                       "(try one of ['box'])")
      assert str(py_reach_error) == error_message, py_reach_error
    assert not gyms_core.path_exists(observation, "boxy.f0")

    # Access past end of dictionary:
    try:
      gyms_core.get_float0(observation, "box.f0.bogus")
      assert False, "Missing exception"
    except core.PyReachError as py_reach_error:
      error_message = "'box.f0' is not a dictionary."
      assert str(py_reach_error) == error_message, py_reach_error
    assert not gyms_core.path_exists(observation, "box.f0.bogus")

    # Missing numpy.ndarray:
    try:
      gyms_core.get_float0(observation, "box.i0")
      assert False, "Missing exception"
    except core.PyReachError as py_reach_error:
      error_message = "'box.i0' is not a numpy.ndarray."
      assert str(py_reach_error) == error_message, py_reach_error

    # Dimensionality mismatch:
    try:
      gyms_core.get_float0(observation, "box.f1")
      assert False, "Missing exception"
    except core.PyReachError as py_reach_error:
      error_message = "Dimensionality of 'box.f1' is 1, not 0"
      assert str(py_reach_error) == error_message, py_reach_error

    # Verify values returned.

    # float0:
    assert 0.0 <= gyms_core.get_float0(observation, "box.f0") <= 10.0
    assert gyms_core.get_float0(observation, "", -1.0) == -1.0

    # float1:
    joint_angles: np.ndarray = gyms_core.get_float1(observation, "box.f1")
    assert joint_angles.shape == (6,)
    assert joint_angles.dtype == np.float_

    # int0:
    assert 0 <= gyms_core.get_int0(observation, "box.i0") <= 10
    assert gyms_core.get_int0(observation, "", -1) == -1

    # int1:
    i1: np.ndarray = gyms_core.get_int1(observation, "box.i1")
    assert isinstance(i1, np.ndarray)
    assert i1.shape == (4,)
    assert i1.dtype == np.int64

    # int2:
    depth_image: np.ndarray = gyms_core.get_int2(observation, "box.i2")
    assert depth_image.shape == (3, 5)
    assert depth_image.dtype == np.uint16, depth_image.dtype

    # int3:
    color_image: np.ndarray = gyms_core.get_int3(observation, "box.i3")
    assert color_image.shape == (3, 5, 3)
    assert color_image.dtype == np.uint8, color_image.dtype

    # Check default returns for arrays:

    # float1:
    joint_angles2: np.ndarray = gyms_core.get_float1(
        observation, "box.f1...", default=joint_angles)
    assert joint_angles2 is joint_angles

    # int2:
    depth_image2: np.ndarray = gyms_core.get_int2(
        observation, "", default=depth_image)
    assert depth_image2 is depth_image

    # int3:
    color_image2: np.ndarray = gyms_core.get_int3(
        observation, "", default=color_image)
    assert color_image2 is color_image

    # Make sure that the default arrays have the right size and shape:

    # float1:
    try:
      gyms_core.get_float1(
          observation, "", default=np.array([], dtype=np.uint8))
      assert False, "Missing exception"
    except core.PyReachError as error:
      error_message = "default has type uint8 not <class 'numpy.float64'>"
      assert str(error) == error_message, error

    try:
      gyms_core.get_float1(
          observation,
          "",
          default=np.array([[0., 1.], [2., 3.]], dtype=np.float_))
      assert False, "Missing exception"
    except core.PyReachError as error:
      error_message = "default has dimensionality of 2, not 1"
      assert str(error) == error_message, error

    # int1:
    try:
      gyms_core.get_int1(
          observation, "", default=np.array([1., 2., 3.], dtype=np.float_))
      assert False, "Missing exception"
    except core.PyReachError as error:
      error_message = "default has type float64 not <class 'numpy.int64'>"
      assert str(error) == error_message, error

    try:
      gyms_core.get_int1(
          observation, "", default=np.array([[0, 1], [2, 3]], dtype=np.int64))
      assert False, "Missing exception"
    except core.PyReachError as error:
      error_message = "default has dimensionality of 2, not 1"
      assert str(error) == error_message, error

    # int2:
    try:
      gyms_core.get_int2(
          observation, "", default=np.array([[0, 1], [2, 3]], dtype=np.float_))
      assert False, "Missing exception"
    except core.PyReachError as error:
      error_message = "default has type float64 not <class 'numpy.uint16'>"
      assert str(error) == error_message, error

    try:
      gyms_core.get_int2(
          observation, "", default=np.array([0, 1, 2, 3], dtype=np.uint16))
      assert False, "Missing exception"
    except core.PyReachError as error:
      error_message = "default has dimensionality of 1, not 2"
      assert str(error) == error_message, error

    # int3:
    try:
      gyms_core.get_int3(
          observation, "", default=np.array([[[0]]], dtype=np.float_))
      assert False, "Missing exception"
    except core.PyReachError as error:
      error_message = "default has type float64 not <class 'numpy.uint8'>"
      assert str(error) == error_message, error

    try:
      gyms_core.get_int3(
          observation, "", default=np.array([0, 1, 2, 3], dtype=np.uint8))
      assert False, "Missing exception"
    except core.PyReachError as error:
      error_message = "default has dimensionality of 1, not 3"
      assert str(error) == error_message, error


if __name__ == "__main__":
  unittest.main()
