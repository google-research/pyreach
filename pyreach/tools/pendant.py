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

"""Pendant displays a control pendant for a Reach workcell.

Sample blaze command:
  blaze run --define OPENCVX_USE_QT=true --config=grte_v5
  //robotics/learning/reach/third_party/pyreach/tools:pendant

Sample non-blaze command:
  python3 pendant.py
"""
from typing import List
from absl import app  # type: ignore
from absl import flags  # type: ignore
from pyreach.tools.lib import pendant_lib

flags.DEFINE_multi_string("robot_id", None, "The robot id to connect to.")


def _main(argv: List[str]) -> None:
  """Run the main for the pendant."""
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")

  pendant_lib.run_pendants(
      flags.FLAGS.robot_id if flags.FLAGS.robot_id else [""], None)


if __name__ == "__main__":
  app.run(_main)
