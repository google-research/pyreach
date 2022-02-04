"""Implementation of the digital output API."""

import logging  # type: ignore
import queue  # pylint: disable=unused-import
from typing import Callable, Iterable, List, Optional, Set, Tuple

from pyreach import core
from pyreach import digital_output
from pyreach.common.python import types_gen
from pyreach.impl import requester
from pyreach.impl import thread_util
from pyreach.impl import utils


class DigitalOutputDevice(requester.Requester[digital_output.DigitalOutputState]
                         ):
  """DigitalOutputDevice interacts with a digital output capability."""
  _type: str
  _name: str
  _robot_name: str
  _pins: Tuple[str, ...]
  _pins_set: Set[str]
  _fused_pins: bool

  def __init__(self, capability_type: str, name: str, robot_name: str,
               pins: Tuple[str, ...], fused_pins: bool) -> None:
    """Initialize the DigitalOutput object.

    Args:
      capability_type: the capability type.
      name: the capability name.
      robot_name: the capability robot name.
      pins: the capability pins.
      fused_pins: true if the capability uses fused pins.
    """
    super().__init__()
    self._type = capability_type
    self._name = name
    self._robot_name = robot_name
    self._pins = pins
    self._pins_set = set(pins)
    self._fused_pins = fused_pins

  @property
  def type(self) -> str:
    """Get the capability type."""
    return self._type

  @property
  def name(self) -> str:
    """Get the capability name."""
    return self._name

  @property
  def robot_name(self) -> str:
    """Get the name of the robot hosting the capability."""
    return self._robot_name

  @property
  def pins(self) -> Tuple[str, ...]:
    """Get the tuple of pin names for this capability."""
    return ("",) if self._fused_pins else self._pins

  def get_message_supplement(
      self,
      msg: types_gen.DeviceData) -> Optional[digital_output.DigitalOutputState]:
    """Get getting supplementary information for the request manager.

    Args:
      msg: device data message.

    Returns:
      Converted DigitalOutputState object.
    """
    if (self._type == msg.device_type and self._name == msg.device_name and
        msg.data_type == "output-state"):
      state: List[digital_output.DigitalOutputPinState] = []
      if msg.state:
        for msg_state in msg.state:
          if msg_state.pin not in self._pins_set and not self._fused_pins:
            logging.warning(
                "Extra pin '%s' in capability type '%s' name '%s' for '%s'",
                msg_state.pin, self._type, self._name, self._robot_name)
            continue
          if self._fused_pins and msg_state.pin:
            logging.warning(
                "Non-empty fused-state pin '%s' in capability type '%s' name "
                "'%s' for '%s'", msg_state.pin, self._type, self._name,
                self._robot_name)
            continue
          value: Optional[bool] = None
          if msg_state.int_value == 1:
            value = True
          elif msg_state.int_value == 0:
            value = False
          state.append(
              digital_output.DigitalOutputPinState(msg_state.pin, value))
      return digital_output.DigitalOutputState(
          time=utils.time_at_timestamp(msg.ts),
          sequence=msg.seq,
          type=self._type,
          name=self._name,
          robot_name=self._robot_name,
          pin_states=tuple(state))
    return None

  def set_pin_states(
      self, states: Iterable[Tuple[str, bool]], intent: str, pick_id: str,
      success_type: str, preemptive: bool, timeout: Optional[float]
  ) -> ("queue.Queue[Optional[Tuple["
        "types_gen.DeviceData, Optional[digital_output.DigitalOutputState]]]]"):
    """Set the state of an output pin.

    Args:
      states: The states (name, state) to set the pins.
      intent: The intent of the command.
      pick_id: The pick_id of the command.
      success_type: The success_type of the command.
      preemptive: True to preempt existing scripts.
      timeout: the timeout for the call, defaults to no timeout.

    Raises:
      PyReachError: if a pin name is invalid or if no pins specified.

    Returns:
      A queue of response data for the command.
    """
    args: List[types_gen.CapabilityState] = []
    if not states:
      raise core.PyReachError("No pins specified")
    if self._fused_pins:
      states = list(states)
      if len(states) != 1 or states[0][0]:
        raise core.PyReachError(
            ("Must specify only a single pin with name '' "
             "for fused pin capability type '%s' name '%s' for robot '%s'") %
            (self.type, self.name, self.robot_name))
      for pin_name in self._pins:
        args.append(
            types_gen.CapabilityState(
                pin=pin_name, int_value=int(states[0][0])))
    else:
      for pin_name, state in states:
        if pin_name not in self._pins_set:
          raise core.PyReachError(
              ("Pin '%s' is not supported by digital output "
               "capability type '%s' name '%s' for robot '%s'") %
              (pin_name, self.type, self.name, self.robot_name))
        args.append(
            types_gen.CapabilityState(pin=pin_name, int_value=int(state)))
    tag = utils.generate_tag()
    script = types_gen.CommandData(
        ts=utils.timestamp_now(),
        device_type="robot",
        device_name=self.robot_name,
        data_type="reach-script",
        pick_id=pick_id,
        intent=intent,
        success_type=success_type,
        tag=tag,
        reach_script=types_gen.ReachScript(
            preemptive=preemptive,
            version=0,
            commands=[
                types_gen.ReachScriptCommand(
                    set_output=types_gen.SetOutput(
                        py_type=self.type, name=self.name, args=args))
            ],
            calibration_requirement=types_gen.ReachScriptCalibrationRequirement(
                allow_uncalibrated=True)))
    return self.send_tagged_request(script, timeout=timeout)

  def get_wrapper(self) -> Tuple["DigitalOutputDevice", "DigitalOutputImpl"]:
    """Return the Device and Wrapper."""
    return (self, DigitalOutputImpl(self))


class DigitalOutputImpl(digital_output.DigitalOutput):
  """DigitalOutputImpl interacts with a digital output capability."""
  _device: DigitalOutputDevice

  def __init__(self, device: DigitalOutputDevice) -> None:
    """Initialize the DigitalOutputImpl object.

    Args:
      device: The device.
    """
    self._device = device

  @property
  def type(self) -> str:
    """Get the capability type."""
    return self._device.type

  @property
  def name(self) -> str:
    """Get the capability name."""
    return self._device.name

  @property
  def robot_name(self) -> str:
    """Get the name of the robot hosting the capability."""
    return self._device.robot_name

  @property
  def pins(self) -> Tuple[str, ...]:
    """Get the tuple of pin names for this capability."""
    return self._device.pins

  @property
  def state(self) -> Optional[digital_output.DigitalOutputState]:
    """Get the state of the digital output."""
    return self._device.get_cached()

  def start_streaming(self, request_period: float = 0.1) -> None:
    """Start streaming of capability states.

    Args:
      request_period: The number of seconds between frames. Defaults to .1
        second between states.
    """
    self._device.set_untagged_request_period(self.type, self.name,
                                             "output-state", request_period)

  def stop_streaming(self) -> None:
    """Stop streaming capability states."""
    self._device.set_untagged_request_period(self.type, self.name,
                                             "output-state", None)

  def add_state_callback(
      self,
      callback: Callable[[digital_output.DigitalOutputState], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a callback for capability states.

    Args:
      callback: Callback called when a capability state arrives. If it returns
        True, the callback will be stopped.
      finished_callback: Optional callback, called when the callback is stopped
        or if the capability state monitor is closed.

    Returns:
      A function that when called stops the callback.
    """
    return self._device.add_update_callback(callback, finished_callback)

  def fetch_state(
      self,
      timeout: float = 15.0) -> Optional[digital_output.DigitalOutputState]:
    """Fetch a state or possibly times out.

    Args:
      timeout: The optional amount of time to wait for a capability state. If
        not specified, 15 seconds is the default timeout.

    Returns:
      Returns the capability state or None for a timeout.

    """
    q = self._device.request_untagged(
        self.type, self.name, data_type="output-state", timeout=timeout)
    msgs = thread_util.extract_all_from_queue(q)
    if not msgs:
      return None
    if len(msgs) != 1:
      logging.warning("too much data returned for state")
    return msgs[0][1]

  def async_fetch_state(self,
                        callback: Optional[Callable[
                            [digital_output.DigitalOutputState], None]] = None,
                        error_callback: Optional[Callable[[core.PyReachStatus],
                                                          None]] = None,
                        timeout: float = 30) -> None:
    """Fetch a state asynchronously.

    The callback function will be invoked when new capability state is
    available.

    Args:
      callback: A callback function that is called when a capability state
        arrives. If the camera fails to load an capability state, the callback
        is not called.
      error_callback: Optional callback that is called if there is an error.
      timeout: Timeout for the fetch, defaults to 30 seconds.
    """
    q = self._device.request_untagged(
        self.type, self.name, data_type="output-state", timeout=timeout)
    self._device.queue_to_error_callback(q, callback, error_callback)

  def set_pin_state(self,
                    pin_name: str,
                    state: bool,
                    intent: str = "",
                    pick_id: str = "",
                    success_type: str = "",
                    preemptive: bool = True,
                    timeout: Optional[float] = None) -> core.PyReachStatus:
    """Set the state of an output pin.

    Args:
      pin_name: The name of the pin.
      state: The state to set the pin.
      intent: The intent of the command.
      pick_id: The pick_id of the command.
      success_type: The success_type of the command.
      preemptive: True to preempt existing scripts.
      timeout: the timeout for the call, defaults to no timeout.

    Raises:
      PyReachError: if pin name is invalid.

    Returns:
      Status of the command.

    """
    return self.set_pin_states(((pin_name, state),),
                               intent=intent,
                               pick_id=pick_id,
                               success_type=success_type,
                               preemptive=preemptive,
                               timeout=timeout)

  def async_set_pin_state(
      self,
      pin_name: str,
      state: bool,
      intent: str = "",
      pick_id: str = "",
      success_type: str = "",
      preemptive: bool = True,
      timeout: Optional[float] = None,
      callback: Optional[Callable[[core.PyReachStatus], None]] = None,
      finished_callback: Optional[Callable[[], None]] = None) -> None:
    """Set the state of an output pin, asynchronously.

    Args:
      pin_name: The name of the pin.
      state: The state to set the pin.
      intent: The intent of the command.
      pick_id: The pick_id of the command.
      success_type: The success_type of the command.
      preemptive: True to preempt existing scripts.
      timeout: the timeout for the call, defaults to no timeout.
      callback: callback called with the status response. If the robot does not
        respond, will not be called.
      finished_callback: callback called after operation is completed.

    Raises:
      PyReachError: if pin name is invalid.
    """
    self.async_set_pin_states(((pin_name, state),),
                              intent=intent,
                              pick_id=pick_id,
                              success_type=success_type,
                              preemptive=preemptive,
                              timeout=timeout,
                              callback=callback,
                              finished_callback=finished_callback)

  def set_pin_states(self,
                     states: Iterable[Tuple[str, bool]],
                     intent: str = "",
                     pick_id: str = "",
                     success_type: str = "",
                     preemptive: bool = True,
                     timeout: Optional[float] = None) -> core.PyReachStatus:
    """Set the state of an output pin.

    Args:
      states: The states (name, state) to set the pins.
      intent: The intent of the command.
      pick_id: The pick_id of the command.
      success_type: The success_type of the command.
      preemptive: True to preempt existing scripts.
      timeout: the timeout for the call, defaults to no timeout.

    Raises:
      PyReachError: if pin name is invalid or if no pins specified.

    Returns:
      Status of the command.

    """
    q = self._device.set_pin_states(states, intent, pick_id, success_type,
                                    preemptive, timeout)
    for msg in thread_util.extract_all_from_queue(q):
      if msg[0].data_type == "cmd-status":
        status = utils.pyreach_status_from_message(msg[0])
        if status.is_last_status():
          return status
    return core.PyReachStatus(
        utils.timestamp_now(), status="done", error="timeout")

  def async_set_pin_states(
      self,
      states: Iterable[Tuple[str, bool]],
      intent: str = "",
      pick_id: str = "",
      success_type: str = "",
      preemptive: bool = True,
      timeout: Optional[float] = None,
      callback: Optional[Callable[[core.PyReachStatus], None]] = None,
      finished_callback: Optional[Callable[[], None]] = None) -> None:
    """Set the state of an output pin, asynchronously.

    Args:
      states: The states (name, state) to set the pins.
      intent: The intent of the command.
      pick_id: The pick_id of the command.
      success_type: The success_type of the command.
      preemptive: True to preempt existing scripts.
      timeout: the timeout for the call, defaults to no timeout.
      callback: callback called with the status response. If the robot does not
        respond, will not be called.
      finished_callback: callback called after operation is completed.

    Raises:
      PyReachError: if pin name is invalid or if no pins specified.
    """
    q = self._device.set_pin_states(states, intent, pick_id, success_type,
                                    preemptive, timeout)
    if callback or finished_callback:

      def cb(
          msg: Tuple[types_gen.DeviceData,
                     Optional[digital_output.DigitalOutputState]]
      ) -> None:
        if msg[0].data_type == "cmd-status" and callback is not None:
          callback(utils.pyreach_status_from_message(msg[0]))

      def fcb() -> None:
        if finished_callback is not None:
          finished_callback()

      self._device.queue_to_callback(q, cb, fcb)
