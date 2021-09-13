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

"""Pipeline Descriptions."""

import dataclasses
import enum
from typing import Optional, Tuple


class InterfaceType(enum.Enum):
  """Represents the type of a machine interface."""

  AUDIO_REQUEST_MUTE = "audio-request-mute"
  AUDIO_REQUEST_UNMUTE = "audio-request-unmute"
  CLIENT_ANNOTATION = "client-annotation"
  CONNECTED_CLIENTS_REQUEST = "connected-clients-request"
  DISABLE_EXPERIMENTS = "disable-experiments"
  ENABLE_EXPERIMENTS = "enable-experiments"
  EVENT = "event"
  FRAME_REQUEST = "frame-request"
  HISTORY_REQUEST = "history-request"
  INFERENCE_REQUEST = "inference-request"
  KEY_VALUE = "key-value"
  KEY_VALUE_REQUEST = "key-value-request"
  MACHINE_INTERFACES_REQUEST = "machine-interfaces-request"
  PING = "ping"
  PIPELINE_DESCRIPTION_REQUEST = "pipeline-description-request"
  POINTER_EVENT = "pointer-event"
  PUBLISH = "publish"
  REACH_SCRIPT = "reach-script"
  RUN_SCRIPT = "run-script"
  STREAM_REQUEST = "stream-request"
  TEXT_INSTRUCTION_REQUEST = "text-instruction-request"
  USER_LABEL = "user-label"
  UR_COMMAND = "ur-command"

  @classmethod
  def from_string(cls, interface_type: str) -> "InterfaceType":
    for option in cls:
      if option.value == interface_type:
        return option
    raise ValueError("Not an interface type: %s" % interface_type)


@dataclasses.dataclass(frozen=True)
class MachineInterface:
  """Represents the interface to a pipeline machine.

  Attributes:
    interface_type: The type of interface.
    device_type: The device type.
    device_name: The device name.
    data_type: The data type.
    keys: The keys provided by the interface.
  """

  interface_type: InterfaceType
  device_type: str
  device_name: str
  data_type: str
  keys: Tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class MachineInterfaces(object):
  """MachineInterfaces to a connection.

  Attributes:
    time: The timestamp of the machine interface.
    machine_interfaces: The list of machine interfaces to run.
  """

  time: float
  machine_interfaces: Tuple[MachineInterface, ...]

  def get_machine_interfaces_with_type(
      self, device_type: str) -> Tuple[MachineInterface, ...]:
    """Get the machine interfaces for a given device-type for this object."""
    return tuple([
        interface for interface in self.machine_interfaces
        if interface.device_type == device_type
    ])

  def get_request_strategy(self, device_type: str, device_name: str,
                           data_type: str) -> Optional[InterfaceType]:
    """Get the correct request strategy to read from a device.

    Args:
      device_type: The device type to consider.
      device_name: The device name to consider.
      data_type: The data type to consider.

    Returns:
      The request strategy for the given data.
    """
    have_frame_request = False
    for interface in self.machine_interfaces:
      if interface.device_type != device_type:
        continue
      if interface.device_name != device_name:
        continue
      if interface.data_type != data_type:
        continue
      if interface.interface_type == InterfaceType.PUBLISH:
        return InterfaceType.PUBLISH
      elif interface.interface_type == InterfaceType.FRAME_REQUEST:
        have_frame_request = True
    if have_frame_request:
      return InterfaceType.FRAME_REQUEST
    return None
