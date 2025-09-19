"""
Test script for simulation controller validation.

This module tests the SimulationController class and related functionality.
It ensures the simulation controller works correctly and handles edge cases properly.

Reference: Task 2.1 - Main Simulation Controller from documentation.md
"""

import unittest
import tempfile
import os
import sys
from unittest.mock import patch, MagicMock
from datetime import datetime

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation_controller import (
    SimulationController, SimulationConfig, create_simulation_controller,
    validate_simulation_controller
)
from data_structures import AnimalCategory, TerrainType
from world_generator import GenerationConfig


class TestSimulationConfig(unittest.TestCase):
    """Test SimulationConfig class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = SimulationConfig()
        
        self.assertEqual(config.max_weeks, 20)
        self.assertEqual(config.max_generations, 10)
        self.assertEqual(config.population_size, 20)
        self.assertTrue(config.enable_logging)
        self.assertEqual(config.log_level, "INFO")
        self.assertIsNone(config.random_seed)
        self.assertIsNone(config.world_config)
    
    def test_custom_config(self):
        """Test custom configuration values."""
        world_config = GenerationConfig()
        config = SimulationConfig(
            max_weeks=50,
            max_generations=5,
            population_size=100,
            enable_logging=False,
            log_level="DEBUG",
            random_seed=42,
            world_config=world_config
        )
        
        self.assertEqual(config.max_weeks, 50)
        self.assertEqual(config.max_generations, 5)
        self.assertEqual(config.population_size, 100)
        self.assertFalse(config.enable_logging)
        self.assertEqual(config.log_level, "DEBUG")
        self.assertEqual(config.random_seed, 42)
        self.assertEqual(config.world_config, world_config)
    
    def test_invalid_config(self):
        """Test configuration validation."""
        with self.assertRaises(ValueError):
            SimulationConfig(max_weeks=0)
        
        with self.assertRaises(ValueError):
            SimulationConfig(max_generations=-1)
        
        with self.assertRaises(ValueError):
            SimulationConfig(population_size=0)


class TestSimulationController(unittest.TestCase):
    """Test SimulationController class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = SimulationConfig(
            max_weeks=5,
            max_generations=2,
            population_size=6,
            enable_logging=False,
            random_seed=42
        )
        self.controller = SimulationController(self.config)
    
    def test_initialization(self):
        """Test controller initialization."""
        self.assertIsNotNone(self.controller.simulation)
        self.assertEqual(self.controller.config, self.config)
        self.assertIsNotNone(self.controller.world_generator)
        self.assertIsNotNone(self.controller.animal_creator)
        self.assertIsNotNone(self.controller.animal_customizer)
        self.assertFalse(self.controller.is_running)
        self.assertFalse(self.controller.is_paused)
        self.assertEqual(self.controller.current_generation, 0)
        self.assertEqual(len(self.controller.generation_stats), 0)
        self.assertEqual(len(self.controller.weekly_stats), 0)
    
    def test_logging_setup(self):
        """Test logging setup."""
        self.assertIsNotNone(self.controller.logger)
        self.assertEqual(self.controller.logger.level, 20)  # INFO level
    
    def test_random_seed_setting(self):
        """Test random seed setting."""
        config = SimulationConfig(random_seed=123)
        controller = SimulationController(config)
        # Note: We can't easily test if random seed was actually set without
        # affecting global random state, so we just check it doesn't crash
    
    def test_initialize_world(self):
        """Test world initialization."""
        world = self.controller.initialize_world()
        
        self.assertIsNotNone(world)
        self.assertEqual(self.controller.simulation.world, world)
        self.assertEqual(world.dimensions[0], 25)  # Default grid width
        self.assertEqual(world.dimensions[1], 25)  # Default grid height
    
    def test_initialize_world_with_config(self):
        """Test world initialization with custom config."""
        world_config = GenerationConfig(width=10, height=10)
        world = self.controller.initialize_world(world_config)
        
        self.assertIsNotNone(world)
        self.assertEqual(world.dimensions[0], 10)
        self.assertEqual(world.dimensions[1], 10)
    
    def test_initialize_world_failure(self):
        """Test world initialization failure handling."""
        with patch('simulation_controller.WorldGenerator') as mock_world_generator:
            mock_instance = mock_world_generator.return_value
            mock_instance.generate_world.return_value = None
            with self.assertRaises(ValueError):
                self.controller.initialize_world()
    
    def test_initialize_population(self):
        """Test population initialization."""
        # Initialize world first
        self.controller.initialize_world()
        
        animals = self.controller.initialize_population()
        
        self.assertEqual(len(animals), 6)  # population_size
        self.assertEqual(len(self.controller.simulation.population), 6)
        
        # Check that all animals have valid locations
        for animal in animals:
            self.assertIsNotNone(animal.location)
            x, y = animal.location
            self.assertGreaterEqual(x, 0)
            self.assertLess(x, 25)
            self.assertGreaterEqual(y, 0)
            self.assertLess(y, 25)
    
    def test_initialize_population_without_world(self):
        """Test population initialization without world."""
        with self.assertRaises(ValueError):
            self.controller.initialize_population()
    
    def test_initialize_population_custom_size(self):
        """Test population initialization with custom size."""
        self.controller.initialize_world()
        
        animals = self.controller.initialize_population(10)
        
        self.assertEqual(len(animals), 10)
        self.assertEqual(len(self.controller.simulation.population), 10)
    
    def test_place_animals_in_world(self):
        """Test animal placement in world."""
        self.controller.initialize_world()
        
        # Create test animals
        animals = []
        for i in range(3):
            animal = self.controller.animal_customizer.create_balanced_animal(f"test_{i}", AnimalCategory.HERBIVORE)
            animals.append(animal)
        
        placed_animals = self.controller._place_animals_in_world(animals)
        
        self.assertEqual(len(placed_animals), 3)
        for animal in placed_animals:
            self.assertIsNotNone(animal.location)
            x, y = animal.location
            tile = self.controller.simulation.world.get_tile(x, y)
            self.assertEqual(tile.occupant, animal)
    
    def test_place_animals_insufficient_space(self):
        """Test animal placement with insufficient space."""
        # Create a small world with limited plains tiles
        world_config = GenerationConfig(width=3, height=3)
        self.controller.initialize_world(world_config)
        
        # Create more animals than available space
        animals = []
        for i in range(10):
            animal = self.controller.animal_customizer.create_balanced_animal(f"test_{i}", AnimalCategory.HERBIVORE)
            animals.append(animal)
        
        placed_animals = self.controller._place_animals_in_world(animals)
        
        # Should place as many as possible
        self.assertLessEqual(len(placed_animals), 9)  # Max 3x3 grid
    
    def test_get_terrain_stats(self):
        """Test terrain statistics calculation."""
        world = self.controller.initialize_world()
        stats = self.controller._get_terrain_stats(world)
        
        self.assertIsInstance(stats, dict)
        self.assertGreater(sum(stats.values()), 0)
        self.assertEqual(sum(stats.values()), world.dimensions[0] * world.dimensions[1])
    
    def test_get_category_stats(self):
        """Test category statistics calculation."""
        self.controller.initialize_world()
        animals = self.controller.initialize_population()
        
        stats = self.controller._get_category_stats(animals)
        
        self.assertIsInstance(stats, dict)
        self.assertEqual(sum(stats.values()), len(animals))
        self.assertIn('Herbivore', stats)
        self.assertIn('Carnivore', stats)
        self.assertIn('Omnivore', stats)
    
    def test_start_simulation(self):
        """Test simulation start."""
        self.controller.initialize_world()
        self.controller.initialize_population()
        
        self.controller.start_simulation()
        
        self.assertTrue(self.controller.is_running)
        self.assertFalse(self.controller.is_paused)
        self.assertIsNotNone(self.controller.simulation_start_time)
    
    def test_start_simulation_already_running(self):
        """Test starting simulation when already running."""
        self.controller.initialize_world()
        self.controller.initialize_population()
        self.controller.start_simulation()
        
        with self.assertRaises(ValueError):
            self.controller.start_simulation()
    
    def test_start_simulation_without_world(self):
        """Test starting simulation without world."""
        with self.assertRaises(ValueError):
            self.controller.start_simulation()
    
    def test_start_simulation_without_population(self):
        """Test starting simulation without population."""
        self.controller.initialize_world()
        
        with self.assertRaises(ValueError):
            self.controller.start_simulation()
    
    def test_pause_resume_simulation(self):
        """Test simulation pause and resume."""
        self.controller.initialize_world()
        self.controller.initialize_population()
        self.controller.start_simulation()
        
        self.controller.pause_simulation()
        self.assertTrue(self.controller.is_paused)
        
        self.controller.resume_simulation()
        self.assertFalse(self.controller.is_paused)
    
    def test_pause_simulation_not_running(self):
        """Test pausing simulation when not running."""
        with self.assertRaises(ValueError):
            self.controller.pause_simulation()
    
    def test_resume_simulation_not_running(self):
        """Test resuming simulation when not running."""
        with self.assertRaises(ValueError):
            self.controller.resume_simulation()
    
    def test_stop_simulation(self):
        """Test simulation stop."""
        self.controller.initialize_world()
        self.controller.initialize_population()
        self.controller.start_simulation()
        
        self.controller.stop_simulation()
        
        self.assertFalse(self.controller.is_running)
        self.assertFalse(self.controller.is_paused)
        self.assertIsNotNone(self.controller.simulation_end_time)
    
    def test_reset_simulation(self):
        """Test simulation reset."""
        self.controller.initialize_world()
        self.controller.initialize_population()
        self.controller.start_simulation()
        self.controller.current_generation = 5
        
        self.controller.reset_simulation()
        
        self.assertFalse(self.controller.is_running)
        self.assertFalse(self.controller.is_paused)
        self.assertEqual(self.controller.current_generation, 0)
        self.assertEqual(self.controller.simulation.current_week, 0)
        self.assertEqual(len(self.controller.simulation.population), 0)
        self.assertEqual(len(self.controller.generation_stats), 0)
        self.assertEqual(len(self.controller.weekly_stats), 0)
        self.assertIsNone(self.controller.simulation_start_time)
        self.assertIsNone(self.controller.simulation_end_time)
    
    def test_get_simulation_status(self):
        """Test simulation status retrieval."""
        status = self.controller.get_simulation_status()
        
        self.assertIsInstance(status, dict)
        self.assertIn('is_running', status)
        self.assertIn('is_paused', status)
        self.assertIn('current_generation', status)
        self.assertIn('current_week', status)
        self.assertIn('total_population', status)
        self.assertIn('living_animals', status)
        self.assertIn('dead_animals', status)
        self.assertIn('world_initialized', status)
        self.assertIn('population_initialized', status)
        self.assertIn('event_queue_length', status)
        
        self.assertFalse(status['is_running'])
        self.assertFalse(status['is_paused'])
        self.assertEqual(status['current_generation'], 0)
        self.assertEqual(status['current_week'], 0)
        self.assertFalse(status['world_initialized'])
        self.assertFalse(status['population_initialized'])
    
    def test_get_simulation_status_with_initialization(self):
        """Test simulation status after initialization."""
        self.controller.initialize_world()
        self.controller.initialize_population()
        
        status = self.controller.get_simulation_status()
        
        self.assertTrue(status['world_initialized'])
        self.assertTrue(status['population_initialized'])
        self.assertEqual(status['total_population'], 6)
        self.assertEqual(status['living_animals'], 6)
        self.assertEqual(status['dead_animals'], 0)
    
    def test_get_generation_stats(self):
        """Test generation statistics retrieval."""
        stats = self.controller.get_generation_stats()
        
        self.assertIsInstance(stats, list)
        self.assertEqual(len(stats), 0)
        
        # Add some mock stats
        self.controller.generation_stats.append({'generation': 1, 'max_fitness': 100})
        
        stats = self.controller.get_generation_stats()
        self.assertEqual(len(stats), 1)
        self.assertEqual(stats[0]['generation'], 1)
    
    def test_get_weekly_stats(self):
        """Test weekly statistics retrieval."""
        stats = self.controller.get_weekly_stats()
        
        self.assertIsInstance(stats, list)
        self.assertEqual(len(stats), 0)
        
        # Add some mock stats
        self.controller.weekly_stats.append({'week': 1, 'population': 6})
        
        stats = self.controller.get_weekly_stats()
        self.assertEqual(len(stats), 1)
        self.assertEqual(stats[0]['week'], 1)
    
    def test_validate_simulation_state(self):
        """Test simulation state validation."""
        # Initially invalid (no world or population)
        self.assertFalse(self.controller.validate_simulation_state())
        
        # Initialize world
        self.controller.initialize_world()
        self.assertFalse(self.controller.validate_simulation_state())  # Still no population
        
        # Initialize population
        self.controller.initialize_population()
        self.assertTrue(self.controller.validate_simulation_state())
    
    def test_validate_simulation_state_with_invalid_animal_locations(self):
        """Test simulation state validation with invalid animal locations."""
        self.controller.initialize_world()
        self.controller.initialize_population()
        
        # Corrupt an animal's location
        if self.controller.simulation.population:
            animal = self.controller.simulation.population[0]
            animal.location = (999, 999)  # Invalid location
        
        self.assertFalse(self.controller.validate_simulation_state())
    
    def test_log_simulation_state(self):
        """Test simulation state logging."""
        # This test just ensures the method doesn't crash
        self.controller.log_simulation_state()
        
        # Test with initialized simulation
        self.controller.initialize_world()
        self.controller.initialize_population()
        self.controller.log_simulation_state()


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions."""
    
    def test_create_simulation_controller(self):
        """Test create_simulation_controller function."""
        controller = create_simulation_controller(
            max_weeks=10,
            max_generations=3,
            population_size=15,
            random_seed=123,
            enable_logging=False
        )
        
        self.assertIsInstance(controller, SimulationController)
        self.assertEqual(controller.config.max_weeks, 10)
        self.assertEqual(controller.config.max_generations, 3)
        self.assertEqual(controller.config.population_size, 15)
        self.assertEqual(controller.config.random_seed, 123)
        self.assertFalse(controller.config.enable_logging)
    
    def test_validate_simulation_controller(self):
        """Test validate_simulation_controller function."""
        controller = create_simulation_controller(enable_logging=False)
        
        # Initially invalid
        self.assertFalse(validate_simulation_controller(controller))
        
        # Initialize properly
        controller.initialize_world()
        controller.initialize_population()
        
        self.assertTrue(validate_simulation_controller(controller))
    
    def test_validate_simulation_controller_invalid(self):
        """Test validate_simulation_controller with invalid controller."""
        # Test with None
        self.assertFalse(validate_simulation_controller(None))
        
        # Test with object missing required attributes
        class MockController:
            pass
        
        mock_controller = MockController()
        self.assertFalse(validate_simulation_controller(mock_controller))


class TestIntegration(unittest.TestCase):
    """Integration tests for simulation controller."""
    
    def test_full_initialization_workflow(self):
        """Test complete initialization workflow."""
        controller = create_simulation_controller(
            max_weeks=5,
            population_size=4,
            enable_logging=False
        )
        
        # Initialize world
        world = controller.initialize_world()
        self.assertIsNotNone(world)
        
        # Initialize population
        animals = controller.initialize_population()
        self.assertEqual(len(animals), 4)
        
        # Start simulation
        controller.start_simulation()
        self.assertTrue(controller.is_running)
        
        # Validate state
        self.assertTrue(controller.validate_simulation_state())
        
        # Get status
        status = controller.get_simulation_status()
        self.assertTrue(status['world_initialized'])
        self.assertTrue(status['population_initialized'])
        self.assertTrue(status['is_running'])
        
        # Stop simulation
        controller.stop_simulation()
        self.assertFalse(controller.is_running)
    
    def test_reset_and_reinitialize(self):
        """Test reset and reinitialize workflow."""
        controller = create_simulation_controller(enable_logging=False)
        
        # Initial setup
        controller.initialize_world()
        controller.initialize_population()
        controller.start_simulation()
        
        # Reset
        controller.reset_simulation()
        
        # Reinitialize
        controller.initialize_world()
        controller.initialize_population()
        controller.start_simulation()
        
        # Should work the same
        self.assertTrue(controller.validate_simulation_state())
        self.assertTrue(controller.is_running)


def run_tests():
    """Run all tests."""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_cases = [
        TestSimulationConfig,
        TestSimulationController,
        TestUtilityFunctions,
        TestIntegration
    ]
    
    for test_case in test_cases:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_case)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("Running Simulation Controller Tests...")
    print("=" * 50)
    
    success = run_tests()
    
    if success:
        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        print("Simulation Controller implementation is working correctly.")
    else:
        print("\n" + "=" * 50)
        print("❌ Some tests failed!")
        print("Please check the implementation and fix any issues.")
    
    print(f"\nTest execution completed.")
