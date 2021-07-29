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

"""Tests for LoggerMock."""

import unittest

from pyreach import text_instruction
from pyreach.mock import text_instructions_mock


class TestTextInstructionsMock(unittest.TestCase):
  """Test the TextInstructionsMock."""

  def test_logger(self) -> None:
    """Test the MockLogger."""
    mock_text_instructions: text_instructions_mock.TextInstructionsMock
    mock_text_instructions = text_instructions_mock.TextInstructionsMock()
    assert isinstance(mock_text_instructions,
                      text_instructions_mock.TextInstructionsMock)
    assert isinstance(mock_text_instructions, text_instruction.TextInstructions)


if __name__ == "__main__":
  unittest.main()
