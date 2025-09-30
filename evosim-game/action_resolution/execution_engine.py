"""
Action Execution Engine

This module handles Phase 3 of the action resolution system: executing actions
in priority order with conflict resolution.
"""

from typing import List, Dict, Any, Optional
import random
import logging

# Import from parent directory
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures import Animal, Simulation, ActionType, AnimalCategory, TerrainType
from .action_data import AnimalAction
from fitness import add_distance, add_resource_units, add_kill


class ExecutionEngine:
    """
    Handles the Action Execution Phase of action resolution.
    
    The stored actions are executed in a specific order of priority:
    - Priority 1 (Stationary Actions): 'Rest', 'Eat', 'Drink', 'Attack'
    - Priority 2 (Movement Actions): All 'Move' actions with conflict resolution
    """
    
    def __init__(self, simulation: Simulation, logger: logging.Logger):
        """Initialize the execution engine."""
        self.simulation = simulation
        self.logger = logger
    
    def execute_action_execution_phase(self, planned_actions: List[AnimalAction]) -> Dict[str, Any]:
        """
        Phase 3: Action Execution Phase
        Execute actions in priority order with conflict resolution.
        """
        results = {
            'actions_executed': 0,
            'actions_failed': 0,
            'conflicts': 0,
            'movement_conflicts': 0,
            'resource_conflicts': 0,
            'combat_encounters': 0
        }
        
        # Separate actions by priority
        stationary_actions = []
        movement_actions = []
        
        for action in planned_actions:
            if action.action_type in [ActionType.REST, ActionType.EAT, ActionType.DRINK, ActionType.ATTACK]:
                stationary_actions.append(action)
            else:
                movement_actions.append(action)
        
        # Execute Priority 1: Stationary Actions
        self.logger.debug(f"Executing {len(stationary_actions)} stationary actions")
        for action in stationary_actions:
            success = self._execute_single_action(action)
            if success:
                results['actions_executed'] += 1
            else:
                results['actions_failed'] += 1
        
        # Execute Priority 2: Movement Actions (with conflict resolution)
        self.logger.debug(f"Executing {len(movement_actions)} movement actions")
        movement_results = self._execute_movement_actions_with_conflicts(movement_actions)
        results['actions_executed'] += movement_results['executed']
        results['actions_failed'] += movement_results['failed']
        results['movement_conflicts'] += movement_results['conflicts']
        results['combat_encounters'] += movement_results['encounters']
        
        results['conflicts'] = results['movement_conflicts'] + results['resource_conflicts']
        
        return results
    
    def _execute_single_action(self, action: AnimalAction) -> bool:
        """Execute a single stationary action."""
        try:
            animal = action.animal
            
            # Check if animal is still alive
            if animal not in self.simulation.get_living_animals():
                action.success = False
                action.result_message = "Animal died before action execution"
                return False
            
            # Check energy requirements
            if animal.status.get('Energy', 100) < action.energy_cost:
                action.success = False
                action.result_message = f"Insufficient energy ({animal.status.get('Energy', 100)} < {action.energy_cost})"
                return False
            
            # Execute based on action type
            if action.action_type == ActionType.REST:
                return self._execute_rest_action(action)
            elif action.action_type == ActionType.EAT:
                return self._execute_eat_action(action)
            elif action.action_type == ActionType.DRINK:
                return self._execute_drink_action(action)
            elif action.action_type == ActionType.ATTACK:
                return self._execute_attack_action(action)
            else:
                action.success = False
                action.result_message = f"Unknown action type: {action.action_type}"
                return False
                
        except Exception as e:
            action.success = False
            action.result_message = f"Action execution failed: {str(e)}"
            self.logger.warning(f"Action execution failed for {action.animal_id}: {e}")
            return False
    
    def _execute_rest_action(self, action: AnimalAction) -> bool:
        """Execute rest action - restore energy and health."""
        animal = action.animal
        
        # Restore energy
        current_energy = animal.status.get('Energy', 100)
        energy_restored = min(20, 100 - current_energy)
        animal.status['Energy'] = current_energy + energy_restored
        
        # Restore small amount of health
        current_health = animal.status.get('Health', 100)
        health_restored = min(5, 100 - current_health)
        animal.status['Health'] = current_health + health_restored
        
        action.success = True
        action.result_message = f"Rested: +{energy_restored} energy, +{health_restored} health"
        
        self.logger.debug(f"Animal {animal.animal_id} rested: +{energy_restored} energy, +{health_restored} health")
        return True
    
    def _execute_eat_action(self, action: AnimalAction) -> bool:
        """Execute eat action - consume food resource."""
        animal = action.animal
        
        # Find food at current location or target location
        location = action.target_location or animal.location
        if not location or not self.simulation.world:
            action.success = False
            action.result_message = "No valid location to eat"
            return False
        
        x, y = location
        tile = self.simulation.world.get_tile(x, y)
        if not tile:
            action.success = False
            action.result_message = "Invalid tile location"
            return False
        
        # Find consumable food resource (supports either a single resource or list)
        food_resource = None
        if hasattr(tile, 'resources') and isinstance(tile.resources, list):
            for resource in tile.resources:
                if resource.resource_type.value in ['Plant', 'Prey', 'Carcass']:
                    food_resource = resource
                    break
        else:
            if getattr(tile, 'resource', None) and tile.resource.resource_type.value in ['Plant', 'Prey', 'Carcass']:
                food_resource = tile.resource
        
        # Validate by category: Herbivore -> Plant; Carnivore -> Prey/Carcass; Omnivore -> any food
        def is_edible_for_category(res_type: str, cat: AnimalCategory) -> bool:
            if cat == AnimalCategory.HERBIVORE:
                return res_type == 'Plant'
            if cat == AnimalCategory.CARNIVORE:
                return res_type in ['Prey', 'Carcass']
            return res_type in ['Plant', 'Prey', 'Carcass']

        if not food_resource or not is_edible_for_category(food_resource.resource_type.value, animal.category):
            action.success = False
            action.result_message = "No edible food available at location"
            return False
        
        # Consume energy for the action
        animal.status['Energy'] = max(0, animal.status.get('Energy', 100) - action.energy_cost)
        
        # Restore hunger based on food type
        hunger_restored = 0
        if food_resource.resource_type.value == 'Plant':
            hunger_restored = 30 if animal.category == AnimalCategory.HERBIVORE else 15
        elif food_resource.resource_type.value in ['Prey', 'Carcass']:
            hunger_restored = 40 if animal.category == AnimalCategory.CARNIVORE else 20
        
        # Apply hunger restoration
        current_hunger = animal.status.get('Hunger', 100)
        animal.status['Hunger'] = min(100, current_hunger + hunger_restored)
        # Fitness: count food units consumed as resource
        add_resource_units(animal, float(hunger_restored))
        
        # Consume the resource
        if hasattr(food_resource, 'uses'):
            food_resource.uses -= 1
            if food_resource.uses <= 0 and hasattr(tile, 'resources') and isinstance(tile.resources, list):
                tile.resources.remove(food_resource)
        elif hasattr(food_resource, 'uses_left'):
            food_resource.uses_left -= 1
            if food_resource.uses_left <= 0:
                if hasattr(tile, 'resources') and isinstance(tile.resources, list):
                    tile.resources.remove(food_resource)
                elif hasattr(tile, 'resource'):
                    tile.resource = None
        
        action.success = True
        action.result_message = f"Ate {food_resource.resource_type.value}: +{hunger_restored} hunger"
        
        self.logger.debug(f"Animal {animal.animal_id} ate {food_resource.resource_type.value}: +{hunger_restored} hunger")
        return True
    
    def _execute_drink_action(self, action: AnimalAction) -> bool:
        """Execute drink action - consume water resource."""
        animal = action.animal
        
        # Find water at current location or target location
        location = action.target_location or animal.location
        if not location or not self.simulation.world:
            action.success = False
            action.result_message = "No valid location to drink"
            return False
        
        x, y = location
        tile = self.simulation.world.get_tile(x, y)
        if not tile:
            action.success = False
            action.result_message = "Invalid tile location"
            return False
        
        # Find water resource OR allow drinking when adjacent to a water tile
        water_resource = None
        if hasattr(tile, 'resources') and isinstance(tile.resources, list):
            for resource in tile.resources:
                if resource.resource_type.value == 'Water':
                    water_resource = resource
                    break
        else:
            if getattr(tile, 'resource', None) and tile.resource.resource_type.value == 'Water':
                water_resource = tile.resource
        
        if not water_resource:
            # Check adjacency to any water terrain tile (drinking from edge)
            ax, ay = location
            world = self.simulation.world
            adjacent = [(ax+1,ay),(ax-1,ay),(ax,ay+1),(ax,ay-1)]
            adjacent_has_water = False
            for nx, ny in adjacent:
                if 0 <= nx < world.dimensions[0] and 0 <= ny < world.dimensions[1]:
                    t = world.get_tile(nx, ny)
                    if t and t.terrain_type == TerrainType.WATER:
                        adjacent_has_water = True
                        break
            if not adjacent_has_water:
                action.success = False
                action.result_message = "No water available at or adjacent to location"
                return False
        
        # Consume energy for the action
        animal.status['Energy'] = max(0, animal.status.get('Energy', 100) - action.energy_cost)
        
        # Restore thirst
        thirst_restored = 50
        current_thirst = animal.status.get('Thirst', 100)
        animal.status['Thirst'] = min(100, current_thirst + thirst_restored)
        # Fitness: count water units as resource
        add_resource_units(animal, float(thirst_restored))
        
        # Water resources typically don't get depleted as quickly
        if water_resource and random.random() < 0.1:  # 10% chance to deplete water
            if hasattr(water_resource, 'uses'):
                water_resource.uses -= 1
                if water_resource.uses <= 0 and hasattr(tile, 'resources') and isinstance(tile.resources, list):
                    tile.resources.remove(water_resource)
            elif hasattr(water_resource, 'uses_left'):
                water_resource.uses_left -= 1
                if water_resource.uses_left <= 0:
                    if hasattr(tile, 'resources') and isinstance(tile.resources, list):
                        tile.resources.remove(water_resource)
                    elif hasattr(tile, 'resource'):
                        tile.resource = None
        
        action.success = True
        action.result_message = f"Drank water: +{thirst_restored} thirst"
        
        self.logger.debug(f"Animal {animal.animal_id} drank water: +{thirst_restored} thirst")
        return True
    
    def _execute_attack_action(self, action: AnimalAction) -> bool:
        """Execute attack action - combat with another animal."""
        animal = action.animal
        
        # Find target animal at current location
        if not animal.location or not self.simulation.world:
            action.success = False
            action.result_message = "No valid location to attack"
            return False
        
        x, y = animal.location
        tile = self.simulation.world.get_tile(x, y)
        if not tile or not tile.occupant or tile.occupant == animal:
            action.success = False
            action.result_message = "No target to attack"
            return False
        
        target = tile.occupant
        
        # Consume energy for attack
        animal.status['Energy'] = max(0, animal.status.get('Energy', 100) - action.energy_cost)
        
        # Calculate damage based on strength
        attacker_strength = animal.traits.get('Strength', 50)
        target_agility = target.traits.get('Agility', 50)
        
        # Simple combat calculation
        hit_chance = 0.6 + (attacker_strength - target_agility) / 200
        hit_chance = max(0.1, min(0.9, hit_chance))  # Clamp between 10% and 90%
        
        if random.random() < hit_chance:
            damage = random.randint(15, 25) + (attacker_strength - 50) // 10
            target.status['Health'] = max(0, target.status.get('Health', 100) - damage)
            
            action.success = True
            action.result_message = f"Attack hit for {damage} damage"
            
            # Check if target died
            if target.status['Health'] <= 0:
                self.logger.info(f"Animal {target.animal_id} killed by {animal.animal_id}")
                self.simulation.remove_animal(target)
                tile.occupant = animal  # Attacker takes the tile
                # Fitness: kill credit
                add_kill(animal, 1)
            
            self.logger.debug(f"Animal {animal.animal_id} attacked {target.animal_id} for {damage} damage")
        else:
            action.success = True
            action.result_message = "Attack missed"
            self.logger.debug(f"Animal {animal.animal_id} missed attack on {target.animal_id}")
        
        return True
    
    def _execute_movement_actions_with_conflicts(self, movement_actions: List[AnimalAction]) -> Dict[str, Any]:
        """Execute movement actions with conflict resolution based on agility."""
        results = {
            'executed': 0,
            'failed': 0,
            'conflicts': 0,
            'encounters': 0
        }
        
        # Group actions by target location
        location_actions = {}
        for action in movement_actions:
            if action.target_location:
                target = action.target_location
                if target not in location_actions:
                    location_actions[target] = []
                location_actions[target].append(action)
        
        # Process each target location
        for target_location, actions in location_actions.items():
            if len(actions) == 1:
                # No conflict, execute normally
                success = self._execute_movement_action(actions[0])
                if success:
                    results['executed'] += 1
                else:
                    results['failed'] += 1
            else:
                # Conflict resolution needed
                results['conflicts'] += 1
                winner = self._resolve_movement_conflict(actions)
                
                # Execute winner's movement
                if winner:
                    success = self._execute_movement_action(winner)
                    if success:
                        results['executed'] += 1
                    else:
                        results['failed'] += 1
                
                # Fail other actions
                for action in actions:
                    if action != winner:
                        action.success = False
                        action.result_message = "Lost movement conflict (lower agility)"
                        results['failed'] += 1
        
        return results
    
    def _resolve_movement_conflict(self, conflicting_actions: List[AnimalAction]) -> Optional[AnimalAction]:
        """Resolve movement conflict based on agility - highest agility wins."""
        if not conflicting_actions:
            return None
        
        # Sort by agility (highest first)
        def get_agi(animal):
            return animal.traits.get('AGI') or animal.traits.get('Agility', 50)
        sorted_actions = sorted(
            conflicting_actions,
            key=lambda a: get_agi(a.animal),
            reverse=True
        )
        
        winner = sorted_actions[0]
        winner_agility = winner.animal.traits.get('AGI') or winner.animal.traits.get('Agility', 50)
        
        self.logger.debug(f"Movement conflict resolved: {winner.animal_id} wins with {winner_agility} agility")
        
        return winner
    
    def _execute_movement_action(self, action: AnimalAction) -> bool:
        """Execute a single movement action."""
        try:
            animal = action.animal
            target_x, target_y = action.target_location
            
            # Check if animal is still alive
            if animal not in self.simulation.get_living_animals():
                action.success = False
                action.result_message = "Animal died before movement"
                return False
            
            # Check bounds
            world = self.simulation.world
            if (target_x < 0 or target_x >= world.dimensions[0] or 
                target_y < 0 or target_y >= world.dimensions[1]):
                action.success = False
                action.result_message = "Target location out of bounds"
                return False
            
            # Check if target tile is passable
            target_tile = world.get_tile(target_x, target_y)
            if not target_tile:
                action.success = False
                action.result_message = "Invalid target tile"
                return False
            
            # Check terrain - mountains are impassable
            if target_tile.terrain_type == TerrainType.MOUNTAINS:
                action.success = False
                action.result_message = "Cannot move into mountains"
                return False
            
            # Check energy requirements
            if animal.status.get('Energy', 100) < action.energy_cost:
                action.success = False
                action.result_message = f"Insufficient energy for movement"
                return False
            
            # Get current tile
            current_x, current_y = animal.location
            current_tile = world.get_tile(current_x, current_y)
            
            # Check if target tile is occupied
            if target_tile.occupant:
                # Animal encounter!
                encounter_result = self._handle_animal_encounter(animal, target_tile.occupant)
                action.success = encounter_result['success']
                action.result_message = encounter_result['message']
                return encounter_result['success']
            
            # Execute movement
            # Consume energy
            animal.status['Energy'] = max(0, animal.status.get('Energy', 100) - action.energy_cost)
            
            # Update locations
            animal.location = (target_x, target_y)
            # Fitness: distance traveled
            add_distance(animal, 1.0)
            
            # Update tile occupants
            if current_tile:
                current_tile.occupant = None
            target_tile.occupant = animal
            
            action.success = True
            action.result_message = f"Moved to ({target_x}, {target_y})"
            
            self.logger.debug(f"Animal {animal.animal_id} moved to ({target_x}, {target_y})")
            return True
            
        except Exception as e:
            action.success = False
            action.result_message = f"Movement failed: {str(e)}"
            self.logger.warning(f"Movement failed for {action.animal_id}: {e}")
            return False
    
    def _handle_animal_encounter(self, moving_animal: Animal, occupying_animal: Animal) -> Dict[str, Any]:
        """Handle encounter when an animal moves into an occupied tile."""
        # Simple encounter logic - this can be expanded
        # For now, treat it as a conflict that prevents movement
        
        self.logger.info(f"Animal encounter: {moving_animal.animal_id} vs {occupying_animal.animal_id}")
        
        # Compare strength to determine outcome
        mover_strength = moving_animal.traits.get('Strength', 50)
        occupier_strength = occupying_animal.traits.get('Strength', 50)
        
        if mover_strength > occupier_strength + 10:  # Significant strength advantage
            # Moving animal displaces occupying animal
            # This is a simplified version - full combat would be more complex
            return {
                'success': False,  # For now, prevent movement to avoid complexity
                'message': f"Encounter with {occupying_animal.animal_id} - movement blocked"
            }
        else:
            # Movement blocked
            return {
                'success': False,
                'message': f"Encounter with {occupying_animal.animal_id} - movement blocked"
            }
