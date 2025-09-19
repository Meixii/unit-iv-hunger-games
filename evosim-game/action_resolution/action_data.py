"""
Action Resolution Data Structures

This module contains the data structures used by the action resolution system.
"""

from dataclasses import dataclass
from typing import Optional, Tuple
from enum import Enum

# Import from parent directory
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures import ActionType, Animal


@dataclass
class AnimalAction:
    """Represents a planned action by an animal during the decision phase."""
    animal_id: str
    animal: Animal
    action_type: ActionType
    target_location: Optional[Tuple[int, int]] = None
    target_animal: Optional[Animal] = None
    energy_cost: float = 0.0
    success: bool = False
    result_message: str = ""
    
    def __post_init__(self):
        """Calculate energy cost based on action type."""
        if self.action_type in [ActionType.MOVE_NORTH, ActionType.MOVE_EAST, 
                               ActionType.MOVE_SOUTH, ActionType.MOVE_WEST]:
            self.energy_cost = 5.0  # Movement costs energy
        elif self.action_type == ActionType.ATTACK:
            self.energy_cost = 10.0  # Attack costs more energy
        elif self.action_type == ActionType.REST:
            self.energy_cost = 0.0  # Rest costs no energy
        else:
            self.energy_cost = 2.0  # Eat/Drink cost minimal energy


class ActionPriority(Enum):
    """Priority levels for action execution."""
    STATIONARY = 1  # Rest, Eat, Drink, Attack
    MOVEMENT = 2    # All movement actions
