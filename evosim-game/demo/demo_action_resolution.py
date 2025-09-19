"""
Action Resolution System Demonstration

This demonstration showcases the modular 4-phase action resolution system:
1. Decision Phase: AI decision making
2. Status & Environmental Phase: Passive effects
3. Action Execution Phase: Action execution with conflicts
4. Cleanup Phase: Effect management

The demonstration shows how the system handles various scenarios including:
- Multiple animals making decisions
- Movement conflicts resolved by agility
- Resource consumption (eating/drinking)
- Combat encounters
- Effect application and removal
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation_controller import SimulationController, SimulationConfig
from action_resolution import ActionResolver, AnimalAction
from data_structures import ActionType, EffectType, Effect, Resource, ResourceType
from world_generator import GenerationConfig
import logging


def demonstrate_action_resolution():
    """Demonstrate the action resolution system."""
    print("🎯 Action Resolution System Demonstration")
    print("=" * 60)
    print("This demo showcases the 4-phase action resolution system:")
    print("1. Decision Phase: Collect actions from all animals")
    print("2. Status & Environmental Phase: Apply passive effects")  
    print("3. Action Execution Phase: Execute actions by priority")
    print("4. Cleanup Phase: Apply new effects and remove expired ones")
    print()

    # Create simulation controller with small world for focused demo
    config = SimulationConfig(
        population_size=6,
        max_weeks=3,
        random_seed=42,
        log_level="INFO"
    )
    
    world_config = GenerationConfig(
        width=8,
        height=8,
        mountain_border=True,
        food_spawn_chance=0.3
    )
    config.world_config = world_config

    print("--- 1. INITIALIZATION ---")
    controller = SimulationController(config)
    controller.initialize_world()
    controller.initialize_population()
    
    print(f"✅ Created {len(controller.simulation.get_living_animals())} animals in 8x8 world")
    print()

    # Display initial animal states
    print("--- 2. INITIAL ANIMAL STATES ---")
    living_animals = controller.simulation.get_living_animals()
    for i, animal in enumerate(living_animals[:4]):  # Show first 4 animals
        print(f"Animal {i+1}: {animal.animal_id}")
        print(f"  Category: {animal.category.value}")
        print(f"  Location: {animal.location}")
        print(f"  Health: {animal.status['Health']:.0f}, Hunger: {animal.status['Hunger']:.0f}, "
              f"Thirst: {animal.status['Thirst']:.0f}, Energy: {animal.status['Energy']:.0f}")
        print(f"  Traits: STR={animal.traits['STR']:.0f}, AGI={animal.traits['AGI']:.0f}")
        print()

    print("--- 3. RUNNING ACTION RESOLUTION PHASES ---")
    print()

    # Demonstrate multiple weeks of action resolution
    for week in range(1, 4):
        print(f"🗓️  WEEK {week}")
        print("-" * 40)
        
        # Get living animals before resolution
        animals_before = controller.simulation.get_living_animals()
        print(f"Living animals before resolution: {len(animals_before)}")
        
        # Execute action resolution system
        result = controller.execute_action_resolution_system(week)
        
        # Display results
        print(f"✅ Action Resolution Complete:")
        print(f"   Phases completed: {result['phases_completed']}/4")
        print(f"   Actions processed: {result['actions_processed']}")
        print(f"   Conflicts resolved: {result['conflicts_resolved']}")
        print(f"   Casualties: {result['casualties']}")
        print(f"   Duration: {result['duration'].total_seconds():.3f}s")
        
        # Show phase details if available
        if 'phase_results' in result:
            phase_results = result['phase_results']
            
            # Decision phase
            decision = phase_results.get('decision', {})
            print(f"   Decision Phase: {decision.get('actions_collected', 0)} actions collected")
            
            # Status & Environmental phase
            status = phase_results.get('status_environmental', {})
            print(f"   Status Phase: {status.get('animals_processed', 0)} animals processed, "
                  f"{len(status.get('casualties', []))} deaths")
            
            # Action Execution phase
            execution = phase_results.get('action_execution', {})
            print(f"   Execution Phase: {execution.get('actions_executed', 0)} executed, "
                  f"{execution.get('actions_failed', 0)} failed, "
                  f"{execution.get('movement_conflicts', 0)} movement conflicts")
            
            # Cleanup phase
            cleanup = phase_results.get('cleanup', {})
            print(f"   Cleanup Phase: {cleanup.get('effects_added', 0)} effects added, "
                  f"{cleanup.get('effects_removed', 0)} effects removed")
        
        # Show surviving animals
        animals_after = controller.simulation.get_living_animals()
        print(f"Living animals after resolution: {len(animals_after)}")
        
        # Show animal status changes
        if len(animals_after) > 0:
            print("\n📊 Sample Animal Status:")
            sample_animal = animals_after[0]
            print(f"   {sample_animal.animal_id}: Health={sample_animal.status['Health']:.0f}, "
                  f"Hunger={sample_animal.status['Hunger']:.0f}, "
                  f"Thirst={sample_animal.status['Thirst']:.0f}, "
                  f"Energy={sample_animal.status['Energy']:.0f}")
            
            # Show effects if any
            if sample_animal.active_effects:
                print(f"   Active effects: {[e.effect_type.value for e in sample_animal.active_effects]}")
        
        print()
        
        # Stop if too few animals remain
        if len(animals_after) <= 2:
            print("⚠️  Few animals remaining - ending demonstration")
            break

    print("--- 4. DETAILED PHASE BREAKDOWN ---")
    print()
    
    # Demonstrate each phase individually with a fresh setup
    print("🔍 Individual Phase Demonstration")
    
    # Reset and create a controlled scenario
    controller.reset_simulation()
    controller.initialize_world()
    controller.initialize_population()
    
    # Get the action resolver
    if not hasattr(controller, '_action_resolver') or controller._action_resolver is None:
        controller._action_resolver = ActionResolver(controller.simulation, controller.logger)
    
    action_resolver = controller._action_resolver
    living_animals = controller.simulation.get_living_animals()
    
    print(f"Using {len(living_animals)} animals for detailed demonstration")
    print()
    
    # Phase 1: Decision Phase
    print("📋 Phase 1: Decision Phase")
    planned_actions = action_resolver.decision_engine.execute_decision_phase(living_animals)
    print(f"   Collected {len(planned_actions)} actions:")
    
    action_counts = {}
    for action in planned_actions:
        action_type = action.action_type.value
        action_counts[action_type] = action_counts.get(action_type, 0) + 1
    
    for action_type, count in action_counts.items():
        print(f"     {action_type}: {count} animals")
    print()
    
    # Phase 2: Status & Environmental Phase
    print("🌡️  Phase 2: Status & Environmental Phase")
    status_results = action_resolver.status_engine.execute_status_environmental_phase(living_animals)
    print(f"   Processed {status_results['animals_processed']} animals")
    print(f"   Hunger depletion: {status_results['hunger_depletion']} animals")
    print(f"   Thirst depletion: {status_results['thirst_depletion']} animals")
    print(f"   Energy regeneration: {status_results['energy_regeneration']} animals")
    if status_results['casualties']:
        print(f"   Casualties: {len(status_results['casualties'])} animals")
        for casualty in status_results['casualties'][:2]:  # Show first 2
            print(f"     {casualty['animal_id']}: died from {casualty['cause']}")
    print()
    
    # Phase 3: Action Execution Phase
    print("⚡ Phase 3: Action Execution Phase")
    execution_results = action_resolver.execution_engine.execute_action_execution_phase(planned_actions)
    print(f"   Actions executed: {execution_results['actions_executed']}")
    print(f"   Actions failed: {execution_results['actions_failed']}")
    print(f"   Movement conflicts: {execution_results['movement_conflicts']}")
    print(f"   Combat encounters: {execution_results['combat_encounters']}")
    print()
    
    # Phase 4: Cleanup Phase
    print("🧹 Phase 4: Cleanup Phase")
    remaining_animals = controller.simulation.get_living_animals()
    cleanup_results = action_resolver.cleanup_engine.execute_cleanup_phase(remaining_animals)
    print(f"   Animals processed: {cleanup_results['animals_processed']}")
    print(f"   Effects added: {cleanup_results['effects_added']}")
    print(f"   Effects removed: {cleanup_results['effects_removed']}")
    print(f"   Effects updated: {cleanup_results['effects_updated']}")
    print()

    print("--- 5. SYSTEM BENEFITS ---")
    print("✅ Modular Design: Each phase is in its own focused module")
    print("✅ Maintainability: Easy to modify or extend individual phases")
    print("✅ Testability: Individual engines can be tested in isolation")
    print("✅ Fairness: All decisions made before any actions executed")
    print("✅ Conflict Resolution: Agility-based movement conflict resolution")
    print("✅ Resource Management: Proper resource consumption tracking")
    print("✅ Effect System: Dynamic effect application and removal")
    print()

    print("--- 6. FUTURE ENHANCEMENTS ---")
    print("🔮 Phase 3 Integration: Replace rule-based decisions with MLP neural networks")
    print("🔮 Advanced Combat: Expand animal encounters with detailed combat mechanics")
    print("🔮 Complex Effects: Add more sophisticated effect interactions")
    print("🔮 Environmental Events: Integrate with disaster and environmental systems")
    print()

    print("🎉 Action Resolution System Demonstration Complete!")
    print("The system successfully demonstrates:")
    print("• 4-phase turn-based action processing")
    print("• Modular, maintainable architecture")
    print("• Fair conflict resolution")
    print("• Comprehensive effect management")
    print("• Integration with the main simulation controller")


if __name__ == "__main__":
    # Suppress excessive logging for cleaner demo output
    logging.getLogger().setLevel(logging.WARNING)
    
    demonstrate_action_resolution()
