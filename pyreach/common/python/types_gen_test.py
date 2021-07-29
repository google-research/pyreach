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

from pyreach.common.proto_gen import logs_pb2  # type: ignore
from pyreach.common.python import types_gen
import unittest


class TypesGenTest(unittest.TestCase):

  def test_convert_empty(self) -> None:
    dd = types_gen.DeviceData()
    json_obj = dd.to_json()
    self.assertEqual(json_obj, {})
    dd_proto = logs_pb2.DeviceData()
    dd = types_gen.DeviceData.from_proto(dd_proto)
    self.assertEqual(dd.to_json(), {})

  def test_convert_simple(self) -> None:
    dd_proto = logs_pb2.DeviceData()
    dd_proto.device_type = 'robot'
    dd = types_gen.DeviceData.from_proto(dd_proto)
    self.assertEqual(dd.to_json(), {'deviceType': 'robot'})

  def test_convert_timestamp(self) -> None:
    dd_proto = logs_pb2.DeviceData()
    dd_proto.ts.seconds = 1
    dd = types_gen.DeviceData.from_proto(dd_proto)
    self.assertEqual(dd.to_json(), {'ts': 1000})

  def test_convert_duration(self) -> None:
    cd_proto = logs_pb2.CommandData()
    cd_proto.event_duration.seconds = 1
    cd_proto.event_duration.nanos = 2
    cd = types_gen.CommandData.from_proto(cd_proto)
    self.assertEqual(cd.to_json(), {'eventDuration': 1.000000002})

  def test_convert_flatten(self) -> None:
    dd_proto = logs_pb2.DeviceData()
    dd_proto.color.color = 'color_file'
    dd = types_gen.DeviceData.from_proto(dd_proto)
    self.assertEqual(dd.to_json(), {'color': 'color_file'})

  def test_convert_legacy(self) -> None:
    dd_proto = logs_pb2.DeviceData()
    dd_proto.ur_state.pose[:] = [1, 2, 3]
    dd = types_gen.DeviceData.from_proto(dd_proto)
    self.assertEqual(dd.to_json(), {'pose': [1.0, 2.0, 3.0]})

  def test_convert_nested(self) -> None:
    dd_proto = logs_pb2.DeviceData()
    dd_proto.audio_request_mute.text_cue = 'abc'
    dd = types_gen.DeviceData.from_proto(dd_proto)
    self.assertEqual(dd.to_json(), {'audioRequestMute': {'textCue': 'abc'}})

  def test_oneof(self) -> None:
    dd_proto = logs_pb2.DeviceData()
    dd_proto.audio_request_mute.text_cue = 'abc'
    dd_proto.audio_request_unmute.text_cue = 'def'
    dd = types_gen.DeviceData.from_proto(dd_proto)
    self.assertEqual(dd.to_json(), {'audioRequestUnmute': {'textCue': 'def'}})

  def test_snapshot(self) -> None:
    cd_proto = logs_pb2.CommandData()
    cd_proto.device_type = 'robot'
    cd_proto.data_type = 'reach-script'
    cd_proto.reach_script.preemptive = True
    cd_proto.snapshot.device_data_refs.add().ts.seconds = 1
    cd_proto.snapshot.device_data_refs.add().seq = 2
    cd_proto.snapshot.gym_actions.add().device_type = 'robot'
    cd_proto.snapshot.gym_actions[0].arm_action_params.command = 1
    cd = types_gen.CommandData.from_proto(cd_proto)
    self.assertEqual(
        cd.to_json(), {
            'dataType': 'reach-script',
            'deviceType': 'robot',
            'reachScript': {
                'preemptive': True
            },
            'snapshot': {
                'deviceDataRefs': [{
                    'ts': 1000
                }, {
                    'seq': 2
                }],
                'gymActions': [{
                    'armActionParams': {
                        'command': 1
                    },
                    'deviceType': 'robot'
                }]
            }
        })


if __name__ == '__main__':
  unittest.main()
