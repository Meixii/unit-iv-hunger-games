#!/usr/bin/env python3
"""
EvoSim GUI Launcher

This script launches the EvoSim GUI application.
It handles path setup and error handling for the GUI.
"""

import sys
import os
import traceback
from pathlib import Path

def setup_paths():
    """Setup Python paths for the GUI application."""
    # Get the directory containing this script
    gui_dir = Path(__file__).parent.absolute()
    project_root = gui_dir.parent
    
    # Add project root to Python path
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # Add evosim-game directory to path
    evosim_dir = project_root / "evosim-game"
    if evosim_dir.exists() and str(evosim_dir) not in sys.path:
        sys.path.insert(0, str(evosim_dir))
    
    return gui_dir, project_root

def check_dependencies():
    """Check if required dependencies are available."""
    missing_deps = []
    
    try:
        import tkinter
    except ImportError:
        missing_deps.append("tkinter (usually included with Python)")
    
    try:
        # Check if evosim-game modules are available
        from evosim_game.simulation_controller import SimulationController
        from evosim_game.data_structures import Animal, World
    except ImportError as e:
        print(f"Warning: Could not import evosim-game modules: {e}")
        print("Make sure the evosim-game directory exists and contains the required modules.")
    
    if missing_deps:
        print("Missing dependencies:")
        for dep in missing_deps:
            print(f"  - {dep}")
        return False
    
    return True

def main():
    """Main entry point for the GUI launcher."""
    print("EvoSim GUI Launcher")
    print("==================")
    
    try:
        # Setup paths
        gui_dir, project_root = setup_paths()
        print(f"GUI directory: {gui_dir}")
        print(f"Project root: {project_root}")
        
        # Check dependencies
        if not check_dependencies():
            print("\nSome dependencies are missing. Please install them and try again.")
            return 1
        
        # Import and run the GUI
        print("\nStarting EvoSim GUI...")
        from main_gui import main as gui_main
        gui_main()
        
    except ImportError as e:
        print(f"\nImport error: {e}")
        print("Make sure all required modules are available.")
        print("Check that the evosim-game directory exists and contains the simulation modules.")
        return 1
        
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("\nFull traceback:")
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
