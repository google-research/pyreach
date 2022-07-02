#! /bin/bash

set -uexo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
readonly SCRIPT_DIR

echo "Installing protoc..."
readonly PROTOC_VERSION="3.12.4"

if [[ -f "$SCRIPT_DIR"/../protoc_install/bin/protoc ]] ; then
  if [[ "$("$SCRIPT_DIR"/../protoc_install/bin/protoc --version)" != "libprotoc $PROTOC_VERSION" ]] ; then
    echo "Incorrect protoc version installed, re-installing..."
    rm -r "$SCRIPT_DIR"/../protoc_install
  fi
fi

if ! [[ -f "$SCRIPT_DIR"/../protoc_install/bin/protoc ]] ; then
  if [[ -e "$SCRIPT_DIR"/../protoc_install ]] ; then
    rm -r "$SCRIPT_DIR"/../protoc_install
  fi
  UNAME_S="$(uname -s | tr '[:lower:]' '[:upper:]')"
  readonly UNAME_S
  if [[ "${UNAME_S:0:6}" == "DARWIN" ]] ; then
    PROTOC_OS="osx-$(uname -m)"
  elif [[ "${UNAME_S:0:5}" == "LINUX" ]] ; then
    PROTOC_OS="linux-$(uname -m)"
  elif [[ "${UNAME_S:0:5}" == "MINGW" ]] || [[ "${UNAME_S:1:5}" == "CYGWIN" ]] ; then
    if [[ "$(uname -m)" == "x86_64" ]] ; then
      PROTOC_OS="win64"
    else
      PROTOC_OS="win32"
    fi
  else
    echo "Unknown OS platform, we could not install protoc."
    exit 1
  fi

  mkdir -p "$SCRIPT_DIR"/../protoc_install
  if [[ -z "${KOKORO_GFILE_DIR-}" ]] ; then
    curl -o "$SCRIPT_DIR"/../protoc_install/protoc.zip "https://storage.googleapis.com/brain-reach/protoc/protoc-$PROTOC_VERSION-$PROTOC_OS.zip"
  else
    cp "$KOKORO_GFILE_DIR/protoc-$PROTOC_VERSION-$PROTOC_OS.zip" "$SCRIPT_DIR"/../protoc_install/protoc.zip
  fi
  (cd "$SCRIPT_DIR"/../protoc_install && unzip protoc.zip)
  chmod a+x "$SCRIPT_DIR"/../protoc_install/bin/protoc
  rm "$SCRIPT_DIR"/../protoc_install/protoc.zip
fi
