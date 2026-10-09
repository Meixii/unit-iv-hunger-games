"""
EvoSim - Test and Simulation Runner Entry Point
Runs either the unit test suite or quick headless/GUI simulation tests.
"""

import sys
import os
import argparse

# Add package root to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_unit_tests():
    """Run the comprehensive EvoSim unit test suite."""
    from test.test_runner import run_all_tests
    return run_all_tests()


def run_headless_simulation():
    """Run a fast multi-generation headless simulation to verify game loop."""
    from simulation_controller import SimulationController
    from config import SimulationConfig
    import constants

    print("🚀 Running quick headless simulation verification...")
    config = SimulationConfig(max_generations=2, max_weeks=4, population_size=12)
    controller = SimulationController(config=config)
    controller.initialize_world()
    controller.initialize_population()
    results = controller.run_generations(num_generations=2, weeks_per_generation=4)
    status = controller.get_simulation_status()
    print("✅ Headless simulation complete!")
    print(f"Generations Run: {len(results)}")
    print(f"Current Gen: {status['current_generation']}")
    print(f"Living Animals: {status['living_animals']}")
    print(f"Dead Animals: {status['dead_animals']}")
    return len(results) == 2


def run_gui_config():
    """Run configuration GUI window."""
    from config import run_config_gui
    return run_config_gui("config.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EvoSim Test & Simulation Runner")
    parser.add_argument("--sim", action="store_true", help="Run quick headless simulation verification")
    parser.add_argument("--gui", action="store_true", help="Launch Tkinter Config GUI")
    args = parser.parse_args()

    if args.gui:
        run_gui_config()
    elif args.sim:
        run_headless_simulation()
    else:
        exit_code = run_unit_tests()
        sys.exit(exit_code)