"""
Test module for the NeuralNetwork class.
"""

import pytest
import numpy as np
from src.neural_network import NeuralNetwork


class TestNeuralNetwork:
    """Test cases for NeuralNetwork class."""
    
    def test_network_initialization(self):
        """Test network initialization with default parameters."""
        network = NeuralNetwork()
        
        assert network.input_size == 2
        assert network.hidden_size == 4
        assert network.output_size == 4
        assert network.weight_range == (-1.0, 1.0)
        assert network.generation == 0
        assert network.fitness == 0.0
        assert network.mutation_count == 0
    
    def test_network_initialization_custom(self):
        """Test network initialization with custom parameters."""
        network = NeuralNetwork(input_size=3, hidden_size=5, output_size=2, 
                                weight_range=(-2.0, 2.0))
        
        assert network.input_size == 3
        assert network.hidden_size == 5
        assert network.output_size == 2
        assert network.weight_range == (-2.0, 2.0)
    
    def test_forward_propagation(self):
        """Test forward propagation with valid inputs."""
        network = NeuralNetwork()
        inputs = np.array([0.5, 0.7])  # hunger=0.5, thirst=0.7
        
        outputs = network.forward_propagation(inputs)
        
        assert outputs.shape == (4,)
        assert all(0 <= output <= 1 for output in outputs)  # Sigmoid outputs
    
    def test_forward_propagation_invalid_input(self):
        """Test forward propagation with invalid input shape."""
        network = NeuralNetwork()
        invalid_inputs = np.array([0.5])  # Wrong shape
        
        with pytest.raises(ValueError):
            network.forward_propagation(invalid_inputs)
    
    def test_get_decision(self):
        """Test decision making based on network output."""
        network = NeuralNetwork()
        inputs = np.array([0.5, 0.7])
        
        decision = network.get_decision(inputs)
        
        assert decision in ['move', 'eat', 'drink', 'rest']
    
    def test_get_action_probabilities(self):
        """Test action probability distribution."""
        network = NeuralNetwork()
        inputs = np.array([0.5, 0.7])
        
        probabilities = network.get_action_probabilities(inputs)
        
        assert len(probabilities) == 4
        assert all(action in probabilities for action in ['move', 'eat', 'drink', 'rest'])
        assert abs(sum(probabilities.values()) - 1.0) < 1e-6  # Should sum to 1
    
    def test_mutation(self):
        """Test network mutation."""
        network = NeuralNetwork()
        original_weights = network.get_weights()
        
        network.mutate(mutation_rate=0.5, mutation_strength=0.1)
        
        new_weights = network.get_weights()
        assert network.mutation_count == 1
        
        # Check that at least some weights changed
        weights_changed = False
        for key in original_weights:
            if not np.allclose(original_weights[key], new_weights[key]):
                weights_changed = True
                break
        
        assert weights_changed
    
    def test_crossover(self):
        """Test network crossover."""
        network1 = NeuralNetwork()
        network2 = NeuralNetwork()
        
        offspring = network1.crossover(network2, crossover_rate=0.5)
        
        assert isinstance(offspring, NeuralNetwork)
        assert offspring.input_size == network1.input_size
        assert offspring.hidden_size == network1.hidden_size
        assert offspring.output_size == network1.output_size
    
    def test_crossover_incompatible_networks(self):
        """Test crossover with incompatible networks."""
        network1 = NeuralNetwork(input_size=2, hidden_size=4, output_size=4)
        network2 = NeuralNetwork(input_size=3, hidden_size=4, output_size=4)
        
        with pytest.raises(ValueError):
            network1.crossover(network2)
    
    def test_copy(self):
        """Test network copying."""
        network = NeuralNetwork()
        network.generation = 5
        network.fitness = 10.0
        
        copy_network = network.copy()
        
        assert copy_network.input_size == network.input_size
        assert copy_network.hidden_size == network.hidden_size
        assert copy_network.output_size == network.output_size
        assert copy_network.generation == network.generation
        assert copy_network.fitness == network.fitness
        
        # Check that weights are identical
        original_weights = network.get_weights()
        copy_weights = copy_network.get_weights()
        
        for key in original_weights:
            assert np.allclose(original_weights[key], copy_weights[key])
    
    def test_serialization(self):
        """Test network serialization and deserialization."""
        network = NeuralNetwork()
        network.generation = 3
        network.fitness = 15.5
        network.mutation_count = 2
        
        # Serialize
        json_string = network.serialize()
        assert isinstance(json_string, str)
        
        # Deserialize
        restored_network = NeuralNetwork.deserialize(json_string)
        
        assert restored_network.input_size == network.input_size
        assert restored_network.hidden_size == network.hidden_size
        assert restored_network.output_size == network.output_size
        assert restored_network.generation == network.generation
        assert restored_network.fitness == network.fitness
        assert restored_network.mutation_count == network.mutation_count
        
        # Check that weights are identical
        original_weights = network.get_weights()
        restored_weights = restored_network.get_weights()
        
        for key in original_weights:
            assert np.allclose(original_weights[key], restored_weights[key])
    
    def test_set_weights(self):
        """Test setting network weights."""
        network = NeuralNetwork()
        new_weights = {
            'weights_input_hidden': np.random.randn(2, 4),
            'weights_hidden_output': np.random.randn(4, 4),
            'bias_hidden': np.random.randn(4),
            'bias_output': np.random.randn(4)
        }
        
        network.set_weights(new_weights)
        retrieved_weights = network.get_weights()
        
        for key in new_weights:
            assert np.allclose(new_weights[key], retrieved_weights[key])
    
    def test_sigmoid_activation(self):
        """Test sigmoid activation function."""
        network = NeuralNetwork()
        
        # Test normal values
        x = np.array([0, 1, -1, 2, -2])
        result = network._sigmoid(x)
        
        assert all(0 <= val <= 1 for val in result)
        assert result[0] == 0.5  # sigmoid(0) = 0.5
        assert result[1] > 0.5   # sigmoid(1) > 0.5
        assert result[2] < 0.5   # sigmoid(-1) < 0.5
    
    def test_softmax_activation(self):
        """Test softmax activation function."""
        network = NeuralNetwork()
        
        x = np.array([1, 2, 3, 4])
        result = network._softmax(x)
        
        assert abs(sum(result) - 1.0) < 1e-6  # Should sum to 1
        assert all(val > 0 for val in result)  # All values should be positive
        assert result[3] > result[2] > result[1] > result[0]  # Should be ordered
    
    def test_string_representation(self):
        """Test string representation of network."""
        network = NeuralNetwork()
        network.generation = 2
        network.fitness = 5.5
        
        str_repr = str(network)
        assert "NeuralNetwork" in str_repr
        assert "inputs=2" in str_repr
        assert "hidden=4" in str_repr
        assert "outputs=4" in str_repr
        assert "generation=2" in str_repr
        assert "fitness=5.500" in str_repr
