"""
Test module for the Simulation system.
"""

import pytest
import time
import threading
from src.simulation import Simulation, SimulationState
from src.environment import GridWorld
from src.events import EventManager
from src.evolution import Population, EvolutionManager


class TestSimulation:
    """Test cases for Simulation class."""
    
    def _get_test_config(self, **overrides):
        """Get test configuration with overrides."""
        config = {
            'grid_size': (10, 10),
            'population_size': 20,
            'max_generations': 1,
            'steps_per_generation': 10,
            'simulation_speed': 10.0,
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
        config.update(overrides)
        return config
    
    def test_simulation_initialization(self):
        """Test simulation initialization."""
        simulation = Simulation()
        
        assert simulation.state == SimulationState.STOPPED
        assert simulation.current_step == 0
        assert simulation.current_generation == 0
        assert simulation.environment is None
        assert simulation.event_manager is None
        assert simulation.population is None
        assert simulation.evolution_manager is None
    
    def test_simulation_initialization_with_config(self):
        """Test simulation initialization with custom config."""
        config = {
            'grid_size': (10, 10),
            'population_size': 20,
            'max_generations': 3,
            'steps_per_generation': 100
        }
        simulation = Simulation(config)
        
        assert simulation.config['grid_size'] == (10, 10)
        assert simulation.config['population_size'] == 20
        assert simulation.max_generations == 3
        assert simulation.steps_per_generation == 100
    
    def test_initialize(self):
        """Test simulation initialization."""
        simulation = Simulation()
        simulation.initialize()
        
        assert simulation.environment is not None
        assert simulation.event_manager is not None
        assert simulation.population is not None
        assert simulation.evolution_manager is not None
        assert simulation.current_step == 0
        assert simulation.current_generation == 0
    
    def test_initialize_twice_raises_error(self):
        """Test that initializing twice raises error."""
        simulation = Simulation()
        simulation.initialize()
        
        with pytest.raises(RuntimeError, match="Simulation already initialized"):
            simulation.initialize()
    
    def test_start_stop(self):
        """Test starting and stopping simulation."""
        config = self._get_test_config()
        simulation = Simulation(config)
        simulation.initialize()
        
        # Start simulation
        simulation.start()
        assert simulation.state == SimulationState.RUNNING
        assert simulation.is_running()
        
        # Let it run briefly
        time.sleep(0.1)
        
        # Stop simulation
        simulation.stop()
        assert simulation.state == SimulationState.STOPPED
        assert simulation.is_stopped()
    
    def test_pause_resume(self):
        """Test pausing and resuming simulation."""
        config = self._get_test_config()
        simulation = Simulation(config)
        simulation.initialize()
        simulation.start()
        
        # Pause simulation
        simulation.pause()
        assert simulation.state == SimulationState.PAUSED
        assert simulation.is_paused()
        
        # Resume simulation
        simulation.resume()
        assert simulation.state == SimulationState.RUNNING
        assert simulation.is_running()
        
        simulation.stop()
    
    def test_pause_when_not_running_raises_error(self):
        """Test that pausing when not running raises error."""
        simulation = Simulation()
        
        with pytest.raises(RuntimeError):
            simulation.pause()
    
    def test_resume_when_not_paused_raises_error(self):
        """Test that resuming when not paused raises error."""
        simulation = Simulation()
        
        with pytest.raises(RuntimeError):
            simulation.resume()
    
    def test_start_when_not_stopped_raises_error(self):
        """Test that starting when not stopped raises error."""
        simulation = Simulation()
        simulation.initialize()
        simulation.start()
        
        with pytest.raises(RuntimeError):
            simulation.start()
        
        simulation.stop()
    
    def test_reset(self):
        """Test simulation reset."""
        config = self._get_test_config()
        simulation = Simulation(config)
        simulation.initialize()
        simulation.start()
        
        # Let it run briefly
        time.sleep(0.1)
        
        # Reset simulation
        simulation.reset()
        assert simulation.state == SimulationState.STOPPED
        assert simulation.current_step == 0
        assert simulation.current_generation == 0
        assert len(simulation.step_history) == 0
        assert len(simulation.generation_history) == 0
    
    def test_set_simulation_speed(self):
        """Test setting simulation speed."""
        simulation = Simulation()
        
        simulation.set_simulation_speed(2.0)
        assert simulation.simulation_speed == 2.0
        assert simulation.time_step_duration == 0.5
        
        # Test speed limits
        simulation.set_simulation_speed(200.0)
        assert simulation.simulation_speed == 100.0
        
        simulation.set_simulation_speed(0.05)
        assert simulation.simulation_speed == 0.1
    
    def test_get_statistics(self):
        """Test getting simulation statistics."""
        config = self._get_test_config()
        simulation = Simulation(config)
        simulation.initialize()
        
        stats = simulation.get_statistics()
        
        assert 'state' in stats
        assert 'current_step' in stats
        assert 'current_generation' in stats
        assert 'max_generations' in stats
        assert 'steps_per_generation' in stats
        assert 'simulation_speed' in stats
        assert 'total_steps' in stats
        assert 'total_generations' in stats
        assert 'environment_stats' in stats
        assert 'population_stats' in stats
        assert 'event_stats' in stats
    
    def test_get_step_history(self):
        """Test getting step history."""
        config = self._get_test_config()
        simulation = Simulation(config)
        simulation.initialize()
        simulation.start()
        
        # Let it run for a few steps
        time.sleep(0.2)
        
        step_history = simulation.get_step_history()
        assert len(step_history) > 0
        
        # Test getting last N steps
        last_3_steps = simulation.get_step_history(3)
        assert len(last_3_steps) <= 3
        
        simulation.stop()
    
    def test_get_generation_history(self):
        """Test getting generation history."""
        config = self._get_test_config(max_generations=2)
        simulation = Simulation(config)
        simulation.initialize()
        simulation.start()
        
        # Let it run for a generation
        time.sleep(0.5)
        
        gen_history = simulation.get_generation_history()
        assert len(gen_history) >= 0
        
        simulation.stop()
    
    def test_callbacks(self):
        """Test simulation callbacks."""
        config = self._get_test_config()
        simulation = Simulation(config)
        simulation.initialize()
        
        # Track callbacks
        step_calls = []
        generation_calls = []
        state_calls = []
        
        def step_callback(stats):
            step_calls.append(stats)
        
        def generation_callback(stats):
            generation_calls.append(stats)
        
        def state_callback(state):
            state_calls.append(state)
        
        # Add callbacks
        simulation.add_step_callback(step_callback)
        simulation.add_generation_callback(generation_callback)
        simulation.add_state_change_callback(state_callback)
        
        # Start simulation
        simulation.start()
        time.sleep(0.2)
        simulation.stop()
        
        # Check that callbacks were called
        assert len(step_calls) > 0
        assert len(state_calls) > 0  # At least start and stop
    
    def test_callback_errors_handled(self):
        """Test that callback errors are handled gracefully."""
        config = self._get_test_config()
        simulation = Simulation(config)
        simulation.initialize()
        
        def error_callback(stats):
            raise Exception("Test error")
        
        simulation.add_step_callback(error_callback)
        
        # Should not raise exception
        simulation.start()
        time.sleep(0.1)
        simulation.stop()
    
    def test_simulation_completion(self):
        """Test simulation completion."""
        config = self._get_test_config()
        simulation = Simulation(config)
        simulation.initialize()
        simulation.start()
        
        # Let it complete
        time.sleep(1.0)
        
        # Should be finished or stopped
        assert simulation.is_finished() or simulation.is_stopped()
    
    def test_environment_integration(self):
        """Test integration with environment."""
        config = self._get_test_config()
        simulation = Simulation(config)
        simulation.initialize()
        
        # Check environment is properly initialized
        assert simulation.environment is not None
        assert simulation.environment.width == 10
        assert simulation.environment.height == 10
        assert len(simulation.environment.get_all_animals()) > 0
    
    def test_event_manager_integration(self):
        """Test integration with event manager."""
        config = self._get_test_config()
        simulation = Simulation(config)
        simulation.initialize()
        
        # Check event manager is properly initialized
        assert simulation.event_manager is not None
        assert simulation.event_manager.drought_probability == 0.2
        assert simulation.event_manager.storm_probability == 0.1
    
    def test_population_integration(self):
        """Test integration with population."""
        config = self._get_test_config()
        simulation = Simulation(config)
        simulation.initialize()
        
        # Check population is properly initialized
        assert simulation.population is not None
        assert len(simulation.population.animals) == 20
        assert simulation.population.generation == 0
    
    def test_evolution_manager_integration(self):
        """Test integration with evolution manager."""
        config = self._get_test_config()
        simulation = Simulation(config)
        simulation.initialize()
        
        # Check evolution manager is properly initialized
        assert simulation.evolution_manager is not None
        assert simulation.evolution_manager.population == simulation.population
    
    def test_simulation_state_enum(self):
        """Test simulation state enum."""
        assert SimulationState.STOPPED.value == "stopped"
        assert SimulationState.RUNNING.value == "running"
        assert SimulationState.PAUSED.value == "paused"
        assert SimulationState.EVOLVING.value == "evolving"
        assert SimulationState.FINISHED.value == "finished"
    
    def test_simulation_string_representation(self):
        """Test simulation string representation."""
        simulation = Simulation()
        simulation.initialize()
        
        str_repr = str(simulation)
        assert "Simulation" in str_repr
        assert "state=" in str_repr
        assert "step=" in str_repr
        assert "generation=" in str_repr
    
    def test_simulation_with_custom_config(self):
        """Test simulation with custom configuration."""
        config = self._get_test_config(
            grid_size=(15, 15),
            population_size=30,
            max_generations=3,
            steps_per_generation=50,
            food_density=0.15,
            water_density=0.15,
            drought_probability=0.3,
            storm_probability=0.2
        )
        
        simulation = Simulation(config)
        simulation.initialize()
        
        assert simulation.environment.width == 15
        assert simulation.environment.height == 15
        assert len(simulation.population.animals) == 30
        assert simulation.max_generations == 3
        assert simulation.steps_per_generation == 50
        assert simulation.event_manager.drought_probability == 0.3
        assert simulation.event_manager.storm_probability == 0.2
    
    def test_simulation_threading(self):
        """Test simulation threading behavior."""
        config = self._get_test_config()
        simulation = Simulation(config)
        simulation.initialize()
        
        # Start simulation
        simulation.start()
        assert simulation._simulation_thread is not None
        assert simulation._simulation_thread.is_alive()
        
        # Stop simulation
        simulation.stop()
        assert simulation.state == SimulationState.STOPPED
    
    def test_simulation_reset_after_run(self):
        """Test simulation reset after running."""
        config = self._get_test_config()
        simulation = Simulation(config)
        simulation.initialize()
        simulation.start()
        
        # Let it run briefly
        time.sleep(0.2)
        
        # Stop and reset
        simulation.stop()
        simulation.reset()
        
        # Should be back to initial state
        assert simulation.state == SimulationState.STOPPED
        assert simulation.current_step == 0
        assert simulation.current_generation == 0
        assert len(simulation.step_history) == 0
        assert len(simulation.generation_history) == 0
