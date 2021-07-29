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

"""User land driver for the spacemouse device.

This program iterates through all the USB devices, printing out their VID
and PIDs. If it finds a 3DConnexion device, it will say so! And if it finds a
SpaceNavigator, it will connect and wait for you to start moving the mouse or
pressing buttons.

# VID and PID from https://3dconnexion.com/faq/27
"""
import binascii
import logging
import multiprocessing as mp
import queue
import time
from typing import Any, List, Optional, Tuple

# Try importing usb1. But don't crash if the library is not installed.
try:
  # pylint:disable=g-import-not-at-top
  import usb1  # type: ignore
  _have_usb = True
except ModuleNotFoundError:
  _have_usb = False

_VID_3DCONNEXION_OLD = 0x046D  # From when 3DConnexion was a Logitech division
_VID_3DCONNEXION = 0x256F

_ALL_THE_3DCONNEXION_THINGS = [
    {
        "pid": 0xC62E,
        "name": "SpaceMouse Wireless Receiver (Cabled)"
    },
    {
        "pid": 0xC62F,
        "name": "SpaceMouse Wireless Receiver"
    },
    {
        "pid": 0xC631,
        "name": "SpaceMouse Pro Wireless Receiver (Cabled)"
    },
    {
        "pid": 0xC632,
        "name": "SpaceMouse Pro Wireless Receiver"
    },
    {
        "pid": 0xC633,
        "name": "SpaceMouse Enterprise"
    },
    {
        "pid": 0xC635,
        "name": "SpaceMouse Compact"
    },
    {
        "pid": 0xC650,
        "name": "CadMouse"
    },
    {
        "pid": 0xC651,
        "name": "CadMouse Wireless"
    },
    {
        "pid": 0xC652,
        "name": "Universal Receiver"
    },
    {
        "pid": 0xC654,
        "name": "CadMouse Pro Wireless"
    },
    {
        "pid": 0xC657,
        "name": "CadMouse Pro Wireless Left"
    },
]

_ALL_THE_LOGITECH_THINGS = [
    {
        "pid": 0xC603,
        "name": "SpaceMouse Plus USB"
    },
    {
        "pid": 0xC605,
        "name": "CadMan"
    },
    {
        "pid": 0xC606,
        "name": "SpaceMouse Classic USB"
    },
    {
        "pid": 0xC623,
        "name": "SpaceBall 5000 USB"
    },
    {
        "pid": 0xC623,
        "name": "SpaceTraveler"
    },
    {
        "pid": 0xC625,
        "name": "SpacePilot"
    },
    {
        "pid": 0xC626,
        "name": "SpaceNavigator",
        "leds": [0x08, 0x4B]
    },
    {
        "pid": 0xC627,
        "name": "SpaceExplorer"
    },
    {
        "pid": 0xC628,
        "name": "SpaceNavigator For Notebooks"
    },
    {
        "pid": 0xC629,
        "name": "SpacePilot Pro"
    },
    {
        "pid": 0xC62B,
        "name": "SpaceMouse Pro"
    },
]


def _show_info(handle: "usb1.USBDeviceHandle") -> None:
  manufacturer = handle.getManufacturer()
  name = handle.getProduct()
  sn = handle.getSerialNumber()
  print(f"  {manufacturer} {name}: S/N {sn}")


def _show_device_info(device: "usb1.USBDevice") -> None:
  """Print the information of a USB device.

  Args:
    device: the USB device.
  """
  print(f"  == {device}")
  print(f"  Num configurations: {device.getNumConfigurations()}")
  for c in device.iterConfiguations():
    print(f" Configuration value {c.getConfigurationValue()}")
    print(f"   Number of interfaces {c.getNumInterfaces()}")
    for i in c:
      print(f"    Number of settings: {i.getNumSettings()}")
      for s in i:
        print(f"      Setting number {s.getNumber()}")
        print(f"      Number of endpoints {s.getNumEndpoints()}")
        print(f"      Class/Subclass: {s.getClass()}/{s.getSubClass()}")
        hid_data = s.getExtra()
        print(f"      HID num extra descriptors: {len(hid_data)}")
        # The data is a standard USB descriptor:
        # bLength: 09
        # bDescriptorType: 21 (HID)
        # bcdHID: 1.11
        # bCountryCode: 0
        # bDescriptorType[0]: 22 (HID)
        # wDescriptorLength[0]: 00D9 (217)
        print(f"      Data: {binascii.hexlify(hid_data[0]).decode('utf-8')}")


def _to_int_16(data: bytes) -> int:
  # Little endian
  x = (data[1] << 8) | data[0]
  if x > 0x7FFF:
    return x - 0x10000
  return x


RSPNAV_EVENT_ANY = 0
RSPNAV_EVENT_MOTION = 1
RSPNAV_EVENT_BUTTON = 2

_rspnav_qs: List["queue.Queue[RSpnavEvent]"] = []
_rspnav_processes = []


class RSpnavEvent(object):
  """A spacemouse event."""

  def __init__(self, device: int, ev_type: int) -> None:
    """A spacemouse event.

    Args:
      device: the device id.
      ev_type: the event type, RSPNAV_EVENT_MOTION or RSPNAV_EVENT_BUTTON.
    """
    self.device: int = device
    self.ev_type: int = ev_type


class RSpnavButtonEvent(RSpnavEvent):
  """Button event."""

  def __init__(self, device: int, bnum: int, press: bool) -> None:
    """Returns a new RspnavButtonEvent.

    Args:
      device: the USB device.
      bnum: the button number (0, 1, ...).
      press: True if the button was pressed, False if released.
    """
    super().__init__(device, RSPNAV_EVENT_BUTTON)
    self.bnum: int = bnum
    self.press: bool = press


class RSpnavMotionEvent(RSpnavEvent):
  """A motion event."""

  def __init__(self, device: int, translation: Tuple[int, int, int],
               rotation: Tuple[int, int, int], period: Any) -> None:
    """A motion event.

    Args:
      device: the USB device.
      translation: 3-tuple of translation force ints (Y, Z, X)
      rotation: 3-tuple of rotation torque ints (Ry, Rz, Rx)
      period: is unknown, and is present only for compatibility with spnav.
    """
    super().__init__(device, RSPNAV_EVENT_MOTION)
    # +Y is towards the mouse cable, and +Z is up.
    # Counterintuitively, translation and rotation are X Y Z.
    self.translation: Tuple[int, int, int] = (translation[0], translation[1],
                                              translation[2])
    self.rotation: Tuple[int, int,
                         int] = (rotation[0], rotation[1], rotation[2])
    self.period: Any = period


def _rspnav_hexdump(bs: bytes) -> str:
  hex_string = str(binascii.hexlify(bs), "ascii")
  return " ".join(hex_string[i:i + 2] for i in range(0, len(hex_string), 2))


def _scan_for_spnav() -> List[int]:
  """Scans USB devices.

  Returns:
    The list of ids for the discovered USB devices.
  """
  found: List[int] = []

  if not _have_usb:
    return found

  with usb1.USBContext() as context:
    devices = context.getDeviceList()
    i = 0
    for device in devices:
      vid = device.getVendorID()
      pid = device.getProductID()
      print(f"VID {vid:04X} PID {pid:04X}")

      if vid == _VID_3DCONNEXION_OLD:
        for d in _ALL_THE_LOGITECH_THINGS:
          if d["pid"] == pid:
            name = d["name"]
            print(f"    it's a {name}")
      if vid == _VID_3DCONNEXION:
        for d in _ALL_THE_3DCONNEXION_THINGS:
          if d["pid"] == pid:
            name = d["name"]
            print(f"    it's a {name}")
      # Make sure cabled takes precedence over universal receiver so that
      # the universal receiver can be kept plugged in while using the cabled
      # version.
      if vid == _VID_3DCONNEXION and pid == 0xC635:
        # SpaceMouse Compact
        found.append(i)
      elif vid == _VID_3DCONNEXION and pid == 0xC62E:
        # SpaceMouse Wireless (Cabled)
        found.append(i)
      elif vid == _VID_3DCONNEXION and pid == 0xC652:
        # Universal Receiver
        found.append(i)
      elif vid == _VID_3DCONNEXION_OLD and pid == 0xC626:
        # SpaceNavigator
        found.append(i)
      i += 1
  return found


def _interpret_space_navigator(device_num: int, handle: "usb1.USBDeviceHandle",
                               event_queue: "queue.Queue[RSpnavEvent]") -> None:
  """Processing space navigator events.

  This functions loops on the provided USB device handle, reads and enqueues
  every event.

  Args:
    device_num: the USB device id.
    handle: the handle to the USB device.
    event_queue: spacemouse event queue.
  """
  last_buttons = 0
  last_translate = None
  last_rotate = None
  num_buttons = 2

  while True:
    data = handle.interruptRead(1, 16)  # endpoint and length, no timeout
    logging.debug(_rspnav_hexdump(data))
    if data[0] == 0x01:  # translate
      x = _to_int_16(data[1:])
      y = -_to_int_16(data[3:])
      z = -_to_int_16(data[5:])
      # print(f"X {x} Y {y} Z {z}")
      last_translate = (x, y, z)
      if last_rotate is not None:
        event_queue.put(
            RSpnavMotionEvent(device_num, last_translate, last_rotate, 0))
    elif data[0] == 0x02:  # rotate
      x = _to_int_16(data[1:])
      y = -_to_int_16(data[3:])
      z = -_to_int_16(data[5:])
      # print(f"RX {x} RY {y} RZ {z}")
      last_rotate = (x, y, z)
      if last_translate is not None:
        event_queue.put(
            RSpnavMotionEvent(device_num, last_translate, last_rotate, 0))
    elif data[0] == 0x03:  # buttons
      press_mask = _to_int_16(data[1:])
      # print(f"Button mask {press_mask:02X}")
      for i in range(num_buttons):
        bit = press_mask & (1 << i)
        if bit != (last_buttons & (1 << i)):
          event_queue.put(RSpnavButtonEvent(device_num, i, bit != 0))
      last_buttons = press_mask
    else:
      print(f"  unknown event: {_rspnav_hexdump(data)}")


def _interpret_space_mouse_wireless(
    device_num: int, handle: "usb1.USBDeviceHandle", endpoint: int,
    event_queue: "queue.Queue[RSpnavEvent]") -> None:
  """Processing space mouse wireless events.

  This functions loops on the provided USB device handle, reads and enqueues
  every event.

  Args:
    device_num: the USB device id.
    handle: the handle to the USB device.
    endpoint: the end point number.
    event_queue: spacemouse event queue.
  """
  last_buttons = 0
  last_translate = None
  last_rotate = None
  num_buttons = 2

  while True:
    data = handle.interruptRead(endpoint, 16)  # endpoint and length, no timeout
    logging.debug(_rspnav_hexdump(data))
    if data[0] == 0x01:  # translate + rotate
      x = _to_int_16(data[1:])
      y = -_to_int_16(data[3:])
      z = -_to_int_16(data[5:])
      rx = _to_int_16(data[7:])
      ry = -_to_int_16(data[9:])
      rz = -_to_int_16(data[11:])
      # print(f"X {x} Y {y} Z {z} RX {rx} RY {ry} RZ {rz}")
      last_translate = (x, y, z)
      last_rotate = (rx, ry, rz)
      event_queue.put(
          RSpnavMotionEvent(device_num, last_translate, last_rotate, 0))
    elif data[0] == 0x03:  # buttons
      press_mask = _to_int_16(data[1:])
      # print(f"Button mask {press_mask:02X}")
      for i in range(num_buttons):
        bit = press_mask & (1 << i)
        if bit != (last_buttons & (1 << i)):
          event_queue.put(RSpnavButtonEvent(device_num, i, bit != 0))
      last_buttons = press_mask
    else:
      print(f"  unknown event: {_rspnav_hexdump(data)}")


def _start_rspnav(device_num: int, device_index: int,
                  event_queue: "queue.Queue[RSpnavEvent]") -> None:
  """Starting a space mouse device.

  Args:
    device_num: the device number.
    device_index: the device index.
    event_queue: event queue.
  """
  print(f"Starting for device {device_num} index {device_index}")
  with usb1.USBContext() as context:
    devices = context.getDeviceList()
    device = devices[device_index]

    vid = device.getVendorID()
    pid = device.getProductID()
    handle = device.open()
    if handle is None:
      print("ERROR: failed to open device")
      return
    _show_device_info(device)
    # _show_info(handle)
    if handle.kernelDriverActive(0):
      print("Detaching kernel driver")
      handle.detachKernelDriver(0)
    with handle.claimInterface(0):
      # We don't actually use this data. I kept it here because it could be
      # useful to look at the descriptor at some point.
      _ = handle.controlRead(
          usb1.RECIPIENT_INTERFACE,
          usb1.REQUEST_GET_DESCRIPTOR,
          usb1.DT_REPORT << 8,
          0,  # index
          300,  # max length
          5000,  # timeout (msec)
      )
      # Here's the real place we parse the data.
      # Make sure cabled takes precedence over universal receiver so that
      # the universal receiver can be kept plugged in while using the cabled
      # version.
      if vid == _VID_3DCONNEXION and pid == 0xC635:
        # SpaceMouse Compact
        _interpret_space_navigator(device_num, handle, event_queue)
      elif vid == _VID_3DCONNEXION and pid == 0xC65E:
        # SpaceMouse Wireless Cabled
        _interpret_space_mouse_wireless(device_num, handle, 3, event_queue)
      elif vid == _VID_3DCONNEXION and pid == 0xC652:
        # Universal Receiver
        _interpret_space_mouse_wireless(device_num, handle, 1, event_queue)
      elif vid == _VID_3DCONNEXION_OLD and pid == 0xC626:
        # SpaceNavigator
        _interpret_space_navigator(device_num, handle, event_queue)
      else:
        print(f"ERROR: can't parse data for VID {vid:04X} PID {pid:04X}")
        return


def rspnav_open() -> None:
  """Scans for all Space Mice and starts up a queue for events.

  Raises:
    RSpnavConnectionException if connection cannot be established
  """
  global _rspnav_processes
  global _rspnav_qs

  devices = _scan_for_spnav()
  print(f"Found {len(devices)} Space Navigator devices")

  for i in range(len(devices)):
    _rspnav_qs.append(mp.Queue())
    _rspnav_processes.append(
        mp.Process(target=_start_rspnav, args=(
            i,
            devices[i],
            _rspnav_qs[i],
        )))
    _rspnav_processes[i].start()


def rspnav_howmany() -> int:
  """Returns the number of Space Mice found."""
  return len(_rspnav_qs)


# Keep the index of which queue we last polled, so that we can
# ensure round-robin when checking all the queues.
_poll_index = 0


def _get_poll_index() -> int:
  global _poll_index
  global _rspnav_qs

  i = _poll_index
  _poll_index = (_poll_index + 1) % len(_rspnav_qs)
  return i


def rspnav_wait_event() -> RSpnavEvent:
  """Blocks waiting for a Space Mouse event.

  Returns:
    An instance of SpnavMotionEvent or SpnavButtonEvent.
  """
  e = None
  while e is None:
    e = rspnav_poll_event()
    if e is None:
      time.sleep(0.001)
  return e


def rspnav_poll_event() -> Optional[RSpnavEvent]:
  """Polls for Space Navigator events.

  Returns:
    None if no waiting events, otherwise an instance of
    SpnavMotionEvent or SpnavButtonEvent.
  """
  global _rspnav_qs

  for _ in range(len(_rspnav_qs)):
    try:
      return _rspnav_qs[_get_poll_index()].get_nowait()
    except queue.Empty:
      pass
  return None


def rspnav_remove_events(unused_ev_type: int) -> None:
  """Removes pending Space Navigator events from all queues.

  Unlike the original spnav library, this call ignores the event type, instead
  removing ALL events.

  Args:
    unused_ev_type: event type
  """
  global _rspnav_qs

  for q in _rspnav_qs:
    try:
      while q.get_nowait() is not None:
        pass
    except queue.Empty:
      continue


def rspnav_kill() -> None:
  global _rspnav_processes
  for rspnav_process in _rspnav_processes:
    rspnav_process.kill()
  _rspnav_processes = []
