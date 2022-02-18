"""Implementation of PyReach Gym Annotation Device."""

import sys
from typing import Any, Optional, Tuple
import gym  # type: ignore
import numpy as np  # type: ignore

import pyreach
from pyreach.common.proto_gen import logs_pb2
from pyreach import client_annotation
from pyreach import snapshot as lib_snapshot
from pyreach.gyms import annotation_element
from pyreach.gyms import core as gyms_core
from pyreach.gyms.devices import reach_device


class ReachDeviceAnnotation(reach_device.ReachDevice):
  """Represents some an Annotation Device.

  Attributes:
    action_space:
      "data": Gym.Space.MultDiscrete()  values: 0-256,  Length set at config.
      "disable": Gym.Space.Discrete()  Value: 0, 1
    observation_space:
      "data": Gym.Space.MultDiscrete()  values: 0-256,  Length set at config.
      "maximum_size": Gym.Space.Discreate() value: 0-1
      "ts": Gym.Space.Box(shape=())  Value: non-negative float
  """

  def __init__(self,
               annotation_config: annotation_element.ReachAnnotation) -> None:
    """Init a Annotation element.

    Args:
      annotation_config: The annotation device configuration information.
    """
    reach_name: str = annotation_config.reach_name
    maximum_size: int = annotation_config.maximum_size
    is_synchronous: bool = annotation_config.is_synchronous
    if maximum_size <= 1:
      raise pyreach.PyReachError(
          f"Annotation device maximum_size(={maximum_size}) is too small")

    action_space: gym.spaces.Dict = gym.spaces.Dict({
        "data": gym.spaces.MultiDiscrete(maximum_size * [256]),
        "disable": gym.spaces.Discrete((1 << 64) - 1),  # uint64
    })
    observation_space: gym.spaces.Dict = gym.spaces.Dict({
        "data": gym.spaces.MultiDiscrete(maximum_size * [256]),
        "maximum_size": gym.spaces.Discrete(maximum_size),
        "ts": gym.spaces.Box(low=0, high=sys.maxsize, shape=()),
    })

    super().__init__(reach_name, action_space, observation_space,
                     is_synchronous)
    self._previous_data: bytes = bytes()
    self._previous_ts: float = 0.0
    self._maximum_size: int = maximum_size
    self._client_annotation: Optional[client_annotation.ClientAnnotation] = None
    self._config: annotation_element.ReachAnnotation = annotation_config
    self._is_synchronous: bool = is_synchronous

  def __str__(self) -> str:
    """Return string representation of ReachDeviceAnnotation."""
    return f"ReachDeviceAnnotation('{self.config_name}':'{self._reach_name}')"

  def start_observation(self, host: pyreach.Host) -> bool:
    """Start a synchronous observation.

    Args:
        host: The host to communiciate with.

    Returns:
        Return True if observation started.

    """
    return True

  def get_observation(self,
                      host: pyreach.Host) -> reach_device.ObservationSnapshot:
    """Return the Reach Server Gym Observation as an empty Dict.

    Args:
      host: The host to get the observation from.

    Returns:
      Returns a Tuple containing the Gym Observation, a tuple of
      SnapshotReference objects and a tuple of SnapshotResponse objects.
    Raises:
      pyreach.PyReachError when there is not observation available.

    """
    return {}, (), ()

  def do_action(
      self, action: gyms_core.Action,
      host: pyreach.Host) -> Tuple[lib_snapshot.SnapshotGymAction, ...]:
    """Start/stop the action.

    Args:
      action: The Gym Action Space to process as a Gym Dict Space with a
        "task_enable" field (0=End, 1=Start).
      host: The reach host to use.

    Returns:
        The list of gym action snapshots.
    """
    with self._timers_select({"!agent*", "gym.annotation"}):
      action_dict: gyms_core.ActionDict = self._get_action_dict(action)
      disable: bool = False
      for key in action_dict.keys():
        if key not in ("data", "disable"):
          raise pyreach.PyReachError(f"Unexpected key '{key}' for annotation.")
      if "disable" in action_dict:
        action_dict_disable: Any = action_dict["disable"]
        if not isinstance(action_dict_disable, int):
          raise pyreach.PyReachError("Annotation 'disable' is not an int")
        disable = action_dict_disable != 0
      if not disable:
        if "data" not in action_dict:
          raise pyreach.PyReachError("Annotation is missing 'data'")
        action_data: Any = action_dict["data"]
        index: int
        end: int
        data: bytes = bytes()
        if isinstance(action_data, bytes):
          data = action_data
        elif isinstance(action_data, (list, tuple)):
          byte: int
          end = -1
          for index, byte in enumerate(action_data):
            if byte < 0 or byte > 256:
              raise pyreach.PyReachError(
                  f"Annotation byte ({byte}) out of range.")
            if end < 0 and byte == 256:
              end = index
          data = bytes(action_data[:end] if end >= 0 else action_data)
        elif isinstance(action_data, np.ndarray):
          shape: Tuple[int, ...] = action_data.shape
          if len(shape) != 1:
            raise pyreach.PyReachError(
                "Annotation data must be a list of bytes terminated by a 256.")
          idata = [int(byte) for byte in action_data]
          end = idata.index(256)  # 256 marks end of data
          data = bytes(idata[:end] if end >= 0 else idata)
        else:
          raise pyreach.PyReachError(
              "Annotation data must be bytes or ndarray "
              f"type={type(action_data)} action_data={action_data}")

        size: int = len(data)
        maximum_size: int = self._maximum_size
        if size > maximum_size:
          raise pyreach.PyReachError(
              f"Annotation data size(={size}) > maximum_size(={maximum_size})")
        if data:
          annotation: logs_pb2.ClientAnnotation
          annotation = logs_pb2.ClientAnnotation()
          annotation.ParseFromString(data)
          snapshot: lib_snapshot.SnapshotGymAction
          snapshot = lib_snapshot.SnapshotGymClientAnnotationAction(
              device_type="annotation",
              device_name=self._reach_name,
              synchronous=self._is_synchronous,
              annotation=annotation)
          return (snapshot,)
      return ()  # No data to snapshot

  def _get_annotation_device(self,
                             host: pyreach.Host) -> pyreach.ClientAnnotation:
    """Return the pyreach.TextInstructions device."""
    if not self._client_annotation:
      if not host.client_annotation:
        raise pyreach.PyReachError(
            "Internal Error: There is no pyreach.Annotation "
            "configured for host.")
      self._client_annotation = host.client_annotation
    return self._client_annotation

  def validate(self, host: pyreach.Host) -> str:
    """Validate that annotation device is operable."""
    try:
      _ = self._get_annotation_device(host)
    except pyreach.PyReachError as pyreach_error:
      return str(pyreach_error)
    return ""

  def synchronize(self, host: pyreach.Host) -> None:
    """Force the annotation device synchronize its observations."""
    pass
