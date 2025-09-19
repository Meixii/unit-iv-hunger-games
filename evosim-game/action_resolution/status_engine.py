"""
Status & Environmental Engine

This module handles Phase 2 of the action resolution system: applying passive changes
to all animals simultaneously before actions are executed.
"""

from typing import List, Dict, Any
import logging

# Import from parent directory
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures import Animal, Simulation, EffectType
from fitness import increment_time


class StatusEngine:
    """
    Handles the Status & Environmental Phase of action resolution.
    
    Before actions are taken, passive changes are applied to all animals simultaneously:
    - Hunger and Thirst depletion
    - Health loss from debuffs like 'Poisoned'
    - Passive Energy regeneration
    """
    
    def __init__(self, simulation: Simulation, logger: logging.Logger):
        """Initialize the status engine."""
        self.simulation = simulation
        self.logger = logger
    
    def execute_status_environmental_phase(self, living_animals: List[Animal]) -> Dict[str, Any]:
        """
        Phase 2: Status & Environmental Phase
        Apply passive changes to all animals simultaneously.
        """
        results = {
            'animals_processed': 0,
            'hunger_depletion': 0,
            'thirst_depletion': 0,
            'health_loss': 0,
            'energy_regeneration': 0,
            'casualties': []
        }
        
        animals_to_remove = []
        
        for animal in living_animals:
            try:
                # Count time survived (per action resolution cycle)
                increment_time(animal, 1)
                # Apply hunger depletion
                current_hunger = animal.status.get('Hunger', 100)
                new_hunger = max(0, current_hunger - 3)  # Lose 3 hunger per turn
                animal.status['Hunger'] = new_hunger
                if current_hunger != new_hunger:
                    results['hunger_depletion'] += 1
                
                # Apply thirst depletion
                current_thirst = animal.status.get('Thirst', 100)
                new_thirst = max(0, current_thirst - 2)  # Lose 2 thirst per turn
                animal.status['Thirst'] = new_thirst
                if current_thirst != new_thirst:
                    results['thirst_depletion'] += 1
                
                # Apply health loss from debuffs
                health_loss = 0
                for effect in animal.active_effects:
                    if effect.name == EffectType.POISONED.value:
                        health_loss += 5
                    elif effect.name == EffectType.INJURED.value:
                        health_loss += 3
                
                if health_loss > 0:
                    current_health = animal.status.get('Health', 100)
                    new_health = max(0, current_health - health_loss)
                    animal.status['Health'] = new_health
                    results['health_loss'] += 1
                
                # Apply passive energy regeneration (if resting or healthy)
                current_energy = animal.status.get('Energy', 100)
                if current_energy < 100:
                    energy_regen = 2 if animal.status.get('Health', 100) > 50 else 1
                    new_energy = min(100, current_energy + energy_regen)
                    animal.status['Energy'] = new_energy
                    if current_energy != new_energy:
                        results['energy_regeneration'] += 1
                
                # Check for death conditions
                if (animal.status.get('Health', 100) <= 0 or 
                    animal.status.get('Hunger', 100) <= 0 or 
                    animal.status.get('Thirst', 100) <= 0):
                    
                    death_cause = []
                    if animal.status.get('Health', 100) <= 0:
                        death_cause.append("health")
                    if animal.status.get('Hunger', 100) <= 0:
                        death_cause.append("starvation")
                    if animal.status.get('Thirst', 100) <= 0:
                        death_cause.append("dehydration")
                    
                    self.logger.info(f"Animal {animal.animal_id} died from {', '.join(death_cause)}")
                    animals_to_remove.append(animal)
                    results['casualties'].append({
                        'animal_id': animal.animal_id,
                        'cause': ', '.join(death_cause)
                    })
                
                results['animals_processed'] += 1
                
            except Exception as e:
                self.logger.warning(f"Status phase failed for animal {animal.animal_id}: {e}")
        
        # Remove dead animals
        for animal in animals_to_remove:
            self.simulation.remove_animal(animal)
        
        return results
