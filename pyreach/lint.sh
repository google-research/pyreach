#/usr/bin/env bash
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

# The Google bash lint tools encourage using bash arrays instead of word splitting.
# Below is an extremely brief tutorial about bash arrays.
# 1. declare -a A                # Declare the array A
# 2. A=("value1", ..., "valueN") # Fill array A with values
# 3. A+=("another_value")        # Append to array A
# 4. "${A[@]}"                   # Access array A as individual words

set -uxeo pipefail

readonly SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
readonly MYPY_CONFIG="${SCRIPT_DIR}/mypy.ini"
cd "$SCRIPT_DIR"

# Code to scan for all Python files and lint most (but not all) of them.
declare -a SKIP_FILES
SKIP_FILES=()
SKIP_FILES+=("tools/view3d.py")
SKIP_FILES+=("tools/view_rgbd.py")
SKIP_FILES+=("tools/lib/view3d.py")
SKIP_FILES+=("tools/lib/view_rgbd.py")

declare -a SKIP_DIRS
SKIP_DIRS=()
SKIP_DIRS+=("common/proto_gen/")

declare -a SKIP_TEST_DIRS
SKIP_TEST_DIRS=()
SKIP_TEST_FILES=()
SKIP_TEST_DIRS+=("gyms/")
SKIP_TEST_DIRS+=("impl/")

declare -a SKIP_TEST_FILES
SKIP_TEST_FILES=()
SKIP_TEST_FILES+=("common/spacemouse/spacemouse_lib.py")
SKIP_TEST_FILES+=("tools/pendant_control.py")
SKIP_TEST_FILES+=("tools/reach.py")

set +x

# Build the file lists.
declare -a PY_FILES
PY_FILES=()
while read -d $'\0' FILE ; do
  SKIP=0
  for SKIP_FILE in "${SKIP_FILES[@]}" ; do
    if [[ "${FILE}" == "${SKIP_FILE}" ]]; then
      SKIP=1
    fi
  done
  for SKIP_DIR in "${SKIP_DIRS[@]}" ; do
    if echo "${FILE} " | grep -q "${SKIP_DIR}" ; then
      SKIP=1
    fi
  done
  if [[ "${SKIP}" == 0 ]] ; then
    PY_FILES+=("${FILE}")
  fi
done < <(find * -type f -name "*.py" -print0)

declare -a TEST_FILES
TEST_FILES=()
for FILE in "${PY_FILES[@]}" ; do
  SKIP=0
  for SKIP_FILE in "${SKIP_TEST_FILES[@]}" ; do
    if [[ "${FILE}" == "${SKIP_FILE}" ]] ; then
      SKIP=1
    fi
  done
  for SKIP_DIR in "${SKIP_TEST_DIRS[@]}" ; do
    if [[ "${FILE}" == "${SKIP_DIR}"* ]] ; then
      SKIP=1
    fi
  done
  if [[ "${SKIP}" == 0 ]] ; then
    TEST_FILES+=("${FILE}")
  fi
done

set -x

# Run the linters.
EXIT_CODE=0
echo "================ mypy ================"
if ! python3 -m mypy -V ; then
  echo "mypy is not installed"
  exit 1
elif ! python3 -m mypy --config-file "${MYPY_CONFIG}" "${PY_FILES[@]}" ; then
  echo "FAILED: mypy errors (temp ignored for PIPE-3272)"
  # temp ignored for https://project-reach.atlassian.net/browse/PIPE-3272
  # EXIT_CODE=1
fi

echo "================ flake8 ================"
if ! python3 -m flake8 --version ; then
  echo "flake8 is not installed"
  exit 1
elif ! python3 -m flake8 --ignore=E111,E114,E121,E123,E124,E125,E126,E127,E129,E266,E131,E305,E501,F401,V305,W293,W391,W504 "${PY_FILES[@]}" ; then
  echo "FAILED: Flake8 errors"
  EXIT_CODE=1
fi

echo "================ unittest ================"
if ! python3 -m unittest -v -c "${TEST_FILES[@]}" ; then
  echo "unittest failed"
  EXIT_CODE=1
fi

# Python unittest module shadows common package incorrectly.
# Run impl test from within the impl folder.
echo "================ impl Unit tests ================"
(cd impl ; python3 -m unittest -v -c *.py)

# Gym register() function breaks in unittest. Run the gym tests individually.
echo "================ gyms Unit tests ================"
while read -d $'\0' FILE ; do
  if [[ "${FILE}" != "gyms/__init__.py" ]] ; then
    python3 "${FILE}"
  fi
done < <(find gyms/* -type f -name "*.py" -print0)

exit "$EXIT_CODE"
