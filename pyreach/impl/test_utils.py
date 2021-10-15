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
"""Testing utilities for PyReach."""

import dataclasses
import hashlib
import json
import os
import queue
import threading
from typing import Any, Callable, Dict, List, Optional, Tuple
import urllib.request

import numpy as np  # type: ignore
from PIL import Image  # type: ignore

from pyreach.common.proto_gen import logs_pb2  # type: ignore
from pyreach.common.python import types_gen
from pyreach.impl import client
from pyreach.impl import device_base
from pyreach.impl import utils
import cv2  # type: ignore


def device_data_equal(data_1: types_gen.DeviceData,
                      data_2: types_gen.DeviceData) -> bool:
  """Test if two device datas are equal, including images.

  Args:
    data_1: first device data
    data_2: second device data

  Returns:
    If the device data elements are equal.
  """
  if json.dumps(data_1.to_json()) != json.dumps(data_2.to_json()):
    return False
  color_image_1: Optional[np.ndarray] = None
  color_image_2: Optional[np.ndarray] = None
  depth_image_1: Optional[np.ndarray] = None
  depth_image_2: Optional[np.ndarray] = None
  if isinstance(data_1, utils.ImagedDeviceData):
    data_1_translated: utils.ImagedDeviceData = data_1
    color_image_1 = data_1_translated.color_image
    depth_image_1 = data_1_translated.depth_image
  if isinstance(data_2, utils.ImagedDeviceData):
    data_2_translated: utils.ImagedDeviceData = data_2
    color_image_2 = data_2_translated.color_image
    depth_image_2 = data_2_translated.depth_image
  if color_image_1 is None and color_image_2 is not None:
    return False
  if color_image_1 is not None and (
      color_image_2 is None or color_image_1.shape != color_image_2.shape or
      not np.array_equal(color_image_1, color_image_2)):
    return False
  if depth_image_1 is None and color_image_2 is not None:
    return False
  if depth_image_1 is not None and (
      depth_image_2 is None or depth_image_1.shape != depth_image_2.shape or
      not np.array_equal(depth_image_1, depth_image_2)):
    return False
  return True


def command_data_equal(data_1: types_gen.CommandData,
                       data_2: types_gen.CommandData) -> bool:
  """Test if two command datas are equal.

  Args:
    data_1: first device data
    data_2: second device data

  Returns:
    If the command data elements are equal.
  """
  return json.dumps(data_1.to_json()) == json.dumps(data_2.to_json())


class TestResponder:
  """TestResponder is a class used for testing the responder."""

  _test_image_dir: str

  def __init__(self) -> None:
    """Init a TestResponder."""
    self._test_image_dir = ""

  def set_test_image_dir(self, test_image_dir: str) -> None:
    """Set the test image dir."""
    self._test_image_dir = test_image_dir

  @property
  def test_image_dir(self) -> str:
    """Get the test image dir."""
    return self._test_image_dir

  def start(self) -> List[types_gen.DeviceData]:
    """Start the TestResponder."""
    raise NotImplementedError("TestResponder does not implement start()")

  def step(self, cmd: types_gen.CommandData) -> List[types_gen.DeviceData]:
    """Step the TestResponder.

    Args:
      cmd: the command to execute.
    """
    raise NotImplementedError("TestResponder does not implement step()")


@dataclasses.dataclass(frozen=True)
class TestResponderStep:
  """TestResponderStep describes a test to the TestResponder."""
  command: types_gen.CommandData
  data: Tuple[types_gen.DeviceData, ...] = ()


class RejectResponder(TestResponder):
  """A class for generating a regected DeviceData message."""

  def start(self) -> List[types_gen.DeviceData]:
    """Start the responder with no messages."""
    return []

  def step(self, cmd: types_gen.CommandData) -> List[types_gen.DeviceData]:
    """Generate one rejected message.

    Args:
      cmd: The CommandData to get the device type/name from.

    Returns:
      A list containing a rejected Device Data message if
      the cmd is untagged; otherwise an empty list is returned.

    """
    if cmd.tag:
      return [
          types_gen.DeviceData(
              device_type=cmd.device_type,
              device_name=cmd.device_name,
              data_type="cmd-status",
              ts=cmd.ts,
              local_ts=cmd.ts,
              tag=cmd.tag,
              status="rejected",
          )
      ]
    return []


def is_frame_request_for(cmd: types_gen.CommandData, device_type: str,
                         device_name: str) -> bool:
  """Return whether CommandData is a frame request..

  Args:
    cmd: The CommandData to examine.
    device_type: The device type to match.
    device_name: The device name to match.

  Returns:
    Returns True for frame frame request and False othewise.

  """
  if cmd.data_type != "frame-request":
    return False
  if cmd.device_type == device_type and cmd.device_name == device_name:
    return True
  return False


def assert_image_equal(image: np.ndarray, filename: str) -> None:
  """Verify that memory image matches a file image.

  Args:
    image: The memory image to test.
    filename: The file name for the image.
  """
  image_pil = Image.open(get_test_image_file(filename))
  im = np.array(image_pil)
  if len(im.shape) == 2:
    im = np.tile(im[..., None], (1, 1, 3))  # grey to rgb.
  assert im is not None, "Failed to read: " + filename
  assert len(im.shape) == len(
      image.shape), "Image shape invalid for %s, got %s wanted %s" % (
          filename, str(image.shape), str(im.shape))
  for im_shape, image_shape in zip(im.shape, image.shape):
    assert im_shape == image_shape, (
        "Image shape invalid for %s, got %s wanted %s") % (
            filename, str(image.shape), str(im.shape))
  assert np.array_equal(im, image), "Images unequal for: " + filename


def assert_image_depth_equal(image: np.ndarray, filename: str) -> None:
  """Verify that memory depth image matches a file depth image.

  Args:
    image: The memory image to test.
    filename: The file name for the image.
  """
  im = cv2.imread(get_test_image_file(filename), cv2.IMREAD_ANYDEPTH)
  assert im is not None, "Failed to read: " + filename
  assert len(im.shape) == len(
      image.shape), "Image shape invalid for %s, got %s wanted %s" % (
          filename, str(image.shape), str(im.shape))
  for im_shape, image_shape in zip(im.shape, image.shape):
    assert im_shape == image_shape, (
        "Image shape invalid for %s, got %s wanted %s") % (
            filename, str(image.shape), str(im.shape))
  assert np.array_equal(im, image), "Images unequal for: " + filename


def run_test_client_test(responders: List[TestResponder],
                         steps: List[TestResponderStep]) -> None:
  """Run a test client with a list of responders.

  Args:
    responders: A list of responders to execute.
    steps: A list of steps to execute.
  """
  with TestClient(responders) as test_client:
    # Flush startup data
    while True:
      try:
        test_client.get_queue().get(block=False)
      except queue.Empty:
        break
    for index, step in enumerate(steps):
      test_client.send_cmd(step.command)
      response: List[types_gen.DeviceData] = []
      while True:
        try:
          data = test_client.get_queue().get(block=False)
          assert data is not None, "client is not"
          response.append(data)
        except queue.Empty:
          break
      assert len(response) == len(
          step.data), (("Got %d data messages, expected %d for step %d (%s)" %
                        (len(response), len(step.data), index,
                         json.dumps(step.command.to_json()))))
      for response_element, expect in zip(response, step.data):
        response_json = json.dumps(response_element.to_json())
        expect_json = json.dumps(expect.to_json())
        assert response_json == expect_json, (
            ("Got %s data, expected %s for step %d (%s)" %
             (response_json, expect_json, index,
              json.dumps(step.command.to_json()))))


_color_only_dirs = ["oracle-pick-points", "uvc", "vnc", "realsense_invoice"]
_depth_dirs = ["photoneo", "realsense"]
_depth_hashes = {
    "photoneo":
        "73bf338cfda219ce902e4f455d6b92d9a9454854c3b75bacd6236205ec26c222",
    "realsense":
        "c8bc837b0ea1bce0aa501628f621b15ddcf783e48d545251b7600458cfdb33cf",
}
_color_hashes = {
    "oracle-pick-points":
        "9570d1a7b8c8bcb2686774e37152e09e1654733e45522bf6ddf2d67c2a3e20ff",
    "uvc":
        "b3f94b6d20e31a4d8a66bc23cb51b22bf77a0e5e261efab6b8f0f52757ee89c4",
    "vnc":
        "fa9efbb9b77a3d173d5504b8c75a2f454d8ed34afec5b9f589b15c899e3e94da",
    "realsense_invoice":
        "391c3ac27293de984748e09c5188fbd5ec2750f3b3ba0d335bab83a66f251f0d",
    "photoneo":
        "67b5cf78146ec6aa7f696b4d80eb27e5846df78c18d106b432478e298594cc98",
    "realsense":
        "4a1e527a915db7ece52a662121c815d417b56f3434ef03eb4ff4018e249941ea",
}


def _file_hash(filename: str) -> str:
  """Compute the hash of a file.

  Args:
    filename: the filename to hash.

  Returns:
    The hash hex string of the file contents.
  """
  sha256_hash = hashlib.sha256()
  with open(filename, "rb") as f:
    # Read and update hash string value in blocks of 4K
    while True:
      l: bytes = f.read(4096)
      if not l:
        return sha256_hash.hexdigest()
      sha256_hash.update(l)


_is_running_on_google3 = False


def _get_google3_resources_directory() -> str:
  return os.path.join(
      
      "google3/robotics/learning/reach/third_party/pyreach/impl")


def _verify_download(test_image_dir: str) -> None:
  """Verify the download of the directory.

  Args:
    test_image_dir: The test image directory.
  """
  for directory in _color_only_dirs + _depth_dirs:
    filename = os.path.join(test_image_dir, "test_images", directory,
                            "color.jpg")
    file_hash = _file_hash(filename)
    expect_file_hash = _color_hashes[directory]
    assert file_hash == expect_file_hash, (
        "Wanted %s got %s for %s" % (expect_file_hash, file_hash, filename))
  for directory in _depth_dirs:
    filename = os.path.join(test_image_dir, "test_images", directory,
                            "depth.pgm")
    file_hash = _file_hash(filename)
    expect_file_hash = _depth_hashes[directory]
    assert file_hash == expect_file_hash, (
        "Wanted %s got %s for %s" % (expect_file_hash, file_hash, filename))


def get_test_image_file(image_file: str) -> str:
  if _is_running_on_google3:
    return os.path.join(_get_google3_resources_directory(), image_file)
  return image_file


class _DataDownloader:
  """DataDownloader downloads testing image data."""
  _test_image_dir: str

  def __init__(self, test_image_dir: str) -> None:
    """Initialize a data downloader.

    Args:
      test_image_dir: path to download to. If None, a temporary directory will
        be created.
    """
    self._test_image_dir = test_image_dir
    if not self._test_image_dir and _is_running_on_google3:
      self._test_image_dir = _get_google3_resources_directory()
    self._download_data_replay()

  def close(self) -> None:
    """Close the temporary directory."""
    pass

  @property
  def test_image_dir(self) -> str:
    """Get the image directory.

    Returns:
      The image directory path.
    """
    return self._test_image_dir

  @classmethod
  def _file_hash(cls, filename: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
      # Read and update hash string value in blocks of 4K
      while True:
        l: bytes = f.read(4096)
        if not l:
          return sha256_hash.hexdigest()
        sha256_hash.update(l)

  def _download_data_replay(self) -> None:
    """Download data replay files."""
    if _is_running_on_google3:
      return
    pd = os.path.join(self._test_image_dir, "test_images")
    if not os.path.isdir(pd):
      os.makedirs(pd)
      if not os.path.isdir(pd):
        raise RuntimeError("Could not create " + pd + " directory")
    for directory in _color_only_dirs + _depth_dirs:
      if not os.path.isdir(os.path.join(pd, directory)):
        os.makedirs(os.path.join(pd, directory))
        if not os.path.isdir(os.path.join(pd, directory)):
          raise Exception("Could not create " + directory + " directory")
    for directory in _depth_dirs:
      filename = os.path.join(pd, directory, "depth.pgm")
      if os.path.isfile(filename):
        if self._file_hash(filename) != _depth_hashes[directory]:
          os.remove(filename)
      if not os.path.isfile(filename):
        urllib.request.urlretrieve(
            "https://storage.googleapis.com/brain-reach-testing-public/" +
            "test_images/" + directory + "/depth.pgm", filename)
        if self._file_hash(filename) != _depth_hashes[directory]:
          raise Exception("File failed to download: " + filename +
                          " invalid hash: " + self._file_hash(filename) +
                          " != " + _depth_hashes[directory])
    for directory in _color_only_dirs + _depth_dirs:
      filename = os.path.join(pd, directory, "color.jpg")
      if os.path.isfile(filename):
        if _file_hash(filename) != _color_hashes[directory]:
          os.remove(filename)
      if not os.path.isfile(filename):
        urllib.request.urlretrieve(
            "https://storage.googleapis.com/brain-reach-testing-public/" +
            "test_images/" + directory + "/color.jpg", filename)
        if _file_hash(filename) != _color_hashes[directory]:
          raise Exception("File failed to download: " + filename +
                          " invalid hash: " + self._file_hash(filename) +
                          " != " + _color_hashes[directory])


class TestClient(client.Client):
  """TestClient is a simulated client for testing."""
  _responders: List[TestResponder]
  _queue: "queue.Queue[Optional[types_gen.DeviceData]]"
  _data_downloader: _DataDownloader
  _key_values: Dict[device_base.KeyValueKey, str]
  _closed: bool
  _lock: threading.Lock

  def __init__(self,
               responders: List[TestResponder],
               test_image_dir: str = "") -> None:
    self._responders = responders.copy()
    self._queue = queue.Queue()
    self._key_values = {}
    self._data_downloader = _DataDownloader(test_image_dir)
    self._closed = False
    self._lock = threading.Lock()
    for responder in self._responders:
      if self._data_downloader:
        responder.set_test_image_dir(self._data_downloader.test_image_dir)
      for data in responder.start():
        self._on_data(data)
    self._send_workcell_constraints()

  def _send_workcell_constraints(self) -> None:
    self._on_data(
        types_gen.DeviceData(
            device_type="settings-engine",
            data_type="key-value",
            key="robot-name",
            value="python-local-test"))
    self._on_data(
        types_gen.DeviceData(
            device_type="settings-engine",
            data_type="key-value",
            key="display-name",
            value="python-local-test-display"))
    value: str = ""
    devices_dict1: Dict[str, Any] = {
        "devices": [
            {
                "deviceName": "",
                "deviceType": "photoneo",
                "parameters": {
                    "distortion": [
                        0.09671527357280167,
                        -0.07269189555506897,
                        -0.000951967008087239,
                        -0.00023978235176561128,
                        0.02222360047734214,
                    ],
                    "distortionDepth": [
                        0.0, 0.0001, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
                    ],
                    "extrinsics": [
                        0.22109726464426824,
                        0.846220696121779,
                        0.6781860180257879,
                        -0.0007419191902880004,
                        -3.0717530124756776,
                        0.0791355221844608,
                    ],
                    "extrinsicsResidual": 0.847604346436239,
                    "height": 720,
                    "intrinsics": [
                        614.4226644188208,
                        614.2925544327617,
                        637.5925421650695,
                        368.6902449579668,
                    ],
                    "intrinsicsResidual": 0.7867047898193731,
                    "lensModel": "pinhole",
                    "width": 1280,
                },
            },
            {
                "deviceName": "",
                "deviceType": "uvc",
                "parameters": {
                    "distortion": [
                        -0.39962187587186027,
                        0.22068272883130644,
                        0.0012368841448122624,
                        -0.005762682607595475,
                        -0.12148691849607768,
                    ],
                    "extrinsics": [
                        0.7531231302651079,
                        1.087324944480214,
                        0.6682052543958973,
                        -0.4748236935049469,
                        -2.5928092583157696,
                        0.7670524228261605,
                    ],
                    "extrinsicsResidual": 0,
                    "height": 480,
                    "intrinsics": [
                        492.4023039438801,
                        659.4542603703194,
                        360.64022589748015,
                        258.97869057403403,
                    ],
                    "intrinsicsResidual": 0.7121210453380693,
                    "lensModel": "pinhole",
                    "width": 640,
                },
            },
            {
                "deviceName": "",
                "deviceType": "ur",
                "parameters": {
                    "calibrationPose": {
                        "cartesian": [
                            0.18981426551943226,
                            0.7577366621584035,
                            0.18993715300539438,
                            3.0948312971138217,
                            -0.22872878991389,
                            -0.15831493331231813,
                        ],
                        "joints": [
                            1.484591484069824,
                            -2.40558971981191,
                            -1.143593788146973,
                            -1.198892430668213,
                            1.6722731590271,
                            0.05952787399291992,
                        ],
                    },
                    "extrinsics": [0, 0, 0, 0, 0, 0],
                    "extrinsicsResidual": 0.8939242386824056,
                    "urdf": "ur5e.urdf",
                },
            },
            {
                "deviceName": "bodyTag",
                "deviceType": "object",
                "parameters": {
                    "extrinsics": [
                        0.004270144488352508,
                        -0.05865820444219114,
                        0.0994273206740789,
                        0.06404749466733574,
                        -2.185599560110493,
                        2.193027383401797,
                    ],
                    "extrinsicsResidual": 0.847604346436239,
                    "id": 100,
                    "intrinsics": [0.0409, 0.0409, 0],
                    "linkName": "wrist_2_link",
                    "toolMount": "ur",
                },
            },
        ],
        "robot-name": "reach10",
        "timestamp": 1582160284.885034,
        "version": 20190118,
    }

    self._on_data(
        types_gen.DeviceData(
            device_type="settings-engine",
            data_type="key-value",
            key="calibration.json",
            value=json.dumps(devices_dict1)))

    value_dict = {
        "actions": None,
        "created": "2020-12-02T22:54:17Z",
        "createdBy": "UoLKe5L3I5R1vdJmxXiE39zy76u2",
        "version": 7
    }

    actions_dict = [{
        "_steps": [{
            "_tipInputIdx": 0,
            "_parentType": 1,
            "pos": {
                "x": -3.0494608879089357,
                "y": -0.00036135315895080566,
                "z": 0.22043436765670777
            },
            "rot": {
                "x": 0.0011294787982478738,
                "y": -0.07471251487731934,
                "z": 0.01551392488181591,
                "w": -0.9970837831497192
            },
            "_delay": 0.0,
            "_radius": 0.0,
            "_velocity": 0.0,
            "_acceleration": 0.0,
            "_wait": 0.0,
            "_parentStepIdx": 0,
            "_useProcessMode": False,
            "_individualVelocityAcceleration": False,
            "_useForceMode": False,
            "_useServoJMode": False,
            "_useSkipMove": False,
            "_setDigitalIO": False,
            "_setToolDigitalIO": False,
            "_setDigitalIONumber": 0,
            "_setToolDigitalIONumber": 0,
            "_setDigitalIOValue": False,
            "_setToolDigitalIOValue": False,
            "_setCapability": False,
            "_setCapabilityName": "",
            "_setCapabilityType": "",
            "_setCapabilityValue": False,
            "_setCapabilityIOType": "",
            "_randomizedOffset": False,
            "_randomizedOffsetRadiusCM": 5.0
        }, {
            "_tipInputIdx": -1,
            "_parentType": 0,
            "pos": {
                "x": 3.5145723819732666,
                "y": -2.0607705116271973,
                "z": -0.9359455108642578
            },
            "rot": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            },
            "_delay": 0.0,
            "_radius": 0.0,
            "_velocity": 0.0,
            "_acceleration": 0.0,
            "_wait": 0.0,
            "_parentStepIdx": 0,
            "_useProcessMode": False,
            "_individualVelocityAcceleration": False,
            "_useForceMode": False,
            "_useServoJMode": False,
            "_useSkipMove": True,
            "_setDigitalIO": False,
            "_setToolDigitalIO": False,
            "_setDigitalIONumber": 0,
            "_setToolDigitalIONumber": 0,
            "_setDigitalIOValue": False,
            "_setToolDigitalIOValue": False,
            "_setCapability": True,
            "_setCapabilityName": "",
            "_setCapabilityType": "vacuum",
            "_setCapabilityValue": True,
            "_setCapabilityIOType": "DigitalOutput",
            "_randomizedOffset": False,
            "_randomizedOffsetRadiusCM": 5.0
        }, {
            "_tipInputIdx": -1,
            "_parentType": 0,
            "pos": {
                "x": 0.21285633742809296,
                "y": 0.2875767946243286,
                "z": 0.3596976399421692
            },
            "rot": {
                "x": 0.6918290257453918,
                "y": 0.7147566080093384,
                "z": 0.07859083265066147,
                "w": 0.0657198429107666
            },
            "_delay": 0.0,
            "_radius": 0.0,
            "_velocity": 0.0,
            "_acceleration": 0.0,
            "_wait": 0.0,
            "_parentStepIdx": 0,
            "_useProcessMode": False,
            "_individualVelocityAcceleration": False,
            "_useForceMode": False,
            "_useServoJMode": False,
            "_useSkipMove": False,
            "_setDigitalIO": False,
            "_setToolDigitalIO": False,
            "_setDigitalIONumber": 0,
            "_setToolDigitalIONumber": 0,
            "_setDigitalIOValue": False,
            "_setToolDigitalIOValue": False,
            "_setCapability": False,
            "_setCapabilityName": "",
            "_setCapabilityType": "",
            "_setCapabilityValue": False,
            "_setCapabilityIOType": "",
            "_randomizedOffset": False,
            "_randomizedOffsetRadiusCM": 5.0
        }, {
            "_tipInputIdx": -1,
            "_parentType": 0,
            "pos": {
                "x": 3.5145723819732666,
                "y": -2.0607705116271973,
                "z": -0.9359455108642578
            },
            "rot": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            },
            "_delay": 0.0,
            "_radius": 0.0,
            "_velocity": 0.0,
            "_acceleration": 0.0,
            "_wait": 0.0,
            "_parentStepIdx": 0,
            "_useProcessMode": False,
            "_individualVelocityAcceleration": False,
            "_useForceMode": False,
            "_useServoJMode": False,
            "_useSkipMove": True,
            "_setDigitalIO": False,
            "_setToolDigitalIO": False,
            "_setDigitalIONumber": 0,
            "_setToolDigitalIONumber": 0,
            "_setDigitalIOValue": False,
            "_setToolDigitalIOValue": False,
            "_setCapability": True,
            "_setCapabilityName": "",
            "_setCapabilityType": "vacuum",
            "_setCapabilityValue": False,
            "_setCapabilityIOType": "DigitalOutput",
            "_randomizedOffset": False,
            "_randomizedOffsetRadiusCM": 5.0
        }, {
            "_tipInputIdx": -1,
            "_parentType": 0,
            "pos": {
                "x": 3.5145723819732666,
                "y": -2.0607705116271973,
                "z": -0.9359455108642578
            },
            "rot": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            },
            "_delay": 0.0,
            "_radius": 0.0,
            "_velocity": 0.0,
            "_acceleration": 0.0,
            "_wait": 0.5,
            "_parentStepIdx": 0,
            "_useProcessMode": False,
            "_individualVelocityAcceleration": False,
            "_useForceMode": False,
            "_useServoJMode": False,
            "_useSkipMove": True,
            "_setDigitalIO": False,
            "_setToolDigitalIO": False,
            "_setDigitalIONumber": 0,
            "_setToolDigitalIONumber": 0,
            "_setDigitalIOValue": False,
            "_setToolDigitalIOValue": False,
            "_setCapability": False,
            "_setCapabilityName": "",
            "_setCapabilityType": "",
            "_setCapabilityValue": False,
            "_setCapabilityIOType": "",
            "_randomizedOffset": False,
            "_randomizedOffsetRadiusCM": 5.0
        }, {
            "_tipInputIdx": -1,
            "_parentType": 0,
            "pos": {
                "x": 3.5145723819732666,
                "y": -2.0607705116271973,
                "z": -0.9359455108642578
            },
            "rot": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            },
            "_delay": 0.0,
            "_radius": 0.0,
            "_velocity": 0.0,
            "_acceleration": 0.0,
            "_wait": 0.5,
            "_parentStepIdx": 0,
            "_useProcessMode": False,
            "_individualVelocityAcceleration": False,
            "_useForceMode": False,
            "_useServoJMode": False,
            "_useSkipMove": True,
            "_setDigitalIO": False,
            "_setToolDigitalIO": False,
            "_setDigitalIONumber": 0,
            "_setToolDigitalIONumber": 0,
            "_setDigitalIOValue": False,
            "_setToolDigitalIOValue": False,
            "_setCapability": False,
            "_setCapabilityName": "",
            "_setCapabilityType": "",
            "_setCapabilityValue": False,
            "_setCapabilityIOType": "",
            "_randomizedOffset": False,
            "_randomizedOffsetRadiusCM": 5.0
        }, {
            "_tipInputIdx": -1,
            "_parentType": 0,
            "pos": {
                "x": 3.5145723819732666,
                "y": -2.0607705116271973,
                "z": -0.9359455108642578
            },
            "rot": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            },
            "_delay": 0.0,
            "_radius": 0.0,
            "_velocity": 0.0,
            "_acceleration": 0.0,
            "_wait": 0.5,
            "_parentStepIdx": 0,
            "_useProcessMode": False,
            "_individualVelocityAcceleration": False,
            "_useForceMode": False,
            "_useServoJMode": False,
            "_useSkipMove": True,
            "_setDigitalIO": False,
            "_setToolDigitalIO": False,
            "_setDigitalIONumber": 0,
            "_setToolDigitalIONumber": 0,
            "_setDigitalIOValue": False,
            "_setToolDigitalIOValue": False,
            "_setCapability": False,
            "_setCapabilityName": "",
            "_setCapabilityType": "",
            "_setCapabilityValue": False,
            "_setCapabilityIOType": "",
            "_randomizedOffset": False,
            "_randomizedOffsetRadiusCM": 5.0
        }, {
            "_tipInputIdx": -1,
            "_parentType": 0,
            "pos": {
                "x": 3.5145723819732666,
                "y": -2.0607705116271973,
                "z": -0.9359455108642578
            },
            "rot": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            },
            "_delay": 0.0,
            "_radius": 0.0,
            "_velocity": 0.0,
            "_acceleration": 0.0,
            "_wait": 0.5,
            "_parentStepIdx": 0,
            "_useProcessMode": False,
            "_individualVelocityAcceleration": False,
            "_useForceMode": False,
            "_useServoJMode": False,
            "_useSkipMove": True,
            "_setDigitalIO": False,
            "_setToolDigitalIO": False,
            "_setDigitalIONumber": 0,
            "_setToolDigitalIONumber": 0,
            "_setDigitalIOValue": False,
            "_setToolDigitalIOValue": False,
            "_setCapability": False,
            "_setCapabilityName": "",
            "_setCapabilityType": "",
            "_setCapabilityValue": False,
            "_setCapabilityIOType": "",
            "_randomizedOffset": False,
            "_randomizedOffsetRadiusCM": 5.0
        }, {
            "_tipInputIdx": -1,
            "_parentType": 0,
            "pos": {
                "x": 3.5145723819732666,
                "y": -2.0607705116271973,
                "z": -0.9359455108642578
            },
            "rot": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            },
            "_delay": 0.0,
            "_radius": 0.0,
            "_velocity": 0.0,
            "_acceleration": 0.0,
            "_wait": 0.5,
            "_parentStepIdx": 0,
            "_useProcessMode": False,
            "_individualVelocityAcceleration": False,
            "_useForceMode": False,
            "_useServoJMode": False,
            "_useSkipMove": True,
            "_setDigitalIO": False,
            "_setToolDigitalIO": False,
            "_setDigitalIONumber": 0,
            "_setToolDigitalIONumber": 0,
            "_setDigitalIOValue": False,
            "_setToolDigitalIOValue": False,
            "_setCapability": False,
            "_setCapabilityName": "",
            "_setCapabilityType": "",
            "_setCapabilityValue": False,
            "_setCapabilityIOType": "",
            "_randomizedOffset": False,
            "_randomizedOffsetRadiusCM": 5.0
        }, {
            "_tipInputIdx": -1,
            "_parentType": 0,
            "pos": {
                "x": 3.5145723819732666,
                "y": -2.0607705116271973,
                "z": -0.9359455108642578
            },
            "rot": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            },
            "_delay": 0.0,
            "_radius": 0.0,
            "_velocity": 0.0,
            "_acceleration": 0.0,
            "_wait": 0.5,
            "_parentStepIdx": 0,
            "_useProcessMode": False,
            "_individualVelocityAcceleration": False,
            "_useForceMode": False,
            "_useServoJMode": False,
            "_useSkipMove": True,
            "_setDigitalIO": False,
            "_setToolDigitalIO": False,
            "_setDigitalIONumber": 0,
            "_setToolDigitalIONumber": 0,
            "_setDigitalIOValue": False,
            "_setToolDigitalIOValue": False,
            "_setCapability": False,
            "_setCapabilityName": "",
            "_setCapabilityType": "",
            "_setCapabilityValue": False,
            "_setCapabilityIOType": "",
            "_randomizedOffset": False,
            "_randomizedOffsetRadiusCM": 5.0
        }, {
            "_tipInputIdx": -1,
            "_parentType": 0,
            "pos": {
                "x": 3.5145723819732666,
                "y": -2.0607705116271973,
                "z": -0.9359455108642578
            },
            "rot": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            },
            "_delay": 0.0,
            "_radius": 0.0,
            "_velocity": 0.0,
            "_acceleration": 0.0,
            "_wait": 0.5,
            "_parentStepIdx": 0,
            "_useProcessMode": False,
            "_individualVelocityAcceleration": False,
            "_useForceMode": False,
            "_useServoJMode": False,
            "_useSkipMove": True,
            "_setDigitalIO": False,
            "_setToolDigitalIO": False,
            "_setDigitalIONumber": 0,
            "_setToolDigitalIONumber": 0,
            "_setDigitalIOValue": False,
            "_setToolDigitalIOValue": False,
            "_setCapability": False,
            "_setCapabilityName": "",
            "_setCapabilityType": "",
            "_setCapabilityValue": False,
            "_setCapabilityIOType": "",
            "_randomizedOffset": False,
            "_randomizedOffsetRadiusCM": 5.0
        }],
        "Preconditions": [],
        "TIPInputs": [{
            "Name": "Torus0",
            "TIPObjectType": "Torus",
            "PickData": {
                "label": "",
                "depthTS": 0,
                "pose2D": {
                    "x": 0.0,
                    "y": 0.0
                },
                "position3D": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0
                },
                "quaternion3D": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0,
                    "w": 0.0
                },
                "tags": [],
                "userTS": 0,
                "deviceType": "",
                "deviceName": ""
            },
            "Dimensions": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0
            },
            "Padding": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "TIPPos": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0
            },
            "TIPRot": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            },
            "LocalGOPos": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0
            },
            "LocalGORot": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            }
        }],
        "Name": "ActionEditorv2TestAction",
        "Softstart": True,
        "SoftstartAccel": 1.0,
        "SoftstartVelocity": 1.0,
        "_maxAccel": 0.20000000298023224,
        "_maxVelocity": 0.20000000298023224,
        "_cyclic": True,
        "_taskIntent": "",
        "_intent": "",
        "_successType": "",
        "_captureDepthBehavior": "none",
        "_loop": False
    }, {
        "_steps": [{
            "_tipInputIdx": 0,
            "_parentType": 1,
            "pos": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0
            },
            "rot": {
                "x": 0.0,
                "y": 0.0,
                "z": -3.7252894102834944e-09,
                "w": 1.0
            },
            "_delay": 0.0,
            "_radius": 0.0,
            "_velocity": 0.0,
            "_acceleration": 0.0,
            "_wait": 0.0,
            "_parentStepIdx": -1,
            "_useProcessMode": False,
            "_individualVelocityAcceleration": False,
            "_useForceMode": False,
            "_useServoJMode": False,
            "_useSkipMove": False,
            "_setDigitalIO": False,
            "_setToolDigitalIO": False,
            "_setDigitalIONumber": 0,
            "_setToolDigitalIONumber": 0,
            "_setDigitalIOValue": False,
            "_setToolDigitalIOValue": False,
            "_setCapability": False,
            "_setCapabilityName": "",
            "_setCapabilityType": "",
            "_setCapabilityValue": False,
            "_setCapabilityIOType": "",
            "_randomizedOffset": False,
            "_randomizedOffsetRadiusCM": 5.0
        }],
        "Preconditions": [],
        "TIPInputs": [{
            "Name": "Torus0",
            "TIPObjectType": "Torus",
            "PickData": {
                "label": "",
                "depthTS": 0,
                "pose2D": {
                    "x": 0.0,
                    "y": 0.0
                },
                "position3D": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0
                },
                "quaternion3D": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0,
                    "w": 0.0
                },
                "tags": [],
                "userTS": 0,
                "deviceType": "",
                "deviceName": ""
            },
            "Dimensions": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0
            },
            "Padding": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "TIPPos": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0
            },
            "TIPRot": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            },
            "LocalGOPos": {
                "x": -0.15814289450645447,
                "y": 0.322115957736969,
                "z": 0.6822412014007568
            },
            "LocalGORot": {
                "x": 0.05359622463583946,
                "y": -0.8026307821273804,
                "z": -0.5566185712814331,
                "w": -0.20757442712783813
            }
        }],
        "Name": "MoveTo",
        "Softstart": True,
        "SoftstartAccel": 1.0,
        "SoftstartVelocity": 1.0,
        "_maxAccel": 0.20000000298023224,
        "_maxVelocity": 0.20000000298023224,
        "_cyclic": True,
        "_taskIntent": "",
        "_intent": "other",
        "_successType": "other",
        "_captureDepthBehavior": "none",
        "_loop": False
    }, {
        "_steps": [{
            "_tipInputIdx": 0,
            "_parentType": 1,
            "pos": {
                "x": -3.0494604110717773,
                "y": -0.00035781413316726685,
                "z": 0.22043925523757935
            },
            "rot": {
                "x": -0.0011294931173324585,
                "y": 0.07471251487731934,
                "z": -0.01551392674446106,
                "w": 0.997083842754364
            },
            "_delay": 0.0,
            "_radius": 0.0,
            "_velocity": 0.0,
            "_acceleration": 0.0,
            "_wait": 0.0,
            "_parentStepIdx": -1,
            "_useProcessMode": False,
            "_individualVelocityAcceleration": False,
            "_useForceMode": False,
            "_useServoJMode": False,
            "_useSkipMove": False,
            "_setDigitalIO": False,
            "_setToolDigitalIO": False,
            "_setDigitalIONumber": 0,
            "_setToolDigitalIONumber": 0,
            "_setDigitalIOValue": False,
            "_setToolDigitalIOValue": False,
            "_setCapability": True,
            "_setCapabilityName": "",
            "_setCapabilityType": "vacuum",
            "_setCapabilityValue": True,
            "_setCapabilityIOType": "DigitalOutput",
            "_randomizedOffset": False,
            "_randomizedOffsetRadiusCM": 5.0
        }, {
            "_tipInputIdx": -1,
            "_parentType": 0,
            "pos": {
                "x": 0.21285633742809296,
                "y": 0.2875767946243286,
                "z": 0.3596976399421692
            },
            "rot": {
                "x": 0.6918290257453918,
                "y": 0.7147566080093384,
                "z": 0.07859083265066147,
                "w": 0.0657198429107666
            },
            "_delay": 0.0,
            "_radius": 0.0,
            "_velocity": 0.0,
            "_acceleration": 0.0,
            "_wait": 0.699999988079071,
            "_parentStepIdx": -1,
            "_useProcessMode": False,
            "_individualVelocityAcceleration": False,
            "_useForceMode": False,
            "_useServoJMode": False,
            "_useSkipMove": False,
            "_setDigitalIO": False,
            "_setToolDigitalIO": False,
            "_setDigitalIONumber": 0,
            "_setToolDigitalIONumber": 0,
            "_setDigitalIOValue": False,
            "_setToolDigitalIOValue": False,
            "_setCapability": True,
            "_setCapabilityName": "",
            "_setCapabilityType": "vacuum",
            "_setCapabilityValue": False,
            "_setCapabilityIOType": "DigitalOutput",
            "_randomizedOffset": False,
            "_randomizedOffsetRadiusCM": 5.0
        }],
        "Preconditions": [],
        "TIPInputs": [{
            "Name": "Torus0",
            "TIPObjectType": "Torus",
            "PickData": {
                "label": "",
                "depthTS": 0,
                "pose2D": {
                    "x": 0.0,
                    "y": 0.0
                },
                "position3D": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0
                },
                "quaternion3D": {
                    "x": 0.0,
                    "y": 0.0,
                    "z": 0.0,
                    "w": 0.0
                },
                "tags": [],
                "userTS": 0,
                "deviceType": "",
                "deviceName": ""
            },
            "Dimensions": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0
            },
            "Padding": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "TIPPos": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0
            },
            "TIPRot": {
                "x": 0.0,
                "y": 0.0,
                "z": 0.0,
                "w": 1.0
            },
            "LocalGOPos": {
                "x": 0.4116259515285492,
                "y": 0.26271939277648926,
                "z": 0.46455642580986023
            },
            "LocalGORot": {
                "x": 0.5184661149978638,
                "y": -0.5769169330596924,
                "z": -0.47576385736465454,
                "w": 0.41473910212516785
            }
        }],
        "Name": "NewAction0",
        "Softstart": False,
        "SoftstartAccel": 1.0,
        "SoftstartVelocity": 1.0,
        "_maxAccel": 0.20000000298023224,
        "_maxVelocity": 0.20000000298023224,
        "_cyclic": True,
        "_taskIntent": "",
        "_intent": "other",
        "_successType": "other",
        "_captureDepthBehavior": "none",
        "_loop": False
    }]

    actions_string = json.dumps(
        actions_dict, indent=None, separators=(",", ":"))
    value_dict["actions"] = actions_string
    value = json.dumps(value_dict, indent=None, separators=(",", ":"))

    self._on_data(
        types_gen.DeviceData(
            device_type="settings-engine",
            data_type="key-value",
            key="actionsets.json",
            value=value))

    devices_dict2: Dict[str, Any] = {
        "devices": [
            {
                "deviceName": "LeftBin",
                "deviceType": "object",
                "parameters": {
                    "geometry": {
                        "type":
                            "composite",
                        "subtype":
                            "bin",
                        "position": {
                            "x": 0.33225405216217,
                            "y": 0.575307250022888,
                            "z": -0.292910367250443,
                        },
                        "rotation": {
                            "rx": 359.650665283203,
                            "ry": 1.17114853858948,
                            "rz": 359.381958007813,
                        },
                        "geometries": [
                            {
                                "type": "box",
                                "scale": {
                                    "x": 0.375705718994141,
                                    "y": 0.618938982486725,
                                    "z": 0.00573757430538535,
                                },
                                "position": {
                                    "x": 2.68919393420219e-08,
                                    "y": -3.69327608495951e-08,
                                    "z": -0.0506818853318691,
                                },
                                "rotation": {
                                    "rx": 3.09492907035747e-06,
                                    "ry": -1.24856114780414e-07,
                                    "rz": -1.70754708506138e-06,
                                },
                            },
                            {
                                "type": "box",
                                "scale": {
                                    "x": 0.375705391168594,
                                    "y": 0.0424835309386253,
                                    "z": 0.107101395726204,
                                },
                                "position": {
                                    "x": 1.97906047105789e-08,
                                    "y": -0.292893022298813,
                                    "z": -6.28642737865448e-09,
                                },
                                "rotation": {
                                    "rx": 0,
                                    "ry": -2.35538113457778e-08,
                                    "rz": 0
                                },
                            },
                            {
                                "type": "box",
                                "scale": {
                                    "x": 0.375705391168594,
                                    "y": 0.0424835309386253,
                                    "z": 0.107101395726204,
                                },
                                "position": {
                                    "x": 6.98491930961609e-10,
                                    "y": 0.29289111495018,
                                    "z": -5.355104804039e-09,
                                },
                                "rotation": {
                                    "rx": 0,
                                    "ry": -2.35538113457778e-08,
                                    "rz": 0
                                },
                            },
                            {
                                "type": "box",
                                "scale": {
                                    "x": 0.0257876738905907,
                                    "y": 0.618938982486725,
                                    "z": 0.107101395726204,
                                },
                                "position": {
                                    "x": -0.177791059017181,
                                    "y": -1.00098986877128e-08,
                                    "z": -1.46337697515264e-07,
                                },
                                "rotation": {
                                    "rx": 0,
                                    "ry": -2.35538113457778e-08,
                                    "rz": 0
                                },
                            },
                            {
                                "type": "box",
                                "scale": {
                                    "x": 0.0257876738905907,
                                    "y": 0.618938982486725,
                                    "z": 0.107101395726204,
                                },
                                "position": {
                                    "x": 0.177790433168411,
                                    "y": 3.37422534357756e-09,
                                    "z": 1.33532012114301e-07,
                                },
                                "rotation": {
                                    "rx": 0,
                                    "ry": -2.35538113457778e-08,
                                    "rz": 0
                                },
                            },
                        ],
                    },
                },
            },
            {
                "deviceName": "RightBin",
                "deviceType": "object",
                "parameters": {
                    "geometry": {
                        "type":
                            "composite",
                        "subtype":
                            "bin",
                        "position": {
                            "x": -0.106909163296223,
                            "y": 0.584619164466858,
                            "z": -0.287746667861938,
                        },
                        "rotation": {
                            "rx": 1.01034247875214,
                            "ry": 359.715270996094,
                            "rz": 181.956497192383,
                        },
                        "geometries": [
                            {
                                "type": "box",
                                "scale": {
                                    "x": 0.347373127937317,
                                    "y": 0.574085354804993,
                                    "z": 0.0383999310433865,
                                },
                                "position": {
                                    "x": -2.47382558882236e-09,
                                    "y": 2.1420419216156e-08,
                                    "z": -0.0583758279681206,
                                },
                                "rotation": {
                                    "rx": 3.09826418742887e-06,
                                    "ry": -1.06721742554328e-07,
                                    "rz": -1.70754708506138e-06,
                                },
                            },
                            {
                                "type": "box",
                                "scale": {
                                    "x": 0.347373127937317,
                                    "y": 0.0384010598063469,
                                    "z": 0.116752542555332,
                                },
                                "position": {
                                    "x": -6.51925802230835e-09,
                                    "y": -0.287031382322311,
                                    "z": -1.2572854757309e-07,
                                },
                                "rotation": {
                                    "rx": -8.33763225127626e-10,
                                    "ry": -5.33608464081681e-08,
                                    "rz": 3.88251205023995e-19,
                                },
                            },
                            {
                                "type": "box",
                                "scale": {
                                    "x": 0.347373127937317,
                                    "y": 0.0384010598063469,
                                    "z": 0.116752542555332,
                                },
                                "position": {
                                    "x": 5.12227416038513e-08,
                                    "y": 0.287032693624496,
                                    "z": 1.49011611938477e-07,
                                },
                                "rotation": {
                                    "rx": -8.33763225127626e-10,
                                    "ry": -5.33608464081681e-08,
                                    "rz": 3.88251205023995e-19,
                                },
                            },
                            {
                                "type": "box",
                                "scale": {
                                    "x": 0.0384011939167976,
                                    "y": 0.574085354804993,
                                    "z": 0.116752542555332,
                                },
                                "position": {
                                    "x": -0.173682510852814,
                                    "y": 2.70083546638489e-08,
                                    "z": -3.49973561242223e-08,
                                },
                                "rotation": {
                                    "rx": -8.33763225127626e-10,
                                    "ry": -5.33608464081681e-08,
                                    "rz": 3.88251205023995e-19,
                                },
                            },
                            {
                                "type": "box",
                                "scale": {
                                    "x": 0.0384011939167976,
                                    "y": 0.574085354804993,
                                    "z": 0.116752542555332,
                                },
                                "position": {
                                    "x": 0.1736830919981,
                                    "y": -4.74974513053894e-08,
                                    "z": 3.79077391698956e-08,
                                },
                                "rotation": {
                                    "rx": -8.33763225127626e-10,
                                    "ry": -5.33608464081681e-08,
                                    "rz": 3.88251205023995e-19,
                                },
                            },
                        ],
                    },
                },
            },
            {
                "deviceName": "RBin",
                "deviceType": "interactable",
                "parameters": {
                    "geometry": {
                        "type": "box",
                        "scale": {
                            "x": 0.370000004768372,
                            "y": 0.550000011920929,
                            "z": 0.200000002980232,
                        },
                        "position": {
                            "x": -0.110589988529682,
                            "y": 0.566380798816681,
                            "z": -0.270000010728836,
                        },
                        "rotation": {
                            "rx": 0,
                            "ry": 0,
                            "rz": 0
                        },
                    },
                },
            },
            {
                "deviceName": "LBin",
                "deviceType": "interactable",
                "parameters": {
                    "geometry": {
                        "type": "box",
                        "scale": {
                            "x": 0.349999994039536,
                            "y": 0.600000023841858,
                            "z": 0.200000002980232,
                        },
                        "position": {
                            "x": 0.327026665210724,
                            "y": 0.58566826581955,
                            "z": -0.263078659772873,
                        },
                        "rotation": {
                            "rx": 0,
                            "ry": 0,
                            "rz": 0
                        },
                    },
                },
            },
        ],
        "version": 20200213,
    }
    geometry_json: str = json.dumps(devices_dict2)

    settings_engine_dict: Dict[str, Any] = {
        "created": "2020-10-12T21:56:02Z",
        "createdBy": "DKIUBvatSwMgUl05tH4KpmL7LF72",
        "geometry": geometry_json,
        "version": 20200213,
    }
    settings_engine_json = json.dumps(settings_engine_dict)

    self._on_data(
        types_gen.DeviceData(
            device_type="settings-engine",
            data_type="key-value",
            key="workcell_constraints.json",
            value=settings_engine_json))

    value = ("{"
             "\"Proto\":"
             "\"ChoKBnZhY3V1bRoCdXIoAjoKEghzdGFuZGFyZAolCg92YWN1dW0tcHJlc3N1c"
             "mUaAnVyKAE6DBIIc3RhbmRhcmQgAwogCgx2YWN1dW0tZ2F1Z2UaAnVyKAM6ChII"
             "c3RhbmRhcmQSCHN0YW5kYXJkEgxjb25maWd1cmFibGUSBHRvb2waDgoIc3RhbmR"
             "hcmQQASAHGg4KCHN0YW5kYXJkEAIgBxoSCgxjb25maWd1cmFibGUQASAHGhIKDG"
             "NvbmZpZ3VyYWJsZRACIAcaDgoIc3RhbmRhcmQQAyABGg4KCHN0YW5kYXJkEAQgA"
             "RoKCgR0b29sEAEgARoKCgR0b29sEAIgARoKCgR0b29sEAMgASIhChp2YWN1dW0t"
             "Z2F1Z2UtbWluLXRocmVzaG9sZB0AAPpEIhwKFXF1YWxpdHktbWluLXRocmVzaG9"
             "sZB0zMzM/IiIKG3NlbnNvci1oZWFsdGgtbWluLXRocmVzaG9sZB0zMzM/\","
             "\"created\":\"2020-12-01T02:06:23.684718Z\","
             "\"createdBy\":\"ytkj76DHYZbsjBVPObfm6dA8rPx1\""
             "}")
    self._on_data(
        types_gen.DeviceData(
            device_type="settings-engine",
            data_type="key-value",
            key="workcell_io.json",
            value=value))

  def _on_data(self, data: types_gen.DeviceData) -> None:
    if data.data_type == "key-value":
      self._key_values[device_base.KeyValueKey(
          device_type=data.device_type,
          device_name=data.device_name,
          key=data.key)] = data.value
    self._queue.put(data)
    protoloop = types_gen.DeviceData.from_proto(
        logs_pb2.DeviceData.FromString(  # type: ignore
            data.to_proto().SerializeToString()))  # type: ignore
    assert protoloop is not None
    assert data.to_json() == protoloop.to_json()

  def send_cmd(self, cmd: types_gen.CommandData) -> None:
    protoloop = types_gen.CommandData.from_proto(
        logs_pb2.CommandData.FromString(  # type: ignore
            cmd.to_proto().SerializeToString()))  # type: ignore
    assert protoloop is not None
    assert cmd.to_json() == protoloop.to_json()
    with self._lock:
      if cmd.data_type == "key-value-request":
        value = self._key_values.get(
            device_base.KeyValueKey(
                device_type=cmd.device_type,
                device_name=cmd.device_name,
                key=cmd.key), None)
        if value is not None:
          self._on_data(
              types_gen.DeviceData(
                  ts=cmd.ts,
                  tag=cmd.tag,
                  device_type=cmd.device_type,
                  device_name=cmd.device_name,
                  data_type="key-value",
                  key=cmd.key,
                  value=value))
      for responder in self._responders:
        for data in responder.step(cmd):
          self._on_data(data)

  def get_queue(self) -> "queue.Queue[Optional[types_gen.DeviceData]]":
    return self._queue

  def __enter__(self) -> "TestClient":
    return self

  def __exit__(self, typ: Any, value: Any, traceback: Any) -> None:
    self.close()

  def close(self) -> None:
    with self._lock:
      if not self._closed:
        self._closed = True
        self._queue.put(None)
    if self._data_downloader:
      self._data_downloader.close()


class TestDevice:
  """TestDevice wraps a device for testing purposes."""
  _data_downloader: _DataDownloader
  _cmds: List[types_gen.CommandData]
  _device: device_base.DeviceBase
  _callback: Tuple[Optional[Callable[[types_gen.CommandData],
                                     List[types_gen.DeviceData]]]]
  _tag_map: Dict[str, str]

  def __init__(self,
               device: device_base.DeviceBase,
               test_image_dir: str = "") -> None:
    """Initialize the TestDevice.

    Args:
      device: the DeviceBase to test.
      test_image_dir: the test device directory.
    """
    self._data_downloader = _DataDownloader(test_image_dir)
    self._device = device
    self._cmds = []
    self._callback = (None,)
    self._tag_map = {}
    device.set_send_cmd(self.send_cmd)

  def set_callback(
      self, callback: Optional[Callable[[types_gen.CommandData],
                                        List[types_gen.DeviceData]]]
  ) -> None:
    """Set the callback for generated commands.

    Args:
      callback: the callback.
    """
    self._callback = (callback,)

  def set_responder(self, responder: TestResponder) -> None:
    """Set the callback for generated commands to be a Responder.

    Args:
      responder: the Responder.
    """
    if self._data_downloader:
      responder.set_test_image_dir(self._data_downloader.test_image_dir)
    for msg in responder.start():
      protoloop = types_gen.DeviceData.from_proto(
          logs_pb2.DeviceData.FromString(  # type: ignore
              msg.to_proto().SerializeToString()))  # type: ignore
      assert protoloop is not None
      assert msg.to_json() == protoloop.to_json()
      self._device.sync_device_data(msg)
    self.set_callback(responder.step)

  def send_cmd(self, cmd: types_gen.CommandData) -> None:
    """Send a command data to the responder or callback.

    Args:
      cmd: the command data to send.
    """
    protoloop_cmd = types_gen.CommandData.from_proto(
        logs_pb2.CommandData.FromString(  # type: ignore
            cmd.to_proto().SerializeToString()))  # type: ignore
    assert protoloop_cmd is not None
    assert cmd.to_json() == protoloop_cmd.to_json()
    self._cmds.append(cmd)
    if cmd.tag:
      self._tag_map[cmd.tag] = "tag-%d" % (len(self._tag_map) + 1,)
    if self._callback[0] is not None:
      for msg in self._callback[0](cmd):
        protoloop = types_gen.DeviceData.from_proto(
            logs_pb2.DeviceData.FromString(  # type: ignore
                msg.to_proto().SerializeToString()))  # type: ignore
        assert protoloop is not None
        assert msg.to_json() == protoloop.to_json()
        self._device.sync_device_data(msg)

  def expect_command_data(self,
                          expect_cmds: List[types_gen.CommandData]) -> None:
    """Set the callback for generated commands to be a Responder.

    Args:
      expect_cmds: the expected command response.
    """
    cmds = self._cmds
    self._cmds = []
    assert len(cmds) == len(expect_cmds), (
        f"Expected {len(expect_cmds)}  commands, got {len(cmds)}")
    for cmd, expect_cmd in zip(cmds, expect_cmds):
      protoloop = types_gen.CommandData.from_proto(
          logs_pb2.CommandData.FromString(  # type: ignore
              cmd.to_proto().SerializeToString()))  # type: ignore
      assert protoloop is not None
      assert cmd.to_json() == protoloop.to_json()
      protoloop = types_gen.CommandData.from_proto(
          logs_pb2.CommandData.FromString(  # type: ignore
              expect_cmd.to_proto().SerializeToString()))  # type: ignore
      assert protoloop is not None
      assert expect_cmd.to_json() == protoloop.to_json()
      cmd_json = cmd.to_json()
      if "ts" in cmd_json:
        del cmd_json["ts"]
      if "tag" in cmd_json:
        cmd_json["tag"] = self._tag_map.get(cmd_json["tag"], "invalid-tag")
      expect_cmd_json = expect_cmd.to_json()
      if "ts" in expect_cmd_json:
        del expect_cmd_json["ts"]
      cmd_str = json.dumps(cmd_json)
      expect_cmd_str = json.dumps(expect_cmd_json)
      assert cmd_str == expect_cmd_str, (
          f"Invalid command, expected {expect_cmd_str} got {cmd_str}")

  def close(self) -> None:
    """Close the device."""
    self._device.close()
    if self._data_downloader:
      self._data_downloader.close()

  def __enter__(self) -> "TestDevice":
    self._device.start()
    return self

  def __exit__(self, typ: Any, value: Any, traceback: Any) -> None:
    self.close()
