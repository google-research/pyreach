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
"""Camera viewer over reach connect.

Example invocations -

  # Standard operation -
  python main.py --cameras=color-camera
  python main.py --cameras=depth-camera

  # Overlay "oracle.pick-points" on "depth-camera" -
  python main.py --cameras=depth-camera+oracle.pick-points

  # Open depth-camera and color-camera simultaneously -
  python main.py --cameras=depth-camera,color-camera

  # Open multiple color-camera cameras -
  python main.py --cameras=color-camera.cam1,color-camera.cam2,color-camera.cam3

  # Use disovery -
  python main.py

"""

# This was forked from scripts/viewer/main.py.
# Mainly to support -
# - concurrent view of multiple feeds in one program,
# - arbitrary device names and types,
# - asynchronous grabbing of images.

import argparse

from pyreach.tools.lib import async_viewer_controller


def main() -> None:
  parser = argparse.ArgumentParser()
  parser.add_argument(
      "--cameras",
      required=False,
      default="",
      help=("Comma separated list of devices to be viewed. "
            "E.g. depth-camera,color-camera.cam1,color-camera.cam2"))
  parser.add_argument(
      "--reqfps",
      type=float,
      default=10,
      help="Fps at which frame requests are sent.")
  parser.add_argument(
      "--tags", action="store_true", help="Use tagged requests where possible.")
  parser.add_argument(
      "--undistortion-field",
      action="store_true",
      help=("Shows vector field showing how undistortion changes pixels "
            "for images that have calibration."))
  parser.add_argument(
      "--uwidth",
      type=int,
      default=1280,
      help="Width of unified window. If 0, will draw images on separate windows."
  )
  parser.add_argument(
      "--force_unified",
      default=False,
      action="store_true",
      help=(
          "Uses \"unified\" view even if only one stream is requested. "
          "Overrides default behavior to stream raw images at native resolution. "
          "Useful to see resolution, fps etc."))
  parser.add_argument(
      "--disable_crosshair",
      default=False,
      action="store_true",
      help="Disables the crosshair at centre of images.")
  parser.add_argument(
      "--request_oracles",
      default=False,
      action="store_true",
      help="Send inference requests to the oracle devices.")
  args = parser.parse_args()

  uwidth: int = args.uwidth

  requested_cameras = async_viewer_controller.parse_cameras(args.cameras)
  if len(requested_cameras) == 1 and not args.force_unified:
    print("NOTE: Original image size(s) will be used for single source.")
    uwidth = 0
  else:
    print("NOTE: Showing multiple image sources on single window. "
          "Use --uwidth=0 to force separate windows.")

  control = async_viewer_controller.Controller(
      camera_names=requested_cameras,
      reqfps=args.reqfps,
      uwidth=uwidth,
      show_undistortion=args.undistortion_field,
      use_tags=args.tags,
      show_detections=True,
      quiet=False,
      show_crosshair=not args.disable_crosshair,
      request_oracles=args.request_oracles)
  control.run()


if __name__ == "__main__":
  main()
