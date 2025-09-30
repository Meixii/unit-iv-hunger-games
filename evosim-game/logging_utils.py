"""
Data logging utilities for AI/Evolution testing.

Provides helpers to summarize populations and generations into CSV-friendly rows
for later analysis (fitness, traits, categories, outcomes).
"""

from __future__ import annotations

from typing import Dict, Any, List
import csv
import os
import statistics

from data_structures import Animal


def summarize_animal(animal: Animal) -> Dict[str, Any]:
    comp = animal.fitness_score_components or {}
    return {
        'animal_id': animal.animal_id,
        'category': animal.category.value,
        'health': animal.status.get('Health', 0),
        'hunger': animal.status.get('Hunger', 0),
        'thirst': animal.status.get('Thirst', 0),
        'energy': animal.status.get('Energy', 0),
        'fitness': animal.get_fitness_score(),
        'time': comp.get('Time', 0.0),
        'resource': comp.get('Resource', 0.0),
        'kill': comp.get('Kill', 0.0),
        'distance': comp.get('Distance', 0.0),
        'event': comp.get('Event', 0.0),
        'STR': animal.traits.get('STR', 0),
        'AGI': animal.traits.get('AGI', 0),
        'INT': animal.traits.get('INT', 0),
        'END': animal.traits.get('END', 0),
        'PER': animal.traits.get('PER', 0),
    }


# Recommended color maps for UI overlays (category and terrain)
CATEGORY_COLORS = {
    'Herbivore': '#2ecc71',   # green
    'Carnivore': '#e74c3c',   # red
    'Omnivore':  '#3498db',   # blue
}

TERRAIN_COLORS = {
    'Plains':    '#d0d6db',  # light gray
    'Forest':    '#2ecc71',  # bright green
    'Jungle':    '#1abc9c',  # teal-green
    'Water':     '#3498db',  # blue
    'Swamp':     '#2c3e50',  # dark slate
    'Mountains': '#7f8c8d',  # mid gray
}


def write_population_csv(path: str, generation_index: int, animals: List[Animal]) -> str:
    # Ensure directory exists
    dir_path = os.path.dirname(path)
    if dir_path:  # Only create directory if there is one
        os.makedirs(dir_path, exist_ok=True)
    fieldnames = [
        'generation','animal_id','category','fitness','time','resource','kill','distance','event',
        'health','hunger','thirst','energy','STR','AGI','INT','END','PER'
    ]
    write_header = not os.path.exists(path)
    with open(path, 'a', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            w.writeheader()
        for a in animals:
            row = summarize_animal(a)
            row['generation'] = generation_index
            w.writerow(row)
    return path



def compute_generation_summary(generation_index: int, animals: List[Animal]) -> Dict[str, Any]:
    """Compute high-level KPIs for a generation from final animal states."""
    fitnesses = [a.get_fitness_score() for a in animals]
    by_cat: Dict[str, List[float]] = {'Herbivore': [], 'Carnivore': [], 'Omnivore': []}
    for a in animals:
        by_cat[a.category.value].append(a.get_fitness_score())
    def avg(lst: List[float]) -> float:
        return float(statistics.mean(lst)) if lst else 0.0
    best = max(animals, key=lambda a: a.get_fitness_score()) if animals else None
    return {
        'generation': generation_index,
        'count': len(animals),
        'avg_fitness': avg(fitnesses),
        'max_fitness': best.get_fitness_score() if best else 0.0,
        'max_fitness_id': best.animal_id if best else '',
        'avg_fitness_herbivore': avg(by_cat['Herbivore']),
        'avg_fitness_carnivore': avg(by_cat['Carnivore']),
        'avg_fitness_omnivore': avg(by_cat['Omnivore']),
    }


def write_generation_summary_csv(path: str, summary: Dict[str, Any]) -> str:
    """Append one summary row to a generations.csv file."""
    # Ensure directory exists
    dir_path = os.path.dirname(path)
    if dir_path:  # Only create directory if there is one
        os.makedirs(dir_path, exist_ok=True)
    fieldnames = [
        'generation','count','avg_fitness','max_fitness','max_fitness_id',
        'avg_fitness_herbivore','avg_fitness_carnivore','avg_fitness_omnivore'
    ]
    write_header = not os.path.exists(path)
    with open(path, 'a', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            w.writeheader()
        w.writerow(summary)
    return path

