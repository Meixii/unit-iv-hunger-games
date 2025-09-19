"""
EvoSim Simulation Controller

This module contains the main simulation controller that orchestrates the entire simulation.
It handles world initialization, population management, event scheduling, and overall control flow.

Reference: Section IV.A - Simulation Flow from documentation.md
Reference: Section XI - Conceptual Data Structure from documentation.md
"""

from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
import random
import logging
from datetime import datetime
from enum import Enum

from data_structures import (
    Simulation, World, Animal, Effect,
    AnimalCategory, TerrainType, EffectType, ActionType
)
from world_generator import WorldGenerator, GenerationConfig
from animal_creator import AnimalCreator, AnimalCustomizer


# =============================================================================
# SIMULATION CONTROLLER CLASS
# =============================================================================

@dataclass
class SimulationConfig:
    """Configuration for simulation parameters."""
    max_weeks: int = 20
    max_generations: int = 10
    population_size: int = 20
    enable_logging: bool = True
    log_level: str = "INFO"
    random_seed: Optional[int] = None
    world_config: Optional[GenerationConfig] = None
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.max_weeks <= 0:
            raise ValueError(f"Max weeks must be positive, got {self.max_weeks}")
        if self.max_generations <= 0:
            raise ValueError(f"Max generations must be positive, got {self.max_generations}")
        if self.population_size <= 0:
            raise ValueError(f"Population size must be positive, got {self.population_size}")


class SimulationController:
    """
    Main simulation controller that orchestrates the entire EvoSim simulation.
    
    This class handles:
    - World and population initialization
    - Event queue management and scheduling
    - Simulation state tracking and validation
    - Logging and debugging capabilities
    - Overall control flow coordination
    """
    
    def __init__(self, config: Optional[SimulationConfig] = None):
        """
        Initialize the simulation controller.
        
        Args:
            config: Simulation configuration. If None, uses default values.
        """
        self.config = config or SimulationConfig()
        self.simulation = Simulation()
        self.world_generator = WorldGenerator(self.config.world_config)
        self.animal_creator = AnimalCreator()
        self.animal_customizer = AnimalCustomizer()
        
        # Setup logging
        self._setup_logging()
        
        # Set random seed if specified
        if self.config.random_seed is not None:
            random.seed(self.config.random_seed)
            self.logger.info(f"Random seed set to: {self.config.random_seed}")
        
        # Simulation state
        self.current_generation = 0
        self.is_running = False
        self.is_paused = False
        self.simulation_start_time = None
        self.simulation_end_time = None
        
        # Statistics tracking
        self.generation_stats = []
        self.weekly_stats = []
        
        self.logger.info("Simulation controller initialized")
    
    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        log_level = getattr(logging, self.config.log_level.upper(), logging.INFO)
        
        # Create logger
        self.logger = logging.getLogger(f"EvoSim_{id(self)}")
        self.logger.setLevel(log_level)
        
        if not self.logger.handlers:
            # Create console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            
            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            
            # Add handler to logger
            self.logger.addHandler(console_handler)
    
    def initialize_world(self, world_config: Optional[GenerationConfig] = None) -> World:
        """
        Initialize the simulation world.
        
        Args:
            world_config: World generation configuration. If None, uses default.
            
        Returns:
            The generated world.
            
        Raises:
            ValueError: If world generation fails.
        """
        try:
            self.logger.info("Initializing world...")
            
            # Use provided config or default
            config = world_config or self.config.world_config or GenerationConfig()
            
            # Create world generator with the config
            world_generator = WorldGenerator(config)
            
            # Generate world
            world = world_generator.generate_world()
            
            # Validate world
            if not world:
                raise ValueError("World generation failed - no world created")
            
            # Set world in simulation
            self.simulation.world = world
            
            self.logger.info(f"World initialized: {world.dimensions[0]}x{world.dimensions[1]} grid")
            self.logger.info(f"Terrain distribution: {self._get_terrain_stats(world)}")
            
            return world
            
        except Exception as e:
            self.logger.error(f"Failed to initialize world: {e}")
            raise
    
    def initialize_population(self, population_size: Optional[int] = None) -> List[Animal]:
        """
        Initialize the simulation population.
        
        Args:
            population_size: Number of animals to create. If None, uses config value.
            
        Returns:
            List of created animals.
            
        Raises:
            ValueError: If population initialization fails.
        """
        try:
            size = population_size or self.config.population_size
            self.logger.info(f"Initializing population of {size} animals...")
            
            if not self.simulation.world:
                raise ValueError("World must be initialized before population")
            
            # Create animals with even distribution across categories
            animals = []
            categories = list(AnimalCategory)
            animals_per_category = size // len(categories)
            remaining = size % len(categories)
            
            for i, category in enumerate(categories):
                # Add one extra animal to some categories if there's a remainder
                count = animals_per_category + (1 if i < remaining else 0)
                
                for j in range(count):
                    animal_id = f"{category.value}_{i}_{j}"
                    animal = self.animal_customizer.create_balanced_animal(animal_id, category)
                    animals.append(animal)
            
            # Place animals in the world
            placed_animals = self._place_animals_in_world(animals)
            
            # Add to simulation population
            for animal in placed_animals:
                self.simulation.add_animal(animal)
            
            self.logger.info(f"Population initialized: {len(placed_animals)} animals placed")
            self.logger.info(f"Category distribution: {self._get_category_stats(placed_animals)}")
            
            return placed_animals
            
        except Exception as e:
            self.logger.error(f"Failed to initialize population: {e}")
            raise
    
    def _place_animals_in_world(self, animals: List[Animal]) -> List[Animal]:
        """
        Place animals in valid locations in the world.
        
        Args:
            animals: List of animals to place.
            
        Returns:
            List of successfully placed animals.
        """
        if not self.simulation.world:
            raise ValueError("World not initialized")
        
        placed_animals = []
        world = self.simulation.world
        
        # Get all valid spawn locations (plains tiles without occupants)
        valid_locations = []
        for x in range(world.dimensions[0]):
            for y in range(world.dimensions[1]):
                tile = world.get_tile(x, y)
                if (tile and 
                    tile.terrain_type == TerrainType.PLAINS and 
                    tile.occupant is None):
                    valid_locations.append((x, y))
        
        if len(valid_locations) < len(animals):
            self.logger.warning(
                f"Not enough valid spawn locations ({len(valid_locations)}) "
                f"for all animals ({len(animals)}). Some animals will not be placed."
            )
        
        # Shuffle locations for random placement
        random.shuffle(valid_locations)
        
        # Place animals
        for i, animal in enumerate(animals):
            if i < len(valid_locations):
                x, y = valid_locations[i]
                animal.location = (x, y)
                
                # Set animal as occupant of the tile
                tile = world.get_tile(x, y)
                if tile:
                    tile.occupant = animal
                    placed_animals.append(animal)
        
        return placed_animals
    
    def _get_terrain_stats(self, world: World) -> Dict[str, int]:
        """Get terrain distribution statistics."""
        stats = {}
        for x in range(world.dimensions[0]):
            for y in range(world.dimensions[1]):
                tile = world.get_tile(x, y)
                if tile:
                    terrain = tile.terrain_type.value
                    stats[terrain] = stats.get(terrain, 0) + 1
        return stats
    
    def _get_category_stats(self, animals: List[Animal]) -> Dict[str, int]:
        """Get animal category distribution statistics."""
        stats = {}
        for animal in animals:
            category = animal.category.value
            stats[category] = stats.get(category, 0) + 1
        return stats
    
    def start_simulation(self) -> None:
        """
        Start the simulation.
        
        Raises:
            ValueError: If simulation is already running or not properly initialized.
        """
        if self.is_running:
            raise ValueError("Simulation is already running")
        
        if not self.simulation.world:
            raise ValueError("World must be initialized before starting simulation")
        
        if not self.simulation.population:
            raise ValueError("Population must be initialized before starting simulation")
        
        self.is_running = True
        self.is_paused = False
        self.simulation_start_time = datetime.now()
        
        self.logger.info("Simulation started")
        self.logger.info(f"Generation: {self.current_generation}")
        self.logger.info(f"Week: {self.simulation.current_week}")
        self.logger.info(f"Population: {len(self.simulation.get_living_animals())} living animals")
    
    def pause_simulation(self) -> None:
        """Pause the simulation."""
        if not self.is_running:
            raise ValueError("Simulation is not running")
        
        self.is_paused = True
        self.logger.info("Simulation paused")
    
    def resume_simulation(self) -> None:
        """Resume the simulation."""
        if not self.is_running:
            raise ValueError("Simulation is not running")
        
        self.is_paused = False
        self.logger.info("Simulation resumed")
    
    def stop_simulation(self) -> None:
        """Stop the simulation."""
        self.is_running = False
        self.is_paused = False
        self.simulation_end_time = datetime.now()
        
        if self.simulation_start_time:
            duration = self.simulation_end_time - self.simulation_start_time
            self.logger.info(f"Simulation stopped. Duration: {duration}")
        else:
            self.logger.info("Simulation stopped")
    
    def reset_simulation(self) -> None:
        """Reset the simulation to initial state."""
        self.stop_simulation()
        self.simulation.reset()
        self.current_generation = 0
        self.generation_stats.clear()
        self.weekly_stats.clear()
        self.simulation_start_time = None
        self.simulation_end_time = None
        
        self.logger.info("Simulation reset to initial state")
    
    def get_simulation_status(self) -> Dict[str, Any]:
        """
        Get current simulation status.
        
        Returns:
            Dictionary containing simulation status information.
        """
        living_animals = self.simulation.get_living_animals()
        dead_animals = self.simulation.get_dead_animals()
        
        return {
            "is_running": self.is_running,
            "is_paused": self.is_paused,
            "current_generation": self.current_generation,
            "current_week": self.simulation.current_week,
            "total_population": len(self.simulation.population),
            "living_animals": len(living_animals),
            "dead_animals": len(dead_animals),
            "world_initialized": self.simulation.world is not None,
            "population_initialized": len(self.simulation.population) > 0,
            "simulation_start_time": self.simulation_start_time,
            "simulation_end_time": self.simulation_end_time,
            "event_queue_length": len(self.simulation.event_queue)
        }
    
    def get_generation_stats(self) -> List[Dict[str, Any]]:
        """
        Get statistics for all completed generations.
        
        Returns:
            List of generation statistics dictionaries.
        """
        return self.generation_stats.copy()
    
    def get_weekly_stats(self) -> List[Dict[str, Any]]:
        """
        Get statistics for all completed weeks.
        
        Returns:
            List of weekly statistics dictionaries.
        """
        return self.weekly_stats.copy()
    
    def validate_simulation_state(self) -> bool:
        """
        Validate the current simulation state.
        
        Returns:
            True if simulation state is valid, False otherwise.
        """
        try:
            # Check basic state
            if self.simulation.current_week < 0:
                self.logger.error("Current week is negative")
                return False
            
            # Check world
            if not self.simulation.world:
                self.logger.error("World not initialized")
                return False
            
            # Check population
            if not self.simulation.population:
                self.logger.error("Population not initialized")
                return False
            
            # Check animal locations
            for animal in self.simulation.population:
                if not animal.location:
                    self.logger.error(f"Animal {animal.animal_id} has no location")
                    return False
                
                x, y = animal.location
                tile = self.simulation.world.get_tile(x, y)
                if not tile:
                    self.logger.error(f"Animal {animal.animal_id} at invalid location ({x}, {y})")
                    return False
                
                if tile.occupant != animal:
                    self.logger.error(f"Animal {animal.animal_id} not properly registered as tile occupant")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Simulation state validation failed: {e}")
            return False
    
    def log_simulation_state(self) -> None:
        """Log current simulation state for debugging."""
        status = self.get_simulation_status()
        
        self.logger.info("=== SIMULATION STATE ===")
        self.logger.info(f"Running: {status['is_running']}")
        self.logger.info(f"Paused: {status['is_paused']}")
        self.logger.info(f"Generation: {status['current_generation']}")
        self.logger.info(f"Week: {status['current_week']}")
        self.logger.info(f"Population: {status['living_animals']} living, {status['dead_animals']} dead")
        self.logger.info(f"World initialized: {status['world_initialized']}")
        self.logger.info(f"Event queue length: {status['event_queue_length']}")
        
        if self.simulation.world:
            self.logger.info(f"World size: {self.simulation.world.dimensions[0]}x{self.simulation.world.dimensions[1]}")
        
        # Log animal details
        living_animals = self.simulation.get_living_animals()
        if living_animals:
            self.logger.info("=== LIVING ANIMALS ===")
            for animal in living_animals[:5]:  # Log first 5 animals
                self.logger.info(
                    f"  {animal.animal_id}: {animal.category.value} at {animal.location}, "
                    f"Health: {animal.status['Health']:.1f}, "
                    f"Hunger: {animal.status['Hunger']:.1f}"
                )
            if len(living_animals) > 5:
                self.logger.info(f"  ... and {len(living_animals) - 5} more animals")


# =============================================================================
# ACTION RESOLUTION SYSTEM
# =============================================================================

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


    def execute_action_resolution_system(self, week: int) -> Dict[str, Any]:
        """
        Execute the complete 4-phase action resolution system.
        
        This implements the turn-based action processing as specified in Section IV.B:
        1. Decision Phase: Collect actions from all animals
        2. Status & Environmental Phase: Apply passive effects
        3. Action Execution Phase: Execute actions by priority
        4. Cleanup Phase: Apply new effects and remove expired ones
        
        Args:
            week: Current week number for logging.
            
        Returns:
            Dictionary containing detailed results of the action resolution.
        """
        self.logger.info("🎯 Starting Action Resolution System")
        
        start_time = datetime.now()
        living_animals = self.simulation.get_living_animals()
        
        if not living_animals:
            return {
                'phase': 'action_resolution',
                'week': week,
                'success': True,
                'message': 'No living animals to process',
                'phases_completed': 0,
                'actions_processed': 0,
                'casualties': 0,
                'duration': datetime.now() - start_time
            }
        
        try:
            # Phase 1: Decision Phase
            self.logger.info("📋 Phase 1: Decision Phase")
            planned_actions = self._execute_decision_phase(living_animals)
            self.logger.info(f"   Collected {len(planned_actions)} actions from {len(living_animals)} animals")
            
            # Phase 2: Status & Environmental Phase
            self.logger.info("🌡️ Phase 2: Status & Environmental Phase")
            status_results = self._execute_status_environmental_phase(living_animals)
            self.logger.info(f"   Applied passive effects to {len(living_animals)} animals")
            
            # Phase 3: Action Execution Phase
            self.logger.info("⚡ Phase 3: Action Execution Phase")
            execution_results = self._execute_action_execution_phase(planned_actions)
            self.logger.info(f"   Executed {len(planned_actions)} actions with {execution_results['conflicts']} conflicts")
            
            # Phase 4: Cleanup Phase
            self.logger.info("🧹 Phase 4: Cleanup Phase")
            cleanup_results = self._execute_cleanup_phase(living_animals)
            self.logger.info(f"   Applied {cleanup_results['effects_added']} new effects, removed {cleanup_results['effects_removed']} expired effects")
            
            # Calculate final results
            final_living = self.simulation.get_living_animals()
            casualties = len(living_animals) - len(final_living)
            
            result = {
                'phase': 'action_resolution',
                'week': week,
                'success': True,
                'message': f'Action resolution completed successfully. {casualties} casualties.',
                'phases_completed': 4,
                'actions_processed': len(planned_actions),
                'casualties': casualties,
                'conflicts_resolved': execution_results['conflicts'],
                'duration': datetime.now() - start_time,
                'phase_results': {
                    'decision': {'actions_collected': len(planned_actions)},
                    'status_environmental': status_results,
                    'action_execution': execution_results,
                    'cleanup': cleanup_results
                }
            }
            
            self.logger.info(f"✅ Action Resolution Complete: {len(planned_actions)} actions, {casualties} casualties")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Action resolution failed: {e}")
            return {
                'phase': 'action_resolution',
                'week': week,
                'success': False,
                'message': f'Action resolution failed: {str(e)}',
                'phases_completed': 0,
                'actions_processed': 0,
                'casualties': 0,
                'duration': datetime.now() - start_time
            }
    
    def _execute_decision_phase(self, living_animals: List[Animal]) -> List[AnimalAction]:
        """
        Phase 1: Decision Phase
        Collect actions from all living animals using simple decision logic.
        In the future, this will integrate with MLP neural networks.
        """
        planned_actions = []
        
        for animal in living_animals:
            try:
                # For now, use simple rule-based decision making
                # This will be replaced with MLP integration in Phase 3
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
        Make a decision for an animal using simple rule-based logic.
        This is a placeholder that will be replaced with MLP neural networks.
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
                    if tile and tile.resources:
                        for resource in tile.resources:
                            if ((resource_type == 'food' and resource.resource_type.value in ['Plant', 'Prey', 'Carcass']) or
                                (resource_type == 'water' and resource.resource_type.value == 'Water')):
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
    
    def _execute_status_environmental_phase(self, living_animals: List[Animal]) -> Dict[str, Any]:
        """
        Phase 2: Status & Environmental Phase
        Apply passive changes to all animals simultaneously.
        """
        results = {
            'animals_processed': 0,
            'hunger_depletion': 0,
            'thirst_depletion': 0,
            'health_loss': 0,
            'energy_regeneration': 0,
            'casualties': []
        }
        
        animals_to_remove = []
        
        for animal in living_animals:
            try:
                # Apply hunger depletion
                current_hunger = animal.status.get('Hunger', 100)
                new_hunger = max(0, current_hunger - 3)  # Lose 3 hunger per turn
                animal.status['Hunger'] = new_hunger
                if current_hunger != new_hunger:
                    results['hunger_depletion'] += 1
                
                # Apply thirst depletion
                current_thirst = animal.status.get('Thirst', 100)
                new_thirst = max(0, current_thirst - 2)  # Lose 2 thirst per turn
                animal.status['Thirst'] = new_thirst
                if current_thirst != new_thirst:
                    results['thirst_depletion'] += 1
                
                # Apply health loss from debuffs
                health_loss = 0
                for effect in animal.effects:
                    if effect.effect_type == EffectType.POISONED:
                        health_loss += 5
                    elif effect.effect_type == EffectType.BLEEDING:
                        health_loss += 3
                
                if health_loss > 0:
                    current_health = animal.status.get('Health', 100)
                    new_health = max(0, current_health - health_loss)
                    animal.status['Health'] = new_health
                    results['health_loss'] += 1
                
                # Apply passive energy regeneration (if resting or healthy)
                current_energy = animal.status.get('Energy', 100)
                if current_energy < 100:
                    energy_regen = 2 if animal.status.get('Health', 100) > 50 else 1
                    new_energy = min(100, current_energy + energy_regen)
                    animal.status['Energy'] = new_energy
                    if current_energy != new_energy:
                        results['energy_regeneration'] += 1
                
                # Check for death conditions
                if (animal.status.get('Health', 100) <= 0 or 
                    animal.status.get('Hunger', 100) <= 0 or 
                    animal.status.get('Thirst', 100) <= 0):
                    
                    death_cause = []
                    if animal.status.get('Health', 100) <= 0:
                        death_cause.append("health")
                    if animal.status.get('Hunger', 100) <= 0:
                        death_cause.append("starvation")
                    if animal.status.get('Thirst', 100) <= 0:
                        death_cause.append("dehydration")
                    
                    self.logger.info(f"Animal {animal.animal_id} died from {', '.join(death_cause)}")
                    animals_to_remove.append(animal)
                    results['casualties'].append({
                        'animal_id': animal.animal_id,
                        'cause': ', '.join(death_cause)
                    })
                
                results['animals_processed'] += 1
                
            except Exception as e:
                self.logger.warning(f"Status phase failed for animal {animal.animal_id}: {e}")
        
        # Remove dead animals
        for animal in animals_to_remove:
            self.simulation.remove_animal(animal)
        
        return results
    
    def _execute_action_execution_phase(self, planned_actions: List[AnimalAction]) -> Dict[str, Any]:
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
        
        # Find consumable food resource
        food_resource = None
        for resource in tile.resources:
            if resource.resource_type.value in ['Plant', 'Prey', 'Carcass']:
                food_resource = resource
                break
        
        if not food_resource:
            action.success = False
            action.result_message = "No food available at location"
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
        
        # Consume the resource
        food_resource.uses -= 1
        if food_resource.uses <= 0:
            tile.resources.remove(food_resource)
        
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
        
        # Find water resource
        water_resource = None
        for resource in tile.resources:
            if resource.resource_type.value == 'Water':
                water_resource = resource
                break
        
        if not water_resource:
            action.success = False
            action.result_message = "No water available at location"
            return False
        
        # Consume energy for the action
        animal.status['Energy'] = max(0, animal.status.get('Energy', 100) - action.energy_cost)
        
        # Restore thirst
        thirst_restored = 50
        current_thirst = animal.status.get('Thirst', 100)
        animal.status['Thirst'] = min(100, current_thirst + thirst_restored)
        
        # Water resources typically don't get depleted as quickly
        if random.random() < 0.1:  # 10% chance to deplete water
            water_resource.uses -= 1
            if water_resource.uses <= 0:
                tile.resources.remove(water_resource)
        
        action.success = True
        action.result_message = f"Drank water: +{thirst_restored} thirst"
        
        self.logger.debug(f"Animal {animal.animal_id} drank water: +{thirst_restored} thirst")
        return True
    
    def _execute_attack_action(self, action: AnimalAction) -> bool:
        """Execute attack action - combat with another animal."""
        animal = action.animal
        
        # For now, implement basic attack logic
        # This will be expanded with proper combat mechanics
        
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
        sorted_actions = sorted(
            conflicting_actions, 
            key=lambda a: a.animal.traits.get('Agility', 50), 
            reverse=True
        )
        
        winner = sorted_actions[0]
        winner_agility = winner.animal.traits.get('Agility', 50)
        
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
    
    def _execute_cleanup_phase(self, living_animals: List[Animal]) -> Dict[str, Any]:
        """
        Phase 4: Cleanup Phase
        Apply new effects and remove expired effects.
        """
        results = {
            'animals_processed': 0,
            'effects_added': 0,
            'effects_removed': 0,
            'effects_updated': 0
        }
        
        for animal in living_animals:
            try:
                # Process existing effects
                effects_to_remove = []
                
                for effect in animal.effects:
                    # Decrease duration
                    if hasattr(effect, 'duration') and effect.duration > 0:
                        effect.duration -= 1
                        results['effects_updated'] += 1
                        
                        # Mark for removal if expired
                        if effect.duration <= 0:
                            effects_to_remove.append(effect)
                
                # Remove expired effects
                for effect in effects_to_remove:
                    animal.effects.remove(effect)
                    results['effects_removed'] += 1
                    self.logger.debug(f"Removed expired effect {effect.effect_type.value} from {animal.animal_id}")
                
                # Add new effects based on conditions
                # Well-Fed effect after eating
                if animal.status.get('Hunger', 100) >= 90 and not any(e.effect_type == EffectType.WELL_FED for e in animal.effects):
                    well_fed_effect = Effect(
                        effect_type=EffectType.WELL_FED,
                        duration=3,
                        strength=1.0
                    )
                    animal.effects.append(well_fed_effect)
                    results['effects_added'] += 1
                    self.logger.debug(f"Added Well-Fed effect to {animal.animal_id}")
                
                # Exhausted effect from low energy
                if animal.status.get('Energy', 100) <= 20 and not any(e.effect_type == EffectType.EXHAUSTED for e in animal.effects):
                    exhausted_effect = Effect(
                        effect_type=EffectType.EXHAUSTED,
                        duration=2,
                        strength=1.0
                    )
                    animal.effects.append(exhausted_effect)
                    results['effects_added'] += 1
                    self.logger.debug(f"Added Exhausted effect to {animal.animal_id}")
                
                results['animals_processed'] += 1
                
            except Exception as e:
                self.logger.warning(f"Cleanup phase failed for animal {animal.animal_id}: {e}")
        
        return results


# =============================================================================
# GAME LOOP IMPLEMENTATION
# =============================================================================

    def run_generation(self, max_weeks: Optional[int] = None) -> Dict[str, Any]:
        """
        Run a complete generation of the simulation.
        
        Args:
            max_weeks: Maximum number of weeks to run. If None, uses config value.
            
        Returns:
            Dictionary containing generation results and statistics.
            
        Raises:
            ValueError: If simulation is not properly initialized.
        """
        try:
            # Validate simulation state
            if not self.simulation.world:
                raise ValueError("World must be initialized before running generation")
            if not self.simulation.population:
                raise ValueError("Population must be initialized before running generation")
            
            max_weeks = max_weeks or self.config.max_weeks
            
            self.logger.info("=== STARTING GENERATION ===")
            self.logger.info(f"Generation {self.current_generation}")
            self.logger.info(f"Starting population: {len(self.simulation.get_living_animals())} animals")
            self.logger.info(f"Maximum weeks: {max_weeks}")
            
            # Initialize generation tracking
            generation_start_time = datetime.now()
            week = 1
            generation_events = []
            
            # Main weekly loop
            while week <= max_weeks:
                self.logger.info(f"--- WEEK {week} ---")
                
                # Run weekly cycle
                week_result = self._run_weekly_cycle(week)
                generation_events.extend(week_result.get('events', []))
                
                # Check win/loss conditions
                living_animals = self.simulation.get_living_animals()
                
                if len(living_animals) <= 1:
                    # Generation complete - single survivor or extinction
                    self.logger.info(f"Generation complete! Survivors: {len(living_animals)}")
                    break
                    
                # Update simulation state
                self.simulation.current_week = week
                week += 1
            
            # Calculate generation results
            generation_end_time = datetime.now()
            generation_duration = generation_end_time - generation_start_time
            
            # Final statistics
            final_living = self.simulation.get_living_animals()
            final_dead = self.simulation.get_dead_animals()
            
            generation_result = {
                'generation': self.current_generation,
                'weeks_completed': week - 1,
                'max_weeks': max_weeks,
                'survivors': len(final_living),
                'casualties': len(final_dead),
                'total_population': len(self.simulation.population),
                'events_count': len(generation_events),
                'duration': generation_duration,
                'winner': final_living[0] if len(final_living) == 1 else None,
                'extinction': len(final_living) == 0,
                'events': generation_events
            }
            
            # Log generation completion
            self.logger.info("=== GENERATION COMPLETE ===")
            self.logger.info(f"Weeks completed: {week - 1}/{max_weeks}")
            self.logger.info(f"Final survivors: {len(final_living)}")
            self.logger.info(f"Total casualties: {len(final_dead)}")
            self.logger.info(f"Duration: {generation_duration}")
            
            if generation_result['winner']:
                self.logger.info(f"Winner: {generation_result['winner'].animal_id}")
            elif generation_result['extinction']:
                self.logger.info("Result: EXTINCTION - No survivors")
            else:
                self.logger.info("Result: TIME LIMIT REACHED")
            
            # Store generation statistics
            self.generation_stats.append(generation_result)
            
            return generation_result
            
        except Exception as e:
            self.logger.error(f"Generation failed: {e}")
            raise
    
    def _run_weekly_cycle(self, week: int) -> Dict[str, Any]:
        """
        Run a single week of the simulation.
        
        Args:
            week: Current week number.
            
        Returns:
            Dictionary containing week results and events.
        """
        week_events = []
        
        try:
            self.logger.info(f"Starting week {week}")
            
            # Get event schedule for this week
            event_schedule = self._get_weekly_event_schedule(week)
            
            # Execute events in order
            for event_type in event_schedule:
                event_result = self._execute_event(event_type, week)
                week_events.append(event_result)
                
                # Check if any animals died during this event
                living_count = len(self.simulation.get_living_animals())
                if living_count <= 1:
                    self.logger.info(f"Early termination: {living_count} animals remaining")
                    break
            
            # Week completion
            week_result = {
                'week': week,
                'events': week_events,
                'living_animals': len(self.simulation.get_living_animals()),
                'dead_animals': len(self.simulation.get_dead_animals())
            }
            
            self.logger.info(f"Week {week} complete: {week_result['living_animals']} living, {week_result['dead_animals']} dead")
            
            # Store weekly statistics
            self.weekly_stats.append(week_result)
            
            return week_result
            
        except Exception as e:
            self.logger.error(f"Week {week} failed: {e}")
            raise
    
    def _get_weekly_event_schedule(self, week: int) -> List[str]:
        """
        Get the event schedule for a given week.
        
        Week 1 has a fixed order, subsequent weeks are randomized.
        
        Args:
            week: Week number.
            
        Returns:
            List of event types in execution order.
        """
        if week == 1:
            # Fixed order for Week 1
            return [
                'movement',
                'triggered_event',
                'random_event',
                'disaster',
                'triggered_event',
                'movement',
                'triggered_event'
            ]
        else:
            # Randomized order for subsequent weeks
            base_events = ['movement', 'triggered_event', 'random_event']
            
            # Add disaster with probability
            if random.random() < 0.3:  # 30% chance of disaster
                base_events.append('disaster')
            
            # Add extra events randomly
            extra_events = random.choices(['movement', 'triggered_event'], k=random.randint(1, 3))
            base_events.extend(extra_events)
            
            # Shuffle the events
            random.shuffle(base_events)
            
            return base_events
    
    def _execute_event(self, event_type: str, week: int) -> Dict[str, Any]:
        """
        Execute a specific event type.
        
        Args:
            event_type: Type of event to execute.
            week: Current week number.
            
        Returns:
            Dictionary containing event results.
        """
        self.logger.debug(f"Executing {event_type} event")
        
        event_result = {
            'type': event_type,
            'week': week,
            'timestamp': datetime.now(),
            'success': True,
            'message': '',
            'affected_animals': [],
            'casualties': 0
        }
        
        try:
            if event_type == 'movement':
                event_result = self._execute_movement_event(week)
            elif event_type == 'triggered_event':
                event_result = self._execute_triggered_event(week)
            elif event_type == 'random_event':
                event_result = self._execute_random_event(week)
            elif event_type == 'disaster':
                event_result = self._execute_disaster_event(week)
            else:
                self.logger.warning(f"Unknown event type: {event_type}")
                event_result['success'] = False
                event_result['message'] = f"Unknown event type: {event_type}"
            
            return event_result
            
        except Exception as e:
            self.logger.error(f"Event {event_type} failed: {e}")
            event_result['success'] = False
            event_result['message'] = str(e)
            return event_result
    
    def _execute_movement_event(self, week: int) -> Dict[str, Any]:
        """
        Execute a movement event using the 4-phase Action Resolution System.
        
        This implements the complete turn-based action processing as specified in Section IV.B.
        """
        self.logger.info("Executing movement event with Action Resolution System")
        
        # Execute the complete 4-phase action resolution system
        action_result = self.execute_action_resolution_system(week)
        
        # Convert action resolution result to movement event format
        return {
            'type': 'movement',
            'week': week,
            'timestamp': datetime.now(),
            'success': action_result['success'],
            'message': f'Movement event with action resolution: {action_result["message"]}',
            'affected_animals': [],  # This would need to be extracted from action_result if needed
            'casualties': action_result['casualties'],
            'actions_processed': action_result.get('actions_processed', 0),
            'conflicts_resolved': action_result.get('conflicts_resolved', 0),
            'phases_completed': action_result.get('phases_completed', 0),
            'action_resolution_details': action_result
        }
    
    def _execute_triggered_event(self, week: int) -> Dict[str, Any]:
        """Execute a triggered event (placeholder implementation)."""
        self.logger.debug("Executing triggered event")
        
        return {
            'type': 'triggered_event',
            'week': week,
            'timestamp': datetime.now(),
            'success': True,
            'message': 'Triggered event completed (placeholder)',
            'affected_animals': [],
            'casualties': 0
        }
    
    def _execute_random_event(self, week: int) -> Dict[str, Any]:
        """Execute a random event (placeholder implementation)."""
        self.logger.debug("Executing random event")
        
        return {
            'type': 'random_event',
            'week': week,
            'timestamp': datetime.now(),
            'success': True,
            'message': 'Random event completed (placeholder)',
            'affected_animals': [],
            'casualties': 0
        }
    
    def _execute_disaster_event(self, week: int) -> Dict[str, Any]:
        """Execute a disaster event (placeholder implementation)."""
        self.logger.info("Executing disaster event")
        
        # Placeholder: Random disaster affects some animals
        living_animals = self.simulation.get_living_animals()
        if not living_animals:
            return {
                'type': 'disaster',
                'week': week,
                'timestamp': datetime.now(),
                'success': True,
                'message': 'Disaster event - no animals to affect',
                'affected_animals': [],
                'casualties': 0
            }
        
        # Randomly affect 20-50% of animals
        num_affected = random.randint(1, max(1, len(living_animals) // 2))
        affected_animals = random.sample(living_animals, num_affected)
        casualties = []
        
        for animal in affected_animals:
            # Apply disaster damage
            damage = random.randint(10, 30)
            animal.status['Health'] = max(0, animal.status.get('Health', 100) - damage)
            
            if animal.status['Health'] <= 0:
                self.logger.info(f"Animal {animal.animal_id} died in disaster")
                self.simulation.remove_animal(animal)
                casualties.append(animal.animal_id)
        
        return {
            'type': 'disaster',
            'week': week,
            'timestamp': datetime.now(),
            'success': True,
            'message': f'Disaster struck! {len(casualties)} casualties from {num_affected} affected animals.',
            'affected_animals': [a.animal_id for a in affected_animals],
            'casualties': len(casualties)
        }


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def create_simulation_controller(
    max_weeks: int = 20,
    max_generations: int = 10,
    population_size: int = 20,
    random_seed: Optional[int] = None,
    enable_logging: bool = True
) -> SimulationController:
    """
    Create a simulation controller with specified parameters.
    
    Args:
        max_weeks: Maximum weeks per generation.
        max_generations: Maximum number of generations.
        population_size: Number of animals in population.
        random_seed: Random seed for reproducible results.
        enable_logging: Whether to enable logging.
        
    Returns:
        Configured simulation controller.
    """
    config = SimulationConfig(
        max_weeks=max_weeks,
        max_generations=max_generations,
        population_size=population_size,
        random_seed=random_seed,
        enable_logging=enable_logging
    )
    
    return SimulationController(config)


def validate_simulation_controller(controller: SimulationController) -> bool:
    """
    Validate a simulation controller.
    
    Args:
        controller: Simulation controller to validate.
        
    Returns:
        True if controller is valid, False otherwise.
    """
    try:
        # Check basic attributes
        if not hasattr(controller, 'simulation'):
            return False
        if not hasattr(controller, 'config'):
            return False
        if not hasattr(controller, 'logger'):
            return False
        
        # Check simulation state
        return controller.validate_simulation_state()
        
    except Exception:
        return False
