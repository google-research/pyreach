"""Implementation of the run_script commands."""

from typing import Callable, Optional, Sequence, Tuple

from pyreach import core
from pyreach import run_script
from pyreach.common.python import types_gen
from pyreach.impl import requester
from pyreach.impl import thread_util
from pyreach.impl import utils


class RunScriptDevice(requester.Requester[core.PyReachStatus]):
  """RunScriptDevice is a device for the run-script node."""

  def get_wrapper(self) -> Tuple["RunScriptDevice", "RunScriptWrapper"]:
    """Return the Device and Wrapper."""
    return self, RunScriptWrapper(self)

  def send_script(
      self, cmd: str, args: Sequence[str], timeout: Optional[float],
      callback: Optional[Callable[[core.PyReachStatus], None]],
      finished_callback: Optional[Callable[[], None]]) -> core.PyReachStatus:
    """Run a script on the reach host.

    Arguments:
      cmd: The name of the script command to run.
      args: The name of and arguments to the script executable.
      timeout: The timeout to wait for the script to complete.
      callback: An optional callback routine call upon completion.
      finished_callback: An optional callback when done.

    Returns:
      The status of the call.
    """
    q = self.send_tagged_request(
        types_gen.CommandData(
            ts=utils.timestamp_now(),
            tag=utils.generate_tag(),
            device_type="delegated-client",
            device_name="run-script",
            data_type="run-script",
            cmd=cmd,
            args=list(args)),
        timeout=timeout)
    if callback or finished_callback:

      def filter_cb(
          msg: Tuple[types_gen.DeviceData,
                     Optional[core.PyReachStatus]]) -> None:
        status = msg[1]
        if status and callback:
          callback(status)

      def filter_fcb() -> None:
        if finished_callback:
          finished_callback()

      self.queue_to_callback(q, filter_cb, filter_fcb)
      return core.PyReachStatus(
          utils.timestamp_now(), status="rejected", error="internal")

    msgs = thread_util.extract_all_from_queue(q)
    if not msgs:
      return core.PyReachStatus(
          utils.timestamp_now(), status="done", error="timeout")
    status = msgs[len(msgs) - 1][1]
    if not status:
      return core.PyReachStatus(
          utils.timestamp_now(), status="done", error="timeout")
    return status

  def get_message_supplement(
      self, msg: types_gen.DeviceData) -> Optional[core.PyReachStatus]:
    """Get additional message."""
    if (msg.device_type == "delegated-client" and
        msg.device_name == "run-script" and msg.data_type == "cmd-status"):
      return utils.pyreach_status_from_message(msg)
    return None


class RunScriptWrapper(run_script.RunScript):
  """Interface for running script executables on the host side."""

  def __init__(self, device: RunScriptDevice) -> None:
    """Construct a RunScriptWrapper."""
    super().__init__()
    self._device = device

  def run_script(self,
                 name: str,
                 args: Sequence[str],
                 timeout: Optional[float] = None) -> core.PyReachStatus:
    """Run a script on the reach host.

    Args:
      name: The name of the script executable to run.
      args: The arguments to the script executable.
      timeout: The timeout to wait for the script to complete.

    Returns:
      The status of the call.
    """
    argv = [name]
    argv.extend(args)
    return self._device.send_script("run-script", argv, timeout, None, None)

  def async_run_script(
      self,
      name: str,
      args: Sequence[str],
      timeout: Optional[float] = None,
      callback: Optional[Callable[[core.PyReachStatus], None]] = None,
      finished_callback: Optional[Callable[[], None]] = None) -> None:
    """Run a script on the reach host.

    Arguments:
      name: The name of the script executable to run.
      args: The arguments to the script executable.
      timeout: The timeout to wait for the script to complete.
      callback: An optional callback routine call upon completion.
      finished_callback: An optional callback when done.
    """
    if finished_callback is None:

      def cb() -> None:
        pass

      finished_callback = cb
    argv = [name]
    argv.extend(args)
    self._device.send_script("run-script", argv, timeout, callback,
                             finished_callback)

  def cancel(self, timeout: Optional[float] = None) -> core.PyReachStatus:
    """Cancels any running script on the host.

    Args:
      timeout: The timeout to wait for the script to complete.

    Returns:
      The status of the call.
    """
    return self._device.send_script("cancel", [], timeout, None, None)

  def async_cancel(
      self,
      timeout: Optional[float] = None,
      callback: Optional[Callable[[core.PyReachStatus], None]] = None,
      finished_callback: Optional[Callable[[], None]] = None) -> None:
    """Cancels any running script on the host.

    Arguments:
      timeout: The timeout to wait for the script to complete.
      callback: An optional callback routine call upon completion.
      finished_callback: An optional callback when done.
    """
    if finished_callback is None:

      def cb() -> None:
        pass

      finished_callback = cb
    self._device.send_script("cancel", [], timeout, callback, finished_callback)
