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
"""Viewer displays camera images for a Reach workcell."""

from typing import List

from absl import app  # type: ignore
from absl import flags  # type: ignore

from pyreach.tools.lib import async_viewer_controller

flags.DEFINE_integer("c", 0, "The type of the camera.")
flags.DEFINE_integer("o", None, "The type of the overlay.")
flags.DEFINE_boolean("t", False, "Use tagged request.")

_camera_names = {
    0: "color-camera",
    1: "depth-camera",
    2: "depth-camera.wrist",
    3: "depth-camera.invoice",
    4: "vnc.vnc0",
    5: "depth-camera.out1",
    6: "depth-camera.out2",
    7: "depth-camera.out3",
    8: "oracle.pick-points",
}


def main(argv: List[str]) -> None:  # pylint: disable=unused-argument
  cameras = _camera_names[0]
  print("Example usage: python main.py -c 1")
  print("Valid IDs:")
  for cid, name in _camera_names.items():
    print("\t{} - {}".format(cid, name))

  if flags.FLAGS.c:
    cameras = _camera_names[int(flags.FLAGS.c)]

  if flags.FLAGS.o:
    cameras += "+" + _camera_names[int(flags.FLAGS.o)]

  requested_cameras = async_viewer_controller.parse_cameras(cameras)
  control = async_viewer_controller.Controller(
      camera_names=requested_cameras,
      reqfps=10,
      uwidth=0,
      show_undistortion=False,
      use_tags=flags.FLAGS.t,
      show_detections=False,
      quiet=True,
      request_oracles=True)
  control.run()


if __name__ == "__main__":
  app.run(main)
