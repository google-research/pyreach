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
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class StatusProto(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    CODE_FIELD_NUMBER: builtins.int
    SPACE_FIELD_NUMBER: builtins.int
    MESSAGE_FIELD_NUMBER: builtins.int
    CANONICAL_CODE_FIELD_NUMBER: builtins.int
    code: builtins.int = ...
    space: typing.Text = ...
    message: typing.Text = ...
    canonical_code: builtins.int = ...
    def __init__(self,
        *,
        code : typing.Optional[builtins.int] = ...,
        space : typing.Optional[typing.Text] = ...,
        message : typing.Optional[typing.Text] = ...,
        canonical_code : typing.Optional[builtins.int] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["canonical_code",b"canonical_code","code",b"code","message",b"message","space",b"space"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["canonical_code",b"canonical_code","code",b"code","message",b"message","space",b"space"]) -> None: ...
global___StatusProto = StatusProto
