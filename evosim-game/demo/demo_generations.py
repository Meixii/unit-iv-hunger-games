"""
Demo: Run multiple generations with evolution.

Initializes world and population, runs a few generations, evolving between them,
and prints concise stats.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation_controller import create_simulation_controller


def main():
    controller = create_simulation_controller(max_weeks=5, max_generations=3, population_size=12, random_seed=42)
    controller.initialize_world()
    controller.initialize_population()
    results = controller.run_generations(num_generations=3, weeks_per_generation=5)

    print("\n=== Summary ===")
    for r in results:
        print(f"Gen {r['generation']}: weeks={r['weeks_completed']}, survivors={r['survivors']}, casualties={r['casualties']}, extinction={r['extinction']}")


if __name__ == "__main__":
    main()


