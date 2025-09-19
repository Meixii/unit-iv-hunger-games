#!/usr/bin/env python3
"""
Demonstration of mountain border feature

This script shows the difference between worlds with and without mountain borders.
"""

import world_generator
from world_generator import *
import constants

def demonstrate_mountain_borders():
    """Demonstrate mountain border functionality."""
    print("⛰️  Mountain Border Demonstration")
    print("=" * 50)
    
    # Create configuration with mountain borders enabled
    config_with_borders = GenerationConfig(
        width=10,
        height=8,
        population_size=6,
        mountain_border=True
    )
    
    # Create configuration without mountain borders
    config_without_borders = GenerationConfig(
        width=10,
        height=8,
        population_size=6,
        mountain_border=False
    )
    
    print("1. World WITH Mountain Borders:")
    print("-" * 30)
    generator_with = WorldGenerator(config_with_borders)
    world_with = generator_with.generate_world(seed=42)
    
    # Show statistics
    stats_with = WorldValidator.validate_world(world_with)
    print(f"Total tiles: {stats_with['total_tiles']}")
    print(f"Mountain tiles: {stats_with['terrain_counts'].get('Mountains', 0)}")
    print(f"Border tiles: {2 * (world_with.dimensions[0] + world_with.dimensions[1]) - 4}")
    
    # Visualize the world
    WorldValidator.visualize_world(world_with, show_resources=False, show_animals=False)
    
    print("\n2. World WITHOUT Mountain Borders:")
    print("-" * 30)
    generator_without = WorldGenerator(config_without_borders)
    world_without = generator_without.generate_world(seed=42)
    
    # Show statistics
    stats_without = WorldValidator.validate_world(world_without)
    print(f"Total tiles: {stats_without['total_tiles']}")
    print(f"Mountain tiles: {stats_without['terrain_counts'].get('Mountains', 0)}")
    
    # Visualize the world
    WorldValidator.visualize_world(world_without, show_resources=False, show_animals=False)
    
    print("\n3. Comparison:")
    print("-" * 30)
    print(f"With borders - Mountains: {stats_with['terrain_counts'].get('Mountains', 0)} tiles")
    print(f"Without borders - Mountains: {stats_without['terrain_counts'].get('Mountains', 0)} tiles")
    
    # Calculate border coverage
    border_tiles = 2 * (world_with.dimensions[0] + world_with.dimensions[1]) - 4
    mountain_tiles_with = stats_with['terrain_counts'].get('Mountains', 0)
    border_coverage = (mountain_tiles_with / border_tiles) * 100 if border_tiles > 0 else 0
    
    print(f"Border coverage with mountain borders: {border_coverage:.1f}%")
    print(f"Expected border coverage: 100.0%")

def demonstrate_border_effects():
    """Demonstrate the effects of mountain borders on gameplay."""
    print("\n🎮 Border Effects on Gameplay")
    print("=" * 50)
    
    # Create a world with borders
    config = GenerationConfig(width=8, height=6, population_size=6, mountain_border=True)
    generator = WorldGenerator(config)
    world = generator.generate_world(seed=123)
    
    # Place some animals
    animals = generator.generate_initial_population(world, seed=123)
    
    print("World with mountain borders and animals:")
    WorldValidator.visualize_world(world, show_resources=True, show_animals=True)
    
    # Analyze spawn locations
    valid_spawns = 0
    border_tiles = 0
    mountain_tiles = 0
    
    for y in range(world.dimensions[1]):
        for x in range(world.dimensions[0]):
            tile = world.get_tile(x, y)
            
            if tile.terrain_type == TerrainType.MOUNTAINS:
                mountain_tiles += 1
                if generator._is_border_tile(x, y):
                    border_tiles += 1
            
            if (tile.terrain_type == TerrainType.PLAINS and 
                not tile.is_occupied()):
                valid_spawns += 1
    
    print(f"Analysis:")
    print(f"  Total mountain tiles: {mountain_tiles}")
    print(f"  Mountain tiles on border: {border_tiles}")
    print(f"  Valid spawn locations: {valid_spawns}")
    print(f"  Animals placed: {len(animals)}")
    
    # Show animal locations
    print(f"\nAnimal locations:")
    for animal in animals:
        x, y = animal.location
        tile = world.get_tile(x, y)
        print(f"  {animal.animal_id} ({animal.category.value}) at ({x}, {y}) - {tile.terrain_type.value}")

def demonstrate_different_world_sizes():
    """Demonstrate mountain borders on different world sizes."""
    print("\n📏 Mountain Borders on Different World Sizes")
    print("=" * 50)
    
    sizes = [(5, 5), (8, 6), (12, 8), (15, 10)]
    
    for width, height in sizes:
        config = GenerationConfig(width=width, height=height, mountain_border=True)
        generator = WorldGenerator(config)
        world = generator.generate_world(seed=42)
        
        stats = WorldValidator.validate_world(world)
        mountain_count = stats['terrain_counts'].get('Mountains', 0)
        border_tiles = 2 * (width + height) - 4
        interior_tiles = (width * height) - border_tiles
        
        print(f"{width}x{height} world:")
        print(f"  Total tiles: {width * height}")
        print(f"  Border tiles: {border_tiles}")
        print(f"  Interior tiles: {interior_tiles}")
        print(f"  Mountain tiles: {mountain_count}")
        print(f"  Mountain percentage: {(mountain_count / (width * height)) * 100:.1f}%")
        print()

def demonstrate_border_validation():
    """Demonstrate border validation."""
    print("\n🔍 Border Validation")
    print("=" * 50)
    
    # Test with borders
    config_with = GenerationConfig(width=6, height=4, mountain_border=True)
    generator_with = WorldGenerator(config_with)
    world_with = generator_with.generate_world(seed=42)
    
    stats_with = WorldValidator.validate_world(world_with)
    print("World with mountain borders:")
    WorldValidator.print_world_stats(stats_with)
    
    # Test without borders
    config_without = GenerationConfig(width=6, height=4, mountain_border=False)
    generator_without = WorldGenerator(config_without)
    world_without = generator_without.generate_world(seed=42)
    
    stats_without = WorldValidator.validate_world(world_without)
    print("\nWorld without mountain borders:")
    WorldValidator.print_world_stats(stats_without)

def main():
    """Run all demonstrations."""
    print("🎮 Mountain Border Feature Demonstration\n")
    
    demonstrate_mountain_borders()
    demonstrate_border_effects()
    demonstrate_different_world_sizes()
    demonstrate_border_validation()
    
    print("✅ Mountain border demonstration completed!")

if __name__ == "__main__":
    main()
