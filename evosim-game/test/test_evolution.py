"""
Unit tests for evolution.py
"""

import unittest
import sys
import os
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from evolution import (
    evolve_population, one_point_crossover, mutate, select_parents_tournament
)
from data_structures import AnimalCategory, create_random_animal
from fitness import increment_time, add_kill


class TestEvolution(unittest.TestCase):
    """Test genetic algorithm operators: elitism, tournament selection, crossover, mutation."""

    def test_one_point_crossover(self):
        """Test crossover combines slices from both parents."""
        rng = random.Random(42)
        p1 = [1.0] * 20
        p2 = [2.0] * 20
        child = one_point_crossover(p1, p2, rng)
        self.assertEqual(len(child), 20)
        self.assertIn(1.0, child)
        self.assertIn(2.0, child)

    def test_mutation(self):
        """Test Gaussian mutation alters weights with probability."""
        rng = random.Random(42)
        params = [0.0] * 50
        mutated = mutate(params, rng, rate=1.0, sigma=0.1)
        self.assertEqual(len(mutated), 50)
        self.assertTrue(any(p != 0.0 for p in mutated))

    def test_evolve_population_preserves_size_and_elitism(self):
        """Test evolving population maintains count and propagates elite."""
        parents = [create_random_animal(f"p_{i}", AnimalCategory.HERBIVORE) for i in range(10)]
        for i, p in enumerate(parents):
            increment_time(p, i * 5)
        
        best_parent = max(parents, key=lambda a: a.get_fitness_score())
        next_gen = evolve_population(parents, rng=random.Random(42))
        
        self.assertEqual(len(next_gen), 10)
        # Verify elite brain preserved
        elite_child = next_gen[0]
        self.assertEqual(elite_child.mlp_network.get_parameters_flat(), best_parent.mlp_network.get_parameters_flat())


if __name__ == '__main__':
    unittest.main()
