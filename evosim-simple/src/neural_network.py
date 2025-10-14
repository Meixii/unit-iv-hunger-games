"""
Neural Network Implementation for Evolutionary Simulation

This module implements a simple Multi-Layer Perceptron (MLP) neural network
designed for the evolutionary simulation. The network has a 2-4-4 architecture:
- 2 inputs: Hunger and Thirst levels
- 4 hidden neurons: Processing layer
- 4 outputs: Move, Eat, Drink, Rest actions

Author: Zen Garden
University of Caloocan City
"""

import numpy as np
import json
from typing import Dict, Tuple


class NeuralNetwork:
    """
    Simple Multi-Layer Perceptron for animal decision-making.
    
    Architecture: 4 inputs → 4 hidden → 4 outputs
    - Inputs: [hunger, thirst, food_nearby, water_nearby] (normalized 0-1)
    - Outputs: [move, eat, drink, rest] (action probabilities)
    """
    
    def __init__(self, input_size: int = 4, hidden_size: int = 4, 
                 output_size: int = 4, weight_range: Tuple[float, float] = (-1.0, 1.0)):
        """
        Initialize the neural network with random weights.
        
        Args:
            input_size: Number of input neurons (default: 4)
            hidden_size: Number of hidden neurons (default: 4)
            output_size: Number of output neurons (default: 4)
            weight_range: Range for random weight initialization
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weight_range = weight_range
        
        # Initialize weights and biases
        self._initialize_weights()
        
        # Network metadata
        self.generation = 0
        self.fitness = 0.0
        self.mutation_count = 0
        
    def _initialize_weights(self) -> None:
        """Initialize network weights and biases with random values."""
        # Weights from input to hidden layer
        self.weights_input_hidden = np.random.uniform(
            self.weight_range[0], self.weight_range[1], 
            (self.input_size, self.hidden_size)
        )
        
        # Weights from hidden to output layer
        self.weights_hidden_output = np.random.uniform(
            self.weight_range[0], self.weight_range[1], 
            (self.hidden_size, self.output_size)
        )
        
        # Bias vectors
        self.bias_hidden = np.zeros(self.hidden_size)
        self.bias_output = np.zeros(self.output_size)
        
    def forward_propagation(self, inputs: np.ndarray) -> np.ndarray:
        """
        Perform forward propagation through the network.
        
        Args:
            inputs: Input vector [hunger, thirst] (shape: 2,)
            
        Returns:
            Output vector [move, eat, drink, rest] (shape: 4,)
        """
        # Ensure inputs are in correct format
        if inputs.shape != (self.input_size,):
            raise ValueError(f"Expected input shape ({self.input_size},), got {inputs.shape}")
            
        # Normalize inputs to [0, 1] range
        inputs = np.clip(inputs, 0.0, 1.0)
        
        # Forward pass through hidden layer
        hidden_input = np.dot(inputs, self.weights_input_hidden) + self.bias_hidden
        hidden_output = self._sigmoid(hidden_input)
        
        # Forward pass through output layer
        output_input = np.dot(hidden_output, self.weights_hidden_output) + self.bias_output
        output = self._sigmoid(output_input)
        
        return output
    
    def get_decision(self, inputs: np.ndarray) -> str:
        """
        Get the action decision based on network output.
        
        Args:
            inputs: Input vector [hunger, thirst]
            
        Returns:
            Action string: 'move', 'eat', 'drink', or 'rest'
        """
        outputs = self.forward_propagation(inputs)
        action_index = np.argmax(outputs)
        
        actions = ['move', 'eat', 'drink', 'rest']
        return actions[action_index]
    
    def get_action_probabilities(self, inputs: np.ndarray) -> Dict[str, float]:
        """
        Get probability distribution over all actions.
        
        Args:
            inputs: Input vector [hunger, thirst]
            
        Returns:
            Dictionary mapping actions to probabilities
        """
        outputs = self.forward_propagation(inputs)
        
        # Convert to probabilities using softmax
        probabilities = self._softmax(outputs)
        
        actions = ['move', 'eat', 'drink', 'rest']
        return {action: float(prob) for action, prob in zip(actions, probabilities)}
    
    def mutate(self, mutation_rate: float = 0.1, mutation_strength: float = 0.1) -> None:
        """
        Apply random mutations to the network weights.
        
        Args:
            mutation_rate: Probability of mutating each weight
            mutation_strength: Strength of mutations (standard deviation)
        """
        # Mutate input-to-hidden weights
        mask = np.random.random(self.weights_input_hidden.shape) < mutation_rate
        mutations = np.random.normal(0, mutation_strength, self.weights_input_hidden.shape)
        self.weights_input_hidden[mask] += mutations[mask]
        
        # Mutate hidden-to-output weights
        mask = np.random.random(self.weights_hidden_output.shape) < mutation_rate
        mutations = np.random.normal(0, mutation_strength, self.weights_hidden_output.shape)
        self.weights_hidden_output[mask] += mutations[mask]
        
        # Mutate biases
        mask = np.random.random(self.bias_hidden.shape) < mutation_rate
        mutations = np.random.normal(0, mutation_strength, self.bias_hidden.shape)
        self.bias_hidden[mask] += mutations[mask]
        
        mask = np.random.random(self.bias_output.shape) < mutation_rate
        mutations = np.random.normal(0, mutation_strength, self.bias_output.shape)
        self.bias_output[mask] += mutations[mask]
        
        self.mutation_count += 1
    
    def crossover(self, other: 'NeuralNetwork', crossover_rate: float = 0.5) -> 'NeuralNetwork':
        """
        Create offspring by combining weights from two parent networks.
        
        Args:
            other: Another NeuralNetwork to crossover with
            crossover_rate: Probability of taking weights from 'other' parent
            
        Returns:
            New NeuralNetwork offspring
        """
        if not isinstance(other, NeuralNetwork):
            raise TypeError("Crossover partner must be a NeuralNetwork instance")
            
        if (self.input_size != other.input_size or 
            self.hidden_size != other.hidden_size or 
            self.output_size != other.output_size):
            raise ValueError("Network architectures must match for crossover")
        
        # Create offspring with same architecture
        offspring = NeuralNetwork(
            self.input_size, self.hidden_size, self.output_size, self.weight_range
        )
        
        # Crossover input-to-hidden weights
        mask = np.random.random(self.weights_input_hidden.shape) < crossover_rate
        offspring.weights_input_hidden = np.where(
            mask, other.weights_input_hidden, self.weights_input_hidden
        )
        
        # Crossover hidden-to-output weights
        mask = np.random.random(self.weights_hidden_output.shape) < crossover_rate
        offspring.weights_hidden_output = np.where(
            mask, other.weights_hidden_output, self.weights_hidden_output
        )
        
        # Crossover biases
        mask = np.random.random(self.bias_hidden.shape) < crossover_rate
        offspring.bias_hidden = np.where(mask, other.bias_hidden, self.bias_hidden)
        
        mask = np.random.random(self.bias_output.shape) < crossover_rate
        offspring.bias_output = np.where(mask, other.bias_output, self.bias_output)
        
        return offspring
    
    def copy(self) -> 'NeuralNetwork':
        """
        Create an identical copy of this network.
        
        Returns:
            New NeuralNetwork with identical weights
        """
        copy_network = NeuralNetwork(
            self.input_size, self.hidden_size, self.output_size, self.weight_range
        )
        
        # Copy weights and biases
        copy_network.weights_input_hidden = self.weights_input_hidden.copy()
        copy_network.weights_hidden_output = self.weights_hidden_output.copy()
        copy_network.bias_hidden = self.bias_hidden.copy()
        copy_network.bias_output = self.bias_output.copy()
        
        # Copy metadata
        copy_network.generation = self.generation
        copy_network.fitness = self.fitness
        copy_network.mutation_count = self.mutation_count
        
        return copy_network
    
    def get_weights(self) -> Dict[str, np.ndarray]:
        """
        Get all network weights and biases as a dictionary.
        
        Returns:
            Dictionary containing all weights and biases
        """
        return {
            'weights_input_hidden': self.weights_input_hidden.copy(),
            'weights_hidden_output': self.weights_hidden_output.copy(),
            'bias_hidden': self.bias_hidden.copy(),
            'bias_output': self.bias_output.copy()
        }
    
    def set_weights(self, weights: Dict[str, np.ndarray]) -> None:
        """
        Set network weights and biases from a dictionary.
        
        Args:
            weights: Dictionary containing weights and biases
        """
        self.weights_input_hidden = weights['weights_input_hidden'].copy()
        self.weights_hidden_output = weights['weights_hidden_output'].copy()
        self.bias_hidden = weights['bias_hidden'].copy()
        self.bias_output = weights['bias_output'].copy()
    
    def serialize(self) -> str:
        """
        Serialize the network to a JSON string.
        
        Returns:
            JSON string representation of the network
        """
        data = {
            'input_size': self.input_size,
            'hidden_size': self.hidden_size,
            'output_size': self.output_size,
            'weight_range': self.weight_range,
            'weights': {
                'weights_input_hidden': self.weights_input_hidden.tolist(),
                'weights_hidden_output': self.weights_hidden_output.tolist(),
                'bias_hidden': self.bias_hidden.tolist(),
                'bias_output': self.bias_output.tolist()
            },
            'metadata': {
                'generation': self.generation,
                'fitness': self.fitness,
                'mutation_count': self.mutation_count
            }
        }
        return json.dumps(data, indent=2)
    
    @classmethod
    def deserialize(cls, json_string: str) -> 'NeuralNetwork':
        """
        Create a network from a JSON string.
        
        Args:
            json_string: JSON string representation of the network
            
        Returns:
            NeuralNetwork instance
        """
        data = json.loads(json_string)
        
        network = cls(
            data['input_size'],
            data['hidden_size'], 
            data['output_size'],
            tuple(data['weight_range'])
        )
        
        # Set weights
        weights = data['weights']
        network.weights_input_hidden = np.array(weights['weights_input_hidden'])
        network.weights_hidden_output = np.array(weights['weights_hidden_output'])
        network.bias_hidden = np.array(weights['bias_hidden'])
        network.bias_output = np.array(weights['bias_output'])
        
        # Set metadata
        metadata = data['metadata']
        network.generation = metadata['generation']
        network.fitness = metadata['fitness']
        network.mutation_count = metadata['mutation_count']
        
        return network
    
    def _sigmoid(self, x: np.ndarray) -> np.ndarray:
        """Apply sigmoid activation function."""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))  # Clip to prevent overflow
    
    def _softmax(self, x: np.ndarray) -> np.ndarray:
        """Apply softmax activation function."""
        exp_x = np.exp(x - np.max(x))  # Subtract max for numerical stability
        return exp_x / np.sum(exp_x)
    
    def __str__(self) -> str:
        """String representation of the network."""
        return (f"NeuralNetwork(inputs={self.input_size}, hidden={self.hidden_size}, "
                f"outputs={self.output_size}, generation={self.generation}, "
                f"fitness={self.fitness:.3f})")
    
    def __repr__(self) -> str:
        """Detailed string representation of the network."""
        return self.__str__()
