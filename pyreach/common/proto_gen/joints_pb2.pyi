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
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class Joints(google.protobuf.message.Message):
    """Joints abstracts information about any kinematics chain or multiple
    kinematics chains. Each repeated field covers an aspect of the joints. For a
    single repeated field, the number of elements is either zero, which denotes
    no information, or the number of simple joint (1d revolute or prismatic).

    When used as logging payload, it is recommended to have consistency on the
    availability of fields in the same log stream, i.e. a single log stream would
    always has some fields (e.g. position and velocity) but not others.

    This type can be used as both commands to and states from robot.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    POSITIONS_FIELD_NUMBER: builtins.int
    VELOCITIES_FIELD_NUMBER: builtins.int
    ACCELERATIONS_FIELD_NUMBER: builtins.int
    JERKS_FIELD_NUMBER: builtins.int
    FORCE_TORQUES_FIELD_NUMBER: builtins.int
    CURRENTS_FIELD_NUMBER: builtins.int
    TEMPERATURE_FIELD_NUMBER: builtins.int
    KPS_FIELD_NUMBER: builtins.int
    KDS_FIELD_NUMBER: builtins.int
    @property
    def positions(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """Position of joints. Depending on joint type, unit is meters or radians."""
        pass
    @property
    def velocities(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """Velocity of joints. Depending on joint type, unit is m/s or rad/s."""
        pass
    @property
    def accelerations(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """Acceleration of joints. Depending on joint type, unit is m/s^2 or rad/s^2."""
        pass
    @property
    def jerks(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """Jerk of joints. Depending on joint type, unit is m/s^3 or rad/s^3."""
        pass
    @property
    def force_torques(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """Force or torques at the joints (applied or measured). Unit is N or N.m."""
        pass
    @property
    def currents(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """Current to joint accuators. Unit is ampere."""
        pass
    @property
    def temperature(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """Temperature of joint actuators. Unit in Celsius degree (C)."""
        pass
    @property
    def kps(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """Proportional gain which determines the joint stiffness.
        High kp could cause instability from overshotting and oscillation.
        Sometimes referred to as position_gain or stiffness.
        """
        pass
    @property
    def kds(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """Derivative gain which is the damping effects on the joint.
        Increasing kd reduces oscillation.
        Sometimes referred to as velocity_gain or damping.
        """
        pass
    def __init__(self,
        *,
        positions: typing.Optional[typing.Iterable[builtins.float]] = ...,
        velocities: typing.Optional[typing.Iterable[builtins.float]] = ...,
        accelerations: typing.Optional[typing.Iterable[builtins.float]] = ...,
        jerks: typing.Optional[typing.Iterable[builtins.float]] = ...,
        force_torques: typing.Optional[typing.Iterable[builtins.float]] = ...,
        currents: typing.Optional[typing.Iterable[builtins.float]] = ...,
        temperature: typing.Optional[typing.Iterable[builtins.float]] = ...,
        kps: typing.Optional[typing.Iterable[builtins.float]] = ...,
        kds: typing.Optional[typing.Iterable[builtins.float]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["accelerations",b"accelerations","currents",b"currents","force_torques",b"force_torques","jerks",b"jerks","kds",b"kds","kps",b"kps","positions",b"positions","temperature",b"temperature","velocities",b"velocities"]) -> None: ...
global___Joints = Joints

class JointsMetadata(google.protobuf.message.Message):
    """Metadata of Joints that does change or changes slowly."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class _JointType:
        ValueType = typing.NewType('ValueType', builtins.int)
        V: typing_extensions.TypeAlias = ValueType
    class _JointTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[JointsMetadata._JointType.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        UNKNOWN: JointsMetadata._JointType.ValueType  # 0
        REVOLUTE: JointsMetadata._JointType.ValueType  # 1
        PRISMATIC: JointsMetadata._JointType.ValueType  # 2
    class JointType(_JointType, metaclass=_JointTypeEnumTypeWrapper):
        """Type of joints. Only simple joint types are available. Complex joints, such
        as spherical joint, can be simulated by multiple simple joints.
        """
        pass

    UNKNOWN: JointsMetadata.JointType.ValueType  # 0
    REVOLUTE: JointsMetadata.JointType.ValueType  # 1
    PRISMATIC: JointsMetadata.JointType.ValueType  # 2

    ROBOT_MODEL_NAME_FIELD_NUMBER: builtins.int
    NUM_DOF_FIELD_NUMBER: builtins.int
    JOINT_TYPES_FIELD_NUMBER: builtins.int
    JOINT_NAMES_FIELD_NUMBER: builtins.int
    MIN_LIMITS_FIELD_NUMBER: builtins.int
    MAX_LIMITS_FIELD_NUMBER: builtins.int
    GOAL_THRESHOLDS_FIELD_NUMBER: builtins.int
    HOME_JOINT_POSITIONS_FIELD_NUMBER: builtins.int
    robot_model_name: typing.Text
    """Name of robot as string. In a single logging data repository, it is
    recommended to have the name uniquely map to a certain JointsMetadata.
    a robot model id string.
    """

    num_dof: builtins.int
    """The number of joints/ degrees of freedom. The repeated fields below
    (including those in Joints messages) should be this size (or empty).
    """

    @property
    def joint_types(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[global___JointsMetadata.JointType.ValueType]:
        """Type of joints."""
        pass
    @property
    def joint_names(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]:
        """Name of joints."""
        pass
    @property
    def min_limits(self) -> global___Joints:
        """Joint limits."""
        pass
    @property
    def max_limits(self) -> global___Joints: ...
    @property
    def goal_thresholds(self) -> global___Joints:
        """Thresholds used to determine when the joint state is close enough to a
        goal/target state to call the command successfully completed. Ie, a command
        is complete when abs(sensed - target) <= threshold for all joints. Each
        field can be length 0 (default threshold used), 1 (same threshold used for
        all dofs) or num_dof (the corresponding threshold used for each dof).
        """
        pass
    @property
    def home_joint_positions(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """Joint positions for the default pose. Simulators should use this for the
        initial state. Zeros should be assumed for all joints if not given.
        """
        pass
    def __init__(self,
        *,
        robot_model_name: typing.Optional[typing.Text] = ...,
        num_dof: typing.Optional[builtins.int] = ...,
        joint_types: typing.Optional[typing.Iterable[global___JointsMetadata.JointType.ValueType]] = ...,
        joint_names: typing.Optional[typing.Iterable[typing.Text]] = ...,
        min_limits: typing.Optional[global___Joints] = ...,
        max_limits: typing.Optional[global___Joints] = ...,
        goal_thresholds: typing.Optional[global___Joints] = ...,
        home_joint_positions: typing.Optional[typing.Iterable[builtins.float]] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["goal_thresholds",b"goal_thresholds","max_limits",b"max_limits","min_limits",b"min_limits","num_dof",b"num_dof","robot_model_name",b"robot_model_name"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["goal_thresholds",b"goal_thresholds","home_joint_positions",b"home_joint_positions","joint_names",b"joint_names","joint_types",b"joint_types","max_limits",b"max_limits","min_limits",b"min_limits","num_dof",b"num_dof","robot_model_name",b"robot_model_name"]) -> None: ...
global___JointsMetadata = JointsMetadata
