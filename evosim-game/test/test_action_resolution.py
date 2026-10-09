"""
Unit tests for action_resolution/
"""

import unittest
import sys
import os
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures import (
    Simulation, AnimalCategory, ActionType, create_random_animal
)
from action_resolution import ActionResolver
from action_resolution.action_data import AnimalAction
from action_resolution.execution_engine import ExecutionEngine
from world_generator import WorldGenerator, GenerationConfig


class TestActionResolution(unittest.TestCase):
    """Test 4-phase action resolution system, combat, and resource consumption."""

    def setUp(self):
        self.logger = logging.getLogger("TestAR")
        self.logger.setLevel(logging.WARNING)
        gen = WorldGenerator(GenerationConfig(width=25, height=25))
        self.world = gen.generate_world(seed=42)
        self.sim = Simulation()
        self.sim.world = self.world

    def test_full_action_resolution_cycle(self):
        """Test complete 4-phase resolution on a living population."""
        animals = [create_random_animal(f"a_{i}", AnimalCategory.HERBIVORE) for i in range(4)]
        WorldGenerator(GenerationConfig()).place_animals(self.world, animals)
        for a in animals:
            self.sim.add_animal(a)
            
        resolver = ActionResolver(self.sim, self.logger)
        res = resolver.execute_action_resolution_system(week=1)
        
        self.assertTrue(res['success'])
        self.assertEqual(res['phases_completed'], 4)
        self.assertEqual(res['actions_processed'], 4)

    def test_combat_attack_execution(self):
        """Test attack action damages adjacent target and credits kill when health reaches 0."""
        engine = ExecutionEngine(self.sim, self.logger)
        
        # Place attacker and target adjacent
        attacker = create_random_animal("attacker", AnimalCategory.CARNIVORE)
        target = create_random_animal("target", AnimalCategory.HERBIVORE)
        
        attacker.location = (10, 10)
        target.location = (10, 11)
        self.world.get_tile(10, 10).occupant = attacker
        self.world.get_tile(10, 11).occupant = target
        
        self.sim.add_animal(attacker)
        self.sim.add_animal(target)
        
        target.status['Health'] = 5.0  # Low health to test kill
        
        action = AnimalAction(
            animal_id=attacker.animal_id,
            animal=attacker,
            action_type=ActionType.ATTACK,
            target_location=(10, 11)
        )
        
        success = engine._execute_attack_action(action)
        self.assertTrue(success)
        self.assertTrue(action.success)
        # Target was low health, so if hit, it dies
        if target.status['Health'] <= 0.0:
            self.assertIn(target, self.sim.get_dead_animals())
            self.assertEqual(attacker.fitness_score_components.get('Kill', 0), 1)


if __name__ == '__main__':
    unittest.main()
