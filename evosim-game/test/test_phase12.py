"""
Simulation Engine Testing: Phase 1 (Decision) + Phase 2 (Status)

Validates that Decision and Status phases run correctly over a small world
using the existing ActionResolver components without executing actions.
"""

import unittest
import sys
import os
from unittest.mock import Mock

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures import (
    Simulation, World, Animal, Tile,
    AnimalCategory, TerrainType
)
from action_resolution import (
    ActionResolver, DecisionEngine, StatusEngine, ActionType, AnimalAction
)


class TestPhase12Simulation(unittest.TestCase):
    """Tests for Decision + Status phases only."""

    def setUp(self):
        self.logger = Mock()
        self.simulation = Simulation()

        # Build a 3x3 simple world with a water tile in center
        grid = []
        for y in range(3):
            row = []
            for x in range(3):
                terrain = TerrainType.PLAINS if (x, y) != (1, 1) else TerrainType.WATER
                row.append(Tile(coordinates=(x, y), terrain_type=terrain))
            grid.append(row)
        self.world = World(grid=grid, dimensions=(3, 3))
        self.simulation.world = self.world

        # Two simple animals
        self.animal1 = Animal(
            animal_id="p12_herbivore",
            category=AnimalCategory.HERBIVORE,
            location=(0, 0),
            status={'Health': 100, 'Hunger': 60, 'Thirst': 60, 'Energy': 80},
            traits={'STR': 50, 'AGI': 60, 'INT': 50, 'END': 50, 'PER': 50}
        )
        self.animal2 = Animal(
            animal_id="p12_carnivore",
            category=AnimalCategory.CARNIVORE,
            location=(2, 2),
            status={'Health': 100, 'Hunger': 60, 'Thirst': 60, 'Energy': 80},
            traits={'STR': 70, 'AGI': 50, 'INT': 50, 'END': 50, 'PER': 50}
        )

        self.world.get_tile(0, 0).occupant = self.animal1
        self.world.get_tile(2, 2).occupant = self.animal2
        self.simulation.add_animal(self.animal1)
        self.simulation.add_animal(self.animal2)

        self.decision_engine = DecisionEngine(self.simulation, self.logger)
        self.status_engine = StatusEngine(self.simulation, self.logger)

    def test_decision_phase_outputs_actions(self):
        living = self.simulation.get_living_animals()
        actions = self.decision_engine.execute_decision_phase(living)
        self.assertEqual(len(actions), len(living))
        for act in actions:
            self.assertIsInstance(act, AnimalAction)
            self.assertIn(act.action_type, list(ActionType))

    def test_status_phase_updates_stats(self):
        living = self.simulation.get_living_animals()
        before = [(a.status['Hunger'], a.status['Thirst'], a.status['Energy'], a.status['Health']) for a in living]
        results = self.status_engine.execute_status_environmental_phase(living)
        self.assertEqual(results['animals_processed'], len(living))
        after = [(a.status['Hunger'], a.status['Thirst'], a.status['Energy'], a.status['Health']) for a in living]
        # Hunger and Thirst should not increase
        for (h0, t0, e0, _), (h1, t1, e1, _) in zip(before, after):
            self.assertLessEqual(h1, h0)
            self.assertLessEqual(t1, t0)
            self.assertGreaterEqual(e1, e0)  # passive regen can increase energy


def run_phase12_tests():
    print("🧪 Running Phase 1+2 tests...")
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestPhase12Simulation)
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite).wasSuccessful()


if __name__ == "__main__":
    run_phase12_tests()


