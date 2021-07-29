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

#/bin/bash
# Google3 lint does not like word splitting at all.
# The following bash code uses bash arrays to make the linter happy.
# 1. declare -a V    # Declare the array
# 2. V=($(cmd ...))  # Fill the array
# 3. "${V[@]}"       # Access the array as individual words.

set -uxeo pipefail

readonly SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd "$SCRIPT_DIR"

../scripts/lint/lint.sh \
  --skip-test-dir gyms/ \
  --skip tools/view3d.py --skip tools/view_rgbd.py \
  --skip tools/lib/view3d.py --skip tools/lib/view_rgbd.py \
  --skip-dir common/proto_gen/ \
  --skip-test-dir impl/ \
  --skip-test common/spacemouse/spacemouse_lib.py \
  --skip-test tools/pendant_control.py \
  --skip-test tools/reach.py


# Python unittest module shadows common package incorrectly.
# Run impl test from within the impl folder.
pushd impl
python3 -m unittest -v -c *.py
popd

# Gym register() function breaks in unittest. Run the gym tests individually.
while read -d $'\0' FILE ; do
  if [[ "$FILE" != "gyms/__init__.py" ]] ; then
    python3 "$FILE"
  fi
done < <(find gyms/* -type f -name "*.py" -print0)
