"""
Demo: Phase 1 (Decision) + Phase 2 (Status)

Runs a small scenario to show Decision and Status phases without executing actions.
Prints a concise log of planned actions and status changes.
"""

import sys
import os
from pprint import pprint

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures import Simulation, World, Tile, TerrainType, Animal, AnimalCategory
from action_resolution import DecisionEngine, StatusEngine


def build_small_world():
    grid = []
    for y in range(3):
        row = []
        for x in range(3):
            terrain = TerrainType.PLAINS if (x, y) != (1, 1) else TerrainType.WATER
            row.append(Tile(coordinates=(x, y), terrain_type=terrain))
        grid.append(row)
    return World(grid=grid, dimensions=(3, 3))


def main():
    sim = Simulation()
    sim.world = build_small_world()

    # Two animals
    a1 = Animal(
        animal_id="demo_h",
        category=AnimalCategory.HERBIVORE,
        location=(0, 0),
        status={'Health': 100, 'Hunger': 55, 'Thirst': 65, 'Energy': 70},
        traits={'STR': 45, 'AGI': 60, 'INT': 50, 'END': 50, 'PER': 50}
    )
    a2 = Animal(
        animal_id="demo_c",
        category=AnimalCategory.CARNIVORE,
        location=(2, 2),
        status={'Health': 100, 'Hunger': 40, 'Thirst': 40, 'Energy': 50},
        traits={'STR': 70, 'AGI': 50, 'INT': 50, 'END': 50, 'PER': 50}
    )

    sim.world.get_tile(0, 0).occupant = a1
    sim.world.get_tile(2, 2).occupant = a2
    sim.add_animal(a1)
    sim.add_animal(a2)

    # Phase 1: Decision
    decision = DecisionEngine(sim, logger=type('L', (), {'debug':print, 'info':print, 'warning':print})())
    living = sim.get_living_animals()
    actions = decision.execute_decision_phase(living)

    print("\nPlanned Actions:")
    for act in actions:
        print(f"- {act.animal_id}: {act.action_type.value} target={act.target_location}")

    # Phase 2: Status
    status = StatusEngine(sim, logger=type('L', (), {'debug':print, 'info':print, 'warning':print})())
    before = {a.animal_id: dict(a.status) for a in living}
    results = status.execute_status_environmental_phase(living)
    after = {a.animal_id: dict(a.status) for a in living}

    print("\nStatus Phase Results:")
    pprint(results)

    print("\nStatus Changes:")
    for aid in before:
        b, a = before[aid], after[aid]
        print(f"{aid}: Hunger {b['Hunger']} -> {a['Hunger']}, Thirst {b['Thirst']} -> {a['Thirst']}, Energy {b['Energy']} -> {a['Energy']}, Health {b['Health']} -> {a['Health']}")


if __name__ == "__main__":
    main()


