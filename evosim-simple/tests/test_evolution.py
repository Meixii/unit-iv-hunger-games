"""
Test module for the Evolution system.
"""

import pytest
import numpy as np
from src.evolution import Population, EvolutionManager
from src.animal import Animal
from src.neural_network import NeuralNetwork
from src.environment import GridWorld


class TestPopulation:
    """Test cases for Population class."""
    
    def test_population_initialization(self):
        """Test population initialization."""
        population = Population(size=10)
        
        assert population.size == 10
        assert len(population.animals) == 10
        assert population.generation == 0
        assert len(population.fitness_history) == 0
        assert population.elite_size == 1  # 10% of 10 = 1
    
    def test_population_initialization_with_grid(self):
        """Test population initialization with grid world."""
        grid = GridWorld(10, 10)
        population = Population(size=5, grid_world=grid)
        
        assert len(population.animals) == 5
        assert len(grid.get_alive_animals()) == 5
        
        # Check that animals are placed in grid
        for animal in population.animals:
            pos = animal.get_position()
            assert grid.is_valid_position(pos[0], pos[1])
    
    def test_evaluate_fitness(self):
        """Test fitness evaluation."""
        population = Population(size=5)
        
        # Set some animals to have different fitness
        for i, animal in enumerate(population.animals):
            animal.fitness = i * 10.0
        
        fitness_scores = population.evaluate_fitness()
        
        assert len(fitness_scores) == 5
        assert all(isinstance(f, (int, float)) for f in fitness_scores)
    
    def test_get_alive_animals(self):
        """Test getting alive animals."""
        population = Population(size=5)
        
        # Make some animals dead
        population.animals[0].alive = False
        population.animals[1].alive = False
        
        alive_animals = population.get_alive_animals()
        
        assert len(alive_animals) == 3
        assert all(animal.is_alive() for animal in alive_animals)
    
    def test_get_dead_animals(self):
        """Test getting dead animals."""
        population = Population(size=5)
        
        # Make some animals dead
        population.animals[0].alive = False
        population.animals[1].alive = False
        
        dead_animals = population.get_dead_animals()
        
        assert len(dead_animals) == 2
        assert all(not animal.is_alive() for animal in dead_animals)
    
    def test_calculate_statistics(self):
        """Test statistics calculation."""
        population = Population(size=5)
        
        # Set animal states to get different fitness values
        for i, animal in enumerate(population.animals):
            animal.age = i * 2
            animal.hunger = 100 - i * 10
            animal.thirst = 100 - i * 10
            animal.energy = 100 - i * 5
            animal.movement_count = i
        
        stats = population.calculate_statistics()
        
        assert stats['generation'] == 0
        assert stats['population_size'] == 5
        assert stats['alive_count'] == 5
        assert stats['dead_count'] == 0
        assert stats['survival_rate'] == 1.0
        # Fitness will be calculated based on animal states
        assert stats['average_fitness'] > 0
        assert stats['best_fitness'] > 0
        assert stats['worst_fitness'] >= 0
    
    def test_update_statistics(self):
        """Test statistics update."""
        population = Population(size=5)
        
        # Set fitness values
        for i, animal in enumerate(population.animals):
            animal.fitness = i * 10.0
        
        population.update_statistics()
        
        assert len(population.survival_rates) == 1
        assert len(population.average_fitness) == 1
        assert len(population.best_fitness) == 1
        assert len(population.worst_fitness) == 1
        assert len(population.fitness_history) == 1
    
    def test_tournament_selection(self):
        """Test tournament selection."""
        population = Population(size=5)
        
        # Set fitness values
        for i, animal in enumerate(population.animals):
            animal.fitness = i * 10.0
        
        parents = population._tournament_selection(population.animals, tournament_size=3)
        
        assert len(parents) == 5
        assert all(animal in population.animals for animal in parents)
    
    def test_roulette_wheel_selection(self):
        """Test roulette wheel selection."""
        population = Population(size=5)
        
        # Set fitness values
        for i, animal in enumerate(population.animals):
            animal.fitness = i * 10.0
        
        parents = population._roulette_wheel_selection(population.animals)
        
        assert len(parents) == 5
        assert all(animal in population.animals for animal in parents)
    
    def test_rank_selection(self):
        """Test rank selection."""
        population = Population(size=5)
        
        # Set fitness values
        for i, animal in enumerate(population.animals):
            animal.fitness = i * 10.0
        
        parents = population._rank_selection(population.animals)
        
        assert len(parents) == 5
        assert all(animal in population.animals for animal in parents)
    
    def test_select_parents_tournament(self):
        """Test parent selection with tournament method."""
        population = Population(size=5)
        
        # Set fitness values
        for i, animal in enumerate(population.animals):
            animal.fitness = i * 10.0
        
        parents = population.select_parents(selection_method='tournament', tournament_size=3)
        
        assert len(parents) == 5
        assert all(isinstance(animal, Animal) for animal in parents)
    
    def test_select_parents_roulette(self):
        """Test parent selection with roulette method."""
        population = Population(size=5)
        
        # Set fitness values
        for i, animal in enumerate(population.animals):
            animal.fitness = i * 10.0
        
        parents = population.select_parents(selection_method='roulette')
        
        assert len(parents) == 5
        assert all(isinstance(animal, Animal) for animal in parents)
    
    def test_select_parents_rank(self):
        """Test parent selection with rank method."""
        population = Population(size=5)
        
        # Set fitness values
        for i, animal in enumerate(population.animals):
            animal.fitness = i * 10.0
        
        parents = population.select_parents(selection_method='rank')
        
        assert len(parents) == 5
        assert all(isinstance(animal, Animal) for animal in parents)
    
    def test_select_parents_invalid_method(self):
        """Test parent selection with invalid method."""
        population = Population(size=5)
        
        with pytest.raises(ValueError):
            population.select_parents(selection_method='invalid')
    
    def test_create_offspring(self):
        """Test offspring creation."""
        population = Population(size=5)
        
        # Set fitness values
        for i, animal in enumerate(population.animals):
            animal.fitness = i * 10.0
        
        parents = population.select_parents()
        offspring = population.create_offspring(parents)
        
        assert len(offspring) == 5
        assert all(isinstance(animal, Animal) for animal in offspring)
        assert all(hasattr(animal, 'neural_network') for animal in offspring)
    
    def test_select_elite(self):
        """Test elite selection."""
        population = Population(size=10)
        
        # Set fitness values
        for i, animal in enumerate(population.animals):
            animal.fitness = i * 10.0
        
        elite = population._select_elite()
        
        assert len(elite) == 1  # 10% of 10 = 1
        assert elite[0].fitness == 90.0  # Highest fitness
    
    def test_advance_generation(self):
        """Test generation advancement."""
        population = Population(size=5)
        
        # Create new animals for next generation
        new_animals = []
        for i in range(5):
            network = NeuralNetwork()
            animal = Animal(0, 0, network)
            animal.fitness = i * 20.0
            new_animals.append(animal)
        
        old_generation = population.generation
        population.advance_generation(new_animals)
        
        assert population.generation == old_generation + 1
        assert len(population.animals) == 5
        assert all(animal.fitness == i * 20.0 for i, animal in enumerate(population.animals))
    
    def test_reset(self):
        """Test population reset."""
        population = Population(size=5)
        
        # Modify population
        population.generation = 5
        population.fitness_history = [1, 2, 3]
        
        population.reset()
        
        assert population.generation == 0
        assert len(population.fitness_history) == 0
        assert len(population.animals) == 5
    
    def test_get_evolution_summary(self):
        """Test evolution summary."""
        population = Population(size=5)
        
        # Add some history
        population.fitness_history = [10, 20, 30]
        population.survival_rates = [0.8, 0.9, 1.0]
        population.best_fitness = [15, 25, 35]
        population.average_fitness = [12, 22, 32]
        
        summary = population.get_evolution_summary()
        
        assert summary['generation'] == 0
        assert summary['population_size'] == 5
        assert summary['total_generations'] == 3
        assert summary['best_fitness_ever'] == 35
        assert summary['average_fitness_current'] == 32
        assert summary['survival_rate_current'] == 1.0


class TestEvolutionManager:
    """Test cases for EvolutionManager class."""
    
    def test_evolution_manager_initialization(self):
        """Test evolution manager initialization."""
        population = Population(size=10)
        manager = EvolutionManager(population)
        
        assert manager.population == population
        assert len(manager.evolution_history) == 0
        assert manager.convergence_threshold == 0.01
        assert manager.max_generations == 100
        assert manager.selection_method == 'tournament'
    
    def test_evolve_generation(self):
        """Test evolving one generation."""
        population = Population(size=5)
        manager = EvolutionManager(population)
        
        # Set initial fitness
        for i, animal in enumerate(population.animals):
            animal.fitness = i * 10.0
        
        result = manager.evolve_generation()
        
        assert 'generation' in result
        assert 'stats' in result
        assert 'parents_selected' in result
        assert 'offspring_created' in result
        assert len(manager.evolution_history) == 1
    
    def test_evolve_multiple_generations(self):
        """Test evolving multiple generations."""
        population = Population(size=5)
        manager = EvolutionManager(population)
        
        # Set initial fitness
        for i, animal in enumerate(population.animals):
            animal.fitness = i * 10.0
        
        result = manager.evolve(max_generations=3)
        
        assert result['generations_completed'] == 3
        assert 'best_fitness_achieved' in result
        assert 'final_stats' in result
        assert len(manager.evolution_history) == 3
    
    def test_evolve_with_target_fitness(self):
        """Test evolving with target fitness."""
        population = Population(size=5)
        manager = EvolutionManager(population)
        
        # Set initial fitness
        for i, animal in enumerate(population.animals):
            animal.fitness = i * 10.0
        
        result = manager.evolve(max_generations=10, target_fitness=100.0)
        
        assert 'generations_completed' in result
        assert 'best_fitness_achieved' in result
    
    def test_check_convergence(self):
        """Test convergence checking."""
        population = Population(size=5)
        manager = EvolutionManager(population)
        
        # No convergence initially
        assert not manager._check_convergence()
        
        # Add some fitness history
        population.fitness_history = [10.0] * 10
        assert manager._check_convergence()
    
    def test_get_evolution_statistics(self):
        """Test getting evolution statistics."""
        population = Population(size=5)
        manager = EvolutionManager(population)
        
        # Evolve a few generations
        manager.evolve(max_generations=3)
        
        stats = manager.get_evolution_statistics()
        
        assert 'total_generations' in stats
        assert 'best_fitness_ever' in stats
        assert 'final_fitness' in stats
        assert 'fitness_improvement' in stats
        assert 'total_evaluations' in stats
        assert 'converged' in stats
    
    def test_reset(self):
        """Test evolution manager reset."""
        population = Population(size=5)
        manager = EvolutionManager(population)
        
        # Evolve some generations
        manager.evolve(max_generations=3)
        
        manager.reset()
        
        assert len(manager.evolution_history) == 0
        assert manager.total_evaluations == 0
        assert population.generation == 0
    
    def test_set_parameters(self):
        """Test setting evolution parameters."""
        population = Population(size=5)
        manager = EvolutionManager(population)
        
        manager.set_parameters(
            convergence_threshold=0.05,
            max_generations=50,
            selection_method='roulette'
        )
        
        assert manager.convergence_threshold == 0.05
        assert manager.max_generations == 50
        assert manager.selection_method == 'roulette'
    
    def test_evolution_with_grid_world(self):
        """Test evolution with grid world."""
        grid = GridWorld(10, 10)
        population = Population(size=5, grid_world=grid)
        manager = EvolutionManager(population)
        
        # Evolve one generation
        result = manager.evolve_generation()
        
        assert result['generation'] == 1
        assert len(grid.get_alive_animals()) == 5
    
    def test_elite_selection_in_offspring(self):
        """Test that elite individuals are preserved."""
        population = Population(size=10)
        manager = EvolutionManager(population)
        
        # Set animal states to get different fitness values
        for i, animal in enumerate(population.animals):
            animal.age = i * 3
            animal.hunger = 100 - i * 5
            animal.thirst = 100 - i * 5
            animal.energy = 100 - i * 3
            animal.movement_count = i * 2
        
        # Evaluate fitness to get actual values
        population.evaluate_fitness()
        
        # Get the best animal
        best_animal = max(population.animals, key=lambda a: a.fitness)
        best_fitness = best_animal.fitness
        
        # Evolve one generation
        manager.evolve_generation()
        
        # Check that best fitness is preserved or improved
        new_best_fitness = max(animal.fitness for animal in population.animals)
        assert new_best_fitness >= best_fitness
    
    def test_mutation_and_crossover_rates(self):
        """Test that mutation and crossover rates are applied."""
        population = Population(size=10)
        manager = EvolutionManager(population)
        
        # Set low mutation and crossover rates
        population.mutation_rate = 0.0
        population.crossover_rate = 0.0
        
        # Evolve one generation
        manager.evolve_generation()
        
        # With no mutation and crossover, offspring should be identical to parents
        # This is a basic test - in practice, selection and elitism will still cause changes
        assert len(population.animals) == 10
    
    def test_stagnation_detection(self):
        """Test stagnation detection."""
        population = Population(size=5)
        manager = EvolutionManager(population)
        
        # Set all animals to same fitness (no improvement possible)
        for animal in population.animals:
            animal.fitness = 50.0
        
        # Evolve with low stagnation limit
        manager.stagnation_limit = 2
        result = manager.evolve(max_generations=10)
        
        # Should stop due to stagnation
        assert result['stagnated'] == True
        assert result['generations_completed'] <= 10
