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

"""Debugging utilities."""
import inspect
import sys


def debug(msg: str) -> None:
  """Write debug message to stderr.

  Debug message consists file name, line number and function name
  of the calling routine.

  Args:
    msg: a custom message.
  """
  parent_frame = inspect.stack()[1]
  file = parent_frame[1]
  line = parent_frame[2]
  func = parent_frame[3]
  sys.stderr.write("{}:{}-{}: {}\n".format(file, line, func, msg))
  sys.stderr.flush()
