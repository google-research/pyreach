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

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class Intervald(google.protobuf.message.Message):
    """A closed interval of double precision values [min, max]."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    MIN_FIELD_NUMBER: builtins.int
    MAX_FIELD_NUMBER: builtins.int
    min: builtins.float
    max: builtins.float
    def __init__(self,
        *,
        min: builtins.float = ...,
        max: builtins.float = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["max",b"max","min",b"min"]) -> None: ...
global___Intervald = Intervald

class Intervalf(google.protobuf.message.Message):
    """A closed interval of single precision values [min, max]."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    MIN_FIELD_NUMBER: builtins.int
    MAX_FIELD_NUMBER: builtins.int
    min: builtins.float
    max: builtins.float
    def __init__(self,
        *,
        min: builtins.float = ...,
        max: builtins.float = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["max",b"max","min",b"min"]) -> None: ...
global___Intervalf = Intervalf

class Intervali(google.protobuf.message.Message):
    """A closed interval of integer values [min, max]."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    MIN_FIELD_NUMBER: builtins.int
    MAX_FIELD_NUMBER: builtins.int
    min: builtins.int
    max: builtins.int
    def __init__(self,
        *,
        min: builtins.int = ...,
        max: builtins.int = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["max",b"max","min",b"min"]) -> None: ...
global___Intervali = Intervali
