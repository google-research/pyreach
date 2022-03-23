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

"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import log_entry_id_pb2
import log_entry_reach_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class LogEntry(google.protobuf.message.Message):
    """Processed result for single log event from robot."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    ID_FIELD_NUMBER: builtins.int
    REACH_FIELD_NUMBER: builtins.int
    @property
    def id(self) -> log_entry_id_pb2.LogEntryId: ...
    @property
    def reach(self) -> log_entry_reach_pb2.ReachPayload: ...
    def __init__(self,
        *,
        id : typing.Optional[log_entry_id_pb2.LogEntryId] = ...,
        reach : typing.Optional[log_entry_reach_pb2.ReachPayload] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["id",b"id","payload",b"payload","reach",b"reach"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["id",b"id","payload",b"payload","reach",b"reach"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["payload",b"payload"]) -> typing.Optional[typing_extensions.Literal["reach"]]: ...
global___LogEntry = LogEntry