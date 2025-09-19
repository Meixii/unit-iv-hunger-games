"""
Data logging utilities for AI/Evolution testing.

Provides helpers to summarize populations and generations into CSV-friendly rows
for later analysis (fitness, traits, categories, outcomes).
"""

from __future__ import annotations

from typing import Dict, Any, List
import csv
import os

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


def write_population_csv(path: str, generation_index: int, animals: List[Animal]) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
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


