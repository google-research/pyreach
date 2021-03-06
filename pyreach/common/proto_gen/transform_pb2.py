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
# source: transform.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='transform.proto',
  package='robotics.logging.messages',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0ftransform.proto\x12\x19robotics.logging.messages\"\xfc\x01\n\tTransform\x12\x14\n\x08position\x18\x01 \x03(\x01\x42\x02\x10\x01\x12\x16\n\nquaternion\x18\x02 \x03(\x01\x42\x02\x10\x01\x12\x14\n\x08velocity\x18\x03 \x03(\x01\x42\x02\x10\x01\x12\x1c\n\x10\x61ngular_velocity\x18\x04 \x03(\x01\x42\x02\x10\x01\x12\x18\n\x0c\x61\x63\x63\x65leration\x18\x05 \x03(\x01\x42\x02\x10\x01\x12 \n\x14\x61ngular_acceleration\x18\x06 \x03(\x01\x42\x02\x10\x01\x12\x10\n\x04jerk\x18\x07 \x03(\x01\x42\x02\x10\x01\x12\x18\n\x0c\x61ngular_jerk\x18\x08 \x03(\x01\x42\x02\x10\x01\x12\x11\n\x05\x66orce\x18\t \x03(\x01\x42\x02\x10\x01\x12\x12\n\x06torque\x18\n \x03(\x01\x42\x02\x10\x01\"^\n\rTransformMeta\x12\x16\n\x0e\x66rame_measured\x18\x01 \x01(\t\x12\x17\n\x0f\x66rame_reference\x18\x02 \x01(\t\x12\x1c\n\x14\x66rame_representation\x18\x03 \x01(\t'
)




_TRANSFORM = _descriptor.Descriptor(
  name='Transform',
  full_name='robotics.logging.messages.Transform',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='position', full_name='robotics.logging.messages.Transform.position', index=0,
      number=1, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='quaternion', full_name='robotics.logging.messages.Transform.quaternion', index=1,
      number=2, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='velocity', full_name='robotics.logging.messages.Transform.velocity', index=2,
      number=3, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='angular_velocity', full_name='robotics.logging.messages.Transform.angular_velocity', index=3,
      number=4, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='acceleration', full_name='robotics.logging.messages.Transform.acceleration', index=4,
      number=5, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='angular_acceleration', full_name='robotics.logging.messages.Transform.angular_acceleration', index=5,
      number=6, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='jerk', full_name='robotics.logging.messages.Transform.jerk', index=6,
      number=7, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='angular_jerk', full_name='robotics.logging.messages.Transform.angular_jerk', index=7,
      number=8, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='force', full_name='robotics.logging.messages.Transform.force', index=8,
      number=9, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='torque', full_name='robotics.logging.messages.Transform.torque', index=9,
      number=10, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  ],
  serialized_start=47,
  serialized_end=299,
)


_TRANSFORMMETA = _descriptor.Descriptor(
  name='TransformMeta',
  full_name='robotics.logging.messages.TransformMeta',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='frame_measured', full_name='robotics.logging.messages.TransformMeta.frame_measured', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='frame_reference', full_name='robotics.logging.messages.TransformMeta.frame_reference', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='frame_representation', full_name='robotics.logging.messages.TransformMeta.frame_representation', index=2,
      number=3, type=9, cpp_type=9, label=1,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=301,
  serialized_end=395,
)

DESCRIPTOR.message_types_by_name['Transform'] = _TRANSFORM
DESCRIPTOR.message_types_by_name['TransformMeta'] = _TRANSFORMMETA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Transform = _reflection.GeneratedProtocolMessageType('Transform', (_message.Message,), {
  'DESCRIPTOR' : _TRANSFORM,
  '__module__' : 'transform_pb2'
  # @@protoc_insertion_point(class_scope:robotics.logging.messages.Transform)
  })
_sym_db.RegisterMessage(Transform)

TransformMeta = _reflection.GeneratedProtocolMessageType('TransformMeta', (_message.Message,), {
  'DESCRIPTOR' : _TRANSFORMMETA,
  '__module__' : 'transform_pb2'
  # @@protoc_insertion_point(class_scope:robotics.logging.messages.TransformMeta)
  })
_sym_db.RegisterMessage(TransformMeta)


_TRANSFORM.fields_by_name['position']._options = None
_TRANSFORM.fields_by_name['quaternion']._options = None
_TRANSFORM.fields_by_name['velocity']._options = None
_TRANSFORM.fields_by_name['angular_velocity']._options = None
_TRANSFORM.fields_by_name['acceleration']._options = None
_TRANSFORM.fields_by_name['angular_acceleration']._options = None
_TRANSFORM.fields_by_name['jerk']._options = None
_TRANSFORM.fields_by_name['angular_jerk']._options = None
_TRANSFORM.fields_by_name['force']._options = None
_TRANSFORM.fields_by_name['torque']._options = None
# @@protoc_insertion_point(module_scope)
