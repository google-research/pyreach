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

"""Lightweight client to reach for point clouds and camera development.

Needs open3d as a pip dependency.

Steps to run -
1. pip install open3d==0.10.0.0
2. reach connect <reach-id>
3. python view3d.py
"""
from pyreach.tools.lib import view3d


def main() -> None:
  """Run the main for the viewer."""
  v = view3d.View3dOverReach()
  v.run_until_closed()


if __name__ == "__main__":
  main()
