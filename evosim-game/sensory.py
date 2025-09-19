"""
Sensory Input Vector Builder (41 nodes)

Builds the normalized input vector for an animal's MLP based on:
- Internal status (5): Health%, Hunger%, Thirst%, Energy%, Instinct (0/1)
- Local 3x3 neighborhood (9 tiles × 4): [threat, food, water, animal]
"""

from __future__ import annotations

from typing import List, Tuple

from data_structures import Simulation, Animal, TerrainType, ResourceType


def _clamp01(x: float) -> float:
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def build_input_vector(simulation: Simulation, animal: Animal) -> List[float]:
    """
    Construct a 41-length input vector for the given animal.

    Order:
    - 5 internal: [health_pct, hunger_pct, thirst_pct, energy_pct, instinct]
    - 9 tiles × 4 features per tile in row-major scan of neighborhood centered on animal:
      For each tile: [threat, food, water, animal_present]
    """
    # Internal 5
    health_max = float(max(1, animal.get_max_health()))
    energy_max = float(max(1, animal.get_max_energy()))
    health_pct = _clamp01(float(animal.status.get('Health', 0.0)) / health_max)
    hunger_pct = _clamp01(float(animal.status.get('Hunger', 0.0)) / 100.0)
    thirst_pct = _clamp01(float(animal.status.get('Thirst', 0.0)) / 100.0)
    energy_pct = _clamp01(float(animal.status.get('Energy', 0.0)) / energy_max)
    instinct = 1.0 if float(animal.status.get('Instinct', 0.0)) >= 0.5 else 0.0

    inputs: List[float] = [health_pct, hunger_pct, thirst_pct, energy_pct, instinct]

    # 3x3 neighborhood
    world = simulation.world
    ax, ay = animal.location
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            tx, ty = ax + dx, ay + dy
            threat = 0.0
            food = 0.0
            water = 0.0
            animal_present = 0.0

            tile = None
            if world and world.is_valid_coordinate(tx, ty):
                tile = world.get_tile(tx, ty)

            if tile:
                # Threat: simplistic heuristic (water center considered non-passable but not a threat)
                if tile.terrain_type in [TerrainType.MOUNTAINS]:
                    threat = 1.0

                # Food/Water detection
                res = getattr(tile, 'resource', None)
                if res and res.uses_left > 0:
                    if res.resource_type in [ResourceType.PLANT, ResourceType.PREY, ResourceType.CARCASS]:
                        food = 1.0
                    if res.resource_type == ResourceType.WATER:
                        water = 1.0

                # Animal presence
                if tile.occupant is not None and tile.occupant != animal:
                    animal_present = 1.0

            inputs.extend([threat, food, water, animal_present])

    # Ensure length is exactly 41
    if len(inputs) != 41:
        raise AssertionError(f"Sensory vector length is {len(inputs)}, expected 41")

    return inputs


