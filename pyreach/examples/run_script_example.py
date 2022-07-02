"""Runs a script on a reach host using run-script.

Arguments:
  -connection_string is the connection string (see connection_string.md)

The first positional argument is the file name of the script to run, the rest
are the command line arguments. Use "--" to avoid conflicts with "-" prefix
arguments to the script. Example:
  python3 run_script_example.py -connection_string=<string> -- name -example

Works as follows:
1. Connects to the robot and gets the run-script node.
2. Cancels any running scripts.
3. Executes a script on the run script node.
4. Reports the error status. Returns an error code if invalid.
"""

import logging
import queue
from typing import Sequence, Optional

from absl import app  # type: ignore
from absl import flags  # type: ignore
from pyreach.core import PyReachError
from pyreach.core import PyReachStatus
from pyreach.factory import ConnectionFactory


def _main(argv: Sequence[str]) -> None:
  """Main method of the program."""
  if len(argv) < 2:
    raise ValueError("Must specify an argument")
  with ConnectionFactory(
      connection_string=flags.FLAGS.connection_string,
      enable_streaming=False).connect() as host:
    run_script = host.run_script
    assert run_script, "Host does not support run-script device and commands."
    logging.info("Cancel running scripts...")
    output = run_script.cancel()
    logging.info("Output: %s", str(output))
    if output.is_error():
      raise PyReachError("Invalid cancel output: " + str(output))
    logging.info("Running script: %s, args %s", str(argv[1]), str(argv[2:]))
    q: queue.Queue[Optional[PyReachStatus]] = queue.Queue()

    def fcb() -> None:
      q.put(None)

    run_script.async_run_script(
        argv[1], argv[2:], callback=q.put, finished_callback=fcb)
    while True:
      status = q.get()
      if status is None:
        break
      logging.info("Output: %s", str(status))
      if status.is_error():
        raise PyReachError("Invalid script output: " + str(output))


if __name__ == "__main__":
  flags.DEFINE_string(
      "connection_string", "", "Connect using a PyReach connection string (see "
      "connection_string.md for examples and documentation).")
  app.run(_main)
