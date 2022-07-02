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


ensure_installed() {
  if ! dpkg -s "$1" > /dev/null ; then
    sudo apt update
    sudo apt-get -y install "$@"
  fi
}

ensure_installed build-essential
ensure_installed libblas-dev
ensure_installed liblapack-dev
ensure_installed wget
ensure_installed python3-pip
ensure_installed python3-opencv
ensure_installed python3-scipy
ensure_installed python3-absl
ensure_installed python3-shapely

pip3 install --upgrade pip

if grep -q "glinux-team@google.com" /proc/version ; then
  ensure_installed python3-open3d
else
  pip3 install open3d
fi

pushd third_party/ikfast
./build_libs.sh
popd

cp third_party/ikfast/linux-so/*.so pyreach/ikfast/linux_so/

pip3 install -r requirements.txt

