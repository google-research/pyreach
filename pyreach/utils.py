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

"""Utility functions for PyReach implementations."""


import numpy as np  # type: ignore
from PIL import Image  # type: ignore

import cv2  # type: ignore


def load_image(filename: str) -> np.ndarray:
  """Load an image file into memory.

  Args:
    filename: name of the image file.

  Raises:
    FileNotFoundError

  Returns:
    Content of the image.
  """
  image_pil = Image.open(filename)
  image_np = np.array(image_pil)
  if len(image_np.shape) == 2:
    image_np = np.tile(image_np[..., None], (1, 1, 3))  # grey to rgb.
  return image_np


def load_depth_image(filename: str) -> np.ndarray:
  """Load a depth image into memory.

  Args:
    filename: name of the depth image file.

  Returns:
    Return the depth image as an numpy.ndarray of type nympy.uint16.
  """
  return cv2.imread(filename, cv2.IMREAD_ANYDEPTH)

