"""
Simulation Engine for Evolutionary Simulation

This module implements the main simulation controller that coordinates
all components of the evolutionary simulation system.

Author: Zen Garden
University of Caloocan City
"""

import time
import threading
from typing import Dict, List, Optional, Callable, Any
from enum import Enum

from .environment import GridWorld
from .events import EventManager
from .evolution import Population, EvolutionManager
from .animal import Animal
from .neural_network import NeuralNetwork


class SimulationState(Enum):
    """Simulation state enumeration."""
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"
    EVOLVING = "evolving"
    FINISHED = "finished"


class Simulation:
    """
    Main simulation controller for the evolutionary simulation.
    
    Coordinates all components:
    - Environment (GridWorld)
    - Events (EventManager)
    - Population (Population)
    - Evolution (EvolutionManager)
    - Time management
    - State management
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the simulation.
        
        Args:
            config: Configuration dictionary
        """
        # Default configuration
        self.config = config or self._get_default_config()
        
        # Core components
        self.environment: Optional[GridWorld] = None
        self.event_manager: Optional[EventManager] = None
        self.population: Optional[Population] = None
        self.evolution_manager: Optional[EvolutionManager] = None
        
        # Simulation state
        self.state = SimulationState.STOPPED
        self.previous_state = SimulationState.STOPPED
        self.current_step = 0
        self.current_generation = 0
        self.max_generations = self.config.get('max_generations', 5)
        self.steps_per_generation = self.config.get('steps_per_generation', 1000)
        
        # Time management
        self.simulation_speed = self.config.get('simulation_speed', 1.0)  # Steps per second
        self.time_step_duration = 1.0 / self.simulation_speed
        self.day_night_cycle = self.config.get('day_night_cycle', False)
        self.seasonal_variations = self.config.get('seasonal_variations', False)
        
        # Statistics
        self.statistics: Dict = {}
        self.step_history: List[Dict] = []
        self.generation_history: List[Dict] = []
        
        # Threading
        self._simulation_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        
        # Callbacks
        self.step_callbacks: List[Callable] = []
        self.generation_callbacks: List[Callable] = []
        self.state_change_callbacks: List[Callable] = []
    
    def _get_default_config(self) -> Dict:
        """Get default simulation configuration."""
        return {
            'grid_size': (20, 20),
            'population_size': 50,
            'max_generations': 5,
            'steps_per_generation': 1000,
            'simulation_speed': 1.0,
            'day_night_cycle': False,
            'seasonal_variations': False,
            'food_density': 0.1,
            'water_density': 0.1,
            'drought_probability': 0.2,
            'storm_probability': 0.1,
            'famine_probability': 0.15,
            'bonus_probability': 0.05,
            'mutation_rate': 0.1,
            'crossover_rate': 0.8,
            'selection_method': 'tournament',
            'tournament_size': 3,
            'elite_percentage': 0.1
        }
    
    def initialize(self) -> None:
        """Initialize all simulation components."""
        if self.state != SimulationState.STOPPED:
            raise RuntimeError("Cannot initialize simulation while running")
        
        if self.environment is not None:
            raise RuntimeError("Simulation already initialized")
        
        # Create environment
        grid_width, grid_height = self.config['grid_size']
        self.environment = GridWorld(grid_width, grid_height)
        
        # Place resources
        self.environment.place_resources(
            food_density=self.config['food_density'],
            water_density=self.config['water_density']
        )
        
        # Create event manager
        self.event_manager = EventManager()
        self.event_manager.set_event_probabilities(
            drought=self.config['drought_probability'],
            storm=self.config['storm_probability'],
            famine=self.config['famine_probability'],
            bonus=self.config['bonus_probability']
        )
        
        # Create population
        self.population = Population(
            size=self.config['population_size'],
            grid_world=self.environment
        )
        
        # Create evolution manager
        self.evolution_manager = EvolutionManager(self.population)
        self.evolution_manager.set_parameters(
            selection_method=self.config['selection_method'],
            tournament_size=self.config['tournament_size'],
            mutation_rate=self.config['mutation_rate'],
            crossover_rate=self.config['crossover_rate']
        )
        
        # Reset simulation state
        self.current_step = 0
        self.current_generation = 0
        self.statistics = {}
        self.step_history.clear()
        self.generation_history.clear()
        
        print(f"[INIT] Simulation initialized with {self.config['population_size']} animals")
        print(f"[INIT] Grid size: {grid_width}x{grid_height}")
        print(f"[INIT] Max generations: {self.max_generations}")
        print(f"[INIT] Steps per generation: {self.steps_per_generation}")
    
    def start(self) -> None:
        """Start the simulation."""
        if self.state != SimulationState.STOPPED:
            raise RuntimeError("Simulation is not stopped")
        
        if not self.environment:
            self.initialize()
        
        self._set_state(SimulationState.RUNNING)
        self._stop_event.clear()
        self._pause_event.set()  # Start unpaused
        
        # Start simulation thread
        self._simulation_thread = threading.Thread(target=self._simulation_loop)
        self._simulation_thread.start()
        
        self._notify_state_change()
        print("[START] Simulation started")
    
    def pause(self) -> None:
        """Pause the simulation."""
        if self.state != SimulationState.RUNNING:
            raise RuntimeError("Simulation is not running")
        
        self._set_state(SimulationState.PAUSED)
        self._pause_event.clear()
        print("[PAUSE] Simulation paused")
    
    def resume(self) -> None:
        """Resume the simulation."""
        if self.state != SimulationState.PAUSED:
            raise RuntimeError("Simulation is not paused")
        
        self._set_state(SimulationState.RUNNING)
        self._pause_event.set()
        print("[RESUME] Simulation resumed")
    
    def stop(self) -> None:
        """Stop the simulation."""
        if self.state == SimulationState.STOPPED:
            return
        
        self._set_state(SimulationState.STOPPED)
        self._stop_event.set()
        self._pause_event.set()  # Unpause to allow thread to exit
        
        if self._simulation_thread and self._simulation_thread.is_alive():
            self._simulation_thread.join(timeout=1.0)
        print("[STOP] Simulation stopped")
    
    def reset(self) -> None:
        """Reset the simulation to initial state."""
        self.stop()
        
        # Reset all components
        if self.environment:
            self.environment.reset()
        if self.event_manager:
            self.event_manager.reset()
        if self.population:
            self.population.reset()
        if self.evolution_manager:
            self.evolution_manager.reset()
        
        # Reset simulation state
        self.current_step = 0
        self.current_generation = 0
        self.statistics = {}
        self.step_history.clear()
        self.generation_history.clear()
        
        print("[RESET] Simulation reset to initial state")
    
    def _simulation_loop(self) -> None:
        """Main simulation loop."""
        try:
            while not self._stop_event.is_set():
                # Check for pause
                self._pause_event.wait()
                
                if self._stop_event.is_set():
                    break
                
                # Run one simulation step
                self._run_step()
                
                # Check if all animals are dead - stop simulation immediately
                if self.environment and len(self.environment.get_alive_animals()) == 0:
                    print(f"[STOP] All animals died at step {self.current_step}, stopping simulation")
                    self._set_state(SimulationState.FINISHED)
                    break
                
                # Check if generation is complete
                if self.current_step >= self.steps_per_generation:
                    self._complete_generation()
                
                # Check if simulation is complete
                if self.current_generation >= self.max_generations:
                    self._set_state(SimulationState.FINISHED)
                    break
                
                # Sleep to control simulation speed
                time.sleep(self.time_step_duration)
        
        except Exception as e:
            print(f"[ERROR] Simulation loop error: {e}")
            self._set_state(SimulationState.STOPPED)
    
    def _run_step(self) -> None:
        """Run one simulation step."""
        self.current_step += 1
        
        # Update environment events
        if self.event_manager:
            self.event_manager.update()
        
        # Update environment with event effects
        if self.environment and self.event_manager:
            self.environment.update_event_effects(self.event_manager)
        
        # Update animals
        if self.environment:
            self.environment.update_animals()
        
        # Apply environmental effects
        self._apply_environmental_effects()
        
        # Collect step statistics
        step_stats = self._collect_step_statistics()
        self.step_history.append(step_stats)
        
        # Notify step callbacks
        self._notify_step_callbacks(step_stats)
    
    def _complete_generation(self) -> None:
        """Complete current generation and evolve."""
        self._set_state(SimulationState.EVOLVING)
        
        print(f"[EVOLVE] Completing generation {self.current_generation}")
        
        # Collect generation statistics
        gen_stats = self._collect_generation_statistics()
        self.generation_history.append(gen_stats)
        
        # Check if any animals are alive before evolving
        alive_animals = self.environment.get_alive_animals() if self.environment else []
        if len(alive_animals) == 0:
            print(f"[EVOLVE] No living animals in generation {self.current_generation}, stopping simulation")
            self._set_state(SimulationState.FINISHED)
            return
        
        # Evolve population only if animals are alive
        if self.evolution_manager:
            evolution_result = self.evolution_manager.evolve_generation()
            print(f"[EVOLVE] Evolution result: {evolution_result}")
        
        # Reset for next generation
        self._reset_for_next_generation()
        
        self.current_generation += 1
        self.current_step = 0
        
        # Notify generation callbacks
        self._notify_generation_callbacks(gen_stats)
        
        self._set_state(SimulationState.RUNNING)
    
    def _reset_for_next_generation(self) -> None:
        """Reset environment for next generation."""
        if self.environment:
            # Remove all animals
            for animal in self.environment.get_all_animals():
                self.environment.remove_animal(animal)
            
            # Place new animals from population
            for animal in self.population.animals:
                empty_positions = self.environment.get_empty_positions()
                if empty_positions:
                    pos = empty_positions[0]
                    self.environment.add_animal(animal, pos[0], pos[1])
        
        # Reset resources
        if self.environment:
            self.environment.place_resources(
                food_density=self.config['food_density'],
                water_density=self.config['water_density']
            )
    
    def _apply_environmental_effects(self) -> None:
        """Apply environmental effects to animals."""
        if not self.event_manager or not self.environment:
            return
        
        effects = self.event_manager.get_event_effects()
        
        for animal in self.environment.get_alive_animals():
            # Apply movement cost multiplier (storm effect)
            if 'movement_cost_multiplier' in effects:
                multiplier = effects['movement_cost_multiplier']
                # Increase energy cost for movement actions
                if hasattr(animal, 'action_costs'):
                    animal.action_costs['move'] *= multiplier
            
            # Apply energy decay multiplier (storm effect)
            if 'energy_decay_multiplier' in effects:
                multiplier = effects['energy_decay_multiplier']
                # Increase energy decay rate
                if hasattr(animal, 'energy_decay'):
                    animal.energy_decay *= multiplier
            
            # Apply water availability reduction (drought effect)
            if 'water_availability' in effects:
                # This affects water resource placement, handled in environment
                pass
            
            # Apply food availability reduction (famine effect)
            if 'food_availability' in effects:
                # This affects food resource placement, handled in environment
                pass
    
    def _collect_step_statistics(self) -> Dict:
        """Collect statistics for current step."""
        stats = {
            'step': self.current_step,
            'generation': self.current_generation,
            'timestamp': time.time()
        }
        
        if self.environment:
            env_stats = self.environment.get_statistics()
            stats.update(env_stats)
        
        if self.event_manager:
            event_stats = self.event_manager.get_statistics()
            stats['active_events'] = event_stats['active_events']
            stats['event_names'] = event_stats['event_names']
        
        return stats
    
    def _collect_generation_statistics(self) -> Dict:
        """Collect statistics for current generation."""
        stats = {
            'generation': self.current_generation,
            'timestamp': time.time()
        }
        
        # Population statistics
        if self.population:
            pop_stats = self.population.calculate_statistics()
            stats['population_stats'] = pop_stats
            stats.update(pop_stats)  # Also add to main stats for backward compatibility
        
        # Environment statistics
        if self.environment:
            env_stats = self.environment.get_statistics()
            stats['environment_stats'] = env_stats
        
        # Event statistics
        if self.event_manager:
            event_stats = self.event_manager.get_statistics()
            stats['event_stats'] = event_stats
        
        # Evolution statistics
        if self.evolution_manager:
            evo_stats = self.evolution_manager.get_evolution_statistics()
            stats.update(evo_stats)
        
        return stats
    
    def _notify_step_callbacks(self, step_stats: Dict) -> None:
        """Notify step callbacks."""
        for callback in self.step_callbacks:
            try:
                callback(step_stats)
            except Exception as e:
                print(f"[WARNING] Step callback error: {e}")
    
    def _notify_generation_callbacks(self, gen_stats: Dict) -> None:
        """Notify generation callbacks."""
        print(f"[DEBUG] Notifying {len(self.generation_callbacks)} generation callbacks with stats: {gen_stats}")
        for callback in self.generation_callbacks:
            try:
                callback(gen_stats)
            except Exception as e:
                print(f"[WARNING] Generation callback error: {e}")
    
    def _set_state(self, new_state: SimulationState) -> None:
        """Set new state and notify callbacks."""
        self.previous_state = self.state
        self.state = new_state
        self._notify_state_change()
    
    def _notify_state_change(self) -> None:
        """Notify state change callbacks."""
        for callback in self.state_change_callbacks:
            try:
                callback(self.previous_state, self.state)
            except Exception as e:
                print(f"[WARNING] State change callback error: {e}")
    
    def add_step_callback(self, callback: Callable[[Dict], None]) -> None:
        """Add step callback."""
        self.step_callbacks.append(callback)
    
    def add_generation_callback(self, callback: Callable[[Dict], None]) -> None:
        """Add generation callback."""
        self.generation_callbacks.append(callback)
    
    def add_state_change_callback(self, callback: Callable[[SimulationState], None]) -> None:
        """Add state change callback."""
        self.state_change_callbacks.append(callback)
    
    def set_simulation_speed(self, speed: float) -> None:
        """Set simulation speed (steps per second)."""
        self.simulation_speed = max(0.1, min(100.0, speed))
        self.time_step_duration = 1.0 / self.simulation_speed
        print(f"[SPEED] Simulation speed set to {self.simulation_speed:.1f} steps/second")
    
    def get_statistics(self) -> Dict:
        """Get comprehensive simulation statistics."""
        return {
            'state': self.state.value,
            'current_step': self.current_step,
            'current_generation': self.current_generation,
            'max_generations': self.max_generations,
            'steps_per_generation': self.steps_per_generation,
            'simulation_speed': self.simulation_speed,
            'total_steps': len(self.step_history),
            'total_generations': len(self.generation_history),
            'environment_stats': self.environment.get_statistics() if self.environment else {},
            'population_stats': self.population.calculate_statistics() if self.population else {},
            'event_stats': self.event_manager.get_statistics() if self.event_manager else {}
        }
    
    def get_step_history(self, last_n: Optional[int] = None) -> List[Dict]:
        """Get step history."""
        if last_n is None:
            return self.step_history.copy()
        return self.step_history[-last_n:]
    
    def get_generation_history(self, last_n: Optional[int] = None) -> List[Dict]:
        """Get generation history."""
        if last_n is None:
            return self.generation_history.copy()
        return self.generation_history[-last_n:]
    
    def is_running(self) -> bool:
        """Check if simulation is running."""
        return self.state == SimulationState.RUNNING
    
    def is_paused(self) -> bool:
        """Check if simulation is paused."""
        return self.state == SimulationState.PAUSED
    
    def is_stopped(self) -> bool:
        """Check if simulation is stopped."""
        return self.state == SimulationState.STOPPED
    
    def is_finished(self) -> bool:
        """Check if simulation is finished."""
        return self.state == SimulationState.FINISHED
    
    def __str__(self) -> str:
        """String representation of the simulation."""
        return (f"Simulation(state={self.state.value}, "
                f"step={self.current_step}, "
                f"generation={self.current_generation})")
    
    def __repr__(self) -> str:
        """Detailed string representation of the simulation."""
        return self.__str__()
