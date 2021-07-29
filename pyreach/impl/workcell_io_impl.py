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

"""Workcell IO related classes."""

import base64
import binascii
import json
import logging
import threading
from typing import Optional, Set

from google.protobuf import message
from pyreach.common.proto_gen import workcell_io_pb2 as workcell_io
from pyreach.impl import device_base


class WorkcellIoDevice(device_base.DeviceBase):
  """Workcell IO device loads and caches workcell IO configuration.

  Workcell IO configuration provides mapping between physical IO pins and
  logical IO names. For example, digital IO pin 1 maps to vacuum on/off.
  """

  _workcell_io: Optional[workcell_io.IOConfig]  # type: ignore
  _workcell_lock: threading.Lock

  def __init__(self) -> None:
    """Construct a workcell IO device."""
    super().__init__()
    self._workcell_io = None
    self._workcell_lock = threading.Lock()

  def get(self) -> Optional[workcell_io.IOConfig]:  # type: ignore
    """Return the latest workcell IO configuration."""
    with self._workcell_lock:
      return self._workcell_io

  def get_key_values(self) -> Set[device_base.KeyValueKey]:
    """Return the key values needed to load workcell IO config.

    Returns:
      The request key for loading the workcell IO config.
    """
    return {
        device_base.KeyValueKey(
            device_type="settings-engine",
            device_name="",
            key="workcell_io.json")
    }

  def on_set_key_value(self, key: device_base.KeyValueKey, value: str) -> None:
    """Called when a key-value is available.

    Args:
      key: the key of the setting.
      value: the settings value.
    """
    if key.device_type != "settings-engine" or key.device_name:
      return

    if key.key != "workcell_io.json":
      return

    if not value:
      return

    try:
      json_data = json.loads(value)
    except json.decoder.JSONDecodeError:
      logging.warning("failed to decode workcell IO JSON")
      return
    if not isinstance(json_data, dict):
      logging.warning("failed to decode workcell IO JSON: not a dictionary")
      return
    if not isinstance(json_data.get("Proto"), str):
      logging.warning("failed to decode workcell IO JSON: not a string")
      return
    try:
      config_bin = base64.b64decode(json_data["Proto"])
    except binascii.Error:
      logging.warning("failed to decode workcell IO JSON: invalid base64")
      return
    config = workcell_io.IOConfig()  # type: ignore
    try:
      config.ParseFromString(config_bin)
    except message.DecodeError:
      logging.warning("failed to decode workcell IO JSON: invalid protobuf")
      return
    self._workcell_io = config
