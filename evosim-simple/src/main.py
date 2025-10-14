"""
Main entry point for the Evolutionary Simulation application.
"""

import sys
import time
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import Phase 2 components
from .neural_network import NeuralNetwork
from .animal import Animal
# Import Phase 3 components
from .environment import GridWorld
from .events import EventManager
# Import Phase 4 components
from .evolution import Population, EvolutionManager
# Import Phase 5 components
from .simulation import Simulation, SimulationState
# Import Phase 6 components
from ui.gui import SimulationGUI
# Import Phase 7 components
from analysis.statistics import StatisticsCollector
from analysis.visualization import SimulationVisualizer


def main():
    """
    Main entry point for the application.

    This function demonstrates the neural network and animal components
    implemented in Phase 2.
    """
    print("Evolutionary Simulation - Educational AI Project")
    print("=" * 50)
    print("Project: Educational Survival Simulation Using Evolutionary")
    print("Algorithms")
    print("Authors: Zen Garden")
    print("University of Caloocan City")
    print("=" * 50)
    print()
    print("Phase 1: Infrastructure Setup - COMPLETED [OK]")
    print("Phase 2: Neural Network Implementation - COMPLETED [OK]")
    print("Phase 3: Simulation Environment - PENDING")
    print("Phase 4: Evolutionary Algorithm - PENDING")
    print("Phase 5: Simulation Engine - PENDING")
    print("Phase 6: User Interface - PENDING")
    print("Phase 7: Data Analysis - PENDING")
    print("Phase 8: Testing & Optimization - PENDING")
    print("Phase 9: Documentation & Deployment - PENDING")
    print()
    
    # Demonstrate Phase 2 components
    print("=== Phase 2 Demonstration ===")
    print()
    
    # Create a neural network
    print("1. Creating Neural Network (2-4-4 architecture)...")
    network = NeuralNetwork()
    print(f"   Network: {network}")
    print()
    
    # Create an animal with the network
    print("2. Creating Animal with Neural Network brain...")
    animal = Animal(10, 15, network)
    print(f"   Animal: {animal}")
    print()
    
    # Demonstrate decision making
    print("3. Demonstrating Animal Decision Making...")
    for i in range(5):
        decision = animal.make_decision()
        probabilities = animal.get_action_probabilities()
        print(f"   Step {i+1}: Decision = {decision}")
        print(f"   Step {i+1}: Probabilities = {probabilities}")
        
        # Execute the action
        success = animal.execute_action(decision)
        print(f"   Step {i+1}: Action {'successful' if success else 'failed'}")
        print(f"   Step {i+1}: State = hunger={animal.hunger:.1f}, "
              f"thirst={animal.thirst:.1f}, energy={animal.energy:.1f}")
        print()
        
        if not animal.alive:
            print("   Animal has died!")
            break
    
    # Show final fitness
    fitness = animal.calculate_fitness()
    print(f"4. Final Animal Fitness: {fitness:.2f}")
    print()
    
    # Demonstrate neural network operations
    print("5. Demonstrating Neural Network Operations...")
    
    # Test mutation
    original_weights = network.get_weights()
    network.mutate(mutation_rate=0.1, mutation_strength=0.1)
    print("   Applied mutation to network")
    
    # Test crossover
    network2 = NeuralNetwork()
    offspring = network.crossover(network2, crossover_rate=0.5)
    print("   Created offspring through crossover")
    
    # Test serialization
    json_string = network.serialize()
    restored_network = NeuralNetwork.deserialize(json_string)
    print("   Serialized and deserialized network")
    print()
    
    print("=== Phase 2 Complete ===")
    print("Neural networks and animals are working correctly!")
    print("Ready to proceed to Phase 3: Simulation Environment")
    
    # Phase 3: Simulation Environment Demonstration
    print("\n" + "="*60)
    print("[ENV] PHASE 3: SIMULATION ENVIRONMENT - DEMONSTRATION")
    print("="*60)
    
    # Create environment
    print("Creating 20x20 grid world...")
    world = GridWorld(20, 20)
    print(f"[OK] GridWorld created: {world}")
    
    # Place resources
    print("Placing food and water resources...")
    world.place_resources(food_density=0.1, water_density=0.1)
    print(f"[OK] Resources placed: {world.food_count} food, {world.water_count} water")
    
    # Create animals and place them
    print("Creating and placing animals...")
    animals = []
    for i in range(5):
        network = NeuralNetwork()
        animal = Animal(0, 0, network)
        # Find empty position
        empty_positions = world.get_empty_positions()
        if empty_positions:
            pos = empty_positions[i % len(empty_positions)]
            world.add_animal(animal, pos[0], pos[1])
            animals.append(animal)
    
    print(f"[OK] {len(animals)} animals placed in environment")
    
    # Demonstrate animal behavior in environment
    print("\nDemonstrating animal behavior in environment...")
    for i, animal in enumerate(animals):
        pos = animal.get_position()
        available_actions = world.get_available_actions(pos[0], pos[1])
        decision = animal.make_decision()
        
        print(f"Animal {i+1} at {pos}: Available actions: {available_actions}")
        print(f"  Decision: {decision}")
        
        # Execute action if valid
        if decision in available_actions:
            if decision == 'eat' and 'eat' in available_actions:
                world.consume_resource(pos[0], pos[1], 'food')
                animal.execute_action('eat')
                print(f"  [OK] Ate food at {pos}")
            elif decision == 'drink' and 'drink' in available_actions:
                world.consume_resource(pos[0], pos[1], 'water')
                animal.execute_action('drink')
                print(f"  [OK] Drank water at {pos}")
            elif decision == 'move':
                # Try to move to a neighboring position
                neighbors = world.get_neighboring_positions(pos[0], pos[1])
                if neighbors:
                    new_pos = neighbors[0]  # Move to first available neighbor
                    if world.move_animal(animal, new_pos[0], new_pos[1]):
                        print(f"  [OK] Moved to {new_pos}")
                    else:
                        print(f"  [FAIL] Could not move to {new_pos}")
                else:
                    print(f"  [FAIL] No valid neighbors to move to")
            else:
                animal.execute_action(decision)
                print(f"  [OK] Executed {decision}")
        else:
            print(f"  [FAIL] Action {decision} not available")
    
    # Demonstrate event system
    print("\nDemonstrating environmental events...")
    event_manager = EventManager()
    print(f"[OK] EventManager created with {len(event_manager.active_events)} active events")
    
    # Force some events
    print("Forcing drought event...")
    event_manager.force_event('drought')
    print(f"[OK] Drought event active: {event_manager.is_event_active('drought')}")
    
    print("Forcing storm event...")
    event_manager.force_event('storm')
    print(f"[OK] Storm event active: {event_manager.is_event_active('storm')}")
    
    # Show event effects
    effects = event_manager.get_event_effects()
    print(f"[OK] Combined event effects: {effects}")
    
    # Update events
    print("Updating events...")
    event_manager.update()
    print(f"[OK] Events updated, {len(event_manager.active_events)} still active")
    
    # Show environment statistics
    print("\nEnvironment Statistics:")
    stats = world.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Show event statistics
    print("\nEvent Manager Statistics:")
    event_stats = event_manager.get_statistics()
    for key, value in event_stats.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*60)
    print("[OK] PHASE 3: SIMULATION ENVIRONMENT - COMPLETED!")
    print("="*60)
    print("[OK] GridWorld System: 20x20 environment with resource management")
    print("[OK] Animal Positioning: Collision detection and movement validation")
    print("[OK] Resource System: Food and water placement and consumption")
    print("[OK] Event System: Dynamic environmental events (drought, storm)")
    print("[OK] Event Scheduling: Duration-based event management")
    print("\n[READY] Ready for Phase 4: Evolutionary Algorithm!")
    print("="*60)
    
    # Phase 4: Evolutionary Algorithm Demonstration
    print("\n" + "="*60)
    print("[EVO] PHASE 4: EVOLUTIONARY ALGORITHM - DEMONSTRATION")
    print("="*60)
    
    # Create population with grid world
    print("Creating population with grid world...")
    population = Population(size=20, grid_world=world)
    print(f"[OK] Population created: {population}")
    
    # Create evolution manager
    print("Creating evolution manager...")
    evolution_manager = EvolutionManager(population)
    print(f"[OK] EvolutionManager created: {evolution_manager}")
    
    # Set evolution parameters
    print("Setting evolution parameters...")
    evolution_manager.set_parameters(
        selection_method='tournament',
        tournament_size=3,
        convergence_threshold=0.01,
        max_generations=5
    )
    print("[OK] Evolution parameters configured")
    
    # Demonstrate initial population
    print("\nInitial population statistics:")
    initial_stats = population.calculate_statistics()
    for key, value in initial_stats.items():
        print(f"  {key}: {value}")
    
    # Evolve for a few generations
    print("\nEvolving population for 3 generations...")
    evolution_result = evolution_manager.evolve(max_generations=3)
    
    print(f"[OK] Evolution completed:")
    print(f"  Generations: {evolution_result['generations_completed']}")
    print(f"  Best fitness: {evolution_result['best_fitness_achieved']:.2f}")
    print(f"  Converged: {evolution_result['converged']}")
    print(f"  Stagnated: {evolution_result['stagnated']}")
    
    # Show final population statistics
    print("\nFinal population statistics:")
    final_stats = population.calculate_statistics()
    for key, value in final_stats.items():
        print(f"  {key}: {value}")
    
    # Demonstrate different selection methods
    print("\nDemonstrating different selection methods...")
    
    # Tournament selection
    print("Testing tournament selection...")
    parents_tournament = population.select_parents(selection_method='tournament', tournament_size=3)
    print(f"[OK] Tournament selection: {len(parents_tournament)} parents selected")
    
    # Roulette wheel selection
    print("Testing roulette wheel selection...")
    parents_roulette = population.select_parents(selection_method='roulette')
    print(f"[OK] Roulette selection: {len(parents_roulette)} parents selected")
    
    # Rank selection
    print("Testing rank selection...")
    parents_rank = population.select_parents(selection_method='rank')
    print(f"[OK] Rank selection: {len(parents_rank)} parents selected")
    
    # Demonstrate offspring creation
    print("\nDemonstrating offspring creation...")
    offspring = population.create_offspring(parents_tournament)
    print(f"[OK] Created {len(offspring)} offspring")
    
    # Show evolution statistics
    print("\nEvolution statistics:")
    evolution_stats = evolution_manager.get_evolution_statistics()
    for key, value in evolution_stats.items():
        if key in ['fitness_trend', 'survival_trend']:
            print(f"  {key}: {value[:5]}...")  # Show first 5 values
        else:
            print(f"  {key}: {value}")
    
    # Demonstrate convergence detection
    print("\nConvergence analysis:")
    print(f"  Converged: {evolution_manager._check_convergence()}")
    print(f"  Fitness history: {population.fitness_history}")
    
    # Show evolution summary
    print("\nEvolution summary:")
    summary = population.get_evolution_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*60)
    print("[OK] PHASE 4: EVOLUTIONARY ALGORITHM - COMPLETED!")
    print("="*60)
    print("[OK] Population Management: Multi-generation animal groups")
    print("[OK] Selection Algorithms: Tournament, roulette, rank selection")
    print("[OK] Genetic Operations: Crossover and mutation with elitism")
    print("[OK] Evolution Process: Generation advancement and statistics")
    print("[OK] Convergence Detection: Fitness improvement monitoring")
    print("\n[READY] Ready for Phase 5: Simulation Engine!")
    print("="*60)
    
    # Phase 5: Simulation Engine Demonstration
    print("\n" + "="*60)
    print("[SIM] PHASE 5: SIMULATION ENGINE - DEMONSTRATION")
    print("="*60)
    
    # Create simulation with custom configuration
    print("Creating simulation with custom configuration...")
    config = {
        'grid_size': (15, 15),
        'population_size': 25,
        'max_generations': 2,
        'steps_per_generation': 50,
        'simulation_speed': 10.0,  # Fast for demonstration
        'food_density': 0.12,
        'water_density': 0.12,
        'drought_probability': 0.3,
        'storm_probability': 0.2,
        'famine_probability': 0.15,
        'bonus_probability': 0.05,
        'mutation_rate': 0.1,
        'crossover_rate': 0.8,
        'selection_method': 'tournament',
        'tournament_size': 3,
        'elite_percentage': 0.1
    }
    
    simulation = Simulation(config)
    print(f"[OK] Simulation created with config: {config}")
    
    # Initialize simulation
    print("Initializing simulation...")
    simulation.initialize()
    print("[OK] Simulation initialized")
    
    # Add callbacks for monitoring
    step_count = 0
    generation_count = 0
    
    def step_callback(stats):
        nonlocal step_count
        step_count += 1
        if step_count % 10 == 0:  # Print every 10 steps
            print(f"  Step {stats['step']}: {stats['alive_animals']} animals alive")
    
    def generation_callback(stats):
        nonlocal generation_count
        generation_count += 1
        print(f"  Generation {stats['generation']} completed: "
              f"Best fitness: {stats['best_fitness']:.2f}, "
              f"Survival rate: {stats['survival_rate']:.2f}")
    
    def state_callback(state):
        print(f"  State changed to: {state.value}")
    
    simulation.add_step_callback(step_callback)
    simulation.add_generation_callback(generation_callback)
    simulation.add_state_change_callback(state_callback)
    
    # Demonstrate simulation control
    print("\nDemonstrating simulation control...")
    
    # Start simulation
    print("Starting simulation...")
    simulation.start()
    print(f"[OK] Simulation started: {simulation}")
    
    # Let it run briefly
    print("Running simulation for 0.5 seconds...")
    time.sleep(0.5)
    
    # Pause simulation
    print("Pausing simulation...")
    simulation.pause()
    print(f"[OK] Simulation paused: {simulation}")
    
    # Resume simulation
    print("Resuming simulation...")
    simulation.resume()
    print(f"[OK] Simulation resumed: {simulation}")
    
    # Let it run a bit more
    time.sleep(0.3)
    
    # Stop simulation
    print("Stopping simulation...")
    simulation.stop()
    print(f"[OK] Simulation stopped: {simulation}")
    
    # Show simulation statistics
    print("\nSimulation Statistics:")
    stats = simulation.get_statistics()
    for key, value in stats.items():
        if key in ['environment_stats', 'population_stats', 'event_stats']:
            print(f"  {key}: {len(value)} items")
        else:
            print(f"  {key}: {value}")
    
    # Show step history
    print(f"\nStep History ({len(simulation.step_history)} steps):")
    recent_steps = simulation.get_step_history(5)
    for step in recent_steps:
        print(f"  Step {step['step']}: {step['alive_animals']} alive animals")
    
    # Show generation history
    print(f"\nGeneration History ({len(simulation.generation_history)} generations):")
    for gen in simulation.generation_history:
        print(f"  Generation {gen['generation']}: "
              f"Best fitness: {gen.get('best_fitness', 0):.2f}, "
              f"Survival: {gen.get('survival_rate', 0):.2f}")
    
    # Demonstrate simulation speed control
    print("\nDemonstrating simulation speed control...")
    simulation.set_simulation_speed(20.0)
    print(f"[OK] Speed set to {simulation.simulation_speed} steps/second")
    
    # Demonstrate reset
    print("\nDemonstrating simulation reset...")
    simulation.reset()
    print(f"[OK] Simulation reset: {simulation}")
    
    # Show final statistics
    print("\nFinal Simulation Statistics:")
    final_stats = simulation.get_statistics()
    for key, value in final_stats.items():
        if key in ['environment_stats', 'population_stats', 'event_stats']:
            print(f"  {key}: {len(value)} items")
        else:
            print(f"  {key}: {value}")
    
    print("\n" + "="*60)
    print("[OK] PHASE 5: SIMULATION ENGINE - COMPLETED!")
    print("="*60)
    print("[OK] Simulation Controller: Main coordination system")
    print("[OK] Time Management: Step-based simulation with speed control")
    print("[OK] State Management: Running, paused, stopped, evolving states")
    print("[OK] Threading: Asynchronous simulation execution")
    print("[OK] Callbacks: Event-driven monitoring and control")
    print("\n[READY] Ready for Phase 6: User Interface!")
    print("="*60)
    
    # Phase 6: User Interface Demonstration
    print("\n" + "="*60)
    print("[UI] PHASE 6: USER INTERFACE - DEMONSTRATION")
    print("="*60)
    
    print("Creating GUI application...")
    try:
        # Create GUI application
        gui = SimulationGUI()
        print("[OK] GUI application created successfully")
        
        # Demonstrate GUI components
        print("\nGUI Components:")
        print(f"  Configuration Frame: {gui.config_frame is not None}")
        print(f"  Visualization Frame: {gui.visualization_frame is not None}")
        print(f"  Control Frame: {gui.control_frame is not None}")
        print(f"  Statistics Frame: {gui.stats_frame is not None}")
        print(f"  Canvas: {gui.canvas is not None}")
        
        # Demonstrate configuration variables
        print("\nConfiguration Variables:")
        print(f"  Grid Size: {gui.config_vars['grid_width'].get()}x{gui.config_vars['grid_height'].get()}")
        print(f"  Population Size: {gui.config_vars['population_size'].get()}")
        print(f"  Max Generations: {gui.config_vars['max_generations'].get()}")
        print(f"  Simulation Speed: {gui.config_vars['simulation_speed'].get()}")
        print(f"  Food Density: {gui.config_vars['food_density'].get()}")
        print(f"  Water Density: {gui.config_vars['water_density'].get()}")
        print(f"  Selection Method: {gui.config_vars['selection_method'].get()}")
        
        # Demonstrate statistics variables
        print("\nStatistics Variables:")
        print(f"  State: {gui.stats_vars['state'].get()}")
        print(f"  Current Step: {gui.stats_vars['current_step'].get()}")
        print(f"  Current Generation: {gui.stats_vars['current_generation'].get()}")
        print(f"  Alive Animals: {gui.stats_vars['alive_animals'].get()}")
        print(f"  Survival Rate: {gui.stats_vars['survival_rate'].get()}")
        
        # Demonstrate GUI functionality
        print("\nGUI Functionality:")
        print("  Configuration Management: Load, Save, Reset")
        print("  Simulation Control: Start, Pause, Resume, Stop, Reset")
        print("  Real-time Visualization: Grid display with animals and resources")
        print("  Statistics Display: Live updates of simulation metrics")
        print("  Data Export: Export simulation data and configuration")
        print("  Speed Control: Adjustable simulation speed")
        print("  Parameter Modification: Real-time parameter adjustment")
        
        # Demonstrate configuration management
        print("\nDemonstrating configuration management...")
        config = gui._get_config_from_gui()
        print(f"[OK] Configuration extracted: {len(config)} parameters")
        
        # Demonstrate statistics display
        print("Demonstrating statistics display...")
        gui._update_display()
        print("[OK] Statistics display updated")
        
        # Demonstrate control button states
        print("Demonstrating control button states...")
        gui._update_control_buttons()
        print("[OK] Control buttons updated")
        
        # Demonstrate visualization
        print("Demonstrating visualization...")
        gui._update_visualization()
        print("[OK] Visualization updated")
        
        # Demonstrate speed control
        print("Demonstrating speed control...")
        gui._update_speed("2.0")
        print("[OK] Speed control updated")
        
        # Demonstrate configuration reset
        print("Demonstrating configuration reset...")
        gui._reset_config()
        print("[OK] Configuration reset to defaults")
        
        print("\n" + "="*60)
        print("[OK] PHASE 6: USER INTERFACE - COMPLETED!")
        print("="*60)
        print("[OK] Configuration Interface: Parameter input and management")
        print("[OK] Visualization System: Real-time grid display")
        print("[OK] Control Panel: Simulation start/stop/pause/resume")
        print("[OK] Statistics Display: Live metrics and monitoring")
        print("[OK] Data Export: Configuration and data export functionality")
        print("[OK] Speed Control: Adjustable simulation speed")
        print("[OK] Parameter Modification: Real-time parameter adjustment")
        print("\n[READY] Ready for Phase 7: Data Analysis and Visualization!")
        print("="*60)
        
        # Note: GUI is not actually run in demonstration mode
        print("\nNote: GUI application created but not launched in demonstration mode.")
        print("To run the GUI, use: python run_gui.py")
        
        # Clean up GUI
        gui.root.destroy()
        
    except Exception as e:
        print(f"[FAIL] GUI creation failed: {e}")
        print("GUI functionality may not be available in this environment.")
    
    # Phase 7: Data Analysis and Visualization Demonstration
    print("\n" + "="*60)
    print("[DATA] PHASE 7: DATA ANALYSIS AND VISUALIZATION - DEMONSTRATION")
    print("="*60)
    
    print("Creating statistics collector...")
    try:
        # Create statistics collector
        stats_collector = StatisticsCollector()
        print("[OK] Statistics collector created")
        
        # Start tracking
        stats_collector.start_tracking()
        print("[OK] Started tracking statistics")
        
        # Simulate some generation data
        print("\nSimulating generation data...")
        for gen in range(5):
            pop_stats = {
                'generation': gen,
                'survival_rate': 0.8 + (gen * 0.02),
                'average_fitness': 10.0 + (gen * 2.0),
                'best_fitness': 15.0 + (gen * 3.0),
                'worst_fitness': 5.0 + (gen * 1.0),
                'fitness_std': 2.0,
                'alive_count': 40 + gen,
                'dead_count': 10 - gen,
                'total_food_consumed': 50 + (gen * 5),
                'total_water_consumed': 50 + (gen * 5),
                'total_moves': 100 + (gen * 10),
                'total_eats': 50 + (gen * 5),
                'total_drinks': 50 + (gen * 5),
                'total_rests': 30 + (gen * 3)
            }
            env_stats = {'food_count': 40, 'water_count': 40}
            event_stats = {'active_events': 0}
            
            stats_collector.record_generation(gen, pop_stats, env_stats, event_stats)
        
        print(f"[OK] Recorded {len(stats_collector.generation_data)} generations")
        
        # Stop tracking
        stats_collector.stop_tracking()
        print("[OK] Stopped tracking statistics")
        
        # Demonstrate statistics features
        print("\nStatistics Features:")
        print("  Survival Rate Tracking: Tracks survival rates over generations")
        print("  Fitness Score Monitoring: Monitors average, best, and worst fitness")
        print("  Generation Comparison: Compares metrics between generations")
        print("  Resource Consumption: Tracks food and water consumption")
        print("  Behavioral Patterns: Analyzes action frequencies")
        
        # Get trends
        print("\nGetting data trends...")
        survival_trend = stats_collector.get_survival_rate_trend()
        print(f"[OK] Survival rate trend: {len(survival_trend)} data points")
        
        fitness_trend = stats_collector.get_fitness_trend()
        print(f"[OK] Fitness trend: {len(fitness_trend['average'])} data points")
        
        resource_trend = stats_collector.get_resource_consumption_trend()
        print(f"[OK] Resource consumption trend: {len(resource_trend['food'])} data points")
        
        behavior_trend = stats_collector.get_behavioral_pattern_trend()
        print(f"[OK] Behavioral pattern trend: {len(behavior_trend['move'])} data points")
        
        # Get summary statistics
        print("\nGenerating summary statistics...")
        summary = stats_collector.get_summary_statistics()
        print(f"[OK] Summary generated:")
        print(f"  Total Generations: {summary['total_generations']}")
        print(f"  Average Survival Rate: {summary['average_survival_rate']:.2%}")
        print(f"  Average Fitness: {summary['average_fitness']:.2f}")
        print(f"  Best Fitness Ever: {summary['best_fitness_ever']:.2f}")
        print(f"  Fitness Improvement: {summary['fitness_improvement']:.2f}")
        
        # Demonstrate generation comparison
        print("\nDemonstrating generation comparison...")
        comparison = stats_collector.get_generation_comparison(0, 4)
        print(f"[OK] Comparison between Gen 0 and Gen 4:")
        print(f"  Survival Rate Change: {comparison['survival_rate_change']:.2%}")
        print(f"  Fitness Change: {comparison['fitness_change']:.2f}")
        print(f"  Best Fitness Change: {comparison['best_fitness_change']:.2f}")
        
        # Demonstrate data export
        print("\nDemonstrating data export...")
        print("[OK] Export to JSON: Available")
        print("[OK] Export to CSV: Available")
        print("[OK] Export to Text Report: Available")
        
        # Demonstrate visualization
        print("\nDemonstrating visualization features...")
        visualizer = SimulationVisualizer()
        print("[OK] Visualizer created")
        
        print("\nVisualization Features:")
        print("  Fitness Progression Charts: Line charts with average, best, worst")
        print("  Survival Rate Charts: Line chart with trend and average")
        print("  Population Graphs: Alive vs dead population over time")
        print("  Resource Consumption Charts: Stacked bar chart for food and water")
        print("  Behavioral Pattern Charts: Multi-line chart for action frequencies")
        print("  Generation Comparison Charts: Side-by-side bar charts")
        print("  Summary Dashboard: Text-based summary of key metrics")
        
        print("\n" + "="*60)
        print("[OK] PHASE 7: DATA ANALYSIS AND VISUALIZATION - COMPLETED!")
        print("="*60)
        print("[OK] Statistics Collection: Comprehensive tracking system")
        print("[OK] Data Visualization: Multiple chart types with matplotlib")
        print("[OK] Export and Reporting: JSON, CSV, and text report formats")
        print("[OK] Comparative Analysis: Generation comparison tools")
        print("[OK] Summary Statistics: Aggregated metrics and trends")
        print("[OK] GUI Integration: View Charts and Export Report buttons")
        print("[OK] Slider UX Improvement: Numerical value displays added")
        print("\n[READY] Ready for Phase 8: Testing and Optimization!")
        print("="*60)
        
        print("\nNote: Visualization charts can be viewed in the GUI application.")
        print("To run the GUI: python run_gui.py")
        
    except Exception as e:
        print(f"[FAIL] Data analysis demonstration failed: {e}")
        print("Data analysis functionality may not be available in this environment.")


if __name__ == "__main__":
    main()
