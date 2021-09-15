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

# A simple shell script to run code coverage on a Python all unit test files
# in the current directory.

set -uxeo pipefail

if [[ ! "$(which coverage)" ]]
then
  echo "You need to run 'pip install coverage' to install Python test coverage."
  exit 1
fi

if [[ "$#" == "0" ]]
then
  echo "usage: coverage.sh DIR1 ... DIRn"
  echo "Each DIR is recursively scanned for '*_test.py'."
  echo "Use 'coverage.sh .' to scan all directories."
  exit 1
fi

# Erase previous coverage results.
coverage erase

# Run each test in directory.
for dir in "$@"
do
  # Google3 lint does not like word splitting at all.
  # The following bash code uses bash arrays to make the Google3 linter happy.
  # 1. declare -a V    # Declare the array
  # 2. V=($(cmd ...))  # Fill the array
  # 3. "${V[@]}"       # Access the array as individual words.
  pushd "$dir" > /dev/null
  declare -a tests
  tests=($(find . -name "*_test.py"))
  popd > /dev/null

  for test in "${tests[@]}"
  do
    echo "Running Test $dir/$test"
    coverage run -a "$dir/$test" 2>/dev/null 1>/dev/null
  done
done

# Generate a report that just contains the files in the directories.
includes=""
separator=""
for dir in "$@"
do
  includes="$includes$separator$dir/*"
  separator=","
done
coverage report "--include=$includes"

echo "For a complete report, simply type 'coverage report'"
