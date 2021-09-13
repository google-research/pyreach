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

"""Implementation of the PyReach Internal interface."""
from typing import Callable, Optional, Tuple

import numpy as np  # type: ignore

from pyreach import internal
from pyreach.common.python import types_gen
from pyreach.impl import client as cli
from pyreach.impl import requester
from pyreach.impl import utils


class PlaybackDevice:
  """PlaybackDevice is a playback object that manages playback of data."""
  _host_flush: Tuple[Callable[[], None]]
  _client: cli.PlaybackClient

  def __init__(self, host_flush: Callable[[], None],
               client: cli.Client) -> None:
    """Create the playback device.

    Args:
      host_flush: Function to flush the reach host queues.
      client: The client object.
    """
    self._host_flush = (host_flush,)
    assert isinstance(client, cli.PlaybackClient)
    self._client = client

  def next_device_data(self) -> Optional[types_gen.DeviceData]:
    """Playback the next device-data object.

    Returns:
      Returns the DeviceData object loaded, if available.
    """
    data = self._client.next_device_data()
    self._host_flush[0]()
    return data

  def device_data_available(self) -> bool:
    return self._client.device_data_available()

  def seek_device_data(
      self, time: Optional[float],
      sequence: Optional[int]) -> Optional[types_gen.DeviceData]:
    """Seek the given device data and output it, if available.

    Args:
      time: the timestamp to seek. If sequence number is not specified, will not
        return any data from before the specified time.
      sequence: the sequence number to seek. If specified, the exact sequence
        number, or any data after it will be returned.

    Returns:
      Returns the DeviceData object loaded, if found.
    """
    data = self._client.seek_device_data(time, sequence)
    self._host_flush[0]()
    return data


class PlaybackImpl(internal.InternalPlayback):
  """PlaybackImpl is a playback object that manages playback of data."""
  _device: PlaybackDevice

  def __init__(self, host_flush: Callable[[], None],
               client: cli.Client) -> None:
    """Create the playback device.

    Args:
      host_flush: Function to flush the reach host queues.
      client: The client object.
    """
    super().__init__()
    self._device = PlaybackDevice(host_flush, client)

  def next_device_data(self) -> Optional[types_gen.DeviceData]:
    """Playback the next device-data object.

    Returns:
      Returns the DeviceData object loaded, if available.
    """
    return self._device.next_device_data()

  def device_data_available(self) -> bool:
    return self._device.device_data_available()

  def seek_device_data(
      self, time: Optional[float],
      sequence: Optional[int]) -> Optional[types_gen.DeviceData]:
    """Seek the given device data and output it, if available.

    Args:
      time: the timestamp to seek. If sequence number is not specified, will not
        return any data from before the specified time.
      sequence: the sequence number to seek. If specified, the exact sequence
        number, or any data after it will be returned.

    Returns:
      Returns the DeviceData object loaded, if found.
    """
    return self._device.seek_device_data(time, sequence)


class InternalDevice(requester.Requester[types_gen.DeviceData]):
  """Device for internal commands."""

  _playback: Optional[internal.InternalPlayback]

  def __init__(self, host_flush: Callable[[], None],
               client: cli.Client) -> None:
    """Create the playback device.

    Args:
      host_flush: Function to flush the reach host queues.
      client: The client object.
    """
    super().__init__()
    self._playback = None
    if isinstance(client, cli.PlaybackClient):
      self._playback = PlaybackImpl(host_flush, client)

  @property
  def playback(self) -> Optional[internal.InternalPlayback]:
    """Get the playback object, if available."""
    return self._playback

  def get_message_supplement(
      self, msg: types_gen.DeviceData) -> Optional[types_gen.DeviceData]:
    """Return message as supplement."""
    return msg

  def get_wrapper(self) -> Tuple["InternalDevice", "InternalImpl"]:
    """Get the wrapper for the device that should be shown to the user."""
    return self, InternalImpl(self)

  def async_send_command_data(
      self,
      command_data: types_gen.CommandData,
      callback: Optional[Callable[[types_gen.DeviceData], bool]] = None,
      finished_callback: Optional[Callable[[], None]] = None) -> None:
    """Send a command data asynchronously.

    Args:
      command_data: The command data to send.
      callback: The callback for tagged response messages. The command data
        message must be tagged if specified. The callback will stop if it
        returns true.
      finished_callback: Callback called after the callback is called.
    """
    if not command_data.tag and callback:
      raise ValueError("callback must not be set if tag is empty")
    if not command_data.tag and finished_callback:
      raise ValueError("finished_callback must not be set if tag is empty")

    if callback:
      tag = command_data.tag

      def callback_wrapper(data: types_gen.DeviceData) -> bool:
        if data.tag == tag:
          if not callback:
            return True
          return callback(data)
        return False

      self.add_update_callback(callback_wrapper, finished_callback)

    self.send_cmd(command_data)


class InternalImpl(internal.Internal):
  """Implementation of the Internal interface."""

  _device: InternalDevice

  def __init__(self, device: InternalDevice) -> None:
    """Initialize a InternalImpl around a device.

    Args:
      device: InternalDevice device.
    """
    super().__init__()
    self._device = device

  @property
  def playback(self) -> Optional[internal.InternalPlayback]:
    """Get the playback object, if available."""
    return self._device.playback

  def load_color_image_from_data(self, msg: types_gen.DeviceData) -> np.ndarray:
    """Load the color image from a device-data.

    Args:
      msg: the data message to load from.

    Raises:
      FileNotFoundError: if the image file is not found.

    Returns:
      The image loaded into an-unwritable np.ndarray.
    """
    return utils.load_color_image_from_data(msg)

  def load_depth_image_from_data(self, msg: types_gen.DeviceData) -> np.ndarray:
    """Load the depth image from a device-data.

    Args:
      msg: the data message to load from.

    Raises:
      FileNotFoundError: if the image file is not found.

    Returns:
      The image loaded into an-unwritable np.ndarray.
    """
    return utils.load_depth_image_from_data(msg)

  def async_send_command_data(
      self,
      command_data: types_gen.CommandData,
      callback: Optional[Callable[[types_gen.DeviceData], bool]] = None,
      finished_callback: Optional[Callable[[], None]] = None) -> None:
    """Send a command data asynchronously.

    Args:
      command_data: The command data to send.
      callback: The callback for tagged response messages. The command data
        message must be tagged if specified. The callback will stop if it
        returns true.
      finished_callback: Callback called after the callback is called.
    """
    self._device.async_send_command_data(command_data, callback,
                                         finished_callback)

  def send_key_value_request(self,
                             device_type: str,
                             device_name: str,
                             key: str,
                             tag: Optional[str] = None) -> str:
    """Send a key-value-request command data message to the host.

    Args:
      device_type: The device type of the message.
      device_name: The device name of the message.
      key: The key to request in the message.
      tag: Optional, if not set will be generated.

    Returns:
      The tag for the message.

    """
    if tag is None:
      tag = utils.generate_tag()
    self._device.send_cmd(
        types_gen.CommandData(
            ts=utils.timestamp_now(),
            device_type=device_type,
            device_name=device_name,
            data_type="key-value-request",
            tag=tag,
            key=key,
        ))
    return tag

  def add_device_data_callback(
      self,
      callback: Callable[[types_gen.DeviceData], bool],
      finished_callback: Optional[Callable[[],
                                           None]] = None) -> Callable[[], None]:
    """Add a listener to the DeviceData stream.

    Args:
      callback: Optional[Callable[[PyReachStatus], None]] = None,
      finished_callback: Optional[Callable[[], None]] = None

    Returns:
      A function that when called stops the callback.

    """
    return self._device.add_update_callback(callback, finished_callback)
