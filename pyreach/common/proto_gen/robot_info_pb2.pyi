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
import google.protobuf.empty_pb2
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import joints_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class RobotInfo(google.protobuf.message.Message):
    """Robot related info provided by robot."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    ROBOT_ID_FIELD_NUMBER: builtins.int
    PROJECT_ID_FIELD_NUMBER: builtins.int
    ROBOT_REPOSITORY_TYPE_FIELD_NUMBER: builtins.int
    LOG_TOPIC_PREFIX_FIELD_NUMBER: builtins.int
    TASK_FIELD_NUMBER: builtins.int
    ROBOT_VERSION_FIELD_NUMBER: builtins.int
    PARTS_FIELD_NUMBER: builtins.int
    SHARED_OBJECTS_FIELD_NUMBER: builtins.int
    CONTROLLER_EXECUTION_FIELD_NUMBER: builtins.int
    TOASTER_COMMAND_HANDLING_FIELD_NUMBER: builtins.int
    robot_id: typing.Text = ...
    """Robot specified ID to identify physical robot. Format varies depending on
    robot species and project, this is used by processing pipeline to join
    event streams with the same robot_id. Required.
    """

    project_id: typing.Text = ...
    """ID to identify the project. Used to construct LogEntryId.log_types."""

    robot_repository_type: typing.Text = ...
    """The repository type used for robot commands and states, ie, `$kind` in
    go/robotics-ssot#repository. If not given, the robot info helpers
    (third_party/robotics/juggler/common/proto_utils/robot_info_helpers.h)
    use "logs" as the default.
    """

    log_topic_prefix: typing.Text = ...
    """String prepended onto the `$topic` in the log_type (go/robotics-ssot#id).
    A '/' is appended after this, followed by other log type identifiers (see
    go/juggler-controller-backend#logentryid). If not given, the robot info
    helpers use "robot" as the default.
    """

    task: typing.Text = ...
    """The task and/or experiment this episode is about, like dqn.123435. this is
    used by processing pipeline to determine output path of final result.
    """

    robot_version: typing.Text = ...
    """The robot software version. Format varies depending on robot species and
    project.
    """

    @property
    def parts(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___RobotPartInfo]:
        """Parts of the robot (eg, arm, gripper, etc)."""
        pass
    @property
    def shared_objects(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___SharedObjectInfo]:
        """Objects that will be shared between all parts and control modules."""
        pass
    @property
    def controller_execution(self) -> global___ControllerExecutionParams:
        """Parameters which control how the robot parts are executed."""
        pass
    toaster_command_handling: builtins.bool = ...
    """Temporary command handling logic that toaster needs. This causes the
    backend to discard non-system commands until the command queue has been
    drained (or a system command is found), to compensate for sending commands
    too fast. This is not really the correct way to handle this (the client
    should run slower than the backend), so this is a temporary hack that will
    be removed eventually. Therefore, no one but toaster should use it.
    """

    def __init__(self,
        *,
        robot_id : typing.Text = ...,
        project_id : typing.Text = ...,
        robot_repository_type : typing.Text = ...,
        log_topic_prefix : typing.Text = ...,
        task : typing.Text = ...,
        robot_version : typing.Text = ...,
        parts : typing.Optional[typing.Iterable[global___RobotPartInfo]] = ...,
        shared_objects : typing.Optional[typing.Iterable[global___SharedObjectInfo]] = ...,
        controller_execution : typing.Optional[global___ControllerExecutionParams] = ...,
        toaster_command_handling : builtins.bool = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["controller_execution",b"controller_execution"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["controller_execution",b"controller_execution","log_topic_prefix",b"log_topic_prefix","parts",b"parts","project_id",b"project_id","robot_id",b"robot_id","robot_repository_type",b"robot_repository_type","robot_version",b"robot_version","shared_objects",b"shared_objects","task",b"task","toaster_command_handling",b"toaster_command_handling"]) -> None: ...
global___RobotInfo = RobotInfo

class RobotPartInfo(google.protobuf.message.Message):
    """Part related info provided by the robot."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    ID_FIELD_NUMBER: builtins.int
    THREAD_ID_FIELD_NUMBER: builtins.int
    CONTROL_FREQUENCY_FIELD_NUMBER: builtins.int
    CONTROL_DUTY_CYCLE_FIELD_NUMBER: builtins.int
    JOINT_METADATA_FIELD_NUMBER: builtins.int
    CONTROL_MODULES_FIELD_NUMBER: builtins.int
    SUBORDINATE_PART_IDS_FIELD_NUMBER: builtins.int
    SUBORDINATE_STATE_SIGNAL_IDS_FIELD_NUMBER: builtins.int
    id: typing.Text = ...
    """Identifier for this part; must be unique within a given robot."""

    thread_id: typing.Text = ...
    """Which thread this part should run in. All parts with the same thread id
    will run in the same thread. If empty, a unique thread_id will be generated
    based on the part id and the part will run in its own thread.
    """

    control_frequency: builtins.float = ...
    """The rate the part steps can be controlled either by specifying an absolute
    frequency or a duty cycle relative to the highest rate part in this thread
    (absolute frequency = highest frequency in part thread / duty cycle).
    Users should only manually set one of these for any given part; the other
    will be filled in automatically by the RobotController when it starts.
    If both are manually specified, they must be consistent each other
    (ie, frequency * duty cycle = highest frequency part in this thread).
    If multiple parts in the same thread specify an absolute frequency, the
    highest frequency must be an integer multiple of all the lower frequencies
    (eg, 50Hz and 100 Hz parts in a single thread is valid, but 70Hz and 100Hz
    parts is not). If no part in a given thread specifies an absolute frequency
    it will run as fast as the processing time allows.
    """

    control_duty_cycle: builtins.int = ...
    @property
    def joint_metadata(self) -> joints_pb2.JointsMetadata:
        """Joint metadata- names, types, limits, etc."""
        pass
    @property
    def control_modules(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ControlModuleInfo]:
        """Control modules used for this part."""
        pass
    @property
    def subordinate_part_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]:
        """Ids of other parts which this part can send commands to and receive states
        from. Ie, when not empty, this part is a virtual part.
        """
        pass
    @property
    def subordinate_state_signal_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]:
        """State signal ids which should be collected from subordinate parts and
        output from a virtual part even if no control modules use them. States do
        *not* need to be listed here to be available to control modules in the
        virtual part. This has no effect if subordinate_part_ids is empty.
        """
        pass
    def __init__(self,
        *,
        id : typing.Text = ...,
        thread_id : typing.Text = ...,
        control_frequency : builtins.float = ...,
        control_duty_cycle : builtins.int = ...,
        joint_metadata : typing.Optional[joints_pb2.JointsMetadata] = ...,
        control_modules : typing.Optional[typing.Iterable[global___ControlModuleInfo]] = ...,
        subordinate_part_ids : typing.Optional[typing.Iterable[typing.Text]] = ...,
        subordinate_state_signal_ids : typing.Optional[typing.Iterable[typing.Text]] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["joint_metadata",b"joint_metadata"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["control_duty_cycle",b"control_duty_cycle","control_frequency",b"control_frequency","control_modules",b"control_modules","id",b"id","joint_metadata",b"joint_metadata","subordinate_part_ids",b"subordinate_part_ids","subordinate_state_signal_ids",b"subordinate_state_signal_ids","thread_id",b"thread_id"]) -> None: ...
global___RobotPartInfo = RobotPartInfo

class ControlModuleInfo(google.protobuf.message.Message):
    """Part related info provided by the robot."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    ID_FIELD_NUMBER: builtins.int
    LOOPBACK_ADAPTER_FIELD_NUMBER: builtins.int
    FAKE_IMU_ADAPTER_FIELD_NUMBER: builtins.int
    XARM_GRIPPER_ADAPTER_FIELD_NUMBER: builtins.int
    MOCK_FIELD_NUMBER: builtins.int
    id: typing.Text = ...
    """Identifier for this control module; must be unique within a given part."""

    @property
    def loopback_adapter(self) -> google.protobuf.empty_pb2.Empty:
        """*** Device Adapters ***

        An adapter which copies its input command to its output state.
        """
        pass
    @property
    def fake_imu_adapter(self) -> google.protobuf.empty_pb2.Empty: ...
    @property
    def xarm_gripper_adapter(self) -> global___SharedObjectReference: ...
    @property
    def mock(self) -> google.protobuf.empty_pb2.Empty:
        """*** Test-only control modules ***

        A control module which defers to callback functions, making it easy to
        test a lot of implementations with less boiler-plate code.
        """
        pass
    def __init__(self,
        *,
        id : typing.Text = ...,
        loopback_adapter : typing.Optional[google.protobuf.empty_pb2.Empty] = ...,
        fake_imu_adapter : typing.Optional[google.protobuf.empty_pb2.Empty] = ...,
        xarm_gripper_adapter : typing.Optional[global___SharedObjectReference] = ...,
        mock : typing.Optional[google.protobuf.empty_pb2.Empty] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["fake_imu_adapter",b"fake_imu_adapter","loopback_adapter",b"loopback_adapter","mock",b"mock","type",b"type","xarm_gripper_adapter",b"xarm_gripper_adapter"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["fake_imu_adapter",b"fake_imu_adapter","id",b"id","loopback_adapter",b"loopback_adapter","mock",b"mock","type",b"type","xarm_gripper_adapter",b"xarm_gripper_adapter"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["type",b"type"]) -> typing.Optional[typing_extensions.Literal["loopback_adapter","fake_imu_adapter","xarm_gripper_adapter","mock"]]: ...
global___ControlModuleInfo = ControlModuleInfo

class SharedObjectInfo(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    ID_FIELD_NUMBER: builtins.int
    MOCK_FIELD_NUMBER: builtins.int
    id: typing.Text = ...
    @property
    def mock(self) -> google.protobuf.empty_pb2.Empty:
        """*** Test-only shared objects ***"""
        pass
    def __init__(self,
        *,
        id : typing.Text = ...,
        mock : typing.Optional[google.protobuf.empty_pb2.Empty] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["mock",b"mock","type",b"type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["id",b"id","mock",b"mock","type",b"type"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["type",b"type"]) -> typing.Optional[typing_extensions.Literal["mock"]]: ...
global___SharedObjectInfo = SharedObjectInfo

class SharedObjectReference(google.protobuf.message.Message):
    """Configuration for a control modules which only reference a shared object."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    SHARED_OBJECT_ID_FIELD_NUMBER: builtins.int
    shared_object_id: typing.Text = ...
    def __init__(self,
        *,
        shared_object_id : typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["shared_object_id",b"shared_object_id"]) -> None: ...
global___SharedObjectReference = SharedObjectReference

class ControllerExecutionParams(google.protobuf.message.Message):
    """Parameters which control how the controllers are run/executed."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    class _Mode:
        ValueType = typing.NewType('ValueType', builtins.int)
        V: typing_extensions.TypeAlias = ValueType
    class _ModeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_Mode.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor = ...
        AUTOMATIC: ControllerExecutionParams.Mode.ValueType = ...  # 0
        """Threads are started to automatically step the controllers at the
        specified frequencies. The standard step order (update state then
        process command) is used. This mode should almost always be used for
        real hardware and may sometimes be used for simulation or testing.
        """

        MANUAL: ControllerExecutionParams.Mode.ValueType = ...  # 1
        """Controllers must be manually stepped with RobotController::ManualStep.
        Absolute step rates (RobotPartInfo.control_frequency) are ignored, but
        relative step rates (RobotPartInfo.control_duty_cycle) of parts in the
        same thread are respected. The inverted step order (process command then
        update state) is used, which moves the division between steps so that
        callers can send a command, run a single step, and see the affect on the
        output state immediately. This mode is primarily used for simulation.
        """

        UNIT_TEST: ControllerExecutionParams.Mode.ValueType = ...  # 2
        """Mode for running unit tests on control modules, parts, etc. Same as
        MANUAL, except that the default initial STOP_MOTION command is not sent,
        so that test commands do not queue behind it, and output command types
        aren't validated, since unit tests do not use a complete control stack.
        """

    class Mode(_Mode, metaclass=_ModeEnumTypeWrapper):
        pass

    AUTOMATIC: ControllerExecutionParams.Mode.ValueType = ...  # 0
    """Threads are started to automatically step the controllers at the
    specified frequencies. The standard step order (update state then
    process command) is used. This mode should almost always be used for
    real hardware and may sometimes be used for simulation or testing.
    """

    MANUAL: ControllerExecutionParams.Mode.ValueType = ...  # 1
    """Controllers must be manually stepped with RobotController::ManualStep.
    Absolute step rates (RobotPartInfo.control_frequency) are ignored, but
    relative step rates (RobotPartInfo.control_duty_cycle) of parts in the
    same thread are respected. The inverted step order (process command then
    update state) is used, which moves the division between steps so that
    callers can send a command, run a single step, and see the affect on the
    output state immediately. This mode is primarily used for simulation.
    """

    UNIT_TEST: ControllerExecutionParams.Mode.ValueType = ...  # 2
    """Mode for running unit tests on control modules, parts, etc. Same as
    MANUAL, except that the default initial STOP_MOTION command is not sent,
    so that test commands do not queue behind it, and output command types
    aren't validated, since unit tests do not use a complete control stack.
    """


    MODE_FIELD_NUMBER: builtins.int
    mode: global___ControllerExecutionParams.Mode.ValueType = ...
    def __init__(self,
        *,
        mode : global___ControllerExecutionParams.Mode.ValueType = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["mode",b"mode"]) -> None: ...
global___ControllerExecutionParams = ControllerExecutionParams
