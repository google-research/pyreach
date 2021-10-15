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

"""Reach depth camera element used for configuration."""

import dataclasses
from typing import Optional, Tuple

from pyreach.gyms import reach_element


@dataclasses.dataclass(frozen=True)
class ReachDepthCamera(reach_element.ReachElement):
  """Depth Camara configuration class.

  Attributes:
    reach_name: Name of the depth camera.  This name must match the name used by
      the remote robot host (e.g. "photoneo", "realsense", etc.)
    shape: The shape (dx, dy) of the depth image with a type of np.unint8.
    color_enabled: If True, color images are enabled.  The ndarray shape same as
      the depth camera shape (i.e.  (dx, dy, 3).) The pixel values are np.uint8.
    force_fit: If True, any misconfigured cameras are simply cropped to shape.
      must match shape.  A PyReachError is raised for
    is_synchronous: If True, the next Gym observation will synchronize all
      observactions element that have this flag set otherwise the next
      observation is asynchronous.  This argument is optional and defaults to
      False.  There is no way to validate the image shape at initialization
      time. Instead, a PyReach exception is raised when the shape mismatch is
      first detected.  Setting force_fit to True avoids the exception and simply
      crops the image to shape.
    lens_mode: When calibration is enabled, this needs to be either "pinhole" of
      "fisheye".
    link_name: When calibration is enabled, this should specify the URDF link
      name to use for getting the camera pose.
  """
  shape: Tuple[int, int]
  color_enabled: bool
  force_fit: bool = False
  is_synchronous: bool = False
  calibration_enable: bool = False
  lens_model: Optional[str] = None
  link_name: Optional[str] = None
