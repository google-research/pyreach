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

"""A basic example of using the PyReach API.

This example demonstrates how to connect to a Reach host, how to retrieve
robot state and camera image, how to move the arm, etc.

Before running this example, please make sure reach connect is running and
listening on localhost:50008.
"""
from pyreach.factory import LocalTCPHostFactory


def main() -> None:
  with LocalTCPHostFactory().connect() as host:
    # By default, streaming is enabled for arm and cameras. This behavior can be
    # disabled by passing enable_streaming=False to LocalTCPHostFactory.
    assert host.arm is not None
    assert host.color_camera is not None
    assert host.depth_camera is not None
    assert host.vacuum is not None

    # Get the joint limits of an arm.
    print("Arm joint limit is ", host.arm.joint_limits)

    # Retrieve the latest cached arm state. Should return instantly.
    state = host.arm.state()
    if state is None:
      raise Exception("Failed to get arm state")

    # Arm state object contains information such as tool pose and joint angles.
    pose = state.pose
    print("Arm pose is ", pose)
    joint_angles = state.joint_angles
    print("Arm joint angles is ", joint_angles)

    # Blocking arm movement, to target joint angles or pose.
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

    # Constraints define limits in the Cartesian and robot configuration space.
    global_constraint = host.config.constraint
    if global_constraint is not None:
      print("Constraint:", global_constraint)
      global_constraint.is_point_in_object([1, 1, 2], "LeftBin")

    # Turning the vacuum on/off.
    print("Vac on:", host.vacuum.on())
    print("Vac off:", host.vacuum.off())

if __name__ == "__main__":
  main()
