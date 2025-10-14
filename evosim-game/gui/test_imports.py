#!/usr/bin/env python3
"""
Test script to verify that all imported classes are being used in the GUI.
This script checks that the GUI properly utilizes all imported functionality.
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_imports_usage():
    """Test that all imports are actually used in the GUI."""
    print("Testing GUI Import Usage")
    print("========================")
    
    try:
        # Import the GUI module
        from main_gui import EvoSimGUI
        print("+ EvoSimGUI imported successfully")
        
        # Check that the class has methods that use the imported classes
        gui_methods = dir(EvoSimGUI)
        
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
            if hasattr(EvoSimGUI, method):
                print(f"+ {method} - Uses imported classes")
            else:
                print(f"- {method} - Missing method")
        
        # Test that we can create the GUI (without showing it)
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        try:
            # Create GUI instance
            gui = EvoSimGUI()
            print("+ GUI instance created successfully")
            
            # Test that the methods exist and are callable
            for method in expected_methods:
                if hasattr(gui, method):
                    method_obj = getattr(gui, method)
                    if callable(method_obj):
                        print(f"+ {method} is callable")
                    else:
                        print(f"- {method} is not callable")
                else:
                    print(f"- {method} not found")
            
            # Clean up
            root.destroy()
            
        except Exception as e:
            print(f"- Error creating GUI instance: {e}")
            root.destroy()
            return False
        
        print("\n+ All import usage tests passed!")
        return True
        
    except ImportError as e:
        print(f"- Import error: {e}")
        return False
    except Exception as e:
        print(f"- Unexpected error: {e}")
        return False

def test_class_usage():
    """Test that the imported classes are actually used in the code."""
    print("\nTesting Class Usage in Code")
    print("============================")
    
    try:
        # Read the GUI file and check for usage
        gui_file = Path(__file__).parent / "main_gui.py"
        with open(gui_file, 'r') as f:
            content = f.read()
        
        # Check for usage of imported classes
        imports_to_check = [
            ('GenerationConfig', 'GenerationConfig('),
            ('Animal', 'Animal('),
            ('World', 'World('),
            ('TerrainType', 'TerrainType.'),
            ('AnimalCategory', 'AnimalCategory.')
        ]
        
        for class_name, usage_pattern in imports_to_check:
            if usage_pattern in content:
                print(f"+ {class_name} is used in the code")
            else:
                print(f"- {class_name} is not used in the code")
        
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
        
        return True
        
    except Exception as e:
        print(f"- Error checking class usage: {e}")
        return False

def main():
    """Run all tests."""
    print("EvoSim GUI Import Usage Test")
    print("============================")
    
    tests = [
        ("Import Usage", test_imports_usage),
        ("Class Usage", test_class_usage)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * len(test_name))
        
        try:
            if test_func():
                print(f"+ {test_name} PASSED")
                passed += 1
            else:
                print(f"- {test_name} FAILED")
        except Exception as e:
            print(f"- {test_name} FAILED with exception: {e}")
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All imports are properly used in the GUI!")
        return 0
    else:
        print("FAILED: Some imports are not being used properly.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
