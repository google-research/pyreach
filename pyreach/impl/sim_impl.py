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
"""Implementation of the PyReach sim interface."""
import logging
import queue  # pylint: disable=unused-import
from typing import Callable, Optional, Tuple

from pyreach import core
from pyreach import sim
from pyreach.common.python import types_gen
from pyreach.impl import requester
from pyreach.impl import thread_util
from pyreach.impl import utils


class SimDevice(requester.Requester[core.PyReachStatus]):
  """Interface for controlling the reach sim console."""

  def get_message_supplement(
      self, msg: types_gen.DeviceData) -> Optional[core.PyReachStatus]:
    """Get additional message."""
    if (msg.device_type == "script-engine" and not msg.device_name and
        msg.data_type == "cmd-status"):
      return utils.pyreach_status_from_message(msg)
    return None

  def get_wrapper(self) -> Tuple["SimDevice", "sim.Sim"]:
    """Get wrapper for the device that should be shown to the user."""
    return self, SimImpl(self)

  def send_sim_script(
      self,
      script: str,
      timeout: Optional[float] = None,
  ) -> ("queue.Queue[Optional[Tuple[types_gen.DeviceData, "
        "Optional[core.PyReachStatus]]]]"):
    return self.send_tagged_request(
        types_gen.CommandData(
            ts=utils.timestamp_now(),
            tag=utils.generate_tag(),
            device_type="script-engine",
            data_type="run-script",
            script=script),
        timeout=timeout)


class SimImpl(sim.Sim):
  """Interface for controlling the reach sim console."""

  _device: SimDevice

  def __init__(self, device: SimDevice) -> None:
    """Construct a sim implementation.

    Args:
      device: The device to log to.
    """
    self._device = device

  def reset(self, timeout: Optional[float] = None) -> core.PyReachStatus:
    """Reset resets the simulator.

    Args:
      timeout: The time in seconds to wait for the simulator reset.

    Returns:
      PyReachStatus representing the result of the command.
    """
    q = self._device.send_sim_script("sim reset", timeout=timeout)
    msgs = thread_util.extract_all_from_queue(q)
    if not msgs:
      return core.PyReachStatus(
          utils.timestamp_now(), status="rejected", error="timeout")
    if len(msgs) != 1:
      logging.warning("expected single message, got %d", len(msgs))
    result = msgs[0][1]
    if result is None:
      return core.PyReachStatus(
          utils.timestamp_now(), status="rejected", error="timeout")
    return result

  def async_reset(self,
                  callback: Optional[Callable[[core.PyReachStatus],
                                              None]] = None,
                  finished_callback: Optional[Callable[[], None]] = None,
                  timeout: Optional[float] = None) -> None:
    """Asynchronously reset the simulator.

    Args:
      callback: callback when message is delivered.
      finished_callback: called when the reset is finished.
      timeout: The time in seconds to wait for the simulator reset.
    """
    q = self._device.send_sim_script("sim reset", timeout=timeout)

    def cb(
        msg: Tuple[types_gen.DeviceData, Optional[core.PyReachStatus]]) -> None:
      status = msg[1]
      if callback and status:
        callback(status)

    def fcb() -> None:
      if finished_callback:
        finished_callback()

    thread_util.queue_to_callback(q, cb, fcb)
