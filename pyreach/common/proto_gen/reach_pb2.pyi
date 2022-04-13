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
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import logs_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class ReachPayload(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    COMMAND_DATA_FIELD_NUMBER: builtins.int
    DEVICE_DATA_FIELD_NUMBER: builtins.int
    SERVER_LOG_DATA_FIELD_NUMBER: builtins.int
    TASK_START_COMMAND_FIELD_NUMBER: builtins.int
    TASK_END_COMMAND_FIELD_NUMBER: builtins.int
    REACH_SERVE_SESSION_ID_FIELD_NUMBER: builtins.int
    @property
    def command_data(self) -> logs_pb2.CommandData: ...
    @property
    def device_data(self) -> logs_pb2.DeviceData: ...
    @property
    def server_log_data(self) -> logs_pb2.TextLogData: ...
    @property
    def task_start_command(self) -> global___TaskStartCommand: ...
    @property
    def task_end_command(self) -> global___TaskEndCommand: ...
    reach_serve_session_id: typing.Text
    """robot session, which may have multiple operator sessions within it. This is
    normally unchanged reach serve lifetime.
    """

    def __init__(self,
        *,
        command_data: typing.Optional[logs_pb2.CommandData] = ...,
        device_data: typing.Optional[logs_pb2.DeviceData] = ...,
        server_log_data: typing.Optional[logs_pb2.TextLogData] = ...,
        task_start_command: typing.Optional[global___TaskStartCommand] = ...,
        task_end_command: typing.Optional[global___TaskEndCommand] = ...,
        reach_serve_session_id: typing.Optional[typing.Text] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["command_data",b"command_data","data",b"data","device_data",b"device_data","reach_serve_session_id",b"reach_serve_session_id","server_log_data",b"server_log_data","task_end_command",b"task_end_command","task_start_command",b"task_start_command"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["command_data",b"command_data","data",b"data","device_data",b"device_data","reach_serve_session_id",b"reach_serve_session_id","server_log_data",b"server_log_data","task_end_command",b"task_end_command","task_start_command",b"task_start_command"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["data",b"data"]) -> typing.Optional[typing_extensions.Literal["command_data","device_data","server_log_data","task_start_command","task_end_command"]]: ...
global___ReachPayload = ReachPayload

class TaskStartCommand(google.protobuf.message.Message):
    """TaskStartCommand represents the start of a Reach task, which is started from
    the UI with a given intent and task code within the Reach system. These
    messages are intended to eventually be replaced by generic log entry task
    messages.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    INTENT_FIELD_NUMBER: builtins.int
    TASK_CODE_FIELD_NUMBER: builtins.int
    intent: typing.Text
    task_code: typing.Text
    def __init__(self,
        *,
        intent: typing.Optional[typing.Text] = ...,
        task_code: typing.Optional[typing.Text] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["intent",b"intent","task_code",b"task_code"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["intent",b"intent","task_code",b"task_code"]) -> None: ...
global___TaskStartCommand = TaskStartCommand

class TaskEndCommand(google.protobuf.message.Message):
    """TaskEndCommand represents the end of a Reach task, which is stopped from the
    UI with either success or failure by the user clicking a corresponding
    button. These messages are intended to eventually be replaced by generic log
    entry task messages.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class _State:
        ValueType = typing.NewType('ValueType', builtins.int)
        V: typing_extensions.TypeAlias = ValueType
    class _StateEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[TaskEndCommand._State.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        UNKNOWN: TaskEndCommand._State.ValueType  # 0
        """event param task-success not found or invalid"""

        FAILURE: TaskEndCommand._State.ValueType  # 1
        """event param task-success = FAILURE"""

        SUCCESS: TaskEndCommand._State.ValueType  # 2
        """event param task-success = SUCCESS"""

    class State(_State, metaclass=_StateEnumTypeWrapper):
        pass

    UNKNOWN: TaskEndCommand.State.ValueType  # 0
    """event param task-success not found or invalid"""

    FAILURE: TaskEndCommand.State.ValueType  # 1
    """event param task-success = FAILURE"""

    SUCCESS: TaskEndCommand.State.ValueType  # 2
    """event param task-success = SUCCESS"""


    EVENT_NAME_FIELD_NUMBER: builtins.int
    STATE_FIELD_NUMBER: builtins.int
    event_name: typing.Text
    state: global___TaskEndCommand.State.ValueType
    def __init__(self,
        *,
        event_name: typing.Optional[typing.Text] = ...,
        state: typing.Optional[global___TaskEndCommand.State.ValueType] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["event_name",b"event_name","state",b"state"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["event_name",b"event_name","state",b"state"]) -> None: ...
global___TaskEndCommand = TaskEndCommand