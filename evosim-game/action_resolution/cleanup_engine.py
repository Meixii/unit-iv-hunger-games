"""
Cleanup Engine

This module handles Phase 4 of the action resolution system: applying new effects
and removing expired effects.
"""

from typing import List, Dict, Any
import logging

# Import from parent directory
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures import Animal, Simulation, Effect, EffectType


class CleanupEngine:
    """
    Handles the Cleanup Phase of action resolution.
    
    Any new effects are applied (e.g., 'Well-Fed' after eating), and expired effects are removed.
    """
    
    def __init__(self, simulation: Simulation, logger: logging.Logger):
        """Initialize the cleanup engine."""
        self.simulation = simulation
        self.logger = logger
    
    def execute_cleanup_phase(self, living_animals: List[Animal]) -> Dict[str, Any]:
        """
        Phase 4: Cleanup Phase
        Apply new effects and remove expired effects.
        """
        results = {
            'animals_processed': 0,
            'effects_added': 0,
            'effects_removed': 0,
            'effects_updated': 0
        }
        
        for animal in living_animals:
            try:
                # Process existing effects
                effects_to_remove = []
                
                for effect in animal.active_effects:
                    # Decrease duration
                    if hasattr(effect, 'duration') and effect.duration > 0:
                        effect.duration -= 1
                        results['effects_updated'] += 1
                        
                        # Mark for removal if expired
                        if effect.duration <= 0:
                            effects_to_remove.append(effect)
                
                # Remove expired effects
                for effect in effects_to_remove:
                    animal.active_effects.remove(effect)
                    results['effects_removed'] += 1
                    self.logger.debug(f"Removed expired effect {effect.name} from {animal.animal_id}")
                
                # Add new effects based on conditions
                # Well-Fed effect after eating
                if animal.status.get('Hunger', 100) >= 90 and not any(e.name == EffectType.WELL_FED.value for e in animal.active_effects):
                    well_fed_effect = Effect(
                        name=EffectType.WELL_FED.value,
                        duration=3
                    )
                    animal.active_effects.append(well_fed_effect)
                    results['effects_added'] += 1
                    self.logger.debug(f"Added Well-Fed effect to {animal.animal_id}")
                
                # Exhausted effect from low energy
                if animal.status.get('Energy', 100) <= 20 and not any(e.name == EffectType.EXHAUSTED.value for e in animal.active_effects):
                    exhausted_effect = Effect(
                        name=EffectType.EXHAUSTED.value,
                        duration=2
                    )
                    animal.active_effects.append(exhausted_effect)
                    results['effects_added'] += 1
                    self.logger.debug(f"Added Exhausted effect to {animal.animal_id}")
                
                results['animals_processed'] += 1
                
            except Exception as e:
                self.logger.warning(f"Cleanup phase failed for animal {animal.animal_id}: {e}")
        
        return results
