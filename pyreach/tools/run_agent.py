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

"""Program to run agent connected to robot/simulator."""

import pathlib
import subprocess
import sys
from typing import Dict, List, Tuple

from pyreach import core
from pyreach.tools import agent_runner


def main() -> None:
  """Run the Agent Runner."""

  arguments: Tuple[str, ...] = tuple(sys.argv)
  if len(arguments) < 3:
    print("usage: python run_agent.py AGENT ROBOT_OR_SIM")
    print("where:")
    print("  AGENT is 2D, AUTOPICK, KIT, FOLD, ALL or explicit agent .py file")
    print("  ROBOT_SIM is SIM, ROBOT, BOTH, or explicit robot/sim name")
    return

  agent_argument: str = arguments[1]
  robot_sim_argument: str = arguments[2]
  print(f"agent_argument='{agent_argument}'")
  print(f"robot_argmuent='{robot_sim_argument}'")

  current_directory: pathlib.Path = pathlib.Path(__file__)
  current_directory = current_directory.parent.parent.absolute()
  agents: Dict[str, pathlib.Path] = {}
  if agent_argument in ("ALL", "AUTOPICK"):
    agents["singulate"] = (
        current_directory / "examples" / "singulation_autopick_agent.py")
  if agent_argument in ("ALL", "2D"):
    agents["2d"] = current_directory / "examples" / "benchmark_2d_agent.py"
  if agent_argument in ("ALL", "KIT"):
    agents["kit"] = (
        current_directory / "examples" / "benchmark_kitting_agent.py")
  if agent_argument in ("ALL", "FOLD"):
    agents["fold"] = (
        current_directory / "examples" / "benchmark_folding_agent.py")
  if agent_argument.endswith(".py"):
    agents["other"] = current_directory / pathlib.Path(agent_argument)
  if not agents:
    print(f"'{agent_argument}' is not 2D, KIT, FOLD, ALL, or a .py file")
    sys.exit(1)

  # Find out what robots and simulators are available.
  exact_match: str = ("" if robot_sim_argument in ("SIM", "ROBOT", "BOTH") else
                      robot_sim_argument)
  print(f"exact_match:'{exact_match}'")
  matches: Dict[str, List[str]] = find_matches(agents, exact_match)
  print(f"matches={matches}")

  # Determine whether to run the robot, simulator or both.
  workcell_modes: Tuple[bool, ...] = ()
  if robot_sim_argument == "BOTH":
    workcell_modes = (True, False)
  elif robot_sim_argument == "SIM":
    workcell_modes = (True,)
  elif robot_sim_argument == "ROBOT":
    workcell_modes = (False,)
  else:
    # When there is an exact match for the robot/simulator name, the value of
    # workcell_mode needs to be a tuple of length 1 to execution of the
    # appropriate robot/simulator.
    workcell_modes = (True,)

  agent: agent_runner.AgentRunner
  if "other" in agents and exact_match:
    # Run just one explicit instance.
    try:
      agent = agent_runner.AgentRunner(agent_argument, robot_sim_argument, True)
      agent.run()
    except core.PyReachError as error:
      print(f"AgentRunner Exception: {error}")

  else:
    # First time: check for robot/simulator availability.
    # Second time: actually run robot/simulator.
    check_run: str
    for check_run in ("check", "run"):
      # Sweep through all of the agents that were specified on command line.
      agent_name: str
      agent_path: pathlib.Path
      is_sim: bool
      for is_sim in workcell_modes:
        workcell_type: str = "simulator" if is_sim else "robot"
        for agent_name, agent_path in agents.items():
          # See which simulators and robot match.
          match: List[str] = matches[agent_name]
          robot_sim: str = match[int(is_sim)]
          if check_run == "check":
            # Check only.
            if robot_sim:
              print(f"{agent_name}: will be run on {workcell_type} "
                    f"'{robot_sim}'")
            else:
              print(f"{agent_name}: {workcell_type} is not available!!!!!!!!!!")
          else:
            # Run robot/simulator.
            print(f"{agent_name}: Run on '{robot_sim}' {workcell_type}")
            try:
              agent = agent_runner.AgentRunner(str(agent_path), robot_sim, True)
              agent.run()
            except core.PyReachError as error:
              print(f"AgentRunner Exception: {error}")
      print("================")


def find_matches(agents: Dict[str, pathlib.Path],
                 exact_name: str) -> Dict[str, List[str]]:
  """Find available robots and simulators.

  Args:
    agents: The dictionary of agents to agent paths.
    exact_name: If a non-empty string, the exact simulator added to the search.

  Returns:
    Return a dictionary containing the available simulators and robots
    for all of the benchmarks.  If exact_name is matched, it is inserted
    into the returned dictionary with a key of "EXACT".

  """

  stdout_bytes: bytes = subprocess.check_output(["reach", "ls"])
  stdout_str: str = stdout_bytes.decode("utf-8")
  platforms: List[str] = stdout_str.split("\n")

  matches: Dict[str, List[str]] = {
      agent_name: ["", ""] for agent_name in agents.keys()
  }
  platform: str
  for platform in platforms:
    fields: List[str] = platform.split("\t")
    if len(fields) == 3:
      name: str = fields[0][5:].strip()
      is_sim: bool = name.find("sim") >= 0
      access: str = fields[1]
      accessible: bool = (
          access == "everyone/" or access.startswith("reach-lab/"))
      available: bool = fields[2].startswith("available")

      match: str
      for match in matches.keys():
        if accessible and available:
          if name.find(match) >= 0 or access.find(match) >= 0:
            # Stick with the first simulator that matches.
            if not matches[match][int(is_sim)]:
              matches[match][int(is_sim)] = name
          if exact_name and name == exact_name:
            matches[match][0] = exact_name
            matches[match][1] = name

  return matches


if __name__ == "__main__":
  main()
