"""Tests the quality of Forward Kinematics (FK) vs pose provided by the robot.

Works as follows:
1. Connects to robot and loads data.
2. Gets the state of the robot.
3. Compares FK of the joint angles of the robot state with the pose in the state
4. Compares FK again, with the tip adjust computed by PyReach and in FK.
"""

import logging
import math
from typing import List

from absl import app  # type: ignore
from absl import flags  # type: ignore
import numpy as np

from pyreach.calibration import CalibrationObject
from pyreach.calibration import CalibrationRobot
from pyreach.common.base import transform_util
from pyreach.factory import ConnectionFactory


def main(unused_argv: List[str]) -> None:
  success = True

  def test_delta(delta: List[float]) -> None:
    nonlocal success
    for x in delta:
      if x < -1e-5 or x > 1e-5:
        logging.info("-- delta too large: %f", x)
        success = False
        return

  logging.info("-" * 80)
  with ConnectionFactory(
      connection_string=flags.FLAGS.connection_string,
      enable_streaming=False).connect() as host:
    calibration = host.config.wait_calibration()
    assert calibration
    arm = host.arm
    assert arm

    state = arm.fetch_state()
    if not state:
      logging.info("State not loaded")
      return

    fk_pose = arm.fk(state.joint_angles, False, False)
    if not fk_pose:
      logging.info("fk failed")
      return

    logging.info("-" * 80)
    logging.info("URDF file: %s", arm.arm_type.urdf_file)
    logging.info("-" * 80)
    robot_dev = calibration.get_device("robot", arm.device_name)
    if robot_dev is None:
      logging.info("Robot is not found in the calibration")
    elif not isinstance(robot_dev, CalibrationRobot):
      logging.info("Robot in calibration is not actually robot device")
    elif robot_dev.tool_mount:
      logging.info(
          "Cannot cannot find base to origin pose, tool_mount is non-empty")
    elif robot_dev.link_name:
      logging.info(
          "Cannot cannot find base to origin pose, link_name is non-empty")
    elif not robot_dev.extrinsics:
      logging.info(
          "Cannot cannot find base to origin pose, robot extrinsics are empty")
    else:
      logging.info("Calibration base to origin pose: %s",
                   str(list(robot_dev.extrinsics)))
      logging.info(
          "  Arm state base to origin pose: %s",
          str(state.base_t_origin.as_list() if state.base_t_origin else None))
    logging.info("-" * 80)
    key = "robot"
    if arm.device_name:
      key += "-" + arm.device_name
    tip_dev = calibration.get_device("object", "tip0." + key)
    tip_adjust = np.array([0.0] * 6)
    if tip_dev and isinstance(tip_dev,
                              CalibrationObject) and tip_dev.extrinsics and len(
                                  tip_dev.extrinsics) == 6:
      logging.info("        Tip dev pose: %s", str(list(tip_dev.extrinsics)))
      tip_adjust = np.array(tip_dev.extrinsics, dtype=np.float64)
      tip_adjust_dev = calibration.get_device("object",
                                              "tip0." + key + ".adjust")
      if tip_adjust_dev and isinstance(
          tip_adjust_dev,
          CalibrationObject) and tip_adjust_dev.extrinsics and len(
              tip_adjust_dev.extrinsics) == 6:
        logging.info(" Tip adjust dev pose: %s",
                     str(list(tip_adjust_dev.extrinsics)))
        tip_adjust = transform_util.multiply_pose(
            tip_adjust, np.array(tip_adjust_dev.extrinsics, dtype=np.float64))

      logging.info("Computed adjust pose: %s", str(tip_adjust.tolist()))
    if state.tip_adjust_t_flange:
      logging.info("          State pose: %s",
                   str(state.tip_adjust_t_flange.as_list()))
      delta = [(x - y) for x, y in zip(state.tip_adjust_t_flange.as_list(),
                                       tip_adjust.tolist())]
      logging.info("                Diff: %s", str(delta))
      logging.info("          Pose Delta: %s",
                   str(math.sqrt(sum([x * x for x in delta[0:3]]))))
      test_delta(delta)
    else:
      logging.info("tip adjust not in state")

    logging.info("-" * 80)
    logging.info("State Flange pose: %s", str(state.pose.as_list()))
    logging.info("   FK Flange pose: %s", str(fk_pose.as_list()))
    delta = [(x - y) for x, y in zip(state.pose.as_list(), fk_pose.as_list())]
    logging.info("             Diff: %s", str(delta))
    logging.info("       Pose Delta: %s",
                 str(math.sqrt(sum([x * x for x in delta[0:3]]))))
    test_delta(delta)
    logging.info(
        "         Multiply: %s",
        str(
            transform_util.multiply_pose(
                np.array(fk_pose.as_list()),
                transform_util.inverse_pose(np.array(
                    state.pose.as_list()))).tolist()))
    if state.flange_t_base:
      for x, y in zip(state.pose.as_list(), state.flange_t_base.as_list()):
        if x != y:
          logging.info("Warning, state pose != flange_t_base:")
          logging.info("  %s", str(state.pose.as_list()))
          logging.info("  %s", str(state.flange_t_base.as_list()))
          success = False
          break

    if state.flange_t_origin:
      logging.info("-" * 80)
      fk_pose_origin = arm.fk(state.joint_angles, False, True)
      if not fk_pose_origin:
        logging.info("fk failed")
        return
      logging.info("State Flange Origin pose: %s",
                   str(state.flange_t_origin.as_list()))
      logging.info("   FK Flange Origin pose: %s",
                   str(fk_pose_origin.as_list()))
      delta = [(x - y) for x, y in zip(state.flange_t_origin.as_list(),
                                       fk_pose_origin.as_list())]
      logging.info("             Diff: %s", str(delta))
      logging.info("       Pose Delta: %s",
                   str(math.sqrt(sum([x * x for x in delta[0:3]]))))
      test_delta(delta)
      logging.info(
          "         Multiply: %s",
          str(
              transform_util.multiply_pose(
                  np.array(fk_pose.as_list()),
                  transform_util.inverse_pose(np.array(
                      state.pose.as_list()))).tolist()))

    logging.info("-" * 80)
    tip_adjust_t_base = state.tip_adjust_t_base
    if tip_adjust_t_base:
      logging.info("State Tip Adjust pose: %s",
                   str(tip_adjust_t_base.as_list()))
      fk_tip_adjust_pose = arm.fk(state.joint_angles, True, False)
      if fk_tip_adjust_pose:
        logging.info("   FK Tip Adjust pose: %s",
                     str(fk_tip_adjust_pose.as_list()))
        delta = [(x - y) for x, y in zip(tip_adjust_t_base.as_list(),
                                         fk_tip_adjust_pose.as_list())]
        logging.info("                 Diff: %s", str(delta))
        logging.info("           Pose Delta: %s",
                     str(math.sqrt(sum([x * x for x in delta[0:3]]))))
        logging.info(
            "             Multiply: %s",
            str(
                transform_util.multiply_pose(
                    np.array(fk_tip_adjust_pose.as_list()),
                    transform_util.inverse_pose(
                        np.array(tip_adjust_t_base.as_list()))).tolist()))
        test_delta(delta)

        delta = [(x - y) for x, y in zip(tip_adjust_t_base.as_list(),
                                         fk_tip_adjust_pose.as_list())]
        logging.info("       Recompute Diff: %s", str(delta))
        test_delta(delta)
      else:
        logging.info("FK failed")

    logging.info("-" * 80)
    tip_adjust_t_origin = state.tip_adjust_t_origin
    if tip_adjust_t_origin:
      logging.info("State Tip Adjust Origin pose: %s",
                   str(tip_adjust_t_origin.as_list()))
      fk_tip_adjust_pose = arm.fk(state.joint_angles, True, True)
      if fk_tip_adjust_pose:
        logging.info("   FK Tip Adjust Origin pose: %s",
                     str(fk_tip_adjust_pose.as_list()))
        delta = [(x - y) for x, y in zip(tip_adjust_t_origin.as_list(),
                                         fk_tip_adjust_pose.as_list())]
        logging.info("                        Diff: %s", str(delta))
        logging.info("                  Pose Delta: %s",
                     str(math.sqrt(sum([x * x for x in delta[0:3]]))))
        logging.info(
            "                    Multiply: %s",
            str(
                transform_util.multiply_pose(
                    np.array(fk_tip_adjust_pose.as_list()),
                    transform_util.inverse_pose(
                        np.array(tip_adjust_t_origin.as_list()))).tolist()))
        test_delta(delta)

        delta = [(x - y) for x, y in zip(tip_adjust_t_origin.as_list(),
                                         fk_tip_adjust_pose.as_list())]
        logging.info("              Recompute Diff: %s", str(delta))
        test_delta(delta)
      else:
        logging.info("FK failed")

    if not success:
      raise ValueError("Delta too large")


if __name__ == "__main__":
  flags.DEFINE_string(
      "connection_string", "", "Connect using a PyReach connection string (see "
      "connection_string.md for examples and documentation).")
  app.run(main)
