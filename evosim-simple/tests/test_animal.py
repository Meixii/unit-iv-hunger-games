"""
Test module for the Animal class.
"""

import pytest
from src.animal import Animal
from src.neural_network import NeuralNetwork


class TestAnimal:
    """Test cases for Animal class."""
    
    def test_animal_initialization(self):
        """Test animal initialization with default parameters."""
        animal = Animal(10, 15)
        
        assert animal.position == (10, 15)
        assert animal.hunger == 100.0
        assert animal.thirst == 100.0
        assert animal.energy == 100.0
        assert animal.age == 0
        assert animal.fitness == 0.0
        assert animal.alive == True
        assert isinstance(animal.neural_network, NeuralNetwork)
    
    def test_animal_initialization_custom(self):
        """Test animal initialization with custom parameters."""
        network = NeuralNetwork()
        animal = Animal(5, 8, network, initial_hunger=80.0, 
                        initial_thirst=90.0, initial_energy=70.0)
        
        assert animal.position == (5, 8)
        assert animal.hunger == 80.0
        assert animal.thirst == 90.0
        assert animal.energy == 70.0
        assert animal.neural_network is network
    
    def test_sense_environment(self):
        """Test environment sensing."""
        animal = Animal(10, 15, initial_hunger=50.0, initial_thirst=75.0)
        
        hunger, thirst = animal.sense_environment()
        
        assert hunger == 0.5  # 50.0 / 100.0
        assert thirst == 0.75  # 75.0 / 100.0
        assert 0 <= hunger <= 1
        assert 0 <= thirst <= 1
    
    def test_make_decision(self):
        """Test decision making."""
        animal = Animal(10, 15)
        
        decision = animal.make_decision()
        
        assert decision in ['move', 'eat', 'drink', 'rest']
    
    def test_get_action_probabilities(self):
        """Test action probability distribution."""
        animal = Animal(10, 15)
        
        probabilities = animal.get_action_probabilities()
        
        assert len(probabilities) == 4
        assert all(action in probabilities for action in ['move', 'eat', 'drink', 'rest'])
        assert abs(sum(probabilities.values()) - 1.0) < 1e-6
    
    def test_execute_move(self):
        """Test move action execution."""
        animal = Animal(10, 15, initial_energy=50.0)
        initial_energy = animal.energy
        
        success = animal.execute_action('move')
        
        assert success == True
        # Account for natural decay (0.05) applied in update_state()
        expected_energy = initial_energy - animal.action_costs['move'] - animal.energy_decay
        assert abs(animal.energy - expected_energy) < 0.01
        assert animal.movement_count == 1
        assert 'move' in animal.action_history
    
    def test_execute_eat(self):
        """Test eat action execution."""
        animal = Animal(10, 15, initial_energy=50.0, initial_hunger=80.0)
        initial_energy = animal.energy
        initial_hunger = animal.hunger
        
        success = animal.execute_action('eat')
        
        assert success == True
        # Account for natural decay (0.05) applied in update_state()
        expected_energy = initial_energy - animal.action_costs['eat'] - animal.energy_decay
        assert abs(animal.energy - expected_energy) < 0.01
        # Account for natural decay (0.1) applied in update_state()
        expected_hunger = initial_hunger - 20 - animal.hunger_decay
        assert abs(animal.hunger - expected_hunger) < 0.01
        assert animal.resource_consumed['food'] == 1
        assert 'eat' in animal.action_history
    
    def test_execute_drink(self):
        """Test drink action execution."""
        animal = Animal(10, 15, initial_energy=50.0, initial_thirst=80.0)
        initial_energy = animal.energy
        initial_thirst = animal.thirst
        
        success = animal.execute_action('drink')
        
        assert success == True
        # Account for natural decay (0.05) applied in update_state()
        expected_energy = initial_energy - animal.action_costs['drink'] - animal.energy_decay
        assert abs(animal.energy - expected_energy) < 0.01
        # Account for natural decay (0.1) applied in update_state()
        expected_thirst = initial_thirst - 20 - animal.thirst_decay
        assert abs(animal.thirst - expected_thirst) < 0.01
        assert animal.resource_consumed['water'] == 1
        assert 'drink' in animal.action_history
    
    def test_execute_rest(self):
        """Test rest action execution."""
        animal = Animal(10, 15, initial_energy=50.0, initial_hunger=80.0, 
                        initial_thirst=90.0)
        initial_energy = animal.energy
        initial_hunger = animal.hunger
        initial_thirst = animal.thirst
        
        success = animal.execute_action('rest')
        
        assert success == True
        # Account for natural decay (0.05) applied in update_state()
        expected_energy = initial_energy - animal.action_costs['rest'] + 5 - animal.energy_decay
        assert abs(animal.energy - expected_energy) < 0.01
        # Account for natural decay (0.1) applied in update_state()
        expected_hunger = initial_hunger - 2 - animal.hunger_decay
        expected_thirst = initial_thirst - 2 - animal.thirst_decay
        assert abs(animal.hunger - expected_hunger) < 0.01
        assert abs(animal.thirst - expected_thirst) < 0.01
        assert 'rest' in animal.action_history
    
    def test_insufficient_energy(self):
        """Test action execution with insufficient energy."""
        animal = Animal(10, 15, initial_energy=1.0)  # Very low energy
        
        success = animal.execute_action('move')  # Costs 5 energy
        
        assert success == False
        # Energy should only have natural decay applied (0.05)
        expected_energy = 1.0 - animal.energy_decay
        assert abs(animal.energy - expected_energy) < 0.01
    
    def test_natural_decay(self):
        """Test natural decay of hunger, thirst, and energy."""
        animal = Animal(10, 15, initial_hunger=50.0, initial_thirst=60.0, 
                        initial_energy=70.0)
        
        animal.update_state()
        
        assert animal.hunger == 50.0 - animal.hunger_decay
        assert animal.thirst == 60.0 - animal.thirst_decay
        assert animal.energy == 70.0 - animal.energy_decay
        assert animal.age == 1
    
    def test_survival_check_hunger(self):
        """Test survival check when hunger reaches 0."""
        animal = Animal(10, 15, initial_hunger=0.1, initial_thirst=50.0)
        
        animal.update_state()
        
        assert animal.alive == False
    
    def test_survival_check_thirst(self):
        """Test survival check when thirst reaches 0."""
        animal = Animal(10, 15, initial_hunger=50.0, initial_thirst=0.1)
        
        animal.update_state()
        
        assert animal.alive == False
    
    def test_survival_check_energy(self):
        """Test survival check when energy reaches 0."""
        animal = Animal(10, 15, initial_energy=0.1)
        
        # Apply decay multiple times to get energy to 0
        for _ in range(3):
            animal.update_state()
        
        assert animal.alive == False
    
    def test_calculate_fitness(self):
        """Test fitness calculation."""
        animal = Animal(10, 15)
        animal.age = 10
        animal.movement_count = 5
        animal.resource_consumed = {'food': 3, 'water': 2}
        
        fitness = animal.calculate_fitness()
        
        assert fitness > 0
        assert animal.fitness == fitness
    
    def test_calculate_fitness_dead_animal(self):
        """Test fitness calculation for dead animal."""
        animal = Animal(10, 15)
        animal.alive = False
        
        fitness = animal.calculate_fitness()
        
        assert fitness == 0.0
    
    def test_get_state(self):
        """Test getting animal state."""
        animal = Animal(10, 15, initial_hunger=80.0, initial_thirst=70.0)
        
        state = animal.get_state()
        
        assert state['position'] == (10, 15)
        assert state['hunger'] == 80.0
        assert state['thirst'] == 70.0
        assert state['energy'] == 100.0
        assert state['age'] == 0
        assert state['fitness'] == 0.0
        assert state['alive'] == True
        assert state['action_count'] == 0
        assert state['movement_count'] == 0
        assert state['resource_consumed'] == {'food': 0, 'water': 0}
    
    def test_set_position(self):
        """Test setting animal position."""
        animal = Animal(10, 15)
        
        animal.set_position(20, 25)
        
        assert animal.position == (20, 25)
        assert animal.get_position() == (20, 25)
    
    def test_add_food(self):
        """Test adding food to animal."""
        animal = Animal(10, 15, initial_hunger=50.0)
        
        animal.add_food(30.0)
        
        assert animal.hunger == 80.0
        assert animal.resource_consumed['food'] == 1
    
    def test_add_water(self):
        """Test adding water to animal."""
        animal = Animal(10, 15, initial_thirst=50.0)
        
        animal.add_water(30.0)
        
        assert animal.thirst == 80.0
        assert animal.resource_consumed['water'] == 1
    
    def test_get_action_summary(self):
        """Test getting action summary."""
        animal = Animal(10, 15)
        
        # Execute some actions
        animal.execute_action('move')
        animal.execute_action('eat')
        animal.execute_action('move')
        animal.execute_action('rest')
        
        summary = animal.get_action_summary()
        
        assert summary['move'] == 2
        assert summary['eat'] == 1
        assert summary['drink'] == 0
        assert summary['rest'] == 1
    
    def test_reset_for_new_generation(self):
        """Test resetting animal for new generation."""
        animal = Animal(10, 15)
        animal.hunger = 20.0
        animal.thirst = 30.0
        animal.energy = 40.0
        animal.age = 50
        animal.fitness = 100.0
        animal.alive = False
        animal.action_history = ['move', 'eat']
        animal.resource_consumed = {'food': 5, 'water': 3}
        animal.movement_count = 10
        
        animal.reset_for_new_generation(25, 30)
        
        assert animal.position == (25, 30)
        assert animal.hunger == 100.0
        assert animal.thirst == 100.0
        assert animal.energy == 100.0
        assert animal.age == 0
        assert animal.fitness == 0.0
        assert animal.alive == True
        assert animal.action_history == []
        assert animal.resource_consumed == {'food': 0, 'water': 0}
        assert animal.movement_count == 0
    
    def test_string_representation(self):
        """Test string representation of animal."""
        animal = Animal(10, 15, initial_hunger=80.0, initial_thirst=70.0, 
                        initial_energy=60.0)
        animal.age = 5
        
        str_repr = str(animal)
        
        assert "Animal" in str_repr
        assert "pos=(10, 15)" in str_repr
        assert "alive" in str_repr
        assert "hunger=80.0" in str_repr
        assert "thirst=70.0" in str_repr
        assert "energy=60.0" in str_repr
        assert "age=5" in str_repr
    
    def test_invalid_action(self):
        """Test executing invalid action."""
        animal = Animal(10, 15)
        
        with pytest.raises(ValueError):
            animal.execute_action('invalid_action')
    
    def test_dead_animal_actions(self):
        """Test that dead animals cannot execute actions."""
        animal = Animal(10, 15)
        animal.alive = False
        
        decision = animal.make_decision()
        probabilities = animal.get_action_probabilities()
        success = animal.execute_action('move')
        
        assert decision == 'rest'
        assert probabilities == {'move': 0.0, 'eat': 0.0, 'drink': 0.0, 'rest': 1.0}
        assert success == False
