#! /usr/bin/env python3
"""This script computes a sha512 hash of all files in a list of directories and writes it to a file as a hex string.

Usage:
  python3 directory_hash.py <action> <output> <path1> <ext1> <path2> <ext2>...

action: either "compare" or "update". If "compare", will compute the hash and
  compare it with the value in output_file, returning a non-zero exit code if
  the hash value is different or the output_file does not exist.
output: the output filename for the hash to be saved to.
path/ext: path of the directory/file to include in the hash, ext is the
  postfix of the filename(s) to include (e.g. ".py" to only include ".py"
  files). The path and ext can be repeated to include many paths. If ext is
  empty or missing (for the last argument), it will include all files.
"""

import hashlib
import os
import sys
from typing import Iterable, List, Optional, Tuple


def _hash_file(filename: str) -> str:
  """Compute the hex sha512 hash of a file."""
  sha512 = hashlib.sha512()
  with open(filename, "rb") as f:
    while True:
      file_data = f.read(4096)
      if not file_data:
        break
      sha512.update(file_data)
  return sha512.hexdigest()


def _hash_files(path: str, postfix: Optional[str]) -> List[Tuple[str, str]]:
  """Compute the sha512 hash all files in a given directory, with an extension."""
  file_hashes = []
  if os.path.isdir(path):
    for root, _, filenames in os.walk(path):
      for filename in filenames:
        filename = os.path.join(root, filename)
        if postfix is not None and not filename.endswith(postfix):
          continue
        file_hashes.append((filename, _hash_file(filename)))
  elif os.path.exists(path) and (postfix is None or path.endswith(postfix)):
    file_hashes.append((path, _hash_file(path)))
  return file_hashes


def _hash_hashes(hashes: Iterable[Tuple[str, str]]) -> str:
  """Compute the sha512 hash of a list of name-hash tuples."""
  hashes_sorted = list(hashes)
  hashes_sorted.sort(key=lambda x: x[0])

  sha512 = hashlib.sha512()
  for name, hash_value in hashes_sorted:
    sha512.update(name.encode("utf-8").hex().encode("utf-8"))
    sha512.update(b"|")
    sha512.update(hash_value.encode("utf-8"))
    sha512.update(b"|")
  return sha512.hexdigest()


def _main() -> None:
  """Main method of the script."""
  if len(sys.argv) <= 1:
    raise ValueError("Must specify action")
  action = sys.argv[1]
  if action != "compare" and action != "update":
    raise ValueError("Action must be compare or update")
  if len(sys.argv) <= 2:
    raise ValueError("Must specify state file")
  state_file = sys.argv[2]

  file_hashes = {}
  dir_index = 0
  while dir_index + 3 < len(sys.argv):
    path = sys.argv[dir_index + 3]
    postfix = None
    if dir_index + 4 < len(sys.argv):
      postfix = sys.argv[dir_index + 4]
    dir_index += 2
    print("Including directory", path, "postfix", postfix)
    for filename, file_hash in _hash_files(path, postfix):
      print(filename, file_hash)
      file_hashes[filename] = file_hash

  total_hash = _hash_hashes(file_hashes.items())
  print("SHA512 data output:", total_hash)

  if action == "update":
    with open(state_file, "wb") as file_writer:
      file_writer.write(total_hash.encode("utf-8"))
    print(state_file, "updated")
  elif action == "compare":
    with open(state_file, "rb") as file_reader:
      hex_data = file_reader.read(1024)
      assert not file_reader.read(1)
      if hex_data.decode("utf-8").strip() != total_hash:
        raise ValueError("hash has changed")
      else:
        print(state_file, "hash is the same")


if __name__ == "__main__":
  _main()
