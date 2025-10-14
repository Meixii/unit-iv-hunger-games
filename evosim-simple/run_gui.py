#!/usr/bin/env python3
"""
GUI Launcher for Evolutionary Simulation

This script launches the graphical user interface for the
evolutionary simulation application.

Author: Zen Garden
University of Caloocan City
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and run the GUI
from ui.gui import main

if __name__ == "__main__":
    main()
