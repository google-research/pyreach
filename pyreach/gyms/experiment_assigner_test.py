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

"""Tests of PyReach Gym."""

import random
from typing import Any, Dict, List, Tuple

import unittest
from unittest import mock

import gym  # type: ignore
from pyreach import host
from pyreach.gyms import core as gyms_core
from pyreach.gyms import experiment_assigner
from pyreach.gyms import pausable_env
from pyreach.gyms import reach_env
from pyreach.gyms.registration import register
from pyreach.mock import host_mock

GYMS_PATH = ''
_MOCK_ENV_ID: str = 'test_env-v0'


def setUpModule() -> None:
  class_name: str = 'FakeReachEnv'
  entry_point: str = GYMS_PATH + 'experiment_assigner_test:' + class_name
  register(
      id=_MOCK_ENV_ID,
      entry_point=entry_point,
      max_episode_steps=200,
      reward_threshold=25.0)


# Set of all session_end_reasons - used mainly for a few tests that don't
# care a lot about the reason.
_ALL_EVENTS = (
    pausable_env.SessionEndReason.AGENT_CALLED_RESET,
    pausable_env.SessionEndReason.STEP_RETURNED_DONE,
    pausable_env.SessionEndReason.AGENT_FINISHED)


class FakeReachEnv(reach_env.ReachEnv):
  """A fake ReachEnv for testing."""

  def __init__(self, **kwargs: Any) -> None:
    pyreach_config: Dict[str, reach_env.ReachElement] = {}

    mock_host: host.Host = host_mock.HostMock()
    assert isinstance(mock_host, host.Host)
    assert isinstance(mock_host, host_mock.HostMock)
    super().__init__(pyreach_config=pyreach_config, host=mock_host, **kwargs)

    # Flags for testing.
    self.recorded_calls: List[str] = []

  def step(
      self, action: gyms_core.Action
  ) -> Tuple[gyms_core.Observation, float, bool, Any]:
    self.recorded_calls.append('step')
    super().step(action)
    # Return done as True if {'done': True} was passed.
    done = action.get('done', False) if isinstance(action, dict) else False
    return {}, 0.0, done, None

  def clear_recorded_calls(self) -> None:
    self.recorded_calls = []

  def reset(self) -> gyms_core.Observation:
    self.recorded_calls.append('reset')
    return {}

  def close(self) -> None:
    self.recorded_calls.append('close')
    return super().close()


class ExperimentAssignerTest(unittest.TestCase):
  """Test ability to pause and resume environments."""

  def _confirm_only_active_index(
      self, envs: List[reach_env.ReachEnv],
      index: int) -> None:
    for i, env in enumerate(envs):
      if i == index:
        self.assertTrue(env.is_active())
      else:
        self.assertFalse(env.is_active())

  def test_divert_only_on_done(self) -> None:

    with gym.make(_MOCK_ENV_ID) as env:
      env.reset()
      assigner = experiment_assigner.ExperimentAssigner(
          env, divert_on={pausable_env.SessionEndReason.STEP_RETURNED_DONE})
      self.next_mock_random = [0.4]

      envs = assigner.randomized_slicer([1.0])

      self.assertEqual(assigner._diversion_count, 1)
      envs[0].step({'done': True})
      # Diversion happens on done=True.
      self.assertEqual(assigner._diversion_count, 2)
      envs[0].reset()
      # No additional diversion on reset.
      self.assertEqual(assigner._diversion_count, 2)

  def test_divert_only_on_reset(self) -> None:

    with gym.make(_MOCK_ENV_ID) as env:
      env.reset()
      assigner = experiment_assigner.ExperimentAssigner(
          env, divert_on={pausable_env.SessionEndReason.AGENT_CALLED_RESET})
      self.next_mock_random = [0.4]

      envs = assigner.randomized_slicer([1.0])

      self.assertEqual(assigner._diversion_count, 1)
      envs[0].step({'done': True})
      # Diversion does not happen, because we are only looking for resets().
      self.assertEqual(assigner._diversion_count, 1)
      envs[0].reset()
      # Diversion happened on reset().
      self.assertEqual(assigner._diversion_count, 2)

  def test_custom_divert_only_on_reset(self) -> None:

    def custom_divert_handler(unused_env: reach_env.ReachEnv,
                              reason: pausable_env.SessionEndReason) -> bool:
      return reason == pausable_env.SessionEndReason.AGENT_CALLED_RESET

    with gym.make(_MOCK_ENV_ID) as env:
      env.reset()
      assigner = experiment_assigner.ExperimentAssigner(
          env, divert_hook=custom_divert_handler, divert_on=_ALL_EVENTS)
      self.next_mock_random = [0.4]

      envs = assigner.randomized_slicer([1.0])

      self.assertEqual(assigner._diversion_count, 1)
      envs[0].step({'done': True})
      # Diversion is inhibited on step().
      self.assertEqual(assigner._diversion_count, 1)
      envs[0].reset()
      # Diversion happened on reset().
      self.assertEqual(assigner._diversion_count, 2)

  def test_custom_divert_enforce_resets(self) -> None:

    def custom_divert_handler(
        env: reach_env.ReachEnv,
        unused_reason: pausable_env.SessionEndReason) -> bool:
      env.reset()
      return True

    with gym.make(_MOCK_ENV_ID) as env:
      env.reset()
      self.assertEqual(env.recorded_calls, ['reset'])
      assigner = experiment_assigner.ExperimentAssigner(
          env, divert_hook=custom_divert_handler, divert_on=_ALL_EVENTS)
      self.next_mock_random = [0.4]
      envs = assigner.randomized_slicer([1.0])
      # When 'done', a reset will be added before switching.
      env.clear_recorded_calls()
      envs[0].step({'done': True})
      self.assertEqual(env.recorded_calls, ['step', 'reset'])
      # After reset, another reset will be added before switching.
      env.clear_recorded_calls()
      envs[0].reset()
      self.assertEqual(env.recorded_calls, ['reset', 'reset'])

  def test_single_env(self) -> None:
    with gym.make(_MOCK_ENV_ID) as env:
      env.reset()
      assigner = experiment_assigner.ExperimentAssigner(
          env, divert_on=_ALL_EVENTS)
      self.next_mock_random = [0.4]
      envs = assigner.randomized_slicer([1.0])
      self.assertTrue(len(envs), 1)
      # Check that the env continues to work across resets, and isn't blocked.
      self._confirm_only_active_index(envs, 0)
      envs[0].reset()
      self._confirm_only_active_index(envs, 0)
      envs[0].reset()
      self._confirm_only_active_index(envs, 0)
      envs[0].reset()
      self._confirm_only_active_index(envs, 0)
      # The calls should be passed to the parent env.
      self.assertEqual(env.recorded_calls,
                       ['reset', 'reset', 'reset', 'reset'])

  def test_time_slicing(self) -> None:
    with gym.make(_MOCK_ENV_ID) as env:
      env.reset()
      assigner = experiment_assigner.ExperimentAssigner(
          env, divert_on=_ALL_EVENTS)
      self.next_mock_random = [0.4]
      envs = assigner.randomized_slicer([0.3, 0.2, 0.5])
      self.assertTrue(len(envs), 3)
      # Since random number is 0.4, only env[1] will be active on start.
      self._confirm_only_active_index(envs, 1)
      # Activate and confirm index 2.
      self.next_mock_random = [0.6]
      envs[1].reset()
      self._confirm_only_active_index(envs, 2)
      # Reactivate and confirm index 2.
      self.next_mock_random = [0.7]
      envs[2].reset()
      self._confirm_only_active_index(envs, 2)
      # Activate and confirm index 1.
      self.next_mock_random = [0.4]
      envs[2].reset()
      self._confirm_only_active_index(envs, 1)
      # The calls should have all been passed to the parent env.
      self.assertEqual(env.recorded_calls,
                       ['reset', 'reset', 'reset', 'reset'])

  def test_num_attempts(self) -> None:
    with gym.make(_MOCK_ENV_ID) as env:
      env.reset()
      assigner = experiment_assigner.ExperimentAssigner(
          env, divert_on=_ALL_EVENTS, num_attempts=3)
      self.next_mock_random = [0.4]
      envs = assigner.randomized_slicer([1.0])
      # Diversion #1 is active.
      self.assertTrue(len(envs), 3)
      self.assertTrue(envs[0].is_active())
      self.assertFalse(assigner._done_enough_attempts.is_set())
      envs[0].reset()
      # Diversion #2 is active.
      self.assertTrue(envs[0].is_active())
      self.assertFalse(assigner._done_enough_attempts.is_set())
      envs[0].reset()
      # Diversion #3 is active.
      self.assertTrue(envs[0].is_active())
      self.assertFalse(assigner._done_enough_attempts.is_set())
      envs[0].reset()

      # Confirm no environment is active.
      self.assertFalse(envs[0].is_active())
      self.assertTrue(assigner._done_enough_attempts.is_set())
      # Confirm that .wait() is not blocking.
      assigner.wait()

      # The calls should have all been passed to the parent env.
      self.assertEqual(env.recorded_calls, ['reset', 'reset', 'reset', 'reset'])

  def test_randomized_run(self) -> None:

    # Record all divert reasons using a custom handler.
    session_end_reasons = []

    def custom_divert_handler(unused_env: reach_env.ReachEnv,
                              reason: pausable_env.SessionEndReason) -> bool:
      nonlocal session_end_reasons
      session_end_reasons.append(reason)
      return True

    # Run the attempt only 5 times, and then raise an exception to stop the
    # thread.
    runcount = 0

    def runner(env: reach_env.ReachEnv) -> None:
      nonlocal runcount
      env.step({})
      runcount += 1
      print(runcount)

    # Execute `randomized_run()`.
    with gym.make(_MOCK_ENV_ID) as env:
      env.reset()
      mock_runner = mock.Mock(side_effect=runner)
      experiment_assigner.randomized_run(
          env, [mock_runner], divert_hook=custom_divert_handler, num_attempts=5)

    # Expect that the agent was called 5 times.
    self.assertEqual(mock_runner.call_count, 5)
    # Expect that the agent was called with the correct env.
    called_with_env = mock_runner.call_args[0][0]
    self.assertIsInstance(called_with_env, pausable_env.PausableEnv)
    # Expect that the agent ran 5 times, so there would be 5 steps.
    self.assertEqual(env.recorded_calls,
                     ['reset', 'step', 'step', 'step', 'step', 'step', 'close'])
    # There should be 5 total diversions including the first run, matching
    # num_attempts.
    self.assertEqual(session_end_reasons, [
        pausable_env.SessionEndReason.AGENT_FINISHED,
        pausable_env.SessionEndReason.AGENT_FINISHED,
        pausable_env.SessionEndReason.AGENT_FINISHED,
        pausable_env.SessionEndReason.AGENT_FINISHED,
        pausable_env.SessionEndReason.AGENT_FINISHED,
    ])

  def test_randomized_run_one_at_a_time(self) -> None:

    # This is set if the runner started when another one is already running.
    # This is an error condition, and we test that it doesn't turn on.
    simultanious_active = False

    # Set to True by a runner when it starts, and False when it stops.
    runner_active = False

    # This runs on a different thread, so assert will not work inside.
    def runner(env: reach_env.ReachEnv) -> None:
      nonlocal simultanious_active
      nonlocal runner_active
      if runner_active:
        simultanious_active = True
      runner_active = True
      env.step({})
      runner_active = False

    mock_runner1 = mock.Mock(side_effect=runner)
    mock_runner2 = mock.Mock(side_effect=runner)
    mock_runner3 = mock.Mock(side_effect=runner)

    # Execute `randomized_run()`.
    self.next_mock_random = [0.2, 0.5, 0.8] * 10
    with gym.make(_MOCK_ENV_ID) as env:
      env.reset()
      experiment_assigner.randomized_run(
          env, [mock_runner1, mock_runner2, mock_runner3], num_attempts=30)

    # Following should be True because of the mocked random.
    self.assertEqual(mock_runner1.call_count, 10)
    self.assertEqual(mock_runner2.call_count, 10)
    self.assertEqual(mock_runner3.call_count, 10)

    # Test that in no instant multiple runners were active together.
    self.assertFalse(simultanious_active)

  def test_bad_probability_sum(self) -> None:
    with gym.make(_MOCK_ENV_ID) as env:
      env.reset()
      assigner = experiment_assigner.ExperimentAssigner(env)
      self.next_mock_random = [0.1]
      with self.assertRaises(ValueError):
        _ = assigner.randomized_slicer([0.3, 0.2, 0.7])

  def test_specified_run_id(self) -> None:
    with gym.make(_MOCK_ENV_ID) as env:
      _ = experiment_assigner.ExperimentAssigner(env, run_id='test-run-id')
      env_params = env.task_params
      self.assertEqual(env_params['experiment_run_id'], 'test-run-id')

  def test_generated_run_id(self) -> None:
    with gym.make(_MOCK_ENV_ID) as env:
      _ = experiment_assigner.ExperimentAssigner(env)
      env_params = env.task_params
      self.assertRegex(
          env_params['experiment_run_id'],
          r'^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}-[0-9a-z]{16}$')

  def test_icdf(self) -> None:
    cdf = [0.3, 0.5, 1.0]
    test_cases = [(-0.1, 0),
                  (0, 0),
                  (0.01, 0),
                  (0.3, 0),
                  (0.31, 1),
                  (0.5, 1),
                  (0.51, 2),
                  (1.0, 2),
                  (1.1, 2)]
    with gym.make(_MOCK_ENV_ID) as env:
      assigner = experiment_assigner.ExperimentAssigner(env)
      for u, index in test_cases:
        self.assertEqual(assigner._icdf(cdf, u), index,
                         f'icdf({u}) != {index}')

  def setUp(self) -> None:
    super().setUp()
    # Any call to random.random() returns from this array.
    # The last number repeates.
    self.next_mock_random = [0.1]

    def mock_random() -> float:
      if len(self.next_mock_random) > 1:
        return self.next_mock_random.pop()
      return self.next_mock_random[0]

    self.patcher = mock.patch.object(random, 'random', side_effect=mock_random)
    self.patcher.start()

  def tearDown(self) -> None:
    super().tearDown()
    self.patcher.stop()


if __name__ == '__main__':
  unittest.main()
