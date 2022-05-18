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
# source: pose.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import pyreach.common.proto_gen.quaternion_pb2 as quaternion__pb2
import pyreach.common.proto_gen.vector_pb2 as vector__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='pose.proto',
  package='robotics.messages',
  syntax='proto3',
  serialized_options=b'\370\001\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\npose.proto\x12\x11robotics.messages\x1a\x10quaternion.proto\x1a\x0cvector.proto\"l\n\x06Pose3d\x12\x30\n\x0btranslation\x18\x01 \x01(\x0b\x32\x1b.robotics.messages.Vector3d\x12\x30\n\x08rotation\x18\x02 \x01(\x0b\x32\x1e.robotics.messages.Quaterniond\"p\n\x06Pose3f\x12\x30\n\x0btranslation\x18\x01 \x01(\x0b\x32\x1b.robotics.messages.Vector3f\x12\x30\n\x08rotation\x18\x02 \x01(\x0b\x32\x1e.robotics.messages.Quaternionf:\x02\x18\x01\"L\n\x06Pose2d\x12\x30\n\x0btranslation\x18\x01 \x01(\x0b\x32\x1b.robotics.messages.Vector2d\x12\x10\n\x08rotation\x18\x02 \x01(\x01\"L\n\x06Pose2f\x12\x30\n\x0btranslation\x18\x01 \x01(\x0b\x32\x1b.robotics.messages.Vector2f\x12\x10\n\x08rotation\x18\x02 \x01(\x02\"2\n\nRotation2d\x12\x11\n\tcos_angle\x18\x01 \x01(\x01\x12\x11\n\tsin_angle\x18\x02 \x01(\x01\"2\n\nRotation2f\x12\x11\n\tcos_angle\x18\x01 \x01(\x02\x12\x11\n\tsin_angle\x18\x02 \x01(\x02\x42\x03\xf8\x01\x01\x62\x06proto3'
  ,
  dependencies=[quaternion__pb2.DESCRIPTOR,vector__pb2.DESCRIPTOR,])




_POSE3D = _descriptor.Descriptor(
  name='Pose3d',
  full_name='robotics.messages.Pose3d',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='translation', full_name='robotics.messages.Pose3d.translation', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rotation', full_name='robotics.messages.Pose3d.rotation', index=1,
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
  serialized_start=65,
  serialized_end=173,
)


_POSE3F = _descriptor.Descriptor(
  name='Pose3f',
  full_name='robotics.messages.Pose3f',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='translation', full_name='robotics.messages.Pose3f.translation', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rotation', full_name='robotics.messages.Pose3f.rotation', index=1,
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
  serialized_options=b'\030\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=175,
  serialized_end=287,
)


_POSE2D = _descriptor.Descriptor(
  name='Pose2d',
  full_name='robotics.messages.Pose2d',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='translation', full_name='robotics.messages.Pose2d.translation', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rotation', full_name='robotics.messages.Pose2d.rotation', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=289,
  serialized_end=365,
)


_POSE2F = _descriptor.Descriptor(
  name='Pose2f',
  full_name='robotics.messages.Pose2f',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='translation', full_name='robotics.messages.Pose2f.translation', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='rotation', full_name='robotics.messages.Pose2f.rotation', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=367,
  serialized_end=443,
)


_ROTATION2D = _descriptor.Descriptor(
  name='Rotation2d',
  full_name='robotics.messages.Rotation2d',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cos_angle', full_name='robotics.messages.Rotation2d.cos_angle', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sin_angle', full_name='robotics.messages.Rotation2d.sin_angle', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=445,
  serialized_end=495,
)


_ROTATION2F = _descriptor.Descriptor(
  name='Rotation2f',
  full_name='robotics.messages.Rotation2f',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='cos_angle', full_name='robotics.messages.Rotation2f.cos_angle', index=0,
      number=1, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='sin_angle', full_name='robotics.messages.Rotation2f.sin_angle', index=1,
      number=2, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
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
  serialized_start=497,
  serialized_end=547,
)

_POSE3D.fields_by_name['translation'].message_type = vector__pb2._VECTOR3D
_POSE3D.fields_by_name['rotation'].message_type = quaternion__pb2._QUATERNIOND
_POSE3F.fields_by_name['translation'].message_type = vector__pb2._VECTOR3F
_POSE3F.fields_by_name['rotation'].message_type = quaternion__pb2._QUATERNIONF
_POSE2D.fields_by_name['translation'].message_type = vector__pb2._VECTOR2D
_POSE2F.fields_by_name['translation'].message_type = vector__pb2._VECTOR2F
DESCRIPTOR.message_types_by_name['Pose3d'] = _POSE3D
DESCRIPTOR.message_types_by_name['Pose3f'] = _POSE3F
DESCRIPTOR.message_types_by_name['Pose2d'] = _POSE2D
DESCRIPTOR.message_types_by_name['Pose2f'] = _POSE2F
DESCRIPTOR.message_types_by_name['Rotation2d'] = _ROTATION2D
DESCRIPTOR.message_types_by_name['Rotation2f'] = _ROTATION2F
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Pose3d = _reflection.GeneratedProtocolMessageType('Pose3d', (_message.Message,), {
  'DESCRIPTOR' : _POSE3D,
  '__module__' : 'pose_pb2'
  # @@protoc_insertion_point(class_scope:robotics.messages.Pose3d)
  })
_sym_db.RegisterMessage(Pose3d)

Pose3f = _reflection.GeneratedProtocolMessageType('Pose3f', (_message.Message,), {
  'DESCRIPTOR' : _POSE3F,
  '__module__' : 'pose_pb2'
  # @@protoc_insertion_point(class_scope:robotics.messages.Pose3f)
  })
_sym_db.RegisterMessage(Pose3f)

Pose2d = _reflection.GeneratedProtocolMessageType('Pose2d', (_message.Message,), {
  'DESCRIPTOR' : _POSE2D,
  '__module__' : 'pose_pb2'
  # @@protoc_insertion_point(class_scope:robotics.messages.Pose2d)
  })
_sym_db.RegisterMessage(Pose2d)

Pose2f = _reflection.GeneratedProtocolMessageType('Pose2f', (_message.Message,), {
  'DESCRIPTOR' : _POSE2F,
  '__module__' : 'pose_pb2'
  # @@protoc_insertion_point(class_scope:robotics.messages.Pose2f)
  })
_sym_db.RegisterMessage(Pose2f)

Rotation2d = _reflection.GeneratedProtocolMessageType('Rotation2d', (_message.Message,), {
  'DESCRIPTOR' : _ROTATION2D,
  '__module__' : 'pose_pb2'
  # @@protoc_insertion_point(class_scope:robotics.messages.Rotation2d)
  })
_sym_db.RegisterMessage(Rotation2d)

Rotation2f = _reflection.GeneratedProtocolMessageType('Rotation2f', (_message.Message,), {
  'DESCRIPTOR' : _ROTATION2F,
  '__module__' : 'pose_pb2'
  # @@protoc_insertion_point(class_scope:robotics.messages.Rotation2f)
  })
_sym_db.RegisterMessage(Rotation2f)


DESCRIPTOR._options = None
_POSE3F._options = None
# @@protoc_insertion_point(module_scope)
