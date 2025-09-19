#!/usr/bin/env python3
"""
Test script for animal_creator.py

This script validates that animal creation and customization work correctly.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import animal_creator
from animal_creator import *
import constants
from data_structures import *

def test_animal_creator_creation():
    """Test AnimalCreator class creation."""
    print("Testing AnimalCreator creation...")
    
    creator = AnimalCreator(seed=42)
    assert creator is not None
    assert len(creator.training_questions) == 5  # 5 training questions
    
    print("✅ AnimalCreator creation tests passed!")

def test_training_questions():
    """Test training questions structure."""
    print("Testing training questions...")
    
    creator = AnimalCreator()
    questions = creator.get_training_questions()
    
    # Check all question types are present
    expected_questions = [
        TrainingQuestion.HUNTING_STYLE,
        TrainingQuestion.SURVIVAL_PRIORITY,
        TrainingQuestion.ENVIRONMENT_PREFERENCE,
        TrainingQuestion.COMBAT_APPROACH,
        TrainingQuestion.RESOURCE_STRATEGY
    ]
    
    for question_type in expected_questions:
        assert question_type in questions
        question_data = questions[question_type]
        assert len(question_data.options) == 4  # 4 options per question
        assert question_data.question is not None
        assert len(question_data.question) > 0
        
        # Check each option has required fields
        for option in question_data.options:
            assert option.text is not None
            assert option.trait_bonus in constants.TRAIT_NAMES
            assert option.description is not None
    
    print("✅ Training questions tests passed!")

def test_animal_creation_with_training():
    """Test animal creation with training choices."""
    print("Testing animal creation with training...")
    
    creator = AnimalCreator(seed=42)
    
    # Test with valid training choices
    training_choices = [0, 1, 2, 3, 4]
    animal = creator.create_animal_with_training("test_001", AnimalCategory.HERBIVORE, training_choices)
    
    assert animal.animal_id == "test_001"
    assert animal.category == AnimalCategory.HERBIVORE
    assert animal.is_alive()
    
    # Check that traits are within valid ranges
    for trait in constants.TRAIT_NAMES:
        assert constants.STANDARD_TRAIT_MIN <= animal.traits[trait] <= constants.PRIMARY_TRAIT_MAX
    
    # Test with invalid number of choices
    try:
        creator.create_animal_with_training("test_002", AnimalCategory.CARNIVORE, [0, 1])
        assert False, "Should have raised ValueError for invalid number of choices"
    except ValueError:
        pass
    
    print("✅ Animal creation with training tests passed!")

def test_trait_bonus_calculation():
    """Test trait bonus calculation from training choices."""
    print("Testing trait bonus calculation...")
    
    creator = AnimalCreator(seed=42)
    
    # Test specific training choices
    training_choices = [0, 0, 0, 0, 0]  # All first options
    bonuses = creator._calculate_training_bonuses(training_choices)
    
    # Check that bonuses are calculated correctly
    assert sum(bonuses.values()) == 5  # 5 total bonuses
    assert bonuses['AGI'] >= 0  # Should have some AGI bonuses
    
    # Test different choices
    training_choices = [1, 1, 1, 1, 1]  # All second options
    bonuses = creator._calculate_training_bonuses(training_choices)
    assert sum(bonuses.values()) == 5
    
    print("✅ Trait bonus calculation tests passed!")

def test_custom_trait_creation():
    """Test animal creation with custom traits."""
    print("Testing custom trait creation...")
    
    creator = AnimalCreator(seed=42)
    
    # Test valid custom traits
    custom_traits = {
        'STR': 8,
        'AGI': 6,
        'INT': 5,
        'END': 7,
        'PER': 4
    }
    
    animal = creator.create_animal_with_custom_traits("custom_001", AnimalCategory.OMNIVORE, custom_traits)
    assert animal.traits == custom_traits
    assert animal.category == AnimalCategory.OMNIVORE
    
    # Test invalid custom traits
    invalid_traits = {
        'STR': 8,
        'AGI': 6,
        'INT': 5,
        'END': 7,
        'PER': 4,
        'INVALID': 5  # Invalid trait
    }
    
    try:
        creator.create_animal_with_custom_traits("custom_002", AnimalCategory.HERBIVORE, invalid_traits)
        assert False, "Should have raised ValueError for invalid trait"
    except ValueError:
        pass
    
    # Test traits exceeding maximum
    invalid_traits = {
        'STR': 15,  # Exceeds maximum
        'AGI': 6,
        'INT': 5,
        'END': 7,
        'PER': 4
    }
    
    try:
        creator.create_animal_with_custom_traits("custom_003", AnimalCategory.HERBIVORE, invalid_traits)
        assert False, "Should have raised ValueError for trait exceeding maximum"
    except ValueError:
        pass
    
    print("✅ Custom trait creation tests passed!")

def test_population_creation():
    """Test population creation with training."""
    print("Testing population creation...")
    
    creator = AnimalCreator(seed=42)
    
    # Create training choices for 6 animals
    training_choices = [
        [0, 1, 2, 3, 4],
        [1, 2, 3, 4, 0],
        [2, 3, 4, 0, 1],
        [3, 4, 0, 1, 2],
        [4, 0, 1, 2, 3],
        [0, 2, 4, 1, 3]
    ]
    
    animals = creator.create_population_with_training(6, training_choices)
    
    assert len(animals) == 6
    
    # Check that animals are distributed across categories
    categories = [animal.category for animal in animals]
    assert AnimalCategory.HERBIVORE in categories
    assert AnimalCategory.CARNIVORE in categories
    assert AnimalCategory.OMNIVORE in categories
    
    # Test with mismatched training choices
    try:
        creator.create_population_with_training(3, [[0, 1, 2, 3, 4]])
        assert False, "Should have raised ValueError for mismatched training choices"
    except ValueError:
        pass
    
    print("✅ Population creation tests passed!")

def test_diverse_population():
    """Test diverse population creation."""
    print("Testing diverse population creation...")
    
    creator = AnimalCreator(seed=42)
    
    animals = creator.create_diverse_population(10, diversity_factor=0.8)
    
    assert len(animals) == 10
    
    # Check that animals have varied traits
    trait_totals = [sum(animal.traits.values()) for animal in animals]
    assert len(set(trait_totals)) > 1, "All animals should not have identical trait totals"
    
    print("✅ Diverse population creation tests passed!")

def test_animal_analysis():
    """Test animal trait analysis."""
    print("Testing animal analysis...")
    
    creator = AnimalCreator(seed=42)
    
    # Create an animal with known traits
    custom_traits = {
        'STR': 8,
        'AGI': 6,
        'INT': 5,
        'END': 7,
        'PER': 4
    }
    
    animal = creator.create_animal_with_custom_traits("analysis_001", AnimalCategory.CARNIVORE, custom_traits)
    analysis = creator.analyze_animal_traits(animal)
    
    assert analysis['total_traits'] == sum(custom_traits.values())
    assert analysis['primary_trait'] == 'STR'  # Highest trait
    assert analysis['primary_value'] == 8
    assert analysis['specialization'] in ['High', 'Medium', 'Low']
    assert len(analysis['effective_traits']) == 5
    
    print("✅ Animal analysis tests passed!")

def test_animal_customizer():
    """Test AnimalCustomizer class."""
    print("Testing AnimalCustomizer...")
    
    customizer = AnimalCustomizer(seed=42)
    
    # Test optimization
    animal = create_random_animal("opt_001", AnimalCategory.HERBIVORE)
    optimized = customizer.optimize_animal_for_category(animal)
    
    assert optimized.traits['AGI'] == constants.PRIMARY_TRAIT_MAX  # Herbivore primary trait
    assert optimized.category == AnimalCategory.HERBIVORE
    
    # Test balanced animal creation
    balanced = customizer.create_balanced_animal("balanced_001", AnimalCategory.CARNIVORE, target_total=30)
    assert sum(balanced.traits.values()) == 30
    assert balanced.traits['STR'] == constants.PRIMARY_TRAIT_MAX  # Carnivore primary trait
    
    # Test specialized animal creation
    specialized = customizer.create_specialized_animal("spec_001", AnimalCategory.OMNIVORE, "END", 9)
    assert specialized.traits['END'] == 9
    assert sum(specialized.traits.values()) == 30
    
    print("✅ AnimalCustomizer tests passed!")

def test_edge_cases():
    """Test edge cases and error handling."""
    print("Testing edge cases...")
    
    creator = AnimalCreator(seed=42)
    customizer = AnimalCustomizer(seed=42)
    
    # Test invalid specialization trait
    try:
        customizer.create_specialized_animal("invalid_001", AnimalCategory.HERBIVORE, "INVALID", 9)
        assert False, "Should have raised ValueError for invalid trait"
    except ValueError:
        pass
    
    # Test invalid specialization level
    try:
        customizer.create_specialized_animal("invalid_002", AnimalCategory.HERBIVORE, "STR", 15)
        assert False, "Should have raised ValueError for invalid specialization level"
    except ValueError:
        pass
    
    # Test negative trait values
    invalid_traits = {
        'STR': -1,
        'AGI': 6,
        'INT': 5,
        'END': 7,
        'PER': 4
    }
    
    try:
        creator.create_animal_with_custom_traits("invalid_003", AnimalCategory.HERBIVORE, invalid_traits)
        assert False, "Should have raised ValueError for negative trait"
    except ValueError:
        pass
    
    print("✅ Edge cases tests passed!")

def test_trait_validation():
    """Test trait validation and constraints."""
    print("Testing trait validation...")
    
    creator = AnimalCreator(seed=42)
    
    # Test that all created animals have valid traits
    for category in AnimalCategory:
        animal = creator.create_animal_with_training(f"valid_{category.value.lower()}", category, [0, 1, 2, 3, 4])
        
        for trait in constants.TRAIT_NAMES:
            value = animal.traits[trait]
            assert constants.STANDARD_TRAIT_MIN <= value <= constants.PRIMARY_TRAIT_MAX
            assert isinstance(value, int)
        
        # Check that health and energy are calculated correctly
        expected_health = constants.BASE_HEALTH + (animal.traits['END'] * constants.HEALTH_PER_ENDURANCE)
        expected_energy = constants.BASE_ENERGY + (animal.traits['END'] * constants.ENERGY_PER_ENDURANCE)
        
        assert animal.status['Health'] == expected_health
        assert animal.status['Energy'] == expected_energy
    
    print("✅ Trait validation tests passed!")

def main():
    """Run all tests."""
    print("🧪 Running animal_creator.py tests...\n")
    
    try:
        test_animal_creator_creation()
        test_training_questions()
        test_animal_creation_with_training()
        test_trait_bonus_calculation()
        test_custom_trait_creation()
        test_population_creation()
        test_diverse_population()
        test_animal_analysis()
        test_animal_customizer()
        test_edge_cases()
        test_trait_validation()
        
        print("\n🎉 All tests passed! Animal creation and customization is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Tests failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
