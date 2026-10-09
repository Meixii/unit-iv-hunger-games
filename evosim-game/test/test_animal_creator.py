"""
Unit tests for animal_creator.py
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from animal_creator import AnimalCreator, AnimalCustomizer, run_training_cli
from data_structures import AnimalCategory
import constants


class TestAnimalCreator(unittest.TestCase):
    """Test animal creation, training question bonuses, and customization."""

    def test_training_choices_apply_bonuses(self):
        """Test answering 5 training questions grants exactly 5 trait bonuses."""
        creator = AnimalCreator(seed=42)
        bonuses = creator._calculate_training_bonuses([0, 1, 2, 3, 0])
        self.assertEqual(sum(bonuses.values()), 5)
        
        base = creator.create_animal_with_custom_traits("base", AnimalCategory.HERBIVORE, {
            'STR': 5, 'AGI': 5, 'INT': 5, 'END': 5, 'PER': 5
        })
        base_total = sum(base.traits.values())
        creator._apply_trait_bonuses(base, bonuses)
        self.assertEqual(sum(base.traits.values()), base_total + 5)

    def test_run_training_cli_non_interactive(self):
        """Test Task 4.1 CLI interface execution in headless mode."""
        animal = run_training_cli(
            interactive=False,
            preset_category=AnimalCategory.CARNIVORE,
            preset_choices=[0, 1, 2, 3, 0],
            animal_id="cli_predator"
        )
        self.assertEqual(animal.animal_id, "cli_predator")
        self.assertEqual(animal.category, AnimalCategory.CARNIVORE)
        self.assertEqual(animal.passive, "Ambush Predator")
        self.assertGreaterEqual(animal.traits['STR'], 7)

    def test_balanced_and_specialized_animals(self):
        """Test AnimalCustomizer optimization and specialization."""
        customizer = AnimalCustomizer()
        balanced = customizer.create_balanced_animal("bal_omni", AnimalCategory.OMNIVORE)
        self.assertEqual(balanced.category, AnimalCategory.OMNIVORE)
        self.assertEqual(balanced.traits['END'], constants.PRIMARY_TRAIT_MAX)
        
        spec = customizer.create_specialized_animal("spec_agi", AnimalCategory.HERBIVORE, 'AGI', specialization_level=9)
        self.assertEqual(spec.traits['AGI'], 9)


if __name__ == '__main__':
    unittest.main()
