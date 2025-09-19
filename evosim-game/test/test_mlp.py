"""
Unit tests for the MLP (Brain) implementation.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import constants
from mlp import MLPNetwork


class TestMLP(unittest.TestCase):
    def test_mlp_initialization(self):
        net = MLPNetwork()
        self.assertEqual(net.input_nodes, constants.INPUT_NODES)
        self.assertEqual(net.hidden1_nodes, constants.HIDDEN_LAYER_1_NODES)
        self.assertEqual(net.hidden2_nodes, constants.HIDDEN_LAYER_2_NODES)
        self.assertEqual(net.output_nodes, constants.OUTPUT_NODES)

    def test_forward_output_shape_and_distribution(self):
        net = MLPNetwork()
        x = [0.0] * constants.INPUT_NODES
        y = net.forward(x)
        self.assertEqual(len(y), constants.OUTPUT_NODES)
        self.assertAlmostEqual(sum(y), 1.0, places=6)
        # all values should be >= 0
        for v in y:
            self.assertGreaterEqual(v, 0.0)

    def test_parameter_roundtrip(self):
        net = MLPNetwork()
        params = net.get_parameters_flat()
        # perturb
        params2 = [p + 0.001 for p in params]
        net.set_parameters_flat(params2)
        self.assertEqual(len(net.get_parameters_flat()), len(params2))


if __name__ == "__main__":
    unittest.main(verbosity=2)


