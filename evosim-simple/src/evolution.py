"""
Evolutionary Algorithm System for Evolutionary Simulation

This module implements the evolutionary algorithm components including
population management, selection, crossover, mutation, and evolution tracking.

Author: Zen Garden
University of Caloocan City
"""

import random
import numpy as np
from typing import List, Dict, Tuple, Optional
from .animal import Animal
from .neural_network import NeuralNetwork


class Population:
    """
    Manages a population of animals for evolutionary simulation.
    
    Handles:
    - Population initialization and management
    - Fitness evaluation and tracking
    - Generation advancement
    - Statistics collection
    """
    
    def __init__(self, size: int = 50, grid_world=None):
        """
        Initialize a population of animals.
        
        Args:
            size: Population size
            grid_world: GridWorld instance for animal placement
        """
        self.size = size
        self.animals: List[Animal] = []
        self.generation = 0
        self.grid_world = grid_world
        
        # Statistics tracking
        self.fitness_history: List[float] = []
        self.survival_rates: List[float] = []
        self.average_fitness: List[float] = []
        self.best_fitness: List[float] = []
        self.worst_fitness: List[float] = []
        
        # Evolution parameters
        self.elite_size = max(1, size // 10)  # Top 10% for elitism
        self.mutation_rate = 0.1
        self.crossover_rate = 0.8
        self.mutation_strength = 0.1
        
        # Initialize population
        self._initialize_population()
    
    def _initialize_population(self) -> None:
        """Initialize the population with random animals."""
        self.animals.clear()
        
        for i in range(self.size):
            # --- FIX: Create neural network with 5 inputs ---
            network = NeuralNetwork(input_size=5)
            # --- End of fix ---
            
            # Create animal
            animal = Animal(0, 0, network)
            
            # Place in grid world if available
            if self.grid_world is not None:
                empty_positions = self.grid_world.get_empty_positions()
                if empty_positions:
                    pos = random.choice(empty_positions)
                    self.grid_world.add_animal(animal, pos[0], pos[1])
            
            self.animals.append(animal)
    
    def evaluate_fitness(self) -> List[float]:
        """
        Evaluate fitness of all animals in the population.
        
        Returns:
            List of fitness scores
        """
        fitness_scores = []
        
        for animal in self.animals:
            if animal.is_alive():
                fitness = animal.calculate_fitness()
                animal.fitness = fitness
                fitness_scores.append(fitness)
            else:
                fitness_scores.append(0.0)
        
        return fitness_scores
    
    def get_alive_animals(self) -> List[Animal]:
        """
        Get all alive animals in the population.
        
        Returns:
            List of alive animals
        """
        return [animal for animal in self.animals if animal.is_alive()]
    
    def get_dead_animals(self) -> List[Animal]:
        """
        Get all dead animals in the population.
        
        Returns:
            List of dead animals
        """
        return [animal for animal in self.animals if not animal.is_alive()]
    
    def calculate_statistics(self) -> Dict:
        """
        Calculate population statistics.
        
        Returns:
            Dictionary with population statistics
        """
        alive_animals = self.get_alive_animals()
        fitness_scores = self.evaluate_fitness()
        
        # Get dead animals from environment if available
        dead_count = 0
        if self.grid_world and hasattr(self.grid_world, 'dead_animals'):
            dead_count = len(self.grid_world.dead_animals)
        
        if not fitness_scores:
            return {
                'generation': self.generation,
                'population_size': len(self.animals),
                'alive_count': 0,
                'dead_count': dead_count,
                'survival_rate': 0.0,
                'average_fitness': 0.0,
                'best_fitness': 0.0,
                'worst_fitness': 0.0,
                'fitness_std': 0.0
            }
        
        alive_fitness = [f for f in fitness_scores if f > 0]
        
        stats = {
            'generation': self.generation,
            'population_size': len(self.animals),
            'alive_count': len(alive_animals),
            'dead_count': dead_count,
            'survival_rate': len(alive_animals) / len(self.animals) if len(self.animals) > 0 else 0.0,
            'average_fitness': np.mean(fitness_scores),
            'best_fitness': np.max(fitness_scores),
            'worst_fitness': np.min(fitness_scores),
            'fitness_std': np.std(fitness_scores)
        }
        
        if alive_fitness:
            stats['alive_average_fitness'] = np.mean(alive_fitness)
            stats['alive_best_fitness'] = np.max(alive_fitness)
            stats['alive_worst_fitness'] = np.min(alive_fitness)
        else:
            stats['alive_average_fitness'] = 0.0
            stats['alive_best_fitness'] = 0.0
            stats['alive_worst_fitness'] = 0.0
        
        # Add behavioral statistics
        total_moves = sum(animal.behavioral_counts.get('move', 0) for animal in self.animals)
        total_eats = sum(animal.behavioral_counts.get('eat', 0) for animal in self.animals)
        total_drinks = sum(animal.behavioral_counts.get('drink', 0) for animal in self.animals)
        total_rests = sum(animal.behavioral_counts.get('rest', 0) for animal in self.animals)
        
        stats['total_moves'] = total_moves
        stats['total_eats'] = total_eats
        stats['total_drinks'] = total_drinks
        stats['total_rests'] = total_rests
        
        return stats
    
    def update_statistics(self) -> None:
        """Update population statistics and history."""
        stats = self.calculate_statistics()
        
        self.survival_rates.append(stats['survival_rate'])
        self.average_fitness.append(stats['average_fitness'])
        self.best_fitness.append(stats['best_fitness'])
        self.worst_fitness.append(stats['worst_fitness'])
        
        # Store fitness history for alive animals
        alive_fitness = [animal.fitness for animal in self.get_alive_animals()]
        if alive_fitness:
            self.fitness_history.append(np.mean(alive_fitness))
        else:
            self.fitness_history.append(0.0)
    
    def select_parents(self, selection_method: str = 'tournament', tournament_size: int = 3) -> List[Animal]:
        """
        Select parents for reproduction.
        
        Args:
            selection_method: Method for parent selection ('tournament', 'roulette', 'rank')
            tournament_size: Size of tournament for tournament selection
            
        Returns:
            List of selected parent animals
        """
        alive_animals = self.get_alive_animals()
        
        if len(alive_animals) < 2:
            # If not enough alive animals, use all animals
            alive_animals = self.animals
        
        if selection_method == 'tournament':
            return self._tournament_selection(alive_animals, tournament_size)
        elif selection_method == 'roulette':
            return self._roulette_wheel_selection(alive_animals)
        elif selection_method == 'rank':
            return self._rank_selection(alive_animals)
        else:
            raise ValueError(f"Unknown selection method: {selection_method}")
    
    def _tournament_selection(self, animals: List[Animal], tournament_size: int) -> List[Animal]:
        """Tournament selection for parent selection."""
        parents = []
        
        for _ in range(self.size):
            # Select random tournament
            tournament = random.sample(animals, min(tournament_size, len(animals)))
            
            # Select best from tournament
            best_animal = max(tournament, key=lambda a: a.fitness)
            parents.append(best_animal)
        
        return parents
    
    def _roulette_wheel_selection(self, animals: List[Animal]) -> List[Animal]:
        """Roulette wheel selection for parent selection."""
        fitness_scores = [animal.fitness for animal in animals]
        
        # Handle negative fitness scores
        min_fitness = min(fitness_scores)
        if min_fitness < 0:
            fitness_scores = [f - min_fitness + 1 for f in fitness_scores]
        
        total_fitness = sum(fitness_scores)
        if total_fitness == 0:
            # If all fitness is 0, select randomly
            return random.choices(animals, k=self.size)
        
        # Calculate selection probabilities
        probabilities = [f / total_fitness for f in fitness_scores]
        
        # Select parents
        parents = random.choices(animals, weights=probabilities, k=self.size)
        return parents
    
    def _rank_selection(self, animals: List[Animal]) -> List[Animal]:
        """Rank-based selection for parent selection."""
        # Sort animals by fitness
        sorted_animals = sorted(animals, key=lambda a: a.fitness, reverse=True)
        
        # Assign ranks (higher rank = better fitness)
        ranks = list(range(1, len(sorted_animals) + 1))
        
        # Calculate selection probabilities based on ranks
        total_rank = sum(ranks)
        probabilities = [r / total_rank for r in ranks]
        
        # Select parents
        parents = random.choices(sorted_animals, weights=probabilities, k=self.size)
        return parents
    
    def create_offspring(self, parents: List[Animal]) -> List[Animal]:
        """
        Create offspring from selected parents.
        
        Args:
            parents: List of parent animals
            
        Returns:
            List of offspring animals
        """
        offspring = []
        
        # --- FIX: Elitism - Create NEW animals with elite brains ---
        elite_animals = self._select_elite()
        for elite in elite_animals:
            # Create a fresh clone with the elite's brain
            new_elite_brain = elite.neural_network.copy()
            new_elite = Animal(0, 0, new_elite_brain, 
                             generation=self.generation + 1)
            offspring.append(new_elite)
        # --- End of fix ---
        
        # Create remaining offspring through crossover and mutation
        remaining_size = self.size - len(offspring)
        
        for i in range(remaining_size):
            # Select two parents
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            
            # Create offspring through crossover
            if random.random() < self.crossover_rate:
                offspring_network = parent1.neural_network.crossover(
                    parent2.neural_network, 
                    crossover_rate=0.5
                )
            else:
                # No crossover, copy parent1's network
                offspring_network = parent1.neural_network.copy()
            
            # Apply mutation
            if random.random() < self.mutation_rate:
                offspring_network.mutate(
                    mutation_rate=0.1, 
                    mutation_strength=self.mutation_strength
                )
            
            # Create offspring animal with proper generation tracking
            offspring_animal = Animal(0, 0, offspring_network, 
                                     generation=self.generation + 1)
            offspring.append(offspring_animal)
        
        return offspring
    
    def _select_elite(self) -> List[Animal]:
        """Select elite individuals for elitism."""
        alive_animals = self.get_alive_animals()
        
        if not alive_animals:
            return []
        
        # Sort by fitness and select top individuals
        sorted_animals = sorted(alive_animals, key=lambda a: a.fitness, reverse=True)
        elite_count = min(self.elite_size, len(sorted_animals))
        
        return sorted_animals[:elite_count]
    
    def advance_generation(self, new_animals: List[Animal]) -> None:
        """
        Advance to the next generation with new animals.
        
        Args:
            new_animals: List of new animals for the next generation
        """
        # Remove old animals from grid world
        if self.grid_world is not None:
            for animal in self.animals:
                self.grid_world.remove_animal(animal)
        
        # Update population
        self.animals = new_animals[:self.size]  # Ensure correct population size
        # Note: Generation counter is now managed by the simulation
        # self.generation += 1  # Removed - simulation manages this
        
        # Place new animals in grid world
        if self.grid_world is not None:
            for animal in self.animals:
                empty_positions = self.grid_world.get_empty_positions()
                if empty_positions:
                    pos = random.choice(empty_positions)
                    self.grid_world.add_animal(animal, pos[0], pos[1])
    
    def reset(self) -> None:
        """Reset the population to initial state."""
        self.animals.clear()
        self.generation = 0
        self.fitness_history.clear()
        self.survival_rates.clear()
        self.average_fitness.clear()
        self.best_fitness.clear()
        self.worst_fitness.clear()
        self._initialize_population()
    
    def get_evolution_summary(self) -> Dict:
        """
        Get summary of evolution progress.
        
        Returns:
            Dictionary with evolution summary
        """
        return {
            'generation': self.generation,
            'population_size': len(self.animals),
            'total_generations': len(self.fitness_history),
            'fitness_trend': self.fitness_history[-10:] if self.fitness_history else [],
            'survival_trend': self.survival_rates[-10:] if self.survival_rates else [],
            'best_fitness_ever': max(self.best_fitness) if self.best_fitness else 0.0,
            'average_fitness_current': self.average_fitness[-1] if self.average_fitness else 0.0,
            'survival_rate_current': self.survival_rates[-1] if self.survival_rates else 0.0
        }
    
    def __str__(self) -> str:
        """String representation of the population."""
        alive_count = len(self.get_alive_animals())
        return f"Population(generation={self.generation}, size={len(self.animals)}, alive={alive_count})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the population."""
        return self.__str__()


class EvolutionManager:
    """
    Manages the evolutionary process and coordinates population evolution.
    
    Handles:
    - Evolution process control
    - Convergence detection
    - Termination conditions
    - Evolution statistics
    """
    
    def __init__(self, population: Population):
        """
        Initialize the evolution manager.
        
        Args:
            population: Population to manage
        """
        self.population = population
        self.evolution_history: List[Dict] = []
        self.convergence_threshold = 0.01  # Fitness improvement threshold
        self.max_generations = 100
        self.min_generations = 5
        self.stagnation_limit = 20  # Generations without improvement
        
        # Evolution parameters
        self.selection_method = 'tournament'
        self.tournament_size = 3
        self.elite_percentage = 0.1
        
        # Statistics
        self.start_time = None
        self.end_time = None
        self.total_evaluations = 0
    
    def evolve_generation(self) -> Dict:
        """
        Evolve one generation.
        
        Returns:
            Dictionary with generation results
        """
        # Evaluate current population
        fitness_scores = self.population.evaluate_fitness()
        self.total_evaluations += len(fitness_scores)
        
        # Update statistics
        self.population.update_statistics()
        stats = self.population.calculate_statistics()
        
        # Select parents
        parents = self.population.select_parents(
            selection_method=self.selection_method,
            tournament_size=self.tournament_size
        )
        
        # Create offspring
        offspring = self.population.create_offspring(parents)
        
        # Advance generation
        self.population.advance_generation(offspring)
        
        # Store generation results
        generation_result = {
            'generation': self.population.generation,
            'stats': stats,
            'parents_selected': len(parents),
            'offspring_created': len(offspring)
        }
        
        self.evolution_history.append(generation_result)
        return generation_result
    
    def evolve(self, max_generations: int = None, target_fitness: float = None) -> Dict:
        """
        Evolve the population for multiple generations.
        
        Args:
            max_generations: Maximum number of generations to evolve
            target_fitness: Target fitness to reach
            
        Returns:
            Dictionary with evolution results
        """
        if max_generations is None:
            max_generations = self.max_generations
        
        generation = 0
        stagnation_count = 0
        best_fitness = 0.0
        
        while generation < max_generations:
            # Evolve one generation
            result = self.evolve_generation()
            generation = result['generation']
            
            current_fitness = result['stats']['best_fitness']
            
            # Check for improvement
            if current_fitness > best_fitness:
                best_fitness = current_fitness
                stagnation_count = 0
            else:
                stagnation_count += 1
            
            # Check termination conditions
            if target_fitness and current_fitness >= target_fitness:
                break
            
            if stagnation_count >= self.stagnation_limit:
                break
            
            # Check convergence
            if self._check_convergence():
                break
        
        return {
            'generations_completed': generation,
            'best_fitness_achieved': best_fitness,
            'final_stats': result['stats'],
            'converged': self._check_convergence(),
            'stagnated': stagnation_count >= self.stagnation_limit
        }
    
    def _check_convergence(self) -> bool:
        """
        Check if the population has converged.
        
        Returns:
            True if converged, False otherwise
        """
        if len(self.population.fitness_history) < 10:
            return False
        
        # Check if fitness improvement is below threshold
        recent_fitness = self.population.fitness_history[-10:]
        fitness_improvement = max(recent_fitness) - min(recent_fitness)
        
        return fitness_improvement < self.convergence_threshold
    
    def get_evolution_statistics(self) -> Dict:
        """
        Get comprehensive evolution statistics.
        
        Returns:
            Dictionary with evolution statistics
        """
        if not self.evolution_history:
            return {}
        
        # Calculate trends
        fitness_trend = [gen['stats']['best_fitness'] for gen in self.evolution_history]
        survival_trend = [gen['stats']['survival_rate'] for gen in self.evolution_history]
        
        return {
            'total_generations': len(self.evolution_history),
            'best_fitness_ever': max(fitness_trend) if fitness_trend else 0.0,
            'final_fitness': fitness_trend[-1] if fitness_trend else 0.0,
            'fitness_improvement': fitness_trend[-1] - fitness_trend[0] if len(fitness_trend) > 1 else 0.0,
            'average_survival_rate': np.mean(survival_trend) if survival_trend else 0.0,
            'total_evaluations': self.total_evaluations,
            'converged': self._check_convergence(),
            'fitness_trend': fitness_trend,
            'survival_trend': survival_trend
        }
    
    def reset(self) -> None:
        """Reset the evolution manager."""
        self.evolution_history.clear()
        self.total_evaluations = 0
        self.population.reset()
    
    def set_parameters(self, **kwargs) -> None:
        """
        Set evolution parameters.
        
        Args:
            **kwargs: Parameter name-value pairs
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            elif hasattr(self.population, key):
                setattr(self.population, key, value)
    
    def __str__(self) -> str:
        """String representation of the evolution manager."""
        return f"EvolutionManager(generations={len(self.evolution_history)}, population={self.population})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the evolution manager."""
        return self.__str__()
