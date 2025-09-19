"""
Demo: Run multiple generations and log population summaries to CSV.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation_controller import create_simulation_controller
from logging_utils import write_population_csv


def main():
    out_csv = os.path.join(os.path.dirname(__file__), 'runs', 'population_summary.csv')
    controller = create_simulation_controller(max_weeks=5, max_generations=3, population_size=20, random_seed=123)
    controller.initialize_world()
    controller.initialize_population()

    # Log initial population as generation 0 pre-run
    write_population_csv(out_csv, 0, controller.simulation.get_living_animals())

    results = controller.run_generations(num_generations=3, weeks_per_generation=5)

    # After each generation in results, the controller already evolved; log post-generation populations
    # We log final population after the last evolution step as well
    gen_index = 1
    for _ in results:
        write_population_csv(out_csv, gen_index, controller.simulation.get_living_animals())
        gen_index += 1

    print(f"Logs written to: {out_csv}")


if __name__ == "__main__":
    main()


