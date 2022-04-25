# PyReach Gym


## Introduction

The [OpenAI Gym](https://gym.openai.com/) API provides a standard way to
interface machine learning code with robot systems. The PyReach Gym API
translates from the Gym API to the lower level PyReach Host API. This document
assumes that you have some familiarity with the OpenAI Gym API.

The PyReach Gym is organized around PyReach Gym devices (e.g. arms, color
cameras, depth cameras, etc.) There can be multiple devices of the same type --
2 arms, multiple color cameras, etc. Each PyReach Gym device is given a unique
name (e.g. "left_arm", "right_arm", "left_color_camera", "right_color_camera",
"depth_camera", "vacuum", etc.)

For a different PyReach Gym environment, both the action and observation spaces
are organized as nested Gym Dict spaces. For both, the top Gym Dict space keys
are one-to-one with PyReach Gym device. The second level Dict spaces have keys
that are specific for the device.

An PyReach Gym action space would be organized as follows:

*   "left_arm":
    *   "command"
    *   "joint_angles"
    *   "pose"
    *   ...
*   "right_arm":
    *   "command"
    *   "joint_angles"
    *   "pose"
    *   ...
*   "color_camera" (no actions for color cameras)
*   "depth_camera" (no actions of depth cameras)
*   "vacuum":
    *   "command"

A PyReach Gym observation space has a very similar structure:

*   "left_arm":
    *   "status"
    *   "joint_angles"
    *   "pose"
    *   "ts"
*   "right_arm":
    *   "status"
    *   "joint_angles"
    *   "pose"
    *   "ts" *
*   "color_camera":
    *   "color":
    *   "ts"
*   "depth_camera":
    *   "color":
    *   "depth"
    *   "ts"
*   "vacuum":
    *   "status"
    *   "ts"

The definition of the observation/action spaces is taken care of by the PyReach
Gym environment configuration process. Most PyReach Gym users use an environment
that has been preconfigured by somebody else.

The basic code to use a PyReach Gym environment is shown below:

```python
import gym  # type: ignore

from google3.robotics.learning.reach.third_party.pyreach.gyms import gyms_core


def main():
  # Use a Python `with` statement to ensure the environment closes properly.

  with gym.make(“your_environment_name”) as env:

    # Your gym episode/step loops follows.
    for episode_i in range(10):
      # Each episode should start with a call to the `reset()` method.
      observation: gyms_core.Observation = env.reset()

      # The main body of your agent consists of a series of `step()` calls:
      for step_i in range(100):
        # Compute an action based on the latest observation.

        # Create an action dictionary.
        action: Action = {“arm”: …, “text_instructions”: …, ...}

        # Use `step()` to process the action and get the next observation
        # along with a reward (float), done (bool), and info (dict).
        observation, reward, done, info = env.step(action)
        if done:
          break

if __name__ == "__main__":
  main()
```

The PyReach Gym environment has the standard Gym properties:

*   `observation`: This is the observation for the current Gym step.
*   `reward`: This is reward amount achieved by the previous action.
*   `done`: This boolean flag indicates when it is time to initiate another
    reset().
*   `info`: This dict is a scratch pad dictionary for diagnostic and debugging
    purposes.

In addition, the PyReach Gym has an additional Gym property:

*   `task_params`: This is a dictionary of information about the current task.
    This is intended to be dictionary of key/value strings. A `PyReachError`
    exception is raised whenever non string keys and/or values are detected in
    this dictionary. The end user is allowed to add/modify/delete any key/value
    string pairs in this dictionary at any time.

    The initial contents of `task_params` is typically specified when the
    PyReach `ReachEnv` base class in initialized, using the `taskparams=`
    keyword. If this keyword is not specified an empty dictionary is used.

    The `task_params` dictionary is recorded to the execution logs whenever the
    environment is reset. In addition, both the PyReach Gym
    [Text Instructions Device](#text-instructions-device) and the
    [Task Device](#task-device) can be used to get `task_params` recorded into
    the execution logs. Please see these two devices for more information.

    The following two keys can be modified PyReach Gym:

    *   `reset_id`: Each time the environment is reset, a new uid string is
        generated.
    *   `agent_id`: This is a commonly used string task string identifier. This
        can be set using the `set_user_agent()` method. This method only sets
        the associated `agent_id` value and does nothing else.

## PyReach Gym Devices {#pyreach_gym_devices .numbered}

The PyReach Gym currently has the following devices:

*   [Annotation Device](#annotation-device): A pseudo device used to record
    client annotations to the logs.

*   [Arm Device](#arm-device): Represents a multi-jointed robot arm.

*   [Color Camera Device](#color-camera-device): Represents a color camera.

*   [Depth Camera Device](#depth-camera-device): Represents a depth camera.

*   [Force Torque Sensor Device](#force-torque-sensor-device): Represents a
    force/torque sensor attach to an end effector.

*   [I/O Device](#io-device): Represents a generic digital/analog input/output
    capability. Currently only digital output is implemented.

*   [Oracle Device](#oracle-device): A deprecated a way to run an machine
    learning algorithm locally on a robot.

*   [Server Device](#server-device): A device to provide information about the
    Reach Server state.

*   [Task Device](#task-device): A device for starting new tasks.

*   [Text Instructions Device](#text-instructions-device): A device for
    receiving text instructions.

*   [Vacuum Device](#vacuum-device): A device for a vacuum end-effector.

An overview of common PyReach Gym device characteristics is presented
immediately below, followed by a detailed discussion of each device.

A PyReach Gym can be configured to have zero, one or more the devices listed
above. Each device is given a unique string name (i.e. the device key). For
example, a robot assembly might consist of the following:

*   2 Robot arms (i.e. "left_arm" and "right_arm"),
*   2 Color cameras (i.e. "left_camera" and "right_camera"),
*   1 Depth camera (i.e. "depth_camera"),
*   1 Vacuum end effector (i.e. "vacuum").

In general, both a PyReach Gym action and observation are represented as double
nested `gym.spaces.Dict` objects. The first level of keys is one-to-one with the
device names configured the PyReach Gym environment (i.e. "left_arm",
"right_arm", "left_camera", etc.) The second level of keys corresponds PyReach
Gym to device specific information.

The OpenAI Gym architecture requires that an observation always fill in all the
fields it has been configured for. However, when it comes to the Gym action
space, the PyReach Gym allows for a sub-set of the keys to be provided. PyReach
Gym treats any action set key that is not present as "do nothing". The extreme
case of this occurs when you simply need a refreshed observation with no actions
required; this is done by simply passing in an empty action dictionary (i.e.
`new_observation = env.step({})`.) Gym implementations other PyReach Gym may not
be as tolerant with regards to incomplete action sets. One final note, is that
`env.actionspace.sample()` always returns a 100% complete randomized action
space (i.e. no fields are missing.)

There are 6 predefined Gym space types. The observations values that come back
for each Gym space are listed below:

*   gym.spaces.Box: Returns a `numpy.ndarray` of `float` or `int`s. There is a
    special case of returning a single `float`, which is always returned as a
    `numpy.ndarray` with a shape of `()` (i.e. the tuple of length 0.)

*   gym.space.Dict: Returns a `dict` of sub observations,

*   gym.space.Discrete: Returns a single bounded `int` from 0 to N-1, where N is
    the pre-configured upper bound.

*   gym.MultiBinary: Returns a tuple of `bool`s.

*   gym.MultiDiscrete: Return a `tuple` of `int`'s, where each is bound from 0
    to N-1, where N is configured separately for tuple index.

*   gym.Tuple: Returns a `tuple` of sub-observations.

Finally, every device observation has a field labeled `'ts'`. This contains an
`numpy.nddarray` of shape `()` that contains the observation time measured as a
`float` since January 1, 1970. These timestamp are taken locally on the computer
running the Reach server that is next to the robot assembly. This timestamp is
usually monotonically increasing, but sometimes the NTP (Network Time Protocol)
will adjust the Reach server time forward/backwards by a few seconds.

The sub-sections below describe each PyReach Gym device.

### Annotation Device

An annotation device is used to record arbitrary data into Gym logs.

The annotation device action space is a Dict with the following keys:

*   `"data"`: A multi-discrete list for values from 0 through to 256. The values
    0 through 255 represent a byte value. The value 256 means there is no byte
    value. The data must be padded with values of 256. The maximum length of
    data is specified when the annotation device is configured. The data must be
    the binary encoding of a proto buffer that is a ClientAnnotation. Gym
    wrappers may provide a utility function to encode a ClientAnnotation for
    loading into data. If this key is not present, it defaults to all 256 (i.e.
    empty data.) As a convenience, if the provided data is less that the maximum
    size (see `"maximum size"` in observation space.) It is padded with 256
    values to make it the correct size. If the provided data is too big, a
    `PyReachError` is raised.

*   `"disable"`: This is an unsigned 64-bit integer. If this value is non-zero,
    the annotation is *NOT* written. If it is zero, the annotation is written.
    The purpose of this field is to deal with env.sample() method which
    generates random values for the action space. This will pretty much prevent
    the `env.actions_space.sample()` method call from filling the log with
    random data, because the probability of a uniformly random 64-bit value
    being zero is vanishingly low.

    If this key is not present, it defaults to 0, which will cause the record to
    be recorded.

There is no annotation device observation space.

### Arm Device

The Arm action is a Dict with the following keys:

*   `"command"`: Must be specified as an integer where:

    *   0: Means do nothing. No `PyReachError` is raised if either the `pose` or
        `joint_angles` keys are present in the action.

    *   1: Means set the joint angles. The `"joint_angles"` key must be present
        when `"command"` is 1 and `PyReachError` is raised if the `"pose"` key
        is present.

    *   2: Means set the pose as modified by the `apply_tip_adjust_transform`
        option specified in the arm configuration. When
        `apply_tip_adjust_transform` is `True`, it is equivalent to command 4
        below; otherwise, it is equivalent to command 5 below.

    *   3: Means to immediately stop any arm motion that is already in progress.

    *   4: Means set the pose without applying the tool tip transform. The
        `pose` key must be present as an `np.ndarray` of the form (x, y, z, rx,
        ry, rz), where (x, y, z) specifies the final "wrist" position and (rx,
        ry, rz) specifies the final "wrist" pose using angle-axis format. In
        synchronous mode, the subsequent returned `pose` observation should be
        close to the `pose` passed in.

    *   5: Means set the pose applying the tool tip transform. The `pose` key
        must be present as an `np.ndarray` of the form (x, y, z, rx, ry, rz),
        where (x, y, z) specifies the final tip_ position and (rx, ry, rz)
        specifies the final tip pose using angle-axis format. In synchronous
        mode, the subsequent returned `tip_pose` observation should be close to
        the `pose` passed in.

    An value that is not between 0 and 5 inclusive is not allowed and results in
    a `PyReachError` exception.

*   `controller`: Specifies the controller to use. It is an index into an a list
    of controller names specified at configuration time. Typically, the first
    entry in this controller name list is the empty string which means "no
    controller". If not explicitly specified, the index defaults to 0. An index
    valid that exceeds the controller list bounds results in a `PyReachError`
    exception.

*   `"use_linear"`: Must be 1 to force a linear move; 0 allows a non-linear move
    is permitted. A value that is neither 0 nor 1 results in a `PyReachError`
    exception.

*   `"servo"`: Must be 1 to force a servo move; 0 allows a non-server move. A
    value that is neither 0 nor 1 results in a `PyReachError` exception.

*   `"servo_time_seconds"`: Specifies the blocking time (in seconds) for the arm
    when it is in servo mode (i.e. `servo` is specified as 1.) If specified, 0.0
    is the default. Currently this only works for UR arms. `servo` must be set
    to 1 to enable. A `PyReachError` is raised if `servo` is either not
    specified or is not set to 1.

*   `"servo_lookahead_time_seconds"`: Specifies the lookahead timing for
    trajectory smoothing for when the arm is in servo mode (i.e. `servo` is
    specified as 1.) If not specified, this defaults to 0.0. Currently this only
    works for UR arms. A `PyReachError` is raised if `servo` is either not
    specified or is not set to 1.

*   `"servo_gain"`: Specifies the gain for servoing. If 0.0, it defaults to
    300.0. If not specified, it defaults to 0.0 (which is turn defaults to
    300.0). Currently this only works for UR arms. A `PyReachError` is raised if
    `servo` is either not specified or is not set to 1.

*   `"velocity"`: Specifies the joints velocity limit in radians per second for
    each arm joint as a `numpy.ndarray`. If not present, there are joint angle
    velocity limits.

*   `"acceleration"`: Specifies a joints acceleration limit in radians per
    second squared.

*   `"synchronous"`: When set to 1, it specifies that synchronous arm movement
    needs to be performed when the arm is configured in asynchronous mode. If
    the arm is configured in synchronous mode, this value is ignored.

*   `"id"`: A unique `int` that identifies this action request. This value
    eventually shows up in the `"responses"` tuple (see below).

*   `"timeout"`: Specifies the timeout for any synchronous arm move. A negative
    timeout specifies that there is no timeout and a timeout of 0.0 specifies an
    immediate timeout (which is not very useful.) The timeout is ignored in
    asynchronous mode.

The observation is a Dict with the following values:

*   `"joint_angles"`: Specifies the arm joint angles in radians at the time of
    observation.

*   `"pose"`: Specifies the arm pose as 6 element linear `numpy.ndarray` that
    contains, (x, y, z, rx, ry, rz) where (x, y, z) is the arm position and (rx,
    ry, rz) is the pose in axis-angle format. This pose does **NOT** have the
    tool tip transform applied to it.

*   `tip_pose`: Specifies the arm pose as 6 element linear `numpy.ndarray` that
    contains, (x, y, z, rx, ry, rz) where (x, y, z) is the arm position and (rx,
    ry, rz) is the pose in axis-angle format. This pose **DOES** have the tool
    tip transform applied to it.

*   `tip_adjust`: Specifies the transform to get the `pose` to the `tip_pose` as
    a 6 element linear `numpy.ndarray` that contains (x, y, z, rx, ry, rz),
    where (x, y, z) is the tip position and (rx, ry, rz) is the tip pose ins
    axis-angle format. Until tool tip changing is implemented, this value will
    not change.

*   `"status"`: Specifies the arm status where:

    *   `0`: Means that no response is present yet.

    *   `1`: Means that the arm movement is successfully done.

    *   `2`: Means that the arm movement failed with an error other than
        timeout.

    *   `3`: Means that the arm movement was aborted.

    *   `4`: Means that the arm movement request was rejected.

    *   `5`: Means that the arm movement timed out.

    *   `6`: Means that the arm is in an Emergency-Stop condition.

    *   `7`: Means that the arm is in a Protective-Stop condition.

*   `"responses"`: {#arm-device-responses}

    When this is configured to be present, it specifies a `tuple` of responses,
    where each response is a `dict` with the following fields:

    *   `"id"`: Specifies the unique action space id that corresponds to this
        response.
    *   `"status"`: The standard arm status value (see immediately above)

    *   `"finished"`: specifies 0 if the arm operation is still taking place and
        1 otherwise.

    *   `"ts"`: Specifies the timestamp associated with the finished arm
        operation.

*   `"ts"`: The timestamp for the arm observation.

### Color Camera Device

The color camera device returns color images.

The color camera device currently has no action space.

The color camera observation space return the following:

*   `"color"`: The color image is returned as `numpy.ndarray` of `uint8`'s of
    shape `(W, H, 3)`. The pixels are in red, green blue order.

*   `"ts"`: The timestamp is returned as a scalar `numpy.ndarray` of type
    `float` and a shape of `()` (i.e. a tuple of length 0.)

If calibration is enabled, the observation has an additional key called
calibration `callibration` with the following items in its dictionary.

*   `distortion`: This is a Box Space of shape (5,) with ordered values for the
    OpenCV distortion model (i....e. k1, k2, p1, p2, k3.)

*   `distortion_depth`: This is a Box Space of shape (7,) with values of d1
    through d7. The adjusted depth is converted from raw 16-bit depth using
    following formula:

    ```
     adjusted_depth = d1 +
         raw_depth * d2 +
         x * d3 +
         y * d4 +
         x * y * d5 +
         x * raw_depth * d6 +
         y * raw_depth * d7
    ```

    The values of x and y are computed from the camera matrix, which is
    currently not available in the PyReachGym. The formulas for x and y are:

    ```
      x = (img_pt[0] - camera_matrix[0][2]) / camera_matrix[0][0]
      y = (img_pt[0] - camera_matrix[1][2]) / camera_matrix[1][1]
    ```

    In most cases, d3 through d7 are 0 and only d1 and d2 do anything. This
    means that the camera matrix is not needed, since d3 through d7 are 0.

*   `extrinsics`: This is a Box Space of shape (6,) that contains a pose in
    axis-angle format (i.e. (x, y, z, rx, ry, rz)).

*   `intrinsics`: This is a Box space of shape (4,) that matches OpenCV
    documentation (i.e. (fx, fy, cx, cy).

This observation must be explicitly enabled at Gym calibration time.

### Depth Camera Device

The depth camera device returns both color images and depth images.

The depth camera device currently has no action space.

The depth camera observation has the following observation space:

*   `color`: The color image is returned as a `numpy.ndarray` of `uint8`'s of
    shape `(W, H, 3)`. The pixels are in red, green blue order.

*   `depth`: The depth image is returned as a `numpy.ndarray` of `uint16`'s of
    shape `(W, H)`.

*   `"ts"`: The timestamp is returned as a scalar `numpy.ndarray` of type
    `float` and a shape of `()` (i.e. a tuple of length 0.)

If calibration is enabled, the observation has an additional key called
calibration `callibration` with the following items in its dictionary.

*   `distortion`: This is a Box Space of shape (5,) with ordered values for the
    OpenCV distortion model (i....e. k1, k2, p1, p2, k3.)

*   `distortion_depth`: This is a Box Space of shape (7,) with values of d1
    through d7. (Addition explanation is needed here.)

*   `extrinsics`: This is a Box Space of shape (6,) that contains a pose in
    axis-angle format (i.e. (x, y, z, rx, ry, rz)).

*   `intrinsics`: This is a Box space of shape (4,) that matches OpenCV
    documentation (i.e. (fx, fy, cx, cy).

### Force Torque Sensor Device

The force torque sensor device returns force and torque measurements for the arm
end effector. The relative position of this sensor with respect to the end
effector is currently not specified.

The force torque sensor device currently has no action space.

The force torque sensor observation has the following observation entries:

*   `"force"`: The force on the end effector is measured Newtons and is
    represented as a `numpy.ndarray` of `float`'s with a shape of `(3)`. This
    represents a tuple of (fx, fy, fz).

*   `"torque"`: The force on the end effector is measured Newtons-meters and is
    represented as a `numpy.ndarray` of `float`'s with a shape of `(3)`. This
    represents a tuple of (tx, ty, tz).

*   `"ts"`: The timestamp is returned as a scalar `numpy.ndarray` of type
    `float` and a shape of `()` (i.e. a tuple of length 0.)

Currently, there is no status information from the device being captured.
Thus, the sensor could be disabled, broken, inactive, with no visible
information in the returned observation.

### I/O Device

The I/O device provides the ability to access digital/analog input/output signal
wires. Currently, only digital output is specified.

The I/O device provides a two level Gym dictionary action space, where the first
level is `"digital_outputs"` and with a sub-dictionary space with one entry for
each named pin named in the device configuration (e.g. `"gym_pin_number1"`, ...,
`"gym_pin_numberN"`.)

Each value is a Gym multi-discrete that takes a value of 0, 1, or 2, where:

*   `0`: Sets the output to 0.

*   `1`: Sets the output to 1.

*   `2`: Leaves the output unchanged.

If the pin name is not included in the action space the pin output is left
unchanged. If the `"digital_outputs"` is not provided by the in the action
space, no digital outputs are changed. Thus, only the entries that need to
change need to be present.

The I/O device observation space is a three level nested Gym Dictionary space of
the form:

```
 "digital_output": {
     "gym_point_name1": {
         "value": True/False,
         "ts": timestamp,
     },
     # ...
     "gym_point_name1": {
         "value": True/False,
         "ts": timestamp,
     },
 }
```

The `"value"` space is Gym returned as a `numpy.ndarray` of type `bool` and a
shape of `()`. In other words, `True` or `False`. The `"ts"` space as is
returned as scalar `numpy.ndarray` of type `float` and a shape of `()`. In other
words, a `float` measured in seconds.

### Oracle Device

A deprecated a way to run an machine learning algorithm locally on a robot. No
further documentation is currently planned.

### Server Device

A server device provides additional information about the Reach Server state and
the observation.

There is action space for the server device.

A server device provides the following observation space:

*   `"latest_ts"`: The latest timestamp is returned as a scalar `numpy.ndarray`
    of type `float` and a shape of `()` (i.e. a tuple of length 0.) The latest
    timestamp is the maximum of all of the timestamps in the current
    observation.

This a utility function so you do not have to compute the maximum on your own.

### Task Device

The task device is a simple device to indicate when a new task has started.

This task device has an action space with the following entries:

*   `"action"`: Setting to this 1 starts new task, 2 stops a task, and 0 leaves
    the task in the current state. The `task_params` key/value pairs are
    recorded to the experiment logs whenever task transitions to/from being
    active. In other words, (START and not active) generates a start task entry
    and (STOP and active) generates an end task entry.

The task device has an observation space with the following entries:

*   `"active"`: This is a multi-binary space of length 1 that is `True` if a
    task is active and `False` otherwise.

Each time the a task is started or stopped, the entire environment `task_params`
dictionary is recorded into the execution logs.

The task device observation space is completely empty:

### Text Instructions Device

A text instruction device is used to get instructions for the next action to
perform.

This text instructions device has an action space with the following entries:

*   `"task_enable"`: When 1, the next text instruction is fetched for the next
    observation; otherwise, when 0, the previous text instruction is returned.
    Whenever, this entry changes its previous value in the in the previous
    action, the `task_params` dictionary is recorded in the experiment log.

The text instructions observation space has the following entries:

*   `"counter"`: This is value is incremented whenever a new text instruction is
    obtained. The purpose of this counter is to detect the same text instruction
    is sent twice in a row.

*   `"instruction"`: The instruction encoded as a 1024 `numpy.ndarray` of shape
    (1024) of `uint8`'s. The instruction is encoded in UTF-8 format and with 0
    for unused entries in the 1024 entry array.

*   `"ts"`: The timestamp is returned as a scalar `numpy.ndarray` of type
    `float` and a shape of `()` (i.e. a tuple of length 0.)

### Vacuum Device

The vacuum device has evolved over time. Not all robot cells implement all of
the vacuum features. In general, there is a suction tip end effector that
usually has a rubberized seal on the end. The vacuum device can either engage
the vacuum to suck an object onto the end effector or engage blow off to force
the object off the end effector.

In addition there are two other sensors:

*   vacuum_gauge: This is an analog sensor that measures the pressure inside of
    the end effector suction tube. This is measured in inverse Pascals where 0.0
    means 1 atmosphere and 101325.0 is a hard vacuum.

*   vacuum_state: This is a binary sensor the is on or off depending upon when
    the pressure is above or below a manually set threshold. The sensor returns
    true, when the tube pressure is below the threshold to indicate that the end
    effector has enough suction to pick up an object; conversely, it is false if
    the pressure is above the threshold suggesting that now seal on the object
    has occurred yet.

The action space currently only has the following entries:

*   `"state"`: Sets the desired state of the Vacuum device. It may have one of
    the following values:

    *   `0`: Off.

    *   `1`: Vacuum on.

    *   `2`: Blow off.

Depending on the vacuum device configuration, the observation state will have
zero, one or more of these entries:

*   `"state"`: There are two electrical outputs, one that activates vacuum and
    another that activates blowoff. Only one or the other is allowed to be
    activated at the same time. As a sanity check these two signals are read
    back in and converted into `0` for off, `1` for on, and `2` for blow off. In
    general, `state` value set in the action space will be reflected here.
    However, it is not instantaneous and it may take an extra observation. This
    entry is set by the `state_enable` configuration option. This observation is
    mostly for completeness and many Gym environments will choose to disable
    this particular observation space entry.

*   `vacuum_detect`: The threshold sensor value that returns 1 if the suction
    suggests that the end-effector has sealed adequately to the surface of an
    object; otherwise 0. This enabled/disabled by the `vacuum_detect_enable`
    configuration option.

*   `vacuum_gauge`: The vacuum pressure when the vacuum is engaged. This is
    measured in inverse Pascals where 0.0 means 1 atmosphere and 101325.0 is a
    hard vacuum. -1.0 is returned if the no valid vacuum pressure is present.
    This observation state is only available if it has been enabled in the using
    the `vacuum_gauge_enable` vacuum device configuration.

*   `"ts"`: The timestamp is returned as a scalar `numpy.ndarray` of type
    `float` and a shape of `()` (i.e. a tuple of length 0.)

## Environment Configuration

In general, the goal is to configure an environment that matches one or more
physical robot assemblies. If there are multiple physical assemblies, the goal
should be allow researcher to treat them interchangeably. The means that the
arms, sensor, and actuators should be configured to be in the same locations,
camera, resolutions. If there are additional artifacts (blocks, trays, bins,
etc.) mounted to the robot assembly, they should be interchangeable as well.

Configuring an environment for PyReach Gym is broken into the sections below:

1.  [Synchronous vs. Asynchronous](#synchronous-vs-asynchronous)

2.  [Environment Setup Module](#environment-setup-module)

3.  [Environment Registration](#environment-registration)

4.  [Environment Example](#environment-example)

5.  [Device Configuration](#device-configuration)

### Synchronous vs Asynchronous

There is an overall concept to the Gym about whether it is behaving in a
synchronous vs. asynchronous mode:

*   synchronous mode: In synchronous mode, the observations are delayed until
    after all of the requested actions are complete. For example, when an arm
    move is requested, it must be stopped at the requested position before, and
    next observation is taken.

*   asynchronous mode: In asynchronous mode, the next observation is performed
    immediately without waiting any requested action to complete. For an arm, it
    may still be moving while the next observation is occurring.

Most device configurations have an optional argument called `is_synchronous`.
This flag defaults to `False` if it is not specified as a keyword argument. When
this flag is explicitly set to `True`, it configures the PyReach Gym to treat
the given device as synchronous. Any time a PyReach Gym device has this flag is
explicitly set to `True` ***AND*** an action is requested of the device, the
next Gym observation is delayed until the action is complete. If more than one
device is configured in `is_synchronous` mode, all requested actions (i.e. move
two arms) must be done before the next observation is taken.

In general, whether a device is synchronous or asynchronous is decided at
configuration time. The arm device is an exception that it be configured to be
asynchronous most of the time, but temporarily put into synchronous mode for the
duration of arm operation. This is done by setting the `synchronous` flag for
the arm action set to 1. Further discussion of this arm feature is deferred
until [Arm Device Configuration](#arm-configuration)

In general, read-only device like color/depth cameras, force/torque sensor, text
instructions, etc., work best when they are in asynchronous mode. The reason for
this, is when they are in asynchronous mode, they are put into an opportunistic
"streaming mode", where they continuously generate observation information
(usually images.) This information is cached by the lower level PyReach host
layer. When the last requested operation completes (e.g. move an arm), there is
an good chance that an image with a timestamp after operation complete is
already present. If not, the next image should already be underway. Synchronous
image requests tend to be slower than asynchronous requests. That being said,
the PyReach Gym cameras work perfectly well in synchronous mode.

### Environment Setup Module

In order to encourage people to share robot assemblies, people are encouraged to
insert their robot configurations into the `.../pyreach/gyms/envs/` directory.
Getting a simulator that matches the physical robot is also desirable.

The overall structure of a configuration file is:

```python
"""Module comment goes here."""

from typing import Any, Dict, List, Tuple  # and any other type hints

from pyreach.gyms import pyreach core
from pyreach.gyms import pyreach reach_env

class DescriptiveNameEnv(reach_env.ReachEnv):
  """A short class description."""

  def __init__(self, **kwargs: Any) -> None:
    """Init DescrptioneNameEnv."""

    # Required:
    pyreach_config: Dict[str, reach_env.ReachElement] = {
        "arm": reach_env.ReachArm("", ...),
        "color": reach_env.ReachColorCamera("", ...),
        "depth": reach_env.ReachDepthCamera("", ...),
        # ...
        "vacuum": reach_env.Vacuum("", ...),
        "server": reach_env.Server(...),
    }

    # Required, but may be empty:
    task_params: Dict[str, str] = {
        "id1": "value1",
        # ...
    }

    # Required:
    super().__init__(
        pyreach_config=pyreach_config,
        task_params=task_params,
        timeout=15.0,  # Generic time value in seconds
        **kwargs)
```

The key data structure is the `pyreach_config` dictionary. This is where each of
the PyReach Gym devices are configured.

Each PyReach Gym device has two names:

*   PyReach Gym Device Name: The device name used by PyReach Gym. This must be
    unique and non-empty string. These names are used as top level keys for the
    both the action and observation space dictionaries.

*   Reach Device Name: This is the device name that has been assigned to the
    device by the Reach Server. It is quite common for this string to be empty
    one there is only one instance of a given device (i.e. only one arm, only
    one depth camera, etc.)

In the code example above, the PyReach Gym Device names are the dictionary keys
and the reach_device names are always the first positional argument (except for
`reachenv.ReachServer` which is a pseudo device.)

In addition, there is an attribute/value dictionary called `task_params`, that
gets passed into ReachEnv super class initializer.

Lastly, the Gym API encourages a `**kwargs` argument be passed through.
`task_params` is meant to be used by Reach and `**kwargs` is mean for additional
configurations appropriate to the environment. PyReach Gym does not use anything
in `kwargs`, but it does use values in `task_params`.

The specific details for configuring each PyReach Gym device are located in the
[Device Configuration](#device-configuration) section below.

### Environment Registration

The Gym architecture has a unified structure for registering environments. This
is done using the file
`google3.robotics.learning.reach.third_party.pyreach.__init__`.

For each new gym environment a call to `register()` must be made in this file.
The format of the call is:

```python
register(
    id="name-v###",
    entrypoint='google3.robotics.learning.reach.third_party.pyreach.gyms.envs.pyreach_gym_example:YourEnvName",
    max_episode_steps=200",  # Your choice here
    reward_threshold=1234.5679,  # Your choice here.
)
```

The 4 fields are:

*   `id`: This is a Gym environment id. The overall goal is that these names be
    fairly unique, so longer names tend to be encouraged. The Gym API also
    enforces that there be a version number, which is positive number (either a
    `float` or an `int`.) Each time you make an incompatible change in the
    configuration, you are encouraged to change this version number. Whenever a
    new PyReachGym device is added, the fractional part of the version should be
    incremented. When a device is removed, or a major changes is made to the
    configuration, the integer portion should be incremented. Realistically,
    most environment remain at `...-v0` and never get changed.

*   `entrypoint`: The entry point is the full Google3 path to the `gyms/envs/`
    directory followed by the class name for the new environment. Please note,
    making a typo in the `entrypoint` string results in a Python exception from
    deep within the `load` module.

*   `max_episode_steps`: This is maximum number of calls to `step()` before the
    Gym will automatically terminate the episode. (This is done by setting the
    `done` value returned from `step()` to `True`.

*   `max_reward_threshold`: Each call to `step()` returns a reward value.
    Whenever this running sum of all reward values exceed this threshold, the
    current episode is terminated by setting `done` to `True`.

### Environment Example

There are several environments in
`google3.robotics.learning.reach.third_party.pyreach.gyms.envs/`. One of
smallest examples is in `pyreach_gym_example`. The entire example is shown
immediately below, followed detailed discussion of the code. Please skim the
code immediately below to get a feel for what is going on.

```python
"""A basic singulation Gym environment used as an example."""

from typing import Any, Dict, List, Tuple

from pyreach.gyms import pyreach reach_env


class PyReachGymExampleEnv(reach_env.ReachEnv):
  """An OpenAI PyReach Gym Example Environment."""

  def __init__(self, **kwargs: Any):
    """Initialize the Singulation environment."""
    center_joint_angles: List[float] = [5.06, -1.66, -1.57, -1.10, 1.7, 0.0]
    low_joint_angles: Tuple[float, ...] = tuple(
        [cja - 0.1 for cja in center_joint_angles])
    high_joint_angles: Tuple[float, ...] = tuple(
        cja + 0.1 for cja in center_joint_angles)
    timeout: float = 15.0

    pyreach_config: Dict[str, reach_env.ReachElement] = {
        "arm":
            reach_env.ReachArm(
                "", low_joint_angles, high_joint_angles, is_synchronous=True),
        "camera":
            reach_env.ReachColorCamera(
                "", (772, 1032), force_fit=True, is_synchronous=True),
        "depth_camera":
            reach_env.ReachDepthCamera(
                "", (720, 1280), True, force_fit=True, is_synchronous=True),
        "server":
            reach_env.ReachServer("Server"),
        "text_instruction":
            reach_env.ReachTextInstructions("text", is_synchronous=True),
        "vacuum":
            reach_env.ReachVacuum(""),
    }

    task_params: Dict[str, str] = {
        "task_code": "122",
        "success_type": "vacuum-pressure-sensor"
    }

    super().__init__(
        pyreach_config=pyreach_config,
        task_params=task_params,
        timeout=timeout,
        **kwargs)
}
```

The code starts with some standard boiler plate:

```python
"""A basic singulation Gym environment used as an example."""

from typing import Any, Dict, List, Tuple

from pyreach.gyms import reach_env
```

In general, PyReach Gym extensively uses Python type hints. While type hints are
encouraged, they are not required. The `pyreach/gyms/reach_env.py` module
currently contains the entire PyReach Gym code base. While this may change in
the future, the intention is that all of the top level classes are always
defined in this module.

Any custom environment needs to sub-class from `reach_env.ReachEnv`, which (in
turn) is a subclass of the OpenAI `gym.Env` class.

```python

class PyReachGymExampleEnv(reach_env.ReachEnv):
  """An OpenAI PyReach Gym Example Environment."""
```

The class name traditionally ends with `...Env`. There is no particular need to
prefix the path name with `PyReachGym`. Example other names are
`BenchmarkFoldingEnv`, `Benchmark2DFoldingEnv`. `KittingBenchMarkEnv`, etc.

The meat of the configuration class is in the `__init__()` method.

```python

  def __init__(self, **kwargs: Any):
    """Initialize the Singulation environment."""
```

The OpenAI `gym.Env` class `__init__()` method expects a `**kwargs` argument.
So, your `__init__()` method should probably have one as well.

The PyReach Gym Arm configuration is typically configured with high/low joint
angle limits. However, this is not a requirement. The reason for this is because
many example use call `env.action_space.sample()` to get randomized set of
values. Frequently the random values can cause the arm to crash into something
and crash. The joint angles avoid the arm crashes.

```python

    center_joint_angles: List[float] = [5.06, -1.66, -1.57, -1.10, 1.7, 0.0]
    low_joint_angles: Tuple[float, ...] = tuple(
        [cja - 0.1 for cja in center_joint_angles])
    high_joint_angles: Tuple[float, ...] = tuple(
        cja + 0.1 for cja in center_joint_angles)
```

`timeout` is used to specify the maximum timeout for the top level `gym.env`
class. It can be defined pretty much anywhere.

```python
    timeout: float = 15.0
```

The meat configuration is the `pyreach_config` dictionary of
`reach_env.ReachElement`'s. In this document, `reach_env.ReachElement` is
synonymous with PyReach Gym device. All PyReach Gym devices sub-class from
`reach_env.ReachElement`.

```python
    pyreach_config: Dict[str, reach_env.ReachElement] = {
```

Each element is given a unique dictionary key that is descriptive. The
dictionary value is a sub-class `reach_env.ReachElement`. The first argument is
always the associated name of the associated device at the PyReach Host API
level. The remaining arguments vary from device to device.

```python
        "arm":
            reach_env.ReachArm(
                "", low_joint_angles, high_joint_angles, is_synchronous=True),
        "camera":
            reach_env.ReachColorCamera(
                "", (772, 1032), force_fit=True, is_synchronous=True),
        "depth_camera":
            reach_env.ReachDepthCamera(
                "", (720, 1280), True, force_fit=True, is_synchronous=True),
        "server":
            reach_env.ReachServer("Server"),
        "text_instruction":
            reach_env.ReachTextInstructions("text", is_synchronous=True),
        "vacuum":
            reach_env.ReachVacuum(""),
    }
```

`task_params` is an example of a `**kwargs` argument that is passed through to
the underlying `gym.Env.__init__()`. These values are typically used by one of
the many OpenAI Gym wrapper environments.

```python
    task_params: Dict[str, str] = {
        "task_code": "122",
        "intent": "pick",
        "success_type": "vacuum-pressure-sensor"
    }
```

Finally, the `reach_env.ReachEnv` super class in initialized. Both
`pyreach_config` and `**kwargs` should be specified.

```python
    super().__init__(
        pyreach_config=pyreach_config,
        task_params=task_params,
        timeout=timeout,
        **kwargs)
}
```

With that walk through, it should be possible to read the other environment
configurations in the `.../pyreach/gyms/envs/` directory.

### Device Configuration

Each device configuration is described in a separate section below:

*   [Annotation Configuration](#annotation-configuration): Configure an
    Annotation device.

*   [Arm Configuration](#arm-configuration): Configure an Arm device.

*   [Color Camera Configuration](#color-camera-configuration): Configure a Color
    Camera device.

*   [Depth Camera Configuration](#depth-camera-configuration): Configure a Depth
    Camera device.

*   [I/O Configuration](#io-configuration): Configure a the signal I/O device.

*   [Force Torque Sensor Configuration](#force-torque-sensor-configuration):
    Configure a Force Torque Sensor device.

*   [Oracle Configuration](#oracle-configuration): Configure the deprecated
    Oracle device.

*   [Server Configuration](#server-configuration): Configure a Reach Server
    pseudo device.

*   [Task Configuration](#task-configuration): Configure a Task device.

*   [Text Instructions Configuration](#text-instructions-configuration):
    Configure a Text Instructions device.

*   [Vacuum Configuration ](#vacuum-configuration): Configure a Vacuum device.

#### Annotation Configuration

The [`Arm Device`](#arm-device) device is initialized with the following
arguments:

*   `reach_name`: (Required) The reach server name of the annotation device.
    This can be an empty string.

*   `maximum_size`: (Required) The maximum number of entries in the data field.

*   `is_synchronous`: (Optional, default = `False`) If `True`, the annotation is
    processed synchronously; otherwise it occurs asynchronously. (For further
    details see [Synchronous vs. Asynchronous](#synchronous-vs-asynchronous) ).

#### Arm Configuration

The [`Arm Device`](#arm-device) device is initialized with the following
arguments:

*   `reach_name`: (Required) The reach server name of the arm. This can be an
    empty string.

*   `controllers`: (Option, default `("",)`) A list of controller names that are
    available for use. The empty string means "no controller". By tradition the
    first entry is the empty string, but this in not required.

*   `is_synchronous`: (Optional, default = `False`) If `True`, the arm is always
    moved synchronously; otherwise it is *usually* moved asynchronously. (For
    further details see
    [Synchronous vs. Asynchronous](#synchronous-vs-asynchronous) ).

*   `low_joint_angles`: (Optional, default = `()`) A list of minimum joint
    angles measured in radians for each arm joint. Any arm joint angles that are
    below these limits are forced up to these values.

*   `high_joint_angles`: (Optional, default = `()`) A tuple of maximum joint
    angles measured in radians for each arm joint. Any arm joint angles that are
    below these limits are forced down to these values.

*   `apply_tip_adjust_transform`: (Optional, default = `False`) If `True`, the
    pose position is offset by the tip transform. (TDOO: specify where tip
    transform is.)

*   `response_queue_length`: (Optional, default = 0) When positive, the PyReach
    Gym returns the last N arm status values for asynchronous moves. See the
    [`"responses"` observation entry](#arm-device-responses) for
    [Arm Device](#arm-device).

*   `ik_lib`: (Optional, default = None) Specifies whether to use IKFast or IK
    PyBullet for inverse kinematics.xo

*   `e_stop_mode`: (Optional, default = 0) Specifies the Gym behavior when an
    emergency stop occurs. 0 specifies that a `PyreachError` will be raised. 1
    specifies that a the gym will immediately terminate by setting the Done flag
    returned from `step()` to `True`. 2 specifies that the arm status will
    indicate an E-stop condition.

*   `p_stop_mode`: (Optional, default = 0) Specifies the Gym behavior when an
    protective stop occurs. 0 specifies that a `PyreachError` will be raised. 1
    specifies that a the gym will immediately terminate by setting the Done flag
    returned from `step()` to `True`. 2 specifies that the arm status will
    indicate an P-stop condition.

#### Color Camera Configuration

The [`Color Camera Device`](#color-camera-device) is initialized with the
following arguments:

*   `reach_name`: (Required) The reach server name of the color camera. This
    name must match the name used by the remote robot host (e.g. "uvc", ...)
    Sometimes the reach server configures the primary color camera with an empty
    string.

*   `is_synchronous`: (Optional, default = `False`) If `True`, all image
    requests for this device are made synchronously.

*   `shape`: (Required) This specifies the shape of the returned image as (dx,
    dy) The ndarray shape is extended to (dx, dy, 3). The pixel values are
    `uint8` in red, green, blue order.

*   `force_fit`: (Optional, default = `False`) If `True`, any mis-configured
    cameras are simply cropped to specified `shape`. If `False`, a
    `PyReachError`is raised for an image shape mismatch detected.

*   `calibration_enable`: (Optional, default = `False`) If `True`, calibration
    information is added to the Color Camera observation space.

*   `lens_model`: (Optional, default = `None`). If calibration is enabled, this
    needs to specified as either `"fisheye"` or `"pinhole"`. Any other values
    will raise `PyReachError`. This value is used as a consistency check to
    ensure that it matches the lens model returned from calibration. If they do
    not match, there is almost certainly some sort of configuration error that
    needs to be resolved.

*   `link_name`: (Optional, default = `None`). The link name in the robot URDF
    model used to for the camera location is specified. This value is used as a
    consistency check to ensure that it matches the lens model returned from
    calibration. If they do not match, there is almost certainly some sort of
    configuration error that needs to be resolved.

#### Depth Camera Configuration

The [`Reach Depth Camera Device`](#depth-camera-device) is initialized with the
following arguments:

*   `reach_name`: (Required) The reach server name of the color camera. This
    name must match the name used by the remote robot host (e.g. "photoneo",
    "realsense", ...) Sometimes the reach server configures the primary depth
    camera with an empty string.

*   `is_synchronous`: (Optional, default = `False`) If `True`, all image
    requests for this device are made synchronously.

*   `shape`: (Required) This specifies the shape of the returned image as (dx,
    dy) The pixel values are uint16.

*   `color_enabled`: If `True`, color images are enabled. The
    `numpy.ndarray`shape is same as the depth camera shape (i.e. (dx, dy, 3).)
    The pixel values are `numpy.uint8`.

*   `force_fit`: (Optional, default = `False`) If `True`, any misconfigured
    cameras are simply cropped to specified `shape`. If `False`, a
    `PyReachError`is raised for an image shape mismatch detected.

*   `calibration_enable`: (Optional, default = `False`) If `True`, calibration
    information is added to the Color Camera observation space.

*   `lens_model`: (Optional, default = `None`). If calibration is enabled, this
    needs to specified as either `"fisheye"` or `"pinhole"`. Any other values
    will raise `PyReachError`. This value is used as a consistency check to
    ensure that it matches the lens model returned from calibration. If they do
    not match, there is almost certainly some sort of configuration error that
    needs to be resolved.

*   `link_name`: (Optional, default = `None`). The link name in the robot URDF
    model used to for the camera location is specified. This value is used as a
    consistency check to ensure that it matches the lens model returned from
    calibration. If they do not match, there is almost certainly some sort of
    configuration error that needs to be resolved.

#### Force Torque Sensor Configuration

This device represents a force/torque sensor attach to an end effector.

The [`Force Torque Sensor Device`](#force-torque-sensor-device) is initialized
with the following arguments:

*   `reach_name`: (Required) The reach server name of the force torque sensor..
    This name must match the name used by the Reach server.

*   `is_synchronous`: (Optional, default = `False`) If `True`, all image
    requests for this device are made synchronously; otherwise, they are made
    asynchronously.

#### I/O Configuration

This device provides the ability to perform read and/or modify I/O pins.
Currently, only digital output us supported. The [`I/O Device`](#io-device) is
initialized with the with a dictionary of the following structure:

```
 {
     "io":
          io_element.ReachIO(
              reach_name="reach_io_device_name",
              is_synchronous=True/False,  # synchronous/asynchronous IO device
              digital_outputs={  # One dict entry for each digital output
                  "gym_digital_output1":
                      io_element.ReachDigitalOutuput(
                          reach_name="",
                          capability_type="",
                          pin_name="")
                  # ...
                  "gym_digital_outputN":
                      io_element.ReachDigitalOutuput(
                          reach_name="",
                          capability_type="",
                          pin_name="")
              )}
              # digital_inputs={...}  # Not implemented yet
              # analog_outputs={...}  # Not implemented yet
              # analog_inputs={...}  # Not implemented yet
 }
```

when the action space is filled in, it will look as follows:

```
    action["io"]["digital_outputs"] = {
       "digital_output1": 0,  # Turn off,
       "digital_outputN": 1,  # Turn on,
    }
```

The three values fed into the `io_element.ReachDigitalOutput` are:

*   `reach_name`: The name of the controller that is managing the I/O. This is
    frequently the same name as the Arm name, but not always.

*   `capability_type`: The capability type string for the pin. This is specifie
    by the robot configuration and is supplied by the operation team.

*   `reach_pin_name`: The specific pin name for the capability. Again, this is
    specified by the robot configuration and is supplied by the operation team.

In practice, trying to the correct values for these 3 strings can be quite
challenging. A useful trick/hack is to specify random strings for these three
strings. The I/O will complain about ones that are incorrect *AND* provide a
list of value values. Thus, tremendously simplifies the task of trying to figure
what values to used.

Eventually, as other I/O types show up, additional top level configuration
dictionary enteries are anticipated (e.g. `digital_inputs`, etc.)

#### Oracle Configuration

A deprecated a way to run an machine learning algorithm locally on a robot. No
further documentation for the configuration of this device is currently planned.

#### Server Configuration

This is a pseudo device that provides additional information about the PyReach
Gym. It currently, provides a single convenience observation -- `"latest_ts"`,
but it is likely that additional features will be added as needed.

The [`Server Device`](#server-device) is initialized with the following
arguments:

*   `reach_name`: (Required) This argument is required to be consistent with the
    other device configuration routines. It is ignored.

*   `is_synchronous`: (Optional, default = `False`) Again, this is argument is
    present to be consistent with the other device configuration routines. It is
    ignored.

#### Task Configuration

The [`Task Device`](#task-device) is initialized with the following arguments.

*   `reach_name`: (Required) The Reach server name of the text instructions
    device. This name must match the name used by the Reach server.

*   `is_synchronous`: (Optional, default = `False`) Again, this is argument is
    present to be consistent with the other device configuration routines. It is
    ignored.

#### Text Instructions Configuration

This is a device that acquires text instructions from the lower level PyReach
Host API. It does not correspond to a physical device.

The [`Text Instructions Device`](#text-instructions-device) is initialized with
the following arguments.

*   `reach_name`: (Required) The Reach server name of the text instructions
    device. This name must match the name used by the Reach server.

*   `is_synchronous`: (Optional, default = `False`) Again, this is argument is
    present to be consistent with the other device configuration routines. It is
    ignored.

*   `task_disable`: (Optional, default = `False`) When this is set to False, the
    "task_enable" key is present in the action space. Otherwise, when True, the
    "task_enable" key is not present. For backwards compatibility reasons, this
    is configured to False. The vastly preferred value is True and use the Task
    Device instead.

#### Vacuum Configuration

A device for a vacuum end-effector.

*   `reach_name`: (Required) The Reach server name of the vacuum device. This
    name must match the name used by the Reach server.

*   `blowoff_ignore`: (Optional) Any blow off request that can not actually be
    performed will be silently ignored. Otherwise, a `PyReachError` exception is
    raised.

*   `is_synchronous`: (Optional, default = `False`) If `True`, all vacuum
    requests for this device are made synchronously.

*   `state_enable`: (Optional, default = `True`) If `True`, the `state` entry is
    present in the observation space. For backwards compatibility reasons, this
    defaults to `True`.

*   `vacuum_detect_enable`: (Optional, default= `True`) If `True`, the
    `vacuum_detect` entry is present in the observation space. For backwards
    compatibility reasons, this defaults to `True`.

*   `vacuum_gauge_enable`: (Optional, default = `False`) If `True`, the
    `vacuum_gauge` entry is present in the observation space.
