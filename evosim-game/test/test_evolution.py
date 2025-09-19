"""
Unit tests for the evolutionary algorithm.
"""

import unittest
import sys
import os
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures import Animal, AnimalCategory
from mlp import MLPNetwork
from evolution import evolve_population, one_point_crossover, mutate


class TestEvolution(unittest.TestCase):
    def _make_animal_with_score(self, aid: str, score: float) -> Animal:
        a = Animal(
            animal_id=aid,
            category=AnimalCategory.HERBIVORE,
            location=(0, 0),
            status={'Health': 100, 'Hunger': 100, 'Thirst': 100, 'Energy': 100, 'Instinct': 0.0},
            traits={'STR': 5, 'AGI': 5, 'INT': 5, 'END': 5, 'PER': 5}
        )
        a.mlp_network = MLPNetwork()
        a.fitness_score_components = {'Time': score, 'Resource': 0.0, 'Kill': 0.0, 'Distance': 0.0, 'Event': 0.0}
        return a

    def test_evolve_population_size_preserved(self):
        rng = random.Random(123)
        parents = [self._make_animal_with_score(f"a{i}", i) for i in range(10)]
        children = evolve_population(parents, rng)
        self.assertEqual(len(children), len(parents))

    def test_crossover_length(self):
        rng = random.Random(1)
        net = MLPNetwork()
        w = net.get_parameters_flat()
        c = one_point_crossover(w, w, rng)
        self.assertEqual(len(c), len(w))

    def test_mutation_changes_some(self):
        rng = random.Random(2)
        net = MLPNetwork()
        w = net.get_parameters_flat()
        m = mutate(w, rng, rate=1.0, sigma=0.01)
        self.assertNotEqual(w, m)


if __name__ == "__main__":
    unittest.main(verbosity=2)


