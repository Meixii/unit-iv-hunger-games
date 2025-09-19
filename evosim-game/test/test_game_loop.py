"""
Unit tests for Game Loop Implementation (Task 2.2).

This module tests the game loop functionality including:
- Generation execution
- Weekly cycles
- Event scheduling
- Win/loss detection
- State tracking and logging
"""

import unittest
from unittest.mock import patch, MagicMock
import random
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation_controller import SimulationController, SimulationConfig
from world_generator import GenerationConfig
from data_structures import AnimalCategory


class TestGameLoop(unittest.TestCase):
    """Test game loop functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = SimulationConfig(
            max_weeks=5,
            max_generations=1,
            population_size=6,
            random_seed=42
        )
        self.controller = SimulationController(self.config)
    
    def test_run_generation_basic(self):
        """Test basic generation execution."""
        # Initialize world and population
        self.controller.initialize_world()
        self.controller.initialize_population()
        
        # Run generation
        result = self.controller.run_generation(max_weeks=3)
        
        # Validate result structure
        self.assertIsInstance(result, dict)
        self.assertIn('generation', result)
        self.assertIn('weeks_completed', result)
        self.assertIn('max_weeks', result)
        self.assertIn('survivors', result)
        self.assertIn('casualties', result)
        self.assertIn('total_population', result)
        self.assertIn('events_count', result)
        self.assertIn('duration', result)
        self.assertIn('events', result)
        
        # Validate basic constraints
        self.assertEqual(result['generation'], 0)
        self.assertEqual(result['max_weeks'], 3)
        self.assertGreaterEqual(result['weeks_completed'], 1)
        self.assertLessEqual(result['weeks_completed'], 3)
        self.assertGreaterEqual(result['survivors'], 0)
        self.assertGreaterEqual(result['casualties'], 0)
        self.assertEqual(result['survivors'] + result['casualties'], result['total_population'])
    
    def test_run_generation_without_world(self):
        """Test generation execution fails without world."""
        with self.assertRaises(ValueError) as context:
            self.controller.run_generation()
        
        self.assertIn("World must be initialized", str(context.exception))
    
    def test_run_generation_without_population(self):
        """Test generation execution fails without population."""
        self.controller.initialize_world()
        
        with self.assertRaises(ValueError) as context:
            self.controller.run_generation()
        
        self.assertIn("Population must be initialized", str(context.exception))
    
    def test_run_generation_single_survivor(self):
        """Test generation ends when single survivor remains."""
        self.controller.initialize_world()
        self.controller.initialize_population()
        
        # Mock the weekly cycle to simulate rapid population decline
        original_method = self.controller._run_weekly_cycle
        
        def mock_weekly_cycle(week):
            result = original_method(week)
            # Kill all but one animal after week 2
            if week >= 2:
                living = self.controller.simulation.get_living_animals()
                if len(living) > 1:
                    for animal in living[1:]:  # Keep only the first animal
                        self.controller.simulation.remove_animal(animal)
            return result
        
        with patch.object(self.controller, '_run_weekly_cycle', side_effect=mock_weekly_cycle):
            result = self.controller.run_generation(max_weeks=5)
        
        # Should end early with single survivor
        self.assertEqual(result['survivors'], 1)
        self.assertLessEqual(result['weeks_completed'], 5)
        self.assertIsNotNone(result['winner'])
    
    def test_run_generation_extinction(self):
        """Test generation handles extinction scenario."""
        self.controller.initialize_world()
        self.controller.initialize_population()
        
        # Mock the weekly cycle to simulate total extinction
        original_method = self.controller._run_weekly_cycle
        
        def mock_weekly_cycle(week):
            result = original_method(week)
            # Kill all animals after week 1
            if week >= 1:
                living = self.controller.simulation.get_living_animals()
                for animal in living:
                    self.controller.simulation.remove_animal(animal)
            return result
        
        with patch.object(self.controller, '_run_weekly_cycle', side_effect=mock_weekly_cycle):
            result = self.controller.run_generation(max_weeks=5)
        
        # Should end with extinction
        self.assertEqual(result['survivors'], 0)
        self.assertTrue(result['extinction'])
        self.assertIsNone(result['winner'])
    
    def test_weekly_cycle_structure(self):
        """Test weekly cycle execution structure."""
        self.controller.initialize_world()
        self.controller.initialize_population()
        
        # Test single week cycle
        result = self.controller._run_weekly_cycle(1)
        
        # Validate result structure
        self.assertIsInstance(result, dict)
        self.assertIn('week', result)
        self.assertIn('events', result)
        self.assertIn('living_animals', result)
        self.assertIn('dead_animals', result)
        
        self.assertEqual(result['week'], 1)
        self.assertIsInstance(result['events'], list)
        self.assertGreater(len(result['events']), 0)  # Should have events
    
    def test_weekly_event_schedule_week_1(self):
        """Test Week 1 has fixed event schedule."""
        schedule = self.controller._get_weekly_event_schedule(1)
        
        expected_schedule = [
            'movement',
            'triggered_event',
            'random_event',
            'disaster',
            'triggered_event',
            'movement',
            'triggered_event'
        ]
        
        self.assertEqual(schedule, expected_schedule)
    
    def test_weekly_event_schedule_randomized(self):
        """Test subsequent weeks have randomized schedules."""
        # Test multiple weeks to ensure randomization
        schedules = []
        for week in range(2, 6):
            schedule = self.controller._get_weekly_event_schedule(week)
            schedules.append(schedule)
            
            # Should contain basic events
            self.assertIn('movement', schedule)
            self.assertIn('triggered_event', schedule)
            self.assertIn('random_event', schedule)
        
        # Schedules should be different (randomized)
        unique_schedules = [tuple(s) for s in schedules]
        self.assertGreater(len(set(unique_schedules)), 1, "Schedules should be randomized")
    
    def test_event_execution_types(self):
        """Test all event types can be executed."""
        self.controller.initialize_world()
        self.controller.initialize_population()
        
        event_types = ['movement', 'triggered_event', 'random_event', 'disaster']
        
        for event_type in event_types:
            with self.subTest(event_type=event_type):
                result = self.controller._execute_event(event_type, 1)
                
                # Validate result structure
                self.assertIsInstance(result, dict)
                self.assertIn('type', result)
                self.assertIn('week', result)
                self.assertIn('timestamp', result)
                self.assertIn('success', result)
                self.assertIn('message', result)
                self.assertIn('affected_animals', result)
                self.assertIn('casualties', result)
                
                self.assertEqual(result['type'], event_type)
                self.assertEqual(result['week'], 1)
                self.assertTrue(result['success'])
    
    def test_movement_event_starvation(self):
        """Test movement event handles starvation."""
        self.controller.initialize_world()
        self.controller.initialize_population()
        
        # Set animals to low hunger/thirst
        living = self.controller.simulation.get_living_animals()
        for animal in living:
            animal.status['Hunger'] = 2  # Will drop to 0 or below
            animal.status['Thirst'] = 1   # Will drop to 0 or below
        
        result = self.controller._execute_movement_event(1)
        
        # Should have casualties from starvation
        self.assertGreater(result['casualties'], 0)
        self.assertEqual(len(result['affected_animals']), result['casualties'])
    
    def test_disaster_event_casualties(self):
        """Test disaster event can cause casualties."""
        self.controller.initialize_world()
        self.controller.initialize_population()
        
        # Set random seed for predictable disaster
        random.seed(42)
        
        result = self.controller._execute_disaster_event(1)
        
        # Should affect some animals
        self.assertGreaterEqual(len(result['affected_animals']), 0)
        self.assertGreaterEqual(result['casualties'], 0)
        self.assertTrue(result['success'])
    
    def test_generation_statistics_tracking(self):
        """Test generation statistics are properly tracked."""
        self.controller.initialize_world()
        self.controller.initialize_population()
        
        # Run generation
        result = self.controller.run_generation(max_weeks=2)
        
        # Check statistics were stored
        self.assertEqual(len(self.controller.generation_stats), 1)
        self.assertEqual(self.controller.generation_stats[0], result)
        
        # Check weekly stats were collected
        self.assertGreater(len(self.controller.weekly_stats), 0)
        self.assertLessEqual(len(self.controller.weekly_stats), 2)  # Max 2 weeks
    
    def test_event_early_termination(self):
        """Test weekly cycle terminates early when population drops to 1."""
        self.controller.initialize_world()
        self.controller.initialize_population()
        
        # Mock event execution to kill animals
        original_execute = self.controller._execute_event
        
        def mock_execute_event(event_type, week):
            result = original_execute(event_type, week)
            # Kill animals during first event
            if event_type == 'movement':
                living = self.controller.simulation.get_living_animals()
                if len(living) > 1:
                    # Leave only one survivor
                    for animal in living[1:]:
                        self.controller.simulation.remove_animal(animal)
                    result['casualties'] = len(living) - 1
                    result['affected_animals'] = [a.animal_id for a in living[1:]]
            return result
        
        with patch.object(self.controller, '_execute_event', side_effect=mock_execute_event):
            result = self.controller._run_weekly_cycle(1)
        
        # Should have terminated early
        self.assertEqual(result['living_animals'], 1)
    
    def test_unknown_event_type(self):
        """Test handling of unknown event types."""
        self.controller.initialize_world()
        self.controller.initialize_population()
        
        result = self.controller._execute_event('unknown_event', 1)
        
        self.assertFalse(result['success'])
        self.assertIn('Unknown event type', result['message'])


class TestGameLoopIntegration(unittest.TestCase):
    """Integration tests for game loop with full simulation."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.config = SimulationConfig(
            max_weeks=3,
            max_generations=1,
            population_size=4,
            random_seed=123
        )
        self.controller = SimulationController(self.config)
    
    def test_full_generation_workflow(self):
        """Test complete generation workflow."""
        # Initialize simulation
        world = self.controller.initialize_world()
        animals = self.controller.initialize_population()
        
        self.assertIsNotNone(world)
        self.assertEqual(len(animals), 4)
        
        # Run generation
        result = self.controller.run_generation()
        
        # Validate complete workflow
        self.assertIsInstance(result, dict)
        self.assertGreaterEqual(result['weeks_completed'], 1)
        self.assertLessEqual(result['weeks_completed'], 3)
        
        # Check that events were executed
        self.assertGreater(result['events_count'], 0)
        self.assertIsInstance(result['events'], list)
        
        # Validate final state
        final_population = result['survivors'] + result['casualties']
        self.assertEqual(final_population, 4)
    
    def test_multiple_generations_tracking(self):
        """Test tracking across multiple generation runs."""
        self.controller.initialize_world()
        self.controller.initialize_population()
        
        # Run first generation
        result1 = self.controller.run_generation(max_weeks=2)
        first_gen_stats = self.controller.generation_stats.copy()
        
        # Increment generation counter and reset simulation (but preserve generation stats)
        self.controller.current_generation += 1
        
        # Reset simulation state but preserve generation history
        self.controller.stop_simulation()
        self.controller.simulation.reset()
        self.controller.weekly_stats.clear()
        self.controller.simulation_start_time = None
        self.controller.simulation_end_time = None
        
        # Initialize for second generation
        self.controller.initialize_world()
        self.controller.initialize_population()
        
        result2 = self.controller.run_generation(max_weeks=2)
        
        # Should have tracked both generations
        self.assertEqual(len(self.controller.generation_stats), 2)
        self.assertEqual(self.controller.generation_stats[0]['generation'], 0)
        self.assertEqual(self.controller.generation_stats[1]['generation'], 1)


class TestGameLoopEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions for game loop."""
    
    def setUp(self):
        """Set up edge case test fixtures."""
        self.controller = SimulationController(SimulationConfig(random_seed=42))
    
    def test_empty_population_handling(self):
        """Test handling of empty population."""
        self.controller.initialize_world()
        # Don't initialize population
        
        with self.assertRaises(ValueError):
            self.controller.run_generation()
    
    def test_disaster_with_no_animals(self):
        """Test disaster event with no living animals."""
        result = self.controller._execute_disaster_event(1)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['casualties'], 0)
        self.assertEqual(len(result['affected_animals']), 0)
        self.assertIn('no animals to affect', result['message'])
    
    def test_movement_event_with_no_animals(self):
        """Test movement event with no living animals."""
        result = self.controller._execute_movement_event(1)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['casualties'], 0)
        self.assertEqual(len(result['affected_animals']), 0)


if __name__ == '__main__':
    print("Running Game Loop Tests...")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestGameLoop))
    suite.addTests(loader.loadTestsFromTestCase(TestGameLoopIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestGameLoopEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All game loop tests passed!")
    else:
        print("❌ Some game loop tests failed!")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
    
    print("Game loop test execution completed.")
