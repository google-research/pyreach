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

"""Implements a wrapper to PyReach env that allows pausing and resuming it.

This is used as a building blcok for EnvTimeSlicer().
"""

import enum
import threading

from typing import Any, Callable, List, Optional, Tuple

import gym  # type: ignore
from pyreach.gyms import reach_env


class SessionEndReason(enum.Enum):
  """Enumerates different reasons for detecting that a session has ended.

  Used by PausableEnv to notify why a session was detected to have ended.
  """
  AGENT_CALLED_RESET = 1
  STEP_RETURNED_DONE = 2
  AGENT_FINISHED = 3


class PausableEnv(gym.Wrapper):
  """Makes a gym environment pausable.

  This environment wrapper allows the environment to be paused and resumed at
  will. When paused, any calls that might modify the environment (such as move
  the robot), will be blocked (i.e. the code path will be put on hold).

  Example usage -

    pausable_env = PausableEnv(env)

    # Start an agent in the background.
    threading.Thread(target=agent.run, args=[pausable_env]).start()

    # The environment may be paused or resumed at any time.
    # Pausing will continue work until the next command from the agent.
    # The next method called by the agent will not return until env resumes.
    pausable_env.pause()

    # On resume(), the env will be marked active. If any agent was running and
    # blocked, it will immediately get control back.
    # Context such as agent id will be monitored and restored on resume.
    pausable_env.resume()

  """

  def __init__(self,
               env: reach_env.ReachEnv,
               start_paused: bool = False) -> None:
    super().__init__(env)

    self._env = env
    # Event to know if the environment is active or paused.
    self._is_active = threading.Event()

    # Since the agent id can be changed while this env is paused, we
    # remember the agent id and set it again on resume.
    self._last_agent_id: Optional[str] = None

    # Contains a tuple with a custom context, and a callback.
    # The callback will be called as -
    #   callback(session_end_reason, custom_context).
    # The custom_context can be defined in add_session_callback().
    self._session_end_callbacks: List[Tuple[Any,
                                            Callable[[SessionEndReason, Any],
                                                     None]]] = []

    if not start_paused:
      self.resume()

  def is_active(self) -> bool:
    return self._is_active.is_set()

  def wait_till_active(self) -> None:
    self._is_active.wait()

  def pause(self) -> None:
    """Pauses this environment.

    All calls that may require the environment to do something will be paused,
    until resume() is called.
    """
    self._is_active.clear()

  def resume(self) -> None:
    """Resumes this particular environment."""
    if self._last_agent_id is not None:
      self._env.set_agent_id(self._last_agent_id)
    self._is_active.set()

  def _delegate(self, method: Callable[..., Any], *args: Any,
                **kwargs: Any) -> Any:
    self._is_active.wait()
    return method(*args, **kwargs)

  def _notify_new_session(self, session_end_reason: SessionEndReason) -> None:
    """Notifies any handlers that a session has ended."""
    for custom_context, on_session_end in self._session_end_callbacks:
      on_session_end(session_end_reason, custom_context)

  def add_session_end_callback(self,
                               fn: Callable[[SessionEndReason, Any], None],
                               context: Any = None) -> None:
    self._session_end_callbacks.append((context, fn))

  def agent_ended(self) -> None:
    """Can be called by an agent to communicate that a session has ended."""
    self._notify_new_session(SessionEndReason.AGENT_FINISHED)
    # The environment may get paused as a result of the call above.
    # If so, we block the agent which called this method until resumed.
    self._is_active.wait()

  # Override all methods that need to be paused when this env is not activated.
  def step(self, *args: Any, **kwargs: Any) -> Any:
    result = self._delegate(self._env.step, *args, **kwargs)
    done = result[2] if len(result) >= 2 else False
    if done:
      self._notify_new_session(SessionEndReason.STEP_RETURNED_DONE)
    return result

  def reset(self, *args: Any, **kwargs: Any) -> Any:
    result = self._delegate(self._env.reset, *args, **kwargs)
    self._notify_new_session(SessionEndReason.AGENT_CALLED_RESET)
    return result

  def render(self, *args: Any, **kwargs: Any) -> Any:
    return self._delegate(self._env.render, *args, **kwargs)

  def close(self, *args: Any, **kwargs: Any) -> Any:
    return self._delegate(self._env.close, *args, **kwargs)

  def set_agent_id(self, agent_id: str) -> None:
    self._last_agent_id = agent_id
    return self._delegate(self._env.set_agent_id, agent_id)
