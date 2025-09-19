"""
Basic tests for fitness helpers and Animal.get_fitness_score.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures import Animal, AnimalCategory
from fitness import init_fitness_components, increment_time, add_distance, add_resource_units, add_kill, add_event_survived


class TestFitness(unittest.TestCase):
    def test_components_and_score(self):
        a = Animal(
            animal_id="f1",
            category=AnimalCategory.HERBIVORE,
            location=(0, 0),
            status={'Health': 100, 'Hunger': 100, 'Thirst': 100, 'Energy': 100, 'Instinct': 0.0},
            traits={'STR': 5, 'AGI': 5, 'INT': 5, 'END': 5, 'PER': 5}
        )
        init_fitness_components(a)
        increment_time(a, 10)
        add_distance(a, 5)
        add_resource_units(a, 80)
        add_kill(a, 1)
        add_event_survived(a, 2)
        score = a.get_fitness_score()
        self.assertGreater(score, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)


