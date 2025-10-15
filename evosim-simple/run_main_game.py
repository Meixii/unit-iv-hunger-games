#!/usr/bin/env python3
"""
Main Game Launcher for Evolutionary Simulation

This script launches the main Arcade-based GUI for the evolutionary simulation.

Usage:
    python run_main_game.py

Features:
    - Interactive grid visualization
    - Real-time statistics panels
    - Animal interaction (click to inspect)
    - Simulation controls (start/pause/stop)
    - Speed control
    - Data export functionality

Author: Zen Garden
University of Caloocan City
"""

import sys
import os
import arcade

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import the main game
from main_game import SimGame


def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import arcade
        print("[SUCCESS] Arcade library found")
    except ImportError:
        print("[ERROR] Arcade library not found!")
        print("Please install it with: pip install arcade")
        return False
    
    try:
        import numpy
        print("[SUCCESS] NumPy found")
    except ImportError:
        print("[ERROR] NumPy not found!")
        print("Please install it with: pip install numpy")
        return False
    
    return True


def main():
    """Main function to launch the main game GUI."""
    print("=" * 60)
    print("EVOLUTIONARY ECOSYSTEM SIMULATOR")
    print("=" * 60)
    print("Launching main Arcade-based GUI...")
    print()
    
    # Check dependencies
    print("Checking dependencies...")
    if not check_dependencies():
        print("\n[ERROR] Missing dependencies. Please install them and try again.")
        print("You can install all dependencies with:")
        print("pip install arcade numpy")
        return 1
    
    print("\n[SUCCESS] All dependencies found!")
    print()
    
    # Launch the GUI
    try:
        print("[INFO] Starting Evolutionary Ecosystem Simulator...")
        print("Features:")
        print("  - Interactive grid visualization with sprites")
        print("  - Real-time statistics panels")
        print("  - Click on animals to inspect their details")
        print("  - Simulation controls (start/pause/stop)")
        print("  - Speed control and data export")
        print()
        print("Controls:")
        print("  - Click 'Initialize' to set up the simulation")
        print("  - Click 'Start' to begin the simulation")
        print("  - Use 'Pause' to pause/resume")
        print("  - Click on animals in the grid to see their details")
        print("  - Adjust speed using the speed input field")
        print("  - Use 'Export Data' to save simulation results")
        print()
        
        # Create and run the game
        window = SimGame()
        arcade.run()
        
    except Exception as e:
        print(f"[ERROR] Error launching GUI: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed")
        print("2. Check that your graphics drivers are up to date")
        print("3. Try running: pip install --upgrade arcade")
        return 1
    
    print("\n[INFO] Thanks for using the Evolutionary Ecosystem Simulator!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
