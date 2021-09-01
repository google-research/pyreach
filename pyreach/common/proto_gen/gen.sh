#!/bin/bash
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

set -uexo pipefail

readonly SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd $SCRIPT_DIR/../../..

protoc -I=common/ --python_out=$SCRIPT_DIR common/pybullet_reach.proto

protoc -I=common/ --python_out=$SCRIPT_DIR common/workcell_io.proto

protoc -I=logs/ --python_out=$SCRIPT_DIR logs.proto

sed -i 's/import\ logs_options_pb2/import\ pyreach.common.proto_gen.logs_options_pb2/' pyreach/common/proto_gen/logs_pb2.py

protoc -I=logs/ --python_out=$SCRIPT_DIR logs_options.proto


