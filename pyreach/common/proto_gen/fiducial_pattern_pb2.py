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
# source: fiducial_pattern.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import pyreach.common.proto_gen.vector_pb2 as vector__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='fiducial_pattern.proto',
  package='robotics.messages',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x16\x66iducial_pattern.proto\x12\x11robotics.messages\x1a\x0cvector.proto\"\x94\x02\n\x15\x41prilTagPatternConfig\x12\x46\n\ntag_family\x18\x01 \x01(\x0e\x32\x32.robotics.messages.AprilTagPatternConfig.TagFamily\x12\x0b\n\x03ids\x18\x02 \x03(\x05\x12\x1b\n\x13square_spacing_bits\x18\x04 \x01(\r\x12\x1d\n\x15intertag_black_square\x18\x05 \x01(\x08\"j\n\tTagFamily\x12\x1a\n\x16UNSPECIFIED_TAG_FAMILY\x10\x00\x12\x0b\n\x07TAG16H5\x10\x01\x12\x0b\n\x07TAG25H7\x10\x02\x12\x0b\n\x07TAG25H9\x10\x03\x12\x0c\n\x08TAG36H10\x10\x04\x12\x0c\n\x08TAG36H11\x10\x05\"\x19\n\x17\x43hessboardPatternConfig\"\xe1\x02\n\x15\x46iducialPatternConfig\x12\x0c\n\x04rows\x18\x01 \x01(\r\x12\x0c\n\x04\x63ols\x18\x02 \x01(\r\x12\x18\n\x0emeters_per_bit\x18\x03 \x01(\x01H\x00\x12\x18\n\x0epixels_per_bit\x18\x04 \x01(\rH\x00\x12O\n\x19\x63hessboard_pattern_config\x18\x05 \x01(\x0b\x32*.robotics.messages.ChessboardPatternConfigH\x01\x12L\n\x18\x61pril_tag_pattern_config\x18\x06 \x01(\x0b\x32(.robotics.messages.AprilTagPatternConfigH\x01\x12+\n\x06offset\x18\x07 \x01(\x0b\x32\x1b.robotics.messages.Vector3dB\x11\n\x0f\x62it_sizing_typeB\x19\n\x17pattern_specific_configb\x06proto3'
  ,
  dependencies=[vector__pb2.DESCRIPTOR,])



_APRILTAGPATTERNCONFIG_TAGFAMILY = _descriptor.EnumDescriptor(
  name='TagFamily',
  full_name='robotics.messages.AprilTagPatternConfig.TagFamily',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSPECIFIED_TAG_FAMILY', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TAG16H5', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TAG25H7', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TAG25H9', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TAG36H10', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TAG36H11', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=230,
  serialized_end=336,
)
_sym_db.RegisterEnumDescriptor(_APRILTAGPATTERNCONFIG_TAGFAMILY)


_APRILTAGPATTERNCONFIG = _descriptor.Descriptor(
  name='AprilTagPatternConfig',
  full_name='robotics.messages.AprilTagPatternConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='tag_family', full_name='robotics.messages.AprilTagPatternConfig.tag_family', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ids', full_name='robotics.messages.AprilTagPatternConfig.ids', index=1,
      number=2, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='square_spacing_bits', full_name='robotics.messages.AprilTagPatternConfig.square_spacing_bits', index=2,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='intertag_black_square', full_name='robotics.messages.AprilTagPatternConfig.intertag_black_square', index=3,
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
    _APRILTAGPATTERNCONFIG_TAGFAMILY,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=60,
  serialized_end=336,
)


_CHESSBOARDPATTERNCONFIG = _descriptor.Descriptor(
  name='ChessboardPatternConfig',
  full_name='robotics.messages.ChessboardPatternConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=338,
  serialized_end=363,
)


_FIDUCIALPATTERNCONFIG = _descriptor.Descriptor(
  name='FiducialPatternConfig',
  full_name='robotics.messages.FiducialPatternConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='rows', full_name='robotics.messages.FiducialPatternConfig.rows', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cols', full_name='robotics.messages.FiducialPatternConfig.cols', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='meters_per_bit', full_name='robotics.messages.FiducialPatternConfig.meters_per_bit', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='pixels_per_bit', full_name='robotics.messages.FiducialPatternConfig.pixels_per_bit', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='chessboard_pattern_config', full_name='robotics.messages.FiducialPatternConfig.chessboard_pattern_config', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='april_tag_pattern_config', full_name='robotics.messages.FiducialPatternConfig.april_tag_pattern_config', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='offset', full_name='robotics.messages.FiducialPatternConfig.offset', index=6,
      number=7, type=11, cpp_type=10, label=1,
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
    _descriptor.OneofDescriptor(
      name='bit_sizing_type', full_name='robotics.messages.FiducialPatternConfig.bit_sizing_type',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='pattern_specific_config', full_name='robotics.messages.FiducialPatternConfig.pattern_specific_config',
      index=1, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=366,
  serialized_end=719,
)

_APRILTAGPATTERNCONFIG.fields_by_name['tag_family'].enum_type = _APRILTAGPATTERNCONFIG_TAGFAMILY
_APRILTAGPATTERNCONFIG_TAGFAMILY.containing_type = _APRILTAGPATTERNCONFIG
_FIDUCIALPATTERNCONFIG.fields_by_name['chessboard_pattern_config'].message_type = _CHESSBOARDPATTERNCONFIG
_FIDUCIALPATTERNCONFIG.fields_by_name['april_tag_pattern_config'].message_type = _APRILTAGPATTERNCONFIG
_FIDUCIALPATTERNCONFIG.fields_by_name['offset'].message_type = vector__pb2._VECTOR3D
_FIDUCIALPATTERNCONFIG.oneofs_by_name['bit_sizing_type'].fields.append(
  _FIDUCIALPATTERNCONFIG.fields_by_name['meters_per_bit'])
_FIDUCIALPATTERNCONFIG.fields_by_name['meters_per_bit'].containing_oneof = _FIDUCIALPATTERNCONFIG.oneofs_by_name['bit_sizing_type']
_FIDUCIALPATTERNCONFIG.oneofs_by_name['bit_sizing_type'].fields.append(
  _FIDUCIALPATTERNCONFIG.fields_by_name['pixels_per_bit'])
_FIDUCIALPATTERNCONFIG.fields_by_name['pixels_per_bit'].containing_oneof = _FIDUCIALPATTERNCONFIG.oneofs_by_name['bit_sizing_type']
_FIDUCIALPATTERNCONFIG.oneofs_by_name['pattern_specific_config'].fields.append(
  _FIDUCIALPATTERNCONFIG.fields_by_name['chessboard_pattern_config'])
_FIDUCIALPATTERNCONFIG.fields_by_name['chessboard_pattern_config'].containing_oneof = _FIDUCIALPATTERNCONFIG.oneofs_by_name['pattern_specific_config']
_FIDUCIALPATTERNCONFIG.oneofs_by_name['pattern_specific_config'].fields.append(
  _FIDUCIALPATTERNCONFIG.fields_by_name['april_tag_pattern_config'])
_FIDUCIALPATTERNCONFIG.fields_by_name['april_tag_pattern_config'].containing_oneof = _FIDUCIALPATTERNCONFIG.oneofs_by_name['pattern_specific_config']
DESCRIPTOR.message_types_by_name['AprilTagPatternConfig'] = _APRILTAGPATTERNCONFIG
DESCRIPTOR.message_types_by_name['ChessboardPatternConfig'] = _CHESSBOARDPATTERNCONFIG
DESCRIPTOR.message_types_by_name['FiducialPatternConfig'] = _FIDUCIALPATTERNCONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AprilTagPatternConfig = _reflection.GeneratedProtocolMessageType('AprilTagPatternConfig', (_message.Message,), {
  'DESCRIPTOR' : _APRILTAGPATTERNCONFIG,
  '__module__' : 'fiducial_pattern_pb2'
  # @@protoc_insertion_point(class_scope:robotics.messages.AprilTagPatternConfig)
  })
_sym_db.RegisterMessage(AprilTagPatternConfig)

ChessboardPatternConfig = _reflection.GeneratedProtocolMessageType('ChessboardPatternConfig', (_message.Message,), {
  'DESCRIPTOR' : _CHESSBOARDPATTERNCONFIG,
  '__module__' : 'fiducial_pattern_pb2'
  # @@protoc_insertion_point(class_scope:robotics.messages.ChessboardPatternConfig)
  })
_sym_db.RegisterMessage(ChessboardPatternConfig)

FiducialPatternConfig = _reflection.GeneratedProtocolMessageType('FiducialPatternConfig', (_message.Message,), {
  'DESCRIPTOR' : _FIDUCIALPATTERNCONFIG,
  '__module__' : 'fiducial_pattern_pb2'
  # @@protoc_insertion_point(class_scope:robotics.messages.FiducialPatternConfig)
  })
_sym_db.RegisterMessage(FiducialPatternConfig)


# @@protoc_insertion_point(module_scope)
