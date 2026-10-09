"""
Unit tests for data_structures.py
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures import (
    Animal, World, Tile, Resource, Effect, Simulation,
    AnimalCategory, TerrainType, ResourceType, EffectType, ActionType,
    create_random_animal, create_effect, create_resource, validate_data_structures
)
import constants


class TestDataStructures(unittest.TestCase):
    """Test core data structures and entity containers."""

    def test_validate_data_structures(self):
        """Test internal validation passes."""
        try:
            validate_data_structures()
        except Exception as e:
            self.fail(f"validate_data_structures() raised an error: {e}")

    def test_animal_creation_and_stats(self):
        """Test Animal traits, derived health and energy calculations."""
        animal = create_random_animal("test_01", AnimalCategory.HERBIVORE)
        self.assertEqual(animal.animal_id, "test_01")
        self.assertEqual(animal.category, AnimalCategory.HERBIVORE)
        self.assertEqual(animal.passive, "Efficient Grazer")
        
        # Derived calculations
        expected_health = constants.BASE_HEALTH + (animal.traits['END'] * constants.HEALTH_PER_ENDURANCE)
        expected_energy = constants.BASE_ENERGY + (animal.traits['END'] * constants.ENERGY_PER_ENDURANCE)
        self.assertEqual(animal.get_max_health(), expected_health)
        self.assertEqual(animal.get_max_energy(), expected_energy)
        self.assertTrue(animal.is_alive())

    def test_effects_and_modifiers(self):
        """Test adding, ticking, and removing effects."""
        animal = create_random_animal("test_02", AnimalCategory.CARNIVORE)
        base_str = animal.traits['STR']
        
        effect = create_effect(
            effect_type=EffectType.WELL_FED,
            duration=3
        )
        animal.add_effect(effect)
        self.assertEqual(animal.get_effective_trait('STR'), base_str + 1)
        
        # Tick effect
        animal.tick_effects()
        self.assertEqual(effect.duration, 2)
        animal.tick_effects()
        animal.tick_effects()
        # Expired effect is removed
        self.assertEqual(animal.get_effective_trait('STR'), base_str)

    def test_simulation_graveyard_and_casualties(self):
        """Test Simulation entity list management, graveyard, and get_dead_animals."""
        sim = Simulation()
        a1 = create_random_animal("a1", AnimalCategory.HERBIVORE)
        a2 = create_random_animal("a2", AnimalCategory.CARNIVORE)
        sim.add_animal(a1)
        sim.add_animal(a2)
        
        self.assertEqual(len(sim.get_living_animals()), 2)
        self.assertEqual(len(sim.get_dead_animals()), 0)
        
        # a1 dies and is removed
        a1.status['Health'] = 0.0
        sim.remove_animal(a1)
        
        self.assertEqual(len(sim.get_living_animals()), 1)
        self.assertIn(a2, sim.get_living_animals())
        self.assertEqual(len(sim.get_dead_animals()), 1)
        self.assertIn(a1, sim.get_dead_animals())


if __name__ == '__main__':
    unittest.main()
