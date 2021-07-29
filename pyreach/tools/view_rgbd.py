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

"""RGBD viewer."""

import argparse
import os
import sys

from pyreach.tools.lib import view_rgbd


def main() -> None:
  parser = argparse.ArgumentParser(description="3D Depth Viewer")
  parser.add_argument(
      "--depth", help="The path to the depth file to be viewed", required=True)
  parser.add_argument(
      "--color",
      help="The path to the color file that will colorize the depth",
      required=True)
  parser.add_argument(
      "--intrinsics",
      nargs="+",
      type=float,
      help="A list of 4 floats in the order fx, fy, cx, cy for the camera",
      required=True)
  parser.add_argument(
      "--distortion",
      nargs="+",
      type=float,
      help="A list of 5 or 8 floats in the order k1, k2, p1, p2, k3, k4, k5, k6",
      required=True)
  args = parser.parse_args()

  if not os.path.exists(args.depth):
    print("Please specify a valid path for a depth file")
    sys.exit(1)
  if not os.path.exists(args.color):
    print("Please specify a valid path for a color file")
    sys.exit(1)
  if len(args.intrinsics) != 4:
    print("The intrinsics arg needs to be a list of 4 parameters in the "
          "order fx, fy, cx, cy")
    sys.exit(1)
  if len(args.distortion) not in (5, 8):
    print("The distortion arg needs to be a list of 5 or 8 parameters"
          "in the order k1, k2, p1, p2, k3, k4, k5, k6")
    sys.exit(1)

  v = view_rgbd.RgbdViewer()
  v.set_calibration(args.intrinsics, args.distortion)
  v.update_image(args.depth, args.color)
  v.wait_until_closed()


if __name__ == "__main__":
  main()
