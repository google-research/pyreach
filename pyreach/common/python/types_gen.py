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

"""Python classes for Reach protos."""
# pylint: disable=line-too-long
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from google.protobuf import duration_pb2
from google.protobuf import timestamp_pb2
from pyreach.common.proto_gen import logs_pb2  # type: ignore

# This file is generated. DO NOT EDIT.


def get_proto_value(field):
  if isinstance(field, timestamp_pb2.Timestamp):
    return int(field.seconds * 1000 + field.nanos / 1000000)
  if isinstance(field, duration_pb2.Duration):
    return field.seconds * 1 + field.nanos / 1000000000
  return field


def get_proto_field(obj, field):
  if not obj.HasField(field):
    return None
  return getattr(obj, field)


class AcquireImageArgs:
  """Representation of proto message AcquireImageArgs.

   AcquireImageArgs contains the arguments for the command to acquire an image
   from the given device type and name at this point in program execution.
   The tag will be present in the response.
  """
  tag: str
  device_type: str
  device_name: str

  # mode is:
  # 0: nonblocking
  # 1: block until exposure complete
  # 2: block until frame delivered
  mode: int

  def __init__(self, device_name: str = '', device_type: str = '', mode: int = 0, tag: str = '') -> None:
    self.device_name = device_name
    self.device_type = device_type
    self.mode = mode
    self.tag = tag

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.device_name:
      assert isinstance(self.device_name, str), 'Wrong type for attribute: device_name. Expected: str. Got: ' + str(type(self.device_name)) + '.'
      json_data['deviceName'] = self.device_name

    if self.device_type:
      assert isinstance(self.device_type, str), 'Wrong type for attribute: device_type. Expected: str. Got: ' + str(type(self.device_type)) + '.'
      json_data['deviceType'] = self.device_type

    if self.mode:
      assert isinstance(self.mode, int), 'Wrong type for attribute: mode. Expected: int. Got: ' + str(type(self.mode)) + '.'
      json_data['mode'] = self.mode

    if self.tag:
      assert isinstance(self.tag, str), 'Wrong type for attribute: tag. Expected: str. Got: ' + str(type(self.tag)) + '.'
      json_data['tag'] = self.tag

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'AcquireImageArgs':
    """Convert JSON to type object."""
    obj = AcquireImageArgs()

    expected_json_keys: List[str] = ['deviceName', 'deviceType', 'mode', 'tag']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid AcquireImageArgs. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'deviceName' in json_data:
      assert isinstance(json_data['deviceName'], str), 'Wrong type for attribute: deviceName. Expected: str. Got: ' + str(type(json_data['deviceName'])) + '.'
      obj.device_name = json_data['deviceName']

    if 'deviceType' in json_data:
      assert isinstance(json_data['deviceType'], str), 'Wrong type for attribute: deviceType. Expected: str. Got: ' + str(type(json_data['deviceType'])) + '.'
      obj.device_type = json_data['deviceType']

    if 'mode' in json_data:
      assert isinstance(json_data['mode'], int), 'Wrong type for attribute: mode. Expected: int. Got: ' + str(type(json_data['mode'])) + '.'
      obj.mode = json_data['mode']

    if 'tag' in json_data:
      assert isinstance(json_data['tag'], str), 'Wrong type for attribute: tag. Expected: str. Got: ' + str(type(json_data['tag'])) + '.'
      obj.tag = json_data['tag']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.AcquireImageArgs) -> 'AcquireImageArgs':
    """Convert AcquireImageArgs proto to type object."""
    if not proto:
      return None
    obj = AcquireImageArgs()
    obj.device_name = get_proto_value(proto.device_name)
    obj.device_type = get_proto_value(proto.device_type)
    obj.mode = get_proto_value(proto.mode)
    obj.tag = get_proto_value(proto.tag)
    return obj


class AddObject:
  """Representation of proto message AddObject.

   AddObject adds a new object in a specific pose within a scene in SIM.

  """
  py_id: str
  py_type: str
  pose_xyzxyzw: List[float]

  def __init__(self, pose_xyzxyzw: Optional[List[float]] = None, py_id: str = '', py_type: str = '') -> None:
    if pose_xyzxyzw is None:
      self.pose_xyzxyzw = []
    else:
      self.pose_xyzxyzw = pose_xyzxyzw
    self.py_id = py_id
    self.py_type = py_type

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.pose_xyzxyzw:
      assert isinstance(self.pose_xyzxyzw, list), 'Wrong type for attribute: pose_xyzxyzw. Expected: list. Got: ' + str(type(self.pose_xyzxyzw)) + '.'
      json_data['poseXYZXYZW'] = self.pose_xyzxyzw

    if self.py_id:
      assert isinstance(self.py_id, str), 'Wrong type for attribute: py_id. Expected: str. Got: ' + str(type(self.py_id)) + '.'
      json_data['id'] = self.py_id

    if self.py_type:
      assert isinstance(self.py_type, str), 'Wrong type for attribute: py_type. Expected: str. Got: ' + str(type(self.py_type)) + '.'
      json_data['type'] = self.py_type

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'AddObject':
    """Convert JSON to type object."""
    obj = AddObject()
    json_list: List[Any]

    expected_json_keys: List[str] = ['poseXYZXYZW', 'id', 'type']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid AddObject. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'poseXYZXYZW' in json_data:
      assert isinstance(json_data['poseXYZXYZW'], list), 'Wrong type for attribute: poseXYZXYZW. Expected: list. Got: ' + str(type(json_data['poseXYZXYZW'])) + '.'
      json_list = []
      for j in json_data['poseXYZXYZW']:
        json_list.append(j)
      obj.pose_xyzxyzw = json_list

    if 'id' in json_data:
      assert isinstance(json_data['id'], str), 'Wrong type for attribute: id. Expected: str. Got: ' + str(type(json_data['id'])) + '.'
      obj.py_id = json_data['id']

    if 'type' in json_data:
      assert isinstance(json_data['type'], str), 'Wrong type for attribute: type. Expected: str. Got: ' + str(type(json_data['type'])) + '.'
      obj.py_type = json_data['type']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.AddObject) -> 'AddObject':
    """Convert AddObject proto to type object."""
    if not proto:
      return None
    obj = AddObject()
    if proto.pose_xyzxyzw:
      json_list = []
      for j in proto.pose_xyzxyzw:
        json_list.append(j)
      obj.pose_xyzxyzw = json_list
    obj.py_id = get_proto_value(proto.id)
    obj.py_type = get_proto_value(proto.type)
    return obj


class AnalogBank:
  """Representation of proto message AnalogBank.

   AnalogBank represents the raw state of one or more contiguous analog pins.
  """
  # The pin space, e.g. "controller", "tool", "user", "group"
  space: str

  # True for outputs, false for inputs
  output: bool

  # The pin number of the first element in state.
  start: int

  # The states of contiguous pins, starting with the pin number in start.
  state: List[float]

  def __init__(self, output: bool = False, space: str = '', start: int = 0, state: Optional[List[float]] = None) -> None:
    self.output = output
    self.space = space
    self.start = start
    if state is None:
      self.state = []
    else:
      self.state = state

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.output:
      assert isinstance(self.output, bool), 'Wrong type for attribute: output. Expected: bool. Got: ' + str(type(self.output)) + '.'
      json_data['output'] = self.output

    if self.space:
      assert isinstance(self.space, str), 'Wrong type for attribute: space. Expected: str. Got: ' + str(type(self.space)) + '.'
      json_data['space'] = self.space

    if self.start:
      assert isinstance(self.start, int), 'Wrong type for attribute: start. Expected: int. Got: ' + str(type(self.start)) + '.'
      json_data['start'] = self.start

    if self.state:
      assert isinstance(self.state, list), 'Wrong type for attribute: state. Expected: list. Got: ' + str(type(self.state)) + '.'
      json_data['state'] = self.state

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'AnalogBank':
    """Convert JSON to type object."""
    obj = AnalogBank()
    json_list: List[Any]

    expected_json_keys: List[str] = ['output', 'space', 'start', 'state']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid AnalogBank. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'output' in json_data:
      assert isinstance(json_data['output'], bool), 'Wrong type for attribute: output. Expected: bool. Got: ' + str(type(json_data['output'])) + '.'
      obj.output = json_data['output']

    if 'space' in json_data:
      assert isinstance(json_data['space'], str), 'Wrong type for attribute: space. Expected: str. Got: ' + str(type(json_data['space'])) + '.'
      obj.space = json_data['space']

    if 'start' in json_data:
      assert isinstance(json_data['start'], int), 'Wrong type for attribute: start. Expected: int. Got: ' + str(type(json_data['start'])) + '.'
      obj.start = json_data['start']

    if 'state' in json_data:
      assert isinstance(json_data['state'], list), 'Wrong type for attribute: state. Expected: list. Got: ' + str(type(json_data['state'])) + '.'
      json_list = []
      for j in json_data['state']:
        json_list.append(j)
      obj.state = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.AnalogBank) -> 'AnalogBank':
    """Convert AnalogBank proto to type object."""
    if not proto:
      return None
    obj = AnalogBank()
    obj.output = get_proto_value(proto.output)
    obj.space = get_proto_value(proto.space)
    obj.start = get_proto_value(proto.start)
    if proto.state:
      json_list = []
      for j in proto.state:
        json_list.append(j)
      obj.state = json_list
    return obj


class ArmActionParams:
  """Representation of proto message ArmActionParams.

   ArmActionParams stores the original arm action.
  """
  command: int
  cid: int
  joint_angles: List[float]
  pose: List[float]
  reach_action: int
  use_linear: bool
  velocity: float
  acceleration: float
  timeout_sec: float
  action_name: str
  use_unity_ik: bool
  intent: str
  success_type: str
  pick_id: str
  apply_tip_adjust_transform: bool
  servo: bool
  servo_t_secs: float
  servo_lookahead_time_secs: float
  servo_gain: float
  allow_uncalibrated: bool

  def __init__(self, acceleration: float = 0.0, action_name: str = '', allow_uncalibrated: bool = False, apply_tip_adjust_transform: bool = False, cid: int = 0, command: int = 0, intent: str = '', joint_angles: Optional[List[float]] = None, pick_id: str = '', pose: Optional[List[float]] = None, reach_action: int = 0, servo: bool = False, servo_gain: float = 0.0, servo_lookahead_time_secs: float = 0.0, servo_t_secs: float = 0.0, success_type: str = '', timeout_sec: float = 0.0, use_linear: bool = False, use_unity_ik: bool = False, velocity: float = 0.0) -> None:
    self.acceleration = acceleration
    self.action_name = action_name
    self.allow_uncalibrated = allow_uncalibrated
    self.apply_tip_adjust_transform = apply_tip_adjust_transform
    self.cid = cid
    self.command = command
    self.intent = intent
    if joint_angles is None:
      self.joint_angles = []
    else:
      self.joint_angles = joint_angles
    self.pick_id = pick_id
    if pose is None:
      self.pose = []
    else:
      self.pose = pose
    self.reach_action = reach_action
    self.servo = servo
    self.servo_gain = servo_gain
    self.servo_lookahead_time_secs = servo_lookahead_time_secs
    self.servo_t_secs = servo_t_secs
    self.success_type = success_type
    self.timeout_sec = timeout_sec
    self.use_linear = use_linear
    self.use_unity_ik = use_unity_ik
    self.velocity = velocity

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.acceleration:
      assert isinstance(self.acceleration, float) or isinstance(self.acceleration, int), 'Wrong type for attribute: acceleration. Expected: float. Got: ' + str(type(self.acceleration)) + '.'
      json_data['acceleration'] = self.acceleration

    if self.action_name:
      assert isinstance(self.action_name, str), 'Wrong type for attribute: action_name. Expected: str. Got: ' + str(type(self.action_name)) + '.'
      json_data['actionName'] = self.action_name

    if self.allow_uncalibrated:
      assert isinstance(self.allow_uncalibrated, bool), 'Wrong type for attribute: allow_uncalibrated. Expected: bool. Got: ' + str(type(self.allow_uncalibrated)) + '.'
      json_data['allowUncalibrated'] = self.allow_uncalibrated

    if self.apply_tip_adjust_transform:
      assert isinstance(self.apply_tip_adjust_transform, bool), 'Wrong type for attribute: apply_tip_adjust_transform. Expected: bool. Got: ' + str(type(self.apply_tip_adjust_transform)) + '.'
      json_data['applyTipAdjustTransform'] = self.apply_tip_adjust_transform

    if self.cid:
      assert isinstance(self.cid, int), 'Wrong type for attribute: cid. Expected: int. Got: ' + str(type(self.cid)) + '.'
      json_data['cid'] = self.cid

    if self.command:
      assert isinstance(self.command, int), 'Wrong type for attribute: command. Expected: int. Got: ' + str(type(self.command)) + '.'
      json_data['command'] = self.command

    if self.intent:
      assert isinstance(self.intent, str), 'Wrong type for attribute: intent. Expected: str. Got: ' + str(type(self.intent)) + '.'
      json_data['intent'] = self.intent

    if self.joint_angles:
      assert isinstance(self.joint_angles, list), 'Wrong type for attribute: joint_angles. Expected: list. Got: ' + str(type(self.joint_angles)) + '.'
      json_data['jointAngles'] = self.joint_angles

    if self.pick_id:
      assert isinstance(self.pick_id, str), 'Wrong type for attribute: pick_id. Expected: str. Got: ' + str(type(self.pick_id)) + '.'
      json_data['pickID'] = self.pick_id

    if self.pose:
      assert isinstance(self.pose, list), 'Wrong type for attribute: pose. Expected: list. Got: ' + str(type(self.pose)) + '.'
      json_data['pose'] = self.pose

    if self.reach_action:
      assert isinstance(self.reach_action, int), 'Wrong type for attribute: reach_action. Expected: int. Got: ' + str(type(self.reach_action)) + '.'
      json_data['reachAction'] = self.reach_action

    if self.servo:
      assert isinstance(self.servo, bool), 'Wrong type for attribute: servo. Expected: bool. Got: ' + str(type(self.servo)) + '.'
      json_data['servo'] = self.servo

    if self.servo_gain:
      assert isinstance(self.servo_gain, float) or isinstance(self.servo_gain, int), 'Wrong type for attribute: servo_gain. Expected: float. Got: ' + str(type(self.servo_gain)) + '.'
      json_data['servoGain'] = self.servo_gain

    if self.servo_lookahead_time_secs:
      assert isinstance(self.servo_lookahead_time_secs, float) or isinstance(self.servo_lookahead_time_secs, int), 'Wrong type for attribute: servo_lookahead_time_secs. Expected: float. Got: ' + str(type(self.servo_lookahead_time_secs)) + '.'
      json_data['servoLookaheadTimeSecs'] = self.servo_lookahead_time_secs

    if self.servo_t_secs:
      assert isinstance(self.servo_t_secs, float) or isinstance(self.servo_t_secs, int), 'Wrong type for attribute: servo_t_secs. Expected: float. Got: ' + str(type(self.servo_t_secs)) + '.'
      json_data['servoTSecs'] = self.servo_t_secs

    if self.success_type:
      assert isinstance(self.success_type, str), 'Wrong type for attribute: success_type. Expected: str. Got: ' + str(type(self.success_type)) + '.'
      json_data['successType'] = self.success_type

    if self.timeout_sec:
      assert isinstance(self.timeout_sec, float) or isinstance(self.timeout_sec, int), 'Wrong type for attribute: timeout_sec. Expected: float. Got: ' + str(type(self.timeout_sec)) + '.'
      json_data['timeoutSec'] = self.timeout_sec

    if self.use_linear:
      assert isinstance(self.use_linear, bool), 'Wrong type for attribute: use_linear. Expected: bool. Got: ' + str(type(self.use_linear)) + '.'
      json_data['useLinear'] = self.use_linear

    if self.use_unity_ik:
      assert isinstance(self.use_unity_ik, bool), 'Wrong type for attribute: use_unity_ik. Expected: bool. Got: ' + str(type(self.use_unity_ik)) + '.'
      json_data['useUnityIk'] = self.use_unity_ik

    if self.velocity:
      assert isinstance(self.velocity, float) or isinstance(self.velocity, int), 'Wrong type for attribute: velocity. Expected: float. Got: ' + str(type(self.velocity)) + '.'
      json_data['velocity'] = self.velocity

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'ArmActionParams':
    """Convert JSON to type object."""
    obj = ArmActionParams()
    json_list: List[Any]

    expected_json_keys: List[str] = ['acceleration', 'actionName', 'allowUncalibrated', 'applyTipAdjustTransform', 'cid', 'command', 'intent', 'jointAngles', 'pickID', 'pose', 'reachAction', 'servo', 'servoGain', 'servoLookaheadTimeSecs', 'servoTSecs', 'successType', 'timeoutSec', 'useLinear', 'useUnityIk', 'velocity']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid ArmActionParams. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'acceleration' in json_data:
      assert isinstance(json_data['acceleration'], float) or isinstance(json_data['acceleration'], int), 'Wrong type for attribute: acceleration. Expected: float. Got: ' + str(type(json_data['acceleration'])) + '.'
      obj.acceleration = json_data['acceleration']

    if 'actionName' in json_data:
      assert isinstance(json_data['actionName'], str), 'Wrong type for attribute: actionName. Expected: str. Got: ' + str(type(json_data['actionName'])) + '.'
      obj.action_name = json_data['actionName']

    if 'allowUncalibrated' in json_data:
      assert isinstance(json_data['allowUncalibrated'], bool), 'Wrong type for attribute: allowUncalibrated. Expected: bool. Got: ' + str(type(json_data['allowUncalibrated'])) + '.'
      obj.allow_uncalibrated = json_data['allowUncalibrated']

    if 'applyTipAdjustTransform' in json_data:
      assert isinstance(json_data['applyTipAdjustTransform'], bool), 'Wrong type for attribute: applyTipAdjustTransform. Expected: bool. Got: ' + str(type(json_data['applyTipAdjustTransform'])) + '.'
      obj.apply_tip_adjust_transform = json_data['applyTipAdjustTransform']

    if 'cid' in json_data:
      assert isinstance(json_data['cid'], int), 'Wrong type for attribute: cid. Expected: int. Got: ' + str(type(json_data['cid'])) + '.'
      obj.cid = json_data['cid']

    if 'command' in json_data:
      assert isinstance(json_data['command'], int), 'Wrong type for attribute: command. Expected: int. Got: ' + str(type(json_data['command'])) + '.'
      obj.command = json_data['command']

    if 'intent' in json_data:
      assert isinstance(json_data['intent'], str), 'Wrong type for attribute: intent. Expected: str. Got: ' + str(type(json_data['intent'])) + '.'
      obj.intent = json_data['intent']

    if 'jointAngles' in json_data:
      assert isinstance(json_data['jointAngles'], list), 'Wrong type for attribute: jointAngles. Expected: list. Got: ' + str(type(json_data['jointAngles'])) + '.'
      json_list = []
      for j in json_data['jointAngles']:
        json_list.append(j)
      obj.joint_angles = json_list

    if 'pickID' in json_data:
      assert isinstance(json_data['pickID'], str), 'Wrong type for attribute: pickID. Expected: str. Got: ' + str(type(json_data['pickID'])) + '.'
      obj.pick_id = json_data['pickID']

    if 'pose' in json_data:
      assert isinstance(json_data['pose'], list), 'Wrong type for attribute: pose. Expected: list. Got: ' + str(type(json_data['pose'])) + '.'
      json_list = []
      for j in json_data['pose']:
        json_list.append(j)
      obj.pose = json_list

    if 'reachAction' in json_data:
      assert isinstance(json_data['reachAction'], int), 'Wrong type for attribute: reachAction. Expected: int. Got: ' + str(type(json_data['reachAction'])) + '.'
      obj.reach_action = json_data['reachAction']

    if 'servo' in json_data:
      assert isinstance(json_data['servo'], bool), 'Wrong type for attribute: servo. Expected: bool. Got: ' + str(type(json_data['servo'])) + '.'
      obj.servo = json_data['servo']

    if 'servoGain' in json_data:
      assert isinstance(json_data['servoGain'], float) or isinstance(json_data['servoGain'], int), 'Wrong type for attribute: servoGain. Expected: float. Got: ' + str(type(json_data['servoGain'])) + '.'
      obj.servo_gain = json_data['servoGain']

    if 'servoLookaheadTimeSecs' in json_data:
      assert isinstance(json_data['servoLookaheadTimeSecs'], float) or isinstance(json_data['servoLookaheadTimeSecs'], int), 'Wrong type for attribute: servoLookaheadTimeSecs. Expected: float. Got: ' + str(type(json_data['servoLookaheadTimeSecs'])) + '.'
      obj.servo_lookahead_time_secs = json_data['servoLookaheadTimeSecs']

    if 'servoTSecs' in json_data:
      assert isinstance(json_data['servoTSecs'], float) or isinstance(json_data['servoTSecs'], int), 'Wrong type for attribute: servoTSecs. Expected: float. Got: ' + str(type(json_data['servoTSecs'])) + '.'
      obj.servo_t_secs = json_data['servoTSecs']

    if 'successType' in json_data:
      assert isinstance(json_data['successType'], str), 'Wrong type for attribute: successType. Expected: str. Got: ' + str(type(json_data['successType'])) + '.'
      obj.success_type = json_data['successType']

    if 'timeoutSec' in json_data:
      assert isinstance(json_data['timeoutSec'], float) or isinstance(json_data['timeoutSec'], int), 'Wrong type for attribute: timeoutSec. Expected: float. Got: ' + str(type(json_data['timeoutSec'])) + '.'
      obj.timeout_sec = json_data['timeoutSec']

    if 'useLinear' in json_data:
      assert isinstance(json_data['useLinear'], bool), 'Wrong type for attribute: useLinear. Expected: bool. Got: ' + str(type(json_data['useLinear'])) + '.'
      obj.use_linear = json_data['useLinear']

    if 'useUnityIk' in json_data:
      assert isinstance(json_data['useUnityIk'], bool), 'Wrong type for attribute: useUnityIk. Expected: bool. Got: ' + str(type(json_data['useUnityIk'])) + '.'
      obj.use_unity_ik = json_data['useUnityIk']

    if 'velocity' in json_data:
      assert isinstance(json_data['velocity'], float) or isinstance(json_data['velocity'], int), 'Wrong type for attribute: velocity. Expected: float. Got: ' + str(type(json_data['velocity'])) + '.'
      obj.velocity = json_data['velocity']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.ArmActionParams) -> 'ArmActionParams':
    """Convert ArmActionParams proto to type object."""
    if not proto:
      return None
    obj = ArmActionParams()
    obj.acceleration = get_proto_value(proto.acceleration)
    obj.action_name = get_proto_value(proto.action_name)
    obj.allow_uncalibrated = get_proto_value(proto.allow_uncalibrated)
    obj.apply_tip_adjust_transform = get_proto_value(proto.apply_tip_adjust_transform)
    obj.cid = get_proto_value(proto.cid)
    obj.command = get_proto_value(proto.command)
    obj.intent = get_proto_value(proto.intent)
    if proto.joint_angles:
      json_list = []
      for j in proto.joint_angles:
        json_list.append(j)
      obj.joint_angles = json_list
    obj.pick_id = get_proto_value(proto.pick_id)
    if proto.pose:
      json_list = []
      for j in proto.pose:
        json_list.append(j)
      obj.pose = json_list
    obj.reach_action = get_proto_value(proto.reach_action)
    obj.servo = get_proto_value(proto.servo)
    obj.servo_gain = get_proto_value(proto.servo_gain)
    obj.servo_lookahead_time_secs = get_proto_value(proto.servo_lookahead_time_secs)
    obj.servo_t_secs = get_proto_value(proto.servo_t_secs)
    obj.success_type = get_proto_value(proto.success_type)
    obj.timeout_sec = get_proto_value(proto.timeout_sec)
    obj.use_linear = get_proto_value(proto.use_linear)
    obj.use_unity_ik = get_proto_value(proto.use_unity_ik)
    obj.velocity = get_proto_value(proto.velocity)
    return obj


class AudioRequest:
  """Representation of proto message AudioRequest.

   AudioRequest is used for audio mute and unmute requests.

   For more details, see design doc:
  """
  text_cue: str

  def __init__(self, text_cue: str = '') -> None:
    self.text_cue = text_cue

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.text_cue:
      assert isinstance(self.text_cue, str), 'Wrong type for attribute: text_cue. Expected: str. Got: ' + str(type(self.text_cue)) + '.'
      json_data['textCue'] = self.text_cue

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'AudioRequest':
    """Convert JSON to type object."""
    obj = AudioRequest()

    expected_json_keys: List[str] = ['textCue']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid AudioRequest. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'textCue' in json_data:
      assert isinstance(json_data['textCue'], str), 'Wrong type for attribute: textCue. Expected: str. Got: ' + str(type(json_data['textCue'])) + '.'
      obj.text_cue = json_data['textCue']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.AudioRequest) -> 'AudioRequest':
    """Convert AudioRequest proto to type object."""
    if not proto:
      return None
    obj = AudioRequest()
    obj.text_cue = get_proto_value(proto.text_cue)
    return obj


class CameraShiftDetection:
  """Representation of proto message CameraShiftDetection.

   CameraShiftDetection is a submessage of Detection, that encodes existence
   and degree of any detected shift of the camera itself.
  """
  # Amount of the maximum shift observed on any static id in pixels.
  max_shift: float

  # The object on which the maximum shift was observed.
  max_shift_object: Optional['DetectionKey']

  # All different shift detections.
  shifts_per_detection: List['ShiftPerDetection']

  def __init__(self, max_shift: float = 0.0, max_shift_object: Optional['DetectionKey'] = None, shifts_per_detection: Optional[List['ShiftPerDetection']] = None) -> None:
    self.max_shift = max_shift
    self.max_shift_object = max_shift_object
    if shifts_per_detection is None:
      self.shifts_per_detection = []
    else:
      self.shifts_per_detection = shifts_per_detection

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.max_shift:
      assert isinstance(self.max_shift, float) or isinstance(self.max_shift, int), 'Wrong type for attribute: max_shift. Expected: float. Got: ' + str(type(self.max_shift)) + '.'
      json_data['maxShift'] = self.max_shift

    if self.max_shift_object:
      assert self.max_shift_object.__class__.__name__ == 'DetectionKey', 'Wrong type for attribute: max_shift_object. Expected: DetectionKey. Got: ' + str(type(self.max_shift_object)) + '.'
      json_data['maxShiftObject'] = self.max_shift_object.to_json()

    if self.shifts_per_detection:
      assert isinstance(self.shifts_per_detection, list), 'Wrong type for attribute: shifts_per_detection. Expected: list. Got: ' + str(type(self.shifts_per_detection)) + '.'
      obj_list = []
      for item in self.shifts_per_detection:
        obj_list.append(item.to_json())
      json_data['shiftsPerDetection'] = obj_list

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'CameraShiftDetection':
    """Convert JSON to type object."""
    obj = CameraShiftDetection()
    json_list: List[Any]

    expected_json_keys: List[str] = ['maxShift', 'maxShiftObject', 'shiftsPerDetection']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid CameraShiftDetection. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'maxShift' in json_data:
      assert isinstance(json_data['maxShift'], float) or isinstance(json_data['maxShift'], int), 'Wrong type for attribute: maxShift. Expected: float. Got: ' + str(type(json_data['maxShift'])) + '.'
      obj.max_shift = json_data['maxShift']

    if 'maxShiftObject' in json_data:
      assert isinstance(json_data['maxShiftObject'], dict), 'Wrong type for attribute: maxShiftObject. Expected: dict. Got: ' + str(type(json_data['maxShiftObject'])) + '.'
      obj.max_shift_object = DetectionKey.from_json(json_data['maxShiftObject'])

    if 'shiftsPerDetection' in json_data:
      assert isinstance(json_data['shiftsPerDetection'], list), 'Wrong type for attribute: shiftsPerDetection. Expected: list. Got: ' + str(type(json_data['shiftsPerDetection'])) + '.'
      json_list = []
      for j in json_data['shiftsPerDetection']:
        json_list.append(ShiftPerDetection.from_json(j))
      obj.shifts_per_detection = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.CameraShiftDetection) -> 'CameraShiftDetection':
    """Convert CameraShiftDetection proto to type object."""
    if not proto:
      return None
    obj = CameraShiftDetection()
    obj.max_shift = get_proto_value(proto.max_shift)
    obj.max_shift_object = DetectionKey.from_proto(get_proto_field(proto, 'max_shift_object'))
    if proto.shifts_per_detection:
      json_list = []
      for j in proto.shifts_per_detection:
        json_list.append(ShiftPerDetection.from_proto(j))
      obj.shifts_per_detection = json_list
    return obj


class CapabilityState:
  """Representation of proto message CapabilityState.

   CapabilityState represents the state of one pin in a workcell capability.

   For more details, see the design doc at
  """
  # The pin name within the capability (if any).
  pin: str

  # for integer and digital outputs. Digital outputs are
  # non-zero: activate, zero: deactivate
  int_value: int

  # for analog outputs
  float_value: float

  def __init__(self, float_value: float = 0.0, int_value: int = 0, pin: str = '') -> None:
    self.float_value = float_value
    self.int_value = int_value
    self.pin = pin

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.float_value:
      assert isinstance(self.float_value, float) or isinstance(self.float_value, int), 'Wrong type for attribute: float_value. Expected: float. Got: ' + str(type(self.float_value)) + '.'
      json_data['floatValue'] = self.float_value

    if self.int_value:
      assert isinstance(self.int_value, int), 'Wrong type for attribute: int_value. Expected: int. Got: ' + str(type(self.int_value)) + '.'
      json_data['intValue'] = self.int_value

    if self.pin:
      assert isinstance(self.pin, str), 'Wrong type for attribute: pin. Expected: str. Got: ' + str(type(self.pin)) + '.'
      json_data['pin'] = self.pin

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'CapabilityState':
    """Convert JSON to type object."""
    obj = CapabilityState()

    expected_json_keys: List[str] = ['floatValue', 'intValue', 'pin']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid CapabilityState. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'floatValue' in json_data:
      assert isinstance(json_data['floatValue'], float) or isinstance(json_data['floatValue'], int), 'Wrong type for attribute: floatValue. Expected: float. Got: ' + str(type(json_data['floatValue'])) + '.'
      obj.float_value = json_data['floatValue']

    if 'intValue' in json_data:
      assert isinstance(json_data['intValue'], int), 'Wrong type for attribute: intValue. Expected: int. Got: ' + str(type(json_data['intValue'])) + '.'
      obj.int_value = json_data['intValue']

    if 'pin' in json_data:
      assert isinstance(json_data['pin'], str), 'Wrong type for attribute: pin. Expected: str. Got: ' + str(type(json_data['pin'])) + '.'
      obj.pin = json_data['pin']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.CapabilityState) -> 'CapabilityState':
    """Convert CapabilityState proto to type object."""
    if not proto:
      return None
    obj = CapabilityState()
    obj.float_value = get_proto_value(proto.float_value)
    obj.int_value = get_proto_value(proto.int_value)
    obj.pin = get_proto_value(proto.pin)
    return obj


class ClientAnnotation:
  """Representation of proto message ClientAnnotation.

   ClientAnnotation is the message type for extra log messages from control
   sessions.
  """
  #
  # The associatedServerTS is server timestamp (TS value) of the most recent
  # message that caused this log to be emitted. The associatedServerTS is set
  # by the client emitting the log message.
  associated_server_ts: int

  # The channel ID this log message is associated with. If empty, it is
  # associated with the "device-data" channel.
  log_channel_id: str
  interval_start: Optional['IntervalStart']
  interval_end: Optional['IntervalEnd']

  def __init__(self, associated_server_ts: int = 0, interval_end: Optional['IntervalEnd'] = None, interval_start: Optional['IntervalStart'] = None, log_channel_id: str = '') -> None:
    self.associated_server_ts = associated_server_ts
    self.interval_end = interval_end
    self.interval_start = interval_start
    self.log_channel_id = log_channel_id

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.associated_server_ts:
      assert isinstance(self.associated_server_ts, int), 'Wrong type for attribute: associated_server_ts. Expected: int. Got: ' + str(type(self.associated_server_ts)) + '.'
      json_data['associatedServerTS'] = self.associated_server_ts

    if self.interval_end:
      assert self.interval_end.__class__.__name__ == 'IntervalEnd', 'Wrong type for attribute: interval_end. Expected: IntervalEnd. Got: ' + str(type(self.interval_end)) + '.'
      json_data['intervalEnd'] = self.interval_end.to_json()

    if self.interval_start:
      assert self.interval_start.__class__.__name__ == 'IntervalStart', 'Wrong type for attribute: interval_start. Expected: IntervalStart. Got: ' + str(type(self.interval_start)) + '.'
      json_data['intervalStart'] = self.interval_start.to_json()

    if self.log_channel_id:
      assert isinstance(self.log_channel_id, str), 'Wrong type for attribute: log_channel_id. Expected: str. Got: ' + str(type(self.log_channel_id)) + '.'
      json_data['logChannelID'] = self.log_channel_id

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'ClientAnnotation':
    """Convert JSON to type object."""
    obj = ClientAnnotation()

    expected_json_keys: List[str] = ['associatedServerTS', 'intervalEnd', 'intervalStart', 'logChannelID']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid ClientAnnotation. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'associatedServerTS' in json_data:
      assert isinstance(json_data['associatedServerTS'], int), 'Wrong type for attribute: associatedServerTS. Expected: int. Got: ' + str(type(json_data['associatedServerTS'])) + '.'
      obj.associated_server_ts = json_data['associatedServerTS']

    if 'intervalEnd' in json_data:
      assert isinstance(json_data['intervalEnd'], dict), 'Wrong type for attribute: intervalEnd. Expected: dict. Got: ' + str(type(json_data['intervalEnd'])) + '.'
      obj.interval_end = IntervalEnd.from_json(json_data['intervalEnd'])

    if 'intervalStart' in json_data:
      assert isinstance(json_data['intervalStart'], dict), 'Wrong type for attribute: intervalStart. Expected: dict. Got: ' + str(type(json_data['intervalStart'])) + '.'
      obj.interval_start = IntervalStart.from_json(json_data['intervalStart'])

    if 'logChannelID' in json_data:
      assert isinstance(json_data['logChannelID'], str), 'Wrong type for attribute: logChannelID. Expected: str. Got: ' + str(type(json_data['logChannelID'])) + '.'
      obj.log_channel_id = json_data['logChannelID']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.ClientAnnotation) -> 'ClientAnnotation':
    """Convert ClientAnnotation proto to type object."""
    if not proto:
      return None
    obj = ClientAnnotation()
    obj.associated_server_ts = get_proto_value(proto.associated_server_ts)
    obj.interval_end = IntervalEnd.from_proto(get_proto_field(proto, 'interval_end'))
    obj.interval_start = IntervalStart.from_proto(get_proto_field(proto, 'interval_start'))
    obj.log_channel_id = get_proto_value(proto.log_channel_id)
    return obj


class ClientSessionStart:
  """Representation of proto message ClientSessionStart.

   ClientSessionStart is the start of a client session.
  """
  # AcceptDepthEncoding is a list
  accept_depth_encoding: List[str]

  def __init__(self, accept_depth_encoding: Optional[List[str]] = None) -> None:
    if accept_depth_encoding is None:
      self.accept_depth_encoding = []
    else:
      self.accept_depth_encoding = accept_depth_encoding

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.accept_depth_encoding:
      assert isinstance(self.accept_depth_encoding, list), 'Wrong type for attribute: accept_depth_encoding. Expected: list. Got: ' + str(type(self.accept_depth_encoding)) + '.'
      json_data['acceptDepthEncoding'] = self.accept_depth_encoding

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'ClientSessionStart':
    """Convert JSON to type object."""
    obj = ClientSessionStart()
    json_list: List[Any]

    expected_json_keys: List[str] = ['acceptDepthEncoding']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid ClientSessionStart. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'acceptDepthEncoding' in json_data:
      assert isinstance(json_data['acceptDepthEncoding'], list), 'Wrong type for attribute: acceptDepthEncoding. Expected: list. Got: ' + str(type(json_data['acceptDepthEncoding'])) + '.'
      json_list = []
      for j in json_data['acceptDepthEncoding']:
        json_list.append(j)
      obj.accept_depth_encoding = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.ClientSessionStart) -> 'ClientSessionStart':
    """Convert ClientSessionStart proto to type object."""
    if not proto:
      return None
    obj = ClientSessionStart()
    if proto.accept_depth_encoding:
      json_list = []
      for j in proto.accept_depth_encoding:
        json_list.append(j)
      obj.accept_depth_encoding = json_list
    return obj


class CommandData:
  """Representation of proto message CommandData.

   Command data, representing commands received from clients.
   See the corresponding file in the Project Reach source code:
   project-reach/go/src/project-reach/pkg/rc/types.go
  """
  # The type of device to deliver this command to, such as photoneo.
  device_type: str

  # Which device the command is coming to. Usually, the deviceType is
  # sufficient to infer what device is being used, but the name disambiguates
  # cases where multiple devices of the same type are used in a robot system.
  # This field may be empty / omitted, if no other device of this type is
  # on the system.
  device_name: str

  # The command data type such as frame-request or reach-script.
  # Please, refer to go/reach-system for more examples.
  data_type: str
  tag: str

  # A Unix timestamp, in milliseconds.
  ts: int
  origin: str
  origin_type: str
  origin_transport_type: str
  origin_client: str
  origin_control: str
  seq: int

  # === Fields for dataType snapshot:
  snapshot: Optional['Snapshot']
  # ==============================

  # === Fields for dataType metadata:

  # Metadata will be used for log file open/close purposes
  metadata: Optional['Metadata']
  # ==============================

  # === Fields for dataType key-value:
  key: str
  value: str
  int_value: int
  float_value: float
  # ==============================

  # === Fields for dataType key-value-request:
  # (also field key)
  # (also field value)
  # (also field int_value)
  # (also field float_value)
  # ==============================

  # === Fields for dataType session-info:

  # session-info data.
  session_info: Optional['SessionInfo']
  # ==============================

  # === Fields for dataType trigger:
  # (no fields)
  # ==============================

  # === Fields for dataType start-shutdown:
  # (no fields)
  # ==============================

  # === Fields for dataType finish-shutdown:
  # (no fields)
  # ==============================

  # === Fields for dataType hangup:
  # (no fields)
  # ==============================

  # === Fields for dataType client-session-start:
  client_session_start: Optional['ClientSessionStart']
  # ==============================

  # === Fields for dataType client-annotation:

  # ClientAnnotation messages and custom log intervals.
  #
  client_annotation: Optional['ClientAnnotation']
  # ==============================

  # === Fields for dataType pipeline-description-request:
  # (no fields)
  # ==============================

  # === Fields for dataType machine-interfaces-request:
  # (no fields)
  # ==============================

  # === Fields for dataType text-instruction-request:
  # (no fields)
  # ==============================

  # The text of the script to run, if the command is run-script.
  script: str

  # === Fields for dataType reach-script:
  reach_script: Optional['ReachScript']
  # ==============================

  # Which command to execute: run-script, clear-stop.
  cmd: str
  args: List[str]
  progress: float
  message: str
  error: str
  detailed_error: str

  # Intent and success_type indicate the method of success detection.
  intent: str
  success_type: str
  x: float
  y: float

  # exp is the original experimental command data for one step actions.
  exp: Optional['ExperimentalCommandData']

  # exp_array is a list of experimental command data for use in multiple step
  # actions like pick and place.
  exp_array: List['ExperimentalCommandData']

  # Information about an event. This data can contain information about when
  # a session ended, as well as the total duration of the session.
  # The total duration of the event.
  event_duration: float

  # The name of the event.
  event_name: str

  # Labels associated with the event.
  event_labels: List[str]
  event_params: List['KeyValue']

  # pickID associates an attempt command/metric to a success.
  pick_id: str
  experiment_token: str

  # === Fields for dataType history:

  # history passes the request to fetch settings config history.
  #
  # For more details, see design doc:
  history: Optional['History']
  # ==============================

  # text_cue is used for audio mute and unmute requests.
  #
  text_cue: str

  # === Fields for dataType webrtc-audio-request:

  # WebrtcAudioRequest is used in a command of dataType "webrtc-audio-request",
  # an internal message for setting mute/unmute status in webrtc.
  #
  webrtc_audio_request: Optional['WebrtcAudioRequest']
  # ==============================

  # === Fields for dataType sim-action:
  sim_action: Optional['SimAction']
  # ==============================

  # === Fields for dataType inference-request:
  # The prediction type to execute. This is approximatly mapped to a model
  # type (although one model may handle multiple request types).
  # Oneof ["ModelPick", "ModelPickAndPlace"].
  prediction_type: str

  # request_type: "sparse" will send a single inference result and wait for
  # another. In the future we will support "continuous" requests will send
  # inference results continuously following the initial request, until "stop"
  # is sent. Oneof ["sparse"], future support: ["continuous", “stop”].
  request_type: str

  # task_code: e.g. TC-101.
  task_code: str
  # (also field intent)

  # label: e.g. SingulateRightBin.
  label: str

  # robot_id: e.g. reach07.
  robot_id: str
  # ==============================

  def __init__(self, args: Optional[List[str]] = None, client_annotation: Optional['ClientAnnotation'] = None, client_session_start: Optional['ClientSessionStart'] = None, cmd: str = '', data_type: str = '', detailed_error: str = '', device_name: str = '', device_type: str = '', error: str = '', event_duration: float = 0.0, event_labels: Optional[List[str]] = None, event_name: str = '', event_params: Optional[List['KeyValue']] = None, exp: Optional['ExperimentalCommandData'] = None, exp_array: Optional[List['ExperimentalCommandData']] = None, experiment_token: str = '', float_value: float = 0.0, history: Optional['History'] = None, int_value: int = 0, intent: str = '', key: str = '', label: str = '', message: str = '', metadata: Optional['Metadata'] = None, origin: str = '', origin_client: str = '', origin_control: str = '', origin_transport_type: str = '', origin_type: str = '', pick_id: str = '', prediction_type: str = '', progress: float = 0.0, reach_script: Optional['ReachScript'] = None, request_type: str = '', robot_id: str = '', script: str = '', seq: int = 0, session_info: Optional['SessionInfo'] = None, sim_action: Optional['SimAction'] = None, snapshot: Optional['Snapshot'] = None, success_type: str = '', tag: str = '', task_code: str = '', text_cue: str = '', ts: int = 0, value: str = '', webrtc_audio_request: Optional['WebrtcAudioRequest'] = None, x: float = 0.0, y: float = 0.0) -> None:
    if args is None:
      self.args = []
    else:
      self.args = args
    self.client_annotation = client_annotation
    self.client_session_start = client_session_start
    self.cmd = cmd
    self.data_type = data_type
    self.detailed_error = detailed_error
    self.device_name = device_name
    self.device_type = device_type
    self.error = error
    self.event_duration = event_duration
    if event_labels is None:
      self.event_labels = []
    else:
      self.event_labels = event_labels
    self.event_name = event_name
    if event_params is None:
      self.event_params = []
    else:
      self.event_params = event_params
    self.exp = exp
    if exp_array is None:
      self.exp_array = []
    else:
      self.exp_array = exp_array
    self.experiment_token = experiment_token
    self.float_value = float_value
    self.history = history
    self.int_value = int_value
    self.intent = intent
    self.key = key
    self.label = label
    self.message = message
    self.metadata = metadata
    self.origin = origin
    self.origin_client = origin_client
    self.origin_control = origin_control
    self.origin_transport_type = origin_transport_type
    self.origin_type = origin_type
    self.pick_id = pick_id
    self.prediction_type = prediction_type
    self.progress = progress
    self.reach_script = reach_script
    self.request_type = request_type
    self.robot_id = robot_id
    self.script = script
    self.seq = seq
    self.session_info = session_info
    self.sim_action = sim_action
    self.snapshot = snapshot
    self.success_type = success_type
    self.tag = tag
    self.task_code = task_code
    self.text_cue = text_cue
    self.ts = ts
    self.value = value
    self.webrtc_audio_request = webrtc_audio_request
    self.x = x
    self.y = y

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.args:
      assert isinstance(self.args, list), 'Wrong type for attribute: args. Expected: list. Got: ' + str(type(self.args)) + '.'
      json_data['args'] = self.args

    if self.client_annotation:
      assert self.client_annotation.__class__.__name__ == 'ClientAnnotation', 'Wrong type for attribute: client_annotation. Expected: ClientAnnotation. Got: ' + str(type(self.client_annotation)) + '.'
      json_data['clientAnnotation'] = self.client_annotation.to_json()

    if self.client_session_start:
      assert self.client_session_start.__class__.__name__ == 'ClientSessionStart', 'Wrong type for attribute: client_session_start. Expected: ClientSessionStart. Got: ' + str(type(self.client_session_start)) + '.'
      json_data['clientSessionStart'] = self.client_session_start.to_json()

    if self.cmd:
      assert isinstance(self.cmd, str), 'Wrong type for attribute: cmd. Expected: str. Got: ' + str(type(self.cmd)) + '.'
      json_data['cmd'] = self.cmd

    if self.data_type:
      assert isinstance(self.data_type, str), 'Wrong type for attribute: data_type. Expected: str. Got: ' + str(type(self.data_type)) + '.'
      json_data['dataType'] = self.data_type

    if self.detailed_error:
      assert isinstance(self.detailed_error, str), 'Wrong type for attribute: detailed_error. Expected: str. Got: ' + str(type(self.detailed_error)) + '.'
      json_data['detailedError'] = self.detailed_error

    if self.device_name:
      assert isinstance(self.device_name, str), 'Wrong type for attribute: device_name. Expected: str. Got: ' + str(type(self.device_name)) + '.'
      json_data['deviceName'] = self.device_name

    if self.device_type:
      assert isinstance(self.device_type, str), 'Wrong type for attribute: device_type. Expected: str. Got: ' + str(type(self.device_type)) + '.'
      json_data['deviceType'] = self.device_type

    if self.error:
      assert isinstance(self.error, str), 'Wrong type for attribute: error. Expected: str. Got: ' + str(type(self.error)) + '.'
      json_data['error'] = self.error

    if self.event_duration:
      assert isinstance(self.event_duration, float) or isinstance(self.event_duration, int), 'Wrong type for attribute: event_duration. Expected: float. Got: ' + str(type(self.event_duration)) + '.'
      json_data['eventDuration'] = self.event_duration

    if self.event_labels:
      assert isinstance(self.event_labels, list), 'Wrong type for attribute: event_labels. Expected: list. Got: ' + str(type(self.event_labels)) + '.'
      json_data['eventLabels'] = self.event_labels

    if self.event_name:
      assert isinstance(self.event_name, str), 'Wrong type for attribute: event_name. Expected: str. Got: ' + str(type(self.event_name)) + '.'
      json_data['eventName'] = self.event_name

    if self.event_params:
      assert isinstance(self.event_params, list), 'Wrong type for attribute: event_params. Expected: list. Got: ' + str(type(self.event_params)) + '.'
      obj_list = []
      for item in self.event_params:
        obj_list.append(item.to_json())
      json_data['eventParams'] = obj_list

    if self.exp:
      assert self.exp.__class__.__name__ == 'ExperimentalCommandData', 'Wrong type for attribute: exp. Expected: ExperimentalCommandData. Got: ' + str(type(self.exp)) + '.'
      json_data['exp'] = self.exp.to_json()

    if self.exp_array:
      assert isinstance(self.exp_array, list), 'Wrong type for attribute: exp_array. Expected: list. Got: ' + str(type(self.exp_array)) + '.'
      obj_list = []
      for item in self.exp_array:
        obj_list.append(item.to_json())
      json_data['expArray'] = obj_list

    if self.experiment_token:
      assert isinstance(self.experiment_token, str), 'Wrong type for attribute: experiment_token. Expected: str. Got: ' + str(type(self.experiment_token)) + '.'
      json_data['experimentToken'] = self.experiment_token

    if self.float_value:
      assert isinstance(self.float_value, float) or isinstance(self.float_value, int), 'Wrong type for attribute: float_value. Expected: float. Got: ' + str(type(self.float_value)) + '.'
      json_data['floatValue'] = self.float_value

    if self.history:
      assert self.history.__class__.__name__ == 'History', 'Wrong type for attribute: history. Expected: History. Got: ' + str(type(self.history)) + '.'
      json_data['history'] = self.history.to_json()

    if self.int_value:
      assert isinstance(self.int_value, int), 'Wrong type for attribute: int_value. Expected: int. Got: ' + str(type(self.int_value)) + '.'
      json_data['intValue'] = self.int_value

    if self.intent:
      assert isinstance(self.intent, str), 'Wrong type for attribute: intent. Expected: str. Got: ' + str(type(self.intent)) + '.'
      json_data['intent'] = self.intent

    if self.key:
      assert isinstance(self.key, str), 'Wrong type for attribute: key. Expected: str. Got: ' + str(type(self.key)) + '.'
      json_data['key'] = self.key

    if self.label:
      assert isinstance(self.label, str), 'Wrong type for attribute: label. Expected: str. Got: ' + str(type(self.label)) + '.'
      json_data['label'] = self.label

    if self.message:
      assert isinstance(self.message, str), 'Wrong type for attribute: message. Expected: str. Got: ' + str(type(self.message)) + '.'
      json_data['message'] = self.message

    if self.metadata:
      assert self.metadata.__class__.__name__ == 'Metadata', 'Wrong type for attribute: metadata. Expected: Metadata. Got: ' + str(type(self.metadata)) + '.'
      json_data['metadata'] = self.metadata.to_json()

    if self.origin:
      assert isinstance(self.origin, str), 'Wrong type for attribute: origin. Expected: str. Got: ' + str(type(self.origin)) + '.'
      json_data['origin'] = self.origin

    if self.origin_client:
      assert isinstance(self.origin_client, str), 'Wrong type for attribute: origin_client. Expected: str. Got: ' + str(type(self.origin_client)) + '.'
      json_data['originClient'] = self.origin_client

    if self.origin_control:
      assert isinstance(self.origin_control, str), 'Wrong type for attribute: origin_control. Expected: str. Got: ' + str(type(self.origin_control)) + '.'
      json_data['originControl'] = self.origin_control

    if self.origin_transport_type:
      assert isinstance(self.origin_transport_type, str), 'Wrong type for attribute: origin_transport_type. Expected: str. Got: ' + str(type(self.origin_transport_type)) + '.'
      json_data['originTransportType'] = self.origin_transport_type

    if self.origin_type:
      assert isinstance(self.origin_type, str), 'Wrong type for attribute: origin_type. Expected: str. Got: ' + str(type(self.origin_type)) + '.'
      json_data['originType'] = self.origin_type

    if self.pick_id:
      assert isinstance(self.pick_id, str), 'Wrong type for attribute: pick_id. Expected: str. Got: ' + str(type(self.pick_id)) + '.'
      json_data['pickID'] = self.pick_id

    if self.prediction_type:
      assert isinstance(self.prediction_type, str), 'Wrong type for attribute: prediction_type. Expected: str. Got: ' + str(type(self.prediction_type)) + '.'
      json_data['predictionType'] = self.prediction_type

    if self.progress:
      assert isinstance(self.progress, float) or isinstance(self.progress, int), 'Wrong type for attribute: progress. Expected: float. Got: ' + str(type(self.progress)) + '.'
      json_data['progress'] = self.progress

    if self.reach_script:
      assert self.reach_script.__class__.__name__ == 'ReachScript', 'Wrong type for attribute: reach_script. Expected: ReachScript. Got: ' + str(type(self.reach_script)) + '.'
      json_data['reachScript'] = self.reach_script.to_json()

    if self.request_type:
      assert isinstance(self.request_type, str), 'Wrong type for attribute: request_type. Expected: str. Got: ' + str(type(self.request_type)) + '.'
      json_data['requestType'] = self.request_type

    if self.robot_id:
      assert isinstance(self.robot_id, str), 'Wrong type for attribute: robot_id. Expected: str. Got: ' + str(type(self.robot_id)) + '.'
      json_data['robotID'] = self.robot_id

    if self.script:
      assert isinstance(self.script, str), 'Wrong type for attribute: script. Expected: str. Got: ' + str(type(self.script)) + '.'
      json_data['script'] = self.script

    if self.seq:
      assert isinstance(self.seq, int), 'Wrong type for attribute: seq. Expected: int. Got: ' + str(type(self.seq)) + '.'
      json_data['seq'] = self.seq

    if self.session_info:
      assert self.session_info.__class__.__name__ == 'SessionInfo', 'Wrong type for attribute: session_info. Expected: SessionInfo. Got: ' + str(type(self.session_info)) + '.'
      json_data['sessionInfo'] = self.session_info.to_json()

    if self.sim_action:
      assert self.sim_action.__class__.__name__ == 'SimAction', 'Wrong type for attribute: sim_action. Expected: SimAction. Got: ' + str(type(self.sim_action)) + '.'
      json_data['simAction'] = self.sim_action.to_json()

    if self.snapshot:
      assert self.snapshot.__class__.__name__ == 'Snapshot', 'Wrong type for attribute: snapshot. Expected: Snapshot. Got: ' + str(type(self.snapshot)) + '.'
      json_data['snapshot'] = self.snapshot.to_json()

    if self.success_type:
      assert isinstance(self.success_type, str), 'Wrong type for attribute: success_type. Expected: str. Got: ' + str(type(self.success_type)) + '.'
      json_data['successType'] = self.success_type

    if self.tag:
      assert isinstance(self.tag, str), 'Wrong type for attribute: tag. Expected: str. Got: ' + str(type(self.tag)) + '.'
      json_data['tag'] = self.tag

    if self.task_code:
      assert isinstance(self.task_code, str), 'Wrong type for attribute: task_code. Expected: str. Got: ' + str(type(self.task_code)) + '.'
      json_data['taskCode'] = self.task_code

    if self.text_cue:
      assert isinstance(self.text_cue, str), 'Wrong type for attribute: text_cue. Expected: str. Got: ' + str(type(self.text_cue)) + '.'
      json_data['textCue'] = self.text_cue

    if self.ts:
      assert isinstance(self.ts, int), 'Wrong type for attribute: ts. Expected: int. Got: ' + str(type(self.ts)) + '.'
      json_data['ts'] = self.ts

    if self.value:
      assert isinstance(self.value, str), 'Wrong type for attribute: value. Expected: str. Got: ' + str(type(self.value)) + '.'
      json_data['value'] = self.value

    if self.webrtc_audio_request:
      assert self.webrtc_audio_request.__class__.__name__ == 'WebrtcAudioRequest', 'Wrong type for attribute: webrtc_audio_request. Expected: WebrtcAudioRequest. Got: ' + str(type(self.webrtc_audio_request)) + '.'
      json_data['webrtcAudioRequest'] = self.webrtc_audio_request.to_json()

    if self.x:
      assert isinstance(self.x, float) or isinstance(self.x, int), 'Wrong type for attribute: x. Expected: float. Got: ' + str(type(self.x)) + '.'
      json_data['x'] = self.x

    if self.y:
      assert isinstance(self.y, float) or isinstance(self.y, int), 'Wrong type for attribute: y. Expected: float. Got: ' + str(type(self.y)) + '.'
      json_data['y'] = self.y

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'CommandData':
    """Convert JSON to type object."""
    obj = CommandData()
    json_list: List[Any]

    expected_json_keys: List[str] = ['args', 'clientAnnotation', 'clientSessionStart', 'cmd', 'dataType', 'detailedError', 'deviceName', 'deviceType', 'error', 'eventDuration', 'eventLabels', 'eventName', 'eventParams', 'exp', 'expArray', 'experimentToken', 'floatValue', 'history', 'intValue', 'intent', 'key', 'label', 'message', 'metadata', 'origin', 'originClient', 'originControl', 'originTransportType', 'originType', 'pickID', 'predictionType', 'progress', 'reachScript', 'requestType', 'robotID', 'script', 'seq', 'sessionInfo', 'simAction', 'snapshot', 'successType', 'tag', 'taskCode', 'textCue', 'ts', 'value', 'webrtcAudioRequest', 'x', 'y']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid CommandData. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'args' in json_data:
      assert isinstance(json_data['args'], list), 'Wrong type for attribute: args. Expected: list. Got: ' + str(type(json_data['args'])) + '.'
      json_list = []
      for j in json_data['args']:
        json_list.append(j)
      obj.args = json_list

    if 'clientAnnotation' in json_data:
      assert isinstance(json_data['clientAnnotation'], dict), 'Wrong type for attribute: clientAnnotation. Expected: dict. Got: ' + str(type(json_data['clientAnnotation'])) + '.'
      obj.client_annotation = ClientAnnotation.from_json(json_data['clientAnnotation'])

    if 'clientSessionStart' in json_data:
      assert isinstance(json_data['clientSessionStart'], dict), 'Wrong type for attribute: clientSessionStart. Expected: dict. Got: ' + str(type(json_data['clientSessionStart'])) + '.'
      obj.client_session_start = ClientSessionStart.from_json(json_data['clientSessionStart'])

    if 'cmd' in json_data:
      assert isinstance(json_data['cmd'], str), 'Wrong type for attribute: cmd. Expected: str. Got: ' + str(type(json_data['cmd'])) + '.'
      obj.cmd = json_data['cmd']

    if 'dataType' in json_data:
      assert isinstance(json_data['dataType'], str), 'Wrong type for attribute: dataType. Expected: str. Got: ' + str(type(json_data['dataType'])) + '.'
      obj.data_type = json_data['dataType']

    if 'detailedError' in json_data:
      assert isinstance(json_data['detailedError'], str), 'Wrong type for attribute: detailedError. Expected: str. Got: ' + str(type(json_data['detailedError'])) + '.'
      obj.detailed_error = json_data['detailedError']

    if 'deviceName' in json_data:
      assert isinstance(json_data['deviceName'], str), 'Wrong type for attribute: deviceName. Expected: str. Got: ' + str(type(json_data['deviceName'])) + '.'
      obj.device_name = json_data['deviceName']

    if 'deviceType' in json_data:
      assert isinstance(json_data['deviceType'], str), 'Wrong type for attribute: deviceType. Expected: str. Got: ' + str(type(json_data['deviceType'])) + '.'
      obj.device_type = json_data['deviceType']

    if 'error' in json_data:
      assert isinstance(json_data['error'], str), 'Wrong type for attribute: error. Expected: str. Got: ' + str(type(json_data['error'])) + '.'
      obj.error = json_data['error']

    if 'eventDuration' in json_data:
      assert isinstance(json_data['eventDuration'], float) or isinstance(json_data['eventDuration'], int), 'Wrong type for attribute: eventDuration. Expected: float. Got: ' + str(type(json_data['eventDuration'])) + '.'
      obj.event_duration = json_data['eventDuration']

    if 'eventLabels' in json_data:
      assert isinstance(json_data['eventLabels'], list), 'Wrong type for attribute: eventLabels. Expected: list. Got: ' + str(type(json_data['eventLabels'])) + '.'
      json_list = []
      for j in json_data['eventLabels']:
        json_list.append(j)
      obj.event_labels = json_list

    if 'eventName' in json_data:
      assert isinstance(json_data['eventName'], str), 'Wrong type for attribute: eventName. Expected: str. Got: ' + str(type(json_data['eventName'])) + '.'
      obj.event_name = json_data['eventName']

    if 'eventParams' in json_data:
      assert isinstance(json_data['eventParams'], list), 'Wrong type for attribute: eventParams. Expected: list. Got: ' + str(type(json_data['eventParams'])) + '.'
      json_list = []
      for j in json_data['eventParams']:
        json_list.append(KeyValue.from_json(j))
      obj.event_params = json_list

    if 'exp' in json_data:
      assert isinstance(json_data['exp'], dict), 'Wrong type for attribute: exp. Expected: dict. Got: ' + str(type(json_data['exp'])) + '.'
      obj.exp = ExperimentalCommandData.from_json(json_data['exp'])

    if 'expArray' in json_data:
      assert isinstance(json_data['expArray'], list), 'Wrong type for attribute: expArray. Expected: list. Got: ' + str(type(json_data['expArray'])) + '.'
      json_list = []
      for j in json_data['expArray']:
        json_list.append(ExperimentalCommandData.from_json(j))
      obj.exp_array = json_list

    if 'experimentToken' in json_data:
      assert isinstance(json_data['experimentToken'], str), 'Wrong type for attribute: experimentToken. Expected: str. Got: ' + str(type(json_data['experimentToken'])) + '.'
      obj.experiment_token = json_data['experimentToken']

    if 'floatValue' in json_data:
      assert isinstance(json_data['floatValue'], float) or isinstance(json_data['floatValue'], int), 'Wrong type for attribute: floatValue. Expected: float. Got: ' + str(type(json_data['floatValue'])) + '.'
      obj.float_value = json_data['floatValue']

    if 'history' in json_data:
      assert isinstance(json_data['history'], dict), 'Wrong type for attribute: history. Expected: dict. Got: ' + str(type(json_data['history'])) + '.'
      obj.history = History.from_json(json_data['history'])

    if 'intValue' in json_data:
      assert isinstance(json_data['intValue'], int), 'Wrong type for attribute: intValue. Expected: int. Got: ' + str(type(json_data['intValue'])) + '.'
      obj.int_value = json_data['intValue']

    if 'intent' in json_data:
      assert isinstance(json_data['intent'], str), 'Wrong type for attribute: intent. Expected: str. Got: ' + str(type(json_data['intent'])) + '.'
      obj.intent = json_data['intent']

    if 'key' in json_data:
      assert isinstance(json_data['key'], str), 'Wrong type for attribute: key. Expected: str. Got: ' + str(type(json_data['key'])) + '.'
      obj.key = json_data['key']

    if 'label' in json_data:
      assert isinstance(json_data['label'], str), 'Wrong type for attribute: label. Expected: str. Got: ' + str(type(json_data['label'])) + '.'
      obj.label = json_data['label']

    if 'message' in json_data:
      assert isinstance(json_data['message'], str), 'Wrong type for attribute: message. Expected: str. Got: ' + str(type(json_data['message'])) + '.'
      obj.message = json_data['message']

    if 'metadata' in json_data:
      assert isinstance(json_data['metadata'], dict), 'Wrong type for attribute: metadata. Expected: dict. Got: ' + str(type(json_data['metadata'])) + '.'
      obj.metadata = Metadata.from_json(json_data['metadata'])

    if 'origin' in json_data:
      assert isinstance(json_data['origin'], str), 'Wrong type for attribute: origin. Expected: str. Got: ' + str(type(json_data['origin'])) + '.'
      obj.origin = json_data['origin']

    if 'originClient' in json_data:
      assert isinstance(json_data['originClient'], str), 'Wrong type for attribute: originClient. Expected: str. Got: ' + str(type(json_data['originClient'])) + '.'
      obj.origin_client = json_data['originClient']

    if 'originControl' in json_data:
      assert isinstance(json_data['originControl'], str), 'Wrong type for attribute: originControl. Expected: str. Got: ' + str(type(json_data['originControl'])) + '.'
      obj.origin_control = json_data['originControl']

    if 'originTransportType' in json_data:
      assert isinstance(json_data['originTransportType'], str), 'Wrong type for attribute: originTransportType. Expected: str. Got: ' + str(type(json_data['originTransportType'])) + '.'
      obj.origin_transport_type = json_data['originTransportType']

    if 'originType' in json_data:
      assert isinstance(json_data['originType'], str), 'Wrong type for attribute: originType. Expected: str. Got: ' + str(type(json_data['originType'])) + '.'
      obj.origin_type = json_data['originType']

    if 'pickID' in json_data:
      assert isinstance(json_data['pickID'], str), 'Wrong type for attribute: pickID. Expected: str. Got: ' + str(type(json_data['pickID'])) + '.'
      obj.pick_id = json_data['pickID']

    if 'predictionType' in json_data:
      assert isinstance(json_data['predictionType'], str), 'Wrong type for attribute: predictionType. Expected: str. Got: ' + str(type(json_data['predictionType'])) + '.'
      obj.prediction_type = json_data['predictionType']

    if 'progress' in json_data:
      assert isinstance(json_data['progress'], float) or isinstance(json_data['progress'], int), 'Wrong type for attribute: progress. Expected: float. Got: ' + str(type(json_data['progress'])) + '.'
      obj.progress = json_data['progress']

    if 'reachScript' in json_data:
      assert isinstance(json_data['reachScript'], dict), 'Wrong type for attribute: reachScript. Expected: dict. Got: ' + str(type(json_data['reachScript'])) + '.'
      obj.reach_script = ReachScript.from_json(json_data['reachScript'])

    if 'requestType' in json_data:
      assert isinstance(json_data['requestType'], str), 'Wrong type for attribute: requestType. Expected: str. Got: ' + str(type(json_data['requestType'])) + '.'
      obj.request_type = json_data['requestType']

    if 'robotID' in json_data:
      assert isinstance(json_data['robotID'], str), 'Wrong type for attribute: robotID. Expected: str. Got: ' + str(type(json_data['robotID'])) + '.'
      obj.robot_id = json_data['robotID']

    if 'script' in json_data:
      assert isinstance(json_data['script'], str), 'Wrong type for attribute: script. Expected: str. Got: ' + str(type(json_data['script'])) + '.'
      obj.script = json_data['script']

    if 'seq' in json_data:
      assert isinstance(json_data['seq'], int), 'Wrong type for attribute: seq. Expected: int. Got: ' + str(type(json_data['seq'])) + '.'
      obj.seq = json_data['seq']

    if 'sessionInfo' in json_data:
      assert isinstance(json_data['sessionInfo'], dict), 'Wrong type for attribute: sessionInfo. Expected: dict. Got: ' + str(type(json_data['sessionInfo'])) + '.'
      obj.session_info = SessionInfo.from_json(json_data['sessionInfo'])

    if 'simAction' in json_data:
      assert isinstance(json_data['simAction'], dict), 'Wrong type for attribute: simAction. Expected: dict. Got: ' + str(type(json_data['simAction'])) + '.'
      obj.sim_action = SimAction.from_json(json_data['simAction'])

    if 'snapshot' in json_data:
      assert isinstance(json_data['snapshot'], dict), 'Wrong type for attribute: snapshot. Expected: dict. Got: ' + str(type(json_data['snapshot'])) + '.'
      obj.snapshot = Snapshot.from_json(json_data['snapshot'])

    if 'successType' in json_data:
      assert isinstance(json_data['successType'], str), 'Wrong type for attribute: successType. Expected: str. Got: ' + str(type(json_data['successType'])) + '.'
      obj.success_type = json_data['successType']

    if 'tag' in json_data:
      assert isinstance(json_data['tag'], str), 'Wrong type for attribute: tag. Expected: str. Got: ' + str(type(json_data['tag'])) + '.'
      obj.tag = json_data['tag']

    if 'taskCode' in json_data:
      assert isinstance(json_data['taskCode'], str), 'Wrong type for attribute: taskCode. Expected: str. Got: ' + str(type(json_data['taskCode'])) + '.'
      obj.task_code = json_data['taskCode']

    if 'textCue' in json_data:
      assert isinstance(json_data['textCue'], str), 'Wrong type for attribute: textCue. Expected: str. Got: ' + str(type(json_data['textCue'])) + '.'
      obj.text_cue = json_data['textCue']

    if 'ts' in json_data:
      assert isinstance(json_data['ts'], int), 'Wrong type for attribute: ts. Expected: int. Got: ' + str(type(json_data['ts'])) + '.'
      obj.ts = json_data['ts']

    if 'value' in json_data:
      assert isinstance(json_data['value'], str), 'Wrong type for attribute: value. Expected: str. Got: ' + str(type(json_data['value'])) + '.'
      obj.value = json_data['value']

    if 'webrtcAudioRequest' in json_data:
      assert isinstance(json_data['webrtcAudioRequest'], dict), 'Wrong type for attribute: webrtcAudioRequest. Expected: dict. Got: ' + str(type(json_data['webrtcAudioRequest'])) + '.'
      obj.webrtc_audio_request = WebrtcAudioRequest.from_json(json_data['webrtcAudioRequest'])

    if 'x' in json_data:
      assert isinstance(json_data['x'], float) or isinstance(json_data['x'], int), 'Wrong type for attribute: x. Expected: float. Got: ' + str(type(json_data['x'])) + '.'
      obj.x = json_data['x']

    if 'y' in json_data:
      assert isinstance(json_data['y'], float) or isinstance(json_data['y'], int), 'Wrong type for attribute: y. Expected: float. Got: ' + str(type(json_data['y'])) + '.'
      obj.y = json_data['y']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.CommandData) -> 'CommandData':
    """Convert CommandData proto to type object."""
    if not proto:
      return None
    obj = CommandData()
    if proto.args:
      json_list = []
      for j in proto.args:
        json_list.append(j)
      obj.args = json_list
    obj.client_annotation = ClientAnnotation.from_proto(get_proto_field(proto, 'client_annotation'))
    obj.client_session_start = ClientSessionStart.from_proto(get_proto_field(proto, 'client_session_start'))
    obj.cmd = get_proto_value(proto.cmd)
    obj.data_type = get_proto_value(proto.data_type)
    obj.detailed_error = get_proto_value(proto.detailed_error)
    obj.device_name = get_proto_value(proto.device_name)
    obj.device_type = get_proto_value(proto.device_type)
    obj.error = get_proto_value(proto.error)
    obj.event_duration = get_proto_value(proto.event_duration)
    if proto.event_labels:
      json_list = []
      for j in proto.event_labels:
        json_list.append(j)
      obj.event_labels = json_list
    obj.event_name = get_proto_value(proto.event_name)
    if proto.event_params:
      json_list = []
      for j in proto.event_params:
        json_list.append(KeyValue.from_proto(j))
      obj.event_params = json_list
    obj.exp = ExperimentalCommandData.from_proto(get_proto_field(proto, 'exp'))
    if proto.exp_array:
      json_list = []
      for j in proto.exp_array:
        json_list.append(ExperimentalCommandData.from_proto(j))
      obj.exp_array = json_list
    obj.experiment_token = get_proto_value(proto.experiment_token)
    obj.float_value = get_proto_value(proto.key_value.float_value)
    obj.history = History.from_proto(get_proto_field(proto, 'history'))
    obj.int_value = get_proto_value(proto.key_value.int_value)
    obj.intent = get_proto_value(proto.intent)
    obj.key = get_proto_value(proto.key_value.key)
    obj.label = get_proto_value(proto.inference_request.label)
    obj.message = get_proto_value(proto.message)
    obj.metadata = Metadata.from_proto(get_proto_field(proto, 'metadata'))
    obj.origin = get_proto_value(proto.origin)
    obj.origin_client = get_proto_value(proto.origin_client)
    obj.origin_control = get_proto_value(proto.origin_control)
    obj.origin_transport_type = get_proto_value(proto.origin_transport_type)
    obj.origin_type = get_proto_value(proto.origin_type)
    obj.pick_id = get_proto_value(proto.pick_id)
    obj.prediction_type = get_proto_value(proto.inference_request.prediction_type)
    obj.progress = get_proto_value(proto.progress)
    obj.reach_script = ReachScript.from_proto(get_proto_field(proto, 'reach_script'))
    obj.request_type = get_proto_value(proto.inference_request.request_type)
    obj.robot_id = get_proto_value(proto.inference_request.robot_id)
    obj.script = get_proto_value(proto.script)
    obj.seq = get_proto_value(proto.seq)
    obj.session_info = SessionInfo.from_proto(get_proto_field(proto, 'session_info'))
    obj.sim_action = SimAction.from_proto(get_proto_field(proto, 'sim_action'))
    obj.snapshot = Snapshot.from_proto(get_proto_field(proto, 'snapshot'))
    obj.success_type = get_proto_value(proto.success_type)
    obj.tag = get_proto_value(proto.tag)
    obj.task_code = get_proto_value(proto.inference_request.task_code)
    obj.text_cue = get_proto_value(proto.text_cue)
    obj.ts = get_proto_value(proto.ts)
    obj.value = get_proto_value(proto.key_value.value)
    obj.webrtc_audio_request = WebrtcAudioRequest.from_proto(get_proto_field(proto, 'webrtc_audio_request'))
    obj.x = get_proto_value(proto.x)
    obj.y = get_proto_value(proto.y)
    return obj


class CompressedDepth:
  """Representation of proto message CompressedDepth.

   CompressedDepth is a compressed depth file.
  """
  # Depth is the depth file path.
  depth: str

  # Encodings is the list of encodings applied to the file.
  encodings: List[str]

  def __init__(self, depth: str = '', encodings: Optional[List[str]] = None) -> None:
    self.depth = depth
    if encodings is None:
      self.encodings = []
    else:
      self.encodings = encodings

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.depth:
      assert isinstance(self.depth, str), 'Wrong type for attribute: depth. Expected: str. Got: ' + str(type(self.depth)) + '.'
      json_data['depth'] = self.depth

    if self.encodings:
      assert isinstance(self.encodings, list), 'Wrong type for attribute: encodings. Expected: list. Got: ' + str(type(self.encodings)) + '.'
      json_data['encodings'] = self.encodings

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'CompressedDepth':
    """Convert JSON to type object."""
    obj = CompressedDepth()
    json_list: List[Any]

    expected_json_keys: List[str] = ['depth', 'encodings']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid CompressedDepth. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'depth' in json_data:
      assert isinstance(json_data['depth'], str), 'Wrong type for attribute: depth. Expected: str. Got: ' + str(type(json_data['depth'])) + '.'
      obj.depth = json_data['depth']

    if 'encodings' in json_data:
      assert isinstance(json_data['encodings'], list), 'Wrong type for attribute: encodings. Expected: list. Got: ' + str(type(json_data['encodings'])) + '.'
      json_list = []
      for j in json_data['encodings']:
        json_list.append(j)
      obj.encodings = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.CompressedDepth) -> 'CompressedDepth':
    """Convert CompressedDepth proto to type object."""
    if not proto:
      return None
    obj = CompressedDepth()
    obj.depth = get_proto_value(proto.depth)
    if proto.encodings:
      json_list = []
      for j in proto.encodings:
        json_list.append(j)
      obj.encodings = json_list
    return obj


class ConnectedClient:
  """Representation of proto message ConnectedClient.

   ConnectedClient is a connected client for the session manager.
  """
  uid: str

  # is_current is set to true by the ClientManager for the current client. The
  # client manager modifies the device-data as it passes through. The
  # is_current field should never be true in the logs. The client-side code
  # can use this value to get the client's UID.
  is_current: bool

  # control_session_active is set to true by the SessionManager for clients
  # that are currently in a control session. The client-side code can use this
  # value to determine if it has a control session, or if another client has
  # a control session.
  control_session_active: bool

  def __init__(self, control_session_active: bool = False, is_current: bool = False, uid: str = '') -> None:
    self.control_session_active = control_session_active
    self.is_current = is_current
    self.uid = uid

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.control_session_active:
      assert isinstance(self.control_session_active, bool), 'Wrong type for attribute: control_session_active. Expected: bool. Got: ' + str(type(self.control_session_active)) + '.'
      json_data['controlSessionActive'] = self.control_session_active

    if self.is_current:
      assert isinstance(self.is_current, bool), 'Wrong type for attribute: is_current. Expected: bool. Got: ' + str(type(self.is_current)) + '.'
      json_data['isCurrent'] = self.is_current

    if self.uid:
      assert isinstance(self.uid, str), 'Wrong type for attribute: uid. Expected: str. Got: ' + str(type(self.uid)) + '.'
      json_data['uid'] = self.uid

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'ConnectedClient':
    """Convert JSON to type object."""
    obj = ConnectedClient()

    expected_json_keys: List[str] = ['controlSessionActive', 'isCurrent', 'uid']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid ConnectedClient. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'controlSessionActive' in json_data:
      assert isinstance(json_data['controlSessionActive'], bool), 'Wrong type for attribute: controlSessionActive. Expected: bool. Got: ' + str(type(json_data['controlSessionActive'])) + '.'
      obj.control_session_active = json_data['controlSessionActive']

    if 'isCurrent' in json_data:
      assert isinstance(json_data['isCurrent'], bool), 'Wrong type for attribute: isCurrent. Expected: bool. Got: ' + str(type(json_data['isCurrent'])) + '.'
      obj.is_current = json_data['isCurrent']

    if 'uid' in json_data:
      assert isinstance(json_data['uid'], str), 'Wrong type for attribute: uid. Expected: str. Got: ' + str(type(json_data['uid'])) + '.'
      obj.uid = json_data['uid']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.ConnectedClient) -> 'ConnectedClient':
    """Convert ConnectedClient proto to type object."""
    if not proto:
      return None
    obj = ConnectedClient()
    obj.control_session_active = get_proto_value(proto.control_session_active)
    obj.is_current = get_proto_value(proto.is_current)
    obj.uid = get_proto_value(proto.uid)
    return obj


class ConnectedClients:
  """Representation of proto message ConnectedClients.

   ConnectedClients is sent in messages for client informatiom.

  """
  clients: List['ConnectedClient']

  def __init__(self, clients: Optional[List['ConnectedClient']] = None) -> None:
    if clients is None:
      self.clients = []
    else:
      self.clients = clients

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.clients:
      assert isinstance(self.clients, list), 'Wrong type for attribute: clients. Expected: list. Got: ' + str(type(self.clients)) + '.'
      obj_list = []
      for item in self.clients:
        obj_list.append(item.to_json())
      json_data['clients'] = obj_list

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'ConnectedClients':
    """Convert JSON to type object."""
    obj = ConnectedClients()
    json_list: List[Any]

    expected_json_keys: List[str] = ['clients']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid ConnectedClients. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'clients' in json_data:
      assert isinstance(json_data['clients'], list), 'Wrong type for attribute: clients. Expected: list. Got: ' + str(type(json_data['clients'])) + '.'
      json_list = []
      for j in json_data['clients']:
        json_list.append(ConnectedClient.from_json(j))
      obj.clients = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.ConnectedClients) -> 'ConnectedClients':
    """Convert ConnectedClients proto to type object."""
    if not proto:
      return None
    obj = ConnectedClients()
    if proto.clients:
      json_list = []
      for j in proto.clients:
        json_list.append(ConnectedClient.from_proto(j))
      obj.clients = json_list
    return obj


class ConveyorState:
  """Representation of proto message ConveyorState.

   ConveyorState represents data from dataType == "conveyor-state" or
   "conveyor-state-update".
  """
  # Whether there is an object detected. If true, implies that a recent pick
  # was successful.
  is_object_detected: bool

  def __init__(self, is_object_detected: bool = False) -> None:
    self.is_object_detected = is_object_detected

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.is_object_detected:
      assert isinstance(self.is_object_detected, bool), 'Wrong type for attribute: is_object_detected. Expected: bool. Got: ' + str(type(self.is_object_detected)) + '.'
      json_data['isObjectDetected'] = self.is_object_detected

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'ConveyorState':
    """Convert JSON to type object."""
    obj = ConveyorState()

    expected_json_keys: List[str] = ['isObjectDetected']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid ConveyorState. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'isObjectDetected' in json_data:
      assert isinstance(json_data['isObjectDetected'], bool), 'Wrong type for attribute: isObjectDetected. Expected: bool. Got: ' + str(type(json_data['isObjectDetected'])) + '.'
      obj.is_object_detected = json_data['isObjectDetected']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.ConveyorState) -> 'ConveyorState':
    """Convert ConveyorState proto to type object."""
    if not proto:
      return None
    obj = ConveyorState()
    obj.is_object_detected = get_proto_value(proto.is_object_detected)
    return obj


class DeleteObject:
  """Representation of proto message DeleteObject.

   DeleteObject requests an object deletion from the scene in SIM.

  """
  py_id: str

  def __init__(self, py_id: str = '') -> None:
    self.py_id = py_id

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.py_id:
      assert isinstance(self.py_id, str), 'Wrong type for attribute: py_id. Expected: str. Got: ' + str(type(self.py_id)) + '.'
      json_data['id'] = self.py_id

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'DeleteObject':
    """Convert JSON to type object."""
    obj = DeleteObject()

    expected_json_keys: List[str] = ['id']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid DeleteObject. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'id' in json_data:
      assert isinstance(json_data['id'], str), 'Wrong type for attribute: id. Expected: str. Got: ' + str(type(json_data['id'])) + '.'
      obj.py_id = json_data['id']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.DeleteObject) -> 'DeleteObject':
    """Convert DeleteObject proto to type object."""
    if not proto:
      return None
    obj = DeleteObject()
    obj.py_id = get_proto_value(proto.id)
    return obj


class Detection:
  """Representation of proto message Detection.

   Detection denotes deviceType == "object-detector", dataType == "detection".
  """
  # Identifies the image on which objects were detected.
  source: Optional['SourceImage']

  # Any number of detected objects.
  detections: List['DetectionEntry']

  # Information on unexpected movement detected on the camera.
  camera_shift: Optional['CameraShiftDetection']

  def __init__(self, camera_shift: Optional['CameraShiftDetection'] = None, detections: Optional[List['DetectionEntry']] = None, source: Optional['SourceImage'] = None) -> None:
    self.camera_shift = camera_shift
    if detections is None:
      self.detections = []
    else:
      self.detections = detections
    self.source = source

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.camera_shift:
      assert self.camera_shift.__class__.__name__ == 'CameraShiftDetection', 'Wrong type for attribute: camera_shift. Expected: CameraShiftDetection. Got: ' + str(type(self.camera_shift)) + '.'
      json_data['cameraShift'] = self.camera_shift.to_json()

    if self.detections:
      assert isinstance(self.detections, list), 'Wrong type for attribute: detections. Expected: list. Got: ' + str(type(self.detections)) + '.'
      obj_list = []
      for item in self.detections:
        obj_list.append(item.to_json())
      json_data['detections'] = obj_list

    if self.source:
      assert self.source.__class__.__name__ == 'SourceImage', 'Wrong type for attribute: source. Expected: SourceImage. Got: ' + str(type(self.source)) + '.'
      json_data['source'] = self.source.to_json()

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'Detection':
    """Convert JSON to type object."""
    obj = Detection()
    json_list: List[Any]

    expected_json_keys: List[str] = ['cameraShift', 'detections', 'source']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid Detection. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'cameraShift' in json_data:
      assert isinstance(json_data['cameraShift'], dict), 'Wrong type for attribute: cameraShift. Expected: dict. Got: ' + str(type(json_data['cameraShift'])) + '.'
      obj.camera_shift = CameraShiftDetection.from_json(json_data['cameraShift'])

    if 'detections' in json_data:
      assert isinstance(json_data['detections'], list), 'Wrong type for attribute: detections. Expected: list. Got: ' + str(type(json_data['detections'])) + '.'
      json_list = []
      for j in json_data['detections']:
        json_list.append(DetectionEntry.from_json(j))
      obj.detections = json_list

    if 'source' in json_data:
      assert isinstance(json_data['source'], dict), 'Wrong type for attribute: source. Expected: dict. Got: ' + str(type(json_data['source'])) + '.'
      obj.source = SourceImage.from_json(json_data['source'])

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.Detection) -> 'Detection':
    """Convert Detection proto to type object."""
    if not proto:
      return None
    obj = Detection()
    obj.camera_shift = CameraShiftDetection.from_proto(get_proto_field(proto, 'camera_shift'))
    if proto.detections:
      json_list = []
      for j in proto.detections:
        json_list.append(DetectionEntry.from_proto(j))
      obj.detections = json_list
    obj.source = SourceImage.from_proto(get_proto_field(proto, 'source'))
    return obj


class DetectionAprilGroupAprilTag:
  """Representation of proto message DetectionAprilGroupAprilTag.

   DetectionAprilGroupAprilTag contains information on a single April Tag
   that constitutes an AprilGroup.
  """
  # Id of the AprilTag. Should exactly match DetectionEntry.id for the
  # corresponding tag's detection.
  py_id: str

  # Reprojected polygon boundaries for the apriltag.
  corners: List[float]

  def __init__(self, corners: Optional[List[float]] = None, py_id: str = '') -> None:
    if corners is None:
      self.corners = []
    else:
      self.corners = corners
    self.py_id = py_id

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.corners:
      assert isinstance(self.corners, list), 'Wrong type for attribute: corners. Expected: list. Got: ' + str(type(self.corners)) + '.'
      json_data['corners'] = self.corners

    if self.py_id:
      assert isinstance(self.py_id, str), 'Wrong type for attribute: py_id. Expected: str. Got: ' + str(type(self.py_id)) + '.'
      json_data['id'] = self.py_id

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'DetectionAprilGroupAprilTag':
    """Convert JSON to type object."""
    obj = DetectionAprilGroupAprilTag()
    json_list: List[Any]

    expected_json_keys: List[str] = ['corners', 'id']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid DetectionAprilGroupAprilTag. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'corners' in json_data:
      assert isinstance(json_data['corners'], list), 'Wrong type for attribute: corners. Expected: list. Got: ' + str(type(json_data['corners'])) + '.'
      json_list = []
      for j in json_data['corners']:
        json_list.append(j)
      obj.corners = json_list

    if 'id' in json_data:
      assert isinstance(json_data['id'], str), 'Wrong type for attribute: id. Expected: str. Got: ' + str(type(json_data['id'])) + '.'
      obj.py_id = json_data['id']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.DetectionAprilGroupAprilTag) -> 'DetectionAprilGroupAprilTag':
    """Convert DetectionAprilGroupAprilTag proto to type object."""
    if not proto:
      return None
    obj = DetectionAprilGroupAprilTag()
    if proto.corners:
      json_list = []
      for j in proto.corners:
        json_list.append(j)
      obj.corners = json_list
    obj.py_id = get_proto_value(proto.id)
    return obj


class DetectionAprilGroupInfo:
  """Representation of proto message DetectionAprilGroupInfo.

   DetectionAprilGroupInfo has additional info when type == "AprilGroup".
  """
  # AprilTag id and polygon boundary.
  april_tags: List['DetectionAprilGroupAprilTag']

  def __init__(self, april_tags: Optional[List['DetectionAprilGroupAprilTag']] = None) -> None:
    if april_tags is None:
      self.april_tags = []
    else:
      self.april_tags = april_tags

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.april_tags:
      assert isinstance(self.april_tags, list), 'Wrong type for attribute: april_tags. Expected: list. Got: ' + str(type(self.april_tags)) + '.'
      obj_list = []
      for item in self.april_tags:
        obj_list.append(item.to_json())
      json_data['aprilTags'] = obj_list

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'DetectionAprilGroupInfo':
    """Convert JSON to type object."""
    obj = DetectionAprilGroupInfo()
    json_list: List[Any]

    expected_json_keys: List[str] = ['aprilTags']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid DetectionAprilGroupInfo. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'aprilTags' in json_data:
      assert isinstance(json_data['aprilTags'], list), 'Wrong type for attribute: aprilTags. Expected: list. Got: ' + str(type(json_data['aprilTags'])) + '.'
      json_list = []
      for j in json_data['aprilTags']:
        json_list.append(DetectionAprilGroupAprilTag.from_json(j))
      obj.april_tags = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.DetectionAprilGroupInfo) -> 'DetectionAprilGroupInfo':
    """Convert DetectionAprilGroupInfo proto to type object."""
    if not proto:
      return None
    obj = DetectionAprilGroupInfo()
    if proto.april_tags:
      json_list = []
      for j in proto.april_tags:
        json_list.append(DetectionAprilGroupAprilTag.from_proto(j))
      obj.april_tags = json_list
    return obj


class DetectionEntry:
  """Representation of proto message DetectionEntry.

   DetectionEntry contains properties of a single detected object.
  """
  # An unique id of the object being detected.
  py_id: str

  # A categorization of the type of object detected, e.g. "AprilTag".
  py_type: str

  # Coordinates for the corners, in the form [x1, y1, x2, y2 ...].
  corners: List[float]

  # Optional 3D pose of the object. If present, must contain 6 entries,
  # [x, y, z, rx, ry, rz] where (rx, ry, rz) are the Rodriguez rotation and
  # (x, y, z) is the translation applied after rotation.
  extrinsics: List[float]

  # Optional 3D bounding box centered at the center of object. If present,
  # must contain [sx, sy, sz] which denote the length, width, height.
  # The box must be transformed by the extrinsics for drawing.
  intrinsics: List[float]
  april_group: Optional['DetectionAprilGroupInfo']

  def __init__(self, april_group: Optional['DetectionAprilGroupInfo'] = None, corners: Optional[List[float]] = None, extrinsics: Optional[List[float]] = None, intrinsics: Optional[List[float]] = None, py_id: str = '', py_type: str = '') -> None:
    self.april_group = april_group
    if corners is None:
      self.corners = []
    else:
      self.corners = corners
    if extrinsics is None:
      self.extrinsics = []
    else:
      self.extrinsics = extrinsics
    if intrinsics is None:
      self.intrinsics = []
    else:
      self.intrinsics = intrinsics
    self.py_id = py_id
    self.py_type = py_type

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.april_group:
      assert self.april_group.__class__.__name__ == 'DetectionAprilGroupInfo', 'Wrong type for attribute: april_group. Expected: DetectionAprilGroupInfo. Got: ' + str(type(self.april_group)) + '.'
      json_data['aprilGroup'] = self.april_group.to_json()

    if self.corners:
      assert isinstance(self.corners, list), 'Wrong type for attribute: corners. Expected: list. Got: ' + str(type(self.corners)) + '.'
      json_data['corners'] = self.corners

    if self.extrinsics:
      assert isinstance(self.extrinsics, list), 'Wrong type for attribute: extrinsics. Expected: list. Got: ' + str(type(self.extrinsics)) + '.'
      json_data['extrinsics'] = self.extrinsics

    if self.intrinsics:
      assert isinstance(self.intrinsics, list), 'Wrong type for attribute: intrinsics. Expected: list. Got: ' + str(type(self.intrinsics)) + '.'
      json_data['intrinsics'] = self.intrinsics

    if self.py_id:
      assert isinstance(self.py_id, str), 'Wrong type for attribute: py_id. Expected: str. Got: ' + str(type(self.py_id)) + '.'
      json_data['id'] = self.py_id

    if self.py_type:
      assert isinstance(self.py_type, str), 'Wrong type for attribute: py_type. Expected: str. Got: ' + str(type(self.py_type)) + '.'
      json_data['type'] = self.py_type

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'DetectionEntry':
    """Convert JSON to type object."""
    obj = DetectionEntry()
    json_list: List[Any]

    expected_json_keys: List[str] = ['aprilGroup', 'corners', 'extrinsics', 'intrinsics', 'id', 'type']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid DetectionEntry. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'aprilGroup' in json_data:
      assert isinstance(json_data['aprilGroup'], dict), 'Wrong type for attribute: aprilGroup. Expected: dict. Got: ' + str(type(json_data['aprilGroup'])) + '.'
      obj.april_group = DetectionAprilGroupInfo.from_json(json_data['aprilGroup'])

    if 'corners' in json_data:
      assert isinstance(json_data['corners'], list), 'Wrong type for attribute: corners. Expected: list. Got: ' + str(type(json_data['corners'])) + '.'
      json_list = []
      for j in json_data['corners']:
        json_list.append(j)
      obj.corners = json_list

    if 'extrinsics' in json_data:
      assert isinstance(json_data['extrinsics'], list), 'Wrong type for attribute: extrinsics. Expected: list. Got: ' + str(type(json_data['extrinsics'])) + '.'
      json_list = []
      for j in json_data['extrinsics']:
        json_list.append(j)
      obj.extrinsics = json_list

    if 'intrinsics' in json_data:
      assert isinstance(json_data['intrinsics'], list), 'Wrong type for attribute: intrinsics. Expected: list. Got: ' + str(type(json_data['intrinsics'])) + '.'
      json_list = []
      for j in json_data['intrinsics']:
        json_list.append(j)
      obj.intrinsics = json_list

    if 'id' in json_data:
      assert isinstance(json_data['id'], str), 'Wrong type for attribute: id. Expected: str. Got: ' + str(type(json_data['id'])) + '.'
      obj.py_id = json_data['id']

    if 'type' in json_data:
      assert isinstance(json_data['type'], str), 'Wrong type for attribute: type. Expected: str. Got: ' + str(type(json_data['type'])) + '.'
      obj.py_type = json_data['type']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.DetectionEntry) -> 'DetectionEntry':
    """Convert DetectionEntry proto to type object."""
    if not proto:
      return None
    obj = DetectionEntry()
    obj.april_group = DetectionAprilGroupInfo.from_proto(get_proto_field(proto, 'april_group'))
    if proto.corners:
      json_list = []
      for j in proto.corners:
        json_list.append(j)
      obj.corners = json_list
    if proto.extrinsics:
      json_list = []
      for j in proto.extrinsics:
        json_list.append(j)
      obj.extrinsics = json_list
    if proto.intrinsics:
      json_list = []
      for j in proto.intrinsics:
        json_list.append(j)
      obj.intrinsics = json_list
    obj.py_id = get_proto_value(proto.id)
    obj.py_type = get_proto_value(proto.type)
    return obj


class DetectionKey:
  """Representation of proto message DetectionKey.

   DetectionKey identifies a DetectionEntry uniquely. This is used within
   CameraShiftDetection message to identify the tags that resulted in a movement
   detection.
  """
  # An unique id of the object being detected.
  py_id: str

  # A categorization of the type of object detected, e.g. "AprilTag".
  py_type: str

  def __init__(self, py_id: str = '', py_type: str = '') -> None:
    self.py_id = py_id
    self.py_type = py_type

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.py_id:
      assert isinstance(self.py_id, str), 'Wrong type for attribute: py_id. Expected: str. Got: ' + str(type(self.py_id)) + '.'
      json_data['id'] = self.py_id

    if self.py_type:
      assert isinstance(self.py_type, str), 'Wrong type for attribute: py_type. Expected: str. Got: ' + str(type(self.py_type)) + '.'
      json_data['type'] = self.py_type

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'DetectionKey':
    """Convert JSON to type object."""
    obj = DetectionKey()

    expected_json_keys: List[str] = ['id', 'type']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid DetectionKey. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'id' in json_data:
      assert isinstance(json_data['id'], str), 'Wrong type for attribute: id. Expected: str. Got: ' + str(type(json_data['id'])) + '.'
      obj.py_id = json_data['id']

    if 'type' in json_data:
      assert isinstance(json_data['type'], str), 'Wrong type for attribute: type. Expected: str. Got: ' + str(type(json_data['type'])) + '.'
      obj.py_type = json_data['type']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.DetectionKey) -> 'DetectionKey':
    """Convert DetectionKey proto to type object."""
    if not proto:
      return None
    obj = DetectionKey()
    obj.py_id = get_proto_value(proto.id)
    obj.py_type = get_proto_value(proto.type)
    return obj


class DeviceData:
  """Representation of proto message DeviceData.

   DeviceData represents sensor data on the robot and in the Reach
   environment.
  """
  # The type of device that generated the data, such as photoneo.
  device_type: str

  # Which sensor the data is coming from. Usually, the deviceType is
  # sufficient to infer what sensor is being used, but the name disambiguates
  # cases where multiple sensors of the same type are used in a robot system.
  # This field may be empty / omitted, if no other device of this type is
  # expected on the system across all producers.
  device_name: str

  # The type of data repo. Typically, this maps to a specific payload in
  # data_type_oneof.
  data_type: str
  hint: str
  label: str
  tag: str

  # SendToClients is a list of clients (and optionally tags) to send to.
  send_to_clients: List['SendToClient']

  inhibit_frame_send: bool
  inhibit_frame_save: bool

  # Timestamps for the device data.
  ts: int

  # Client-side timestamp at the time of receipt of this message.
  local_ts: int

  # Robot-side timestamp, when the message was sent over WebRTC.
  remote_ts: int
  experiment_token: str

  # Event parameters can be found primarily on metrics DeviceData.
  event_params: List['KeyValue']

  # Last timestamp for message timestamps. See design doc:
  message_last_timestamps: List['MessageLastTimestamp']

  # Sequence number of the DeviceData. Unique within a Reach serve run.
  seq: int

  # === Fields for dataType color:
  # A reference to a color image.
  # In the JSON world, this is a path to the image file in the GCS bucket.
  color: str

  # A list containing a camera intrinsics of the form  [cx, cy, fx, fy].
  # Can be left blank or omitted, if intrinsics are unknown.
  color_intrinsics: List[float]
  # ==============================

  # === Fields for dataType color-depth:
  # (also field color)
  # (also field color_intrinsics)

  # A reference to a depth image.
  # In the JSON world, this is a path to the image file in the GCS bucket.
  depth: str

  # A list containing a camera intrinsics of the form  [cx, cy, fx, fy].
  # Can be left blank or omitted, if intrinsics are unknown.
  depth_intrinsics: List[float]

  # UploadDepth is the depth data filename for upload
  upload_depth: str

  # UncompressedDepth is the path to the uncompressed filename
  uncompressed_depth: str

  # CompressedDepth is a list of compressed files and algorithms used
  # to generate the same.
  compressed_depth: List['CompressedDepth']
  # ==============================

  # === Fields for dataType key-value:
  key: str
  value: str
  int_value: int
  float_value: float
  # ==============================

  # === Fields for dataType prediction:
  # ModelPick Predictions.
  pick_points: List['PickPoint']

  # ModelPickAndPlace Predictions.
  position_3d: List['Vec3d']
  quaternion_3d: List['Quaternion3d']
  place_position_3d: List['Vec3d']
  place_quaternion_3d: List['Quaternion3d']

  # confidence score for each prediction (in [0, 1]).
  confidence: List[float]
  # The prediction type to execute. This is approximatly mapped to a model
  # type (although one model may handle multiple request types).
  # Oneof ["ModelPick", "ModelPickAndPlace"].
  prediction_type: str

  # request_type: "sparse" will send a single inference result and wait for
  # another. In the future we will support "continuous" requests will send
  # inference results continuously following the initial request, until "stop"
  # is sent. Oneof ["sparse"], future support: ["continuous", “stop”].
  request_type: str

  # task_code: e.g. TC-101.
  task_code: str

  # intent: supported values: ["pick"].
  intent: str
  # (also field label)

  # robot_id: e.g. reach07.
  robot_id: str

  # color_ts is the color frame timestamp used as input to the model.
  color_ts: int

  # depth_ts is the depth frame timestamp used as input to the model.
  depth_ts: int
  # ==============================

  # === Fields for dataType ur-state:
  # Robot pose, 6 numbers: x, y, z, rx, ry, rz.
  pose: List[float]

  # Joints positions in radians.
  joints: List[float]

  # Forces reported by robot. There is no standard for this field; it is
  # robot-specific.
  force: List[float]

  # Torques reported by robot. There is no standard for this field; it is
  # robot-specific.
  torque: List[float]
  robot_dexterity: float

  # Is the robot turned on.
  is_robot_power_on: bool
  is_emergency_stopped: bool
  is_protective_stopped: bool
  is_safeguard_stopped: bool
  is_reduced_mode: bool
  safety_message: str
  is_program_running: bool

  # Digital inputs.
  digital_in: List[bool]
  sensor_in: List[bool]

  # Digital outputs.
  digital_out: List[bool]

  # Analog inputs.
  analog_in: List[float]
  analog_out: List[float]
  tool_digital_in: List[bool]
  tool_digital_out: List[bool]
  tool_analog_in: List[float]
  tool_analog_out: List[float]
  board_temp_c: float
  robot_voltage_v: float
  robot_current_a: float
  board_io_current_a: float
  tool_temp_c: float
  tool_voltage_v: float
  tool_current_a: float
  joint_voltages_v: List[float]
  joint_currents_a: List[float]
  joint_temps_c: List[float]

  # One of {"", "remote", "local"}
  robot_mode: str

  # ProgramCounter is the number of executed programs.
  # It only gets incremented after a program finished running.
  program_counter: int

  # I/O states for digital pins. When present, overrides digital_in,
  # sensor_in, digital_out, tool_digital_in, and tool_digital_out.
  digital_bank: List['DigitalBank']

  # I/O states for analog pins. When present, overrides analog_in, analog_out,
  # tool_analog_in, and tool_analog_out.
  analog_bank: List['AnalogBank']

  # I/O states for integer pins.
  integer_bank: List['IntegerBank']

  # Tag of last terminated (aborted or done) program.
  last_terminated_program: str
  # ==============================

  # === Fields for dataType conveyor-state:
  # Whether there is an object detected. If true, implies that a recent pick
  # was successful.
  is_object_detected: bool
  # ==============================

  # === Fields for dataType conveyor-state-update:
  # (also field is_object_detected)
  # ==============================

  # === Fields for dataType tool-state:
  vacuum_level_pa: float
  on: bool
  # ==============================

  # === Fields for dataType tool-state-update:
  # (also field vacuum_level_pa)
  # (also field on)
  # ==============================

  # === Fields for dataType status:
  status: str

  # script is the name of the script/cmd/downlink that the status refers to.
  script: str
  error: str
  progress: float
  message: str
  code: int
  # ==============================

  # === Fields for dataType session-info:
  operator_uid: str
  operator_type: str
  session_id: str
  start_time: int
  robot_name: str
  client_os: str
  ui_version: str
  calibration_version: str
  accept_depth_encoding: List[str]
  relay: str

  # ActionsetsVersion is the version of action sets being used in the
  # current session.
  actionsets_version: str

  # SafetyVersion is the version of safety planes being used in the
  # current session.
  safety_version: str

  # WorkcellIOVersion is the version of workcell I/O configuration being used
  # in the current session.
  workcell_io_version: str

  # Transport is the name of the transport used to transmit the session.
  # Currently, "webrtc" is the only accepted value.
  transport: str
  client_session_uid: str

  # WorkcellSetupVersion is the version of the workcell setup configuration.
  workcell_setup_version: str

  # ConstraintsVersion is the version of constraints being used in the
  # current session.
  constraints_version: str
  # ==============================

  # === Fields for dataType pick-label:

  # The pick-label is sent locally on the reach serve side, and is not sent
  # out via webrtc. It is however sent to the oracle-pick-points downlink
  # with device_type of “label-engine”.
  pick_label: Optional['PickLabel']
  # ==============================

  # === Fields for dataType place-label:
  place_label: Optional['PlaceLabel']
  # ==============================

  # === Fields for dataType level:
  level: float
  # ==============================

  # === Fields for dataType robot-power-state:

  # The robot power state.
  robot_power_state: Optional['RobotPowerState']
  # ==============================

  # === Fields for dataType robot-power-state-update:

  # The robot power state. Data will be in this message whenever
  # the state changes.
  robot_power_state_update: Optional['RobotPowerState']
  # ==============================

  # === Fields for dataType metric:
  metric_value: Optional['KeyValue']
  labels: List['KeyValue']
  # ==============================

  # === Fields for dataType reach-script-status:
  # (also field status)
  # (also field script)
  # (also field error)
  # (also field progress)
  # (also field message)
  # (also field code)
  # ==============================

  # === Fields for dataType cmd-status:
  # (also field status)
  # (also field script)
  # (also field error)
  # (also field progress)
  # (also field message)
  # (also field code)
  # ==============================

  # === Fields for dataType vacuum-pressure-state:
  # (also field vacuum_level_pa)
  # (also field on)
  # ==============================

  # === Fields for dataType vacuum-pressure-update:
  # (also field vacuum_level_pa)
  # (also field on)
  # ==============================

  # === Fields for dataType downlink-status:
  # (also field status)
  # (also field script)
  # (also field error)
  # (also field progress)
  # (also field message)
  # (also field code)
  # ==============================

  # === Fields for dataType sensor-state:
  state: List['CapabilityState']
  # ==============================

  # === Fields for dataType sensor-state-update:
  # (also field state)
  # ==============================

  # === Fields for dataType output-state:
  # (also field state)
  # ==============================

  # === Fields for dataType output-state-update:
  # (also field state)
  # ==============================

  # === Fields for dataType health-check:
  # (no fields)
  # ==============================

  # === Fields for dataType history:

  # History serves for returning settings config history when requested.
  history: Optional['History']
  # ==============================

  # === Fields for dataType audio-request-mute:

  # AudioRequest is used for audio mute and unmute requests.
  #
  audio_request_mute: Optional['AudioRequest']
  # ==============================

  # === Fields for dataType audio-request-unmute:
  audio_request_unmute: Optional['AudioRequest']
  # ==============================

  # === Fields for dataType error:
  # (also field status)
  # (also field script)
  # (also field error)
  # (also field progress)
  # (also field message)
  # (also field code)
  # ==============================

  # === Fields for dataType webrtc-audio-response:

  # WebrtcAudioResponse is the response to a webrtc-audio-request command.
  #
  webrtc_audio_response: Optional['WebrtcAudioResponse']
  # ==============================

  # === Fields for dataType metadata:

  # Metadata will be used for log file open/close purposes
  metadata: Optional['Metadata']
  # ==============================

  # === Fields for dataType sim-state:

  # SimState is the list of object states in SIM for ML research.
  #
  sim_state: Optional['SimState']
  # ==============================

  # === Fields for dataType device-status:
  # (also field status)
  # (also field script)
  # (also field error)
  # (also field progress)
  # (also field message)
  # (also field code)
  # ==============================

  # === Fields for dataType webrtc-audio-request:

  # WebrtcAudioRequest is used in a data of dataType "webrtc-audio-request",
  # an internal message for setting mute/unmute status in webrtc.
  #
  webrtc_audio_request: Optional['WebrtcAudioRequest']
  # ==============================

  # === Fields for dataType sim-instance-segmentation:
  sim_instance_segmentation: Optional['SimInstanceSegmentation']
  # ==============================

  # === Fields for dataType exposure-complete:
  # (no fields)
  # ==============================

  # === Fields for dataType start-shutdown:
  # (no fields)
  # ==============================

  # === Fields for dataType finish-shutdown:
  # (no fields)
  # ==============================

  # === Fields for dataType hangup:
  # (no fields)
  # ==============================

  # === Fields for dataType connected-clients:

  # connected_clients is sent in messages for client informatiom.
  #
  connected_clients: Optional['ConnectedClients']
  # ==============================

  # === Fields for dataType detection:

  # Message for detection of arbitrary objects.
  detection: Optional['Detection']
  # ==============================

  # === Fields for dataType client-annotation:

  # ClientAnnotation messages and custom log intervals.
  #
  client_annotation: Optional['ClientAnnotation']
  # ==============================

  # === Fields for dataType pipeline-description:

  # Machine and interface description messages.
  #
  pipeline_description: Optional['PipelineDescription']
  # ==============================

  # === Fields for dataType machine-interfaces:
  machine_interfaces: Optional['MachineInterfaces']
  # ==============================

  # === Fields for dataType machine-description:
  machine_description: Optional['MachineDescription']
  # ==============================

  # === Fields for dataType text-instruction:

  # TextInstruction messages for providing instructions to the user.
  #
  text_instruction: Optional['TextInstruction']
  # ==============================

  # === Fields for dataType report-error:

  # ReportError for "report-error" messages. See design doc:
  report_error: Optional['ReportError']
  # ==============================

  def __init__(self, accept_depth_encoding: Optional[List[str]] = None, actionsets_version: str = '', analog_bank: Optional[List['AnalogBank']] = None, analog_in: Optional[List[float]] = None, analog_out: Optional[List[float]] = None, audio_request_mute: Optional['AudioRequest'] = None, audio_request_unmute: Optional['AudioRequest'] = None, board_io_current_a: float = 0.0, board_temp_c: float = 0.0, calibration_version: str = '', client_annotation: Optional['ClientAnnotation'] = None, client_os: str = '', client_session_uid: str = '', code: int = 0, color: str = '', color_intrinsics: Optional[List[float]] = None, color_ts: int = 0, compressed_depth: Optional[List['CompressedDepth']] = None, confidence: Optional[List[float]] = None, connected_clients: Optional['ConnectedClients'] = None, constraints_version: str = '', data_type: str = '', depth: str = '', depth_intrinsics: Optional[List[float]] = None, depth_ts: int = 0, detection: Optional['Detection'] = None, device_name: str = '', device_type: str = '', digital_bank: Optional[List['DigitalBank']] = None, digital_in: Optional[List[bool]] = None, digital_out: Optional[List[bool]] = None, error: str = '', event_params: Optional[List['KeyValue']] = None, experiment_token: str = '', float_value: float = 0.0, force: Optional[List[float]] = None, hint: str = '', history: Optional['History'] = None, inhibit_frame_save: bool = False, inhibit_frame_send: bool = False, int_value: int = 0, integer_bank: Optional[List['IntegerBank']] = None, intent: str = '', is_emergency_stopped: bool = False, is_object_detected: bool = False, is_program_running: bool = False, is_protective_stopped: bool = False, is_reduced_mode: bool = False, is_robot_power_on: bool = False, is_safeguard_stopped: bool = False, joint_currents_a: Optional[List[float]] = None, joint_temps_c: Optional[List[float]] = None, joint_voltages_v: Optional[List[float]] = None, joints: Optional[List[float]] = None, key: str = '', label: str = '', labels: Optional[List['KeyValue']] = None, last_terminated_program: str = '', level: float = 0.0, local_ts: int = 0, machine_description: Optional['MachineDescription'] = None, machine_interfaces: Optional['MachineInterfaces'] = None, message: str = '', message_last_timestamps: Optional[List['MessageLastTimestamp']] = None, metadata: Optional['Metadata'] = None, metric_value: Optional['KeyValue'] = None, on: bool = False, operator_type: str = '', operator_uid: str = '', pick_label: Optional['PickLabel'] = None, pick_points: Optional[List['PickPoint']] = None, pipeline_description: Optional['PipelineDescription'] = None, place_label: Optional['PlaceLabel'] = None, place_position_3d: Optional[List['Vec3d']] = None, place_quaternion_3d: Optional[List['Quaternion3d']] = None, pose: Optional[List[float]] = None, position_3d: Optional[List['Vec3d']] = None, prediction_type: str = '', program_counter: int = 0, progress: float = 0.0, quaternion_3d: Optional[List['Quaternion3d']] = None, relay: str = '', remote_ts: int = 0, report_error: Optional['ReportError'] = None, request_type: str = '', robot_current_a: float = 0.0, robot_dexterity: float = 0.0, robot_id: str = '', robot_mode: str = '', robot_name: str = '', robot_power_state: Optional['RobotPowerState'] = None, robot_power_state_update: Optional['RobotPowerState'] = None, robot_voltage_v: float = 0.0, safety_message: str = '', safety_version: str = '', script: str = '', send_to_clients: Optional[List['SendToClient']] = None, sensor_in: Optional[List[bool]] = None, seq: int = 0, session_id: str = '', sim_instance_segmentation: Optional['SimInstanceSegmentation'] = None, sim_state: Optional['SimState'] = None, start_time: int = 0, state: Optional[List['CapabilityState']] = None, status: str = '', tag: str = '', task_code: str = '', text_instruction: Optional['TextInstruction'] = None, tool_analog_in: Optional[List[float]] = None, tool_analog_out: Optional[List[float]] = None, tool_current_a: float = 0.0, tool_digital_in: Optional[List[bool]] = None, tool_digital_out: Optional[List[bool]] = None, tool_temp_c: float = 0.0, tool_voltage_v: float = 0.0, torque: Optional[List[float]] = None, transport: str = '', ts: int = 0, ui_version: str = '', uncompressed_depth: str = '', upload_depth: str = '', vacuum_level_pa: float = 0.0, value: str = '', webrtc_audio_request: Optional['WebrtcAudioRequest'] = None, webrtc_audio_response: Optional['WebrtcAudioResponse'] = None, workcell_io_version: str = '', workcell_setup_version: str = '') -> None:
    if accept_depth_encoding is None:
      self.accept_depth_encoding = []
    else:
      self.accept_depth_encoding = accept_depth_encoding
    self.actionsets_version = actionsets_version
    if analog_bank is None:
      self.analog_bank = []
    else:
      self.analog_bank = analog_bank
    if analog_in is None:
      self.analog_in = []
    else:
      self.analog_in = analog_in
    if analog_out is None:
      self.analog_out = []
    else:
      self.analog_out = analog_out
    self.audio_request_mute = audio_request_mute
    self.audio_request_unmute = audio_request_unmute
    self.board_io_current_a = board_io_current_a
    self.board_temp_c = board_temp_c
    self.calibration_version = calibration_version
    self.client_annotation = client_annotation
    self.client_os = client_os
    self.client_session_uid = client_session_uid
    self.code = code
    self.color = color
    if color_intrinsics is None:
      self.color_intrinsics = []
    else:
      self.color_intrinsics = color_intrinsics
    self.color_ts = color_ts
    if compressed_depth is None:
      self.compressed_depth = []
    else:
      self.compressed_depth = compressed_depth
    if confidence is None:
      self.confidence = []
    else:
      self.confidence = confidence
    self.connected_clients = connected_clients
    self.constraints_version = constraints_version
    self.data_type = data_type
    self.depth = depth
    if depth_intrinsics is None:
      self.depth_intrinsics = []
    else:
      self.depth_intrinsics = depth_intrinsics
    self.depth_ts = depth_ts
    self.detection = detection
    self.device_name = device_name
    self.device_type = device_type
    if digital_bank is None:
      self.digital_bank = []
    else:
      self.digital_bank = digital_bank
    if digital_in is None:
      self.digital_in = []
    else:
      self.digital_in = digital_in
    if digital_out is None:
      self.digital_out = []
    else:
      self.digital_out = digital_out
    self.error = error
    if event_params is None:
      self.event_params = []
    else:
      self.event_params = event_params
    self.experiment_token = experiment_token
    self.float_value = float_value
    if force is None:
      self.force = []
    else:
      self.force = force
    self.hint = hint
    self.history = history
    self.inhibit_frame_save = inhibit_frame_save
    self.inhibit_frame_send = inhibit_frame_send
    self.int_value = int_value
    if integer_bank is None:
      self.integer_bank = []
    else:
      self.integer_bank = integer_bank
    self.intent = intent
    self.is_emergency_stopped = is_emergency_stopped
    self.is_object_detected = is_object_detected
    self.is_program_running = is_program_running
    self.is_protective_stopped = is_protective_stopped
    self.is_reduced_mode = is_reduced_mode
    self.is_robot_power_on = is_robot_power_on
    self.is_safeguard_stopped = is_safeguard_stopped
    if joint_currents_a is None:
      self.joint_currents_a = []
    else:
      self.joint_currents_a = joint_currents_a
    if joint_temps_c is None:
      self.joint_temps_c = []
    else:
      self.joint_temps_c = joint_temps_c
    if joint_voltages_v is None:
      self.joint_voltages_v = []
    else:
      self.joint_voltages_v = joint_voltages_v
    if joints is None:
      self.joints = []
    else:
      self.joints = joints
    self.key = key
    self.label = label
    if labels is None:
      self.labels = []
    else:
      self.labels = labels
    self.last_terminated_program = last_terminated_program
    self.level = level
    self.local_ts = local_ts
    self.machine_description = machine_description
    self.machine_interfaces = machine_interfaces
    self.message = message
    if message_last_timestamps is None:
      self.message_last_timestamps = []
    else:
      self.message_last_timestamps = message_last_timestamps
    self.metadata = metadata
    self.metric_value = metric_value
    self.on = on
    self.operator_type = operator_type
    self.operator_uid = operator_uid
    self.pick_label = pick_label
    if pick_points is None:
      self.pick_points = []
    else:
      self.pick_points = pick_points
    self.pipeline_description = pipeline_description
    self.place_label = place_label
    if place_position_3d is None:
      self.place_position_3d = []
    else:
      self.place_position_3d = place_position_3d
    if place_quaternion_3d is None:
      self.place_quaternion_3d = []
    else:
      self.place_quaternion_3d = place_quaternion_3d
    if pose is None:
      self.pose = []
    else:
      self.pose = pose
    if position_3d is None:
      self.position_3d = []
    else:
      self.position_3d = position_3d
    self.prediction_type = prediction_type
    self.program_counter = program_counter
    self.progress = progress
    if quaternion_3d is None:
      self.quaternion_3d = []
    else:
      self.quaternion_3d = quaternion_3d
    self.relay = relay
    self.remote_ts = remote_ts
    self.report_error = report_error
    self.request_type = request_type
    self.robot_current_a = robot_current_a
    self.robot_dexterity = robot_dexterity
    self.robot_id = robot_id
    self.robot_mode = robot_mode
    self.robot_name = robot_name
    self.robot_power_state = robot_power_state
    self.robot_power_state_update = robot_power_state_update
    self.robot_voltage_v = robot_voltage_v
    self.safety_message = safety_message
    self.safety_version = safety_version
    self.script = script
    if send_to_clients is None:
      self.send_to_clients = []
    else:
      self.send_to_clients = send_to_clients
    if sensor_in is None:
      self.sensor_in = []
    else:
      self.sensor_in = sensor_in
    self.seq = seq
    self.session_id = session_id
    self.sim_instance_segmentation = sim_instance_segmentation
    self.sim_state = sim_state
    self.start_time = start_time
    if state is None:
      self.state = []
    else:
      self.state = state
    self.status = status
    self.tag = tag
    self.task_code = task_code
    self.text_instruction = text_instruction
    if tool_analog_in is None:
      self.tool_analog_in = []
    else:
      self.tool_analog_in = tool_analog_in
    if tool_analog_out is None:
      self.tool_analog_out = []
    else:
      self.tool_analog_out = tool_analog_out
    self.tool_current_a = tool_current_a
    if tool_digital_in is None:
      self.tool_digital_in = []
    else:
      self.tool_digital_in = tool_digital_in
    if tool_digital_out is None:
      self.tool_digital_out = []
    else:
      self.tool_digital_out = tool_digital_out
    self.tool_temp_c = tool_temp_c
    self.tool_voltage_v = tool_voltage_v
    if torque is None:
      self.torque = []
    else:
      self.torque = torque
    self.transport = transport
    self.ts = ts
    self.ui_version = ui_version
    self.uncompressed_depth = uncompressed_depth
    self.upload_depth = upload_depth
    self.vacuum_level_pa = vacuum_level_pa
    self.value = value
    self.webrtc_audio_request = webrtc_audio_request
    self.webrtc_audio_response = webrtc_audio_response
    self.workcell_io_version = workcell_io_version
    self.workcell_setup_version = workcell_setup_version

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.accept_depth_encoding:
      assert isinstance(self.accept_depth_encoding, list), 'Wrong type for attribute: accept_depth_encoding. Expected: list. Got: ' + str(type(self.accept_depth_encoding)) + '.'
      json_data['acceptDepthEncoding'] = self.accept_depth_encoding

    if self.actionsets_version:
      assert isinstance(self.actionsets_version, str), 'Wrong type for attribute: actionsets_version. Expected: str. Got: ' + str(type(self.actionsets_version)) + '.'
      json_data['actionsetsVersion'] = self.actionsets_version

    if self.analog_bank:
      assert isinstance(self.analog_bank, list), 'Wrong type for attribute: analog_bank. Expected: list. Got: ' + str(type(self.analog_bank)) + '.'
      obj_list = []
      for item in self.analog_bank:
        obj_list.append(item.to_json())
      json_data['analogBank'] = obj_list

    if self.analog_in:
      assert isinstance(self.analog_in, list), 'Wrong type for attribute: analog_in. Expected: list. Got: ' + str(type(self.analog_in)) + '.'
      json_data['analogIn'] = self.analog_in

    if self.analog_out:
      assert isinstance(self.analog_out, list), 'Wrong type for attribute: analog_out. Expected: list. Got: ' + str(type(self.analog_out)) + '.'
      json_data['analogOut'] = self.analog_out

    if self.audio_request_mute:
      assert self.audio_request_mute.__class__.__name__ == 'AudioRequest', 'Wrong type for attribute: audio_request_mute. Expected: AudioRequest. Got: ' + str(type(self.audio_request_mute)) + '.'
      json_data['audioRequestMute'] = self.audio_request_mute.to_json()

    if self.audio_request_unmute:
      assert self.audio_request_unmute.__class__.__name__ == 'AudioRequest', 'Wrong type for attribute: audio_request_unmute. Expected: AudioRequest. Got: ' + str(type(self.audio_request_unmute)) + '.'
      json_data['audioRequestUnmute'] = self.audio_request_unmute.to_json()

    if self.board_io_current_a:
      assert isinstance(self.board_io_current_a, float) or isinstance(self.board_io_current_a, int), 'Wrong type for attribute: board_io_current_a. Expected: float. Got: ' + str(type(self.board_io_current_a)) + '.'
      json_data['boardIOCurrentA'] = self.board_io_current_a

    if self.board_temp_c:
      assert isinstance(self.board_temp_c, float) or isinstance(self.board_temp_c, int), 'Wrong type for attribute: board_temp_c. Expected: float. Got: ' + str(type(self.board_temp_c)) + '.'
      json_data['boardTempC'] = self.board_temp_c

    if self.calibration_version:
      assert isinstance(self.calibration_version, str), 'Wrong type for attribute: calibration_version. Expected: str. Got: ' + str(type(self.calibration_version)) + '.'
      json_data['calibrationVersion'] = self.calibration_version

    if self.client_annotation:
      assert self.client_annotation.__class__.__name__ == 'ClientAnnotation', 'Wrong type for attribute: client_annotation. Expected: ClientAnnotation. Got: ' + str(type(self.client_annotation)) + '.'
      json_data['clientAnnotation'] = self.client_annotation.to_json()

    if self.client_os:
      assert isinstance(self.client_os, str), 'Wrong type for attribute: client_os. Expected: str. Got: ' + str(type(self.client_os)) + '.'
      json_data['clientOS'] = self.client_os

    if self.client_session_uid:
      assert isinstance(self.client_session_uid, str), 'Wrong type for attribute: client_session_uid. Expected: str. Got: ' + str(type(self.client_session_uid)) + '.'
      json_data['clientSessionUID'] = self.client_session_uid

    if self.code:
      assert isinstance(self.code, int), 'Wrong type for attribute: code. Expected: int. Got: ' + str(type(self.code)) + '.'
      json_data['code'] = self.code

    if self.color:
      assert isinstance(self.color, str), 'Wrong type for attribute: color. Expected: str. Got: ' + str(type(self.color)) + '.'
      json_data['color'] = self.color

    if self.color_intrinsics:
      assert isinstance(self.color_intrinsics, list), 'Wrong type for attribute: color_intrinsics. Expected: list. Got: ' + str(type(self.color_intrinsics)) + '.'
      json_data['colorIntrinsics'] = self.color_intrinsics

    if self.color_ts:
      assert isinstance(self.color_ts, int), 'Wrong type for attribute: color_ts. Expected: int. Got: ' + str(type(self.color_ts)) + '.'
      json_data['colorTS'] = self.color_ts

    if self.compressed_depth:
      assert isinstance(self.compressed_depth, list), 'Wrong type for attribute: compressed_depth. Expected: list. Got: ' + str(type(self.compressed_depth)) + '.'
      obj_list = []
      for item in self.compressed_depth:
        obj_list.append(item.to_json())
      json_data['compressedDepth'] = obj_list

    if self.confidence:
      assert isinstance(self.confidence, list), 'Wrong type for attribute: confidence. Expected: list. Got: ' + str(type(self.confidence)) + '.'
      json_data['confidence'] = self.confidence

    if self.connected_clients:
      assert self.connected_clients.__class__.__name__ == 'ConnectedClients', 'Wrong type for attribute: connected_clients. Expected: ConnectedClients. Got: ' + str(type(self.connected_clients)) + '.'
      json_data['connectedClients'] = self.connected_clients.to_json()

    if self.constraints_version:
      assert isinstance(self.constraints_version, str), 'Wrong type for attribute: constraints_version. Expected: str. Got: ' + str(type(self.constraints_version)) + '.'
      json_data['constraintsVersion'] = self.constraints_version

    if self.data_type:
      assert isinstance(self.data_type, str), 'Wrong type for attribute: data_type. Expected: str. Got: ' + str(type(self.data_type)) + '.'
      json_data['dataType'] = self.data_type

    if self.depth:
      assert isinstance(self.depth, str), 'Wrong type for attribute: depth. Expected: str. Got: ' + str(type(self.depth)) + '.'
      json_data['depth'] = self.depth

    if self.depth_intrinsics:
      assert isinstance(self.depth_intrinsics, list), 'Wrong type for attribute: depth_intrinsics. Expected: list. Got: ' + str(type(self.depth_intrinsics)) + '.'
      json_data['depthIntrinsics'] = self.depth_intrinsics

    if self.depth_ts:
      assert isinstance(self.depth_ts, int), 'Wrong type for attribute: depth_ts. Expected: int. Got: ' + str(type(self.depth_ts)) + '.'
      json_data['depthTS'] = self.depth_ts

    if self.detection:
      assert self.detection.__class__.__name__ == 'Detection', 'Wrong type for attribute: detection. Expected: Detection. Got: ' + str(type(self.detection)) + '.'
      json_data['detection'] = self.detection.to_json()

    if self.device_name:
      assert isinstance(self.device_name, str), 'Wrong type for attribute: device_name. Expected: str. Got: ' + str(type(self.device_name)) + '.'
      json_data['deviceName'] = self.device_name

    if self.device_type:
      assert isinstance(self.device_type, str), 'Wrong type for attribute: device_type. Expected: str. Got: ' + str(type(self.device_type)) + '.'
      json_data['deviceType'] = self.device_type

    if self.digital_bank:
      assert isinstance(self.digital_bank, list), 'Wrong type for attribute: digital_bank. Expected: list. Got: ' + str(type(self.digital_bank)) + '.'
      obj_list = []
      for item in self.digital_bank:
        obj_list.append(item.to_json())
      json_data['digitalBank'] = obj_list

    if self.digital_in:
      assert isinstance(self.digital_in, list), 'Wrong type for attribute: digital_in. Expected: list. Got: ' + str(type(self.digital_in)) + '.'
      json_data['digitalIn'] = self.digital_in

    if self.digital_out:
      assert isinstance(self.digital_out, list), 'Wrong type for attribute: digital_out. Expected: list. Got: ' + str(type(self.digital_out)) + '.'
      json_data['digitalOut'] = self.digital_out

    if self.error:
      assert isinstance(self.error, str), 'Wrong type for attribute: error. Expected: str. Got: ' + str(type(self.error)) + '.'
      json_data['error'] = self.error

    if self.event_params:
      assert isinstance(self.event_params, list), 'Wrong type for attribute: event_params. Expected: list. Got: ' + str(type(self.event_params)) + '.'
      obj_list = []
      for item in self.event_params:
        obj_list.append(item.to_json())
      json_data['eventParams'] = obj_list

    if self.experiment_token:
      assert isinstance(self.experiment_token, str), 'Wrong type for attribute: experiment_token. Expected: str. Got: ' + str(type(self.experiment_token)) + '.'
      json_data['experimentToken'] = self.experiment_token

    if self.float_value:
      assert isinstance(self.float_value, float) or isinstance(self.float_value, int), 'Wrong type for attribute: float_value. Expected: float. Got: ' + str(type(self.float_value)) + '.'
      json_data['floatValue'] = self.float_value

    if self.force:
      assert isinstance(self.force, list), 'Wrong type for attribute: force. Expected: list. Got: ' + str(type(self.force)) + '.'
      json_data['force'] = self.force

    if self.hint:
      assert isinstance(self.hint, str), 'Wrong type for attribute: hint. Expected: str. Got: ' + str(type(self.hint)) + '.'
      json_data['hint'] = self.hint

    if self.history:
      assert self.history.__class__.__name__ == 'History', 'Wrong type for attribute: history. Expected: History. Got: ' + str(type(self.history)) + '.'
      json_data['history'] = self.history.to_json()

    if self.inhibit_frame_save:
      assert isinstance(self.inhibit_frame_save, bool), 'Wrong type for attribute: inhibit_frame_save. Expected: bool. Got: ' + str(type(self.inhibit_frame_save)) + '.'
      json_data['inhibitFrameSave'] = self.inhibit_frame_save

    if self.inhibit_frame_send:
      assert isinstance(self.inhibit_frame_send, bool), 'Wrong type for attribute: inhibit_frame_send. Expected: bool. Got: ' + str(type(self.inhibit_frame_send)) + '.'
      json_data['inhibitFrameSend'] = self.inhibit_frame_send

    if self.int_value:
      assert isinstance(self.int_value, int), 'Wrong type for attribute: int_value. Expected: int. Got: ' + str(type(self.int_value)) + '.'
      json_data['intValue'] = self.int_value

    if self.integer_bank:
      assert isinstance(self.integer_bank, list), 'Wrong type for attribute: integer_bank. Expected: list. Got: ' + str(type(self.integer_bank)) + '.'
      obj_list = []
      for item in self.integer_bank:
        obj_list.append(item.to_json())
      json_data['integerBank'] = obj_list

    if self.intent:
      assert isinstance(self.intent, str), 'Wrong type for attribute: intent. Expected: str. Got: ' + str(type(self.intent)) + '.'
      json_data['intent'] = self.intent

    if self.is_emergency_stopped:
      assert isinstance(self.is_emergency_stopped, bool), 'Wrong type for attribute: is_emergency_stopped. Expected: bool. Got: ' + str(type(self.is_emergency_stopped)) + '.'
      json_data['isEmergencyStopped'] = self.is_emergency_stopped

    if self.is_object_detected:
      assert isinstance(self.is_object_detected, bool), 'Wrong type for attribute: is_object_detected. Expected: bool. Got: ' + str(type(self.is_object_detected)) + '.'
      json_data['isObjectDetected'] = self.is_object_detected

    if self.is_program_running:
      assert isinstance(self.is_program_running, bool), 'Wrong type for attribute: is_program_running. Expected: bool. Got: ' + str(type(self.is_program_running)) + '.'
      json_data['isProgramRunning'] = self.is_program_running

    if self.is_protective_stopped:
      assert isinstance(self.is_protective_stopped, bool), 'Wrong type for attribute: is_protective_stopped. Expected: bool. Got: ' + str(type(self.is_protective_stopped)) + '.'
      json_data['isProtectiveStopped'] = self.is_protective_stopped

    if self.is_reduced_mode:
      assert isinstance(self.is_reduced_mode, bool), 'Wrong type for attribute: is_reduced_mode. Expected: bool. Got: ' + str(type(self.is_reduced_mode)) + '.'
      json_data['isReducedMode'] = self.is_reduced_mode

    if self.is_robot_power_on:
      assert isinstance(self.is_robot_power_on, bool), 'Wrong type for attribute: is_robot_power_on. Expected: bool. Got: ' + str(type(self.is_robot_power_on)) + '.'
      json_data['isRobotPowerOn'] = self.is_robot_power_on

    if self.is_safeguard_stopped:
      assert isinstance(self.is_safeguard_stopped, bool), 'Wrong type for attribute: is_safeguard_stopped. Expected: bool. Got: ' + str(type(self.is_safeguard_stopped)) + '.'
      json_data['isSafeguardStopped'] = self.is_safeguard_stopped

    if self.joint_currents_a:
      assert isinstance(self.joint_currents_a, list), 'Wrong type for attribute: joint_currents_a. Expected: list. Got: ' + str(type(self.joint_currents_a)) + '.'
      json_data['jointCurrentsA'] = self.joint_currents_a

    if self.joint_temps_c:
      assert isinstance(self.joint_temps_c, list), 'Wrong type for attribute: joint_temps_c. Expected: list. Got: ' + str(type(self.joint_temps_c)) + '.'
      json_data['jointTempsC'] = self.joint_temps_c

    if self.joint_voltages_v:
      assert isinstance(self.joint_voltages_v, list), 'Wrong type for attribute: joint_voltages_v. Expected: list. Got: ' + str(type(self.joint_voltages_v)) + '.'
      json_data['jointVoltagesV'] = self.joint_voltages_v

    if self.joints:
      assert isinstance(self.joints, list), 'Wrong type for attribute: joints. Expected: list. Got: ' + str(type(self.joints)) + '.'
      json_data['joints'] = self.joints

    if self.key:
      assert isinstance(self.key, str), 'Wrong type for attribute: key. Expected: str. Got: ' + str(type(self.key)) + '.'
      json_data['key'] = self.key

    if self.label:
      assert isinstance(self.label, str), 'Wrong type for attribute: label. Expected: str. Got: ' + str(type(self.label)) + '.'
      json_data['label'] = self.label

    if self.labels:
      assert isinstance(self.labels, list), 'Wrong type for attribute: labels. Expected: list. Got: ' + str(type(self.labels)) + '.'
      obj_list = []
      for item in self.labels:
        obj_list.append(item.to_json())
      json_data['metricLabels'] = obj_list

    if self.last_terminated_program:
      assert isinstance(self.last_terminated_program, str), 'Wrong type for attribute: last_terminated_program. Expected: str. Got: ' + str(type(self.last_terminated_program)) + '.'
      json_data['lastTerminatedProgram'] = self.last_terminated_program

    if self.level:
      assert isinstance(self.level, float) or isinstance(self.level, int), 'Wrong type for attribute: level. Expected: float. Got: ' + str(type(self.level)) + '.'
      json_data['level'] = self.level

    if self.local_ts:
      assert isinstance(self.local_ts, int), 'Wrong type for attribute: local_ts. Expected: int. Got: ' + str(type(self.local_ts)) + '.'
      json_data['localTS'] = self.local_ts

    if self.machine_description:
      assert self.machine_description.__class__.__name__ == 'MachineDescription', 'Wrong type for attribute: machine_description. Expected: MachineDescription. Got: ' + str(type(self.machine_description)) + '.'
      json_data['machineDescription'] = self.machine_description.to_json()

    if self.machine_interfaces:
      assert self.machine_interfaces.__class__.__name__ == 'MachineInterfaces', 'Wrong type for attribute: machine_interfaces. Expected: MachineInterfaces. Got: ' + str(type(self.machine_interfaces)) + '.'
      json_data['machineInterfaces'] = self.machine_interfaces.to_json()

    if self.message:
      assert isinstance(self.message, str), 'Wrong type for attribute: message. Expected: str. Got: ' + str(type(self.message)) + '.'
      json_data['message'] = self.message

    if self.message_last_timestamps:
      assert isinstance(self.message_last_timestamps, list), 'Wrong type for attribute: message_last_timestamps. Expected: list. Got: ' + str(type(self.message_last_timestamps)) + '.'
      obj_list = []
      for item in self.message_last_timestamps:
        obj_list.append(item.to_json())
      json_data['messageLastTimestamps'] = obj_list

    if self.metadata:
      assert self.metadata.__class__.__name__ == 'Metadata', 'Wrong type for attribute: metadata. Expected: Metadata. Got: ' + str(type(self.metadata)) + '.'
      json_data['metadata'] = self.metadata.to_json()

    if self.metric_value:
      assert self.metric_value.__class__.__name__ == 'KeyValue', 'Wrong type for attribute: metric_value. Expected: KeyValue. Got: ' + str(type(self.metric_value)) + '.'
      json_data['metricValue'] = self.metric_value.to_json()

    if self.on:
      assert isinstance(self.on, bool), 'Wrong type for attribute: on. Expected: bool. Got: ' + str(type(self.on)) + '.'
      json_data['on'] = self.on

    if self.operator_type:
      assert isinstance(self.operator_type, str), 'Wrong type for attribute: operator_type. Expected: str. Got: ' + str(type(self.operator_type)) + '.'
      json_data['operatorType'] = self.operator_type

    if self.operator_uid:
      assert isinstance(self.operator_uid, str), 'Wrong type for attribute: operator_uid. Expected: str. Got: ' + str(type(self.operator_uid)) + '.'
      json_data['operatorUID'] = self.operator_uid

    if self.pick_label:
      assert self.pick_label.__class__.__name__ == 'PickLabel', 'Wrong type for attribute: pick_label. Expected: PickLabel. Got: ' + str(type(self.pick_label)) + '.'
      json_data['pickLabel'] = self.pick_label.to_json()

    if self.pick_points:
      assert isinstance(self.pick_points, list), 'Wrong type for attribute: pick_points. Expected: list. Got: ' + str(type(self.pick_points)) + '.'
      obj_list = []
      for item in self.pick_points:
        obj_list.append(item.to_json())
      json_data['pickPoints'] = obj_list

    if self.pipeline_description:
      assert self.pipeline_description.__class__.__name__ == 'PipelineDescription', 'Wrong type for attribute: pipeline_description. Expected: PipelineDescription. Got: ' + str(type(self.pipeline_description)) + '.'
      json_data['pipelineDescription'] = self.pipeline_description.to_json()

    if self.place_label:
      assert self.place_label.__class__.__name__ == 'PlaceLabel', 'Wrong type for attribute: place_label. Expected: PlaceLabel. Got: ' + str(type(self.place_label)) + '.'
      json_data['placeLabel'] = self.place_label.to_json()

    if self.place_position_3d:
      assert isinstance(self.place_position_3d, list), 'Wrong type for attribute: place_position_3d. Expected: list. Got: ' + str(type(self.place_position_3d)) + '.'
      obj_list = []
      for item in self.place_position_3d:
        obj_list.append(item.to_json())
      json_data['placePosition3D'] = obj_list

    if self.place_quaternion_3d:
      assert isinstance(self.place_quaternion_3d, list), 'Wrong type for attribute: place_quaternion_3d. Expected: list. Got: ' + str(type(self.place_quaternion_3d)) + '.'
      obj_list = []
      for item in self.place_quaternion_3d:
        obj_list.append(item.to_json())
      json_data['placeQuaternion3D'] = obj_list

    if self.pose:
      assert isinstance(self.pose, list), 'Wrong type for attribute: pose. Expected: list. Got: ' + str(type(self.pose)) + '.'
      json_data['pose'] = self.pose

    if self.position_3d:
      assert isinstance(self.position_3d, list), 'Wrong type for attribute: position_3d. Expected: list. Got: ' + str(type(self.position_3d)) + '.'
      obj_list = []
      for item in self.position_3d:
        obj_list.append(item.to_json())
      json_data['position3D'] = obj_list

    if self.prediction_type:
      assert isinstance(self.prediction_type, str), 'Wrong type for attribute: prediction_type. Expected: str. Got: ' + str(type(self.prediction_type)) + '.'
      json_data['predictionType'] = self.prediction_type

    if self.program_counter:
      assert isinstance(self.program_counter, int), 'Wrong type for attribute: program_counter. Expected: int. Got: ' + str(type(self.program_counter)) + '.'
      json_data['programCounter'] = self.program_counter

    if self.progress:
      assert isinstance(self.progress, float) or isinstance(self.progress, int), 'Wrong type for attribute: progress. Expected: float. Got: ' + str(type(self.progress)) + '.'
      json_data['progress'] = self.progress

    if self.quaternion_3d:
      assert isinstance(self.quaternion_3d, list), 'Wrong type for attribute: quaternion_3d. Expected: list. Got: ' + str(type(self.quaternion_3d)) + '.'
      obj_list = []
      for item in self.quaternion_3d:
        obj_list.append(item.to_json())
      json_data['quaternion3D'] = obj_list

    if self.relay:
      assert isinstance(self.relay, str), 'Wrong type for attribute: relay. Expected: str. Got: ' + str(type(self.relay)) + '.'
      json_data['relay'] = self.relay

    if self.remote_ts:
      assert isinstance(self.remote_ts, int), 'Wrong type for attribute: remote_ts. Expected: int. Got: ' + str(type(self.remote_ts)) + '.'
      json_data['remoteTS'] = self.remote_ts

    if self.report_error:
      assert self.report_error.__class__.__name__ == 'ReportError', 'Wrong type for attribute: report_error. Expected: ReportError. Got: ' + str(type(self.report_error)) + '.'
      json_data['reportError'] = self.report_error.to_json()

    if self.request_type:
      assert isinstance(self.request_type, str), 'Wrong type for attribute: request_type. Expected: str. Got: ' + str(type(self.request_type)) + '.'
      json_data['requestType'] = self.request_type

    if self.robot_current_a:
      assert isinstance(self.robot_current_a, float) or isinstance(self.robot_current_a, int), 'Wrong type for attribute: robot_current_a. Expected: float. Got: ' + str(type(self.robot_current_a)) + '.'
      json_data['robotCurrentA'] = self.robot_current_a

    if self.robot_dexterity:
      assert isinstance(self.robot_dexterity, float) or isinstance(self.robot_dexterity, int), 'Wrong type for attribute: robot_dexterity. Expected: float. Got: ' + str(type(self.robot_dexterity)) + '.'
      json_data['robotDexterity'] = self.robot_dexterity

    if self.robot_id:
      assert isinstance(self.robot_id, str), 'Wrong type for attribute: robot_id. Expected: str. Got: ' + str(type(self.robot_id)) + '.'
      json_data['robotID'] = self.robot_id

    if self.robot_mode:
      assert isinstance(self.robot_mode, str), 'Wrong type for attribute: robot_mode. Expected: str. Got: ' + str(type(self.robot_mode)) + '.'
      json_data['robotMode'] = self.robot_mode

    if self.robot_name:
      assert isinstance(self.robot_name, str), 'Wrong type for attribute: robot_name. Expected: str. Got: ' + str(type(self.robot_name)) + '.'
      json_data['robotName'] = self.robot_name

    if self.robot_power_state:
      assert self.robot_power_state.__class__.__name__ == 'RobotPowerState', 'Wrong type for attribute: robot_power_state. Expected: RobotPowerState. Got: ' + str(type(self.robot_power_state)) + '.'
      json_data['robotPowerState'] = self.robot_power_state.to_json()

    if self.robot_power_state_update:
      assert self.robot_power_state_update.__class__.__name__ == 'RobotPowerState', 'Wrong type for attribute: robot_power_state_update. Expected: RobotPowerState. Got: ' + str(type(self.robot_power_state_update)) + '.'
      json_data['robotPowerStateUpdate'] = self.robot_power_state_update.to_json()

    if self.robot_voltage_v:
      assert isinstance(self.robot_voltage_v, float) or isinstance(self.robot_voltage_v, int), 'Wrong type for attribute: robot_voltage_v. Expected: float. Got: ' + str(type(self.robot_voltage_v)) + '.'
      json_data['robotVoltageV'] = self.robot_voltage_v

    if self.safety_message:
      assert isinstance(self.safety_message, str), 'Wrong type for attribute: safety_message. Expected: str. Got: ' + str(type(self.safety_message)) + '.'
      json_data['safetyMessage'] = self.safety_message

    if self.safety_version:
      assert isinstance(self.safety_version, str), 'Wrong type for attribute: safety_version. Expected: str. Got: ' + str(type(self.safety_version)) + '.'
      json_data['safetyVersion'] = self.safety_version

    if self.script:
      assert isinstance(self.script, str), 'Wrong type for attribute: script. Expected: str. Got: ' + str(type(self.script)) + '.'
      json_data['script'] = self.script

    if self.send_to_clients:
      assert isinstance(self.send_to_clients, list), 'Wrong type for attribute: send_to_clients. Expected: list. Got: ' + str(type(self.send_to_clients)) + '.'
      obj_list = []
      for item in self.send_to_clients:
        obj_list.append(item.to_json())
      json_data['sendToClients'] = obj_list

    if self.sensor_in:
      assert isinstance(self.sensor_in, list), 'Wrong type for attribute: sensor_in. Expected: list. Got: ' + str(type(self.sensor_in)) + '.'
      json_data['sensorIn'] = self.sensor_in

    if self.seq:
      assert isinstance(self.seq, int), 'Wrong type for attribute: seq. Expected: int. Got: ' + str(type(self.seq)) + '.'
      json_data['seq'] = self.seq

    if self.session_id:
      assert isinstance(self.session_id, str), 'Wrong type for attribute: session_id. Expected: str. Got: ' + str(type(self.session_id)) + '.'
      json_data['sessionID'] = self.session_id

    if self.sim_instance_segmentation:
      assert self.sim_instance_segmentation.__class__.__name__ == 'SimInstanceSegmentation', 'Wrong type for attribute: sim_instance_segmentation. Expected: SimInstanceSegmentation. Got: ' + str(type(self.sim_instance_segmentation)) + '.'
      json_data['simInstanceSegmentation'] = self.sim_instance_segmentation.to_json()

    if self.sim_state:
      assert self.sim_state.__class__.__name__ == 'SimState', 'Wrong type for attribute: sim_state. Expected: SimState. Got: ' + str(type(self.sim_state)) + '.'
      json_data['simState'] = self.sim_state.to_json()

    if self.start_time:
      assert isinstance(self.start_time, int), 'Wrong type for attribute: start_time. Expected: int. Got: ' + str(type(self.start_time)) + '.'
      json_data['startTime'] = self.start_time

    if self.state:
      assert isinstance(self.state, list), 'Wrong type for attribute: state. Expected: list. Got: ' + str(type(self.state)) + '.'
      obj_list = []
      for item in self.state:
        obj_list.append(item.to_json())
      json_data['state'] = obj_list

    if self.status:
      assert isinstance(self.status, str), 'Wrong type for attribute: status. Expected: str. Got: ' + str(type(self.status)) + '.'
      json_data['status'] = self.status

    if self.tag:
      assert isinstance(self.tag, str), 'Wrong type for attribute: tag. Expected: str. Got: ' + str(type(self.tag)) + '.'
      json_data['tag'] = self.tag

    if self.task_code:
      assert isinstance(self.task_code, str), 'Wrong type for attribute: task_code. Expected: str. Got: ' + str(type(self.task_code)) + '.'
      json_data['taskCode'] = self.task_code

    if self.text_instruction:
      assert self.text_instruction.__class__.__name__ == 'TextInstruction', 'Wrong type for attribute: text_instruction. Expected: TextInstruction. Got: ' + str(type(self.text_instruction)) + '.'
      json_data['textInstruction'] = self.text_instruction.to_json()

    if self.tool_analog_in:
      assert isinstance(self.tool_analog_in, list), 'Wrong type for attribute: tool_analog_in. Expected: list. Got: ' + str(type(self.tool_analog_in)) + '.'
      json_data['toolAnalogIn'] = self.tool_analog_in

    if self.tool_analog_out:
      assert isinstance(self.tool_analog_out, list), 'Wrong type for attribute: tool_analog_out. Expected: list. Got: ' + str(type(self.tool_analog_out)) + '.'
      json_data['toolAnalogOut'] = self.tool_analog_out

    if self.tool_current_a:
      assert isinstance(self.tool_current_a, float) or isinstance(self.tool_current_a, int), 'Wrong type for attribute: tool_current_a. Expected: float. Got: ' + str(type(self.tool_current_a)) + '.'
      json_data['toolCurrentA'] = self.tool_current_a

    if self.tool_digital_in:
      assert isinstance(self.tool_digital_in, list), 'Wrong type for attribute: tool_digital_in. Expected: list. Got: ' + str(type(self.tool_digital_in)) + '.'
      json_data['toolDigitalIn'] = self.tool_digital_in

    if self.tool_digital_out:
      assert isinstance(self.tool_digital_out, list), 'Wrong type for attribute: tool_digital_out. Expected: list. Got: ' + str(type(self.tool_digital_out)) + '.'
      json_data['toolDigitalOut'] = self.tool_digital_out

    if self.tool_temp_c:
      assert isinstance(self.tool_temp_c, float) or isinstance(self.tool_temp_c, int), 'Wrong type for attribute: tool_temp_c. Expected: float. Got: ' + str(type(self.tool_temp_c)) + '.'
      json_data['toolTempC'] = self.tool_temp_c

    if self.tool_voltage_v:
      assert isinstance(self.tool_voltage_v, float) or isinstance(self.tool_voltage_v, int), 'Wrong type for attribute: tool_voltage_v. Expected: float. Got: ' + str(type(self.tool_voltage_v)) + '.'
      json_data['toolVoltageV'] = self.tool_voltage_v

    if self.torque:
      assert isinstance(self.torque, list), 'Wrong type for attribute: torque. Expected: list. Got: ' + str(type(self.torque)) + '.'
      json_data['torque'] = self.torque

    if self.transport:
      assert isinstance(self.transport, str), 'Wrong type for attribute: transport. Expected: str. Got: ' + str(type(self.transport)) + '.'
      json_data['transport'] = self.transport

    if self.ts:
      assert isinstance(self.ts, int), 'Wrong type for attribute: ts. Expected: int. Got: ' + str(type(self.ts)) + '.'
      json_data['ts'] = self.ts

    if self.ui_version:
      assert isinstance(self.ui_version, str), 'Wrong type for attribute: ui_version. Expected: str. Got: ' + str(type(self.ui_version)) + '.'
      json_data['uiVersion'] = self.ui_version

    if self.uncompressed_depth:
      assert isinstance(self.uncompressed_depth, str), 'Wrong type for attribute: uncompressed_depth. Expected: str. Got: ' + str(type(self.uncompressed_depth)) + '.'
      json_data['uncompressedDepth'] = self.uncompressed_depth

    if self.upload_depth:
      assert isinstance(self.upload_depth, str), 'Wrong type for attribute: upload_depth. Expected: str. Got: ' + str(type(self.upload_depth)) + '.'
      json_data['uploadDepth'] = self.upload_depth

    if self.vacuum_level_pa:
      assert isinstance(self.vacuum_level_pa, float) or isinstance(self.vacuum_level_pa, int), 'Wrong type for attribute: vacuum_level_pa. Expected: float. Got: ' + str(type(self.vacuum_level_pa)) + '.'
      json_data['vacuumLevelPa'] = self.vacuum_level_pa

    if self.value:
      assert isinstance(self.value, str), 'Wrong type for attribute: value. Expected: str. Got: ' + str(type(self.value)) + '.'
      json_data['value'] = self.value

    if self.webrtc_audio_request:
      assert self.webrtc_audio_request.__class__.__name__ == 'WebrtcAudioRequest', 'Wrong type for attribute: webrtc_audio_request. Expected: WebrtcAudioRequest. Got: ' + str(type(self.webrtc_audio_request)) + '.'
      json_data['webrtcAudioRequest'] = self.webrtc_audio_request.to_json()

    if self.webrtc_audio_response:
      assert self.webrtc_audio_response.__class__.__name__ == 'WebrtcAudioResponse', 'Wrong type for attribute: webrtc_audio_response. Expected: WebrtcAudioResponse. Got: ' + str(type(self.webrtc_audio_response)) + '.'
      json_data['webrtcAudioResponse'] = self.webrtc_audio_response.to_json()

    if self.workcell_io_version:
      assert isinstance(self.workcell_io_version, str), 'Wrong type for attribute: workcell_io_version. Expected: str. Got: ' + str(type(self.workcell_io_version)) + '.'
      json_data['workcellIOVersion'] = self.workcell_io_version

    if self.workcell_setup_version:
      assert isinstance(self.workcell_setup_version, str), 'Wrong type for attribute: workcell_setup_version. Expected: str. Got: ' + str(type(self.workcell_setup_version)) + '.'
      json_data['workcellSetupVersion'] = self.workcell_setup_version

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'DeviceData':
    """Convert JSON to type object."""
    obj = DeviceData()
    json_list: List[Any]

    expected_json_keys: List[str] = ['acceptDepthEncoding', 'actionsetsVersion', 'analogBank', 'analogIn', 'analogOut', 'audioRequestMute', 'audioRequestUnmute', 'boardIOCurrentA', 'boardTempC', 'calibrationVersion', 'clientAnnotation', 'clientOS', 'clientSessionUID', 'code', 'color', 'colorIntrinsics', 'colorTS', 'compressedDepth', 'confidence', 'connectedClients', 'constraintsVersion', 'dataType', 'depth', 'depthIntrinsics', 'depthTS', 'detection', 'deviceName', 'deviceType', 'digitalBank', 'digitalIn', 'digitalOut', 'error', 'eventParams', 'experimentToken', 'floatValue', 'force', 'hint', 'history', 'inhibitFrameSave', 'inhibitFrameSend', 'intValue', 'integerBank', 'intent', 'isEmergencyStopped', 'isObjectDetected', 'isProgramRunning', 'isProtectiveStopped', 'isReducedMode', 'isRobotPowerOn', 'isSafeguardStopped', 'jointCurrentsA', 'jointTempsC', 'jointVoltagesV', 'joints', 'key', 'label', 'metricLabels', 'lastTerminatedProgram', 'level', 'localTS', 'machineDescription', 'machineInterfaces', 'message', 'messageLastTimestamps', 'metadata', 'metricValue', 'on', 'operatorType', 'operatorUID', 'pickLabel', 'pickPoints', 'pipelineDescription', 'placeLabel', 'placePosition3D', 'placeQuaternion3D', 'pose', 'position3D', 'predictionType', 'programCounter', 'progress', 'quaternion3D', 'relay', 'remoteTS', 'reportError', 'requestType', 'robotCurrentA', 'robotDexterity', 'robotID', 'robotMode', 'robotName', 'robotPowerState', 'robotPowerStateUpdate', 'robotVoltageV', 'safetyMessage', 'safetyVersion', 'script', 'sendToClients', 'sensorIn', 'seq', 'sessionID', 'simInstanceSegmentation', 'simState', 'startTime', 'state', 'status', 'tag', 'taskCode', 'textInstruction', 'toolAnalogIn', 'toolAnalogOut', 'toolCurrentA', 'toolDigitalIn', 'toolDigitalOut', 'toolTempC', 'toolVoltageV', 'torque', 'transport', 'ts', 'uiVersion', 'uncompressedDepth', 'uploadDepth', 'vacuumLevelPa', 'value', 'webrtcAudioRequest', 'webrtcAudioResponse', 'workcellIOVersion', 'workcellSetupVersion']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid DeviceData. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'acceptDepthEncoding' in json_data:
      assert isinstance(json_data['acceptDepthEncoding'], list), 'Wrong type for attribute: acceptDepthEncoding. Expected: list. Got: ' + str(type(json_data['acceptDepthEncoding'])) + '.'
      json_list = []
      for j in json_data['acceptDepthEncoding']:
        json_list.append(j)
      obj.accept_depth_encoding = json_list

    if 'actionsetsVersion' in json_data:
      assert isinstance(json_data['actionsetsVersion'], str), 'Wrong type for attribute: actionsetsVersion. Expected: str. Got: ' + str(type(json_data['actionsetsVersion'])) + '.'
      obj.actionsets_version = json_data['actionsetsVersion']

    if 'analogBank' in json_data:
      assert isinstance(json_data['analogBank'], list), 'Wrong type for attribute: analogBank. Expected: list. Got: ' + str(type(json_data['analogBank'])) + '.'
      json_list = []
      for j in json_data['analogBank']:
        json_list.append(AnalogBank.from_json(j))
      obj.analog_bank = json_list

    if 'analogIn' in json_data:
      assert isinstance(json_data['analogIn'], list), 'Wrong type for attribute: analogIn. Expected: list. Got: ' + str(type(json_data['analogIn'])) + '.'
      json_list = []
      for j in json_data['analogIn']:
        json_list.append(j)
      obj.analog_in = json_list

    if 'analogOut' in json_data:
      assert isinstance(json_data['analogOut'], list), 'Wrong type for attribute: analogOut. Expected: list. Got: ' + str(type(json_data['analogOut'])) + '.'
      json_list = []
      for j in json_data['analogOut']:
        json_list.append(j)
      obj.analog_out = json_list

    if 'audioRequestMute' in json_data:
      assert isinstance(json_data['audioRequestMute'], dict), 'Wrong type for attribute: audioRequestMute. Expected: dict. Got: ' + str(type(json_data['audioRequestMute'])) + '.'
      obj.audio_request_mute = AudioRequest.from_json(json_data['audioRequestMute'])

    if 'audioRequestUnmute' in json_data:
      assert isinstance(json_data['audioRequestUnmute'], dict), 'Wrong type for attribute: audioRequestUnmute. Expected: dict. Got: ' + str(type(json_data['audioRequestUnmute'])) + '.'
      obj.audio_request_unmute = AudioRequest.from_json(json_data['audioRequestUnmute'])

    if 'boardIOCurrentA' in json_data:
      assert isinstance(json_data['boardIOCurrentA'], float) or isinstance(json_data['boardIOCurrentA'], int), 'Wrong type for attribute: boardIOCurrentA. Expected: float. Got: ' + str(type(json_data['boardIOCurrentA'])) + '.'
      obj.board_io_current_a = json_data['boardIOCurrentA']

    if 'boardTempC' in json_data:
      assert isinstance(json_data['boardTempC'], float) or isinstance(json_data['boardTempC'], int), 'Wrong type for attribute: boardTempC. Expected: float. Got: ' + str(type(json_data['boardTempC'])) + '.'
      obj.board_temp_c = json_data['boardTempC']

    if 'calibrationVersion' in json_data:
      assert isinstance(json_data['calibrationVersion'], str), 'Wrong type for attribute: calibrationVersion. Expected: str. Got: ' + str(type(json_data['calibrationVersion'])) + '.'
      obj.calibration_version = json_data['calibrationVersion']

    if 'clientAnnotation' in json_data:
      assert isinstance(json_data['clientAnnotation'], dict), 'Wrong type for attribute: clientAnnotation. Expected: dict. Got: ' + str(type(json_data['clientAnnotation'])) + '.'
      obj.client_annotation = ClientAnnotation.from_json(json_data['clientAnnotation'])

    if 'clientOS' in json_data:
      assert isinstance(json_data['clientOS'], str), 'Wrong type for attribute: clientOS. Expected: str. Got: ' + str(type(json_data['clientOS'])) + '.'
      obj.client_os = json_data['clientOS']

    if 'clientSessionUID' in json_data:
      assert isinstance(json_data['clientSessionUID'], str), 'Wrong type for attribute: clientSessionUID. Expected: str. Got: ' + str(type(json_data['clientSessionUID'])) + '.'
      obj.client_session_uid = json_data['clientSessionUID']

    if 'code' in json_data:
      assert isinstance(json_data['code'], int), 'Wrong type for attribute: code. Expected: int. Got: ' + str(type(json_data['code'])) + '.'
      obj.code = json_data['code']

    if 'color' in json_data:
      assert isinstance(json_data['color'], str), 'Wrong type for attribute: color. Expected: str. Got: ' + str(type(json_data['color'])) + '.'
      obj.color = json_data['color']

    if 'colorIntrinsics' in json_data:
      assert isinstance(json_data['colorIntrinsics'], list), 'Wrong type for attribute: colorIntrinsics. Expected: list. Got: ' + str(type(json_data['colorIntrinsics'])) + '.'
      json_list = []
      for j in json_data['colorIntrinsics']:
        json_list.append(j)
      obj.color_intrinsics = json_list

    if 'colorTS' in json_data:
      assert isinstance(json_data['colorTS'], int), 'Wrong type for attribute: colorTS. Expected: int. Got: ' + str(type(json_data['colorTS'])) + '.'
      obj.color_ts = json_data['colorTS']

    if 'compressedDepth' in json_data:
      assert isinstance(json_data['compressedDepth'], list), 'Wrong type for attribute: compressedDepth. Expected: list. Got: ' + str(type(json_data['compressedDepth'])) + '.'
      json_list = []
      for j in json_data['compressedDepth']:
        json_list.append(CompressedDepth.from_json(j))
      obj.compressed_depth = json_list

    if 'confidence' in json_data:
      assert isinstance(json_data['confidence'], list), 'Wrong type for attribute: confidence. Expected: list. Got: ' + str(type(json_data['confidence'])) + '.'
      json_list = []
      for j in json_data['confidence']:
        json_list.append(j)
      obj.confidence = json_list

    if 'connectedClients' in json_data:
      assert isinstance(json_data['connectedClients'], dict), 'Wrong type for attribute: connectedClients. Expected: dict. Got: ' + str(type(json_data['connectedClients'])) + '.'
      obj.connected_clients = ConnectedClients.from_json(json_data['connectedClients'])

    if 'constraintsVersion' in json_data:
      assert isinstance(json_data['constraintsVersion'], str), 'Wrong type for attribute: constraintsVersion. Expected: str. Got: ' + str(type(json_data['constraintsVersion'])) + '.'
      obj.constraints_version = json_data['constraintsVersion']

    if 'dataType' in json_data:
      assert isinstance(json_data['dataType'], str), 'Wrong type for attribute: dataType. Expected: str. Got: ' + str(type(json_data['dataType'])) + '.'
      obj.data_type = json_data['dataType']

    if 'depth' in json_data:
      assert isinstance(json_data['depth'], str), 'Wrong type for attribute: depth. Expected: str. Got: ' + str(type(json_data['depth'])) + '.'
      obj.depth = json_data['depth']

    if 'depthIntrinsics' in json_data:
      assert isinstance(json_data['depthIntrinsics'], list), 'Wrong type for attribute: depthIntrinsics. Expected: list. Got: ' + str(type(json_data['depthIntrinsics'])) + '.'
      json_list = []
      for j in json_data['depthIntrinsics']:
        json_list.append(j)
      obj.depth_intrinsics = json_list

    if 'depthTS' in json_data:
      assert isinstance(json_data['depthTS'], int), 'Wrong type for attribute: depthTS. Expected: int. Got: ' + str(type(json_data['depthTS'])) + '.'
      obj.depth_ts = json_data['depthTS']

    if 'detection' in json_data:
      assert isinstance(json_data['detection'], dict), 'Wrong type for attribute: detection. Expected: dict. Got: ' + str(type(json_data['detection'])) + '.'
      obj.detection = Detection.from_json(json_data['detection'])

    if 'deviceName' in json_data:
      assert isinstance(json_data['deviceName'], str), 'Wrong type for attribute: deviceName. Expected: str. Got: ' + str(type(json_data['deviceName'])) + '.'
      obj.device_name = json_data['deviceName']

    if 'deviceType' in json_data:
      assert isinstance(json_data['deviceType'], str), 'Wrong type for attribute: deviceType. Expected: str. Got: ' + str(type(json_data['deviceType'])) + '.'
      obj.device_type = json_data['deviceType']

    if 'digitalBank' in json_data:
      assert isinstance(json_data['digitalBank'], list), 'Wrong type for attribute: digitalBank. Expected: list. Got: ' + str(type(json_data['digitalBank'])) + '.'
      json_list = []
      for j in json_data['digitalBank']:
        json_list.append(DigitalBank.from_json(j))
      obj.digital_bank = json_list

    if 'digitalIn' in json_data:
      assert isinstance(json_data['digitalIn'], list), 'Wrong type for attribute: digitalIn. Expected: list. Got: ' + str(type(json_data['digitalIn'])) + '.'
      json_list = []
      for j in json_data['digitalIn']:
        json_list.append(j)
      obj.digital_in = json_list

    if 'digitalOut' in json_data:
      assert isinstance(json_data['digitalOut'], list), 'Wrong type for attribute: digitalOut. Expected: list. Got: ' + str(type(json_data['digitalOut'])) + '.'
      json_list = []
      for j in json_data['digitalOut']:
        json_list.append(j)
      obj.digital_out = json_list

    if 'error' in json_data:
      assert isinstance(json_data['error'], str), 'Wrong type for attribute: error. Expected: str. Got: ' + str(type(json_data['error'])) + '.'
      obj.error = json_data['error']

    if 'eventParams' in json_data:
      assert isinstance(json_data['eventParams'], list), 'Wrong type for attribute: eventParams. Expected: list. Got: ' + str(type(json_data['eventParams'])) + '.'
      json_list = []
      for j in json_data['eventParams']:
        json_list.append(KeyValue.from_json(j))
      obj.event_params = json_list

    if 'experimentToken' in json_data:
      assert isinstance(json_data['experimentToken'], str), 'Wrong type for attribute: experimentToken. Expected: str. Got: ' + str(type(json_data['experimentToken'])) + '.'
      obj.experiment_token = json_data['experimentToken']

    if 'floatValue' in json_data:
      assert isinstance(json_data['floatValue'], float) or isinstance(json_data['floatValue'], int), 'Wrong type for attribute: floatValue. Expected: float. Got: ' + str(type(json_data['floatValue'])) + '.'
      obj.float_value = json_data['floatValue']

    if 'force' in json_data:
      assert isinstance(json_data['force'], list), 'Wrong type for attribute: force. Expected: list. Got: ' + str(type(json_data['force'])) + '.'
      json_list = []
      for j in json_data['force']:
        json_list.append(j)
      obj.force = json_list

    if 'hint' in json_data:
      assert isinstance(json_data['hint'], str), 'Wrong type for attribute: hint. Expected: str. Got: ' + str(type(json_data['hint'])) + '.'
      obj.hint = json_data['hint']

    if 'history' in json_data:
      assert isinstance(json_data['history'], dict), 'Wrong type for attribute: history. Expected: dict. Got: ' + str(type(json_data['history'])) + '.'
      obj.history = History.from_json(json_data['history'])

    if 'inhibitFrameSave' in json_data:
      assert isinstance(json_data['inhibitFrameSave'], bool), 'Wrong type for attribute: inhibitFrameSave. Expected: bool. Got: ' + str(type(json_data['inhibitFrameSave'])) + '.'
      obj.inhibit_frame_save = json_data['inhibitFrameSave']

    if 'inhibitFrameSend' in json_data:
      assert isinstance(json_data['inhibitFrameSend'], bool), 'Wrong type for attribute: inhibitFrameSend. Expected: bool. Got: ' + str(type(json_data['inhibitFrameSend'])) + '.'
      obj.inhibit_frame_send = json_data['inhibitFrameSend']

    if 'intValue' in json_data:
      assert isinstance(json_data['intValue'], int), 'Wrong type for attribute: intValue. Expected: int. Got: ' + str(type(json_data['intValue'])) + '.'
      obj.int_value = json_data['intValue']

    if 'integerBank' in json_data:
      assert isinstance(json_data['integerBank'], list), 'Wrong type for attribute: integerBank. Expected: list. Got: ' + str(type(json_data['integerBank'])) + '.'
      json_list = []
      for j in json_data['integerBank']:
        json_list.append(IntegerBank.from_json(j))
      obj.integer_bank = json_list

    if 'intent' in json_data:
      assert isinstance(json_data['intent'], str), 'Wrong type for attribute: intent. Expected: str. Got: ' + str(type(json_data['intent'])) + '.'
      obj.intent = json_data['intent']

    if 'isEmergencyStopped' in json_data:
      assert isinstance(json_data['isEmergencyStopped'], bool), 'Wrong type for attribute: isEmergencyStopped. Expected: bool. Got: ' + str(type(json_data['isEmergencyStopped'])) + '.'
      obj.is_emergency_stopped = json_data['isEmergencyStopped']

    if 'isObjectDetected' in json_data:
      assert isinstance(json_data['isObjectDetected'], bool), 'Wrong type for attribute: isObjectDetected. Expected: bool. Got: ' + str(type(json_data['isObjectDetected'])) + '.'
      obj.is_object_detected = json_data['isObjectDetected']

    if 'isProgramRunning' in json_data:
      assert isinstance(json_data['isProgramRunning'], bool), 'Wrong type for attribute: isProgramRunning. Expected: bool. Got: ' + str(type(json_data['isProgramRunning'])) + '.'
      obj.is_program_running = json_data['isProgramRunning']

    if 'isProtectiveStopped' in json_data:
      assert isinstance(json_data['isProtectiveStopped'], bool), 'Wrong type for attribute: isProtectiveStopped. Expected: bool. Got: ' + str(type(json_data['isProtectiveStopped'])) + '.'
      obj.is_protective_stopped = json_data['isProtectiveStopped']

    if 'isReducedMode' in json_data:
      assert isinstance(json_data['isReducedMode'], bool), 'Wrong type for attribute: isReducedMode. Expected: bool. Got: ' + str(type(json_data['isReducedMode'])) + '.'
      obj.is_reduced_mode = json_data['isReducedMode']

    if 'isRobotPowerOn' in json_data:
      assert isinstance(json_data['isRobotPowerOn'], bool), 'Wrong type for attribute: isRobotPowerOn. Expected: bool. Got: ' + str(type(json_data['isRobotPowerOn'])) + '.'
      obj.is_robot_power_on = json_data['isRobotPowerOn']

    if 'isSafeguardStopped' in json_data:
      assert isinstance(json_data['isSafeguardStopped'], bool), 'Wrong type for attribute: isSafeguardStopped. Expected: bool. Got: ' + str(type(json_data['isSafeguardStopped'])) + '.'
      obj.is_safeguard_stopped = json_data['isSafeguardStopped']

    if 'jointCurrentsA' in json_data:
      assert isinstance(json_data['jointCurrentsA'], list), 'Wrong type for attribute: jointCurrentsA. Expected: list. Got: ' + str(type(json_data['jointCurrentsA'])) + '.'
      json_list = []
      for j in json_data['jointCurrentsA']:
        json_list.append(j)
      obj.joint_currents_a = json_list

    if 'jointTempsC' in json_data:
      assert isinstance(json_data['jointTempsC'], list), 'Wrong type for attribute: jointTempsC. Expected: list. Got: ' + str(type(json_data['jointTempsC'])) + '.'
      json_list = []
      for j in json_data['jointTempsC']:
        json_list.append(j)
      obj.joint_temps_c = json_list

    if 'jointVoltagesV' in json_data:
      assert isinstance(json_data['jointVoltagesV'], list), 'Wrong type for attribute: jointVoltagesV. Expected: list. Got: ' + str(type(json_data['jointVoltagesV'])) + '.'
      json_list = []
      for j in json_data['jointVoltagesV']:
        json_list.append(j)
      obj.joint_voltages_v = json_list

    if 'joints' in json_data:
      assert isinstance(json_data['joints'], list), 'Wrong type for attribute: joints. Expected: list. Got: ' + str(type(json_data['joints'])) + '.'
      json_list = []
      for j in json_data['joints']:
        json_list.append(j)
      obj.joints = json_list

    if 'key' in json_data:
      assert isinstance(json_data['key'], str), 'Wrong type for attribute: key. Expected: str. Got: ' + str(type(json_data['key'])) + '.'
      obj.key = json_data['key']

    if 'label' in json_data:
      assert isinstance(json_data['label'], str), 'Wrong type for attribute: label. Expected: str. Got: ' + str(type(json_data['label'])) + '.'
      obj.label = json_data['label']

    if 'metricLabels' in json_data:
      assert isinstance(json_data['metricLabels'], list), 'Wrong type for attribute: metricLabels. Expected: list. Got: ' + str(type(json_data['metricLabels'])) + '.'
      json_list = []
      for j in json_data['metricLabels']:
        json_list.append(KeyValue.from_json(j))
      obj.labels = json_list

    if 'lastTerminatedProgram' in json_data:
      assert isinstance(json_data['lastTerminatedProgram'], str), 'Wrong type for attribute: lastTerminatedProgram. Expected: str. Got: ' + str(type(json_data['lastTerminatedProgram'])) + '.'
      obj.last_terminated_program = json_data['lastTerminatedProgram']

    if 'level' in json_data:
      assert isinstance(json_data['level'], float) or isinstance(json_data['level'], int), 'Wrong type for attribute: level. Expected: float. Got: ' + str(type(json_data['level'])) + '.'
      obj.level = json_data['level']

    if 'localTS' in json_data:
      assert isinstance(json_data['localTS'], int), 'Wrong type for attribute: localTS. Expected: int. Got: ' + str(type(json_data['localTS'])) + '.'
      obj.local_ts = json_data['localTS']

    if 'machineDescription' in json_data:
      assert isinstance(json_data['machineDescription'], dict), 'Wrong type for attribute: machineDescription. Expected: dict. Got: ' + str(type(json_data['machineDescription'])) + '.'
      obj.machine_description = MachineDescription.from_json(json_data['machineDescription'])

    if 'machineInterfaces' in json_data:
      assert isinstance(json_data['machineInterfaces'], dict), 'Wrong type for attribute: machineInterfaces. Expected: dict. Got: ' + str(type(json_data['machineInterfaces'])) + '.'
      obj.machine_interfaces = MachineInterfaces.from_json(json_data['machineInterfaces'])

    if 'message' in json_data:
      assert isinstance(json_data['message'], str), 'Wrong type for attribute: message. Expected: str. Got: ' + str(type(json_data['message'])) + '.'
      obj.message = json_data['message']

    if 'messageLastTimestamps' in json_data:
      assert isinstance(json_data['messageLastTimestamps'], list), 'Wrong type for attribute: messageLastTimestamps. Expected: list. Got: ' + str(type(json_data['messageLastTimestamps'])) + '.'
      json_list = []
      for j in json_data['messageLastTimestamps']:
        json_list.append(MessageLastTimestamp.from_json(j))
      obj.message_last_timestamps = json_list

    if 'metadata' in json_data:
      assert isinstance(json_data['metadata'], dict), 'Wrong type for attribute: metadata. Expected: dict. Got: ' + str(type(json_data['metadata'])) + '.'
      obj.metadata = Metadata.from_json(json_data['metadata'])

    if 'metricValue' in json_data:
      assert isinstance(json_data['metricValue'], dict), 'Wrong type for attribute: metricValue. Expected: dict. Got: ' + str(type(json_data['metricValue'])) + '.'
      obj.metric_value = KeyValue.from_json(json_data['metricValue'])

    if 'on' in json_data:
      assert isinstance(json_data['on'], bool), 'Wrong type for attribute: on. Expected: bool. Got: ' + str(type(json_data['on'])) + '.'
      obj.on = json_data['on']

    if 'operatorType' in json_data:
      assert isinstance(json_data['operatorType'], str), 'Wrong type for attribute: operatorType. Expected: str. Got: ' + str(type(json_data['operatorType'])) + '.'
      obj.operator_type = json_data['operatorType']

    if 'operatorUID' in json_data:
      assert isinstance(json_data['operatorUID'], str), 'Wrong type for attribute: operatorUID. Expected: str. Got: ' + str(type(json_data['operatorUID'])) + '.'
      obj.operator_uid = json_data['operatorUID']

    if 'pickLabel' in json_data:
      assert isinstance(json_data['pickLabel'], dict), 'Wrong type for attribute: pickLabel. Expected: dict. Got: ' + str(type(json_data['pickLabel'])) + '.'
      obj.pick_label = PickLabel.from_json(json_data['pickLabel'])

    if 'pickPoints' in json_data:
      assert isinstance(json_data['pickPoints'], list), 'Wrong type for attribute: pickPoints. Expected: list. Got: ' + str(type(json_data['pickPoints'])) + '.'
      json_list = []
      for j in json_data['pickPoints']:
        json_list.append(PickPoint.from_json(j))
      obj.pick_points = json_list

    if 'pipelineDescription' in json_data:
      assert isinstance(json_data['pipelineDescription'], dict), 'Wrong type for attribute: pipelineDescription. Expected: dict. Got: ' + str(type(json_data['pipelineDescription'])) + '.'
      obj.pipeline_description = PipelineDescription.from_json(json_data['pipelineDescription'])

    if 'placeLabel' in json_data:
      assert isinstance(json_data['placeLabel'], dict), 'Wrong type for attribute: placeLabel. Expected: dict. Got: ' + str(type(json_data['placeLabel'])) + '.'
      obj.place_label = PlaceLabel.from_json(json_data['placeLabel'])

    if 'placePosition3D' in json_data:
      assert isinstance(json_data['placePosition3D'], list), 'Wrong type for attribute: placePosition3D. Expected: list. Got: ' + str(type(json_data['placePosition3D'])) + '.'
      json_list = []
      for j in json_data['placePosition3D']:
        json_list.append(Vec3d.from_json(j))
      obj.place_position_3d = json_list

    if 'placeQuaternion3D' in json_data:
      assert isinstance(json_data['placeQuaternion3D'], list), 'Wrong type for attribute: placeQuaternion3D. Expected: list. Got: ' + str(type(json_data['placeQuaternion3D'])) + '.'
      json_list = []
      for j in json_data['placeQuaternion3D']:
        json_list.append(Quaternion3d.from_json(j))
      obj.place_quaternion_3d = json_list

    if 'pose' in json_data:
      assert isinstance(json_data['pose'], list), 'Wrong type for attribute: pose. Expected: list. Got: ' + str(type(json_data['pose'])) + '.'
      json_list = []
      for j in json_data['pose']:
        json_list.append(j)
      obj.pose = json_list

    if 'position3D' in json_data:
      assert isinstance(json_data['position3D'], list), 'Wrong type for attribute: position3D. Expected: list. Got: ' + str(type(json_data['position3D'])) + '.'
      json_list = []
      for j in json_data['position3D']:
        json_list.append(Vec3d.from_json(j))
      obj.position_3d = json_list

    if 'predictionType' in json_data:
      assert isinstance(json_data['predictionType'], str), 'Wrong type for attribute: predictionType. Expected: str. Got: ' + str(type(json_data['predictionType'])) + '.'
      obj.prediction_type = json_data['predictionType']

    if 'programCounter' in json_data:
      assert isinstance(json_data['programCounter'], int), 'Wrong type for attribute: programCounter. Expected: int. Got: ' + str(type(json_data['programCounter'])) + '.'
      obj.program_counter = json_data['programCounter']

    if 'progress' in json_data:
      assert isinstance(json_data['progress'], float) or isinstance(json_data['progress'], int), 'Wrong type for attribute: progress. Expected: float. Got: ' + str(type(json_data['progress'])) + '.'
      obj.progress = json_data['progress']

    if 'quaternion3D' in json_data:
      assert isinstance(json_data['quaternion3D'], list), 'Wrong type for attribute: quaternion3D. Expected: list. Got: ' + str(type(json_data['quaternion3D'])) + '.'
      json_list = []
      for j in json_data['quaternion3D']:
        json_list.append(Quaternion3d.from_json(j))
      obj.quaternion_3d = json_list

    if 'relay' in json_data:
      assert isinstance(json_data['relay'], str), 'Wrong type for attribute: relay. Expected: str. Got: ' + str(type(json_data['relay'])) + '.'
      obj.relay = json_data['relay']

    if 'remoteTS' in json_data:
      assert isinstance(json_data['remoteTS'], int), 'Wrong type for attribute: remoteTS. Expected: int. Got: ' + str(type(json_data['remoteTS'])) + '.'
      obj.remote_ts = json_data['remoteTS']

    if 'reportError' in json_data:
      assert isinstance(json_data['reportError'], dict), 'Wrong type for attribute: reportError. Expected: dict. Got: ' + str(type(json_data['reportError'])) + '.'
      obj.report_error = ReportError.from_json(json_data['reportError'])

    if 'requestType' in json_data:
      assert isinstance(json_data['requestType'], str), 'Wrong type for attribute: requestType. Expected: str. Got: ' + str(type(json_data['requestType'])) + '.'
      obj.request_type = json_data['requestType']

    if 'robotCurrentA' in json_data:
      assert isinstance(json_data['robotCurrentA'], float) or isinstance(json_data['robotCurrentA'], int), 'Wrong type for attribute: robotCurrentA. Expected: float. Got: ' + str(type(json_data['robotCurrentA'])) + '.'
      obj.robot_current_a = json_data['robotCurrentA']

    if 'robotDexterity' in json_data:
      assert isinstance(json_data['robotDexterity'], float) or isinstance(json_data['robotDexterity'], int), 'Wrong type for attribute: robotDexterity. Expected: float. Got: ' + str(type(json_data['robotDexterity'])) + '.'
      obj.robot_dexterity = json_data['robotDexterity']

    if 'robotID' in json_data:
      assert isinstance(json_data['robotID'], str), 'Wrong type for attribute: robotID. Expected: str. Got: ' + str(type(json_data['robotID'])) + '.'
      obj.robot_id = json_data['robotID']

    if 'robotMode' in json_data:
      assert isinstance(json_data['robotMode'], str), 'Wrong type for attribute: robotMode. Expected: str. Got: ' + str(type(json_data['robotMode'])) + '.'
      obj.robot_mode = json_data['robotMode']

    if 'robotName' in json_data:
      assert isinstance(json_data['robotName'], str), 'Wrong type for attribute: robotName. Expected: str. Got: ' + str(type(json_data['robotName'])) + '.'
      obj.robot_name = json_data['robotName']

    if 'robotPowerState' in json_data:
      assert isinstance(json_data['robotPowerState'], dict), 'Wrong type for attribute: robotPowerState. Expected: dict. Got: ' + str(type(json_data['robotPowerState'])) + '.'
      obj.robot_power_state = RobotPowerState.from_json(json_data['robotPowerState'])

    if 'robotPowerStateUpdate' in json_data:
      assert isinstance(json_data['robotPowerStateUpdate'], dict), 'Wrong type for attribute: robotPowerStateUpdate. Expected: dict. Got: ' + str(type(json_data['robotPowerStateUpdate'])) + '.'
      obj.robot_power_state_update = RobotPowerState.from_json(json_data['robotPowerStateUpdate'])

    if 'robotVoltageV' in json_data:
      assert isinstance(json_data['robotVoltageV'], float) or isinstance(json_data['robotVoltageV'], int), 'Wrong type for attribute: robotVoltageV. Expected: float. Got: ' + str(type(json_data['robotVoltageV'])) + '.'
      obj.robot_voltage_v = json_data['robotVoltageV']

    if 'safetyMessage' in json_data:
      assert isinstance(json_data['safetyMessage'], str), 'Wrong type for attribute: safetyMessage. Expected: str. Got: ' + str(type(json_data['safetyMessage'])) + '.'
      obj.safety_message = json_data['safetyMessage']

    if 'safetyVersion' in json_data:
      assert isinstance(json_data['safetyVersion'], str), 'Wrong type for attribute: safetyVersion. Expected: str. Got: ' + str(type(json_data['safetyVersion'])) + '.'
      obj.safety_version = json_data['safetyVersion']

    if 'script' in json_data:
      assert isinstance(json_data['script'], str), 'Wrong type for attribute: script. Expected: str. Got: ' + str(type(json_data['script'])) + '.'
      obj.script = json_data['script']

    if 'sendToClients' in json_data:
      assert isinstance(json_data['sendToClients'], list), 'Wrong type for attribute: sendToClients. Expected: list. Got: ' + str(type(json_data['sendToClients'])) + '.'
      json_list = []
      for j in json_data['sendToClients']:
        json_list.append(SendToClient.from_json(j))
      obj.send_to_clients = json_list

    if 'sensorIn' in json_data:
      assert isinstance(json_data['sensorIn'], list), 'Wrong type for attribute: sensorIn. Expected: list. Got: ' + str(type(json_data['sensorIn'])) + '.'
      json_list = []
      for j in json_data['sensorIn']:
        json_list.append(j)
      obj.sensor_in = json_list

    if 'seq' in json_data:
      assert isinstance(json_data['seq'], int), 'Wrong type for attribute: seq. Expected: int. Got: ' + str(type(json_data['seq'])) + '.'
      obj.seq = json_data['seq']

    if 'sessionID' in json_data:
      assert isinstance(json_data['sessionID'], str), 'Wrong type for attribute: sessionID. Expected: str. Got: ' + str(type(json_data['sessionID'])) + '.'
      obj.session_id = json_data['sessionID']

    if 'simInstanceSegmentation' in json_data:
      assert isinstance(json_data['simInstanceSegmentation'], dict), 'Wrong type for attribute: simInstanceSegmentation. Expected: dict. Got: ' + str(type(json_data['simInstanceSegmentation'])) + '.'
      obj.sim_instance_segmentation = SimInstanceSegmentation.from_json(json_data['simInstanceSegmentation'])

    if 'simState' in json_data:
      assert isinstance(json_data['simState'], dict), 'Wrong type for attribute: simState. Expected: dict. Got: ' + str(type(json_data['simState'])) + '.'
      obj.sim_state = SimState.from_json(json_data['simState'])

    if 'startTime' in json_data:
      assert isinstance(json_data['startTime'], int), 'Wrong type for attribute: startTime. Expected: int. Got: ' + str(type(json_data['startTime'])) + '.'
      obj.start_time = json_data['startTime']

    if 'state' in json_data:
      assert isinstance(json_data['state'], list), 'Wrong type for attribute: state. Expected: list. Got: ' + str(type(json_data['state'])) + '.'
      json_list = []
      for j in json_data['state']:
        json_list.append(CapabilityState.from_json(j))
      obj.state = json_list

    if 'status' in json_data:
      assert isinstance(json_data['status'], str), 'Wrong type for attribute: status. Expected: str. Got: ' + str(type(json_data['status'])) + '.'
      obj.status = json_data['status']

    if 'tag' in json_data:
      assert isinstance(json_data['tag'], str), 'Wrong type for attribute: tag. Expected: str. Got: ' + str(type(json_data['tag'])) + '.'
      obj.tag = json_data['tag']

    if 'taskCode' in json_data:
      assert isinstance(json_data['taskCode'], str), 'Wrong type for attribute: taskCode. Expected: str. Got: ' + str(type(json_data['taskCode'])) + '.'
      obj.task_code = json_data['taskCode']

    if 'textInstruction' in json_data:
      assert isinstance(json_data['textInstruction'], dict), 'Wrong type for attribute: textInstruction. Expected: dict. Got: ' + str(type(json_data['textInstruction'])) + '.'
      obj.text_instruction = TextInstruction.from_json(json_data['textInstruction'])

    if 'toolAnalogIn' in json_data:
      assert isinstance(json_data['toolAnalogIn'], list), 'Wrong type for attribute: toolAnalogIn. Expected: list. Got: ' + str(type(json_data['toolAnalogIn'])) + '.'
      json_list = []
      for j in json_data['toolAnalogIn']:
        json_list.append(j)
      obj.tool_analog_in = json_list

    if 'toolAnalogOut' in json_data:
      assert isinstance(json_data['toolAnalogOut'], list), 'Wrong type for attribute: toolAnalogOut. Expected: list. Got: ' + str(type(json_data['toolAnalogOut'])) + '.'
      json_list = []
      for j in json_data['toolAnalogOut']:
        json_list.append(j)
      obj.tool_analog_out = json_list

    if 'toolCurrentA' in json_data:
      assert isinstance(json_data['toolCurrentA'], float) or isinstance(json_data['toolCurrentA'], int), 'Wrong type for attribute: toolCurrentA. Expected: float. Got: ' + str(type(json_data['toolCurrentA'])) + '.'
      obj.tool_current_a = json_data['toolCurrentA']

    if 'toolDigitalIn' in json_data:
      assert isinstance(json_data['toolDigitalIn'], list), 'Wrong type for attribute: toolDigitalIn. Expected: list. Got: ' + str(type(json_data['toolDigitalIn'])) + '.'
      json_list = []
      for j in json_data['toolDigitalIn']:
        json_list.append(j)
      obj.tool_digital_in = json_list

    if 'toolDigitalOut' in json_data:
      assert isinstance(json_data['toolDigitalOut'], list), 'Wrong type for attribute: toolDigitalOut. Expected: list. Got: ' + str(type(json_data['toolDigitalOut'])) + '.'
      json_list = []
      for j in json_data['toolDigitalOut']:
        json_list.append(j)
      obj.tool_digital_out = json_list

    if 'toolTempC' in json_data:
      assert isinstance(json_data['toolTempC'], float) or isinstance(json_data['toolTempC'], int), 'Wrong type for attribute: toolTempC. Expected: float. Got: ' + str(type(json_data['toolTempC'])) + '.'
      obj.tool_temp_c = json_data['toolTempC']

    if 'toolVoltageV' in json_data:
      assert isinstance(json_data['toolVoltageV'], float) or isinstance(json_data['toolVoltageV'], int), 'Wrong type for attribute: toolVoltageV. Expected: float. Got: ' + str(type(json_data['toolVoltageV'])) + '.'
      obj.tool_voltage_v = json_data['toolVoltageV']

    if 'torque' in json_data:
      assert isinstance(json_data['torque'], list), 'Wrong type for attribute: torque. Expected: list. Got: ' + str(type(json_data['torque'])) + '.'
      json_list = []
      for j in json_data['torque']:
        json_list.append(j)
      obj.torque = json_list

    if 'transport' in json_data:
      assert isinstance(json_data['transport'], str), 'Wrong type for attribute: transport. Expected: str. Got: ' + str(type(json_data['transport'])) + '.'
      obj.transport = json_data['transport']

    if 'ts' in json_data:
      assert isinstance(json_data['ts'], int), 'Wrong type for attribute: ts. Expected: int. Got: ' + str(type(json_data['ts'])) + '.'
      obj.ts = json_data['ts']

    if 'uiVersion' in json_data:
      assert isinstance(json_data['uiVersion'], str), 'Wrong type for attribute: uiVersion. Expected: str. Got: ' + str(type(json_data['uiVersion'])) + '.'
      obj.ui_version = json_data['uiVersion']

    if 'uncompressedDepth' in json_data:
      assert isinstance(json_data['uncompressedDepth'], str), 'Wrong type for attribute: uncompressedDepth. Expected: str. Got: ' + str(type(json_data['uncompressedDepth'])) + '.'
      obj.uncompressed_depth = json_data['uncompressedDepth']

    if 'uploadDepth' in json_data:
      assert isinstance(json_data['uploadDepth'], str), 'Wrong type for attribute: uploadDepth. Expected: str. Got: ' + str(type(json_data['uploadDepth'])) + '.'
      obj.upload_depth = json_data['uploadDepth']

    if 'vacuumLevelPa' in json_data:
      assert isinstance(json_data['vacuumLevelPa'], float) or isinstance(json_data['vacuumLevelPa'], int), 'Wrong type for attribute: vacuumLevelPa. Expected: float. Got: ' + str(type(json_data['vacuumLevelPa'])) + '.'
      obj.vacuum_level_pa = json_data['vacuumLevelPa']

    if 'value' in json_data:
      assert isinstance(json_data['value'], str), 'Wrong type for attribute: value. Expected: str. Got: ' + str(type(json_data['value'])) + '.'
      obj.value = json_data['value']

    if 'webrtcAudioRequest' in json_data:
      assert isinstance(json_data['webrtcAudioRequest'], dict), 'Wrong type for attribute: webrtcAudioRequest. Expected: dict. Got: ' + str(type(json_data['webrtcAudioRequest'])) + '.'
      obj.webrtc_audio_request = WebrtcAudioRequest.from_json(json_data['webrtcAudioRequest'])

    if 'webrtcAudioResponse' in json_data:
      assert isinstance(json_data['webrtcAudioResponse'], dict), 'Wrong type for attribute: webrtcAudioResponse. Expected: dict. Got: ' + str(type(json_data['webrtcAudioResponse'])) + '.'
      obj.webrtc_audio_response = WebrtcAudioResponse.from_json(json_data['webrtcAudioResponse'])

    if 'workcellIOVersion' in json_data:
      assert isinstance(json_data['workcellIOVersion'], str), 'Wrong type for attribute: workcellIOVersion. Expected: str. Got: ' + str(type(json_data['workcellIOVersion'])) + '.'
      obj.workcell_io_version = json_data['workcellIOVersion']

    if 'workcellSetupVersion' in json_data:
      assert isinstance(json_data['workcellSetupVersion'], str), 'Wrong type for attribute: workcellSetupVersion. Expected: str. Got: ' + str(type(json_data['workcellSetupVersion'])) + '.'
      obj.workcell_setup_version = json_data['workcellSetupVersion']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.DeviceData) -> 'DeviceData':
    """Convert DeviceData proto to type object."""
    if not proto:
      return None
    obj = DeviceData()
    if proto.session_info.accept_depth_encoding:
      json_list = []
      for j in proto.session_info.accept_depth_encoding:
        json_list.append(j)
      obj.accept_depth_encoding = json_list
    obj.actionsets_version = get_proto_value(proto.session_info.actionsets_version)
    if proto.ur_state.analog_bank:
      json_list = []
      for j in proto.ur_state.analog_bank:
        json_list.append(AnalogBank.from_proto(j))
      obj.analog_bank = json_list
    if proto.ur_state.analog_in:
      json_list = []
      for j in proto.ur_state.analog_in:
        json_list.append(j)
      obj.analog_in = json_list
    if proto.ur_state.analog_out:
      json_list = []
      for j in proto.ur_state.analog_out:
        json_list.append(j)
      obj.analog_out = json_list
    obj.audio_request_mute = AudioRequest.from_proto(get_proto_field(proto, 'audio_request_mute'))
    obj.audio_request_unmute = AudioRequest.from_proto(get_proto_field(proto, 'audio_request_unmute'))
    obj.board_io_current_a = get_proto_value(proto.ur_state.board_io_current_a)
    obj.board_temp_c = get_proto_value(proto.ur_state.board_temp_c)
    obj.calibration_version = get_proto_value(proto.session_info.calibration_version)
    obj.client_annotation = ClientAnnotation.from_proto(get_proto_field(proto, 'client_annotation'))
    obj.client_os = get_proto_value(proto.session_info.client_os)
    obj.client_session_uid = get_proto_value(proto.session_info.client_session_uid)
    obj.code = get_proto_value(proto.status.code)
    obj.color = get_proto_value(proto.color.color)
    if proto.color.color_intrinsics:
      json_list = []
      for j in proto.color.color_intrinsics:
        json_list.append(j)
      obj.color_intrinsics = json_list
    obj.color_ts = get_proto_value(proto.prediction.color_ts)
    if proto.color_depth.compressed_depth:
      json_list = []
      for j in proto.color_depth.compressed_depth:
        json_list.append(CompressedDepth.from_proto(j))
      obj.compressed_depth = json_list
    if proto.prediction.confidence:
      json_list = []
      for j in proto.prediction.confidence:
        json_list.append(j)
      obj.confidence = json_list
    obj.connected_clients = ConnectedClients.from_proto(get_proto_field(proto, 'connected_clients'))
    obj.constraints_version = get_proto_value(proto.session_info.constraints_version)
    obj.data_type = get_proto_value(proto.data_type)
    obj.depth = get_proto_value(proto.color_depth.depth)
    if proto.color_depth.depth_intrinsics:
      json_list = []
      for j in proto.color_depth.depth_intrinsics:
        json_list.append(j)
      obj.depth_intrinsics = json_list
    obj.depth_ts = get_proto_value(proto.prediction.depth_ts)
    obj.detection = Detection.from_proto(get_proto_field(proto, 'detection'))
    obj.device_name = get_proto_value(proto.device_name)
    obj.device_type = get_proto_value(proto.device_type)
    if proto.ur_state.digital_bank:
      json_list = []
      for j in proto.ur_state.digital_bank:
        json_list.append(DigitalBank.from_proto(j))
      obj.digital_bank = json_list
    if proto.ur_state.digital_in:
      json_list = []
      for j in proto.ur_state.digital_in:
        json_list.append(j)
      obj.digital_in = json_list
    if proto.ur_state.digital_out:
      json_list = []
      for j in proto.ur_state.digital_out:
        json_list.append(j)
      obj.digital_out = json_list
    obj.error = get_proto_value(proto.status.error)
    if proto.event_params:
      json_list = []
      for j in proto.event_params:
        json_list.append(KeyValue.from_proto(j))
      obj.event_params = json_list
    obj.experiment_token = get_proto_value(proto.experiment_token)
    obj.float_value = get_proto_value(proto.key_value.float_value)
    if proto.ur_state.force:
      json_list = []
      for j in proto.ur_state.force:
        json_list.append(j)
      obj.force = json_list
    obj.hint = get_proto_value(proto.hint)
    obj.history = History.from_proto(get_proto_field(proto, 'history'))
    obj.inhibit_frame_save = get_proto_value(proto.inhibit_frame_save)
    obj.inhibit_frame_send = get_proto_value(proto.inhibit_frame_send)
    obj.int_value = get_proto_value(proto.key_value.int_value)
    if proto.ur_state.integer_bank:
      json_list = []
      for j in proto.ur_state.integer_bank:
        json_list.append(IntegerBank.from_proto(j))
      obj.integer_bank = json_list
    obj.intent = get_proto_value(proto.prediction.inference_request.intent)
    obj.is_emergency_stopped = get_proto_value(proto.ur_state.robot_stop_state.is_emergency_stopped)
    obj.is_object_detected = get_proto_value(proto.conveyor_state.is_object_detected)
    obj.is_program_running = get_proto_value(proto.ur_state.is_program_running)
    obj.is_protective_stopped = get_proto_value(proto.ur_state.robot_stop_state.is_protective_stopped)
    obj.is_reduced_mode = get_proto_value(proto.ur_state.robot_stop_state.is_reduced_mode)
    obj.is_robot_power_on = get_proto_value(proto.ur_state.is_robot_power_on)
    obj.is_safeguard_stopped = get_proto_value(proto.ur_state.robot_stop_state.is_safeguard_stopped)
    if proto.ur_state.joint_currents_a:
      json_list = []
      for j in proto.ur_state.joint_currents_a:
        json_list.append(j)
      obj.joint_currents_a = json_list
    if proto.ur_state.joint_temps_c:
      json_list = []
      for j in proto.ur_state.joint_temps_c:
        json_list.append(j)
      obj.joint_temps_c = json_list
    if proto.ur_state.joint_voltages_v:
      json_list = []
      for j in proto.ur_state.joint_voltages_v:
        json_list.append(j)
      obj.joint_voltages_v = json_list
    if proto.ur_state.joints:
      json_list = []
      for j in proto.ur_state.joints:
        json_list.append(j)
      obj.joints = json_list
    obj.key = get_proto_value(proto.key_value.key)
    obj.label = get_proto_value(proto.label)
    if proto.metric.labels:
      json_list = []
      for j in proto.metric.labels:
        json_list.append(KeyValue.from_proto(j))
      obj.labels = json_list
    obj.last_terminated_program = get_proto_value(proto.ur_state.last_terminated_program)
    obj.level = get_proto_value(proto.level.level)
    obj.local_ts = get_proto_value(proto.local_ts)
    obj.machine_description = MachineDescription.from_proto(get_proto_field(proto, 'machine_description'))
    obj.machine_interfaces = MachineInterfaces.from_proto(get_proto_field(proto, 'machine_interfaces'))
    obj.message = get_proto_value(proto.status.message)
    if proto.message_last_timestamps:
      json_list = []
      for j in proto.message_last_timestamps:
        json_list.append(MessageLastTimestamp.from_proto(j))
      obj.message_last_timestamps = json_list
    obj.metadata = Metadata.from_proto(get_proto_field(proto, 'metadata'))
    obj.metric_value = KeyValue.from_proto(get_proto_field(proto.metric, 'value'))
    obj.on = get_proto_value(proto.tool_state.on)
    obj.operator_type = get_proto_value(proto.session_info.operator_type)
    obj.operator_uid = get_proto_value(proto.session_info.operator_uid)
    obj.pick_label = PickLabel.from_proto(get_proto_field(proto, 'pick_label'))
    if proto.prediction.pick_points:
      json_list = []
      for j in proto.prediction.pick_points:
        json_list.append(PickPoint.from_proto(j))
      obj.pick_points = json_list
    obj.pipeline_description = PipelineDescription.from_proto(get_proto_field(proto, 'pipeline_description'))
    obj.place_label = PlaceLabel.from_proto(get_proto_field(proto, 'place_label'))
    if proto.prediction.place_position_3d:
      json_list = []
      for j in proto.prediction.place_position_3d:
        json_list.append(Vec3d.from_proto(j))
      obj.place_position_3d = json_list
    if proto.prediction.place_quaternion_3d:
      json_list = []
      for j in proto.prediction.place_quaternion_3d:
        json_list.append(Quaternion3d.from_proto(j))
      obj.place_quaternion_3d = json_list
    if proto.ur_state.pose:
      json_list = []
      for j in proto.ur_state.pose:
        json_list.append(j)
      obj.pose = json_list
    if proto.prediction.position_3d:
      json_list = []
      for j in proto.prediction.position_3d:
        json_list.append(Vec3d.from_proto(j))
      obj.position_3d = json_list
    obj.prediction_type = get_proto_value(proto.prediction.inference_request.prediction_type)
    obj.program_counter = get_proto_value(proto.ur_state.program_counter)
    obj.progress = get_proto_value(proto.status.progress)
    if proto.prediction.quaternion_3d:
      json_list = []
      for j in proto.prediction.quaternion_3d:
        json_list.append(Quaternion3d.from_proto(j))
      obj.quaternion_3d = json_list
    obj.relay = get_proto_value(proto.session_info.relay)
    obj.remote_ts = get_proto_value(proto.remote_ts)
    obj.report_error = ReportError.from_proto(get_proto_field(proto, 'report_error'))
    obj.request_type = get_proto_value(proto.prediction.inference_request.request_type)
    obj.robot_current_a = get_proto_value(proto.ur_state.robot_current_a)
    obj.robot_dexterity = get_proto_value(proto.ur_state.robot_dexterity)
    obj.robot_id = get_proto_value(proto.prediction.inference_request.robot_id)
    obj.robot_mode = get_proto_value(proto.ur_state.robot_mode)
    obj.robot_name = get_proto_value(proto.session_info.robot_name)
    obj.robot_power_state = RobotPowerState.from_proto(get_proto_field(proto, 'robot_power_state'))
    obj.robot_power_state_update = RobotPowerState.from_proto(get_proto_field(proto, 'robot_power_state_update'))
    obj.robot_voltage_v = get_proto_value(proto.ur_state.robot_voltage_v)
    obj.safety_message = get_proto_value(proto.ur_state.robot_stop_state.safety_message)
    obj.safety_version = get_proto_value(proto.session_info.safety_version)
    obj.script = get_proto_value(proto.status.script)
    if proto.send_to_clients:
      json_list = []
      for j in proto.send_to_clients:
        json_list.append(SendToClient.from_proto(j))
      obj.send_to_clients = json_list
    if proto.ur_state.sensor_in:
      json_list = []
      for j in proto.ur_state.sensor_in:
        json_list.append(j)
      obj.sensor_in = json_list
    obj.seq = get_proto_value(proto.seq)
    obj.session_id = get_proto_value(proto.session_info.session_id)
    obj.sim_instance_segmentation = SimInstanceSegmentation.from_proto(get_proto_field(proto, 'sim_instance_segmentation'))
    obj.sim_state = SimState.from_proto(get_proto_field(proto, 'sim_state'))
    obj.start_time = get_proto_value(proto.session_info.start_time)
    if proto.sensor_state.state:
      json_list = []
      for j in proto.sensor_state.state:
        json_list.append(CapabilityState.from_proto(j))
      obj.state = json_list
    obj.status = get_proto_value(proto.status.status)
    obj.tag = get_proto_value(proto.tag)
    obj.task_code = get_proto_value(proto.prediction.inference_request.task_code)
    obj.text_instruction = TextInstruction.from_proto(get_proto_field(proto, 'text_instruction'))
    if proto.ur_state.tool_analog_in:
      json_list = []
      for j in proto.ur_state.tool_analog_in:
        json_list.append(j)
      obj.tool_analog_in = json_list
    if proto.ur_state.tool_analog_out:
      json_list = []
      for j in proto.ur_state.tool_analog_out:
        json_list.append(j)
      obj.tool_analog_out = json_list
    obj.tool_current_a = get_proto_value(proto.ur_state.tool_current_a)
    if proto.ur_state.tool_digital_in:
      json_list = []
      for j in proto.ur_state.tool_digital_in:
        json_list.append(j)
      obj.tool_digital_in = json_list
    if proto.ur_state.tool_digital_out:
      json_list = []
      for j in proto.ur_state.tool_digital_out:
        json_list.append(j)
      obj.tool_digital_out = json_list
    obj.tool_temp_c = get_proto_value(proto.ur_state.tool_temp_c)
    obj.tool_voltage_v = get_proto_value(proto.ur_state.tool_voltage_v)
    if proto.ur_state.torque:
      json_list = []
      for j in proto.ur_state.torque:
        json_list.append(j)
      obj.torque = json_list
    obj.transport = get_proto_value(proto.session_info.transport)
    obj.ts = get_proto_value(proto.ts)
    obj.ui_version = get_proto_value(proto.session_info.ui_version)
    obj.uncompressed_depth = get_proto_value(proto.color_depth.uncompressed_depth)
    obj.upload_depth = get_proto_value(proto.color_depth.upload_depth)
    obj.vacuum_level_pa = get_proto_value(proto.tool_state.vacuum_level_pa)
    obj.value = get_proto_value(proto.key_value.value)
    obj.webrtc_audio_request = WebrtcAudioRequest.from_proto(get_proto_field(proto, 'webrtc_audio_request'))
    obj.webrtc_audio_response = WebrtcAudioResponse.from_proto(get_proto_field(proto, 'webrtc_audio_response'))
    obj.workcell_io_version = get_proto_value(proto.session_info.workcell_io_version)
    obj.workcell_setup_version = get_proto_value(proto.session_info.workcell_setup_version)
    return obj


class DeviceDataRef:
  """Representation of proto message DeviceDataRef.

   DeviceDataRef contains fields that associate a pick label with a depth image.
   See the requirements at go/reach-ml-logging-requirements
  """
  ts: int
  device_name: str
  device_type: str
  seq: int

  def __init__(self, device_name: str = '', device_type: str = '', seq: int = 0, ts: int = 0) -> None:
    self.device_name = device_name
    self.device_type = device_type
    self.seq = seq
    self.ts = ts

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.device_name:
      assert isinstance(self.device_name, str), 'Wrong type for attribute: device_name. Expected: str. Got: ' + str(type(self.device_name)) + '.'
      json_data['deviceName'] = self.device_name

    if self.device_type:
      assert isinstance(self.device_type, str), 'Wrong type for attribute: device_type. Expected: str. Got: ' + str(type(self.device_type)) + '.'
      json_data['deviceType'] = self.device_type

    if self.seq:
      assert isinstance(self.seq, int), 'Wrong type for attribute: seq. Expected: int. Got: ' + str(type(self.seq)) + '.'
      json_data['seq'] = self.seq

    if self.ts:
      assert isinstance(self.ts, int), 'Wrong type for attribute: ts. Expected: int. Got: ' + str(type(self.ts)) + '.'
      json_data['ts'] = self.ts

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'DeviceDataRef':
    """Convert JSON to type object."""
    obj = DeviceDataRef()

    expected_json_keys: List[str] = ['deviceName', 'deviceType', 'seq', 'ts']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid DeviceDataRef. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'deviceName' in json_data:
      assert isinstance(json_data['deviceName'], str), 'Wrong type for attribute: deviceName. Expected: str. Got: ' + str(type(json_data['deviceName'])) + '.'
      obj.device_name = json_data['deviceName']

    if 'deviceType' in json_data:
      assert isinstance(json_data['deviceType'], str), 'Wrong type for attribute: deviceType. Expected: str. Got: ' + str(type(json_data['deviceType'])) + '.'
      obj.device_type = json_data['deviceType']

    if 'seq' in json_data:
      assert isinstance(json_data['seq'], int), 'Wrong type for attribute: seq. Expected: int. Got: ' + str(type(json_data['seq'])) + '.'
      obj.seq = json_data['seq']

    if 'ts' in json_data:
      assert isinstance(json_data['ts'], int), 'Wrong type for attribute: ts. Expected: int. Got: ' + str(type(json_data['ts'])) + '.'
      obj.ts = json_data['ts']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.DeviceDataRef) -> 'DeviceDataRef':
    """Convert DeviceDataRef proto to type object."""
    if not proto:
      return None
    obj = DeviceDataRef()
    obj.device_name = get_proto_value(proto.device_name)
    obj.device_type = get_proto_value(proto.device_type)
    obj.seq = get_proto_value(proto.seq)
    obj.ts = get_proto_value(proto.ts)
    return obj


class DigitalBank:
  """Representation of proto message DigitalBank.

   DigitalBank represents the raw state of one or more contiguous digital pins.
  """
  # The pin space, e.g. "controller", "tool", "user", "group"
  space: str

  # True for outputs, false for inputs
  output: bool

  # The pin number of the first element in state.
  start: int

  # The states of contiguous pins, starting with the pin number in start.
  state: List[bool]

  def __init__(self, output: bool = False, space: str = '', start: int = 0, state: Optional[List[bool]] = None) -> None:
    self.output = output
    self.space = space
    self.start = start
    if state is None:
      self.state = []
    else:
      self.state = state

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.output:
      assert isinstance(self.output, bool), 'Wrong type for attribute: output. Expected: bool. Got: ' + str(type(self.output)) + '.'
      json_data['output'] = self.output

    if self.space:
      assert isinstance(self.space, str), 'Wrong type for attribute: space. Expected: str. Got: ' + str(type(self.space)) + '.'
      json_data['space'] = self.space

    if self.start:
      assert isinstance(self.start, int), 'Wrong type for attribute: start. Expected: int. Got: ' + str(type(self.start)) + '.'
      json_data['start'] = self.start

    if self.state:
      assert isinstance(self.state, list), 'Wrong type for attribute: state. Expected: list. Got: ' + str(type(self.state)) + '.'
      json_data['state'] = self.state

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'DigitalBank':
    """Convert JSON to type object."""
    obj = DigitalBank()
    json_list: List[Any]

    expected_json_keys: List[str] = ['output', 'space', 'start', 'state']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid DigitalBank. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'output' in json_data:
      assert isinstance(json_data['output'], bool), 'Wrong type for attribute: output. Expected: bool. Got: ' + str(type(json_data['output'])) + '.'
      obj.output = json_data['output']

    if 'space' in json_data:
      assert isinstance(json_data['space'], str), 'Wrong type for attribute: space. Expected: str. Got: ' + str(type(json_data['space'])) + '.'
      obj.space = json_data['space']

    if 'start' in json_data:
      assert isinstance(json_data['start'], int), 'Wrong type for attribute: start. Expected: int. Got: ' + str(type(json_data['start'])) + '.'
      obj.start = json_data['start']

    if 'state' in json_data:
      assert isinstance(json_data['state'], list), 'Wrong type for attribute: state. Expected: list. Got: ' + str(type(json_data['state'])) + '.'
      json_list = []
      for j in json_data['state']:
        json_list.append(j)
      obj.state = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.DigitalBank) -> 'DigitalBank':
    """Convert DigitalBank proto to type object."""
    if not proto:
      return None
    obj = DigitalBank()
    obj.output = get_proto_value(proto.output)
    obj.space = get_proto_value(proto.space)
    obj.start = get_proto_value(proto.start)
    if proto.state:
      json_list = []
      for j in proto.state:
        json_list.append(j)
      obj.state = json_list
    return obj


class ExperimentalCommandData:
  """Representation of proto message ExperimentalCommandData.

   Experimental command data, augmenting CommandData.
   No new fields should be added to this structure; the existing
   fields might be migrated to proper places in the future.
   See the corresponding file in the Project Reach source code:
   project-reach/go/src/project-reach/pkg/rc/types.go
  """
  # Label, usually the name of the action executed.
  label: str

  # Timestamp of the depth image when action is being sent.
  depth_ts: int

  # 2D position of the end effector on the depth image.
  pose_2d: Optional['Pose2d']

  # 3D position in Camera space.
  position_3d: Optional['Vec3d']

  # Rotation of pick point in Camera space.
  quaternion_3d: Optional['Quaternion3d']

  # List of tags for the pick point, such as
  # "full-autonomy", "accept-reject","accept", "reject", "manual", etc.
  tags: List[str]

  # Timestamp of the depth image when action is queued.
  user_ts: int

  # Possible in future that different exp data reference different cameras.
  device_type: str
  device_name: str

  def __init__(self, depth_ts: int = 0, device_name: str = '', device_type: str = '', label: str = '', pose_2d: Optional['Pose2d'] = None, position_3d: Optional['Vec3d'] = None, quaternion_3d: Optional['Quaternion3d'] = None, tags: Optional[List[str]] = None, user_ts: int = 0) -> None:
    self.depth_ts = depth_ts
    self.device_name = device_name
    self.device_type = device_type
    self.label = label
    self.pose_2d = pose_2d
    self.position_3d = position_3d
    self.quaternion_3d = quaternion_3d
    if tags is None:
      self.tags = []
    else:
      self.tags = tags
    self.user_ts = user_ts

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.depth_ts:
      assert isinstance(self.depth_ts, int), 'Wrong type for attribute: depth_ts. Expected: int. Got: ' + str(type(self.depth_ts)) + '.'
      json_data['depthTS'] = self.depth_ts

    if self.device_name:
      assert isinstance(self.device_name, str), 'Wrong type for attribute: device_name. Expected: str. Got: ' + str(type(self.device_name)) + '.'
      json_data['deviceName'] = self.device_name

    if self.device_type:
      assert isinstance(self.device_type, str), 'Wrong type for attribute: device_type. Expected: str. Got: ' + str(type(self.device_type)) + '.'
      json_data['deviceType'] = self.device_type

    if self.label:
      assert isinstance(self.label, str), 'Wrong type for attribute: label. Expected: str. Got: ' + str(type(self.label)) + '.'
      json_data['label'] = self.label

    if self.pose_2d:
      assert self.pose_2d.__class__.__name__ == 'Pose2d', 'Wrong type for attribute: pose_2d. Expected: Pose2d. Got: ' + str(type(self.pose_2d)) + '.'
      json_data['pose2D'] = self.pose_2d.to_json()

    if self.position_3d:
      assert self.position_3d.__class__.__name__ == 'Vec3d', 'Wrong type for attribute: position_3d. Expected: Vec3d. Got: ' + str(type(self.position_3d)) + '.'
      json_data['position3D'] = self.position_3d.to_json()

    if self.quaternion_3d:
      assert self.quaternion_3d.__class__.__name__ == 'Quaternion3d', 'Wrong type for attribute: quaternion_3d. Expected: Quaternion3d. Got: ' + str(type(self.quaternion_3d)) + '.'
      json_data['quaternion3D'] = self.quaternion_3d.to_json()

    if self.tags:
      assert isinstance(self.tags, list), 'Wrong type for attribute: tags. Expected: list. Got: ' + str(type(self.tags)) + '.'
      json_data['tags'] = self.tags

    if self.user_ts:
      assert isinstance(self.user_ts, int), 'Wrong type for attribute: user_ts. Expected: int. Got: ' + str(type(self.user_ts)) + '.'
      json_data['userTS'] = self.user_ts

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'ExperimentalCommandData':
    """Convert JSON to type object."""
    obj = ExperimentalCommandData()
    json_list: List[Any]

    expected_json_keys: List[str] = ['depthTS', 'deviceName', 'deviceType', 'label', 'pose2D', 'position3D', 'quaternion3D', 'tags', 'userTS']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid ExperimentalCommandData. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'depthTS' in json_data:
      assert isinstance(json_data['depthTS'], int), 'Wrong type for attribute: depthTS. Expected: int. Got: ' + str(type(json_data['depthTS'])) + '.'
      obj.depth_ts = json_data['depthTS']

    if 'deviceName' in json_data:
      assert isinstance(json_data['deviceName'], str), 'Wrong type for attribute: deviceName. Expected: str. Got: ' + str(type(json_data['deviceName'])) + '.'
      obj.device_name = json_data['deviceName']

    if 'deviceType' in json_data:
      assert isinstance(json_data['deviceType'], str), 'Wrong type for attribute: deviceType. Expected: str. Got: ' + str(type(json_data['deviceType'])) + '.'
      obj.device_type = json_data['deviceType']

    if 'label' in json_data:
      assert isinstance(json_data['label'], str), 'Wrong type for attribute: label. Expected: str. Got: ' + str(type(json_data['label'])) + '.'
      obj.label = json_data['label']

    if 'pose2D' in json_data:
      assert isinstance(json_data['pose2D'], dict), 'Wrong type for attribute: pose2D. Expected: dict. Got: ' + str(type(json_data['pose2D'])) + '.'
      obj.pose_2d = Pose2d.from_json(json_data['pose2D'])

    if 'position3D' in json_data:
      assert isinstance(json_data['position3D'], dict), 'Wrong type for attribute: position3D. Expected: dict. Got: ' + str(type(json_data['position3D'])) + '.'
      obj.position_3d = Vec3d.from_json(json_data['position3D'])

    if 'quaternion3D' in json_data:
      assert isinstance(json_data['quaternion3D'], dict), 'Wrong type for attribute: quaternion3D. Expected: dict. Got: ' + str(type(json_data['quaternion3D'])) + '.'
      obj.quaternion_3d = Quaternion3d.from_json(json_data['quaternion3D'])

    if 'tags' in json_data:
      assert isinstance(json_data['tags'], list), 'Wrong type for attribute: tags. Expected: list. Got: ' + str(type(json_data['tags'])) + '.'
      json_list = []
      for j in json_data['tags']:
        json_list.append(j)
      obj.tags = json_list

    if 'userTS' in json_data:
      assert isinstance(json_data['userTS'], int), 'Wrong type for attribute: userTS. Expected: int. Got: ' + str(type(json_data['userTS'])) + '.'
      obj.user_ts = json_data['userTS']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.ExperimentalCommandData) -> 'ExperimentalCommandData':
    """Convert ExperimentalCommandData proto to type object."""
    if not proto:
      return None
    obj = ExperimentalCommandData()
    obj.depth_ts = get_proto_value(proto.depth_ts)
    obj.device_name = get_proto_value(proto.device_name)
    obj.device_type = get_proto_value(proto.device_type)
    obj.label = get_proto_value(proto.label)
    obj.pose_2d = Pose2d.from_proto(get_proto_field(proto, 'pose_2d'))
    obj.position_3d = Vec3d.from_proto(get_proto_field(proto, 'position_3d'))
    obj.quaternion_3d = Quaternion3d.from_proto(get_proto_field(proto, 'quaternion_3d'))
    if proto.tags:
      json_list = []
      for j in proto.tags:
        json_list.append(j)
      obj.tags = json_list
    obj.user_ts = get_proto_value(proto.user_ts)
    return obj


class ForceLimits:
  """Representation of proto message ForceLimits.

   ForceLimits are force limits to use with Limits in waypoints.
  """
  maximum: List[float]
  minimum: List[float]

  def __init__(self, maximum: Optional[List[float]] = None, minimum: Optional[List[float]] = None) -> None:
    if maximum is None:
      self.maximum = []
    else:
      self.maximum = maximum
    if minimum is None:
      self.minimum = []
    else:
      self.minimum = minimum

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.maximum:
      assert isinstance(self.maximum, list), 'Wrong type for attribute: maximum. Expected: list. Got: ' + str(type(self.maximum)) + '.'
      json_data['maximum'] = self.maximum

    if self.minimum:
      assert isinstance(self.minimum, list), 'Wrong type for attribute: minimum. Expected: list. Got: ' + str(type(self.minimum)) + '.'
      json_data['minimum'] = self.minimum

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'ForceLimits':
    """Convert JSON to type object."""
    obj = ForceLimits()
    json_list: List[Any]

    expected_json_keys: List[str] = ['maximum', 'minimum']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid ForceLimits. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'maximum' in json_data:
      assert isinstance(json_data['maximum'], list), 'Wrong type for attribute: maximum. Expected: list. Got: ' + str(type(json_data['maximum'])) + '.'
      json_list = []
      for j in json_data['maximum']:
        json_list.append(j)
      obj.maximum = json_list

    if 'minimum' in json_data:
      assert isinstance(json_data['minimum'], list), 'Wrong type for attribute: minimum. Expected: list. Got: ' + str(type(json_data['minimum'])) + '.'
      json_list = []
      for j in json_data['minimum']:
        json_list.append(j)
      obj.minimum = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.ForceLimits) -> 'ForceLimits':
    """Convert ForceLimits proto to type object."""
    if not proto:
      return None
    obj = ForceLimits()
    if proto.maximum:
      json_list = []
      for j in proto.maximum:
        json_list.append(j)
      obj.maximum = json_list
    if proto.minimum:
      json_list = []
      for j in proto.minimum:
        json_list.append(j)
      obj.minimum = json_list
    return obj


class GetAllObjectPoses:
  """Representation of proto message GetAllObjectPoses.

   GetAllObjectPoses requests all object poses of a scene in SIM.
   Deliberately an empty message. Serves like a marker of the type of SIM
   action and also to be consistent with all other actions.

  """

  def __init__(self) -> None:
    pass

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'GetAllObjectPoses':
    """Convert JSON to type object."""
    obj = GetAllObjectPoses()

    expected_json_keys: List[str] = []

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid GetAllObjectPoses. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.GetAllObjectPoses) -> 'GetAllObjectPoses':  # pylint: disable=unused-argument
    """Convert GetAllObjectPoses proto to type object."""
    if not proto:
      return None
    obj = GetAllObjectPoses()
    return obj


class GetSegmentedImage:
  """Representation of proto message GetSegmentedImage.

   GetSegmentedImage requests a segmented image from the SIM.

  """
  device_key: str

  def __init__(self, device_key: str = '') -> None:
    self.device_key = device_key

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.device_key:
      assert isinstance(self.device_key, str), 'Wrong type for attribute: device_key. Expected: str. Got: ' + str(type(self.device_key)) + '.'
      json_data['deviceKey'] = self.device_key

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'GetSegmentedImage':
    """Convert JSON to type object."""
    obj = GetSegmentedImage()

    expected_json_keys: List[str] = ['deviceKey']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid GetSegmentedImage. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'deviceKey' in json_data:
      assert isinstance(json_data['deviceKey'], str), 'Wrong type for attribute: deviceKey. Expected: str. Got: ' + str(type(json_data['deviceKey'])) + '.'
      obj.device_key = json_data['deviceKey']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.GetSegmentedImage) -> 'GetSegmentedImage':
    """Convert GetSegmentedImage proto to type object."""
    if not proto:
      return None
    obj = GetSegmentedImage()
    obj.device_key = get_proto_value(proto.device_key)
    return obj


class GymAction:
  """Representation of proto message GymAction.

   GymAction stores the original action from PyReach gym.
  """
  device_type: str
  device_name: str
  synchronous: bool
  arm_action_params: Optional['ArmActionParams']
  vacuum_action_params: Optional['VacuumActionParams']
  logger_action_params: Optional['LoggerActionParams']

  def __init__(self, arm_action_params: Optional['ArmActionParams'] = None, device_name: str = '', device_type: str = '', logger_action_params: Optional['LoggerActionParams'] = None, synchronous: bool = False, vacuum_action_params: Optional['VacuumActionParams'] = None) -> None:
    self.arm_action_params = arm_action_params
    self.device_name = device_name
    self.device_type = device_type
    self.logger_action_params = logger_action_params
    self.synchronous = synchronous
    self.vacuum_action_params = vacuum_action_params

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.arm_action_params:
      assert self.arm_action_params.__class__.__name__ == 'ArmActionParams', 'Wrong type for attribute: arm_action_params. Expected: ArmActionParams. Got: ' + str(type(self.arm_action_params)) + '.'
      json_data['armActionParams'] = self.arm_action_params.to_json()

    if self.device_name:
      assert isinstance(self.device_name, str), 'Wrong type for attribute: device_name. Expected: str. Got: ' + str(type(self.device_name)) + '.'
      json_data['deviceName'] = self.device_name

    if self.device_type:
      assert isinstance(self.device_type, str), 'Wrong type for attribute: device_type. Expected: str. Got: ' + str(type(self.device_type)) + '.'
      json_data['deviceType'] = self.device_type

    if self.logger_action_params:
      assert self.logger_action_params.__class__.__name__ == 'LoggerActionParams', 'Wrong type for attribute: logger_action_params. Expected: LoggerActionParams. Got: ' + str(type(self.logger_action_params)) + '.'
      json_data['loggerActionParams'] = self.logger_action_params.to_json()

    if self.synchronous:
      assert isinstance(self.synchronous, bool), 'Wrong type for attribute: synchronous. Expected: bool. Got: ' + str(type(self.synchronous)) + '.'
      json_data['synchronous'] = self.synchronous

    if self.vacuum_action_params:
      assert self.vacuum_action_params.__class__.__name__ == 'VacuumActionParams', 'Wrong type for attribute: vacuum_action_params. Expected: VacuumActionParams. Got: ' + str(type(self.vacuum_action_params)) + '.'
      json_data['vacuumActionParams'] = self.vacuum_action_params.to_json()

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'GymAction':
    """Convert JSON to type object."""
    obj = GymAction()

    expected_json_keys: List[str] = ['armActionParams', 'deviceName', 'deviceType', 'loggerActionParams', 'synchronous', 'vacuumActionParams']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid GymAction. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'armActionParams' in json_data:
      assert isinstance(json_data['armActionParams'], dict), 'Wrong type for attribute: armActionParams. Expected: dict. Got: ' + str(type(json_data['armActionParams'])) + '.'
      obj.arm_action_params = ArmActionParams.from_json(json_data['armActionParams'])

    if 'deviceName' in json_data:
      assert isinstance(json_data['deviceName'], str), 'Wrong type for attribute: deviceName. Expected: str. Got: ' + str(type(json_data['deviceName'])) + '.'
      obj.device_name = json_data['deviceName']

    if 'deviceType' in json_data:
      assert isinstance(json_data['deviceType'], str), 'Wrong type for attribute: deviceType. Expected: str. Got: ' + str(type(json_data['deviceType'])) + '.'
      obj.device_type = json_data['deviceType']

    if 'loggerActionParams' in json_data:
      assert isinstance(json_data['loggerActionParams'], dict), 'Wrong type for attribute: loggerActionParams. Expected: dict. Got: ' + str(type(json_data['loggerActionParams'])) + '.'
      obj.logger_action_params = LoggerActionParams.from_json(json_data['loggerActionParams'])

    if 'synchronous' in json_data:
      assert isinstance(json_data['synchronous'], bool), 'Wrong type for attribute: synchronous. Expected: bool. Got: ' + str(type(json_data['synchronous'])) + '.'
      obj.synchronous = json_data['synchronous']

    if 'vacuumActionParams' in json_data:
      assert isinstance(json_data['vacuumActionParams'], dict), 'Wrong type for attribute: vacuumActionParams. Expected: dict. Got: ' + str(type(json_data['vacuumActionParams'])) + '.'
      obj.vacuum_action_params = VacuumActionParams.from_json(json_data['vacuumActionParams'])

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.GymAction) -> 'GymAction':
    """Convert GymAction proto to type object."""
    if not proto:
      return None
    obj = GymAction()
    obj.arm_action_params = ArmActionParams.from_proto(get_proto_field(proto, 'arm_action_params'))
    obj.device_name = get_proto_value(proto.device_name)
    obj.device_type = get_proto_value(proto.device_type)
    obj.logger_action_params = LoggerActionParams.from_proto(get_proto_field(proto, 'logger_action_params'))
    obj.synchronous = get_proto_value(proto.synchronous)
    obj.vacuum_action_params = VacuumActionParams.from_proto(get_proto_field(proto, 'vacuum_action_params'))
    return obj


class History:
  """Representation of proto message History.

   History represents history storing configuration data.

   For more details, see design doc:
  """
  # history document name
  key: str

  # array of strings of JSON-encoded firestore documents
  values: List[str]

  # index to start history paging
  history_start: int

  # index to end history paging
  history_end: int

  def __init__(self, history_end: int = 0, history_start: int = 0, key: str = '', values: Optional[List[str]] = None) -> None:
    self.history_end = history_end
    self.history_start = history_start
    self.key = key
    if values is None:
      self.values = []
    else:
      self.values = values

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.history_end:
      assert isinstance(self.history_end, int), 'Wrong type for attribute: history_end. Expected: int. Got: ' + str(type(self.history_end)) + '.'
      json_data['historyEnd'] = self.history_end

    if self.history_start:
      assert isinstance(self.history_start, int), 'Wrong type for attribute: history_start. Expected: int. Got: ' + str(type(self.history_start)) + '.'
      json_data['historyStart'] = self.history_start

    if self.key:
      assert isinstance(self.key, str), 'Wrong type for attribute: key. Expected: str. Got: ' + str(type(self.key)) + '.'
      json_data['key'] = self.key

    if self.values:
      assert isinstance(self.values, list), 'Wrong type for attribute: values. Expected: list. Got: ' + str(type(self.values)) + '.'
      json_data['values'] = self.values

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'History':
    """Convert JSON to type object."""
    obj = History()
    json_list: List[Any]

    expected_json_keys: List[str] = ['historyEnd', 'historyStart', 'key', 'values']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid History. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'historyEnd' in json_data:
      assert isinstance(json_data['historyEnd'], int), 'Wrong type for attribute: historyEnd. Expected: int. Got: ' + str(type(json_data['historyEnd'])) + '.'
      obj.history_end = json_data['historyEnd']

    if 'historyStart' in json_data:
      assert isinstance(json_data['historyStart'], int), 'Wrong type for attribute: historyStart. Expected: int. Got: ' + str(type(json_data['historyStart'])) + '.'
      obj.history_start = json_data['historyStart']

    if 'key' in json_data:
      assert isinstance(json_data['key'], str), 'Wrong type for attribute: key. Expected: str. Got: ' + str(type(json_data['key'])) + '.'
      obj.key = json_data['key']

    if 'values' in json_data:
      assert isinstance(json_data['values'], list), 'Wrong type for attribute: values. Expected: list. Got: ' + str(type(json_data['values'])) + '.'
      json_list = []
      for j in json_data['values']:
        json_list.append(j)
      obj.values = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.History) -> 'History':
    """Convert History proto to type object."""
    if not proto:
      return None
    obj = History()
    obj.history_end = get_proto_value(proto.history_end)
    obj.history_start = get_proto_value(proto.history_start)
    obj.key = get_proto_value(proto.key)
    if proto.values:
      json_list = []
      for j in proto.values:
        json_list.append(j)
      obj.values = json_list
    return obj


class IOState:
  """Representation of proto message IOState.

   IOState is the state of a single input or output capability. Since a
   capability can have more than one pin, state is repeated, one for each
   pin. Note that if the capability is digital and fused, then there will only
   be one pin representing the state of all pins in the capability.

   For more details, see the design doc at
  """
  state: List['CapabilityState']

  def __init__(self, state: Optional[List['CapabilityState']] = None) -> None:
    if state is None:
      self.state = []
    else:
      self.state = state

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.state:
      assert isinstance(self.state, list), 'Wrong type for attribute: state. Expected: list. Got: ' + str(type(self.state)) + '.'
      obj_list = []
      for item in self.state:
        obj_list.append(item.to_json())
      json_data['state'] = obj_list

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'IOState':
    """Convert JSON to type object."""
    obj = IOState()
    json_list: List[Any]

    expected_json_keys: List[str] = ['state']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid IOState. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'state' in json_data:
      assert isinstance(json_data['state'], list), 'Wrong type for attribute: state. Expected: list. Got: ' + str(type(json_data['state'])) + '.'
      json_list = []
      for j in json_data['state']:
        json_list.append(CapabilityState.from_json(j))
      obj.state = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.IOState) -> 'IOState':
    """Convert IOState proto to type object."""
    if not proto:
      return None
    obj = IOState()
    if proto.state:
      json_list = []
      for j in proto.state:
        json_list.append(CapabilityState.from_proto(j))
      obj.state = json_list
    return obj


class IntegerBank:
  """Representation of proto message IntegerBank.

   IntegerBank represents the raw state of one or more contiguous integer pins.
  """
  # The pin space, e.g. "controller", "tool", "user", "group"
  space: str

  # True for outputs, false for inputs
  output: bool

  # The pin number of the first element in state.
  start: int

  # The states of contiguous pins, starting with the pin number in start.
  state: List[int]

  def __init__(self, output: bool = False, space: str = '', start: int = 0, state: Optional[List[int]] = None) -> None:
    self.output = output
    self.space = space
    self.start = start
    if state is None:
      self.state = []
    else:
      self.state = state

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.output:
      assert isinstance(self.output, bool), 'Wrong type for attribute: output. Expected: bool. Got: ' + str(type(self.output)) + '.'
      json_data['output'] = self.output

    if self.space:
      assert isinstance(self.space, str), 'Wrong type for attribute: space. Expected: str. Got: ' + str(type(self.space)) + '.'
      json_data['space'] = self.space

    if self.start:
      assert isinstance(self.start, int), 'Wrong type for attribute: start. Expected: int. Got: ' + str(type(self.start)) + '.'
      json_data['start'] = self.start

    if self.state:
      assert isinstance(self.state, list), 'Wrong type for attribute: state. Expected: list. Got: ' + str(type(self.state)) + '.'
      json_data['state'] = self.state

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'IntegerBank':
    """Convert JSON to type object."""
    obj = IntegerBank()
    json_list: List[Any]

    expected_json_keys: List[str] = ['output', 'space', 'start', 'state']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid IntegerBank. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'output' in json_data:
      assert isinstance(json_data['output'], bool), 'Wrong type for attribute: output. Expected: bool. Got: ' + str(type(json_data['output'])) + '.'
      obj.output = json_data['output']

    if 'space' in json_data:
      assert isinstance(json_data['space'], str), 'Wrong type for attribute: space. Expected: str. Got: ' + str(type(json_data['space'])) + '.'
      obj.space = json_data['space']

    if 'start' in json_data:
      assert isinstance(json_data['start'], int), 'Wrong type for attribute: start. Expected: int. Got: ' + str(type(json_data['start'])) + '.'
      obj.start = json_data['start']

    if 'state' in json_data:
      assert isinstance(json_data['state'], list), 'Wrong type for attribute: state. Expected: list. Got: ' + str(type(json_data['state'])) + '.'
      json_list = []
      for j in json_data['state']:
        json_list.append(j)
      obj.state = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.IntegerBank) -> 'IntegerBank':
    """Convert IntegerBank proto to type object."""
    if not proto:
      return None
    obj = IntegerBank()
    obj.output = get_proto_value(proto.output)
    obj.space = get_proto_value(proto.space)
    obj.start = get_proto_value(proto.start)
    if proto.state:
      json_list = []
      for j in proto.state:
        json_list.append(j)
      obj.state = json_list
    return obj


class IntervalEnd:
  """Representation of proto message IntervalEnd.

   IntervalEnd ends a named interval.
  """
  # The name of the interval to end.
  name: str

  # The start time for the interval.
  start_ts: int

  # The end time for the interval.
  end_ts: int

  def __init__(self, end_ts: int = 0, name: str = '', start_ts: int = 0) -> None:
    self.end_ts = end_ts
    self.name = name
    self.start_ts = start_ts

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.end_ts:
      assert isinstance(self.end_ts, int), 'Wrong type for attribute: end_ts. Expected: int. Got: ' + str(type(self.end_ts)) + '.'
      json_data['endTS'] = self.end_ts

    if self.name:
      assert isinstance(self.name, str), 'Wrong type for attribute: name. Expected: str. Got: ' + str(type(self.name)) + '.'
      json_data['name'] = self.name

    if self.start_ts:
      assert isinstance(self.start_ts, int), 'Wrong type for attribute: start_ts. Expected: int. Got: ' + str(type(self.start_ts)) + '.'
      json_data['startTS'] = self.start_ts

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'IntervalEnd':
    """Convert JSON to type object."""
    obj = IntervalEnd()

    expected_json_keys: List[str] = ['endTS', 'name', 'startTS']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid IntervalEnd. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'endTS' in json_data:
      assert isinstance(json_data['endTS'], int), 'Wrong type for attribute: endTS. Expected: int. Got: ' + str(type(json_data['endTS'])) + '.'
      obj.end_ts = json_data['endTS']

    if 'name' in json_data:
      assert isinstance(json_data['name'], str), 'Wrong type for attribute: name. Expected: str. Got: ' + str(type(json_data['name'])) + '.'
      obj.name = json_data['name']

    if 'startTS' in json_data:
      assert isinstance(json_data['startTS'], int), 'Wrong type for attribute: startTS. Expected: int. Got: ' + str(type(json_data['startTS'])) + '.'
      obj.start_ts = json_data['startTS']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.IntervalEnd) -> 'IntervalEnd':
    """Convert IntervalEnd proto to type object."""
    if not proto:
      return None
    obj = IntervalEnd()
    obj.end_ts = get_proto_value(proto.end_ts)
    obj.name = get_proto_value(proto.name)
    obj.start_ts = get_proto_value(proto.start_ts)
    return obj


class IntervalStart:
  """Representation of proto message IntervalStart.

   IntervalStart starts a named interval.
  """
  # The name of the interval to start.
  name: str

  def __init__(self, name: str = '') -> None:
    self.name = name

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.name:
      assert isinstance(self.name, str), 'Wrong type for attribute: name. Expected: str. Got: ' + str(type(self.name)) + '.'
      json_data['name'] = self.name

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'IntervalStart':
    """Convert JSON to type object."""
    obj = IntervalStart()

    expected_json_keys: List[str] = ['name']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid IntervalStart. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'name' in json_data:
      assert isinstance(json_data['name'], str), 'Wrong type for attribute: name. Expected: str. Got: ' + str(type(json_data['name'])) + '.'
      obj.name = json_data['name']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.IntervalStart) -> 'IntervalStart':
    """Convert IntervalStart proto to type object."""
    if not proto:
      return None
    obj = IntervalStart()
    obj.name = get_proto_value(proto.name)
    return obj


class KeyValue:
  """Representation of proto message KeyValue.

   Message for generic key-value data.
  """
  key: str
  value: str
  int_value: int
  float_value: float

  def __init__(self, float_value: float = 0.0, int_value: int = 0, key: str = '', value: str = '') -> None:
    self.float_value = float_value
    self.int_value = int_value
    self.key = key
    self.value = value

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.float_value:
      assert isinstance(self.float_value, float) or isinstance(self.float_value, int), 'Wrong type for attribute: float_value. Expected: float. Got: ' + str(type(self.float_value)) + '.'
      json_data['floatValue'] = self.float_value

    if self.int_value:
      assert isinstance(self.int_value, int), 'Wrong type for attribute: int_value. Expected: int. Got: ' + str(type(self.int_value)) + '.'
      json_data['intValue'] = self.int_value

    if self.key:
      assert isinstance(self.key, str), 'Wrong type for attribute: key. Expected: str. Got: ' + str(type(self.key)) + '.'
      json_data['key'] = self.key

    if self.value:
      assert isinstance(self.value, str), 'Wrong type for attribute: value. Expected: str. Got: ' + str(type(self.value)) + '.'
      json_data['value'] = self.value

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'KeyValue':
    """Convert JSON to type object."""
    obj = KeyValue()

    expected_json_keys: List[str] = ['floatValue', 'intValue', 'key', 'value']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid KeyValue. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'floatValue' in json_data:
      assert isinstance(json_data['floatValue'], float) or isinstance(json_data['floatValue'], int), 'Wrong type for attribute: floatValue. Expected: float. Got: ' + str(type(json_data['floatValue'])) + '.'
      obj.float_value = json_data['floatValue']

    if 'intValue' in json_data:
      assert isinstance(json_data['intValue'], int), 'Wrong type for attribute: intValue. Expected: int. Got: ' + str(type(json_data['intValue'])) + '.'
      obj.int_value = json_data['intValue']

    if 'key' in json_data:
      assert isinstance(json_data['key'], str), 'Wrong type for attribute: key. Expected: str. Got: ' + str(type(json_data['key'])) + '.'
      obj.key = json_data['key']

    if 'value' in json_data:
      assert isinstance(json_data['value'], str), 'Wrong type for attribute: value. Expected: str. Got: ' + str(type(json_data['value'])) + '.'
      obj.value = json_data['value']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.KeyValue) -> 'KeyValue':
    """Convert KeyValue proto to type object."""
    if not proto:
      return None
    obj = KeyValue()
    obj.float_value = get_proto_value(proto.float_value)
    obj.int_value = get_proto_value(proto.int_value)
    obj.key = get_proto_value(proto.key)
    obj.value = get_proto_value(proto.value)
    return obj


class Limits:
  """Representation of proto message Limits.

   Limits for a MoveJWaypointArgs or MoveLWaypointArgs to early stop
   the movement.
  """
  force: Optional['ForceLimits']
  torque: Optional['TorqueLimits']
  sensor: List['SensorLimits']

  def __init__(self, force: Optional['ForceLimits'] = None, sensor: Optional[List['SensorLimits']] = None, torque: Optional['TorqueLimits'] = None) -> None:
    self.force = force
    if sensor is None:
      self.sensor = []
    else:
      self.sensor = sensor
    self.torque = torque

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.force:
      assert self.force.__class__.__name__ == 'ForceLimits', 'Wrong type for attribute: force. Expected: ForceLimits. Got: ' + str(type(self.force)) + '.'
      json_data['force'] = self.force.to_json()

    if self.sensor:
      assert isinstance(self.sensor, list), 'Wrong type for attribute: sensor. Expected: list. Got: ' + str(type(self.sensor)) + '.'
      obj_list = []
      for item in self.sensor:
        obj_list.append(item.to_json())
      json_data['sensor'] = obj_list

    if self.torque:
      assert self.torque.__class__.__name__ == 'TorqueLimits', 'Wrong type for attribute: torque. Expected: TorqueLimits. Got: ' + str(type(self.torque)) + '.'
      json_data['torque'] = self.torque.to_json()

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'Limits':
    """Convert JSON to type object."""
    obj = Limits()
    json_list: List[Any]

    expected_json_keys: List[str] = ['force', 'sensor', 'torque']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid Limits. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'force' in json_data:
      assert isinstance(json_data['force'], dict), 'Wrong type for attribute: force. Expected: dict. Got: ' + str(type(json_data['force'])) + '.'
      obj.force = ForceLimits.from_json(json_data['force'])

    if 'sensor' in json_data:
      assert isinstance(json_data['sensor'], list), 'Wrong type for attribute: sensor. Expected: list. Got: ' + str(type(json_data['sensor'])) + '.'
      json_list = []
      for j in json_data['sensor']:
        json_list.append(SensorLimits.from_json(j))
      obj.sensor = json_list

    if 'torque' in json_data:
      assert isinstance(json_data['torque'], dict), 'Wrong type for attribute: torque. Expected: dict. Got: ' + str(type(json_data['torque'])) + '.'
      obj.torque = TorqueLimits.from_json(json_data['torque'])

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.Limits) -> 'Limits':
    """Convert Limits proto to type object."""
    if not proto:
      return None
    obj = Limits()
    obj.force = ForceLimits.from_proto(get_proto_field(proto, 'force'))
    if proto.sensor:
      json_list = []
      for j in proto.sensor:
        json_list.append(SensorLimits.from_proto(j))
      obj.sensor = json_list
    obj.torque = TorqueLimits.from_proto(get_proto_field(proto, 'torque'))
    return obj


class LoggerActionParams:
  """Representation of proto message LoggerActionParams.

   LoggerActionParams stores the logger action params.
  """
  is_start: bool
  event_params: List['KeyValue']

  def __init__(self, event_params: Optional[List['KeyValue']] = None, is_start: bool = False) -> None:
    if event_params is None:
      self.event_params = []
    else:
      self.event_params = event_params
    self.is_start = is_start

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.event_params:
      assert isinstance(self.event_params, list), 'Wrong type for attribute: event_params. Expected: list. Got: ' + str(type(self.event_params)) + '.'
      obj_list = []
      for item in self.event_params:
        obj_list.append(item.to_json())
      json_data['eventParams'] = obj_list

    if self.is_start:
      assert isinstance(self.is_start, bool), 'Wrong type for attribute: is_start. Expected: bool. Got: ' + str(type(self.is_start)) + '.'
      json_data['isStart'] = self.is_start

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'LoggerActionParams':
    """Convert JSON to type object."""
    obj = LoggerActionParams()
    json_list: List[Any]

    expected_json_keys: List[str] = ['eventParams', 'isStart']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid LoggerActionParams. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'eventParams' in json_data:
      assert isinstance(json_data['eventParams'], list), 'Wrong type for attribute: eventParams. Expected: list. Got: ' + str(type(json_data['eventParams'])) + '.'
      json_list = []
      for j in json_data['eventParams']:
        json_list.append(KeyValue.from_json(j))
      obj.event_params = json_list

    if 'isStart' in json_data:
      assert isinstance(json_data['isStart'], bool), 'Wrong type for attribute: isStart. Expected: bool. Got: ' + str(type(json_data['isStart'])) + '.'
      obj.is_start = json_data['isStart']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.LoggerActionParams) -> 'LoggerActionParams':
    """Convert LoggerActionParams proto to type object."""
    if not proto:
      return None
    obj = LoggerActionParams()
    if proto.event_params:
      json_list = []
      for j in proto.event_params:
        json_list.append(KeyValue.from_proto(j))
      obj.event_params = json_list
    obj.is_start = get_proto_value(proto.is_start)
    return obj


class MachineDescription:
  """Representation of proto message MachineDescription.

   MachineDescription is the description of a state machine in the pipeline.
  """
  # The interfaces provided by the machine.
  interfaces: List['MachineInterface']

  def __init__(self, interfaces: Optional[List['MachineInterface']] = None) -> None:
    if interfaces is None:
      self.interfaces = []
    else:
      self.interfaces = interfaces

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.interfaces:
      assert isinstance(self.interfaces, list), 'Wrong type for attribute: interfaces. Expected: list. Got: ' + str(type(self.interfaces)) + '.'
      obj_list = []
      for item in self.interfaces:
        obj_list.append(item.to_json())
      json_data['interfaces'] = obj_list

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'MachineDescription':
    """Convert JSON to type object."""
    obj = MachineDescription()
    json_list: List[Any]

    expected_json_keys: List[str] = ['interfaces']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid MachineDescription. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'interfaces' in json_data:
      assert isinstance(json_data['interfaces'], list), 'Wrong type for attribute: interfaces. Expected: list. Got: ' + str(type(json_data['interfaces'])) + '.'
      json_list = []
      for j in json_data['interfaces']:
        json_list.append(MachineInterface.from_json(j))
      obj.interfaces = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.MachineDescription) -> 'MachineDescription':
    """Convert MachineDescription proto to type object."""
    if not proto:
      return None
    obj = MachineDescription()
    if proto.interfaces:
      json_list = []
      for j in proto.interfaces:
        json_list.append(MachineInterface.from_proto(j))
      obj.interfaces = json_list
    return obj


class MachineInterface:
  """Representation of proto message MachineInterface.

   MachineInterface describes a type of data (specified by device type, device
   name, request type, and key) that is provided by a machine.
  """
  # The type of interface.
  py_type: str

  # The device_type of the interface.
  device_type: str

  # The device_name of the interface.
  device_name: str

  # The data_type of the interface.
  data_type: str

  # The keys of the interface.
  keys: List[str]

  # If the interface replaces another.
  replaces: bool

  # If the interface stops propagation, blocking access to the interface
  # upwards in the pipeline.
  stop_propagation: bool

  def __init__(self, data_type: str = '', device_name: str = '', device_type: str = '', keys: Optional[List[str]] = None, py_type: str = '', replaces: bool = False, stop_propagation: bool = False) -> None:
    self.data_type = data_type
    self.device_name = device_name
    self.device_type = device_type
    if keys is None:
      self.keys = []
    else:
      self.keys = keys
    self.py_type = py_type
    self.replaces = replaces
    self.stop_propagation = stop_propagation

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.data_type:
      assert isinstance(self.data_type, str), 'Wrong type for attribute: data_type. Expected: str. Got: ' + str(type(self.data_type)) + '.'
      json_data['dataType'] = self.data_type

    if self.device_name:
      assert isinstance(self.device_name, str), 'Wrong type for attribute: device_name. Expected: str. Got: ' + str(type(self.device_name)) + '.'
      json_data['deviceName'] = self.device_name

    if self.device_type:
      assert isinstance(self.device_type, str), 'Wrong type for attribute: device_type. Expected: str. Got: ' + str(type(self.device_type)) + '.'
      json_data['deviceType'] = self.device_type

    if self.keys:
      assert isinstance(self.keys, list), 'Wrong type for attribute: keys. Expected: list. Got: ' + str(type(self.keys)) + '.'
      json_data['keys'] = self.keys

    if self.py_type:
      assert isinstance(self.py_type, str), 'Wrong type for attribute: py_type. Expected: str. Got: ' + str(type(self.py_type)) + '.'
      json_data['type'] = self.py_type

    if self.replaces:
      assert isinstance(self.replaces, bool), 'Wrong type for attribute: replaces. Expected: bool. Got: ' + str(type(self.replaces)) + '.'
      json_data['replaces'] = self.replaces

    if self.stop_propagation:
      assert isinstance(self.stop_propagation, bool), 'Wrong type for attribute: stop_propagation. Expected: bool. Got: ' + str(type(self.stop_propagation)) + '.'
      json_data['stopPropagation'] = self.stop_propagation

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'MachineInterface':
    """Convert JSON to type object."""
    obj = MachineInterface()
    json_list: List[Any]

    expected_json_keys: List[str] = ['dataType', 'deviceName', 'deviceType', 'keys', 'type', 'replaces', 'stopPropagation']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid MachineInterface. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'dataType' in json_data:
      assert isinstance(json_data['dataType'], str), 'Wrong type for attribute: dataType. Expected: str. Got: ' + str(type(json_data['dataType'])) + '.'
      obj.data_type = json_data['dataType']

    if 'deviceName' in json_data:
      assert isinstance(json_data['deviceName'], str), 'Wrong type for attribute: deviceName. Expected: str. Got: ' + str(type(json_data['deviceName'])) + '.'
      obj.device_name = json_data['deviceName']

    if 'deviceType' in json_data:
      assert isinstance(json_data['deviceType'], str), 'Wrong type for attribute: deviceType. Expected: str. Got: ' + str(type(json_data['deviceType'])) + '.'
      obj.device_type = json_data['deviceType']

    if 'keys' in json_data:
      assert isinstance(json_data['keys'], list), 'Wrong type for attribute: keys. Expected: list. Got: ' + str(type(json_data['keys'])) + '.'
      json_list = []
      for j in json_data['keys']:
        json_list.append(j)
      obj.keys = json_list

    if 'type' in json_data:
      assert isinstance(json_data['type'], str), 'Wrong type for attribute: type. Expected: str. Got: ' + str(type(json_data['type'])) + '.'
      obj.py_type = json_data['type']

    if 'replaces' in json_data:
      assert isinstance(json_data['replaces'], bool), 'Wrong type for attribute: replaces. Expected: bool. Got: ' + str(type(json_data['replaces'])) + '.'
      obj.replaces = json_data['replaces']

    if 'stopPropagation' in json_data:
      assert isinstance(json_data['stopPropagation'], bool), 'Wrong type for attribute: stopPropagation. Expected: bool. Got: ' + str(type(json_data['stopPropagation'])) + '.'
      obj.stop_propagation = json_data['stopPropagation']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.MachineInterface) -> 'MachineInterface':
    """Convert MachineInterface proto to type object."""
    if not proto:
      return None
    obj = MachineInterface()
    obj.data_type = get_proto_value(proto.data_type)
    obj.device_name = get_proto_value(proto.device_name)
    obj.device_type = get_proto_value(proto.device_type)
    if proto.keys:
      json_list = []
      for j in proto.keys:
        json_list.append(j)
      obj.keys = json_list
    obj.py_type = get_proto_value(proto.type)
    obj.replaces = get_proto_value(proto.replaces)
    obj.stop_propagation = get_proto_value(proto.stop_propagation)
    return obj


class MachineInterfaces:
  """Representation of proto message MachineInterfaces.

   MachineInterfaces is a list of machine interfaces.
  """
  # The interfaces provided by the machine.
  interfaces: List['MachineInterface']

  def __init__(self, interfaces: Optional[List['MachineInterface']] = None) -> None:
    if interfaces is None:
      self.interfaces = []
    else:
      self.interfaces = interfaces

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.interfaces:
      assert isinstance(self.interfaces, list), 'Wrong type for attribute: interfaces. Expected: list. Got: ' + str(type(self.interfaces)) + '.'
      obj_list = []
      for item in self.interfaces:
        obj_list.append(item.to_json())
      json_data['interfaces'] = obj_list

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'MachineInterfaces':
    """Convert JSON to type object."""
    obj = MachineInterfaces()
    json_list: List[Any]

    expected_json_keys: List[str] = ['interfaces']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid MachineInterfaces. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'interfaces' in json_data:
      assert isinstance(json_data['interfaces'], list), 'Wrong type for attribute: interfaces. Expected: list. Got: ' + str(type(json_data['interfaces'])) + '.'
      json_list = []
      for j in json_data['interfaces']:
        json_list.append(MachineInterface.from_json(j))
      obj.interfaces = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.MachineInterfaces) -> 'MachineInterfaces':
    """Convert MachineInterfaces proto to type object."""
    if not proto:
      return None
    obj = MachineInterfaces()
    if proto.interfaces:
      json_list = []
      for j in proto.interfaces:
        json_list.append(MachineInterface.from_proto(j))
      obj.interfaces = json_list
    return obj


class MessageLastTimestamp:
  """Representation of proto message MessageLastTimestamp.

   MessageLastTimestamp stores the last timestamp of a given message in the
   metadata for logs. The timestamp can be used to go back in the logs to
   retrieve that last value of the message. See design doc:
  """
  device_type: str
  device_name: str
  data_type: str
  key: str
  last_ts: int

  def __init__(self, data_type: str = '', device_name: str = '', device_type: str = '', key: str = '', last_ts: int = 0) -> None:
    self.data_type = data_type
    self.device_name = device_name
    self.device_type = device_type
    self.key = key
    self.last_ts = last_ts

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.data_type:
      assert isinstance(self.data_type, str), 'Wrong type for attribute: data_type. Expected: str. Got: ' + str(type(self.data_type)) + '.'
      json_data['dataType'] = self.data_type

    if self.device_name:
      assert isinstance(self.device_name, str), 'Wrong type for attribute: device_name. Expected: str. Got: ' + str(type(self.device_name)) + '.'
      json_data['deviceName'] = self.device_name

    if self.device_type:
      assert isinstance(self.device_type, str), 'Wrong type for attribute: device_type. Expected: str. Got: ' + str(type(self.device_type)) + '.'
      json_data['deviceType'] = self.device_type

    if self.key:
      assert isinstance(self.key, str), 'Wrong type for attribute: key. Expected: str. Got: ' + str(type(self.key)) + '.'
      json_data['key'] = self.key

    if self.last_ts:
      assert isinstance(self.last_ts, int), 'Wrong type for attribute: last_ts. Expected: int. Got: ' + str(type(self.last_ts)) + '.'
      json_data['LastTS'] = self.last_ts

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'MessageLastTimestamp':
    """Convert JSON to type object."""
    obj = MessageLastTimestamp()

    expected_json_keys: List[str] = ['dataType', 'deviceName', 'deviceType', 'key', 'LastTS']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid MessageLastTimestamp. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'dataType' in json_data:
      assert isinstance(json_data['dataType'], str), 'Wrong type for attribute: dataType. Expected: str. Got: ' + str(type(json_data['dataType'])) + '.'
      obj.data_type = json_data['dataType']

    if 'deviceName' in json_data:
      assert isinstance(json_data['deviceName'], str), 'Wrong type for attribute: deviceName. Expected: str. Got: ' + str(type(json_data['deviceName'])) + '.'
      obj.device_name = json_data['deviceName']

    if 'deviceType' in json_data:
      assert isinstance(json_data['deviceType'], str), 'Wrong type for attribute: deviceType. Expected: str. Got: ' + str(type(json_data['deviceType'])) + '.'
      obj.device_type = json_data['deviceType']

    if 'key' in json_data:
      assert isinstance(json_data['key'], str), 'Wrong type for attribute: key. Expected: str. Got: ' + str(type(json_data['key'])) + '.'
      obj.key = json_data['key']

    if 'LastTS' in json_data:
      assert isinstance(json_data['LastTS'], int), 'Wrong type for attribute: LastTS. Expected: int. Got: ' + str(type(json_data['LastTS'])) + '.'
      obj.last_ts = json_data['LastTS']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.MessageLastTimestamp) -> 'MessageLastTimestamp':
    """Convert MessageLastTimestamp proto to type object."""
    if not proto:
      return None
    obj = MessageLastTimestamp()
    obj.data_type = get_proto_value(proto.data_type)
    obj.device_name = get_proto_value(proto.device_name)
    obj.device_type = get_proto_value(proto.device_type)
    obj.key = get_proto_value(proto.key)
    obj.last_ts = get_proto_value(proto.last_ts)
    return obj


class Metadata:
  """Representation of proto message Metadata.

   Metadata will be used for any kind of metadata logging purposes.
  """
  # Comment can contain any metadata related information.
  comment: str

  # Refers to log files. Only existent if it's the first line of the file.
  begin_file: bool

  # Refers to log files. Only existent if it's the last line of the file.
  end_file: bool

  # Reflects the command line argument value of “--real_time_logs”
  real_time_logs: bool

  def __init__(self, begin_file: bool = False, comment: str = '', end_file: bool = False, real_time_logs: bool = False) -> None:
    self.begin_file = begin_file
    self.comment = comment
    self.end_file = end_file
    self.real_time_logs = real_time_logs

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.begin_file:
      assert isinstance(self.begin_file, bool), 'Wrong type for attribute: begin_file. Expected: bool. Got: ' + str(type(self.begin_file)) + '.'
      json_data['beginFile'] = self.begin_file

    if self.comment:
      assert isinstance(self.comment, str), 'Wrong type for attribute: comment. Expected: str. Got: ' + str(type(self.comment)) + '.'
      json_data['comment'] = self.comment

    if self.end_file:
      assert isinstance(self.end_file, bool), 'Wrong type for attribute: end_file. Expected: bool. Got: ' + str(type(self.end_file)) + '.'
      json_data['endFile'] = self.end_file

    if self.real_time_logs:
      assert isinstance(self.real_time_logs, bool), 'Wrong type for attribute: real_time_logs. Expected: bool. Got: ' + str(type(self.real_time_logs)) + '.'
      json_data['realTimeLogs'] = self.real_time_logs

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'Metadata':
    """Convert JSON to type object."""
    obj = Metadata()

    expected_json_keys: List[str] = ['beginFile', 'comment', 'endFile', 'realTimeLogs']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid Metadata. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'beginFile' in json_data:
      assert isinstance(json_data['beginFile'], bool), 'Wrong type for attribute: beginFile. Expected: bool. Got: ' + str(type(json_data['beginFile'])) + '.'
      obj.begin_file = json_data['beginFile']

    if 'comment' in json_data:
      assert isinstance(json_data['comment'], str), 'Wrong type for attribute: comment. Expected: str. Got: ' + str(type(json_data['comment'])) + '.'
      obj.comment = json_data['comment']

    if 'endFile' in json_data:
      assert isinstance(json_data['endFile'], bool), 'Wrong type for attribute: endFile. Expected: bool. Got: ' + str(type(json_data['endFile'])) + '.'
      obj.end_file = json_data['endFile']

    if 'realTimeLogs' in json_data:
      assert isinstance(json_data['realTimeLogs'], bool), 'Wrong type for attribute: realTimeLogs. Expected: bool. Got: ' + str(type(json_data['realTimeLogs'])) + '.'
      obj.real_time_logs = json_data['realTimeLogs']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.Metadata) -> 'Metadata':
    """Convert Metadata proto to type object."""
    if not proto:
      return None
    obj = Metadata()
    obj.begin_file = get_proto_value(proto.begin_file)
    obj.comment = get_proto_value(proto.comment)
    obj.end_file = get_proto_value(proto.end_file)
    obj.real_time_logs = get_proto_value(proto.real_time_logs)
    return obj


class Metric:
  """Representation of proto message Metric.

   Metric is a metric value for internal metrics tracking. Values are always of
   type KeyValue. Labels are always of type array of KeyValue.
  """
  metric_value: Optional['KeyValue']
  labels: List['KeyValue']

  def __init__(self, labels: Optional[List['KeyValue']] = None, metric_value: Optional['KeyValue'] = None) -> None:
    if labels is None:
      self.labels = []
    else:
      self.labels = labels
    self.metric_value = metric_value

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.labels:
      assert isinstance(self.labels, list), 'Wrong type for attribute: labels. Expected: list. Got: ' + str(type(self.labels)) + '.'
      obj_list = []
      for item in self.labels:
        obj_list.append(item.to_json())
      json_data['metricLabels'] = obj_list

    if self.metric_value:
      assert self.metric_value.__class__.__name__ == 'KeyValue', 'Wrong type for attribute: metric_value. Expected: KeyValue. Got: ' + str(type(self.metric_value)) + '.'
      json_data['metricValue'] = self.metric_value.to_json()

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'Metric':
    """Convert JSON to type object."""
    obj = Metric()
    json_list: List[Any]

    expected_json_keys: List[str] = ['metricLabels', 'metricValue']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid Metric. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'metricLabels' in json_data:
      assert isinstance(json_data['metricLabels'], list), 'Wrong type for attribute: metricLabels. Expected: list. Got: ' + str(type(json_data['metricLabels'])) + '.'
      json_list = []
      for j in json_data['metricLabels']:
        json_list.append(KeyValue.from_json(j))
      obj.labels = json_list

    if 'metricValue' in json_data:
      assert isinstance(json_data['metricValue'], dict), 'Wrong type for attribute: metricValue. Expected: dict. Got: ' + str(type(json_data['metricValue'])) + '.'
      obj.metric_value = KeyValue.from_json(json_data['metricValue'])

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.Metric) -> 'Metric':
    """Convert Metric proto to type object."""
    if not proto:
      return None
    obj = Metric()
    if proto.labels:
      json_list = []
      for j in proto.labels:
        json_list.append(KeyValue.from_proto(j))
      obj.labels = json_list
    obj.metric_value = KeyValue.from_proto(get_proto_field(proto, 'value'))
    return obj


class MoveJPathArgs:
  """Representation of proto message MoveJPathArgs.

   Execute a path in joint-space.
  """
  waypoints: List['MoveJWaypointArgs']

  def __init__(self, waypoints: Optional[List['MoveJWaypointArgs']] = None) -> None:
    if waypoints is None:
      self.waypoints = []
    else:
      self.waypoints = waypoints

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.waypoints:
      assert isinstance(self.waypoints, list), 'Wrong type for attribute: waypoints. Expected: list. Got: ' + str(type(self.waypoints)) + '.'
      obj_list = []
      for item in self.waypoints:
        obj_list.append(item.to_json())
      json_data['waypoints'] = obj_list

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'MoveJPathArgs':
    """Convert JSON to type object."""
    obj = MoveJPathArgs()
    json_list: List[Any]

    expected_json_keys: List[str] = ['waypoints']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid MoveJPathArgs. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'waypoints' in json_data:
      assert isinstance(json_data['waypoints'], list), 'Wrong type for attribute: waypoints. Expected: list. Got: ' + str(type(json_data['waypoints'])) + '.'
      json_list = []
      for j in json_data['waypoints']:
        json_list.append(MoveJWaypointArgs.from_json(j))
      obj.waypoints = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.MoveJPathArgs) -> 'MoveJPathArgs':
    """Convert MoveJPathArgs proto to type object."""
    if not proto:
      return None
    obj = MoveJPathArgs()
    if proto.waypoints:
      json_list = []
      for j in proto.waypoints:
        json_list.append(MoveJWaypointArgs.from_proto(j))
      obj.waypoints = json_list
    return obj


class MoveJWaypointArgs:
  """Representation of proto message MoveJWaypointArgs.

   Move to a position in joint-space. The exact number and interpretation
   of rotation elements is robot-dependent. If the blend radius is not present,
   then the default blend radius (set via SetBlendRadius) will be used.
   The velocity is measured in rad/sec and acceleration in rad/sec/sec.
   If the velocity is not present then the default velocity (set via
   SetRadialSpeed) will be used (but it will be interpreted as rad/sec). If the
   acceleration is not present then the default acceleration (set via
   SetRadialSpeed) will be used (but it will be interpreted as rad/sec/sec).
  """
  rotation: List[float]
  blend_radius: float

  # In going from the current joint position to this waypoint, this is the
  # highest velocity across all joints.
  velocity: float

  # In going from the current joint position to this waypoint, this is the
  # highest acceleration across all joints.
  acceleration: float

  # Early termination limits for the move.
  limits: Optional['Limits']

  # If set, the move should be as rapid as the robot can go. It is generally
  # expected that the movement distance is "small".
  servo: bool

  # For UR only. Applies only if servo is true.
  # If nonzero, this is the "t" parameter in the servoj command
  # in the generated URScript. According to the URScript documentation
  # (https://s3-eu-west-1.amazonaws.com/ur-support-site/32554/scriptManual-3.5.4.pdf),
  # this parameter is "time where the command is controlling the robot. The
  # function is blocking for time t [S]"
  #
  # If zero, the parameter is UR's default, which according to the
  # documentation is 0.008 seconds.
  #
  # If this parameter is nonzero for a robot other than UR, an error will be
  # returned.
  servo_t_secs: float

  # For UR only. Applies only if servo is true.
  # If nonzero, this is the "lookahead_time" parameter in the
  # servoj command in the generated URScript. According to the URScript
  # documentation
  # (https://s3-eu-west-1.amazonaws.com/ur-support-site/32554/scriptManual-3.5.4.pdf),
  # this parameter is "time [S], range [0.03,0.2] smoothens the trajectory with
  # this lookahead time"
  #
  # If zero, the parameter is UR's default, which according to the
  # documentation is 0.1 seconds.
  #
  # If this parameter is nonzero for a robot other than UR, an error will be
  # returned.
  servo_lookahead_time_secs: float

  # For UR only. Applies only if servo is true.
  # If nonzero, this is the "gain" parameter in the
  # servoj command in the generated URScript. According to the URScript
  # documentation
  # (https://s3-eu-west-1.amazonaws.com/ur-support-site/32554/scriptManual-3.5.4.pdf),
  # this parameter is "proportional gain for following target position, range
  # [100,2000]"
  #
  # If zero, the parameter is UR's default, which according to the
  # documentation is 300.
  #
  # If this parameter is nonzero for a robot other than UR, an error will be
  # returned.
  servo_gain: float

  def __init__(self, acceleration: float = 0.0, blend_radius: float = 0.0, limits: Optional['Limits'] = None, rotation: Optional[List[float]] = None, servo: bool = False, servo_gain: float = 0.0, servo_lookahead_time_secs: float = 0.0, servo_t_secs: float = 0.0, velocity: float = 0.0) -> None:
    self.acceleration = acceleration
    self.blend_radius = blend_radius
    self.limits = limits
    if rotation is None:
      self.rotation = []
    else:
      self.rotation = rotation
    self.servo = servo
    self.servo_gain = servo_gain
    self.servo_lookahead_time_secs = servo_lookahead_time_secs
    self.servo_t_secs = servo_t_secs
    self.velocity = velocity

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.acceleration:
      assert isinstance(self.acceleration, float) or isinstance(self.acceleration, int), 'Wrong type for attribute: acceleration. Expected: float. Got: ' + str(type(self.acceleration)) + '.'
      json_data['acceleration'] = self.acceleration

    if self.blend_radius:
      assert isinstance(self.blend_radius, float) or isinstance(self.blend_radius, int), 'Wrong type for attribute: blend_radius. Expected: float. Got: ' + str(type(self.blend_radius)) + '.'
      json_data['blendRadius'] = self.blend_radius

    if self.limits:
      assert self.limits.__class__.__name__ == 'Limits', 'Wrong type for attribute: limits. Expected: Limits. Got: ' + str(type(self.limits)) + '.'
      json_data['limits'] = self.limits.to_json()

    if self.rotation:
      assert isinstance(self.rotation, list), 'Wrong type for attribute: rotation. Expected: list. Got: ' + str(type(self.rotation)) + '.'
      json_data['rotation'] = self.rotation

    if self.servo:
      assert isinstance(self.servo, bool), 'Wrong type for attribute: servo. Expected: bool. Got: ' + str(type(self.servo)) + '.'
      json_data['servo'] = self.servo

    if self.servo_gain:
      assert isinstance(self.servo_gain, float) or isinstance(self.servo_gain, int), 'Wrong type for attribute: servo_gain. Expected: float. Got: ' + str(type(self.servo_gain)) + '.'
      json_data['servoGain'] = self.servo_gain

    if self.servo_lookahead_time_secs:
      assert isinstance(self.servo_lookahead_time_secs, float) or isinstance(self.servo_lookahead_time_secs, int), 'Wrong type for attribute: servo_lookahead_time_secs. Expected: float. Got: ' + str(type(self.servo_lookahead_time_secs)) + '.'
      json_data['servoLookaheadTimeSecs'] = self.servo_lookahead_time_secs

    if self.servo_t_secs:
      assert isinstance(self.servo_t_secs, float) or isinstance(self.servo_t_secs, int), 'Wrong type for attribute: servo_t_secs. Expected: float. Got: ' + str(type(self.servo_t_secs)) + '.'
      json_data['servoTSecs'] = self.servo_t_secs

    if self.velocity:
      assert isinstance(self.velocity, float) or isinstance(self.velocity, int), 'Wrong type for attribute: velocity. Expected: float. Got: ' + str(type(self.velocity)) + '.'
      json_data['velocity'] = self.velocity

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'MoveJWaypointArgs':
    """Convert JSON to type object."""
    obj = MoveJWaypointArgs()
    json_list: List[Any]

    expected_json_keys: List[str] = ['acceleration', 'blendRadius', 'limits', 'rotation', 'servo', 'servoGain', 'servoLookaheadTimeSecs', 'servoTSecs', 'velocity']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid MoveJWaypointArgs. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'acceleration' in json_data:
      assert isinstance(json_data['acceleration'], float) or isinstance(json_data['acceleration'], int), 'Wrong type for attribute: acceleration. Expected: float. Got: ' + str(type(json_data['acceleration'])) + '.'
      obj.acceleration = json_data['acceleration']

    if 'blendRadius' in json_data:
      assert isinstance(json_data['blendRadius'], float) or isinstance(json_data['blendRadius'], int), 'Wrong type for attribute: blendRadius. Expected: float. Got: ' + str(type(json_data['blendRadius'])) + '.'
      obj.blend_radius = json_data['blendRadius']

    if 'limits' in json_data:
      assert isinstance(json_data['limits'], dict), 'Wrong type for attribute: limits. Expected: dict. Got: ' + str(type(json_data['limits'])) + '.'
      obj.limits = Limits.from_json(json_data['limits'])

    if 'rotation' in json_data:
      assert isinstance(json_data['rotation'], list), 'Wrong type for attribute: rotation. Expected: list. Got: ' + str(type(json_data['rotation'])) + '.'
      json_list = []
      for j in json_data['rotation']:
        json_list.append(j)
      obj.rotation = json_list

    if 'servo' in json_data:
      assert isinstance(json_data['servo'], bool), 'Wrong type for attribute: servo. Expected: bool. Got: ' + str(type(json_data['servo'])) + '.'
      obj.servo = json_data['servo']

    if 'servoGain' in json_data:
      assert isinstance(json_data['servoGain'], float) or isinstance(json_data['servoGain'], int), 'Wrong type for attribute: servoGain. Expected: float. Got: ' + str(type(json_data['servoGain'])) + '.'
      obj.servo_gain = json_data['servoGain']

    if 'servoLookaheadTimeSecs' in json_data:
      assert isinstance(json_data['servoLookaheadTimeSecs'], float) or isinstance(json_data['servoLookaheadTimeSecs'], int), 'Wrong type for attribute: servoLookaheadTimeSecs. Expected: float. Got: ' + str(type(json_data['servoLookaheadTimeSecs'])) + '.'
      obj.servo_lookahead_time_secs = json_data['servoLookaheadTimeSecs']

    if 'servoTSecs' in json_data:
      assert isinstance(json_data['servoTSecs'], float) or isinstance(json_data['servoTSecs'], int), 'Wrong type for attribute: servoTSecs. Expected: float. Got: ' + str(type(json_data['servoTSecs'])) + '.'
      obj.servo_t_secs = json_data['servoTSecs']

    if 'velocity' in json_data:
      assert isinstance(json_data['velocity'], float) or isinstance(json_data['velocity'], int), 'Wrong type for attribute: velocity. Expected: float. Got: ' + str(type(json_data['velocity'])) + '.'
      obj.velocity = json_data['velocity']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.MoveJWaypointArgs) -> 'MoveJWaypointArgs':
    """Convert MoveJWaypointArgs proto to type object."""
    if not proto:
      return None
    obj = MoveJWaypointArgs()
    obj.acceleration = get_proto_value(proto.acceleration)
    obj.blend_radius = get_proto_value(proto.blend_radius)
    obj.limits = Limits.from_proto(get_proto_field(proto, 'limits'))
    if proto.rotation:
      json_list = []
      for j in proto.rotation:
        json_list.append(j)
      obj.rotation = json_list
    obj.servo = get_proto_value(proto.servo)
    obj.servo_gain = get_proto_value(proto.servo_gain)
    obj.servo_lookahead_time_secs = get_proto_value(proto.servo_lookahead_time_secs)
    obj.servo_t_secs = get_proto_value(proto.servo_t_secs)
    obj.velocity = get_proto_value(proto.velocity)
    return obj


class MoveLPathArgs:
  """Representation of proto message MoveLPathArgs.

   Execute a linear path in joint-space.
  """
  waypoints: List['MoveLWaypointArgs']

  def __init__(self, waypoints: Optional[List['MoveLWaypointArgs']] = None) -> None:
    if waypoints is None:
      self.waypoints = []
    else:
      self.waypoints = waypoints

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.waypoints:
      assert isinstance(self.waypoints, list), 'Wrong type for attribute: waypoints. Expected: list. Got: ' + str(type(self.waypoints)) + '.'
      obj_list = []
      for item in self.waypoints:
        obj_list.append(item.to_json())
      json_data['waypoints'] = obj_list

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'MoveLPathArgs':
    """Convert JSON to type object."""
    obj = MoveLPathArgs()
    json_list: List[Any]

    expected_json_keys: List[str] = ['waypoints']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid MoveLPathArgs. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'waypoints' in json_data:
      assert isinstance(json_data['waypoints'], list), 'Wrong type for attribute: waypoints. Expected: list. Got: ' + str(type(json_data['waypoints'])) + '.'
      json_list = []
      for j in json_data['waypoints']:
        json_list.append(MoveLWaypointArgs.from_json(j))
      obj.waypoints = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.MoveLPathArgs) -> 'MoveLPathArgs':
    """Convert MoveLPathArgs proto to type object."""
    if not proto:
      return None
    obj = MoveLPathArgs()
    if proto.waypoints:
      json_list = []
      for j in proto.waypoints:
        json_list.append(MoveLWaypointArgs.from_proto(j))
      obj.waypoints = json_list
    return obj


class MoveLWaypointArgs:
  """Representation of proto message MoveLWaypointArgs.

   Move to a position linearly in joint-space. The exact number and
   interpretation of rotation elements is robot-dependent. If the blend radius
   is not present, then the default blend radius (set via SetBlendRadius) will
   be used. The velocity is measured in m/sec and acceleration in m/sec/sec.
   If the velocity is not present then the default velocity (set via
   SetRadialSpeed) will be used (but it will be interpreted as m/sec). If the
   acceleration is not present then the default acceleration (set via
   SetRadialSpeed) will be used (but it will be interpreted as m/sec/sec).
  """
  rotation: List[float]
  blend_radius: float
  velocity: float
  acceleration: float

  # Early termination limits for the move.
  limits: Optional['Limits']

  # If set, the move should be as rapid as the robot can go. It is generally
  # expected that the movement distance is "small".
  servo: bool

  def __init__(self, acceleration: float = 0.0, blend_radius: float = 0.0, limits: Optional['Limits'] = None, rotation: Optional[List[float]] = None, servo: bool = False, velocity: float = 0.0) -> None:
    self.acceleration = acceleration
    self.blend_radius = blend_radius
    self.limits = limits
    if rotation is None:
      self.rotation = []
    else:
      self.rotation = rotation
    self.servo = servo
    self.velocity = velocity

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.acceleration:
      assert isinstance(self.acceleration, float) or isinstance(self.acceleration, int), 'Wrong type for attribute: acceleration. Expected: float. Got: ' + str(type(self.acceleration)) + '.'
      json_data['acceleration'] = self.acceleration

    if self.blend_radius:
      assert isinstance(self.blend_radius, float) or isinstance(self.blend_radius, int), 'Wrong type for attribute: blend_radius. Expected: float. Got: ' + str(type(self.blend_radius)) + '.'
      json_data['blendRadius'] = self.blend_radius

    if self.limits:
      assert self.limits.__class__.__name__ == 'Limits', 'Wrong type for attribute: limits. Expected: Limits. Got: ' + str(type(self.limits)) + '.'
      json_data['limits'] = self.limits.to_json()

    if self.rotation:
      assert isinstance(self.rotation, list), 'Wrong type for attribute: rotation. Expected: list. Got: ' + str(type(self.rotation)) + '.'
      json_data['rotation'] = self.rotation

    if self.servo:
      assert isinstance(self.servo, bool), 'Wrong type for attribute: servo. Expected: bool. Got: ' + str(type(self.servo)) + '.'
      json_data['servo'] = self.servo

    if self.velocity:
      assert isinstance(self.velocity, float) or isinstance(self.velocity, int), 'Wrong type for attribute: velocity. Expected: float. Got: ' + str(type(self.velocity)) + '.'
      json_data['velocity'] = self.velocity

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'MoveLWaypointArgs':
    """Convert JSON to type object."""
    obj = MoveLWaypointArgs()
    json_list: List[Any]

    expected_json_keys: List[str] = ['acceleration', 'blendRadius', 'limits', 'rotation', 'servo', 'velocity']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid MoveLWaypointArgs. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'acceleration' in json_data:
      assert isinstance(json_data['acceleration'], float) or isinstance(json_data['acceleration'], int), 'Wrong type for attribute: acceleration. Expected: float. Got: ' + str(type(json_data['acceleration'])) + '.'
      obj.acceleration = json_data['acceleration']

    if 'blendRadius' in json_data:
      assert isinstance(json_data['blendRadius'], float) or isinstance(json_data['blendRadius'], int), 'Wrong type for attribute: blendRadius. Expected: float. Got: ' + str(type(json_data['blendRadius'])) + '.'
      obj.blend_radius = json_data['blendRadius']

    if 'limits' in json_data:
      assert isinstance(json_data['limits'], dict), 'Wrong type for attribute: limits. Expected: dict. Got: ' + str(type(json_data['limits'])) + '.'
      obj.limits = Limits.from_json(json_data['limits'])

    if 'rotation' in json_data:
      assert isinstance(json_data['rotation'], list), 'Wrong type for attribute: rotation. Expected: list. Got: ' + str(type(json_data['rotation'])) + '.'
      json_list = []
      for j in json_data['rotation']:
        json_list.append(j)
      obj.rotation = json_list

    if 'servo' in json_data:
      assert isinstance(json_data['servo'], bool), 'Wrong type for attribute: servo. Expected: bool. Got: ' + str(type(json_data['servo'])) + '.'
      obj.servo = json_data['servo']

    if 'velocity' in json_data:
      assert isinstance(json_data['velocity'], float) or isinstance(json_data['velocity'], int), 'Wrong type for attribute: velocity. Expected: float. Got: ' + str(type(json_data['velocity'])) + '.'
      obj.velocity = json_data['velocity']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.MoveLWaypointArgs) -> 'MoveLWaypointArgs':
    """Convert MoveLWaypointArgs proto to type object."""
    if not proto:
      return None
    obj = MoveLWaypointArgs()
    obj.acceleration = get_proto_value(proto.acceleration)
    obj.blend_radius = get_proto_value(proto.blend_radius)
    obj.limits = Limits.from_proto(get_proto_field(proto, 'limits'))
    if proto.rotation:
      json_list = []
      for j in proto.rotation:
        json_list.append(j)
      obj.rotation = json_list
    obj.servo = get_proto_value(proto.servo)
    obj.velocity = get_proto_value(proto.velocity)
    return obj


class MovePosePathArgs:
  """Representation of proto message MovePosePathArgs.

   MovePosePathArgs executes a path in Cartesian space.
  """
  waypoints: List['MovePoseWaypointArgs']

  def __init__(self, waypoints: Optional[List['MovePoseWaypointArgs']] = None) -> None:
    if waypoints is None:
      self.waypoints = []
    else:
      self.waypoints = waypoints

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.waypoints:
      assert isinstance(self.waypoints, list), 'Wrong type for attribute: waypoints. Expected: list. Got: ' + str(type(self.waypoints)) + '.'
      obj_list = []
      for item in self.waypoints:
        obj_list.append(item.to_json())
      json_data['waypoints'] = obj_list

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'MovePosePathArgs':
    """Convert JSON to type object."""
    obj = MovePosePathArgs()
    json_list: List[Any]

    expected_json_keys: List[str] = ['waypoints']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid MovePosePathArgs. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'waypoints' in json_data:
      assert isinstance(json_data['waypoints'], list), 'Wrong type for attribute: waypoints. Expected: list. Got: ' + str(type(json_data['waypoints'])) + '.'
      json_list = []
      for j in json_data['waypoints']:
        json_list.append(MovePoseWaypointArgs.from_json(j))
      obj.waypoints = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.MovePosePathArgs) -> 'MovePosePathArgs':
    """Convert MovePosePathArgs proto to type object."""
    if not proto:
      return None
    obj = MovePosePathArgs()
    if proto.waypoints:
      json_list = []
      for j in proto.waypoints:
        json_list.append(MovePoseWaypointArgs.from_proto(j))
      obj.waypoints = json_list
    return obj


class MovePoseWaypointArgs:
  """Representation of proto message MovePoseWaypointArgs.

   MovePoseWaypointArgs moves to a position in cartesion-space.
  """
  # u, v, w in meters
  translation: Optional['Vec3d']

  # ru, rv, rw as Rodrigues axis-angle, in radians
  rotation: Optional['Vec3d']

  # Whether the move is linear. It is in joint-space otherwise.
  linear: bool

  # The blend radius is measured in meters.
  # If the blend radius is not present, then the default blend radius
  # (set via SetBlendRadius) will be used.
  blend_radius: float

  # The velocity is measured in m/sec if linear, rad/sec if not.
  # If the velocity is not present then the default velocity (set via
  # SetRadialSpeed) will be used (but it will be interpreted as rad/sec).
  velocity: float

  # The acceleration is measured in m/sec/sec if linear, rad/sec/sec if not.
  # If the acceleration is not present then the default acceleration (set via
  # SetRadialSpeed) will be used (but it will be interpreted as rad/sec/sec).
  acceleration: float

  # Early termination limits for the move.
  limits: Optional['Limits']

  def __init__(self, acceleration: float = 0.0, blend_radius: float = 0.0, limits: Optional['Limits'] = None, linear: bool = False, rotation: Optional['Vec3d'] = None, translation: Optional['Vec3d'] = None, velocity: float = 0.0) -> None:
    self.acceleration = acceleration
    self.blend_radius = blend_radius
    self.limits = limits
    self.linear = linear
    self.rotation = rotation
    self.translation = translation
    self.velocity = velocity

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.acceleration:
      assert isinstance(self.acceleration, float) or isinstance(self.acceleration, int), 'Wrong type for attribute: acceleration. Expected: float. Got: ' + str(type(self.acceleration)) + '.'
      json_data['acceleration'] = self.acceleration

    if self.blend_radius:
      assert isinstance(self.blend_radius, float) or isinstance(self.blend_radius, int), 'Wrong type for attribute: blend_radius. Expected: float. Got: ' + str(type(self.blend_radius)) + '.'
      json_data['blendRadius'] = self.blend_radius

    if self.limits:
      assert self.limits.__class__.__name__ == 'Limits', 'Wrong type for attribute: limits. Expected: Limits. Got: ' + str(type(self.limits)) + '.'
      json_data['limits'] = self.limits.to_json()

    if self.linear:
      assert isinstance(self.linear, bool), 'Wrong type for attribute: linear. Expected: bool. Got: ' + str(type(self.linear)) + '.'
      json_data['linear'] = self.linear

    if self.rotation:
      assert self.rotation.__class__.__name__ == 'Vec3d', 'Wrong type for attribute: rotation. Expected: Vec3d. Got: ' + str(type(self.rotation)) + '.'
      json_data['rotation'] = self.rotation.to_json()

    if self.translation:
      assert self.translation.__class__.__name__ == 'Vec3d', 'Wrong type for attribute: translation. Expected: Vec3d. Got: ' + str(type(self.translation)) + '.'
      json_data['translation'] = self.translation.to_json()

    if self.velocity:
      assert isinstance(self.velocity, float) or isinstance(self.velocity, int), 'Wrong type for attribute: velocity. Expected: float. Got: ' + str(type(self.velocity)) + '.'
      json_data['velocity'] = self.velocity

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'MovePoseWaypointArgs':
    """Convert JSON to type object."""
    obj = MovePoseWaypointArgs()

    expected_json_keys: List[str] = ['acceleration', 'blendRadius', 'limits', 'linear', 'rotation', 'translation', 'velocity']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid MovePoseWaypointArgs. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'acceleration' in json_data:
      assert isinstance(json_data['acceleration'], float) or isinstance(json_data['acceleration'], int), 'Wrong type for attribute: acceleration. Expected: float. Got: ' + str(type(json_data['acceleration'])) + '.'
      obj.acceleration = json_data['acceleration']

    if 'blendRadius' in json_data:
      assert isinstance(json_data['blendRadius'], float) or isinstance(json_data['blendRadius'], int), 'Wrong type for attribute: blendRadius. Expected: float. Got: ' + str(type(json_data['blendRadius'])) + '.'
      obj.blend_radius = json_data['blendRadius']

    if 'limits' in json_data:
      assert isinstance(json_data['limits'], dict), 'Wrong type for attribute: limits. Expected: dict. Got: ' + str(type(json_data['limits'])) + '.'
      obj.limits = Limits.from_json(json_data['limits'])

    if 'linear' in json_data:
      assert isinstance(json_data['linear'], bool), 'Wrong type for attribute: linear. Expected: bool. Got: ' + str(type(json_data['linear'])) + '.'
      obj.linear = json_data['linear']

    if 'rotation' in json_data:
      assert isinstance(json_data['rotation'], dict), 'Wrong type for attribute: rotation. Expected: dict. Got: ' + str(type(json_data['rotation'])) + '.'
      obj.rotation = Vec3d.from_json(json_data['rotation'])

    if 'translation' in json_data:
      assert isinstance(json_data['translation'], dict), 'Wrong type for attribute: translation. Expected: dict. Got: ' + str(type(json_data['translation'])) + '.'
      obj.translation = Vec3d.from_json(json_data['translation'])

    if 'velocity' in json_data:
      assert isinstance(json_data['velocity'], float) or isinstance(json_data['velocity'], int), 'Wrong type for attribute: velocity. Expected: float. Got: ' + str(type(json_data['velocity'])) + '.'
      obj.velocity = json_data['velocity']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.MovePoseWaypointArgs) -> 'MovePoseWaypointArgs':
    """Convert MovePoseWaypointArgs proto to type object."""
    if not proto:
      return None
    obj = MovePoseWaypointArgs()
    obj.acceleration = get_proto_value(proto.acceleration)
    obj.blend_radius = get_proto_value(proto.blend_radius)
    obj.limits = Limits.from_proto(get_proto_field(proto, 'limits'))
    obj.linear = get_proto_value(proto.linear)
    obj.rotation = Vec3d.from_proto(get_proto_field(proto, 'rotation'))
    obj.translation = Vec3d.from_proto(get_proto_field(proto, 'translation'))
    obj.velocity = get_proto_value(proto.velocity)
    return obj


class ObjectState:
  """Representation of proto message ObjectState.

   ObjectState is the list of object states in SIM for ML research.

  """
  # unique object identifier
  py_id: str

  # the name of the gameobject in the Unity scene
  object_name: str

  # the pose of the object
  pose_xyzxyzw: List[float]

  # the linear velocity of the object in each axis, in meters/second
  linear_vel: List[float]

  def __init__(self, linear_vel: Optional[List[float]] = None, object_name: str = '', pose_xyzxyzw: Optional[List[float]] = None, py_id: str = '') -> None:
    if linear_vel is None:
      self.linear_vel = []
    else:
      self.linear_vel = linear_vel
    self.object_name = object_name
    if pose_xyzxyzw is None:
      self.pose_xyzxyzw = []
    else:
      self.pose_xyzxyzw = pose_xyzxyzw
    self.py_id = py_id

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.linear_vel:
      assert isinstance(self.linear_vel, list), 'Wrong type for attribute: linear_vel. Expected: list. Got: ' + str(type(self.linear_vel)) + '.'
      json_data['linearVel'] = self.linear_vel

    if self.object_name:
      assert isinstance(self.object_name, str), 'Wrong type for attribute: object_name. Expected: str. Got: ' + str(type(self.object_name)) + '.'
      json_data['objectName'] = self.object_name

    if self.pose_xyzxyzw:
      assert isinstance(self.pose_xyzxyzw, list), 'Wrong type for attribute: pose_xyzxyzw. Expected: list. Got: ' + str(type(self.pose_xyzxyzw)) + '.'
      json_data['poseXYZXYZW'] = self.pose_xyzxyzw

    if self.py_id:
      assert isinstance(self.py_id, str), 'Wrong type for attribute: py_id. Expected: str. Got: ' + str(type(self.py_id)) + '.'
      json_data['id'] = self.py_id

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'ObjectState':
    """Convert JSON to type object."""
    obj = ObjectState()
    json_list: List[Any]

    expected_json_keys: List[str] = ['linearVel', 'objectName', 'poseXYZXYZW', 'id']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid ObjectState. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'linearVel' in json_data:
      assert isinstance(json_data['linearVel'], list), 'Wrong type for attribute: linearVel. Expected: list. Got: ' + str(type(json_data['linearVel'])) + '.'
      json_list = []
      for j in json_data['linearVel']:
        json_list.append(j)
      obj.linear_vel = json_list

    if 'objectName' in json_data:
      assert isinstance(json_data['objectName'], str), 'Wrong type for attribute: objectName. Expected: str. Got: ' + str(type(json_data['objectName'])) + '.'
      obj.object_name = json_data['objectName']

    if 'poseXYZXYZW' in json_data:
      assert isinstance(json_data['poseXYZXYZW'], list), 'Wrong type for attribute: poseXYZXYZW. Expected: list. Got: ' + str(type(json_data['poseXYZXYZW'])) + '.'
      json_list = []
      for j in json_data['poseXYZXYZW']:
        json_list.append(j)
      obj.pose_xyzxyzw = json_list

    if 'id' in json_data:
      assert isinstance(json_data['id'], str), 'Wrong type for attribute: id. Expected: str. Got: ' + str(type(json_data['id'])) + '.'
      obj.py_id = json_data['id']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.ObjectState) -> 'ObjectState':
    """Convert ObjectState proto to type object."""
    if not proto:
      return None
    obj = ObjectState()
    if proto.linear_vel:
      json_list = []
      for j in proto.linear_vel:
        json_list.append(j)
      obj.linear_vel = json_list
    obj.object_name = get_proto_value(proto.object_name)
    if proto.pose_xyzxyzw:
      json_list = []
      for j in proto.pose_xyzxyzw:
        json_list.append(j)
      obj.pose_xyzxyzw = json_list
    obj.py_id = get_proto_value(proto.id)
    return obj


class PickLabel:
  """Representation of proto message PickLabel.

   PickLabel contains fields associated with a pick.
   See the requirements at go/reach-ml-logging-requirements
  """
  label: str

  # The field depth_ts will be deprecated. Please use device_data_ref instead.
  depth_ts: int

  # device_data_ref contains the timestamp of an action being executed.
  device_data_ref: List['DeviceDataRef']

  # user_data_ref contains the timestamp of when an action got queued.
  user_data_ref: List['DeviceDataRef']

  # Pose2D will be a 1 item list from a Reach serve logs perspective.
  # More than one will typically be from crowdcompute.
  pose_2d: List['Pose2d']
  position_3d: List['Vec3d']
  quaternion_3d: List['Quaternion3d']
  task_code: str
  pick_id: str
  tags: List[str]
  intent: str

  success_type: str

  def __init__(self, depth_ts: int = 0, device_data_ref: Optional[List['DeviceDataRef']] = None, intent: str = '', label: str = '', pick_id: str = '', pose_2d: Optional[List['Pose2d']] = None, position_3d: Optional[List['Vec3d']] = None, quaternion_3d: Optional[List['Quaternion3d']] = None, success_type: str = '', tags: Optional[List[str]] = None, task_code: str = '', user_data_ref: Optional[List['DeviceDataRef']] = None) -> None:
    self.depth_ts = depth_ts
    if device_data_ref is None:
      self.device_data_ref = []
    else:
      self.device_data_ref = device_data_ref
    self.intent = intent
    self.label = label
    self.pick_id = pick_id
    if pose_2d is None:
      self.pose_2d = []
    else:
      self.pose_2d = pose_2d
    if position_3d is None:
      self.position_3d = []
    else:
      self.position_3d = position_3d
    if quaternion_3d is None:
      self.quaternion_3d = []
    else:
      self.quaternion_3d = quaternion_3d
    self.success_type = success_type
    if tags is None:
      self.tags = []
    else:
      self.tags = tags
    self.task_code = task_code
    if user_data_ref is None:
      self.user_data_ref = []
    else:
      self.user_data_ref = user_data_ref

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.depth_ts:
      assert isinstance(self.depth_ts, int), 'Wrong type for attribute: depth_ts. Expected: int. Got: ' + str(type(self.depth_ts)) + '.'
      json_data['depthTS'] = self.depth_ts

    if self.device_data_ref:
      assert isinstance(self.device_data_ref, list), 'Wrong type for attribute: device_data_ref. Expected: list. Got: ' + str(type(self.device_data_ref)) + '.'
      obj_list = []
      for item in self.device_data_ref:
        obj_list.append(item.to_json())
      json_data['deviceDataRef'] = obj_list

    if self.intent:
      assert isinstance(self.intent, str), 'Wrong type for attribute: intent. Expected: str. Got: ' + str(type(self.intent)) + '.'
      json_data['intent'] = self.intent

    if self.label:
      assert isinstance(self.label, str), 'Wrong type for attribute: label. Expected: str. Got: ' + str(type(self.label)) + '.'
      json_data['label'] = self.label

    if self.pick_id:
      assert isinstance(self.pick_id, str), 'Wrong type for attribute: pick_id. Expected: str. Got: ' + str(type(self.pick_id)) + '.'
      json_data['pickID'] = self.pick_id

    if self.pose_2d:
      assert isinstance(self.pose_2d, list), 'Wrong type for attribute: pose_2d. Expected: list. Got: ' + str(type(self.pose_2d)) + '.'
      obj_list = []
      for item in self.pose_2d:
        obj_list.append(item.to_json())
      json_data['pose2D'] = obj_list

    if self.position_3d:
      assert isinstance(self.position_3d, list), 'Wrong type for attribute: position_3d. Expected: list. Got: ' + str(type(self.position_3d)) + '.'
      obj_list = []
      for item in self.position_3d:
        obj_list.append(item.to_json())
      json_data['position3D'] = obj_list

    if self.quaternion_3d:
      assert isinstance(self.quaternion_3d, list), 'Wrong type for attribute: quaternion_3d. Expected: list. Got: ' + str(type(self.quaternion_3d)) + '.'
      obj_list = []
      for item in self.quaternion_3d:
        obj_list.append(item.to_json())
      json_data['quaternion3D'] = obj_list

    if self.success_type:
      assert isinstance(self.success_type, str), 'Wrong type for attribute: success_type. Expected: str. Got: ' + str(type(self.success_type)) + '.'
      json_data['successType'] = self.success_type

    if self.tags:
      assert isinstance(self.tags, list), 'Wrong type for attribute: tags. Expected: list. Got: ' + str(type(self.tags)) + '.'
      json_data['tags'] = self.tags

    if self.task_code:
      assert isinstance(self.task_code, str), 'Wrong type for attribute: task_code. Expected: str. Got: ' + str(type(self.task_code)) + '.'
      json_data['taskCode'] = self.task_code

    if self.user_data_ref:
      assert isinstance(self.user_data_ref, list), 'Wrong type for attribute: user_data_ref. Expected: list. Got: ' + str(type(self.user_data_ref)) + '.'
      obj_list = []
      for item in self.user_data_ref:
        obj_list.append(item.to_json())
      json_data['userDataRef'] = obj_list

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'PickLabel':
    """Convert JSON to type object."""
    obj = PickLabel()
    json_list: List[Any]

    expected_json_keys: List[str] = ['depthTS', 'deviceDataRef', 'intent', 'label', 'pickID', 'pose2D', 'position3D', 'quaternion3D', 'successType', 'tags', 'taskCode', 'userDataRef']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid PickLabel. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'depthTS' in json_data:
      assert isinstance(json_data['depthTS'], int), 'Wrong type for attribute: depthTS. Expected: int. Got: ' + str(type(json_data['depthTS'])) + '.'
      obj.depth_ts = json_data['depthTS']

    if 'deviceDataRef' in json_data:
      assert isinstance(json_data['deviceDataRef'], list), 'Wrong type for attribute: deviceDataRef. Expected: list. Got: ' + str(type(json_data['deviceDataRef'])) + '.'
      json_list = []
      for j in json_data['deviceDataRef']:
        json_list.append(DeviceDataRef.from_json(j))
      obj.device_data_ref = json_list

    if 'intent' in json_data:
      assert isinstance(json_data['intent'], str), 'Wrong type for attribute: intent. Expected: str. Got: ' + str(type(json_data['intent'])) + '.'
      obj.intent = json_data['intent']

    if 'label' in json_data:
      assert isinstance(json_data['label'], str), 'Wrong type for attribute: label. Expected: str. Got: ' + str(type(json_data['label'])) + '.'
      obj.label = json_data['label']

    if 'pickID' in json_data:
      assert isinstance(json_data['pickID'], str), 'Wrong type for attribute: pickID. Expected: str. Got: ' + str(type(json_data['pickID'])) + '.'
      obj.pick_id = json_data['pickID']

    if 'pose2D' in json_data:
      assert isinstance(json_data['pose2D'], list), 'Wrong type for attribute: pose2D. Expected: list. Got: ' + str(type(json_data['pose2D'])) + '.'
      json_list = []
      for j in json_data['pose2D']:
        json_list.append(Pose2d.from_json(j))
      obj.pose_2d = json_list

    if 'position3D' in json_data:
      assert isinstance(json_data['position3D'], list), 'Wrong type for attribute: position3D. Expected: list. Got: ' + str(type(json_data['position3D'])) + '.'
      json_list = []
      for j in json_data['position3D']:
        json_list.append(Vec3d.from_json(j))
      obj.position_3d = json_list

    if 'quaternion3D' in json_data:
      assert isinstance(json_data['quaternion3D'], list), 'Wrong type for attribute: quaternion3D. Expected: list. Got: ' + str(type(json_data['quaternion3D'])) + '.'
      json_list = []
      for j in json_data['quaternion3D']:
        json_list.append(Quaternion3d.from_json(j))
      obj.quaternion_3d = json_list

    if 'successType' in json_data:
      assert isinstance(json_data['successType'], str), 'Wrong type for attribute: successType. Expected: str. Got: ' + str(type(json_data['successType'])) + '.'
      obj.success_type = json_data['successType']

    if 'tags' in json_data:
      assert isinstance(json_data['tags'], list), 'Wrong type for attribute: tags. Expected: list. Got: ' + str(type(json_data['tags'])) + '.'
      json_list = []
      for j in json_data['tags']:
        json_list.append(j)
      obj.tags = json_list

    if 'taskCode' in json_data:
      assert isinstance(json_data['taskCode'], str), 'Wrong type for attribute: taskCode. Expected: str. Got: ' + str(type(json_data['taskCode'])) + '.'
      obj.task_code = json_data['taskCode']

    if 'userDataRef' in json_data:
      assert isinstance(json_data['userDataRef'], list), 'Wrong type for attribute: userDataRef. Expected: list. Got: ' + str(type(json_data['userDataRef'])) + '.'
      json_list = []
      for j in json_data['userDataRef']:
        json_list.append(DeviceDataRef.from_json(j))
      obj.user_data_ref = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.PickLabel) -> 'PickLabel':
    """Convert PickLabel proto to type object."""
    if not proto:
      return None
    obj = PickLabel()
    obj.depth_ts = get_proto_value(proto.depth_ts)
    if proto.device_data_ref:
      json_list = []
      for j in proto.device_data_ref:
        json_list.append(DeviceDataRef.from_proto(j))
      obj.device_data_ref = json_list
    obj.intent = get_proto_value(proto.intent)
    obj.label = get_proto_value(proto.label)
    obj.pick_id = get_proto_value(proto.pick_id)
    if proto.pose_2d:
      json_list = []
      for j in proto.pose_2d:
        json_list.append(Pose2d.from_proto(j))
      obj.pose_2d = json_list
    if proto.position_3d:
      json_list = []
      for j in proto.position_3d:
        json_list.append(Vec3d.from_proto(j))
      obj.position_3d = json_list
    if proto.quaternion_3d:
      json_list = []
      for j in proto.quaternion_3d:
        json_list.append(Quaternion3d.from_proto(j))
      obj.quaternion_3d = json_list
    obj.success_type = get_proto_value(proto.success_type)
    if proto.tags:
      json_list = []
      for j in proto.tags:
        json_list.append(j)
      obj.tags = json_list
    obj.task_code = get_proto_value(proto.task_code)
    if proto.user_data_ref:
      json_list = []
      for j in proto.user_data_ref:
        json_list.append(DeviceDataRef.from_proto(j))
      obj.user_data_ref = json_list
    return obj


class PickPoint:
  """Representation of proto message PickPoint.

   PickPoint is the message for a point that can contain any number of values.
  """
  x: float
  y: float

  def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
    self.x = x
    self.y = y

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.x:
      assert isinstance(self.x, float) or isinstance(self.x, int), 'Wrong type for attribute: x. Expected: float. Got: ' + str(type(self.x)) + '.'
      json_data['x'] = self.x

    if self.y:
      assert isinstance(self.y, float) or isinstance(self.y, int), 'Wrong type for attribute: y. Expected: float. Got: ' + str(type(self.y)) + '.'
      json_data['y'] = self.y

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'PickPoint':
    """Convert JSON to type object."""
    obj = PickPoint()

    expected_json_keys: List[str] = ['x', 'y']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid PickPoint. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'x' in json_data:
      assert isinstance(json_data['x'], float) or isinstance(json_data['x'], int), 'Wrong type for attribute: x. Expected: float. Got: ' + str(type(json_data['x'])) + '.'
      obj.x = json_data['x']

    if 'y' in json_data:
      assert isinstance(json_data['y'], float) or isinstance(json_data['y'], int), 'Wrong type for attribute: y. Expected: float. Got: ' + str(type(json_data['y'])) + '.'
      obj.y = json_data['y']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.PickPoint) -> 'PickPoint':
    """Convert PickPoint proto to type object."""
    if not proto:
      return None
    obj = PickPoint()
    obj.x = get_proto_value(proto.x)
    obj.y = get_proto_value(proto.y)
    return obj


class PipelineDescription:
  """Representation of proto message PipelineDescription.

   PipelineDescription is the description of state machines in the pipeline.
  """
  # The descriptions provided by the machines in the pipeline.
  descriptions: List['MachineDescription']

  def __init__(self, descriptions: Optional[List['MachineDescription']] = None) -> None:
    if descriptions is None:
      self.descriptions = []
    else:
      self.descriptions = descriptions

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.descriptions:
      assert isinstance(self.descriptions, list), 'Wrong type for attribute: descriptions. Expected: list. Got: ' + str(type(self.descriptions)) + '.'
      obj_list = []
      for item in self.descriptions:
        obj_list.append(item.to_json())
      json_data['descriptions'] = obj_list

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'PipelineDescription':
    """Convert JSON to type object."""
    obj = PipelineDescription()
    json_list: List[Any]

    expected_json_keys: List[str] = ['descriptions']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid PipelineDescription. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'descriptions' in json_data:
      assert isinstance(json_data['descriptions'], list), 'Wrong type for attribute: descriptions. Expected: list. Got: ' + str(type(json_data['descriptions'])) + '.'
      json_list = []
      for j in json_data['descriptions']:
        json_list.append(MachineDescription.from_json(j))
      obj.descriptions = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.PipelineDescription) -> 'PipelineDescription':
    """Convert PipelineDescription proto to type object."""
    if not proto:
      return None
    obj = PipelineDescription()
    if proto.descriptions:
      json_list = []
      for j in proto.descriptions:
        json_list.append(MachineDescription.from_proto(j))
      obj.descriptions = json_list
    return obj


class PlaceLabel:
  """Representation of proto message PlaceLabel.

   PlaceLabel contains fields associated with a place.
   Added to support future ML needs for pick and place tasks.
   See the requirements at go/reach-ml-logging-requirements
  """
  label: str
  pose_2d: List['Pose2d']
  position_3d: List['Vec3d']
  quaternion_3d: List['Quaternion3d']

  def __init__(self, label: str = '', pose_2d: Optional[List['Pose2d']] = None, position_3d: Optional[List['Vec3d']] = None, quaternion_3d: Optional[List['Quaternion3d']] = None) -> None:
    self.label = label
    if pose_2d is None:
      self.pose_2d = []
    else:
      self.pose_2d = pose_2d
    if position_3d is None:
      self.position_3d = []
    else:
      self.position_3d = position_3d
    if quaternion_3d is None:
      self.quaternion_3d = []
    else:
      self.quaternion_3d = quaternion_3d

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.label:
      assert isinstance(self.label, str), 'Wrong type for attribute: label. Expected: str. Got: ' + str(type(self.label)) + '.'
      json_data['label'] = self.label

    if self.pose_2d:
      assert isinstance(self.pose_2d, list), 'Wrong type for attribute: pose_2d. Expected: list. Got: ' + str(type(self.pose_2d)) + '.'
      obj_list = []
      for item in self.pose_2d:
        obj_list.append(item.to_json())
      json_data['pose2D'] = obj_list

    if self.position_3d:
      assert isinstance(self.position_3d, list), 'Wrong type for attribute: position_3d. Expected: list. Got: ' + str(type(self.position_3d)) + '.'
      obj_list = []
      for item in self.position_3d:
        obj_list.append(item.to_json())
      json_data['position3D'] = obj_list

    if self.quaternion_3d:
      assert isinstance(self.quaternion_3d, list), 'Wrong type for attribute: quaternion_3d. Expected: list. Got: ' + str(type(self.quaternion_3d)) + '.'
      obj_list = []
      for item in self.quaternion_3d:
        obj_list.append(item.to_json())
      json_data['quaternion3D'] = obj_list

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'PlaceLabel':
    """Convert JSON to type object."""
    obj = PlaceLabel()
    json_list: List[Any]

    expected_json_keys: List[str] = ['label', 'pose2D', 'position3D', 'quaternion3D']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid PlaceLabel. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'label' in json_data:
      assert isinstance(json_data['label'], str), 'Wrong type for attribute: label. Expected: str. Got: ' + str(type(json_data['label'])) + '.'
      obj.label = json_data['label']

    if 'pose2D' in json_data:
      assert isinstance(json_data['pose2D'], list), 'Wrong type for attribute: pose2D. Expected: list. Got: ' + str(type(json_data['pose2D'])) + '.'
      json_list = []
      for j in json_data['pose2D']:
        json_list.append(Pose2d.from_json(j))
      obj.pose_2d = json_list

    if 'position3D' in json_data:
      assert isinstance(json_data['position3D'], list), 'Wrong type for attribute: position3D. Expected: list. Got: ' + str(type(json_data['position3D'])) + '.'
      json_list = []
      for j in json_data['position3D']:
        json_list.append(Vec3d.from_json(j))
      obj.position_3d = json_list

    if 'quaternion3D' in json_data:
      assert isinstance(json_data['quaternion3D'], list), 'Wrong type for attribute: quaternion3D. Expected: list. Got: ' + str(type(json_data['quaternion3D'])) + '.'
      json_list = []
      for j in json_data['quaternion3D']:
        json_list.append(Quaternion3d.from_json(j))
      obj.quaternion_3d = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.PlaceLabel) -> 'PlaceLabel':
    """Convert PlaceLabel proto to type object."""
    if not proto:
      return None
    obj = PlaceLabel()
    obj.label = get_proto_value(proto.label)
    if proto.pose_2d:
      json_list = []
      for j in proto.pose_2d:
        json_list.append(Pose2d.from_proto(j))
      obj.pose_2d = json_list
    if proto.position_3d:
      json_list = []
      for j in proto.position_3d:
        json_list.append(Vec3d.from_proto(j))
      obj.position_3d = json_list
    if proto.quaternion_3d:
      json_list = []
      for j in proto.quaternion_3d:
        json_list.append(Quaternion3d.from_proto(j))
      obj.quaternion_3d = json_list
    return obj


class Pose2d:
  """Representation of proto message Pose2d.

   Pose2D contains an X,Y coordinate pair.
  """
  x: float
  y: float

  def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
    self.x = x
    self.y = y

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.x:
      assert isinstance(self.x, float) or isinstance(self.x, int), 'Wrong type for attribute: x. Expected: float. Got: ' + str(type(self.x)) + '.'
      json_data['x'] = self.x

    if self.y:
      assert isinstance(self.y, float) or isinstance(self.y, int), 'Wrong type for attribute: y. Expected: float. Got: ' + str(type(self.y)) + '.'
      json_data['y'] = self.y

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'Pose2d':
    """Convert JSON to type object."""
    obj = Pose2d()

    expected_json_keys: List[str] = ['x', 'y']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid Pose2d. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'x' in json_data:
      assert isinstance(json_data['x'], float) or isinstance(json_data['x'], int), 'Wrong type for attribute: x. Expected: float. Got: ' + str(type(json_data['x'])) + '.'
      obj.x = json_data['x']

    if 'y' in json_data:
      assert isinstance(json_data['y'], float) or isinstance(json_data['y'], int), 'Wrong type for attribute: y. Expected: float. Got: ' + str(type(json_data['y'])) + '.'
      obj.y = json_data['y']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.Pose2d) -> 'Pose2d':
    """Convert Pose2d proto to type object."""
    if not proto:
      return None
    obj = Pose2d()
    obj.x = get_proto_value(proto.x)
    obj.y = get_proto_value(proto.y)
    return obj


class Quaternion3d:
  """Representation of proto message Quaternion3d.

  """
  w: float
  x: float
  y: float
  z: float

  def __init__(self, w: float = 0.0, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
    self.w = w
    self.x = x
    self.y = y
    self.z = z

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.w:
      assert isinstance(self.w, float) or isinstance(self.w, int), 'Wrong type for attribute: w. Expected: float. Got: ' + str(type(self.w)) + '.'
      json_data['w'] = self.w

    if self.x:
      assert isinstance(self.x, float) or isinstance(self.x, int), 'Wrong type for attribute: x. Expected: float. Got: ' + str(type(self.x)) + '.'
      json_data['x'] = self.x

    if self.y:
      assert isinstance(self.y, float) or isinstance(self.y, int), 'Wrong type for attribute: y. Expected: float. Got: ' + str(type(self.y)) + '.'
      json_data['y'] = self.y

    if self.z:
      assert isinstance(self.z, float) or isinstance(self.z, int), 'Wrong type for attribute: z. Expected: float. Got: ' + str(type(self.z)) + '.'
      json_data['z'] = self.z

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'Quaternion3d':
    """Convert JSON to type object."""
    obj = Quaternion3d()

    expected_json_keys: List[str] = ['w', 'x', 'y', 'z']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid Quaternion3d. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'w' in json_data:
      assert isinstance(json_data['w'], float) or isinstance(json_data['w'], int), 'Wrong type for attribute: w. Expected: float. Got: ' + str(type(json_data['w'])) + '.'
      obj.w = json_data['w']

    if 'x' in json_data:
      assert isinstance(json_data['x'], float) or isinstance(json_data['x'], int), 'Wrong type for attribute: x. Expected: float. Got: ' + str(type(json_data['x'])) + '.'
      obj.x = json_data['x']

    if 'y' in json_data:
      assert isinstance(json_data['y'], float) or isinstance(json_data['y'], int), 'Wrong type for attribute: y. Expected: float. Got: ' + str(type(json_data['y'])) + '.'
      obj.y = json_data['y']

    if 'z' in json_data:
      assert isinstance(json_data['z'], float) or isinstance(json_data['z'], int), 'Wrong type for attribute: z. Expected: float. Got: ' + str(type(json_data['z'])) + '.'
      obj.z = json_data['z']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.Quaternion3d) -> 'Quaternion3d':
    """Convert Quaternion3d proto to type object."""
    if not proto:
      return None
    obj = Quaternion3d()
    obj.w = get_proto_value(proto.w)
    obj.x = get_proto_value(proto.x)
    obj.y = get_proto_value(proto.y)
    obj.z = get_proto_value(proto.z)
    return obj


class RawArgs:
  """Representation of proto message RawArgs.

   Sends the given text verbatim to the robot. Use this only when necessary. If
   you find yourself using this often, then consider asking to add the command
   formally to Reach Script.
  """
  text: str

  def __init__(self, text: str = '') -> None:
    self.text = text

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.text:
      assert isinstance(self.text, str), 'Wrong type for attribute: text. Expected: str. Got: ' + str(type(self.text)) + '.'
      json_data['text'] = self.text

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'RawArgs':
    """Convert JSON to type object."""
    obj = RawArgs()

    expected_json_keys: List[str] = ['text']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid RawArgs. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'text' in json_data:
      assert isinstance(json_data['text'], str), 'Wrong type for attribute: text. Expected: str. Got: ' + str(type(json_data['text'])) + '.'
      obj.text = json_data['text']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.RawArgs) -> 'RawArgs':
    """Convert RawArgs proto to type object."""
    if not proto:
      return None
    obj = RawArgs()
    obj.text = get_proto_value(proto.text)
    return obj


class ReachScript:
  """Representation of proto message ReachScript.

  """
  # If true, the command will stop any currently executing command and start
  # executing this one.
  preemptive: bool
  commands: List['ReachScriptCommand']

  # The minimum version of ReachScript this program requires the server to
  # implement. If the server cannot handle the given version, the program
  # will be rejected.
  version: int
  preemptive_reason: str

  # States if the command depends on calibration.
  # TODO: Jira VIS-274. Reject reach script without
  # calibration_requirement once all clients are updated to send it.
  calibration_requirement: Optional['ReachScriptCalibrationRequirement']

  def __init__(self, calibration_requirement: Optional['ReachScriptCalibrationRequirement'] = None, commands: Optional[List['ReachScriptCommand']] = None, preemptive: bool = False, preemptive_reason: str = '', version: int = 0) -> None:
    self.calibration_requirement = calibration_requirement
    if commands is None:
      self.commands = []
    else:
      self.commands = commands
    self.preemptive = preemptive
    self.preemptive_reason = preemptive_reason
    self.version = version

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.calibration_requirement:
      assert self.calibration_requirement.__class__.__name__ == 'ReachScriptCalibrationRequirement', 'Wrong type for attribute: calibration_requirement. Expected: ReachScriptCalibrationRequirement. Got: ' + str(type(self.calibration_requirement)) + '.'
      json_data['calibrationRequirement'] = self.calibration_requirement.to_json()

    if self.commands:
      assert isinstance(self.commands, list), 'Wrong type for attribute: commands. Expected: list. Got: ' + str(type(self.commands)) + '.'
      obj_list = []
      for item in self.commands:
        obj_list.append(item.to_json())
      json_data['commands'] = obj_list

    if self.preemptive:
      assert isinstance(self.preemptive, bool), 'Wrong type for attribute: preemptive. Expected: bool. Got: ' + str(type(self.preemptive)) + '.'
      json_data['preemptive'] = self.preemptive

    if self.preemptive_reason:
      assert isinstance(self.preemptive_reason, str), 'Wrong type for attribute: preemptive_reason. Expected: str. Got: ' + str(type(self.preemptive_reason)) + '.'
      json_data['preemptiveReason'] = self.preemptive_reason

    if self.version:
      assert isinstance(self.version, int), 'Wrong type for attribute: version. Expected: int. Got: ' + str(type(self.version)) + '.'
      json_data['version'] = self.version

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'ReachScript':
    """Convert JSON to type object."""
    obj = ReachScript()
    json_list: List[Any]

    expected_json_keys: List[str] = ['calibrationRequirement', 'commands', 'preemptive', 'preemptiveReason', 'version']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid ReachScript. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'calibrationRequirement' in json_data:
      assert isinstance(json_data['calibrationRequirement'], dict), 'Wrong type for attribute: calibrationRequirement. Expected: dict. Got: ' + str(type(json_data['calibrationRequirement'])) + '.'
      obj.calibration_requirement = ReachScriptCalibrationRequirement.from_json(json_data['calibrationRequirement'])

    if 'commands' in json_data:
      assert isinstance(json_data['commands'], list), 'Wrong type for attribute: commands. Expected: list. Got: ' + str(type(json_data['commands'])) + '.'
      json_list = []
      for j in json_data['commands']:
        json_list.append(ReachScriptCommand.from_json(j))
      obj.commands = json_list

    if 'preemptive' in json_data:
      assert isinstance(json_data['preemptive'], bool), 'Wrong type for attribute: preemptive. Expected: bool. Got: ' + str(type(json_data['preemptive'])) + '.'
      obj.preemptive = json_data['preemptive']

    if 'preemptiveReason' in json_data:
      assert isinstance(json_data['preemptiveReason'], str), 'Wrong type for attribute: preemptiveReason. Expected: str. Got: ' + str(type(json_data['preemptiveReason'])) + '.'
      obj.preemptive_reason = json_data['preemptiveReason']

    if 'version' in json_data:
      assert isinstance(json_data['version'], int), 'Wrong type for attribute: version. Expected: int. Got: ' + str(type(json_data['version'])) + '.'
      obj.version = json_data['version']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.ReachScript) -> 'ReachScript':
    """Convert ReachScript proto to type object."""
    if not proto:
      return None
    obj = ReachScript()
    obj.calibration_requirement = ReachScriptCalibrationRequirement.from_proto(get_proto_field(proto, 'calibration_requirement'))
    if proto.commands:
      json_list = []
      for j in proto.commands:
        json_list.append(ReachScriptCommand.from_proto(j))
      obj.commands = json_list
    obj.preemptive = get_proto_value(proto.preemptive)
    obj.preemptive_reason = get_proto_value(proto.preemptive_reason)
    obj.version = get_proto_value(proto.version)
    return obj


class ReachScriptBooleanExpression:
  """Representation of proto message ReachScriptBooleanExpression.

   ReachScriptBooleanExpression represents an expression evaluating
   to a boolean. All args must be of the same type. If they are not,
   the command will be rejected. For the 'not' operator, only
   the first arg may be present, and it must evaluate to a boolean.
  """
  # The operator to apply to the args. Must be one of:
  #   * eq
  #   * not
  #   * and
  #   * or
  #   * lt
  #   * gt
  #   * lte
  #   * gte
  # Any other string shall result in command rejection.
  op: str

  # The first argument.
  arg1: Optional['ReachScriptExpression']

  # The second argument. Must not be present for the 'not' operator.
  arg2: Optional['ReachScriptExpression']

  def __init__(self, arg1: Optional['ReachScriptExpression'] = None, arg2: Optional['ReachScriptExpression'] = None, op: str = '') -> None:
    self.arg1 = arg1
    self.arg2 = arg2
    self.op = op

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.arg1:
      assert self.arg1.__class__.__name__ == 'ReachScriptExpression', 'Wrong type for attribute: arg1. Expected: ReachScriptExpression. Got: ' + str(type(self.arg1)) + '.'
      json_data['arg1'] = self.arg1.to_json()

    if self.arg2:
      assert self.arg2.__class__.__name__ == 'ReachScriptExpression', 'Wrong type for attribute: arg2. Expected: ReachScriptExpression. Got: ' + str(type(self.arg2)) + '.'
      json_data['arg2'] = self.arg2.to_json()

    if self.op:
      assert isinstance(self.op, str), 'Wrong type for attribute: op. Expected: str. Got: ' + str(type(self.op)) + '.'
      json_data['op'] = self.op

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'ReachScriptBooleanExpression':
    """Convert JSON to type object."""
    obj = ReachScriptBooleanExpression()

    expected_json_keys: List[str] = ['arg1', 'arg2', 'op']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid ReachScriptBooleanExpression. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'arg1' in json_data:
      assert isinstance(json_data['arg1'], dict), 'Wrong type for attribute: arg1. Expected: dict. Got: ' + str(type(json_data['arg1'])) + '.'
      obj.arg1 = ReachScriptExpression.from_json(json_data['arg1'])

    if 'arg2' in json_data:
      assert isinstance(json_data['arg2'], dict), 'Wrong type for attribute: arg2. Expected: dict. Got: ' + str(type(json_data['arg2'])) + '.'
      obj.arg2 = ReachScriptExpression.from_json(json_data['arg2'])

    if 'op' in json_data:
      assert isinstance(json_data['op'], str), 'Wrong type for attribute: op. Expected: str. Got: ' + str(type(json_data['op'])) + '.'
      obj.op = json_data['op']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.ReachScriptBooleanExpression) -> 'ReachScriptBooleanExpression':
    """Convert ReachScriptBooleanExpression proto to type object."""
    if not proto:
      return None
    obj = ReachScriptBooleanExpression()
    obj.arg1 = ReachScriptExpression.from_proto(get_proto_field(proto, 'arg1'))
    obj.arg2 = ReachScriptExpression.from_proto(get_proto_field(proto, 'arg2'))
    obj.op = get_proto_value(proto.op)
    return obj


class ReachScriptCalibrationRequirement:
  """Representation of proto message ReachScriptCalibrationRequirement.

   ReachScriptCalibrationRequirement states if the requested movement is
   dependent on having a good calibration, i.e. when there was no detected
   camera movement that crossed internal thresholds.
  """
  # States if the command should be allowed without good calibration.
  allow_uncalibrated: bool

  def __init__(self, allow_uncalibrated: bool = False) -> None:
    self.allow_uncalibrated = allow_uncalibrated

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.allow_uncalibrated:
      assert isinstance(self.allow_uncalibrated, bool), 'Wrong type for attribute: allow_uncalibrated. Expected: bool. Got: ' + str(type(self.allow_uncalibrated)) + '.'
      json_data['allowUncalibrated'] = self.allow_uncalibrated

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'ReachScriptCalibrationRequirement':
    """Convert JSON to type object."""
    obj = ReachScriptCalibrationRequirement()

    expected_json_keys: List[str] = ['allowUncalibrated']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid ReachScriptCalibrationRequirement. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'allowUncalibrated' in json_data:
      assert isinstance(json_data['allowUncalibrated'], bool), 'Wrong type for attribute: allowUncalibrated. Expected: bool. Got: ' + str(type(json_data['allowUncalibrated'])) + '.'
      obj.allow_uncalibrated = json_data['allowUncalibrated']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.ReachScriptCalibrationRequirement) -> 'ReachScriptCalibrationRequirement':
    """Convert ReachScriptCalibrationRequirement proto to type object."""
    if not proto:
      return None
    obj = ReachScriptCalibrationRequirement()
    obj.allow_uncalibrated = get_proto_value(proto.allow_uncalibrated)
    return obj


class ReachScriptCapability:
  """Representation of proto message ReachScriptCapability.

   ReachScriptCapability is a specification for a capability,
   with optional state, for a ReachScriptExpression or
   command.
  """
  # The type of the capability from the workcell I/O config.
  py_type: str

  # The name of the capability from the workcell I/O config.
  name: str

  # The states of all pins in the capability.
  state: List['CapabilityState']

  def __init__(self, name: str = '', py_type: str = '', state: Optional[List['CapabilityState']] = None) -> None:
    self.name = name
    self.py_type = py_type
    if state is None:
      self.state = []
    else:
      self.state = state

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.name:
      assert isinstance(self.name, str), 'Wrong type for attribute: name. Expected: str. Got: ' + str(type(self.name)) + '.'
      json_data['name'] = self.name

    if self.py_type:
      assert isinstance(self.py_type, str), 'Wrong type for attribute: py_type. Expected: str. Got: ' + str(type(self.py_type)) + '.'
      json_data['type'] = self.py_type

    if self.state:
      assert isinstance(self.state, list), 'Wrong type for attribute: state. Expected: list. Got: ' + str(type(self.state)) + '.'
      obj_list = []
      for item in self.state:
        obj_list.append(item.to_json())
      json_data['state'] = obj_list

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'ReachScriptCapability':
    """Convert JSON to type object."""
    obj = ReachScriptCapability()
    json_list: List[Any]

    expected_json_keys: List[str] = ['name', 'type', 'state']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid ReachScriptCapability. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'name' in json_data:
      assert isinstance(json_data['name'], str), 'Wrong type for attribute: name. Expected: str. Got: ' + str(type(json_data['name'])) + '.'
      obj.name = json_data['name']

    if 'type' in json_data:
      assert isinstance(json_data['type'], str), 'Wrong type for attribute: type. Expected: str. Got: ' + str(type(json_data['type'])) + '.'
      obj.py_type = json_data['type']

    if 'state' in json_data:
      assert isinstance(json_data['state'], list), 'Wrong type for attribute: state. Expected: list. Got: ' + str(type(json_data['state'])) + '.'
      json_list = []
      for j in json_data['state']:
        json_list.append(CapabilityState.from_json(j))
      obj.state = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.ReachScriptCapability) -> 'ReachScriptCapability':
    """Convert ReachScriptCapability proto to type object."""
    if not proto:
      return None
    obj = ReachScriptCapability()
    obj.name = get_proto_value(proto.name)
    obj.py_type = get_proto_value(proto.type)
    if proto.state:
      json_list = []
      for j in proto.state:
        json_list.append(CapabilityState.from_proto(j))
      obj.state = json_list
    return obj


class ReachScriptCommand:
  """Representation of proto message ReachScriptCommand.

   Each command should contain one of these. If there are zero, then nothing
   happens. If there are more than one, then the result is undefined behavior.
   In general, it will result in one and only one of the commands being
   executed.
  """
  set_radial_speed: Optional['SetRadialSpeedArgs']
  set_blend_radius: Optional['SetBlendRadiusArgs']
  move_j_path: Optional['MoveJPathArgs']
  move_l_path: Optional['MoveLPathArgs']
  stop_j: Optional['StopJArgs']
  set_digital_out: Optional['SetDigitalOutArgs']
  set_analog_out: Optional['SetAnalogOutArgs']
  set_tool_digital_out: Optional['SetDigitalOutArgs']
  sleep: Optional['SleepArgs']
  raw: Optional['RawArgs']
  acquire_image: Optional['AcquireImageArgs']
  set_output: Optional['SetOutput']

  sync: Optional['SyncArgs']

  move_pose_path: Optional['MovePosePathArgs']

  wait: Optional['WaitArgs']

  def __init__(self, acquire_image: Optional['AcquireImageArgs'] = None, move_j_path: Optional['MoveJPathArgs'] = None, move_l_path: Optional['MoveLPathArgs'] = None, move_pose_path: Optional['MovePosePathArgs'] = None, raw: Optional['RawArgs'] = None, set_analog_out: Optional['SetAnalogOutArgs'] = None, set_blend_radius: Optional['SetBlendRadiusArgs'] = None, set_digital_out: Optional['SetDigitalOutArgs'] = None, set_output: Optional['SetOutput'] = None, set_radial_speed: Optional['SetRadialSpeedArgs'] = None, set_tool_digital_out: Optional['SetDigitalOutArgs'] = None, sleep: Optional['SleepArgs'] = None, stop_j: Optional['StopJArgs'] = None, sync: Optional['SyncArgs'] = None, wait: Optional['WaitArgs'] = None) -> None:
    self.acquire_image = acquire_image
    self.move_j_path = move_j_path
    self.move_l_path = move_l_path
    self.move_pose_path = move_pose_path
    self.raw = raw
    self.set_analog_out = set_analog_out
    self.set_blend_radius = set_blend_radius
    self.set_digital_out = set_digital_out
    self.set_output = set_output
    self.set_radial_speed = set_radial_speed
    self.set_tool_digital_out = set_tool_digital_out
    self.sleep = sleep
    self.stop_j = stop_j
    self.sync = sync
    self.wait = wait

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.acquire_image:
      assert self.acquire_image.__class__.__name__ == 'AcquireImageArgs', 'Wrong type for attribute: acquire_image. Expected: AcquireImageArgs. Got: ' + str(type(self.acquire_image)) + '.'
      json_data['acquireImage'] = self.acquire_image.to_json()

    if self.move_j_path:
      assert self.move_j_path.__class__.__name__ == 'MoveJPathArgs', 'Wrong type for attribute: move_j_path. Expected: MoveJPathArgs. Got: ' + str(type(self.move_j_path)) + '.'
      json_data['movejPath'] = self.move_j_path.to_json()

    if self.move_l_path:
      assert self.move_l_path.__class__.__name__ == 'MoveLPathArgs', 'Wrong type for attribute: move_l_path. Expected: MoveLPathArgs. Got: ' + str(type(self.move_l_path)) + '.'
      json_data['movelPath'] = self.move_l_path.to_json()

    if self.move_pose_path:
      assert self.move_pose_path.__class__.__name__ == 'MovePosePathArgs', 'Wrong type for attribute: move_pose_path. Expected: MovePosePathArgs. Got: ' + str(type(self.move_pose_path)) + '.'
      json_data['movePosePath'] = self.move_pose_path.to_json()

    if self.raw:
      assert self.raw.__class__.__name__ == 'RawArgs', 'Wrong type for attribute: raw. Expected: RawArgs. Got: ' + str(type(self.raw)) + '.'
      json_data['raw'] = self.raw.to_json()

    if self.set_analog_out:
      assert self.set_analog_out.__class__.__name__ == 'SetAnalogOutArgs', 'Wrong type for attribute: set_analog_out. Expected: SetAnalogOutArgs. Got: ' + str(type(self.set_analog_out)) + '.'
      json_data['setAnalogOut'] = self.set_analog_out.to_json()

    if self.set_blend_radius:
      assert self.set_blend_radius.__class__.__name__ == 'SetBlendRadiusArgs', 'Wrong type for attribute: set_blend_radius. Expected: SetBlendRadiusArgs. Got: ' + str(type(self.set_blend_radius)) + '.'
      json_data['setBlendRadius'] = self.set_blend_radius.to_json()

    if self.set_digital_out:
      assert self.set_digital_out.__class__.__name__ == 'SetDigitalOutArgs', 'Wrong type for attribute: set_digital_out. Expected: SetDigitalOutArgs. Got: ' + str(type(self.set_digital_out)) + '.'
      json_data['setDigitalOut'] = self.set_digital_out.to_json()

    if self.set_output:
      assert self.set_output.__class__.__name__ == 'SetOutput', 'Wrong type for attribute: set_output. Expected: SetOutput. Got: ' + str(type(self.set_output)) + '.'
      json_data['setOutput'] = self.set_output.to_json()

    if self.set_radial_speed:
      assert self.set_radial_speed.__class__.__name__ == 'SetRadialSpeedArgs', 'Wrong type for attribute: set_radial_speed. Expected: SetRadialSpeedArgs. Got: ' + str(type(self.set_radial_speed)) + '.'
      json_data['setRadialSpeed'] = self.set_radial_speed.to_json()

    if self.set_tool_digital_out:
      assert self.set_tool_digital_out.__class__.__name__ == 'SetDigitalOutArgs', 'Wrong type for attribute: set_tool_digital_out. Expected: SetDigitalOutArgs. Got: ' + str(type(self.set_tool_digital_out)) + '.'
      json_data['setToolDigitalOut'] = self.set_tool_digital_out.to_json()

    if self.sleep:
      assert self.sleep.__class__.__name__ == 'SleepArgs', 'Wrong type for attribute: sleep. Expected: SleepArgs. Got: ' + str(type(self.sleep)) + '.'
      json_data['sleep'] = self.sleep.to_json()

    if self.stop_j:
      assert self.stop_j.__class__.__name__ == 'StopJArgs', 'Wrong type for attribute: stop_j. Expected: StopJArgs. Got: ' + str(type(self.stop_j)) + '.'
      json_data['stopJ'] = self.stop_j.to_json()

    if self.sync:
      assert self.sync.__class__.__name__ == 'SyncArgs', 'Wrong type for attribute: sync. Expected: SyncArgs. Got: ' + str(type(self.sync)) + '.'
      json_data['sync'] = self.sync.to_json()

    if self.wait:
      assert self.wait.__class__.__name__ == 'WaitArgs', 'Wrong type for attribute: wait. Expected: WaitArgs. Got: ' + str(type(self.wait)) + '.'
      json_data['wait'] = self.wait.to_json()

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'ReachScriptCommand':
    """Convert JSON to type object."""
    obj = ReachScriptCommand()

    expected_json_keys: List[str] = ['acquireImage', 'movejPath', 'movelPath', 'movePosePath', 'raw', 'setAnalogOut', 'setBlendRadius', 'setDigitalOut', 'setOutput', 'setRadialSpeed', 'setToolDigitalOut', 'sleep', 'stopJ', 'sync', 'wait']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid ReachScriptCommand. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'acquireImage' in json_data:
      assert isinstance(json_data['acquireImage'], dict), 'Wrong type for attribute: acquireImage. Expected: dict. Got: ' + str(type(json_data['acquireImage'])) + '.'
      obj.acquire_image = AcquireImageArgs.from_json(json_data['acquireImage'])

    if 'movejPath' in json_data:
      assert isinstance(json_data['movejPath'], dict), 'Wrong type for attribute: movejPath. Expected: dict. Got: ' + str(type(json_data['movejPath'])) + '.'
      obj.move_j_path = MoveJPathArgs.from_json(json_data['movejPath'])

    if 'movelPath' in json_data:
      assert isinstance(json_data['movelPath'], dict), 'Wrong type for attribute: movelPath. Expected: dict. Got: ' + str(type(json_data['movelPath'])) + '.'
      obj.move_l_path = MoveLPathArgs.from_json(json_data['movelPath'])

    if 'movePosePath' in json_data:
      assert isinstance(json_data['movePosePath'], dict), 'Wrong type for attribute: movePosePath. Expected: dict. Got: ' + str(type(json_data['movePosePath'])) + '.'
      obj.move_pose_path = MovePosePathArgs.from_json(json_data['movePosePath'])

    if 'raw' in json_data:
      assert isinstance(json_data['raw'], dict), 'Wrong type for attribute: raw. Expected: dict. Got: ' + str(type(json_data['raw'])) + '.'
      obj.raw = RawArgs.from_json(json_data['raw'])

    if 'setAnalogOut' in json_data:
      assert isinstance(json_data['setAnalogOut'], dict), 'Wrong type for attribute: setAnalogOut. Expected: dict. Got: ' + str(type(json_data['setAnalogOut'])) + '.'
      obj.set_analog_out = SetAnalogOutArgs.from_json(json_data['setAnalogOut'])

    if 'setBlendRadius' in json_data:
      assert isinstance(json_data['setBlendRadius'], dict), 'Wrong type for attribute: setBlendRadius. Expected: dict. Got: ' + str(type(json_data['setBlendRadius'])) + '.'
      obj.set_blend_radius = SetBlendRadiusArgs.from_json(json_data['setBlendRadius'])

    if 'setDigitalOut' in json_data:
      assert isinstance(json_data['setDigitalOut'], dict), 'Wrong type for attribute: setDigitalOut. Expected: dict. Got: ' + str(type(json_data['setDigitalOut'])) + '.'
      obj.set_digital_out = SetDigitalOutArgs.from_json(json_data['setDigitalOut'])

    if 'setOutput' in json_data:
      assert isinstance(json_data['setOutput'], dict), 'Wrong type for attribute: setOutput. Expected: dict. Got: ' + str(type(json_data['setOutput'])) + '.'
      obj.set_output = SetOutput.from_json(json_data['setOutput'])

    if 'setRadialSpeed' in json_data:
      assert isinstance(json_data['setRadialSpeed'], dict), 'Wrong type for attribute: setRadialSpeed. Expected: dict. Got: ' + str(type(json_data['setRadialSpeed'])) + '.'
      obj.set_radial_speed = SetRadialSpeedArgs.from_json(json_data['setRadialSpeed'])

    if 'setToolDigitalOut' in json_data:
      assert isinstance(json_data['setToolDigitalOut'], dict), 'Wrong type for attribute: setToolDigitalOut. Expected: dict. Got: ' + str(type(json_data['setToolDigitalOut'])) + '.'
      obj.set_tool_digital_out = SetDigitalOutArgs.from_json(json_data['setToolDigitalOut'])

    if 'sleep' in json_data:
      assert isinstance(json_data['sleep'], dict), 'Wrong type for attribute: sleep. Expected: dict. Got: ' + str(type(json_data['sleep'])) + '.'
      obj.sleep = SleepArgs.from_json(json_data['sleep'])

    if 'stopJ' in json_data:
      assert isinstance(json_data['stopJ'], dict), 'Wrong type for attribute: stopJ. Expected: dict. Got: ' + str(type(json_data['stopJ'])) + '.'
      obj.stop_j = StopJArgs.from_json(json_data['stopJ'])

    if 'sync' in json_data:
      assert isinstance(json_data['sync'], dict), 'Wrong type for attribute: sync. Expected: dict. Got: ' + str(type(json_data['sync'])) + '.'
      obj.sync = SyncArgs.from_json(json_data['sync'])

    if 'wait' in json_data:
      assert isinstance(json_data['wait'], dict), 'Wrong type for attribute: wait. Expected: dict. Got: ' + str(type(json_data['wait'])) + '.'
      obj.wait = WaitArgs.from_json(json_data['wait'])

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.ReachScriptCommand) -> 'ReachScriptCommand':
    """Convert ReachScriptCommand proto to type object."""
    if not proto:
      return None
    obj = ReachScriptCommand()
    obj.acquire_image = AcquireImageArgs.from_proto(get_proto_field(proto, 'acquire_image'))
    obj.move_j_path = MoveJPathArgs.from_proto(get_proto_field(proto, 'move_j_path'))
    obj.move_l_path = MoveLPathArgs.from_proto(get_proto_field(proto, 'move_l_path'))
    obj.move_pose_path = MovePosePathArgs.from_proto(get_proto_field(proto, 'move_pose_path'))
    obj.raw = RawArgs.from_proto(get_proto_field(proto, 'raw'))
    obj.set_analog_out = SetAnalogOutArgs.from_proto(get_proto_field(proto, 'set_analog_out'))
    obj.set_blend_radius = SetBlendRadiusArgs.from_proto(get_proto_field(proto, 'set_blend_radius'))
    obj.set_digital_out = SetDigitalOutArgs.from_proto(get_proto_field(proto, 'set_digital_out'))
    obj.set_output = SetOutput.from_proto(get_proto_field(proto, 'set_output'))
    obj.set_radial_speed = SetRadialSpeedArgs.from_proto(get_proto_field(proto, 'set_radial_speed'))
    obj.set_tool_digital_out = SetDigitalOutArgs.from_proto(get_proto_field(proto, 'set_tool_digital_out'))
    obj.sleep = SleepArgs.from_proto(get_proto_field(proto, 'sleep'))
    obj.stop_j = StopJArgs.from_proto(get_proto_field(proto, 'stop_j'))
    obj.sync = SyncArgs.from_proto(get_proto_field(proto, 'sync'))
    obj.wait = WaitArgs.from_proto(get_proto_field(proto, 'wait'))
    return obj


class ReachScriptConst:
  """Representation of proto message ReachScriptConst.

   ReachScriptConst is a constant that can be used in a
   ReachScriptExpression.
  """
  # The value of all pins in a capability.
  capability: Optional['ReachScriptCapability']
  bool_value: bool

  def __init__(self, bool_value: bool = False, capability: Optional['ReachScriptCapability'] = None) -> None:
    self.bool_value = bool_value
    self.capability = capability

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.bool_value:
      assert isinstance(self.bool_value, bool), 'Wrong type for attribute: bool_value. Expected: bool. Got: ' + str(type(self.bool_value)) + '.'
      json_data['boolValue'] = self.bool_value

    if self.capability:
      assert self.capability.__class__.__name__ == 'ReachScriptCapability', 'Wrong type for attribute: capability. Expected: ReachScriptCapability. Got: ' + str(type(self.capability)) + '.'
      json_data['capability'] = self.capability.to_json()

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'ReachScriptConst':
    """Convert JSON to type object."""
    obj = ReachScriptConst()

    expected_json_keys: List[str] = ['boolValue', 'capability']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid ReachScriptConst. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'boolValue' in json_data:
      assert isinstance(json_data['boolValue'], bool), 'Wrong type for attribute: boolValue. Expected: bool. Got: ' + str(type(json_data['boolValue'])) + '.'
      obj.bool_value = json_data['boolValue']

    if 'capability' in json_data:
      assert isinstance(json_data['capability'], dict), 'Wrong type for attribute: capability. Expected: dict. Got: ' + str(type(json_data['capability'])) + '.'
      obj.capability = ReachScriptCapability.from_json(json_data['capability'])

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.ReachScriptConst) -> 'ReachScriptConst':
    """Convert ReachScriptConst proto to type object."""
    if not proto:
      return None
    obj = ReachScriptConst()
    obj.bool_value = get_proto_value(proto.bool_value)
    obj.capability = ReachScriptCapability.from_proto(get_proto_field(proto, 'capability'))
    return obj


class ReachScriptExpression:
  """Representation of proto message ReachScriptExpression.

   ReachScriptExpression is a boolean expression, variable,
   or constant used in a ReachScript command.
  """
  # A boolean expression.
  bool_expr: Optional['ReachScriptBooleanExpression']

  # An evaluated value of a variable.
  var_expr: Optional['ReachScriptVar']

  # A constant.
  const_expr: Optional['ReachScriptConst']

  def __init__(self, bool_expr: Optional['ReachScriptBooleanExpression'] = None, const_expr: Optional['ReachScriptConst'] = None, var_expr: Optional['ReachScriptVar'] = None) -> None:
    self.bool_expr = bool_expr
    self.const_expr = const_expr
    self.var_expr = var_expr

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.bool_expr:
      assert self.bool_expr.__class__.__name__ == 'ReachScriptBooleanExpression', 'Wrong type for attribute: bool_expr. Expected: ReachScriptBooleanExpression. Got: ' + str(type(self.bool_expr)) + '.'
      json_data['boolExpr'] = self.bool_expr.to_json()

    if self.const_expr:
      assert self.const_expr.__class__.__name__ == 'ReachScriptConst', 'Wrong type for attribute: const_expr. Expected: ReachScriptConst. Got: ' + str(type(self.const_expr)) + '.'
      json_data['constExpr'] = self.const_expr.to_json()

    if self.var_expr:
      assert self.var_expr.__class__.__name__ == 'ReachScriptVar', 'Wrong type for attribute: var_expr. Expected: ReachScriptVar. Got: ' + str(type(self.var_expr)) + '.'
      json_data['varExpr'] = self.var_expr.to_json()

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'ReachScriptExpression':
    """Convert JSON to type object."""
    obj = ReachScriptExpression()

    expected_json_keys: List[str] = ['boolExpr', 'constExpr', 'varExpr']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid ReachScriptExpression. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'boolExpr' in json_data:
      assert isinstance(json_data['boolExpr'], dict), 'Wrong type for attribute: boolExpr. Expected: dict. Got: ' + str(type(json_data['boolExpr'])) + '.'
      obj.bool_expr = ReachScriptBooleanExpression.from_json(json_data['boolExpr'])

    if 'constExpr' in json_data:
      assert isinstance(json_data['constExpr'], dict), 'Wrong type for attribute: constExpr. Expected: dict. Got: ' + str(type(json_data['constExpr'])) + '.'
      obj.const_expr = ReachScriptConst.from_json(json_data['constExpr'])

    if 'varExpr' in json_data:
      assert isinstance(json_data['varExpr'], dict), 'Wrong type for attribute: varExpr. Expected: dict. Got: ' + str(type(json_data['varExpr'])) + '.'
      obj.var_expr = ReachScriptVar.from_json(json_data['varExpr'])

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.ReachScriptExpression) -> 'ReachScriptExpression':
    """Convert ReachScriptExpression proto to type object."""
    if not proto:
      return None
    obj = ReachScriptExpression()
    obj.bool_expr = ReachScriptBooleanExpression.from_proto(get_proto_field(proto, 'bool_expr'))
    obj.const_expr = ReachScriptConst.from_proto(get_proto_field(proto, 'const_expr'))
    obj.var_expr = ReachScriptVar.from_proto(get_proto_field(proto, 'var_expr'))
    return obj


class ReachScriptVar:
  """Representation of proto message ReachScriptVar.

   ReachScriptVar is a variable that can be used in a
   ReachScriptExpression.
  """
  # The value of a capability. For variables, don't specify
  # any pins (CapabilityStates).
  capability: Optional['ReachScriptCapability']

  def __init__(self, capability: Optional['ReachScriptCapability'] = None) -> None:
    self.capability = capability

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.capability:
      assert self.capability.__class__.__name__ == 'ReachScriptCapability', 'Wrong type for attribute: capability. Expected: ReachScriptCapability. Got: ' + str(type(self.capability)) + '.'
      json_data['capability'] = self.capability.to_json()

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'ReachScriptVar':
    """Convert JSON to type object."""
    obj = ReachScriptVar()

    expected_json_keys: List[str] = ['capability']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid ReachScriptVar. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'capability' in json_data:
      assert isinstance(json_data['capability'], dict), 'Wrong type for attribute: capability. Expected: dict. Got: ' + str(type(json_data['capability'])) + '.'
      obj.capability = ReachScriptCapability.from_json(json_data['capability'])

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.ReachScriptVar) -> 'ReachScriptVar':
    """Convert ReachScriptVar proto to type object."""
    if not proto:
      return None
    obj = ReachScriptVar()
    obj.capability = ReachScriptCapability.from_proto(get_proto_field(proto, 'capability'))
    return obj


class ReportError:
  """Representation of proto message ReportError.

   ReportError for "report-error" messages. See design doc:
  """
  error: str
  tags: List[str]

  def __init__(self, error: str = '', tags: Optional[List[str]] = None) -> None:
    self.error = error
    if tags is None:
      self.tags = []
    else:
      self.tags = tags

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.error:
      assert isinstance(self.error, str), 'Wrong type for attribute: error. Expected: str. Got: ' + str(type(self.error)) + '.'
      json_data['error'] = self.error

    if self.tags:
      assert isinstance(self.tags, list), 'Wrong type for attribute: tags. Expected: list. Got: ' + str(type(self.tags)) + '.'
      json_data['tags'] = self.tags

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'ReportError':
    """Convert JSON to type object."""
    obj = ReportError()
    json_list: List[Any]

    expected_json_keys: List[str] = ['error', 'tags']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid ReportError. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'error' in json_data:
      assert isinstance(json_data['error'], str), 'Wrong type for attribute: error. Expected: str. Got: ' + str(type(json_data['error'])) + '.'
      obj.error = json_data['error']

    if 'tags' in json_data:
      assert isinstance(json_data['tags'], list), 'Wrong type for attribute: tags. Expected: list. Got: ' + str(type(json_data['tags'])) + '.'
      json_list = []
      for j in json_data['tags']:
        json_list.append(j)
      obj.tags = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.ReportError) -> 'ReportError':
    """Convert ReportError proto to type object."""
    if not proto:
      return None
    obj = ReportError()
    obj.error = get_proto_value(proto.error)
    if proto.tags:
      json_list = []
      for j in proto.tags:
        json_list.append(j)
      obj.tags = json_list
    return obj


class RobotPowerState:
  """Representation of proto message RobotPowerState.

  """
  is_robot_power_on: bool

  def __init__(self, is_robot_power_on: bool = False) -> None:
    self.is_robot_power_on = is_robot_power_on

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.is_robot_power_on:
      assert isinstance(self.is_robot_power_on, bool), 'Wrong type for attribute: is_robot_power_on. Expected: bool. Got: ' + str(type(self.is_robot_power_on)) + '.'
      json_data['isRobotPowerOn'] = self.is_robot_power_on

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'RobotPowerState':
    """Convert JSON to type object."""
    obj = RobotPowerState()

    expected_json_keys: List[str] = ['isRobotPowerOn']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid RobotPowerState. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'isRobotPowerOn' in json_data:
      assert isinstance(json_data['isRobotPowerOn'], bool), 'Wrong type for attribute: isRobotPowerOn. Expected: bool. Got: ' + str(type(json_data['isRobotPowerOn'])) + '.'
      obj.is_robot_power_on = json_data['isRobotPowerOn']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.RobotPowerState) -> 'RobotPowerState':
    """Convert RobotPowerState proto to type object."""
    if not proto:
      return None
    obj = RobotPowerState()
    obj.is_robot_power_on = get_proto_value(proto.is_robot_power_on)
    return obj


class RobotState:
  """Representation of proto message RobotState.

   RobotState is the message for the state of a robot,
   dataType == "robot-state".
  """
  # Robot pose, 6 numbers: x, y, z, rx, ry, rz.
  pose: List[float]

  # Joints positions in radians.
  joints: List[float]

  # Forces reported by robot. There is no standard for this field; it is
  # robot-specific.
  force: List[float]

  # Torques reported by robot. There is no standard for this field; it is
  # robot-specific.
  torque: List[float]
  robot_dexterity: float

  # Is the robot turned on.
  is_robot_power_on: bool
  is_emergency_stopped: bool
  is_protective_stopped: bool
  is_safeguard_stopped: bool
  is_reduced_mode: bool
  safety_message: str
  is_program_running: bool

  # Digital inputs.
  digital_in: List[bool]
  sensor_in: List[bool]

  # Digital outputs.
  digital_out: List[bool]

  # Analog inputs.
  analog_in: List[float]
  analog_out: List[float]
  tool_digital_in: List[bool]
  tool_digital_out: List[bool]
  tool_analog_in: List[float]
  tool_analog_out: List[float]
  board_temp_c: float
  robot_voltage_v: float
  robot_current_a: float
  board_io_current_a: float
  tool_temp_c: float
  tool_voltage_v: float
  tool_current_a: float
  joint_voltages_v: List[float]
  joint_currents_a: List[float]
  joint_temps_c: List[float]

  # One of {"", "remote", "local"}
  robot_mode: str

  # ProgramCounter is the number of executed programs.
  # It only gets incremented after a program finished running.
  program_counter: int

  # I/O states for digital pins. When present, overrides digital_in,
  # sensor_in, digital_out, tool_digital_in, and tool_digital_out.
  digital_bank: List['DigitalBank']

  # I/O states for analog pins. When present, overrides analog_in, analog_out,
  # tool_analog_in, and tool_analog_out.
  analog_bank: List['AnalogBank']

  # I/O states for integer pins.
  integer_bank: List['IntegerBank']

  # Tag of last terminated (aborted or done) program.
  last_terminated_program: str

  def __init__(self, analog_bank: Optional[List['AnalogBank']] = None, analog_in: Optional[List[float]] = None, analog_out: Optional[List[float]] = None, board_io_current_a: float = 0.0, board_temp_c: float = 0.0, digital_bank: Optional[List['DigitalBank']] = None, digital_in: Optional[List[bool]] = None, digital_out: Optional[List[bool]] = None, force: Optional[List[float]] = None, integer_bank: Optional[List['IntegerBank']] = None, is_emergency_stopped: bool = False, is_program_running: bool = False, is_protective_stopped: bool = False, is_reduced_mode: bool = False, is_robot_power_on: bool = False, is_safeguard_stopped: bool = False, joint_currents_a: Optional[List[float]] = None, joint_temps_c: Optional[List[float]] = None, joint_voltages_v: Optional[List[float]] = None, joints: Optional[List[float]] = None, last_terminated_program: str = '', pose: Optional[List[float]] = None, program_counter: int = 0, robot_current_a: float = 0.0, robot_dexterity: float = 0.0, robot_mode: str = '', robot_voltage_v: float = 0.0, safety_message: str = '', sensor_in: Optional[List[bool]] = None, tool_analog_in: Optional[List[float]] = None, tool_analog_out: Optional[List[float]] = None, tool_current_a: float = 0.0, tool_digital_in: Optional[List[bool]] = None, tool_digital_out: Optional[List[bool]] = None, tool_temp_c: float = 0.0, tool_voltage_v: float = 0.0, torque: Optional[List[float]] = None) -> None:
    if analog_bank is None:
      self.analog_bank = []
    else:
      self.analog_bank = analog_bank
    if analog_in is None:
      self.analog_in = []
    else:
      self.analog_in = analog_in
    if analog_out is None:
      self.analog_out = []
    else:
      self.analog_out = analog_out
    self.board_io_current_a = board_io_current_a
    self.board_temp_c = board_temp_c
    if digital_bank is None:
      self.digital_bank = []
    else:
      self.digital_bank = digital_bank
    if digital_in is None:
      self.digital_in = []
    else:
      self.digital_in = digital_in
    if digital_out is None:
      self.digital_out = []
    else:
      self.digital_out = digital_out
    if force is None:
      self.force = []
    else:
      self.force = force
    if integer_bank is None:
      self.integer_bank = []
    else:
      self.integer_bank = integer_bank
    self.is_emergency_stopped = is_emergency_stopped
    self.is_program_running = is_program_running
    self.is_protective_stopped = is_protective_stopped
    self.is_reduced_mode = is_reduced_mode
    self.is_robot_power_on = is_robot_power_on
    self.is_safeguard_stopped = is_safeguard_stopped
    if joint_currents_a is None:
      self.joint_currents_a = []
    else:
      self.joint_currents_a = joint_currents_a
    if joint_temps_c is None:
      self.joint_temps_c = []
    else:
      self.joint_temps_c = joint_temps_c
    if joint_voltages_v is None:
      self.joint_voltages_v = []
    else:
      self.joint_voltages_v = joint_voltages_v
    if joints is None:
      self.joints = []
    else:
      self.joints = joints
    self.last_terminated_program = last_terminated_program
    if pose is None:
      self.pose = []
    else:
      self.pose = pose
    self.program_counter = program_counter
    self.robot_current_a = robot_current_a
    self.robot_dexterity = robot_dexterity
    self.robot_mode = robot_mode
    self.robot_voltage_v = robot_voltage_v
    self.safety_message = safety_message
    if sensor_in is None:
      self.sensor_in = []
    else:
      self.sensor_in = sensor_in
    if tool_analog_in is None:
      self.tool_analog_in = []
    else:
      self.tool_analog_in = tool_analog_in
    if tool_analog_out is None:
      self.tool_analog_out = []
    else:
      self.tool_analog_out = tool_analog_out
    self.tool_current_a = tool_current_a
    if tool_digital_in is None:
      self.tool_digital_in = []
    else:
      self.tool_digital_in = tool_digital_in
    if tool_digital_out is None:
      self.tool_digital_out = []
    else:
      self.tool_digital_out = tool_digital_out
    self.tool_temp_c = tool_temp_c
    self.tool_voltage_v = tool_voltage_v
    if torque is None:
      self.torque = []
    else:
      self.torque = torque

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.analog_bank:
      assert isinstance(self.analog_bank, list), 'Wrong type for attribute: analog_bank. Expected: list. Got: ' + str(type(self.analog_bank)) + '.'
      obj_list = []
      for item in self.analog_bank:
        obj_list.append(item.to_json())
      json_data['analogBank'] = obj_list

    if self.analog_in:
      assert isinstance(self.analog_in, list), 'Wrong type for attribute: analog_in. Expected: list. Got: ' + str(type(self.analog_in)) + '.'
      json_data['analogIn'] = self.analog_in

    if self.analog_out:
      assert isinstance(self.analog_out, list), 'Wrong type for attribute: analog_out. Expected: list. Got: ' + str(type(self.analog_out)) + '.'
      json_data['analogOut'] = self.analog_out

    if self.board_io_current_a:
      assert isinstance(self.board_io_current_a, float) or isinstance(self.board_io_current_a, int), 'Wrong type for attribute: board_io_current_a. Expected: float. Got: ' + str(type(self.board_io_current_a)) + '.'
      json_data['boardIOCurrentA'] = self.board_io_current_a

    if self.board_temp_c:
      assert isinstance(self.board_temp_c, float) or isinstance(self.board_temp_c, int), 'Wrong type for attribute: board_temp_c. Expected: float. Got: ' + str(type(self.board_temp_c)) + '.'
      json_data['boardTempC'] = self.board_temp_c

    if self.digital_bank:
      assert isinstance(self.digital_bank, list), 'Wrong type for attribute: digital_bank. Expected: list. Got: ' + str(type(self.digital_bank)) + '.'
      obj_list = []
      for item in self.digital_bank:
        obj_list.append(item.to_json())
      json_data['digitalBank'] = obj_list

    if self.digital_in:
      assert isinstance(self.digital_in, list), 'Wrong type for attribute: digital_in. Expected: list. Got: ' + str(type(self.digital_in)) + '.'
      json_data['digitalIn'] = self.digital_in

    if self.digital_out:
      assert isinstance(self.digital_out, list), 'Wrong type for attribute: digital_out. Expected: list. Got: ' + str(type(self.digital_out)) + '.'
      json_data['digitalOut'] = self.digital_out

    if self.force:
      assert isinstance(self.force, list), 'Wrong type for attribute: force. Expected: list. Got: ' + str(type(self.force)) + '.'
      json_data['force'] = self.force

    if self.integer_bank:
      assert isinstance(self.integer_bank, list), 'Wrong type for attribute: integer_bank. Expected: list. Got: ' + str(type(self.integer_bank)) + '.'
      obj_list = []
      for item in self.integer_bank:
        obj_list.append(item.to_json())
      json_data['integerBank'] = obj_list

    if self.is_emergency_stopped:
      assert isinstance(self.is_emergency_stopped, bool), 'Wrong type for attribute: is_emergency_stopped. Expected: bool. Got: ' + str(type(self.is_emergency_stopped)) + '.'
      json_data['isEmergencyStopped'] = self.is_emergency_stopped

    if self.is_program_running:
      assert isinstance(self.is_program_running, bool), 'Wrong type for attribute: is_program_running. Expected: bool. Got: ' + str(type(self.is_program_running)) + '.'
      json_data['isProgramRunning'] = self.is_program_running

    if self.is_protective_stopped:
      assert isinstance(self.is_protective_stopped, bool), 'Wrong type for attribute: is_protective_stopped. Expected: bool. Got: ' + str(type(self.is_protective_stopped)) + '.'
      json_data['isProtectiveStopped'] = self.is_protective_stopped

    if self.is_reduced_mode:
      assert isinstance(self.is_reduced_mode, bool), 'Wrong type for attribute: is_reduced_mode. Expected: bool. Got: ' + str(type(self.is_reduced_mode)) + '.'
      json_data['isReducedMode'] = self.is_reduced_mode

    if self.is_robot_power_on:
      assert isinstance(self.is_robot_power_on, bool), 'Wrong type for attribute: is_robot_power_on. Expected: bool. Got: ' + str(type(self.is_robot_power_on)) + '.'
      json_data['isRobotPowerOn'] = self.is_robot_power_on

    if self.is_safeguard_stopped:
      assert isinstance(self.is_safeguard_stopped, bool), 'Wrong type for attribute: is_safeguard_stopped. Expected: bool. Got: ' + str(type(self.is_safeguard_stopped)) + '.'
      json_data['isSafeguardStopped'] = self.is_safeguard_stopped

    if self.joint_currents_a:
      assert isinstance(self.joint_currents_a, list), 'Wrong type for attribute: joint_currents_a. Expected: list. Got: ' + str(type(self.joint_currents_a)) + '.'
      json_data['jointCurrentsA'] = self.joint_currents_a

    if self.joint_temps_c:
      assert isinstance(self.joint_temps_c, list), 'Wrong type for attribute: joint_temps_c. Expected: list. Got: ' + str(type(self.joint_temps_c)) + '.'
      json_data['jointTempsC'] = self.joint_temps_c

    if self.joint_voltages_v:
      assert isinstance(self.joint_voltages_v, list), 'Wrong type for attribute: joint_voltages_v. Expected: list. Got: ' + str(type(self.joint_voltages_v)) + '.'
      json_data['jointVoltagesV'] = self.joint_voltages_v

    if self.joints:
      assert isinstance(self.joints, list), 'Wrong type for attribute: joints. Expected: list. Got: ' + str(type(self.joints)) + '.'
      json_data['joints'] = self.joints

    if self.last_terminated_program:
      assert isinstance(self.last_terminated_program, str), 'Wrong type for attribute: last_terminated_program. Expected: str. Got: ' + str(type(self.last_terminated_program)) + '.'
      json_data['lastTerminatedProgram'] = self.last_terminated_program

    if self.pose:
      assert isinstance(self.pose, list), 'Wrong type for attribute: pose. Expected: list. Got: ' + str(type(self.pose)) + '.'
      json_data['pose'] = self.pose

    if self.program_counter:
      assert isinstance(self.program_counter, int), 'Wrong type for attribute: program_counter. Expected: int. Got: ' + str(type(self.program_counter)) + '.'
      json_data['programCounter'] = self.program_counter

    if self.robot_current_a:
      assert isinstance(self.robot_current_a, float) or isinstance(self.robot_current_a, int), 'Wrong type for attribute: robot_current_a. Expected: float. Got: ' + str(type(self.robot_current_a)) + '.'
      json_data['robotCurrentA'] = self.robot_current_a

    if self.robot_dexterity:
      assert isinstance(self.robot_dexterity, float) or isinstance(self.robot_dexterity, int), 'Wrong type for attribute: robot_dexterity. Expected: float. Got: ' + str(type(self.robot_dexterity)) + '.'
      json_data['robotDexterity'] = self.robot_dexterity

    if self.robot_mode:
      assert isinstance(self.robot_mode, str), 'Wrong type for attribute: robot_mode. Expected: str. Got: ' + str(type(self.robot_mode)) + '.'
      json_data['robotMode'] = self.robot_mode

    if self.robot_voltage_v:
      assert isinstance(self.robot_voltage_v, float) or isinstance(self.robot_voltage_v, int), 'Wrong type for attribute: robot_voltage_v. Expected: float. Got: ' + str(type(self.robot_voltage_v)) + '.'
      json_data['robotVoltageV'] = self.robot_voltage_v

    if self.safety_message:
      assert isinstance(self.safety_message, str), 'Wrong type for attribute: safety_message. Expected: str. Got: ' + str(type(self.safety_message)) + '.'
      json_data['safetyMessage'] = self.safety_message

    if self.sensor_in:
      assert isinstance(self.sensor_in, list), 'Wrong type for attribute: sensor_in. Expected: list. Got: ' + str(type(self.sensor_in)) + '.'
      json_data['sensorIn'] = self.sensor_in

    if self.tool_analog_in:
      assert isinstance(self.tool_analog_in, list), 'Wrong type for attribute: tool_analog_in. Expected: list. Got: ' + str(type(self.tool_analog_in)) + '.'
      json_data['toolAnalogIn'] = self.tool_analog_in

    if self.tool_analog_out:
      assert isinstance(self.tool_analog_out, list), 'Wrong type for attribute: tool_analog_out. Expected: list. Got: ' + str(type(self.tool_analog_out)) + '.'
      json_data['toolAnalogOut'] = self.tool_analog_out

    if self.tool_current_a:
      assert isinstance(self.tool_current_a, float) or isinstance(self.tool_current_a, int), 'Wrong type for attribute: tool_current_a. Expected: float. Got: ' + str(type(self.tool_current_a)) + '.'
      json_data['toolCurrentA'] = self.tool_current_a

    if self.tool_digital_in:
      assert isinstance(self.tool_digital_in, list), 'Wrong type for attribute: tool_digital_in. Expected: list. Got: ' + str(type(self.tool_digital_in)) + '.'
      json_data['toolDigitalIn'] = self.tool_digital_in

    if self.tool_digital_out:
      assert isinstance(self.tool_digital_out, list), 'Wrong type for attribute: tool_digital_out. Expected: list. Got: ' + str(type(self.tool_digital_out)) + '.'
      json_data['toolDigitalOut'] = self.tool_digital_out

    if self.tool_temp_c:
      assert isinstance(self.tool_temp_c, float) or isinstance(self.tool_temp_c, int), 'Wrong type for attribute: tool_temp_c. Expected: float. Got: ' + str(type(self.tool_temp_c)) + '.'
      json_data['toolTempC'] = self.tool_temp_c

    if self.tool_voltage_v:
      assert isinstance(self.tool_voltage_v, float) or isinstance(self.tool_voltage_v, int), 'Wrong type for attribute: tool_voltage_v. Expected: float. Got: ' + str(type(self.tool_voltage_v)) + '.'
      json_data['toolVoltageV'] = self.tool_voltage_v

    if self.torque:
      assert isinstance(self.torque, list), 'Wrong type for attribute: torque. Expected: list. Got: ' + str(type(self.torque)) + '.'
      json_data['torque'] = self.torque

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'RobotState':
    """Convert JSON to type object."""
    obj = RobotState()
    json_list: List[Any]

    expected_json_keys: List[str] = ['analogBank', 'analogIn', 'analogOut', 'boardIOCurrentA', 'boardTempC', 'digitalBank', 'digitalIn', 'digitalOut', 'force', 'integerBank', 'isEmergencyStopped', 'isProgramRunning', 'isProtectiveStopped', 'isReducedMode', 'isRobotPowerOn', 'isSafeguardStopped', 'jointCurrentsA', 'jointTempsC', 'jointVoltagesV', 'joints', 'lastTerminatedProgram', 'pose', 'programCounter', 'robotCurrentA', 'robotDexterity', 'robotMode', 'robotVoltageV', 'safetyMessage', 'sensorIn', 'toolAnalogIn', 'toolAnalogOut', 'toolCurrentA', 'toolDigitalIn', 'toolDigitalOut', 'toolTempC', 'toolVoltageV', 'torque']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid RobotState. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'analogBank' in json_data:
      assert isinstance(json_data['analogBank'], list), 'Wrong type for attribute: analogBank. Expected: list. Got: ' + str(type(json_data['analogBank'])) + '.'
      json_list = []
      for j in json_data['analogBank']:
        json_list.append(AnalogBank.from_json(j))
      obj.analog_bank = json_list

    if 'analogIn' in json_data:
      assert isinstance(json_data['analogIn'], list), 'Wrong type for attribute: analogIn. Expected: list. Got: ' + str(type(json_data['analogIn'])) + '.'
      json_list = []
      for j in json_data['analogIn']:
        json_list.append(j)
      obj.analog_in = json_list

    if 'analogOut' in json_data:
      assert isinstance(json_data['analogOut'], list), 'Wrong type for attribute: analogOut. Expected: list. Got: ' + str(type(json_data['analogOut'])) + '.'
      json_list = []
      for j in json_data['analogOut']:
        json_list.append(j)
      obj.analog_out = json_list

    if 'boardIOCurrentA' in json_data:
      assert isinstance(json_data['boardIOCurrentA'], float) or isinstance(json_data['boardIOCurrentA'], int), 'Wrong type for attribute: boardIOCurrentA. Expected: float. Got: ' + str(type(json_data['boardIOCurrentA'])) + '.'
      obj.board_io_current_a = json_data['boardIOCurrentA']

    if 'boardTempC' in json_data:
      assert isinstance(json_data['boardTempC'], float) or isinstance(json_data['boardTempC'], int), 'Wrong type for attribute: boardTempC. Expected: float. Got: ' + str(type(json_data['boardTempC'])) + '.'
      obj.board_temp_c = json_data['boardTempC']

    if 'digitalBank' in json_data:
      assert isinstance(json_data['digitalBank'], list), 'Wrong type for attribute: digitalBank. Expected: list. Got: ' + str(type(json_data['digitalBank'])) + '.'
      json_list = []
      for j in json_data['digitalBank']:
        json_list.append(DigitalBank.from_json(j))
      obj.digital_bank = json_list

    if 'digitalIn' in json_data:
      assert isinstance(json_data['digitalIn'], list), 'Wrong type for attribute: digitalIn. Expected: list. Got: ' + str(type(json_data['digitalIn'])) + '.'
      json_list = []
      for j in json_data['digitalIn']:
        json_list.append(j)
      obj.digital_in = json_list

    if 'digitalOut' in json_data:
      assert isinstance(json_data['digitalOut'], list), 'Wrong type for attribute: digitalOut. Expected: list. Got: ' + str(type(json_data['digitalOut'])) + '.'
      json_list = []
      for j in json_data['digitalOut']:
        json_list.append(j)
      obj.digital_out = json_list

    if 'force' in json_data:
      assert isinstance(json_data['force'], list), 'Wrong type for attribute: force. Expected: list. Got: ' + str(type(json_data['force'])) + '.'
      json_list = []
      for j in json_data['force']:
        json_list.append(j)
      obj.force = json_list

    if 'integerBank' in json_data:
      assert isinstance(json_data['integerBank'], list), 'Wrong type for attribute: integerBank. Expected: list. Got: ' + str(type(json_data['integerBank'])) + '.'
      json_list = []
      for j in json_data['integerBank']:
        json_list.append(IntegerBank.from_json(j))
      obj.integer_bank = json_list

    if 'isEmergencyStopped' in json_data:
      assert isinstance(json_data['isEmergencyStopped'], bool), 'Wrong type for attribute: isEmergencyStopped. Expected: bool. Got: ' + str(type(json_data['isEmergencyStopped'])) + '.'
      obj.is_emergency_stopped = json_data['isEmergencyStopped']

    if 'isProgramRunning' in json_data:
      assert isinstance(json_data['isProgramRunning'], bool), 'Wrong type for attribute: isProgramRunning. Expected: bool. Got: ' + str(type(json_data['isProgramRunning'])) + '.'
      obj.is_program_running = json_data['isProgramRunning']

    if 'isProtectiveStopped' in json_data:
      assert isinstance(json_data['isProtectiveStopped'], bool), 'Wrong type for attribute: isProtectiveStopped. Expected: bool. Got: ' + str(type(json_data['isProtectiveStopped'])) + '.'
      obj.is_protective_stopped = json_data['isProtectiveStopped']

    if 'isReducedMode' in json_data:
      assert isinstance(json_data['isReducedMode'], bool), 'Wrong type for attribute: isReducedMode. Expected: bool. Got: ' + str(type(json_data['isReducedMode'])) + '.'
      obj.is_reduced_mode = json_data['isReducedMode']

    if 'isRobotPowerOn' in json_data:
      assert isinstance(json_data['isRobotPowerOn'], bool), 'Wrong type for attribute: isRobotPowerOn. Expected: bool. Got: ' + str(type(json_data['isRobotPowerOn'])) + '.'
      obj.is_robot_power_on = json_data['isRobotPowerOn']

    if 'isSafeguardStopped' in json_data:
      assert isinstance(json_data['isSafeguardStopped'], bool), 'Wrong type for attribute: isSafeguardStopped. Expected: bool. Got: ' + str(type(json_data['isSafeguardStopped'])) + '.'
      obj.is_safeguard_stopped = json_data['isSafeguardStopped']

    if 'jointCurrentsA' in json_data:
      assert isinstance(json_data['jointCurrentsA'], list), 'Wrong type for attribute: jointCurrentsA. Expected: list. Got: ' + str(type(json_data['jointCurrentsA'])) + '.'
      json_list = []
      for j in json_data['jointCurrentsA']:
        json_list.append(j)
      obj.joint_currents_a = json_list

    if 'jointTempsC' in json_data:
      assert isinstance(json_data['jointTempsC'], list), 'Wrong type for attribute: jointTempsC. Expected: list. Got: ' + str(type(json_data['jointTempsC'])) + '.'
      json_list = []
      for j in json_data['jointTempsC']:
        json_list.append(j)
      obj.joint_temps_c = json_list

    if 'jointVoltagesV' in json_data:
      assert isinstance(json_data['jointVoltagesV'], list), 'Wrong type for attribute: jointVoltagesV. Expected: list. Got: ' + str(type(json_data['jointVoltagesV'])) + '.'
      json_list = []
      for j in json_data['jointVoltagesV']:
        json_list.append(j)
      obj.joint_voltages_v = json_list

    if 'joints' in json_data:
      assert isinstance(json_data['joints'], list), 'Wrong type for attribute: joints. Expected: list. Got: ' + str(type(json_data['joints'])) + '.'
      json_list = []
      for j in json_data['joints']:
        json_list.append(j)
      obj.joints = json_list

    if 'lastTerminatedProgram' in json_data:
      assert isinstance(json_data['lastTerminatedProgram'], str), 'Wrong type for attribute: lastTerminatedProgram. Expected: str. Got: ' + str(type(json_data['lastTerminatedProgram'])) + '.'
      obj.last_terminated_program = json_data['lastTerminatedProgram']

    if 'pose' in json_data:
      assert isinstance(json_data['pose'], list), 'Wrong type for attribute: pose. Expected: list. Got: ' + str(type(json_data['pose'])) + '.'
      json_list = []
      for j in json_data['pose']:
        json_list.append(j)
      obj.pose = json_list

    if 'programCounter' in json_data:
      assert isinstance(json_data['programCounter'], int), 'Wrong type for attribute: programCounter. Expected: int. Got: ' + str(type(json_data['programCounter'])) + '.'
      obj.program_counter = json_data['programCounter']

    if 'robotCurrentA' in json_data:
      assert isinstance(json_data['robotCurrentA'], float) or isinstance(json_data['robotCurrentA'], int), 'Wrong type for attribute: robotCurrentA. Expected: float. Got: ' + str(type(json_data['robotCurrentA'])) + '.'
      obj.robot_current_a = json_data['robotCurrentA']

    if 'robotDexterity' in json_data:
      assert isinstance(json_data['robotDexterity'], float) or isinstance(json_data['robotDexterity'], int), 'Wrong type for attribute: robotDexterity. Expected: float. Got: ' + str(type(json_data['robotDexterity'])) + '.'
      obj.robot_dexterity = json_data['robotDexterity']

    if 'robotMode' in json_data:
      assert isinstance(json_data['robotMode'], str), 'Wrong type for attribute: robotMode. Expected: str. Got: ' + str(type(json_data['robotMode'])) + '.'
      obj.robot_mode = json_data['robotMode']

    if 'robotVoltageV' in json_data:
      assert isinstance(json_data['robotVoltageV'], float) or isinstance(json_data['robotVoltageV'], int), 'Wrong type for attribute: robotVoltageV. Expected: float. Got: ' + str(type(json_data['robotVoltageV'])) + '.'
      obj.robot_voltage_v = json_data['robotVoltageV']

    if 'safetyMessage' in json_data:
      assert isinstance(json_data['safetyMessage'], str), 'Wrong type for attribute: safetyMessage. Expected: str. Got: ' + str(type(json_data['safetyMessage'])) + '.'
      obj.safety_message = json_data['safetyMessage']

    if 'sensorIn' in json_data:
      assert isinstance(json_data['sensorIn'], list), 'Wrong type for attribute: sensorIn. Expected: list. Got: ' + str(type(json_data['sensorIn'])) + '.'
      json_list = []
      for j in json_data['sensorIn']:
        json_list.append(j)
      obj.sensor_in = json_list

    if 'toolAnalogIn' in json_data:
      assert isinstance(json_data['toolAnalogIn'], list), 'Wrong type for attribute: toolAnalogIn. Expected: list. Got: ' + str(type(json_data['toolAnalogIn'])) + '.'
      json_list = []
      for j in json_data['toolAnalogIn']:
        json_list.append(j)
      obj.tool_analog_in = json_list

    if 'toolAnalogOut' in json_data:
      assert isinstance(json_data['toolAnalogOut'], list), 'Wrong type for attribute: toolAnalogOut. Expected: list. Got: ' + str(type(json_data['toolAnalogOut'])) + '.'
      json_list = []
      for j in json_data['toolAnalogOut']:
        json_list.append(j)
      obj.tool_analog_out = json_list

    if 'toolCurrentA' in json_data:
      assert isinstance(json_data['toolCurrentA'], float) or isinstance(json_data['toolCurrentA'], int), 'Wrong type for attribute: toolCurrentA. Expected: float. Got: ' + str(type(json_data['toolCurrentA'])) + '.'
      obj.tool_current_a = json_data['toolCurrentA']

    if 'toolDigitalIn' in json_data:
      assert isinstance(json_data['toolDigitalIn'], list), 'Wrong type for attribute: toolDigitalIn. Expected: list. Got: ' + str(type(json_data['toolDigitalIn'])) + '.'
      json_list = []
      for j in json_data['toolDigitalIn']:
        json_list.append(j)
      obj.tool_digital_in = json_list

    if 'toolDigitalOut' in json_data:
      assert isinstance(json_data['toolDigitalOut'], list), 'Wrong type for attribute: toolDigitalOut. Expected: list. Got: ' + str(type(json_data['toolDigitalOut'])) + '.'
      json_list = []
      for j in json_data['toolDigitalOut']:
        json_list.append(j)
      obj.tool_digital_out = json_list

    if 'toolTempC' in json_data:
      assert isinstance(json_data['toolTempC'], float) or isinstance(json_data['toolTempC'], int), 'Wrong type for attribute: toolTempC. Expected: float. Got: ' + str(type(json_data['toolTempC'])) + '.'
      obj.tool_temp_c = json_data['toolTempC']

    if 'toolVoltageV' in json_data:
      assert isinstance(json_data['toolVoltageV'], float) or isinstance(json_data['toolVoltageV'], int), 'Wrong type for attribute: toolVoltageV. Expected: float. Got: ' + str(type(json_data['toolVoltageV'])) + '.'
      obj.tool_voltage_v = json_data['toolVoltageV']

    if 'torque' in json_data:
      assert isinstance(json_data['torque'], list), 'Wrong type for attribute: torque. Expected: list. Got: ' + str(type(json_data['torque'])) + '.'
      json_list = []
      for j in json_data['torque']:
        json_list.append(j)
      obj.torque = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.RobotState) -> 'RobotState':
    """Convert RobotState proto to type object."""
    if not proto:
      return None
    obj = RobotState()
    if proto.analog_bank:
      json_list = []
      for j in proto.analog_bank:
        json_list.append(AnalogBank.from_proto(j))
      obj.analog_bank = json_list
    if proto.analog_in:
      json_list = []
      for j in proto.analog_in:
        json_list.append(j)
      obj.analog_in = json_list
    if proto.analog_out:
      json_list = []
      for j in proto.analog_out:
        json_list.append(j)
      obj.analog_out = json_list
    obj.board_io_current_a = get_proto_value(proto.board_io_current_a)
    obj.board_temp_c = get_proto_value(proto.board_temp_c)
    if proto.digital_bank:
      json_list = []
      for j in proto.digital_bank:
        json_list.append(DigitalBank.from_proto(j))
      obj.digital_bank = json_list
    if proto.digital_in:
      json_list = []
      for j in proto.digital_in:
        json_list.append(j)
      obj.digital_in = json_list
    if proto.digital_out:
      json_list = []
      for j in proto.digital_out:
        json_list.append(j)
      obj.digital_out = json_list
    if proto.force:
      json_list = []
      for j in proto.force:
        json_list.append(j)
      obj.force = json_list
    if proto.integer_bank:
      json_list = []
      for j in proto.integer_bank:
        json_list.append(IntegerBank.from_proto(j))
      obj.integer_bank = json_list
    obj.is_emergency_stopped = get_proto_value(proto.robot_stop_state.is_emergency_stopped)
    obj.is_program_running = get_proto_value(proto.is_program_running)
    obj.is_protective_stopped = get_proto_value(proto.robot_stop_state.is_protective_stopped)
    obj.is_reduced_mode = get_proto_value(proto.robot_stop_state.is_reduced_mode)
    obj.is_robot_power_on = get_proto_value(proto.is_robot_power_on)
    obj.is_safeguard_stopped = get_proto_value(proto.robot_stop_state.is_safeguard_stopped)
    if proto.joint_currents_a:
      json_list = []
      for j in proto.joint_currents_a:
        json_list.append(j)
      obj.joint_currents_a = json_list
    if proto.joint_temps_c:
      json_list = []
      for j in proto.joint_temps_c:
        json_list.append(j)
      obj.joint_temps_c = json_list
    if proto.joint_voltages_v:
      json_list = []
      for j in proto.joint_voltages_v:
        json_list.append(j)
      obj.joint_voltages_v = json_list
    if proto.joints:
      json_list = []
      for j in proto.joints:
        json_list.append(j)
      obj.joints = json_list
    obj.last_terminated_program = get_proto_value(proto.last_terminated_program)
    if proto.pose:
      json_list = []
      for j in proto.pose:
        json_list.append(j)
      obj.pose = json_list
    obj.program_counter = get_proto_value(proto.program_counter)
    obj.robot_current_a = get_proto_value(proto.robot_current_a)
    obj.robot_dexterity = get_proto_value(proto.robot_dexterity)
    obj.robot_mode = get_proto_value(proto.robot_mode)
    obj.robot_voltage_v = get_proto_value(proto.robot_voltage_v)
    obj.safety_message = get_proto_value(proto.robot_stop_state.safety_message)
    if proto.sensor_in:
      json_list = []
      for j in proto.sensor_in:
        json_list.append(j)
      obj.sensor_in = json_list
    if proto.tool_analog_in:
      json_list = []
      for j in proto.tool_analog_in:
        json_list.append(j)
      obj.tool_analog_in = json_list
    if proto.tool_analog_out:
      json_list = []
      for j in proto.tool_analog_out:
        json_list.append(j)
      obj.tool_analog_out = json_list
    obj.tool_current_a = get_proto_value(proto.tool_current_a)
    if proto.tool_digital_in:
      json_list = []
      for j in proto.tool_digital_in:
        json_list.append(j)
      obj.tool_digital_in = json_list
    if proto.tool_digital_out:
      json_list = []
      for j in proto.tool_digital_out:
        json_list.append(j)
      obj.tool_digital_out = json_list
    obj.tool_temp_c = get_proto_value(proto.tool_temp_c)
    obj.tool_voltage_v = get_proto_value(proto.tool_voltage_v)
    if proto.torque:
      json_list = []
      for j in proto.torque:
        json_list.append(j)
      obj.torque = json_list
    return obj


class RobotStopState:
  """Representation of proto message RobotStopState.

   RobotStopState indicates various reasons why a robot may have stopped.
   Fields are present in robot-state messages and *-stop-state/
   *-stop-state-update messages.
  """
  is_emergency_stopped: bool
  is_protective_stopped: bool
  is_safeguard_stopped: bool
  is_reduced_mode: bool
  safety_message: str

  def __init__(self, is_emergency_stopped: bool = False, is_protective_stopped: bool = False, is_reduced_mode: bool = False, is_safeguard_stopped: bool = False, safety_message: str = '') -> None:
    self.is_emergency_stopped = is_emergency_stopped
    self.is_protective_stopped = is_protective_stopped
    self.is_reduced_mode = is_reduced_mode
    self.is_safeguard_stopped = is_safeguard_stopped
    self.safety_message = safety_message

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.is_emergency_stopped:
      assert isinstance(self.is_emergency_stopped, bool), 'Wrong type for attribute: is_emergency_stopped. Expected: bool. Got: ' + str(type(self.is_emergency_stopped)) + '.'
      json_data['isEmergencyStopped'] = self.is_emergency_stopped

    if self.is_protective_stopped:
      assert isinstance(self.is_protective_stopped, bool), 'Wrong type for attribute: is_protective_stopped. Expected: bool. Got: ' + str(type(self.is_protective_stopped)) + '.'
      json_data['isProtectiveStopped'] = self.is_protective_stopped

    if self.is_reduced_mode:
      assert isinstance(self.is_reduced_mode, bool), 'Wrong type for attribute: is_reduced_mode. Expected: bool. Got: ' + str(type(self.is_reduced_mode)) + '.'
      json_data['isReducedMode'] = self.is_reduced_mode

    if self.is_safeguard_stopped:
      assert isinstance(self.is_safeguard_stopped, bool), 'Wrong type for attribute: is_safeguard_stopped. Expected: bool. Got: ' + str(type(self.is_safeguard_stopped)) + '.'
      json_data['isSafeguardStopped'] = self.is_safeguard_stopped

    if self.safety_message:
      assert isinstance(self.safety_message, str), 'Wrong type for attribute: safety_message. Expected: str. Got: ' + str(type(self.safety_message)) + '.'
      json_data['safetyMessage'] = self.safety_message

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'RobotStopState':
    """Convert JSON to type object."""
    obj = RobotStopState()

    expected_json_keys: List[str] = ['isEmergencyStopped', 'isProtectiveStopped', 'isReducedMode', 'isSafeguardStopped', 'safetyMessage']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid RobotStopState. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'isEmergencyStopped' in json_data:
      assert isinstance(json_data['isEmergencyStopped'], bool), 'Wrong type for attribute: isEmergencyStopped. Expected: bool. Got: ' + str(type(json_data['isEmergencyStopped'])) + '.'
      obj.is_emergency_stopped = json_data['isEmergencyStopped']

    if 'isProtectiveStopped' in json_data:
      assert isinstance(json_data['isProtectiveStopped'], bool), 'Wrong type for attribute: isProtectiveStopped. Expected: bool. Got: ' + str(type(json_data['isProtectiveStopped'])) + '.'
      obj.is_protective_stopped = json_data['isProtectiveStopped']

    if 'isReducedMode' in json_data:
      assert isinstance(json_data['isReducedMode'], bool), 'Wrong type for attribute: isReducedMode. Expected: bool. Got: ' + str(type(json_data['isReducedMode'])) + '.'
      obj.is_reduced_mode = json_data['isReducedMode']

    if 'isSafeguardStopped' in json_data:
      assert isinstance(json_data['isSafeguardStopped'], bool), 'Wrong type for attribute: isSafeguardStopped. Expected: bool. Got: ' + str(type(json_data['isSafeguardStopped'])) + '.'
      obj.is_safeguard_stopped = json_data['isSafeguardStopped']

    if 'safetyMessage' in json_data:
      assert isinstance(json_data['safetyMessage'], str), 'Wrong type for attribute: safetyMessage. Expected: str. Got: ' + str(type(json_data['safetyMessage'])) + '.'
      obj.safety_message = json_data['safetyMessage']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.RobotStopState) -> 'RobotStopState':
    """Convert RobotStopState proto to type object."""
    if not proto:
      return None
    obj = RobotStopState()
    obj.is_emergency_stopped = get_proto_value(proto.is_emergency_stopped)
    obj.is_protective_stopped = get_proto_value(proto.is_protective_stopped)
    obj.is_reduced_mode = get_proto_value(proto.is_reduced_mode)
    obj.is_safeguard_stopped = get_proto_value(proto.is_safeguard_stopped)
    obj.safety_message = get_proto_value(proto.safety_message)
    return obj


class SendToClient:
  """Representation of proto message SendToClient.

   SendToClient is data about a client to which the message should be sent.
  """
  # UID is the UID of the client.
  uid: str

  # Tag is the tag of the message for the client.
  tag: str

  def __init__(self, tag: str = '', uid: str = '') -> None:
    self.tag = tag
    self.uid = uid

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.tag:
      assert isinstance(self.tag, str), 'Wrong type for attribute: tag. Expected: str. Got: ' + str(type(self.tag)) + '.'
      json_data['tag'] = self.tag

    if self.uid:
      assert isinstance(self.uid, str), 'Wrong type for attribute: uid. Expected: str. Got: ' + str(type(self.uid)) + '.'
      json_data['uid'] = self.uid

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'SendToClient':
    """Convert JSON to type object."""
    obj = SendToClient()

    expected_json_keys: List[str] = ['tag', 'uid']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid SendToClient. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'tag' in json_data:
      assert isinstance(json_data['tag'], str), 'Wrong type for attribute: tag. Expected: str. Got: ' + str(type(json_data['tag'])) + '.'
      obj.tag = json_data['tag']

    if 'uid' in json_data:
      assert isinstance(json_data['uid'], str), 'Wrong type for attribute: uid. Expected: str. Got: ' + str(type(json_data['uid'])) + '.'
      obj.uid = json_data['uid']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.SendToClient) -> 'SendToClient':
    """Convert SendToClient proto to type object."""
    if not proto:
      return None
    obj = SendToClient()
    obj.tag = get_proto_value(proto.tag)
    obj.uid = get_proto_value(proto.uid)
    return obj


class SensorLimits:
  """Representation of proto message SensorLimits.

   SensorLimits are sensor limits to use with Limits in waypoints.
  """
  device_type: str
  device_name: str
  value: Optional['CapabilityState']
  maximum: Optional['CapabilityState']
  minimum: Optional['CapabilityState']

  def __init__(self, device_name: str = '', device_type: str = '', maximum: Optional['CapabilityState'] = None, minimum: Optional['CapabilityState'] = None, value: Optional['CapabilityState'] = None) -> None:
    self.device_name = device_name
    self.device_type = device_type
    self.maximum = maximum
    self.minimum = minimum
    self.value = value

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.device_name:
      assert isinstance(self.device_name, str), 'Wrong type for attribute: device_name. Expected: str. Got: ' + str(type(self.device_name)) + '.'
      json_data['deviceName'] = self.device_name

    if self.device_type:
      assert isinstance(self.device_type, str), 'Wrong type for attribute: device_type. Expected: str. Got: ' + str(type(self.device_type)) + '.'
      json_data['deviceType'] = self.device_type

    if self.maximum:
      assert self.maximum.__class__.__name__ == 'CapabilityState', 'Wrong type for attribute: maximum. Expected: CapabilityState. Got: ' + str(type(self.maximum)) + '.'
      json_data['maximum'] = self.maximum.to_json()

    if self.minimum:
      assert self.minimum.__class__.__name__ == 'CapabilityState', 'Wrong type for attribute: minimum. Expected: CapabilityState. Got: ' + str(type(self.minimum)) + '.'
      json_data['minimum'] = self.minimum.to_json()

    if self.value:
      assert self.value.__class__.__name__ == 'CapabilityState', 'Wrong type for attribute: value. Expected: CapabilityState. Got: ' + str(type(self.value)) + '.'
      json_data['value'] = self.value.to_json()

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'SensorLimits':
    """Convert JSON to type object."""
    obj = SensorLimits()

    expected_json_keys: List[str] = ['deviceName', 'deviceType', 'maximum', 'minimum', 'value']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid SensorLimits. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'deviceName' in json_data:
      assert isinstance(json_data['deviceName'], str), 'Wrong type for attribute: deviceName. Expected: str. Got: ' + str(type(json_data['deviceName'])) + '.'
      obj.device_name = json_data['deviceName']

    if 'deviceType' in json_data:
      assert isinstance(json_data['deviceType'], str), 'Wrong type for attribute: deviceType. Expected: str. Got: ' + str(type(json_data['deviceType'])) + '.'
      obj.device_type = json_data['deviceType']

    if 'maximum' in json_data:
      assert isinstance(json_data['maximum'], dict), 'Wrong type for attribute: maximum. Expected: dict. Got: ' + str(type(json_data['maximum'])) + '.'
      obj.maximum = CapabilityState.from_json(json_data['maximum'])

    if 'minimum' in json_data:
      assert isinstance(json_data['minimum'], dict), 'Wrong type for attribute: minimum. Expected: dict. Got: ' + str(type(json_data['minimum'])) + '.'
      obj.minimum = CapabilityState.from_json(json_data['minimum'])

    if 'value' in json_data:
      assert isinstance(json_data['value'], dict), 'Wrong type for attribute: value. Expected: dict. Got: ' + str(type(json_data['value'])) + '.'
      obj.value = CapabilityState.from_json(json_data['value'])

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.SensorLimits) -> 'SensorLimits':
    """Convert SensorLimits proto to type object."""
    if not proto:
      return None
    obj = SensorLimits()
    obj.device_name = get_proto_value(proto.device_name)
    obj.device_type = get_proto_value(proto.device_type)
    obj.maximum = CapabilityState.from_proto(get_proto_field(proto, 'maximum'))
    obj.minimum = CapabilityState.from_proto(get_proto_field(proto, 'minimum'))
    obj.value = CapabilityState.from_proto(get_proto_field(proto, 'value'))
    return obj


class SessionInfo:
  """Representation of proto message SessionInfo.

   SessionInfo is written to the device data log to store information about the
   session for analytics.
  """
  operator_uid: str
  operator_type: str
  session_id: str
  start_time: int
  robot_name: str
  client_os: str
  ui_version: str
  calibration_version: str
  accept_depth_encoding: List[str]
  relay: str

  # ActionsetsVersion is the version of action sets being used in the
  # current session.
  actionsets_version: str

  # SafetyVersion is the version of safety planes being used in the
  # current session.
  safety_version: str

  # WorkcellIOVersion is the version of workcell I/O configuration being used
  # in the current session.
  workcell_io_version: str

  # Transport is the name of the transport used to transmit the session.
  # Currently, "webrtc" is the only accepted value.
  transport: str
  client_session_uid: str

  # WorkcellSetupVersion is the version of the workcell setup configuration.
  workcell_setup_version: str

  # ConstraintsVersion is the version of constraints being used in the
  # current session.
  constraints_version: str

  def __init__(self, accept_depth_encoding: Optional[List[str]] = None, actionsets_version: str = '', calibration_version: str = '', client_os: str = '', client_session_uid: str = '', constraints_version: str = '', operator_type: str = '', operator_uid: str = '', relay: str = '', robot_name: str = '', safety_version: str = '', session_id: str = '', start_time: int = 0, transport: str = '', ui_version: str = '', workcell_io_version: str = '', workcell_setup_version: str = '') -> None:
    if accept_depth_encoding is None:
      self.accept_depth_encoding = []
    else:
      self.accept_depth_encoding = accept_depth_encoding
    self.actionsets_version = actionsets_version
    self.calibration_version = calibration_version
    self.client_os = client_os
    self.client_session_uid = client_session_uid
    self.constraints_version = constraints_version
    self.operator_type = operator_type
    self.operator_uid = operator_uid
    self.relay = relay
    self.robot_name = robot_name
    self.safety_version = safety_version
    self.session_id = session_id
    self.start_time = start_time
    self.transport = transport
    self.ui_version = ui_version
    self.workcell_io_version = workcell_io_version
    self.workcell_setup_version = workcell_setup_version

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.accept_depth_encoding:
      assert isinstance(self.accept_depth_encoding, list), 'Wrong type for attribute: accept_depth_encoding. Expected: list. Got: ' + str(type(self.accept_depth_encoding)) + '.'
      json_data['acceptDepthEncoding'] = self.accept_depth_encoding

    if self.actionsets_version:
      assert isinstance(self.actionsets_version, str), 'Wrong type for attribute: actionsets_version. Expected: str. Got: ' + str(type(self.actionsets_version)) + '.'
      json_data['actionsetsVersion'] = self.actionsets_version

    if self.calibration_version:
      assert isinstance(self.calibration_version, str), 'Wrong type for attribute: calibration_version. Expected: str. Got: ' + str(type(self.calibration_version)) + '.'
      json_data['calibrationVersion'] = self.calibration_version

    if self.client_os:
      assert isinstance(self.client_os, str), 'Wrong type for attribute: client_os. Expected: str. Got: ' + str(type(self.client_os)) + '.'
      json_data['clientOS'] = self.client_os

    if self.client_session_uid:
      assert isinstance(self.client_session_uid, str), 'Wrong type for attribute: client_session_uid. Expected: str. Got: ' + str(type(self.client_session_uid)) + '.'
      json_data['clientSessionUID'] = self.client_session_uid

    if self.constraints_version:
      assert isinstance(self.constraints_version, str), 'Wrong type for attribute: constraints_version. Expected: str. Got: ' + str(type(self.constraints_version)) + '.'
      json_data['constraintsVersion'] = self.constraints_version

    if self.operator_type:
      assert isinstance(self.operator_type, str), 'Wrong type for attribute: operator_type. Expected: str. Got: ' + str(type(self.operator_type)) + '.'
      json_data['operatorType'] = self.operator_type

    if self.operator_uid:
      assert isinstance(self.operator_uid, str), 'Wrong type for attribute: operator_uid. Expected: str. Got: ' + str(type(self.operator_uid)) + '.'
      json_data['operatorUID'] = self.operator_uid

    if self.relay:
      assert isinstance(self.relay, str), 'Wrong type for attribute: relay. Expected: str. Got: ' + str(type(self.relay)) + '.'
      json_data['relay'] = self.relay

    if self.robot_name:
      assert isinstance(self.robot_name, str), 'Wrong type for attribute: robot_name. Expected: str. Got: ' + str(type(self.robot_name)) + '.'
      json_data['robotName'] = self.robot_name

    if self.safety_version:
      assert isinstance(self.safety_version, str), 'Wrong type for attribute: safety_version. Expected: str. Got: ' + str(type(self.safety_version)) + '.'
      json_data['safetyVersion'] = self.safety_version

    if self.session_id:
      assert isinstance(self.session_id, str), 'Wrong type for attribute: session_id. Expected: str. Got: ' + str(type(self.session_id)) + '.'
      json_data['sessionID'] = self.session_id

    if self.start_time:
      assert isinstance(self.start_time, int), 'Wrong type for attribute: start_time. Expected: int. Got: ' + str(type(self.start_time)) + '.'
      json_data['startTime'] = self.start_time

    if self.transport:
      assert isinstance(self.transport, str), 'Wrong type for attribute: transport. Expected: str. Got: ' + str(type(self.transport)) + '.'
      json_data['transport'] = self.transport

    if self.ui_version:
      assert isinstance(self.ui_version, str), 'Wrong type for attribute: ui_version. Expected: str. Got: ' + str(type(self.ui_version)) + '.'
      json_data['uiVersion'] = self.ui_version

    if self.workcell_io_version:
      assert isinstance(self.workcell_io_version, str), 'Wrong type for attribute: workcell_io_version. Expected: str. Got: ' + str(type(self.workcell_io_version)) + '.'
      json_data['workcellIOVersion'] = self.workcell_io_version

    if self.workcell_setup_version:
      assert isinstance(self.workcell_setup_version, str), 'Wrong type for attribute: workcell_setup_version. Expected: str. Got: ' + str(type(self.workcell_setup_version)) + '.'
      json_data['workcellSetupVersion'] = self.workcell_setup_version

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'SessionInfo':
    """Convert JSON to type object."""
    obj = SessionInfo()
    json_list: List[Any]

    expected_json_keys: List[str] = ['acceptDepthEncoding', 'actionsetsVersion', 'calibrationVersion', 'clientOS', 'clientSessionUID', 'constraintsVersion', 'operatorType', 'operatorUID', 'relay', 'robotName', 'safetyVersion', 'sessionID', 'startTime', 'transport', 'uiVersion', 'workcellIOVersion', 'workcellSetupVersion']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid SessionInfo. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'acceptDepthEncoding' in json_data:
      assert isinstance(json_data['acceptDepthEncoding'], list), 'Wrong type for attribute: acceptDepthEncoding. Expected: list. Got: ' + str(type(json_data['acceptDepthEncoding'])) + '.'
      json_list = []
      for j in json_data['acceptDepthEncoding']:
        json_list.append(j)
      obj.accept_depth_encoding = json_list

    if 'actionsetsVersion' in json_data:
      assert isinstance(json_data['actionsetsVersion'], str), 'Wrong type for attribute: actionsetsVersion. Expected: str. Got: ' + str(type(json_data['actionsetsVersion'])) + '.'
      obj.actionsets_version = json_data['actionsetsVersion']

    if 'calibrationVersion' in json_data:
      assert isinstance(json_data['calibrationVersion'], str), 'Wrong type for attribute: calibrationVersion. Expected: str. Got: ' + str(type(json_data['calibrationVersion'])) + '.'
      obj.calibration_version = json_data['calibrationVersion']

    if 'clientOS' in json_data:
      assert isinstance(json_data['clientOS'], str), 'Wrong type for attribute: clientOS. Expected: str. Got: ' + str(type(json_data['clientOS'])) + '.'
      obj.client_os = json_data['clientOS']

    if 'clientSessionUID' in json_data:
      assert isinstance(json_data['clientSessionUID'], str), 'Wrong type for attribute: clientSessionUID. Expected: str. Got: ' + str(type(json_data['clientSessionUID'])) + '.'
      obj.client_session_uid = json_data['clientSessionUID']

    if 'constraintsVersion' in json_data:
      assert isinstance(json_data['constraintsVersion'], str), 'Wrong type for attribute: constraintsVersion. Expected: str. Got: ' + str(type(json_data['constraintsVersion'])) + '.'
      obj.constraints_version = json_data['constraintsVersion']

    if 'operatorType' in json_data:
      assert isinstance(json_data['operatorType'], str), 'Wrong type for attribute: operatorType. Expected: str. Got: ' + str(type(json_data['operatorType'])) + '.'
      obj.operator_type = json_data['operatorType']

    if 'operatorUID' in json_data:
      assert isinstance(json_data['operatorUID'], str), 'Wrong type for attribute: operatorUID. Expected: str. Got: ' + str(type(json_data['operatorUID'])) + '.'
      obj.operator_uid = json_data['operatorUID']

    if 'relay' in json_data:
      assert isinstance(json_data['relay'], str), 'Wrong type for attribute: relay. Expected: str. Got: ' + str(type(json_data['relay'])) + '.'
      obj.relay = json_data['relay']

    if 'robotName' in json_data:
      assert isinstance(json_data['robotName'], str), 'Wrong type for attribute: robotName. Expected: str. Got: ' + str(type(json_data['robotName'])) + '.'
      obj.robot_name = json_data['robotName']

    if 'safetyVersion' in json_data:
      assert isinstance(json_data['safetyVersion'], str), 'Wrong type for attribute: safetyVersion. Expected: str. Got: ' + str(type(json_data['safetyVersion'])) + '.'
      obj.safety_version = json_data['safetyVersion']

    if 'sessionID' in json_data:
      assert isinstance(json_data['sessionID'], str), 'Wrong type for attribute: sessionID. Expected: str. Got: ' + str(type(json_data['sessionID'])) + '.'
      obj.session_id = json_data['sessionID']

    if 'startTime' in json_data:
      assert isinstance(json_data['startTime'], int), 'Wrong type for attribute: startTime. Expected: int. Got: ' + str(type(json_data['startTime'])) + '.'
      obj.start_time = json_data['startTime']

    if 'transport' in json_data:
      assert isinstance(json_data['transport'], str), 'Wrong type for attribute: transport. Expected: str. Got: ' + str(type(json_data['transport'])) + '.'
      obj.transport = json_data['transport']

    if 'uiVersion' in json_data:
      assert isinstance(json_data['uiVersion'], str), 'Wrong type for attribute: uiVersion. Expected: str. Got: ' + str(type(json_data['uiVersion'])) + '.'
      obj.ui_version = json_data['uiVersion']

    if 'workcellIOVersion' in json_data:
      assert isinstance(json_data['workcellIOVersion'], str), 'Wrong type for attribute: workcellIOVersion. Expected: str. Got: ' + str(type(json_data['workcellIOVersion'])) + '.'
      obj.workcell_io_version = json_data['workcellIOVersion']

    if 'workcellSetupVersion' in json_data:
      assert isinstance(json_data['workcellSetupVersion'], str), 'Wrong type for attribute: workcellSetupVersion. Expected: str. Got: ' + str(type(json_data['workcellSetupVersion'])) + '.'
      obj.workcell_setup_version = json_data['workcellSetupVersion']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.SessionInfo) -> 'SessionInfo':
    """Convert SessionInfo proto to type object."""
    if not proto:
      return None
    obj = SessionInfo()
    if proto.accept_depth_encoding:
      json_list = []
      for j in proto.accept_depth_encoding:
        json_list.append(j)
      obj.accept_depth_encoding = json_list
    obj.actionsets_version = get_proto_value(proto.actionsets_version)
    obj.calibration_version = get_proto_value(proto.calibration_version)
    obj.client_os = get_proto_value(proto.client_os)
    obj.client_session_uid = get_proto_value(proto.client_session_uid)
    obj.constraints_version = get_proto_value(proto.constraints_version)
    obj.operator_type = get_proto_value(proto.operator_type)
    obj.operator_uid = get_proto_value(proto.operator_uid)
    obj.relay = get_proto_value(proto.relay)
    obj.robot_name = get_proto_value(proto.robot_name)
    obj.safety_version = get_proto_value(proto.safety_version)
    obj.session_id = get_proto_value(proto.session_id)
    obj.start_time = get_proto_value(proto.start_time)
    obj.transport = get_proto_value(proto.transport)
    obj.ui_version = get_proto_value(proto.ui_version)
    obj.workcell_io_version = get_proto_value(proto.workcell_io_version)
    obj.workcell_setup_version = get_proto_value(proto.workcell_setup_version)
    return obj


class SetAnalogOutArgs:
  """Representation of proto message SetAnalogOutArgs.

   Sets an analog output. The value must be in the range [0, 1]. Values outside
   this range will result in undefined behavior.
  """
  output: int
  value: float

  def __init__(self, output: int = 0, value: float = 0.0) -> None:
    self.output = output
    self.value = value

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.output:
      assert isinstance(self.output, int), 'Wrong type for attribute: output. Expected: int. Got: ' + str(type(self.output)) + '.'
      json_data['output'] = self.output

    if self.value:
      assert isinstance(self.value, float) or isinstance(self.value, int), 'Wrong type for attribute: value. Expected: float. Got: ' + str(type(self.value)) + '.'
      json_data['value'] = self.value

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'SetAnalogOutArgs':
    """Convert JSON to type object."""
    obj = SetAnalogOutArgs()

    expected_json_keys: List[str] = ['output', 'value']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid SetAnalogOutArgs. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'output' in json_data:
      assert isinstance(json_data['output'], int), 'Wrong type for attribute: output. Expected: int. Got: ' + str(type(json_data['output'])) + '.'
      obj.output = json_data['output']

    if 'value' in json_data:
      assert isinstance(json_data['value'], float) or isinstance(json_data['value'], int), 'Wrong type for attribute: value. Expected: float. Got: ' + str(type(json_data['value'])) + '.'
      obj.value = json_data['value']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.SetAnalogOutArgs) -> 'SetAnalogOutArgs':
    """Convert SetAnalogOutArgs proto to type object."""
    if not proto:
      return None
    obj = SetAnalogOutArgs()
    obj.output = get_proto_value(proto.output)
    obj.value = get_proto_value(proto.value)
    return obj


class SetBlendRadiusArgs:
  """Representation of proto message SetBlendRadiusArgs.

   Sets blend radius for following commands.
  """
  radius: float

  def __init__(self, radius: float = 0.0) -> None:
    self.radius = radius

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.radius:
      assert isinstance(self.radius, float) or isinstance(self.radius, int), 'Wrong type for attribute: radius. Expected: float. Got: ' + str(type(self.radius)) + '.'
      json_data['radius'] = self.radius

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'SetBlendRadiusArgs':
    """Convert JSON to type object."""
    obj = SetBlendRadiusArgs()

    expected_json_keys: List[str] = ['radius']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid SetBlendRadiusArgs. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'radius' in json_data:
      assert isinstance(json_data['radius'], float) or isinstance(json_data['radius'], int), 'Wrong type for attribute: radius. Expected: float. Got: ' + str(type(json_data['radius'])) + '.'
      obj.radius = json_data['radius']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.SetBlendRadiusArgs) -> 'SetBlendRadiusArgs':
    """Convert SetBlendRadiusArgs proto to type object."""
    if not proto:
      return None
    obj = SetBlendRadiusArgs()
    obj.radius = get_proto_value(proto.radius)
    return obj


class SetCameraIntrinsics:
  """Representation of proto message SetCameraIntrinsics.

   SetCameraIntrinsics sets the camera intrinsics in SIM.

  """
  py_id: str
  intrinsics: List[float]
  near_clip: float
  far_clip: float

  def __init__(self, far_clip: float = 0.0, intrinsics: Optional[List[float]] = None, near_clip: float = 0.0, py_id: str = '') -> None:
    self.far_clip = far_clip
    if intrinsics is None:
      self.intrinsics = []
    else:
      self.intrinsics = intrinsics
    self.near_clip = near_clip
    self.py_id = py_id

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.far_clip:
      assert isinstance(self.far_clip, float) or isinstance(self.far_clip, int), 'Wrong type for attribute: far_clip. Expected: float. Got: ' + str(type(self.far_clip)) + '.'
      json_data['farClip'] = self.far_clip

    if self.intrinsics:
      assert isinstance(self.intrinsics, list), 'Wrong type for attribute: intrinsics. Expected: list. Got: ' + str(type(self.intrinsics)) + '.'
      json_data['intrinsics'] = self.intrinsics

    if self.near_clip:
      assert isinstance(self.near_clip, float) or isinstance(self.near_clip, int), 'Wrong type for attribute: near_clip. Expected: float. Got: ' + str(type(self.near_clip)) + '.'
      json_data['nearClip'] = self.near_clip

    if self.py_id:
      assert isinstance(self.py_id, str), 'Wrong type for attribute: py_id. Expected: str. Got: ' + str(type(self.py_id)) + '.'
      json_data['id'] = self.py_id

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'SetCameraIntrinsics':
    """Convert JSON to type object."""
    obj = SetCameraIntrinsics()
    json_list: List[Any]

    expected_json_keys: List[str] = ['farClip', 'intrinsics', 'nearClip', 'id']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid SetCameraIntrinsics. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'farClip' in json_data:
      assert isinstance(json_data['farClip'], float) or isinstance(json_data['farClip'], int), 'Wrong type for attribute: farClip. Expected: float. Got: ' + str(type(json_data['farClip'])) + '.'
      obj.far_clip = json_data['farClip']

    if 'intrinsics' in json_data:
      assert isinstance(json_data['intrinsics'], list), 'Wrong type for attribute: intrinsics. Expected: list. Got: ' + str(type(json_data['intrinsics'])) + '.'
      json_list = []
      for j in json_data['intrinsics']:
        json_list.append(j)
      obj.intrinsics = json_list

    if 'nearClip' in json_data:
      assert isinstance(json_data['nearClip'], float) or isinstance(json_data['nearClip'], int), 'Wrong type for attribute: nearClip. Expected: float. Got: ' + str(type(json_data['nearClip'])) + '.'
      obj.near_clip = json_data['nearClip']

    if 'id' in json_data:
      assert isinstance(json_data['id'], str), 'Wrong type for attribute: id. Expected: str. Got: ' + str(type(json_data['id'])) + '.'
      obj.py_id = json_data['id']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.SetCameraIntrinsics) -> 'SetCameraIntrinsics':
    """Convert SetCameraIntrinsics proto to type object."""
    if not proto:
      return None
    obj = SetCameraIntrinsics()
    obj.far_clip = get_proto_value(proto.far_clip)
    if proto.intrinsics:
      json_list = []
      for j in proto.intrinsics:
        json_list.append(j)
      obj.intrinsics = json_list
    obj.near_clip = get_proto_value(proto.near_clip)
    obj.py_id = get_proto_value(proto.id)
    return obj


class SetDigitalOutArgs:
  """Representation of proto message SetDigitalOutArgs.

   Sets a digital output. This is not a tool digital output, see
   SetToolDigitalOutArgs for that.
  """
  output: int
  value: bool

  def __init__(self, output: int = 0, value: bool = False) -> None:
    self.output = output
    self.value = value

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.output:
      assert isinstance(self.output, int), 'Wrong type for attribute: output. Expected: int. Got: ' + str(type(self.output)) + '.'
      json_data['output'] = self.output

    if self.value:
      assert isinstance(self.value, bool), 'Wrong type for attribute: value. Expected: bool. Got: ' + str(type(self.value)) + '.'
      json_data['value'] = self.value

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'SetDigitalOutArgs':
    """Convert JSON to type object."""
    obj = SetDigitalOutArgs()

    expected_json_keys: List[str] = ['output', 'value']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid SetDigitalOutArgs. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'output' in json_data:
      assert isinstance(json_data['output'], int), 'Wrong type for attribute: output. Expected: int. Got: ' + str(type(json_data['output'])) + '.'
      obj.output = json_data['output']

    if 'value' in json_data:
      assert isinstance(json_data['value'], bool), 'Wrong type for attribute: value. Expected: bool. Got: ' + str(type(json_data['value'])) + '.'
      obj.value = json_data['value']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.SetDigitalOutArgs) -> 'SetDigitalOutArgs':
    """Convert SetDigitalOutArgs proto to type object."""
    if not proto:
      return None
    obj = SetDigitalOutArgs()
    obj.output = get_proto_value(proto.output)
    obj.value = get_proto_value(proto.value)
    return obj


class SetObjectPose:
  """Representation of proto message SetObjectPose.

   SetObjectPose sets the pose of a specific object of the scene in SIM.

  """
  py_id: str
  pose_xyzxyzw: List[float]

  def __init__(self, pose_xyzxyzw: Optional[List[float]] = None, py_id: str = '') -> None:
    if pose_xyzxyzw is None:
      self.pose_xyzxyzw = []
    else:
      self.pose_xyzxyzw = pose_xyzxyzw
    self.py_id = py_id

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.pose_xyzxyzw:
      assert isinstance(self.pose_xyzxyzw, list), 'Wrong type for attribute: pose_xyzxyzw. Expected: list. Got: ' + str(type(self.pose_xyzxyzw)) + '.'
      json_data['poseXYZXYZW'] = self.pose_xyzxyzw

    if self.py_id:
      assert isinstance(self.py_id, str), 'Wrong type for attribute: py_id. Expected: str. Got: ' + str(type(self.py_id)) + '.'
      json_data['id'] = self.py_id

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'SetObjectPose':
    """Convert JSON to type object."""
    obj = SetObjectPose()
    json_list: List[Any]

    expected_json_keys: List[str] = ['poseXYZXYZW', 'id']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid SetObjectPose. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'poseXYZXYZW' in json_data:
      assert isinstance(json_data['poseXYZXYZW'], list), 'Wrong type for attribute: poseXYZXYZW. Expected: list. Got: ' + str(type(json_data['poseXYZXYZW'])) + '.'
      json_list = []
      for j in json_data['poseXYZXYZW']:
        json_list.append(j)
      obj.pose_xyzxyzw = json_list

    if 'id' in json_data:
      assert isinstance(json_data['id'], str), 'Wrong type for attribute: id. Expected: str. Got: ' + str(type(json_data['id'])) + '.'
      obj.py_id = json_data['id']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.SetObjectPose) -> 'SetObjectPose':
    """Convert SetObjectPose proto to type object."""
    if not proto:
      return None
    obj = SetObjectPose()
    if proto.pose_xyzxyzw:
      json_list = []
      for j in proto.pose_xyzxyzw:
        json_list.append(j)
      obj.pose_xyzxyzw = json_list
    obj.py_id = get_proto_value(proto.id)
    return obj


class SetOutput:
  """Representation of proto message SetOutput.

   SetOutput allows setting output based on workcell I/O config reference.
  """
  # The device type specified in the workcell I/O config that
  # corresponds to the capability.
  py_type: str
  name: str
  args: List['CapabilityState']

  def __init__(self, args: Optional[List['CapabilityState']] = None, name: str = '', py_type: str = '') -> None:
    if args is None:
      self.args = []
    else:
      self.args = args
    self.name = name
    self.py_type = py_type

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.args:
      assert isinstance(self.args, list), 'Wrong type for attribute: args. Expected: list. Got: ' + str(type(self.args)) + '.'
      obj_list = []
      for item in self.args:
        obj_list.append(item.to_json())
      json_data['args'] = obj_list

    if self.name:
      assert isinstance(self.name, str), 'Wrong type for attribute: name. Expected: str. Got: ' + str(type(self.name)) + '.'
      json_data['name'] = self.name

    if self.py_type:
      assert isinstance(self.py_type, str), 'Wrong type for attribute: py_type. Expected: str. Got: ' + str(type(self.py_type)) + '.'
      json_data['type'] = self.py_type

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'SetOutput':
    """Convert JSON to type object."""
    obj = SetOutput()
    json_list: List[Any]

    expected_json_keys: List[str] = ['args', 'name', 'type']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid SetOutput. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'args' in json_data:
      assert isinstance(json_data['args'], list), 'Wrong type for attribute: args. Expected: list. Got: ' + str(type(json_data['args'])) + '.'
      json_list = []
      for j in json_data['args']:
        json_list.append(CapabilityState.from_json(j))
      obj.args = json_list

    if 'name' in json_data:
      assert isinstance(json_data['name'], str), 'Wrong type for attribute: name. Expected: str. Got: ' + str(type(json_data['name'])) + '.'
      obj.name = json_data['name']

    if 'type' in json_data:
      assert isinstance(json_data['type'], str), 'Wrong type for attribute: type. Expected: str. Got: ' + str(type(json_data['type'])) + '.'
      obj.py_type = json_data['type']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.SetOutput) -> 'SetOutput':
    """Convert SetOutput proto to type object."""
    if not proto:
      return None
    obj = SetOutput()
    if proto.args:
      json_list = []
      for j in proto.args:
        json_list.append(CapabilityState.from_proto(j))
      obj.args = json_list
    obj.name = get_proto_value(proto.name)
    obj.py_type = get_proto_value(proto.type)
    return obj


class SetRadialSpeedArgs:
  """Representation of proto message SetRadialSpeedArgs.

   Sets radial velocity and acceleration for following commands.
  """
  velocity: float
  acceleration: float

  def __init__(self, acceleration: float = 0.0, velocity: float = 0.0) -> None:
    self.acceleration = acceleration
    self.velocity = velocity

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.acceleration:
      assert isinstance(self.acceleration, float) or isinstance(self.acceleration, int), 'Wrong type for attribute: acceleration. Expected: float. Got: ' + str(type(self.acceleration)) + '.'
      json_data['acceleration'] = self.acceleration

    if self.velocity:
      assert isinstance(self.velocity, float) or isinstance(self.velocity, int), 'Wrong type for attribute: velocity. Expected: float. Got: ' + str(type(self.velocity)) + '.'
      json_data['velocity'] = self.velocity

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'SetRadialSpeedArgs':
    """Convert JSON to type object."""
    obj = SetRadialSpeedArgs()

    expected_json_keys: List[str] = ['acceleration', 'velocity']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid SetRadialSpeedArgs. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'acceleration' in json_data:
      assert isinstance(json_data['acceleration'], float) or isinstance(json_data['acceleration'], int), 'Wrong type for attribute: acceleration. Expected: float. Got: ' + str(type(json_data['acceleration'])) + '.'
      obj.acceleration = json_data['acceleration']

    if 'velocity' in json_data:
      assert isinstance(json_data['velocity'], float) or isinstance(json_data['velocity'], int), 'Wrong type for attribute: velocity. Expected: float. Got: ' + str(type(json_data['velocity'])) + '.'
      obj.velocity = json_data['velocity']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.SetRadialSpeedArgs) -> 'SetRadialSpeedArgs':
    """Convert SetRadialSpeedArgs proto to type object."""
    if not proto:
      return None
    obj = SetRadialSpeedArgs()
    obj.acceleration = get_proto_value(proto.acceleration)
    obj.velocity = get_proto_value(proto.velocity)
    return obj


class ShiftPerDetection:
  """Representation of proto message ShiftPerDetection.

   ShiftPerDetection encodes any inference of camera shift attached to a
   detected object.
  """
  # Refers to an object if it led to a camera shift detection.
  detection_key: Optional['DetectionKey']

  # Type of camera shift detector. E.g. "initial" meaning a tag shifted from
  # previously seen location, or "calibration" meaning it shifted from
  # calibrated pose.
  shift_type: str

  # Degree of camera shift detected. The unit is pixels. The implementation
  # is allowed to vary by detectors. Valid only if is_object_detected == true.
  shift_amount: float

  # If false, this object was expected but not detected.
  is_object_detected: bool

  def __init__(self, detection_key: Optional['DetectionKey'] = None, is_object_detected: bool = False, shift_amount: float = 0.0, shift_type: str = '') -> None:
    self.detection_key = detection_key
    self.is_object_detected = is_object_detected
    self.shift_amount = shift_amount
    self.shift_type = shift_type

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.detection_key:
      assert self.detection_key.__class__.__name__ == 'DetectionKey', 'Wrong type for attribute: detection_key. Expected: DetectionKey. Got: ' + str(type(self.detection_key)) + '.'
      json_data['detectionKey'] = self.detection_key.to_json()

    if self.is_object_detected:
      assert isinstance(self.is_object_detected, bool), 'Wrong type for attribute: is_object_detected. Expected: bool. Got: ' + str(type(self.is_object_detected)) + '.'
      json_data['isObjectDetected'] = self.is_object_detected

    if self.shift_amount:
      assert isinstance(self.shift_amount, float) or isinstance(self.shift_amount, int), 'Wrong type for attribute: shift_amount. Expected: float. Got: ' + str(type(self.shift_amount)) + '.'
      json_data['shiftAmount'] = self.shift_amount

    if self.shift_type:
      assert isinstance(self.shift_type, str), 'Wrong type for attribute: shift_type. Expected: str. Got: ' + str(type(self.shift_type)) + '.'
      json_data['shiftType'] = self.shift_type

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'ShiftPerDetection':
    """Convert JSON to type object."""
    obj = ShiftPerDetection()

    expected_json_keys: List[str] = ['detectionKey', 'isObjectDetected', 'shiftAmount', 'shiftType']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid ShiftPerDetection. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'detectionKey' in json_data:
      assert isinstance(json_data['detectionKey'], dict), 'Wrong type for attribute: detectionKey. Expected: dict. Got: ' + str(type(json_data['detectionKey'])) + '.'
      obj.detection_key = DetectionKey.from_json(json_data['detectionKey'])

    if 'isObjectDetected' in json_data:
      assert isinstance(json_data['isObjectDetected'], bool), 'Wrong type for attribute: isObjectDetected. Expected: bool. Got: ' + str(type(json_data['isObjectDetected'])) + '.'
      obj.is_object_detected = json_data['isObjectDetected']

    if 'shiftAmount' in json_data:
      assert isinstance(json_data['shiftAmount'], float) or isinstance(json_data['shiftAmount'], int), 'Wrong type for attribute: shiftAmount. Expected: float. Got: ' + str(type(json_data['shiftAmount'])) + '.'
      obj.shift_amount = json_data['shiftAmount']

    if 'shiftType' in json_data:
      assert isinstance(json_data['shiftType'], str), 'Wrong type for attribute: shiftType. Expected: str. Got: ' + str(type(json_data['shiftType'])) + '.'
      obj.shift_type = json_data['shiftType']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.ShiftPerDetection) -> 'ShiftPerDetection':
    """Convert ShiftPerDetection proto to type object."""
    if not proto:
      return None
    obj = ShiftPerDetection()
    obj.detection_key = DetectionKey.from_proto(get_proto_field(proto, 'detection_key'))
    obj.is_object_detected = get_proto_value(proto.is_object_detected)
    obj.shift_amount = get_proto_value(proto.shift_amount)
    obj.shift_type = get_proto_value(proto.shift_type)
    return obj


class SimAction:
  """Representation of proto message SimAction.

   SimAction is the type of environment interaction in SIM for ML research.

  """
  get_all_object_poses: Optional['GetAllObjectPoses']
  set_object_pose: Optional['SetObjectPose']
  delete_object: Optional['DeleteObject']
  set_camera_intrinsics: Optional['SetCameraIntrinsics']
  add_object: Optional['AddObject']
  get_segmented_image: Optional['GetSegmentedImage']

  def __init__(self, add_object: Optional['AddObject'] = None, delete_object: Optional['DeleteObject'] = None, get_all_object_poses: Optional['GetAllObjectPoses'] = None, get_segmented_image: Optional['GetSegmentedImage'] = None, set_camera_intrinsics: Optional['SetCameraIntrinsics'] = None, set_object_pose: Optional['SetObjectPose'] = None) -> None:
    self.add_object = add_object
    self.delete_object = delete_object
    self.get_all_object_poses = get_all_object_poses
    self.get_segmented_image = get_segmented_image
    self.set_camera_intrinsics = set_camera_intrinsics
    self.set_object_pose = set_object_pose

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.add_object:
      assert self.add_object.__class__.__name__ == 'AddObject', 'Wrong type for attribute: add_object. Expected: AddObject. Got: ' + str(type(self.add_object)) + '.'
      json_data['addObject'] = self.add_object.to_json()

    if self.delete_object:
      assert self.delete_object.__class__.__name__ == 'DeleteObject', 'Wrong type for attribute: delete_object. Expected: DeleteObject. Got: ' + str(type(self.delete_object)) + '.'
      json_data['deleteObject'] = self.delete_object.to_json()

    if self.get_all_object_poses:
      assert self.get_all_object_poses.__class__.__name__ == 'GetAllObjectPoses', 'Wrong type for attribute: get_all_object_poses. Expected: GetAllObjectPoses. Got: ' + str(type(self.get_all_object_poses)) + '.'
      json_data['getAllObjectPoses'] = self.get_all_object_poses.to_json()

    if self.get_segmented_image:
      assert self.get_segmented_image.__class__.__name__ == 'GetSegmentedImage', 'Wrong type for attribute: get_segmented_image. Expected: GetSegmentedImage. Got: ' + str(type(self.get_segmented_image)) + '.'
      json_data['getSegmentedImage'] = self.get_segmented_image.to_json()

    if self.set_camera_intrinsics:
      assert self.set_camera_intrinsics.__class__.__name__ == 'SetCameraIntrinsics', 'Wrong type for attribute: set_camera_intrinsics. Expected: SetCameraIntrinsics. Got: ' + str(type(self.set_camera_intrinsics)) + '.'
      json_data['setCameraIntrinsics'] = self.set_camera_intrinsics.to_json()

    if self.set_object_pose:
      assert self.set_object_pose.__class__.__name__ == 'SetObjectPose', 'Wrong type for attribute: set_object_pose. Expected: SetObjectPose. Got: ' + str(type(self.set_object_pose)) + '.'
      json_data['setObjectPose'] = self.set_object_pose.to_json()

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'SimAction':
    """Convert JSON to type object."""
    obj = SimAction()

    expected_json_keys: List[str] = ['addObject', 'deleteObject', 'getAllObjectPoses', 'getSegmentedImage', 'setCameraIntrinsics', 'setObjectPose']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid SimAction. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'addObject' in json_data:
      assert isinstance(json_data['addObject'], dict), 'Wrong type for attribute: addObject. Expected: dict. Got: ' + str(type(json_data['addObject'])) + '.'
      obj.add_object = AddObject.from_json(json_data['addObject'])

    if 'deleteObject' in json_data:
      assert isinstance(json_data['deleteObject'], dict), 'Wrong type for attribute: deleteObject. Expected: dict. Got: ' + str(type(json_data['deleteObject'])) + '.'
      obj.delete_object = DeleteObject.from_json(json_data['deleteObject'])

    if 'getAllObjectPoses' in json_data:
      assert isinstance(json_data['getAllObjectPoses'], dict), 'Wrong type for attribute: getAllObjectPoses. Expected: dict. Got: ' + str(type(json_data['getAllObjectPoses'])) + '.'
      obj.get_all_object_poses = GetAllObjectPoses.from_json(json_data['getAllObjectPoses'])

    if 'getSegmentedImage' in json_data:
      assert isinstance(json_data['getSegmentedImage'], dict), 'Wrong type for attribute: getSegmentedImage. Expected: dict. Got: ' + str(type(json_data['getSegmentedImage'])) + '.'
      obj.get_segmented_image = GetSegmentedImage.from_json(json_data['getSegmentedImage'])

    if 'setCameraIntrinsics' in json_data:
      assert isinstance(json_data['setCameraIntrinsics'], dict), 'Wrong type for attribute: setCameraIntrinsics. Expected: dict. Got: ' + str(type(json_data['setCameraIntrinsics'])) + '.'
      obj.set_camera_intrinsics = SetCameraIntrinsics.from_json(json_data['setCameraIntrinsics'])

    if 'setObjectPose' in json_data:
      assert isinstance(json_data['setObjectPose'], dict), 'Wrong type for attribute: setObjectPose. Expected: dict. Got: ' + str(type(json_data['setObjectPose'])) + '.'
      obj.set_object_pose = SetObjectPose.from_json(json_data['setObjectPose'])

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.SimAction) -> 'SimAction':
    """Convert SimAction proto to type object."""
    if not proto:
      return None
    obj = SimAction()
    obj.add_object = AddObject.from_proto(get_proto_field(proto, 'add_object'))
    obj.delete_object = DeleteObject.from_proto(get_proto_field(proto, 'delete_object'))
    obj.get_all_object_poses = GetAllObjectPoses.from_proto(get_proto_field(proto, 'get_all_object_poses'))
    obj.get_segmented_image = GetSegmentedImage.from_proto(get_proto_field(proto, 'get_segmented_image'))
    obj.set_camera_intrinsics = SetCameraIntrinsics.from_proto(get_proto_field(proto, 'set_camera_intrinsics'))
    obj.set_object_pose = SetObjectPose.from_proto(get_proto_field(proto, 'set_object_pose'))
    return obj


class SimInstanceSegmentation:
  """Representation of proto message SimInstanceSegmentation.

   SimInstanceSegmentation is the object sent when a SIM instance segmentation
   is requested.

  """
  # sim_ts is the internal SIM time if the SIM is sped up.
  sim_ts: int

  # image_path is the relative path to the image saved by the SIM.
  image_path: str

  # relation is the key-value objectID mapping in the SIM scene.
  relation: List['KeyValue']

  def __init__(self, image_path: str = '', relation: Optional[List['KeyValue']] = None, sim_ts: int = 0) -> None:
    self.image_path = image_path
    if relation is None:
      self.relation = []
    else:
      self.relation = relation
    self.sim_ts = sim_ts

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.image_path:
      assert isinstance(self.image_path, str), 'Wrong type for attribute: image_path. Expected: str. Got: ' + str(type(self.image_path)) + '.'
      json_data['imagePath'] = self.image_path

    if self.relation:
      assert isinstance(self.relation, list), 'Wrong type for attribute: relation. Expected: list. Got: ' + str(type(self.relation)) + '.'
      obj_list = []
      for item in self.relation:
        obj_list.append(item.to_json())
      json_data['relation'] = obj_list

    if self.sim_ts:
      assert isinstance(self.sim_ts, int), 'Wrong type for attribute: sim_ts. Expected: int. Got: ' + str(type(self.sim_ts)) + '.'
      json_data['simTS'] = self.sim_ts

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'SimInstanceSegmentation':
    """Convert JSON to type object."""
    obj = SimInstanceSegmentation()
    json_list: List[Any]

    expected_json_keys: List[str] = ['imagePath', 'relation', 'simTS']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid SimInstanceSegmentation. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'imagePath' in json_data:
      assert isinstance(json_data['imagePath'], str), 'Wrong type for attribute: imagePath. Expected: str. Got: ' + str(type(json_data['imagePath'])) + '.'
      obj.image_path = json_data['imagePath']

    if 'relation' in json_data:
      assert isinstance(json_data['relation'], list), 'Wrong type for attribute: relation. Expected: list. Got: ' + str(type(json_data['relation'])) + '.'
      json_list = []
      for j in json_data['relation']:
        json_list.append(KeyValue.from_json(j))
      obj.relation = json_list

    if 'simTS' in json_data:
      assert isinstance(json_data['simTS'], int), 'Wrong type for attribute: simTS. Expected: int. Got: ' + str(type(json_data['simTS'])) + '.'
      obj.sim_ts = json_data['simTS']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.SimInstanceSegmentation) -> 'SimInstanceSegmentation':
    """Convert SimInstanceSegmentation proto to type object."""
    if not proto:
      return None
    obj = SimInstanceSegmentation()
    obj.image_path = get_proto_value(proto.image_path)
    if proto.relation:
      json_list = []
      for j in proto.relation:
        json_list.append(KeyValue.from_proto(j))
      obj.relation = json_list
    obj.sim_ts = get_proto_value(proto.sim_ts)
    return obj


class SimState:
  """Representation of proto message SimState.

   SimState is the list of object states and timestamp
   in SIM for ML research.

  """
  # sim_ts is the internal SIM time if the SIM is sped up.
  sim_ts: int

  # object_state is the list of SIM object states.
  object_state: List['ObjectState']

  def __init__(self, object_state: Optional[List['ObjectState']] = None, sim_ts: int = 0) -> None:
    if object_state is None:
      self.object_state = []
    else:
      self.object_state = object_state
    self.sim_ts = sim_ts

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.object_state:
      assert isinstance(self.object_state, list), 'Wrong type for attribute: object_state. Expected: list. Got: ' + str(type(self.object_state)) + '.'
      obj_list = []
      for item in self.object_state:
        obj_list.append(item.to_json())
      json_data['objectState'] = obj_list

    if self.sim_ts:
      assert isinstance(self.sim_ts, int), 'Wrong type for attribute: sim_ts. Expected: int. Got: ' + str(type(self.sim_ts)) + '.'
      json_data['simTS'] = self.sim_ts

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'SimState':
    """Convert JSON to type object."""
    obj = SimState()
    json_list: List[Any]

    expected_json_keys: List[str] = ['objectState', 'simTS']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid SimState. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'objectState' in json_data:
      assert isinstance(json_data['objectState'], list), 'Wrong type for attribute: objectState. Expected: list. Got: ' + str(type(json_data['objectState'])) + '.'
      json_list = []
      for j in json_data['objectState']:
        json_list.append(ObjectState.from_json(j))
      obj.object_state = json_list

    if 'simTS' in json_data:
      assert isinstance(json_data['simTS'], int), 'Wrong type for attribute: simTS. Expected: int. Got: ' + str(type(json_data['simTS'])) + '.'
      obj.sim_ts = json_data['simTS']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.SimState) -> 'SimState':
    """Convert SimState proto to type object."""
    if not proto:
      return None
    obj = SimState()
    if proto.object_state:
      json_list = []
      for j in proto.object_state:
        json_list.append(ObjectState.from_proto(j))
      obj.object_state = json_list
    obj.sim_ts = get_proto_value(proto.sim_ts)
    return obj


class SleepArgs:
  """Representation of proto message SleepArgs.

   Sleeps for the given time. Sleeps (e.g. 200msec) may not be effective if
   the latency of the robot reporting that a command is complete is on the
   same order.
  """
  seconds: float

  def __init__(self, seconds: float = 0.0) -> None:
    self.seconds = seconds

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.seconds:
      assert isinstance(self.seconds, float) or isinstance(self.seconds, int), 'Wrong type for attribute: seconds. Expected: float. Got: ' + str(type(self.seconds)) + '.'
      json_data['seconds'] = self.seconds

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'SleepArgs':
    """Convert JSON to type object."""
    obj = SleepArgs()

    expected_json_keys: List[str] = ['seconds']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid SleepArgs. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'seconds' in json_data:
      assert isinstance(json_data['seconds'], float) or isinstance(json_data['seconds'], int), 'Wrong type for attribute: seconds. Expected: float. Got: ' + str(type(json_data['seconds'])) + '.'
      obj.seconds = json_data['seconds']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.SleepArgs) -> 'SleepArgs':
    """Convert SleepArgs proto to type object."""
    if not proto:
      return None
    obj = SleepArgs()
    obj.seconds = get_proto_value(proto.seconds)
    return obj


class Snapshot:
  """Representation of proto message Snapshot.

   Snapshot is the client's view of the robot state at a given moment.
   Design doc:
  """
  # The application source that generates this snapshot, such as PyReach.
  source: str

  # DeviceData needed to reconstruct this snapshot.
  device_data_refs: List['DeviceDataRef']

  # Response device data references needed to reconstruct the snapshot with
  # action ids.
  responses: List['SnapshotResponse']

  # PyReach gym specific fields
  # The gym environment id.
  gym_env_id: str

  # The gym run id.
  gym_run_id: str

  # The Gym episode number starting with 1 for the first episode.  Each time
  # Each time env.reset() is called, the episode number is incremented.
  gym_episode: int

  # The Gym step number for the current episode starting with 0 for the first
  # step.
  gym_step: int

  # The reward returned from the call to env.step().  If env.reset() is called,
  # 0.0 is returned.
  gym_reward: float

  # The boolean flag returned from the call to env.step().  If env.reset() is
  # called, done is set to False.
  gym_done: bool

  # Actions.
  gym_actions: List['GymAction']

  def __init__(self, device_data_refs: Optional[List['DeviceDataRef']] = None, gym_actions: Optional[List['GymAction']] = None, gym_done: bool = False, gym_env_id: str = '', gym_episode: int = 0, gym_reward: float = 0.0, gym_run_id: str = '', gym_step: int = 0, responses: Optional[List['SnapshotResponse']] = None, source: str = '') -> None:
    if device_data_refs is None:
      self.device_data_refs = []
    else:
      self.device_data_refs = device_data_refs
    if gym_actions is None:
      self.gym_actions = []
    else:
      self.gym_actions = gym_actions
    self.gym_done = gym_done
    self.gym_env_id = gym_env_id
    self.gym_episode = gym_episode
    self.gym_reward = gym_reward
    self.gym_run_id = gym_run_id
    self.gym_step = gym_step
    if responses is None:
      self.responses = []
    else:
      self.responses = responses
    self.source = source

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.device_data_refs:
      assert isinstance(self.device_data_refs, list), 'Wrong type for attribute: device_data_refs. Expected: list. Got: ' + str(type(self.device_data_refs)) + '.'
      obj_list = []
      for item in self.device_data_refs:
        obj_list.append(item.to_json())
      json_data['deviceDataRefs'] = obj_list

    if self.gym_actions:
      assert isinstance(self.gym_actions, list), 'Wrong type for attribute: gym_actions. Expected: list. Got: ' + str(type(self.gym_actions)) + '.'
      obj_list = []
      for item in self.gym_actions:
        obj_list.append(item.to_json())
      json_data['gymActions'] = obj_list

    if self.gym_done:
      assert isinstance(self.gym_done, bool), 'Wrong type for attribute: gym_done. Expected: bool. Got: ' + str(type(self.gym_done)) + '.'
      json_data['gymDone'] = self.gym_done

    if self.gym_env_id:
      assert isinstance(self.gym_env_id, str), 'Wrong type for attribute: gym_env_id. Expected: str. Got: ' + str(type(self.gym_env_id)) + '.'
      json_data['gymEnvId'] = self.gym_env_id

    if self.gym_episode:
      assert isinstance(self.gym_episode, int), 'Wrong type for attribute: gym_episode. Expected: int. Got: ' + str(type(self.gym_episode)) + '.'
      json_data['gymEpisode'] = self.gym_episode

    if self.gym_reward:
      assert isinstance(self.gym_reward, float) or isinstance(self.gym_reward, int), 'Wrong type for attribute: gym_reward. Expected: float. Got: ' + str(type(self.gym_reward)) + '.'
      json_data['gymReward'] = self.gym_reward

    if self.gym_run_id:
      assert isinstance(self.gym_run_id, str), 'Wrong type for attribute: gym_run_id. Expected: str. Got: ' + str(type(self.gym_run_id)) + '.'
      json_data['gymRunId'] = self.gym_run_id

    if self.gym_step:
      assert isinstance(self.gym_step, int), 'Wrong type for attribute: gym_step. Expected: int. Got: ' + str(type(self.gym_step)) + '.'
      json_data['gymStep'] = self.gym_step

    if self.responses:
      assert isinstance(self.responses, list), 'Wrong type for attribute: responses. Expected: list. Got: ' + str(type(self.responses)) + '.'
      obj_list = []
      for item in self.responses:
        obj_list.append(item.to_json())
      json_data['responses'] = obj_list

    if self.source:
      assert isinstance(self.source, str), 'Wrong type for attribute: source. Expected: str. Got: ' + str(type(self.source)) + '.'
      json_data['source'] = self.source

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'Snapshot':
    """Convert JSON to type object."""
    obj = Snapshot()
    json_list: List[Any]

    expected_json_keys: List[str] = ['deviceDataRefs', 'gymActions', 'gymDone', 'gymEnvId', 'gymEpisode', 'gymReward', 'gymRunId', 'gymStep', 'responses', 'source']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid Snapshot. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'deviceDataRefs' in json_data:
      assert isinstance(json_data['deviceDataRefs'], list), 'Wrong type for attribute: deviceDataRefs. Expected: list. Got: ' + str(type(json_data['deviceDataRefs'])) + '.'
      json_list = []
      for j in json_data['deviceDataRefs']:
        json_list.append(DeviceDataRef.from_json(j))
      obj.device_data_refs = json_list

    if 'gymActions' in json_data:
      assert isinstance(json_data['gymActions'], list), 'Wrong type for attribute: gymActions. Expected: list. Got: ' + str(type(json_data['gymActions'])) + '.'
      json_list = []
      for j in json_data['gymActions']:
        json_list.append(GymAction.from_json(j))
      obj.gym_actions = json_list

    if 'gymDone' in json_data:
      assert isinstance(json_data['gymDone'], bool), 'Wrong type for attribute: gymDone. Expected: bool. Got: ' + str(type(json_data['gymDone'])) + '.'
      obj.gym_done = json_data['gymDone']

    if 'gymEnvId' in json_data:
      assert isinstance(json_data['gymEnvId'], str), 'Wrong type for attribute: gymEnvId. Expected: str. Got: ' + str(type(json_data['gymEnvId'])) + '.'
      obj.gym_env_id = json_data['gymEnvId']

    if 'gymEpisode' in json_data:
      assert isinstance(json_data['gymEpisode'], int), 'Wrong type for attribute: gymEpisode. Expected: int. Got: ' + str(type(json_data['gymEpisode'])) + '.'
      obj.gym_episode = json_data['gymEpisode']

    if 'gymReward' in json_data:
      assert isinstance(json_data['gymReward'], float) or isinstance(json_data['gymReward'], int), 'Wrong type for attribute: gymReward. Expected: float. Got: ' + str(type(json_data['gymReward'])) + '.'
      obj.gym_reward = json_data['gymReward']

    if 'gymRunId' in json_data:
      assert isinstance(json_data['gymRunId'], str), 'Wrong type for attribute: gymRunId. Expected: str. Got: ' + str(type(json_data['gymRunId'])) + '.'
      obj.gym_run_id = json_data['gymRunId']

    if 'gymStep' in json_data:
      assert isinstance(json_data['gymStep'], int), 'Wrong type for attribute: gymStep. Expected: int. Got: ' + str(type(json_data['gymStep'])) + '.'
      obj.gym_step = json_data['gymStep']

    if 'responses' in json_data:
      assert isinstance(json_data['responses'], list), 'Wrong type for attribute: responses. Expected: list. Got: ' + str(type(json_data['responses'])) + '.'
      json_list = []
      for j in json_data['responses']:
        json_list.append(SnapshotResponse.from_json(j))
      obj.responses = json_list

    if 'source' in json_data:
      assert isinstance(json_data['source'], str), 'Wrong type for attribute: source. Expected: str. Got: ' + str(type(json_data['source'])) + '.'
      obj.source = json_data['source']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.Snapshot) -> 'Snapshot':
    """Convert Snapshot proto to type object."""
    if not proto:
      return None
    obj = Snapshot()
    if proto.device_data_refs:
      json_list = []
      for j in proto.device_data_refs:
        json_list.append(DeviceDataRef.from_proto(j))
      obj.device_data_refs = json_list
    if proto.gym_actions:
      json_list = []
      for j in proto.gym_actions:
        json_list.append(GymAction.from_proto(j))
      obj.gym_actions = json_list
    obj.gym_done = get_proto_value(proto.gym_done)
    obj.gym_env_id = get_proto_value(proto.gym_env_id)
    obj.gym_episode = get_proto_value(proto.gym_episode)
    obj.gym_reward = get_proto_value(proto.gym_reward)
    obj.gym_run_id = get_proto_value(proto.gym_run_id)
    obj.gym_step = get_proto_value(proto.gym_step)
    if proto.responses:
      json_list = []
      for j in proto.responses:
        json_list.append(SnapshotResponse.from_proto(j))
      obj.responses = json_list
    obj.source = get_proto_value(proto.source)
    return obj


class SnapshotResponse:
  """Representation of proto message SnapshotResponse.

   SnapshotResponse stores response data in a snapshot.
  """
  device_data_ref: Optional['DeviceDataRef']
  cid: int
  status: Optional['Status']
  gym_element_type: str
  gym_config_name: str

  def __init__(self, cid: int = 0, device_data_ref: Optional['DeviceDataRef'] = None, gym_config_name: str = '', gym_element_type: str = '', status: Optional['Status'] = None) -> None:
    self.cid = cid
    self.device_data_ref = device_data_ref
    self.gym_config_name = gym_config_name
    self.gym_element_type = gym_element_type
    self.status = status

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.cid:
      assert isinstance(self.cid, int), 'Wrong type for attribute: cid. Expected: int. Got: ' + str(type(self.cid)) + '.'
      json_data['cid'] = self.cid

    if self.device_data_ref:
      assert self.device_data_ref.__class__.__name__ == 'DeviceDataRef', 'Wrong type for attribute: device_data_ref. Expected: DeviceDataRef. Got: ' + str(type(self.device_data_ref)) + '.'
      json_data['deviceDataRef'] = self.device_data_ref.to_json()

    if self.gym_config_name:
      assert isinstance(self.gym_config_name, str), 'Wrong type for attribute: gym_config_name. Expected: str. Got: ' + str(type(self.gym_config_name)) + '.'
      json_data['gymConfigName'] = self.gym_config_name

    if self.gym_element_type:
      assert isinstance(self.gym_element_type, str), 'Wrong type for attribute: gym_element_type. Expected: str. Got: ' + str(type(self.gym_element_type)) + '.'
      json_data['gymElementType'] = self.gym_element_type

    if self.status:
      assert self.status.__class__.__name__ == 'Status', 'Wrong type for attribute: status. Expected: Status. Got: ' + str(type(self.status)) + '.'
      json_data['status'] = self.status.to_json()

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'SnapshotResponse':
    """Convert JSON to type object."""
    obj = SnapshotResponse()

    expected_json_keys: List[str] = ['cid', 'deviceDataRef', 'gymConfigName', 'gymElementType', 'status']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid SnapshotResponse. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'cid' in json_data:
      assert isinstance(json_data['cid'], int), 'Wrong type for attribute: cid. Expected: int. Got: ' + str(type(json_data['cid'])) + '.'
      obj.cid = json_data['cid']

    if 'deviceDataRef' in json_data:
      assert isinstance(json_data['deviceDataRef'], dict), 'Wrong type for attribute: deviceDataRef. Expected: dict. Got: ' + str(type(json_data['deviceDataRef'])) + '.'
      obj.device_data_ref = DeviceDataRef.from_json(json_data['deviceDataRef'])

    if 'gymConfigName' in json_data:
      assert isinstance(json_data['gymConfigName'], str), 'Wrong type for attribute: gymConfigName. Expected: str. Got: ' + str(type(json_data['gymConfigName'])) + '.'
      obj.gym_config_name = json_data['gymConfigName']

    if 'gymElementType' in json_data:
      assert isinstance(json_data['gymElementType'], str), 'Wrong type for attribute: gymElementType. Expected: str. Got: ' + str(type(json_data['gymElementType'])) + '.'
      obj.gym_element_type = json_data['gymElementType']

    if 'status' in json_data:
      assert isinstance(json_data['status'], dict), 'Wrong type for attribute: status. Expected: dict. Got: ' + str(type(json_data['status'])) + '.'
      obj.status = Status.from_json(json_data['status'])

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.SnapshotResponse) -> 'SnapshotResponse':
    """Convert SnapshotResponse proto to type object."""
    if not proto:
      return None
    obj = SnapshotResponse()
    obj.cid = get_proto_value(proto.cid)
    obj.device_data_ref = DeviceDataRef.from_proto(get_proto_field(proto, 'device_data_ref'))
    obj.gym_config_name = get_proto_value(proto.gym_config_name)
    obj.gym_element_type = get_proto_value(proto.gym_element_type)
    obj.status = Status.from_proto(get_proto_field(proto, 'status'))
    return obj


class SourceImage:
  """Representation of proto message SourceImage.

   SourceImage uniquely identifies a past color or color-depth (rgbd) image.
   It does not differentiate between color and depth image data, but
   assumes that rgbd image would be aligned - and annotations apply to either.
  """
  # Timestamp for original message.
  ts: int

  # Device type for original message.
  device_type: str

  # Device name for original message.
  device_name: str

  # Data type for original message.
  data_type: str

  def __init__(self, data_type: str = '', device_name: str = '', device_type: str = '', ts: int = 0) -> None:
    self.data_type = data_type
    self.device_name = device_name
    self.device_type = device_type
    self.ts = ts

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.data_type:
      assert isinstance(self.data_type, str), 'Wrong type for attribute: data_type. Expected: str. Got: ' + str(type(self.data_type)) + '.'
      json_data['dataType'] = self.data_type

    if self.device_name:
      assert isinstance(self.device_name, str), 'Wrong type for attribute: device_name. Expected: str. Got: ' + str(type(self.device_name)) + '.'
      json_data['deviceName'] = self.device_name

    if self.device_type:
      assert isinstance(self.device_type, str), 'Wrong type for attribute: device_type. Expected: str. Got: ' + str(type(self.device_type)) + '.'
      json_data['deviceType'] = self.device_type

    if self.ts:
      assert isinstance(self.ts, int), 'Wrong type for attribute: ts. Expected: int. Got: ' + str(type(self.ts)) + '.'
      json_data['ts'] = self.ts

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'SourceImage':
    """Convert JSON to type object."""
    obj = SourceImage()

    expected_json_keys: List[str] = ['dataType', 'deviceName', 'deviceType', 'ts']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid SourceImage. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'dataType' in json_data:
      assert isinstance(json_data['dataType'], str), 'Wrong type for attribute: dataType. Expected: str. Got: ' + str(type(json_data['dataType'])) + '.'
      obj.data_type = json_data['dataType']

    if 'deviceName' in json_data:
      assert isinstance(json_data['deviceName'], str), 'Wrong type for attribute: deviceName. Expected: str. Got: ' + str(type(json_data['deviceName'])) + '.'
      obj.device_name = json_data['deviceName']

    if 'deviceType' in json_data:
      assert isinstance(json_data['deviceType'], str), 'Wrong type for attribute: deviceType. Expected: str. Got: ' + str(type(json_data['deviceType'])) + '.'
      obj.device_type = json_data['deviceType']

    if 'ts' in json_data:
      assert isinstance(json_data['ts'], int), 'Wrong type for attribute: ts. Expected: int. Got: ' + str(type(json_data['ts'])) + '.'
      obj.ts = json_data['ts']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.SourceImage) -> 'SourceImage':
    """Convert SourceImage proto to type object."""
    if not proto:
      return None
    obj = SourceImage()
    obj.data_type = get_proto_value(proto.data_type)
    obj.device_name = get_proto_value(proto.device_name)
    obj.device_type = get_proto_value(proto.device_type)
    obj.ts = get_proto_value(proto.ts)
    return obj


class Status:
  """Representation of proto message Status.

   Status is a ScriptEngine or cmd-status or downlink-status status.
  """
  status: str

  # script is the name of the script/cmd/downlink that the status refers to.
  script: str
  error: str
  progress: float
  message: str
  code: int

  def __init__(self, code: int = 0, error: str = '', message: str = '', progress: float = 0.0, script: str = '', status: str = '') -> None:
    self.code = code
    self.error = error
    self.message = message
    self.progress = progress
    self.script = script
    self.status = status

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.code:
      assert isinstance(self.code, int), 'Wrong type for attribute: code. Expected: int. Got: ' + str(type(self.code)) + '.'
      json_data['code'] = self.code

    if self.error:
      assert isinstance(self.error, str), 'Wrong type for attribute: error. Expected: str. Got: ' + str(type(self.error)) + '.'
      json_data['error'] = self.error

    if self.message:
      assert isinstance(self.message, str), 'Wrong type for attribute: message. Expected: str. Got: ' + str(type(self.message)) + '.'
      json_data['message'] = self.message

    if self.progress:
      assert isinstance(self.progress, float) or isinstance(self.progress, int), 'Wrong type for attribute: progress. Expected: float. Got: ' + str(type(self.progress)) + '.'
      json_data['progress'] = self.progress

    if self.script:
      assert isinstance(self.script, str), 'Wrong type for attribute: script. Expected: str. Got: ' + str(type(self.script)) + '.'
      json_data['script'] = self.script

    if self.status:
      assert isinstance(self.status, str), 'Wrong type for attribute: status. Expected: str. Got: ' + str(type(self.status)) + '.'
      json_data['status'] = self.status

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'Status':
    """Convert JSON to type object."""
    obj = Status()

    expected_json_keys: List[str] = ['code', 'error', 'message', 'progress', 'script', 'status']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid Status. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'code' in json_data:
      assert isinstance(json_data['code'], int), 'Wrong type for attribute: code. Expected: int. Got: ' + str(type(json_data['code'])) + '.'
      obj.code = json_data['code']

    if 'error' in json_data:
      assert isinstance(json_data['error'], str), 'Wrong type for attribute: error. Expected: str. Got: ' + str(type(json_data['error'])) + '.'
      obj.error = json_data['error']

    if 'message' in json_data:
      assert isinstance(json_data['message'], str), 'Wrong type for attribute: message. Expected: str. Got: ' + str(type(json_data['message'])) + '.'
      obj.message = json_data['message']

    if 'progress' in json_data:
      assert isinstance(json_data['progress'], float) or isinstance(json_data['progress'], int), 'Wrong type for attribute: progress. Expected: float. Got: ' + str(type(json_data['progress'])) + '.'
      obj.progress = json_data['progress']

    if 'script' in json_data:
      assert isinstance(json_data['script'], str), 'Wrong type for attribute: script. Expected: str. Got: ' + str(type(json_data['script'])) + '.'
      obj.script = json_data['script']

    if 'status' in json_data:
      assert isinstance(json_data['status'], str), 'Wrong type for attribute: status. Expected: str. Got: ' + str(type(json_data['status'])) + '.'
      obj.status = json_data['status']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.Status) -> 'Status':
    """Convert Status proto to type object."""
    if not proto:
      return None
    obj = Status()
    obj.code = get_proto_value(proto.code)
    obj.error = get_proto_value(proto.error)
    obj.message = get_proto_value(proto.message)
    obj.progress = get_proto_value(proto.progress)
    obj.script = get_proto_value(proto.script)
    obj.status = get_proto_value(proto.status)
    return obj


class StopJArgs:
  """Representation of proto message StopJArgs.

   Decelerates all joint speeds to zero. The deceleration, if specified,
   overrides the acceleration set in SetRadialSpeed for this command only.
  """
  deceleration: float

  def __init__(self, deceleration: float = 0.0) -> None:
    self.deceleration = deceleration

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.deceleration:
      assert isinstance(self.deceleration, float) or isinstance(self.deceleration, int), 'Wrong type for attribute: deceleration. Expected: float. Got: ' + str(type(self.deceleration)) + '.'
      json_data['deceleration'] = self.deceleration

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'StopJArgs':
    """Convert JSON to type object."""
    obj = StopJArgs()

    expected_json_keys: List[str] = ['deceleration']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid StopJArgs. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'deceleration' in json_data:
      assert isinstance(json_data['deceleration'], float) or isinstance(json_data['deceleration'], int), 'Wrong type for attribute: deceleration. Expected: float. Got: ' + str(type(json_data['deceleration'])) + '.'
      obj.deceleration = json_data['deceleration']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.StopJArgs) -> 'StopJArgs':
    """Convert StopJArgs proto to type object."""
    if not proto:
      return None
    obj = StopJArgs()
    obj.deceleration = get_proto_value(proto.deceleration)
    return obj


class SyncArgs:
  """Representation of proto message SyncArgs.

   SyncArgs contains the arguments for the Sync command, which causes
   all arms in a multi-arm system to wait until all arms have reached
   a Sync statement. Times out and aborts after the given number of seconds.
  """
  seconds: float

  def __init__(self, seconds: float = 0.0) -> None:
    self.seconds = seconds

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.seconds:
      assert isinstance(self.seconds, float) or isinstance(self.seconds, int), 'Wrong type for attribute: seconds. Expected: float. Got: ' + str(type(self.seconds)) + '.'
      json_data['seconds'] = self.seconds

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'SyncArgs':
    """Convert JSON to type object."""
    obj = SyncArgs()

    expected_json_keys: List[str] = ['seconds']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid SyncArgs. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'seconds' in json_data:
      assert isinstance(json_data['seconds'], float) or isinstance(json_data['seconds'], int), 'Wrong type for attribute: seconds. Expected: float. Got: ' + str(type(json_data['seconds'])) + '.'
      obj.seconds = json_data['seconds']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.SyncArgs) -> 'SyncArgs':
    """Convert SyncArgs proto to type object."""
    if not proto:
      return None
    obj = SyncArgs()
    obj.seconds = get_proto_value(proto.seconds)
    return obj


class TextInstruction:
  """Representation of proto message TextInstruction.

   TextInstruction is the description of an instruction for a task.
  """
  # The intent of the instruction.
  intent: str

  # The success type of the instruction aka what makes this particular
  # instruction successful.
  success_type: str

  # The success detection the system may use to define success,
  # if one is available.
  success_detection: str

  # The natural language instruction to be presented to the user.
  instruction: str

  # UID is a UUID for the instruction.
  uid: str

  # ID that identifies the list of instructions that this instruction is a
  # part of. Used when it is important to identify that an instruction is part
  # of a specific group of instructions. Design doc:
  supertask_id: str

  def __init__(self, instruction: str = '', intent: str = '', success_detection: str = '', success_type: str = '', supertask_id: str = '', uid: str = '') -> None:
    self.instruction = instruction
    self.intent = intent
    self.success_detection = success_detection
    self.success_type = success_type
    self.supertask_id = supertask_id
    self.uid = uid

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.instruction:
      assert isinstance(self.instruction, str), 'Wrong type for attribute: instruction. Expected: str. Got: ' + str(type(self.instruction)) + '.'
      json_data['instruction'] = self.instruction

    if self.intent:
      assert isinstance(self.intent, str), 'Wrong type for attribute: intent. Expected: str. Got: ' + str(type(self.intent)) + '.'
      json_data['intent'] = self.intent

    if self.success_detection:
      assert isinstance(self.success_detection, str), 'Wrong type for attribute: success_detection. Expected: str. Got: ' + str(type(self.success_detection)) + '.'
      json_data['successDetection'] = self.success_detection

    if self.success_type:
      assert isinstance(self.success_type, str), 'Wrong type for attribute: success_type. Expected: str. Got: ' + str(type(self.success_type)) + '.'
      json_data['successType'] = self.success_type

    if self.supertask_id:
      assert isinstance(self.supertask_id, str), 'Wrong type for attribute: supertask_id. Expected: str. Got: ' + str(type(self.supertask_id)) + '.'
      json_data['supertaskID'] = self.supertask_id

    if self.uid:
      assert isinstance(self.uid, str), 'Wrong type for attribute: uid. Expected: str. Got: ' + str(type(self.uid)) + '.'
      json_data['uid'] = self.uid

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'TextInstruction':
    """Convert JSON to type object."""
    obj = TextInstruction()

    expected_json_keys: List[str] = ['instruction', 'intent', 'successDetection', 'successType', 'supertaskID', 'uid']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid TextInstruction. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'instruction' in json_data:
      assert isinstance(json_data['instruction'], str), 'Wrong type for attribute: instruction. Expected: str. Got: ' + str(type(json_data['instruction'])) + '.'
      obj.instruction = json_data['instruction']

    if 'intent' in json_data:
      assert isinstance(json_data['intent'], str), 'Wrong type for attribute: intent. Expected: str. Got: ' + str(type(json_data['intent'])) + '.'
      obj.intent = json_data['intent']

    if 'successDetection' in json_data:
      assert isinstance(json_data['successDetection'], str), 'Wrong type for attribute: successDetection. Expected: str. Got: ' + str(type(json_data['successDetection'])) + '.'
      obj.success_detection = json_data['successDetection']

    if 'successType' in json_data:
      assert isinstance(json_data['successType'], str), 'Wrong type for attribute: successType. Expected: str. Got: ' + str(type(json_data['successType'])) + '.'
      obj.success_type = json_data['successType']

    if 'supertaskID' in json_data:
      assert isinstance(json_data['supertaskID'], str), 'Wrong type for attribute: supertaskID. Expected: str. Got: ' + str(type(json_data['supertaskID'])) + '.'
      obj.supertask_id = json_data['supertaskID']

    if 'uid' in json_data:
      assert isinstance(json_data['uid'], str), 'Wrong type for attribute: uid. Expected: str. Got: ' + str(type(json_data['uid'])) + '.'
      obj.uid = json_data['uid']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.TextInstruction) -> 'TextInstruction':
    """Convert TextInstruction proto to type object."""
    if not proto:
      return None
    obj = TextInstruction()
    obj.instruction = get_proto_value(proto.instruction)
    obj.intent = get_proto_value(proto.intent)
    obj.success_detection = get_proto_value(proto.success_detection)
    obj.success_type = get_proto_value(proto.success_type)
    obj.supertask_id = get_proto_value(proto.supertask_id)
    obj.uid = get_proto_value(proto.uid)
    return obj


class ToolState:
  """Representation of proto message ToolState.

   ToolState represents data from dataType == "tool-state" or
   "tool-state-update".
  """
  vacuum_level_pa: float
  on: bool

  def __init__(self, on: bool = False, vacuum_level_pa: float = 0.0) -> None:
    self.on = on
    self.vacuum_level_pa = vacuum_level_pa

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.on:
      assert isinstance(self.on, bool), 'Wrong type for attribute: on. Expected: bool. Got: ' + str(type(self.on)) + '.'
      json_data['on'] = self.on

    if self.vacuum_level_pa:
      assert isinstance(self.vacuum_level_pa, float) or isinstance(self.vacuum_level_pa, int), 'Wrong type for attribute: vacuum_level_pa. Expected: float. Got: ' + str(type(self.vacuum_level_pa)) + '.'
      json_data['vacuumLevelPa'] = self.vacuum_level_pa

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'ToolState':
    """Convert JSON to type object."""
    obj = ToolState()

    expected_json_keys: List[str] = ['on', 'vacuumLevelPa']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid ToolState. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'on' in json_data:
      assert isinstance(json_data['on'], bool), 'Wrong type for attribute: on. Expected: bool. Got: ' + str(type(json_data['on'])) + '.'
      obj.on = json_data['on']

    if 'vacuumLevelPa' in json_data:
      assert isinstance(json_data['vacuumLevelPa'], float) or isinstance(json_data['vacuumLevelPa'], int), 'Wrong type for attribute: vacuumLevelPa. Expected: float. Got: ' + str(type(json_data['vacuumLevelPa'])) + '.'
      obj.vacuum_level_pa = json_data['vacuumLevelPa']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.ToolState) -> 'ToolState':
    """Convert ToolState proto to type object."""
    if not proto:
      return None
    obj = ToolState()
    obj.on = get_proto_value(proto.on)
    obj.vacuum_level_pa = get_proto_value(proto.vacuum_level_pa)
    return obj


class TorqueLimits:
  """Representation of proto message TorqueLimits.

   TorqueLimits are torque limits to use with Limits in waypoints.
  """
  maximum: List[float]
  minimum: List[float]

  def __init__(self, maximum: Optional[List[float]] = None, minimum: Optional[List[float]] = None) -> None:
    if maximum is None:
      self.maximum = []
    else:
      self.maximum = maximum
    if minimum is None:
      self.minimum = []
    else:
      self.minimum = minimum

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.maximum:
      assert isinstance(self.maximum, list), 'Wrong type for attribute: maximum. Expected: list. Got: ' + str(type(self.maximum)) + '.'
      json_data['maximum'] = self.maximum

    if self.minimum:
      assert isinstance(self.minimum, list), 'Wrong type for attribute: minimum. Expected: list. Got: ' + str(type(self.minimum)) + '.'
      json_data['minimum'] = self.minimum

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'TorqueLimits':
    """Convert JSON to type object."""
    obj = TorqueLimits()
    json_list: List[Any]

    expected_json_keys: List[str] = ['maximum', 'minimum']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid TorqueLimits. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'maximum' in json_data:
      assert isinstance(json_data['maximum'], list), 'Wrong type for attribute: maximum. Expected: list. Got: ' + str(type(json_data['maximum'])) + '.'
      json_list = []
      for j in json_data['maximum']:
        json_list.append(j)
      obj.maximum = json_list

    if 'minimum' in json_data:
      assert isinstance(json_data['minimum'], list), 'Wrong type for attribute: minimum. Expected: list. Got: ' + str(type(json_data['minimum'])) + '.'
      json_list = []
      for j in json_data['minimum']:
        json_list.append(j)
      obj.minimum = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.TorqueLimits) -> 'TorqueLimits':
    """Convert TorqueLimits proto to type object."""
    if not proto:
      return None
    obj = TorqueLimits()
    if proto.maximum:
      json_list = []
      for j in proto.maximum:
        json_list.append(j)
      obj.maximum = json_list
    if proto.minimum:
      json_list = []
      for j in proto.minimum:
        json_list.append(j)
      obj.minimum = json_list
    return obj


class UrState:
  """Representation of proto message UrState.

   URRobotState is the message for the state of a robot, dataType == "ur-state".
  """
  # Robot pose, 6 numbers: x, y, z, rx, ry, rz.
  pose: List[float]

  # Joints positions in radians.
  joints: List[float]

  # Forces reported by robot. There is no standard for this field; it is
  # robot-specific.
  force: List[float]

  # Torques reported by robot. There is no standard for this field; it is
  # robot-specific.
  torque: List[float]
  robot_dexterity: float

  # Is the robot turned on.
  is_robot_power_on: bool
  is_emergency_stopped: bool
  is_protective_stopped: bool
  is_safeguard_stopped: bool
  is_reduced_mode: bool
  safety_message: str
  is_program_running: bool

  # Digital inputs.
  digital_in: List[bool]
  sensor_in: List[bool]

  # Digital outputs.
  digital_out: List[bool]

  # Analog inputs.
  analog_in: List[float]
  analog_out: List[float]
  tool_digital_in: List[bool]
  tool_digital_out: List[bool]
  tool_analog_in: List[float]
  tool_analog_out: List[float]
  board_temp_c: float
  robot_voltage_v: float
  robot_current_a: float
  board_io_current_a: float
  tool_temp_c: float
  tool_voltage_v: float
  tool_current_a: float
  joint_voltages_v: List[float]
  joint_currents_a: List[float]
  joint_temps_c: List[float]

  # One of {"", "remote", "local"}
  robot_mode: str

  # ProgramCounter is the number of executed programs.
  # It only gets incremented after a program finished running.
  program_counter: int

  # I/O states for digital pins. When present, overrides digital_in,
  # sensor_in, digital_out, tool_digital_in, and tool_digital_out.
  digital_bank: List['DigitalBank']

  # I/O states for analog pins. When present, overrides analog_in, analog_out,
  # tool_analog_in, and tool_analog_out.
  analog_bank: List['AnalogBank']

  # I/O states for integer pins.
  integer_bank: List['IntegerBank']

  # Tag of last terminated (aborted or done) program.
  last_terminated_program: str

  def __init__(self, analog_bank: Optional[List['AnalogBank']] = None, analog_in: Optional[List[float]] = None, analog_out: Optional[List[float]] = None, board_io_current_a: float = 0.0, board_temp_c: float = 0.0, digital_bank: Optional[List['DigitalBank']] = None, digital_in: Optional[List[bool]] = None, digital_out: Optional[List[bool]] = None, force: Optional[List[float]] = None, integer_bank: Optional[List['IntegerBank']] = None, is_emergency_stopped: bool = False, is_program_running: bool = False, is_protective_stopped: bool = False, is_reduced_mode: bool = False, is_robot_power_on: bool = False, is_safeguard_stopped: bool = False, joint_currents_a: Optional[List[float]] = None, joint_temps_c: Optional[List[float]] = None, joint_voltages_v: Optional[List[float]] = None, joints: Optional[List[float]] = None, last_terminated_program: str = '', pose: Optional[List[float]] = None, program_counter: int = 0, robot_current_a: float = 0.0, robot_dexterity: float = 0.0, robot_mode: str = '', robot_voltage_v: float = 0.0, safety_message: str = '', sensor_in: Optional[List[bool]] = None, tool_analog_in: Optional[List[float]] = None, tool_analog_out: Optional[List[float]] = None, tool_current_a: float = 0.0, tool_digital_in: Optional[List[bool]] = None, tool_digital_out: Optional[List[bool]] = None, tool_temp_c: float = 0.0, tool_voltage_v: float = 0.0, torque: Optional[List[float]] = None) -> None:
    if analog_bank is None:
      self.analog_bank = []
    else:
      self.analog_bank = analog_bank
    if analog_in is None:
      self.analog_in = []
    else:
      self.analog_in = analog_in
    if analog_out is None:
      self.analog_out = []
    else:
      self.analog_out = analog_out
    self.board_io_current_a = board_io_current_a
    self.board_temp_c = board_temp_c
    if digital_bank is None:
      self.digital_bank = []
    else:
      self.digital_bank = digital_bank
    if digital_in is None:
      self.digital_in = []
    else:
      self.digital_in = digital_in
    if digital_out is None:
      self.digital_out = []
    else:
      self.digital_out = digital_out
    if force is None:
      self.force = []
    else:
      self.force = force
    if integer_bank is None:
      self.integer_bank = []
    else:
      self.integer_bank = integer_bank
    self.is_emergency_stopped = is_emergency_stopped
    self.is_program_running = is_program_running
    self.is_protective_stopped = is_protective_stopped
    self.is_reduced_mode = is_reduced_mode
    self.is_robot_power_on = is_robot_power_on
    self.is_safeguard_stopped = is_safeguard_stopped
    if joint_currents_a is None:
      self.joint_currents_a = []
    else:
      self.joint_currents_a = joint_currents_a
    if joint_temps_c is None:
      self.joint_temps_c = []
    else:
      self.joint_temps_c = joint_temps_c
    if joint_voltages_v is None:
      self.joint_voltages_v = []
    else:
      self.joint_voltages_v = joint_voltages_v
    if joints is None:
      self.joints = []
    else:
      self.joints = joints
    self.last_terminated_program = last_terminated_program
    if pose is None:
      self.pose = []
    else:
      self.pose = pose
    self.program_counter = program_counter
    self.robot_current_a = robot_current_a
    self.robot_dexterity = robot_dexterity
    self.robot_mode = robot_mode
    self.robot_voltage_v = robot_voltage_v
    self.safety_message = safety_message
    if sensor_in is None:
      self.sensor_in = []
    else:
      self.sensor_in = sensor_in
    if tool_analog_in is None:
      self.tool_analog_in = []
    else:
      self.tool_analog_in = tool_analog_in
    if tool_analog_out is None:
      self.tool_analog_out = []
    else:
      self.tool_analog_out = tool_analog_out
    self.tool_current_a = tool_current_a
    if tool_digital_in is None:
      self.tool_digital_in = []
    else:
      self.tool_digital_in = tool_digital_in
    if tool_digital_out is None:
      self.tool_digital_out = []
    else:
      self.tool_digital_out = tool_digital_out
    self.tool_temp_c = tool_temp_c
    self.tool_voltage_v = tool_voltage_v
    if torque is None:
      self.torque = []
    else:
      self.torque = torque

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()
    item: Any

    if self.analog_bank:
      assert isinstance(self.analog_bank, list), 'Wrong type for attribute: analog_bank. Expected: list. Got: ' + str(type(self.analog_bank)) + '.'
      obj_list = []
      for item in self.analog_bank:
        obj_list.append(item.to_json())
      json_data['analogBank'] = obj_list

    if self.analog_in:
      assert isinstance(self.analog_in, list), 'Wrong type for attribute: analog_in. Expected: list. Got: ' + str(type(self.analog_in)) + '.'
      json_data['analogIn'] = self.analog_in

    if self.analog_out:
      assert isinstance(self.analog_out, list), 'Wrong type for attribute: analog_out. Expected: list. Got: ' + str(type(self.analog_out)) + '.'
      json_data['analogOut'] = self.analog_out

    if self.board_io_current_a:
      assert isinstance(self.board_io_current_a, float) or isinstance(self.board_io_current_a, int), 'Wrong type for attribute: board_io_current_a. Expected: float. Got: ' + str(type(self.board_io_current_a)) + '.'
      json_data['boardIOCurrentA'] = self.board_io_current_a

    if self.board_temp_c:
      assert isinstance(self.board_temp_c, float) or isinstance(self.board_temp_c, int), 'Wrong type for attribute: board_temp_c. Expected: float. Got: ' + str(type(self.board_temp_c)) + '.'
      json_data['boardTempC'] = self.board_temp_c

    if self.digital_bank:
      assert isinstance(self.digital_bank, list), 'Wrong type for attribute: digital_bank. Expected: list. Got: ' + str(type(self.digital_bank)) + '.'
      obj_list = []
      for item in self.digital_bank:
        obj_list.append(item.to_json())
      json_data['digitalBank'] = obj_list

    if self.digital_in:
      assert isinstance(self.digital_in, list), 'Wrong type for attribute: digital_in. Expected: list. Got: ' + str(type(self.digital_in)) + '.'
      json_data['digitalIn'] = self.digital_in

    if self.digital_out:
      assert isinstance(self.digital_out, list), 'Wrong type for attribute: digital_out. Expected: list. Got: ' + str(type(self.digital_out)) + '.'
      json_data['digitalOut'] = self.digital_out

    if self.force:
      assert isinstance(self.force, list), 'Wrong type for attribute: force. Expected: list. Got: ' + str(type(self.force)) + '.'
      json_data['force'] = self.force

    if self.integer_bank:
      assert isinstance(self.integer_bank, list), 'Wrong type for attribute: integer_bank. Expected: list. Got: ' + str(type(self.integer_bank)) + '.'
      obj_list = []
      for item in self.integer_bank:
        obj_list.append(item.to_json())
      json_data['integerBank'] = obj_list

    if self.is_emergency_stopped:
      assert isinstance(self.is_emergency_stopped, bool), 'Wrong type for attribute: is_emergency_stopped. Expected: bool. Got: ' + str(type(self.is_emergency_stopped)) + '.'
      json_data['isEmergencyStopped'] = self.is_emergency_stopped

    if self.is_program_running:
      assert isinstance(self.is_program_running, bool), 'Wrong type for attribute: is_program_running. Expected: bool. Got: ' + str(type(self.is_program_running)) + '.'
      json_data['isProgramRunning'] = self.is_program_running

    if self.is_protective_stopped:
      assert isinstance(self.is_protective_stopped, bool), 'Wrong type for attribute: is_protective_stopped. Expected: bool. Got: ' + str(type(self.is_protective_stopped)) + '.'
      json_data['isProtectiveStopped'] = self.is_protective_stopped

    if self.is_reduced_mode:
      assert isinstance(self.is_reduced_mode, bool), 'Wrong type for attribute: is_reduced_mode. Expected: bool. Got: ' + str(type(self.is_reduced_mode)) + '.'
      json_data['isReducedMode'] = self.is_reduced_mode

    if self.is_robot_power_on:
      assert isinstance(self.is_robot_power_on, bool), 'Wrong type for attribute: is_robot_power_on. Expected: bool. Got: ' + str(type(self.is_robot_power_on)) + '.'
      json_data['isRobotPowerOn'] = self.is_robot_power_on

    if self.is_safeguard_stopped:
      assert isinstance(self.is_safeguard_stopped, bool), 'Wrong type for attribute: is_safeguard_stopped. Expected: bool. Got: ' + str(type(self.is_safeguard_stopped)) + '.'
      json_data['isSafeguardStopped'] = self.is_safeguard_stopped

    if self.joint_currents_a:
      assert isinstance(self.joint_currents_a, list), 'Wrong type for attribute: joint_currents_a. Expected: list. Got: ' + str(type(self.joint_currents_a)) + '.'
      json_data['jointCurrentsA'] = self.joint_currents_a

    if self.joint_temps_c:
      assert isinstance(self.joint_temps_c, list), 'Wrong type for attribute: joint_temps_c. Expected: list. Got: ' + str(type(self.joint_temps_c)) + '.'
      json_data['jointTempsC'] = self.joint_temps_c

    if self.joint_voltages_v:
      assert isinstance(self.joint_voltages_v, list), 'Wrong type for attribute: joint_voltages_v. Expected: list. Got: ' + str(type(self.joint_voltages_v)) + '.'
      json_data['jointVoltagesV'] = self.joint_voltages_v

    if self.joints:
      assert isinstance(self.joints, list), 'Wrong type for attribute: joints. Expected: list. Got: ' + str(type(self.joints)) + '.'
      json_data['joints'] = self.joints

    if self.last_terminated_program:
      assert isinstance(self.last_terminated_program, str), 'Wrong type for attribute: last_terminated_program. Expected: str. Got: ' + str(type(self.last_terminated_program)) + '.'
      json_data['lastTerminatedProgram'] = self.last_terminated_program

    if self.pose:
      assert isinstance(self.pose, list), 'Wrong type for attribute: pose. Expected: list. Got: ' + str(type(self.pose)) + '.'
      json_data['pose'] = self.pose

    if self.program_counter:
      assert isinstance(self.program_counter, int), 'Wrong type for attribute: program_counter. Expected: int. Got: ' + str(type(self.program_counter)) + '.'
      json_data['programCounter'] = self.program_counter

    if self.robot_current_a:
      assert isinstance(self.robot_current_a, float) or isinstance(self.robot_current_a, int), 'Wrong type for attribute: robot_current_a. Expected: float. Got: ' + str(type(self.robot_current_a)) + '.'
      json_data['robotCurrentA'] = self.robot_current_a

    if self.robot_dexterity:
      assert isinstance(self.robot_dexterity, float) or isinstance(self.robot_dexterity, int), 'Wrong type for attribute: robot_dexterity. Expected: float. Got: ' + str(type(self.robot_dexterity)) + '.'
      json_data['robotDexterity'] = self.robot_dexterity

    if self.robot_mode:
      assert isinstance(self.robot_mode, str), 'Wrong type for attribute: robot_mode. Expected: str. Got: ' + str(type(self.robot_mode)) + '.'
      json_data['robotMode'] = self.robot_mode

    if self.robot_voltage_v:
      assert isinstance(self.robot_voltage_v, float) or isinstance(self.robot_voltage_v, int), 'Wrong type for attribute: robot_voltage_v. Expected: float. Got: ' + str(type(self.robot_voltage_v)) + '.'
      json_data['robotVoltageV'] = self.robot_voltage_v

    if self.safety_message:
      assert isinstance(self.safety_message, str), 'Wrong type for attribute: safety_message. Expected: str. Got: ' + str(type(self.safety_message)) + '.'
      json_data['safetyMessage'] = self.safety_message

    if self.sensor_in:
      assert isinstance(self.sensor_in, list), 'Wrong type for attribute: sensor_in. Expected: list. Got: ' + str(type(self.sensor_in)) + '.'
      json_data['sensorIn'] = self.sensor_in

    if self.tool_analog_in:
      assert isinstance(self.tool_analog_in, list), 'Wrong type for attribute: tool_analog_in. Expected: list. Got: ' + str(type(self.tool_analog_in)) + '.'
      json_data['toolAnalogIn'] = self.tool_analog_in

    if self.tool_analog_out:
      assert isinstance(self.tool_analog_out, list), 'Wrong type for attribute: tool_analog_out. Expected: list. Got: ' + str(type(self.tool_analog_out)) + '.'
      json_data['toolAnalogOut'] = self.tool_analog_out

    if self.tool_current_a:
      assert isinstance(self.tool_current_a, float) or isinstance(self.tool_current_a, int), 'Wrong type for attribute: tool_current_a. Expected: float. Got: ' + str(type(self.tool_current_a)) + '.'
      json_data['toolCurrentA'] = self.tool_current_a

    if self.tool_digital_in:
      assert isinstance(self.tool_digital_in, list), 'Wrong type for attribute: tool_digital_in. Expected: list. Got: ' + str(type(self.tool_digital_in)) + '.'
      json_data['toolDigitalIn'] = self.tool_digital_in

    if self.tool_digital_out:
      assert isinstance(self.tool_digital_out, list), 'Wrong type for attribute: tool_digital_out. Expected: list. Got: ' + str(type(self.tool_digital_out)) + '.'
      json_data['toolDigitalOut'] = self.tool_digital_out

    if self.tool_temp_c:
      assert isinstance(self.tool_temp_c, float) or isinstance(self.tool_temp_c, int), 'Wrong type for attribute: tool_temp_c. Expected: float. Got: ' + str(type(self.tool_temp_c)) + '.'
      json_data['toolTempC'] = self.tool_temp_c

    if self.tool_voltage_v:
      assert isinstance(self.tool_voltage_v, float) or isinstance(self.tool_voltage_v, int), 'Wrong type for attribute: tool_voltage_v. Expected: float. Got: ' + str(type(self.tool_voltage_v)) + '.'
      json_data['toolVoltageV'] = self.tool_voltage_v

    if self.torque:
      assert isinstance(self.torque, list), 'Wrong type for attribute: torque. Expected: list. Got: ' + str(type(self.torque)) + '.'
      json_data['torque'] = self.torque

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'UrState':
    """Convert JSON to type object."""
    obj = UrState()
    json_list: List[Any]

    expected_json_keys: List[str] = ['analogBank', 'analogIn', 'analogOut', 'boardIOCurrentA', 'boardTempC', 'digitalBank', 'digitalIn', 'digitalOut', 'force', 'integerBank', 'isEmergencyStopped', 'isProgramRunning', 'isProtectiveStopped', 'isReducedMode', 'isRobotPowerOn', 'isSafeguardStopped', 'jointCurrentsA', 'jointTempsC', 'jointVoltagesV', 'joints', 'lastTerminatedProgram', 'pose', 'programCounter', 'robotCurrentA', 'robotDexterity', 'robotMode', 'robotVoltageV', 'safetyMessage', 'sensorIn', 'toolAnalogIn', 'toolAnalogOut', 'toolCurrentA', 'toolDigitalIn', 'toolDigitalOut', 'toolTempC', 'toolVoltageV', 'torque']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid UrState. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'analogBank' in json_data:
      assert isinstance(json_data['analogBank'], list), 'Wrong type for attribute: analogBank. Expected: list. Got: ' + str(type(json_data['analogBank'])) + '.'
      json_list = []
      for j in json_data['analogBank']:
        json_list.append(AnalogBank.from_json(j))
      obj.analog_bank = json_list

    if 'analogIn' in json_data:
      assert isinstance(json_data['analogIn'], list), 'Wrong type for attribute: analogIn. Expected: list. Got: ' + str(type(json_data['analogIn'])) + '.'
      json_list = []
      for j in json_data['analogIn']:
        json_list.append(j)
      obj.analog_in = json_list

    if 'analogOut' in json_data:
      assert isinstance(json_data['analogOut'], list), 'Wrong type for attribute: analogOut. Expected: list. Got: ' + str(type(json_data['analogOut'])) + '.'
      json_list = []
      for j in json_data['analogOut']:
        json_list.append(j)
      obj.analog_out = json_list

    if 'boardIOCurrentA' in json_data:
      assert isinstance(json_data['boardIOCurrentA'], float) or isinstance(json_data['boardIOCurrentA'], int), 'Wrong type for attribute: boardIOCurrentA. Expected: float. Got: ' + str(type(json_data['boardIOCurrentA'])) + '.'
      obj.board_io_current_a = json_data['boardIOCurrentA']

    if 'boardTempC' in json_data:
      assert isinstance(json_data['boardTempC'], float) or isinstance(json_data['boardTempC'], int), 'Wrong type for attribute: boardTempC. Expected: float. Got: ' + str(type(json_data['boardTempC'])) + '.'
      obj.board_temp_c = json_data['boardTempC']

    if 'digitalBank' in json_data:
      assert isinstance(json_data['digitalBank'], list), 'Wrong type for attribute: digitalBank. Expected: list. Got: ' + str(type(json_data['digitalBank'])) + '.'
      json_list = []
      for j in json_data['digitalBank']:
        json_list.append(DigitalBank.from_json(j))
      obj.digital_bank = json_list

    if 'digitalIn' in json_data:
      assert isinstance(json_data['digitalIn'], list), 'Wrong type for attribute: digitalIn. Expected: list. Got: ' + str(type(json_data['digitalIn'])) + '.'
      json_list = []
      for j in json_data['digitalIn']:
        json_list.append(j)
      obj.digital_in = json_list

    if 'digitalOut' in json_data:
      assert isinstance(json_data['digitalOut'], list), 'Wrong type for attribute: digitalOut. Expected: list. Got: ' + str(type(json_data['digitalOut'])) + '.'
      json_list = []
      for j in json_data['digitalOut']:
        json_list.append(j)
      obj.digital_out = json_list

    if 'force' in json_data:
      assert isinstance(json_data['force'], list), 'Wrong type for attribute: force. Expected: list. Got: ' + str(type(json_data['force'])) + '.'
      json_list = []
      for j in json_data['force']:
        json_list.append(j)
      obj.force = json_list

    if 'integerBank' in json_data:
      assert isinstance(json_data['integerBank'], list), 'Wrong type for attribute: integerBank. Expected: list. Got: ' + str(type(json_data['integerBank'])) + '.'
      json_list = []
      for j in json_data['integerBank']:
        json_list.append(IntegerBank.from_json(j))
      obj.integer_bank = json_list

    if 'isEmergencyStopped' in json_data:
      assert isinstance(json_data['isEmergencyStopped'], bool), 'Wrong type for attribute: isEmergencyStopped. Expected: bool. Got: ' + str(type(json_data['isEmergencyStopped'])) + '.'
      obj.is_emergency_stopped = json_data['isEmergencyStopped']

    if 'isProgramRunning' in json_data:
      assert isinstance(json_data['isProgramRunning'], bool), 'Wrong type for attribute: isProgramRunning. Expected: bool. Got: ' + str(type(json_data['isProgramRunning'])) + '.'
      obj.is_program_running = json_data['isProgramRunning']

    if 'isProtectiveStopped' in json_data:
      assert isinstance(json_data['isProtectiveStopped'], bool), 'Wrong type for attribute: isProtectiveStopped. Expected: bool. Got: ' + str(type(json_data['isProtectiveStopped'])) + '.'
      obj.is_protective_stopped = json_data['isProtectiveStopped']

    if 'isReducedMode' in json_data:
      assert isinstance(json_data['isReducedMode'], bool), 'Wrong type for attribute: isReducedMode. Expected: bool. Got: ' + str(type(json_data['isReducedMode'])) + '.'
      obj.is_reduced_mode = json_data['isReducedMode']

    if 'isRobotPowerOn' in json_data:
      assert isinstance(json_data['isRobotPowerOn'], bool), 'Wrong type for attribute: isRobotPowerOn. Expected: bool. Got: ' + str(type(json_data['isRobotPowerOn'])) + '.'
      obj.is_robot_power_on = json_data['isRobotPowerOn']

    if 'isSafeguardStopped' in json_data:
      assert isinstance(json_data['isSafeguardStopped'], bool), 'Wrong type for attribute: isSafeguardStopped. Expected: bool. Got: ' + str(type(json_data['isSafeguardStopped'])) + '.'
      obj.is_safeguard_stopped = json_data['isSafeguardStopped']

    if 'jointCurrentsA' in json_data:
      assert isinstance(json_data['jointCurrentsA'], list), 'Wrong type for attribute: jointCurrentsA. Expected: list. Got: ' + str(type(json_data['jointCurrentsA'])) + '.'
      json_list = []
      for j in json_data['jointCurrentsA']:
        json_list.append(j)
      obj.joint_currents_a = json_list

    if 'jointTempsC' in json_data:
      assert isinstance(json_data['jointTempsC'], list), 'Wrong type for attribute: jointTempsC. Expected: list. Got: ' + str(type(json_data['jointTempsC'])) + '.'
      json_list = []
      for j in json_data['jointTempsC']:
        json_list.append(j)
      obj.joint_temps_c = json_list

    if 'jointVoltagesV' in json_data:
      assert isinstance(json_data['jointVoltagesV'], list), 'Wrong type for attribute: jointVoltagesV. Expected: list. Got: ' + str(type(json_data['jointVoltagesV'])) + '.'
      json_list = []
      for j in json_data['jointVoltagesV']:
        json_list.append(j)
      obj.joint_voltages_v = json_list

    if 'joints' in json_data:
      assert isinstance(json_data['joints'], list), 'Wrong type for attribute: joints. Expected: list. Got: ' + str(type(json_data['joints'])) + '.'
      json_list = []
      for j in json_data['joints']:
        json_list.append(j)
      obj.joints = json_list

    if 'lastTerminatedProgram' in json_data:
      assert isinstance(json_data['lastTerminatedProgram'], str), 'Wrong type for attribute: lastTerminatedProgram. Expected: str. Got: ' + str(type(json_data['lastTerminatedProgram'])) + '.'
      obj.last_terminated_program = json_data['lastTerminatedProgram']

    if 'pose' in json_data:
      assert isinstance(json_data['pose'], list), 'Wrong type for attribute: pose. Expected: list. Got: ' + str(type(json_data['pose'])) + '.'
      json_list = []
      for j in json_data['pose']:
        json_list.append(j)
      obj.pose = json_list

    if 'programCounter' in json_data:
      assert isinstance(json_data['programCounter'], int), 'Wrong type for attribute: programCounter. Expected: int. Got: ' + str(type(json_data['programCounter'])) + '.'
      obj.program_counter = json_data['programCounter']

    if 'robotCurrentA' in json_data:
      assert isinstance(json_data['robotCurrentA'], float) or isinstance(json_data['robotCurrentA'], int), 'Wrong type for attribute: robotCurrentA. Expected: float. Got: ' + str(type(json_data['robotCurrentA'])) + '.'
      obj.robot_current_a = json_data['robotCurrentA']

    if 'robotDexterity' in json_data:
      assert isinstance(json_data['robotDexterity'], float) or isinstance(json_data['robotDexterity'], int), 'Wrong type for attribute: robotDexterity. Expected: float. Got: ' + str(type(json_data['robotDexterity'])) + '.'
      obj.robot_dexterity = json_data['robotDexterity']

    if 'robotMode' in json_data:
      assert isinstance(json_data['robotMode'], str), 'Wrong type for attribute: robotMode. Expected: str. Got: ' + str(type(json_data['robotMode'])) + '.'
      obj.robot_mode = json_data['robotMode']

    if 'robotVoltageV' in json_data:
      assert isinstance(json_data['robotVoltageV'], float) or isinstance(json_data['robotVoltageV'], int), 'Wrong type for attribute: robotVoltageV. Expected: float. Got: ' + str(type(json_data['robotVoltageV'])) + '.'
      obj.robot_voltage_v = json_data['robotVoltageV']

    if 'safetyMessage' in json_data:
      assert isinstance(json_data['safetyMessage'], str), 'Wrong type for attribute: safetyMessage. Expected: str. Got: ' + str(type(json_data['safetyMessage'])) + '.'
      obj.safety_message = json_data['safetyMessage']

    if 'sensorIn' in json_data:
      assert isinstance(json_data['sensorIn'], list), 'Wrong type for attribute: sensorIn. Expected: list. Got: ' + str(type(json_data['sensorIn'])) + '.'
      json_list = []
      for j in json_data['sensorIn']:
        json_list.append(j)
      obj.sensor_in = json_list

    if 'toolAnalogIn' in json_data:
      assert isinstance(json_data['toolAnalogIn'], list), 'Wrong type for attribute: toolAnalogIn. Expected: list. Got: ' + str(type(json_data['toolAnalogIn'])) + '.'
      json_list = []
      for j in json_data['toolAnalogIn']:
        json_list.append(j)
      obj.tool_analog_in = json_list

    if 'toolAnalogOut' in json_data:
      assert isinstance(json_data['toolAnalogOut'], list), 'Wrong type for attribute: toolAnalogOut. Expected: list. Got: ' + str(type(json_data['toolAnalogOut'])) + '.'
      json_list = []
      for j in json_data['toolAnalogOut']:
        json_list.append(j)
      obj.tool_analog_out = json_list

    if 'toolCurrentA' in json_data:
      assert isinstance(json_data['toolCurrentA'], float) or isinstance(json_data['toolCurrentA'], int), 'Wrong type for attribute: toolCurrentA. Expected: float. Got: ' + str(type(json_data['toolCurrentA'])) + '.'
      obj.tool_current_a = json_data['toolCurrentA']

    if 'toolDigitalIn' in json_data:
      assert isinstance(json_data['toolDigitalIn'], list), 'Wrong type for attribute: toolDigitalIn. Expected: list. Got: ' + str(type(json_data['toolDigitalIn'])) + '.'
      json_list = []
      for j in json_data['toolDigitalIn']:
        json_list.append(j)
      obj.tool_digital_in = json_list

    if 'toolDigitalOut' in json_data:
      assert isinstance(json_data['toolDigitalOut'], list), 'Wrong type for attribute: toolDigitalOut. Expected: list. Got: ' + str(type(json_data['toolDigitalOut'])) + '.'
      json_list = []
      for j in json_data['toolDigitalOut']:
        json_list.append(j)
      obj.tool_digital_out = json_list

    if 'toolTempC' in json_data:
      assert isinstance(json_data['toolTempC'], float) or isinstance(json_data['toolTempC'], int), 'Wrong type for attribute: toolTempC. Expected: float. Got: ' + str(type(json_data['toolTempC'])) + '.'
      obj.tool_temp_c = json_data['toolTempC']

    if 'toolVoltageV' in json_data:
      assert isinstance(json_data['toolVoltageV'], float) or isinstance(json_data['toolVoltageV'], int), 'Wrong type for attribute: toolVoltageV. Expected: float. Got: ' + str(type(json_data['toolVoltageV'])) + '.'
      obj.tool_voltage_v = json_data['toolVoltageV']

    if 'torque' in json_data:
      assert isinstance(json_data['torque'], list), 'Wrong type for attribute: torque. Expected: list. Got: ' + str(type(json_data['torque'])) + '.'
      json_list = []
      for j in json_data['torque']:
        json_list.append(j)
      obj.torque = json_list

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.UrState) -> 'UrState':
    """Convert UrState proto to type object."""
    if not proto:
      return None
    obj = UrState()
    if proto.analog_bank:
      json_list = []
      for j in proto.analog_bank:
        json_list.append(AnalogBank.from_proto(j))
      obj.analog_bank = json_list
    if proto.analog_in:
      json_list = []
      for j in proto.analog_in:
        json_list.append(j)
      obj.analog_in = json_list
    if proto.analog_out:
      json_list = []
      for j in proto.analog_out:
        json_list.append(j)
      obj.analog_out = json_list
    obj.board_io_current_a = get_proto_value(proto.board_io_current_a)
    obj.board_temp_c = get_proto_value(proto.board_temp_c)
    if proto.digital_bank:
      json_list = []
      for j in proto.digital_bank:
        json_list.append(DigitalBank.from_proto(j))
      obj.digital_bank = json_list
    if proto.digital_in:
      json_list = []
      for j in proto.digital_in:
        json_list.append(j)
      obj.digital_in = json_list
    if proto.digital_out:
      json_list = []
      for j in proto.digital_out:
        json_list.append(j)
      obj.digital_out = json_list
    if proto.force:
      json_list = []
      for j in proto.force:
        json_list.append(j)
      obj.force = json_list
    if proto.integer_bank:
      json_list = []
      for j in proto.integer_bank:
        json_list.append(IntegerBank.from_proto(j))
      obj.integer_bank = json_list
    obj.is_emergency_stopped = get_proto_value(proto.robot_stop_state.is_emergency_stopped)
    obj.is_program_running = get_proto_value(proto.is_program_running)
    obj.is_protective_stopped = get_proto_value(proto.robot_stop_state.is_protective_stopped)
    obj.is_reduced_mode = get_proto_value(proto.robot_stop_state.is_reduced_mode)
    obj.is_robot_power_on = get_proto_value(proto.is_robot_power_on)
    obj.is_safeguard_stopped = get_proto_value(proto.robot_stop_state.is_safeguard_stopped)
    if proto.joint_currents_a:
      json_list = []
      for j in proto.joint_currents_a:
        json_list.append(j)
      obj.joint_currents_a = json_list
    if proto.joint_temps_c:
      json_list = []
      for j in proto.joint_temps_c:
        json_list.append(j)
      obj.joint_temps_c = json_list
    if proto.joint_voltages_v:
      json_list = []
      for j in proto.joint_voltages_v:
        json_list.append(j)
      obj.joint_voltages_v = json_list
    if proto.joints:
      json_list = []
      for j in proto.joints:
        json_list.append(j)
      obj.joints = json_list
    obj.last_terminated_program = get_proto_value(proto.last_terminated_program)
    if proto.pose:
      json_list = []
      for j in proto.pose:
        json_list.append(j)
      obj.pose = json_list
    obj.program_counter = get_proto_value(proto.program_counter)
    obj.robot_current_a = get_proto_value(proto.robot_current_a)
    obj.robot_dexterity = get_proto_value(proto.robot_dexterity)
    obj.robot_mode = get_proto_value(proto.robot_mode)
    obj.robot_voltage_v = get_proto_value(proto.robot_voltage_v)
    obj.safety_message = get_proto_value(proto.robot_stop_state.safety_message)
    if proto.sensor_in:
      json_list = []
      for j in proto.sensor_in:
        json_list.append(j)
      obj.sensor_in = json_list
    if proto.tool_analog_in:
      json_list = []
      for j in proto.tool_analog_in:
        json_list.append(j)
      obj.tool_analog_in = json_list
    if proto.tool_analog_out:
      json_list = []
      for j in proto.tool_analog_out:
        json_list.append(j)
      obj.tool_analog_out = json_list
    obj.tool_current_a = get_proto_value(proto.tool_current_a)
    if proto.tool_digital_in:
      json_list = []
      for j in proto.tool_digital_in:
        json_list.append(j)
      obj.tool_digital_in = json_list
    if proto.tool_digital_out:
      json_list = []
      for j in proto.tool_digital_out:
        json_list.append(j)
      obj.tool_digital_out = json_list
    obj.tool_temp_c = get_proto_value(proto.tool_temp_c)
    obj.tool_voltage_v = get_proto_value(proto.tool_voltage_v)
    if proto.torque:
      json_list = []
      for j in proto.torque:
        json_list.append(j)
      obj.torque = json_list
    return obj


class VacuumActionParams:
  """Representation of proto message VacuumActionParams.

   VacuumActionParams stores the original vacuum action.
  """
  state: int

  def __init__(self, state: int = 0) -> None:
    self.state = state

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.state:
      assert isinstance(self.state, int), 'Wrong type for attribute: state. Expected: int. Got: ' + str(type(self.state)) + '.'
      json_data['state'] = self.state

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'VacuumActionParams':
    """Convert JSON to type object."""
    obj = VacuumActionParams()

    expected_json_keys: List[str] = ['state']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid VacuumActionParams. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'state' in json_data:
      assert isinstance(json_data['state'], int), 'Wrong type for attribute: state. Expected: int. Got: ' + str(type(json_data['state'])) + '.'
      obj.state = json_data['state']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.VacuumActionParams) -> 'VacuumActionParams':
    """Convert VacuumActionParams proto to type object."""
    if not proto:
      return None
    obj = VacuumActionParams()
    obj.state = get_proto_value(proto.state)
    return obj


class Vec3d:
  """Representation of proto message Vec3d.

   Vec3D contains an X,Y,Z coordinate triplet.
  """
  x: float
  y: float
  z: float

  def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
    self.x = x
    self.y = y
    self.z = z

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.x:
      assert isinstance(self.x, float) or isinstance(self.x, int), 'Wrong type for attribute: x. Expected: float. Got: ' + str(type(self.x)) + '.'
      json_data['x'] = self.x

    if self.y:
      assert isinstance(self.y, float) or isinstance(self.y, int), 'Wrong type for attribute: y. Expected: float. Got: ' + str(type(self.y)) + '.'
      json_data['y'] = self.y

    if self.z:
      assert isinstance(self.z, float) or isinstance(self.z, int), 'Wrong type for attribute: z. Expected: float. Got: ' + str(type(self.z)) + '.'
      json_data['z'] = self.z

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'Vec3d':
    """Convert JSON to type object."""
    obj = Vec3d()

    expected_json_keys: List[str] = ['x', 'y', 'z']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid Vec3d. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'x' in json_data:
      assert isinstance(json_data['x'], float) or isinstance(json_data['x'], int), 'Wrong type for attribute: x. Expected: float. Got: ' + str(type(json_data['x'])) + '.'
      obj.x = json_data['x']

    if 'y' in json_data:
      assert isinstance(json_data['y'], float) or isinstance(json_data['y'], int), 'Wrong type for attribute: y. Expected: float. Got: ' + str(type(json_data['y'])) + '.'
      obj.y = json_data['y']

    if 'z' in json_data:
      assert isinstance(json_data['z'], float) or isinstance(json_data['z'], int), 'Wrong type for attribute: z. Expected: float. Got: ' + str(type(json_data['z'])) + '.'
      obj.z = json_data['z']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.Vec3d) -> 'Vec3d':
    """Convert Vec3d proto to type object."""
    if not proto:
      return None
    obj = Vec3d()
    obj.x = get_proto_value(proto.x)
    obj.y = get_proto_value(proto.y)
    obj.z = get_proto_value(proto.z)
    return obj


class WaitArgs:
  """Representation of proto message WaitArgs.

   WaitArgs are the arguments to the Wait ReachScript command.
  """
  # The timeout in seconds. Zero means evaluating the expression
  # and immediately deciding whether to perform the timeout_action.
  timeout_seconds: float

  # What to do on timeout.
  timeout_action: Optional['WaitTimeoutAction']

  # The expression to evaluate, waiting for it to become true.
  expr: Optional['ReachScriptBooleanExpression']

  def __init__(self, expr: Optional['ReachScriptBooleanExpression'] = None, timeout_action: Optional['WaitTimeoutAction'] = None, timeout_seconds: float = 0.0) -> None:
    self.expr = expr
    self.timeout_action = timeout_action
    self.timeout_seconds = timeout_seconds

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.expr:
      assert self.expr.__class__.__name__ == 'ReachScriptBooleanExpression', 'Wrong type for attribute: expr. Expected: ReachScriptBooleanExpression. Got: ' + str(type(self.expr)) + '.'
      json_data['expr'] = self.expr.to_json()

    if self.timeout_action:
      assert self.timeout_action.__class__.__name__ == 'WaitTimeoutAction', 'Wrong type for attribute: timeout_action. Expected: WaitTimeoutAction. Got: ' + str(type(self.timeout_action)) + '.'
      json_data['timeoutAction'] = self.timeout_action.to_json()

    if self.timeout_seconds:
      assert isinstance(self.timeout_seconds, float) or isinstance(self.timeout_seconds, int), 'Wrong type for attribute: timeout_seconds. Expected: float. Got: ' + str(type(self.timeout_seconds)) + '.'
      json_data['timeoutSeconds'] = self.timeout_seconds

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'WaitArgs':
    """Convert JSON to type object."""
    obj = WaitArgs()

    expected_json_keys: List[str] = ['expr', 'timeoutAction', 'timeoutSeconds']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid WaitArgs. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'expr' in json_data:
      assert isinstance(json_data['expr'], dict), 'Wrong type for attribute: expr. Expected: dict. Got: ' + str(type(json_data['expr'])) + '.'
      obj.expr = ReachScriptBooleanExpression.from_json(json_data['expr'])

    if 'timeoutAction' in json_data:
      assert isinstance(json_data['timeoutAction'], dict), 'Wrong type for attribute: timeoutAction. Expected: dict. Got: ' + str(type(json_data['timeoutAction'])) + '.'
      obj.timeout_action = WaitTimeoutAction.from_json(json_data['timeoutAction'])

    if 'timeoutSeconds' in json_data:
      assert isinstance(json_data['timeoutSeconds'], float) or isinstance(json_data['timeoutSeconds'], int), 'Wrong type for attribute: timeoutSeconds. Expected: float. Got: ' + str(type(json_data['timeoutSeconds'])) + '.'
      obj.timeout_seconds = json_data['timeoutSeconds']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.WaitArgs) -> 'WaitArgs':
    """Convert WaitArgs proto to type object."""
    if not proto:
      return None
    obj = WaitArgs()
    obj.expr = ReachScriptBooleanExpression.from_proto(get_proto_field(proto, 'expr'))
    obj.timeout_action = WaitTimeoutAction.from_proto(get_proto_field(proto, 'timeout_action'))
    obj.timeout_seconds = get_proto_value(proto.timeout_seconds)
    return obj


class WaitTimeoutAction:
  """Representation of proto message WaitTimeoutAction.

   WaitTimeoutAction specifies what to do if a Wait statement
   times out.
  """
  # type is one of:
  #   * abort: Sends an aborted status with error "stopped"
  #     for the command, and clears the queue.
  #   * abort_recoverable: Sends an aborted status with
  #     error "recoverable" for the command, and does not clear
  #     the queue.
  #   * continue: Continues on to the next statement.
  # Any other string shall result in command rejection.
  py_type: str

  # Message field of resulting status if aborted.
  abort_message: str

  def __init__(self, abort_message: str = '', py_type: str = '') -> None:
    self.abort_message = abort_message
    self.py_type = py_type

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.abort_message:
      assert isinstance(self.abort_message, str), 'Wrong type for attribute: abort_message. Expected: str. Got: ' + str(type(self.abort_message)) + '.'
      json_data['abortMessage'] = self.abort_message

    if self.py_type:
      assert isinstance(self.py_type, str), 'Wrong type for attribute: py_type. Expected: str. Got: ' + str(type(self.py_type)) + '.'
      json_data['type'] = self.py_type

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'WaitTimeoutAction':
    """Convert JSON to type object."""
    obj = WaitTimeoutAction()

    expected_json_keys: List[str] = ['abortMessage', 'type']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid WaitTimeoutAction. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'abortMessage' in json_data:
      assert isinstance(json_data['abortMessage'], str), 'Wrong type for attribute: abortMessage. Expected: str. Got: ' + str(type(json_data['abortMessage'])) + '.'
      obj.abort_message = json_data['abortMessage']

    if 'type' in json_data:
      assert isinstance(json_data['type'], str), 'Wrong type for attribute: type. Expected: str. Got: ' + str(type(json_data['type'])) + '.'
      obj.py_type = json_data['type']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.WaitTimeoutAction) -> 'WaitTimeoutAction':
    """Convert WaitTimeoutAction proto to type object."""
    if not proto:
      return None
    obj = WaitTimeoutAction()
    obj.abort_message = get_proto_value(proto.abort_message)
    obj.py_type = get_proto_value(proto.type)
    return obj


class WebrtcAudioRequest:
  """Representation of proto message WebrtcAudioRequest.

   WebrtcAudioRequest is used in a command of dataType "webrtc-audio-request",
   an internal message for setting mute/unmute status in webrtc.

  """
  speaker_unmute: bool
  microphone_unmute: bool

  def __init__(self, microphone_unmute: bool = False, speaker_unmute: bool = False) -> None:
    self.microphone_unmute = microphone_unmute
    self.speaker_unmute = speaker_unmute

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.microphone_unmute:
      assert isinstance(self.microphone_unmute, bool), 'Wrong type for attribute: microphone_unmute. Expected: bool. Got: ' + str(type(self.microphone_unmute)) + '.'
      json_data['microphoneUnmute'] = self.microphone_unmute

    if self.speaker_unmute:
      assert isinstance(self.speaker_unmute, bool), 'Wrong type for attribute: speaker_unmute. Expected: bool. Got: ' + str(type(self.speaker_unmute)) + '.'
      json_data['speakerUnmute'] = self.speaker_unmute

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'WebrtcAudioRequest':
    """Convert JSON to type object."""
    obj = WebrtcAudioRequest()

    expected_json_keys: List[str] = ['microphoneUnmute', 'speakerUnmute']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid WebrtcAudioRequest. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'microphoneUnmute' in json_data:
      assert isinstance(json_data['microphoneUnmute'], bool), 'Wrong type for attribute: microphoneUnmute. Expected: bool. Got: ' + str(type(json_data['microphoneUnmute'])) + '.'
      obj.microphone_unmute = json_data['microphoneUnmute']

    if 'speakerUnmute' in json_data:
      assert isinstance(json_data['speakerUnmute'], bool), 'Wrong type for attribute: speakerUnmute. Expected: bool. Got: ' + str(type(json_data['speakerUnmute'])) + '.'
      obj.speaker_unmute = json_data['speakerUnmute']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.WebrtcAudioRequest) -> 'WebrtcAudioRequest':
    """Convert WebrtcAudioRequest proto to type object."""
    if not proto:
      return None
    obj = WebrtcAudioRequest()
    obj.microphone_unmute = get_proto_value(proto.microphone_unmute)
    obj.speaker_unmute = get_proto_value(proto.speaker_unmute)
    return obj


class WebrtcAudioResponse:
  """Representation of proto message WebrtcAudioResponse.

   WebrtcAudioResponse is the response to a webrtc-audio-request command.

  """
  success: bool

  def __init__(self, success: bool = False) -> None:
    self.success = success

  def to_json(self) -> Dict[str, Any]:
    """Convert type object to JSON."""
    json_data: Dict[str, Any] = dict()

    if self.success:
      assert isinstance(self.success, bool), 'Wrong type for attribute: success. Expected: bool. Got: ' + str(type(self.success)) + '.'
      json_data['success'] = self.success

    return json_data

  @staticmethod
  def from_json(json_data: Dict[str, Any]) -> 'WebrtcAudioResponse':
    """Convert JSON to type object."""
    obj = WebrtcAudioResponse()

    expected_json_keys: List[str] = ['success']

    if not set(json_data.keys()).issubset(set(expected_json_keys)):
      raise ValueError('JSON object is not a valid WebrtcAudioResponse. keys found: ' + str(json_data.keys()) + ', valid keys: ' + str(expected_json_keys))

    if 'success' in json_data:
      assert isinstance(json_data['success'], bool), 'Wrong type for attribute: success. Expected: bool. Got: ' + str(type(json_data['success'])) + '.'
      obj.success = json_data['success']

    return obj

  @staticmethod
  def from_proto(proto: logs_pb2.WebrtcAudioResponse) -> 'WebrtcAudioResponse':
    """Convert WebrtcAudioResponse proto to type object."""
    if not proto:
      return None
    obj = WebrtcAudioResponse()
    obj.success = get_proto_value(proto.success)
    return obj
