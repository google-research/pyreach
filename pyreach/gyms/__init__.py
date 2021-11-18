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

"""Initialize Reach Gyms package."""

from pyreach.gyms.registration import register  # type: ignore

register(
    id='pyreach_gym_example-v0',
    entry_point=(
        'pyreach.gyms.envs.pyreach_gym_example:PyReachGymExampleEnv'
    ),
    max_episode_steps=200,
    reward_threshold=25.0,
)

register(
    id='benchmark-2d-v0',
    entry_point=(
        'pyreach.gyms.envs.benchmark_2d:Benchmark2DEnv'
    ),
    max_episode_steps=9999999999999999999999,
    reward_threshold=99999999999999999999.0,
)

register(
    id='benchmark-kitting-v0',
    entry_point=(
        'pyreach.gyms.envs.benchmark_kitting:KittingBenchmarkEnv'
    ),
    max_episode_steps=200,
    reward_threshold=25.0,
)

register(
    id='benchmark-folding-v0',
    entry_point=(
        'pyreach.gyms.envs.benchmark_folding:BenchmarkFoldingEnv'
    ),
    max_episode_steps=9999999999999999999999,
    reward_threshold=99999999999999999999.0,
)

register(
    id='benchmark-folding-v2',
    entry_point=(
        'pyreach.gyms.envs.benchmark_folding_v2:BenchmarkFoldingEnv'
    ),
    max_episode_steps=9999999999999999999999,
    reward_threshold=99999999999999999999.0,
)

register(
    id='singulation-autopick-v0',
    entry_point=(
        'pyreach.gyms.envs.singulation_autopick:SingulationAutopickEnv'
    ),
    max_episode_steps=200,
    reward_threshold=25.0,
)

register(
    id='integration-xarm-v0',
    entry_point=(
        'pyreach.gyms.envs.integration_xarm:IntegrationTestXarmEnv'
    ),
    max_episode_steps=9999999999999999999999,
    reward_threshold=99999999999999999999.0,
)

register(
    id='integration-xarm-sync-v0',
    entry_point=(
        'pyreach.gyms.envs.integration_xarm:IntegrationTestXarmSyncEnv'
    ),
    max_episode_steps=9999999999999999999999,
    reward_threshold=99999999999999999999.0,
)

register(
    id='integration-xarm-async-v0',
    entry_point=(
        'pyreach.gyms.envs.integration_xarm:IntegrationTestXarmAsyncEnv'
    ),
    max_episode_steps=9999999999999999999999,
    reward_threshold=99999999999999999999.0,
)

register(
    id='integration-ur-v0',
    entry_point=('pyreach.gyms.envs.integration_ur:IntegrationTestUREnv'),
    max_episode_steps=9999999999999999999999,
    reward_threshold=99999999999999999999.0,
)

register(
    id='integration-ur-sync-v0',
    entry_point=('pyreach.gyms.envs.integration_ur:IntegrationTestURSyncEnv'),
    max_episode_steps=9999999999999999999999,
    reward_threshold=99999999999999999999.0,
)

register(
    id='integration-ur-async-v0',
    entry_point=('pyreach.gyms.envs.integration_ur:IntegrationTestURAsyncEnv'),
    max_episode_steps=9999999999999999999999,
    reward_threshold=99999999999999999999.0,
)

register(
    id='integration-fanuc-sync-v0',
    entry_point=(
        'pyreach.gyms.envs.integration_ur:IntegrationTestFanucSyncEnv'),
    max_episode_steps=9999999999999999999999,
    reward_threshold=99999999999999999999.0,
)

register(
    id='integration-fanuc-async-v0',
    entry_point=(
        'pyreach.gyms.envs.integration_ur:IntegrationTestFanucAsyncEnv'),
    max_episode_steps=9999999999999999999999,
    reward_threshold=99999999999999999999.0,
)

register(
    id='benchmark-integration-v0',
    entry_point=(
        'pyreach.gyms.envs.benchmark_integration_test:BenchmarkIntegrationEnv'),
    max_episode_steps=9999999999999999999999,
    reward_threshold=99999999999999999999.0,
)
