"""
Main entry point for the Evolutionary Simulation application.
"""

import sys
import time
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import Phase 2 components
from .neural_network import NeuralNetwork
from .animal import Animal
# Import Phase 3 components
from .environment import GridWorld
from .events import EventManager
# Import Phase 4 components
from .evolution import Population, EvolutionManager
# Import Phase 5 components
from .simulation import Simulation, SimulationState
# Import Phase 6 components
from ui.gui import SimulationGUI
# Import Phase 7 components
from analysis.statistics import StatisticsCollector
from analysis.visualization import SimulationVisualizer
