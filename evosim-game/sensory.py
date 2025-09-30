"""
Sensory System

Provides field-of-view (vision) utilities and the input vector builder used by
the Decision Engine's MLP. Vision radius varies per animal category:
- Herbivore: 3x3 (radius=1)
- Omnivore: 5x5 (radius=2)
- Carnivore: 7x7 (radius=3)

The MLP expects a fixed-length input vector of size constants.INPUT_NODES.
We map variable-radius vision to a fixed 3x3 directional sample by, for each
of the 8 directions and the center, selecting the first visible tile along
that direction within the animal's vision radius and extracting features.
"""

from __future__ import annotations

from typing import List, Tuple, Optional

import constants
from data_structures import Simulation, Animal, AnimalCategory, TerrainType, ResourceType, Tile


# -----------------------------------------------------------------------------
# Vision radius per category
# -----------------------------------------------------------------------------

def get_vision_radius(category: AnimalCategory) -> int:
    if category == AnimalCategory.HERBIVORE:
        return 1  # 3x3
    if category == AnimalCategory.OMNIVORE:
        return 2  # 5x5
    if category == AnimalCategory.CARNIVORE:
        return 3  # 7x7
    return 1


def get_visible_coordinates(sim: Simulation, center: Tuple[int, int], radius: int) -> List[Tuple[int, int]]:
    if not sim.world:
        return []
    cx, cy = center
    w, h = sim.world.dimensions
    coords: List[Tuple[int, int]] = []
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            x, y = cx + dx, cy + dy
            if 0 <= x < w and 0 <= y < h:
                coords.append((x, y))
    return coords


def get_visible_tiles(sim: Simulation, animal: Animal) -> List[Tile]:
    """Return tiles within the animal's vision radius (square area)."""
    if not sim.world or not animal.location:
        return []
    radius = get_vision_radius(animal.category)
    tiles: List[Tile] = []
    for (x, y) in get_visible_coordinates(sim, animal.location, radius):
        t = sim.world.get_tile(x, y)
        if t:
            tiles.append(t)
    return tiles


# -----------------------------------------------------------------------------
# Input vector (fixed length)
# -----------------------------------------------------------------------------

def build_input_vector(sim: Simulation, animal: Animal) -> List[float]:
    """
    Build the MLP input vector:
      - 5 internal signals: health, hunger, thirst, energy, instinct (all 0..1)
      - 9 directional samples (center + 8 compass directions) × 4 features each
    Total length = 5 + 9*4 = 41 (as defined in constants.INPUT_NODES)

    For each of the 9 positions, we look along that direction (or the center)
    up to the animal's vision radius and take the first in-bounds tile.
    If none is found, zeros are used for that position.
    """
    v: List[float] = []

    # ---- Internal signals (normalized 0..1) ----
    health = _clamp01(animal.status.get('Health', 0) / max(animal.get_max_health(), 1))
    hunger = _clamp01(animal.status.get('Hunger', 0) / 100.0)
    thirst = _clamp01(animal.status.get('Thirst', 0) / 100.0)
    energy = _clamp01(animal.status.get('Energy', 0) / max(animal.get_max_energy(), 1))
    instinct = _clamp01(animal.status.get('Instinct', 0))
    v.extend([health, hunger, thirst, energy, instinct])

    # ---- 3x3 directional sampling within vision ----
    # Order: center, N, NE, E, SE, S, SW, W, NW
    directions: List[Tuple[int, int]] = [
        (0, 0),
        (0, -1), (1, -1), (1, 0), (1, 1),
        (0, 1), (-1, 1), (-1, 0), (-1, -1)
    ]

    radius = get_vision_radius(animal.category)
    cx, cy = animal.location

    for (dx, dy) in directions:
        tile = _first_visible_tile_along(sim, cx, cy, dx, dy, radius)
        v.extend(_tile_features(tile, animal))

    # Sanity: pad/trim to INPUT_NODES
    if len(v) < constants.INPUT_NODES:
        v.extend([0.0] * (constants.INPUT_NODES - len(v)))
    elif len(v) > constants.INPUT_NODES:
        v = v[:constants.INPUT_NODES]
    return v


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def _first_visible_tile_along(sim: Simulation, cx: int, cy: int, dx: int, dy: int, radius: int) -> Optional[Tile]:
    if not sim.world:
        return None
    if dx == 0 and dy == 0:
        return sim.world.get_tile(cx, cy)
    x, y = cx, cy
    for _ in range(radius):
        x += dx
        y += dy
        if not (0 <= x < sim.world.dimensions[0] and 0 <= y < sim.world.dimensions[1]):
            return None
        t = sim.world.get_tile(x, y)
        if t is not None:
            return t
    return None


def _tile_features(tile: Optional[Tile], viewer: Animal) -> List[float]:
    """
    Encode a tile into 4 features:
      1) terrain_index normalized (0..1)
      2) resource_index normalized (0..1) or 0 if none
      3) resource_uses normalized (0..1) based on a simple cap
      4) occupant_relation: 0 none, 0.5 same-category, 1.0 different-category
    """
    if tile is None:
        return [0.0, 0.0, 0.0, 0.0]

    # Terrain index
    terrain_names = constants.TERRAIN_TYPES
    terrain_idx = 0
    try:
        terrain_idx = terrain_names.index(tile.terrain_type.value)
    except Exception:
        terrain_idx = 0
    terrain_norm = _norm_index(terrain_idx, len(terrain_names))

    # Resource index and uses
    res_norm = 0.0
    uses_norm = 0.0
    res = getattr(tile, 'resource', None)
    if res is not None:
        res_names = constants.RESOURCE_TYPES
        try:
            res_idx = res_names.index(res.resource_type.value)
        except Exception:
            res_idx = 0
        res_norm = _norm_index(res_idx, len(res_names))
        # Normalize by simple cap to 10 uses for scaling
        uses_norm = _clamp01(float(getattr(res, 'uses_left', 0)) / 10.0)

    # Occupant relation
    occ = getattr(tile, 'occupant', None)
    if occ is None:
        relation = 0.0
    else:
        relation = 0.5 if occ.category == viewer.category else 1.0

    return [terrain_norm, res_norm, uses_norm, relation]


def _norm_index(idx: int, size: int) -> float:
    if size <= 1:
        return 0.0
    return _clamp01(idx / float(size - 1))


def _clamp01(v: float) -> float:
    return 0.0 if v < 0.0 else 1.0 if v > 1.0 else v


