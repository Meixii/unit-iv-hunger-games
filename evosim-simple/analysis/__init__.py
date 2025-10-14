"""
Data Analysis and Visualization Components

This package contains modules for collecting, analyzing, and visualizing
simulation data including statistics, charts, and export functionality.
"""

from .statistics import StatisticsCollector  # noqa: F401
from .visualization import SimulationVisualizer, create_visualization_window  # noqa: F401

__version__ = "1.0.0"
__author__ = "Zen Garden"
__email__ = "zengarden.thesisdev@gmail.com"

__all__ = ['StatisticsCollector', 'SimulationVisualizer', 'create_visualization_window']
