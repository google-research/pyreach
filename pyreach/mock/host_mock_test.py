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

"""Tests for HostMock."""

import math
from typing import Dict, Tuple
import unittest

# import numpy as np  # type: ignore

from pyreach import host
from pyreach.gyms import arm_element
from pyreach.gyms import reach_env
from pyreach.mock import host_mock


class TestMockHost(unittest.TestCase):
  """Test the MockHost class."""

  def test_host(self) -> None:
    """Test the host."""
    pi: float = math.pi
    low_joint_angles: Tuple[float, ...] = (-pi, -pi, -pi, -pi, -pi, -pi)
    high_joint_angles: Tuple[float, ...] = (pi, pi, pi, pi, pi, pi)

    pyreach_config: Dict[str, reach_env.ReachElement] = {
        "arm:":
            reach_env.ReachArm(
                reach_name="robot",
                low_joint_angles=low_joint_angles,
                high_joint_angles=high_joint_angles,
                apply_tip_adjust_transform=False,
                is_synchronous=False,
                response_queue_length=0,
                p_stop_mode=arm_element.ReachStopMode.STOP_STATUS,
                e_stop_mode=arm_element.ReachStopMode.STOP_DONE,
                test_states=[])
    }
    pyreach_host: host.Host = host_mock.HostMock(pyreach_config)
    assert isinstance(pyreach_host, host.Host)


if __name__ == "__main__":
  unittest.main()
