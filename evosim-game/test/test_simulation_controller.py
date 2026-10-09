"""
Unit tests for simulation_controller.py
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation_controller import SimulationController
from config import SimulationConfig


class TestSimulationController(unittest.TestCase):
    """Test full multi-generation, multi-week simulation lifecycle."""

    def test_run_generation_and_evolution(self):
        """Test SimulationController runs generations, logs data, and tracks casualties accurately."""
        cfg = SimulationConfig(
            max_weeks=10,
            max_generations=2,
            population_size=10,
            random_seed=42,
            enable_logging=False,
            log_level="WARNING"
        )
        ctrl = SimulationController(cfg)
        ctrl.initialize_world()
        ctrl.initialize_population()
        
        self.assertEqual(len(ctrl.simulation.get_living_animals()), 10)
        
        results = ctrl.run_generations(num_generations=2, weeks_per_generation=8)
        self.assertEqual(len(results), 2)
        
        for r in results:
            self.assertIn('generation', r)
            self.assertIn('weeks_completed', r)
            self.assertIn('survivors', r)
            self.assertIn('casualties', r)
            # Survivors + casualties must equal total population
            self.assertEqual(r['survivors'] + r['casualties'], r['total_population'])


if __name__ == '__main__':
    unittest.main()
