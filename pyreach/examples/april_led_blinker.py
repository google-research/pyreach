"""Blink the april-led on and off."""

import time
from typing import List

from absl import app  # type: ignore
from absl import flags  # type: ignore
from pyreach.factory import ConnectionFactory


def main(unused_argv: List[str]) -> None:
  with ConnectionFactory(
      connection_string=flags.FLAGS.connection_string,
      enable_streaming=False,
      robot_types={
          "april-led": "april-led.urdf"
      }).connect() as host:
    april_led = host.arms.get("april-led")
    assert april_led
    digital_outputs = april_led.digital_outputs
    assert digital_outputs
    digital_outputs_by_type = digital_outputs.get("april-led")
    assert digital_outputs_by_type
    output = digital_outputs_by_type.get("")
    assert output
    led_state = False
    while not host.is_closed():
      print("Set led state", led_state)
      output.set_pin_state("", led_state)
      while not host.is_closed():
        state = output.fetch_state()
        if not state:
          return
        pin_state = state.get_pin_state("")
        if pin_state and pin_state.state == led_state:
          break
      time.sleep(5.0)
      led_state = not led_state


if __name__ == "__main__":
  flags.DEFINE_string(
      "connection_string", "", "Connect using a PyReach connection string (see "
      "connection_string.md for examples and documentation).")
  app.run(main)
