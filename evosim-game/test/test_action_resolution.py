"""
Unit Tests for Action Resolution System

Tests the modular action resolution system including all 4 phases:
1. Decision Phase
2. Status & Environmental Phase  
3. Action Execution Phase
4. Cleanup Phase
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from action_resolution import (
    ActionResolver, DecisionEngine, StatusEngine, 
    ExecutionEngine, CleanupEngine, AnimalAction, ActionPriority
)
from data_structures import (
    Simulation, World, Animal, Tile, Effect,
    AnimalCategory, TerrainType, EffectType, ActionType, Resource, ResourceType
)
from simulation_controller import SimulationController, SimulationConfig
import logging


class TestActionResolutionSystem(unittest.TestCase):
    """Test the complete action resolution system."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a mock logger
        self.logger = Mock()
        
        # Create a simple simulation with world and animals
        self.simulation = Simulation()
        
        # Create a simple 3x3 world
        grid = []
        for y in range(3):
            row = []
            for x in range(3):
                terrain = TerrainType.PLAINS if (x, y) != (1, 1) else TerrainType.WATER
                tile = Tile(coordinates=(x, y), terrain_type=terrain)
                if terrain == TerrainType.WATER:
                    # Add water resource
                    water = Resource(resource_type=ResourceType.WATER, quantity=10, uses_left=10)
                    tile.resource = water
                elif x == 0 and y == 0:
                    # Add plant resource
                    plant = Resource(resource_type=ResourceType.PLANT, quantity=5, uses_left=5)
                    tile.resource = plant
                row.append(tile)
            grid.append(row)
        
        self.world = World(grid=grid, dimensions=(3, 3))
        
        self.simulation.world = self.world
        
        # Create test animals
        self.animal1 = Animal(
            animal_id="test_herbivore",
            category=AnimalCategory.HERBIVORE,
            location=(0, 0),
            status={'Health': 100, 'Hunger': 50, 'Thirst': 80, 'Energy': 60},
            traits={'Strength': 40, 'Agility': 70, 'Intelligence': 50, 'Endurance': 50, 'Perception': 50}
        )
        
        self.animal2 = Animal(
            animal_id="test_carnivore", 
            category=AnimalCategory.CARNIVORE,
            location=(2, 0),
            status={'Health': 90, 'Hunger': 30, 'Thirst': 70, 'Energy': 80},
            traits={'Strength': 80, 'Agility': 50, 'Intelligence': 50, 'Endurance': 50, 'Perception': 50}
        )
        
        # Place animals in world
        self.world.get_tile(0, 0).occupant = self.animal1
        self.world.get_tile(2, 0).occupant = self.animal2
        
        # Add animals to simulation
        self.simulation.add_animal(self.animal1)
        self.simulation.add_animal(self.animal2)
        
        # Create action resolver
        self.action_resolver = ActionResolver(self.simulation, self.logger)

    def test_action_resolver_initialization(self):
        """Test ActionResolver initialization."""
        self.assertIsNotNone(self.action_resolver)
        self.assertEqual(self.action_resolver.simulation, self.simulation)
        self.assertEqual(self.action_resolver.logger, self.logger)
        self.assertIsInstance(self.action_resolver.decision_engine, DecisionEngine)
        self.assertIsInstance(self.action_resolver.status_engine, StatusEngine)
        self.assertIsInstance(self.action_resolver.execution_engine, ExecutionEngine)
        self.assertIsInstance(self.action_resolver.cleanup_engine, CleanupEngine)

    def test_animal_action_creation(self):
        """Test AnimalAction data structure."""
        action = AnimalAction(
            animal_id="test_id",
            animal=self.animal1,
            action_type=ActionType.MOVE_NORTH
        )
        
        self.assertEqual(action.animal_id, "test_id")
        self.assertEqual(action.animal, self.animal1)
        self.assertEqual(action.action_type, ActionType.MOVE_NORTH)
        self.assertEqual(action.energy_cost, 5.0)  # Movement cost
        self.assertFalse(action.success)
        self.assertEqual(action.result_message, "")

    def test_animal_action_energy_costs(self):
        """Test energy cost calculation for different actions."""
        # Movement actions
        move_action = AnimalAction("test", self.animal1, ActionType.MOVE_EAST)
        self.assertEqual(move_action.energy_cost, 5.0)
        
        # Attack action
        attack_action = AnimalAction("test", self.animal1, ActionType.ATTACK)
        self.assertEqual(attack_action.energy_cost, 10.0)
        
        # Rest action
        rest_action = AnimalAction("test", self.animal1, ActionType.REST)
        self.assertEqual(rest_action.energy_cost, 0.0)
        
        # Eat/Drink actions
        eat_action = AnimalAction("test", self.animal1, ActionType.EAT)
        self.assertEqual(eat_action.energy_cost, 2.0)

    def test_complete_action_resolution_system(self):
        """Test the complete 4-phase action resolution system."""
        result = self.action_resolver.execute_action_resolution_system(1)
        
        # Verify result structure
        self.assertIsInstance(result, dict)
        self.assertIn('phase', result)
        self.assertIn('week', result)
        self.assertIn('success', result)
        self.assertIn('phases_completed', result)
        self.assertIn('actions_processed', result)
        self.assertIn('casualties', result)
        
        # Should complete all 4 phases
        self.assertEqual(result['phases_completed'], 4)
        self.assertTrue(result['success'])

    def test_decision_phase(self):
        """Test the decision phase."""
        living_animals = self.simulation.get_living_animals()
        actions = self.action_resolver.decision_engine.execute_decision_phase(living_animals)
        
        # Should create actions for all living animals
        self.assertEqual(len(actions), 2)
        
        # All actions should be AnimalAction instances
        for action in actions:
            self.assertIsInstance(action, AnimalAction)
            self.assertIn(action.animal, living_animals)

    def test_status_environmental_phase(self):
        """Test the status & environmental phase."""
        living_animals = self.simulation.get_living_animals()
        initial_count = len(living_animals)
        
        results = self.action_resolver.status_engine.execute_status_environmental_phase(living_animals)
        
        # Verify results structure
        self.assertIn('animals_processed', results)
        self.assertIn('hunger_depletion', results)
        self.assertIn('thirst_depletion', results)
        self.assertIn('health_loss', results)
        self.assertIn('energy_regeneration', results)
        self.assertIn('casualties', results)
        
        # Should process all animals
        self.assertEqual(results['animals_processed'], initial_count)

    def test_action_execution_phase(self):
        """Test the action execution phase."""
        # Create some test actions
        actions = [
            AnimalAction("test1", self.animal1, ActionType.REST),
            AnimalAction("test2", self.animal2, ActionType.MOVE_NORTH, target_location=(2, -1))  # Out of bounds
        ]
        
        results = self.action_resolver.execution_engine.execute_action_execution_phase(actions)
        
        # Verify results structure
        self.assertIn('actions_executed', results)
        self.assertIn('actions_failed', results)
        self.assertIn('conflicts', results)
        self.assertIn('movement_conflicts', results)
        
        # Should process all actions
        total_processed = results['actions_executed'] + results['actions_failed']
        self.assertEqual(total_processed, len(actions))

    def test_cleanup_phase(self):
        """Test the cleanup phase."""
        living_animals = self.simulation.get_living_animals()
        
        # Set up some conditions for effect addition
        self.animal1.status['Hunger'] = 95  # Should get Well-Fed effect
        self.animal2.status['Energy'] = 15  # Should get Exhausted effect
        
        results = self.action_resolver.cleanup_engine.execute_cleanup_phase(living_animals)
        
        # Verify results structure
        self.assertIn('animals_processed', results)
        self.assertIn('effects_added', results)
        self.assertIn('effects_removed', results)
        self.assertIn('effects_updated', results)
        
        # Should process all animals
        self.assertEqual(results['animals_processed'], len(living_animals))

    def test_movement_conflict_resolution(self):
        """Test movement conflict resolution based on agility."""
        # Create conflicting movement actions to same location
        action1 = AnimalAction("test1", self.animal1, ActionType.MOVE_EAST, target_location=(1, 0))
        action2 = AnimalAction("test2", self.animal2, ActionType.MOVE_WEST, target_location=(1, 0))
        
        # animal1 has higher agility (70 vs 50), so should win
        winner = self.action_resolver.execution_engine._resolve_movement_conflict([action1, action2])
        
        self.assertEqual(winner, action1)  # Higher agility wins

    def test_resource_consumption(self):
        """Test resource consumption during eat/drink actions."""
        # Test eating
        eat_action = AnimalAction("test", self.animal1, ActionType.EAT, target_location=(0, 0))
        
        # Get initial resource count
        tile = self.world.get_tile(0, 0)
        initial_uses = tile.resource.uses_left if tile.resource else 0
        
        if initial_uses > 0:
            success = self.action_resolver.execution_engine._execute_eat_action(eat_action)
            self.assertTrue(success)
            
            # Resource should be consumed
            if tile.resource:
                self.assertLess(tile.resource.uses_left, initial_uses)

    def test_animal_death_conditions(self):
        """Test animal death from various causes."""
        # Set up animal with critical status
        dying_animal = Animal(
            animal_id="dying",
            category=AnimalCategory.OMNIVORE,
            location=(2, 2),
            status={'Health': 1, 'Hunger': 0, 'Thirst': 0, 'Energy': 50},
            traits={'Strength': 50, 'Agility': 50, 'Intelligence': 50, 'Endurance': 50, 'Perception': 50}
        )
        
        self.simulation.add_animal(dying_animal)
        self.world.get_tile(2, 2).occupant = dying_animal
        
        # Run status phase
        living_animals = self.simulation.get_living_animals()
        results = self.action_resolver.status_engine.execute_status_environmental_phase(living_animals)
        
        # Should have casualties
        self.assertGreater(len(results['casualties']), 0)

    def test_integration_with_simulation_controller(self):
        """Test integration with SimulationController."""
        config = SimulationConfig(population_size=5, max_weeks=2)
        controller = SimulationController(config)
        
        # Initialize world and population
        controller.initialize_world()
        controller.initialize_population()
        
        # Test action resolution system
        result = controller.execute_action_resolution_system(1)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['phases_completed'], 4)


class TestDecisionEngine(unittest.TestCase):
    """Test the decision engine specifically."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.logger = Mock()
        self.simulation = Mock()
        self.decision_engine = DecisionEngine(self.simulation, self.logger)

    def test_decision_engine_initialization(self):
        """Test DecisionEngine initialization."""
        self.assertEqual(self.decision_engine.simulation, self.simulation)
        self.assertEqual(self.decision_engine.logger, self.logger)

    def test_target_location_calculation(self):
        """Test target location calculation for movement."""
        # Test all movement directions
        self.assertEqual(self.decision_engine._calculate_target_location(1, 1, ActionType.MOVE_NORTH), (1, 0))
        self.assertEqual(self.decision_engine._calculate_target_location(1, 1, ActionType.MOVE_EAST), (2, 1))
        self.assertEqual(self.decision_engine._calculate_target_location(1, 1, ActionType.MOVE_SOUTH), (1, 2))
        self.assertEqual(self.decision_engine._calculate_target_location(1, 1, ActionType.MOVE_WEST), (0, 1))
        
        # Test non-movement action
        self.assertEqual(self.decision_engine._calculate_target_location(1, 1, ActionType.REST), (1, 1))


class TestExecutionEngine(unittest.TestCase):
    """Test the execution engine specifically."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.logger = Mock()
        self.simulation = Mock()
        self.execution_engine = ExecutionEngine(self.simulation, self.logger)

    def test_execution_engine_initialization(self):
        """Test ExecutionEngine initialization."""
        self.assertEqual(self.execution_engine.simulation, self.simulation)
        self.assertEqual(self.execution_engine.logger, self.logger)


def run_action_resolution_tests():
    """Run all action resolution tests."""
    print("🧪 Running Action Resolution System tests...")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestActionResolutionSystem))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDecisionEngine))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestExecutionEngine))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print("=" * 60)
    if result.wasSuccessful():
        print("✅ All action resolution tests passed!")
        return True
    else:
        print("❌ Some action resolution tests failed!")
        return False


if __name__ == "__main__":
    run_action_resolution_tests()
