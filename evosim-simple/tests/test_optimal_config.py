#!/usr/bin/env python3
"""
Test script for optimal configuration
"""

import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.simulation import Simulation

def test_optimal_config():
    """Test the optimal configuration."""
    
    # Load optimal configuration
    with open('config/optimal_config.json', 'r') as f:
        config = json.load(f)
    
    print("[TEST] Testing Optimal Configuration")
    print("=" * 50)
    
    # Create simulation
    simulation = Simulation(config)
    simulation.initialize()
    
    print(f"[OK] Simulation initialized")
    print(f"[INFO] Population size: {len(simulation.population.animals)}")
    print(f"[INFO] Grid size: {simulation.environment.width}x{simulation.environment.height}")
    print(f"[INFO] Food density: {config['food_density']}")
    print(f"[INFO] Water density: {config['water_density']}")
    print(f"[INFO] Event probabilities: {config['drought_probability']}, {config['storm_probability']}, {config['famine_probability']}, {config['bonus_probability']}")
    
    # Run a few steps to test
    print("\n[RUN] Running test steps...")
    for i in range(10):
        simulation._run_step()
        alive = len(simulation.environment.get_alive_animals())
        print(f"Step {i+1}: {alive} animals alive")
        
        if alive == 0:
            print("[FAIL] All animals died!")
            return False
    
    print("[OK] Test completed successfully!")
    return True

if __name__ == "__main__":
    success = test_optimal_config()
    sys.exit(0 if success else 1)
