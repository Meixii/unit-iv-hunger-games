"""
Educational Survival Simulation Using Evolutionary Algorithms

This package implements a simple evolutionary simulation where virtual animals
with neural network brains learn to survive in a 2D grid world.

Author: Zen Garden
University of Caloocan City
"""

__version__ = "0.1.0"
__author__ = "Zen Garden"
__email__ = "zengarden.thesisdev@gmail.com"

# Import main components when they are implemented
# These imports make the classes available at package level
from .neural_network import NeuralNetwork  # noqa: F401
from .animal import Animal  # noqa: F401
from .environment import GridWorld  # noqa: F401
from .events import EventManager  # noqa: F401
from .evolution import Population, EvolutionManager  # noqa: F401
from .simulation import Simulation, SimulationState  # noqa: F401
