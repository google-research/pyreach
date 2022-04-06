"""Tests the quality of Forward Kinematics (FK) vs pose provided by the robot.

Works as follows:
1. Connects to robot and loads data.
2. Gets the state of the robot.
3. Compares FK of the joint angles of the robot state with the pose in the state
4. Compares FK again, with the tip adjust computed by PyReach and in FK.
"""

import math
import time
from typing import List

from absl import app  # type: ignore
from absl import flags  # type: ignore
import numpy as np
from pyreach.common.base import transform_util
from pyreach.factory import ConnectionFactory


def main(unused_argv: List[str]) -> None:
  with ConnectionFactory(
      connection_string=flags.FLAGS.connection_string,
      enable_streaming=False).connect() as host:
    while host.config.calibration is None or host.config.constraint is None:
      if host.is_closed():
        return
      time.sleep(0.001)
    arm = host.arm
    assert arm
    print("URDF file:", arm.arm_type.urdf_file)
    state = arm.fetch_state()
    if not state:
      print("State not loaded")
      return
    goal = arm.fk(state.joint_angles, False)
    print("State Flange pose:", state.pose.as_list())
    if goal:
      print("   FK Flange pose:", goal.as_list())
      delta = [(x - y) for x, y in zip(state.pose.as_list(), goal.as_list())]
      print("             Diff:", delta)
      print("       Pose Delta:", math.sqrt(sum([x * x for x in delta[0:3]])))
      print(
          "         Multiply:",
          transform_util.multiply_pose(
              np.array(goal.as_list()),
              transform_util.inverse_pose(np.array(
                  state.pose.as_list()))).tolist())
    else:
      print("FK failed")
    tip_adjust_t_base = state.tip_adjust_t_base
    if tip_adjust_t_base:
      goal = arm.fk(state.joint_angles, True)
      print("State Tool pose:", tip_adjust_t_base.as_list())
      if goal:
        print("   FK Tool pose:", goal.as_list())
        delta = [
            (x - y) for x, y in zip(tip_adjust_t_base.as_list(), goal.as_list())
        ]
        print("           Diff:", delta)
        print("     Pose Delta:", math.sqrt(sum([x * x for x in delta[0:3]])))
        print(
            "       Multiply:",
            transform_util.multiply_pose(
                np.array(goal.as_list()),
                transform_util.inverse_pose(
                    np.array(tip_adjust_t_base.as_list()))).tolist())
      else:
        print("FK failed")


if __name__ == "__main__":
  flags.DEFINE_string(
      "connection_string", "", "Connect using a PyReach connection string (see "
      "connection_string.md for examples and documentation).")
  app.run(main)
