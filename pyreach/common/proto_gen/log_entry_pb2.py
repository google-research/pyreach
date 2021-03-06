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
# source: log_entry.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
import pyreach.common.proto_gen.log_entry_id_pb2 as log__entry__id__pb2
import pyreach.common.proto_gen.calibration_config_pb2 as calibration__config__pb2
import pyreach.common.proto_gen.general_io_pb2 as general__io__pb2
import pyreach.common.proto_gen.image_pb2 as image__pb2
import pyreach.common.proto_gen.named_io_pb2 as named__io__pb2
import pyreach.common.proto_gen.joints_pb2 as joints__pb2
import pyreach.common.proto_gen.juggler_pb2 as juggler__pb2
import pyreach.common.proto_gen.reach_pb2 as reach__pb2
import pyreach.common.proto_gen.robot_control_pb2 as robot__control__pb2
import pyreach.common.proto_gen.simulation_pb2 as simulation__pb2
import pyreach.common.proto_gen.transform_pb2 as transform__pb2
import pyreach.common.proto_gen.calibration_pb2 as calibration__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='log_entry.proto',
  package='robotics.logging',
  syntax='proto2',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0flog_entry.proto\x12\x10robotics.logging\x1a\x19google/protobuf/any.proto\x1a\x12log_entry_id.proto\x1a\x18\x63\x61libration_config.proto\x1a\x10general_io.proto\x1a\x0bimage.proto\x1a\x0enamed_io.proto\x1a\x0cjoints.proto\x1a\rjuggler.proto\x1a\x0breach.proto\x1a\x13robot_control.proto\x1a\x10simulation.proto\x1a\x0ftransform.proto\x1a\x11\x63\x61libration.proto\"\xb7\x03\n\x10LogEntryMetadata\x12>\n\tkey_value\x18\x01 \x03(\x0b\x32+.robotics.logging.LogEntryMetadata.KeyValue\x12=\n\x07\x63ommand\x18\x06 \x01(\x0b\x32*.robotics.logging.messages.CommandMetadataH\x00\x12\x39\n\x05state\x18\x10 \x01(\x0b\x32(.robotics.logging.messages.StateMetadataH\x00\x12\x43\n\nphasespace\x18\n \x01(\x0b\x32-.robotics.logging.messages.PhaseSpaceMetadataH\x00\x12\x39\n\x05image\x18\x0c \x01(\x0b\x32(.robotics.logging.messages.ImageMetadataH\x00\x12\x39\n\x05video\x18\r \x01(\x0b\x32(.robotics.logging.messages.VideoMetadataH\x00\x1a&\n\x08KeyValue\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\tB\x06\n\x04\x64\x61ta\"\xb1\x06\n\x08LogEntry\x12(\n\x02id\x18\x01 \x01(\x0b\x32\x1c.robotics.logging.LogEntryId\x12\x30\n\x04meta\x18\x0f \x01(\x0b\x32\".robotics.logging.LogEntryMetadata\x12:\n\ngeneral_io\x18\x0b \x01(\x0b\x32$.robotics.logging.messages.GeneralIoH\x00\x12\x36\n\x08named_io\x18\x1d \x01(\x0b\x32\".robotics.logging.messages.NamedIoH\x00\x12\x33\n\x06joints\x18\x0c \x01(\x0b\x32!.robotics.logging.messages.JointsH\x00\x12\x39\n\ttransform\x18\r \x01(\x0b\x32$.robotics.logging.messages.TransformH\x00\x12\x38\n\rencoded_image\x18\x0e \x01(\x0b\x32\x1f.robotics.messages.EncodedImageH\x00\x12J\n\x12simulation_command\x18\x1a \x01(\x0b\x32,.robotics.logging.messages.SimulationCommandH\x00\x12\x42\n\x12\x63\x61mera_calibration\x18\x1b \x01(\x0b\x32$.robotics.messages.CameraCalibrationH\x00\x12Q\n\x19\x63\x61mera_calibration_config\x18\x1c \x01(\x0b\x32,.robotics.logging.messages.CalibrationConfigH\x00\x12\x42\n\x0esystem_command\x18\x13 \x01(\x0b\x32(.robotics.logging.messages.SystemCommandH\x00\x12>\n\x0csystem_state\x18\x16 \x01(\x0b\x32&.robotics.logging.messages.SystemStateH\x00\x12\x39\n\x05reach\x18\xe8\x07 \x01(\x0b\x32\'.robotics.logging.messages.ReachPayloadH\x00\x42\t\n\x07payload'
  ,
  dependencies=[google_dot_protobuf_dot_any__pb2.DESCRIPTOR,log__entry__id__pb2.DESCRIPTOR,calibration__config__pb2.DESCRIPTOR,general__io__pb2.DESCRIPTOR,image__pb2.DESCRIPTOR,named__io__pb2.DESCRIPTOR,joints__pb2.DESCRIPTOR,juggler__pb2.DESCRIPTOR,reach__pb2.DESCRIPTOR,robot__control__pb2.DESCRIPTOR,simulation__pb2.DESCRIPTOR,transform__pb2.DESCRIPTOR,calibration__pb2.DESCRIPTOR,])




_LOGENTRYMETADATA_KEYVALUE = _descriptor.Descriptor(
  name='KeyValue',
  full_name='robotics.logging.LogEntryMetadata.KeyValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='robotics.logging.LogEntryMetadata.KeyValue.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='robotics.logging.LogEntryMetadata.KeyValue.value', index=1,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=668,
  serialized_end=706,
)

_LOGENTRYMETADATA = _descriptor.Descriptor(
  name='LogEntryMetadata',
  full_name='robotics.logging.LogEntryMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key_value', full_name='robotics.logging.LogEntryMetadata.key_value', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='command', full_name='robotics.logging.LogEntryMetadata.command', index=1,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='state', full_name='robotics.logging.LogEntryMetadata.state', index=2,
      number=16, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='phasespace', full_name='robotics.logging.LogEntryMetadata.phasespace', index=3,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='image', full_name='robotics.logging.LogEntryMetadata.image', index=4,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='video', full_name='robotics.logging.LogEntryMetadata.video', index=5,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_LOGENTRYMETADATA_KEYVALUE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='data', full_name='robotics.logging.LogEntryMetadata.data',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=275,
  serialized_end=714,
)


_LOGENTRY = _descriptor.Descriptor(
  name='LogEntry',
  full_name='robotics.logging.LogEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='robotics.logging.LogEntry.id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='meta', full_name='robotics.logging.LogEntry.meta', index=1,
      number=15, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='general_io', full_name='robotics.logging.LogEntry.general_io', index=2,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='named_io', full_name='robotics.logging.LogEntry.named_io', index=3,
      number=29, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='joints', full_name='robotics.logging.LogEntry.joints', index=4,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='transform', full_name='robotics.logging.LogEntry.transform', index=5,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='encoded_image', full_name='robotics.logging.LogEntry.encoded_image', index=6,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='simulation_command', full_name='robotics.logging.LogEntry.simulation_command', index=7,
      number=26, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='camera_calibration', full_name='robotics.logging.LogEntry.camera_calibration', index=8,
      number=27, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='camera_calibration_config', full_name='robotics.logging.LogEntry.camera_calibration_config', index=9,
      number=28, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='system_command', full_name='robotics.logging.LogEntry.system_command', index=10,
      number=19, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='system_state', full_name='robotics.logging.LogEntry.system_state', index=11,
      number=22, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='reach', full_name='robotics.logging.LogEntry.reach', index=12,
      number=1000, type=11, cpp_type=10, label=1,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='payload', full_name='robotics.logging.LogEntry.payload',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=717,
  serialized_end=1534,
)

_LOGENTRYMETADATA_KEYVALUE.containing_type = _LOGENTRYMETADATA
_LOGENTRYMETADATA.fields_by_name['key_value'].message_type = _LOGENTRYMETADATA_KEYVALUE
_LOGENTRYMETADATA.fields_by_name['command'].message_type = robot__control__pb2._COMMANDMETADATA
_LOGENTRYMETADATA.fields_by_name['state'].message_type = robot__control__pb2._STATEMETADATA
_LOGENTRYMETADATA.fields_by_name['phasespace'].message_type = juggler__pb2._PHASESPACEMETADATA
_LOGENTRYMETADATA.fields_by_name['image'].message_type = juggler__pb2._IMAGEMETADATA
_LOGENTRYMETADATA.fields_by_name['video'].message_type = juggler__pb2._VIDEOMETADATA
_LOGENTRYMETADATA.oneofs_by_name['data'].fields.append(
  _LOGENTRYMETADATA.fields_by_name['command'])
_LOGENTRYMETADATA.fields_by_name['command'].containing_oneof = _LOGENTRYMETADATA.oneofs_by_name['data']
_LOGENTRYMETADATA.oneofs_by_name['data'].fields.append(
  _LOGENTRYMETADATA.fields_by_name['state'])
_LOGENTRYMETADATA.fields_by_name['state'].containing_oneof = _LOGENTRYMETADATA.oneofs_by_name['data']
_LOGENTRYMETADATA.oneofs_by_name['data'].fields.append(
  _LOGENTRYMETADATA.fields_by_name['phasespace'])
_LOGENTRYMETADATA.fields_by_name['phasespace'].containing_oneof = _LOGENTRYMETADATA.oneofs_by_name['data']
_LOGENTRYMETADATA.oneofs_by_name['data'].fields.append(
  _LOGENTRYMETADATA.fields_by_name['image'])
_LOGENTRYMETADATA.fields_by_name['image'].containing_oneof = _LOGENTRYMETADATA.oneofs_by_name['data']
_LOGENTRYMETADATA.oneofs_by_name['data'].fields.append(
  _LOGENTRYMETADATA.fields_by_name['video'])
_LOGENTRYMETADATA.fields_by_name['video'].containing_oneof = _LOGENTRYMETADATA.oneofs_by_name['data']
_LOGENTRY.fields_by_name['id'].message_type = log__entry__id__pb2._LOGENTRYID
_LOGENTRY.fields_by_name['meta'].message_type = _LOGENTRYMETADATA
_LOGENTRY.fields_by_name['general_io'].message_type = general__io__pb2._GENERALIO
_LOGENTRY.fields_by_name['named_io'].message_type = named__io__pb2._NAMEDIO
_LOGENTRY.fields_by_name['joints'].message_type = joints__pb2._JOINTS
_LOGENTRY.fields_by_name['transform'].message_type = transform__pb2._TRANSFORM
_LOGENTRY.fields_by_name['encoded_image'].message_type = image__pb2._ENCODEDIMAGE
_LOGENTRY.fields_by_name['simulation_command'].message_type = simulation__pb2._SIMULATIONCOMMAND
_LOGENTRY.fields_by_name['camera_calibration'].message_type = calibration__pb2._CAMERACALIBRATION
_LOGENTRY.fields_by_name['camera_calibration_config'].message_type = calibration__config__pb2._CALIBRATIONCONFIG
_LOGENTRY.fields_by_name['system_command'].message_type = robot__control__pb2._SYSTEMCOMMAND
_LOGENTRY.fields_by_name['system_state'].message_type = robot__control__pb2._SYSTEMSTATE
_LOGENTRY.fields_by_name['reach'].message_type = reach__pb2._REACHPAYLOAD
_LOGENTRY.oneofs_by_name['payload'].fields.append(
  _LOGENTRY.fields_by_name['general_io'])
_LOGENTRY.fields_by_name['general_io'].containing_oneof = _LOGENTRY.oneofs_by_name['payload']
_LOGENTRY.oneofs_by_name['payload'].fields.append(
  _LOGENTRY.fields_by_name['named_io'])
_LOGENTRY.fields_by_name['named_io'].containing_oneof = _LOGENTRY.oneofs_by_name['payload']
_LOGENTRY.oneofs_by_name['payload'].fields.append(
  _LOGENTRY.fields_by_name['joints'])
_LOGENTRY.fields_by_name['joints'].containing_oneof = _LOGENTRY.oneofs_by_name['payload']
_LOGENTRY.oneofs_by_name['payload'].fields.append(
  _LOGENTRY.fields_by_name['transform'])
_LOGENTRY.fields_by_name['transform'].containing_oneof = _LOGENTRY.oneofs_by_name['payload']
_LOGENTRY.oneofs_by_name['payload'].fields.append(
  _LOGENTRY.fields_by_name['encoded_image'])
_LOGENTRY.fields_by_name['encoded_image'].containing_oneof = _LOGENTRY.oneofs_by_name['payload']
_LOGENTRY.oneofs_by_name['payload'].fields.append(
  _LOGENTRY.fields_by_name['simulation_command'])
_LOGENTRY.fields_by_name['simulation_command'].containing_oneof = _LOGENTRY.oneofs_by_name['payload']
_LOGENTRY.oneofs_by_name['payload'].fields.append(
  _LOGENTRY.fields_by_name['camera_calibration'])
_LOGENTRY.fields_by_name['camera_calibration'].containing_oneof = _LOGENTRY.oneofs_by_name['payload']
_LOGENTRY.oneofs_by_name['payload'].fields.append(
  _LOGENTRY.fields_by_name['camera_calibration_config'])
_LOGENTRY.fields_by_name['camera_calibration_config'].containing_oneof = _LOGENTRY.oneofs_by_name['payload']
_LOGENTRY.oneofs_by_name['payload'].fields.append(
  _LOGENTRY.fields_by_name['system_command'])
_LOGENTRY.fields_by_name['system_command'].containing_oneof = _LOGENTRY.oneofs_by_name['payload']
_LOGENTRY.oneofs_by_name['payload'].fields.append(
  _LOGENTRY.fields_by_name['system_state'])
_LOGENTRY.fields_by_name['system_state'].containing_oneof = _LOGENTRY.oneofs_by_name['payload']
_LOGENTRY.oneofs_by_name['payload'].fields.append(
  _LOGENTRY.fields_by_name['reach'])
_LOGENTRY.fields_by_name['reach'].containing_oneof = _LOGENTRY.oneofs_by_name['payload']
DESCRIPTOR.message_types_by_name['LogEntryMetadata'] = _LOGENTRYMETADATA
DESCRIPTOR.message_types_by_name['LogEntry'] = _LOGENTRY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LogEntryMetadata = _reflection.GeneratedProtocolMessageType('LogEntryMetadata', (_message.Message,), {

  'KeyValue' : _reflection.GeneratedProtocolMessageType('KeyValue', (_message.Message,), {
    'DESCRIPTOR' : _LOGENTRYMETADATA_KEYVALUE,
    '__module__' : 'log_entry_pb2'
    # @@protoc_insertion_point(class_scope:robotics.logging.LogEntryMetadata.KeyValue)
    })
  ,
  'DESCRIPTOR' : _LOGENTRYMETADATA,
  '__module__' : 'log_entry_pb2'
  # @@protoc_insertion_point(class_scope:robotics.logging.LogEntryMetadata)
  })
_sym_db.RegisterMessage(LogEntryMetadata)
_sym_db.RegisterMessage(LogEntryMetadata.KeyValue)

LogEntry = _reflection.GeneratedProtocolMessageType('LogEntry', (_message.Message,), {
  'DESCRIPTOR' : _LOGENTRY,
  '__module__' : 'log_entry_pb2'
  # @@protoc_insertion_point(class_scope:robotics.logging.LogEntry)
  })
_sym_db.RegisterMessage(LogEntry)


# @@protoc_insertion_point(module_scope)
