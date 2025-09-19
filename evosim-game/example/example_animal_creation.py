#!/usr/bin/env python3
"""
Example usage of animal_creator.py

This script demonstrates the animal creation and customization features.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import animal_creator
from animal_creator import *
import constants
from data_structures import *

def demonstrate_basic_animal_creation():
    """Demonstrate basic animal creation."""
    print("🐾 Basic Animal Creation")
    print("=" * 40)
    
    creator = AnimalCreator(seed=42)
    
    # Create animals of each category
    for category in AnimalCategory:
        animal = creator.create_animal_with_training(f"basic_{category.value.lower()}", category, [0, 1, 2, 3, 4])
        print(f"\n{category.value}:")
        print(f"  Traits: {animal.traits}")
        print(f"  Health: {animal.status['Health']:.0f}/{animal.get_max_health()}")
        print(f"  Energy: {animal.status['Energy']:.0f}/{animal.get_max_energy()}")
        print(f"  Passive: {animal.passive}")
    
    print()

def demonstrate_training_system():
    """Demonstrate the training system."""
    print("🎓 Training System")
    print("=" * 40)
    
    creator = AnimalCreator(seed=42)
    questions = creator.get_training_questions()
    
    print("Training Questions:")
    for i, (question_type, question_data) in enumerate(questions.items()):
        print(f"\n{i+1}. {question_data.question}")
        for j, option in enumerate(question_data.options):
            print(f"   {j+1}. {option.text} (+{option.trait_bonus}) - {option.description}")
    
    print("\nExample Training Choices: [0, 1, 2, 3, 4]")
    animal = creator.create_animal_with_training("trained_001", AnimalCategory.HERBIVORE, [0, 1, 2, 3, 4])
    print(f"Resulting traits: {animal.traits}")
    
    print()

def demonstrate_custom_traits():
    """Demonstrate custom trait creation."""
    print("⚙️ Custom Trait Creation")
    print("=" * 40)
    
    creator = AnimalCreator(seed=42)
    
    # Create a custom animal
    custom_traits = {
        'STR': 9,  # High strength
        'AGI': 4,  # Low agility
        'INT': 6,  # Medium intelligence
        'END': 8,  # High endurance
        'PER': 3   # Low perception
    }
    
    animal = creator.create_animal_with_custom_traits("custom_001", AnimalCategory.CARNIVORE, custom_traits)
    print(f"Custom Carnivore:")
    print(f"  Traits: {animal.traits}")
    print(f"  Health: {animal.status['Health']:.0f}/{animal.get_max_health()}")
    print(f"  Energy: {animal.status['Energy']:.0f}/{animal.get_max_energy()}")
    
    # Analyze the animal
    analysis = creator.analyze_animal_traits(animal)
    print(f"\nAnalysis:")
    print(f"  Total traits: {analysis['total_traits']}")
    print(f"  Primary trait: {analysis['primary_trait']} ({analysis['primary_value']})")
    print(f"  Specialization: {analysis['specialization']}")
    print(f"  Trait balance: {analysis['trait_balance']}")
    
    print()

def demonstrate_population_creation():
    """Demonstrate population creation."""
    print("👥 Population Creation")
    print("=" * 40)
    
    creator = AnimalCreator(seed=42)
    
    # Create diverse training choices
    training_choices = [
        [0, 0, 0, 0, 0],  # All AGI focus
        [1, 1, 1, 1, 1],  # All STR focus
        [2, 2, 2, 2, 2],  # All INT focus
        [3, 3, 3, 3, 3],  # All END focus
        [0, 1, 2, 3, 0],  # Mixed
        [1, 2, 3, 0, 1]   # Mixed
    ]
    
    animals = creator.create_population_with_training(6, training_choices)
    
    print("Population with Training:")
    for i, animal in enumerate(animals):
        print(f"  {animal.animal_id} ({animal.category.value}): {animal.traits}")
    
    # Create diverse population
    diverse_animals = creator.create_diverse_population(4, diversity_factor=0.8)
    
    print("\nDiverse Population:")
    for animal in diverse_animals:
        print(f"  {animal.animal_id} ({animal.category.value}): {animal.traits}")
    
    print()

def demonstrate_animal_customizer():
    """Demonstrate the animal customizer."""
    print("🔧 Animal Customizer")
    print("=" * 40)
    
    customizer = AnimalCustomizer(seed=42)
    
    # Test optimization
    print("Optimization:")
    animal = create_random_animal("original", AnimalCategory.HERBIVORE)
    print(f"  Original: {animal.traits}")
    
    optimized = customizer.optimize_animal_for_category(animal)
    print(f"  Optimized: {optimized.traits}")
    
    # Test balanced creation
    print("\nBalanced Animal:")
    balanced = customizer.create_balanced_animal("balanced", AnimalCategory.CARNIVORE, target_total=30)
    print(f"  Traits: {balanced.traits}")
    print(f"  Total: {sum(balanced.traits.values())}")
    
    # Test specialized creation
    print("\nSpecialized Animals:")
    for trait in constants.TRAIT_NAMES:
        specialized = customizer.create_specialized_animal(f"spec_{trait.lower()}", AnimalCategory.OMNIVORE, trait, 9)
        print(f"  {trait} specialist: {specialized.traits}")
    
    print()

def demonstrate_trait_analysis():
    """Demonstrate trait analysis."""
    print("📊 Trait Analysis")
    print("=" * 40)
    
    creator = AnimalCreator(seed=42)
    
    # Create different types of animals
    animals = [
        creator.create_animal_with_training("balanced_001", AnimalCategory.HERBIVORE, [0, 1, 2, 3, 4]),
        creator.create_animal_with_training("agile_001", AnimalCategory.HERBIVORE, [0, 0, 0, 0, 0]),
        creator.create_animal_with_training("strong_001", AnimalCategory.CARNIVORE, [1, 1, 1, 1, 1]),
        creator.create_animal_with_training("smart_001", AnimalCategory.OMNIVORE, [2, 2, 2, 2, 2])
    ]
    
    for animal in animals:
        analysis = creator.analyze_animal_traits(animal)
        print(f"\n{animal.animal_id} ({animal.category.value}):")
        print(f"  Traits: {animal.traits}")
        print(f"  Primary: {analysis['primary_trait']} ({analysis['primary_value']})")
        print(f"  Specialization: {analysis['specialization']}")
        print(f"  Balance: {analysis['trait_balance']}")
        print(f"  Health: {analysis['max_health']}")
        print(f"  Energy: {analysis['max_energy']}")
    
    print()

def demonstrate_training_impact():
    """Demonstrate the impact of training choices."""
    print("🎯 Training Impact Analysis")
    print("=" * 40)
    
    creator = AnimalCreator(seed=42)
    
    # Create same animal with different training choices
    base_animal = create_random_animal("base", AnimalCategory.HERBIVORE)
    print(f"Base animal (no training): {base_animal.traits}")
    
    # Test different training strategies
    strategies = [
        ("All AGI", [0, 0, 0, 0, 0]),
        ("All STR", [1, 1, 1, 1, 1]),
        ("All INT", [2, 2, 2, 2, 2]),
        ("All END", [3, 3, 3, 3, 3]),
        ("Balanced", [0, 1, 2, 3, 0])
    ]
    
    for strategy_name, choices in strategies:
        animal = creator.create_animal_with_training(f"strategy_{strategy_name.lower()}", AnimalCategory.HERBIVORE, choices)
        analysis = creator.analyze_animal_traits(animal)
        
        print(f"\n{strategy_name} strategy:")
        print(f"  Traits: {animal.traits}")
        print(f"  Primary: {analysis['primary_trait']} ({analysis['primary_value']})")
        print(f"  Total: {analysis['total_traits']}")
    
    print()

def demonstrate_category_optimization():
    """Demonstrate category-specific optimization."""
    print("🏆 Category Optimization")
    print("=" * 40)
    
    customizer = AnimalCustomizer(seed=42)
    
    for category in AnimalCategory:
        # Create random animal
        random_animal = create_random_animal(f"random_{category.value.lower()}", category)
        
        # Optimize for category
        optimized_animal = customizer.optimize_animal_for_category(random_animal)
        
        primary_trait = constants.CATEGORY_PRIMARY_TRAITS[category.value]
        
        print(f"\n{category.value}:")
        print(f"  Random: {random_animal.traits}")
        print(f"  Optimized: {optimized_animal.traits}")
        print(f"  Primary trait ({primary_trait}): {optimized_animal.traits[primary_trait]}")
        print(f"  Health: {optimized_animal.get_max_health()}")
        print(f"  Energy: {optimized_animal.get_max_energy()}")
    
    print()

def demonstrate_effective_traits():
    """Demonstrate effective trait calculation with effects."""
    print("⚡ Effective Traits with Effects")
    print("=" * 40)
    
    creator = AnimalCreator(seed=42)
    animal = creator.create_animal_with_training("effective_001", AnimalCategory.CARNIVORE, [1, 1, 1, 1, 1])
    
    print(f"Base traits: {animal.traits}")
    print(f"Effective traits: {animal.get_effective_trait('STR')} STR, {animal.get_effective_trait('AGI')} AGI")
    
    # Add some effects
    well_fed = create_effect(EffectType.WELL_FED)
    animal.add_effect(well_fed)
    
    print(f"With Well-Fed effect: {animal.get_effective_trait('STR')} STR, {animal.get_effective_trait('AGI')} AGI")
    
    # Add more effects
    injured = create_effect(EffectType.INJURED)
    animal.add_effect(injured)
    
    print(f"With Well-Fed + Injured: {animal.get_effective_trait('STR')} STR, {animal.get_effective_trait('AGI')} AGI")
    
    print()

def main():
    """Run all demonstrations."""
    print("🎮 EvoSim Animal Creation Examples\n")
    
    demonstrate_basic_animal_creation()
    demonstrate_training_system()
    demonstrate_custom_traits()
    demonstrate_population_creation()
    demonstrate_animal_customizer()
    demonstrate_trait_analysis()
    demonstrate_training_impact()
    demonstrate_category_optimization()
    demonstrate_effective_traits()
    
    print("✅ All animal creation examples completed successfully!")

if __name__ == "__main__":
    main()
