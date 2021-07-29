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

"""Tests for metrics implementation."""

from typing import List
import unittest

from pyreach import metrics
from pyreach.common.python import types_gen
from pyreach.impl import metrics_impl
from pyreach.impl import test_utils
from pyreach.impl import thread_util


class MetricsTest(unittest.TestCase):

  def test_metrics_test(self) -> None:
    test_utils.run_test_client_test([TestMetrics()], [
        test_utils.TestResponderStep(
            types_gen.CommandData(
                ts=1,
                device_type="robot",
                data_type="reach-script",
                pick_id="test-pick-id",
                cmd="test-metric"),
            (types_gen.DeviceData(
                ts=1,
                seq=11,
                device_type="server",
                data_type="metric",
                metric_value=types_gen.KeyValue(
                    key="float-key", float_value=1.0),
                labels=[
                    types_gen.KeyValue(
                        key="test-label", value="test-float-value"),
                    types_gen.KeyValue(key="pick_id", value="test-pick-id")
                ],
                event_params=[
                    types_gen.KeyValue(
                        key="test-event", value="test-float-value")
                ],
            ),
             types_gen.DeviceData(
                 ts=1,
                 seq=12,
                 device_type="server",
                 data_type="metric",
                 metric_value=types_gen.KeyValue(
                     key="test-metric", float_value=1.0),
                 labels=[
                     types_gen.KeyValue(
                         key="test-label", value="test-float-value"),
                     types_gen.KeyValue(key="pick_id", value="test-pick-id")
                 ],
                 event_params=[
                     types_gen.KeyValue(
                         key="test-event", value="test-float-value")
                 ],
             )))
    ])

  def test_metrics(self) -> None:
    rdev, dev = metrics_impl.MetricDevice().get_wrapper()
    with test_utils.TestDevice(rdev) as test_device:
      test_device.set_responder(TestMetrics())
      global_capturer: "thread_util.CallbackCapturer[metrics.Metric]"
      global_capturer = thread_util.CallbackCapturer()
      stop = dev.add_update_callback(global_capturer.callback_false,
                                     global_capturer.finished_callback)
      capturer: "thread_util.CallbackCapturer[metrics.Metric]"
      capturer = thread_util.CallbackCapturer()
      pick_id_0, wait = dev.start_pick(None, capturer.callback_false,
                                       capturer.finished_callback)
      test_device.send_cmd(
          types_gen.CommandData(
              ts=1,
              device_type="robot",
              data_type="reach-script",
              pick_id=pick_id_0,
              cmd="operator/success"))

      def get_metrics(key: str) -> List[metrics.Metric]:
        float_key = dev.get_metric("float-key")
        exit_metric = dev.get_metric(key)
        self.assertIsNotNone(float_key)
        self.assertIsNotNone(exit_metric)
        if float_key and exit_metric:
          return [float_key, exit_metric]
        return []

      self._validate_metrics("operator/success", pick_id_0, wait())
      self._validate_metrics("operator/success", pick_id_0, capturer.wait())
      self._validate_metrics("operator/success", pick_id_0,
                             get_metrics("operator/success"))

      capturer = thread_util.CallbackCapturer()
      pick_id_1, wait = dev.start_pick(None, capturer.callback_false,
                                       capturer.finished_callback)
      test_device.send_cmd(
          types_gen.CommandData(
              ts=1,
              device_type="robot",
              data_type="reach-script",
              pick_id=pick_id_1,
              cmd="operator/pick_success"))
      self._validate_metrics("operator/pick_success", pick_id_1, wait())
      self._validate_metrics("operator/pick_success", pick_id_1,
                             capturer.wait())
      self._validate_metrics("operator/pick_success", pick_id_1,
                             get_metrics("operator/pick_success"))

      capturer = thread_util.CallbackCapturer()
      pick_id_2, wait = dev.start_pick(None, capturer.callback_false,
                                       capturer.finished_callback)
      test_device.send_cmd(
          types_gen.CommandData(
              ts=1,
              device_type="robot",
              data_type="reach-script",
              pick_id=pick_id_2,
              cmd="operator/failure"))
      self._validate_metrics("operator/failure", pick_id_2, wait())
      self._validate_metrics("operator/failure", pick_id_2, capturer.wait())
      self._validate_metrics("operator/failure", pick_id_2,
                             get_metrics("operator/failure"))

      capturer = thread_util.CallbackCapturer()
      pick_id_3, wait = dev.start_pick(None, capturer.callback_false,
                                       capturer.finished_callback)
      test_device.send_cmd(
          types_gen.CommandData(
              ts=1,
              device_type="robot",
              data_type="reach-script",
              pick_id=pick_id_3,
              cmd="operator/pick_failure"))
      self._validate_metrics("operator/pick_failure", pick_id_3, wait())
      self._validate_metrics("operator/pick_failure", pick_id_3,
                             capturer.wait())
      self._validate_metrics("operator/pick_failure", pick_id_3,
                             get_metrics("operator/pick_failure"))

      capturer = thread_util.CallbackCapturer()
      _, wait = dev.start_pick(0, capturer.callback_false,
                               capturer.finished_callback)
      self.assertEqual(len(wait()), 0)
      self.assertEqual(len(capturer.wait()), 0)

      stop()
      msgs = global_capturer.wait()
      self.assertEqual(len(msgs), 8)
      self._validate_metrics("operator/success", pick_id_0, msgs[0:2])
      self._validate_metrics("operator/pick_success", pick_id_1, msgs[2:4])
      self._validate_metrics("operator/failure", pick_id_2, msgs[4:6])
      self._validate_metrics("operator/pick_failure", pick_id_3, msgs[6:8])

  def _validate_metrics(self, exit_key: str, pick_id: str,
                        metrics_msgs: List[metrics.Metric]) -> None:
    self.assertEqual(len(metrics_msgs), 2)
    self.assertEqual(metrics_msgs[0].key, "float-key")
    self.assertEqual(metrics_msgs[0].float_value, 1.0)
    self.assertEqual(metrics_msgs[0].sequence, 11)
    self.assertEqual(len(metrics_msgs[0].labels), 2)
    self.assertEqual(metrics_msgs[0].labels[0][0], "test-label")
    self.assertEqual(metrics_msgs[0].labels[0][1], "test-float-value")
    self.assertEqual(metrics_msgs[0].labels[1][0], "pick_id")
    self.assertEqual(metrics_msgs[0].labels[1][1], pick_id)
    self.assertEqual(len(metrics_msgs[0].event_params), 1)
    self.assertEqual(metrics_msgs[0].event_params[0][0], "test-event")
    self.assertEqual(metrics_msgs[0].event_params[0][1], "test-float-value")
    self.assertEqual(metrics_msgs[1].key, exit_key)
    self.assertEqual(metrics_msgs[1].float_value, 1.0)
    self.assertEqual(metrics_msgs[1].sequence, 12)
    self.assertEqual(len(metrics_msgs[1].labels), 2)
    self.assertEqual(metrics_msgs[1].labels[0][0], "test-label")
    self.assertEqual(metrics_msgs[1].labels[0][1], "test-float-value")
    self.assertEqual(metrics_msgs[1].labels[1][0], "pick_id")
    self.assertEqual(metrics_msgs[1].labels[1][1], pick_id)
    self.assertEqual(len(metrics_msgs[1].event_params), 1)
    self.assertEqual(metrics_msgs[1].event_params[0][0], "test-event")
    self.assertEqual(metrics_msgs[1].event_params[0][1], "test-float-value")


class TestMetrics(test_utils.TestResponder):
  """Represents a Metrics for use in a test suite."""

  def step(self, cmd: types_gen.CommandData) -> List[types_gen.DeviceData]:
    """Test step, generates a response for testing framework data."""
    if cmd.device_type == "robot" and not cmd.device_name and cmd.data_type == "reach-script":
      return [
          types_gen.DeviceData(
              ts=cmd.ts,
              seq=11,
              device_type="server",
              data_type="metric",
              metric_value=types_gen.KeyValue(key="float-key", float_value=1.0),
              labels=[
                  types_gen.KeyValue(
                      key="test-label", value="test-float-value"),
                  types_gen.KeyValue(key="pick_id", value=cmd.pick_id)
              ],
              event_params=[
                  types_gen.KeyValue(
                      key="test-event", value="test-float-value")
              ],
          ),
          types_gen.DeviceData(
              ts=cmd.ts,
              seq=12,
              device_type="server",
              data_type="metric",
              metric_value=types_gen.KeyValue(key=cmd.cmd, float_value=1.0),
              labels=[
                  types_gen.KeyValue(
                      key="test-label", value="test-float-value"),
                  types_gen.KeyValue(key="pick_id", value=cmd.pick_id)
              ],
              event_params=[
                  types_gen.KeyValue(
                      key="test-event", value="test-float-value")
              ],
          ),
      ]
    return []

  def start(self) -> List[types_gen.DeviceData]:
    return []


if __name__ == "__main__":
  unittest.main()
