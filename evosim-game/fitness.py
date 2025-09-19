"""
Fitness measurement helpers.

Tracks and computes fitness score components per documentation:
Time, Resource, Kill, Distance, Event.
"""

from __future__ import annotations

from typing import Dict

import constants
from data_structures import Animal


def init_fitness_components(animal: Animal) -> None:
    if not animal.fitness_score_components:
        animal.fitness_score_components = {
            'Time': 0.0,
            'Resource': 0.0,
            'Kill': 0.0,
            'Distance': 0.0,
            'Event': 0.0,
        }


def increment_time(animal: Animal, turns: int = 1) -> None:
    init_fitness_components(animal)
    animal.fitness_score_components['Time'] += float(turns)


def add_distance(animal: Animal, tiles: float) -> None:
    init_fitness_components(animal)
    animal.fitness_score_components['Distance'] += float(tiles)


def add_resource_units(animal: Animal, amount: float) -> None:
    """Resources gathered measured in raw units (food/water)."""
    init_fitness_components(animal)
    animal.fitness_score_components['Resource'] += float(amount)


def add_kill(animal: Animal, count: int = 1) -> None:
    init_fitness_components(animal)
    animal.fitness_score_components['Kill'] += float(count)


def add_event_survived(animal: Animal, count: int = 1) -> None:
    init_fitness_components(animal)
    animal.fitness_score_components['Event'] += float(count)


