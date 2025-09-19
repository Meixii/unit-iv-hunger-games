"""
Decision Engine

This module handles Phase 1 of the action resolution system: collecting decisions from all animals.
"""

from typing import List, Optional, Tuple
import random
import logging

# Import from parent directory
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures import Animal, Simulation, ActionType, AnimalCategory
from sensory import build_input_vector
from .action_data import AnimalAction


class DecisionEngine:
    """
    Handles the Decision Phase of action resolution.
    
    In this phase, every living animal's decision system outputs a chosen action.
    Prefers MLP when available, with a simple rule-based fallback. All decisions
    are stored without being executed yet.
    """
    
    def __init__(self, simulation: Simulation, logger: logging.Logger):
        """Initialize the decision engine."""
        self.simulation = simulation
        self.logger = logger
    
    def execute_decision_phase(self, living_animals: List[Animal]) -> List[AnimalAction]:
        """
        Phase 1: Decision Phase
        Collect actions from all living animals using MLP if available,
        otherwise fall back to simple rule-based logic.
        """
        planned_actions = []
        
        for animal in living_animals:
            try:
                # Prefer MLP-based decision when available
                if getattr(animal, 'mlp_network', None) is not None:
                    action = self._make_animal_decision_mlp(animal)
                else:
                    action = self._make_animal_decision(animal)
                planned_actions.append(action)
                
                self.logger.debug(f"Animal {animal.animal_id} chose action: {action.action_type.value}")
                
            except Exception as e:
                self.logger.warning(f"Decision failed for animal {animal.animal_id}: {e}")
                # Default to rest if decision fails
                default_action = AnimalAction(
                    animal_id=animal.animal_id,
                    animal=animal,
                    action_type=ActionType.REST,
                    result_message=f"Defaulted to rest due to decision error: {e}"
                )
                planned_actions.append(default_action)
        
        return planned_actions
    
    def _make_animal_decision(self, animal: Animal) -> AnimalAction:
        """
        Fallback rule-based decision used when no MLP is available or desired.
        Kept intentionally to ensure robustness during partial integrations.
        """
        # Get current status
        health = animal.status.get('Health', 100)
        hunger = animal.status.get('Hunger', 100)
        thirst = animal.status.get('Thirst', 100)
        energy = animal.status.get('Energy', 100)
        
        # Priority 1: Critical survival needs
        if health <= 20:
            return AnimalAction(animal.animal_id, animal, ActionType.REST)
        
        if hunger <= 30:
            # Look for food resources nearby
            food_location = self._find_nearby_resource(animal, 'food')
            if food_location:
                return AnimalAction(animal.animal_id, animal, ActionType.EAT, target_location=food_location)
        
        if thirst <= 30:
            # Look for water resources nearby
            water_location = self._find_nearby_resource(animal, 'water')
            if water_location:
                return AnimalAction(animal.animal_id, animal, ActionType.DRINK, target_location=water_location)
        
        # Priority 2: Energy management
        if energy <= 40:
            return AnimalAction(animal.animal_id, animal, ActionType.REST)
        
        # Priority 3: Exploration/Movement
        # Choose a random movement direction
        movement_actions = [ActionType.MOVE_NORTH, ActionType.MOVE_EAST, 
                          ActionType.MOVE_SOUTH, ActionType.MOVE_WEST]
        chosen_movement = random.choice(movement_actions)
        
        # Calculate target location
        current_x, current_y = animal.location
        target_location = self._calculate_target_location(current_x, current_y, chosen_movement)
        
        return AnimalAction(
            animal.animal_id, 
            animal, 
            chosen_movement,
            target_location=target_location
        )

    def _make_animal_decision_mlp(self, animal: Animal) -> AnimalAction:
        """Make a decision using the animal's MLP over the action space."""
        x = build_input_vector(self.simulation, animal)
        probs = animal.mlp_network.forward(x)
        # Map output index to ActionType order defined in constants and ActionType
        action_space = [
            ActionType.MOVE_NORTH,
            ActionType.MOVE_EAST,
            ActionType.MOVE_SOUTH,
            ActionType.MOVE_WEST,
            ActionType.REST,
            ActionType.EAT,
            ActionType.DRINK,
            ActionType.ATTACK,
        ]
        # Choose argmax
        best_idx = max(range(len(probs)), key=lambda i: probs[i]) if probs else 4  # default REST idx=4
        chosen = action_space[best_idx]

        # Determine target location for movement or context actions
        current_x, current_y = animal.location
        target_location = self._calculate_target_location(current_x, current_y, chosen)

        return AnimalAction(
            animal_id=animal.animal_id,
            animal=animal,
            action_type=chosen,
            target_location=target_location
        )
    
    def _find_nearby_resource(self, animal: Animal, resource_type: str) -> Optional[Tuple[int, int]]:
        """Find nearby resource of specified type."""
        if not animal.location or not self.simulation.world:
            return None
        
        current_x, current_y = animal.location
        world = self.simulation.world
        
        # Check adjacent tiles for resources
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                    
                check_x, check_y = current_x + dx, current_y + dy
                
                # Check bounds
                if (0 <= check_x < world.dimensions[0] and 
                    0 <= check_y < world.dimensions[1]):
                    
                    tile = world.get_tile(check_x, check_y)
                    if tile:
                        # Support both a list of resources and a single resource attribute
                        if hasattr(tile, 'resources') and tile.resources:
                            for resource in tile.resources:
                                if ((resource_type == 'food' and resource.resource_type.value in ['Plant', 'Prey', 'Carcass']) or
                                    (resource_type == 'water' and resource.resource_type.value == 'Water')):
                                    return (check_x, check_y)
                        elif getattr(tile, 'resource', None):
                            res = tile.resource
                            if ((resource_type == 'food' and res.resource_type.value in ['Plant', 'Prey', 'Carcass']) or
                                (resource_type == 'water' and res.resource_type.value == 'Water')):
                                return (check_x, check_y)
        
        return None
    
    def _calculate_target_location(self, x: int, y: int, action: ActionType) -> Tuple[int, int]:
        """Calculate target location based on movement action."""
        if action == ActionType.MOVE_NORTH:
            return (x, y - 1)
        elif action == ActionType.MOVE_EAST:
            return (x + 1, y)
        elif action == ActionType.MOVE_SOUTH:
            return (x, y + 1)
        elif action == ActionType.MOVE_WEST:
            return (x - 1, y)
        else:
            return (x, y)
