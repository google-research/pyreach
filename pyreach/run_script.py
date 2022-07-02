"""Implements a script for controlling current running script."""

from typing import Callable, Sequence, Optional

from pyreach.core import PyReachStatus


class RunScript(object):
  """Interface for running script executables on the host side."""

  def run_script(self,
                 name: str,
                 args: Sequence[str],
                 timeout: Optional[float] = None) -> PyReachStatus:
    """Run a script on the reach host.

    Arguments:
      name: The name of the script executable to run.
      args: The arguments to the script executable.
      timeout: The timeout to wait for the script to complete.

    Returns:
      The status of the call.
    """
    raise NotImplementedError

  def async_run_script(
      self,
      name: str,
      args: Sequence[str],
      timeout: Optional[float] = None,
      callback: Optional[Callable[[PyReachStatus], None]] = None,
      finished_callback: Optional[Callable[[], None]] = None) -> None:
    """Run a script on the reach host.

    Arguments:
      name: The name of the script executable to run.
      args: The arguments to the script executable.
      timeout: The timeout to wait for the script to complete.
      callback: An optional callback routine call upon completion.
      finished_callback: An optional callback when done.
    """
    raise NotImplementedError

  def cancel(self, timeout: Optional[float] = None) -> PyReachStatus:
    """Cancels any running script on the host.

    Arguments:
      timeout: The timeout to wait for the script to complete.

    Returns:
      The status of the call.
    """
    raise NotImplementedError

  def async_cancel(
      self,
      timeout: Optional[float] = None,
      callback: Optional[Callable[[PyReachStatus], None]] = None,
      finished_callback: Optional[Callable[[], None]] = None) -> None:
    """Cancels any running script on the host.

    Arguments:
      timeout: The timeout to wait for the script to complete.
      callback: An optional callback routine call upon completion.
      finished_callback: An optional callback when done.
    """
    raise NotImplementedError
