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


def main() -> None:
  # Connect to the reach host.
  with LocalTCPHostFactory().connect() as host:
    assert host.oracle

    # Loop continuously, reading predictions.
    while not host.is_closed():
      # Read a prediction from the robot.
      oracle_prediction = host.oracle.fetch_prediction(
          intent="pick",
          prediction_type="pick",
          request_type="sparse",
          task_code="97",
          label="SingulateLeftBin")

      # Print the oracle
      if oracle_prediction:
        print("Oracle prediction points: ", oracle_prediction.points)
      else:
        print("Robot did not return oracle pick points")

if __name__ == "__main__":
  main()
