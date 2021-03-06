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
# source: named_io.proto

from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='named_io.proto',
  package='robotics.logging.messages',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0enamed_io.proto\x12\x19robotics.logging.messages\"\x9e\x01\n\x07NamedIo\x12<\n\x05state\x18\x01 \x03(\x0b\x32-.robotics.logging.messages.NamedIo.StateEntry\x1aU\n\nStateEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x36\n\x05value\x18\x02 \x01(\x0b\x32\'.robotics.logging.messages.NamedIoState:\x02\x38\x01\"[\n\x0cNamedIoState\x12@\n\rdigital_value\x18\x02 \x01(\x0e\x32\'.robotics.logging.messages.DigitalStateH\x00\x42\t\n\x07payload*{\n\x0c\x44igitalState\x12\x1d\n\x19\x44IGITAL_STATE_UNSPECIFIED\x10\x00\x12\x15\n\x11\x44IGITAL_STATE_OFF\x10\x01\x12\x14\n\x10\x44IGITAL_STATE_ON\x10\x02\x12\x1f\n\x1b\x44IGITAL_STATE_INDETERMINATE\x10\x03'
)

_DIGITALSTATE = _descriptor.EnumDescriptor(
  name='DigitalState',
  full_name='robotics.logging.messages.DigitalState',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DIGITAL_STATE_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DIGITAL_STATE_OFF', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DIGITAL_STATE_ON', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DIGITAL_STATE_INDETERMINATE', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=299,
  serialized_end=422,
)
_sym_db.RegisterEnumDescriptor(_DIGITALSTATE)

DigitalState = enum_type_wrapper.EnumTypeWrapper(_DIGITALSTATE)
DIGITAL_STATE_UNSPECIFIED = 0
DIGITAL_STATE_OFF = 1
DIGITAL_STATE_ON = 2
DIGITAL_STATE_INDETERMINATE = 3



_NAMEDIO_STATEENTRY = _descriptor.Descriptor(
  name='StateEntry',
  full_name='robotics.logging.messages.NamedIo.StateEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='robotics.logging.messages.NamedIo.StateEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='robotics.logging.messages.NamedIo.StateEntry.value', index=1,
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
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=119,
  serialized_end=204,
)

_NAMEDIO = _descriptor.Descriptor(
  name='NamedIo',
  full_name='robotics.logging.messages.NamedIo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='state', full_name='robotics.logging.messages.NamedIo.state', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_NAMEDIO_STATEENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=46,
  serialized_end=204,
)


_NAMEDIOSTATE = _descriptor.Descriptor(
  name='NamedIoState',
  full_name='robotics.logging.messages.NamedIoState',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='digital_value', full_name='robotics.logging.messages.NamedIoState.digital_value', index=0,
      number=2, type=14, cpp_type=8, label=1,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='payload', full_name='robotics.logging.messages.NamedIoState.payload',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=206,
  serialized_end=297,
)

_NAMEDIO_STATEENTRY.fields_by_name['value'].message_type = _NAMEDIOSTATE
_NAMEDIO_STATEENTRY.containing_type = _NAMEDIO
_NAMEDIO.fields_by_name['state'].message_type = _NAMEDIO_STATEENTRY
_NAMEDIOSTATE.fields_by_name['digital_value'].enum_type = _DIGITALSTATE
_NAMEDIOSTATE.oneofs_by_name['payload'].fields.append(
  _NAMEDIOSTATE.fields_by_name['digital_value'])
_NAMEDIOSTATE.fields_by_name['digital_value'].containing_oneof = _NAMEDIOSTATE.oneofs_by_name['payload']
DESCRIPTOR.message_types_by_name['NamedIo'] = _NAMEDIO
DESCRIPTOR.message_types_by_name['NamedIoState'] = _NAMEDIOSTATE
DESCRIPTOR.enum_types_by_name['DigitalState'] = _DIGITALSTATE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

NamedIo = _reflection.GeneratedProtocolMessageType('NamedIo', (_message.Message,), {

  'StateEntry' : _reflection.GeneratedProtocolMessageType('StateEntry', (_message.Message,), {
    'DESCRIPTOR' : _NAMEDIO_STATEENTRY,
    '__module__' : 'named_io_pb2'
    # @@protoc_insertion_point(class_scope:robotics.logging.messages.NamedIo.StateEntry)
    })
  ,
  'DESCRIPTOR' : _NAMEDIO,
  '__module__' : 'named_io_pb2'
  # @@protoc_insertion_point(class_scope:robotics.logging.messages.NamedIo)
  })
_sym_db.RegisterMessage(NamedIo)
_sym_db.RegisterMessage(NamedIo.StateEntry)

NamedIoState = _reflection.GeneratedProtocolMessageType('NamedIoState', (_message.Message,), {
  'DESCRIPTOR' : _NAMEDIOSTATE,
  '__module__' : 'named_io_pb2'
  # @@protoc_insertion_point(class_scope:robotics.logging.messages.NamedIoState)
  })
_sym_db.RegisterMessage(NamedIoState)


_NAMEDIO_STATEENTRY._options = None
# @@protoc_insertion_point(module_scope)
