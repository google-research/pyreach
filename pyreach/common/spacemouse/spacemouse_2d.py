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
"""Test example for the spacemouse driver."""

from typing import Sequence

from absl import app  # type: ignore
from absl import flags  # type: ignore

from pyreach.common.spacemouse import spacemouse_2d_driver


def main(unused_argv: Sequence[str]) -> None:
  fs = flags.FLAGS
  driver = spacemouse_2d_driver.SpacemouseDriver(None, fs.id, fs.planar,
                                                 fs.scale, fs.gripper, fs.dt)
  driver.run()


if __name__ == "__main__":
  flags.DEFINE_integer("id", None, "Spacemouse ID to monitor.")
  flags.DEFINE_bool("planar", False, "Send only motion on the xy plane.")
  flags.DEFINE_bool("gripper", False, "Button controls gripper.")
  flags.DEFINE_float("scale", 4.0, "Scale of rotation and translation.")
  flags.DEFINE_float("dt", 0.1, "Poll time in seconds.")
  app.run(main)
