"""
Event & Disaster Engine Demonstration

This demonstration showcases the comprehensive event system including:
- Triggered events based on simulation conditions
- Random events with probability-based occurrence
- Disaster events with area-of-effect mechanics
- Event scheduling and coordination
- Integration with the simulation controller

The demo shows how the event system creates dynamic and engaging gameplay
through environmental challenges and opportunities.
"""

import sys
import os
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation_controller import SimulationController, SimulationConfig
from event_engine import EventEngine
from world_generator import GenerationConfig


def demonstrate_event_engine():
    """Demonstrate the event engine system."""
    print("🎪 Event & Disaster Engine Demonstration")
    print("=" * 60)
    print("This demo showcases the comprehensive event system:")
    print("• Triggered Events: Condition-based events")
    print("• Random Events: Probability-based events")
    print("• Disaster Events: Large-scale area-effect events")
    print("• Event Scheduling: Coordinated event management")
    print("• Simulation Integration: Seamless controller integration")
    print()

    # Create simulation controller with configuration for interesting events
    config = SimulationConfig(
        population_size=8,
        max_weeks=8,
        random_seed=42,
        log_level="INFO"
    )
    
    world_config = GenerationConfig(
        width=10,
        height=10,
        mountain_border=True,
        food_spawn_chance=0.4
    )
    config.world_config = world_config

    print("--- 1. INITIALIZATION ---")
    controller = SimulationController(config)
    controller.initialize_world()
    controller.initialize_population()
    
    print(f"✅ Created simulation with {len(controller.simulation.get_living_animals())} animals in 10x10 world")
    print()

    print("--- 2. EVENT ENGINE OVERVIEW ---")
    # Initialize event engine directly for demonstration
    event_engine = EventEngine(controller.simulation, controller.logger)
    
    # Get engine status
    status = event_engine.get_engine_status()
    print(f"Event Engine Status:")
    print(f"  Enabled: {status['is_enabled']}")
    print(f"  Active Events: {status['total_active_events']}")
    print(f"  Event Types:")
    for event_type, events in status['active_events'].items():
        print(f"    {event_type.title()}: {len(events)} events")
    print()

    print("--- 3. INDIVIDUAL EVENT TYPE DEMONSTRATIONS ---")
    print()

    # Demonstrate Triggered Events
    print("🎯 Triggered Events Demonstration")
    print("These events occur when specific conditions are met:")
    
    triggered_engine = event_engine.scheduler.triggered_engine
    print(f"Available triggered events: {len(triggered_engine.events)}")
    
    for event in triggered_engine.events[:3]:  # Show first 3
        print(f"  • {event.name}: {event.description}")
        conditions_met = []
        for condition in event.conditions:
            is_met = condition.is_met(controller.simulation)
            conditions_met.append(f"{condition.name}: {'✓' if is_met else '✗'}")
        print(f"    Conditions: {', '.join(conditions_met)}")
    print()

    # Demonstrate Random Events
    print("🎲 Random Events Demonstration")
    print("These events occur randomly with specific probabilities:")
    
    random_engine = event_engine.scheduler.random_engine
    print(f"Available random events: {len(random_engine.events)}")
    
    for event in random_engine.events[:3]:  # Show first 3
        probability = event.calculate_probability(controller.simulation)
        print(f"  • {event.name}: {event.description}")
        print(f"    Probability: {probability:.1%} per week")
    print()

    # Demonstrate Disaster Events
    print("⚡ Disaster Events Demonstration")
    print("These are large-scale events with area-of-effect:")
    
    disaster_engine = event_engine.scheduler.disaster_engine
    print(f"Available disaster events: {len(disaster_engine.events)}")
    
    for event in disaster_engine.events[:3]:  # Show first 3
        print(f"  • {event.name}: {event.description}")
        print(f"    Severity: {event.severity}, Area of Effect: {event.area_of_effect} tiles")
        print(f"    Probability: {event.probability:.1%} per week")
    print()

    print("--- 4. WEEKLY EVENT SIMULATION ---")
    print("Running simulation to demonstrate event occurrences:")
    print()

    # Run simulation with detailed event tracking
    controller.start_simulation()
    
    for week in range(1, 6):  # Run 5 weeks
        print(f"🗓️  WEEK {week}")
        print("-" * 30)
        
        # Show population status
        living_animals = controller.simulation.get_living_animals()
        print(f"Population: {len(living_animals)} living animals")
        
        # Execute weekly events using the integrated system
        week_result = controller._run_weekly_cycle(week)
        
        # Display event results
        events_occurred = []
        total_casualties = 0
        
        for event_result in week_result.get('events', []):
            if 'event_details' in event_result:
                # This is one of our new event types
                event_details = event_result['event_details']
                if event_details:
                    for detail in event_details:
                        events_occurred.append(detail.message)
                        total_casualties += detail.casualties
            else:
                # Regular event
                if event_result['success'] and event_result['type'] != 'movement':
                    events_occurred.append(f"{event_result['type']}: {event_result['message']}")
                    total_casualties += event_result.get('casualties', 0)
        
        if events_occurred:
            print("📢 Events this week:")
            for event_msg in events_occurred:
                print(f"  • {event_msg}")
        else:
            print("📢 No special events occurred this week")
        
        if total_casualties > 0:
            print(f"⚠️  Total casualties: {total_casualties}")
        
        # Show updated population
        final_living = controller.simulation.get_living_animals()
        print(f"Population after events: {len(final_living)} living animals")
        
        print()
        
        # Stop if population gets too low
        if len(final_living) <= 2:
            print("⚠️  Population critically low - ending demonstration")
            break

    print("--- 5. EVENT STATISTICS ---")
    
    # Get comprehensive statistics
    stats = event_engine.get_statistics()
    
    print("📊 Event Engine Statistics:")
    print(f"  Total Events Executed: {stats['total_events_executed']}")
    print(f"  Total Casualties: {stats['total_casualties']}")
    print(f"  Total Resources Affected: {stats['total_resources_affected']}")
    
    scheduler_stats = stats['scheduler_statistics']
    print(f"  Overall Success Rate: {scheduler_stats['success_rate']:.1%}")
    
    if scheduler_stats['by_type']:
        print("  Events by Type:")
        for event_type, type_stats in scheduler_stats['by_type'].items():
            success_rate = type_stats['successful'] / type_stats['count'] if type_stats['count'] > 0 else 0
            print(f"    {event_type.title()}: {type_stats['count']} total, {success_rate:.1%} success rate")
    
    print()

    print("--- 6. EVENT SYSTEM FEATURES ---")
    print("✅ Condition-Based Triggering: Events respond to simulation state")
    print("✅ Probability Management: Realistic random event occurrence")
    print("✅ Area-of-Effect Mechanics: Disasters affect multiple locations")
    print("✅ Event Scheduling: Coordinated timing and frequency control")
    print("✅ Cooldown Management: Prevents event spam and maintains balance")
    print("✅ Severity Scaling: Different impact levels for varied gameplay")
    print("✅ Resource Integration: Events affect world resources dynamically")
    print("✅ Population Response: Events scale with population size")
    print("✅ Comprehensive Logging: Detailed event tracking and statistics")
    print("✅ Modular Design: Easy to add new event types")
    print()

    print("--- 7. CONFIGURATION DEMONSTRATION ---")
    
    # Demonstrate event configuration
    print("🔧 Event System Configuration:")
    
    original_config = event_engine.scheduler.config.copy()
    print(f"Original disaster probability modifier: {original_config['disaster_probability_modifier']}")
    
    # Modify configuration
    event_engine.configure(
        disaster_probability_modifier=2.0,
        triggered_events_enabled=True,
        random_events_enabled=True
    )
    
    print("Modified configuration to increase disaster probability")
    print(f"New disaster probability modifier: {event_engine.scheduler.config['disaster_probability_modifier']}")
    print()

    print("--- 8. CUSTOM EVENT DEMONSTRATION ---")
    
    # Create a custom event (example)
    from event_engine.random_events import RandomEvent
    from event_engine.event_data import EventResult, EventType
    
    class CustomBonusEvent(RandomEvent):
        """Custom event that gives all animals a bonus."""
        
        def execute(self, simulation, week):
            super().execute(simulation, week)
            
            living_animals = simulation.get_living_animals()
            if not living_animals:
                return EventResult(
                    event_id=self.event_id,
                    event_type=self.event_type,
                    success=True,
                    message="Bonus event occurred but no animals to benefit"
                )
            
            # Give all animals a small health boost
            for animal in living_animals:
                current_health = animal.status.get('Health', 100)
                animal.status['Health'] = min(100, current_health + 10)
            
            return EventResult(
                event_id=self.event_id,
                event_type=self.event_type,
                success=True,
                message=f"Lucky day! All {len(living_animals)} animals received health boost",
                affected_animals=[a.animal_id for a in living_animals],
                effects_applied=len(living_animals)
            )
    
    # Add custom event
    custom_event = CustomBonusEvent(
        event_id="lucky_day",
        name="Lucky Day",
        description="A fortunate day brings health benefits to all animals",
        base_probability=0.3
    )
    
    event_engine.add_custom_event(custom_event)
    print(f"✅ Added custom event: {custom_event.name}")
    print(f"   Description: {custom_event.description}")
    print(f"   Probability: {custom_event.base_probability:.1%} per week")
    print()

    print("--- 9. SYSTEM BENEFITS ---")
    print("🎮 Enhanced Gameplay: Dynamic events create engaging challenges")
    print("🎯 Realistic Simulation: Events respond to actual simulation conditions")
    print("⚖️  Balanced Design: Cooldowns and probabilities prevent overwhelming events")
    print("🔧 Highly Configurable: Easy to adjust event frequency and intensity")
    print("📈 Comprehensive Tracking: Detailed statistics for analysis")
    print("🧩 Modular Architecture: Easy to extend with new event types")
    print("🎪 Variety: Multiple event categories provide diverse experiences")
    print("🌍 World Impact: Events meaningfully affect the simulation environment")
    print()

    print("🎉 Event & Disaster Engine Demonstration Complete!")
    print()
    print("The Event Engine successfully demonstrates:")
    print("• 🎯 Condition-based triggered events")
    print("• 🎲 Probability-based random events")  
    print("• ⚡ Large-scale disaster events")
    print("• 📅 Intelligent event scheduling")
    print("• 🎮 Seamless simulation integration")
    print("• 🔧 Flexible configuration system")
    print("• 📊 Comprehensive event tracking")
    print()
    print("Ready for integration with Phase 3: Neural Network Evolution!")


if __name__ == "__main__":
    # Set logging to show important events but not overwhelm output
    logging.getLogger().setLevel(logging.WARNING)
    
    demonstrate_event_engine()
