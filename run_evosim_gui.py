#!/usr/bin/env python3
"""
EvoSim GUI Launcher

This script launches the EvoSim GUI application from the project root.
It automatically sets up the correct paths and handles any import issues.
"""

import sys
import os
from pathlib import Path

def main():
    """Launch the EvoSim GUI."""
    print("EvoSim GUI Launcher")
    print("==================")
    
    # Get the project root directory
    project_root = Path(__file__).parent.absolute()
    gui_dir = project_root / "gui"
    
    # Check if gui directory exists
    if not gui_dir.exists():
        print(f"Error: GUI directory not found at {gui_dir}")
        print("Make sure the gui folder exists in the project root.")
        return 1
    
    # Add gui directory to Python path
    if str(gui_dir) not in sys.path:
        sys.path.insert(0, str(gui_dir))
    
    # Add evosim-game directory to path
    evosim_dir = project_root / "evosim-game"
    if evosim_dir.exists() and str(evosim_dir) not in sys.path:
        sys.path.insert(0, str(evosim_dir))
    
    try:
        # Import and run the GUI
        print("Starting EvoSim GUI...")
        from gui.main_gui import main as gui_main
        gui_main()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Python 3.7+ is installed")
        print("2. Check that tkinter is available (usually included with Python)")
        print("3. Verify the evosim-game directory exists and contains the simulation modules")
        return 1
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
