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

# type: ignore

# In order for mypy checking to pass, we need to add "type: ignore" at
# the top of the generated python code, however, we do not control that
# code. instead, we add "type: ignore" to the current file, which we
# import instead of the raw generated code.

from pyreach.common.proto_gen.workcell_io_pb2 import IOConfig as IOConfig
from pyreach.common.proto_gen.workcell_io_pb2 import Capability as Capability
from pyreach.common.proto_gen.workcell_io_pb2 import Pin as Pin
from pyreach.common.proto_gen.workcell_io_pb2 import IOBank as IOBank
from pyreach.common.proto_gen.workcell_io_pb2 import Setting as Setting
from pyreach.common.proto_gen.workcell_io_pb2 import CAPABILITY_TYPE_UNSPECIFIED as CAPABILITY_TYPE_UNSPECIFIED
from pyreach.common.proto_gen.workcell_io_pb2 import DIGITAL_INPUT as DIGITAL_INPUT
from pyreach.common.proto_gen.workcell_io_pb2 import DIGITAL_OUTPUT as DIGITAL_OUTPUT
from pyreach.common.proto_gen.workcell_io_pb2 import ANALOG_INPUT as ANALOG_INPUT
from pyreach.common.proto_gen.workcell_io_pb2 import ANALOG_OUTPUT as ANALOG_OUTPUT
from pyreach.common.proto_gen.workcell_io_pb2 import INTEGER_INPUT as INTEGER_INPUT
from pyreach.common.proto_gen.workcell_io_pb2 import INTEGER_OUTPUT as INTEGER_OUTPUT
from pyreach.common.proto_gen.workcell_io_pb2 import EVENT as EVENT
