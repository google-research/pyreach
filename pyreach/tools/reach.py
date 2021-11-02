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
"""Wrapper script to download and invoke reach command automatically."""

import os
import subprocess
import sys
from typing import Sequence

from absl import app  # type: ignore
from absl import flags  # type: ignore

from pyreach.impl import reach_tools_impl

flags.DEFINE_string("o", None, "Reach working directory")


def main(unused_argv: Sequence[str]) -> None:
  workspace = flags.FLAGS.o
  if workspace is None:
    workspace = reach_tools_impl.create_reach_workspace()
  reach_file, _ = reach_tools_impl.download_reach_tool(workspace)

  args = sys.argv[1:]
  if (args and "connect" == args[0] and "--webrtc_headless" not in args and
      "-webrtc_headless" not in args and "-connect_host" not in args and
      "--connect_host" not in args):
    webrtc_headless_file = reach_tools_impl.download_webrtc_headless(workspace)
    args = ["connect", "--webrtc_headless",
            str(webrtc_headless_file)] + args[1:]

  os.chdir(workspace)
  subprocess.call([str(reach_file)] + args)


if __name__ == "__main__":
  app.run(main)
