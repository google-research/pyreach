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
  success = True

  def test_delta(delta: List[float]) -> None:
    nonlocal success
    for x in delta:
      if x < -1e-5 or x > 1e-5:
        print("-- delta too large:", x)
        success = False
        return

  print("-" * 80)
  with ConnectionFactory(
      connection_string=flags.FLAGS.connection_string,
      enable_streaming=False).connect() as host:
    calibration = None
    while calibration is None:
      calibration = host.config.calibration
      if host.is_closed():
        return
      if not calibration:
        time.sleep(0.001)
    arm = host.arm
    assert arm

    state = arm.fetch_state()
    if not state:
      print("State not loaded")
      return

    fk_pose = arm.fk(state.joint_angles, False)
    if not fk_pose:
      print("fk failed")
      return

    print("-" * 80)
    print("URDF file:", arm.arm_type.urdf_file)
    print("-" * 80)
    key = "robot"
    if arm.device_name:
      key += "-" + arm.device_name
    tip_dev = calibration.get_device("object", "tip0." + key)
    tip_adjust = np.array([0.0] * 6)
    if tip_dev and tip_dev.extrinsics and len(tip_dev.extrinsics) == 6:
      print("Tip dev pose:        ", tip_dev.extrinsics)
      tip_adjust = np.array(tip_dev.extrinsics, dtype=np.float64)
      tip_adjust_dev = calibration.get_device("object",
                                              "tip0." + key + ".adjust")
      if tip_adjust_dev and tip_adjust_dev.extrinsics and len(
          tip_adjust_dev.extrinsics) == 6:
        print("Tip adjust dev pose: ", tip_adjust_dev.extrinsics)
        tip_adjust = transform_util.multiply_pose(
            tip_adjust, np.array(tip_adjust_dev.extrinsics, dtype=np.float64))

      print("Computed adjust pose:", tip_adjust.tolist())
    if state.tip_adjust_t_flange:
      print("          State pose:", state.tip_adjust_t_flange.as_list())
      delta = [(x - y) for x, y in zip(state.tip_adjust_t_flange.as_list(),
                                       tip_adjust.tolist())]
      print("                Diff:", delta)
      print("          Pose Delta:",
            math.sqrt(sum([x * x for x in delta[0:3]])))
      test_delta(delta)
    else:
      print("tip adjust not in state")

    print("-" * 80)
    print("State Flange pose:", state.pose.as_list())
    print("   FK Flange pose:", fk_pose.as_list())
    delta = [(x - y) for x, y in zip(state.pose.as_list(), fk_pose.as_list())]
    print("             Diff:", delta)
    print("       Pose Delta:", math.sqrt(sum([x * x for x in delta[0:3]])))
    test_delta(delta)
    print(
        "         Multiply:",
        transform_util.multiply_pose(
            np.array(fk_pose.as_list()),
            transform_util.inverse_pose(np.array(
                state.pose.as_list()))).tolist())
    if state.flange_t_base:
      for x, y in zip(state.pose.as_list(), state.flange_t_base.as_list()):
        if x != y:
          print("Warning, state pose != flange_t_base:")
          print("  ", state.pose.as_list())
          print("  ", state.flange_t_base.as_list())
          success = False
          break

    print("-" * 80)
    tip_adjust_t_base = state.tip_adjust_t_base
    if tip_adjust_t_base:
      print("State Tool pose:", tip_adjust_t_base.as_list())
      fk_tip_adjust_pose = arm.fk(state.joint_angles, True)
      if fk_tip_adjust_pose:
        print("   FK Tool pose:", fk_tip_adjust_pose.as_list())
        delta = [(x - y) for x, y in zip(tip_adjust_t_base.as_list(),
                                         fk_tip_adjust_pose.as_list())]
        print("           Diff:", delta)
        print("     Pose Delta:", math.sqrt(sum([x * x for x in delta[0:3]])))
        print(
            "       Multiply:",
            transform_util.multiply_pose(
                np.array(fk_tip_adjust_pose.as_list()),
                transform_util.inverse_pose(
                    np.array(tip_adjust_t_base.as_list()))).tolist())
        test_delta(delta)

        delta = [(x - y) for x, y in zip(tip_adjust_t_base.as_list(),
                                         fk_tip_adjust_pose.as_list())]
        print(" Recompute Diff:", delta)
        test_delta(delta)
      else:
        print("FK failed")

    if not success:
      raise ValueError("Delta too large")


if __name__ == "__main__":
  flags.DEFINE_string(
      "connection_string", "", "Connect using a PyReach connection string (see "
      "connection_string.md for examples and documentation).")
  app.run(main)
