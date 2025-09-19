#!/usr/bin/env python3
"""
Example usage of constants.py

This script demonstrates how to use the constants file for various game calculations.
"""

import constants

def demonstrate_world_generation():
    """Demonstrate world generation constants."""
    print("🌍 World Generation Constants")
    print(f"Grid size: {constants.GRID_WIDTH}x{constants.GRID_HEIGHT}")
    print(f"Total tiles: {constants.GRID_WIDTH * constants.GRID_HEIGHT}")
    print(f"Terrain distribution: {constants.TERRAIN_DISTRIBUTION}")
    print(f"Food spawn chance: {constants.FOOD_SPAWN_CHANCE * 100}%")
    print(f"Water spawn chance: {constants.WATER_SPAWN_CHANCE * 100}%")
    print()

def demonstrate_animal_parameters():
    """Demonstrate animal parameter constants."""
    print("🐾 Animal Parameters")
    print(f"Standard trait range: {constants.STANDARD_TRAIT_MIN}-{constants.STANDARD_TRAIT_MAX}")
    print(f"Primary trait range: {constants.PRIMARY_TRAIT_MIN}-{constants.PRIMARY_TRAIT_MAX}")
    print(f"Base health: {constants.BASE_HEALTH}")
    print(f"Health per endurance: {constants.HEALTH_PER_ENDURANCE}")
    print(f"Initial training points: {constants.INITIAL_TRAINING_POINTS}")
    print()

def demonstrate_fitness_calculation():
    """Demonstrate fitness calculation constants."""
    print("📊 Fitness Calculation")
    print("Fitness weights:")
    for component, weight in constants.FITNESS_WEIGHTS.items():
        print(f"  {component}: {weight}")
    print()

def demonstrate_combat_mechanics():
    """Demonstrate combat mechanics constants."""
    print("⚔️ Combat Mechanics")
    print(f"Strength damage multiplier: {constants.STRENGTH_DAMAGE_MULTIPLIER}")
    print(f"Agility evasion multiplier: {constants.AGILITY_EVASION_MULTIPLIER}")
    print(f"Ambush predator multiplier: {constants.AMBUSH_PREDATOR_MULTIPLIER}")
    print()

def demonstrate_events():
    """Demonstrate event constants."""
    print("🎲 Events & Disasters")
    print(f"Triggered events: {len(constants.TRIGGERED_EVENTS)}")
    print(f"Random events: {len(constants.RANDOM_EVENTS)}")
    print(f"Disasters: {len(constants.DISASTERS)}")
    print(f"Rockslide escape DC: {constants.ROCKSLIDE_ESCAPE_DC}")
    print(f"Wildfire damage: {constants.WILDFIRE_DAMAGE}")
    print()

def demonstrate_mlp_architecture():
    """Demonstrate MLP architecture constants."""
    print("🧠 MLP Architecture")
    print(f"Input nodes: {constants.INPUT_NODES}")
    print(f"Hidden layer 1: {constants.HIDDEN_LAYER_1_NODES}")
    print(f"Hidden layer 2: {constants.HIDDEN_LAYER_2_NODES}")
    print(f"Output nodes: {constants.OUTPUT_NODES}")
    print(f"Available actions: {len(constants.ACTIONS)}")
    print()

def calculate_example_animal_stats():
    """Calculate example animal stats using constants."""
    print("📈 Example Animal Stats Calculation")
    
    # Example: Herbivore with endurance 8
    endurance = 8
    max_health = constants.BASE_HEALTH + (endurance * constants.HEALTH_PER_ENDURANCE)
    max_energy = constants.BASE_ENERGY + (endurance * constants.ENERGY_PER_ENDURANCE)
    
    print(f"Herbivore with {endurance} endurance:")
    print(f"  Max Health: {max_health}")
    print(f"  Max Energy: {max_energy}")
    print()

def calculate_example_fitness():
    """Calculate example fitness score using constants."""
    print("🏆 Example Fitness Score Calculation")
    
    # Example animal performance
    time_survived = 100
    resources_gathered = 200  # 5 * 40 units
    kills = 2
    distance_traveled = 50
    events_survived = 3
    
    # Calculate fitness using weights
    fitness = (
        time_survived * constants.FITNESS_WEIGHTS['Time'] +
        (resources_gathered / 40) * constants.FITNESS_WEIGHTS['Resource'] +
        kills * constants.FITNESS_WEIGHTS['Kill'] +
        distance_traveled * constants.FITNESS_WEIGHTS['Distance'] +
        events_survived * constants.FITNESS_WEIGHTS['Event']
    )
    
    print(f"Animal performance:")
    print(f"  Time survived: {time_survived}")
    print(f"  Resources gathered: {resources_gathered}")
    print(f"  Kills: {kills}")
    print(f"  Distance traveled: {distance_traveled}")
    print(f"  Events survived: {events_survived}")
    print(f"  Total fitness score: {fitness}")
    print()

def main():
    """Run all demonstrations."""
    print("🎮 EvoSim Constants Usage Examples\n")
    
    # Validate constants first
    print("🔍 Validating constants...")
    constants.validate_constants()
    print()
    
    # Run demonstrations
    demonstrate_world_generation()
    demonstrate_animal_parameters()
    demonstrate_fitness_calculation()
    demonstrate_combat_mechanics()
    demonstrate_events()
    demonstrate_mlp_architecture()
    calculate_example_animal_stats()
    calculate_example_fitness()
    
    print("✅ All examples completed successfully!")

if __name__ == "__main__":
    main()
