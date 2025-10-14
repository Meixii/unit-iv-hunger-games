"""
Environment System for Evolutionary Simulation

This module implements the grid world environment where animals live,
including resource management, animal positioning, and environmental events.

Author: Zen Garden
University of Caloocan City
"""

import numpy as np
import random
from typing import List, Tuple, Dict, Optional, Set
from .animal import Animal


class GridWorld:
    """
    2D Grid world environment for the evolutionary simulation.
    
    Manages:
    - Grid state and boundaries
    - Resource placement (food, water)
    - Animal positioning and movement
    - Resource consumption
    - Collision detection
    """
    
    def __init__(self, width: int = 20, height: int = 20):
        """
        Initialize the grid world.
        
        Args:
            width: Grid width (default: 20)
            height: Grid height (default: 20)
        """
        self.width = width
        self.height = height
        
        # Grid state: 0=empty, 1=food, 2=water, 3=animal
        self.grid = np.zeros((height, width), dtype=int)
        
        # Resource positions
        self.food_positions: Set[Tuple[int, int]] = set()
        self.water_positions: Set[Tuple[int, int]] = set()
        
        # Animal tracking
        self.animals: List[Animal] = []
        self.animal_positions: Dict[Tuple[int, int], Animal] = {}
        self.dead_animals: List[Animal] = []  # Track dead animals for statistics
        
        # Resource consumption tracking
        self.total_food_consumed = 0
        self.total_water_consumed = 0
        
        # Resource counts
        self.food_count = 0
        self.water_count = 0
        
        # Environmental effects
        self.active_events: Dict[str, Dict] = {}
        self.event_modifiers = {
            'drought': {'water_multiplier': 1.0, 'water_regeneration': 1.0},
            'storm': {'movement_cost_multiplier': 1.0, 'visibility_reduction': 1.0},
            'famine': {'food_multiplier': 1.0, 'food_regeneration': 1.0},
            'bonus': {'food_multiplier': 1.0, 'water_multiplier': 1.0, 'resource_regeneration': 1.0}
        }
    
    def place_resources(self, food_density: float = 0.15, water_density: float = 0.15) -> None:
        """
        Place food and water resources randomly on the grid.
        
        Args:
            food_density: Fraction of grid cells to place food (0-1)
            water_density: Fraction of grid cells to place water (0-1)
        """
        # Clear existing resources
        self.food_positions.clear()
        self.water_positions.clear()
        self.food_count = 0
        self.water_count = 0
        
        # Clear grid cells that were food or water (but preserve animals)
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y, x] in [1, 2]:  # Food or water
                    self.grid[y, x] = 0  # Make empty
        
        # Reset event application flag for new generation
        if hasattr(self, '_events_applied'):
            delattr(self, '_events_applied')
        
        # Apply event modifiers to resource density
        modified_food_density = self.apply_event_modifiers(food_density, 'food')
        modified_water_density = self.apply_event_modifiers(water_density, 'water')
        
        # Calculate number of resources to place
        total_cells = self.width * self.height
        num_food = int(total_cells * modified_food_density)
        num_water = int(total_cells * modified_water_density)
        
        # Get all possible positions
        all_positions = [(x, y) for x in range(self.width) for y in range(self.height)]
        
        # Place food
        food_positions = random.sample(all_positions, min(num_food, len(all_positions)))
        for pos in food_positions:
            self.food_positions.add(pos)
            self.grid[pos[1], pos[0]] = 1
            self.food_count += 1
        
        # Place water (avoiding food positions)
        available_positions = [pos for pos in all_positions if pos not in food_positions]
        water_positions = random.sample(available_positions, min(num_water, len(available_positions)))
        for pos in water_positions:
            self.water_positions.add(pos)
            self.grid[pos[1], pos[0]] = 2
            self.water_count += 1
    
    def add_animal(self, animal: Animal, x: int, y: int) -> bool:
        """
        Add an animal to the grid at specified position.
        
        Args:
            animal: Animal to add
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if successfully placed, False if position occupied
        """
        if not self.is_valid_position(x, y):
            return False
        
        if (x, y) in self.animal_positions:
            return False
        
        # Place animal
        animal.set_position(x, y)
        self.animals.append(animal)
        self.animal_positions[(x, y)] = animal
        self.grid[y, x] = 3
        
        return True
    
    def remove_animal(self, animal: Animal) -> None:
        """
        Remove an animal from the grid.
        
        Args:
            animal: Animal to remove
        """
        if animal in self.animals:
            self.animals.remove(animal)
            pos = animal.get_position()
            if pos in self.animal_positions:
                del self.animal_positions[pos]
                self.grid[pos[1], pos[0]] = 0
    
    def move_animal(self, animal: Animal, new_x: int, new_y: int) -> bool:
        """
        Move an animal to a new position.
        
        Args:
            animal: Animal to move
            new_x: New X coordinate
            new_y: New Y coordinate
            
        Returns:
            True if move successful, False otherwise
        """
        if not self.is_valid_position(new_x, new_y):
            return False
        
        # Check if new position is occupied by another animal
        if (new_x, new_y) in self.animal_positions:
            return False
        
        # Get current position
        old_x, old_y = animal.get_position()
        
        # Update grid
        self.grid[old_y, old_x] = 0
        self.grid[new_y, new_x] = 3
        
        # Update tracking
        del self.animal_positions[(old_x, old_y)]
        self.animal_positions[(new_x, new_y)] = animal
        
        # Update animal position
        animal.set_position(new_x, new_y)
        
        return True
    
    def is_valid_position(self, x: int, y: int) -> bool:
        """
        Check if position is valid (within bounds).
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if position is valid
        """
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_cell_content(self, x: int, y: int) -> str:
        """
        Get the content of a grid cell.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Content type: 'empty', 'food', 'water', 'animal'
        """
        if not self.is_valid_position(x, y):
            return 'invalid'
        
        cell_value = self.grid[y, x]
        if cell_value == 0:
            return 'empty'
        elif cell_value == 1:
            return 'food'
        elif cell_value == 2:
            return 'water'
        elif cell_value == 3:
            return 'animal'
        else:
            return 'unknown'
    
    def consume_resource(self, x: int, y: int, resource_type: str) -> bool:
        """
        Consume a resource at the specified position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            resource_type: Type of resource ('food' or 'water')
            
        Returns:
            True if resource was consumed, False otherwise
        """
        if not self.is_valid_position(x, y):
            return False
        
        if resource_type == 'food' and (x, y) in self.food_positions:
            self.food_positions.remove((x, y))
            self.grid[y, x] = 0
            self.food_count -= 1
            self.total_food_consumed += 1
            return True
        elif resource_type == 'water' and (x, y) in self.water_positions:
            self.water_positions.remove((x, y))
            self.grid[y, x] = 0
            self.water_count -= 1
            self.total_water_consumed += 1
            return True
        
        return False
    
    def get_available_actions(self, x: int, y: int) -> List[str]:
        """
        Get available actions for an animal at the specified position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            List of available actions
        """
        actions = ['move', 'rest']  # Always available
        
        # Check for food
        if (x, y) in self.food_positions:
            actions.append('eat')
        
        # Check for water
        if (x, y) in self.water_positions:
            actions.append('drink')
        
        return actions
    
    def get_neighboring_positions(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Get valid neighboring positions (including diagonals).
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            List of valid neighboring positions
        """
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x, new_y = x + dx, y + dy
                if self.is_valid_position(new_x, new_y):
                    neighbors.append((new_x, new_y))
        return neighbors
    
    def get_empty_positions(self) -> List[Tuple[int, int]]:
        """
        Get all empty positions on the grid.
        
        Returns:
            List of empty positions (randomized for better distribution)
        """
        empty_positions = []
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[y, x] == 0:
                    empty_positions.append((x, y))
        
        # Randomize the order to prevent clustering on left side
        random.shuffle(empty_positions)
        return empty_positions
    
    def get_resource_positions(self, resource_type: str) -> List[Tuple[int, int]]:
        """
        Get all positions of a specific resource type.
        
        Args:
            resource_type: Type of resource ('food' or 'water')
            
        Returns:
            List of resource positions
        """
        if resource_type == 'food':
            return list(self.food_positions)
        elif resource_type == 'water':
            return list(self.water_positions)
        else:
            return []
    
    def get_animal_at_position(self, x: int, y: int) -> Optional[Animal]:
        """
        Get the animal at the specified position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Animal at position, or None if no animal
        """
        return self.animal_positions.get((x, y))
    
    def get_all_animals(self) -> List[Animal]:
        """
        Get all animals in the environment.
        
        Returns:
            List of all animals
        """
        return self.animals.copy()
    
    def get_alive_animals(self) -> List[Animal]:
        """
        Get all alive animals in the environment.
        
        Returns:
            List of alive animals
        """
        return [animal for animal in self.animals if animal.is_alive()]
    
    def get_animals_at_position(self, x: int, y: int) -> List[Animal]:
        """
        Get all animals at a specific position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            List of animals at the position
        """
        animals_at_pos = []
        for animal in self.animals:
            if animal.position == (x, y):
                animals_at_pos.append(animal)
        return animals_at_pos
    
    def get_animal_by_id(self, animal_id: str) -> Optional[Animal]:
        """
        Get an animal by its ID.
        
        Args:
            animal_id: Animal identifier
            
        Returns:
            Animal object or None if not found
        """
        for animal in self.animals + self.dead_animals:
            if animal.animal_id == animal_id:
                return animal
        return None
    
    def update_animals(self) -> None:
        """
        Update all animals in the environment.
        Animals make decisions, execute actions, and move around.
        Remove dead animals and update their positions.
        """
        dead_animals = []
        
        for animal in self.animals:
            if not animal.is_alive():
                dead_animals.append(animal)
            else:
                # Make decision and execute action
                decision = animal.make_decision(self)
                success = self._execute_animal_action(animal, decision)
                
                # Update animal state (aging, decay, survival check)
                # Note: Action recording is now handled by _execute_animal_action
                animal.update_state()
                if not animal.is_alive():
                    dead_animals.append(animal)
        
        # Move dead animals to dead_animals list instead of removing them
        for animal in dead_animals:
            self.dead_animals.append(animal)
            self.remove_animal(animal)
    
    def _execute_animal_action(self, animal: Animal, action: str) -> bool:
        """
        Execute an animal's action in the environment.
        
        Args:
            animal: Animal performing the action
            action: Action to execute
            
        Returns:
            True if action was successful, False if failed (allows new decision next step)
        """
        if not animal.is_alive():
            return False
        
        pos = animal.get_position()
        x, y = pos
        
        if action == 'move':
            # Check if animal has enough energy to move
            if animal.energy < animal.action_costs['move']:
                return False  # Let animal try other actions
            
            # Try to move towards resources first
            neighbors = self.get_neighboring_positions(x, y)
            if neighbors:
                # Prioritize moving towards resources
                resource_neighbors = []
                for neighbor in neighbors:
                    nx, ny = neighbor
                    if (nx, ny) in self.food_positions or (nx, ny) in self.water_positions:
                        resource_neighbors.append(neighbor)
                
                # Choose target position
                import random
                if resource_neighbors:
                    # Move towards resources (80% chance)
                    if random.random() < 0.8:
                        new_pos = random.choice(resource_neighbors)
                    else:
                        # Sometimes explore randomly even when resources are nearby
                        new_pos = random.choice(neighbors)
                else:
                    # Move randomly if no resources nearby
                    new_pos = random.choice(neighbors)
                
                if self.move_animal(animal, new_pos[0], new_pos[1]):
                    # Animal was successfully moved, consume energy and increment movement count
                    animal.energy -= animal.action_costs['move']
                    animal.movement_count += 1
                    # Record the move action
                    animal.action_history.append('move')
                    animal.behavioral_counts['move'] += 1
                    return True
                else:
                    # If can't move, return False to let animal try other actions
                    return False
            else:
                # No neighbors available, return False to let animal try other actions
                return False
        
        elif action == 'eat':
            # Check if there's food at current position
            if self.get_cell_content(x, y) == 'food':
                if self.consume_resource(x, y, 'food'):
                    animal.add_food(40)  # Properly add food to animal
                    # Record the successful eat action
                    animal.action_history.append('eat')
                    animal.behavioral_counts['eat'] += 1
                    return True
                else:
                    return False  # Failed to consume, let animal try again next step
            else:
                # No food at current position - try to move towards food
                nearby_food = self._find_nearby_resource(x, y, 'food')
                if nearby_food:
                    # Move towards the food - record as move action
                    if self.move_animal(animal, nearby_food[0], nearby_food[1]):
                        animal.energy -= animal.action_costs['move']
                        animal.movement_count += 1
                        # Record the actual action that happened (move, not eat)
                        animal.action_history.append('move')
                        animal.behavioral_counts['move'] += 1
                        return True
                # If no food nearby or can't move, action fails
                return False
        
        elif action == 'drink':
            # Check if there's water at current position
            if self.get_cell_content(x, y) == 'water':
                if self.consume_resource(x, y, 'water'):
                    animal.add_water(40)  # Properly add water to animal
                    # Record the successful drink action
                    animal.action_history.append('drink')
                    animal.behavioral_counts['drink'] += 1
                    return True
                else:
                    return False  # Failed to consume, let animal try again next step
            else:
                # No water at current position - try to move towards water
                nearby_water = self._find_nearby_resource(x, y, 'water')
                if nearby_water:
                    # Move towards the water - record as move action
                    if self.move_animal(animal, nearby_water[0], nearby_water[1]):
                        animal.energy -= animal.action_costs['move']
                        animal.movement_count += 1
                        # Record the actual action that happened (move, not drink)
                        animal.action_history.append('move')
                        animal.behavioral_counts['move'] += 1
                        return True
                # If no water nearby or can't move, action fails
                return False
        
        elif action == 'rest':
            # Rest action - record the action and apply rest benefits
            animal.action_history.append('rest')
            animal.behavioral_counts['rest'] += 1
            # Apply rest benefits immediately
            animal.energy = min(animal.max_energy, animal.energy + 5)
            return True
        
        return False
    
    def get_statistics(self) -> Dict:
        """
        Get environment statistics.
        
        Returns:
            Dictionary with environment statistics
        """
        alive_animals = self.get_alive_animals()
        
        return {
            'grid_size': (self.width, self.height),
            'total_animals': len(self.animals) + len(self.dead_animals),
            'alive_animals': len(alive_animals),
            'dead_animals': len(self.dead_animals),
            'food_count': self.food_count,
            'water_count': self.water_count,
            'empty_cells': len(self.get_empty_positions()),
            'active_events': list(self.active_events.keys()),
            'total_food_consumed': self.total_food_consumed,
            'total_water_consumed': self.total_water_consumed
        }
    
    def reset(self) -> None:
        """
        Reset the environment to initial state.
        """
        self.grid = np.zeros((self.height, self.width), dtype=int)
        self.food_positions.clear()
        self.water_positions.clear()
        self.animals.clear()
        self.animal_positions.clear()
        self.dead_animals.clear()  # Clear dead animals tracking
        self.food_count = 0
        self.water_count = 0
        self.active_events.clear()
    
    def apply_event_modifiers(self, base_value: float, resource_type: str) -> float:
        """
        Apply environmental event modifiers to a value.
        
        Args:
            base_value: Base value to modify
            resource_type: Type of resource or effect
            
        Returns:
            Modified value
        """
        modified_value = base_value
        
        for event_name, modifiers in self.active_events.items():
            if resource_type == 'water' and 'water_multiplier' in modifiers:
                modified_value *= modifiers['water_multiplier']
            elif resource_type == 'food' and 'food_multiplier' in modifiers:
                modified_value *= modifiers['food_multiplier']
            elif resource_type == 'movement_cost' and 'movement_cost_multiplier' in modifiers:
                modified_value *= modifiers['movement_cost_multiplier']
        
        return modified_value
    

    def update_event_effects(self, event_manager) -> None:
        """
        Update environment based on active events.
        
        Args:
            event_manager: EventManager instance to get active events
        """
        # Get active events from event manager
        active_events = event_manager.get_active_events()
        event_effects = event_manager.get_event_effects()
        
        # Update active events
        self.active_events.clear()
        for event_name, event in active_events.items():
            self.active_events[event_name] = event.get_effects()
        
        # Apply event effects to resources (only once per event activation)
        if event_effects and not hasattr(self, '_events_applied'):
            self._events_applied = True
            # Drought: Reduce water availability (with 15% minimum cap)
            if 'water_availability' in event_effects:
                water_multiplier = event_effects['water_availability']
                # Calculate target water count with 15% minimum cap
                total_cells = self.width * self.height
                min_water = max(1, int(total_cells * 0.15))  # 15% minimum
                target_water = max(min_water, int(self.water_count * water_multiplier))
                
                if self.water_count > target_water:
                    water_to_remove = self.water_count - target_water
                    water_positions_list = list(self.water_positions)
                    positions_to_remove = random.sample(water_positions_list, min(water_to_remove, len(water_positions_list)))
                    for pos in positions_to_remove:
                        self.water_positions.remove(pos)
                        self.grid[pos[1], pos[0]] = 0
                        self.water_count -= 1
            
            # Famine: Reduce food availability (with 15% minimum cap)
            if 'food_availability' in event_effects:
                food_multiplier = event_effects['food_availability']
                # Calculate target food count with 15% minimum cap
                total_cells = self.width * self.height
                min_food = max(1, int(total_cells * 0.15))  # 15% minimum
                target_food = max(min_food, int(self.food_count * food_multiplier))
                
                if self.food_count > target_food:
                    food_to_remove = self.food_count - target_food
                    food_positions_list = list(self.food_positions)
                    positions_to_remove = random.sample(food_positions_list, min(food_to_remove, len(food_positions_list)))
                    for pos in positions_to_remove:
                        self.food_positions.remove(pos)
                        self.grid[pos[1], pos[0]] = 0
                        self.food_count -= 1
            
            # Bonus: Add more resources
            if 'food_availability' in event_effects and event_effects['food_availability'] > 1.0:
                food_multiplier = event_effects['food_availability']
                # Add more food resources
                food_to_add = int(self.food_count * (food_multiplier - 1.0))
                if food_to_add > 0:
                    empty_positions = self.get_empty_positions()
                    positions_to_add = random.sample(empty_positions, min(food_to_add, len(empty_positions)))
                    for pos in positions_to_add:
                        self.food_positions.add(pos)
                        self.grid[pos[1], pos[0]] = 1
                        self.food_count += 1
            
            if 'water_availability' in event_effects and event_effects['water_availability'] > 1.0:
                water_multiplier = event_effects['water_availability']
                # Add more water resources
                water_to_add = int(self.water_count * (water_multiplier - 1.0))
                if water_to_add > 0:
                    empty_positions = self.get_empty_positions()
                    positions_to_add = random.sample(empty_positions, min(water_to_add, len(empty_positions)))
                    for pos in positions_to_add:
                        self.water_positions.add(pos)
                        self.grid[pos[1], pos[0]] = 2
                        self.water_count += 1
    
    def move_animal(self, animal: Animal, new_x: int, new_y: int) -> bool:
        """
        Move an animal to a new position.
        
        Args:
            animal: Animal to move
            new_x: New X coordinate
            new_y: New Y coordinate
            
        Returns:
            True if move was successful, False otherwise
        """
        if not self.is_valid_position(new_x, new_y):
            return False
        
        # Get current position
        old_x, old_y = animal.get_position()
        
        # Check if new position is occupied by another animal
        if (new_x, new_y) in self.animal_positions:
            return False
        
        # Move animal
        animal.set_position(new_x, new_y)
        
        # Update grid
        self.grid[old_y, old_x] = 0  # Clear old position
        self.grid[new_y, new_x] = 3  # Set new position
        
        # Update animal positions tracking
        del self.animal_positions[(old_x, old_y)]
        self.animal_positions[(new_x, new_y)] = animal
        
        return True
    
    def _find_nearby_resource(self, x: int, y: int, resource_type: str) -> Optional[Tuple[int, int]]:
        """
        Find a nearby resource of the specified type within a 3-tile radius.
        
        Args:
            x: Current X coordinate
            y: Current Y coordinate
            resource_type: Type of resource to find ('food' or 'water')
            
        Returns:
            Position of nearby resource or None if not found
        """
        # Check cells within 3-tile radius for better resource detection
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if dx == 0 and dy == 0:
                    continue
                
                check_x, check_y = x + dx, y + dy
                if (0 <= check_x < self.width and 0 <= check_y < self.height):
                    if resource_type == 'food' and (check_x, check_y) in self.food_positions:
                        return (check_x, check_y)
                    elif resource_type == 'water' and (check_x, check_y) in self.water_positions:
                        return (check_x, check_y)
        
        return None
    
    def get_neighboring_positions(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Get all valid neighboring positions for an animal.
        
        Args:
            x: Current X coordinate
            y: Current Y coordinate
            
        Returns:
            List of valid neighboring positions
        """
        neighbors = []
        
        # Check all 8 directions (including diagonals)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # Skip current position
                
                new_x, new_y = x + dx, y + dy
                
                # Check if position is valid and not occupied by another animal
                if (self.is_valid_position(new_x, new_y) and 
                    (new_x, new_y) not in self.animal_positions):
                    neighbors.append((new_x, new_y))
        
        return neighbors
    
    def __str__(self) -> str:
        """String representation of the environment."""
        stats = self.get_statistics()
        return (f"GridWorld({self.width}x{self.height}, "
                f"animals={stats['alive_animals']}, "
                f"food={stats['food_count']}, "
                f"water={stats['water_count']})")
    
    def __repr__(self) -> str:
        """Detailed string representation of the environment."""
        return self.__str__()
