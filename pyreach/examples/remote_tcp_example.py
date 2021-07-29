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

"""A basic example of using the PyReach API with automatic reach connect.

To run this example, please install reach connect, and set up a robot for
remote TCP access.
"""
from typing import List
from absl import app  # type: ignore
from absl import flags  # type: ignore
from pyreach.factory import RemoteTCPHostFactory


def main(argv: List[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")

  with RemoteTCPHostFactory(flags.FLAGS.robot_id, flags.FLAGS.connect_host,
                            flags.FLAGS.connect_port,
                            flags.FLAGS.working_directory).connect() as host:
    assert host.arm is not None
    assert host.color_camera is not None
    assert host.depth_camera is not None
    assert host.oracle is not None
    assert host.vacuum is not None

    # Get the joint limits of an arm.
    print("Arm joint limit is ", host.arm.joint_limits)

    # Retrieve the latest cached arm state. Should return instantly.
    state = host.arm.state()
    if state is None:
      raise Exception("Failed to get arm state")
    assert state is not None

    # Arm state object contains information such as tool pose and joint angles.
    pose = state.pose
    print("Get state pose:", pose)
    joint_angles = state.joint_angles
    print("Get state joint angles:", joint_angles)

    # Blocking arm movement, to targetArm joint angles or pose.
    status = host.arm.to_joints(joint_angles)
    print("Arm to joint angles:", status)
    status = host.arm.to_pose(pose)
    print("Arm to pose:", status)

    # Non-blocking arm movement.
    host.arm.async_to_joints(
        joint_angles, callback=lambda s: print("To joint angles:", s))

    # Getting the latest cached images for color and depth camera.
    # Should return instantly.
    # Image object carries information about the pose of the camera when the
    # image is taken. The pose is relative to the robot base frame.
    color = host.color_camera.image()
    if color is not None:
      print("Color:", color)
      print("Color image pose", color.pose())
    color_depth = host.depth_camera.image()
    if color_depth is not None:
      print("Color depth:", color_depth)
      print("Color depth pose", color_depth.pose())

    # Getting the current camera pose.
    print("Camera pose ", host.color_camera.pose)
    print("Depth camera pose ", host.depth_camera.pose)

    calibration = host.config.calibration
    if calibration is None:
      print("Failed to get calibration")
    elif color_depth is None:
      print("Failed to get color depth, cannot find pick point")
    else:
      print("Calibration: ", calibration)

    # Oracle is a special type of device which runs pick point ML model and
    # returns heatmap for the pick points.
    oracle_prediction = host.oracle.fetch_prediction(
        intent="pick",
        prediction_type="pick",
        request_type="sparse",
        task_code="97",
        label="SingulateLeftBin")
    oracle_prediction_points = (
        oracle_prediction.points if oracle_prediction is not None else None)
    print("Oracle prediction: ", oracle_prediction_points)
    if (oracle_prediction_points is not None and calibration is not None and
        color_depth is not None):
      for point in oracle_prediction_points:
        print("Calibration 3d pick point:",
              color_depth.get_point_normal(int(point.x), int(point.y)))

    # Actions are scripted robot movement. Actions can be created in Reach UI
    # and used by PyReach clients.
    print("Actionset:", host.config.actionset)

    # Constraints define limits in the Cartesion and robot configuration space.
    global_constraint = host.config.constraint
    if global_constraint is not None:
      print("Constraint:", global_constraint)
      global_constraint.is_point_in_object([1, 1, 2], "LeftBin")

    # Turning the vacuum on/off.
    print("Vac on:", host.vacuum.on())
    print("Vac off:", host.vacuum.off())


if __name__ == "__main__":
  flags.DEFINE_string("robot_id", None, "The robot id to connect to.")
  flags.DEFINE_string(
      "working_directory", None, "Working directory for reach tools. Defaults "
      "to ~/reach_workspace.")
  flags.mark_flag_as_required("robot_id")
  flags.DEFINE_string(
      "connect_host", "",
      "The host to connect to. Defaults to \"<robot_id>.local\"")
  flags.DEFINE_integer(
      "connect_port",
      default=50009,
      lower_bound=0,
      upper_bound=65535,
      help="The port number to connect to.")
  app.run(main)
