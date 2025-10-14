"""
Test script for improved animal behavior with resource detection
"""

import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.simulation import Simulation

def test_animal_behavior():
    """Test the improved animal behavior with resource detection."""
    
    print("[TEST] Animal Behavior with Resource Detection")
    print("=" * 60)
    
    # Load optimal configuration
    with open('config/optimal_config.json', 'r') as f:
        config = json.load(f)
    
    # Create simulation
    simulation = Simulation(config)
    simulation.initialize()
    
    print(f"[OK] Simulation initialized with {len(simulation.population.animals)} animals")
    print(f"[INFO] Grid size: {simulation.environment.width}x{simulation.environment.height}")
    print(f"[INFO] Food: {simulation.environment.food_count}, Water: {simulation.environment.water_count}")
    
    # Test animal decision-making with resource detection
    print(f"\n[TEST] Testing Animal Decision-Making:")
    print("-" * 50)
    
    for i, animal in enumerate(simulation.environment.animals[:5]):  # Test first 5 animals
        # Get animal's sensory input with resource detection
        inputs = animal.sense_environment(simulation.environment)
        decision = animal.make_decision(simulation.environment)
        
        print(f"Animal {i+1} ({animal.animal_id[:8]}):")
        print(f"  Position: {animal.position}")
        print(f"  Health: H:{animal.hunger:.0f} T:{animal.thirst:.0f} E:{animal.energy:.0f}")
        print(f"  Sensory: Hunger:{inputs[0]:.2f} Thirst:{inputs[1]:.2f} Food:{inputs[2]:.1f} Water:{inputs[3]:.1f}")
        print(f"  Decision: {decision}")
        print()
    
    # Run simulation steps
    print(f"[RUN] Running simulation steps...")
    for step in range(10):
        simulation._run_step()
        
        # Get statistics
        alive_count = len(simulation.environment.animals)
        dead_count = len(simulation.environment.dead_animals)
        
        # Count actions
        total_moves = sum(animal.behavioral_counts.get('move', 0) for animal in simulation.environment.animals)
        total_eats = sum(animal.behavioral_counts.get('eat', 0) for animal in simulation.environment.animals)
        total_drinks = sum(animal.behavioral_counts.get('drink', 0) for animal in simulation.environment.animals)
        total_rests = sum(animal.behavioral_counts.get('rest', 0) for animal in simulation.environment.animals)
        
        print(f"Step {step+1:2d}: {alive_count:2d} alive, {dead_count:2d} dead | Actions: M:{total_moves} E:{total_eats} D:{total_drinks} R:{total_rests}")
        
        if alive_count == 0:
            print(f"[FAIL] All animals died at step {step+1}")
            break
    
    # Final statistics
    print(f"\n[SUMMARY] Final Results:")
    print(f"- Alive: {alive_count}")
    print(f"- Dead: {dead_count}")
    print(f"- Survival rate: {alive_count/(alive_count+dead_count)*100:.1f}%")
    
    # Check if animals are now moving and consuming resources
    if total_moves > 0:
        print(f"[SUCCESS] Animals are now moving! ({total_moves} moves)")
    else:
        print(f"[WARNING] Animals still not moving")
    
    if total_eats > 0 or total_drinks > 0:
        print(f"[SUCCESS] Animals are consuming resources! (Eats: {total_eats}, Drinks: {total_drinks})")
    else:
        print(f"[WARNING] Animals still not consuming resources")
    
    return alive_count > 0

if __name__ == "__main__":
    success = test_animal_behavior()
    sys.exit(0 if success else 1)
