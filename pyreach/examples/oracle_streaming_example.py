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

"""A basic example of using the PyReach oracle streaming API.

To run this example, please run reach connect first.
If running on the reach host, this example will connect directly if
-tcp_uplink_port 50008 is specified.
"""
from pyreach.factory import LocalTCPHostFactory
from pyreach.oracle import Prediction


def main() -> None:
  # Connect to the reach host.
  with LocalTCPHostFactory().connect() as host:
    assert host.oracle

    # Callback to print the prediction. Returns false so it will continue to be
    # called. If the callback returns true, it will be removed from the
    # callbacks list and stop being called.
    def callback(prediction: Prediction) -> bool:
      print("Oracle prediction:", prediction)
      return False

    # Add a callback for all predictions from the oracle.
    host.oracle.add_update_callback(callback)

    # Start tagged request streaming from the oracle.
    host.oracle.enable_tagged_request(
        intent="pick",
        prediction_type="pick",
        request_type="sparse",
        task_code="97",
        label="SingulateLeftBin")

    # Spin until host exits, either by losing connection or control+C.
    host.wait()

if __name__ == "__main__":
  main()
