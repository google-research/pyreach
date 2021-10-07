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

from pyreach import client_annotation
from pyreach.mock import client_annotation_mock


class TestClientAnnotationMock(unittest.TestCase):
  """Test the TextInstructionsMock."""

  def test_logger(self) -> None:
    """Test the MockLogger."""
    mock_client_annotation: client_annotation_mock.ClientAnnotationMock
    mock_client_annotation = client_annotation_mock.ClientAnnotationMock()
    assert isinstance(mock_client_annotation,
                      client_annotation_mock.ClientAnnotationMock)
    assert isinstance(mock_client_annotation,
                      client_annotation.ClientAnnotation)


if __name__ == "__main__":
  unittest.main()
