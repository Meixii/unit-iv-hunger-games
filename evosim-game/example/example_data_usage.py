#!/usr/bin/env python3
"""
Example usage of data_structures.py

This script demonstrates how to use the core data structures for the EvoSim simulation.
"""

import data_structures
from data_structures import *
import constants

def demonstrate_effect_system():
    """Demonstrate the effect system."""
    print("🔮 Effect System Demonstration")
    print("=" * 40)
    
    # Create a test animal
    animal = create_random_animal("demo_001", AnimalCategory.HERBIVORE)
    print(f"Created {animal.category.value} with base STR: {animal.traits['STR']}")
    
    # Add a buff effect
    well_fed = create_effect(EffectType.WELL_FED)
    animal.add_effect(well_fed)
    print(f"Added {well_fed.name} effect (duration: {well_fed.duration})")
    
    # Show effective trait
    effective_str = animal.get_effective_trait('STR')
    print(f"Effective STR with {well_fed.name}: {effective_str}")
    
    # Add a debuff effect
    injured = create_effect(EffectType.INJURED)
    animal.add_effect(injured)
    print(f"Added {injured.name} effect (duration: {injured.duration})")
    
    # Show effective trait with both effects
    effective_str_with_both = animal.get_effective_trait('STR')
    effective_agi_with_both = animal.get_effective_trait('AGI')
    print(f"Effective STR with both effects: {effective_str_with_both}")
    print(f"Effective AGI with both effects: {effective_agi_with_both}")
    
    # Simulate time passing
    print("\nSimulating 2 turns...")
    for turn in range(2):
        animal.tick_effects()
        print(f"Turn {turn + 1}: {well_fed.name} duration = {well_fed.duration}")
    
    print()

def demonstrate_resource_system():
    """Demonstrate the resource system."""
    print("🍎 Resource System Demonstration")
    print("=" * 40)
    
    # Create different types of resources
    plant = create_resource(ResourceType.PLANT, 40, 2)
    water = create_resource(ResourceType.WATER, 30, 3)
    prey = create_resource(ResourceType.PREY, 50, 1)
    
    print(f"Created {plant.resource_type.value}: {plant.quantity} units, {plant.uses_left} uses")
    print(f"Created {water.resource_type.value}: {water.quantity} units, {water.uses_left} uses")
    print(f"Created {prey.resource_type.value}: {prey.quantity} units, {prey.uses_left} uses")
    
    # Simulate consumption
    print("\nSimulating consumption...")
    for i in range(3):
        if not plant.is_depleted():
            gained = plant.consume()
            print(f"Consumed {plant.resource_type.value}: gained {gained} units, {plant.uses_left} uses left")
        else:
            print(f"{plant.resource_type.value} is depleted!")
    
    print()

def demonstrate_world_system():
    """Demonstrate the world system."""
    print("🌍 World System Demonstration")
    print("=" * 40)
    
    # Create a small test world
    print("Creating a 5x5 test world...")
    grid = []
    for y in range(5):
        row = []
        for x in range(5):
            # Create different terrain types
            if x == 0 or y == 0 or x == 4 or y == 4:
                terrain = TerrainType.MOUNTAINS
            elif x == 2 and y == 2:
                terrain = TerrainType.WATER
            elif (x + y) % 2 == 0:
                terrain = TerrainType.FOREST
            else:
                terrain = TerrainType.PLAINS
            
            tile = Tile((x, y), terrain)
            row.append(tile)
        grid.append(row)
    
    world = World(grid, (5, 5))
    print(f"World created: {world.dimensions[0]}x{world.dimensions[1]}")
    
    # Show terrain distribution
    terrain_counts = {}
    for y in range(5):
        for x in range(5):
            tile = world.get_tile(x, y)
            terrain = tile.terrain_type.value
            terrain_counts[terrain] = terrain_counts.get(terrain, 0) + 1
    
    print("Terrain distribution:")
    for terrain, count in terrain_counts.items():
        print(f"  {terrain}: {count} tiles")
    
    # Test coordinate validation
    print(f"\nValid coordinates (0,0): {world.is_valid_coordinate(0, 0)}")
    print(f"Valid coordinates (4,4): {world.is_valid_coordinate(4, 4)}")
    print(f"Valid coordinates (5,5): {world.is_valid_coordinate(5, 5)}")
    print(f"Valid coordinates (-1,0): {world.is_valid_coordinate(-1, 0)}")
    
    # Test adjacent tiles
    adjacent = world.get_adjacent_tiles(2, 2)
    print(f"Adjacent tiles to (2,2): {len(adjacent)}")
    for tile in adjacent:
        print(f"  {tile.coordinates}: {tile.terrain_type.value}")
    
    print()

def demonstrate_animal_system():
    """Demonstrate the animal system."""
    print("🐾 Animal System Demonstration")
    print("=" * 40)
    
    # Create animals of different categories
    animals = []
    for i, category in enumerate(AnimalCategory):
        animal = create_random_animal(f"demo_{i:03d}", category)
        animals.append(animal)
        print(f"Created {category.value}:")
        print(f"  Traits: {animal.traits}")
        print(f"  Max Health: {animal.get_max_health()}")
        print(f"  Max Energy: {animal.get_max_energy()}")
        print(f"  Passive: {animal.passive}")
        print()
    
    # Demonstrate trait differences
    print("Trait comparison:")
    print("Category    STR  AGI  INT  END  PER")
    print("-" * 35)
    for animal in animals:
        traits_str = "  ".join(f"{animal.traits[trait]:3d}" for trait in constants.TRAIT_NAMES)
        print(f"{animal.category.value:10s} {traits_str}")
    
    print()

def demonstrate_simulation_system():
    """Demonstrate the simulation system."""
    print("🎮 Simulation System Demonstration")
    print("=" * 40)
    
    # Create a simulation
    sim = Simulation()
    print(f"Created simulation at week {sim.current_week}")
    
    # Add some animals
    for i in range(5):
        category = list(AnimalCategory)[i % 3]
        animal = create_random_animal(f"sim_{i:03d}", category)
        sim.add_animal(animal)
    
    print(f"Added {len(sim.population)} animals to simulation")
    
    # Show population breakdown
    living = sim.get_living_animals()
    dead = sim.get_dead_animals()
    print(f"Living animals: {len(living)}")
    print(f"Dead animals: {len(dead)}")
    
    # Simulate some time passing
    print("\nSimulating 3 weeks...")
    for week in range(3):
        sim.advance_week()
        print(f"Week {sim.current_week}: {len(sim.get_living_animals())} living animals")
    
    # Demonstrate animal removal
    if sim.population:
        animal_to_remove = sim.population[0]
        print(f"\nRemoving animal {animal_to_remove.animal_id}")
        sim.remove_animal(animal_to_remove)
        print(f"Population: {len(sim.population)}, Graveyard: {len(sim.graveyard)}")
    
    print()

def demonstrate_fitness_system():
    """Demonstrate the fitness system."""
    print("🏆 Fitness System Demonstration")
    print("=" * 40)
    
    # Create an animal and simulate some performance
    animal = create_random_animal("fitness_demo", AnimalCategory.CARNIVORE)
    
    # Simulate some performance
    animal.fitness_score_components = {
        'Time': 100,      # 100 turns survived
        'Resource': 200,  # 200 units of resources (5 * 40)
        'Kill': 2,        # 2 kills
        'Distance': 50,   # 50 tiles traveled
        'Event': 3        # 3 events survived
    }
    
    # Calculate fitness score
    fitness_score = animal.get_fitness_score()
    
    print(f"Animal performance:")
    for component, value in animal.fitness_score_components.items():
        weight = constants.FITNESS_WEIGHTS[component]
        if component == 'Resource':
            contribution = (value / 40) * weight
            print(f"  {component}: {value} units (contribution: {contribution:.1f})")
        else:
            contribution = value * weight
            print(f"  {component}: {value} (contribution: {contribution:.1f})")
    
    print(f"\nTotal fitness score: {fitness_score:.1f}")
    print()

def main():
    """Run all demonstrations."""
    print("🎮 EvoSim Data Structures Usage Examples\n")
    
    # Validate data structures first
    print("🔍 Validating data structures...")
    data_structures.validate_data_structures()
    print()
    
    # Run demonstrations
    demonstrate_effect_system()
    demonstrate_resource_system()
    demonstrate_world_system()
    demonstrate_animal_system()
    demonstrate_simulation_system()
    demonstrate_fitness_system()
    
    print("✅ All examples completed successfully!")

if __name__ == "__main__":
    main()
