"""Tests for instruction_generator."""

import unittest

from pyreach.gyms.envs import instruction_generator


class InstructionGeneratorTest(unittest.TestCase):

  def test_generates_instruction(self) -> None:
    gen = instruction_generator.InstructionGeneratorBlock8()
    self.assertIsNotNone(gen.generate_instruction())


if __name__ == '__main__':
  unittest.main()
