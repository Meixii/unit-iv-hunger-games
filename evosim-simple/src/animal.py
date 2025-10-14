"""
Animal Implementation for Evolutionary Simulation

This module implements the Animal class that represents individual animals
in the simulation. Each animal has a neural network brain that processes
sensory inputs (hunger, thirst) and makes decisions about actions to take.

Author: Zen Garden
University of Caloocan City
"""

import numpy as np
import uuid
from typing import Tuple, Dict, Optional
from .neural_network import NeuralNetwork


class Animal:
    """
    Individual animal with neural network brain for decision-making.
    
    Each animal has:
    - Position in the grid world
    - Internal state (hunger, thirst, energy, age)
    - Neural network brain for decision-making
    - Fitness tracking for evolution
    """
    
    def __init__(self, x: int, y: int, neural_network: Optional[NeuralNetwork] = None,
                 initial_hunger: float = 100.0, initial_thirst: float = 100.0, 
                 initial_energy: float = 100.0, animal_id: Optional[str] = None,
                 generation: int = 0):
        """
        Initialize an animal with position and neural network brain.
        
        Args:
            x: X coordinate in the grid
            y: Y coordinate in the grid
            neural_network: Neural network brain (creates new one if None)
            initial_hunger: Starting hunger level (0-100)
            initial_thirst: Starting thirst level (0-100)
            initial_energy: Starting energy level (0-100)
            animal_id: Unique identifier for the animal
            generation: Generation when this animal was born
        """
        self.animal_id = animal_id or f"animal_{uuid.uuid4().hex[:12]}"
        self.position = (x, y)
        self.generation = generation  # Track which generation this animal was born in
        self.neural_network = neural_network if neural_network else NeuralNetwork()
        
        # Internal state
        self.hunger = initial_hunger
        self.thirst = initial_thirst
        self.energy = initial_energy
        self.health = 100.0
        self.age = 0
        self.fitness = 0.0
        self.alive = True
        
        # Action tracking for analysis
        self.action_history = []
        self.resource_consumed = {'food': 0, 'water': 0}
        self.movement_count = 0
        
        # Behavioral pattern tracking
        self.behavioral_counts = {
            'move': 0,
            'eat': 0, 
            'drink': 0,
            'rest': 0
        }
        
        # State limits
        self.max_hunger = 100.0
        self.max_thirst = 100.0
        self.max_energy = 100.0
        self.max_health = 100.0
        
        # Decay rates (per time step)
        self.hunger_decay = 0.5  # Increased hunger decay
        self.thirst_decay = 0.5  # Increased thirst decay
        self.energy_decay = 0.2  # Increased energy decay
        self.health_decay = 0.3 # Health decays when hunger/thirst are low
        
        # Action costs
        self.action_costs = {
            'move': 3.0,  # Reduced move cost
            'eat': 1.0,   # Reduced eat cost
            'drink': 1.0, # Reduced drink cost
            'rest': 0.0   # Resting should not cost energy
        }
    
    def sense_environment(self, environment=None) -> Tuple[float, float, float, float]:
        """
        Sense the environment and return normalized inputs for the neural network.
        
        Args:
            environment: GridWorld instance to detect nearby resources
            
        Returns:
            Tuple of (normalized_hunger, normalized_thirst, food_nearby, water_nearby)
        """
        # Normalize hunger and thirst to [0, 1] range
        normalized_hunger = self.hunger / self.max_hunger
        normalized_thirst = self.thirst / self.max_thirst
        
        # Detect nearby resources if environment is provided
        food_nearby = 0.0
        water_nearby = 0.0
        
        if environment:
            x, y = self.position
            # Check cells within 3-5 tile radius for resources (extended field of view)
            for dx in range(-5, 6):
                for dy in range(-5, 6):
                    if dx == 0 and dy == 0:
                        continue  # Skip current position
                    
                    check_x, check_y = x + dx, y + dy
                    if 0 <= check_x < environment.width and 0 <= check_y < environment.height:
                        cell_content = environment.get_cell_content(check_x, check_y)
                        if cell_content == 'food':
                            # Closer food gets higher priority
                            distance = abs(dx) + abs(dy)
                            food_nearby = max(food_nearby, 1.0 / (distance + 1))
                        elif cell_content == 'water':
                            # Closer water gets higher priority
                            distance = abs(dx) + abs(dy)
                            water_nearby = max(water_nearby, 1.0 / (distance + 1))
        
        return (normalized_hunger, normalized_thirst, food_nearby, water_nearby)
    
    def make_decision(self, environment=None) -> str:
        """
        Use neural network to make a decision about what action to take.
        
        Args:
            environment: GridWorld instance for resource detection
            
        Returns:
            Action string: 'move', 'eat', 'drink', or 'rest'
        """
        if not self.alive:
            return 'rest'
        
        # Get sensory inputs (including resource detection)
        inputs = np.array(self.sense_environment(environment))
        
        # Use neural network to decide
        action = self.neural_network.get_decision(inputs)
        
        return action
    
    def get_action_probabilities(self) -> Dict[str, float]:
        """
        Get probability distribution over all possible actions.
        
        Returns:
            Dictionary mapping actions to probabilities
        """
        if not self.alive:
            return {'move': 0.0, 'eat': 0.0, 'drink': 0.0, 'rest': 1.0}
        
        inputs = np.array(self.sense_environment())
        return self.neural_network.get_action_probabilities(inputs)
    
    def execute_action(self, action: str, environment=None) -> bool:
        """
        Execute the chosen action and update animal state.
        
        Args:
            action: Action to execute ('move', 'eat', 'drink', 'rest')
            environment: Environment object for action validation (optional)
            
        Returns:
            True if action was successful, False otherwise
        """
        if not self.alive:
            return False
        
        success = False
        
        if action == 'move':
            success = self._execute_move(environment)
        elif action == 'eat':
            success = self._execute_eat(environment)
        elif action == 'drink':
            success = self._execute_drink(environment)
        elif action == 'rest':
            success = self._execute_rest()
        else:
            raise ValueError(f"Unknown action: {action}")
        
        # Record action in history
        self.action_history.append(action)
        
        # Track behavioral patterns
        if action in self.behavioral_counts:
            self.behavioral_counts[action] += 1
        
        # Update age
        self.age += 1
        
        # Apply natural decay
        self._apply_decay()
        
        # Check survival conditions
        self._check_survival()
        
        return success
    
    def _execute_move(self, environment=None) -> bool:
        """Execute move action."""
        # Check if we have enough energy
        if self.energy < self.action_costs['move']:
            return False
        
        # Consume energy
        self.energy -= self.action_costs['move']
        self.movement_count += 1
        
        # If environment is provided, attempt to move
        if environment:
            # For now, just mark as successful
            # Actual movement will be handled by the environment
            return True
        
        return True
    
    def _execute_eat(self, environment=None) -> bool:
        """Execute eat action."""
        # Check if we have enough energy
        if self.energy < self.action_costs['eat']:
            return False
        
        # Consume energy
        self.energy -= self.action_costs['eat']
        
        # If environment is provided, check for food availability
        if environment:
            # For now, assume food is available and reduce hunger
            # Actual food consumption will be handled by the environment
            self.hunger = min(self.max_hunger, self.hunger + 40)  # Increase hunger (reduce hunger level)
            self.health = min(self.max_health, self.health + 15)  # Improve health
            self.energy = min(self.max_energy, self.energy + 5)  # Eating gives energy
            self.resource_consumed['food'] += 1
            return True
        
        # Without environment, just reduce hunger
        self.hunger = min(self.max_hunger, self.hunger + 40)
        self.health = min(self.max_health, self.health + 15)
        self.energy = min(self.max_energy, self.energy + 5)  # Eating gives energy
        self.resource_consumed['food'] += 1
        return True
    
    def _execute_drink(self, environment=None) -> bool:
        """Execute drink action."""
        # Check if we have enough energy
        if self.energy < self.action_costs['drink']:
            return False
        
        # Consume energy
        self.energy -= self.action_costs['drink']
        
        # If environment is provided, check for water availability
        if environment:
            # For now, assume water is available and reduce thirst
            # Actual water consumption will be handled by the environment
            self.thirst = min(self.max_thirst, self.thirst + 40)  # Increase thirst (reduce thirst level)
            self.health = min(self.max_health, self.health + 15)  # Improve health
            self.energy = min(self.max_energy, self.energy + 5)  # Drinking gives energy
            self.resource_consumed['water'] += 1
            return True
        
        # Without environment, just reduce thirst
        self.thirst = min(self.max_thirst, self.thirst + 40)
        self.health = min(self.max_health, self.health + 15)
        self.energy = min(self.max_energy, self.energy + 5)  # Drinking gives energy
        self.resource_consumed['water'] += 1
        return True
    
    def _execute_rest(self) -> bool:
        """Execute rest action."""
        # Resting doesn't require energy - it's meant to recover energy
        # Resting recovers energy and slowly reduces hunger/thirst
        self.energy = min(self.max_energy, self.energy + 8)  # Increased recovery
        self.hunger = max(0, self.hunger - 1)  # Reduced hunger decay
        self.thirst = max(0, self.thirst - 1)  # Reduced thirst decay
        
        return True
    
    def _apply_decay(self) -> None:
        """Apply natural decay to hunger, thirst, energy, and health."""
        self.hunger = max(0, self.hunger - self.hunger_decay)
        self.thirst = max(0, self.thirst - self.thirst_decay)
        self.energy = max(0, self.energy - self.energy_decay)
        
        # Health decays when hunger or thirst are low
        if self.hunger < 30 or self.thirst < 30:
            # Gradual health decay when resources are low
            decay_rate = self.health_decay * 2 if (self.hunger < 20 or self.thirst < 20) else self.health_decay * 1.5
            self.health = max(0, self.health - decay_rate)
        elif self.hunger > 70 and self.thirst > 70:
            # Health slowly recovers when well-fed
            self.health = min(self.max_health, self.health + 0.05)
    
    def _check_survival(self) -> None:
        """Check if the animal survives based on current state."""
        # Animal dies if health reaches 0 (new health system)
        if self.health <= 0:
            self.alive = False
        
        # Animal dies if both hunger and thirst are 0 for too long
        if self.hunger <= 0 and self.thirst <= 0:
            if not hasattr(self, '_starvation_steps'):
                self._starvation_steps = 0
            self._starvation_steps += 1
            
            # Die after 3 steps of complete starvation
            if self._starvation_steps >= 3:
                self.alive = False
        else:
            # Reset starvation counter if hunger or thirst is restored
            if hasattr(self, '_starvation_steps'):
                self._starvation_steps = 0
        
        # Animal dies if energy reaches 0 AND has been without energy for too long
        if self.energy <= 0:
            # Give animals a grace period when energy hits 0
            if not hasattr(self, '_energy_zero_steps'):
                self._energy_zero_steps = 0
            self._energy_zero_steps += 1
            
            # Die after 5 steps without energy
            if self._energy_zero_steps >= 5:
                self.alive = False
        else:
            # Reset energy zero counter if energy is restored
            if hasattr(self, '_energy_zero_steps'):
                self._energy_zero_steps = 0
    
    def update_state(self) -> None:
        """Update animal state (called each time step)."""
        if not self.alive:
            return
        
        # Apply natural decay
        self._apply_decay()
        
        # Update age
        self.age += 1
        
        # Check survival
        self._check_survival()
    
    def calculate_fitness(self) -> float:
        """
        Calculate fitness score based on survival and behavior.
        
        Returns:
            Fitness score (higher is better)
        """
        if not self.alive:
            return 0.0
        
        # Base fitness from survival time
        survival_bonus = self.age * 10
        
        # Resource efficiency bonus
        resource_efficiency = (self.hunger + self.thirst) / 200.0
        
        # Energy management bonus
        energy_bonus = self.energy / 100.0
        
        # Movement efficiency (animals that move more might be more successful)
        movement_bonus = min(self.movement_count * 0.1, 10.0)
        
        # Resource consumption bonus
        resource_consumption = (self.resource_consumed['food'] + 
                               self.resource_consumed['water']) * 2
        
        # Calculate total fitness
        fitness = (survival_bonus + resource_efficiency + energy_bonus + 
                  movement_bonus + resource_consumption)
        
        self.fitness = fitness
        return fitness
    
    def is_alive(self) -> bool:
        """Check if the animal is alive."""
        return self.alive
    
    def get_state(self) -> Dict:
        """
        Get current animal state as a dictionary.
        
        Returns:
            Dictionary containing all state information
        """
        return {
            'animal_id': self.animal_id,
            'position': self.position,
            'coordinates': {'x': self.position[0], 'y': self.position[1]},
            'hunger': self.hunger,
            'thirst': self.thirst,
            'energy': self.energy,
            'health': self.health,
            'age': self.age,
            'fitness': self.fitness,
            'alive': self.alive,
            'action_count': len(self.action_history),
            'movement_count': self.movement_count,
            'resource_consumed': self.resource_consumed.copy(),
            'behavioral_counts': self.behavioral_counts.copy()
        }
    
    def set_position(self, x: int, y: int) -> None:
        """Set the animal's position."""
        self.position = (x, y)
    
    def get_position(self) -> Tuple[int, int]:
        """Get the animal's current position."""
        return self.position
    
    def add_food(self, amount: float = 30.0) -> None:
        """Add food to reduce hunger."""
        self.hunger = min(self.max_hunger, self.hunger + amount)
        self.health = min(self.max_health, self.health + 10)
        self.resource_consumed['food'] += 1
    
    def add_water(self, amount: float = 30.0) -> None:
        """Add water to reduce thirst."""
        self.thirst = min(self.max_thirst, self.thirst + amount)
        self.health = min(self.max_health, self.health + 10)
        self.resource_consumed['water'] += 1
    
    def get_action_summary(self) -> Dict[str, int]:
        """
        Get summary of actions taken by this animal.
        
        Returns:
            Dictionary with action counts
        """
        action_counts = {'move': 0, 'eat': 0, 'drink': 0, 'rest': 0}
        for action in self.action_history:
            action_counts[action] += 1
        return action_counts
    
    def get_learning_progress(self) -> Dict[str, float]:
        """
        Get learning progress indicators for educational purposes.
        
        Returns:
            Dictionary with learning metrics
        """
        total_actions = len(self.action_history)
        if total_actions == 0:
            return {
                'survival_rate': 0.0,
                'resource_efficiency': 0.0,
                'exploration_rate': 0.0,
                'adaptation_score': 0.0
            }
        
        # Calculate survival rate (how long they've stayed alive)
        survival_rate = min(1.0, self.age / 100.0)  # Normalize to 100 steps
        
        # Calculate resource efficiency (how well they find resources)
        resource_actions = self.behavioral_counts['eat'] + self.behavioral_counts['drink']
        resource_efficiency = resource_actions / total_actions if total_actions > 0 else 0.0
        
        # Calculate exploration rate (how much they move)
        exploration_rate = self.behavioral_counts['move'] / total_actions if total_actions > 0 else 0.0
        
        # Calculate adaptation score (combination of all factors)
        adaptation_score = (survival_rate * 0.4 + resource_efficiency * 0.3 + exploration_rate * 0.3)
        
        return {
            'survival_rate': survival_rate,
            'resource_efficiency': resource_efficiency,
            'exploration_rate': exploration_rate,
            'adaptation_score': adaptation_score
        }
    
    def reset_for_new_generation(self, x: int, y: int) -> None:
        """
        Reset animal for a new generation while preserving the neural network.
        
        Args:
            x: New X coordinate
            y: New Y coordinate
        """
        self.position = (x, y)
        self.hunger = self.max_hunger
        self.thirst = self.max_thirst
        self.energy = self.max_energy
        self.health = self.max_health
        self.age = 0
        self.fitness = 0.0
        self.alive = True
        self.action_history = []
        self.resource_consumed = {'food': 0, 'water': 0}
        self.movement_count = 0
    
    def __str__(self) -> str:
        """String representation of the animal."""
        status = "alive" if self.alive else "dead"
        return (f"Animal(pos={self.position}, {status}, hunger={self.hunger:.1f}, "
                f"thirst={self.thirst:.1f}, energy={self.energy:.1f}, health={self.health:.1f}, age={self.age})")
    
    def __repr__(self) -> str:
        """Detailed string representation of the animal."""
        return self.__str__()
