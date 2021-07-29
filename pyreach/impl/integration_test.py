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

import logging
import threading
import unittest

import pyreach
from pyreach.impl import test_client


class Integration(unittest.TestCase):

  def test_integration(self) -> None:
    with test_client.connect_test(
        host_args={"enable_streaming": False}) as host:
      assert host.color_camera is not None
      assert host.depth_camera is not None
      assert host.arm is not None
      assert host.oracle is not None
      assert host.vacuum is not None

      host.logger.start_task({})
      host.logger.end_task({})
      logging.info("Start annotation: %s",
                   host.logger.start_annotation_interval("test-annotation"))

      logging.info("Constraint: %s", host.config.constraint)
      logging.info("Calibration: %s", host.config.calibration)
      actionset = host.config.actionset
      logging.info("Actionset: %s",
                   actionset.action_names() if actionset is not None else None)
      logging.info("Text Instruction: %s",
                   host.text_instructions.text_instruction)

      state = host.arm.fetch_state()
      assert state is not None
      pose = state.pose
      logging.info("Get state pose: %s", pose)
      joint_angles = state.joint_angles
      logging.info("Get state joint angles: %s", joint_angles)

      state = host.arm.state()
      assert state is not None
      pose = state.pose
      logging.info("Cached state pose: %s", pose)
      joint_angles = state.joint_angles
      logging.info("Cached state joint angles: %s", joint_angles)

      final_status = host.arm.to_joints([0, 0, 0, 0, 0, 0])
      logging.info("Arm to joint angles: %s", final_status)
      final_status = host.arm.to_pose(
          pyreach.Pose(
              position=pyreach.Translation(10000.0, 10000.0, 10000.0),
              orientation=pose.orientation))
      logging.info("Arm to invalid pose: %s", final_status)
      final_status = host.arm.to_pose(pose)
      logging.info("Arm to pose: %s", final_status)
      host.arm.async_to_joints(
          [0, 0, 0, 0, 0, 0],
          callback=lambda statuses: logging.info("To joint angles: %s", statuses
                                                ),
          finished_callback=lambda: logging.info("To joint angles finished"))

      color = host.color_camera.fetch_image()
      logging.info("Color: %s", color)
      color = host.color_camera.image()
      logging.info("Color cached: %s", color)
      if color is not None:
        logging.info("Color cached image: %s", color.color_image.shape)

      color_depth = host.depth_camera.fetch_image()
      logging.info("Color depth: %s", color_depth)
      color_depth = host.depth_camera.image()
      logging.info("Color depth cached: %s", color_depth)
      if color_depth is not None:
        logging.info("Color depth cached color image: %s",
                     color_depth.color_data.shape)
        logging.info("Color depth cached depth image: %s",
                     color_depth.depth_data.shape)

      def oracle_cb(msg: pyreach.Prediction) -> None:
        logging.info("Oracle callback prediction: %s", msg)

      def oracle_err_cb(status: pyreach.PyReachStatus) -> None:
        logging.info("Error getting prediction: %s", status)

      host.oracle.async_fetch_prediction(
          "pick",
          "pick",
          "sparse",
          "122",
          "SingulateLeftBin",
          callback=oracle_cb,
          error_callback=oracle_err_cb)

      prediction = host.oracle.fetch_prediction("pick", "pick", "sparse", "122",
                                                "SingulateLeftBin")
      logging.info("Oracle: %s, %s", prediction,
                   prediction.points if prediction is not None else None)

      logging.info("Vac on: %s", host.vacuum.on())
      if host.vacuum.support_blowoff:
        logging.info("Vac blowoff: %s", host.vacuum.blowoff())
      logging.info("Vac off: %s", host.vacuum.off())

      logging.info("End annotation: %s",
                   host.logger.end_annotation_interval("test-annotation"))

    for thread in threading.enumerate():
      if thread != threading.current_thread():
        logging.info("Thread still running: %s", thread.name)


if __name__ == "__main__":
  unittest.main()
