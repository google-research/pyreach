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

"""Tests of PyReach Gym."""

import collections
import math
from typing import Any, Dict, Set, Tuple
import unittest

import gym  # type: ignore
import numpy as np  # type: ignore
from pyreach import host
from pyreach.gyms import core as gyms_core
from pyreach.gyms import reach_env
from pyreach.gyms.registration import register
from pyreach.mock import host_mock

GYMS_PATH = ""


class GymArmEnv(reach_env.ReachEnv):
  """Configure a Gym environment with a synchronous arm."""

  def __init__(self, is_synchronous: bool = True, **kwargs: Any) -> None:
    """Init GymArmEnv."""
    pi: float = math.pi
    low_joint_angles: Tuple[float, ...] = (-pi, -pi, -pi, -pi, -pi, -pi)
    high_joint_angles: Tuple[float, ...] = (pi, pi, pi, pi, pi, pi)
    response_queue_length: int = 0 if is_synchronous else 2

    pyreach_config: Dict[str, reach_env.ReachElement] = {
        "arm":
            reach_env.ReachArm(
                reach_name="robot",
                low_joint_angles=low_joint_angles,
                high_joint_angles=high_joint_angles,
                apply_tip_adjust_transform=False,
                is_synchronous=is_synchronous,
                response_queue_length=response_queue_length),
    }

    mock_host: host.Host = host_mock.HostMock()
    assert isinstance(mock_host, host.Host)
    assert isinstance(mock_host, host_mock.HostMock)
    super().__init__(pyreach_config=pyreach_config, host=mock_host, **kwargs)


class GymArmSyncEnv(GymArmEnv):
  """Configure a Gym environment with a synchronous arm."""

  def __init__(self, **kwargs: Any) -> None:
    """Init a synchronous arm."""
    super().__init__(is_synchronous=True, **kwargs)


class GymArmAsyncEnv(GymArmEnv):
  """Configure a Gym environment with a synchronous arm."""

  def __init__(self, **kwargs: Any) -> None:
    """Init a synchronous arm."""
    super().__init__(is_synchronous=False, **kwargs)


class TestGymArmEnv(unittest.TestCase):
  """Test the Gym ArmElement environments."""

  def test_asynchronous_arm_register(self) -> None:
    """Test asynchronous Arm registration."""
    self.arm_register_test(is_synchronous=False)

  def test_synchronous_arm_register(self) -> None:
    """Test synchronous Arm registration."""
    # self.arm_register_test(is_synchronous=True)
    pass

  def arm_register_test(self, is_synchronous: bool) -> None:
    """Test Gym ArmElement."""
    env_id_name: str = ("synchronous_arm_element_env-v0" if is_synchronous else
                        "asynchronous_arm_element_env-v0")
    class_name: str = ("GymArmSyncEnv" if is_synchronous else "GymArmAsyncEnv")
    entry_point: str = GYMS_PATH + "reach_env_test:" + class_name
    register(
        id=env_id_name,
        entry_point=entry_point,
        max_episode_steps=200,
        reward_threshold=25.0)

    response_queue_length: int = 0 if is_synchronous else 2
    env: Any
    with gym.make(env_id_name) as env:
      assert isinstance(env, gym.Env), env

      action_space: Any = env.action_space
      assert isinstance(action_space, gym.spaces.Space)

      observation_space: Any = env.observation_space
      assert isinstance(observation_space, gym.spaces.Space)

      action_match: Dict[str, Any] = {
          "arm": {
              "command": 0,
              "id": 0,
              "joint_angles": np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
              "pose": np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
              "reach_action": 0,
              "use_linear": 0,
              "preemptive": 0,
              "velocity": np.full((), 0.0),
              "acceleration": np.full((), 0.0),
              "timeout": gyms_core.Timestamp.new(0.0),
          }
      }
      if not is_synchronous:
        action_match["arm"]["synchronous"] = 0

      observation_match: Dict[str, Any] = {
          "arm": {
              "ts": gyms_core.Timestamp.new(0.0),
              "joint_angles": np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
              "pose": np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
              "status": 0,
          }
      }

      response: Dict[str, Any] = {}
      if not is_synchronous and response_queue_length:
        response = {
            "ts": gyms_core.Timestamp.new(0.0),
            "id": 0,
            "status": 0,
            "finished": 0,
        }
        responses: Tuple[Dict[str, Any], ...]
        responses = response_queue_length * (response,)
        observation_match["arm"]["responses"] = responses

      assert space_match(action_space, action_match, ("action",))
      assert space_match(observation_space, observation_match, ("observation",))

      observation: gyms_core.Observation = env.reset()
      assert space_match(observation_space, observation_match, ("reset",))
      assert action_observation_eq(observation, observation_match)

      # Now do some steps:
      if not is_synchronous:
        to_joints_action: gyms_core.Action = {
            "arm": {
                "command": 1,
                "id": 1,
                "joint_angles": np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
            }
        }
        response1 = {
            "ts": gyms_core.Timestamp.new(0.0),
            "id": 1,
            "status": 0,
            "finished": 1,
        }
        response2 = {
            "ts": gyms_core.Timestamp.new(0.0),
            "id": 0,
            "status": 0,
            "finished": 0,
        }
        to_joints_observation: Dict[str, Any] = {
            "arm": {
                "joint_angles": np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                "pose": np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
                "responses": (response1, response2),
                "status": 0,
                "ts": gyms_core.Timestamp.new(0.0),
            }
        }

        assert space_match(
            action_space, to_joints_action, ("to_joints",),
            exact=False), "Invalid action"
        done: bool
        observation, _, done, _ = env.step(to_joints_action)
        assert action_observation_eq(observation,
                                     to_joints_observation), observation
        _ = done


class GymColorCameraEnv(reach_env.ReachEnv):
  """Configure a Gym environment with a synchronous colorcamera."""

  def __init__(self, is_synchronous: bool = True, **kwargs: Any) -> None:
    """Init GymColorCameraEnv."""
    pyreach_config: Dict[str, reach_env.ReachElement] = {
        "colorcamera":
            reach_env.ReachColorCamera(
                reach_name="ColorCamera",
                shape=(3, 5),
                is_synchronous=is_synchronous)
    }

    mock_host: host.Host = host_mock.HostMock()
    assert isinstance(mock_host, host.Host)
    assert isinstance(mock_host, host_mock.HostMock)
    super().__init__(pyreach_config=pyreach_config, host=mock_host, **kwargs)


class GymColorCameraSyncEnv(GymColorCameraEnv):
  """Configure a Gym environment with a synchronous colorcamera."""

  def __init__(self, **kwargs: Any) -> None:
    """Init a synchronous colorcamera."""
    super().__init__(is_synchronous=True, **kwargs)


class GymColorCameraAsyncEnv(GymColorCameraEnv):
  """Configure a Gym environment with a synchronous colorcamera."""

  def __init__(self, **kwargs: Any) -> None:
    """Init a synchronous colorcamera."""
    super().__init__(is_synchronous=False, **kwargs)


class TestGymColorCameraEnv(unittest.TestCase):
  """Test the Gym ColorCameraElement environments."""

  def test_asynchronous_colorcamera_register(self) -> None:
    """Test asynchronous ColorCamera registration."""
    self.colorcamera_register_test(is_synchronous=False)

  def test_synchronous_colorcamera_register(self) -> None:
    """Test synchronous ColorCamera registration."""
    self.colorcamera_register_test(is_synchronous=True)

  def colorcamera_register_test(self, is_synchronous: bool) -> None:
    """Test Gym ColorCameraElement."""
    env_id_name: str = ("synchronous_colorcamera_element_env-v0"
                        if is_synchronous else
                        "asynchronous_colorcamera_element_env-v0")
    class_name: str = ("GymColorCameraSyncEnv"
                       if is_synchronous else "GymColorCameraAsyncEnv")
    entry_point: str = GYMS_PATH + "reach_env_test:" + class_name
    register(
        id=env_id_name,
        entry_point=entry_point,
        max_episode_steps=200,
        reward_threshold=25.0)

    env: Any
    with gym.make(env_id_name) as env:
      assert isinstance(env, gym.Env), env

      action_space: Any = env.action_space
      assert isinstance(action_space, gym.spaces.Space)
      action_match: Dict[str, Any] = {"colorcamera": {}}
      assert space_match(action_space, action_match, ("action",))

      observation_space: Any = env.observation_space
      assert isinstance(observation_space, gym.spaces.Space)
      observation_match: Dict[str, Any] = {
          "colorcamera": {
              "color":
                  np.array([[(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                             (0, 0, 0)],
                            [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                             (0, 0, 0)],
                            [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                             (0, 0, 0)]],
                           dtype=np.uint8),
              "ts":
                  gyms_core.Timestamp.new(1.0),
          }
      }
      assert space_match(observation_space, observation_match, ("observation",))

      if not is_synchronous:
        observation: gyms_core.Observation = env.reset()
        assert gyms_core.get_float0(observation, "colorcamera.ts") == 1.0
        image: np.ndarray = gyms_core.get_int3(observation, "colorcamera.color")
        assert image.shape == (3, 5, 3)
        assert image.dtype == np.uint8
        assert action_observation_eq(observation, observation_match)


class GymDepthCameraEnv(reach_env.ReachEnv):
  """Configure a Gym environment with a synchronous depthcamera."""

  def __init__(self,
               is_synchronous: bool = True,
               color_enabled: bool = True,
               **kwargs: Any) -> None:
    """Init GymDepthCameraEnv."""
    pyreach_config: Dict[str, reach_env.ReachElement] = {
        "depthcamera":
            reach_env.ReachDepthCamera(
                reach_name="DepthCamera",
                shape=(3, 5),
                is_synchronous=is_synchronous,
                color_enabled=color_enabled)
    }

    mock_host: host.Host = host_mock.HostMock()
    assert isinstance(mock_host, host.Host)
    assert isinstance(mock_host, host_mock.HostMock)
    super().__init__(pyreach_config=pyreach_config, host=mock_host, **kwargs)


class GymDepthCameraSyncEnv(GymDepthCameraEnv):
  """Configure a Gym environment with a synchronous depth camera."""

  def __init__(self, **kwargs: Any) -> None:
    """Init a synchronous depthcamera."""
    super().__init__(is_synchronous=True, color_enabled=False, **kwargs)


class GymDepthCameraAsyncEnv(GymDepthCameraEnv):
  """Configure a Gym environment with an asynchronous depth camera."""

  def __init__(self, **kwargs: Any) -> None:
    """Init a synchronous depthcamera."""
    super().__init__(is_synchronous=False, color_enabled=False, **kwargs)


class GymDepthColorCameraSyncEnv(GymDepthCameraEnv):
  """Configure a Gym environment with a synchronous depth and color camera."""

  def __init__(self, **kwargs: Any) -> None:
    """Init a synchronous depthcamera."""
    super().__init__(is_synchronous=True, color_enabled=True, **kwargs)


class GymDepthColorCameraAsyncEnv(GymDepthCameraEnv):
  """Configure a Gym environment with an asynchronous depth and color camera."""

  def __init__(self, **kwargs: Any) -> None:
    """Init a synchronous depthcamera."""
    super().__init__(is_synchronous=False, color_enabled=True, **kwargs)


class TestGymDepthCameraEnv(unittest.TestCase):
  """Test the Gym DepthCameraElement environments."""

  def test_asynchronous_depthcamera_register(self) -> None:
    """Test asynchronous DepthCamera registration."""
    self.depthcamera_register_test(is_synchronous=False, color_enabled=False)

  def test_synchronous_depthcamera_register(self) -> None:
    """Test synchronous DepthCamera registration."""
    self.depthcamera_register_test(is_synchronous=True, color_enabled=False)

  def test_asynchronous_depthcolorcamera_register(self) -> None:
    """Test asynchronous DepthCamera registration."""
    self.depthcamera_register_test(is_synchronous=False, color_enabled=True)

  def test_synchronous_depthcolorcamera_register(self) -> None:
    """Test synchronous DepthCamera registration."""
    self.depthcamera_register_test(is_synchronous=True, color_enabled=True)

  def depthcamera_register_test(self, is_synchronous: bool,
                                color_enabled: bool) -> None:
    """Test Gym DepthCameraElement."""
    env_id_name: str = ("{0}_depth{1}_element_env-v0".format(
        "sync" if is_synchronous else "async",
        "color" if color_enabled else ""))
    class_name: str = "GymDepth{0}Camera{1}Env".format(
        "Color" if color_enabled else "", "Sync" if is_synchronous else "Async")
    entry_point: str = GYMS_PATH + "reach_env_test:" + class_name
    register(
        id=env_id_name,
        entry_point=entry_point,
        max_episode_steps=200,
        reward_threshold=25.0)

    env: Any
    with gym.make(env_id_name) as env:
      assert isinstance(env, gym.Env), env

      action_space: Any = env.action_space
      assert isinstance(action_space, gym.spaces.Space)
      action_match: Dict[str, Any] = {"depthcamera": {}}
      assert space_match(action_space, action_match, ("action",))

      observation_space: Any = env.observation_space
      assert isinstance(observation_space, gym.spaces.Space)
      observation_match: Dict[str, Any] = {
          "depthcamera": {
              "depth":
                  np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
                           dtype=np.uint8),
              "ts":
                  gyms_core.Timestamp.new(1.0),
          }
      }
      if color_enabled:
        observation_match["depthcamera"]["color"] = np.array([[
            (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)
        ], [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
            (0, 0, 0)], [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                         (0, 0, 0)]],
                                                             dtype=np.uint8)
      assert space_match(observation_space, observation_match, ("observation",))

      if not is_synchronous:
        observation: gyms_core.Observation = env.reset()
        assert gyms_core.get_float0(observation, "depthcamera.ts") == 1.0
        depth: np.ndarray = gyms_core.get_int2(observation, "depthcamera.depth")
        assert depth.shape == (3, 5)
        assert depth.dtype == np.uint16

        if color_enabled:
          color: np.ndarray = gyms_core.get_int3(observation,
                                                 "depthcamera.color")
          assert color.shape == (3, 5, 3)
          assert color.dtype == np.uint8
        assert action_observation_eq(observation, observation_match)


class GymForceTorqueSensorEnv(reach_env.ReachEnv):
  """Configure a Gym environment with a ForceTorqueSensor."""

  def __init__(self, is_synchronous: bool = True, **kwargs: Any) -> None:
    """Init GymForceTorqueSensorEnv."""
    pyreach_config: Dict[str, reach_env.ReachElement] = {
        "force_torque_sensor":
            reach_env.ReachForceTorqueSensor(
                reach_name="ForceTorqueSensor", is_synchronous=is_synchronous)
    }

    mock_host: host.Host = host_mock.HostMock()
    assert isinstance(mock_host, host.Host)
    assert isinstance(mock_host, host_mock.HostMock)
    super().__init__(pyreach_config=pyreach_config, host=mock_host, **kwargs)


class GymForceTorqueSensorSyncEnv(GymForceTorqueSensorEnv):
  """Configure a Gym environment with a synchronous ForceTorqueSensor."""

  def __init__(self, is_synchronous: bool = True, **kwargs: Any) -> None:
    """Init a synchronous ForceTorqueSensor."""
    super().__init__(is_synchronous=is_synchronous, **kwargs)


class GymForceTorqueSensorAsyncEnv(GymForceTorqueSensorEnv):
  """Configure a Gym environment with a synchronous ForceTorqueSensor."""

  def __init__(self, is_synchronous: bool = True, **kwargs: Any) -> None:
    """Init an asynchronous ForceTorqueSensor."""
    super().__init__(is_synchronous=False, **kwargs)


class TestGymForcetorqueSensorEnv(unittest.TestCase):
  """Test the Gym ForceTorqueSensorElement environments."""

  def test_asynchronous_force_torque_sensor_register(self) -> None:
    """Test asynchronous ForceTorqueSensor registration."""
    self.force_torque_sensor_register_test(is_synchronous=False)

  def test_synchronous_force_torque_sensor_register(self) -> None:
    """Test synchronous ForceTorqueSensor registration."""
    self.force_torque_sensor_register_test(is_synchronous=True)

  def force_torque_sensor_register_test(self,
                                        is_synchronous: bool = True) -> None:
    """Test Gym ForceTorqueSensorElement."""
    env_id_name: str = "{0}_force_torque_sensor_element_env-v0".format(
        "sync" if is_synchronous else "async")
    class_name: str = "GymForceTorqueSensor{0}Env".format(
        "Sync" if is_synchronous else "Async")
    entry_point: str = GYMS_PATH + "reach_env_test:" + class_name
    register(
        id=env_id_name,
        entry_point=entry_point,
        max_episode_steps=200,
        reward_threshold=25.0)

    env: Any
    with gym.make(env_id_name) as env:
      assert isinstance(env, gym.Env), env

      action_space: Any = env.action_space
      assert isinstance(action_space, gym.spaces.Space)
      action_match: Dict[str, Any] = {"force_torque_sensor": {}}
      assert space_match(action_space, action_match, ("action",))

      observation_space: Any = env.observation_space
      assert isinstance(observation_space, gym.spaces.Space)
      observation_match: Dict[str, Any] = {
          "force_torque_sensor": {
              "force": np.array([0.0, 0.0, 0.0], dtype=np.float_),
              "torque": np.array([0.0, 0.0, 0.0], dtype=np.float_),
              "ts": gyms_core.Timestamp.new(0.0),
          }
      }
      assert space_match(observation_space, observation_match, ("observation",))

      observation: gyms_core.Observation = env.reset()
      assert action_observation_eq(observation, observation_match)

      # Now do some steps:
      if is_synchronous:
        no_action: gyms_core.Action = {}

        done: bool
        observation, _, done, _ = env.step(no_action)
        assert not done
        assert space_match(observation_space, observation,
                           ("observation",)), observation
        assert action_observation_eq(observation_match,
                                     observation), observation


class GymOracleEnv(reach_env.ReachEnv):
  """Configure a Gym environment with an oracle."""

  def __init__(self, is_synchronous: bool = True, **kwargs: Any) -> None:
    """Init GymOracleEnv."""
    pyreach_config: Dict[str, reach_env.ReachElement] = {
        "oracle":
            reach_env.ReachOracle(
                reach_name="robot",
                task_code="task_code",
                intent="intent",
                success_type="success_type",
                is_synchronous=is_synchronous)
    }

    mock_host: host.Host = host_mock.HostMock()
    assert isinstance(mock_host, host.Host)
    assert isinstance(mock_host, host_mock.HostMock)
    super().__init__(pyreach_config=pyreach_config, host=mock_host, **kwargs)


class GymOracleSyncEnv(GymOracleEnv):
  """Configure a Gym environment with a synchronous oracle."""

  def __init__(self, is_synchronous: bool = True, **kwargs: Any) -> None:
    """Init a synchronous oracle."""
    super().__init__(is_synchronous=is_synchronous, **kwargs)


class GymOracleAsyncEnv(GymOracleEnv):
  """Configure a Gym environment with a synchronous oracle."""

  def __init__(self, is_synchronous: bool = True, **kwargs: Any) -> None:
    """Init an asynchronous oracle."""
    super().__init__(is_synchronous=False, **kwargs)


class TestGymOracleEnv(unittest.TestCase):
  """Test the Gym OracleElement environments."""

  def test_asynchronous_oracle_register(self) -> None:
    """Test asynchronous Oracle registration."""
    self.oracle_register_test(is_synchronous=False)

  def test_synchronous_oracle_register(self) -> None:
    """Test synchronous Oracle registration."""
    self.oracle_register_test(is_synchronous=True)

  def oracle_register_test(self, is_synchronous: bool = True) -> None:
    """Test Gym OracleElement."""
    env_id_name: str = ("{0}synchronous_oracle_element_env-v0".format(
        "synchronous" if is_synchronous else "asynchronous"))
    class_name: str = (
        "GymOracle{0}Env".format("Sync" if is_synchronous else "Async"))
    entry_point: str = GYMS_PATH + "reach_env_test:" + class_name
    register(
        id=env_id_name,
        entry_point=entry_point,
        max_episode_steps=200,
        reward_threshold=25.0)

    env: Any
    with gym.make(env_id_name) as env:
      assert isinstance(env, gym.Env), env

      action_space: Any = env.action_space
      assert isinstance(action_space, gym.spaces.Space)
      action_match: Dict[str, Any] = {"oracle": {"request": 0}}
      assert space_match(action_space, action_match, ("action",))

      observation_space: Any = env.observation_space
      assert isinstance(observation_space, gym.spaces.Space)
      observation_match: Dict[str, Any] = {
          "oracle": {
              "request": 0,
              "pick_point": np.array([-1.0, -1.0]),
              "response": 0,
              "ts": gyms_core.Timestamp.new(0.0),
          }
      }
      assert space_match(observation_space, observation_match, ("observation",))

      observation: gyms_core.Observation = env.reset()
      assert action_observation_eq(observation, observation_match)

      assert gyms_core.get_int0(observation, "oracle.request") == 0
      assert gyms_core.get_int0(observation, "oracle.response") == 0
      assert gyms_core.get_float0(observation, "oracle.ts") == 0.0
      pick_point: np.ndarray
      pick_point = gyms_core.get_float1(observation, "oracle.pick_point")
      assert pick_point.dtype == np.float_
      assert pick_point.shape == (2,)


class GymServerEnv(reach_env.ReachEnv):
  """Class to test PyReach Gym Server Element."""

  def __init__(self, **kwargs: Any):
    """Init GymServerEnv."""
    pyreach_config: Dict[str, reach_env.ReachElement] = {
        "server": reach_env.ReachServer("server"),
    }
    mock_host: host.Host = host_mock.HostMock()
    assert isinstance(mock_host, host.Host)
    assert isinstance(mock_host, host_mock.HostMock)
    super().__init__(pyreach_config=pyreach_config, host=mock_host, **kwargs)


class TestGymServerEnv(unittest.TestCase):
  """Test GymServerEnv."""

  def test_register(self) -> None:
    """Test GymServerElement."""
    entry_point: str = GYMS_PATH + "reach_env_test:GymServerEnv"

    register(
        id="server_element_env-v0",
        entry_point=entry_point,
        max_episode_steps=200,
        reward_threshold=25.0)

    env: Any
    with gym.make("server_element_env-v0") as env:
      assert isinstance(env, gym.Env), env

      action_space: Any = env.action_space
      assert isinstance(action_space, gym.spaces.Space)
      action_match: Dict[str, Any] = {"server": {}}
      assert space_match(action_space, action_match, ("action",))

      observation_space: Any = env.observation_space
      assert isinstance(observation_space, gym.spaces.Space)
      observation_match: Dict[str, Any] = {
          "server": {
              "latest_ts": gyms_core.Timestamp.new(0.0),
              "server_ts": gyms_core.Timestamp.new(0.0),
          }
      }

      assert space_match(observation_space, observation_match, ("observation",))

      observation: Dict[str, Any] = env.reset()
      if "server" in observation and "server_ts" in observation["server"]:
        observation["server"]["server_ts"] = gyms_core.Timestamp.new(0.0)
      assert action_observation_eq(observation, observation_match)


class GymTextInstructionsEnv(reach_env.ReachEnv):
  """Configure a Gym environment with an textinstructions."""

  def __init__(self, is_synchronous: bool = True, **kwargs: Any) -> None:
    """Init GymTextInstructionsEnv."""
    pyreach_config: Dict[str, reach_env.ReachElement] = {
        "textinstructions":
            reach_env.ReachTextInstructions(
                reach_name="robot", is_synchronous=is_synchronous)
    }

    mock_host: host.Host = host_mock.HostMock()
    assert isinstance(mock_host, host.Host)
    assert isinstance(mock_host, host_mock.HostMock)
    super().__init__(pyreach_config=pyreach_config, host=mock_host, **kwargs)


class GymTextInstructionsSyncEnv(GymTextInstructionsEnv):
  """Configure a Gym environment with a synchronous textinstructions."""

  def __init__(self, is_synchronous: bool = True, **kwargs: Any) -> None:
    """Init a synchronous textinstructions."""
    super().__init__(is_synchronous=is_synchronous, **kwargs)


class GymTextInstructionsAsyncEnv(GymTextInstructionsEnv):
  """Configure a Gym environment with a synchronous textinstructions."""

  def __init__(self, is_synchronous: bool = True, **kwargs: Any) -> None:
    """Init an asynchronous textinstructions."""
    super().__init__(is_synchronous=False, **kwargs)


class TestGymTextInstructionsEnv(unittest.TestCase):
  """Test the Gym TextInstructionsElement environments."""

  def test_asynchronous_textinstructions_register(self) -> None:
    """Test asynchronous TextInstructions registration."""
    self.textinstructions_register_test(is_synchronous=False)

  def test_synchronous_textinstructions_register(self) -> None:
    """Test synchronous TextInstructions registration."""
    self.textinstructions_register_test(is_synchronous=True)

  def textinstructions_register_test(self, is_synchronous: bool = True) -> None:
    """Test Gym TextInstructionsElement."""
    env_id_name: str = "{0}_textinstructions_element_env-v0".format(
        "sync" if is_synchronous else "async")
    class_name: str = "GymTextInstructions{0}Env".format(
        "Sync" if is_synchronous else "Async")
    entry_point: str = GYMS_PATH + "reach_env_test:" + class_name
    register(
        id=env_id_name,
        entry_point=entry_point,
        max_episode_steps=200,
        reward_threshold=25.0)

    env: Any
    with gym.make(env_id_name) as env:
      assert isinstance(env, gym.Env), env

      action_space: Any = env.action_space
      assert isinstance(action_space, gym.spaces.Space)
      action_match: Dict[str, Any] = {"textinstructions": {}}
      assert space_match(action_space, action_match, ("action",))

      observation_space: Any = env.observation_space
      assert isinstance(observation_space, gym.spaces.Space)
      observation_match: Dict[str, Any] = {
          "textinstructions": {
              "instruction": 1024 * (0,),
              "ts": gyms_core.Timestamp.new(0.0),
          }
      }
      assert space_match(observation_space, observation_match, ("observation",))

      if is_synchronous:
        observation: gyms_core.Observation = env.reset()
        instruction: np.ndarray = gyms_core.get_int1(
            observation, "textinstructions.instruction")
        assert instruction.shape == (1024,)
        assert instruction.dtype == np.int64


class GymVacuumEnv(reach_env.ReachEnv):
  """Configure a Gym environment with an vacuum."""

  def __init__(self, is_synchronous: bool = True, **kwargs: Any) -> None:
    """Init GymVacuumEnv."""
    pyreach_config: Dict[str, reach_env.ReachElement] = {
        "vacuum":
            reach_env.ReachVacuum(
                reach_name="",
                is_synchronous=is_synchronous,
                vacuum_detect_enable=True,
                vacuum_gauge_enable=True)
    }

    mock_host: host.Host = host_mock.HostMock()
    assert isinstance(mock_host, host.Host)
    assert isinstance(mock_host, host_mock.HostMock)
    super().__init__(pyreach_config=pyreach_config, host=mock_host, **kwargs)


class GymVacuumSyncEnv(GymVacuumEnv):
  """Configure a Gym environment with a synchronous vacuum."""

  def __init__(self, is_synchronous: bool = True, **kwargs: Any) -> None:
    """Init a synchronous vacuum."""
    super().__init__(is_synchronous=is_synchronous, **kwargs)


class GymVacuumAsyncEnv(GymVacuumEnv):
  """Configure a Gym environment with a synchronous vacuum."""

  def __init__(self, is_synchronous: bool = True, **kwargs: Any) -> None:
    """Init an asynchronous vacuum."""
    super().__init__(is_synchronous=False, **kwargs)


class TestGymVacuumEnv(unittest.TestCase):
  """Test the Gym VacuumElement environments."""

  def test_asynchronous_vacuum_register(self) -> None:
    """Test asynchronous Vacuum registration."""
    self.vacuum_register_test(is_synchronous=False)

  def test_synchronous_vacuum_register(self) -> None:
    """Test synchronous Vacuum registration."""
    self.vacuum_register_test(is_synchronous=True)

  def vacuum_register_test(self, is_synchronous: bool = True) -> None:
    """Test Gym VacuumElement."""
    env_id_name: str = "{0}_vacuum_element_env-v0".format(
        "sync" if is_synchronous else "async")
    class_name: str = "GymVacuum{0}Env".format(
        "Sync" if is_synchronous else "Async")
    entry_point: str = GYMS_PATH + "reach_env_test:" + class_name
    register(
        id=env_id_name,
        entry_point=entry_point,
        max_episode_steps=200,
        reward_threshold=25.0)

    env: Any
    with gym.make(env_id_name) as env:
      assert isinstance(env, gym.Env), env

      action_space: Any = env.action_space
      assert isinstance(action_space, gym.spaces.Space)
      action_match: Dict[str, Any] = {"vacuum": {"state": 0}}
      assert space_match(action_space, action_match, ("action",))

      observation_space: Any = env.observation_space
      assert isinstance(observation_space, gym.spaces.Space)
      observation_match: Dict[str, Any] = {
          "vacuum": {
              "state": reach_env.ReachVacuumState.BLOWOFF,
              "vacuum_detect": 1,
              "vacuum_gauge": np.array(123.456),
              "ts": gyms_core.Timestamp.new(0.0),
          }
      }
      assert space_match(observation_space, observation_match, ("observation",))

      observation: gyms_core.Observation = env.reset()
      assert action_observation_eq(observation,
                                   observation_match), ("got_observation=",
                                                        observation,
                                                        "want_observation=",
                                                        observation_match)

      # Now do some steps:
      if is_synchronous:
        action_off: gyms_core.Action = {
            "vacuum": {
                "state": reach_env.ReachVacuumState.OFF
            },
        }

        done: bool
        observation, _, done, _ = env.step(action_off)
        assert not done
        assert space_match(observation_space, observation,
                           ("observation_off",)), observation
        assert action_observation_eq(observation_match,
                                     observation), observation


def space_match(space: gym.spaces.Space,
                action_observation: Any,
                where: Tuple[str, ...],
                exact: bool = True,
                fail_level: int = -1) -> bool:
  """Verify that an action/observation matches a corresponding Gym Space.

  Args:
    space: The Gym Space match:
    action_observation: The action observation data to match to space.
    where: A debugging tuple that is used when mismatches occur.
    exact: When True, a 1-to-1 match is required; otherwise dictionary matches
      may be partial.
    fail_level: The nesting level at which to force a failure.  Defaults: -1)

  Returns:
    True for a match and False otherwise.

  """
  assert isinstance(space, gym.spaces.Space), ("{0}: Not a space {1}".format(
      where, space))

  match: bool = False
  if (isinstance(space, gym.spaces.Box) and
      isinstance(action_observation, np.ndarray)):
    # Ugly: Using the internal implementation of gym.spaces.Box!
    space_shape: Tuple[int, ...] = space.shape
    assert isinstance(space_shape, tuple)
    action_observation_shape: Tuple[int, ...] = action_observation.shape
    match = space_shape == action_observation_shape
    return match

  if (isinstance(space, gym.spaces.Dict) and
      isinstance(action_observation, dict)):
    dict_space: gym.spaces.Dict = space
    # Ugly: Using the internal implementation of gym.spaces.Dict!
    dict_spaces: Any = dict_space.spaces
    assert isinstance(dict_spaces, collections.OrderedDict)

    def to_key_set(dictionary: Dict[str, Any], where: Tuple[str,
                                                            ...]) -> Set[str]:
      """Convert dictionary keys to a set of strings."""
      key: Any
      keys_set: Set[str] = set()
      for key in dictionary.keys():
        assert isinstance(key, str), f"{where}: key {1} is not a str"
        keys_set.add(key)
      return keys_set

    space_keys: Set[str] = to_key_set(dict_spaces, where)
    action_observation_keys: Set[str] = to_key_set(action_observation, where)
    all_keys: Set[str] = space_keys | action_observation_keys
    common_keys: Set[str] = space_keys & action_observation_keys
    differ_keys: Set[str] = all_keys - common_keys
    if exact:
      assert space_keys == action_observation_keys, (
          f"{where}: keys mismatch "
          f"{space_keys} != {action_observation_keys}: "
          f"differ:{differ_keys} "
          f"space={space} "
          f"observation={action_observation}")

    assert fail_level != 0, (
        f"space_keys={space_keys} "
        f"action_observation_keys={action_observation_keys} "
        f"all_keys={all_keys} "
        f"common_keys={common_keys} "
        f"differ_keys={differ_keys} "
        f"exact={exact} ")

    key: str
    for key in action_observation_keys:
      assert key in dict_spaces, f"{where}: Key '{key}' is not in space"
      sub_where: Tuple[str, ...] = where + (key,)
      sub_space: Any = dict_spaces[key]
      assert isinstance(sub_space,
                        gym.spaces.Space), f"{where}: Not a space {sub_space}"
      sub_action_observation: Any = action_observation[key]
      assert space_match(
          sub_space,
          sub_action_observation,
          sub_where,
          exact=exact,
          fail_level=fail_level - 1), (sub_space, "|", sub_action_observation)
    return True

  if (isinstance(space, gym.spaces.Discrete) and
      isinstance(action_observation, int)):
    return True

  if (isinstance(space, gym.spaces.MultiBinary) and
      isinstance(action_observation, tuple)):
    assert False, "{0}: not implemented".format(where)

  if (isinstance(space, gym.spaces.MultiDiscrete) and
      isinstance(action_observation, tuple)):
    # Ugly: Using the internal implementation of gym.spaces.Discrete!
    nvec: Any = space.nvec
    assert isinstance(nvec, np.ndarray), "type(nvec)={0}".format(type(nvec))
    assert len(nvec.shape) == 1, "nvec.shape={0}".format(nvec.shape)
    nvec_size: int = nvec.shape[0]
    assert nvec_size == len(action_observation), (
        "{0}: nvec.shape:{1} != len(action_observation):{2} ".format(
            where, nvec_size, len(action_observation)))
    index: int
    for index in range(nvec_size):
      assert isinstance(nvec[index],
                        np.int64), ("Invalid discrete [{0}]:{1}type={2}".format(
                            index, nvec[index], type(nvec[index])))
      assert isinstance(action_observation[index],
                        int), ("Invalid action_observation [{0}]:{1}".format(
                            index, action_observation[index]))
    return True

  if (isinstance(space, gym.spaces.Tuple) and
      isinstance(action_observation, tuple)):
    # Ugly: Using the internal implementation of gym.spaces.Tuple!
    tuple_spaces: Any = space.spaces
    assert isinstance(tuple_spaces, tuple)
    assert len(tuple_spaces) == len(action_observation), (
        "{0}: len(tuple_spaces):{1} != len(action_observation):{2}".format(
            where, len(tuple_spaces), len(action_observation)))
    match = True
    for index in range(len(tuple_spaces)):
      sub_where = where + ("[" + str(index) + "]",)
      sub_space = tuple_spaces[index]
      assert isinstance(sub_space, gym.spaces.Space), (
          "{0}: gym.spaces.Space not found".format(sub_where))
      sub_action_observation = action_observation[index]
      match &= space_match(sub_space, sub_action_observation, sub_where)
    return match

  assert False, "Unrecognized '{0}' space={1} action_observation={2}".format(
      where, type(space), type(action_observation))
  return False


def action_observation_eq(ao1: Any, ao2: Any, trace: str = "") -> bool:
  """Return True if two observations are equal."""
  next_trace: str = ""
  if trace:
    print(f"{trace}=>action_oberervation({ao1}, {ao2})")
    next_trace = trace + " "
  if isinstance(ao1, (int, float)) and isinstance(ao2, (int, float)):
    if trace:
      print(f"{trace}scalar:")
    if ao1 != ao2:
      if trace:
        print(f"{trace}{ao1} != {ao1}")
      return False
    return True
  if isinstance(ao1, tuple) and isinstance(ao2, tuple):
    if trace:
      print(f"{trace}tuple:")
    if len(ao1) != len(ao2):
      if trace:
        print(f"{trace}Tuple size Mismatch:len({ao1}) != len({ao2})")
      return False
    for i in range(len(ao1)):
      if not action_observation_eq(ao1[i], ao2[i], trace=next_trace):
        if trace:
          print(f"{trace}Tuple Mismatch:ao1[{i}] != ao2[{2}]")
        return False
    return True
  if isinstance(ao1, np.ndarray) and isinstance(ao2, np.ndarray):
    if trace:
      print(f"{trace}ndarray:")
    if ao1.shape != ao2.shape:
      if trace:
        print(f"{trace}shapes mismatch {ao1.shape} != {ao2.shape}")
      return False
    if ao1.dtype != ao2.dtype:
      if trace:
        print(f"{trace}dtypes mismatche{ao1.dtype} !+ {ao2.dtype}")
        return False
    if not ao1.shape:
      return ao1 == ao2
    if not (ao1 == ao2).all():
      if trace:
        print(f"{trace}Array Mismatch{ao1} != {ao2}")
      return False
    return True
  if isinstance(ao1, dict) and isinstance(ao2, dict):
    if trace:
      print(f"{trace}dict:")
    if set(ao1.keys()) != set(ao2.keys()):
      if trace:
        print(f"{trace}Dict Keys :{set(ao1.keys())} != {set(ao2.keys())}")
      return False
    for key in ao1.keys():
      if not action_observation_eq(ao1[key], ao2[key], trace=next_trace):
        if trace:
          print(f"{trace}key mismatch={key}")
        return False
    return True
  raise ValueError(f"type(ao1)={type(ao1)} type(ao2)={type(ao2)}")


if __name__ == "__main__":
  unittest.main()
