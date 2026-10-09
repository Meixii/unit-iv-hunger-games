"""
Unit tests for world_generator.py
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from world_generator import WorldGenerator, GenerationConfig, WorldValidator
from data_structures import TerrainType, AnimalCategory, create_random_animal


class TestWorldGenerator(unittest.TestCase):
    """Test procedural 2D world generation and entity placement."""

    def test_world_dimensions_and_borders(self):
        """Test world generation grid size and mountain borders."""
        cfg = GenerationConfig(width=25, height=25, mountain_border=True)
        gen = WorldGenerator(cfg)
        world = gen.generate_world(seed=42)
        
        self.assertEqual(world.dimensions, (25, 25))
        
        # Check border tiles are Mountains
        for x in range(25):
            self.assertEqual(world.get_tile(x, 0).terrain_type, TerrainType.MOUNTAINS)
            self.assertEqual(world.get_tile(x, 24).terrain_type, TerrainType.MOUNTAINS)
        for y in range(25):
            self.assertEqual(world.get_tile(0, y).terrain_type, TerrainType.MOUNTAINS)
            self.assertEqual(world.get_tile(24, y).terrain_type, TerrainType.MOUNTAINS)

    def test_animal_placement_validity(self):
        """Test animals are placed on passable, non-duplicate tiles."""
        cfg = GenerationConfig(width=25, height=25, mountain_border=True)
        gen = WorldGenerator(cfg)
        world = gen.generate_world(seed=123)
        
        animals = [create_random_animal(f"a_{i}", AnimalCategory.HERBIVORE) for i in range(10)]
        gen.place_animals(world, animals)
        self.assertEqual(len(animals), 10)
        
        locations = set()
        for a in animals:
            self.assertIsNotNone(a.location)
            self.assertNotIn(a.location, locations)
            locations.add(a.location)
            
            tile = world.get_tile(*a.location)
            self.assertIsNotNone(tile)
            self.assertNotEqual(tile.terrain_type, TerrainType.MOUNTAINS)
            self.assertEqual(tile.occupant, a)


if __name__ == '__main__':
    unittest.main()
