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

"""Utilities for IKFast."""

import ctypes
import logging
import math
import os
import sys
from typing import Dict, List, Optional, Union, Tuple
import numpy as np  # type: ignore
from scipy.spatial.transform import Rotation  # type: ignore
from pyreach.common.base import debug
from pyreach.common.base import transform_util

_is_running_on_google3 = False

_FloatOrInt = Union[float, int]
ArrayOrList = Union[List[_FloatOrInt], Tuple[_FloatOrInt], np.ndarray]


def _find_reach_path(cur_dir: str) -> str:
  if os.path.exists(os.path.join(cur_dir, ".reach")):
    return cur_dir
  if os.path.dirname(cur_dir) == cur_dir:
    logging.error("Can't find Reach root marked by .reach file")
    return "./"

  return _find_reach_path(os.path.dirname(cur_dir))


def _get_library_path() -> str:
  """Find library path for compiled IK fast libraries.

  Look for sub-package 'linux_so', or '.reach/third_party/ikfast/linux-so'
  Only supports Linux "so" file.

  Returns:
    Library path.

  """
  if _is_running_on_google3:
    return "./"

  current_folder = os.path.dirname(os.path.abspath(__file__))
  ur5e_so = os.path.join(current_folder, "linux_so", "libur5e_ikfast61.so")
  if os.path.exists(ur5e_so):
    return os.path.join(current_folder, "linux_so")

  reach_path = _find_reach_path(current_folder)
  sys.path.append(reach_path)
  return os.path.join(reach_path, "third_party/ikfast/linux-so")


_IKFAST_PATH = _get_library_path()

_URDF_LIB_FILEMAP: Dict[str, str] = {
    "ur5e.urdf":
        os.path.join(_IKFAST_PATH, "libur5e_ikfast61.so"),
    "ur5.urdf":
        os.path.join(_IKFAST_PATH, "libur5_ikfast61.so"),
    "XArm6.urdf":
        os.path.join(_IKFAST_PATH, "libxarm6_ikfast61.so"),
    "lrmate200ic.urdf":
        os.path.join(_IKFAST_PATH, "libFLRM200ic_ikfast61.so"),
    "lrmate200id.urdf":
        os.path.join(_IKFAST_PATH, "libFLRM200id_ikfast61.so"),
    "FanucCR7ia.urdf":
        os.path.join(_IKFAST_PATH, "libFCR7ia_ikfast61.so"),
    "FanucLrmate200id7l.urdf":
        os.path.join(_IKFAST_PATH, "libFLRM200id7l_ikfast61.so"),
    "ur10e.urdf":
        os.path.join(_IKFAST_PATH, "libur10e_ikfast61.so"),
    "FanucR2000ia165f.urdf":
        os.path.join(_IKFAST_PATH, "libFR2000ia165f_ikfast61.so"),
}

_FUNCTION_PREFIX_FILEMAP: Dict[str, str] = {
    "ur5e.urdf": "ur5e",
    "ur5.urdf": "ur5",
    "XArm6.urdf": "xarm6",
    "lrmate200ic.urdf": "FLRM200ic",
    "lrmate200id.urdf": "FLRM200id",
    "FanucCR7ia.urdf": "FCR7ia",
    "FanucLrmate200id7l.urdf": "FLRM200id7l",
    "ur10e.urdf": "ur10e",
    "FanucR2000ia165f.urdf": "FR2000ia165f",
}


class IKFast:
  """IKFast main class."""
  _urdf: str
  _libfile: str
  _libik: Optional[ctypes.CDLL]
  _ik_function: str
  _fk_function: str

  @property
  def urdf(self) -> str:
    """Get the name of the URDF file."""
    return self._urdf

  def __init__(self, urdf_file: str) -> None:
    """Create a new IKFast.

    Args:
      urdf_file: the URDF file.
    """
    self._urdf = os.path.basename(urdf_file)
    if self._urdf not in _URDF_LIB_FILEMAP:
      logging.info("ikfast.py: URDF not found in filemap.  Continuing anyway")
    self._ik_function = "ik"
    self._fk_function = "fk"

    self._libfile = _URDF_LIB_FILEMAP[self._urdf]
    if _is_running_on_google3:
      self._ik_function = _FUNCTION_PREFIX_FILEMAP[self._urdf] + "_ik"
      self._fk_function = _FUNCTION_PREFIX_FILEMAP[self._urdf] + "_fk"
      self._libik = ctypes.cdll.LoadLibrary("")
    else:
      try:
        self._libik = ctypes.cdll.LoadLibrary(self._libfile)
      except OSError:
        logging.error("Cannot load ikfast library %s", self._libfile)
        self._libik = None
        return

    getattr(self._libik, self._ik_function).argtypes = [
        np.ctypeslib.ndpointer(np.float),
        np.ctypeslib.ndpointer(np.float),
        np.ctypeslib.ndpointer(np.float)
    ]
    getattr(self._libik, self._ik_function).restype = ctypes.c_int
    getattr(self._libik, self._fk_function).argtypes = [
        np.ctypeslib.ndpointer(np.float),
        np.ctypeslib.ndpointer(np.float),
        np.ctypeslib.ndpointer(np.float)
    ]

  def ik(self, pose: ArrayOrList) -> Optional[np.ndarray]:
    """Main IK calculation.

    Args:
      pose: the pose to attempt to convert to joints.

    Returns:
      An array of joint positions for the specific pose.
    """
    if not self._libik:
      return None
    if isinstance(pose, (tuple, list)):
      pose = np.array(pose, dtype=np.float64)
    rvec = Rotation.from_rotvec(pose[3:])
    if hasattr(rvec, "as_matrix"):
      r = rvec.as_matrix()
    else:
      r = rvec.as_dcm()
    t = pose[:3].reshape((3, 1))
    solutions = np.zeros((16, 6))
    res = getattr(self._libik, self._ik_function)(t, r, solutions)
    if res > 0:
      return solutions[:res, :]
    elif res == -1:
      debug.debug("Free joint not yet supported")
      return None
    else:
      return None

  def fk(self, joints: ArrayOrList) -> Optional[np.ndarray]:
    """Convert joint angles to a pose.

    Args:
      joints: the joint angles.

    Returns:
      the pose.
    """
    if not self._libik:
      return None

    r = np.zeros((3, 3), dtype=np.float)
    t = np.zeros((1, 3), dtype=np.float)[0]
    getattr(self._libik, self._fk_function)(np.array(joints, dtype=np.float64),
                                            t, r)
    if hasattr(Rotation, "from_matrix"):
      rvec = Rotation.from_matrix(r)
    else:
      rvec = Rotation.from_dcm(r)
    r = rvec.as_rotvec()
    pose = np.concatenate((t, r))
    return pose

  # includes +/- 2*pi search on joints.  Necessary for UR5
  def ik_search(self, pose: ArrayOrList,
                ik_hints: Dict[int, List[float]]) -> Optional[np.ndarray]:
    """Perform IK search and return a single joint pose.

    Args:
      pose: The pose.
      ik_hints: The ik hints for the search.

    Returns:
      The joint position.
    """
    if not self._libik:
      return None

    solution_list = []
    poses = [pose]
    pi2 = 2 * math.pi

    for p in poses:
      res = self.ik(p)
      if res is None:
        continue

      for s in res:
        # ik fast never provide a solution beyond -pi/+pi
        # UR supports +/- 2*pi on j3,j4,j5
        #                solution_list.append(s)
        for j in [-1, 0, 1]:
          for k in [-1, 0, 1]:
            for l in [-1, 0, 1]:  # noqa: E741
              s2 = np.copy(s)
              s2[3] += j * pi2
              s2[4] += k * pi2
              s2[5] += l * pi2

              if s2[3] >= pi2:
                continue
              if s2[3] <= -pi2:
                continue
              if s2[4] >= pi2:
                continue
              if s2[4] <= -pi2:
                continue
              if s2[5] >= pi2:
                continue
              if s2[5] <= -pi2:
                continue
              solution_list.append(s2)

    if not solution_list:
      return None
    if not ik_hints:
      debug.debug("IKHints are empty, not safe to search for IK solution")
      return None

    # find solution the is closest to an IK hint
    scored_results = []
    for s in solution_list:
      # check distance to every hint, and store the distance
      for h in ik_hints.values():
        dist = transform_util.angular_distance(np.array(h), s)
        scored_results.append((dist, s))

    if not scored_results:
      return None

    scored_results.sort(key=lambda x: x[0])
    return scored_results[0][1]

  def unity_ik_solve_search(
      self, target_pose: List[float], current_joints: List[float],
      ik_hints: Dict[int, List[float]]) -> Optional[np.ndarray]:
    """Returns the best joint angles for the given pose, or None.

    Algorithm is ported from Reach UI.

    Args:
      target_pose: the target pose to move to.
      current_joints: the current joint state.
      ik_hints: the ik_hints object
    """
    if not self._libik:
      return None

    if not ik_hints:
      ik_hints = {0: current_joints}

    # # Determine best IK hint by smallest end-effector distance
    closest_hint = ik_hints[0]
    closest_distance = None

    for hint in ik_hints.values():
      hint_pose = self.fk(hint)
      if hint_pose is not None:
        dist = np.linalg.norm(hint_pose[:3] - target_pose[:3])
        if closest_distance is None or dist < closest_distance:
          closest_distance = dist
          closest_hint = hint

    res = self.ik(target_pose)
    if res is None:
      logging.info("UNITY IK SOLVER: No IK solution found")
      return None

    minimal_solution_dist = None
    best_solution = None
    for solution in res:
      diff = 0.0
      for i in range(len(solution)):
        new_solution_angle, diff_angle = transform_util.ik_diff_angle(
            closest_hint[i], solution[i])
        solution[i] = new_solution_angle
        diff += diff_angle
      # Here we would ignore this solution if it exceeds joint angle limits
      # based on constraint information.

      if minimal_solution_dist is None or diff < minimal_solution_dist:
        minimal_solution_dist = diff
        best_solution = solution

    if best_solution is None:
      logging.info("UNITY IK SOLVER: No IK solution was allowed")
    return best_solution
