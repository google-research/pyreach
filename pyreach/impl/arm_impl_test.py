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

from typing import Dict, List, Optional, Tuple, Union
import unittest
import numpy as np  # type: ignore
from pyreach import arm
from pyreach import core
from pyreach.common.python import types_gen
from pyreach.impl import actions_impl
from pyreach.impl import arm_impl
from pyreach.impl import calibration_impl as cal
from pyreach.impl import device_base
from pyreach.impl import test_data
from pyreach.impl import test_utils
from pyreach.impl import thread_util
from pyreach.impl import workcell_io_impl


class TestPyreachArmImpl(unittest.TestCase):

  def _init_arm(
      self, urdf_file: str, expect_ik_search: List[np.ndarray]
  ) -> Tuple[device_base.DeviceBase, arm_impl.ArmImpl]:
    calibration_device = cal.CalDevice()
    key = device_base.KeyValueKey(
        device_type="settings-engine", device_name="", key="calibration.json")
    calibration_device.on_set_key_value(key, test_data.get_calibration_json())
    calibration_device.close()
    actionsets_device = actions_impl.ActionDevice()
    key = device_base.KeyValueKey(
        device_type="settings-engine", device_name="", key="actionsets.json")
    actionsets_device.on_set_key_value(key, test_data.get_actionsets_json())
    actionsets_device.close()
    workcell_io_device = workcell_io_impl.WorkcellIoDevice()
    key = device_base.KeyValueKey(
        device_type="settings-engine", device_name="", key="workcell_io.json")
    workcell_io_device.on_set_key_value(key, test_data.get_workcell_io_json())
    workcell_io_device.close()
    iklib = TestIKFast(urdf_file, expect_ik_search)  # type: ignore
    rdev, extra_devs, dev = arm_impl.ArmDevice(
        arm_impl.ArmTypeImpl.from_urdf_file(urdf_file), calibration_device,
        actionsets_device, workcell_io_device.get(), "", iklib, False,
        arm.IKLibType.IKFAST).get_wrapper()
    dev._enable_randomization = False
    for extra_dev in extra_devs:
      extra_dev.close()
    self.assertEqual(dev.device_name, "")
    self.assertEqual(dev.arm_type.urdf_file, urdf_file)
    self.assertEqual(dev.arm_type.joint_count, 6)
    for digital_output_type in dev.digital_outputs:
      self.fail("Got digital outputs of type: " + digital_output_type)
    return rdev, dev

  def _validate_async_response(self,
                               statuses: List[core.PyReachStatus]) -> None:
    self.assertEqual(len(statuses), 2)
    self.assertEqual(statuses[0].status, "executing")
    self.assertEqual(statuses[0].error, "")
    self.assertEqual(statuses[0].message, "")
    self.assertEqual(statuses[1].status, "done")
    self.assertEqual(statuses[1].error, "")
    self.assertEqual(statuses[1].message, "")

  def test_to_pose(self) -> None:
    rdev, dev = self._init_arm("ur5e.urdf", [
        np.array([
            1.6540831333902932, -0.65556380727104, 1.394939944111822,
            -2.296503262239259, 4.649417918706931, 0.006600704600401741
        ]),
        np.array([
            1.6540831333902932, -0.65556380727104, 1.394939944111822,
            -2.296503262239259, 4.649417918706931, 0.006600704600401741
        ]),
        np.array([
            1.6763853648318705, -0.9809819685779639, 1.5026367936800202,
            -2.0773793705696866, 4.649738410960897, 0.02894469760442231
        ]),
    ])
    with test_utils.TestDevice(rdev) as test_device:
      test_device.set_responder(TestArm(""))
      state = dev.fetch_state()
      test_device.expect_command_data([
          types_gen.CommandData(device_type="robot", data_type="frame-request")
      ])
      self.assertIsNotNone(state)
      if state is None:
        return
      # Test to_pose without adjust
      status = dev.to_pose(
          core.Pose(
              core.Translation(0.1875917, -0.71203265, 0.0567831),
              core.AxisAngle(0.11865415, -3.07573961, -0.01666055)),
          intent="test-intent",
          pick_id="test-pick-id",
          success_type="test-success-type",
          acceleration=4.0,
          velocity=1.0)
      self.assertEqual(status.status, "done")
      self.assertEqual(status.error, "")
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="reach-script",
              device_type="robot",
              intent="test-intent",
              pick_id="test-pick-id",
              success_type="test-success-type",
              tag="tag-1",
              reach_script=types_gen.ReachScript(
                  preemptive=False,
                  preemptive_reason="",
                  version=0,
                  calibration_requirement=types_gen
                  .ReachScriptCalibrationRequirement(allow_uncalibrated=False),
                  commands=[
                      types_gen.ReachScriptCommand(
                          move_j_path=types_gen.MoveJPathArgs(waypoints=[
                              types_gen.MoveJWaypointArgs(
                                  acceleration=4.0,
                                  rotation=[
                                      1.6540831333902932, -0.65556380727104,
                                      1.394939944111822, -2.296503262239259,
                                      4.649417918706931, 0.006600704600401741
                                  ],
                                  velocity=1.0)
                          ]))
                  ]))
      ])
      # Test to_pose without adjust, linear
      status = dev.to_pose(
          core.Pose(
              core.Translation(0.1875917, -0.71203265, 0.0567831),
              core.AxisAngle(0.11865415, -3.07573961, -0.01666055)),
          intent="test-intent",
          pick_id="test-pick-id",
          success_type="test-success-type",
          use_linear=True,
          acceleration=4.0,
          velocity=1.0)
      self.assertEqual(status.status, "done")
      self.assertEqual(status.error, "")
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="reach-script",
              device_type="robot",
              intent="test-intent",
              pick_id="test-pick-id",
              success_type="test-success-type",
              tag="tag-2",
              reach_script=types_gen.ReachScript(
                  preemptive=False,
                  preemptive_reason="",
                  version=0,
                  calibration_requirement=types_gen
                  .ReachScriptCalibrationRequirement(allow_uncalibrated=False),
                  commands=[
                      types_gen.ReachScriptCommand(
                          move_l_path=types_gen.MoveLPathArgs(waypoints=[
                              types_gen.MoveLWaypointArgs(
                                  acceleration=4.0,
                                  rotation=[
                                      1.6540831333902932, -0.65556380727104,
                                      1.394939944111822, -2.296503262239259,
                                      4.649417918706931, 0.006600704600401741
                                  ],
                                  velocity=1.0)
                          ]))
                  ]))
      ])
      # Test to_pose without adjust
      status = dev.to_pose(
          core.Pose(
              core.Translation(0.1875917, -0.71203265, 0.0567831),
              core.AxisAngle(0.11865415, -3.07573961, -0.01666055)),
          intent="test-intent",
          pick_id="test-pick-id",
          success_type="test-success-type",
          acceleration=3.0,
          velocity=2.0,
          apply_tip_adjust_transform=True)
      self.assertEqual(status.status, "done")
      self.assertEqual(status.error, "")
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="reach-script",
              device_type="robot",
              intent="test-intent",
              pick_id="test-pick-id",
              success_type="test-success-type",
              tag="tag-3",
              reach_script=types_gen.ReachScript(
                  preemptive=False,
                  preemptive_reason="",
                  version=0,
                  calibration_requirement=types_gen
                  .ReachScriptCalibrationRequirement(allow_uncalibrated=False),
                  commands=[
                      types_gen.ReachScriptCommand(
                          move_j_path=types_gen.MoveJPathArgs(waypoints=[
                              types_gen.MoveJWaypointArgs(
                                  acceleration=3.0,
                                  rotation=[
                                      1.6763853648318705, -0.9809819685779639,
                                      1.5026367936800202, -2.0773793705696866,
                                      4.649738410960897, 0.02894469760442231
                                  ],
                                  velocity=2.0)
                          ]))
                  ]))
      ])

  def test_async_to_pose(self) -> None:
    rdev, dev = self._init_arm("ur5e.urdf", [
        np.array([
            1.6540831333902932, -0.65556380727104, 1.394939944111822,
            -2.296503262239259, 4.649417918706931, 0.006600704600401741
        ]),
        np.array([
            1.6540831333902932, -0.65556380727104, 1.394939944111822,
            -2.296503262239259, 4.649417918706931, 0.006600704600401741
        ]),
        np.array([
            1.6763853648318705, -0.9809819685779639, 1.5026367936800202,
            -2.0773793705696866, 4.649738410960897, 0.02894469760442231
        ]),
    ])
    with test_utils.TestDevice(rdev) as test_device:
      test_device.set_responder(TestArm(""))
      state = dev.fetch_state()
      test_device.expect_command_data([
          types_gen.CommandData(device_type="robot", data_type="frame-request")
      ])
      self.assertIsNotNone(state)
      if state is None:
        return
      # Test to_pose without adjust
      capturer: "thread_util.CallbackCapturer[core.PyReachStatus]"
      capturer = thread_util.CallbackCapturer()
      dev.async_to_pose(
          core.Pose(
              core.Translation(0.1875917, -0.71203265, 0.0567831),
              core.AxisAngle(0.11865415, -3.07573961, -0.01666055)),
          intent="test-intent",
          pick_id="test-pick-id",
          success_type="test-success-type",
          acceleration=4.0,
          velocity=1.0,
          callback=capturer.callback,
          finished_callback=capturer.finished_callback)
      self._validate_async_response(capturer.wait())
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="reach-script",
              device_type="robot",
              intent="test-intent",
              pick_id="test-pick-id",
              success_type="test-success-type",
              tag="tag-1",
              reach_script=types_gen.ReachScript(
                  preemptive=False,
                  preemptive_reason="",
                  version=0,
                  calibration_requirement=types_gen
                  .ReachScriptCalibrationRequirement(allow_uncalibrated=False),
                  commands=[
                      types_gen.ReachScriptCommand(
                          move_j_path=types_gen.MoveJPathArgs(waypoints=[
                              types_gen.MoveJWaypointArgs(
                                  acceleration=4.0,
                                  rotation=[
                                      1.6540831333902932, -0.65556380727104,
                                      1.394939944111822, -2.296503262239259,
                                      4.649417918706931, 0.006600704600401741
                                  ],
                                  velocity=1.0)
                          ]))
                  ]))
      ])
      # Test to_pose without adjust, linear
      capturer = thread_util.CallbackCapturer()
      dev.async_to_pose(
          core.Pose(
              core.Translation(0.1875917, -0.71203265, 0.0567831),
              core.AxisAngle(0.11865415, -3.07573961, -0.01666055)),
          intent="test-intent",
          pick_id="test-pick-id",
          success_type="test-success-type",
          use_linear=True,
          acceleration=4.0,
          velocity=1.0,
          callback=capturer.callback,
          finished_callback=capturer.finished_callback)
      self._validate_async_response(capturer.wait())
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="reach-script",
              device_type="robot",
              intent="test-intent",
              pick_id="test-pick-id",
              success_type="test-success-type",
              tag="tag-2",
              reach_script=types_gen.ReachScript(
                  preemptive=False,
                  preemptive_reason="",
                  version=0,
                  calibration_requirement=types_gen
                  .ReachScriptCalibrationRequirement(allow_uncalibrated=False),
                  commands=[
                      types_gen.ReachScriptCommand(
                          move_l_path=types_gen.MoveLPathArgs(waypoints=[
                              types_gen.MoveLWaypointArgs(
                                  acceleration=4.0,
                                  rotation=[
                                      1.6540831333902932, -0.65556380727104,
                                      1.394939944111822, -2.296503262239259,
                                      4.649417918706931, 0.006600704600401741
                                  ],
                                  velocity=1.0)
                          ]))
                  ]))
      ])
      # Test to_pose without adjust
      capturer = thread_util.CallbackCapturer()
      dev.async_to_pose(
          core.Pose(
              core.Translation(0.1875917, -0.71203265, 0.0567831),
              core.AxisAngle(0.11865415, -3.07573961, -0.01666055)),
          intent="test-intent",
          pick_id="test-pick-id",
          success_type="test-success-type",
          acceleration=3.0,
          velocity=2.0,
          apply_tip_adjust_transform=True,
          callback=capturer.callback,
          finished_callback=capturer.finished_callback)
      self._validate_async_response(capturer.wait())
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="reach-script",
              device_type="robot",
              intent="test-intent",
              pick_id="test-pick-id",
              success_type="test-success-type",
              tag="tag-3",
              reach_script=types_gen.ReachScript(
                  preemptive=False,
                  preemptive_reason="",
                  version=0,
                  calibration_requirement=types_gen
                  .ReachScriptCalibrationRequirement(allow_uncalibrated=False),
                  commands=[
                      types_gen.ReachScriptCommand(
                          move_j_path=types_gen.MoveJPathArgs(waypoints=[
                              types_gen.MoveJWaypointArgs(
                                  acceleration=3.0,
                                  rotation=[
                                      1.6763853648318705, -0.9809819685779639,
                                      1.5026367936800202, -2.0773793705696866,
                                      4.649738410960897, 0.02894469760442231
                                  ],
                                  velocity=2.0)
                          ]))
                  ]))
      ])

  def test_to_joints(self) -> None:
    rdev, dev = self._init_arm("ur5e.urdf", [])
    with test_utils.TestDevice(rdev) as test_device:
      test_device.set_responder(TestArm(""))
      state = dev.fetch_state()
      test_device.expect_command_data([
          types_gen.CommandData(device_type="robot", data_type="frame-request")
      ])
      self.assertIsNotNone(state)
      if state is None:
        return
      # Test to_joints without adjust
      status = dev.to_joints([0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                             intent="test-intent",
                             pick_id="test-pick-id",
                             success_type="test-success-type",
                             acceleration=4.0,
                             velocity=1.0)
      self.assertEqual(status.status, "done")
      self.assertEqual(status.error, "")
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="reach-script",
              device_type="robot",
              intent="test-intent",
              pick_id="test-pick-id",
              success_type="test-success-type",
              tag="tag-1",
              reach_script=types_gen.ReachScript(
                  preemptive=False,
                  preemptive_reason="",
                  version=0,
                  calibration_requirement=types_gen
                  .ReachScriptCalibrationRequirement(allow_uncalibrated=False),
                  commands=[
                      types_gen.ReachScriptCommand(
                          move_j_path=types_gen.MoveJPathArgs(waypoints=[
                              types_gen.MoveJWaypointArgs(
                                  acceleration=4.0,
                                  rotation=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                                  velocity=1.0)
                          ]))
                  ]))
      ])
      # Test to_joints, linear
      status = dev.to_joints([0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                             intent="test-intent",
                             pick_id="test-pick-id",
                             success_type="test-success-type",
                             use_linear=True,
                             acceleration=4.0,
                             velocity=1.0)
      self.assertEqual(status.status, "done")
      self.assertEqual(status.error, "")
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="reach-script",
              device_type="robot",
              intent="test-intent",
              pick_id="test-pick-id",
              success_type="test-success-type",
              tag="tag-2",
              reach_script=types_gen.ReachScript(
                  preemptive=False,
                  preemptive_reason="",
                  version=0,
                  calibration_requirement=types_gen
                  .ReachScriptCalibrationRequirement(allow_uncalibrated=False),
                  commands=[
                      types_gen.ReachScriptCommand(
                          move_l_path=types_gen.MoveLPathArgs(waypoints=[
                              types_gen.MoveLWaypointArgs(
                                  acceleration=4.0,
                                  rotation=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                                  velocity=1.0)
                          ]))
                  ]))
      ])
      # Test to_joints
      status = dev.to_joints([0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                             intent="test-intent",
                             pick_id="test-pick-id",
                             success_type="test-success-type",
                             acceleration=3.0,
                             servo=True,
                             velocity=2.0)
      self.assertEqual(status.status, "done")
      self.assertEqual(status.error, "")
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="reach-script",
              device_type="robot",
              intent="test-intent",
              pick_id="test-pick-id",
              success_type="test-success-type",
              tag="tag-3",
              reach_script=types_gen.ReachScript(
                  preemptive=False,
                  preemptive_reason="",
                  version=0,
                  calibration_requirement=types_gen
                  .ReachScriptCalibrationRequirement(allow_uncalibrated=False),
                  commands=[
                      types_gen.ReachScriptCommand(
                          move_j_path=types_gen.MoveJPathArgs(waypoints=[
                              types_gen.MoveJWaypointArgs(
                                  acceleration=3.0,
                                  servo=True,
                                  rotation=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                                  velocity=2.0)
                          ]))
                  ]))
      ])

  def test_async_to_joints(self) -> None:
    rdev, dev = self._init_arm("ur5e.urdf", [])
    with test_utils.TestDevice(rdev) as test_device:
      test_device.set_responder(TestArm(""))
      state = dev.fetch_state()
      test_device.expect_command_data([
          types_gen.CommandData(device_type="robot", data_type="frame-request")
      ])
      self.assertIsNotNone(state)
      if state is None:
        return
      # Test async_to_joints
      capturer: "thread_util.CallbackCapturer[core.PyReachStatus]"
      capturer = thread_util.CallbackCapturer()
      dev.async_to_joints([0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                          intent="test-intent",
                          pick_id="test-pick-id",
                          success_type="test-success-type",
                          acceleration=4.0,
                          velocity=1.0,
                          callback=capturer.callback,
                          finished_callback=capturer.finished_callback)
      self._validate_async_response(capturer.wait())
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="reach-script",
              device_type="robot",
              intent="test-intent",
              pick_id="test-pick-id",
              success_type="test-success-type",
              tag="tag-1",
              reach_script=types_gen.ReachScript(
                  preemptive=False,
                  preemptive_reason="",
                  version=0,
                  calibration_requirement=(
                      types_gen.ReachScriptCalibrationRequirement()),
                  commands=[
                      types_gen.ReachScriptCommand(
                          move_j_path=types_gen.MoveJPathArgs(waypoints=[
                              types_gen.MoveJWaypointArgs(
                                  acceleration=4.0,
                                  rotation=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                                  velocity=1.0)
                          ]))
                  ]))
      ])
      # Test async_to_joints linear
      capturer = thread_util.CallbackCapturer()
      dev.async_to_joints([0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                          intent="test-intent",
                          pick_id="test-pick-id",
                          success_type="test-success-type",
                          use_linear=True,
                          acceleration=4.0,
                          velocity=1.0,
                          callback=capturer.callback,
                          finished_callback=capturer.finished_callback)
      self._validate_async_response(capturer.wait())
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="reach-script",
              device_type="robot",
              intent="test-intent",
              pick_id="test-pick-id",
              success_type="test-success-type",
              tag="tag-2",
              reach_script=types_gen.ReachScript(
                  preemptive=False,
                  preemptive_reason="",
                  version=0,
                  calibration_requirement=(
                      types_gen.ReachScriptCalibrationRequirement()),
                  commands=[
                      types_gen.ReachScriptCommand(
                          move_l_path=types_gen.MoveLPathArgs(waypoints=[
                              types_gen.MoveLWaypointArgs(
                                  acceleration=4.0,
                                  rotation=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                                  velocity=1.0)
                          ]))
                  ]))
      ])
      # Test async_to_joints without adjust
      capturer = thread_util.CallbackCapturer()
      dev.async_to_joints([0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                          intent="test-intent",
                          pick_id="test-pick-id",
                          success_type="test-success-type",
                          acceleration=3.0,
                          velocity=2.0,
                          servo=True,
                          callback=capturer.callback,
                          finished_callback=capturer.finished_callback)
      self._validate_async_response(capturer.wait())
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="reach-script",
              device_type="robot",
              intent="test-intent",
              pick_id="test-pick-id",
              success_type="test-success-type",
              tag="tag-3",
              reach_script=types_gen.ReachScript(
                  preemptive=False,
                  preemptive_reason="",
                  version=0,
                  calibration_requirement=(
                      types_gen.ReachScriptCalibrationRequirement()),
                  commands=[
                      types_gen.ReachScriptCommand(
                          move_j_path=types_gen.MoveJPathArgs(waypoints=[
                              types_gen.MoveJWaypointArgs(
                                  servo=True,
                                  acceleration=3.0,
                                  rotation=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
                                  velocity=2.0)
                          ]))
                  ]))
      ])

  def test_stop(self) -> None:
    rdev, dev = self._init_arm("ur5e.urdf", [
        np.array([
            1.6540831333902932, -0.65556380727104, 1.394939944111822,
            -2.296503262239259, 4.649417918706931, 0.006600704600401741
        ]),
        np.array([
            1.6540831333902932, -0.65556380727104, 1.394939944111822,
            -2.296503262239259, 4.649417918706931, 0.006600704600401741
        ]),
        np.array([
            1.6763853648318705, -0.9809819685779639, 1.5026367936800202,
            -2.0773793705696866, 4.649738410960897, 0.02894469760442231
        ]),
    ])
    with test_utils.TestDevice(rdev) as test_device:
      test_device.set_responder(TestArm(""))
      state = dev.fetch_state()
      test_device.expect_command_data([
          types_gen.CommandData(device_type="robot", data_type="frame-request")
      ])
      self.assertIsNotNone(state)
      if state is None:
        return
      # Test async_stop
      capturer: "thread_util.CallbackCapturer[core.PyReachStatus]"
      capturer = thread_util.CallbackCapturer()
      dev.async_stop(
          deceleration=5.0,
          intent="test-intent",
          pick_id="test-pick-id",
          success_type="test-success-type",
          callback=capturer.callback,
          finished_callback=capturer.finished_callback)
      self._validate_async_response(capturer.wait())
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="reach-script",
              device_type="robot",
              intent="test-intent",
              pick_id="test-pick-id",
              success_type="test-success-type",
              tag="tag-1",
              reach_script=types_gen.ReachScript(
                  preemptive=False,
                  preemptive_reason="",
                  version=0,
                  calibration_requirement=types_gen
                  .ReachScriptCalibrationRequirement(allow_uncalibrated=False),
                  commands=[
                      types_gen.ReachScriptCommand(
                          stop_j=types_gen.StopJArgs(deceleration=5.0)),
                  ]))
      ])
      # Test stop
      status = dev.stop(
          deceleration=6.0,
          intent="test-intent",
          pick_id="test-pick-id",
          success_type="test-success-type")
      self.assertEqual(status.status, "done")
      self.assertEqual(status.error, "")
      test_device.expect_command_data([
          types_gen.CommandData(
              data_type="reach-script",
              device_type="robot",
              intent="test-intent",
              pick_id="test-pick-id",
              success_type="test-success-type",
              tag="tag-2",
              reach_script=types_gen.ReachScript(
                  preemptive=False,
                  preemptive_reason="",
                  version=0,
                  calibration_requirement=types_gen
                  .ReachScriptCalibrationRequirement(allow_uncalibrated=False),
                  commands=[
                      types_gen.ReachScriptCommand(
                          stop_j=types_gen.StopJArgs(deceleration=6.0)),
                  ]))
      ])

  def test_arm_state(self) -> None:
    rdev, dev = self._init_arm("ur5e.urdf", [])
    with test_utils.TestDevice(rdev) as test_device:
      global_callbacks: ("thread_util.CallbackCapturer[arm.ArmState]"
                        ) = thread_util.CallbackCapturer()
      stop = dev.add_update_callback(global_callbacks.callback_false,
                                     global_callbacks.finished_callback)
      test_device.set_responder(TestArm(""))
      state = dev.fetch_state()
      test_device.expect_command_data([
          types_gen.CommandData(device_type="robot", data_type="frame-request")
      ])
      self.assertIsNotNone(state)
      if state is None:
        return
      self._verify_state(state)
      self.assertEqual(state, dev.state())
      capturer: ("thread_util.DoubleCallbackCapturer[arm.ArmState, "
                 "core.PyReachStatus]") = thread_util.DoubleCallbackCapturer()
      dev.async_fetch_state(
          callback=capturer.first_callback_finish,
          error_callback=capturer.second_callback_finish)
      test_device.expect_command_data([
          types_gen.CommandData(device_type="robot", data_type="frame-request")
      ])
      states = capturer.wait()
      self.assertEqual(len(states), 1)
      self.assertIsNone(states[0][1])
      test_state = states[0][0]
      self.assertIsNotNone(test_state)
      if test_state:
        self._verify_state(test_state)
      self.assertEqual(states[0][0], dev.state())
      stop()
      global_states = global_callbacks.wait()
      self.assertEqual(len(global_states), 2)
      self.assertEqual(state, global_states[0])
      self.assertEqual(states[0][0], global_states[1])

  def _verify_state(self, state: arm.ArmState) -> None:
    self.assertEqual(
        state.joint_angles,
        (1.665570735931396, -0.7995384496501465, 1.341465298329489,
         -2.12082638363027, 4.660228729248047, 0.01271963119506836))
    self.assertEqual(state.pose.position.x, 0.1961122234076476)
    self.assertEqual(state.pose.position.y, -0.7146550885497088)
    self.assertEqual(state.pose.position.z, 0.1642837633972083)
    self.assertEqual(state.pose.orientation.axis_angle.rx, 0.1186541477907012)
    self.assertEqual(state.pose.orientation.axis_angle.ry, -3.075739605978813)
    self.assertEqual(state.pose.orientation.axis_angle.rz, -0.01666054968029903)
    self.assertEqual(
        state.force,
        (-6.514813773909755, 5.273554158068752, -3.661764071560078,
         -0.1562602891054569, -0.2400126816079334, 0.1363557378946311))
    self.assertFalse(state.is_protective_stopped)


class TestArm(test_utils.TestResponder):
  _device_name: str

  def __init__(self, device_name: str = "") -> None:
    super().__init__()
    self._device_name = device_name

  def start(self) -> List[types_gen.DeviceData]:
    return [
        types_gen.DeviceData(
            device_type="robot",
            data_type="key-value",
            key="robot_constraints.json",
            value=test_data.get_robot_constraints_json()),
        types_gen.DeviceData(
            device_type="settings-engine",
            data_type="key-value",
            key="document-config/ikhints",
            value=test_data.get_ikhints_json()),
    ]

  def step(self, cmd: types_gen.CommandData) -> List[types_gen.DeviceData]:
    if (cmd.device_type == "robot" and cmd.device_name == self._device_name and
        cmd.data_type == "reach-script"):
      if not cmd.tag:
        return []
      return [
          types_gen.DeviceData(
              device_type="robot",
              data_type="cmd-status",
              device_name=self._device_name,
              tag=cmd.tag,
              ts=cmd.ts,
              status="executing"),
          types_gen.DeviceData(
              device_type="robot",
              data_type="cmd-status",
              device_name=self._device_name,
              tag=cmd.tag,
              ts=cmd.ts,
              status="done"),
      ]
    if test_utils.is_frame_request_for(cmd, "robot", self._device_name):
      output = [
          types_gen.DeviceData(
              device_type="robot",
              data_type="robot-state",
              device_name=self._device_name,
              tag=cmd.tag,
              ts=cmd.ts,
              pose=[
                  0.1961122234076476, -0.7146550885497088, 0.1642837633972083,
                  0.1186541477907012, -3.075739605978813, -0.01666054968029903
              ],
              joints=[
                  1.665570735931396, -0.7995384496501465, 1.341465298329489,
                  -2.12082638363027, 4.660228729248047, 0.01271963119506836
              ],
              force=[
                  -6.514813773909755, 5.273554158068752, -3.661764071560078,
                  -0.1562602891054569, -0.2400126816079334, 0.1363557378946311
              ],
              is_robot_power_on=True,
              safety_message="NORMAL",
              digital_in=[
                  False, False, False, False, True, False, False, False, False,
                  False, False, False, False, False, False, False, False, False,
                  False, False, False, False, False, False, False, False, False,
                  False, False, False, False, False
              ],
              sensor_in=[
                  True, False, False, False, True, False, False, False, False,
                  False, False, False, False, False, False, False, False, False,
                  False, False, False, False, False, False, False, False, False,
                  False, False, False, False, False
              ],
              digital_out=[
                  False, False, False, False, False, False, False, False, True,
                  True, False, False, False, False, False, False, False, False,
                  False, False, False, False, False, False, False, False, False,
                  False, False, False, False, False
              ],
              analog_in=[0.7910740375518799, 0.0508582592010498],
              analog_out=[0.004000000189989805, 0.004000000189989805],
              tool_digital_in=[False, False],
              tool_digital_out=[False, False],
              tool_analog_in=[0.03083583153784275, 0.0239834263920784],
              board_temp_c=33.75,
              robot_voltage_v=47.7191276550293,
              robot_current_a=0.7933669090270996,
              tool_temp_c=34.125,
              tool_current_a=0.01900213956832886,
              joint_voltages_v=[
                  47.5275993347168, 47.5275993347168, 47.65659713745117,
                  47.75692367553711, 47.67092895507812, 47.49893188476562
              ],
              joint_currents_a=[
                  0.2138899713754654, -4.85020112991333, -1.559797167778015,
                  -0.4086463451385498, -0.1050002723932266, 0.007281774654984474
              ],
              joint_temps_c=[33.5, 35, 31.625, 34.25, 36.375, 36.625],
              robot_mode="remote",
              program_counter=5479,
              digital_bank=[
                  types_gen.DigitalBank(
                      space="standard",
                      output=True,
                      state=[
                          False, False, False, False, False, False, False, False
                      ]),
                  types_gen.DigitalBank(
                      space="standard",
                      state=[
                          False, False, False, False, True, False, False, False
                      ]),
                  types_gen.DigitalBank(
                      space="configurable",
                      output=True,
                      state=[
                          True, True, False, False, False, False, False, False
                      ]),
                  types_gen.DigitalBank(
                      space="configurable",
                      state=[
                          False, False, False, False, False, False, False, False
                      ]),
                  types_gen.DigitalBank(
                      space="tool", output=True, state=[False, False]),
                  types_gen.DigitalBank(space="tool", state=[False, False])
              ],
              analog_bank=[
                  types_gen.AnalogBank(
                      space="standard",
                      output=True,
                      state=[0.004000000189989805, 0.004000000189989805]),
                  types_gen.AnalogBank(
                      space="standard",
                      state=[0.7910740375518799, 0.0508582592010498]),
                  types_gen.AnalogBank(
                      space="tool",
                      state=[0.03083583153784275, 0.0239834263920784])
              ],
              last_terminated_program="f3e3d852-88ec-45cb-97c5-2d3b45429c22")
      ]
      if cmd.tag:
        output += [
            types_gen.DeviceData(
                device_type="robot",
                data_type="cmd-status",
                device_name=self._device_name,
                tag=cmd.tag,
                ts=cmd.ts,
                status="done")
        ]
      return output
    return []


class TestIKFast(arm_impl.IKLibIKFast):

  def __init__(self, urdf_file: str,
               expect_ik_search: List[np.ndarray]) -> None:
    super().__init__(urdf_file)
    self._ik_search_count = 0
    self._expect_ik_search = expect_ik_search

  def ik_search(self, pose: Union[List[Union[float, int]], Tuple[Union[float,
                                                                       int]]],
                current_joints: List[float], ik_hints: Dict[int, List[float]],
                use_unity_ik: bool) -> Optional[List[float]]:
    """Perform IK search and return a single joint pose.

    Args:
      pose: The pose.
      current_joints: the current joint state.
      ik_hints: The ik hints for the search.
      use_unity_ik: If true, use Unity IK.

    Returns:
      The joint position.
    """
    joints = super().ik_search([float(v) for v in pose], current_joints,
                               ik_hints, use_unity_ik)
    assert self._ik_search_count < len(self._expect_ik_search)
    assert joints is not None
    assert np.allclose(
        np.array(joints, dtype=np.float64),
        self._expect_ik_search[self._ik_search_count]), (
            "Got %s, expected %s for step %d" %
            (joints, self._expect_ik_search[self._ik_search_count].tolist(),
             self._ik_search_count))
    override_joints = self._expect_ik_search[self._ik_search_count]
    self._ik_search_count += 1
    return override_joints.tolist()


if __name__ == "__main__":
  unittest.main()
