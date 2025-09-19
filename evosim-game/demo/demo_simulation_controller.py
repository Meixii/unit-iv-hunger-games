"""
EvoSim Simulation Controller Demonstration

This script demonstrates the SimulationController functionality including:
- Controller initialization and configuration
- World and population initialization
- Simulation state management
- Status monitoring and validation
- Complete workflow demonstration

Reference: Task 2.1 - Main Simulation Controller from documentation.md
"""

import sys
import os
import time
from datetime import datetime

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation_controller import (
    SimulationController, SimulationConfig, create_simulation_controller
)
from world_generator import GenerationConfig
from data_structures import AnimalCategory


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def print_subsection(title: str):
    """Print a formatted subsection header."""
    print(f"\n--- {title} ---")


def demonstrate_controller_initialization():
    """Demonstrate controller initialization."""
    print_section("1. SIMULATION CONTROLLER INITIALIZATION")
    
    print_subsection("Default Configuration")
    controller1 = SimulationController()
    print(f"Default max weeks: {controller1.config.max_weeks}")
    print(f"Default max generations: {controller1.config.max_generations}")
    print(f"Default population size: {controller1.config.population_size}")
    print(f"Default logging enabled: {controller1.config.enable_logging}")
    
    print_subsection("Custom Configuration")
    custom_config = SimulationConfig(
        max_weeks=15,
        max_generations=5,
        population_size=12,
        enable_logging=True,
        log_level="DEBUG",
        random_seed=42
    )
    controller2 = SimulationController(custom_config)
    print(f"Custom max weeks: {controller2.config.max_weeks}")
    print(f"Custom max generations: {controller2.config.max_generations}")
    print(f"Custom population size: {controller2.config.population_size}")
    print(f"Custom logging enabled: {controller2.config.enable_logging}")
    print(f"Custom log level: {controller2.config.log_level}")
    print(f"Custom random seed: {controller2.config.random_seed}")
    
    print_subsection("Utility Function Creation")
    controller3 = create_simulation_controller(
        max_weeks=10,
        max_generations=3,
        population_size=8,
        random_seed=123,
        enable_logging=False
    )
    print(f"Created controller with {controller3.config.population_size} animals")
    print(f"Max weeks: {controller3.config.max_weeks}")
    print(f"Random seed: {controller3.config.random_seed}")
    
    return controller3


def demonstrate_world_initialization(controller: SimulationController):
    """Demonstrate world initialization."""
    print_section("2. WORLD INITIALIZATION")
    
    print_subsection("Default World Generation")
    world = controller.initialize_world()
    print(f"World created: {world.dimensions[0]}x{world.dimensions[1]} grid")
    print(f"Total tiles: {world.dimensions[0] * world.dimensions[1]}")
    
    # Get terrain statistics
    terrain_stats = controller._get_terrain_stats(world)
    print(f"Terrain distribution:")
    for terrain, count in terrain_stats.items():
        percentage = (count / (world.dimensions[0] * world.dimensions[1])) * 100
        print(f"  {terrain}: {count} tiles ({percentage:.1f}%)")
    
    print_subsection("Custom World Generation")
    custom_world_config = GenerationConfig(
        width=15,
        height=15,
        mountain_border=True
    )
    custom_world = controller.initialize_world(custom_world_config)
    print(f"Custom world created: {custom_world.dimensions[0]}x{custom_world.dimensions[1]} grid")
    print(f"Custom world total tiles: {custom_world.dimensions[0] * custom_world.dimensions[1]}")
    
    return world


def demonstrate_population_initialization(controller: SimulationController):
    """Demonstrate population initialization."""
    print_section("3. POPULATION INITIALIZATION")
    
    print_subsection("Default Population Generation")
    animals = controller.initialize_population()
    print(f"Population created: {len(animals)} animals")
    
    # Get category statistics
    category_stats = controller._get_category_stats(animals)
    print(f"Category distribution:")
    for category, count in category_stats.items():
        print(f"  {category}: {count} animals")
    
    print_subsection("Animal Details")
    for i, animal in enumerate(animals[:5]):  # Show first 5 animals
        print(f"Animal {i+1}: {animal.animal_id}")
        print(f"  Category: {animal.category.value}")
        print(f"  Location: {animal.location}")
        print(f"  Health: {animal.status['Health']:.1f}")
        print(f"  Hunger: {animal.status['Hunger']:.1f}")
        print(f"  Thirst: {animal.status['Thirst']:.1f}")
        print(f"  Energy: {animal.status['Energy']:.1f}")
        print(f"  Traits: STR={animal.traits['STR']}, AGI={animal.traits['AGI']}, "
              f"INT={animal.traits['INT']}, END={animal.traits['END']}, PER={animal.traits['PER']}")
        print()
    
    if len(animals) > 5:
        print(f"... and {len(animals) - 5} more animals")
    
    print_subsection("Custom Population Size")
    # Reset for custom population
    controller.reset_simulation()
    controller.initialize_world()
    
    custom_animals = controller.initialize_population(15)
    print(f"Custom population created: {len(custom_animals)} animals")
    
    custom_category_stats = controller._get_category_stats(custom_animals)
    print(f"Custom category distribution:")
    for category, count in custom_category_stats.items():
        print(f"  {category}: {count} animals")
    
    return animals


def demonstrate_simulation_control(controller: SimulationController):
    """Demonstrate simulation control functionality."""
    print_section("4. SIMULATION CONTROL")
    
    print_subsection("Starting Simulation")
    controller.start_simulation()
    print(f"Simulation started: {controller.is_running}")
    print(f"Simulation paused: {controller.is_paused}")
    print(f"Start time: {controller.simulation_start_time}")
    
    print_subsection("Pausing and Resuming")
    controller.pause_simulation()
    print(f"Simulation paused: {controller.is_paused}")
    
    controller.resume_simulation()
    print(f"Simulation resumed: {not controller.is_paused}")
    
    print_subsection("Stopping Simulation")
    controller.stop_simulation()
    print(f"Simulation stopped: {not controller.is_running}")
    print(f"End time: {controller.simulation_end_time}")
    
    if controller.simulation_start_time and controller.simulation_end_time:
        duration = controller.simulation_end_time - controller.simulation_start_time
        print(f"Simulation duration: {duration}")


def demonstrate_status_monitoring(controller: SimulationController):
    """Demonstrate status monitoring and validation."""
    print_section("5. STATUS MONITORING AND VALIDATION")
    
    print_subsection("Simulation Status")
    status = controller.get_simulation_status()
    print("Current simulation status:")
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    print_subsection("State Validation")
    is_valid = controller.validate_simulation_state()
    print(f"Simulation state is valid: {is_valid}")
    
    print_subsection("Detailed State Logging")
    print("Detailed simulation state:")
    controller.log_simulation_state()
    
    print_subsection("Statistics Tracking")
    generation_stats = controller.get_generation_stats()
    weekly_stats = controller.get_weekly_stats()
    
    print(f"Generation statistics: {len(generation_stats)} entries")
    print(f"Weekly statistics: {len(weekly_stats)} entries")
    
    # Add some mock statistics
    controller.generation_stats.append({
        'generation': 1,
        'max_fitness': 150.5,
        'avg_fitness': 75.2,
        'survivors': 8
    })
    controller.weekly_stats.append({
        'week': 1,
        'population': 12,
        'events': 3,
        'deaths': 0
    })
    
    updated_generation_stats = controller.get_generation_stats()
    updated_weekly_stats = controller.get_weekly_stats()
    
    print(f"Updated generation statistics: {len(updated_generation_stats)} entries")
    print(f"Updated weekly statistics: {len(updated_weekly_stats)} entries")
    
    if updated_generation_stats:
        print(f"Latest generation stats: {updated_generation_stats[-1]}")
    if updated_weekly_stats:
        print(f"Latest weekly stats: {updated_weekly_stats[-1]}")


def demonstrate_error_handling(controller: SimulationController):
    """Demonstrate error handling."""
    print_section("6. ERROR HANDLING")
    
    print_subsection("Invalid Operations")
    
    # Try to start simulation without world
    controller.reset_simulation()
    try:
        controller.start_simulation()
        print("ERROR: Should have failed to start without world")
    except ValueError as e:
        print(f"✓ Correctly caught error: {e}")
    
    # Try to start simulation without population
    controller.initialize_world()
    try:
        controller.start_simulation()
        print("ERROR: Should have failed to start without population")
    except ValueError as e:
        print(f"✓ Correctly caught error: {e}")
    
    # Try to pause simulation when not running
    try:
        controller.pause_simulation()
        print("ERROR: Should have failed to pause when not running")
    except ValueError as e:
        print(f"✓ Correctly caught error: {e}")
    
    # Try to resume simulation when not running
    try:
        controller.resume_simulation()
        print("ERROR: Should have failed to resume when not running")
    except ValueError as e:
        print(f"✓ Correctly caught error: {e}")
    
    print_subsection("Invalid Configuration")
    try:
        from simulation_controller import SimulationConfig
        invalid_config = SimulationConfig(max_weeks=0)
        print("ERROR: Should have failed with invalid config")
    except ValueError as e:
        print(f"✓ Correctly caught config error: {e}")


def demonstrate_complete_workflow():
    """Demonstrate complete simulation workflow."""
    print_section("7. COMPLETE WORKFLOW DEMONSTRATION")
    
    print_subsection("Creating Controller")
    controller = create_simulation_controller(
        max_weeks=10,
        max_generations=3,
        population_size=8,
        random_seed=42,
        enable_logging=False
    )
    print(f"Controller created with {controller.config.population_size} animals")
    
    print_subsection("Initializing World")
    world = controller.initialize_world()
    print(f"World initialized: {world.dimensions[0]}x{world.dimensions[1]}")
    
    print_subsection("Initializing Population")
    animals = controller.initialize_population()
    print(f"Population initialized: {len(animals)} animals")
    
    print_subsection("Validating State")
    is_valid = controller.validate_simulation_state()
    print(f"State validation: {'PASSED' if is_valid else 'FAILED'}")
    
    print_subsection("Starting Simulation")
    controller.start_simulation()
    print(f"Simulation started successfully")
    
    print_subsection("Monitoring Status")
    status = controller.get_simulation_status()
    print(f"Living animals: {status['living_animals']}")
    print(f"Dead animals: {status['dead_animals']}")
    print(f"Current week: {status['current_week']}")
    print(f"Current generation: {status['current_generation']}")
    
    print_subsection("Stopping Simulation")
    controller.stop_simulation()
    print(f"Simulation stopped successfully")
    
    print_subsection("Resetting Simulation")
    controller.reset_simulation()
    print(f"Simulation reset - ready for new run")
    
    print_subsection("Final Status")
    final_status = controller.get_simulation_status()
    print(f"Final population: {final_status['total_population']}")
    print(f"World initialized: {final_status['world_initialized']}")
    print(f"Population initialized: {final_status['population_initialized']}")


def main():
    """Main demonstration function."""
    print("EvoSim Simulation Controller Demonstration")
    print("=" * 60)
    print("This demonstration showcases the SimulationController functionality")
    print("including initialization, world/population management, and control flow.")
    print()
    
    try:
        # Create a controller for demonstrations
        controller = demonstrate_controller_initialization()
        
        # Demonstrate world initialization
        world = demonstrate_world_initialization(controller)
        
        # Demonstrate population initialization
        animals = demonstrate_population_initialization(controller)
        
        # Demonstrate simulation control
        demonstrate_simulation_control(controller)
        
        # Demonstrate status monitoring
        demonstrate_status_monitoring(controller)
        
        # Demonstrate error handling
        demonstrate_error_handling(controller)
        
        # Demonstrate complete workflow
        demonstrate_complete_workflow()
        
        print_section("DEMONSTRATION COMPLETE")
        print("✅ All simulation controller features demonstrated successfully!")
        print("The SimulationController is ready for Phase 2 implementation.")
        print()
        print("Key Features Demonstrated:")
        print("• Controller initialization and configuration")
        print("• World generation and validation")
        print("• Population creation and placement")
        print("• Simulation state management")
        print("• Status monitoring and logging")
        print("• Error handling and validation")
        print("• Complete workflow orchestration")
        
    except Exception as e:
        print(f"\n❌ Demonstration failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    if success:
        print(f"\n🎉 Demonstration completed successfully!")
    else:
        print(f"\n💥 Demonstration failed!")
        sys.exit(1)
