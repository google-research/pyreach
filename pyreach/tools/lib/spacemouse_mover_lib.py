"""Moves a robot around with a spacemouse."""

import copy
import multiprocessing as mp
from multiprocessing import connection as mpc
import os
import sys
import time
from typing import cast, Optional

from absl import logging  # type: ignore

from pyreach.common.spacemouse import spacemouse_2d_driver
from pyreach.core import Pose
from pyreach.host import Host

# Restricts to 2D plane at PUSHY_HEIGHT_METERS
ONLY_2D = True

# The center x,y coordinates that the agent goes to at the beginning of a task,
# so that jiggling around won't hit joint limits.
CENTER_X_METERS = 0.39
CENTER_Y_METERS = 0

# How long to wait between actions.
ACTION_TIME_INCREMENT_SECONDS = 0.01

# The orientation for the tool to point straight down.
TOOL_ORIENTATION_RADS = (0, -3.14, 0)

# The rough limits for the workspace. This is based on the end effector tip.
# It's a bit sloppy, because there may be some areas which can't be reached,
# especially close to the robot base and close to the far corners.
BOARD_X_LIMITS_METERS = (0.200, 0.610)  # near, far w.r.t. base
BOARD_Y_LIMITS_METERS = (-0.330, 0.335)  # right, left w.r.t. base
BOARD_Z_LIMITS_METERS = (0.1, 0.5)

# Safe z-height. This is above the blocks, so movement at this height will
# not impact against any blocks.
SAFE_Z_METERS = 0.262

# z-height where the end-effector can push the blocks around.
PUSHY_HEIGHT_METERS = 0.184

# Maximum allowed linear distance (meters) between (i) desired cartesian pose,
# and (ii) measured cartesian pose.
SAFE_SERVO_DIST_METERS = 0.071

# Resting corner x,y coordinates (upper right with respect to a camera
# facing the base from the far side of the board, or near left with respect to
# the base) where the arm goes after a test case.
CORNER_X_METERS = 0.342
CORNER_Y_METERS = -0.242


class KeyboardDriver:
  """Keyboard input pipe thing."""

  def __init__(self, pipe: mpc.Connection):
    self._pipe = pipe
    sys.stdin = os.fdopen(0)

  def run(self) -> None:
    logging.info("Started keyboard driver")
    while True:
      command = input()
      self._pipe.send(command)


class SpacemouseMover:
  """Moves the arm according to the spacemouse."""

  previous_commanded_pose: Optional[Pose] = None

  def __init__(self, host: Host, task_code: str):
    assert host.arm is not None

    self.host = host
    self.task_code = task_code

    self.previous_commanded_pose = None
    parent_conn, child_conn = mp.Pipe()
    self._spacemouse_pipe = parent_conn
    self.spacemouse_proc = mp.Process(
        target=self._start_spacemouse_driver, args=(child_conn,), daemon=False)
    self.spacemouse_proc.start()

    parent_conn, child_conn = mp.Pipe()
    self._keyboard_pipe = parent_conn
    self.keyboard_proc = mp.Process(
        target=self._start_keyboard_driver, args=(child_conn,), daemon=False)
    self.keyboard_proc.start()

    self._in_task = False

  def _get_spacemouse_command(self, pose: Pose) -> Pose:
    """Gets the spacemouse command, if any, as a desired Pose."""
    cmd = self._spacemouse_pipe.recv()
    cmd = cast(spacemouse_2d_driver.CartesianDeltaPositionAction, cmd)

    logging.info("Current pose: %s", str(pose.as_list()))

    if self.previous_commanded_pose is None:
      self.previous_commanded_pose = copy.deepcopy(pose)

    new_commanded_pose = copy.deepcopy(self.previous_commanded_pose.as_list())
    new_commanded_pose[0] += cmd.delta_x
    new_commanded_pose[1] += cmd.delta_y
    if not ONLY_2D:
      new_commanded_pose[2] += cmd.delta_z
      new_commanded_pose[3] += cmd.delta_roll  # rx
      new_commanded_pose[4] += cmd.delta_pitch  # ry
      new_commanded_pose[5] += cmd.delta_yaw  # rz
    else:
      new_commanded_pose[2] = PUSHY_HEIGHT_METERS
      new_commanded_pose[3:] = TOOL_ORIENTATION_RADS
    logging.info("Desired pose: %s", str(new_commanded_pose))

    self.previous_commanded_pose = Pose.from_list(new_commanded_pose)
    return self.previous_commanded_pose

  def loop(self) -> bool:
    """Runs one iteration of the loop."""
    done: bool = False
    start_time: float = time.time()

    found = True
    send_cmd = False
    while found:
      found = False
      if self._keyboard_pipe.poll():
        cmd = self._keyboard_pipe.recv()
        cmd = cast(str, cmd).strip()
        logging.info("Received keyboard command: %s", cmd)
        if cmd == "x":
          self.reset(final_reset=True)
          return True
        else:
          done = done or self.handle_keyboard_command(cmd)
        found = True

      if self._spacemouse_pipe.poll():
        logging.info("Got into spacemouse readable.")
        arm = self.host.arm
        assert arm is not None
        current_state = arm.state()
        assert current_state is not None
        new_pose = self._get_spacemouse_command(current_state.pose)
        arm.async_to_pose(new_pose, servo=True, preemptive=False)
        found = True
        send_cmd = True

    if not send_cmd and self.previous_commanded_pose:
      arm = self.host.arm
      assert arm is not None
      arm.async_to_pose(
          self.previous_commanded_pose, servo=True, preemptive=False)

    if done:
      logging.info("Done set, exiting loop.")
      self._clear_spacemouse_queue()
      return True

    end_time: float = time.time()
    loop_time: float = end_time - start_time
    slack_time: float = ACTION_TIME_INCREMENT_SECONDS - loop_time

    if slack_time > 0:
      # Send actions at 1/ACTION_TIME_INCREMENT_SECONDS Hz
      time.sleep(slack_time)

    return done

  def reset(self, final_reset: bool = False) -> None:
    """Move the arm up and out of the way."""
    if self._in_task:
      self.host.logger.end_task({"task-code": "9999"})
      self._in_task = False

    # Get the current pose, set the z-height to the safe z-height, and
    # synchronously move.
    arm = self.host.arm
    assert arm is not None
    arm.start_streaming()
    current_state = arm.state()
    assert current_state is not None
    current_pose = current_state.pose.as_list()
    current_pose[2] = SAFE_Z_METERS
    current_pose[3:] = TOOL_ORIENTATION_RADS
    logging.info("Move arm to %s", str(current_pose))
    status = arm.to_pose(
        Pose.from_list(current_pose),
        preemptive=True,
        use_linear=True,
        velocity=0.7,
        acceleration=0.3)
    logging.info("Moved arm up: %s", status)

    current_state = arm.fetch_state()
    assert current_state is not None
    logging.info("Arm now at %s", str(current_state.pose.as_list()))

    # Move the arm to one corner.
    current_pose[0] = CORNER_X_METERS
    current_pose[1] = CORNER_Y_METERS
    current_pose[2] = SAFE_Z_METERS
    current_pose[3:] = TOOL_ORIENTATION_RADS
    logging.info("Move arm to %s", str(current_pose))
    status = arm.to_pose(
        Pose.from_list(current_pose),
        use_linear=True,
        velocity=0.7,
        acceleration=0.3)
    logging.info("Moved arm out of the way: %s", status)

    current_state = arm.fetch_state()
    assert current_state is not None

    if not final_reset:
      logging.info("Arm now at %s", str(current_state.pose.as_list()))

      current_pose[0] = CORNER_X_METERS
      current_pose[1] = CORNER_Y_METERS
      current_pose[2] = PUSHY_HEIGHT_METERS
      current_pose[3:] = TOOL_ORIENTATION_RADS
      logging.info("Move arm to %s", str(current_pose))
      status = arm.to_pose(
          Pose.from_list(current_pose),
          use_linear=True,
          velocity=0.7,
          acceleration=0.3)
      logging.info("Moved arm to pushy height: %s", status)

    current_state = arm.fetch_state()
    assert current_state is not None
    logging.info("Arm now at %s", str(current_state.pose.as_list()))
    logging.info("Reset complete!")

    if not final_reset:
      self._in_task = True
      self.host.logger.start_task({"task-code": "9999"})

  def handle_keyboard_command(self, cmd: str) -> bool:
    """Handles keyboard commands other than 'x'.

    Args:
      cmd: The keyboard command

    Returns:
      True to exit, False to continue.
    """
    del cmd
    return False

  def run(self) -> None:
    """Runs the loop and exits gracefully."""

    self.reset()
    self._clear_spacemouse_queue()

    done: bool = False
    while not done:
      done = self.loop()

    # Stop the spacemouse driver
    self._spacemouse_pipe.send(True)
    self._clear_spacemouse_queue()
    self.spacemouse_proc.join(timeout=1)
    if self.spacemouse_proc.is_alive():
      logging.info("========== spacemouse didn't quit")
      self.spacemouse_proc.terminate()
      self.spacemouse_proc.join(timeout=1)
    if self.spacemouse_proc.is_alive():
      logging.info("========== spacemouse still didn't quit")
      self.spacemouse_proc.kill()
      self.spacemouse_proc.join(timeout=1)
    self.spacemouse_proc.close()

    self.keyboard_proc.kill()
    self.keyboard_proc.join(timeout=1)
    self.keyboard_proc.close()

  def _clear_spacemouse_queue(self) -> None:
    """Clears the spacemouse command pipe."""
    self.previous_commanded_pose = None
    while self._spacemouse_pipe.poll(timeout=0.001):
      self._spacemouse_pipe.recv()

  def _start_spacemouse_driver(self, conn: mpc.Connection) -> None:
    driver = spacemouse_2d_driver.SpacemouseDriver(
        pipe=conn, spacemouse_id=None, two_dof_mode=ONLY_2D, dt=0.01)
    logging.info("Started spacemouse driver")
    driver.run()

  def _start_keyboard_driver(self, conn: mpc.Connection) -> None:
    driver = KeyboardDriver(pipe=conn)
    driver.run()
