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

"""A basic example of using the PyReach API to playback a local log.

The local logs playback API can playback both host-side and client-side logs.
The logs are directories stored on disk with subdirectories for command-data
and device-data, containing JSON files, and other directories containing images.
The example program will playback both the raw device-data using the internal
API, and the stored gym "snapshots" that allow simulation of gym sessions.

Playback all device-data and snapshots in a directory:
 - python3 logs_playback_example.py --robot_id=<my-robot>
   --working_directory=<log_directory>

Playback only device-data and snapshots sent to a given client in a directory:
 - python3 logs_playback_example.py --robot_id=<my-robot>
   --working_directory=<log_directory> --client_id=<my-client-id>

Playback only device-data and snapshots sent to the first client in a directory:
 - python3 logs_playback_example.py --robot_id=<my-robot>
   --working_directory=<log_directory> --select_client

Playback all snapshots sent to the given gym run, and all device-data sent to
the client that created that gym run:
 - python3 logs_playback_example.py --robot_id=<my-robot>
   --working_directory=<log_directory> --gym_run_id=<gym-run-id>

Playback all snapshots sent to the first gym run in the log, and all device-data
sent client that created that gym run:
 - python3 logs_playback_example.py --robot_id=<my-robot>
   --working_directory=<log_directory> --select_gym_run
"""
from typing import Any, List

from absl import app  # type: ignore
from absl import flags  # type: ignore

from pyreach.common.python import types_gen
from pyreach.factory import LocalPlaybackHostFactory


def main(argv: List[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError("Too many command-line arguments.")

  with LocalPlaybackHostFactory(flags.FLAGS.robot_id,
                                flags.FLAGS.working_directory,
                                flags.FLAGS.client_id,
                                flags.FLAGS.select_client,
                                flags.FLAGS.gym_run_id,
                                flags.FLAGS.select_gym_run).connect() as host:
    print("Host loaded, starting playback...")
    assert host.playback
    assert host.internal
    assert host.internal.playback

    if flags.FLAGS.sequence is not None:
      host.internal.playback.seek_device_data(None, flags.FLAGS.sequence)

    sequence_numbers = []
    timestamps = []

    def print_data(data: types_gen.DeviceData) -> bool:
      print(data.to_json())
      if data.seq > 0:
        sequence_numbers.append(data.seq)
      if data.ts > 0:
        timestamps.append(float(data.ts) / 1000.0)
      return False

    def print_object(obj: Any) -> bool:
      print(obj)
      return False

    for name, arm in host.arms.items():
      print("Discover arm:", name)
      arm.add_update_callback(print_object)

    for name, color_camera in host.color_cameras.items():
      print("Discover color camera:", name)
      color_camera.add_update_callback(print_object)

    for name, depth_camera in host.depth_cameras.items():
      print("Discover depth camera:", name)
      depth_camera.add_update_callback(print_object)

    for name, oracle in host.oracles.items():
      print("Discover oracle:", name)
      oracle.add_update_callback(print_object)

    for _, vacuum in host.vacuums.items():
      vacuum.add_state_callback(print_object)
      vacuum.add_blowoff_state_callback(print_object)
      vacuum.add_pressure_state_callback(print_object)
      vacuum.add_gauge_state_callback(print_object)

    host.internal.add_device_data_callback(print_data)

    while host.internal.playback.device_data_available():
      print("----")
      host.internal.playback.next_device_data()

    print("------------------ SEEK SEQ --------------------")
    if sequence_numbers:
      sequence = sequence_numbers[int(len(sequence_numbers) / 2)]
      print("Reset to sequence:", sequence)
      sequence_numbers = []
      host.internal.playback.seek_device_data(None, sequence)
      while host.internal.playback.device_data_available():
        print("----")
        host.internal.playback.next_device_data()

    print("------------------ SEEK TIME --------------------")
    if timestamps:
      timestamp = timestamps[int(len(timestamps) / 2)]
      print("Reset to timestamp:", timestamp)
      timestamps = []
      host.internal.playback.seek_device_data(timestamp, None)
      while host.internal.playback.device_data_available():
        print("----")
        host.internal.playback.next_device_data()

    gym_steps = []
    while True:
      snapshot = host.playback.next_snapshot()
      if snapshot is None:
        break
      gym_steps.append(
          (snapshot.gym_run_id, snapshot.gym_episode, snapshot.gym_step))
      print("----")
      print(snapshot)
      print(host.playback.replay_snapshot(snapshot))

    print("----------------- SNAPSHOT SEQ --------------------")
    if gym_steps:
      gym_step = gym_steps[int(len(gym_steps) / 2)]
      print("Gym Run ID:", gym_step[0], "episode:", gym_step[1], "step:",
            gym_step[2])
      snapshot = host.playback.seek_snapshot(gym_step[0], gym_step[1],
                                             gym_step[2])

      while True:
        if snapshot is None:
          break
        gym_steps.append(
            (snapshot.gym_run_id, snapshot.gym_episode, snapshot.gym_step))
        print("----")
        print(snapshot)
        snapshot = host.playback.next_snapshot()


if __name__ == "__main__":
  flags.DEFINE_string("robot_id", None, "The robot id to connect to.")
  flags.DEFINE_string("working_directory", None, "Working directory to load.")
  flags.DEFINE_string("client_id", None, "Optional, client id to replay as.")
  flags.DEFINE_bool("select_client", False,
                    "Optional, if true, select the first client and replay.")
  flags.DEFINE_string("gym_run_id", None, "Optional, gym run id to replay.")
  flags.DEFINE_bool(
      "select_gym_run", False,
      "Optional, if set will select the first run id and replay.")
  flags.DEFINE_integer("sequence", None,
                       "Optional, sequence number to start at.")
  flags.mark_flag_as_required("robot_id")
  flags.mark_flag_as_required("working_directory")
  app.run(main)
