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

"""Utilities for PyBullet IK."""

import os
import sys
from typing import Any
from absl import logging  # type: ignore
import numpy as np  # type: ignore
import six

from pyreach.common.base import transform_util
import pybullet  # type: ignore
import pybullet_data  # type: ignore
import pybullet_utils.bullet_client as bullet_client  # type: ignore

XARM_URDF_PATH = ('third_party/bullet/examples/pybullet/gym/pybullet_data/'
                  'xarm/xarm6_robot.urdf')


def _load_g3_resources(load_fn: Any, file_path: str, *args: Any,
                       **kwargs: Any) -> Any:
  """Wraps the PyBullet loadURDF to support g3 resource loading.

  May need to write to local file system. So make sure tmpfs is enabled on
  Borg.

  Args:
    load_fn: A function to load the file.
    file_path: the file to be loaded.
    *args: Other arguments. Check PyBullet documentation for details.
    **kwargs: Other keyward arguments. Check PyBullet documentation for details.

  Returns:
    The unique URDF id if successful.
  """
  g3_file_path = file_path

  if not six.ensure_str(g3_file_path).startswith('google3/'):
    g3_file_path = os.path.join('google3', g3_file_path)

  file_dir_name = os.path.dirname(g3_file_path)

  # Using `skip_previous_extraction_check` since we are using the
  # `filename_predicate`.
  # flake8: noqa
  root_dir = resources.GetARootDirWithAllResources(  # type: ignore
      filename_predicate=lambda x: file_dir_name in x,
      skip_previous_extraction_check=True)

  g3_file_path = os.path.join(root_dir, g3_file_path)

  return load_fn(g3_file_path, *args, **kwargs)


def load_urdf(pybullet_client: Any, file_path: str, *args: Any,
              **kwargs: Any) -> Any:
  """Loads the given URDF filepath in g3 and borg."""
  if file_path.startswith('google3/'):
    file_path = file_path[len('google3/'):]

  # Handles most general file open case (blaze build and execute in code tree,
  # or running unit tests) and CNS case if enable_cns() is called.
  try:
    if os.path.exists(file_path):
      return pybullet_client.loadURDF(file_path, *args, **kwargs)
  except pybullet_client.error:
    pass

  # Handles the PAR case and blaze run case. Unlikely if path is absolute.
  if not file_path.startswith('/'):
    try:
      if os.path.exists(file_path):
        return pybullet_client.loadURDF(
            os.path.join('google3', file_path), *args, **kwargs)
    except pybullet.error:
      pass

  if 'google3.pyglib.resources' in sys.modules:
    try:
      # Big Hammer.
      return _load_g3_resources(pybullet_client.loadURDF, file_path, *args,
                                **kwargs)
    except pybullet.error:
      raise FileNotFoundError('Cannot load the URDF file {}'.format(file_path))

  else:
    try:
      if file_path.startswith(
          'third_party/bullet/examples/pybullet/gym/pybullet_data/'):
        pybullet_client.setAdditionalSearchPath(pybullet_data.getDataPath())
        file_path = file_path[55:]
      elif file_path.startswith('robotics/'):
        pybullet_client.setAdditionalSearchPath(os.environ['PYTHONPATH'])
        file_path = file_path[9:]

      logging.info('Loading URDF %s', file_path)
      return pybullet_client.loadURDF(file_path, *args, **kwargs)
    except pybullet.error:
      raise FileNotFoundError('Cannot load the URDF file {}'.format(file_path))


class IKPybullet:
  """PyBullet IK."""

  def __init__(self) -> None:
    self._connection_mode = pybullet.DIRECT
    self._pybullet_client = bullet_client.BulletClient(self._connection_mode)
    self._effector_link = 6
    self._arm_urdf = load_urdf(self._pybullet_client, XARM_URDF_PATH, [0, 0, 0])

    joints = []
    joint_indices = []
    for i in range(self._pybullet_client.getNumJoints(self._arm_urdf)):
      joint_info = self._pybullet_client.getJointInfo(self._arm_urdf, i)
      if joint_info[2] == pybullet.JOINT_REVOLUTE:
        joints.append(joint_info[0])
        joint_indices.append(i)
    self._n_joints = len(joints)
    self._joints = tuple(joints)
    self._joint_indices = tuple(joint_indices)

  def _set_joints(self, joints_values: np.ndarray) -> None:
    for i in range(self._n_joints):
      self._pybullet_client.resetJointState(self._arm_urdf, self._joints[i],
                                            joints_values[i])

  def _get_joints(self) -> np.ndarray:
    joint_states = self._pybullet_client.getJointStates(self._arm_urdf,
                                                        self._joint_indices)
    joint_positions = np.array([state[0] for state in joint_states])
    return joint_positions

  def ik_search(self, target_effector_pose: np.ndarray,
                current_joints: np.ndarray) -> np.ndarray:
    """Inverse kinematics.

    Args:
      target_effector_pose: Target pose for the robot's end effector.
      current_joints: The current joints of the robot.

    Returns:
      Numpy array with required joint angles to reach the requested pose.
    """
    self._set_joints(current_joints)

    translation = target_effector_pose[0:3]
    quaternion_xyzw = transform_util.axis_angle_to_quaternion(
        target_effector_pose[3:])

    target_joints = np.array(
        self._pybullet_client.calculateInverseKinematics(
            self._arm_urdf,
            self._effector_link,
            translation,
            quaternion_xyzw,
            # TODO: use real limits
            lowerLimits=[-17] * 6,
            upperLimits=[17] * 6,
            jointRanges=[17] * 6,
            # TODO: Understand why examples don't use actual positions for
            # the first two joints. Taken from
            # `pybullet/gym/pybullet_robots/xarm/xarm_sim.py`
            restPoses=[0, 0] + self._get_joints()[2:].tolist(),
            maxNumIterations=500,
            residualThreshold=1e-4))

    self._set_joints(target_joints)
    return target_joints

  def fk(self, current_joints: np.ndarray) -> np.ndarray:
    """Forward kinematics.

    Args:
      current_joints: The current joints of the robot.

    Returns:
      Numpy array with the t pose.
    """
    self._set_joints(current_joints)

    ee_link_state = self._pybullet_client.getLinkState(
        self._arm_urdf, self._effector_link, 0, computeForwardKinematics=True)
    ee_link_pose = np.array(ee_link_state[4] + ee_link_state[5])
    quaternion_xyzw = np.asarray(
        [ee_link_pose[3], ee_link_pose[4], ee_link_pose[5], ee_link_pose[6]])
    pose = transform_util.pos_quaternion_to_pose(ee_link_pose[0:3],
                                                 quaternion_xyzw)
    return pose
