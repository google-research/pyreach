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

"""Tests for playback_client."""

import json
from typing import Callable, List, Optional, Tuple, TypeVar, Union
import unittest

from pyreach import core
from pyreach.common.python import types_gen
from pyreach.impl import playback_client
from pyreach.impl import test_utils
from pyreach.impl import utils

# Some example (time, sequence) pairs for testing the seek() function for data
# elements that do not actually exist.
_test_invalid_seqs = [
    (0.0, 0),
    (1.0, 0),
    (1.0, 1),
    (2.001, 3),
    (2.0, 2),
    (1.001, None),
    (1.2, None),
    (None, 4),
    (None, 0),
    (0.0, None),
]


class PlaybackClientTest(unittest.TestCase):
  """Implement a test of the playback client and subcomponents.

  Performs a detailed test of the playback client logic by testing each
  component against simulated device-data and command-data logs. In addition,
  there are some re-usable functions for testing implementations of the
  iterators and playback clients.
  """

  def test_client_simulator_empty(self) -> None:
    """Test the client simulator with a log that contains no clients.

    Variant one of four - a completely empty log.
    """
    # Create empty log.
    device_data = TestDeviceDataIterator([])
    command_data = TestCommandDataIterator([])
    device_data.start()
    command_data.start()
    # Client simulator will fail to find a client, since the log is empty.
    self.assertRaises(core.PyReachError, playback_client.ClientSimulator, None,
                      device_data, command_data, True)
    device_data.reset()
    command_data.reset()
    # Client simulator will fail to find the "invalid" client, since the log
    # is empty and contains no clients.
    self.assertRaises(core.PyReachError, playback_client.ClientSimulator,
                      "invalid", device_data, command_data, True)

  def test_client_simulator_empty_no_object(self) -> None:
    """Test the client simulator with a log that contains no clients.

    Variant one of four - a client state data missing the object.
    """
    # Create a log with no clients despite having an empty client state object.
    device_data = TestDeviceDataIterator([
        types_gen.DeviceData(
            device_type="session-manager", data_type="connected-clients")
    ])
    command_data = TestCommandDataIterator([])
    device_data.start()
    command_data.start()
    # Client simulator will fail to find a client, since the log is empty.
    self.assertRaises(core.PyReachError, playback_client.ClientSimulator, None,
                      device_data, command_data, True)
    device_data.reset()
    command_data.reset()
    # Client simulator will fail to find the "invalid" client, since the log
    # is empty and contains no clients.
    self.assertRaises(core.PyReachError, playback_client.ClientSimulator,
                      "invalid", device_data, command_data, True)

  def test_client_simulator_empty_object(self) -> None:
    """Test the client simulator with a log that contains no clients.

    Variant one of four - a client state data with no client list.
    """
    # Create a log with no clients despite having an empty client state object.
    device_data = TestDeviceDataIterator([
        types_gen.DeviceData(
            device_type="session-manager",
            data_type="connected-clients",
            connected_clients=types_gen.ConnectedClients())
    ])
    command_data = TestCommandDataIterator([])
    device_data.start()
    command_data.start()
    # Client simulator will fail to find a client, since the log is empty.
    self.assertRaises(core.PyReachError, playback_client.ClientSimulator, None,
                      device_data, command_data, True)
    device_data.reset()
    command_data.reset()
    # Client simulator will fail to find the "invalid" client, since the log
    # is empty and contains no clients.
    self.assertRaises(core.PyReachError, playback_client.ClientSimulator,
                      "invalid", device_data, command_data, True)

  def test_client_simulator_empty_object_list(self) -> None:
    """Test the client simulator with a log that contains no clients.

    Variant one of four - a client state data with any empty client list.
    """
    # Create a log with no clients despite having an empty client state object.
    device_data = TestDeviceDataIterator([
        types_gen.DeviceData(
            device_type="session-manager",
            data_type="connected-clients",
            connected_clients=types_gen.ConnectedClients([]))
    ])
    command_data = TestCommandDataIterator([])
    device_data.start()
    command_data.start()
    # Client simulator will fail to find a client, since the log is empty.
    self.assertRaises(core.PyReachError, playback_client.ClientSimulator, None,
                      device_data, command_data, True)
    device_data.reset()
    command_data.reset()
    # Client simulator will fail to find the "invalid" client, since the log
    # is empty and contains no clients.
    self.assertRaises(core.PyReachError, playback_client.ClientSimulator,
                      "invalid", device_data, command_data, True)

  def test_client_simulator_find_client(self) -> None:
    """Test the client simulator searching for a client in data."""
    device_data = TestDeviceDataIterator([
        types_gen.DeviceData(
            device_type="session-manager",
            data_type="connected-clients",
            connected_clients=types_gen.ConnectedClients([
                types_gen.ConnectedClient(uid="client-1"),
                types_gen.ConnectedClient(uid="client-2"),
            ]))
    ])
    command_data = TestCommandDataIterator([])
    device_data.start()
    command_data.start()
    # We expect the client simulator to find the first client, which is
    # "client-1" since it appears first in the data.
    sim = playback_client.ClientSimulator(None, device_data, command_data, True)
    self.assertEqual(sim.client_id, "client-1")
    device_data.reset()
    command_data.reset()
    # Failure is expected when searching for the non-existent client.
    self.assertRaises(core.PyReachError, playback_client.ClientSimulator,
                      "invalid", device_data, command_data, True)

  def test_client_simulator_find_client_connected(self) -> None:
    """Test the client simulator search with is_current in data."""
    device_data = TestDeviceDataIterator([
        types_gen.DeviceData(
            device_type="session-manager",
            data_type="connected-clients",
            connected_clients=types_gen.ConnectedClients([
                types_gen.ConnectedClient(uid="client-1"),
                types_gen.ConnectedClient(uid="client-2", is_current=True),
            ]))
    ])
    command_data = TestCommandDataIterator([])
    device_data.start()
    command_data.start()
    # We expect the client simulator to find the first client, which is
    # "client-2" since it has is_current = True in the device data.
    sim = playback_client.ClientSimulator(None, device_data, command_data, True)
    self.assertEqual(sim.client_id, "client-2")
    device_data.reset()
    command_data.reset()
    # Failure is expected when searching for the non-existent client.
    self.assertRaises(core.PyReachError, playback_client.ClientSimulator,
                      "invalid", device_data, command_data, True)

  def test_client_simulator(self) -> None:
    self._test_client_simulator(True)

  def test_client_simulator_client(self) -> None:
    self._test_client_simulator(False)

  def _test_client_simulator(self, allow_client_logs: bool) -> None:
    """Test the filtering logic of the client simulator.

    Args:
      allow_client_logs: simulate logs from the client side.
    """
    # Create a log where there are two test clients, one of which ("client-2")
    # starts and stops.
    device_data = TestDeviceDataIterator([
        types_gen.DeviceData(
            ts=1000,
            seq=1,
            device_type="session-manager",
            data_type="connected-clients",
            connected_clients=types_gen.ConnectedClients([
                types_gen.ConnectedClient(uid="client-1"),
                types_gen.ConnectedClient(uid="client-2", is_current=True),
            ])),
        types_gen.DeviceData(
            ts=10000,
            seq=2,
            device_type="session-manager",
            data_type="connected-clients",
            connected_clients=types_gen.ConnectedClients([
                types_gen.ConnectedClient(uid="client-1"),
            ]))
    ])
    command_data = TestCommandDataIterator([
        types_gen.CommandData(
            device_type="robot",
            data_type="frame-request",
            tag="test-allow",
            origin_client="client-2")
    ])
    device_data.start()
    command_data.start()
    # Test the simulator with client-2
    sim = playback_client.ClientSimulator(None, device_data, command_data,
                                          allow_client_logs)
    self.assertEqual(sim.client_id, "client-2")

    # Data equal test functions that also run the data through the client
    # simulator filter function.
    def same_data(data: types_gen.DeviceData,
                  cmp_data: Optional[types_gen.DeviceData] = None) -> None:
      if not cmp_data:
        cmp_data = utils.copy_device_data(data)
      tf = sim.transform_data(data)
      self.assertIsNotNone(tf)
      assert tf
      log_data_equal(self, tf, cmp_data)

    def same_cmd(cmd: types_gen.CommandData,
                 cmp_cmd: Optional[types_gen.CommandData] = None) -> None:
      if not cmp_cmd:
        cmp_cmd = utils.copy_command_data(cmd)
      tf = sim.transform_command(cmd)
      self.assertIsNotNone(tf)
      assert tf
      log_data_equal(self, tf, cmp_cmd)

    # Test data this is within the client-2 session and will pass through.
    same_data(
        types_gen.DeviceData(
            ts=1000,
            seq=4,
            device_type="robot",
            device_name="",
            data_type="robot-state"))
    same_data(
        types_gen.DeviceData(
            ts=10000,
            seq=4,
            device_type="robot",
            device_name="",
            data_type="robot-state"))
    # Test some data with out-of-bounds timestamps.
    self.assertIsNone(
        sim.transform_data(
            types_gen.DeviceData(
                ts=999,
                seq=4,
                device_type="robot",
                device_name="",
                data_type="robot-state")))
    self.assertIsNone(
        sim.transform_data(
            types_gen.DeviceData(
                ts=10001,
                seq=4,
                device_type="robot",
                device_name="",
                data_type="robot-state")))
    # Data with inhibit_frame_send = True is not allowed through.
    self.assertIsNone(
        sim.transform_data(
            types_gen.DeviceData(
                ts=1000,
                inhibit_frame_send=True,
                seq=4,
                device_type="robot",
                device_name="",
                data_type="robot-state")))
    # Data without the correct send_to_client client ID is not allowed.
    self.assertIsNone(
        sim.transform_data(
            types_gen.DeviceData(
                ts=1000,
                send_to_clients=[
                    types_gen.SendToClient(tag="test", uid="client-1")
                ],
                seq=4,
                device_type="robot",
                device_name="",
                data_type="robot-state")))
    self.assertIsNone(
        sim.transform_data(
            types_gen.DeviceData(
                ts=1000,
                tag="test",
                send_to_clients=[types_gen.SendToClient(uid="client-1")],
                seq=4,
                device_type="robot",
                device_name="",
                data_type="robot-state")))
    # Data with the correct send_to_clients should be allowed and re-tagged.
    # The send_to_clients list is also removed from the data during transform.
    same_data(
        types_gen.DeviceData(
            ts=1,
            tag="",
            send_to_clients=[
                types_gen.SendToClient(tag="test-1", uid="client-1"),
                types_gen.SendToClient(tag="test-2", uid="client-2")
            ],
            seq=4,
            device_type="robot",
            device_name="",
            data_type="robot-state"),
        types_gen.DeviceData(
            ts=1,
            tag="test-2",
            seq=4,
            device_type="robot",
            device_name="",
            data_type="robot-state"))
    same_data(
        types_gen.DeviceData(
            ts=1,
            tag="",
            send_to_clients=[
                types_gen.SendToClient(tag="test-1", uid="client-1"),
                types_gen.SendToClient(tag="test-allow", uid="client-2")
            ],
            seq=4,
            device_type="robot",
            device_name="",
            data_type="robot-state"),
        types_gen.DeviceData(
            ts=1,
            tag="test-allow",
            seq=4,
            device_type="robot",
            device_name="",
            data_type="robot-state"))
    same_data(
        types_gen.DeviceData(
            ts=1,
            tag="test-tag",
            send_to_clients=[
                types_gen.SendToClient(tag="test-1", uid="client-1"),
                types_gen.SendToClient(tag="", uid="client-2")
            ],
            seq=4,
            device_type="robot",
            device_name="",
            data_type="robot-state"),
        types_gen.DeviceData(
            ts=1,
            tag="",
            seq=4,
            device_type="robot",
            device_name="",
            data_type="robot-state"))
    # Data is allowed if its tag was within the sent command data being played
    # back by the server.
    same_data(
        types_gen.DeviceData(
            ts=1,
            tag="test-allow",
            seq=4,
            device_type="robot",
            device_name="",
            data_type="robot-state"))
    # Tag not in command-data, disallowed.
    self.assertIsNone(
        sim.transform_data(
            types_gen.DeviceData(
                ts=1000,
                tag="test-block",
                seq=4,
                device_type="robot",
                device_name="",
                data_type="robot-state")))
    # Test sending connected_clients data. The connected_clients list will be
    # transformed to simulate the client's perspective - is_current will be
    # set on the current client ("client-2"), all others set to false.
    same_data(
        types_gen.DeviceData(
            ts=1000,
            seq=4,
            device_type="session-manager",
            data_type="connected-clients",
            connected_clients=types_gen.ConnectedClients([
                types_gen.ConnectedClient(uid="client-1", is_current=True),
                types_gen.ConnectedClient(uid="client-2"),
            ])),
        types_gen.DeviceData(
            ts=1000,
            seq=4,
            device_type="session-manager",
            data_type="connected-clients",
            connected_clients=types_gen.ConnectedClients([
                types_gen.ConnectedClient(uid="client-1"),
                types_gen.ConnectedClient(uid="client-2", is_current=True),
            ])))
    same_data(
        types_gen.DeviceData(
            ts=1000,
            seq=4,
            device_type="session-manager",
            data_type="connected-clients",
            connected_clients=types_gen.ConnectedClients([
                types_gen.ConnectedClient(uid="client-1"),
                types_gen.ConnectedClient(uid="client-2"),
            ])),
        types_gen.DeviceData(
            ts=1000,
            seq=4,
            device_type="session-manager",
            data_type="connected-clients",
            connected_clients=types_gen.ConnectedClients([
                types_gen.ConnectedClient(uid="client-1"),
                types_gen.ConnectedClient(uid="client-2", is_current=True),
            ])))
    same_data(
        types_gen.DeviceData(
            ts=1000,
            seq=4,
            device_type="session-manager",
            data_type="connected-clients",
            connected_clients=types_gen.ConnectedClients([
                types_gen.ConnectedClient(uid="client-2"),
                types_gen.ConnectedClient(uid="client-1"),
            ])),
        types_gen.DeviceData(
            ts=1000,
            seq=4,
            device_type="session-manager",
            data_type="connected-clients",
            connected_clients=types_gen.ConnectedClients([
                types_gen.ConnectedClient(uid="client-2", is_current=True),
                types_gen.ConnectedClient(uid="client-1"),
            ])))

    # Test the client simulator filtering command-data.
    empty_origin_client_cmds = [
        types_gen.CommandData(
            device_type="robot", data_type="frame-request", tag="test-allow"),
        types_gen.CommandData(
            device_type="robot", data_type="frame-request", tag="test"),
        types_gen.CommandData(
            device_type="robot", data_type="frame-request", tag=""),
    ]
    if allow_client_logs:
      # If client logs are allowed, then empty commands will be allowed
      for cmd in empty_origin_client_cmds:
        same_cmd(cmd)
    else:
      # Empty client logs are not allowed.
      for cmd in empty_origin_client_cmds:
        self.assertIsNone(sim.transform_command(cmd))
    # Commands from the same client should be allowed.
    same_cmd(
        types_gen.CommandData(
            device_type="robot",
            data_type="frame-request",
            tag="test-allow",
            origin_client="client-2"))
    same_cmd(
        types_gen.CommandData(
            device_type="robot",
            data_type="frame-request",
            tag="test",
            origin_client="client-2"))
    same_cmd(
        types_gen.CommandData(
            device_type="robot",
            data_type="frame-request",
            tag="",
            origin_client="client-2"))
    # Commands not from the same client should not be allowed.
    self.assertIsNone(
        sim.transform_command(
            types_gen.CommandData(
                device_type="robot",
                data_type="frame-request",
                tag="test-allow",
                origin_client="client-1")))
    self.assertIsNone(
        sim.transform_command(
            types_gen.CommandData(
                device_type="robot",
                data_type="frame-request",
                tag="test",
                origin_client="client-1")))
    self.assertIsNone(
        sim.transform_command(
            types_gen.CommandData(
                device_type="robot",
                data_type="frame-request",
                tag="",
                origin_client="client-1")))

  def test_data_reader(self) -> None:
    """Test the simulated device-data reader."""
    device_data = [
        types_gen.DeviceData(
            ts=1000,
            seq=2,
            data_type="robot-state",
            device_type="robot",
            device_name="test"),
        types_gen.DeviceData(
            ts=2001,
            seq=1,
            data_type="robot-state",
            device_type="robot",
            device_name="test"),
        types_gen.DeviceData(
            ts=2000,
            seq=3,
            data_type="robot-state",
            device_type="robot",
            device_name="test"),
    ]

    def factory() -> "TestDeviceDataIterator":
      return TestDeviceDataIterator(device_data)

    log_iterator_test(self, device_data, _test_invalid_seqs, factory, False)

  def test_command_reader(self) -> None:
    """Test the simulated command-data iterator."""
    command_data = [
        types_gen.CommandData(
            ts=1000,
            seq=2,
            data_type="frame-request",
            device_type="robot",
            device_name="test"),
        types_gen.CommandData(
            ts=2001,
            seq=1,
            data_type="frame-request",
            device_type="robot",
            device_name="test"),
        types_gen.CommandData(
            ts=2000,
            seq=3,
            data_type="frame-request",
            device_type="robot",
            device_name="test"),
    ]

    def factory() -> "TestCommandDataIterator":
      return TestCommandDataIterator(command_data)

    log_iterator_test(self, command_data, _test_invalid_seqs, factory, False)

  def test_empty_data_reader(self) -> None:
    """Test an empty simulated device-data iterator."""

    def factory() -> "TestDeviceDataIterator":
      return TestDeviceDataIterator([])

    empty_log_iterator_test(self, factory)

  def test_empty_command_reader(self) -> None:
    """Test an empty simulated command-data iterator."""

    def factory() -> "TestCommandDataIterator":
      return TestCommandDataIterator([])

    empty_log_iterator_test(self, factory)


def empty_log_iterator_test(
    test_case: unittest.TestCase,
    factory: Callable[[],
                      Union[playback_client.Iterator[types_gen.DeviceData],
                            playback_client.Iterator[types_gen.CommandData]]]
) -> None:
  """Test an iterator implementation in the case of an empty log.

  This function is designed to be re-used in playback implementations to test
  other iterator implementations.

  Args:
    test_case: the unittest.TestCase to run asserts upon.
    factory: the factory to generate the iterators.
  """
  # Create and close an iterator, testing that calls to functions return an
  # assert error, and that valid() is False and value() is None (since iterator
  # is never started).
  reader = factory()
  test_case.assertFalse(reader.valid())
  test_case.assertIsNone(reader.value())
  test_case.assertRaises(AssertionError, reader.reset)
  test_case.assertRaises(AssertionError, reader.step)
  test_case.assertRaises(AssertionError, reader.seek, 1.0, None)
  reader.close()
  test_case.assertRaises(AssertionError, reader.reset)
  test_case.assertRaises(AssertionError, reader.step)
  test_case.assertRaises(AssertionError, reader.seek, 1.0, None)
  test_case.assertRaises(AssertionError, reader.start)
  test_case.assertFalse(reader.valid())
  test_case.assertIsNone(reader.value())

  # Create an iterator.
  reader = factory()
  # Ensure functions assert or return false or None before starting.
  test_case.assertFalse(reader.valid())
  test_case.assertIsNone(reader.value())
  test_case.assertRaises(AssertionError, reader.reset)
  test_case.assertRaises(AssertionError, reader.step)
  test_case.assertRaises(AssertionError, reader.seek, 1.0, None)
  # Start the iterator.
  reader.start()
  # Ensure value is None and valid is False after start. They should never be
  # set since the iterator is empty and has no data to return.
  test_case.assertFalse(reader.valid())
  test_case.assertIsNone(reader.value())
  # Try step, which should return False.
  test_case.assertFalse(reader.step())
  test_case.assertFalse(reader.valid())
  test_case.assertIsNone(reader.value())
  # Try seeking a timestamp. Should return False since there's no data to seek.
  test_case.assertFalse(reader.seek(1.0, None))
  test_case.assertFalse(reader.valid())
  test_case.assertIsNone(reader.value())
  # Try seeking a sequence number. Should return False.
  test_case.assertFalse(reader.seek(None, 1))
  test_case.assertFalse(reader.valid())
  test_case.assertIsNone(reader.value())
  # Try seeking both sequence number and timestamp. Should return False.
  test_case.assertFalse(reader.seek(1.0, 1))
  test_case.assertFalse(reader.valid())
  test_case.assertIsNone(reader.value())
  # Try an invalid seek that should fail with an error.
  test_case.assertRaises(core.PyReachError, reader.seek, None, None)
  test_case.assertFalse(reader.valid())
  test_case.assertIsNone(reader.value())
  # Try reset. Will return False since there is not data.
  test_case.assertFalse(reader.reset())
  test_case.assertFalse(reader.valid())
  test_case.assertIsNone(reader.value())
  # Close and test assertions again after close.
  reader.close()
  test_case.assertFalse(reader.valid())
  test_case.assertIsNone(reader.value())
  test_case.assertRaises(AssertionError, reader.step)
  test_case.assertRaises(AssertionError, reader.reset)
  test_case.assertRaises(AssertionError, reader.seek, 1.0, None)
  test_case.assertFalse(reader.valid())
  test_case.assertIsNone(reader.value())


def log_data_equal(
    test_case: unittest.TestCase, data_1: Union[types_gen.DeviceData,
                                                types_gen.CommandData],
    data_2: Union[types_gen.DeviceData, types_gen.CommandData]) -> None:
  """Test if log points are equal.

  Args:
    test_case: the unittest.TestCase to run asserts upon.
    data_1: the first data element.
    data_2: the second data element.
  """
  if isinstance(data_1, types_gen.CommandData):
    test_case.assertIsInstance(data_2, types_gen.CommandData)
    assert isinstance(data_2, types_gen.CommandData)
    if not test_utils.command_data_equal(data_1, data_2):
      test_case.assertEqual(
          json.dumps(data_1.to_json()), json.dumps(data_2.to_json()))
      test_case.fail("Commands not equal: " + str(data_1.to_json()) + " != " +
                     str(data_2.to_json()))
  else:
    test_case.assertIsInstance(data_1, types_gen.DeviceData)
    test_case.assertIsInstance(data_2, types_gen.DeviceData)
    assert isinstance(data_2, types_gen.DeviceData)
    if not test_utils.device_data_equal(data_1, data_2):
      test_case.assertEqual(
          json.dumps(data_1.to_json()), json.dumps(data_2.to_json()))
      test_case.fail("Data not equal: " + str(data_1.to_json()) + " != " +
                     str(data_2.to_json()))


def log_iterator_test(test_case: unittest.TestCase,
                      data: Union[List[types_gen.DeviceData],
                                  List[types_gen.CommandData]],
                      test_invalid_seqs: List[Tuple[Optional[float],
                                                    Optional[int]]],
                      factory: Callable[[], Union[
                          playback_client.Iterator[types_gen.DeviceData],
                          playback_client.Iterator[types_gen.CommandData]]],
                      short_test: bool) -> None:
  """Test an iterator implementation against some expected log of data.

  This function is designed to be re-used in playback implementations to test
  other iterator implementations.

  Args:
    test_case: the unittest.TestCase to run asserts upon.
    data: the expected iteration data. Must not be empty.
    test_invalid_seqs:
    factory: factory to generate iterators.
    short_test: short test.
  """

  # Data must be non-empty. For empty data cases, use empty_log_iterator_test.
  test_case.assertGreater(len(data), 0)

  data_ts_seq = {}
  for data_item in data:
    if data_item.ts not in data_ts_seq:
      data_ts_seq[data_item.ts] = data_item.seq

  # Assert the iterator value matches data at a given index.
  def assert_data(
      index: int, value: Optional[Union[Tuple[types_gen.DeviceData, float, int],
                                        Tuple[types_gen.CommandData, float,
                                              int]]]
  ) -> None:
    # Assert the data value is not None.
    test_case.assertIsNotNone(value)
    assert value
    # Assert that the timestamps and sequence numbers are correct.
    test_case.assertEqual(value[1], utils.time_at_timestamp(data[index].ts))
    test_case.assertEqual(utils.timestamp_at_time(value[1]), data[index].ts)
    test_case.assertEqual(value[2], data[index].seq)
    # Assert that the actual data is equal.
    log_data_equal(test_case, value[0], data[index])

  # Read an iterator to the end from a given data index, checking each element.
  def read_to_end(index: int,
                  reader: Union[
                      playback_client.Iterator[types_gen.DeviceData],
                      playback_client.Iterator[types_gen.CommandData]],
                  force_long: bool = False) -> None:
    while index < len(data):
      test_case.assertTrue(reader.valid())
      test_case.assertIsNotNone(reader.value())
      assert_data(index, reader.value())
      index += 1
      if index < len(data):
        test_case.assertTrue(reader.step())
        if short_test and not force_long:
          return
    test_case.assertFalse(reader.step())
    test_case.assertFalse(reader.valid())
    test_case.assertIsNone(reader.value())

  # Test creating and closing an iterator.
  reader = factory()
  test_case.assertFalse(reader.valid())
  test_case.assertIsNone(reader.value())
  test_case.assertRaises(AssertionError, reader.step)
  test_case.assertRaises(AssertionError, reader.reset)
  test_case.assertRaises(AssertionError, reader.seek, 1.0, None)
  reader.close()
  test_case.assertRaises(AssertionError, reader.step)
  test_case.assertRaises(AssertionError, reader.reset)
  test_case.assertRaises(AssertionError, reader.seek, 1.0, None)
  test_case.assertRaises(AssertionError, reader.start)
  test_case.assertFalse(reader.valid())
  test_case.assertIsNone(reader.value())

  # Create an iterator for testing.
  reader = factory()
  test_case.assertFalse(reader.valid())
  test_case.assertIsNone(reader.value())
  test_case.assertRaises(AssertionError, reader.step)
  test_case.assertRaises(AssertionError, reader.reset)
  test_case.assertRaises(AssertionError, reader.seek, 1.0, None)
  reader.start()
  # Read the iterator to the end
  read_to_end(0, reader, True)
  # Invalid seek should not be allowed
  test_case.assertRaises(core.PyReachError, reader.seek, None, None)
  start_index = max(0, len(data) - 3) if short_test else 0
  # Test seeking by timestamp forwards
  counter = 0
  for i in range(0, len(data)):
    if data_ts_seq[data[i].ts] != data[i].seq:
      continue
    counter += 1
    if counter > 3 and short_test:
      break
    test_case.assertTrue(reader.seek(utils.time_at_timestamp(data[i].ts), None))
    read_to_end(i, reader)
  # Test seeking by timestamp backwards
  counter = 0
  for i in range(len(data) - 1, -1, -1):
    if data_ts_seq[data[i].ts] != data[i].seq:
      continue
    counter += 1
    if counter > 3 and short_test:
      break
    test_case.assertTrue(reader.seek(utils.time_at_timestamp(data[i].ts), None))
    read_to_end(i, reader)
  # Test seeking by sequence forwards
  for i in range(start_index, len(data)):
    test_case.assertTrue(reader.seek(None, data[i].seq))
    read_to_end(i, reader)
  # Test seeking by sequence backwards
  for i in range(len(data) - 1, start_index - 1, -1):
    test_case.assertTrue(reader.seek(None, data[i].seq))
    read_to_end(i, reader)
  # Test seeking by timestamp and sequence forwards
  for i in range(start_index, len(data)):
    test_case.assertTrue(
        reader.seek(utils.time_at_timestamp(data[i].ts), data[i].seq))
    read_to_end(i, reader)
  # Test seeking by timestamp and sequence backwards
  for i in range(len(data) - 1, start_index - 1, -1):
    test_case.assertTrue(
        reader.seek(utils.time_at_timestamp(data[i].ts), data[i].seq))
    read_to_end(i, reader)

  # Try resetting the reader, ensure data returned is correct.
  test_case.assertTrue(reader.reset())
  assert_data(0, reader.value())
  read_to_end(0, reader)

  # Try seeking the invalid sequence tests.
  for test_time, sequence in test_invalid_seqs:
    # First, seek the zeroth data.
    test_case.assertTrue(
        reader.seek(utils.time_at_timestamp(data[0].ts), data[0].seq))
    assert_data(0, reader.value())
    test_case.assertTrue(reader.valid())
    # Seek an invalid data item.
    test_case.assertFalse(reader.seek(test_time, sequence))
    # We do not validate valid() and value(). They are undefined after an
    # invalid seek.

  # Test closing the reader.
  reader.close()
  test_case.assertFalse(reader.valid())
  test_case.assertIsNone(reader.value())
  test_case.assertRaises(AssertionError, reader.step)
  test_case.assertRaises(AssertionError, reader.reset)
  test_case.assertRaises(AssertionError, reader.seek, 1.0, None)
  test_case.assertRaises(AssertionError, reader.start)
  test_case.assertFalse(reader.valid())
  test_case.assertIsNone(reader.value())


T = TypeVar("T")


class _TestIterator(playback_client.Iterator[T]):
  """Test iterator for reading device-data or command-data."""
  _index: int
  _data: List[T]
  _started: bool
  _closed: bool

  def __init__(self, data: List[T]) -> None:
    """Create the test iterator."""
    self._index = 0
    self._data = data
    self._started = False
    self._closed = False

  def transform(self, data: T) -> Optional[Tuple[T, float, int]]:
    """Transform a line of data into the correct data type.

    Args:
      data: the data.

    Returns:
      The converted data object, the timestamp, and the sequence.
    """
    raise NotImplementedError

  def valid(self) -> bool:
    """Get if the current value is valid."""
    return self._started and not self._closed and self._index < len(self._data)

  def value(self) -> Optional[Tuple[T, float, int]]:
    """Get the current value."""
    if self.valid():
      return self.transform(self._data[self._index])
    return None

  def start(self) -> None:
    """Start the directory reader."""
    self._started = True
    assert not self._closed

  def step(self) -> bool:
    """Load the next device data."""
    assert self._started
    assert not self._closed
    if self._index < len(self._data):
      self._index += 1
    return self.valid()

  def reset(self) -> bool:
    """Reset the iterator back to the start."""
    assert self._started
    assert not self._closed
    self._index = 0
    return self.valid()

  def close(self) -> None:
    """Close the object."""
    self._closed = True


class TestDeviceDataIterator(_TestIterator[types_gen.DeviceData]):
  """Test device-data iterator iterates through a list of device-data."""

  def transform(
      self, data: types_gen.DeviceData
  ) -> Optional[Tuple[types_gen.DeviceData, float, int]]:
    """Transform a line of data into the correct data type.

    Args:
      data: the data.

    Returns:
      The converted data object, the timestamp, and the sequence.
    """
    return (data, utils.time_at_timestamp(data.ts), data.seq)


class TestCommandDataIterator(_TestIterator[types_gen.CommandData]):
  """Test command-data iterator iterates through a list of command-data."""

  def transform(
      self, data: types_gen.CommandData
  ) -> Optional[Tuple[types_gen.CommandData, float, int]]:
    """Transform a line of data into the correct data type.

    Args:
      data: the data.

    Returns:
      The converted data object, the timestamp, and the sequence.
    """
    return (data, utils.time_at_timestamp(data.ts), data.seq)


if __name__ == "__main__":
  unittest.main()
