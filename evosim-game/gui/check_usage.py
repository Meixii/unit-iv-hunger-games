#!/usr/bin/env python3
"""
Simple script to check that all imported classes are used in the GUI code.
This script analyzes the code without importing the modules.
"""

import os
from pathlib import Path

def check_import_usage():
    """Check that all imports are used in the GUI code."""
    print("Checking Import Usage in GUI Code")
    print("================================")
    
    # Read the GUI file
    gui_file = Path(__file__).parent / "main_gui.py"
    
    if not gui_file.exists():
        print("ERROR: main_gui.py not found")
        return False
    
    with open(gui_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for usage of imported classes
    imports_to_check = [
        ('GenerationConfig', 'GenerationConfig('),
        ('Animal', 'Animal'),
        ('World', 'World'),
        ('TerrainType', 'TerrainType.'),
        ('AnimalCategory', 'AnimalCategory.')
    ]
    
    print("\nChecking for class usage:")
    all_used = True
    
    for class_name, usage_pattern in imports_to_check:
        if usage_pattern in content:
            print(f"+ {class_name} is used in the code")
        else:
            print(f"- {class_name} is not used in the code")
            all_used = False
    
    # Check for specific method calls that use the classes
    method_usage = [
        ('animal.get_fitness_score()', 'Animal fitness method'),
        ('animal.is_alive()', 'Animal alive method'),
        ('animal.category.value', 'Animal category property'),
        ('tile.terrain_type.value', 'Terrain type property'),
        ('world.width', 'World width property'),
        ('world.height', 'World height property')
    ]
    
    print("\nChecking for specific class method usage:")
    for pattern, description in method_usage:
        if pattern in content:
            print(f"+ {description} - {pattern}")
        else:
            print(f"- {description} - {pattern} not found")
            all_used = False
    
    # Check for methods that should use the imported classes
    expected_methods = [
        'log_world_info',      # Uses World class
        'log_animal_info',     # Uses Animal class
        'get_animal_details',  # Uses Animal class
        'analyze_animal_population',  # Uses Animal class
        'export_animal_data',  # Uses Animal class
        'start_simulation'     # Uses GenerationConfig class
    ]
    
    print("\nChecking for methods that use imported classes:")
    for method in expected_methods:
        if f"def {method}(" in content:
            print(f"+ {method} method found")
        else:
            print(f"- {method} method not found")
            all_used = False
    
    return all_used

def main():
    """Run the usage check."""
    print("EvoSim GUI Import Usage Check")
    print("=============================")
    
    if check_import_usage():
        print("\nSUCCESS: All imports are properly used in the GUI!")
        return 0
    else:
        print("\nFAILED: Some imports are not being used properly.")
        return 1

if __name__ == "__main__":
    exit(main())
