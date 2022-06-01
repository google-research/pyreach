"""Moves a robot around with a spacemouse, with some logging annotations."""

from typing import Sequence

from absl import app  # type: ignore
from absl import flags  # type: ignore
from absl import logging  # type: ignore

from pyreach.common.proto_gen import logs_pb2
from pyreach.factory import LocalTCPHostFactory
from pyreach.tools.lib.spacemouse_mover_lib import SpacemouseMover


class App(SpacemouseMover):
  """An app that is a SpacemouseMover that inserts annotations in the log."""

  def handle_keyboard_command(self, cmd: str) -> bool:
    """Handles keyboard commands other than 'x'.

    Args:
      cmd: The keyboard command

    Returns:
      True to exit, False to continue.
    """
    logging.info("Handling an overridden keyboard command")
    if cmd == "r":  # reset
      annotation = logs_pb2.ClientAnnotation()
      annotation.text_annotation.category = "segment"
      annotation.text_annotation.text = "reset"
      self.host.client_annotation.async_annotate(annotation)
      print("OK, moving the arm out of the way.")
      self.reset()

    elif cmd == "i":  # give Instruction
      annotation = logs_pb2.ClientAnnotation()
      annotation.text_annotation.category = "segment"
      annotation.text_annotation.text = "instruction"
      self.host.client_annotation.async_annotate(annotation)
      print("OK, move the block to the nearest corner.")

    elif cmd == "d":  # done
      annotation = logs_pb2.ClientAnnotation()
      annotation.text_annotation.category = "segment"
      annotation.text_annotation.text = "done"
      self.host.client_annotation.async_annotate(annotation)
      print("OK, you did it!")

    return False


def main(argv: Sequence[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")
  logging.info("Connecting to local reach....")
  with LocalTCPHostFactory().connect() as host:
    logging.info("Connected")
    mover = App(host, flags.FLAGS.task_code)
    mover.run()


if __name__ == "__main__":
  flags.DEFINE_string("task_code", "9999", "Task code for start/end task")
  app.run(main)
