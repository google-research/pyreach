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

"""Reach arm element used for configuration."""

import dataclasses
from typing import Optional, Tuple

from pyreach.gyms import reach_element


@dataclasses.dataclass(frozen=True)
class ReachArm(reach_element.ReachElement):
  """Base class for for Reach arm configuration.

  The arm may be moved either synchronously or asynchronously.
  In synchronous mode, the follow on observation is delayed until
  the arm stops moving.  In asynchronous mode, the follow on observation
  is performed immediately without waiting for the arm to stop moving.

  There are two ways to put the arm in synchronous mode:
  1. Set is_synchronous to True when the arm is initially configured.
  2. Set is_synchronous to False for initial configuration, but set the
     "synchronous" flag in the arm action space to 1 during a step() call.
     Whenever the "synchronous" flag is set, the arm will move synchronously.
  If the arm is not in synchronous mode, it is moved asynchronously.

  All reach elements that are configured in synchronous mode (arm, vacuum,
  text instructions, etc.) are moved as a group.  The step() call initiates
  all of these synchronous together and waits for them all to complete before
  returning the final observation.

  The other non synchronous reach elements are being continuously polled
  by the PyReach Gym.  Whenever at least one element is in synchronous mode
  (i.e. the arm), the PyReach Gym will also wait for the polled information
  to have timestamps after all of the synchronous operations completed.
  For the arm, this means is that the color camera(s) and depth camera(s)
  will contain images after arm has stopped moving.

  Atrributes:
    reach_name: The Reach name of the arm.
    low_joint_angles : The minimum values for the joint angles in radians. Use
      an empty list if no low limits are specified.
    high_joint_angles: The maximum values for the joint angles in radians. Use
      an empty list if no high limits are specified.
    apply_tip_adjust_transform: If True and a tip adjustment transform is
      available, apply the transform for each arm movement operation.
    is_synchronous: If True, the arm is always moved synchronously; otherwise
      it is typically moved asynchronously.  (For further details see above.)
    response_queue_length: When positive, the PyReach Gym returns the last N
      arm status values for asynchronous moves.
    ik_lib: Whether to use IKFast or IK PyBullet for inverse kinematics.
    controllers: A list of the controller names to allow for arm control.
      In the Gym, the controller is specified by a number that indexes into
      this list.  The empty string means "no controller".  This list must
      not empty.  By convention, the first entry is the empty string.
      If not specified, the list defaults to `("",)`
  """
  low_joint_angles: Tuple[float, ...] = ()
  high_joint_angles: Tuple[float, ...] = ()
  apply_tip_adjust_transform: bool = False
  is_synchronous: bool = False
  response_queue_length: int = 0
  ik_lib: Optional[str] = None
  controllers: Tuple[str] = ("",)
