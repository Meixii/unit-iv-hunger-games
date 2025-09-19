"""
Evolutionary Algorithm

Implements selection (elitism + tournament), one-point crossover on flattened
MLP parameters, and gaussian mutation. Produces a next-generation population.
"""

from __future__ import annotations

from typing import List, Tuple
import random

import constants
from data_structures import Animal, AnimalCategory, create_random_animal
from mlp import MLPNetwork


def _flatten_brain(animal: Animal) -> List[float]:
    if not getattr(animal, 'mlp_network', None):
        animal.mlp_network = MLPNetwork()
    return animal.mlp_network.get_parameters_flat()


def _set_brain_from_flat(animal: Animal, params: List[float]) -> None:
    if not getattr(animal, 'mlp_network', None):
        animal.mlp_network = MLPNetwork()
    animal.mlp_network.set_parameters_flat(params)


def select_parents_tournament(population: List[Animal], rng: random.Random) -> Tuple[Animal, Animal]:
    """Tournament selection to pick two parents based on fitness score."""
    size = max(2, constants.TOURNAMENT_SIZE)

    def tournament() -> Animal:
        contenders = rng.sample(population, min(size, len(population)))
        return max(contenders, key=lambda a: a.get_fitness_score())

    return tournament(), tournament()


def one_point_crossover(params_a: List[float], params_b: List[float], rng: random.Random) -> List[float]:
    if len(params_a) != len(params_b):
        raise ValueError("Parent parameter vectors must be same length")
    if len(params_a) == 0:
        return []
    cut = rng.randint(1, len(params_a) - 1)
    return params_a[:cut] + params_b[cut:]


def mutate(params: List[float], rng: random.Random, rate: float = None, sigma: float = 0.02) -> List[float]:
    r = constants.MUTATION_RATE if rate is None else rate
    out = []
    for p in params:
        if rng.random() < r:
            out.append(p + rng.gauss(0.0, sigma))
        else:
            out.append(p)
    return out


def evolve_population(parent_population: List[Animal], rng: random.Random | None = None) -> List[Animal]:
    """
    Create a next generation of animals using elitism + tournament selection,
    one-point crossover on MLP weights, and gaussian mutation.
    """
    if not parent_population:
        return []

    rnd = rng or random.Random()
    pop_size = len(parent_population)

    # Sort by fitness descending
    sorted_parents = sorted(parent_population, key=lambda a: a.get_fitness_score(), reverse=True)

    # Elitism: carry top elites unchanged
    elite_count = max(1, int(pop_size * constants.ELITE_PERCENTAGE))
    next_gen: List[Animal] = []
    for i in range(elite_count):
        parent = sorted_parents[i]
        child = create_random_animal(f"elite_{i}_{parent.animal_id}", parent.category)
        _set_brain_from_flat(child, _flatten_brain(parent))
        next_gen.append(child)

    # Fill remainder via crossover + mutation
    while len(next_gen) < pop_size:
        p1, p2 = select_parents_tournament(sorted_parents, rnd)

        # Child inherits category randomly from a parent for now (could be strategy-specific)
        child_category = rnd.choice([p1.category, p2.category])
        child = create_random_animal(f"child_{len(next_gen)}", child_category)

        w1 = _flatten_brain(p1)
        w2 = _flatten_brain(p2)
        crossed = one_point_crossover(w1, w2, rnd)
        mutated = mutate(crossed, rnd)
        _set_brain_from_flat(child, mutated)

        next_gen.append(child)

    return next_gen


