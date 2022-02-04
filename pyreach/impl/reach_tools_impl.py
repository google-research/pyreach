"""Download and/or find the reach tools binaries."""

import hashlib
import os
import pathlib
import platform
import shutil
import stat
from typing import Dict, Optional, Tuple

import requests

WEBRTC_LINUX_X86_64_HASH = "afeb5d7fe13823c4316894823e0b9b10aadefa609eb2623dc218118866beb1ca"
_WEBRTC_SHA256 = {
    "linux": {
        "x86_64":
            WEBRTC_LINUX_X86_64_HASH,
    },
}

REACH_LINUX_X86_64_HASH = "09ea88231624f2707dda529f15a09d0633240cbdfa7151a4b873e5b5d900634a"
_REACH_SHA256 = {
    "linux": {
        "x86_64":
            REACH_LINUX_X86_64_HASH,
    },
}

_WEBRTC_BASE = "https://storage.googleapis.com/brain-reach-public/releases/webrtc/%s-%s/webrtc_headless%s."
_REACH_BASE = "https://storage.googleapis.com/brain-reach-public/releases/reach/%s-%s/reach%s."

_is_running_on_google3 = False


class DownloadError(SystemError):
  """Error if the tool cannot be downloaded or located."""
  pass


def _get_extension() -> str:
  if platform.system().lower() == "windows":
    return ".exe"
  return ""


def _download(base: str, digests: Dict[str, Dict[str, str]],
              target_file: pathlib.Path) -> None:
  """Download an executable file.

  Args:
    base: the base URL.
    digests: the digest of the files.
    target_file: the path to which to save the file.

  Raises:
    DownloadError: if the file cannot be downloaded.

  """
  if platform.system().lower() not in digests:
    raise DownloadError("Platform \"%s\" is not supported" %
                        platform.system().lower())
  if platform.machine().lower() not in digests[platform.system().lower()]:
    raise DownloadError("Machine \"%s\" on platform \"%s\" is not supported" %
                        (platform.machine().lower(), platform.system().lower()))
  digest = digests[platform.system().lower()][platform.machine().lower()]
  if target_file.exists():
    bin_file = target_file.open("rb")
    bin_content = bin_file.read()
    bin_file.close()

    sha = hashlib.sha256()
    sha.update(bin_content)
    if sha.hexdigest() == digest:
      return

  remote_name = (base % (platform.system().lower(), platform.machine().lower(),
                         _get_extension())) + digest
  remote_file = requests.get(remote_name, allow_redirects=True)
  sha = hashlib.sha256()
  sha.update(remote_file.content)
  if sha.hexdigest() != digest:
    raise DownloadError("digest mismatch for %s" % remote_name)

  if os.path.exists(target_file):
    os.remove(target_file)

  bin_file = target_file.open("wb")
  bin_file.write(remote_file.content)
  bin_file.close()

  st = target_file.stat()
  target_file.chmod(st.st_mode | stat.S_IEXEC)


def _get_reach_dir() -> Optional[pathlib.Path]:
  """Get the reach directory using .reach files."""
  test_directories = []
  cwd: pathlib.Path = pathlib.Path(".").absolute()
  test_directories.append(cwd)
  test_directories.extend(cwd.parents)
  test_directories.extend(pathlib.Path(__file__).parents)
  for test_dir in test_directories:
    test_file: pathlib.Path = test_dir / ".reach"
    if test_file.is_file():
      return test_dir
  return None


def download_reach_tool(
    workspace: Optional[pathlib.Path]) -> Tuple[pathlib.Path, pathlib.Path]:
  """Get the reach tool path or download the reach tool from the cloud.

  Args:
    workspace: the workspace path to download the tool to.

  Raises:
    DownloadError: if the file cannot be downloaded.

  Returns:
    The path of the reach tool, which may not be in the workspace, and the
    working directory to launch to tool within.
  """
  if _is_running_on_google3:
    if workspace is None:
      raise DownloadError("Workspace required in google3")
    reach_file = workspace / "reach"
    return reach_file, workspace
  else:
    reach_dir = _get_reach_dir()
    if reach_dir:
      reach_exe_paths = [
          (reach_dir / "go" / "bin" / ("reach" + _get_extension()),
           reach_dir / "go"),
          (reach_dir / "bin" / ("reach" + _get_extension()), reach_dir),
      ]
      for exe, wd in reach_exe_paths:
        if exe.exists():
          return exe, wd

      if workspace is None:
        raise DownloadError("Reach binary not found in {reach_exe_paths}")
    if workspace is None:
      raise DownloadError("Reach directory not found, no workspace specified")
    _download(_REACH_BASE, _REACH_SHA256, workspace / "reach")
    return workspace / "reach", workspace


def download_webrtc_headless(workspace: Optional[pathlib.Path]) -> pathlib.Path:
  """Get the webrtc_headless path or download the reach tool from the cloud.

  Args:
    workspace: the workspace path to download webrtc_headless to.

  Raises:
    DownloadError: if the file cannot be downloaded.

  Returns:
    The path of the webrtc_headless binary, which may not be in the workspace.
  """
  if not _is_running_on_google3:
    reach_dir = _get_reach_dir()
    if reach_dir:
      webrtc_exe_paths = [
          reach_dir / "go" / ("webrtc_headless" + _get_extension()),
          reach_dir / ("webrtc_headless" + _get_extension()),
      ]
      for exe in webrtc_exe_paths:
        if exe.exists():
          return exe
      if workspace is None:
        raise DownloadError("WebRTC binary not found in {webrtc_exe_paths}")
  if workspace is None:
    raise DownloadError("Reach directory not found, no workspace specified")
  webrtc_file = workspace / ("webrtc_headless" + _get_extension())
  _download(_WEBRTC_BASE, _WEBRTC_SHA256, webrtc_file)
  return webrtc_file


def create_reach_workspace() -> pathlib.Path:
  """Create the ~reach_workspace folder and return the path to it."""
  home_dir = pathlib.Path.home()
  if not home_dir.is_dir():
    raise RuntimeError(
        "Operating system home directory %s is not a home directory" % home_dir)
  working_directory = home_dir / "reach_workspace"
  if not working_directory.is_dir():
    working_directory.mkdir()
  return working_directory
