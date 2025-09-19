"""
MLP ("Brain") Implementation

A lightweight, pure-Python Multi-Layer Perceptron used for animal decision-making.
Architecture and activations are driven by values from constants.py.
"""

from __future__ import annotations

from typing import List, Sequence
import math
import random

import constants


def _relu(x: float) -> float:
    return x if x > 0.0 else 0.0


def _softmax(z: Sequence[float]) -> List[float]:
    if not z:
        return []
    # Numerical stability: shift by max
    m = max(z)
    exps = [math.exp(v - m) for v in z]
    s = sum(exps)
    if s == 0.0:
        # Fallback to uniform distribution if all exps underflow
        return [1.0 / len(z) for _ in z]
    return [v / s for v in exps]


class MLPNetwork:
    """
    Simple feed-forward MLP with two hidden layers and softmax output.

    - Hidden activation: ReLU (per constants.HIDDEN_ACTIVATION)
    - Output activation: Softmax (per constants.OUTPUT_ACTIVATION)

    Weights and biases are stored as nested lists for readability.
    """

    def __init__(
        self,
        input_nodes: int | None = None,
        hidden1_nodes: int | None = None,
        hidden2_nodes: int | None = None,
        output_nodes: int | None = None,
        rng: random.Random | None = None,
    ) -> None:
        self.input_nodes = input_nodes or constants.INPUT_NODES
        self.hidden1_nodes = hidden1_nodes or constants.HIDDEN_LAYER_1_NODES
        self.hidden2_nodes = hidden2_nodes or constants.HIDDEN_LAYER_2_NODES
        self.output_nodes = output_nodes or constants.OUTPUT_NODES

        self.rng = rng or random.Random()

        # Initialize weights with small random values (He/Xavier-like simple scaling)
        def init_matrix(rows: int, cols: int, scale: float) -> List[List[float]]:
            return [[self.rng.uniform(-scale, scale) for _ in range(cols)] for _ in range(rows)]

        # Layer shapes: W shape is [out_dim][in_dim]
        self.W1 = init_matrix(self.hidden1_nodes, self.input_nodes, scale=0.1)
        self.b1 = [0.0 for _ in range(self.hidden1_nodes)]

        self.W2 = init_matrix(self.hidden2_nodes, self.hidden1_nodes, scale=0.1)
        self.b2 = [0.0 for _ in range(self.hidden2_nodes)]

        self.W3 = init_matrix(self.output_nodes, self.hidden2_nodes, scale=0.1)
        self.b3 = [0.0 for _ in range(self.output_nodes)]

    def forward(self, x: Sequence[float]) -> List[float]:
        """
        Forward pass: x -> ReLU(W1x + b1) -> ReLU(W2h1 + b2) -> Softmax(W3h2 + b3)
        - x length must equal input_nodes
        Returns probability distribution over actions (length = output_nodes).
        """
        if len(x) != self.input_nodes:
            raise ValueError(f"Input length {len(x)} does not match expected {self.input_nodes}")

        # Layer 1
        h1: List[float] = []
        for i in range(self.hidden1_nodes):
            s = self.b1[i]
            wi = self.W1[i]
            # dot product
            for j in range(self.input_nodes):
                s += wi[j] * x[j]
            h1.append(_relu(s))

        # Layer 2
        h2: List[float] = []
        for i in range(self.hidden2_nodes):
            s = self.b2[i]
            wi = self.W2[i]
            for j in range(self.hidden1_nodes):
                s += wi[j] * h1[j]
            h2.append(_relu(s))

        # Output
        logits: List[float] = []
        for i in range(self.output_nodes):
            s = self.b3[i]
            wi = self.W3[i]
            for j in range(self.hidden2_nodes):
                s += wi[j] * h2[j]
            logits.append(s)

        return _softmax(logits)

    # --- Optional utilities for EA integration ---
    def get_parameters_flat(self) -> List[float]:
        """Flatten all weights and biases to a single list."""
        flat: List[float] = []
        for row in self.W1:
            flat.extend(row)
        flat.extend(self.b1)
        for row in self.W2:
            flat.extend(row)
        flat.extend(self.b2)
        for row in self.W3:
            flat.extend(row)
        flat.extend(self.b3)
        return flat

    def set_parameters_flat(self, params: Sequence[float]) -> None:
        """
        Set network weights and biases from a flat parameter list.
        Expects the exact length produced by get_parameters_flat().
        """
        idx = 0

        def take(n: int) -> List[float]:
            nonlocal idx
            if idx + n > len(params):
                raise ValueError("Parameter vector too short")
            chunk = list(params[idx:idx + n])
            idx += n
            return chunk

        # W1
        for i in range(self.hidden1_nodes):
            self.W1[i] = take(self.input_nodes)
        self.b1 = take(self.hidden1_nodes)

        # W2
        for i in range(self.hidden2_nodes):
            self.W2[i] = take(self.hidden1_nodes)
        self.b2 = take(self.hidden2_nodes)

        # W3
        for i in range(self.output_nodes):
            self.W3[i] = take(self.hidden2_nodes)
        self.b3 = take(self.output_nodes)

        if idx != len(params):
            raise ValueError("Parameter vector has extra values")
