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

import threading
from typing import Any, Dict, List, Tuple

import unittest
from unittest import mock

import gym  # type: ignore
from pyreach import host
from pyreach.gyms import core as gyms_core
from pyreach.gyms import pausable_env
from pyreach.gyms import reach_env
from pyreach.gyms.registration import register
from pyreach.mock import host_mock

GYMS_PATH = ''
_MOCK_ENV_ID: str = 'test_env-v0'


def setUpModule() -> None:
  class_name: str = 'FakeReachEnv'
  entry_point: str = GYMS_PATH + 'pausable_env_test:' + class_name
  register(
      id=_MOCK_ENV_ID,
      entry_point=entry_point,
      max_episode_steps=200,
      reward_threshold=25.0)


class FakeReachEnv(reach_env.ReachEnv):
  """A fake ReachEnv for testing."""

  def __init__(self, **kwargs: Any) -> None:
    pyreach_config: Dict[str, reach_env.ReachElement] = {}

    mock_host: host.Host = host_mock.HostMock(pyreach_config)
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

  def reset(self) -> gyms_core.Observation:
    self.recorded_calls.append('reset')
    return {}

  def close(self) -> None:
    self.recorded_calls.append('close')
    return super().close()


class PausableEnvTest(unittest.TestCase):
  """Test ability to pause and resume environments."""

  def test_pause_event_states(self) -> None:
    with gym.make(_MOCK_ENV_ID) as env:
      pausable = pausable_env.PausableEnv(env, start_paused=True)
    with gym.make(_MOCK_ENV_ID) as env:
      pausable = pausable_env.PausableEnv(env, start_paused=False)
      self.assertTrue(pausable._is_active.is_set())
      pausable.pause()
      self.assertFalse(pausable._is_active.is_set())

  def test_pause_pauses(self) -> None:
    # Test that pause indeed pauses the calls.
    with gym.make(_MOCK_ENV_ID) as env:
      pausable = pausable_env.PausableEnv(env, start_paused=True)

      with mock.patch.object(
          pausable._is_active, 'wait',
          wraps=pausable._is_active.wait) as mock_wait:

        self.assertEqual(mock_wait.call_count, 0)

        def reset_and_step() -> None:
          pausable.reset()
          pausable.step({})

        t = threading.Thread(target=reset_and_step)
        t.start()

        # Wait till the _is_active event is waited on.
        # Also confirms that _is_active was indeed waited on.
        while mock_wait.call_count == 0:
          pass

        # No call should have been allowed before resume.
        self.assertEqual(env.recorded_calls, [])

        # Resuming the environment should cause the reset to finally happen.
        pausable.resume()
        t.join()
        self.assertEqual(env.recorded_calls, ['reset', 'step'])

  def test_callback(self) -> None:
    session_callback = mock.Mock()
    with gym.make(_MOCK_ENV_ID) as env:
      pausable = pausable_env.PausableEnv(env, start_paused=False)
      pausable.add_session_end_callback(session_callback, 'callback_context')
      self.assertEqual(session_callback.call_count, 0)
      pausable.reset()
      self.assertEqual(session_callback.call_count, 1)
      pausable.step({})
      self.assertEqual(session_callback.call_count, 1)
      pausable.step({'done': True})
      self.assertEqual(session_callback.call_count, 2)
    self.assertEqual(session_callback.call_args_list, [
        mock.call(pausable_env.SessionEndReason.AGENT_CALLED_RESET,
                  'callback_context'),
        mock.call(pausable_env.SessionEndReason.STEP_RETURNED_DONE,
                  'callback_context')
    ])

  def test_calls_go_to_parent(self) -> None:
    with gym.make(_MOCK_ENV_ID) as env:
      pausable = pausable_env.PausableEnv(env, start_paused=True)
      pausable.resume()
      pausable.reset()
      self.assertEqual(env.recorded_calls, ['reset'])
      step_result = pausable.step({})
      self.assertEqual(len(step_result), 4)
      self.assertEqual(env.recorded_calls, ['reset', 'step'])
      pausable.close()
      self.assertEqual(env.recorded_calls, ['reset', 'step', 'close'])

  def test_context_is_saved(self) -> None:
    with gym.make(_MOCK_ENV_ID) as env:
      pausable = pausable_env.PausableEnv(env, start_paused=False)
      pausable.pause()
      with mock.patch.object(env, 'set_agent_id', wraps=env.set_agent_id) as m:
        pausable.resume()
        # No previous calls to set_agent_id have been made.
        m.assert_not_called()

    with gym.make(_MOCK_ENV_ID) as env:
      pausable = pausable_env.PausableEnv(env, start_paused=False)
      pausable.set_agent_id('agent_utopia-v0')
      pausable.pause()
      with mock.patch.object(env, 'set_agent_id', wraps=env.set_agent_id) as m:
        m.assert_not_called()
        # resume() should restore the last agent id used.
        pausable.resume()
        m.assert_called_once_with('agent_utopia-v0')


if __name__ == '__main__':
  unittest.main()
