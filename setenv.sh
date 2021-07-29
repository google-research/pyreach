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

#
# To use: source setenv.sh

# The directory this script is located at.
REACH_ROOT_DIR="$(SHELL_SESSION_FILE= && cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Set Python environment
export PYTHONPATH="${PYTHONPATH:-}:${REACH_ROOT_DIR}"

# Add current folder to PATH
export PATH="${PATH:-}:${REACH_ROOT_DIR}"

# Set Go environment
if [ -d ${REACH_ROOT_DIR}/go ]; then
  source ${REACH_ROOT_DIR}/go/setenv.sh
fi
