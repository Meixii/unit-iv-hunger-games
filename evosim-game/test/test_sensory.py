"""
Unit tests for sensory.py
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sensory import build_input_vector, get_vision_radius
from data_structures import Simulation, AnimalCategory, create_random_animal
from world_generator import WorldGenerator, GenerationConfig


class TestSensory(unittest.TestCase):
    """Test sensory input perception vector generation."""

    def test_vision_radii(self):
        """Test category-specific sensory vision radius."""
        self.assertEqual(get_vision_radius(AnimalCategory.HERBIVORE), 1)  # 3x3
        self.assertEqual(get_vision_radius(AnimalCategory.OMNIVORE), 2)   # 5x5
        self.assertEqual(get_vision_radius(AnimalCategory.CARNIVORE), 3)  # 7x7

    def test_input_vector_shape_and_bounds(self):
        """Test 41-node input vector generation is normalized between 0.0 and 1.0."""
        gen = WorldGenerator(GenerationConfig(width=25, height=25))
        world = gen.generate_world(seed=42)
        sim = Simulation()
        sim.world = world
        
        animal = create_random_animal("perceiver", AnimalCategory.HERBIVORE)
        gen.place_animals(world, [animal])
        sim.add_animal(animal)
        
        vector = build_input_vector(sim, animal)
        self.assertEqual(len(vector), 41)
        for val in vector:
            self.assertTrue(0.0 <= val <= 1.0, f"Value {val} out of bounds [0.0, 1.0]")


if __name__ == '__main__':
    unittest.main()
