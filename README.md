# PyReach - Python Client SDK for robot remote control

### Disclaimer: this is not an officially supported Google product.

PyReach is the Python client SDK to remotely control robots.
Operator credentials will be approved by invitation only at this time

## Supported Platform

Ubuntu 18.04, Ubuntu 20.04, and gLinux.

## Build

```shell
git clone https://github.com/google-research/pyreach.git
cd pyreach
./build.sh
```

## Getting Started

If build.sh runs successfully, PyReach is ready to be used. It is supported,
but not required to install PyReach into the system path.

**Step 1.** (Only the first time) Login to the system.

```shell
cd pyreach
./reach login

# Follow the login instructions.
```

**Step 2.** Connect to a robot.

In a new shell session.

```shell
cd pyreach
./reach ls
./reach connect <robot id>
```

**Step 3.** View camera image

In a new shell session.

```shell
cd pyreach
./reach-viewer
```

**Step 4.** Run pendant tool.

In a new shell session.

```shell
cd pyreach
./reach-pendant
```

**Step 5.** Run example agent.

In a new shell session.

```shell
cd pyreach
source setenv.sh
python -m pyreach.examples.pyreach_gym_example
```


**Logs**

By default, all the client logs are saved under:

```shell
$HOME/reach_workspace
```

## Install

Optionally, PyReach can be installed as a pip package:

```shell
cd pyreach
pip install .
```

Once PyReach is installed, the command "reach", "reach-viewer", and "reach-pendant" can be access directly through command line.

## Uninstall

To remove the PyReach pip package:

```shell
pip uninstall pyreach
```
