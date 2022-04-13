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

class _IOType:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _IOTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_IOType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    CAPABILITY_TYPE_UNSPECIFIED: _IOType.ValueType  # 0
    """DO NOT USE"""

    DIGITAL_INPUT: _IOType.ValueType  # 1
    """Type for a digital input. Digital inputs may be
    considered true/false, 0/1, active/inactive.
    """

    DIGITAL_OUTPUT: _IOType.ValueType  # 2
    """Type for a digital output. Digital outputs may be
    considered true/false, 0/1, active/inactive.
    """

    ANALOG_INPUT: _IOType.ValueType  # 3
    """Type for an analog input. The range is unspecified."""

    ANALOG_OUTPUT: _IOType.ValueType  # 4
    """Type for an analog output. The range is unspecified."""

    INTEGER_INPUT: _IOType.ValueType  # 5
    """Type for any integer input, up to 64 bits."""

    INTEGER_OUTPUT: _IOType.ValueType  # 6
    """Type for any integer output, up to 64 bits."""

    EVENT: _IOType.ValueType  # 7
    """Type for event."""

class IOType(_IOType, metaclass=_IOTypeEnumTypeWrapper):
    pass

CAPABILITY_TYPE_UNSPECIFIED: IOType.ValueType  # 0
"""DO NOT USE"""

DIGITAL_INPUT: IOType.ValueType  # 1
"""Type for a digital input. Digital inputs may be
considered true/false, 0/1, active/inactive.
"""

DIGITAL_OUTPUT: IOType.ValueType  # 2
"""Type for a digital output. Digital outputs may be
considered true/false, 0/1, active/inactive.
"""

ANALOG_INPUT: IOType.ValueType  # 3
"""Type for an analog input. The range is unspecified."""

ANALOG_OUTPUT: IOType.ValueType  # 4
"""Type for an analog output. The range is unspecified."""

INTEGER_INPUT: IOType.ValueType  # 5
"""Type for any integer input, up to 64 bits."""

INTEGER_OUTPUT: IOType.ValueType  # 6
"""Type for any integer output, up to 64 bits."""

EVENT: IOType.ValueType  # 7
"""Type for event."""

global___IOType = IOType


class IOConfig(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    CAPABILITY_FIELD_NUMBER: builtins.int
    IO_SPACE_FIELD_NUMBER: builtins.int
    IO_BANK_FIELD_NUMBER: builtins.int
    SETTING_FIELD_NUMBER: builtins.int
    @property
    def capability(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Capability]:
        """Signal and sensor specs"""
        pass
    @property
    def io_space(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]:
        """The valid I/O spaces"""
        pass
    @property
    def io_bank(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___IOBank]:
        """Types and pin ranges for I/O"""
        pass
    @property
    def setting(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Setting]:
        """Available settings"""
        pass
    def __init__(self,
        *,
        capability: typing.Optional[typing.Iterable[global___Capability]] = ...,
        io_space: typing.Optional[typing.Iterable[typing.Text]] = ...,
        io_bank: typing.Optional[typing.Iterable[global___IOBank]] = ...,
        setting: typing.Optional[typing.Iterable[global___Setting]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["capability",b"capability","io_bank",b"io_bank","io_space",b"io_space","setting",b"setting"]) -> None: ...
global___IOConfig = IOConfig

class Capability(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    TYPE_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    DEVICE_TYPE_FIELD_NUMBER: builtins.int
    DEVICE_NAME_FIELD_NUMBER: builtins.int
    IO_TYPE_FIELD_NUMBER: builtins.int
    FUSED_PINS_FIELD_NUMBER: builtins.int
    PIN_FIELD_NUMBER: builtins.int
    type: typing.Text
    """The capability type. This will be used in commands and status."""

    name: typing.Text
    """The capability name. This will be used in commands and status."""

    device_type: typing.Text
    device_name: typing.Text
    io_type: global___IOType.ValueType
    fused_pins: builtins.bool
    @property
    def pin(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Pin]: ...
    def __init__(self,
        *,
        type: typing.Text = ...,
        name: typing.Text = ...,
        device_type: typing.Text = ...,
        device_name: typing.Text = ...,
        io_type: global___IOType.ValueType = ...,
        fused_pins: builtins.bool = ...,
        pin: typing.Optional[typing.Iterable[global___Pin]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["device_name",b"device_name","device_type",b"device_type","fused_pins",b"fused_pins","io_type",b"io_type","name",b"name","pin",b"pin","type",b"type"]) -> None: ...
global___Capability = Capability

class Pin(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    SPACE_FIELD_NUMBER: builtins.int
    IS_ACTIVE_LOW_FIELD_NUMBER: builtins.int
    N_FIELD_NUMBER: builtins.int
    name: typing.Text
    """A pin name."""

    space: typing.Text
    """The name of the pin's space. Must be one of the strings
    specified in WorkcellConfig.io_space.
    """

    is_active_low: builtins.bool
    n: builtins.int
    """Pin number."""

    def __init__(self,
        *,
        name: typing.Text = ...,
        space: typing.Text = ...,
        is_active_low: builtins.bool = ...,
        n: builtins.int = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["is_active_low",b"is_active_low","n",b"n","name",b"name","space",b"space"]) -> None: ...
global___Pin = Pin

class IOBank(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    SPACE_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    MIN_FIELD_NUMBER: builtins.int
    MAX_FIELD_NUMBER: builtins.int
    space: typing.Text
    """The name of the pin space for this bank. Must be
    one of the strings specified in WorkcellConfig.io_space.
    """

    type: global___IOType.ValueType
    min: builtins.int
    """Minimum pin number, inclusive"""

    max: builtins.int
    """Maximum pin number, inclusive"""

    def __init__(self,
        *,
        space: typing.Text = ...,
        type: global___IOType.ValueType = ...,
        min: builtins.int = ...,
        max: builtins.int = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["max",b"max","min",b"min","space",b"space","type",b"type"]) -> None: ...
global___IOBank = IOBank

class Setting(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    NAME_FIELD_NUMBER: builtins.int
    INT_VALUE_FIELD_NUMBER: builtins.int
    FLOAT_VALUE_FIELD_NUMBER: builtins.int
    VALUE_FIELD_NUMBER: builtins.int
    name: typing.Text
    """The name of the setting"""

    int_value: builtins.int
    """Integer value if the setting has an integer threshold."""

    float_value: builtins.float
    """Float value if the setting has a float threshold."""

    value: typing.Text
    """String value if the setting has a string value."""

    def __init__(self,
        *,
        name: typing.Text = ...,
        int_value: builtins.int = ...,
        float_value: builtins.float = ...,
        value: typing.Text = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["float_value",b"float_value","int_value",b"int_value","value",b"value","value_type",b"value_type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["float_value",b"float_value","int_value",b"int_value","name",b"name","value",b"value","value_type",b"value_type"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["value_type",b"value_type"]) -> typing.Optional[typing_extensions.Literal["int_value","float_value","value"]]: ...
global___Setting = Setting
