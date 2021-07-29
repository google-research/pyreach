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

from typing import Any, List, Tuple

import unittest
from unittest import mock

import numpy as np  # type: ignore

from pyreach.gyms import core
from pyreach.gyms import reach_env
from pyreach.gyms.envs import benchmark_folding

# The exact stringss of instruction set for T-Shirt Folding.
_INSTRUCTION_SET = ['Fold the t-shirt', 'Unfold the t-shirt']

# The next instruction a mocked environment should return.
# This may be changed for tests to try out different instructions.
_NEXT_INSTRUCTION = _INSTRUCTION_SET[0]


# A mock class to represent a ReachEnv.
class MockEnv(reach_env.ReachEnv):

  def __init__(self, *args: Any, **kwargs: Any):
    pass

  def step(self,
           action: core.Action) -> Tuple[core.Observation, float, bool, Any]:
    return {
        'text_instructions': {
            'instruction': np.array(bytearray(_NEXT_INSTRUCTION, 'utf-8'))
        }
    }, 0, True, None

  def reset(self, *params: Any) -> core.Observation:
    return None

  def close(self) -> None:
    pass


class BenchmarkFoldingTest(unittest.TestCase):

  def test_parse_instruction(self) -> None:
    self.folding_env.reset()
    obs, _, _, _ = self.folding_env.step({})
    self.assertEqual(
        self.folding_env.parse_instruction(obs), 'Fold the t-shirt')

  def setUp(self) -> None:
    self._patches: List[Any] = [
        mock.patch.object(reach_env.ReachEnv, '__init__', MockEnv.__init__),
        mock.patch.object(reach_env.ReachEnv, 'step', MockEnv.step),
        mock.patch.object(reach_env.ReachEnv, 'reset', MockEnv.reset),
        mock.patch.object(reach_env.ReachEnv, 'close', MockEnv.close),
    ]
    for p in self._patches:
      p.start()
      self.addCleanup(p.stop)
    super().setUp()
    self.folding_env = benchmark_folding.BenchmarkFoldingEnv()


if __name__ == '__main__':
  unittest.main()
