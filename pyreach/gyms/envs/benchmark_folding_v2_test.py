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

import numpy as np

from pyreach.gyms import core
from pyreach.gyms import reach_env
from pyreach.gyms.envs import benchmark_folding_v2

# The exact stringss of instruction set for T-Shirt Folding.
# Used by the mock parent environment to simulate reach serve generating them.
_INSTRUCTION_SET = ['Scramble the t-shirt', 'Fold the t-shirt']


# A mock class to represent a ReachEnv.
class MockReachEnv(reach_env.ReachEnv):

  def __init__(self, *args: Any, **kwargs: Any):
    self._next_instruction_no = 0
    self._task_enabled = False

  def step(self,
           action: core.Action) -> Tuple[core.Observation, float, bool, Any]:
    assert isinstance(action, dict)
    if 'text_instructions' in action:
      assert isinstance(action['text_instructions'], dict)
      if 'task_enable' in action['text_instructions']:
        task_enable = action['text_instructions']['task_enable']
        if task_enable == 0:
          self._task_enabled = False
          self._next_instruction_no += 1
        elif task_enable == 1:
          self._task_enabled = True

    next_instruction = ''
    if self._task_enabled:
      if self._next_instruction_no < len(_INSTRUCTION_SET):
        next_instruction = _INSTRUCTION_SET[self._next_instruction_no]
    done = False if next_instruction else True
    print(f'{next_instruction}')
    return {
        'text_instructions': {
            'instruction': np.array(bytearray(next_instruction, 'utf-8'))
        }
    }, 0, done, None

  def reset(self, *params: Any) -> core.Observation:
    self._next_instruction_no = 0
    self._task_enabled = True
    print('reset called')
    return {}

  def close(self) -> None:
    pass


class BenchmarkFoldingTest(unittest.TestCase):

  def test_parse_instruction(self) -> None:
    # Reset and check the instruction a few times.
    self.folding_env.reset()
    for _ in range(2):
      obs, _, done, _ = self.folding_env.step({})
      self.assertEqual(
          self.folding_env.parse_instruction(obs), 'Scramble the t-shirt')
      self.assertFalse(done)

    # Report scramble_done(), confirm instruction afterwards few times.
    self.folding_env.scramble_done()
    for _ in range(2):
      obs, _, done, _ = self.folding_env.step({})
      self.assertEqual(
          self.folding_env.parse_instruction(obs), 'Fold the t-shirt')
      self.assertFalse(done)

    # Report scramble_done(), confirm instruction and done status.
    self.folding_env.fold_done()
    for _ in range(2):
      obs, _, done, _ = self.folding_env.step({})
      self.assertEqual(
          self.folding_env.parse_instruction(obs), '')
      self.assertTrue(done)

  def setUp(self) -> None:
    self._patches: List[Any] = [
        mock.patch.object(
            reach_env.ReachEnv, '__init__', MockReachEnv.__init__),
        mock.patch.object(reach_env.ReachEnv, 'step', MockReachEnv.step),
        mock.patch.object(reach_env.ReachEnv, 'reset', MockReachEnv.reset),
        mock.patch.object(reach_env.ReachEnv, 'close', MockReachEnv.close),
    ]
    for p in self._patches:
      p.start()
      self.addCleanup(p.stop)
    super().setUp()
    self.folding_env = benchmark_folding_v2.BenchmarkFoldingEnv()


if __name__ == '__main__':
  unittest.main()
