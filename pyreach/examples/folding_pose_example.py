"""Tests the arm pose by running a set of poses on a folding robot."""

import math
import time
from typing import Tuple, List

from absl import app  # type: ignore
from absl import flags  # type: ignore
from pyreach.core import Pose
from pyreach.factory import ConnectionFactory


def main(unused_argv: List[str]) -> None:
  with ConnectionFactory(
      connection_string=flags.FLAGS.connection_string,
      enable_streaming=False).connect() as host:
    arm = host.arm
    assert arm
    arm.start_streaming(10)
    while (host.config.calibration is None or host.config.constraint is None or
           arm.state() is None):
      if host.is_closed():
        return
      time.sleep(0.001)
    tip_adjust = flags.FLAGS.tip_adjust
    poses: Tuple[Pose, ...]
    if tip_adjust:
      poses = (
          Pose.from_list(
              [-0.10248441, -0.7, -0.05, 0.15279271, -3.09590045, -0.02854629]),
          Pose.from_list([
              -0.15083604, -0.69993669, -0.05, 0.15279271, -3.09590045,
              -0.02854629
          ]),
          Pose.from_list([
              -0.1984006, -0.6999271, -0.05, 0.15279271, -3.09590045,
              -0.02854629
          ]),
      )
    else:
      raise NotImplementedError("No unadjusted poses provided")
    for pose in list(poses) * 2:
      print("---------------")
      print("    Move to:", pose)
      cmd_state = arm.to_pose(pose, apply_tip_adjust_transform=tip_adjust)
      assert cmd_state and not cmd_state.is_error(
      ), "output cmd-status is %s" % (str(cmd_state),)
      print("     Output:", cmd_state)
      state = arm.fetch_state()
      assert state
      output = state.tip_adjust_t_base if tip_adjust else state.pose
      print("     Joints:", state.joint_angles)
      print("Output pose:", output)
      assert output is not None
      delta = [(x - y) for x, y in zip(output.as_list(), pose.as_list())]
      print("       Diff:", delta)
      print(" Pose Delta:", math.sqrt(sum([x * x for x in delta[0:3]])))
      print("      Delta:", math.sqrt(sum([x * x for x in delta])))


if __name__ == "__main__":
  flags.DEFINE_string(
      "connection_string", "", "Connect using a PyReach connection string (see "
      "connection_string.md for examples and documentation).")
  flags.DEFINE_bool("tip_adjust", True, "Test with tip adjust")
  app.run(main)
