"""Moves a robot around with a spacemouse."""

from typing import Sequence

from absl import app  # type: ignore
from absl import flags  # type: ignore
from absl import logging  # type: ignore

from pyreach.factory import LocalTCPHostFactory
from pyreach.tools.lib.spacemouse_mover_lib import SpacemouseMover


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")
  logging.info("Connecting to local reach....")
  with LocalTCPHostFactory().connect() as host:
    logging.info("Connected")
    mover = SpacemouseMover(host, flags.FLAGS.task_code)
    mover.run()


if __name__ == "__main__":
  flags.DEFINE_string("task_code", "9999", "Task code for start/end task")
  app.run(main)
