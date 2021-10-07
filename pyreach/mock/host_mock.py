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

"""HostMock unit tests."""

from typing import Any, Optional

from pyreach import arm
from pyreach import client_annotation
from pyreach import color_camera
from pyreach import core
from pyreach import depth_camera
from pyreach import force_torque_sensor
from pyreach import host
from pyreach import internal as pyreach_internal
from pyreach import logger
from pyreach import metrics
from pyreach import oracle
from pyreach import text_instruction
from pyreach import vacuum
from pyreach.mock import arm_mock
from pyreach.mock import client_annotation_mock
from pyreach.mock import color_camera_mock
from pyreach.mock import depth_camera_mock
from pyreach.mock import force_torque_sensor_mock
from pyreach.mock import logger_mock
from pyreach.mock import text_instructions_mock
from pyreach.mock import vacuum_mock


class HostMock(host.Host):
  """Mock implementation of PyReachHost."""

  def __init__(self) -> None:
    """Initialize the MockHost."""
    super().__init__()
    self._logger: logger.Logger = logger_mock.LoggerMock()
    self._timers: pyreach_internal.Timers = pyreach_internal.Timers(set())

  def __enter__(self) -> "host.Host":
    """With statement entry dunder."""
    raise NotImplementedError

  def __exit__(self, typ: Any, value: Any, traceback: Any) -> None:
    """With statement exit dunder."""
    raise NotImplementedError

  def __str__(self) -> str:
    """Return a string representation."""
    return "MockHost()"

  def close(self) -> None:
    """Close the connection to the host."""
    pass

  def wait(self) -> None:
    """Wait for the host to close."""
    raise NotImplementedError

  def is_closed(self) -> bool:
    """Determine if the host is closed."""
    raise NotImplementedError

  def reset(self) -> None:
    """Reset the host."""
    pass

  @property
  def config(self) -> host.Config:
    """Return the config dictionary."""
    raise NotImplementedError

  @property
  def arms(self) -> core.ImmutableDictionary[arm.Arm]:
    """Return all the robot arms connected to the system.

    The key of the dictionary is the device name, such as "left" or "right".
    """
    mock_arm: arm.Arm = arm_mock.ArmMock()
    return core.ImmutableDictionary[arm.Arm]({"robot": mock_arm})

  @property
  def arm(self) -> Optional[arm.Arm]:
    """Return the robot arm if there is just one.

    None if there is no robot arm or multiple robot arms.
    """
    mock_arm: arm_mock.ArmMock = arm_mock.ArmMock()
    return mock_arm

  @property
  def client_annotation(self) -> client_annotation.ClientAnnotation:
    """Return the client annotation device."""
    mock_client_annotation: client_annotation.ClientAnnotation
    mock_client_annotation = client_annotation_mock.ClientAnnotationMock()
    return mock_client_annotation

  @property
  def color_cameras(self) -> core.ImmutableDictionary[color_camera.ColorCamera]:
    """Return all the color cameras connected to the system.

    The key of the dictionary is the device name, such as "front" or "overview".
    """
    mock_color_camera: color_camera.ColorCamera
    mock_color_camera = color_camera_mock.ColorCameraMock()
    return core.ImmutableDictionary({"ColorCamera": mock_color_camera})

  @property
  def color_camera(self) -> Optional[color_camera.ColorCamera]:
    """Return the color camera if there is just one.

    None if there is no color camera or multiple color cameras.
    """
    mock_color_camera: color_camera.ColorCamera
    mock_color_camera = color_camera_mock.ColorCameraMock()
    return mock_color_camera

  @property
  def depth_cameras(self) -> core.ImmutableDictionary[depth_camera.DepthCamera]:
    """Return all the depth cameras connected to the system.

    The key of the dictionary is the device name, such as "top" or "side".
    """
    mock_depth_camera: depth_camera.DepthCamera
    mock_depth_camera = depth_camera_mock.DepthCameraMock()
    return core.ImmutableDictionary({"DepthCamera": mock_depth_camera})

  @property
  def depth_camera(self) -> Optional[depth_camera.DepthCamera]:
    """Return the depth camera if there is just one.

    None if there is no depth camera or multiple depth cameras.
    """
    raise NotImplementedError

  @property
  def force_torque_sensors(
      self) -> core.ImmutableDictionary[force_torque_sensor.ForceTorqueSensor]:
    """Return all the force torque sensor devices connected to the system.

    The key of the dictionary is the device name.
    """
    mock_force_torque_sensor: force_torque_sensor_mock.ForceTorqueSensorMock
    mock_force_torque_sensor = force_torque_sensor_mock.ForceTorqueSensorMock()
    return core.ImmutableDictionary(
        {"ForceTorqueSensor": mock_force_torque_sensor})

  @property
  def force_torque_sensor(
      self) -> Optional[force_torque_sensor.ForceTorqueSensor]:
    """Return the force torque sensor device if there is just one."""
    raise NotImplementedError

  @property
  def vacuums(self) -> core.ImmutableDictionary[vacuum.Vacuum]:
    """Return all the vacuum devices connected to the system.

    The key of the dictionary is the device name.
    """
    mock_vacuum: vacuum.Vacuum = vacuum_mock.VacuumMock()
    return core.ImmutableDictionary({"": mock_vacuum})

  @property
  def vacuum(self) -> Optional[vacuum.Vacuum]:
    """Return the vacuum device if there is just one.

    None if there is no vacuum device or multiple vacuum devices.
    """
    raise NotImplementedError

  @property
  def oracles(self) -> core.ImmutableDictionary[oracle.Oracle]:
    """Return all the oracle devices connected to the system.

    The key of the dictionary is the device name.
    """
    raise NotImplementedError

  @property
  def oracle(self) -> Optional[oracle.Oracle]:
    """Return the oracle device if there is just one.

    None if there is no oracle device or multiple oracle devices.
    """
    raise NotImplementedError

  @property
  def internal(self) -> Optional[pyreach_internal.Internal]:
    """Access PyReach internal APIs."""
    raise NotImplementedError

  @property
  def logger(self) -> logger.Logger:
    """Return the Logger object."""
    return self._logger

  @property
  def metrics(self) -> metrics.Metrics:
    """Return the Metrics object."""
    raise NotImplementedError

  @property
  def text_instructions(self) -> text_instruction.TextInstructions:
    """Return the TextInstructions object."""
    text_instructions: text_instruction.TextInstructions
    text_instructions = text_instructions_mock.TextInstructionsMock()
    return text_instructions

  def get_server_offset_time(self) -> Optional[float]:
    """Return the offset to the server time.

    Returns:
      The offset to the server-side time, or None if it could not be computed.
    """
    return None

  def set_timers(self, timers: pyreach_internal.Timers) -> None:
    """Set the Host performance timers."""
    self._timers = timers
