#!/usr/bin/env bash
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


OUTPUTDIR=linux-so

mkdir -p $OUTPUTDIR

if [ "$(uname)" == "Darwin" ]; then
  readonly COMPILER="cc"
  readonly CFLAGS="-std=c++11 -dynamiclib"
  readonly LIBS="-llapack -lstdc++"
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
  readonly COMPILER="g++"
  readonly CFLAGS="-fPIC -shared"
  readonly LIBS="-lm -lblas -llapack -lstdc++"
else
  echo "Unsupported platform $(uname). Sorry about that!"
  exit 1
fi

for FILE in reachrobots/*ikfast61.cpp
do
   FILENAME=$(basename $FILE)
   LIBNAME="$OUTPUTDIR/lib${FILENAME%.*}.so"
   APPNAME="${FILENAME%.*}"
   HELPER=python_helper.cpp
   echo $LIBNAME
   $COMPILER -DIKFAST_NO_MAIN -DIKFAST_CLIBRARY $CFLAGS -o $LIBNAME $FILE $HELPER $LIBS
done

