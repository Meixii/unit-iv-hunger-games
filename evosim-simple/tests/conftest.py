"""
Pytest configuration and shared fixtures for the test suite.
"""

import pytest
import numpy as np
import json
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent


@pytest.fixture
def project_root():
    """Return the project root directory."""
    return PROJECT_ROOT


@pytest.fixture
def config_dir():
    """Return the path to the config directory."""
    return PROJECT_ROOT / "config"


@pytest.fixture
def default_config():
    """Load and return the default configuration."""
    config_path = PROJECT_ROOT / "config" / "default_config.json"
    with open(config_path, 'r') as f:
        return json.load(f)


@pytest.fixture
def event_config():
    """Load and return the event configuration."""
    config_path = PROJECT_ROOT / "config" / "event_config.json"
    with open(config_path, 'r') as f:
        return json.load(f)


@pytest.fixture
def sample_neural_network_weights():
    """Return sample neural network weights for testing."""
    return {
        'input_hidden': np.random.randn(2, 4),
        'hidden_output': np.random.randn(4, 4),
        'bias_hidden': np.zeros(4),
        'bias_output': np.zeros(4)
    }


@pytest.fixture
def sample_animal_data():
    """Return sample animal data for testing."""
    return {
        'position': (10, 10),
        'hunger': 75.0,
        'thirst': 80.0,
        'energy': 90.0,
        'age': 50,
        'fitness': 0.0,
        'alive': True
    }


@pytest.fixture
def sample_grid_data():
    """Return sample grid data for testing."""
    return {
        'width': 20,
        'height': 20,
        'food_positions': [(5, 5), (15, 15), (10, 10)],
        'water_positions': [(3, 3), (17, 17), (8, 8)]
    }
