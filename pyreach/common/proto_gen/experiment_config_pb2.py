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

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: experiment_config.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='experiment_config.proto',
  package='robotics.infrastructure',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x17\x65xperiment_config.proto\x12\x17robotics.infrastructure\x1a\x19google/protobuf/any.proto\",\n\x14RoboticsClientConfig\x12\x14\n\x0cproject_name\x18\x01 \x01(\t\"Q\n\x0eTaskProperties\x12\x11\n\ttask_name\x18\x01 \x01(\t\x12\x12\n\nepisode_id\x18\x02 \x01(\t\x12\x18\n\x10timestamp_coarse\x18\x03 \x01(\x03\"x\n\x04\x46lag\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\tint_value\x18\x02 \x01(\x03H\x00\x12\x16\n\x0cstring_value\x18\x03 \x01(\tH\x00\x12\x16\n\x0c\x64ouble_value\x18\x04 \x01(\x01H\x00\x12\x14\n\nbool_value\x18\x05 \x01(\x08H\x00\x42\x07\n\x05value\"O\n\x05\x46lags\x12,\n\x05\x66lags\x18\x01 \x03(\x0b\x32\x1d.robotics.infrastructure.Flag\x12\x18\n\x10\x65xperiment_token\x18\x02 \x01(\t\":\n\x0e\x46wFlagsRequest\x12(\n\nproperties\x18\x01 \x01(\x0b\x32\x14.google.protobuf.Any\"Y\n\x0f\x46wFlagsResponse\x12\x17\n\x0fsubscription_id\x18\x01 \x01(\t\x12-\n\x05\x66lags\x18\x02 \x01(\x0b\x32\x1e.robotics.infrastructure.Flags\"\x82\x01\n\x1f\x46wExperimentSubscriptionRequest\x12\x17\n\x0fsubscription_id\x18\x01 \x01(\t\x12(\n\nproperties\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any\x12\x1c\n\x14refresh_rate_seconds\x18\x03 \x01(\x05\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_any__pb2.DESCRIPTOR,])




_ROBOTICSCLIENTCONFIG = _descriptor.Descriptor(
  name='RoboticsClientConfig',
  full_name='robotics.infrastructure.RoboticsClientConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='project_name', full_name='robotics.infrastructure.RoboticsClientConfig.project_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=79,
  serialized_end=123,
)


_TASKPROPERTIES = _descriptor.Descriptor(
  name='TaskProperties',
  full_name='robotics.infrastructure.TaskProperties',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_name', full_name='robotics.infrastructure.TaskProperties.task_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='episode_id', full_name='robotics.infrastructure.TaskProperties.episode_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timestamp_coarse', full_name='robotics.infrastructure.TaskProperties.timestamp_coarse', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=125,
  serialized_end=206,
)


_FLAG = _descriptor.Descriptor(
  name='Flag',
  full_name='robotics.infrastructure.Flag',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='robotics.infrastructure.Flag.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='int_value', full_name='robotics.infrastructure.Flag.int_value', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='string_value', full_name='robotics.infrastructure.Flag.string_value', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='double_value', full_name='robotics.infrastructure.Flag.double_value', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bool_value', full_name='robotics.infrastructure.Flag.bool_value', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='value', full_name='robotics.infrastructure.Flag.value',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=208,
  serialized_end=328,
)


_FLAGS = _descriptor.Descriptor(
  name='Flags',
  full_name='robotics.infrastructure.Flags',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='flags', full_name='robotics.infrastructure.Flags.flags', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='experiment_token', full_name='robotics.infrastructure.Flags.experiment_token', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=330,
  serialized_end=409,
)


_FWFLAGSREQUEST = _descriptor.Descriptor(
  name='FwFlagsRequest',
  full_name='robotics.infrastructure.FwFlagsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='properties', full_name='robotics.infrastructure.FwFlagsRequest.properties', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=411,
  serialized_end=469,
)


_FWFLAGSRESPONSE = _descriptor.Descriptor(
  name='FwFlagsResponse',
  full_name='robotics.infrastructure.FwFlagsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='subscription_id', full_name='robotics.infrastructure.FwFlagsResponse.subscription_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='flags', full_name='robotics.infrastructure.FwFlagsResponse.flags', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=471,
  serialized_end=560,
)


_FWEXPERIMENTSUBSCRIPTIONREQUEST = _descriptor.Descriptor(
  name='FwExperimentSubscriptionRequest',
  full_name='robotics.infrastructure.FwExperimentSubscriptionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='subscription_id', full_name='robotics.infrastructure.FwExperimentSubscriptionRequest.subscription_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='properties', full_name='robotics.infrastructure.FwExperimentSubscriptionRequest.properties', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='refresh_rate_seconds', full_name='robotics.infrastructure.FwExperimentSubscriptionRequest.refresh_rate_seconds', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=563,
  serialized_end=693,
)

_FLAG.oneofs_by_name['value'].fields.append(
  _FLAG.fields_by_name['int_value'])
_FLAG.fields_by_name['int_value'].containing_oneof = _FLAG.oneofs_by_name['value']
_FLAG.oneofs_by_name['value'].fields.append(
  _FLAG.fields_by_name['string_value'])
_FLAG.fields_by_name['string_value'].containing_oneof = _FLAG.oneofs_by_name['value']
_FLAG.oneofs_by_name['value'].fields.append(
  _FLAG.fields_by_name['double_value'])
_FLAG.fields_by_name['double_value'].containing_oneof = _FLAG.oneofs_by_name['value']
_FLAG.oneofs_by_name['value'].fields.append(
  _FLAG.fields_by_name['bool_value'])
_FLAG.fields_by_name['bool_value'].containing_oneof = _FLAG.oneofs_by_name['value']
_FLAGS.fields_by_name['flags'].message_type = _FLAG
_FWFLAGSREQUEST.fields_by_name['properties'].message_type = google_dot_protobuf_dot_any__pb2._ANY
_FWFLAGSRESPONSE.fields_by_name['flags'].message_type = _FLAGS
_FWEXPERIMENTSUBSCRIPTIONREQUEST.fields_by_name['properties'].message_type = google_dot_protobuf_dot_any__pb2._ANY
DESCRIPTOR.message_types_by_name['RoboticsClientConfig'] = _ROBOTICSCLIENTCONFIG
DESCRIPTOR.message_types_by_name['TaskProperties'] = _TASKPROPERTIES
DESCRIPTOR.message_types_by_name['Flag'] = _FLAG
DESCRIPTOR.message_types_by_name['Flags'] = _FLAGS
DESCRIPTOR.message_types_by_name['FwFlagsRequest'] = _FWFLAGSREQUEST
DESCRIPTOR.message_types_by_name['FwFlagsResponse'] = _FWFLAGSRESPONSE
DESCRIPTOR.message_types_by_name['FwExperimentSubscriptionRequest'] = _FWEXPERIMENTSUBSCRIPTIONREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RoboticsClientConfig = _reflection.GeneratedProtocolMessageType('RoboticsClientConfig', (_message.Message,), {
  'DESCRIPTOR' : _ROBOTICSCLIENTCONFIG,
  '__module__' : 'experiment_config_pb2'
  # @@protoc_insertion_point(class_scope:robotics.infrastructure.RoboticsClientConfig)
  })
_sym_db.RegisterMessage(RoboticsClientConfig)

TaskProperties = _reflection.GeneratedProtocolMessageType('TaskProperties', (_message.Message,), {
  'DESCRIPTOR' : _TASKPROPERTIES,
  '__module__' : 'experiment_config_pb2'
  # @@protoc_insertion_point(class_scope:robotics.infrastructure.TaskProperties)
  })
_sym_db.RegisterMessage(TaskProperties)

Flag = _reflection.GeneratedProtocolMessageType('Flag', (_message.Message,), {
  'DESCRIPTOR' : _FLAG,
  '__module__' : 'experiment_config_pb2'
  # @@protoc_insertion_point(class_scope:robotics.infrastructure.Flag)
  })
_sym_db.RegisterMessage(Flag)

Flags = _reflection.GeneratedProtocolMessageType('Flags', (_message.Message,), {
  'DESCRIPTOR' : _FLAGS,
  '__module__' : 'experiment_config_pb2'
  # @@protoc_insertion_point(class_scope:robotics.infrastructure.Flags)
  })
_sym_db.RegisterMessage(Flags)

FwFlagsRequest = _reflection.GeneratedProtocolMessageType('FwFlagsRequest', (_message.Message,), {
  'DESCRIPTOR' : _FWFLAGSREQUEST,
  '__module__' : 'experiment_config_pb2'
  # @@protoc_insertion_point(class_scope:robotics.infrastructure.FwFlagsRequest)
  })
_sym_db.RegisterMessage(FwFlagsRequest)

FwFlagsResponse = _reflection.GeneratedProtocolMessageType('FwFlagsResponse', (_message.Message,), {
  'DESCRIPTOR' : _FWFLAGSRESPONSE,
  '__module__' : 'experiment_config_pb2'
  # @@protoc_insertion_point(class_scope:robotics.infrastructure.FwFlagsResponse)
  })
_sym_db.RegisterMessage(FwFlagsResponse)

FwExperimentSubscriptionRequest = _reflection.GeneratedProtocolMessageType('FwExperimentSubscriptionRequest', (_message.Message,), {
  'DESCRIPTOR' : _FWEXPERIMENTSUBSCRIPTIONREQUEST,
  '__module__' : 'experiment_config_pb2'
  # @@protoc_insertion_point(class_scope:robotics.infrastructure.FwExperimentSubscriptionRequest)
  })
_sym_db.RegisterMessage(FwExperimentSubscriptionRequest)


# @@protoc_insertion_point(module_scope)
