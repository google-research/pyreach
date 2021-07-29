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

"""Tests of Pyreach Internal and Timers."""

import math
import os
from typing import Tuple
import unittest
from pyreach import internal


class FakeClock(object):
  """A fake clock class for testing."""

  current_time = 0.0

  @classmethod
  def get_time(cls) -> float:
    # Return the increment of time.
    cls.current_time += .001  # 1ms
    return cls.current_time


class TimersTest(unittest.TestCase):
  """Test the performance timers."""

  def test_timers(self) -> None:
    """Test the performance timers."""

    os.environ["PYREACH_PERF"] = ""
    timers: internal.Timers = internal.Timers(
        {"gym", "step", "reset", "host", "arm", "color", "depth", "vacuum"},
        get_time=FakeClock.get_time)

    # A more interesting test:
    with timers.select({"gym", "reset"}):
      with timers.select({"!gym", "!reset", "host", "arm"}):
        pass
      with timers.select({"!gym", "!reset", "host", "color"}):
        pass
      with timers.select({"!gym", "!reset", "host", "depth"}):
        pass
      with timers.select({"!gym", "!reset", "host", "vacuum"}):
        pass

    desired_results = [
        ("arm", 1, 0.008),
        ("color", 1, 0.004),
        ("depth", 1, 0.004),
        ("gym", 1, 0.018),
        ("host", 4, 0.016),
        ("reset", 1, 0.018),
        ("step", 0, 0.000),
        ("vacuum", 1, 0.004),
    ]
    results = sorted(timers.results())
    errors: int = 0
    assert len(desired_results) == len(results), [desired_results, results]
    for index, result in enumerate(results):
      desired_result: Tuple[str, int, float] = desired_results[index]
      assert result[0] == desired_result[0], [result, desired_result]
      assert result[1] == desired_result[1], [result, desired_result]
      if not math.isclose(result[2], desired_result[2], rel_tol=1.0):
        print("Mismatch('{0}'): {1:.7f}, {2:.7f}".format(
            result[0], result[2], desired_result[2]))
        errors += 1
    assert not errors, errors

    # Nesting test:
    timers = internal.Timers({"gym.arm", "gym.color", "host.arm", "host.color"})
    assert timers.enabled() == set(), timers.enabled()
    with timers.select({"gym"}):
      assert timers.enabled() == {"gym"}, f"got:{timers.enabled()}"
      with timers.select({"gym.arm"}):
        assert timers.enabled() == {"gym", "gym.arm"}, timers.enabled()
        with timers.select({"!gym*", "host.arm"}):
          assert timers.enabled() == {"host", "host.arm"}, timers.enabled()
        assert timers.enabled() == {"gym", "gym.arm"}, timers.enabled()
        with timers.select({"!gym*", "host.color"}):
          assert timers.enabled() == {"host", "host.color"}, timers.enabled()
        assert timers.enabled() == {"gym", "gym.arm"}, timers.enabled()
      assert timers.enabled() == {"gym"}, timers.enabled()
    assert timers.enabled() == set(), timers.enabled()


if __name__ == "__main__":
  unittest.main()
