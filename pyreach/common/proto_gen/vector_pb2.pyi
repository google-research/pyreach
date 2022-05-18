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

class Vector4d(google.protobuf.message.Message):
    """A four-dimensional double precision vector."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    X_FIELD_NUMBER: builtins.int
    Y_FIELD_NUMBER: builtins.int
    Z_FIELD_NUMBER: builtins.int
    W_FIELD_NUMBER: builtins.int
    x: builtins.float
    y: builtins.float
    z: builtins.float
    w: builtins.float
    def __init__(self,
        *,
        x: builtins.float = ...,
        y: builtins.float = ...,
        z: builtins.float = ...,
        w: builtins.float = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["w",b"w","x",b"x","y",b"y","z",b"z"]) -> None: ...
global___Vector4d = Vector4d

class Vector4f(google.protobuf.message.Message):
    """A four-dimensional single precision vector."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    X_FIELD_NUMBER: builtins.int
    Y_FIELD_NUMBER: builtins.int
    Z_FIELD_NUMBER: builtins.int
    W_FIELD_NUMBER: builtins.int
    x: builtins.float
    y: builtins.float
    z: builtins.float
    w: builtins.float
    def __init__(self,
        *,
        x: builtins.float = ...,
        y: builtins.float = ...,
        z: builtins.float = ...,
        w: builtins.float = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["w",b"w","x",b"x","y",b"y","z",b"z"]) -> None: ...
global___Vector4f = Vector4f

class Vector4i(google.protobuf.message.Message):
    """A four-dimensional integer vector."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    X_FIELD_NUMBER: builtins.int
    Y_FIELD_NUMBER: builtins.int
    Z_FIELD_NUMBER: builtins.int
    W_FIELD_NUMBER: builtins.int
    x: builtins.int
    y: builtins.int
    z: builtins.int
    w: builtins.int
    def __init__(self,
        *,
        x: builtins.int = ...,
        y: builtins.int = ...,
        z: builtins.int = ...,
        w: builtins.int = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["w",b"w","x",b"x","y",b"y","z",b"z"]) -> None: ...
global___Vector4i = Vector4i

class Vector3d(google.protobuf.message.Message):
    """A three-dimensional double precision vector."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    X_FIELD_NUMBER: builtins.int
    Y_FIELD_NUMBER: builtins.int
    Z_FIELD_NUMBER: builtins.int
    x: builtins.float
    y: builtins.float
    z: builtins.float
    def __init__(self,
        *,
        x: builtins.float = ...,
        y: builtins.float = ...,
        z: builtins.float = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["x",b"x","y",b"y","z",b"z"]) -> None: ...
global___Vector3d = Vector3d

class Vector3f(google.protobuf.message.Message):
    """A three-dimensional single precision vector."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    X_FIELD_NUMBER: builtins.int
    Y_FIELD_NUMBER: builtins.int
    Z_FIELD_NUMBER: builtins.int
    x: builtins.float
    y: builtins.float
    z: builtins.float
    def __init__(self,
        *,
        x: builtins.float = ...,
        y: builtins.float = ...,
        z: builtins.float = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["x",b"x","y",b"y","z",b"z"]) -> None: ...
global___Vector3f = Vector3f

class Vector3i(google.protobuf.message.Message):
    """A three-dimensional integer vector."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    X_FIELD_NUMBER: builtins.int
    Y_FIELD_NUMBER: builtins.int
    Z_FIELD_NUMBER: builtins.int
    x: builtins.int
    y: builtins.int
    z: builtins.int
    def __init__(self,
        *,
        x: builtins.int = ...,
        y: builtins.int = ...,
        z: builtins.int = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["x",b"x","y",b"y","z",b"z"]) -> None: ...
global___Vector3i = Vector3i

class Vector2d(google.protobuf.message.Message):
    """A two-dimensional double precision vector."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    X_FIELD_NUMBER: builtins.int
    Y_FIELD_NUMBER: builtins.int
    x: builtins.float
    y: builtins.float
    def __init__(self,
        *,
        x: builtins.float = ...,
        y: builtins.float = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["x",b"x","y",b"y"]) -> None: ...
global___Vector2d = Vector2d

class Vector2f(google.protobuf.message.Message):
    """A two-dimensional single precision vector."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    X_FIELD_NUMBER: builtins.int
    Y_FIELD_NUMBER: builtins.int
    x: builtins.float
    y: builtins.float
    def __init__(self,
        *,
        x: builtins.float = ...,
        y: builtins.float = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["x",b"x","y",b"y"]) -> None: ...
global___Vector2f = Vector2f

class Vector2i(google.protobuf.message.Message):
    """A two-dimensional integer vector."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    X_FIELD_NUMBER: builtins.int
    Y_FIELD_NUMBER: builtins.int
    x: builtins.int
    y: builtins.int
    def __init__(self,
        *,
        x: builtins.int = ...,
        y: builtins.int = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["x",b"x","y",b"y"]) -> None: ...
global___Vector2i = Vector2i

class Vectord(google.protobuf.message.Message):
    """Double precision vector of arbitrary size."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    DATA_FIELD_NUMBER: builtins.int
    @property
    def data(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]: ...
    def __init__(self,
        *,
        data: typing.Optional[typing.Iterable[builtins.float]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["data",b"data"]) -> None: ...
global___Vectord = Vectord

class Vectorf(google.protobuf.message.Message):
    """Single precision vector of arbitrary size."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    DATA_FIELD_NUMBER: builtins.int
    @property
    def data(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]: ...
    def __init__(self,
        *,
        data: typing.Optional[typing.Iterable[builtins.float]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["data",b"data"]) -> None: ...
global___Vectorf = Vectorf

class Vectori(google.protobuf.message.Message):
    """Integer vector of arbitrary size."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    DATA_FIELD_NUMBER: builtins.int
    @property
    def data(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    def __init__(self,
        *,
        data: typing.Optional[typing.Iterable[builtins.int]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["data",b"data"]) -> None: ...
global___Vectori = Vectori
