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
"""Internal structure for Action template."""
import enum
import json
import logging
import threading
from typing import Any, Dict, List, Optional, Set, Tuple, Union, Type

from pyreach import actionsets
from pyreach.common.python import types_gen
from pyreach.impl import device_base


class PreconditionType(enum.Enum):
  """A precondition enumeration type."""

  DIGITAL_IO = 0


class Precondition:
  """Represents a precondition."""

  _precondition_type: PreconditionType
  _digital_io_value: bool
  _digital_io_number: int
  _max_digital_io_number: int

  def __init__(self, precondition_type: PreconditionType,
               digital_io_value: bool, digital_io_number: int,
               max_digital_io_number: int) -> None:
    """Init a Precondition.

    Args:
      precondition_type: The type of the precondition.
      digital_io_value: The initial boolean value for the digital I/O.
      digital_io_number: The digital I/O port number.
      max_digital_io_number: The maximum I/O port_number.
    """
    self._precondition_type = precondition_type
    self._digital_io_value = digital_io_value
    self._digital_io_number = digital_io_number
    self._max_digital_io_number = max_digital_io_number

  def get_precondition_type(self) -> PreconditionType:
    """Return the precondition type."""
    return self._precondition_type

  def get_digital_io_value(self) -> bool:
    """Return the digital io value."""
    return self._digital_io_value

  def get_digital_io_number(self) -> int:
    """Return the digital I/O number."""
    return self._digital_io_number

  def get_max_digital_io_number(self) -> int:
    """Return the maximum digital I/O number."""
    return self._max_digital_io_number

  @classmethod
  def from_json(cls, json_data: Dict[str, Any]) -> Optional["Precondition"]:
    """Return a Precondition extracted from a JSON dictionary.

    Args:
      json_data: A JSON dictionary containing the precondition.

    Returns:
      Returns the precondition on success and None on failure.

    """
    if (not isinstance(json_data.get("_preconditionType", ""), int) or
        json_data["_preconditionType"] < 0 or
        json_data["_preconditionType"] >= len(list(PreconditionType))):
      logging.warning("Invalid _preconditionType in %s", json_data)
      return None
    if not isinstance(json_data.get("_digitalIONumber"), int):
      logging.warning("Invalid _digitalIONumber in %s", json_data)
      return None
    if not isinstance(json_data.get("_digitalIOValue"), bool):
      logging.warning("Invalid _digitalIOValue in %s", json_data)
      return None
    if not isinstance(json_data.get("_maxDigitalIONumber"), int):
      logging.warning("Invalid _maxDigitalIONumber in %s", json_data)
      return None
    return Precondition(
        list(PreconditionType)[json_data["_preconditionType"]],
        json_data["_digitalIOValue"], json_data["_digitalIONumber"],
        json_data["_maxDigitalIONumber"])


TOOL_INTERACTION_POINT_OBJECT_TYPES = ("Torus", "Capsule", "Cube", "Cylinder",
                                       "Sphere", "Blister", "BlisterBatchInput",
                                       "Deodorant", "DeodorantKitPose", "Empty")


class ToolInteractionPoint:
  """Represents a Tool Interaction Point."""

  _name: str
  _tip_object_type: str
  _pick_data: types_gen.ExperimentalCommandData
  _dimensions: types_gen.Vec3d
  _padding: Tuple[float, float, float, float, float, float]
  _tip_pos: types_gen.Vec3d
  _tip_rot: types_gen.Quaternion3d
  _local_go_pos: types_gen.Vec3d
  _local_go_rot: types_gen.Quaternion3d

  def __init__(self, name: str, tip_object_type: str,
               pick_data: types_gen.ExperimentalCommandData,
               dimensions: types_gen.Vec3d, padding: Tuple[float, float, float,
                                                           float, float, float],
               tip_pos: types_gen.Vec3d, tip_rot: types_gen.Quaternion3d,
               local_go_pos: types_gen.Vec3d,
               local_go_rot: types_gen.Quaternion3d) -> None:
    """Init a ToolInteractionPoint.

    Args:
      name: The name of the tool interaction point.
      tip_object_type: The type of end effector as a string.
      pick_data:
      dimensions: The bounding box of the end effector a (dx, dy, dz) Vec3d.
      padding:
      tip_pos: The tip position relative to end effector origin point.
      tip_rot: The tip rotation as a quaternion.
      local_go_pos:
      local_go_rot:
    """
    self._name = name
    self._tip_object_type = tip_object_type
    self._pick_data = pick_data
    self._dimensions = dimensions
    self._padding = padding
    self._tip_pos = tip_pos
    self._tip_rot = tip_rot
    self._local_go_pos = local_go_pos
    self._local_go_rot = local_go_rot

  def get_name(self) -> str:
    """Return the ToolInteractionPoint name."""
    return self._name

  def get_tip_object_type(self) -> str:
    """Return the ToolInteractionPoint type."""
    return self._tip_object_type

  def get_pick_data(self) -> types_gen.ExperimentalCommandData:
    """Return the pick data."""
    return self._pick_data

  def get_dimensions(self) -> types_gen.Vec3d:
    """Return the dimensions."""
    return self._dimensions

  def get_padding(self) -> Tuple[float, float, float, float, float, float]:
    """Return the padding."""
    return self._padding

  def get_tip_pos(self) -> types_gen.Vec3d:
    """Return the tip position."""
    return self._tip_pos

  def get_tip_rot(self) -> types_gen.Quaternion3d:
    """Return the tip rotation."""
    return self._tip_rot

  def get_local_go_pos(self) -> types_gen.Vec3d:
    """Return the local go position."""
    return self._local_go_pos

  def get_local_go_rot(self) -> types_gen.Quaternion3d:
    """Return the local go rotation."""
    return self._local_go_rot

  @classmethod
  def from_json(cls, json_data: Dict[str,
                                     Any]) -> Optional["ToolInteractionPoint"]:
    """Return ToolInteractionPoint extracted from JSON data.

    Args:
      json_data: The JSON dictionary containing the information.

    Returns:
      Returns a ToolInteractionPoint on success and None otherwise.

    """
    if not isinstance(json_data.get("Name"), str):
      logging.warning("Action ToolInteractionPoint Name invalid: %s", json_data)
      return None
    if (json_data.get("TIPObjectType")
        not in TOOL_INTERACTION_POINT_OBJECT_TYPES):
      logging.warning("Action ToolInteractionPoint TIPObjectType invalid: %s",
                      json_data)
      return None
    if not isinstance(json_data.get("PickData"), dict):
      logging.warning("Action ToolInteractionPoint PickData invalid: %s",
                      json_data)
      return None
    try:
      pick_data = types_gen.ExperimentalCommandData.from_json(
          json_data["PickData"])
    except ValueError as ex:
      logging.warning("Action ToolInteractionPoint PickData invalid: %s %s",
                      json_data, ex)
      return None
    dimensions = _from_json_vector3(json_data.get("Dimensions"))
    if dimensions is None:
      logging.warning("Action ToolInteractionPoint Dimensions invalid: %s",
                      json_data)
      return None
    if not isinstance(json_data.get("Padding"), list):
      logging.warning("Action ToolInteractionPoint Padding invalid: %s",
                      json_data)
      return None
    for padding_element in json_data["Padding"]:
      if not (isinstance(padding_element, float) or
              isinstance(padding_element, int)):
        logging.warning("Action ToolInteractionPoint Padding invalid: %s",
                        json_data)
        return None
    if len(json_data["Padding"]) != 6:
      logging.warning("Action ToolInteractionPoint Padding invalid: %s",
                      json_data)
      return None
    padding = (float(json_data["Padding"][0]), float(json_data["Padding"][1]),
               float(json_data["Padding"][2]), float(json_data["Padding"][3]),
               float(json_data["Padding"][4]), float(json_data["Padding"][5]))
    tip_pos = _from_json_vector3(json_data.get("TIPPos"))
    if tip_pos is None:
      logging.warning("Action ToolInteractionPoint TIPPos invalid: %s",
                      json_data)
      return None
    tip_rot = _from_json_quaternion(json_data.get("TIPRot"))
    if tip_rot is None:
      logging.warning("Action ToolInteractionPoint TIPRot invalid: %s",
                      json_data)
      return None
    local_go_pos = _from_json_vector3(json_data.get("LocalGOPos"))
    if local_go_pos is None:
      logging.warning("Action ToolInteractionPoint LocalGOPos invalid: %s",
                      json_data)
      return None
    local_go_rot = _from_json_quaternion(json_data.get("LocalGORot"))
    if local_go_rot is None:
      logging.warning("Action ToolInteractionPoint LocalGORot invalid: %s",
                      json_data)
      return None
    return ToolInteractionPoint(json_data["Name"], json_data["TIPObjectType"],
                                pick_data, dimensions, padding, tip_pos,
                                tip_rot, local_go_pos, local_go_rot)


class ActionStepParentType(enum.Enum):
  """Enumeration type for an Action Step."""

  ABSOLUTE = 0
  TIP_INPUT = 1
  OTHER_STEP = 2


class ActionStep:
  """Represents an Action step."""

  _tip_input_idx: int
  _parent_type: ActionStepParentType
  _pos: types_gen.Vec3d
  _rot: types_gen.Quaternion3d
  _delay: float
  _radius: float
  _velocity: float
  _acceleration: float
  _wait: float
  _parent_step_idx: int
  _use_process_mode: bool
  _individual_velocity_acceleration: float
  _use_force_mode: bool
  _use_servo_j_mode: bool
  _use_skip_move: bool
  _set_digital_io: bool
  _set_tool_digital_io: bool
  _set_digital_io_number: int
  _set_digital_io_value: bool
  _set_tool_digital_io_number: int
  _set_tool_digital_io_value: bool
  _set_capability: bool
  _set_capability_name: str
  _set_capability_type: str
  _set_capability_value: bool
  _set_capability_io_type: str
  _randomized_offset: bool
  _randomized_offset_radius_cm: float
  _acquire_image_tag: str
  _acquire_image_mode: int

  def __init__(self, tip_input_idx: int, parent_type: ActionStepParentType,
               pos: types_gen.Vec3d, rot: types_gen.Quaternion3d, delay: float,
               radius: float, velocity: float, acceleration: float, wait: float,
               parent_step_idx: int, use_process_mode: bool,
               individual_velocity_acceleration: float, use_force_mode: bool,
               use_servo_j_mode: bool, use_skip_move: bool,
               set_digital_io: bool, set_tool_digital_io: bool,
               set_digital_io_number: int, set_digital_io_value: bool,
               set_tool_digital_io_number: int, set_tool_digital_io_value: bool,
               set_capability: bool, set_capability_name: str,
               set_capability_type: str, set_capability_value: bool,
               set_capability_io_type: str, randomized_offset: bool,
               randomized_offset_radius_cm: float, acquire_image_tag: str,
               acquire_image_mode: int) -> None:
    """Construct an ActionStep.

    Args:
      tip_input_idx:
      parent_type:
      pos:
      rot:
      delay:
      radius:
      velocity:
      acceleration:
      wait:
      parent_step_idx:
      use_process_mode:
      individual_velocity_acceleration:
      use_force_mode:
      use_servo_j_mode:
      use_skip_move:
      set_digital_io:
      set_tool_digital_io:
      set_digital_io_number:
      set_digital_io_value:
      set_tool_digital_io_number:
      set_tool_digital_io_value:
      set_capability:
      set_capability_name:
      set_capability_type:
      set_capability_value:
      set_capability_io_type:
      randomized_offset:
      randomized_offset_radius_cm:
      acquire_image_tag:
      acquire_image_mode:
    """
    self._tip_input_idx = tip_input_idx
    self._parent_type = parent_type
    self._pos = pos
    self._rot = rot
    self._delay = delay
    self._radius = radius
    self._velocity = velocity
    self._acceleration = acceleration
    self._wait = wait
    self._parent_step_idx = parent_step_idx
    self._use_process_mode = use_process_mode
    self._individual_velocity_acceleration = individual_velocity_acceleration
    self._use_force_mode = use_force_mode
    self._use_servo_j_mode = use_servo_j_mode
    self._use_skip_move = use_skip_move
    self._set_digital_io = set_digital_io
    self._set_tool_digital_io = set_tool_digital_io
    self._set_digital_io_number = set_digital_io_number
    self._set_digital_io_value = set_digital_io_value
    self._set_tool_digital_io_number = set_tool_digital_io_number
    self._set_tool_digital_io_value = set_tool_digital_io_value
    self._set_capability = set_capability
    self._set_capability_name = set_capability_name
    self._set_capability_type = set_capability_type
    self._set_capability_value = set_capability_value
    self._set_capability_io_type = set_capability_io_type
    self._randomized_offset = randomized_offset
    self._randomized_offset_radius_cm = randomized_offset_radius_cm
    self._acquire_image_tag = acquire_image_tag
    self._acquire_image_mode = acquire_image_mode

  def get_tip_input_idx(self) -> int:
    """Get tip input index."""
    return self._tip_input_idx

  def get_parent_type(self) -> ActionStepParentType:
    """Get the parent type as an ActionStepParentType."""
    return self._parent_type

  def get_pos(self) -> types_gen.Vec3d:
    """Get the position."""
    return self._pos

  def get_rot(self) -> types_gen.Quaternion3d:
    """Get the rotation as a Quaternion3d."""
    return self._rot

  def get_delay(self) -> float:
    """Get the delay in seconds."""
    return self._delay

  def get_radius(self) -> float:
    """Get the radius in meters."""
    return self._radius

  def get_velocity(self) -> float:
    """Get the velocity in meters/sec."""
    return self._velocity

  def get_acceleration(self) -> float:
    """Get the acceleration in meters/sec-sec."""
    return self._acceleration

  def get_wait(self) -> float:
    """Get the wait amount in seconds."""
    return self._wait

  def get_parent_step_idx(self) -> int:
    """Get the parent step index."""
    return self._parent_step_idx

  def get_use_process_mode(self) -> bool:
    """Get the use process mode."""
    return self._use_process_mode

  def get_individual_velocity_acceleration(self) -> float:
    """Get the individual velocity acceleration."""
    return self._individual_velocity_acceleration

  def get_use_force_mode(self) -> bool:
    """Get whether use force mode is enabled."""
    return self._use_force_mode

  def get_use_servo_j_mode(self) -> bool:
    """Get the servo j mode flag."""
    return self._use_servo_j_mode

  def get_use_skip_move(self) -> bool:
    """Return whether to use skip mode."""
    return self._use_skip_move

  def get_set_digital_io(self) -> bool:
    """Return whether get/set digial I/O is enabled."""
    return self._set_digital_io

  def get_set_tool_digital_io(self) -> bool:
    """Return whether tool digital I/O is enabled."""
    return self._set_tool_digital_io

  def get_set_digital_io_number(self) -> int:
    """Return digital IO number to set."""
    return self._set_digital_io_number

  def get_set_digital_io_value(self) -> bool:
    """Return the digital IO value to set."""
    return self._set_digital_io_value

  def get_set_tool_digital_io_number(self) -> int:
    """Return the tool digital IO number to set."""
    return self._set_tool_digital_io_number

  def get_set_tool_digital_io_value(self) -> bool:
    """Return the tool digital IO value to set."""
    return self._set_tool_digital_io_value

  def get_set_capability(self) -> bool:
    """Return true to set capability."""
    return self._set_capability

  def get_set_capability_name(self) -> str:
    """Return the capability name to set."""
    return self._set_capability_name

  def get_set_capability_type(self) -> str:
    """Return the type of capability to set."""
    return self._set_capability_type

  def get_set_capability_value(self) -> bool:
    """Return the value of capability to set."""
    return self._set_capability_value

  def get_set_capability_io_type(self) -> str:
    """Return the capability IO get to set."""
    return self._set_capability_io_type

  def get_randomized_offset(self) -> bool:
    """Return true set randomized offset."""
    return self._randomized_offset

  def get_randomized_offset_radius_cm(self) -> float:
    """Return the randomized offset radius in cm."""
    return self._randomized_offset_radius_cm

  def get_acquire_image_tag(self) -> str:
    """Return the acquire image tag."""
    return self._acquire_image_tag

  def get_acquire_image_mode(self) -> int:
    """Return the acquire image mode."""
    return self._acquire_image_mode

  @classmethod
  def from_json(cls, json_data: Dict[str, Any]) -> Optional["ActionStep"]:
    """Decode a JSON message to ActionStep object."""
    remap = {
        "TIPInputIdx": "_tipInputIdx",
        "ParentType": "_parentType",
        "Delay": "_delay",
        "Radius": "_radius",
        "Velocity": "_velocity",
        "Acceleration": "_acceleration",
        "wait": "_wait",
        "Wait": "_wait",
        "ParentStepIdx": "_parentStepIdx",
        "UseProcessMode": "_useProcessMode",
        "setDigitalIO": "_setDigitalIO",
        "setDigitalIOValue": "_setDigitalIOValue",
    }
    for from_key, to_key in remap.items():
      if from_key in json_data:
        json_data[to_key] = json_data[from_key]
        del json_data[from_key]
    if not isinstance(json_data.get("_tipInputIdx"), int):
      logging.warning("Action Step _tipInputIdx invalid: %s", json_data)
      return None
    if (not isinstance(json_data.get("_parentType"), int) or
        not 0 <= json_data["_parentType"] < len(list(ActionStepParentType))):
      logging.warning("Action Step _parentType invalid: %s", json_data)
      return None
    pos = _from_json_vector3(json_data.get("pos"))
    if pos is None:
      logging.warning("Action Step pos invalid: %s", json_data)
      return None
    rot = _from_json_quaternion(json_data.get("rot"))
    if rot is None:
      logging.warning("Action Step rot invalid: %s", json_data)
      return None
    if not (isinstance(json_data.get("_delay"), float) or
            isinstance(json_data.get("_delay"), int)):
      logging.warning("Action Step _delay invalid: %s", json_data)
      return None
    if not (isinstance(json_data.get("_radius"), float) or
            isinstance(json_data.get("_radius"), int)):
      logging.warning("Action Step _radius invalid: %s", json_data)
      return None
    if not (isinstance(json_data.get("_velocity"), float) or
            isinstance(json_data.get("_velocity"), int)):
      logging.warning("Action Step _velocity invalid: %s", json_data)
      return None
    if not (isinstance(json_data.get("_acceleration"), float) or
            isinstance(json_data.get("_acceleration"), int)):
      logging.warning("Action Step _acceleration invalid: %s", json_data)
      return None
    if not (isinstance(json_data.get("_wait"), float) or
            isinstance(json_data.get("_wait"), int)):
      logging.warning("Action Step _wait invalid: %s", json_data)
      return None
    if not (isinstance(json_data.get("_parentStepIdx"), float) or
            isinstance(json_data.get("_parentStepIdx"), int)):
      logging.warning("Action Step _parentStepIdx invalid: %s", json_data)
      return None
    if not isinstance(json_data.get("_useProcessMode"), bool):
      logging.warning("Action Step _useProcessMode invalid: %s", json_data)
      return None
    if not isinstance(json_data.get("_individualVelocityAcceleration"), bool):
      logging.warning("Action Step _individualVelocityAcceleration invalid: %s",
                      json_data)
      return None
    if not isinstance(json_data.get("_useForceMode"), bool):
      logging.warning("Action Step _useForceMode invalid: %s", json_data)
      return None
    if not isinstance(json_data.get("_useServoJMode"), bool):
      logging.warning("Action Step _useServoJMode invalid: %s", json_data)
      return None
    if not isinstance(json_data.get("_useSkipMove"), bool):
      logging.warning("Action Step _useSkipMove invalid: %s", json_data)
      return None
    if not isinstance(json_data.get("_setDigitalIO"), bool):
      logging.warning("Action Step _setDigitalIO invalid: %s", json_data)
      return None
    if not isinstance(json_data.get("_setToolDigitalIO"), bool):
      logging.warning("Action Step _setToolDigitalIO invalid: %s", json_data)
      return None
    if not isinstance(json_data.get("_setDigitalIONumber"), int):
      logging.warning("Action Step _setDigitalIONumber invalid: %s", json_data)
      return None
    if json_data.get("_setToolDigitalIO", False) and not isinstance(
        json_data.get("_setToolDigitalIONumber"), int):
      logging.warning("Action Step _setToolDigitalIONumber invalid: %s",
                      json_data)
      return None
    if json_data.get("_setToolDigitalIO", False) and not isinstance(
        json_data.get("_setToolDigitalIOValue"), bool):
      logging.warning("Action Step _setToolDigitalIOValue invalid: %s",
                      json_data)
      return None
    if not isinstance(json_data.get("_setCapability"), bool):
      logging.warning("Action Step _setCapability invalid: %s", json_data)
      return None
    if not isinstance(json_data.get("_setCapabilityName"), str):
      logging.warning("Action Step _setCapabilityName invalid: %s", json_data)
      return None
    if not isinstance(json_data.get("_setCapabilityType"), str):
      logging.warning("Action Step _setCapabilityType invalid: %s", json_data)
      return None
    if not isinstance(json_data.get("_setCapabilityValue"), bool):
      logging.warning("Action Step _setCapabilityValue invalid: %s", json_data)
      return None
    if not isinstance(json_data.get("_setCapabilityIOType"), str):
      logging.warning("Action Step _setCapabilityIOType invalid: %s", json_data)
      return None
    if not isinstance(json_data.get("_randomizedOffset"), bool):
      logging.warning("Action Step _randomizedOffset invalid: %s", json_data)
      return None
    if not (isinstance(json_data.get("_randomizedOffsetRadiusCM"), float) or
            isinstance(json_data.get("_randomizedOffsetRadiusCM"), int)):
      logging.warning("Action Step _randomizedOffsetRadiusCM invalid: %s",
                      json_data)
      return None
    if not isinstance(json_data.get("_acquireImageTag", ""), str):
      logging.warning("Action Step _acquireImageTag invalid: %s", json_data)
      return None
    if not isinstance(json_data.get("_acquireImageMode", 0), int):
      logging.warning("Action Step _acquireImageMode invalid: %s", json_data)
      return None
    return ActionStep(
        json_data["_tipInputIdx"],
        list(ActionStepParentType)[json_data["_parentType"]], pos, rot,
        float(json_data["_delay"]), float(json_data["_radius"]),
        float(json_data["_velocity"]), float(json_data["_acceleration"]),
        float(json_data["_wait"]), json_data["_parentStepIdx"],
        json_data["_useProcessMode"],
        float(json_data["_individualVelocityAcceleration"]),
        json_data["_useForceMode"], json_data["_useServoJMode"],
        json_data["_useSkipMove"], json_data["_setDigitalIO"],
        json_data["_setToolDigitalIO"], json_data["_setDigitalIONumber"],
        json_data["_setDigitalIOValue"],
        json_data.get("_setToolDigitalIONumber", 0),
        json_data.get("_setToolDigitalIOValue", False),
        json_data["_setCapability"], json_data["_setCapabilityName"],
        json_data["_setCapabilityType"], json_data["_setCapabilityValue"],
        json_data["_setCapabilityIOType"], json_data["_randomizedOffset"],
        float(json_data["_randomizedOffsetRadiusCM"]),
        json_data.get("_acquireImageTag", ""),
        json_data.get("_acquireImageMode", 0))


class Action:
  """Action is a pre-programed set of instructions for a Robot."""

  _steps: List[ActionStep]
  _preconditions: List[Precondition]
  _tip_inputs: List[ToolInteractionPoint]
  _name: str
  _softstart: bool
  _softstart_accel: float
  _softstart_velocity: float
  _max_accel: float
  _max_velocity: float
  _cyclic: bool
  _task_intent: str
  _intent: str
  _success_type: str
  _capture_depth_behavior: str
  _loop: bool

  def __init__(self, steps: List[ActionStep], preconditions: List[Precondition],
               tip_inputs: List[ToolInteractionPoint], name: str,
               softstart: bool, softstart_accel: float,
               softstart_velocity: float, max_accel: float, max_velocity: float,
               cyclic: bool, task_intent: str, intent: str, success_type: str,
               capture_depth_behavior: str, loop: bool,
               use_steps_as_ikhints: bool) -> None:
    """Construct a Action template."""
    self._steps = steps
    self._preconditions = preconditions
    self._tip_inputs = tip_inputs
    self._name = name
    self._softstart = softstart
    self._softstart_accel = softstart_accel
    self._softstart_velocity = softstart_velocity
    self._max_accel = max_accel
    self._max_velocity = max_velocity
    self._cyclic = cyclic
    self._task_intent = task_intent
    self._intent = intent
    self._success_type = success_type
    self._capture_depth_behavior = capture_depth_behavior
    self._loop = loop
    self._use_steps_as_ikhints = use_steps_as_ikhints

  def get_steps(self) -> List[ActionStep]:
    """Return the list of steps for an action template."""
    return self._steps

  def get_preconditions(self) -> List[Precondition]:
    """Return the pre-condition for the action."""
    return self._preconditions

  def get_tip_inputs(self) -> List[ToolInteractionPoint]:
    """Return the input to the action as a list of tool interaction point."""
    return self._tip_inputs

  def get_name(self) -> str:
    """Return the name of the action."""
    return self._name

  def get_softstart(self) -> bool:
    """Return true if the action should have soft start."""
    return self._softstart

  def get_softstart_accel(self) -> float:
    """Return the max acceleration for the soft start."""
    return self._softstart_accel

  def get_softstart_velocity(self) -> float:
    """Return the max velocity for the soft start."""
    return self._softstart_velocity

  def get_max_accel(self) -> float:
    """Return the max acceleration of the action."""
    return self._max_accel

  def get_max_velocity(self) -> float:
    """Return the max velocity of the action."""
    return self._max_velocity

  def get_cyclic(self) -> bool:
    """Return true if the action should repeat."""
    return self._cyclic

  def get_task_intent(self) -> str:
    """Return the task intent of the action."""
    return self._task_intent

  def get_intent(self) -> str:
    """Return the intent of the action."""
    return self._intent

  def get_success_type(self) -> str:
    """Return the success type of the action."""
    return self._success_type

  def get_capture_depth_behavior(self) -> str:
    """Return the capture depth behavior."""
    return self._capture_depth_behavior

  def get_loop(self) -> bool:
    """Return true if the action should loop."""
    return self._loop

  def get_use_steps_as_ikhints(self) -> bool:
    """Return the steps as ikhints value."""
    return self._use_steps_as_ikhints

  @classmethod
  def from_json(cls, json_data: Dict[str, Any]) -> Optional["Action"]:
    """Extract an action object from JSON data.

    Args:
      json_data: JSON decoded dictionary.

    Returns:
      An action object.

    """
    remap = {
        "Preconditions": "_preconditions",
        "TIPInputs": "_tipInputs",
        "Softstart": "_softstart",
        "SoftstartAccel": "_softstartAccel",
        "SoftstartVelocity": "_softstartVelocity",
        "Name": "_name",
        "Steps": "_steps",
        "MaxAccel": "_maxAccel",
        "MaxVelocity": "_maxVelocity",
        "Cyclic": "_cylic",
        "Loop": "_loop",
    }
    for from_key, to_key in remap.items():
      if from_key in json_data:
        json_data[to_key] = json_data[from_key]
        del json_data[from_key]
    expect: Dict[str, Union[Type[Any], Tuple[Type[Any], ...]]] = {
        "_steps": list,
        "_preconditions": list,
        "_tipInputs": list,
        "_name": str,
        "_maxAccel": float,
        "_maxVelocity": float,
        "_cyclic": bool,
        "_taskIntent": (str, type(None)),
        "_intent": str,
        "_successType": str,
        "_captureDepthBehavior": str,
        "_loop": bool
    }
    optional: Dict[str, Union[Type[Any], Tuple[Type[Any], ...]]] = {
        "_useStepsAsIKHints": bool,
        "_softstart": bool,
        "_softstartAccel": float,
        "_softstartVelocity": float,
    }
    for name, t in expect.items():
      if not isinstance(json_data.get(name, None), t):
        logging.warning("Invalid type for %s in %s.", name, json_data)
        return None
    for name, t in optional.items():
      if name in json_data and not isinstance(json_data[name], t):
        logging.warning("Invalid type for %s in %s.", name, json_data)
        return None
    for name in json_data:
      if name not in expect and name not in optional:
        logging.warning("extra field %s in %s", name, json_data)
    steps = []
    for step in json_data["_steps"]:
      step_object = ActionStep.from_json(step)
      if step_object is None:
        return None
      steps.append(step_object)
    preconditions = []
    for precondition in json_data["_preconditions"]:
      precondition_object = Precondition.from_json(precondition)
      if precondition_object is None:
        return None
      preconditions.append(precondition_object)
    tips = []
    for tip in json_data["_tipInputs"]:
      tip_object = ToolInteractionPoint.from_json(tip)
      if tip_object is None:
        return None
      tips.append(tip_object)
    return Action(steps, preconditions, tips, json_data["_name"],
                  json_data.get("_softstart", False),
                  float(json_data.get("_softstartAccel", 0.0)),
                  float(json_data.get("_softstartVelocity",
                                      0.0)), float(json_data["_maxAccel"]),
                  float(json_data["_maxVelocity"]), json_data["_cyclic"],
                  json_data.get("_taskIntent", ""), json_data["_intent"],
                  json_data["_successType"],
                  json_data["_captureDepthBehavior"], json_data["_loop"],
                  json_data.get("_useStepsAsIKHints", False))


def _from_json_vector3(json_data: Any) -> Optional[types_gen.Vec3d]:
  """Return the X/Y/Z values from JSON.

  Args:
    json_data: A JSON dictionary containing "x", "y", and "z" entries.

  Returns:
    Return a Vec3d containing the X/Y/Z values.

  """
  if not (isinstance(json_data.get("x"), float) or
          isinstance(json_data.get("x"), int)):
    return None
  if not (isinstance(json_data.get("y"), float) or
          isinstance(json_data.get("y"), int)):
    return None
  if not (isinstance(json_data.get("z"), float) or
          isinstance(json_data.get("z"), int)):
    return None
  if len(json_data) != 3:
    return None
  return types_gen.Vec3d(
      float(json_data["x"]), float(json_data["y"]), float(json_data["z"]))


def _from_json_quaternion(json_data: Any) -> Optional[types_gen.Quaternion3d]:
  """Return a quaternion extracted from JSON.

  Args:
    json_data: A JSON dictionary containing "x", "y", "z", and "w" entries.

  Returns:
    The appropriate Quaternion3d is returned.

  """
  if not isinstance(json_data, dict):
    return None
  if not (isinstance(json_data.get("x"), float) or
          isinstance(json_data.get("x"), int)):
    return None
  if not (isinstance(json_data.get("y"), float) or
          isinstance(json_data.get("y"), int)):
    return None
  if not (isinstance(json_data.get("z"), float) or
          isinstance(json_data.get("z"), int)):
    return None
  if not (isinstance(json_data.get("w"), float) or
          isinstance(json_data.get("w"), int)):
    return None
  if len(json_data) != 4:
    return None
  return types_gen.Quaternion3d(
      float(json_data["w"]), float(json_data["x"]), float(json_data["y"]),
      float(json_data["z"]))


class ActionsImpl(actionsets.Actions):
  """Implementation of the Actions interface."""

  _actions: List[Action]

  def __init__(self, actions: List[Action]) -> None:
    """Construct a new ActionsImpl object."""
    self._actions = actions

  def action_names(self) -> Tuple[str, ...]:
    """Return the list of available action template names."""
    return tuple([action.get_name() for action in self._actions])

  def get_action(self, name: str) -> Optional[Action]:
    """Return the action with the provided name."""
    for action in self._actions:
      if action.get_name() == name:
        return action
    return None


class ActionDevice(device_base.DeviceBase):
  """Device for accessing action template."""

  _actions: Optional[ActionsImpl]
  _actions_lock: threading.Lock
  _actions_loaded: threading.Event

  def __init__(self) -> None:
    """Construct an ActionDevice."""
    super().__init__()
    self._actions = None
    self._actions_lock = threading.Lock()
    self._actions_loaded = threading.Event()

  def on_close(self) -> None:
    """Invoke when the device is closing at shutdown."""
    self._actions_loaded.set()

  def wait_actions(self, timeout: Optional[float]) -> Optional[ActionsImpl]:
    """Waits for the actions to load and returns the actions.

    Args:
      timeout: the optional timeout to wait for the actions to load.

    Returns:
      The actions, if it loaded.
    """
    self._actions_loaded.wait(timeout)
    return self.get_actions()

  def get_key_values(self) -> Set[device_base.KeyValueKey]:
    """Construct keys for action sets."""
    return {
        device_base.KeyValueKey(
            device_type="settings-engine",
            device_name="",
            key="actionsets.json")
    }

  def get_actions(self) -> Optional[ActionsImpl]:
    """Get the list of action templates."""
    with self._actions_lock:
      return self._actions

  def on_set_key_value(self, key: device_base.KeyValueKey, value: str) -> None:
    """Process key value event for action templates."""
    if key.device_type != "settings-engine" or key.device_name:
      return
    if key.key != "actionsets.json":
      return
    if not value:
      with self._actions_lock:
        self._actions = None
        self._actions_loaded.set()
      return
    try:
      data = json.loads(value)
    except json.decoder.JSONDecodeError as decode_error:
      logging.warning("failed to parse actionsets.json %s", decode_error)
      self._actions_loaded.set()
      return
    if not isinstance(data.get("actions"), str):
      logging.warning("failed to parse actionsets.json - "
                      "does not contain 'actions' key")
      self._actions_loaded.set()
      return
    try:
      json_data = json.loads(data["actions"])
    except json.decoder.JSONDecodeError as decode_error:
      logging.warning(
          "failed to parse actionsets.json 'actions' "
          "content: %s", decode_error)
      self._actions_loaded.set()
      return
    if json_data is None:
      self._actions_loaded.set()
      return None
    if not isinstance(json_data, list):
      logging.warning("actionsets data was not a list")
      self._actions_loaded.set()
      return None
    actions: List[Action] = []
    for action in json_data:
      if not isinstance(action, dict):
        logging.warning("action was not a dictionary, ignored: %s", str(action))
      else:
        action_object = Action.from_json(action)
        if not action_object:
          logging.warning(
              "Invalid action %s dropped: %s",
              str(action.get("_name", action.get("Name", "<invalid name>"))),
              str(action))
        else:
          actions.append(action_object)
    with self._actions_lock:
      self._actions = ActionsImpl(actions)
      self._actions_loaded.set()

  def get_wrapper(self) -> Tuple["ActionDevice", "ActionsetsWrapper"]:
    """Get a wrapper for the device that should be shown to the user."""
    return self, ActionsetsWrapper(self)


class ActionsetsWrapper:
  """A wrapper class for Actionsets."""

  _device: ActionDevice

  def __init__(self, device: "ActionDevice"):
    """Construct a wrapper for action sets."""
    self._device = device

  def get(self) -> Optional[ActionsImpl]:
    """Return an implementation of Actions."""
    return self._device.get_actions()
