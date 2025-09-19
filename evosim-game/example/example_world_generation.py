#!/usr/bin/env python3
"""
Example usage of world_generator.py

This script demonstrates how to generate worlds and analyze their properties.
"""

import world_generator
from world_generator import *
import constants
from data_structures import *

def demonstrate_basic_world_generation():
    """Demonstrate basic world generation."""
    print("🌍 Basic World Generation")
    print("=" * 40)
    
    # Create a small world for demonstration
    config = GenerationConfig(width=8, height=8, population_size=6)
    generator = WorldGenerator(config)
    
    # Generate world
    world = generator.generate_world(seed=42)
    print(f"Generated world: {world.dimensions[0]}x{world.dimensions[1]}")
    
    # Show terrain distribution
    terrain_counts = {}
    for y in range(world.dimensions[1]):
        for x in range(world.dimensions[0]):
            tile = world.get_tile(x, y)
            terrain = tile.terrain_type.value
            terrain_counts[terrain] = terrain_counts.get(terrain, 0) + 1
    
    print("\nTerrain distribution:")
    total_tiles = world.dimensions[0] * world.dimensions[1]
    for terrain, count in sorted(terrain_counts.items()):
        percentage = (count / total_tiles) * 100
        print(f"  {terrain}: {count} tiles ({percentage:.1f}%)")
    
    print()

def demonstrate_resource_placement():
    """Demonstrate resource placement."""
    print("🍎 Resource Placement")
    print("=" * 40)
    
    # Generate world
    generator = WorldGenerator()
    world = generator.generate_world(seed=123)
    
    # Count resources
    resource_counts = {}
    water_locations = []
    food_locations = []
    
    for y in range(world.dimensions[1]):
        for x in range(world.dimensions[0]):
            tile = world.get_tile(x, y)
            if tile.resource is not None:
                resource_type = tile.resource.resource_type.value
                resource_counts[resource_type] = resource_counts.get(resource_type, 0) + 1
                
                if resource_type == "Water":
                    water_locations.append((x, y))
                else:
                    food_locations.append((x, y))
    
    print(f"Total resources placed: {sum(resource_counts.values())}")
    print("\nResource distribution:")
    for resource_type, count in resource_counts.items():
        print(f"  {resource_type}: {count} tiles")
    
    print(f"\nWater locations: {water_locations[:5]}{'...' if len(water_locations) > 5 else ''}")
    print(f"Food locations: {food_locations[:5]}{'...' if len(food_locations) > 5 else ''}")
    
    print()

def demonstrate_animal_placement():
    """Demonstrate animal placement."""
    print("🐾 Animal Placement")
    print("=" * 40)
    
    # Generate world with population
    config = GenerationConfig(width=6, height=6, population_size=8)
    generator = WorldGenerator(config)
    world = generator.generate_world(seed=456)
    animals = generator.generate_initial_population(world, seed=456)
    
    print(f"Placed {len(animals)} animals in {world.dimensions[0]}x{world.dimensions[1]} world")
    
    # Show animal distribution
    category_counts = {}
    for animal in animals:
        category = animal.category.value
        category_counts[category] = category_counts.get(category, 0) + 1
    
    print("\nAnimal distribution:")
    for category, count in category_counts.items():
        print(f"  {category}: {count} animals")
    
    # Show animal locations
    print("\nAnimal locations:")
    for animal in animals[:5]:  # Show first 5
        x, y = animal.location
        tile = world.get_tile(x, y)
        print(f"  {animal.animal_id} ({animal.category.value}) at ({x}, {y}) on {tile.terrain_type.value}")
    
    if len(animals) > 5:
        print(f"  ... and {len(animals) - 5} more")
    
    print()

def demonstrate_world_validation():
    """Demonstrate world validation."""
    print("🔍 World Validation")
    print("=" * 40)
    
    # Generate world
    generator = WorldGenerator()
    world = generator.generate_world(seed=789)
    
    # Validate world
    stats = WorldValidator.validate_world(world)
    
    print(f"Total tiles: {stats['total_tiles']}")
    print(f"Occupied tiles: {stats['occupied_tiles']}")
    print(f"Valid spawn locations: {stats['valid_spawn_locations']}")
    
    print("\nTerrain distribution:")
    total_tiles = stats['total_tiles']
    for terrain, count in sorted(stats['terrain_counts'].items()):
        percentage = (count / total_tiles) * 100
        expected = constants.TERRAIN_DISTRIBUTION.get(terrain, 0) * 100
        print(f"  {terrain}: {count} tiles ({percentage:.1f}%) [expected: {expected:.1f}%]")
    
    print("\nResource distribution:")
    for resource, count in sorted(stats['resource_counts'].items()):
        print(f"  {resource}: {count} tiles")
    
    if stats['errors']:
        print("\n⚠️  Validation errors:")
        for error in stats['errors']:
            print(f"  - {error}")
    else:
        print("\n✅ World validation passed!")
    
    print()

def demonstrate_terrain_effects():
    """Demonstrate terrain effects on movement and resources."""
    print("🏔️ Terrain Effects")
    print("=" * 40)
    
    # Generate world
    generator = WorldGenerator()
    world = generator.generate_world(seed=101112)
    
    # Analyze terrain effects
    terrain_effects = {}
    for y in range(world.dimensions[1]):
        for x in range(world.dimensions[0]):
            tile = world.get_tile(x, y)
            terrain = tile.terrain_type.value
            
            if terrain not in terrain_effects:
                terrain_effects[terrain] = {
                    'count': 0,
                    'movement_cost': tile.get_movement_cost(),
                    'has_resources': 0,
                    'is_passable': 0
                }
            
            terrain_effects[terrain]['count'] += 1
            if tile.resource is not None:
                terrain_effects[terrain]['has_resources'] += 1
            if tile.is_passable():
                terrain_effects[terrain]['is_passable'] += 1
    
    print("Terrain analysis:")
    for terrain, data in sorted(terrain_effects.items()):
        count = data['count']
        movement_cost = data['movement_cost']
        resource_rate = (data['has_resources'] / count) * 100 if count > 0 else 0
        passable_rate = (data['is_passable'] / count) * 100 if count > 0 else 0
        
        print(f"\n{terrain}:")
        print(f"  Tiles: {count}")
        print(f"  Movement cost: {movement_cost}x")
        print(f"  Resource rate: {resource_rate:.1f}%")
        print(f"  Passable: {passable_rate:.1f}%")
    
    print()

def demonstrate_different_world_sizes():
    """Demonstrate generation of different world sizes."""
    print("📏 Different World Sizes")
    print("=" * 40)
    
    sizes = [(5, 5), (10, 10), (15, 15)]
    
    for width, height in sizes:
        config = GenerationConfig(width=width, height=height, population_size=min(10, width * height // 4))
        generator = WorldGenerator(config)
        world = generator.generate_world(seed=42)
        
        # Count resources
        resource_count = 0
        for y in range(height):
            for x in range(width):
                tile = world.get_tile(x, y)
                if tile.resource is not None:
                    resource_count += 1
        
        print(f"{width}x{height} world: {resource_count} resources ({resource_count/(width*height)*100:.1f}%)")
    
    print()

def demonstrate_deterministic_generation():
    """Demonstrate deterministic generation with seeds."""
    print("🎲 Deterministic Generation")
    print("=" * 40)
    
    # Generate two identical worlds
    world1 = create_test_world(5)
    world2 = create_test_world(5)
    
    # Compare terrains
    identical_terrains = 0
    total_tiles = 5 * 5
    
    for y in range(5):
        for x in range(5):
            tile1 = world1.get_tile(x, y)
            tile2 = world2.get_tile(x, y)
            if tile1.terrain_type == tile2.terrain_type:
                identical_terrains += 1
    
    print(f"Identical terrains: {identical_terrains}/{total_tiles} ({identical_terrains/total_tiles*100:.1f}%)")
    
    # Generate different worlds
    world3 = create_test_world(5)
    world4 = create_test_world(5)
    
    # Compare with different seeds
    different_terrains = 0
    for y in range(5):
        for x in range(5):
            tile3 = world3.get_tile(x, y)
            tile4 = world4.get_tile(x, y)
            if tile3.terrain_type != tile4.terrain_type:
                different_terrains += 1
    
    print(f"Different terrains: {different_terrains}/{total_tiles} ({different_terrains/total_tiles*100:.1f}%)")
    
    print()

def demonstrate_complete_simulation_setup():
    """Demonstrate complete simulation setup."""
    print("🎮 Complete Simulation Setup")
    print("=" * 40)
    
    # Generate complete world with population
    world, population = generate_world_with_population(
        config=GenerationConfig(width=8, height=8, population_size=12),
        world_seed=42,
        population_seed=123
    )
    
    print(f"Generated {world.dimensions[0]}x{world.dimensions[1]} world with {len(population)} animals")
    
    # Show population breakdown
    category_counts = {}
    for animal in population:
        category = animal.category.value
        category_counts[category] = category_counts.get(category, 0) + 1
    
    print("\nPopulation breakdown:")
    for category, count in category_counts.items():
        print(f"  {category}: {count} animals")
    
    # Show some animal details
    print("\nSample animals:")
    for animal in population[:3]:
        x, y = animal.location
        tile = world.get_tile(x, y)
        print(f"  {animal.animal_id} ({animal.category.value}) at ({x}, {y})")
        print(f"    Traits: STR={animal.traits['STR']}, AGI={animal.traits['AGI']}, END={animal.traits['END']}")
        print(f"    Health: {animal.status['Health']:.0f}/{animal.get_max_health()}")
        print(f"    Location: {tile.terrain_type.value}")
    
    # Validate the complete setup
    stats = WorldValidator.validate_world(world)
    print(f"\nValidation: {len(stats['errors'])} errors")
    if stats['errors']:
        for error in stats['errors'][:3]:  # Show first 3 errors
            print(f"  - {error}")
    
    print()

def main():
    """Run all demonstrations."""
    print("🎮 EvoSim World Generation Examples\n")
    
    # Run demonstrations
    demonstrate_basic_world_generation()
    demonstrate_resource_placement()
    demonstrate_animal_placement()
    demonstrate_world_validation()
    demonstrate_terrain_effects()
    demonstrate_different_world_sizes()
    demonstrate_deterministic_generation()
    demonstrate_complete_simulation_setup()
    
    print("✅ All world generation examples completed successfully!")

if __name__ == "__main__":
    main()
