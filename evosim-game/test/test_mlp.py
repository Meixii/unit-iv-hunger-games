"""
Unit tests for mlp.py
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mlp import MLPNetwork
import constants


class TestMLP(unittest.TestCase):
    """Test Multi-Layer Perceptron neural network architecture."""

    def test_mlp_topology(self):
        """Test layer dimensions match 41 -> 16 -> 12 -> 8."""
        net = MLPNetwork()
        self.assertEqual(net.input_nodes, 41)
        self.assertEqual(net.hidden1_nodes, 16)
        self.assertEqual(net.hidden2_nodes, 12)
        self.assertEqual(net.output_nodes, 8)

    def test_forward_pass_probabilities(self):
        """Test forward pass returns 8-element probability distribution summing to 1.0."""
        net = MLPNetwork()
        inputs = [0.5] * 41
        probs = net.forward(inputs)
        
        self.assertEqual(len(probs), 8)
        self.assertAlmostEqual(sum(probs), 1.0, places=4)
        for p in probs:
            self.assertTrue(0.0 <= p <= 1.0)

    def test_flatten_and_set_parameters(self):
        """Test parameter flattening and restoring for genetic algorithm."""
        net = MLPNetwork()
        params = net.get_parameters_flat()
        expected_param_count = (41 * 16 + 16) + (16 * 12 + 12) + (12 * 8 + 8)
        self.assertEqual(len(params), expected_param_count)
        
        # Modify parameters and restore
        modified = [p + 0.1 for p in params]
        net.set_parameters_flat(modified)
        restored = net.get_parameters_flat()
        self.assertEqual(modified, restored)


if __name__ == '__main__':
    unittest.main()
