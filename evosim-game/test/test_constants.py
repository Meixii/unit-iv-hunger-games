"""
Unit tests for constants.py
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import constants


class TestConstants(unittest.TestCase):
    """Test all numeric and categorical constants."""

    def test_constants_validation(self):
        """Validate all constants pass the internal validation check."""
        try:
            constants.validate_constants()
        except AssertionError as e:
            self.fail(f"constants.validate_constants() failed: {e}")

    def test_grid_constants(self):
        """Test world grid dimensions and terrain distributions."""
        self.assertEqual(constants.GRID_WIDTH, 25)
        self.assertEqual(constants.GRID_HEIGHT, 25)
        self.assertAlmostEqual(sum(constants.TERRAIN_DISTRIBUTION.values()), 1.0, places=2)

    def test_animal_traits_constants(self):
        """Test animal traits and status names."""
        expected_traits = ['STR', 'AGI', 'INT', 'END', 'PER']
        self.assertEqual(sorted(constants.TRAIT_NAMES), sorted(expected_traits))
        self.assertTrue(constants.STANDARD_TRAIT_MIN <= constants.STANDARD_TRAIT_MAX)
        self.assertTrue(constants.PRIMARY_TRAIT_MIN <= constants.PRIMARY_TRAIT_MAX)

    def test_fitness_weights(self):
        """Test fitness score component weights."""
        self.assertIn('Time', constants.FITNESS_WEIGHTS)
        self.assertIn('Resource', constants.FITNESS_WEIGHTS)
        self.assertIn('Kill', constants.FITNESS_WEIGHTS)
        self.assertIn('Distance', constants.FITNESS_WEIGHTS)
        self.assertIn('Event', constants.FITNESS_WEIGHTS)

    def test_neural_architecture(self):
        """Test MLP dimensions."""
        self.assertEqual(constants.INPUT_NODES, 41)
        self.assertEqual(constants.HIDDEN_LAYER_1_NODES, 16)
        self.assertEqual(constants.HIDDEN_LAYER_2_NODES, 12)
        self.assertEqual(constants.OUTPUT_NODES, 8)


if __name__ == '__main__':
    unittest.main()
