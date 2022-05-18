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

"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.duration_pb2
import google.protobuf.message
import google.protobuf.timestamp_pb2
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class SimulationCommand(google.protobuf.message.Message):
    """SimulationCommand controls a simulation session.

    A simulation session is initialized with a scene model and an initial
    timestamp (frequently zero).  It may be free-running or advanced by time
    increments.

    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor
    class Start(google.protobuf.message.Message):
        """Begins a simulation session."""
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        INITIAL_FIELD_NUMBER: builtins.int
        @property
        def initial(self) -> google.protobuf.timestamp_pb2.Timestamp:
            """Initial timestamp for simulation.
            Always specified in the simulation's own clock domain.
            """
            pass
        def __init__(self,
            *,
            initial: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["initial",b"initial"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["initial",b"initial"]) -> None: ...

    class Stop(google.protobuf.message.Message):
        """Ends a simulation session."""
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        def __init__(self,
            ) -> None: ...

    class Reset(google.protobuf.message.Message):
        """Stops simulation, reloads the previously loaded scene, resets time to the
        initial time.
        """
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        def __init__(self,
            ) -> None: ...

    class Advance(google.protobuf.message.Message):
        """Advances simulation time by a fixed amount."""
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        DURATION_FIELD_NUMBER: builtins.int
        TIMESTAMP_FIELD_NUMBER: builtins.int
        STEPS_FIELD_NUMBER: builtins.int
        @property
        def duration(self) -> google.protobuf.duration_pb2.Duration:
            """Advance simulation by duration."""
            pass
        @property
        def timestamp(self) -> google.protobuf.timestamp_pb2.Timestamp:
            """Advance simulation to timestamp.
            Always specified in the simulation's own clock domain.
            """
            pass
        steps: builtins.int
        """Advance by a number of fixed time steps."""

        def __init__(self,
            *,
            duration: typing.Optional[google.protobuf.duration_pb2.Duration] = ...,
            timestamp: typing.Optional[google.protobuf.timestamp_pb2.Timestamp] = ...,
            steps: typing.Optional[builtins.int] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["duration",b"duration","steps",b"steps","time",b"time","timestamp",b"timestamp"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["duration",b"duration","steps",b"steps","time",b"time","timestamp",b"timestamp"]) -> None: ...
        def WhichOneof(self, oneof_group: typing_extensions.Literal["time",b"time"]) -> typing.Optional[typing_extensions.Literal["duration","timestamp","steps"]]: ...

    class Run(google.protobuf.message.Message):
        """Starts simulation running freely."""
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        REAL_TIME_RATIO_FIELD_NUMBER: builtins.int
        MAX_SIMULATION_RUNTIME_FIELD_NUMBER: builtins.int
        MAX_REAL_RUNTIME_FIELD_NUMBER: builtins.int
        real_time_ratio: builtins.float
        """Desired ratio of simulation time to real time.
        For example, real_time_ratio=2  means run twice as fast as real time.
        If this value is omitted, simulation should run as fast as possible.
        """

        @property
        def max_simulation_runtime(self) -> google.protobuf.duration_pb2.Duration:
            """Maximum simulation time for simulation to run."""
            pass
        @property
        def max_real_runtime(self) -> google.protobuf.duration_pb2.Duration:
            """Maximum real time for simulation to run."""
            pass
        def __init__(self,
            *,
            real_time_ratio: typing.Optional[builtins.float] = ...,
            max_simulation_runtime: typing.Optional[google.protobuf.duration_pb2.Duration] = ...,
            max_real_runtime: typing.Optional[google.protobuf.duration_pb2.Duration] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["max_real_runtime",b"max_real_runtime","max_simulation_runtime",b"max_simulation_runtime","real_time_ratio",b"real_time_ratio"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["max_real_runtime",b"max_real_runtime","max_simulation_runtime",b"max_simulation_runtime","real_time_ratio",b"real_time_ratio"]) -> None: ...

    class Pause(google.protobuf.message.Message):
        """Pauses free running simulation."""
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        def __init__(self,
            ) -> None: ...

    class Load(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        SCENE_NAME_FIELD_NUMBER: builtins.int
        scene_name: typing.Text
        """Loads an entire scene, which can be named by this string or specified in
        configuration.
        """

        def __init__(self,
            *,
            scene_name: typing.Optional[typing.Text] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["scene_name",b"scene_name"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["scene_name",b"scene_name"]) -> None: ...

    class ClearWorld(google.protobuf.message.Message):
        """Removes all objects from the simulation and clears all data structures."""
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        def __init__(self,
            ) -> None: ...

    class Snapshot(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor
        SHAPSHOT_NAME_FIELD_NUMBER: builtins.int
        shapshot_name: typing.Text
        """Saves the current simulation state.  Simulation may be paused while this
        operation completes.
        """

        def __init__(self,
            *,
            shapshot_name: typing.Optional[typing.Text] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["shapshot_name",b"shapshot_name"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["shapshot_name",b"shapshot_name"]) -> None: ...

    START_FIELD_NUMBER: builtins.int
    STOP_FIELD_NUMBER: builtins.int
    RESET_FIELD_NUMBER: builtins.int
    ADVANCE_FIELD_NUMBER: builtins.int
    RUN_FIELD_NUMBER: builtins.int
    PAUSE_FIELD_NUMBER: builtins.int
    LOAD_FIELD_NUMBER: builtins.int
    CLEAR_WORLD_FIELD_NUMBER: builtins.int
    SHAPSHOT_FIELD_NUMBER: builtins.int
    @property
    def start(self) -> global___SimulationCommand.Start: ...
    @property
    def stop(self) -> global___SimulationCommand.Stop: ...
    @property
    def reset(self) -> global___SimulationCommand.Reset: ...
    @property
    def advance(self) -> global___SimulationCommand.Advance: ...
    @property
    def run(self) -> global___SimulationCommand.Run: ...
    @property
    def pause(self) -> global___SimulationCommand.Pause: ...
    @property
    def load(self) -> global___SimulationCommand.Load: ...
    @property
    def clear_world(self) -> global___SimulationCommand.ClearWorld: ...
    @property
    def shapshot(self) -> global___SimulationCommand.Snapshot: ...
    def __init__(self,
        *,
        start: typing.Optional[global___SimulationCommand.Start] = ...,
        stop: typing.Optional[global___SimulationCommand.Stop] = ...,
        reset: typing.Optional[global___SimulationCommand.Reset] = ...,
        advance: typing.Optional[global___SimulationCommand.Advance] = ...,
        run: typing.Optional[global___SimulationCommand.Run] = ...,
        pause: typing.Optional[global___SimulationCommand.Pause] = ...,
        load: typing.Optional[global___SimulationCommand.Load] = ...,
        clear_world: typing.Optional[global___SimulationCommand.ClearWorld] = ...,
        shapshot: typing.Optional[global___SimulationCommand.Snapshot] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["advance",b"advance","clear_world",b"clear_world","load",b"load","pause",b"pause","reset",b"reset","run",b"run","shapshot",b"shapshot","start",b"start","stop",b"stop","type",b"type"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["advance",b"advance","clear_world",b"clear_world","load",b"load","pause",b"pause","reset",b"reset","run",b"run","shapshot",b"shapshot","start",b"start","stop",b"stop","type",b"type"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["type",b"type"]) -> typing.Optional[typing_extensions.Literal["start","stop","reset","advance","run","pause","load","clear_world","shapshot"]]: ...
global___SimulationCommand = SimulationCommand