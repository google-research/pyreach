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

"""Shared utility functions for PyReach implementation."""

import time
import uuid

from pyreach import core
from pyreach.common.python import types_gen


def time_at_timestamp(timestamp_ms: int) -> float:
  """Convert millisecond Epoch timestamp to Python float time value.

  Args:
    timestamp_ms: Epoch timestamp in milliseconds.

  Returns:
    Python time value in float.

  """
  return float(timestamp_ms) / 1000.0


def timestamp_at_time(time_sec: float) -> int:
  """Convert Python float time value to millisecond Epoch timestamp.

  Args:
    time_sec: Python time value in seconds.

  Returns:
    Epoch timestamp in milliseconds.

  """
  return int(time_sec * 1000)


def timestamp_now() -> int:
  """Return the current epoch time in milliseconds."""
  return timestamp_at_time(time.time())


def generate_tag() -> str:
  """Generate a unique random tag."""
  return str(uuid.uuid4())


def pyreach_status_from_message(
    msg: types_gen.DeviceData) -> core.PyReachStatus:
  """Extract PyReachStatus from a DeviceData message.

  Args:
    msg: The source DeviceData instance.

  Returns:
    The decoded PyReachStatus object.

  """
  return core.PyReachStatus(
      time=time_at_timestamp(msg.ts),
      sequence=msg.seq,
      status=msg.status,
      script=msg.script,
      error=msg.error,
      progress=msg.progress,
      message=msg.message,
      code=msg.code)


def convert_pyreach_status(status: core.PyReachStatus) -> types_gen.Status:
  """Convert a PyReachStatus to a types_gen Status.

  Args:
    status: The PyReachStatus.

  Returns:
    The types_gen status.
  """
  return types_gen.Status(
      code=status.code,
      error=status.error,
      message=status.message,
      progress=status.progress,
      script=status.script,
      status=status.status)


def reverse_pyreach_status(status: types_gen.Status,
                           timestamp: float = 0.0,
                           sequence: int = 0) -> core.PyReachStatus:
  """Convert a PyReachStatus from a types_gen Status.

  Args:
    status: The types_gen Status.
    timestamp: The time this status is generated.
    sequence: the sequence number for the status.

  Returns:
    The PyReachStatus.
  """
  return core.PyReachStatus(
      time=timestamp,
      sequence=sequence,
      code=status.code,
      error=status.error,
      message=status.message,
      progress=status.progress,
      script=status.script,
      status=status.status)
