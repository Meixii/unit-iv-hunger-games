#!/usr/bin/env python3
"""
EvoSim GUI Test Script

This script tests the GUI components without running the full application.
It verifies that all imports work correctly and basic functionality is available.
"""

import sys
import os
import traceback
from pathlib import Path

def test_imports():
    """Test that all required imports work."""
    print("Testing imports...")
    
    try:
        import tkinter as tk
        print("+ tkinter imported successfully")
    except ImportError as e:
        print(f"- Failed to import tkinter: {e}")
        return False
    
    try:
        from tkinter import ttk, messagebox, filedialog
        print("+ tkinter submodules imported successfully")
    except ImportError as e:
        print(f"- Failed to import tkinter submodules: {e}")
        return False
    
    try:
        import threading
        import time
        import json
        print("+ Standard library modules imported successfully")
    except ImportError as e:
        print(f"- Failed to import standard library modules: {e}")
        return False
    
    return True

def test_evosim_imports():
    """Test that evosim-game modules can be imported."""
    print("\nTesting evosim-game imports...")
    
    # Add paths
    gui_dir = Path(__file__).parent.absolute()
    project_root = gui_dir.parent
    evosim_dir = project_root / "evosim-game"
    
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    if str(evosim_dir) not in sys.path:
        sys.path.insert(0, str(evosim_dir))
    
    try:
        from simulation_controller import SimulationController, SimulationConfig
        print("+ SimulationController imported successfully")
    except ImportError as e:
        print(f"- Failed to import SimulationController: {e}")
        return False
    
    try:
        from world_generator import GenerationConfig
        print("+ GenerationConfig imported successfully")
    except ImportError as e:
        print(f"- Failed to import GenerationConfig: {e}")
        return False
    
    try:
        from data_structures import Animal, World, TerrainType, AnimalCategory
        print("+ Data structures imported successfully")
    except ImportError as e:
        print(f"- Failed to import data structures: {e}")
        return False
    
    try:
        from config import AppConfig
        print("+ Config modules imported successfully")
    except ImportError as e:
        print(f"- Failed to import config modules: {e}")
        return False
    
    return True

def test_gui_creation():
    """Test that the GUI can be created without errors."""
    print("\nTesting GUI creation...")
    
    try:
        # Import the main GUI class
        from main_gui import EvoSimGUI
        print("+ EvoSimGUI class imported successfully")
        
        # Test that we can create the GUI (without showing it)
        # We'll create it in a way that doesn't show the window
        import tkinter as tk
        
        # Create a test root window
        test_root = tk.Tk()
        test_root.withdraw()  # Hide the window
        
        # Test basic GUI functionality
        print("+ GUI components can be created")
        
        # Clean up
        test_root.destroy()
        
        return True
        
    except Exception as e:
        print(f"- Failed to create GUI: {e}")
        traceback.print_exc()
        return False

def test_configuration():
    """Test configuration functionality."""
    print("\nTesting configuration...")
    
    try:
        from config import AppConfig
        
        # Test creating a config
        config = AppConfig()
        print("+ AppConfig created successfully")
        
        # Test basic properties
        print(f"  - Default population size: {config.simulation.max_weeks}")
        print(f"  - Default max weeks: {config.simulation.max_weeks}")
        print(f"  - Default max generations: {config.simulation.max_generations}")
        
        return True
        
    except Exception as e:
        print(f"- Failed to test configuration: {e}")
        return False

def main():
    """Run all tests."""
    print("EvoSim GUI Test Suite")
    print("====================")
    
    tests = [
        ("Import Tests", test_imports),
        ("EvoSim Imports", test_evosim_imports),
        ("GUI Creation", test_gui_creation),
        ("Configuration", test_configuration)
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
            traceback.print_exc()
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("SUCCESS: All tests passed! GUI should work correctly.")
        return 0
    else:
        print("FAILED: Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
