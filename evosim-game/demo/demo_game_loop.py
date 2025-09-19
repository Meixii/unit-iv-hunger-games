"""
Demonstration of Game Loop Implementation (Task 2.2).

This demo showcases the game loop functionality including:
- Generation execution with week-based progression
- Event scheduling and management
- Win/loss detection
- Comprehensive logging and statistics tracking
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation_controller import SimulationController, SimulationConfig
from world_generator import GenerationConfig


def demo_basic_generation():
    """Demonstrate basic generation execution."""
    print("🎮 DEMO: Basic Generation Execution")
    print("=" * 50)
    
    # Create simulation with small population for demo
    config = SimulationConfig(
        max_weeks=4,
        population_size=8,
        random_seed=42,
        log_level="INFO"
    )
    
    controller = SimulationController(config)
    
    # Initialize world and population
    print("\n📍 Initializing simulation...")
    world = controller.initialize_world()
    animals = controller.initialize_population()
    
    print(f"✅ World: {world.dimensions[0]}x{world.dimensions[1]} grid")
    print(f"✅ Population: {len(animals)} animals")
    
    # Run generation
    print(f"\n🚀 Running generation with max {config.max_weeks} weeks...")
    result = controller.run_generation()
    
    # Display results
    print(f"\n📊 GENERATION RESULTS:")
    print(f"   • Weeks completed: {result['weeks_completed']}/{result['max_weeks']}")
    print(f"   • Final survivors: {result['survivors']}")
    print(f"   • Total casualties: {result['casualties']}")
    print(f"   • Events executed: {result['events_count']}")
    print(f"   • Duration: {result['duration']}")
    
    if result['winner']:
        print(f"   🏆 Winner: {result['winner'].animal_id}")
    elif result['extinction']:
        print(f"   💀 Result: EXTINCTION")
    else:
        print(f"   ⏰ Result: TIME LIMIT REACHED")
    
    return result


def demo_event_scheduling():
    """Demonstrate event scheduling mechanics."""
    print("\n\n🎲 DEMO: Event Scheduling")
    print("=" * 50)
    
    controller = SimulationController(SimulationConfig(random_seed=123))
    
    # Show Week 1 fixed schedule
    print("\n📅 Week 1 (Fixed Schedule):")
    week1_schedule = controller._get_weekly_event_schedule(1)
    for i, event in enumerate(week1_schedule, 1):
        print(f"   {i}. {event}")
    
    # Show randomized schedules for subsequent weeks
    print(f"\n🎯 Weeks 2-4 (Randomized Schedules):")
    for week in range(2, 5):
        schedule = controller._get_weekly_event_schedule(week)
        print(f"   Week {week}: {', '.join(schedule)}")


def demo_win_loss_scenarios():
    """Demonstrate different win/loss scenarios."""
    print("\n\n🏁 DEMO: Win/Loss Scenarios")
    print("=" * 50)
    
    # Scenario 1: Single Survivor
    print("\n🥇 Scenario 1: Single Survivor")
    config = SimulationConfig(
        max_weeks=10,
        population_size=4,
        random_seed=789,
        log_level="WARNING"  # Reduce logging for demo
    )
    
    controller = SimulationController(config)
    controller.initialize_world()
    controller.initialize_population()
    
    # Mock rapid population decline
    def mock_movement_event(week):
        living = controller.simulation.get_living_animals()
        if len(living) > 1 and week >= 2:
            # Remove all but one animal
            for animal in living[1:]:
                controller.simulation.remove_animal(animal)
        
        return {
            'type': 'movement',
            'week': week,
            'success': True,
            'message': f'Movement event - {len(living)-1 if len(living)>1 else 0} casualties',
            'affected_animals': [a.animal_id for a in living[1:]] if len(living)>1 else [],
            'casualties': len(living)-1 if len(living)>1 else 0
        }
    
    # Replace movement event temporarily
    original_method = controller._execute_movement_event
    controller._execute_movement_event = mock_movement_event
    
    result1 = controller.run_generation()
    print(f"   Result: {result1['survivors']} survivor(s), completed in {result1['weeks_completed']} weeks")
    
    # Restore original method
    controller._execute_movement_event = original_method
    
    # Scenario 2: Time Limit Reached
    print(f"\n⏰ Scenario 2: Time Limit Reached")
    config2 = SimulationConfig(
        max_weeks=2,  # Very short time limit
        population_size=6,
        random_seed=456,
        log_level="WARNING"
    )
    
    controller2 = SimulationController(config2)
    controller2.initialize_world()
    controller2.initialize_population()
    
    result2 = controller2.run_generation()
    print(f"   Result: {result2['survivors']} survivors, time limit reached after {result2['weeks_completed']} weeks")


def demo_statistics_tracking():
    """Demonstrate statistics and tracking capabilities."""
    print("\n\n📈 DEMO: Statistics Tracking")
    print("=" * 50)
    
    config = SimulationConfig(
        max_weeks=3,
        population_size=6,
        random_seed=999,
        log_level="WARNING"
    )
    
    controller = SimulationController(config)
    controller.initialize_world()
    controller.initialize_population()
    
    # Run generation
    result = controller.run_generation()
    
    # Show generation statistics
    gen_stats = controller.get_generation_stats()
    print(f"\n📊 Generation Statistics:")
    print(f"   • Generations completed: {len(gen_stats)}")
    
    for i, stats in enumerate(gen_stats):
        print(f"   • Generation {i}:")
        print(f"     - Weeks: {stats['weeks_completed']}/{stats['max_weeks']}")
        print(f"     - Survivors: {stats['survivors']}")
        print(f"     - Events: {stats['events_count']}")
    
    # Show weekly statistics
    weekly_stats = controller.get_weekly_stats()
    print(f"\n📅 Weekly Statistics:")
    for week_stat in weekly_stats:
        print(f"   • Week {week_stat['week']}: {len(week_stat['events'])} events, "
              f"{week_stat['living_animals']} living")
    
    # Show simulation status
    status = controller.get_simulation_status()
    print(f"\n🔍 Simulation Status:")
    for key, value in status.items():
        if key not in ['simulation_start_time', 'simulation_end_time']:
            print(f"   • {key.replace('_', ' ').title()}: {value}")


def demo_multiple_generations():
    """Demonstrate multiple generation tracking."""
    print("\n\n🔄 DEMO: Multiple Generations")
    print("=" * 50)
    
    config = SimulationConfig(
        max_weeks=2,
        population_size=4,
        random_seed=333,
        log_level="WARNING"
    )
    
    controller = SimulationController(config)
    
    # Run multiple generations
    for gen in range(3):
        print(f"\n🎯 Running Generation {gen}...")
        
        # Initialize for this generation
        controller.current_generation = gen
        controller.initialize_world()
        controller.initialize_population()
        
        # Run generation
        result = controller.run_generation()
        print(f"   ✅ Completed: {result['survivors']} survivors, {result['events_count']} events")
        
        # Reset for next generation (but preserve stats)
        if gen < 2:  # Don't reset after last generation
            controller.stop_simulation()
            controller.simulation.reset()
            controller.weekly_stats.clear()
            controller.simulation_start_time = None
            controller.simulation_end_time = None
    
    # Show final statistics
    all_gen_stats = controller.get_generation_stats()
    print(f"\n📈 Final Statistics:")
    print(f"   • Total generations: {len(all_gen_stats)}")
    
    for i, stats in enumerate(all_gen_stats):
        print(f"   • Gen {i}: {stats['survivors']} survivors, "
              f"{stats['weeks_completed']} weeks, {stats['events_count']} events")


def main():
    """Run all game loop demonstrations."""
    print("🎮 EVOSIM GAME LOOP DEMONSTRATION")
    print("=" * 60)
    print("This demo showcases Task 2.2: Game Loop Implementation")
    print("Features: Week-based simulation, event scheduling, win/loss detection")
    print("=" * 60)
    
    try:
        # Run all demonstrations
        demo_basic_generation()
        demo_event_scheduling()
        demo_win_loss_scenarios()
        demo_statistics_tracking()
        demo_multiple_generations()
        
        print("\n" + "=" * 60)
        print("✅ ALL DEMONSTRATIONS COMPLETED SUCCESSFULLY!")
        print("🎯 Game Loop Implementation (Task 2.2) is fully functional")
        print("=" * 60)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
