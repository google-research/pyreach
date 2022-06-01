"""Instruction generator for 2d board data collection."""

import itertools
import logging
from typing import List, Tuple

import numpy as np

# The real blocks are defined in go/which-8
BLOCKS8 = [
    'red star', 'red circle', 'blue triangle', 'blue cube', 'green circle',
    'green star', 'yellow heart', 'yellow hexagon'
]
LOCATIONS = [
    'top left corner', 'top center', 'top right corner', 'center left',
    'center', 'center right', 'bottom left corner', 'bottom center',
    'bottom right corner'
]
COLORS = ['red', 'blue', 'green', 'yellow']


class InstructionGeneratorBlock8():
  """Instruction generator for 8 block tasks."""

  def __init__(self, seed: int = 0):
    self._fn_rng = np.random.RandomState(seed)
    self._inst_rng = np.random.RandomState(seed)

  def generate_instruction(self) -> str:
    """Gets random from each 'instruction class'."""
    all_task_fns = [
        self.get_sort_tasks,
        self.colors_in_locations,
        self.group_color_pairs,
        self.get_colors_in_lines,
        self.group_color_pairs_in_locations,
        self.get_line_tasks,
        self.get_surround_tasks,
        self.blocks_in_order_outer_edge,
        self.all_blocks_in_location,
        self.k_blocks_in_location_i_rest_in_location_j,
        self.get_shape_instructions
    ]

    task_fn = all_task_fns[self._fn_rng.choice(range(len(all_task_fns)))]
    inst_choices = task_fn()
    inst = self._inst_rng.choice(inst_choices)
    return inst

  def colors_in_locations(self) -> List[str]:
    """Get tasks for putting colors in locations."""
    all_inst = []
    all_colors_in_all_locations = list(
        itertools.product(
            itertools.permutations(COLORS, 4),
            itertools.permutations(LOCATIONS, 4)))
    for (colors, locations) in all_colors_in_all_locations:
      inst = (f'put the {colors[0]} blocks in the {locations[0]}, '
              f'the {colors[1]} blocks in the {locations[1]}, '
              f'the {colors[2]} blocks in the {locations[2]}, '
              f'and the {colors[3]} blocks in the {locations[3]}.')
      if len(inst) > 256:  # 256 is max length.
        logging.info('Instruction greater than max length: %s', inst)
      all_inst.append(inst)
    return all_inst

  def group_color_pairs(self) -> List[str]:
    all_inst = []
    perms = list(itertools.permutations(COLORS, len(COLORS)))
    for (color_i, color_j, color_k, color_l) in perms:
      all_inst.append(
          (f'put the {color_i} and {color_j} blocks together in a group, '
           f'then put the '
           f'{color_k} and {color_l} blocks together in a group.'))
    return all_inst

  def group_color_pairs_in_locations(self) -> List[str]:
    """Get tasks for putting pairs of colors in locations."""
    all_inst = []
    color_combos = self.unique_color_combos()
    location_pairs = list(itertools.permutations(LOCATIONS, 2))
    for (color_i, color_j, color_k, color_l) in color_combos:
      for (loc_i, loc_j) in location_pairs:
        all_inst.append(
            (f'put the {color_i} and {color_j} blocks together in the {loc_i}, '
             f'then put the '
             f'{color_k} and {color_l} blocks together in the {loc_j}.'))
    return all_inst

  def unique_color_combos(self) -> List[Tuple[str, str, str, str]]:
    color_combos = list(itertools.combinations(COLORS, 2))
    all_orders = []
    for (color_i, color_j) in color_combos:
      complement = [(i, j)
                    for (i, j) in color_combos
                    if color_i not in [i, j] and color_j not in [i, j]]
      all_orders.append((color_i, color_j, complement[0][0], complement[0][1]))
    return all_orders

  def get_colors_in_lines(self) -> List[str]:
    """Get 'put colors in lines' tasks."""
    all_inst = []
    color_combos = self.unique_color_combos()
    for mode_i in ['horizontal', 'vertical']:
      for mode_j in ['horizontal', 'vertical']:
        for (color_i, color_j, color_k, color_l) in color_combos:
          all_inst.append((f'make one {mode_i} line out of the {color_i} '
                           f'and {color_j} blocks, then '
                           f'make a {mode_j} line out of the '
                           f'{color_k} and {color_l} blocks'))
    return all_inst

  def get_line_tasks(self) -> List[str]:
    """Get put blocks in a line tasks."""
    line_tasks = [
        'put the blocks in a line',
        'put all the blocks in a vertical line',
        'put all the blocks in a horizontal line',
    ]
    for mode in ['left', 'center', 'right']:
      line_tasks.append(
          f'put all the blocks in a vertical line on the {mode} of the board')
    for mode in ['bottom', 'center', 'top']:
      line_tasks.append(
          f'put all the blocks in a horizontal line on the {mode} of the board')
    for mode in ['top left to bottom right', 'top right to bottom left']:
      line_tasks.append(f'put the blocks in a diagonal line from the {mode}')
    return line_tasks

  def get_surround_tasks(self) -> List[str]:
    all_inst = []
    for block in BLOCKS8:
      all_inst.append(f'surround the {block} with the others')
    return all_inst

  def blocks_in_order_outer_edge(self) -> List[str]:
    """Get instructions for putting all blocks in locations on edge."""
    all_inst = []
    block_orderings = list(itertools.permutations(BLOCKS8, len(BLOCKS8)))
    outer_edge_locations = [
        'top left', 'top center', 'top right', 'center left', 'center right',
        'bottom left', 'bottom center', 'bottom right'
    ]
    for ordering in block_orderings:
      inst = 'put the: \n'
      for idx, (block_i, loc_i) in enumerate(
          zip(ordering, outer_edge_locations)):
        inst += f'{idx}) {block_i} to {loc_i}, \n'
      if len(inst) > 256:  # 256 is max instruction length.
        logging.info('Instruction greater than max length: %s', inst)
      all_inst.append(inst)
    return all_inst

  def all_blocks_in_location(self) -> List[str]:
    all_inst = []
    for loc_i in LOCATIONS:
      all_inst.append(f'put all the blocks in the {loc_i}')
    return all_inst

  def k_blocks_in_location_i_rest_in_location_j(self) -> List[str]:
    all_inst = []
    location_pairs = list(itertools.permutations(LOCATIONS, 2))
    for k in range(1, 8):
      for (loc_i, loc_j) in location_pairs:
        all_inst.append(
            f'put {k} blocks in the {loc_i}, then the rest in the {loc_j}')
    return all_inst

  def get_shape_instructions(self) -> List[str]:
    """Get shape instructions."""
    all_inst = []
    for shape in [
        'square', 'triangle', 'circle', 'diamond', 'parallelogram', 'G', 'O',
        'L', 'E', 'A', 'T', 'X', 'V', 'Y', 'U', 'S', 'C', 'Z', 'N', 'J'
    ]:
      all_inst.append(f'make a "{shape}"" shape out of all the blocks')
    all_inst.append('make a smiley face out of the blocks')
    all_inst.append('make a rainbow out of the blocks (red, yellow, green, '
                    'blue in a semicircle)')
    return all_inst

  def get_sort_tasks(self) -> List[str]:
    sort_tasks = ['group the blocks by color']
    return sort_tasks
