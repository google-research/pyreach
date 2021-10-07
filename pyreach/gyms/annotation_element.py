"""Reach arm element used for configuration."""

import dataclasses

from pyreach.gyms import reach_element


@dataclasses.dataclass(frozen=True)
class ReachAnnotation(reach_element.ReachElement):
  """Text instructions configuration class.

  Attributes:
    reach_name: The name of the corresponding device on the Reach server. This
      name can be empty.
    is_synchronous: If True, the next Gym observation will synchronize all
      observactions elements that have this flag set otherwise the next
      observation is asynchronous.  This argument is optional and defaults to
      False.
  """
  reach_name: str
  maximum_size: int
  is_synchronous: bool = False
