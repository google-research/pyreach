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
"""Constraints implementation."""

import json
import logging  # type: ignore
import math
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np  # type: ignore
from scipy.spatial import transform  # type: ignore
import shapely.geometry  # type: ignore

from pyreach import constraints
from pyreach import core
from pyreach.common.base import transform_util
from pyreach.impl import device_base


class ConstraintDevice:
  """A container for the device name and type."""

  _device_type: str
  _device_name: str

  def __init__(self, device_type: str, device_name: str) -> None:
    """Construct a constraint device.

    Args:
      device_type: The device type.
      device_name: The device name.
    """
    self._device_type = device_type
    self._device_name = device_name

  @property
  def device_type(self) -> str:
    """Get the device type."""
    return self._device_type

  @property
  def device_name(self) -> str:
    """Get the device name."""
    return self._device_name

  def __str__(self) -> str:
    """Return a string version of Device."""
    return "Device('" + self._device_type + "', '" + self._device_name + "')"


class BoxImpl(constraints.Box):
  """Represents a Box constraint geometry."""

  def get_position(self) -> List[float]:
    """Return the box center position."""
    return self.pose.position.as_list()

  def get_rotation(self) -> List[float]:
    """Return the axis/angle of the box."""
    return self.pose.orientation.axis_angle.as_list()

  def get_scale(self) -> List[float]:
    """Return the size of the box."""
    return self.scale.as_list()

  def get_vertices(self) -> List[np.array]:
    """Return the vertices of the box."""
    self._vertices = []
    self._vertices.append(
        np.array([-self.scale.x / 2, -self.scale.y / 2, -self.scale.z / 2],
                 dtype=np.float))
    self._vertices.append(
        np.array([-self.scale.x / 2, self.scale.y / 2, -self.scale.z / 2],
                 dtype=np.float))
    self._vertices.append(
        np.array([self.scale.x / 2, self.scale.y / 2, -self.scale.z / 2],
                 dtype=np.float))
    self._vertices.append(
        np.array([self.scale.x / 2, -self.scale.y / 2, -self.scale.z / 2],
                 dtype=np.float))
    self._vertices.append(
        np.array([-self.scale.x / 2, -self.scale.y / 2, self.scale.z / 2],
                 dtype=np.float))
    self._vertices.append(
        np.array([-self.scale.x / 2, self.scale.y / 2, self.scale.z / 2],
                 dtype=np.float))
    self._vertices.append(
        np.array([self.scale.x / 2, self.scale.y / 2, self.scale.z / 2],
                 dtype=np.float))
    self._vertices.append(
        np.array([self.scale.x / 2, -self.scale.y / 2, self.scale.z / 2],
                 dtype=np.float))
    self._vertices.append(np.array([0, 0, 0], dtype=np.float))
    rotation = transform.Rotation.from_euler(
        "zxy", np.array(self.get_rotation()), degrees=True).as_rotvec()
    for i in range(len(self._vertices)):
      self._vertices[i] = transform_util.transform(
          self._vertices[i], np.array(self.get_position()), rotation)
    return self._vertices

  @classmethod
  def from_json(cls, from_json: Dict[str,
                                     Any]) -> Optional[constraints.Geometry]:
    """Convert JSON into into a Constraints Box Geometry.

    Args:
      from_json: The JSON dictionary to extract the Box Geometry from.

    Returns:
      constraint geometry.
    """
    args: Dict[str, List[float]] = {"position": [], "rotation": [], "scale": []}
    for d, fvs in [("position", ["x", "y", "z"]),
                   ("rotation", ["rx", "ry", "rz"]), ("scale", ["x", "y",
                                                                "z"])]:
      if not isinstance(from_json.get(d, {}), dict):
        logging.warning("was not a dictionary in Box: %s, %s", d, from_json)
        return None
      for fv in fvs:
        a = from_json.get(d, {}).get(fv, 0.0)
        if not isinstance(a, (float, int)):
          logging.warning("value was not a float in Box: %s, %s, %s, %s", d, fv,
                          a, from_json)
          return None
        args[d].append(float(a))
      for fv in from_json.get(d, {}):
        if fv not in fvs:
          logging.warning("extra value in Box: %s, %s, %s", d, fv, from_json)
    for d in from_json:
      if d not in ["position", "rotation", "scale", "type"]:
        logging.warning("extra value in Box: %s, %s", d, from_json)
    rot = [x * math.pi / 180.0 for x in args["rotation"]]
    return BoxImpl(
        core.Pose(
            core.Translation.from_list(args["position"]),
            core.Rotation(
                core.AxisAngle.from_list(
                    transform_util.euler_to_axis_angle(*rot).tolist()))),
        core.Scale.from_list(args["scale"]))


class Plane(constraints.Geometry):
  """Represents a Plane constraint."""

  _d: float
  _x: float
  _y: float
  _z: float

  def __init__(self, d: float, x: float, y: float, z: float) -> None:
    """Init a Plane Geometry.

    Args:
      d: The distance between the origin and the plane along the normal.
      x: The plane normal x axis.
      y: The plane normal y axis.
      z: The plane normal z axis.
    """
    super().__init__()
    self._d = d
    self._x = x
    self._y = y
    self._z = z

  def get_d(self) -> float:
    """Return the plane distance."""
    return self._d

  def get_x(self) -> float:
    """Return the normal x value."""
    return self._x

  def get_y(self) -> float:
    """Return the normal y value."""
    return self._y

  def get_z(self) -> float:
    """Return the normal z value."""
    return self._z

  @classmethod
  def from_json(cls, from_json: Dict[str,
                                     Any]) -> Optional[constraints.Geometry]:
    """Extract the plane geometry from a JSON dictionary.

    Args:
      from_json: The JSON dictionary to extract Plane Geometry from.

    Returns:
      Returns PlaneGeometry on success and None otherwise.

    """
    args = [from_json.get("d", 0.0)]
    if not isinstance(from_json.get("d", 0.0), (float, int)):
      return None
    if not isinstance(from_json.get("n", {}), dict):
      return None
    for fv in ["x", "y", "z"]:
      a = from_json.get("n", {}).get(fv, 0.0)
      args.append(a)
      if not isinstance(a, (float, int)):
        return None
    for fv in from_json.get("n", {}):
      if fv not in ["x", "y", "z"]:
        logging.warning("extra value in Plane normal: %s %s", fv, from_json)
    for d in from_json:
      if d not in ["n", "d", "type"]:
        logging.warning("extra value in Plane: %s %s", d, from_json)
    return Plane(*args)  # pylint: disable=no-value-for-parameter


class Composite(constraints.Geometry):
  """Represents a geometries list that has been repositioned and rotated."""

  _subtype: str
  _x: float
  _y: float
  _z: float
  _rx: float
  _ry: float
  _rz: float
  _geometries: List[constraints.Geometry]

  def __init__(self, subtype: str, x: float, y: float, z: float, rx: float,
               ry: float, rz: float,
               geometries: List[constraints.Geometry]) -> None:
    """Init a Composite Geometry Constraint.

    Args:
      subtype:
      x: The X location of the composite geometry constraint.
      y: The Y location of the composite geometry constraint.
      z: The Z location of the composite geometry constraint.
      rx: rotation x in axis-angle format
      ry: rotation y in axis-angle format
      rz: rotation z in axis-angle format
      geometries: A list of geometries to reposition and rotate.
    """
    super().__init__()
    self._subtype = subtype
    self._x = x
    self._y = y
    self._z = z
    self._rx = rx
    self._ry = ry
    self._rz = rz
    self._geometries = geometries

  def get_geometries(self) -> List[constraints.Geometry]:
    """Return the Geometries list."""
    return self._geometries.copy()

  def get_position(self) -> List[float]:
    """Return the X/Y/Z position."""
    return [self._x, self._y, self._z]

  def get_rotation(self) -> List[float]:
    """Return the RX/RY/RZ axis-angle rotation."""
    return [self._rx, self._ry, self._rz]

  def get_subtype(self) -> str:
    """Return the subtype."""
    return self._subtype

  @classmethod
  def from_json(cls, from_json: Dict[str,
                                     Any]) -> Optional[constraints.Geometry]:
    """Extract a Composite Geometry Constraint from a JSON message.

    Args:
      from_json: The JSON dictionary to extract from.

    Returns:
      The extracted Composite Geometry on success and None otherwise.

    """
    for d, fvs in [("position", ["x", "y", "z"]),
                   ("rotation", ["rx", "ry", "rz"])]:
      if not isinstance(from_json.get(d, {}), dict):
        return None
      for fv in fvs:
        if not isinstance(from_json.get(d, {}).get(fv, 0.0), (float, int)):
          return None
      for fv in from_json.get(d, {}):
        if fv not in fvs:
          logging.warning("extra value in Composite: %s %s %s", d, fv,
                          from_json)
    if not isinstance(from_json.get("subtype", ""), str):
      return None
    if not isinstance(from_json.get("geometries", []), list):
      return None
    geometries = []
    for geom in from_json.get("geometries", []):
      geo = load_geometry(geom)
      if geo is None:
        return None
      geometries.append(geo)
    for d in from_json:
      if d not in ["geometries", "subtype", "type", "position", "rotation"]:
        logging.warning("extra value in Composite: %s %s", d, from_json)
    return Composite(
        from_json.get("subtype", ""),
        from_json.get("position", {}).get("x", 0.0),
        from_json.get("position", {}).get("y", 0.0),
        from_json.get("position", {}).get("z", 0.0),
        from_json.get("rotation", {}).get("rx", 0.0),
        from_json.get("rotation", {}).get("ry", 0.0),
        from_json.get("rotation", {}).get("rz", 0.0), geometries)


def load_geometry(from_json: Dict[str, Any]) -> Optional[constraints.Geometry]:
  """Load a geometry from some JSON.

  Args:
    from_json: The JSON to extract the Geometry from.

  Returns:
    Returns Geometry on success and None othewise.

  """
  if from_json.get("type") == "composite":
    return Composite.from_json(from_json)
  elif from_json.get("type") == "box":
    return BoxImpl.from_json(from_json)
  elif from_json.get("type") == "plane":
    return Plane.from_json(from_json)
  return None


class ConstraintObject(ConstraintDevice):
  """Constraints object."""

  _geometry: constraints.Geometry

  def __init__(self, device_type: str, device_name: str,
               geometry: constraints.Geometry) -> None:
    """Init the Object.

    Args:
      device_type: The device type string.
      device_name: The device name string.
      geometry: The Geometry for the device.
    """
    super().__init__(device_type, device_name)
    self._geometry = geometry

  def get_geometry(self) -> constraints.Geometry:
    """Return the Geometry."""
    return self._geometry

  @classmethod
  def from_json(cls, json_data: Dict[str, Any]) -> Optional["ConstraintObject"]:
    """Extract an Object from a JSON dictionary.

    Args:
      json_data: The JSON data dictionary containing the Object.

    Returns:
      Returns the extract Object on success and None otherwise.

    """
    if not isinstance(json_data.get("parameters", None), dict):
      return None
    geometry = json_data["parameters"].get("geometry")
    if not isinstance(geometry, dict):
      return None
    geometry_object = load_geometry(geometry)
    if geometry_object is None:
      return None
    for d in json_data:
      if d not in ["parameters", "deviceType", "deviceName"]:
        logging.warning("extra Object field: %s", d)
    for d in json_data["parameters"]:
      if d not in ["geometry"]:
        logging.warning("extra Object parameter: %s", d)
    return ConstraintObject(
        json_data.get("deviceType", ""), json_data.get("deviceName", ""),
        geometry_object)


class Interactable(ConstraintDevice):
  """Interactable object in constraints."""

  _geometry: constraints.Geometry

  def __init__(self, device_type: str, device_name: str,
               geometry: constraints.Geometry) -> None:
    """Init an Interactble.

    Args:
      device_type: The device type string.
      device_name: The device name string.
      geometry: The Geometry of the device.
    """
    ConstraintDevice.__init__(self, device_type, device_name)
    self._geometry = geometry

  def get_geometry(self) -> constraints.Geometry:
    """Return the Geometry of the Interactable."""
    return self._geometry

  @classmethod
  def from_json(cls, json_data: Dict[str, Any]) -> Optional["Interactable"]:
    """Extract an Interactable from JSON data.

    Args:
      json_data: The JSON data to extract the Ineractable from.

    Returns:
      Returns the Interacable on succsss an None otherwise.

    """
    parameters = json_data.get("parameters", None)
    if parameters is None or not isinstance(parameters, dict):
      return None
    geo = json_data["parameters"].get("geometry")
    if not geo or not isinstance(geo, dict):
      return None
    geometry_object = load_geometry(geo)
    if geometry_object is None:
      return None
    for d in json_data:
      if d not in ["parameters", "deviceType", "deviceName"]:
        logging.warning("extra Interactable field: %s", d)
    for d in json_data["parameters"]:
      if d not in ["geometry"]:
        logging.warning("extra Interactable parameter: %s", d)
    return Interactable(
        json_data.get("deviceType", ""), json_data.get("deviceName", ""),
        geometry_object)


class ConstraintRobot(ConstraintDevice):
  """Robot device within constraints."""

  _joint_limits: List[constraints.JointLimit]

  def __init__(self, device_type: str, device_name: str,
               joint_limits: List[constraints.JointLimit]) -> None:
    """Init the Robot type, name and joint limits.

    Args:
      device_type: The device type as a string.
      device_name: The device name as a string.
      joint_limits: List of joint limits.
    """
    super().__init__(device_type, device_name)
    self._joint_limits = joint_limits.copy()

  def get_joint_limits(self) -> Tuple[constraints.JointLimit, ...]:
    """Return the joint limits."""
    return tuple(self._joint_limits)

  @classmethod
  def from_json(cls, json_data: Dict[str, Any]) -> Optional["ConstraintRobot"]:
    """Extract the Robot from some JSON data.

    Args:
      json_data: The JSON data to extract the Robot from.

    Returns:
      Returns Robot on success and None otherwise.

    """
    parameters = json_data.get("parameters", None)
    if parameters is None or not isinstance(parameters, dict):
      return None
    joint_limits = parameters.get("jointLimits", None)
    if joint_limits is None or not isinstance(joint_limits, list):
      return None
    joints = []
    for joint in joint_limits:
      if not isinstance(joint, list):
        return None
      if len(joint) != 2:
        return None
      joints.append(
          constraints.JointLimit(joint[0] * math.pi / 180.,
                                 joint[1] * math.pi / 180.))
    for d in json_data:
      if d not in {"parameters", "deviceType", "deviceName"}:
        logging.warning("extra Robot field: %s", d)
    for d in json_data["parameters"]:
      if d not in {"jointLimits"}:
        logging.warning("extra Robot parameter: %s", d)
    return ConstraintRobot(
        json_data.get("deviceType", ""), json_data.get("deviceName", ""),
        joints)


class ConstraintsImpl(constraints.Constraints):
  """A set of constraints returned by the robot."""

  _devices: List[ConstraintDevice]
  _bins: Dict[str, shapely.geometry.Polygon]

  def __init__(self, devices: List[ConstraintDevice]):
    """Init a Constraints.

    Args:
      devices: A list of devices.
    """
    self._devices = devices
    self._bins = {}
    for name, bin_name in [("LeftBin", "left"), ("RightBin", "right")]:
      self._bins[bin_name] = self._construct_bin(name)

  def __str__(self) -> str:
    """Return a string for Constraints."""
    devices_text = ",".join([str(device) for device in self._devices])
    return ("Constraints(_devices=[" + devices_text + "], _bins=" +
            str(self._bins) + ")")

  def _get_device(self, device_type: str,
                  device_name: str) -> Optional[ConstraintDevice]:
    """Lookup a device.

    Args:
      device_type: The device type as a string.
      device_name: The device name as a string.

    Returns:
      The device is returned if successfully found and None otherwise.

    """
    for device in self._devices:
      if (device.device_type == device_type and
          device.device_name == device_name):
        return device
    return None

  def _construct_bin(self,
                     device_name: str) -> Optional[shapely.geometry.Polygon]:
    object_constraint = self._get_device("object", device_name)
    if object_constraint is None:
      logging.warning(
          "Unable to make bin, no object in constraint with "
          "name: %s", device_name)
      return None
    if (not isinstance(object_constraint, Interactable) and
        not isinstance(object_constraint, ConstraintObject)):
      logging.warning(
          "Unable to make bin, constraint with name is not an "
          "Interactable or Object: %s", device_name)
      return None

    composite_geometry: constraints.Geometry = object_constraint.get_geometry()
    if not isinstance(composite_geometry, Composite):
      logging.warning(
          "Bin geometry is not composite in constraint with "
          "name: %s", device_name)
      return None
    if composite_geometry.get_subtype() != "bin":
      logging.warning(
          "Unable to find bin subtype in composite "
          "constraint with name: %s", device_name)
      return None

    position: List[float] = composite_geometry.get_position()
    rotation: List[float] = composite_geometry.get_rotation()

    rotation = transform.Rotation.from_euler(
        "zxy", rotation, degrees=True).as_rotvec()
    geometries = composite_geometry.get_geometries()

    points: List[Tuple[float, float]] = []
    for geo in geometries:
      if not isinstance(geo, BoxImpl):
        logging.warning(
            "Geometry is not of type Box in composite constraint "
            "with name: %s", device_name)
        return None

      for vertex in geo.get_vertices():
        vertex = transform_util.transform(vertex, np.array(position), rotation)
        points.append((vertex[0], vertex[1]))
    return shapely.geometry.MultiPoint(points).convex_hull

  def is_point_in_object(self, point: np.array, device_name: str) -> bool:
    """Check if a 3D point is colliding with a named device.

    set_bin_hulls() must have been previously called.
    Args:
      point: [x, y, z] coordinate of the point.
      device_name: name of the object to check.

    Returns:
      True if the point is inside the object.

    """
    if device_name not in self._bins:
      return False
    pt = shapely.geometry.Point(point[0], point[1])
    return pt.within(self._bins[device_name])

  def get_joint_limits(
      self, device_name: str) -> Optional[Tuple[constraints.JointLimit, ...]]:
    """Return the joint limits."""
    device = self._get_device("robot", device_name)
    if device is None:
      return None

    if not isinstance(device, ConstraintRobot):
      return None

    return device.get_joint_limits()

  def get_interactables(self) -> Tuple[constraints.Interactable, ...]:
    """Get the list of interactable geometries.

    Returns:
      Limits of all the interactable geometries if available.

    """
    interactables: List[constraints.Interactable] = []
    for dev in self._devices:
      if isinstance(dev, Interactable):
        if isinstance(dev.get_geometry(), constraints.Box):
          interactables.append(
              constraints.Interactable(dev.device_name, dev.get_geometry()))
    return tuple(interactables)


class ConstraintsDevice(device_base.DeviceBase):
  """Represents a Constraints Device."""

  _robot_name: Optional[str]

  def __init__(self, robot_name: Optional[str] = None) -> None:
    """Init a ConstraintsDevice.

    Args:
      robot_name: The robot name (or None.)
    """
    super().__init__()
    self._robot_name = robot_name

  def get_key_values(self) -> Set[device_base.KeyValueKey]:
    """Return the key values.

    Returns:
      Return a set of KeyValueKeys.

    """
    ret = {
        device_base.KeyValueKey(
            device_type="settings-engine",
            device_name="",
            key="workcell_constraints.json")
    }
    if self._robot_name is not None:
      ret.add(
          device_base.KeyValueKey(
              device_type="robot",
              device_name=self._robot_name,
              key="robot_constraints.json"))
    return ret

  def _extract_devices(
      self, const: str, name: str,
      extract_geometry: bool) -> Optional[List[Dict[str, Any]]]:
    try:
      data = json.loads(const)
      if not isinstance(data, dict):
        logging.warning(
            "constraints failed to load for %s - json was "
            "not a dictionary: %s", name, const)
        return None
      if extract_geometry and "geometry" not in data:
        logging.warning(
            "constraints failed to load for %s - json did not "
            "include 'geometry' tag: %s", name, const)
        return None
      geo = data
      if extract_geometry:
        geo = json.loads(data["geometry"])
      if not isinstance(geo.get("devices", []), list):
        logging.warning(
            "constraints failed to load for %s - 'geometry' "
            "'devices' is not a list: %s", name, const)
        return None
      return geo.get("devices", [])
    except json.decoder.JSONDecodeError:
      logging.warning("constraints failed to load for %s - "
                      "json data: %s", name, const)
      return None

  def get(self) -> Optional[ConstraintsImpl]:
    """Get the constraints.

    Returns:
      Return the constraints if available or None otherwise.

    """
    const = self.get_key_value(
        device_base.KeyValueKey(
            device_type="settings-engine",
            device_name="",
            key="workcell_constraints.json"))
    if not const or not const.strip():
      return None
    devices = self._extract_devices(const, "workcell_constraints.json", True)
    if devices is None:
      return None
    if self._robot_name is not None:
      const = self.get_key_value(
          device_base.KeyValueKey(
              device_type="robot",
              device_name=self._robot_name,
              key="robot_constraints.json"))
      if not const or not const.strip():
        return None
      robot_constraints = self._extract_devices(
          const, self._robot_name + " robot_constraints.json"
          if self._robot_name else "robot_constraints.json", False)
      if robot_constraints is None:
        return None
      devices += robot_constraints
    c_devices: List[ConstraintDevice] = []
    for dev in devices:
      obj: Optional[ConstraintDevice] = None
      if dev.get("deviceType", "") == "object":
        obj = ConstraintObject.from_json(dev)
      elif dev.get("deviceType", "") == "interactable":
        obj = Interactable.from_json(dev)
      elif dev.get("deviceType", "") == "robot":
        obj = ConstraintRobot.from_json(dev)
      else:
        logging.warning("Invalid device type: %s", dev)
        return None
      if obj is None:
        logging.warning("Invalid device element: %s", dev)
        return None
      c_devices.append(obj)
    return ConstraintsImpl(c_devices)
