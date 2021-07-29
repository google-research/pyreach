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

"""Provides mechanisms to time-slice Reach Gym Environments.

Example usage -

  agent1 = KittingAgent()
  agent2 = KittingAgent(new_features=True)
  with gym.make("benchmark-kitting-v0") as env:
    env_time_slicer.randomized_run(
      env,                       # Environment.
      [agent1.attempt, agent2.attempt],  # Functions to run different agents.
      [0.3, 0.7],                # Proportion of times an agent gets control.
      divert_on={pausable_env.SessionEndReasons.AGENT_FINISHED},
                                 # Optional set of reasons when to divert.
      run_id = 'test'            # Optional id to find this in the logs.
    )

The usage above assumes that agent1.run() and agent2.run() return control after
each attempt. This is the recommended way to set up the agents for experiments.
"""
import bisect
import datetime
import random
import string
import sys
import threading

from typing import Any, Callable, Iterable, List, Optional

from pyreach.gyms import pausable_env
from pyreach.gyms import reach_env

_TOLERANCE = 1e-6


class ExperimentAssigner:
  """Manages multiple environments keeping exactly one active at a time."""

  def __init__(
      self,
      env: reach_env.ReachEnv,
      run_id: Optional[str] = None,
      divert_on: Optional[Iterable[pausable_env.SessionEndReason]] = None,
      divert_hook: Optional[Callable[
          [reach_env.ReachEnv, pausable_env.SessionEndReason], bool]] = None,
      num_attempts: Optional[int] = None):
    """Instantiates a Gym Environment Time Slicer.

    This object can be used to share an environment between multiple agents.

    Note that the randomized_run() method provides a convenient entry point
    for this object, and in most cases one would not need to instantiate it
    directly.

    Args:
      env: The environment which needs to be shared.
      run_id: Optional context that will be logged. If not specified, a unique
        id will be generated and logged.
      divert_on: Can be passed to restrict diversion only to certain
        reasons. E.g. divert_on={AGENT_FINISHED, AGENT_CALLED_RESET}.
        Defaults to {AGENT_FINISHED}, which assumes that the agents will return
        control after each attempt.
      divert_hook: A method that will be called every time a diversion decision
        needs to be taken. If the method returns False, the agent will not be
        changed.
        E.g. to ensure diversion only on resets -
          divert_hook=lambda _, reason: reason == AGENT_CALLED_RESET
        E.g. to call reset between all diversions -
          divert_hook=lambda env, _: env.reset() or True.
       num_attempts: If passed, the assignmer will stop after exactly this many
         attempts are completed. This is should usually be paired with a call to
         .wait(), which blocks until this happens.
    """
    self._env = env

    self._run_id: Optional[str] = run_id
    self._validate_and_store_run_id()

    self._sub_envs: List[pausable_env.PausableEnv] = []
    self._cumulative_props: List[float] = []  # Filled by randomized_slicer()

    self._divert_on = {pausable_env.SessionEndReason.AGENT_FINISHED}
    if divert_on is not None:
      self._divert_on = set(divert_on)

    self._divert_hook = divert_hook

    self._num_attempts = num_attempts
    self._done_enough_attempts = threading.Event()

    # Number of time an diversion happened.
    self._diversion_count = 0

  def _validate_and_store_run_id(self) -> None:
    """Stores the run_id for logging.

    If self._run_id is None, generates a new one.
    """
    if self._run_id is None:
      # Create a randomized id based on current date and time.
      timestamp_str = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
      random_str = ''.join(
          random.choice(string.digits + string.ascii_lowercase)
          for _ in range(16))
      self._run_id = timestamp_str + '-' + random_str

    self._env.task_params['experiment_run_id'] = self._run_id
    sys.stderr.write(f'Stored run_id as: {self._run_id!r}\n')

  def _on_session_end(self, reason: pausable_env.SessionEndReason,
                      session_index: int) -> None:
    """Handles session-end notification."""
    if reason not in self._divert_on:
      return
    if self._divert_hook is not None:
      # Do not change agent if the divert_hook() returns False.
      if not self._divert_hook(self._env, reason):
        return

    # The pause will be called on the same thread, hence it will be invoked
    # before any new command that needs to be blocked.
    self._sub_envs[session_index].pause()
    sys.stderr.write(
        f'ExperimentAssigner Paused environment #{session_index}\n')

    self._roll_dice_and_resume()

  @staticmethod
  def _icdf(cdf: List[float], value: float) -> int:
    """Randomly selects one index given cumulative probabilities.

    Args:
      cdf: A list with floats in ascending order. For a proper probability CDF,
        it will also end at 1, but we don't force the CDF to be normalized.
      value: A number between 0 and cdf[-1].

    Returns:
      An int between 0 to len(cdf) - 1. If value is selected at random, this
      number will be a random index drawn from the CDF as defined by cdf.
    """
    index = bisect.bisect_left(cdf, value)
    # Index may be larger if value > cdf[-1] (e.g. floating point rounding).
    if index >= len(cdf):
      index -= 1
    return index

  def _roll_dice_and_resume(self) -> None:
    """Selects an environment at random and resumes it."""
    self._diversion_count += 1
    if self._num_attempts is not None:
      if self._diversion_count > self._num_attempts:
        self._done_enough_attempts.set()
        # We are now in a state where the environment is completely paused.
        return
    sys.stderr.write(f'EnvTimeSlicer Diversion #{self._diversion_count}\n')
    new_env_index = self._icdf(self._cumulative_props, random.random())
    self._sub_envs[new_env_index].resume()
    sys.stderr.write(f'EnvTimeSlicer Resumed environment #{new_env_index}\n')

  def randomized_slicer(self,
                        proportions: List[float]) -> List[reach_env.ReachEnv]:
    """Returns a list of env's which will get traffic as defined by proportions.

    Args:
      proportions: Set of probabilities. Should be positive and sum up to 1.

    Returns:
      A list of environments, one each for proportions passed as arg. It will
      be guaranteed that only one environment will be active at a time, chosen
      at random. Also over long period of time, number of times a particular
      env is activated will converge to the requested proportions.
    """
    self._cumulative_props = []
    self._sub_envs = []
    cumulative_proportion = 0.0  # Total proportion accounted for so far.

    # Create a sub environment for each traffic.
    for index, proportion in enumerate(proportions):
      subenv = pausable_env.PausableEnv(self._env, start_paused=True)
      subenv.add_session_end_callback(self._on_session_end, index)
      cumulative_proportion += proportion
      self._cumulative_props.append(cumulative_proportion)
      self._sub_envs.append(subenv)

    if abs(cumulative_proportion - 1) > _TOLERANCE:
      raise ValueError(
          f'Proportion of traffic {proportions!r} does not sum to 1')

    self._roll_dice_and_resume()
    return self._sub_envs

  def wait(self) -> None:
    """Blocks until we finish number of attempts passed as num_attempts."""
    self._done_enough_attempts.wait()


def _run_agent(env: pausable_env.PausableEnv,
               agent_attempt: Callable[[reach_env.ReachEnv], None]) -> None:
  """Runs agent in loop, sends a notification to the env each time it ends."""
  env.wait_till_active()
  while True:
    agent_attempt(env)
    # Communicate to pausable environment that attempt has finished.
    env.agent_ended()


def randomized_run(env: reach_env.ReachEnv,
                   runners: List[Callable[[reach_env.ReachEnv], None]],
                   traffic: Optional[List[float]] = None,
                   **kwargs: Any) -> None:
  """A method to run multiple environments with time-sharing.

  This is a convenience method, which will need to be stopped with Ctrl+C.
  If more flexibility is needed, consider instancing and using EnvTimeSlicer
  directly.

  Args:
    env: The env on which the runners will work. Internally new sub-env's will
      be created and each runner will be passed one.
    runners: A function, typycally the .run() of an agent, which takes an env.
    traffic: The proportions of traffic for each runner. If unspecified,
      will use equal traffic.
    **kwargs: Additional arguments for EnvTimeSlicer, e.g. run_id.
  """
  assigner = ExperimentAssigner(env, **kwargs)
  if traffic is None:
    traffic = [1.0 / len(runners)] * len(runners)
  envs = assigner.randomized_slicer(traffic)
  threads: List[threading.Thread] = []
  # Create and start threads for each runner with corresponding env.
  for env, runner in zip(envs, runners):
    threads.append(
        threading.Thread(target=_run_agent, args=[env, runner], daemon=True))
    threads[-1].start()
  # Wait till the environment stops. This is needed to return control if
  # num_attempts was passed.
  assigner.wait()
