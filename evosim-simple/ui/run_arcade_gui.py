"""Entry point for Arcade GUI version of Evolution Simulation"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import arcade
from ui.arcade_gui.main_window import EvolutionSimulationWindow

def main():
    # Default to 1366x768
    window = EvolutionSimulationWindow(1366, 768, "Evolution Simulation")
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
