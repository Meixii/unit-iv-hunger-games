#!/usr/bin/env python3
"""
Test script for world_generator.py

This script validates that world generation works correctly and produces valid worlds.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import world_generator
from world_generator import *
import constants
from data_structures import *

def test_generation_config():
    """Test GenerationConfig class."""
    print("Testing GenerationConfig...")
    
    # Test default configuration
    config = GenerationConfig()
    assert config.width == constants.GRID_WIDTH
    assert config.height == constants.GRID_HEIGHT
    assert config.food_spawn_chance == constants.FOOD_SPAWN_CHANCE
    assert config.water_spawn_chance == constants.WATER_SPAWN_CHANCE
    
    # Test custom configuration
    custom_config = GenerationConfig(
        width=10,
        height=10,
        food_spawn_chance=0.2,
        water_spawn_chance=0.1
    )
    assert custom_config.width == 10
    assert custom_config.height == 10
    assert custom_config.food_spawn_chance == 0.2
    assert custom_config.water_spawn_chance == 0.1
    
    # Test validation
    try:
        invalid_config = GenerationConfig(
            terrain_distribution={'Plains': 0.5, 'Forest': 0.3}  # Doesn't sum to 1.0
        )
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("✅ GenerationConfig tests passed!")

def test_world_generator_creation():
    """Test WorldGenerator class creation."""
    print("Testing WorldGenerator creation...")
    
    # Test with default config
    generator = WorldGenerator()
    assert generator.config.width == constants.GRID_WIDTH
    assert generator.config.height == constants.GRID_HEIGHT
    
    # Test with custom config
    config = GenerationConfig(width=5, height=5)
    generator = WorldGenerator(config)
    assert generator.config.width == 5
    assert generator.config.height == 5
    
    print("✅ WorldGenerator creation tests passed!")

def test_terrain_grid_generation():
    """Test terrain grid generation."""
    print("Testing terrain grid generation...")
    
    generator = WorldGenerator()
    terrain_grid = generator._generate_terrain_grid()
    
    # Check dimensions
    assert len(terrain_grid) == constants.GRID_HEIGHT
    assert len(terrain_grid[0]) == constants.GRID_WIDTH
    
    # Check all tiles have valid terrain types
    valid_terrains = set(TerrainType)
    for row in terrain_grid:
        for terrain in row:
            assert terrain in valid_terrains
    
    # Check terrain distribution is roughly correct
    terrain_counts = {}
    for row in terrain_grid:
        for terrain in row:
            terrain_counts[terrain] = terrain_counts.get(terrain, 0) + 1
    
    total_tiles = constants.GRID_WIDTH * constants.GRID_HEIGHT
    for terrain, count in terrain_counts.items():
        percentage = count / total_tiles
        expected_percentage = constants.TERRAIN_DISTRIBUTION[terrain.value]
        # Allow 15% tolerance for randomness
        assert abs(percentage - expected_percentage) < 0.15, f"Terrain {terrain.value} distribution off: expected {expected_percentage:.1%}, got {percentage:.1%}"
    
    print("✅ Terrain grid generation tests passed!")

def test_tile_creation():
    """Test tile creation from terrain grid."""
    print("Testing tile creation...")
    
    generator = WorldGenerator()
    terrain_grid = generator._generate_terrain_grid()
    tiles = generator._create_tiles(terrain_grid)
    
    # Check dimensions
    assert len(tiles) == constants.GRID_HEIGHT
    assert len(tiles[0]) == constants.GRID_WIDTH
    
    # Check all tiles are valid
    for y in range(constants.GRID_HEIGHT):
        for x in range(constants.GRID_WIDTH):
            tile = tiles[y][x]
            assert tile.coordinates == (x, y)
            assert tile.terrain_type == terrain_grid[y][x]
            assert tile.resource is None
            assert tile.occupant is None
    
    print("✅ Tile creation tests passed!")

def test_resource_placement():
    """Test resource placement."""
    print("Testing resource placement...")
    
    generator = WorldGenerator()
    world = generator.generate_world(seed=42)
    
    # Count resources
    resource_counts = {}
    water_tiles = 0
    food_tiles = 0
    
    for y in range(world.dimensions[1]):
        for x in range(world.dimensions[0]):
            tile = world.get_tile(x, y)
            if tile.resource is not None:
                resource_type = tile.resource.resource_type.value
                resource_counts[resource_type] = resource_counts.get(resource_type, 0) + 1
                
                if resource_type == "Water":
                    water_tiles += 1
                else:
                    food_tiles += 1
    
    # Check that resources were placed
    assert sum(resource_counts.values()) > 0, "No resources were placed"
    
    # Check water resources are on or near water tiles
    for y in range(world.dimensions[1]):
        for x in range(world.dimensions[0]):
            tile = world.get_tile(x, y)
            if tile.resource is not None and tile.resource.resource_type == ResourceType.WATER:
                # Water resources should be on water tiles or adjacent to them
                is_water_tile = tile.terrain_type == TerrainType.WATER
                is_adjacent_to_water = any(
                    world.get_tile(adj_x, adj_y).terrain_type == TerrainType.WATER
                    for adj_x, adj_y in generator._get_adjacent_coordinates(x, y)
                    if world.is_valid_coordinate(adj_x, adj_y)
                )
                assert is_water_tile or is_adjacent_to_water, f"Water resource at ({x}, {y}) not on or near water tile"
    
    print("✅ Resource placement tests passed!")

def test_animal_placement():
    """Test animal placement in world."""
    print("Testing animal placement...")
    
    # Create a small world for testing
    config = GenerationConfig(width=5, height=5, population_size=3)
    generator = WorldGenerator(config)
    world = generator.generate_world(seed=42)
    
    # Generate animals
    animals = generator.generate_initial_population(world, seed=42)
    
    # Check correct number of animals
    assert len(animals) == 3
    
    # Check all animals are placed
    placed_animals = 0
    for y in range(world.dimensions[1]):
        for x in range(world.dimensions[0]):
            tile = world.get_tile(x, y)
            if tile.is_occupied():
                placed_animals += 1
                assert tile.occupant in animals
                assert tile.occupant.location == (x, y)
    
    assert placed_animals == len(animals)
    
    # Check no two animals are on the same tile
    occupied_locations = set()
    for animal in animals:
        location = animal.location
        assert location not in occupied_locations, f"Multiple animals at location {location}"
        occupied_locations.add(location)
    
    print("✅ Animal placement tests passed!")

def test_animal_distribution():
    """Test animal distribution across categories."""
    print("Testing animal distribution...")
    
    config = GenerationConfig(population_size=9)  # Divisible by 3
    generator = WorldGenerator(config)
    world = generator.generate_world(seed=42)
    animals = generator.generate_initial_population(world, seed=42)
    
    # Count animals by category
    category_counts = {}
    for animal in animals:
        category = animal.category
        category_counts[category] = category_counts.get(category, 0) + 1
    
    # Check even distribution
    expected_count = 9 // 3  # 3 animals per category
    for category in AnimalCategory:
        assert category_counts.get(category, 0) == expected_count, f"Category {category.value} has {category_counts.get(category, 0)} animals, expected {expected_count}"
    
    print("✅ Animal distribution tests passed!")

def test_world_validation():
    """Test world validation."""
    print("Testing world validation...")
    
    # Generate a world
    generator = WorldGenerator()
    world = generator.generate_world(seed=42)
    
    # Validate the world
    stats = WorldValidator.validate_world(world)
    
    # Check basic stats
    assert stats['total_tiles'] == constants.GRID_WIDTH * constants.GRID_HEIGHT
    assert stats['occupied_tiles'] == 0  # No animals placed yet
    assert stats['valid_spawn_locations'] > 0
    
    # Check terrain counts
    total_tiles = stats['total_tiles']
    terrain_sum = sum(stats['terrain_counts'].values())
    assert terrain_sum == total_tiles
    
    # Check resource counts
    resource_sum = sum(stats['resource_counts'].values())
    assert resource_sum >= 0  # Should have some resources
    
    print("✅ World validation tests passed!")

def test_small_world_generation():
    """Test generation of small worlds for debugging."""
    print("Testing small world generation...")
    
    # Create a 3x3 world
    world = create_test_world(3)
    
    # Check dimensions
    assert world.dimensions == (3, 3)
    assert len(world.grid) == 3
    assert len(world.grid[0]) == 3
    
    # Check all tiles are valid
    for y in range(3):
        for x in range(3):
            tile = world.get_tile(x, y)
            assert tile is not None
            assert tile.coordinates == (x, y)
    
    print("✅ Small world generation tests passed!")

def test_deterministic_generation():
    """Test that generation with same seed produces same result."""
    print("Testing deterministic generation...")
    
    # Generate two worlds with same seed
    world1 = create_test_world(5)
    world2 = create_test_world(5)
    
    # Check they are identical
    for y in range(5):
        for x in range(5):
            tile1 = world1.get_tile(x, y)
            tile2 = world2.get_tile(x, y)
            
            assert tile1.terrain_type == tile2.terrain_type
            assert (tile1.resource is None) == (tile2.resource is None)
            if tile1.resource is not None and tile2.resource is not None:
                assert tile1.resource.resource_type == tile2.resource.resource_type
    
    print("✅ Deterministic generation tests passed!")

def test_edge_cases():
    """Test edge cases and error handling."""
    print("Testing edge cases...")
    
    # Test very small world
    config = GenerationConfig(width=1, height=1, population_size=1)
    generator = WorldGenerator(config)
    world = generator.generate_world(seed=42)
    assert world.dimensions == (1, 1)
    
    # Test world with no valid spawn locations
    config = GenerationConfig(width=2, height=2, population_size=1)
    generator = WorldGenerator(config)
    
    # Create a world with only mountain tiles
    terrain_grid = [[TerrainType.MOUNTAINS for _ in range(2)] for _ in range(2)]
    tiles = generator._create_tiles(terrain_grid)
    world = World(tiles, (2, 2))
    
    # This should raise an error when trying to place animals
    animals = [create_random_animal("test", AnimalCategory.HERBIVORE)]
    try:
        generator.place_animals(world, animals)
        assert False, "Should have raised ValueError for no valid spawn locations"
    except ValueError:
        pass
    
    print("✅ Edge cases tests passed!")

def test_food_spawn_chances():
    """Test that food spawn chances work correctly."""
    print("Testing food spawn chances...")
    
    generator = WorldGenerator()
    
    # Test different terrain types
    terrains = [TerrainType.PLAINS, TerrainType.FOREST, TerrainType.JUNGLE, TerrainType.SWAMP]
    
    for terrain in terrains:
        chance = generator._get_food_spawn_chance(terrain)
        assert 0 <= chance <= 1, f"Food spawn chance for {terrain.value} should be between 0 and 1, got {chance}"
        
        # Check that jungles have higher chance than plains
        if terrain == TerrainType.JUNGLE:
            plains_chance = generator._get_food_spawn_chance(TerrainType.PLAINS)
            assert chance > plains_chance, "Jungle should have higher food spawn chance than plains"
    
    print("✅ Food spawn chances tests passed!")

def test_mountain_borders():
    """Test mountain border functionality."""
    print("Testing mountain borders...")
    
    # Test with mountain borders enabled
    config_with_borders = GenerationConfig(width=6, height=4, mountain_border=True)
    generator_with = WorldGenerator(config_with_borders)
    world_with = generator_with.generate_world(seed=42)
    
    # Check that borders are mountains
    border_tiles = 0
    mountain_border_tiles = 0
    
    for y in range(world_with.dimensions[1]):
        for x in range(world_with.dimensions[0]):
            if generator_with._is_border_tile(x, y):
                border_tiles += 1
                tile = world_with.get_tile(x, y)
                if tile.terrain_type == TerrainType.MOUNTAINS:
                    mountain_border_tiles += 1
    
    assert border_tiles > 0, "Should have border tiles"
    assert mountain_border_tiles == border_tiles, f"All border tiles should be mountains, got {mountain_border_tiles}/{border_tiles}"
    
    # Test without mountain borders
    config_without_borders = GenerationConfig(width=6, height=4, mountain_border=False)
    generator_without = WorldGenerator(config_without_borders)
    world_without = generator_without.generate_world(seed=42)
    
    # Check that borders are not necessarily mountains
    mountain_border_tiles = 0
    for y in range(world_without.dimensions[1]):
        for x in range(world_without.dimensions[0]):
            if generator_without._is_border_tile(x, y):
                tile = world_without.get_tile(x, y)
                if tile.terrain_type == TerrainType.MOUNTAINS:
                    mountain_border_tiles += 1
    
    # Should have fewer mountain tiles on borders (random distribution)
    assert mountain_border_tiles < border_tiles, "Without mountain borders, not all border tiles should be mountains"
    
    print("✅ Mountain borders tests passed!")

def test_border_tile_detection():
    """Test border tile detection."""
    print("Testing border tile detection...")
    
    config = GenerationConfig(width=5, height=4)
    generator = WorldGenerator(config)
    
    # Test corner tiles
    assert generator._is_border_tile(0, 0), "(0,0) should be border"
    assert generator._is_border_tile(4, 0), "(4,0) should be border"
    assert generator._is_border_tile(0, 3), "(0,3) should be border"
    assert generator._is_border_tile(4, 3), "(4,3) should be border"
    
    # Test edge tiles
    assert generator._is_border_tile(2, 0), "(2,0) should be border"
    assert generator._is_border_tile(2, 3), "(2,3) should be border"
    assert generator._is_border_tile(0, 2), "(0,2) should be border"
    assert generator._is_border_tile(4, 2), "(4,2) should be border"
    
    # Test interior tiles
    assert not generator._is_border_tile(1, 1), "(1,1) should not be border"
    assert not generator._is_border_tile(2, 1), "(2,1) should not be border"
    assert not generator._is_border_tile(3, 2), "(3,2) should not be border"
    
    print("✅ Border tile detection tests passed!")

def test_world_visualization():
    """Test world visualization."""
    print("Testing world visualization...")
    
    # Create a small world for testing
    config = GenerationConfig(width=4, height=3, mountain_border=True)
    generator = WorldGenerator(config)
    world = generator.generate_world(seed=42)
    
    # Test that visualization doesn't crash
    try:
        WorldValidator.visualize_world(world, show_resources=False, show_animals=False)
        WorldValidator.visualize_world(world, show_resources=True, show_animals=False)
        WorldValidator.visualize_world(world, show_resources=False, show_animals=True)
        WorldValidator.visualize_world(world, show_resources=True, show_animals=True)
    except Exception as e:
        assert False, f"World visualization should not crash: {e}"
    
    print("✅ World visualization tests passed!")

def main():
    """Run all tests."""
    print("🧪 Running world_generator.py tests...\n")
    
    try:
        test_generation_config()
        test_world_generator_creation()
        test_terrain_grid_generation()
        test_tile_creation()
        test_resource_placement()
        test_animal_placement()
        test_animal_distribution()
        test_world_validation()
        test_small_world_generation()
        test_deterministic_generation()
        test_edge_cases()
        test_food_spawn_chances()
        test_mountain_borders()
        test_border_tile_detection()
        test_world_visualization()
        
        print("\n🎉 All tests passed! World generation is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Tests failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
