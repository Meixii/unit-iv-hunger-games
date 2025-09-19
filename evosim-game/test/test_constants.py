#!/usr/bin/env python3
"""
Test script for constants.py

This script validates that all constants are properly defined and accessible.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import constants

def test_constants_import():
    """Test that all constants can be imported and accessed."""
    print("Testing constants import...")
    
    # Test world generation constants
    assert constants.GRID_WIDTH == 25
    assert constants.GRID_HEIGHT == 25
    assert len(constants.TERRAIN_DISTRIBUTION) == 4
    assert sum(constants.TERRAIN_DISTRIBUTION.values()) == 1.0
    
    # Test animal parameters
    assert constants.STANDARD_TRAIT_MIN == 4
    assert constants.STANDARD_TRAIT_MAX == 6
    assert constants.PRIMARY_TRAIT_MIN == 7
    assert constants.PRIMARY_TRAIT_MAX == 9
    
    # Test fitness weights
    assert len(constants.FITNESS_WEIGHTS) == 5
    assert constants.FITNESS_WEIGHTS['Time'] == 1
    assert constants.FITNESS_WEIGHTS['Kill'] == 50
    
    # Test animal categories
    assert len(constants.ANIMAL_CATEGORIES) == 3
    assert 'Herbivore' in constants.ANIMAL_CATEGORIES
    assert 'Carnivore' in constants.ANIMAL_CATEGORIES
    assert 'Omnivore' in constants.ANIMAL_CATEGORIES
    
    # Test trait names
    assert len(constants.TRAIT_NAMES) == 5
    assert 'STR' in constants.TRAIT_NAMES
    assert 'AGI' in constants.TRAIT_NAMES
    
    # Test actions
    assert len(constants.ACTIONS) == 8
    assert 'Move North' in constants.ACTIONS
    assert 'Attack' in constants.ACTIONS
    
    print("✅ All constants import tests passed!")

def test_validation_function():
    """Test the validation function."""
    print("Testing validation function...")
    
    try:
        constants.validate_constants()
        print("✅ Validation function test passed!")
    except Exception as e:
        print(f"❌ Validation function test failed: {e}")
        raise

def test_constant_accessibility():
    """Test that constants can be accessed in different ways."""
    print("Testing constant accessibility...")
    
    # Test direct access
    grid_size = constants.GRID_WIDTH * constants.GRID_HEIGHT
    assert grid_size == 625
    
    # Test dictionary access
    plains_chance = constants.TERRAIN_DISTRIBUTION['Plains']
    assert plains_chance == 0.60
    
    # Test list access
    first_action = constants.ACTIONS[0]
    assert first_action == 'Move North'
    
    # Test string formatting with constants
    message = f"Grid size: {constants.GRID_WIDTH}x{constants.GRID_HEIGHT}"
    assert "25x25" in message
    
    print("✅ Constant accessibility tests passed!")

def main():
    """Run all tests."""
    print("🧪 Running constants.py tests...\n")
    
    try:
        test_constants_import()
        test_validation_function()
        test_constant_accessibility()
        
        print("\n🎉 All tests passed! Constants file is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Tests failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
