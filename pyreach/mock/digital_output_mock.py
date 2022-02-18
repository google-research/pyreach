"""Digital output API."""

import collections
from typing import Callable, Iterable, Tuple, Optional
from pyreach import core
from pyreach import digital_output

DigOutState = digital_output.DigitalOutputState
DigOutPinState = digital_output.DigitalOutputPinState


class DigitalOutputMock(digital_output.DigitalOutput):
  """Class for interacting with a digital output."""

  def __init__(self) -> None:
    """Initialize DigitalOutputMock."""
    super().__init__()
    self.pin_states: collections.OrderedDict[str, DigOutPinState] = (
        collections.OrderedDict())
    self.sequence: int = 0
    self.timestamp: float = 1.0
    self.mock_set_pin_state("pin_name", False)

  def mock_set_pin_state(self, pin_name: str, value: Optional[bool]) -> None:
    """Set the state of a gym pin name for DigitalOutputMock."""
    assert value is None or isinstance(value, bool), value
    pin_state: DigOutPinState = DigOutPinState(pin_name, value)
    self.sequence += 1
    self.timestamp += 1.0
    self.pin_states[pin_name] = pin_state

  @property
  def type(self) -> str:
    """Get the capability type."""
    raise NotImplementedError

  @property
  def name(self) -> str:
    """Get the capability name."""
    raise NotImplementedError

  @property
  def robot_name(self) -> str:
    """Get the name of the robot hosting the capability."""
    raise NotImplementedError

  @property
  def pins(self) -> Tuple[str, ...]:
    """Get the tuple of pin names for this capability."""
    raise NotImplementedError

  @property
  def state(self) -> Optional[digital_output.DigitalOutputState]:
    """Get the state of the digital output."""
    robot_name: str = "arm"
    pin_states: Tuple[DigOutPinState, ...] = tuple(self.pin_states.values())
    output_state: digital_output.DigitalOutputState = (
        digital_output.DigitalOutputState(self.timestamp, self.sequence,
                                          "capability_type", "pin_name",
                                          robot_name, pin_states))
    self.timestamp += 1.0
    self.sequence += 1
    return output_state

  def start_streaming(self, request_period: float = 0.1) -> None:
    """Start streaming of capability states.

    Args:
      request_period: The number of seconds between frames. Defaults to .1
        second between states.
    """

  def stop_streaming(self) -> None:
    """Stop streaming capability states."""
    raise NotImplementedError

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
    raise NotImplementedError

  def fetch_state(self, timeout: float = 15.0) -> Optional[DigOutState]:
    """Fetch a state or possibly times out.

    Args:
      timeout: The optional amount of time to wait for a capability state. If
        not specified, 15 seconds is the default timeout.

    Returns:
      Returns the capability state or None for a timeout.

    """
    pin_states: Tuple[DigOutPinState, ...] = tuple(self.pin_states.values())
    timestamp: float = self.timestamp
    self.timestamp += 1.0
    sequence: int = self.sequence
    self.sequence += 1
    capability_type: str = "capability_type"
    capability_name: str = "capability_name"  # Not capability_type.
    robot_name: str = "robot_name"
    digital_output_state: DigOutState = DigOutState(timestamp, sequence,
                                                    capability_type,
                                                    capability_name, robot_name,
                                                    pin_states)
    return digital_output_state

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
    raise NotImplementedError

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
    raise NotImplementedError

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
    assert pin_name and isinstance(state, bool)
    self.mock_set_pin_state(pin_name, state)

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
    raise NotImplementedError

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
    value: bool
    pin_name: str
    for pin_name, value in states:
      self.mock_set_pin_state(pin_name, value)
