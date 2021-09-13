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

"""Test the Host class."""

from typing import Any, Dict, Optional

import pyreach
from pyreach.impl import arm_impl_test
from pyreach.impl import color_camera_impl_test
from pyreach.impl import depth_camera_impl_test
from pyreach.impl import host_impl
from pyreach.impl import logger_impl_test
from pyreach.impl import oracle_impl_test
from pyreach.impl import reach_host_test
from pyreach.impl import test_utils
from pyreach.impl import text_instruction_impl_test


def connect_test(host_args: Optional[Dict[str, Any]] = None) -> pyreach.Host:
  """Return a Test Host."""
  test_client = test_utils.TestClient([
      reach_host_test.TestPipelineDescription(),
      reach_host_test.TestPingResponder(),
      reach_host_test.TestSessionManager(),
      depth_camera_impl_test.TestDepthCamera("depth-camera", "", "photoneo"),
      color_camera_impl_test.TestColorCamera("color-camera", "", "uvc"),
      arm_impl_test.TestArm(""),
      oracle_impl_test.TestOracle("oracle", "pick-points",
                                  "oracle-pick-points"),
      logger_impl_test.TestLogger(),
      text_instruction_impl_test.TestTextInstructions(),
  ])
  if host_args is None:
    host_args = {}
  host = host_impl.HostImpl(test_client, **host_args)
  return host
