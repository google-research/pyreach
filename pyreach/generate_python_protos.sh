#! /bin/bash

set -uxeo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
readonly SCRIPT_DIR
cd "$SCRIPT_DIR"

readonly PROTOGEN_DIR="$SCRIPT_DIR"/common/proto_gen
readonly PROTOS_DIR="$SCRIPT_DIR"/../protos

if python3 "$SCRIPT_DIR/common/utils/directory_hash.py" compare "$SCRIPT_DIR/../python_proto_sum.txt" \
  "$PROTOS_DIR" ".proto" "$PROTOGEN_DIR" ".py" "$PROTOGEN_DIR" ".pyi" \
  "$SCRIPT_DIR/install_protoc.sh" "" "$SCRIPT_DIR/../protoc_install" "" "$SCRIPT_DIR/generate_python_protos.sh" "" \
  "$SCRIPT_DIR/common/utils/directory_hash.py" "" ; then
  echo "Protos already generated for existing values"
  # Special case if we are running on the corp linux
  if grep -q "glinux-team@google.com" /proc/version ; then
    if python3 -c "import google.protobuf; assert google.protobuf.__version__ == '3.19.1';"; then
      exit 0
    fi
    echo "Force regeneration since protobuf library has changed."
  else
    exit 0
  fi
fi

./install_protoc.sh

# Special case if we are running on the corp linux
if grep -q "glinux-team@google.com" /proc/version ; then
  python3 -m pip install "mypy-protobuf==3.1.0" "protobuf==3.19.1"
else
  python3 -m pip install "mypy-protobuf==3.1.0"
fi

cd "$PROTOGEN_DIR"
while read -r -d $'\0' PROTO_FILE ; do
  if [[ "$PROTO_FILE" != "./__init__.py" ]] && [[ "$PROTO_FILE" != "." ]] && [[ "$PROTO_FILE" != ".." ]] ; then
    rm -rf "$PROTO_FILE"
  fi
done < <(find "." -print0)
cd "$SCRIPT_DIR/.."

TEMP_DIR=$(mktemp -d)
readonly TEMP_DIR
trap 'rm -rf -- "$TEMP_DIR"' EXIT

cat > "$TEMP_DIR/protoc-gen-mypy" <<EOF
#!$(which python3)
# -*- coding: utf-8 -*-
import re
import sys
from mypy_protobuf.main import main
if __name__ == '__main__':
  sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
  sys.exit(main())
EOF
chmod a+x "$TEMP_DIR/protoc-gen-mypy"

# Copy the protos to a temporary directory
while read -r -d $'\0' PROTO_FILE ; do
  if [[ "$PROTO_FILE" =~ ^protos/third_party/fluxworks/core/fluxworks.* ]] ; then
    continue
  fi
  cp "$PROTO_FILE" "$TEMP_DIR"
done < <(find protos -name "*.proto" -print0)

# Flatten the proto structure, copying protos to temp dir.
cd "$PROTOS_DIR"
while read -r -d $'\0' PROTO_FILE ; do
  while read -r -d $'\0' PROTO_FILE_RENAME_PREFIX ; do
    # shellcheck disable=SC2001
    PROTO_FILE_RENAME=$(echo "${PROTO_FILE_RENAME_PREFIX}" | sed s,^./,,g)
    RENAME_TO=$(basename "$PROTO_FILE_RENAME")
    sed -i.bak -e "s,import*.\"$PROTO_FILE_RENAME,import \"$RENAME_TO,g" -- "$PROTO_FILE"
    rm "$PROTO_FILE".bak
  done < <(find "." -type f -name "*.proto" -print0)
done < <(find "$TEMP_DIR" -name "*.proto" -print0)

# Generate protos
cd "$TEMP_DIR"
"$SCRIPT_DIR/../protoc_install/bin/protoc" --experimental_allow_proto3_optional \
  -I="." --plugin=protoc-gen-mypy="${TEMP_DIR}/protoc-gen-mypy" \
  --python_out="." -I="." --mypy_out="." ./*.proto

# Update the import path of the protos
cd "$PROTOS_DIR"
while read -r -d $'\0' PROTO_FILE ; do
  while read -r -d $'\0' PROTO_FILE_RENAME_PREFIX ; do
    # shellcheck disable=SC2001
    PROTO_FILE_RENAME=$(echo "${PROTO_FILE_RENAME_PREFIX}" | sed s,^./,,g)
    PYTHON_NAME=$(basename -s ".proto" "$PROTO_FILE_RENAME")
    sed -i.bak -e "s,import*.$PYTHON_NAME,import pyreach.common.proto_gen.$PYTHON_NAME,g" -- "$PROTO_FILE"
    rm "$PROTO_FILE".bak
  done < <(find "." -type f -name "*.proto" -print0)
done < <(find "$TEMP_DIR" -name "*.py" -print0)

cat >> "${TEMP_DIR}"/header <<'EOF'
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

EOF

# Add open-source copyright header to the generated python files.
while read -r -d $'\0' PROTO_FILE ; do
  cp "${TEMP_DIR}"/header "${TEMP_DIR}"/file
  cat "$PROTO_FILE" >> "${TEMP_DIR}"/file
  cat "${TEMP_DIR}"/file > "$PROTO_FILE"
done < <(find "$TEMP_DIR" -name "*.py" -print0)

# Add open-source copyright header to the generated interface files.
while read -r -d $'\0' PROTO_FILE ; do
  cp "${TEMP_DIR}"/header "${TEMP_DIR}"/file
  cat "$PROTO_FILE" >> "${TEMP_DIR}"/file
  cat "${TEMP_DIR}"/file > "$PROTO_FILE"
done < <(find "$TEMP_DIR" -name "*.pyi" -print0)

# Copy the files back
while read -r -d $'\0' PROTO_FILE ; do
  FILENAME=$(basename "$PROTO_FILE")
  cp "${PROTO_FILE}" "${PROTOGEN_DIR}/$FILENAME"
done < <(find "$TEMP_DIR" -name "*.py" -print0)
while read -r -d $'\0' PROTO_FILE ; do
  FILENAME=$(basename "$PROTO_FILE")
  cp "${PROTO_FILE}" "${PROTOGEN_DIR}/$FILENAME"
done < <(find "$TEMP_DIR" -name "*.pyi" -print0)

# Write file
python3 "$SCRIPT_DIR/common/utils/directory_hash.py" update "$SCRIPT_DIR/../python_proto_sum.txt" \
  "$PROTOS_DIR" ".proto" "$PROTOGEN_DIR" ".py" "$PROTOGEN_DIR" ".pyi" \
  "$SCRIPT_DIR/install_protoc.sh" "" "$SCRIPT_DIR/../protoc_install" "" "$SCRIPT_DIR/generate_python_protos.sh" "" \
  "$SCRIPT_DIR/common/utils/directory_hash.py" ""
