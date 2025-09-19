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

# Import the modular action resolution system
from action_resolution import ActionResolver

# Import the event engine system
from event_engine import EventEngine


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
        
        # Initialize action resolver (lazy initialization)
        self._action_resolver = None
        
        # Initialize event engine (lazy initialization)
        self._event_engine = None
        
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

    def execute_action_resolution_system(self, week: int) -> Dict[str, Any]:
        """
        Execute the complete 4-phase action resolution system using the modular system.
        
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
        # Initialize the action resolver if not already done
        if self._action_resolver is None:
            self._action_resolver = ActionResolver(self.simulation, self.logger)
        
        # Execute the action resolution system
        return self._action_resolver.execute_action_resolution_system(week)
    
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
        # Extract affected animals from action resolution result
        affected_animals = action_result.get('affected_animals', [])
        
        return {
            'type': 'movement',
            'week': week,
            'timestamp': datetime.now(),
            'success': action_result['success'],
            'message': f'Movement event with action resolution: {action_result["message"]}',
            'affected_animals': affected_animals,
            'casualties': action_result['casualties'],
            'actions_processed': action_result.get('actions_processed', 0),
            'conflicts_resolved': action_result.get('conflicts_resolved', 0),
            'phases_completed': action_result.get('phases_completed', 0),
            'action_resolution_details': action_result
        }
    
    def _execute_triggered_event(self, week: int) -> Dict[str, Any]:
        """Execute triggered events using the Event Engine."""
        # Initialize the event engine if not already done
        if self._event_engine is None:
            self._event_engine = EventEngine(self.simulation, self.logger)
        
        # Execute only triggered events
        event_results = self._event_engine.scheduler.triggered_engine.check_and_execute_events(week)
        
        # Convert to the expected format
        total_casualties = sum(r.casualties for r in event_results)
        affected_animals = []
        for result in event_results:
            affected_animals.extend(result.affected_animals)
        
        message = f"Triggered events: {len(event_results)} executed"
        if event_results:
            messages = [r.message for r in event_results if r.success]
            if messages:
                message = "; ".join(messages)
        
        return {
            'type': 'triggered_event',
            'week': week,
            'timestamp': datetime.now(),
            'success': True,  # Always successful - no events triggering is normal
            'message': message,
            'affected_animals': affected_animals,
            'casualties': total_casualties,
            'event_details': event_results
        }
    
    def _execute_random_event(self, week: int) -> Dict[str, Any]:
        """Execute random events using the Event Engine."""
        # Initialize the event engine if not already done
        if self._event_engine is None:
            self._event_engine = EventEngine(self.simulation, self.logger)
        
        # Execute only random events
        event_results = self._event_engine.scheduler.random_engine.execute_random_events(week, max_events=1)
        
        # Convert to the expected format
        total_casualties = sum(r.casualties for r in event_results)
        affected_animals = []
        for result in event_results:
            affected_animals.extend(result.affected_animals)
        
        message = f"Random events: {len(event_results)} executed"
        if event_results:
            messages = [r.message for r in event_results if r.success]
            if messages:
                message = "; ".join(messages)
        
        return {
            'type': 'random_event',
            'week': week,
            'timestamp': datetime.now(),
            'success': True,
            'message': message,
            'affected_animals': affected_animals,
            'casualties': total_casualties,
            'event_details': event_results
        }
    
    def _execute_disaster_event(self, week: int) -> Dict[str, Any]:
        """Execute disaster events using the Event Engine."""
        # Initialize the event engine if not already done
        if self._event_engine is None:
            self._event_engine = EventEngine(self.simulation, self.logger)
        
        # Execute only disaster events
        event_results = self._event_engine.scheduler.disaster_engine.execute_disaster_events(week, max_disasters=1)
        
        # Convert to the expected format
        total_casualties = sum(r.casualties for r in event_results)
        affected_animals = []
        for result in event_results:
            affected_animals.extend(result.affected_animals)
        
        # Check if there are no living animals
        living_animals = self.simulation.get_living_animals()
        if not living_animals:
            message = "Disaster events: 0 executed - no animals to affect"
        else:
            message = f"Disaster events: {len(event_results)} executed"
            if event_results:
                messages = [r.message for r in event_results if r.success]
                if messages:
                    message = "; ".join(messages)
        
        return {
            'type': 'disaster',
            'week': week,
            'timestamp': datetime.now(),
            'success': True,
            'message': message,
            'affected_animals': affected_animals,
            'casualties': total_casualties,
            'event_details': event_results
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
