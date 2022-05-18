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
"""Library for async_viewer_3d.py."""

import dataclasses
import math
import threading
import time
from typing import Any, List, Tuple

from absl import logging
import glfw
import numpy as np
import OpenGL.GL as gl
from OpenGL.GL import shaders
from scipy.spatial import transform

import pyreach
from pyreach.common.proto_gen import logs_pb2
from pyreach.calibration import CalibrationCamera
from pyreach.common.base import transform_util
from pyreach.depth_camera import DepthFrame
from pyreach.factory import ConnectionFactory

VERTEX_SHADER = """
  #version 330 core
  in vec3 aVert;
  in vec3 aColor;
  uniform mat4 uMVMatrix;
  uniform mat4 uPMatrix;
  uniform float point_size;
  out vec4 vCol;
  void main() {
    // set position.
    vec4 pos_view = uMVMatrix * vec4(aVert, 1.0);
    gl_Position = uPMatrix * pos_view;
    // set color.
    vCol = vec4(aColor, 1.0);
    // Scale the screen-space quad by distance to the camera so that
    // points appear to have constant size.
    gl_PointSize = point_size / (-1.0f * pos_view.z);
  }
"""

FRAGMENT_SHADER = """
  #version 330 core
  in vec4 vCol;
  out vec4 FragColor;
  uniform int uDrawCircles;
  void main() {
    // Render as circles.
    if (uDrawCircles == 1 && dot(gl_PointCoord-0.5, gl_PointCoord-0.5) > 0.25)
      discard;
    else
      FragColor = vCol;
  }
"""

MOUSE_POS_SPEED = 1.0
MOUSE_POS_SHIFT_SPEED = 5.0
MOUSE_ROT_SPEED = 0.005
BACKGROUND_COLOR = [0.8, 0.8, 0.8]
STARTING_POINT_SIZE = 4.0
PICK_PLACE_POINT_SIZE_MUL = 10.0
# Transform all points so that robot-space up is OpenGL up.
POINT_CLOUD_ROTATION_EULER = [0, np.pi/2, 0]
STARTING_CAMERA_POS = np.array([0, 0.0, 1.5], np.float32)
PICK_AXIS_COLORS = np.array([[1, 0, 0],
                             [0, 1, 0],
                             [0, 0, 1]], np.float32)
PLACE_AXIS_COLORS = np.array([[0.5, 0, 0],
                              [0, 0.5, 0],
                              [0, 0, 0.5]], np.float32)


def _rotation_to_matrix(rotation: transform.Rotation) -> np.ndarray:
  if hasattr(rotation, "as_dcm"):  # scipy in google3 (old)
    return rotation.as_dcm()
  else:
    assert hasattr(rotation, "as_matrix")
    return rotation.as_matrix()


def _calc_cone_vert(nsteps: int = 20, rad: float = 1.0, length: float = 1.0
                    ) -> List[np.ndarray]:
  """Calculate vertices of a cone."""
  assert nsteps > 3
  verts = []
  angles = np.linspace(
      0.0, 2.0 * np.pi, num=nsteps, endpoint=False, dtype=np.float32)
  d = angles[1] - angles[0]
  for a in angles:
    # Side.
    p0 = np.array([rad * math.cos(a), rad * math.sin(a), 0], np.float32)
    p1 = np.array([rad * math.cos(a + d), rad * math.sin(a + d), 0], np.float32)
    verts.append(np.array([0, 0, length], np.float32))
    verts.append(p0)
    verts.append(p1)

    # Base.
    verts.append(np.array([0, 0, 0], np.float32))
    verts.append(p0)
    verts.append(p1)
  return verts


@dataclasses.dataclass(frozen=True)
class GLData():
  """Container for OpenGL reference ids."""
  program: gl.shaders.ShaderProgram
  vert_index: int  # vert shader in
  color_index: int  # vert shader in
  point_size: int  # vert shader uniform
  p_matrix_uniform: int  # vert shader uniform
  mv_matrix_uniform: int  # vert shader uniform
  draw_circles: int  # frag shader uniform


class RenderElement():
  """Base virtual class for renderable elements."""

  def __init__(self, vert: np.ndarray, color: np.ndarray):
    """Note: constructor must be called from within main python thread."""
    self._check_shapes(vert, color)
    self._vert: np.ndarray = vert
    self._color: np.ndarray = color

    # Make a vertex array object.
    self._vao = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(self._vao)

    # Vertices.
    self._vertex_buffer: int = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vertex_buffer)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, vert.nbytes,
                    vert.reshape(-1), gl.GL_DYNAMIC_DRAW)

    # Colors.
    self._color_buffer: int = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._color_buffer)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, color.nbytes,
                    color.reshape(-1), gl.GL_DYNAMIC_DRAW)

    gl.glBindVertexArray(0)  # Unbind to be safe.

    self._new_geom: bool = False
    self._lock: threading.Lock = threading.Lock()

  @property
  def vao(self) -> int:
    return self._vao

  @classmethod
  def _check_shapes(cls, vert: np.ndarray, color: np.ndarray):
    assert vert.dtype == np.float32 and color.dtype == np.float32
    assert vert.shape[1]
    assert vert.shape == color.shape

  def update(self, vert: np.ndarray, color: np.ndarray):
    """Modify the vertex and color data. Called from any thread."""
    self._check_shapes(vert, color)
    with self._lock:
      self._vert = vert
      self._color = color
      self._new_geom = True

  def sync(self):
    """Make sure OpenGL VAO is up to date. Must be called from main thread."""
    with self._lock:
      if self._new_geom:
        gl.glBindVertexArray(self._vao)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vertex_buffer)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0,
                           self._vert.nbytes, self._vert.reshape(-1))
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._color_buffer)
        gl.glBufferSubData(gl.GL_ARRAY_BUFFER, 0,
                           self._color.nbytes, self._color.reshape(-1))
        gl.glBindVertexArray(0)  # Unbind to be safe.
        self._new_geom = False

  def _render_base(self,
                   gl_data: GLData,
                   point_size: float,
                   mode: int,
                   draw_circles: bool):
    """Render the geometry."""
    with self._lock:
      # Enable data arrays.
      gl.glUniform1f(gl_data.point_size, point_size)
      gl.glUniform1i(gl_data.draw_circles, 1 if draw_circles else 0)
      gl.glBindVertexArray(self._vao)
      gl.glEnableVertexAttribArray(gl_data.vert_index)
      gl.glEnableVertexAttribArray(gl_data.color_index)
      gl.glCullFace(gl.GL_BACK)

      # Set buffers.
      gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vertex_buffer)
      gl.glVertexAttribPointer(
          gl_data.vert_index, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None)
      gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._color_buffer)
      gl.glVertexAttribPointer(
          gl_data.color_index, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, None)

      # Draw.
      gl.glDrawArrays(mode, 0, self._vert.shape[0])

      # Cleanup.
      gl.glDisableVertexAttribArray(gl_data.vert_index)
      gl.glDisableVertexAttribArray(gl_data.color_index)
      gl.glBindVertexArray(0)


class Basis(RenderElement):
  """Call to render an oriented point as a basis element."""

  def __init__(self,
               xyz: np.ndarray,
               rot: transform.Rotation,
               axis_colors: np.ndarray,
               length: float = 0.1,
               thickness: float = 0.005):
    self._axis_colors = axis_colors
    self._length = length
    self._thickness = thickness
    vert, color = self._xyz_rot_to_axis_geom(
        xyz, rot, self._axis_colors, self._length, self._thickness)
    super().__init__(vert, color)

  def update(self, xyz: np.ndarray, rot: transform.Rotation):
    vert, color = self._xyz_rot_to_axis_geom(
        xyz, rot, self._axis_colors, self._length, self._thickness)
    super().update(vert, color)

  @classmethod
  def _xyz_rot_to_axis_geom(
      cls, xyz: np.ndarray, rot: transform.Rotation, basis_colors,
      length: float, thickness: float) -> Tuple[np.ndarray, np.ndarray]:
    """Calculate vertex and color array for basis visualization."""

    # TODO: Would be faster with a static vertex set + transform.
    vert = []
    color = []
    for i, permute in enumerate([[0, 1, 2], [2, 0, 1], [1, 2, 0]]):
      cone_verts = _calc_cone_vert(rad=thickness, length=length)
      # The cone points up in the y-axis by default.
      # Permute the points so to point in each cardinal axis.
      cone_verts = [v[permute] for v in cone_verts]
      vert.extend(cone_verts)
      color.extend([basis_colors[i]] * len(cone_verts))

    vert = np.stack(vert, axis=0).astype(np.float32)
    color = np.stack(color, axis=0).astype(np.float32)

    # Now apply the transform.
    rot_mat = _rotation_to_matrix(rot).astype(np.float32)
    vert = vert.dot(rot_mat)
    vert = vert + xyz[None, :]

    return vert, color

  def render(self, gl_data: GLData):
    self._render_base(gl_data=gl_data,
                      point_size=1.0,
                      mode=gl.GL_TRIANGLES,
                      draw_circles=False)


class PointCloud(RenderElement):
  """Render a point cloud using screen-space spheres."""

  def render(self, gl_data: GLData, point_size: float):
    self._render_base(gl_data=gl_data,
                      point_size=point_size,
                      mode=gl.GL_POINTS,
                      draw_circles=True)


class Controller:
  """Controller for the async viewer."""

  def __init__(self,
               window_width: int,
               window_height: int,
               reqfps: float,
               use_tags: bool,
               connection_string: str = "") -> None:
    """Instantiate a controller for multiple cameras.

    Args:
      window_width: Width of the OpenGL window (in pixels).
      window_height: Height of the OpenGL window (in pixels).
      reqfps: the request rate for cameras.
      use_tags: if true, will use tagged requests.
      connection_string: The PyReach connection string.

    Raises:
      RuntimeError: if GLFW can't create a window.
    """
    self._window_width = window_width
    self._window_height = window_height
    self._close = False
    self._camera_pos = STARTING_CAMERA_POS
    self._camera_yaw = 0.0
    self._camera_pitch = 0.0
    self._ipred = 0
    self._point_size = STARTING_POINT_SIZE
    self._keys_down = set()
    self._mouse_down = set()

    (self._host, self._depth_name, self._depth_width,
     self._depth_height) = self._connect_to_host(connection_string)
    # Now that depth camera size is known, we can initialize OpenGL.
    (self._window, self._gl_data, self._pick_geom, self._place_geom,
     self._point_cloud_geom) = self._init_gl(
         self._window_width, self._window_height,
         self._depth_width, self._depth_height)
    self._register_opengl_callbacks()
    self._register_host_callbacks(use_tags, reqfps)

  @classmethod
  def _connect_to_host(cls, connection_string: str
                       ) -> Tuple[pyreach.Host, str, int, int]:
    """Connect to the pyreach host and get depth camera size."""

    host = ConnectionFactory(
        connection_string=connection_string,
        take_control_at_start=False,
        enable_streaming=False).connect()

    # Choose a depth camera to render.
    # TODO: Support rendering from all cameras.
    if not host.depth_cameras:
      raise ValueError("No Depth camera found.")

    # Grab the first camera alphabetically to make it deterministic.
    depth_name = sorted(host.depth_cameras.keys())[0]
    device = host.config.calibration.get_device(
        "depth-camera", depth_name)
    assert device and isinstance(device, CalibrationCamera)
    depth_width = device.width
    depth_height = device.height

    return host, depth_name, depth_width, depth_height

  def _register_host_callbacks(self, use_tags, reqfps):
    """Register pyreach host callbacks for depth and predictions."""
    is_playback = self._host.playback is not None

    depth_camera = self._host.depth_cameras[self._depth_name]
    depth_camera.add_update_callback(self._depth_camera_callback)
    if use_tags and not is_playback:
      depth_camera.enable_tagged_request()
    elif reqfps > 0 and not is_playback:
      depth_camera.start_streaming(1.0 / reqfps)

    internal = self._host.internal
    if internal:
      internal.add_device_data_callback(self._internal_callback)
    else:
      raise ValueError("No host.internal device.")

  def _register_opengl_callbacks(self):
    glfw.set_key_callback(self._window, self._key_callback)
    glfw.set_mouse_button_callback(self._window, self._mouse_button_callback)
    glfw.set_cursor_pos_callback(self._window, self._mouse_move_callback)

  @classmethod
  def _init_gl(cls, window_width: int, window_height: int,
               depth_width: int, depth_height: int
               ) -> Tuple[Any, GLData, Basis, Basis, PointCloud]:
    """Initialize OpenGL structures.

    Args:
      window_width: Width of the OpenGL window (pixels).
      window_height: Height of the OpenGL window (pixels).
      depth_width: Depth camera width (pixels).
      depth_height: Depth camera height (pixels).

    Returns:
      window: OpenGL window.
      gl_data: GLData struct containing opengl ids.
      pick_geom: Render object for 6DOF picks.
      place_geom: Render object for 6DOF place.
      point_cloud_geom: Render object for point cloud.

    Raises:
      RuntimeError: if the window cannot be initialized.
    """

    if not glfw.init():
      raise RuntimeError("glfw.init() failed.")
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)  # For Mac OS X
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    window = glfw.create_window(
        window_width, window_height,
        "async_viewer_3d_controller", None, None)
    if not window:
      glfw.terminate()
      raise RuntimeError("Could not create an window")

    glfw.make_context_current(window)

    # Initialize Geometry (push them off the screen with np.inf).
    pick_geom = Basis(xyz=np.array([0, 0, np.inf], np.float32),
                      rot=transform.Rotation.from_quat([0, 0, 0, 1]),
                      axis_colors=PICK_AXIS_COLORS)
    place_geom = Basis(xyz=np.array([0, 0, np.inf], np.float32),
                       rot=transform.Rotation.from_quat([0, 0, 0, 1]),
                       axis_colors=PLACE_AXIS_COLORS)
    point_cloud_geom = PointCloud(
        vert=np.inf * np.ones((depth_width * depth_height, 3), np.float32),
        color=np.zeros((depth_width * depth_height, 3), np.float32))

    # Compile shaders.
    gl.glBindVertexArray(point_cloud_geom.vao)  # Needed for shader verification
    program = shaders.compileProgram(
        shaders.compileShader(VERTEX_SHADER, gl.GL_VERTEX_SHADER),
        shaders.compileShader(FRAGMENT_SHADER, gl.GL_FRAGMENT_SHADER))
    gl.glUseProgram(program)
    gl.glBindVertexArray(0)

    # Make sure it compiled properly.
    attribs = [gl.glGetActiveAttrib(program, i) for i in
               range(gl.glGetProgramiv(program, gl.GL_ACTIVE_ATTRIBUTES))]
    uniforms = [gl.glGetActiveUniform(program, i) for i in
                range(gl.glGetProgramiv(program, gl.GL_ACTIVE_UNIFORMS))]
    logging.info("Program attributes: %s", str(attribs))
    logging.info("Program uniforms: %s", str(uniforms))

    p_matrix_uniform = gl.glGetUniformLocation(program, "uPMatrix")
    mv_matrix_uniform = gl.glGetUniformLocation(program, "uMVMatrix")
    point_size = gl.glGetUniformLocation(program, "point_size")
    vert_index = gl.glGetAttribLocation(program, "aVert")
    color_index = gl.glGetAttribLocation(program, "aColor")
    draw_circles = gl.glGetUniformLocation(program, "uDrawCircles")

    cls._print_helper_string()

    gl_data = GLData(
        program=program, vert_index=vert_index, color_index=color_index,
        point_size=point_size, p_matrix_uniform=p_matrix_uniform,
        mv_matrix_uniform=mv_matrix_uniform, draw_circles=draw_circles)

    return window, gl_data, pick_geom, place_geom, point_cloud_geom

  @classmethod
  def _print_helper_string(cls):
    """Print string with controls information."""
    helper_string = """\n\n
    WASDQE - move camera.
    left-Shift - Sprint!!!
    left-mouse + drag - rotate camera.
    '=' - increase point size.
    '-' - decrease point size.
    'p' - Visualize next oracle prediction (if shown).\n
    """
    logging.info(helper_string)

  def _depth_camera_callback(self, msg: DepthFrame) -> bool:
    """Calculate depth point cloud and update geometry."""
    calibration = self._host.config.calibration

    if not calibration:
      logging.info("No calibration, skipping frame.")
      return False

    device = calibration.get_device("depth-camera", msg.device_name)
    if not (device and isinstance(device, CalibrationCamera)):
      logging.info("No calibration, skipping frame.")
      return False

    assert msg.color_data.shape == (self._depth_height, self._depth_width, 3)
    assert msg.depth_data.shape == (self._depth_height, self._depth_width)

    color_np = msg.color_data.astype(np.float32).reshape(-1, 3) / 255.0
    depth_np = msg.depth_data.astype(np.float32)

    # Convert UVD -> XYZ (robot base coords).
    intrinsics = transform_util.intrinsics_to_matrix(
        device.intrinsics, dtype=depth_np.dtype)
    xyz_camera = transform_util.unproject_depth_vectorized(
        im_depth=depth_np.squeeze(),
        depth_dist=device.distortion_depth,
        camera_mtx=intrinsics,
        camera_dist=device.distortion)

    extrinsics = np.array(device.extrinsics, dtype=np.float32)
    xyz_robot = transform_util.transform(
        xyz_camera.transpose(), extrinsics[:3],
        extrinsics[3:]).transpose().reshape(-1, 3)

    self._point_cloud_geom.update(xyz_robot, color_np)

    return False

  def _internal_callback(self, msg: logs_pb2.DeviceData) -> bool:
    """Handle oracle events and visualize pick and place points."""
    if self._window is None:  # Ignore until the depth is received.
      return False

    if (msg.device_name == "pick-points" and
        msg.device_type == "oracle" and
        msg.data_type == "prediction"):
      if not msg.prediction.place_position_3d or not msg.prediction.position_3d:
        logging.info("No predicted xyz points.")
      self._ipred = self._ipred % len(msg.prediction.place_position_3d)

      pick_xyz = msg.prediction.position_3d[self._ipred]
      pick_quat = msg.prediction.quaternion_3d[self._ipred]
      self._pick_geom.update(
          np.array([pick_xyz.x, pick_xyz.y, pick_xyz.z], np.float32),
          transform.Rotation.from_quat([
              pick_quat.x, pick_quat.y, pick_quat.z, pick_quat.w]))

      place_xyz = msg.prediction.place_position_3d[self._ipred]
      place_quat = msg.prediction.place_quaternion_3d[self._ipred]
      self._place_geom.update(
          np.array([place_xyz.x, place_xyz.y, place_xyz.z], np.float32),
          transform.Rotation.from_quat([
              place_quat.x, place_quat.y, place_quat.z, place_quat.w]))

    return False

  def _key_callback(self, window, key, scancode, action, mods):
    """Keyboard callback."""
    del window
    del scancode
    del mods

    if action == glfw.PRESS:
      self._keys_down.add(key)
    elif action == glfw.RELEASE:
      self._keys_down.remove(key)

    if action == glfw.PRESS and key == glfw.KEY_MINUS:
      self._point_size *= 0.8
      logging.info("point_size: %f", self._point_size)
    elif action == glfw.PRESS and key == glfw.KEY_EQUAL:
      self._point_size *= 1.2
      logging.info("point_size: %f", self._point_size)
    elif action == glfw.PRESS and key == glfw.KEY_ESCAPE:
      self._close = True
    elif action == glfw.PRESS and key == glfw.KEY_P:
      self._ipred += 1

  def _mouse_button_callback(self, window, button, action, mods):
    """Mouse button callback."""
    del window
    del mods
    if action == glfw.PRESS:
      self._mouse_xpos, self._mouse_ypos = glfw.get_cursor_pos(self._window)
      self._mouse_down.add(button)
    elif action == glfw.RELEASE:
      self._mouse_down.remove(button)

  def _mouse_move_callback(self, window, xpos, ypos):
    """Mouse cursor movement callback."""
    del window
    if glfw.MOUSE_BUTTON_1 in self._mouse_down:
      # Convert mouse movement into camera rotation.
      dx = xpos - self._mouse_xpos
      dy = ypos - self._mouse_ypos
      self._camera_yaw += dx * MOUSE_ROT_SPEED
      self._camera_pitch += dy * MOUSE_ROT_SPEED

    self._mouse_xpos = xpos
    self._mouse_ypos = ypos

  @classmethod
  def perspective(cls, fov, aspect, near, far):
    n, f = near, far
    t = np.tan((fov * np.pi / 180) / 2) * near
    b = - t
    r = t * aspect
    l = b * aspect
    assert abs(n - f) > 0
    # pylint: disable=bad-whitespace
    return np.array((
        ((2*n)/(r-l),           0,           0,  0),
        (          0, (2*n)/(t-b),           0,  0),
        ((r+l)/(r-l), (t+b)/(t-b), (f+n)/(n-f), -1),
        (          0,           0, 2*f*n/(n-f),  0)), np.float32)
    # pylint: enable=bad-whitespace

  def _update_matricies(self,
                        dt: float) -> Tuple[np.ndarray, np.ndarray]:
    """Calculate projection and model matricies."""
    # Build projection matrix.
    p_matrix = self.perspective(
        fov=45,
        aspect=float(self._window_width) / self._window_height,
        near=0.01,
        far=100.0)

    # Move the camera in camera space if using the WSADQE keys.
    if glfw.KEY_LEFT_SHIFT in self._keys_down:
      speed = MOUSE_POS_SHIFT_SPEED
    else:
      speed = MOUSE_POS_SPEED
    mat = np.linalg.inv(self._calc_camera_rot_mat())
    if glfw.KEY_S in self._keys_down:
      self._camera_pos += dt * mat.dot(np.array([0, 0, 1])) * speed
    if glfw.KEY_W in self._keys_down:
      self._camera_pos -= dt * mat.dot(np.array([0, 0, 1])) * speed
    if glfw.KEY_A in self._keys_down:
      self._camera_pos -= dt * mat.dot(np.array([1, 0, 0])) * speed
    if glfw.KEY_D in self._keys_down:
      self._camera_pos += dt * mat.dot(np.array([1, 0, 0])) * speed
    if glfw.KEY_Q in self._keys_down:
      self._camera_pos -= dt * mat.dot(np.array([0, 1, 0])) * speed
    if glfw.KEY_E in self._keys_down:
      self._camera_pos += dt * mat.dot(np.array([0, 1, 0])) * speed

    # modelview matrix.
    camera_matrix = np.eye(4, dtype=np.float32)
    camera_matrix[0:3, 0:3] = self._calc_camera_rot_mat()
    camera_matrix[3, 0:3] = self._camera_pos
    mv_matrix = np.linalg.inv(camera_matrix)

    # Make the robot up (z-axis) match the openGL up (y-axis).
    pc_matrix = np.eye(4, dtype=np.float32)
    pc_matrix[0:3, 0:3] = _rotation_to_matrix(transform.Rotation.from_euler(
        angles=POINT_CLOUD_ROTATION_EULER, seq="yxz"))
    mv_matrix = pc_matrix.dot(mv_matrix)

    return p_matrix, mv_matrix

  def _calc_camera_rot_mat(self):
    return _rotation_to_matrix(transform.Rotation.from_euler(
        angles=[self._camera_yaw, self._camera_pitch, 0], seq="yxz"))

  def run_until_closed(self) -> None:
    """Run app until window is closed."""
    t_last_frame = time.time()
    while not glfw.window_should_close(self._window) and not self._close:
      glfw.poll_events()

      self._place_geom.sync()
      self._pick_geom.sync()
      self._point_cloud_geom.sync()

      cur_time = time.time()
      gl.glEnable(gl.GL_DEPTH_TEST)
      gl.glClearColor(
          BACKGROUND_COLOR[0], BACKGROUND_COLOR[1], BACKGROUND_COLOR[2], 1.0)
      gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

      # Use shader.
      gl.glUseProgram(self._gl_data.program)
      gl.glEnable(gl.GL_PROGRAM_POINT_SIZE)

      # Set matricies and uniforms.
      p_matrix, mv_matrix = self._update_matricies(cur_time - t_last_frame)
      gl.glUniformMatrix4fv(
          self._gl_data.p_matrix_uniform, 1, gl.GL_FALSE, p_matrix)
      gl.glUniformMatrix4fv(
          self._gl_data.mv_matrix_uniform, 1, gl.GL_FALSE, mv_matrix)

      # Render all objects.
      self._point_cloud_geom.render(self._gl_data, self._point_size)
      self._place_geom.render(self._gl_data)
      self._pick_geom.render(self._gl_data)

      glfw.swap_buffers(self._window)
      t_last_frame = cur_time

      time.sleep(1.0 / 60.0)

    glfw.destroy_window(self._window)
