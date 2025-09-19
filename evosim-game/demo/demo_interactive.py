#!/usr/bin/env python3
"""
EvoSim Interactive Demo

This interactive demo allows you to explore the EvoSim system hands-on.
You can create worlds, customize animals, and see the results in real-time.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import constants
from data_structures import *
from world_generator import *
from animal_creator import *

def print_menu():
    """Print the main menu."""
    print("\n" + "="*60)
    print("🎮 EVOSIM INTERACTIVE DEMO")
    print("="*60)
    print("1. Create a custom world")
    print("2. Create and customize animals")
    print("3. Generate a complete scenario")
    print("4. Test animal training system")
    print("5. Explore world generation options")
    print("6. Run performance tests")
    print("7. View system information")
    print("0. Exit")
    print("="*60)

def create_custom_world():
    """Interactive world creation."""
    print("\n🌍 CUSTOM WORLD CREATION")
    print("-" * 40)
    
    try:
        # Get world parameters
        width = int(input("Enter world width (5-50): ") or "15")
        height = int(input("Enter world height (5-50): ") or "10")
        population = int(input("Enter population size (1-50): ") or "5")
        
        # Validate inputs
        width = max(5, min(50, width))
        height = max(5, min(50, height))
        population = max(1, min(50, population))
        
        # Ask about mountain borders
        mountain_border = input("Add mountain borders? (y/n): ").lower().startswith('y')
        
        print(f"\nCreating {width}x{height} world with {population} animals...")
        
        # Create world
        config = GenerationConfig(
            width=width, 
            height=height, 
            population_size=population,
            mountain_border=mountain_border
        )
        generator = WorldGenerator(config)
        world = generator.generate_world(seed=42)
        
        print(f"✅ World created successfully!")
        print(f"Dimensions: {world.dimensions}")
        
        # Show world
        WorldValidator.visualize_world(world, show_resources=True, show_animals=False)
        
        # Show statistics
        stats = WorldValidator.validate_world(world)
        print(f"\n📊 World Statistics:")
        print(f"Total Tiles: {stats['total_tiles']}")
        print(f"Terrain: {stats['terrain_counts']}")
        print(f"Resources: {stats['resource_counts']}")
        print(f"Valid Spawn Locations: {stats['valid_spawn_locations']}")
        
        return world
        
    except ValueError as e:
        print(f"❌ Invalid input: {e}")
        return None
    except Exception as e:
        print(f"❌ Error creating world: {e}")
        return None

def create_custom_animals():
    """Interactive animal creation."""
    print("\n🐾 CUSTOM ANIMAL CREATION")
    print("-" * 40)
    
    try:
        # Get number of animals
        num_animals = int(input("How many animals to create? (1-10): ") or "3")
        num_animals = max(1, min(10, num_animals))
        
        creator = AnimalCreator(seed=42)
        animals = []
        
        for i in range(num_animals):
            print(f"\n--- Animal {i+1} ---")
            
            # Choose category
            print("Choose animal category:")
            print("1. Herbivore (AGI primary)")
            print("2. Carnivore (STR primary)")
            print("3. Omnivore (END primary)")
            
            choice = input("Enter choice (1-3): ") or "1"
            category_map = {"1": AnimalCategory.HERBIVORE, "2": AnimalCategory.CARNIVORE, "3": AnimalCategory.OMNIVORE}
            category = category_map.get(choice, AnimalCategory.HERBIVORE)
            
            # Choose creation method
            print("\nChoose creation method:")
            print("1. Random with training")
            print("2. Custom traits")
            print("3. Specialized")
            
            method = input("Enter choice (1-3): ") or "1"
            
            if method == "1":
                # Training system
                print("\nTraining Questions (choose 0-3 for each):")
                choices = []
                questions = creator.get_training_questions()
                
                for j, (question_type, question_data) in enumerate(questions.items()):
                    print(f"\n{j+1}. {question_data.question}")
                    for k, option in enumerate(question_data.options):
                        print(f"   {k}. {option.text} (+{option.trait_bonus})")
                    
                    choice = input(f"Choice for question {j+1} (0-3): ") or "0"
                    try:
                        choices.append(int(choice))
                    except ValueError:
                        choices.append(0)
                
                animal = creator.create_animal_with_training(f"custom_{i+1}", category, choices)
                
            elif method == "2":
                # Custom traits
                print("\nEnter custom traits (4-9 for each):")
                traits = {}
                for trait in constants.TRAIT_NAMES:
                    value = input(f"{trait} (4-9): ") or "5"
                    try:
                        traits[trait] = max(4, min(9, int(value)))
                    except ValueError:
                        traits[trait] = 5
                
                animal = creator.create_animal_with_custom_traits(f"custom_{i+1}", category, traits)
                
            else:
                # Specialized
                print("\nChoose specialization trait:")
                for j, trait in enumerate(constants.TRAIT_NAMES):
                    print(f"{j+1}. {trait}")
                
                trait_choice = input("Enter choice (1-5): ") or "1"
                try:
                    trait_idx = int(trait_choice) - 1
                    specialization_trait = constants.TRAIT_NAMES[trait_idx]
                except (ValueError, IndexError):
                    specialization_trait = constants.TRAIT_NAMES[0]
                
                level = input(f"Specialization level for {specialization_trait} (7-9): ") or "9"
                try:
                    level = max(7, min(9, int(level)))
                except ValueError:
                    level = 9
                
                customizer = AnimalCustomizer(seed=42)
                animal = customizer.create_specialized_animal(f"custom_{i+1}", category, specialization_trait, level)
            
            animals.append(animal)
            
            # Show animal details
            analysis = creator.analyze_animal_traits(animal)
            print(f"\n✅ Animal created:")
            print(f"   Category: {animal.category.value}")
            print(f"   Traits: {animal.traits}")
            print(f"   Primary: {analysis['primary_trait']} ({analysis['primary_value']})")
            print(f"   Health: {analysis['max_health']}, Energy: {analysis['max_energy']}")
        
        return animals
        
    except Exception as e:
        print(f"❌ Error creating animals: {e}")
        return None

def generate_complete_scenario():
    """Generate a complete scenario with world and animals."""
    print("\n🎬 COMPLETE SCENARIO GENERATION")
    print("-" * 40)
    
    try:
        # Create world
        print("Creating world...")
        config = GenerationConfig(width=12, height=8, population_size=6, mountain_border=True)
        generator = WorldGenerator(config)
        world = generator.generate_world(seed=42)
        print(f"✅ World created: {world.dimensions}")
        
        # Create animals
        print("Creating animals...")
        creator = AnimalCreator(seed=42)
        training_choices = [
            [0, 1, 2, 3, 4],  # Balanced
            [1, 1, 1, 1, 1],  # Strength
            [2, 2, 2, 2, 2],  # Intelligence
            [0, 0, 0, 0, 0],  # Agility
            [3, 3, 3, 3, 3],  # Endurance
            [0, 1, 2, 3, 0]   # Mixed
        ]
        animals = creator.create_population_with_training(6, training_choices)
        print(f"✅ {len(animals)} animals created")
        
        # Place animals in world
        print("Placing animals in world...")
        valid_tiles = []
        for y in range(world.dimensions[1]):
            for x in range(world.dimensions[0]):
                tile = world.get_tile(x, y)
                if tile.is_passable() and not tile.is_occupied():
                    valid_tiles.append((x, y))
        
        for i, animal in enumerate(animals):
            if i < len(valid_tiles):
                x, y = valid_tiles[i]
                animal.location = (x, y)
                world.get_tile(x, y).occupant = animal
        
        print(f"✅ {len(animals)} animals placed")
        
        # Show final world
        print("\n🗺️  Final Scenario:")
        WorldValidator.visualize_world(world, show_resources=True, show_animals=True)
        
        # Show animal details
        print("\n🐾 Animal Details:")
        for i, animal in enumerate(animals):
            analysis = creator.analyze_animal_traits(animal)
            print(f"   {i+1}. {animal.category.value}: {animal.traits} - {analysis['specialization']} specialization")
        
        return world, animals
        
    except Exception as e:
        print(f"❌ Error generating scenario: {e}")
        return None, None

def test_training_system():
    """Test the training system interactively."""
    print("\n🎓 TRAINING SYSTEM TEST")
    print("-" * 40)
    
    creator = AnimalCreator(seed=42)
    questions = creator.get_training_questions()
    
    print("Answer the training questions to create your animal:")
    print("(Choose 0-3 for each question)\n")
    
    choices = []
    for i, (question_type, question_data) in enumerate(questions.items()):
        print(f"Question {i+1}: {question_data.question}")
        for j, option in enumerate(question_data.options):
            print(f"  {j}. {option.text} (+{option.trait_bonus})")
        
        while True:
            try:
                choice = int(input(f"Your choice (0-3): "))
                if 0 <= choice <= 3:
                    choices.append(choice)
                    break
                else:
                    print("Please enter 0, 1, 2, or 3")
            except ValueError:
                print("Please enter a number")
    
    # Create animal with choices
    animal = creator.create_animal_with_training("trained_animal", AnimalCategory.HERBIVORE, choices)
    analysis = creator.analyze_animal_traits(animal)
    
    print(f"\n✅ Your trained animal:")
    print(f"   Traits: {animal.traits}")
    print(f"   Primary: {analysis['primary_trait']} ({analysis['primary_value']})")
    print(f"   Specialization: {analysis['specialization']}")
    print(f"   Health: {analysis['max_health']}, Energy: {analysis['max_energy']}")
    
    # Show what each choice did
    print(f"\n📊 Training Analysis:")
    trait_bonuses = creator._calculate_training_bonuses(choices)
    for trait, bonus in trait_bonuses.items():
        if bonus > 0:
            print(f"   {trait}: +{bonus} from training")

def explore_world_options():
    """Explore different world generation options."""
    print("\n🌍 WORLD GENERATION OPTIONS")
    print("-" * 40)
    
    print("Testing different world configurations...")
    
    configs = [
        ("Small World", GenerationConfig(width=6, height=4, population_size=2, mountain_border=True)),
        ("Medium World", GenerationConfig(width=15, height=10, population_size=8, mountain_border=True)),
        ("Large World", GenerationConfig(width=25, height=20, population_size=20, mountain_border=True)),
        ("No Borders", GenerationConfig(width=10, height=8, population_size=5, mountain_border=False)),
    ]
    
    for name, config in configs:
        print(f"\n{name}:")
        generator = WorldGenerator(config)
        world = generator.generate_world(seed=42)
        stats = WorldValidator.validate_world(world)
        
        print(f"   Size: {world.dimensions}")
        print(f"   Terrain: {stats['terrain_counts']}")
        print(f"   Resources: {stats['resource_counts']}")
        print(f"   Spawn Locations: {stats['valid_spawn_locations']}")

def run_performance_tests():
    """Run performance tests."""
    print("\n⚡ PERFORMANCE TESTS")
    print("-" * 40)
    
    import time
    
    # World generation tests
    print("World Generation Performance:")
    sizes = [(10, 10), (20, 20), (30, 30), (50, 50)]
    populations = [10, 25, 50, 100]
    
    for (width, height), pop_size in zip(sizes, populations):
        config = GenerationConfig(width=width, height=height, population_size=pop_size)
        generator = WorldGenerator(config)
        
        start_time = time.time()
        world = generator.generate_world(seed=42)
        generation_time = time.time() - start_time
        
        print(f"   {width}x{height}, {pop_size} animals: {generation_time:.3f}s")
    
    # Animal creation tests
    print("\nAnimal Creation Performance:")
    creator = AnimalCreator(seed=42)
    sizes = [10, 50, 100, 500, 1000]
    
    for size in sizes:
        start_time = time.time()
        animals = creator.create_diverse_population(size, diversity_factor=0.5)
        creation_time = time.time() - start_time
        
        print(f"   {size} animals: {creation_time:.3f}s")

def view_system_info():
    """View system information."""
    print("\n📊 SYSTEM INFORMATION")
    print("-" * 40)
    
    print("🔧 Configuration:")
    print(f"   World Size: {constants.GRID_WIDTH}x{constants.GRID_HEIGHT}")
    print(f"   Population: {constants.POPULATION_SIZE}")
    print(f"   Terrain Distribution: {constants.TERRAIN_DISTRIBUTION}")
    
    print("\n🎯 Animal Parameters:")
    print(f"   Trait Ranges: {constants.STANDARD_TRAIT_MIN}-{constants.STANDARD_TRAIT_MAX} (standard)")
    print(f"   Primary Ranges: {constants.PRIMARY_TRAIT_MIN}-{constants.PRIMARY_TRAIT_MAX} (primary)")
    print(f"   Base Health: {constants.BASE_HEALTH} + (END × {constants.HEALTH_PER_ENDURANCE})")
    print(f"   Base Energy: {constants.BASE_ENERGY} + (END × {constants.ENERGY_PER_ENDURANCE})")
    
    print("\n⚔️ Combat & Actions:")
    print(f"   Movement Cost: {constants.MOVEMENT_BASE_COST} base")
    print(f"   Strength Damage: ×{constants.STRENGTH_DAMAGE_MULTIPLIER}")
    print(f"   Agility Evasion: ×{constants.AGILITY_EVASION_MULTIPLIER}")
    
    print("\n📁 Available Components:")
    print("   • Constants & Configuration")
    print("   • Data Structures (Effect, Resource, Tile, World, Animal, Simulation)")
    print("   • World Generator (Terrain, Resources, Animals)")
    print("   • Animal Creator (Training, Customization, Analysis)")
    print("   • Comprehensive Test Suite")

def main():
    """Main interactive loop."""
    print("🎮 Welcome to EvoSim Interactive Demo!")
    print("Explore the foundational components of our evolution simulation.")
    
    while True:
        print_menu()
        choice = input("\nEnter your choice (0-7): ").strip()
        
        if choice == "0":
            print("\n👋 Thanks for exploring EvoSim! Goodbye!")
            break
        elif choice == "1":
            create_custom_world()
        elif choice == "2":
            create_custom_animals()
        elif choice == "3":
            generate_complete_scenario()
        elif choice == "4":
            test_training_system()
        elif choice == "5":
            explore_world_options()
        elif choice == "6":
            run_performance_tests()
        elif choice == "7":
            view_system_info()
        else:
            print("❌ Invalid choice. Please enter 0-7.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
