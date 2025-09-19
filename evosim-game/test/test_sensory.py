"""
Unit tests for sensory input builder.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures import Simulation, World, Tile, TerrainType, Animal, AnimalCategory, Resource, ResourceType
from sensory import build_input_vector


class TestSensory(unittest.TestCase):
    def setUp(self):
        self.sim = Simulation()
        # 3x3 with water center and a plant at (0,0)
        grid = []
        for y in range(3):
            row = []
            for x in range(3):
                terrain = TerrainType.PLAINS if (x, y) != (1, 1) else TerrainType.WATER
                row.append(Tile(coordinates=(x, y), terrain_type=terrain))
            grid.append(row)
        world = World(grid=grid, dimensions=(3, 3))
        world.get_tile(0, 0).resource = Resource(resource_type=ResourceType.PLANT, quantity=5, uses_left=2)
        self.sim.world = world

        self.animal = Animal(
            animal_id="s1",
            category=AnimalCategory.HERBIVORE,
            location=(1, 1),
            status={'Health': 100, 'Hunger': 80, 'Thirst': 90, 'Energy': 100, 'Instinct': 0.0},
            traits={'STR': 5, 'AGI': 5, 'INT': 5, 'END': 5, 'PER': 5}
        )

    def test_vector_length_and_bounds(self):
        v = build_input_vector(self.sim, self.animal)
        self.assertEqual(len(v), 41)
        for val in v:
            self.assertGreaterEqual(val, 0.0)
            self.assertLessEqual(val, 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)


