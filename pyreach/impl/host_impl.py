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

"""Implementation of the PyReach Host interface."""
import logging
import queue
import threading
import time
from typing import Any, Callable, Dict, List, Set, Optional, Tuple

import pyreach
from pyreach import actionsets
from pyreach import arm
from pyreach import calibration
from pyreach import client_annotation
from pyreach import constraints
from pyreach import core
from pyreach import force_torque_sensor
from pyreach import host
from pyreach import internal
from pyreach import vnc
from pyreach.common.python import types_gen
from pyreach.impl import actions_impl
from pyreach.impl import arm_impl
from pyreach.impl import calibration_impl
from pyreach.impl import client as cli
from pyreach.impl import client_annotation_impl
from pyreach.impl import color_camera_impl
from pyreach.impl import constraints_impl
from pyreach.impl import depth_camera_impl
from pyreach.impl import device_base
from pyreach.impl import force_torque_sensor_impl
from pyreach.impl import internal_impl
from pyreach.impl import logger_impl
from pyreach.impl import machine_interfaces
from pyreach.impl import machine_interfaces_impl
from pyreach.impl import metrics_impl
from pyreach.impl import oracle_impl
from pyreach.impl import playback_impl
from pyreach.impl import reach_host
from pyreach.impl import text_instruction_impl
from pyreach.impl import utils
from pyreach.impl import vacuum_impl
from pyreach.impl import vnc_impl
from pyreach.impl import workcell_io_impl
from pyreach.playback import Playback
from pyreach.common.proto_gen import workcell_io_pb2 as workcell_io


class ConfigImpl(host.Config):
  """Configuration group."""

  _devices: List[device_base.DeviceBase]
  _constraints: constraints_impl.ConstraintsDevice
  _calibration: calibration_impl.CalDevice
  _actionsets: actions_impl.ActionDevice
  _machine_interfaces: machine_interfaces_impl.MachineInterfacesWrapper
  _workcell_io: workcell_io_impl.WorkcellIoDevice

  def __init__(self) -> None:
    """Construct a configuration group."""
    self._devices = []

    def add_device(dev: Tuple[device_base.DeviceBase, host.T]) -> host.T:
      self._devices.append(dev[0])
      return dev[1]

    # Add constraints
    self._constraints = constraints_impl.ConstraintsDevice("")
    self._devices.append(self._constraints)
    # Add calibration
    self._calibration = calibration_impl.CalDevice()
    self._devices.append(self._calibration)
    # Add actionsets
    self._actionsets = actions_impl.ActionDevice()
    self._devices.append(self._actionsets)
    # Add machine interfaces
    self._machine_interfaces = add_device(
        machine_interfaces_impl.MachineInterfacesDevice().get_wrapper())
    # Add workcell io
    self._workcell_io = workcell_io_impl.WorkcellIoDevice()
    self._devices.append(self._workcell_io)

  @property
  def calibration(self) -> Optional[pyreach.Calibration]:
    """Return the Calibration."""
    return self._calibration.get()

  @property
  def constraint(self) -> Optional[constraints.Constraints]:
    """Return the Constraints."""
    return self._constraints.get()

  @property
  def actionset(self) -> Optional[actionsets.Actions]:
    """Return the Actonset."""
    return self._actionsets.get_actions()

  @property
  def machine_interfaces(
      self) -> Optional[machine_interfaces.MachineInterfaces]:
    """Return the Machine Interfaces."""
    return self._machine_interfaces.get()

  @property
  def workcell_io(self) -> Optional[workcell_io.IOConfig]:
    """Return the Workcell IO."""
    return self._workcell_io.get()


class HostImpl(pyreach.Host):
  """Entry point of PyReach for accessing resources of a Reach host."""

  _host: reach_host.ReachHost
  _client_annotation: client_annotation.ClientAnnotation
  _color_cameras: core.ImmutableDictionary[pyreach.ColorCamera]
  _color_camera: Optional[pyreach.ColorCamera]
  _depth_cameras: core.ImmutableDictionary[pyreach.DepthCamera]
  _depth_camera: Optional[pyreach.DepthCamera]
  _force_torque_sensors: core.ImmutableDictionary[pyreach.ForceTorqueSensor]
  _force_torque_sensor: Optional[pyreach.ForceTorqueSensor]
  _arms: core.ImmutableDictionary[arm_impl.ArmImpl]
  _arm: Optional[arm_impl.ArmImpl]
  _internal: Optional[internal.Internal]
  _vacuums: core.ImmutableDictionary[pyreach.Vacuum]
  _vacuum: Optional[pyreach.Vacuum]
  _vncs: core.ImmutableDictionary[vnc.VNC]
  _vnc: Optional[vnc.VNC]
  _oracles: core.ImmutableDictionary[pyreach.Oracle]
  _oracle: Optional[pyreach.Oracle]
  _logger: pyreach.Logger
  _playback: Optional[Playback]
  _metrics: pyreach.Metrics
  _text_instructions: pyreach.TextInstructions
  _arm_devices: List[arm_impl.ArmDevice]

  def __init__(
      self,
      client: cli.Client,
      arm_types: Optional[Dict[str, str]] = None,
      enable_streaming: bool = True,
      take_control_at_start: bool = True,
  ) -> None:
    """Initialize the Host.

    Args:
      client: Connection to the client.
      arm_types: Overrides for arm types.
      enable_streaming: If True, automatically start streaming for Arm,
        ColorCamera and DepthCamera devices.
      take_control_at_start: If True, immediately take control.

    Raises:
      Exception: when failed to load config.

    """
    is_playback = isinstance(client, cli.PlaybackClient)

    # Load config
    self._config = ConfigImpl()
    self._arm_devices = []

    # Read the initial key-value requests:
    msgs: List[Optional[types_gen.DeviceData]] = []
    request_kv: Dict[device_base.KeyValueKey, Optional[float]] = {
        device_base.KeyValueKey(
            device_type="settings-engine",
            device_name="",
            key="workcell_io.json"):
            None,
        device_base.KeyValueKey(
            device_type="settings-engine",
            device_name="",
            key="calibration.json"):
            None,
        device_base.KeyValueKey(
            device_type="settings-engine", device_name="", key="robot-name"):
            None,
        device_base.KeyValueKey(
            device_type="settings-engine", device_name="", key="display-name"):
            None,
    }
    request_description: Optional[float] = None
    block = False
    while request_kv or self._config.machine_interfaces is None:
      if block and not is_playback:
        if request_description is None or time.time() > request_description:
          request_description = time.time() + 15
          client.send_cmd(
              types_gen.CommandData(
                  ts=utils.timestamp_now(),
                  tag=utils.generate_tag(),
                  device_type="discovery-aggregator",
                  data_type="machine-interfaces-request"))
        for kv, timeout in request_kv.items():
          if timeout is None or time.time() > timeout:
            request_kv[kv] = time.time() + 15
            client.send_cmd(
                types_gen.CommandData(
                    ts=utils.timestamp_now(),
                    tag=utils.generate_tag(),
                    device_type=kv.device_type,
                    device_name=kv.device_name,
                    data_type="key-value-request",
                    key=kv.key))
      msg: Optional[types_gen.DeviceData] = None
      if is_playback and block:
        assert isinstance(client, cli.PlaybackClient)
        playback_client: cli.PlaybackClient = client
        playback_client.next_device_data()
      try:
        msg = client.get_queue().get(block=block, timeout=0.1)
        msgs.append(msg)
        if msg is None:
          break
      except queue.Empty:
        block = True
      if msg is not None and msg.data_type == "key-value":
        kv = device_base.KeyValueKey(
            device_type=msg.device_type,
            device_name=msg.device_name,
            key=msg.key)
        self._config._workcell_io.on_set_key_value(kv, msg.value)
        self._config._calibration.on_set_key_value(kv, msg.value)
        if kv in request_kv:
          del request_kv[kv]
      if msg is not None:
        self._config._machine_interfaces._device.on_device_data(msg)

    workcell_io_config = self._config.workcell_io
    current_calibration = self._config.calibration
    interfaces = self._config.machine_interfaces

    def get_arm_type(name: str) -> Optional[arm.ArmType]:
      if arm_types and name in arm_types:
        try:
          return arm_impl.ArmTypeImpl.from_urdf_file(arm_types[name])
        except ValueError:
          logging.warning("Arm type override %s for %s invalid",
                          arm_types[name], name)
      if current_calibration is None:
        logging.warning("Calibration not found and no arm type override for %s",
                        name)
        return None
      robot_dev = current_calibration.get_device("robot", name)
      if robot_dev is None:
        robot_dev = current_calibration.get_device("ur", name)
      if robot_dev is None:
        logging.warning("No calibration device and no arm type override for %s",
                        name)
        return None
      if not isinstance(robot_dev, calibration.CalibrationRobot):
        logging.warning(
            "Non-robot calibration device and no arm type "
            "override for %s", name)
        return None
      cal_robot: calibration.CalibrationRobot = robot_dev
      try:
        return arm_impl.ArmTypeImpl.from_urdf_file(cal_robot.urdf)
      except ValueError:
        logging.warning("Calibation urdf %s for %s invalid", cal_robot.urdf,
                        name)
      return None

    # Build up device list
    devices: List[device_base.DeviceBase] = []

    def add_device(dev: Tuple[device_base.DeviceBase, host.T]) -> host.T:
      devices.append(dev[0])
      return dev[1]

    def add_arm_device(
        dev: Tuple[arm_impl.ArmDevice, device_base.DeviceBase,
                   host.T]) -> host.T:
      devices.append(dev[0])
      devices.append(dev[1])
      self._arm_devices.append(dev[0])
      return dev[2]

    # Load oracles
    oracles = {}
    if interfaces:
      oracle_interfaces = interfaces.get_machine_interfaces_with_type("oracle")
      for oracle_interface in oracle_interfaces:
        if (oracle_interface.interface_type !=
            machine_interfaces.InterfaceType.INFERENCE_REQUEST):
          continue
        if oracle_interface.data_type != "prediction":
          continue
        if oracle_interface.device_name in oracles:
          continue
        oracles[oracle_interface.device_name] = add_device(
            oracle_impl.OracleDevice(
                "oracle", oracle_interface.device_name).get_wrapper())
    self._oracles = core.ImmutableDictionary(oracles)
    self._oracle = self._oracles.get("pick-points", self._oracles.get(""))
    # Load cameras
    color_cameras: Dict[str, pyreach.ColorCamera] = {}
    if interfaces is not None:
      color_interfaces = interfaces.get_machine_interfaces_with_type(
          "color-camera")
      for color_interface in color_interfaces:
        if color_interface.device_name in color_cameras:
          continue
        if color_interface.data_type != "color":
          continue
        if (color_interface.interface_type !=
            machine_interfaces.InterfaceType.FRAME_REQUEST):
          continue
        color_cameras[color_interface.device_name] = add_device(
            color_camera_impl.ColorCameraDevice(
                color_interface.device_type, color_interface.device_name,
                self._config._calibration).get_wrapper())
    self._color_camera = color_cameras.get("")
    self._color_cameras = core.ImmutableDictionary(color_cameras)
    # Load depth cameras
    depth_cameras: Dict[str, pyreach.DepthCamera] = {}
    if interfaces is not None:
      depth_interfaces = interfaces.get_machine_interfaces_with_type(
          "depth-camera")
      for depth_camera_interface in depth_interfaces:
        if depth_camera_interface.device_name in depth_cameras:
          continue
        if depth_camera_interface.data_type != "color-depth":
          continue
        if (depth_camera_interface.interface_type !=
            machine_interfaces.InterfaceType.FRAME_REQUEST):
          continue
        depth_cameras[depth_camera_interface.device_name] = add_device(
            depth_camera_impl.DepthCameraDevice(
                depth_camera_interface.device_type,
                depth_camera_interface.device_name,
                self._config._calibration).get_wrapper())
    self._depth_camera = depth_cameras.get("")
    self._depth_cameras = core.ImmutableDictionary(depth_cameras)
    # Load VNC cameras
    vncs: Dict[str, vnc.VNC] = {}
    if interfaces is not None:
      vnc_interfaces = interfaces.get_machine_interfaces_with_type("vnc")
      for vnc_interface in vnc_interfaces:
        if vnc_interface.device_name in vnc_interfaces:
          continue
        if vnc_interface.data_type not in {"event-pointer", "color"}:
          continue
        if vnc_interface.interface_type not in {
            machine_interfaces.InterfaceType.FRAME_REQUEST,
            machine_interfaces.InterfaceType.POINTER_EVENT
        }:
          continue
        vncs[vnc_interface.device_name] = add_device(
            vnc_impl.VNCDevice(vnc_interface.device_type,
                               vnc_interface.device_name).get_wrapper())
    self._vnc = vncs.get("", vncs.get("vnc"))
    self._vncs = core.ImmutableDictionary(vncs)
    # Load force torque sensors
    force_torque_sensors: Dict[str, force_torque_sensor.ForceTorqueSensor] = {}
    if interfaces is not None:
      force_torque_sensor_interfaces = interfaces.get_machine_interfaces_with_type(
          "force-torque-sensor")
      for force_torque_sensor_interface in force_torque_sensor_interfaces:
        if force_torque_sensor_interface.device_name in force_torque_sensor_interfaces:
          continue
        if force_torque_sensor_interface.data_type != "sensor-state":
          continue
        if force_torque_sensor_interface.interface_type not in {
            machine_interfaces.InterfaceType.FRAME_REQUEST,
            machine_interfaces.InterfaceType.PUBLISH
        }:
          continue
        force_torque_sensors[
            force_torque_sensor_interface.device_name] = add_device(
                force_torque_sensor_impl.ForceTorqueSensorDevice(
                    force_torque_sensor_interface.device_name).get_wrapper())
    self._force_torque_sensor = force_torque_sensors.get("", None)
    self._force_torque_sensors = core.ImmutableDictionary(force_torque_sensors)
    # Load arms
    arms: Dict[str, arm_impl.ArmImpl] = {}
    if interfaces is not None:
      arm_interfaces = interfaces.get_machine_interfaces_with_type("robot")
      support_controllers: Set[str] = set()
      for arm_interface in arm_interfaces:
        # Constant name makes line to long unless shortened via local variable.
        cdr = machine_interfaces.InterfaceType.CONTROLLER_DESCRIPTIONS_REQUEST
        if (arm_interface.data_type == "controller-descriptions" and
            arm_interface.interface_type == cdr and
            arm_interface.device_type == "robot"):
          support_controllers.add(arm_interface.device_name)
      for arm_interface in arm_interfaces:
        if arm_interface.device_name in arms:
          continue
        if arm_interface.data_type != "robot-state":
          continue
        if arm_interface.interface_type not in {
            machine_interfaces.InterfaceType.FRAME_REQUEST,
            machine_interfaces.InterfaceType.PUBLISH,
        }:
          continue
        arm_type = get_arm_type(arm_interface.device_name)
        if arm_type is None:
          continue
        arms[arm_interface.device_name] = add_arm_device(
            arm_impl.ArmDevice(
                arm_type,
                self._config._calibration,
                self._config._actionsets,
                workcell_io_config,
                arm_interface.device_name,
                support_controllers=(arm_interface.device_name
                                     in support_controllers)).get_wrapper())
    self._arms = core.ImmutableDictionary(arms)
    self._arm = arms.get("")
    # Add vacuums
    vacuums: Dict[str, pyreach.Vacuum] = {}
    self._vacuum = None
    for name, arm_for_vacuum in self._arms.items():
      if not arm_for_vacuum.support_vacuum or not interfaces:
        continue
      vacuums[name] = add_device(
          vacuum_impl.VacuumDevice(interfaces, arm_for_vacuum).get_wrapper())
      if arm_for_vacuum == self._arm:
        self._vacuum = vacuums[name]
    self._vacuums = core.ImmutableDictionary(vacuums)
    # Add logger
    self._logger = add_device(logger_impl.LoggerDevice().get_wrapper())
    # Add client annotation
    self._client_annotation = add_device(
        client_annotation_impl.ClientAnnotationDevice().get_wrapper())
    # Add metrics
    self._metrics = add_device(metrics_impl.MetricDevice().get_wrapper())
    # Add text instruction
    self._text_instructions = add_device(
        text_instruction_impl.TextInstructionDevice().get_wrapper())
    # Add internal
    self._internal = add_device(
        internal_impl.InternalDevice(self._flush, client).get_wrapper())
    # Create host
    self._host = reach_host.ReachHost(
        client,
        devices + self._config._devices,
        initial_messages=msgs,
        take_control_at_start=take_control_at_start)
    self._playback = None
    if is_playback:
      load_internal = self.internal
      assert load_internal is not None
      internal_playback = load_internal.playback
      assert internal_playback is not None
      self._playback = playback_impl.PlaybackImpl(internal_playback, self._host,
                                                  client)

    machine_lock = threading.Lock()

    def machine_callback(
        unused_interfaces: Optional[machine_interfaces.MachineInterfaces]
    ) -> bool:
      with machine_lock:
        self._host.set_machine_interfaces(self._config.machine_interfaces)
      return False

    self._config._machine_interfaces.add_update_callback(machine_callback)
    machine_callback(interfaces)
    self._host.start()
    if enable_streaming and not is_playback:
      self._start_streaming()
    else:
      for t in self._start_arm_read_controller():
        t.join()

  def get_timers(self) -> internal.Timers:  # pylint: disable=unused-argument
    """Return the global timers object."""
    return internal.Internal.get_timers()

  def _start_arm_read_controller(self) -> List[threading.Thread]:

    def arm_read_controllers(load_arm: arm_impl.ArmDevice) -> None:
      while (load_arm.fetch_supported_controllers() is None and
             not self.is_closed()):
        pass

    threads: List[threading.Thread] = []

    for arm_dev in self._arm_devices:
      t = threading.Thread(target=arm_read_controllers, args=(arm_dev,))
      t.start()
      threads.append(t)

    return threads

  def _start_streaming(self) -> None:
    """Start streaming from hosts."""
    # Create a queue for callbacks. In order to start up, we must have all
    # callbacks be called at least once, so that all data is loaded. For
    # example, host.arm.state is guaranteed not to be none if _start_streaming()
    # completes and the host was not closed.
    callback_queue: "queue.Queue[bool]" = queue.Queue()
    request_count = 0

    # Create new callback by first incrementing the callback_count, and then
    # returning a callback function.
    def new_callback() -> Callable[[Optional[Any]], bool]:
      nonlocal request_count, callback_queue
      request_count += 1

      # The callback function will wait for a state (e.g. arm state) and then
      # return True, stopping it from getting called again.
      def cb_func(input_state: Optional[Any]) -> bool:
        nonlocal callback_queue
        if input_state is not None:
          callback_queue.put(True)
          return True
        return False

      return cb_func

    for _, v1 in self._arms.items():
      v1.start_streaming()
      v1.add_update_callback(new_callback())

    threads = self._start_arm_read_controller()

    for _, v2 in self._color_cameras.items():
      v2.start_streaming()
      v2.add_update_callback(new_callback())

    for _, v3 in self._depth_cameras.items():
      v3.start_streaming()
      v3.add_update_callback(new_callback())

    for _, v4 in self._force_torque_sensors.items():
      v4.start_streaming()
      v4.add_update_callback(new_callback())

    for _, v5 in self._vacuums.items():
      v5.start_streaming()
      v5.add_state_callback(new_callback())
      if v5.support_blowoff:
        v5.start_blowoff_streaming()
        v5.add_blowoff_state_callback(new_callback())
      if v5.support_gauge:
        v5.start_gauge_streaming()
        v5.add_gauge_state_callback(new_callback())
      if v5.support_pressure:
        v5.start_pressure_streaming()
        v5.add_pressure_state_callback(new_callback())

    # Wait for all the callbacks to respond.
    callback_count = 0
    while callback_count < request_count and not self.is_closed():
      try:
        if callback_queue.get(block=True, timeout=0.01):
          callback_count += 1
      except queue.Empty:
        pass
    for t in threads:
      t.join()

  def __enter__(self) -> "pyreach.Host":
    """With statement entry dunder."""
    return self

  def __exit__(self, typ: Any, value: Any, traceback: Any) -> None:
    """With statement exit dunder."""
    self.close()

  def close(self) -> None:
    """Close the connection to the host."""
    self._host.close()

  def wait(self) -> None:
    """Wait for the host to close."""
    self._host.wait()

  def is_closed(self) -> bool:
    """Determine if the host is closed."""
    return self._host.is_closed()

  def reset(self) -> None:
    """Reset the host."""
    if self._arm:
      self._arm.reset_sim()

  def _flush(self) -> None:
    """Flush the data queues."""
    self._host.flush()

  @property
  def config(self) -> host.Config:
    """Return the config dictionary."""
    return self._config

  @property
  def client_annotation(self) -> client_annotation.ClientAnnotation:
    """Return the client annotation device."""
    return self._client_annotation

  @property
  def color_cameras(self) -> core.ImmutableDictionary[pyreach.ColorCamera]:
    """Return all the color cameras connected to the system.

    The key of the dictionary is the device name, such as "front" or "overview".
    """
    return self._color_cameras

  @property
  def color_camera(self) -> Optional[pyreach.ColorCamera]:
    """Return the color camera if there is just one.

    None if there is no color camera or multiple color cameras.
    """
    return self._color_camera

  @property
  def depth_cameras(self) -> core.ImmutableDictionary[pyreach.DepthCamera]:
    """Return all the depth cameras connected to the system.

    The key of the dictionary is the device name, such as "top" or "side".
    """
    return self._depth_cameras

  @property
  def depth_camera(self) -> Optional[pyreach.DepthCamera]:
    """Return the depth camera if there is just one.

    None if there is no depth camera or multiple depth cameras.
    """
    return self._depth_camera

  @property
  def arms(self) -> core.ImmutableDictionary[pyreach.Arm]:
    """Return all the robot arms connected to the system.

    The key of the dictionary is the device name, such as "left" or "right".
    """
    return self._arms  # type: ignore

  @property
  def arm(self) -> Optional[pyreach.Arm]:
    """Return the robot arm if there is just one.

    None if there is no robot arm or multiple robot arms.
    """
    return self._arm

  @property
  def vacuums(self) -> core.ImmutableDictionary[pyreach.Vacuum]:
    """Return all the vacuum devices connected to the system.

    The key of the dictionary is the device name.
    """
    return self._vacuums

  @property
  def vacuum(self) -> Optional[pyreach.Vacuum]:
    """Return the vacuum device if there is just one.

    None if there is no vacuum device or multiple vacuum devices.
    """
    return self._vacuum

  @property
  def vncs(self) -> core.ImmutableDictionary[pyreach.VNC]:
    """Return all the VNC devices connected to the system.

    The key of the dictionary is the device name.
    """
    return self._vncs

  @property
  def vnc(self) -> Optional[pyreach.VNC]:
    """Return the VNC device if there is just one.

    None if there is no VNC device.
    """
    return self._vnc

  @property
  def oracles(self) -> core.ImmutableDictionary[pyreach.Oracle]:
    """Return all the oracle devices connected to the system.

    The key of the dictionary is the device name.
    """
    return self._oracles

  @property
  def oracle(self) -> Optional[pyreach.Oracle]:
    """Return the oracle device if there is just one.

    None if there is no oracle device or multiple oracle devices.
    """
    return self._oracle

  @property
  def force_torque_sensors(
      self) -> core.ImmutableDictionary[force_torque_sensor.ForceTorqueSensor]:
    """Return all the force torque sensors connected to the system.

    The key of the dictionary is the device name.
    """
    return self._force_torque_sensors

  @property
  def force_torque_sensor(
      self) -> Optional[force_torque_sensor.ForceTorqueSensor]:
    """Return the default force torque sensor.

    None if there is no force torque sensor device or the default sensor.
    """
    return self._force_torque_sensor

  @property
  def internal(self) -> Optional[internal.Internal]:
    """Access PyReach internal APIs."""
    return self._internal

  @property
  def logger(self) -> pyreach.Logger:
    """Return the Logger object."""
    return self._logger

  @property
  def playback(self) -> Optional[Playback]:
    """Return the playback object."""
    return self._playback

  @property
  def metrics(self) -> pyreach.Metrics:
    """Return the Metrics object."""
    return self._metrics

  @property
  def text_instructions(self) -> pyreach.TextInstructions:
    """Access TextInstructions object."""
    return self._text_instructions

  def get_ping_time(self) -> Optional[float]:
    """Return the latest ping time.

    Returns:
      Returns the latest ping time or None if no ping time is available.

    """
    return self._host.get_ping_time()

  def get_server_offset_time(self) -> Optional[float]:
    """Return the offset to the server time.

    Returns:
      The offset to the server-side time, or None if it could not be computed.
    """
    return self._host.get_server_offset_time()

  def set_should_take_control(self,
                              should_take_control: bool,
                              should_release_control: bool = False) -> None:
    """Set the should take control flag.

    Args:
      should_take_control: If true, will try to start a control session.
      should_release_control: If true, will force release of control session.
    """
    self._host.set_should_take_control(should_take_control,
                                       should_release_control)

  def wait_for_control(self, timeout: Optional[float] = None) -> bool:
    """Wait until the session becomes active.

    Args:
      timeout: timeout for time to wait for state.

    Returns:
      True if have taken control, false otherwise.
    """
    return self._host.wait_for_control(timeout=timeout)

  def wait_for_session_state(self,
                             state: host.SessionState,
                             timeout: Optional[float] = None) -> bool:
    """Wait for a specific session state.

    Args:
      state: the state to wait for.
      timeout: timeout for time to wait for state.

    Returns:
      True if have entered the state, false otherwise.
    """
    return self._host.wait_for_session_state(state, timeout=timeout)

  def get_session_state(self) -> host.SessionState:
    """Get the session state of the host.

    Returns:
      The session state.
    """
    return self._host.get_session_state()

  def add_session_state_callback(
      self,
      callback: Callable[[host.SessionState], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback when new a session state is received.

    Args:
      callback: triggers when new a session state is received.
      finished_callback: triggers when update is finished.

    Returns:
      Returns a function when called stops the callback.
    """
    return self._host.add_session_state_callback(callback, finished_callback)

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
    return self._host.add_host_id_callback(callback, finished_callback)

  @property
  def host_id(self) -> Optional[str]:
    """Name gets the current host id of the robot.

    Returns:
      The current id of the host, or none if it is not loaded.
    """
    return self._host.host_id

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
    return self._host.add_display_name_callback(callback, finished_callback)

  @property
  def display_name(self) -> Optional[str]:
    """Name gets the current display name of the robot.

    Returns:
      The current display name of the robot, or none if it is not loaded.
    """
    return self._host.display_name
