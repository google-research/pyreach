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

"""Host is the entry point to the PyReach API.

A Host object is responsible for connecting to a Reach host, initializing
interfaces objects for accessing various devices such as robot arm and camera.
"""
import enum
from typing import Any, Callable, Optional, TypeVar

from pyreach import actionsets
from pyreach import arm
from pyreach import calibration
from pyreach import client_annotation
from pyreach import color_camera
from pyreach import constraints
from pyreach import core
from pyreach import depth_camera
from pyreach import force_torque_sensor
from pyreach import internal as pyreach_internal
from pyreach import logger
from pyreach import metrics
from pyreach import oracle
from pyreach import playback
from pyreach import text_instruction
from pyreach import vacuum
from pyreach import vnc

T = TypeVar("T")


class SessionState(enum.Enum):
  """An enumeration class of session states."""

  UNKNOWN = "UNKNOWN"
  BLOCKED = "BLOCKED"
  EVICTABLE = "EVICTABLE"
  INACTIVE = "INACTIVE"
  ACTIVE = "ACTIVE"
  SHUTDOWN = "SHUTDOWN"
  PLAYBACK = "PLAYBACK"


class Config(object):
  """Configuration group."""

  @property
  def calibration(self) -> Optional[calibration.Calibration]:
    """Return the Calibration."""
    raise NotImplementedError

  @property
  def constraint(self) -> Optional[constraints.Constraints]:
    """Return the Constraints."""
    raise NotImplementedError

  @property
  def actionset(self) -> Optional[actionsets.Actions]:
    """Return the Actonset."""
    raise NotImplementedError


class Host(object):
  """Entry point of PyReach for accessing resources of a Reach host."""

  def __enter__(self) -> "Host":
    """With statement entry dunder."""
    raise NotImplementedError

  def __exit__(self, typ: Any, value: Any, traceback: Any) -> None:
    """With statement exit dunder."""
    raise NotImplementedError

  def close(self) -> None:
    """Close the connection to the host."""
    raise NotImplementedError

  def wait(self) -> None:
    """Wait for the host to close."""
    raise NotImplementedError

  def is_closed(self) -> bool:
    """Determine if the host is closed."""
    raise NotImplementedError

  def reset(self) -> None:
    """Reset the host."""
    raise NotImplementedError

  @property
  def config(self) -> Config:
    """Return the config dictionary."""
    raise NotImplementedError

  @property
  def client_annotation(self) -> client_annotation.ClientAnnotation:
    """Return the client annotation device."""
    raise NotImplementedError

  @property
  def color_cameras(self) -> core.ImmutableDictionary[color_camera.ColorCamera]:
    """Return all the color cameras connected to the system.

    The key of the dictionary is the device name, such as "front" or "overview".
    """
    raise NotImplementedError

  @property
  def color_camera(self) -> Optional[color_camera.ColorCamera]:
    """Return the color camera if there is just one.

    None if there is no color camera or multiple color cameras.
    """
    raise NotImplementedError

  @property
  def depth_cameras(self) -> core.ImmutableDictionary[depth_camera.DepthCamera]:
    """Return all the depth cameras connected to the system.

    The key of the dictionary is the device name, such as "top" or "side".
    """
    raise NotImplementedError

  @property
  def depth_camera(self) -> Optional[depth_camera.DepthCamera]:
    """Return the depth camera if there is just one.

    None if there is no depth camera or multiple depth cameras.
    """
    raise NotImplementedError

  @property
  def arms(self) -> core.ImmutableDictionary[arm.Arm]:
    """Return all the robot arms connected to the system.

    The key of the dictionary is the device name, such as "left" or "right".
    """
    raise NotImplementedError

  @property
  def arm(self) -> Optional[arm.Arm]:
    """Return the robot arm if there is just one.

    None if there is no robot arm or multiple robot arms.
    """
    raise NotImplementedError

  @property
  def vacuums(self) -> core.ImmutableDictionary[vacuum.Vacuum]:
    """Return all the vacuum devices connected to the system.

    The key of the dictionary is the device name.
    """
    raise NotImplementedError

  @property
  def vacuum(self) -> Optional[vacuum.Vacuum]:
    """Return the vacuum device if there is just one.

    None if there is no vacuum device or multiple vacuum devices.
    """
    raise NotImplementedError

  @property
  def vncs(self) -> core.ImmutableDictionary[vnc.VNC]:
    """Return all the VNC devices connected to the system.

    The key of the dictionary is the device name.
    """
    raise NotImplementedError

  @property
  def vnc(self) -> Optional[vnc.VNC]:
    """Return the VNC device if there is just one.

    None if there is no VNC device.
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
  def force_torque_sensors(
      self) -> core.ImmutableDictionary[force_torque_sensor.ForceTorqueSensor]:
    """Return all the force torque sensors connected to the system.

    The key of the dictionary is the device name.
    """
    raise NotImplementedError

  @property
  def force_torque_sensor(
      self) -> Optional[force_torque_sensor.ForceTorqueSensor]:
    """Return the default force torque sensor.

    None if there is no force torque sensor device or the default sensor.
    """
    raise NotImplementedError

  @property
  def internal(self) -> Optional[pyreach_internal.Internal]:
    """Access PyReach internal APIs."""
    raise NotImplementedError

  @property
  def logger(self) -> logger.Logger:
    """Return the Logger object."""
    raise NotImplementedError

  @property
  def playback(self) -> Optional[playback.Playback]:
    """Return the playback object."""
    raise NotImplementedError

  @property
  def metrics(self) -> metrics.Metrics:
    """Return the Metrics object."""
    raise NotImplementedError

  @property
  def text_instructions(self) -> text_instruction.TextInstructions:
    """Return the TextInstructions object."""
    raise NotImplementedError

  def get_ping_time(self) -> Optional[float]:
    """Return the latest ping time.

    Returns:
      Returns the latest ping time or None if no ping time is available.

    """
    raise NotImplementedError

  def get_server_offset_time(self) -> Optional[float]:
    """Return the offset to the server time.

    Returns:
      The offset to the server-side time, or None if it could not be computed.
    """
    raise NotImplementedError

  def set_should_take_control(self,
                              should_take_control: bool,
                              should_release_control: bool = False) -> None:
    """Set the should take control flag.

    Args:
      should_take_control: If true, will try to start a control session.
      should_release_control: If true, will force release of control session.
    """
    raise NotImplementedError

  def wait_for_control(self, timeout: Optional[float] = None) -> bool:
    """Wait until the session becomes active.

    Args:
      timeout: timeout for time to wait for state.

    Returns:
      True if have taken control, false otherwise.
    """
    raise NotImplementedError

  def wait_for_session_state(self,
                             state: SessionState,
                             timeout: Optional[float] = None) -> bool:
    """Wait for a specific session state.

    Args:
      state: the state to wait for.
      timeout: timeout for time to wait for state.

    Returns:
      True if have entered the state, false otherwise.
    """
    raise NotImplementedError

  def get_session_state(self) -> SessionState:
    """Get the session state of the host.

    Returns:
      The session state.
    """
    raise NotImplementedError

  def add_session_state_callback(
      self,
      callback: Callable[[SessionState], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback when new a session state is received.

    Args:
      callback: triggers when new a session state is received.
      finished_callback: triggers when update is finished.

    Returns:
      Returns a function when called stops the callback.
    """
    raise NotImplementedError

  def add_host_id_callback(
      self,
      callback: Callable[[str], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback when new a host id is received.

    Args:
      callback: triggers when new host id is received.
      finished_callback: triggers when update is finished.

    Returns:
      Returns a function when called stops the callback.
    """
    raise NotImplementedError

  @property
  def host_id(self) -> Optional[str]:
    """Name gets the current host id of the robot.

    Returns:
      The current id of the host, or none if it is not loaded.
    """
    raise NotImplementedError

  def add_display_name_callback(
      self,
      callback: Callable[[str], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback when new a display name is received.

    Args:
      callback: triggers when new display name is received.
      finished_callback: triggers when update is finished.

    Returns:
      Returns a function when called stops the callback.
    """
    raise NotImplementedError

  @property
  def display_name(self) -> Optional[str]:
    """Name gets the current display name of the robot.

    Returns:
      The current display name of the robot, or none if it is not loaded.
    """
    raise NotImplementedError
