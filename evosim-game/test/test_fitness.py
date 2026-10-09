"""
Unit tests for fitness.py
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fitness import (
    init_fitness_components, increment_time, add_distance,
    add_resource_units, add_kill, add_event_survived
)
from data_structures import AnimalCategory, create_random_animal
import constants


class TestFitness(unittest.TestCase):
    """Test fitness scoring and multi-component aggregation."""

    def test_fitness_components_and_weighting(self):
        """Test fitness score accurately computes weighted terms."""
        animal = create_random_animal("scorer", AnimalCategory.HERBIVORE)
        init_fitness_components(animal)
        
        increment_time(animal, 10)       # 10 * 1 = 10
        add_resource_units(animal, 80)   # (80 / 40) * 5 = 10
        add_kill(animal, 1)              # 1 * 50 = 50
        add_distance(animal, 25.0)       # 25 * 0.2 = 5
        add_event_survived(animal, 2)    # 2 * 10 = 20
        
        expected_score = (10 * 1) + ((80 / 40) * 5) + (1 * 50) + (25 * 0.2) + (2 * 10)
        self.assertAlmostEqual(animal.get_fitness_score(), expected_score)


if __name__ == '__main__':
    unittest.main()
