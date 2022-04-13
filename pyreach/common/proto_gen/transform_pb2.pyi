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
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class Transform(google.protobuf.message.Message):
    """Transform represents homogenous transform between two coordinate systems
    (frames) and its time derivatives. All vectors and quaternion share the same
    reference frame and cartesian basis frame.

    When used as logging payload, it is recommended to have consistency on the
    availability of fields in the same log stream, i.e. a single log stream would
    always has some fields (e.g. position and velocity) but not others.

    This type can be used as both commands to and measurements.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    POSITION_FIELD_NUMBER: builtins.int
    QUATERNION_FIELD_NUMBER: builtins.int
    VELOCITY_FIELD_NUMBER: builtins.int
    ANGULAR_VELOCITY_FIELD_NUMBER: builtins.int
    ACCELERATION_FIELD_NUMBER: builtins.int
    ANGULAR_ACCELERATION_FIELD_NUMBER: builtins.int
    JERK_FIELD_NUMBER: builtins.int
    ANGULAR_JERK_FIELD_NUMBER: builtins.int
    FORCE_FIELD_NUMBER: builtins.int
    TORQUE_FIELD_NUMBER: builtins.int
    @property
    def position(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """Translation, xyz, len == 3, in meters."""
        pass
    @property
    def quaternion(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """Rotation represented in quaternion, order wxyz. w is always >=0."""
        pass
    @property
    def velocity(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """Linear velocity, xyz, len == 3, in m/s."""
        pass
    @property
    def angular_velocity(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """Angular velocity, xyz, len == 3, in rad/s."""
        pass
    @property
    def acceleration(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """Linear acceleration, xyz, len == 3, in m/s^2."""
        pass
    @property
    def angular_acceleration(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """Angular acceleration, xyz, len == 3, in rad/s^2."""
        pass
    @property
    def jerk(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """Linear jerk, xyz, len == 3, in m/s^3. Rarely used, defined for
        completeness.
        """
        pass
    @property
    def angular_jerk(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """Angular jerk, xyz, len == 3, in rad/s^3. Rarely used, defined for
        completeness.
        """
        pass
    @property
    def force(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """Linear force, xyz, len == 3, in N."""
        pass
    @property
    def torque(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """Torque (rotational force), xyz, len==3, in N*m."""
        pass
    def __init__(self,
        *,
        position: typing.Optional[typing.Iterable[builtins.float]] = ...,
        quaternion: typing.Optional[typing.Iterable[builtins.float]] = ...,
        velocity: typing.Optional[typing.Iterable[builtins.float]] = ...,
        angular_velocity: typing.Optional[typing.Iterable[builtins.float]] = ...,
        acceleration: typing.Optional[typing.Iterable[builtins.float]] = ...,
        angular_acceleration: typing.Optional[typing.Iterable[builtins.float]] = ...,
        jerk: typing.Optional[typing.Iterable[builtins.float]] = ...,
        angular_jerk: typing.Optional[typing.Iterable[builtins.float]] = ...,
        force: typing.Optional[typing.Iterable[builtins.float]] = ...,
        torque: typing.Optional[typing.Iterable[builtins.float]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["acceleration",b"acceleration","angular_acceleration",b"angular_acceleration","angular_jerk",b"angular_jerk","angular_velocity",b"angular_velocity","force",b"force","jerk",b"jerk","position",b"position","quaternion",b"quaternion","torque",b"torque","velocity",b"velocity"]) -> None: ...
global___Transform = Transform

class TransformMeta(google.protobuf.message.Message):
    """Metadata of Transform. Frame in robotic system is identified as string. To
    avoid name conflict, it is recommended to name frame inside one or multiple
    level of name space. For example, system number 3's abb robot effector frame
    can be named "robot3/abb/end_effector".

    Three frames are required to fully qualify a Transform and its numerical
    representation: frame being measured, frame of reference and frame that
    defines the cartesian basis, which is called frame of representation. Take an
    example, a stereo camera system mounted at an intersecion measures relative
    position and rotation of car A relative to car B. Frame being measured is the
    frame attached to car A; frame of reference is the one attached to car B;
    frame of representation defines the coordinate system in which vectors are
    represented. Rotation of frame of representation affects meaning of vector
    logged as it changes x, y, and z axis unit vector.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    FRAME_MEASURED_FIELD_NUMBER: builtins.int
    FRAME_REFERENCE_FIELD_NUMBER: builtins.int
    FRAME_REPRESENTATION_FIELD_NUMBER: builtins.int
    frame_measured: typing.Text
    """The frame being measured."""

    frame_reference: typing.Text
    """The frame of reference."""

    frame_representation: typing.Text
    """The frame that defines the cartesian basis."""

    def __init__(self,
        *,
        frame_measured: typing.Optional[typing.Text] = ...,
        frame_reference: typing.Optional[typing.Text] = ...,
        frame_representation: typing.Optional[typing.Text] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["frame_measured",b"frame_measured","frame_reference",b"frame_reference","frame_representation",b"frame_representation"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["frame_measured",b"frame_measured","frame_reference",b"frame_reference","frame_representation",b"frame_representation"]) -> None: ...
global___TransformMeta = TransformMeta
