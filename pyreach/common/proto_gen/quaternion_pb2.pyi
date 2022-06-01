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
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class Quaterniond(google.protobuf.message.Message):
    """A double precision quaternion."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    X_FIELD_NUMBER: builtins.int
    Y_FIELD_NUMBER: builtins.int
    Z_FIELD_NUMBER: builtins.int
    W_FIELD_NUMBER: builtins.int
    x: builtins.float = ...
    """The x-component."""

    y: builtins.float = ...
    """The y-component."""

    z: builtins.float = ...
    """The z-component."""

    w: builtins.float = ...
    """The w-component."""

    def __init__(self,
        *,
        x : builtins.float = ...,
        y : builtins.float = ...,
        z : builtins.float = ...,
        w : builtins.float = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["w",b"w","x",b"x","y",b"y","z",b"z"]) -> None: ...
global___Quaterniond = Quaterniond

class Quaternionf(google.protobuf.message.Message):
    """A single precision quaternion."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    X_FIELD_NUMBER: builtins.int
    Y_FIELD_NUMBER: builtins.int
    Z_FIELD_NUMBER: builtins.int
    W_FIELD_NUMBER: builtins.int
    x: builtins.float = ...
    """The x-component."""

    y: builtins.float = ...
    """The y-component."""

    z: builtins.float = ...
    """The z-component."""

    w: builtins.float = ...
    """The w-component."""

    def __init__(self,
        *,
        x : builtins.float = ...,
        y : builtins.float = ...,
        z : builtins.float = ...,
        w : builtins.float = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["w",b"w","x",b"x","y",b"y","z",b"z"]) -> None: ...
global___Quaternionf = Quaternionf
