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
import frame_context_pb2
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import interval_pb2
import pose_pb2
import stats_pb2
import typing
import typing_extensions
import vector_pb2

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class CameraSpecification(google.protobuf.message.Message):
    """---------------------------------------------------------------------------
    Stats - Error statistics for calibration.

    Where error is represented as a Stats protobuf, the represented value is the
    per-pixel error of the metric.

    The average per-pixel scalar error will be saved in Stats.mean.
    The total error can be calculated as Stats.mean * Stats.count
    ---------------------------------------------------------------------------

    Specifications for an ideal camera.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    class ImageSpec(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        COLS_FIELD_NUMBER: builtins.int
        ROWS_FIELD_NUMBER: builtins.int
        CHANNELS_FIELD_NUMBER: builtins.int
        cols: builtins.int = ...
        """Dimensions and encoding type of camera images."""

        rows: builtins.int = ...
        channels: builtins.int = ...
        def __init__(self,
            *,
            cols : builtins.int = ...,
            rows : builtins.int = ...,
            channels : builtins.int = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["channels",b"channels","cols",b"cols","rows",b"rows"]) -> None: ...

    IMAGE_SPEC_FIELD_NUMBER: builtins.int
    FOV_FIELD_NUMBER: builtins.int
    CLIP_FIELD_NUMBER: builtins.int
    @property
    def image_spec(self) -> global___CameraSpecification.ImageSpec: ...
    @property
    def fov(self) -> vector_pb2.Vector2d:
        """Field of View in screen radians for width and height."""
        pass
    @property
    def clip(self) -> interval_pb2.Intervald:
        """Positive distance to near and far clip planes in meters.
        This is only used for rendering synthetic cameras as real cameras do not
        have clip planes.
        """
        pass
    def __init__(self,
        *,
        image_spec : typing.Optional[global___CameraSpecification.ImageSpec] = ...,
        fov : typing.Optional[vector_pb2.Vector2d] = ...,
        clip : typing.Optional[interval_pb2.Intervald] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["clip",b"clip","fov",b"fov","image_spec",b"image_spec"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["clip",b"clip","fov",b"fov","image_spec",b"image_spec"]) -> None: ...
global___CameraSpecification = CameraSpecification

class CameraIntrinsics(google.protobuf.message.Message):
    """Camera matrix and distortion parameters.

    https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
    https://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html
    Camera matrix:
       |  fx   0   cx |
       |   0  fy   cy |
       |   0   0    1 |
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    FX_FIELD_NUMBER: builtins.int
    FY_FIELD_NUMBER: builtins.int
    CX_FIELD_NUMBER: builtins.int
    CY_FIELD_NUMBER: builtins.int
    K1_FIELD_NUMBER: builtins.int
    K2_FIELD_NUMBER: builtins.int
    K3_FIELD_NUMBER: builtins.int
    K4_FIELD_NUMBER: builtins.int
    K5_FIELD_NUMBER: builtins.int
    K6_FIELD_NUMBER: builtins.int
    P1_FIELD_NUMBER: builtins.int
    P2_FIELD_NUMBER: builtins.int
    EXTRA_FIELD_NUMBER: builtins.int
    ERROR_STATS_FIELD_NUMBER: builtins.int
    CAMERA_SPEC_FIELD_NUMBER: builtins.int
    fx: builtins.float = ...
    """Focal length in x."""

    fy: builtins.float = ...
    """Focal length in y."""

    cx: builtins.float = ...
    """Center in x."""

    cy: builtins.float = ...
    """Center in y."""

    k1: builtins.float = ...
    """(x,y) are projected coordinates in the z=1 plane.

    f = (1 + k1r^2 + k2r^4 + k3r^6) / (1 + k4r^2 + k5r^4 + k6r^6)
    x' = x * f
    y' = y * f
    r^2 distortion coefficient.
    """

    k2: builtins.float = ...
    """r^4 distortion coefficient."""

    k3: builtins.float = ...
    """r^6 distortion coefficient."""

    k4: builtins.float = ...
    """Denominator coefficients.
    r^2 distortion coefficient.
    """

    k5: builtins.float = ...
    """r^4 distortion coefficient."""

    k6: builtins.float = ...
    """r^6 distortion coefficient."""

    p1: builtins.float = ...
    """x' += 2p1xy + p2(r^2 + 2x^2)
    y' += 2p2xy + p1(r^2 + 2y^2)
    y distortion coefficient.
    """

    p2: builtins.float = ...
    """x distortion coefficient."""

    @property
    def extra(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]:
        """Additional distortion parameters beyond k6."""
        pass
    @property
    def error_stats(self) -> stats_pb2.Stats:
        """Accumulated scalar error for intrinsics."""
        pass
    @property
    def camera_spec(self) -> global___CameraSpecification:
        """Camera specification includes image size in pixels and field-of-view
        angles.
        """
        pass
    def __init__(self,
        *,
        fx : typing.Optional[builtins.float] = ...,
        fy : typing.Optional[builtins.float] = ...,
        cx : typing.Optional[builtins.float] = ...,
        cy : typing.Optional[builtins.float] = ...,
        k1 : typing.Optional[builtins.float] = ...,
        k2 : typing.Optional[builtins.float] = ...,
        k3 : typing.Optional[builtins.float] = ...,
        k4 : typing.Optional[builtins.float] = ...,
        k5 : typing.Optional[builtins.float] = ...,
        k6 : typing.Optional[builtins.float] = ...,
        p1 : typing.Optional[builtins.float] = ...,
        p2 : typing.Optional[builtins.float] = ...,
        extra : typing.Optional[typing.Iterable[builtins.float]] = ...,
        error_stats : typing.Optional[stats_pb2.Stats] = ...,
        camera_spec : typing.Optional[global___CameraSpecification] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_cx",b"_cx","_cy",b"_cy","_fx",b"_fx","_fy",b"_fy","_k1",b"_k1","_k2",b"_k2","_k3",b"_k3","_k4",b"_k4","_k5",b"_k5","_k6",b"_k6","_p1",b"_p1","_p2",b"_p2","camera_spec",b"camera_spec","cx",b"cx","cy",b"cy","error_stats",b"error_stats","fx",b"fx","fy",b"fy","k1",b"k1","k2",b"k2","k3",b"k3","k4",b"k4","k5",b"k5","k6",b"k6","p1",b"p1","p2",b"p2"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_cx",b"_cx","_cy",b"_cy","_fx",b"_fx","_fy",b"_fy","_k1",b"_k1","_k2",b"_k2","_k3",b"_k3","_k4",b"_k4","_k5",b"_k5","_k6",b"_k6","_p1",b"_p1","_p2",b"_p2","camera_spec",b"camera_spec","cx",b"cx","cy",b"cy","error_stats",b"error_stats","extra",b"extra","fx",b"fx","fy",b"fy","k1",b"k1","k2",b"k2","k3",b"k3","k4",b"k4","k5",b"k5","k6",b"k6","p1",b"p1","p2",b"p2"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_cx",b"_cx"]) -> typing.Optional[typing_extensions.Literal["cx"]]: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_cy",b"_cy"]) -> typing.Optional[typing_extensions.Literal["cy"]]: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_fx",b"_fx"]) -> typing.Optional[typing_extensions.Literal["fx"]]: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_fy",b"_fy"]) -> typing.Optional[typing_extensions.Literal["fy"]]: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_k1",b"_k1"]) -> typing.Optional[typing_extensions.Literal["k1"]]: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_k2",b"_k2"]) -> typing.Optional[typing_extensions.Literal["k2"]]: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_k3",b"_k3"]) -> typing.Optional[typing_extensions.Literal["k3"]]: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_k4",b"_k4"]) -> typing.Optional[typing_extensions.Literal["k4"]]: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_k5",b"_k5"]) -> typing.Optional[typing_extensions.Literal["k5"]]: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_k6",b"_k6"]) -> typing.Optional[typing_extensions.Literal["k6"]]: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_p1",b"_p1"]) -> typing.Optional[typing_extensions.Literal["p1"]]: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_p2",b"_p2"]) -> typing.Optional[typing_extensions.Literal["p2"]]: ...
global___CameraIntrinsics = CameraIntrinsics

class CameraExtrinsics(google.protobuf.message.Message):
    """Pose of a camera in the world frame or with respect to a named object."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    WORLD_POSE_CAMERA_FIELD_NUMBER: builtins.int
    FRAME_CONTEXT_FIELD_NUMBER: builtins.int
    ERROR_STATS_FIELD_NUMBER: builtins.int
    @property
    def world_pose_camera(self) -> pose_pb2.Pose3d:
        """Places the camera at an absolute position in the world."""
        pass
    @property
    def frame_context(self) -> frame_context_pb2.FrameContextRelative:
        """Describes the camera pose relative to a, possibly moving, named frame of
        reference.
        """
        pass
    @property
    def error_stats(self) -> stats_pb2.Stats:
        """Accumulated scalar error for extrinsics."""
        pass
    def __init__(self,
        *,
        world_pose_camera : typing.Optional[pose_pb2.Pose3d] = ...,
        frame_context : typing.Optional[frame_context_pb2.FrameContextRelative] = ...,
        error_stats : typing.Optional[stats_pb2.Stats] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["error_stats",b"error_stats","extrinsic_type",b"extrinsic_type","frame_context",b"frame_context","world_pose_camera",b"world_pose_camera"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["error_stats",b"error_stats","extrinsic_type",b"extrinsic_type","frame_context",b"frame_context","world_pose_camera",b"world_pose_camera"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["extrinsic_type",b"extrinsic_type"]) -> typing.Optional[typing_extensions.Literal["world_pose_camera","frame_context"]]: ...
global___CameraExtrinsics = CameraExtrinsics

class CameraCalibration(google.protobuf.message.Message):
    """Total calibration data for a camera."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    INTRINSICS_FIELD_NUMBER: builtins.int
    EXTRINSICS_FIELD_NUMBER: builtins.int
    @property
    def intrinsics(self) -> global___CameraIntrinsics:
        """Intrinsics: image size, distortion, center, focal length"""
        pass
    @property
    def extrinsics(self) -> global___CameraExtrinsics:
        """Extrinsics: 3D position of the camera with orientation, may be relative."""
        pass
    def __init__(self,
        *,
        intrinsics : typing.Optional[global___CameraIntrinsics] = ...,
        extrinsics : typing.Optional[global___CameraExtrinsics] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["extrinsics",b"extrinsics","intrinsics",b"intrinsics"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["extrinsics",b"extrinsics","intrinsics",b"intrinsics"]) -> None: ...
global___CameraCalibration = CameraCalibration
