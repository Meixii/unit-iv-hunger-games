#!/usr/bin/env python3
"""
Demonstration script for the new Animal List functionality
"""

import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.simulation import Simulation

def demo_animal_list():
    """Demonstrate the animal list functionality."""
    
    print("[DEMO] Animal List Functionality Demonstration")
    print("=" * 60)
    
    # Load optimal configuration
    with open('config/optimal_config.json', 'r') as f:
        config = json.load(f)
    
    # Create simulation
    simulation = Simulation(config)
    simulation.initialize()
    
    print(f"[OK] Simulation initialized with {len(simulation.population.animals)} animals")
    
    # Run a few steps to generate some data
    print("\n[RUN] Running simulation steps...")
    for step in range(20):
        simulation._run_step()
        
        # Get animal data
        all_animals = simulation.environment.animals + simulation.environment.dead_animals
        alive_count = len(simulation.environment.animals)
        dead_count = len(simulation.environment.dead_animals)
        
        print(f"Step {step+1:2d}: {alive_count:2d} alive, {dead_count:2d} dead")
        
        # Show detailed animal info every 5 steps
        if (step + 1) % 5 == 0:
            print(f"\n[ANIMALS] Detailed Animal Statistics (Step {step+1}):")
            print("-" * 80)
            print(f"{'ID':<12} {'Position':<10} {'Status':<6} {'Health':<20} {'Age':<4} {'Fitness':<8} {'Actions':<20}")
            print("-" * 80)
            
            for animal in all_animals[:10]:  # Show first 10 animals
                state = animal.get_state()
                health = f"H:{state['hunger']:.0f} T:{state['thirst']:.0f} E:{state['energy']:.0f}"
                pos = f"({state['coordinates']['x']},{state['coordinates']['y']})"
                status = "Alive" if state['alive'] else "Dead"
                actions = f"M:{state['behavioral_counts']['move']} E:{state['behavioral_counts']['eat']} D:{state['behavioral_counts']['drink']} R:{state['behavioral_counts']['rest']}"
                
                print(f"{state['animal_id'][:10]:<12} {pos:<10} {status:<6} {health:<20} {state['age']:<4} {state['fitness']:<8.1f} {actions:<20}")
            
            if len(all_animals) > 10:
                print(f"... and {len(all_animals) - 10} more animals")
    
    print(f"\n[SUMMARY] Final Statistics:")
    print(f"- Total animals: {len(all_animals)}")
    print(f"- Alive: {alive_count}")
    print(f"- Dead: {dead_count}")
    print(f"- Survival rate: {alive_count/len(all_animals)*100:.1f}%")
    
    # Show behavioral patterns
    print(f"\n[BEHAVIOR] Behavioral Patterns:")
    total_moves = sum(animal.behavioral_counts.get('move', 0) for animal in all_animals)
    total_eats = sum(animal.behavioral_counts.get('eat', 0) for animal in all_animals)
    total_drinks = sum(animal.behavioral_counts.get('drink', 0) for animal in all_animals)
    total_rests = sum(animal.behavioral_counts.get('rest', 0) for animal in all_animals)
    
    print(f"- Total Moves: {total_moves}")
    print(f"- Total Eats: {total_eats}")
    print(f"- Total Drinks: {total_drinks}")
    print(f"- Total Rests: {total_rests}")
    
    print(f"\n[SUCCESS] Animal list functionality demonstrated!")
    print(f"[INFO] In the GUI, you can now see:")
    print(f"  - Individual animal statistics in real-time")
    print(f"  - Health status (Hunger, Thirst, Energy)")
    print(f"  - Position coordinates")
    print(f"  - Behavioral action counts")
    print(f"  - Age and fitness scores")
    print(f"  - Export individual animal data")

if __name__ == "__main__":
    demo_animal_list()
