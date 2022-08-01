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
# pylint: disable=line-too-long
r"""3D viewer over reach connect.

First generate the proto types using project-reach:

```
cd ~/project-reach
source ../setenv.sh
./generate_python_protos.sh
```

For google3: this is not supported from within blaze binaries because GLFW has
issues with Google's GLIBC. Either run within project-reach, or export using
local copybara:

```
/google/data/ro/teams/copybara/copybara
robotics/learning/reach/third_party/copy.bara.sky local_debug ..
--folder-dir=/tmp/project-reach --ignore-noop && \
  cp -r ~/project-reach/pyreach/common/proto_gen
  /tmp/project-reach/pyreach/common && \
  PYTHONPATH=/tmp/project-reach python
  /tmp/project-reach/pyreach/tools/async_viewer_3d.py \
    --connection_string="connection-type=webrtc,robot-id=9932CC"
```

Or you can drop the connection_string flag and instead connect using:

```
reach connect <robot_id>
```

TODO: Fix GLIBC issues.
"""
# pylint: enable=line-too-long

# This was forked from
# //robotics/learning/reach/third_party/pyreach/tools/async_viewer.py.

from absl import app
from absl import flags

from pyreach.tools.lib import async_viewer_3d_controller

_REQFPS = flags.DEFINE_float('reqfps', 10,
                             'Fps at which frame requests are sent.')
_USE_TAGS = flags.DEFINE_bool('use_tags', False,
                              'Use tagged requests where possible.')
_CONNECTION_STRING = flags.DEFINE_string(
    'connection_string', '',
    'Connect using a PyReach connection string (see connection_string.md '
    'for examples and documentation).')
_WINDOW_HEIGHT = flags.DEFINE_integer('window_height', 960,
                                      'Height of OpenGL window (in pixels).')
_WINDOW_WIDTH = flags.DEFINE_integer('window_width', 1280,
                                     'Width of OpenGL window (in pixels).')
_USER_UID = flags.DEFINE_string('user_uid', None,
                                'Set user UID to connect with.')


def main(_) -> None:
  control = async_viewer_3d_controller.Controller(
      _WINDOW_WIDTH.value,
      _WINDOW_HEIGHT.value,
      reqfps=_REQFPS.value,
      use_tags=_USE_TAGS.value,
      connection_string=_CONNECTION_STRING.value,
      user_uid=_USER_UID.value)
  control.run_until_closed()


if __name__ == '__main__':
  app.run(main)
