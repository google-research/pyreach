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

import hashlib
import os
import shutil
import stat
import subprocess
import sys
from typing import Sequence

from absl import app  # type: ignore
from absl import flags  # type: ignore
import requests

FLAGS = flags.FLAGS

flags.DEFINE_string("o",
                    os.path.join(os.getenv("HOME") or "",
                                 "reach_workspace"), "Reach working directory")

WEBRTC_SHA256 = "afeb5d7fe13823c4316894823e0b9b10aadefa609eb2623dc218118866beb1ca"
REACH_SHA256 = "428af9a7560e1db1f60b531bdfd3db58eb10412841c121de11fb56c57540e7d6"
WEBRTC_BASE = "https://storage.googleapis.com/brain-reach-public/releases/webrtc/linux-x86_64/webrtc_headless."
REACH_BASE = "https://storage.googleapis.com/brain-reach-public/releases/reach/linux-x86_64/reach."

_is_running_on_google3 = False


def _download(base: str, digest: str, folder: str, save_as: str) -> None:
  """Download an executable file.

  Args:
    base: the base URL.
    digest: the digest of the file.
    folder: download to folder.
    save_as: save as file name.

  Raises:
    SystemError: if the file cannot be downloaded.

  """
  target_file = os.path.join(folder, save_as)
  if os.path.exists(target_file):
    bin_file = open(target_file, "rb")
    bin_content = bin_file.read()
    bin_file.close()

    sha = hashlib.sha256()
    sha.update(bin_content)
    if sha.hexdigest() == digest:
      return

  remote_file = requests.get(base + digest, allow_redirects=True)
  sha = hashlib.sha256()
  sha.update(remote_file.content)
  if sha.hexdigest() != digest:
    raise SystemError("digest mismatch for %s" % base + digest)

  if os.path.exists(target_file):
    os.remove(target_file)

  bin_file = open(target_file, "wb")
  bin_file.write(remote_file.content)
  bin_file.close()

  st = os.stat(target_file)
  os.chmod(target_file, st.st_mode | stat.S_IEXEC)


def main(unused_argv: Sequence[str]) -> None:
  workspace = FLAGS.o
  if not os.path.exists(workspace):
    os.mkdir(workspace)

  reach_file = os.path.join(workspace, "reach")
  if _is_running_on_google3:
    pass
  else:
    _download(REACH_BASE, REACH_SHA256, workspace, "reach")

  args = sys.argv[1:]
  if args and "connect" == args[
      0] and "--webrtc_headless" not in args and "-webrtc_headless" not in args:
    _download(WEBRTC_BASE, WEBRTC_SHA256, workspace, "webrtc_headless")
    webrtc_headless_file = os.path.join(workspace, "webrtc_headless")
    args = ["connect", "--webrtc_headless", webrtc_headless_file] + args[1:]

  os.chdir(workspace)
  subprocess.call([reach_file] + args)


if __name__ == "__main__":
  app.run(main)
