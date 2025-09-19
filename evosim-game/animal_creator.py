"""
EvoSim Animal Creator & Customization

This module handles the creation and customization of animals, including
the initial training system and trait allocation.

Reference: Section V - Parameters and Variables, Section VII - Preparations Stage
"""

import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

import constants
from data_structures import (
    Animal, AnimalCategory, create_random_animal, Effect, EffectType
)


class TrainingQuestion(Enum):
    """Training questions for initial animal customization."""
    HUNTING_STYLE = "hunting_style"
    SURVIVAL_PRIORITY = "survival_priority"
    ENVIRONMENT_PREFERENCE = "environment_preference"
    COMBAT_APPROACH = "combat_approach"
    RESOURCE_STRATEGY = "resource_strategy"


@dataclass
class QuestionOption:
    """Represents an option for a training question."""
    text: str
    trait_bonus: str  # Which trait gets +1
    description: str


@dataclass
class TrainingQuestionData:
    """Complete training question with options."""
    question: str
    options: List[QuestionOption]


class AnimalCreator:
    """Handles animal creation and customization."""
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize the animal creator."""
        self.random = random.Random(seed)
        self.training_questions = self._create_training_questions()
    
    def _create_training_questions(self) -> Dict[TrainingQuestion, TrainingQuestionData]:
        """Create the training questions for animal customization."""
        questions = {}
        
        # Question 1: Hunting Style
        questions[TrainingQuestion.HUNTING_STYLE] = TrainingQuestionData(
            question="What is your preferred hunting style?",
            options=[
                QuestionOption(
                    text="Ambush and strike quickly",
                    trait_bonus="AGI",
                    description="Focus on speed and stealth"
                ),
                QuestionOption(
                    text="Direct confrontation",
                    trait_bonus="STR",
                    description="Rely on strength and power"
                ),
                QuestionOption(
                    text="Patient observation",
                    trait_bonus="PER",
                    description="Use intelligence and awareness"
                ),
                QuestionOption(
                    text="Endure long pursuits",
                    trait_bonus="END",
                    description="Outlast your prey"
                )
            ]
        )
        
        # Question 2: Survival Priority
        questions[TrainingQuestion.SURVIVAL_PRIORITY] = TrainingQuestionData(
            question="What is your top survival priority?",
            options=[
                QuestionOption(
                    text="Finding food quickly",
                    trait_bonus="AGI",
                    description="Speed in resource gathering"
                ),
                QuestionOption(
                    text="Avoiding predators",
                    trait_bonus="PER",
                    description="Awareness of threats"
                ),
                QuestionOption(
                    text="Conserving energy",
                    trait_bonus="END",
                    description="Efficiency in movement"
                ),
                QuestionOption(
                    text="Learning from experience",
                    trait_bonus="INT",
                    description="Adaptability and intelligence"
                )
            ]
        )
        
        # Question 3: Environment Preference
        questions[TrainingQuestion.ENVIRONMENT_PREFERENCE] = TrainingQuestionData(
            question="Which environment do you prefer?",
            options=[
                QuestionOption(
                    text="Open plains",
                    trait_bonus="AGI",
                    description="Speed and mobility"
                ),
                QuestionOption(
                    text="Dense forests",
                    trait_bonus="PER",
                    description="Stealth and awareness"
                ),
                QuestionOption(
                    text="Harsh mountains",
                    trait_bonus="END",
                    description="Endurance and toughness"
                ),
                QuestionOption(
                    text="Complex terrain",
                    trait_bonus="INT",
                    description="Problem-solving ability"
                )
            ]
        )
        
        # Question 4: Combat Approach
        questions[TrainingQuestion.COMBAT_APPROACH] = TrainingQuestionData(
            question="How do you handle conflicts?",
            options=[
                QuestionOption(
                    text="Strike first and hard",
                    trait_bonus="STR",
                    description="Overwhelming force"
                ),
                QuestionOption(
                    text="Dodge and counter",
                    trait_bonus="AGI",
                    description="Speed and reflexes"
                ),
                QuestionOption(
                    text="Outsmart opponents",
                    trait_bonus="INT",
                    description="Tactical advantage"
                ),
                QuestionOption(
                    text="Outlast the fight",
                    trait_bonus="END",
                    description="Persistence and stamina"
                )
            ]
        )
        
        # Question 5: Resource Strategy
        questions[TrainingQuestion.RESOURCE_STRATEGY] = TrainingQuestionData(
            question="What's your resource strategy?",
            options=[
                QuestionOption(
                    text="Gather as much as possible",
                    trait_bonus="STR",
                    description="Carrying capacity"
                ),
                QuestionOption(
                    text="Find the best sources",
                    trait_bonus="PER",
                    description="Quality over quantity"
                ),
                QuestionOption(
                    text="Efficient collection",
                    trait_bonus="AGI",
                    description="Speed and efficiency"
                ),
                QuestionOption(
                    text="Plan for the future",
                    trait_bonus="INT",
                    description="Strategic thinking"
                )
            ]
        )
        
        return questions
    
    def create_animal_with_training(
        self, 
        animal_id: str, 
        category: AnimalCategory,
        training_choices: List[int]
    ) -> Animal:
        """Create an animal with custom training choices."""
        if len(training_choices) != len(TrainingQuestion):
            raise ValueError(f"Expected {len(TrainingQuestion)} training choices, got {len(training_choices)}")
        
        # Create base animal
        animal = create_random_animal(animal_id, category)
        
        # Apply training bonuses
        trait_bonuses = self._calculate_training_bonuses(training_choices)
        self._apply_trait_bonuses(animal, trait_bonuses)
        
        return animal
    
    def _calculate_training_bonuses(self, training_choices: List[int]) -> Dict[str, int]:
        """Calculate trait bonuses from training choices."""
        bonuses = {trait: 0 for trait in constants.TRAIT_NAMES}
        
        for i, choice in enumerate(training_choices):
            question_type = list(TrainingQuestion)[i]
            question_data = self.training_questions[question_type]
            
            if 0 <= choice < len(question_data.options):
                trait = question_data.options[choice].trait_bonus
                bonuses[trait] += 1
        
        return bonuses
    
    def _apply_trait_bonuses(self, animal: Animal, bonuses: Dict[str, int]) -> None:
        """Apply trait bonuses to an animal."""
        for trait, bonus in bonuses.items():
            if bonus > 0:
                animal.traits[trait] += bonus
                # Ensure traits don't exceed maximum
                animal.traits[trait] = min(animal.traits[trait], constants.PRIMARY_TRAIT_MAX)
        
        # Recalculate health and energy based on new endurance
        max_health = constants.BASE_HEALTH + (animal.traits['END'] * constants.HEALTH_PER_ENDURANCE)
        max_energy = constants.BASE_ENERGY + (animal.traits['END'] * constants.ENERGY_PER_ENDURANCE)
        
        animal.status['Health'] = float(max_health)
        animal.status['Energy'] = float(max_energy)
    
    def create_animal_with_custom_traits(
        self,
        animal_id: str,
        category: AnimalCategory,
        custom_traits: Dict[str, int]
    ) -> Animal:
        """Create an animal with custom trait values."""
        # Validate custom traits
        self._validate_custom_traits(custom_traits)
        
        # Create base animal
        animal = create_random_animal(animal_id, category)
        
        # Apply custom traits
        for trait, value in custom_traits.items():
            animal.traits[trait] = value
        
        # Recalculate health and energy
        max_health = constants.BASE_HEALTH + (animal.traits['END'] * constants.HEALTH_PER_ENDURANCE)
        max_energy = constants.BASE_ENERGY + (animal.traits['END'] * constants.ENERGY_PER_ENDURANCE)
        
        animal.status['Health'] = float(max_health)
        animal.status['Energy'] = float(max_energy)
        
        return animal
    
    def _validate_custom_traits(self, traits: Dict[str, int]) -> None:
        """Validate custom trait values."""
        # Check for invalid trait names
        for trait in traits:
            if trait not in constants.TRAIT_NAMES:
                raise ValueError(f"Invalid trait: {trait}")
        
        # Check for missing required traits
        for trait in constants.TRAIT_NAMES:
            if trait not in traits:
                raise ValueError(f"Missing required trait: {trait}")
            
            value = traits[trait]
            if not isinstance(value, int) or value < 1:
                raise ValueError(f"Trait {trait} must be a positive integer, got {value}")
            
            if value > constants.PRIMARY_TRAIT_MAX:
                raise ValueError(f"Trait {trait} cannot exceed {constants.PRIMARY_TRAIT_MAX}, got {value}")
    
    def create_population_with_training(
        self,
        population_size: int,
        training_choices: List[List[int]]
    ) -> List[Animal]:
        """Create a population of animals with training choices."""
        if len(training_choices) != population_size:
            raise ValueError(f"Expected {population_size} training choice sets, got {len(training_choices)}")
        
        animals = []
        categories = list(AnimalCategory)
        
        for i in range(population_size):
            category = categories[i % len(categories)]
            animal_id = f"trained_{i:03d}"
            animal = self.create_animal_with_training(animal_id, category, training_choices[i])
            animals.append(animal)
        
        return animals
    
    def create_diverse_population(
        self,
        population_size: int,
        diversity_factor: float = 0.5
    ) -> List[Animal]:
        """Create a diverse population with varied traits."""
        animals = []
        categories = list(AnimalCategory)
        
        for i in range(population_size):
            category = categories[i % len(categories)]
            animal_id = f"diverse_{i:03d}"
            
            # Create base animal
            animal = create_random_animal(animal_id, category)
            
            # Add some random variation
            if self.random.random() < diversity_factor:
                self._add_trait_variation(animal)
            
            animals.append(animal)
        
        return animals
    
    def _add_trait_variation(self, animal: Animal) -> None:
        """Add random variation to an animal's traits."""
        # Randomly boost one trait
        trait_to_boost = self.random.choice(constants.TRAIT_NAMES)
        boost_amount = self.random.randint(1, 2)
        
        animal.traits[trait_to_boost] = min(
            animal.traits[trait_to_boost] + boost_amount,
            constants.PRIMARY_TRAIT_MAX
        )
        
        # Randomly reduce another trait
        trait_to_reduce = self.random.choice(constants.TRAIT_NAMES)
        if trait_to_reduce != trait_to_boost:
            animal.traits[trait_to_reduce] = max(
                animal.traits[trait_to_reduce] - 1,
                constants.STANDARD_TRAIT_MIN
            )
        
        # Recalculate health and energy
        max_health = constants.BASE_HEALTH + (animal.traits['END'] * constants.HEALTH_PER_ENDURANCE)
        max_energy = constants.BASE_ENERGY + (animal.traits['END'] * constants.ENERGY_PER_ENDURANCE)
        
        animal.status['Health'] = float(max_health)
        animal.status['Energy'] = float(max_energy)
    
    def get_training_questions(self) -> Dict[TrainingQuestion, TrainingQuestionData]:
        """Get the training questions for display."""
        return self.training_questions
    
    def analyze_animal_traits(self, animal: Animal) -> Dict[str, any]:
        """Analyze an animal's trait distribution."""
        traits = animal.traits
        total_traits = sum(traits.values())
        
        # Find primary trait
        primary_trait = max(traits, key=traits.get)
        primary_value = traits[primary_trait]
        
        # Calculate trait balance
        trait_values = list(traits.values())
        trait_balance = max(trait_values) - min(trait_values)
        
        # Determine specialization level
        specialization = "High" if trait_balance >= 3 else "Medium" if trait_balance >= 2 else "Low"
        
        # Calculate effective stats
        effective_traits = {}
        for trait in constants.TRAIT_NAMES:
            effective_traits[trait] = animal.get_effective_trait(trait)
        
        return {
            'total_traits': total_traits,
            'primary_trait': primary_trait,
            'primary_value': primary_value,
            'trait_balance': trait_balance,
            'specialization': specialization,
            'effective_traits': effective_traits,
            'max_health': animal.get_max_health(),
            'max_energy': animal.get_max_energy()
        }


class AnimalCustomizer:
    """Handles advanced animal customization and trait optimization."""
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize the animal customizer."""
        self.random = random.Random(seed)
    
    def optimize_animal_for_category(self, animal: Animal) -> Animal:
        """Optimize an animal's traits for its category."""
        category = animal.category
        primary_trait = constants.CATEGORY_PRIMARY_TRAITS[category.value]
        
        # Boost primary trait if it's not already maxed
        if animal.traits[primary_trait] < constants.PRIMARY_TRAIT_MAX:
            animal.traits[primary_trait] = constants.PRIMARY_TRAIT_MAX
        
        # Ensure other traits are within standard range
        for trait in constants.TRAIT_NAMES:
            if trait != primary_trait:
                if animal.traits[trait] < constants.STANDARD_TRAIT_MIN:
                    animal.traits[trait] = constants.STANDARD_TRAIT_MIN
                elif animal.traits[trait] > constants.STANDARD_TRAIT_MAX:
                    animal.traits[trait] = constants.STANDARD_TRAIT_MAX
        
        # Recalculate health and energy
        max_health = constants.BASE_HEALTH + (animal.traits['END'] * constants.HEALTH_PER_ENDURANCE)
        max_energy = constants.BASE_ENERGY + (animal.traits['END'] * constants.ENERGY_PER_ENDURANCE)
        
        animal.status['Health'] = float(max_health)
        animal.status['Energy'] = float(max_energy)
        
        return animal
    
    def create_balanced_animal(
        self,
        animal_id: str,
        category: AnimalCategory,
        target_total: int = 30
    ) -> Animal:
        """Create an animal with balanced traits."""
        # Calculate trait distribution
        primary_trait = constants.CATEGORY_PRIMARY_TRAITS[category.value]
        remaining_points = target_total - constants.PRIMARY_TRAIT_MAX
        
        # Distribute remaining points among other traits
        other_traits = [t for t in constants.TRAIT_NAMES if t != primary_trait]
        points_per_trait = remaining_points // len(other_traits)
        extra_points = remaining_points % len(other_traits)
        
        traits = {primary_trait: constants.PRIMARY_TRAIT_MAX}
        for i, trait in enumerate(other_traits):
            base_points = points_per_trait
            if i < extra_points:
                base_points += 1
            traits[trait] = max(constants.STANDARD_TRAIT_MIN, base_points)
        
        # Create animal with custom traits
        creator = AnimalCreator()
        return creator.create_animal_with_custom_traits(animal_id, category, traits)
    
    def create_specialized_animal(
        self,
        animal_id: str,
        category: AnimalCategory,
        specialization_trait: str,
        specialization_level: int = 9
    ) -> Animal:
        """Create an animal specialized in a specific trait."""
        if specialization_trait not in constants.TRAIT_NAMES:
            raise ValueError(f"Invalid trait: {specialization_trait}")
        
        if not isinstance(specialization_level, int) or specialization_level < 1:
            raise ValueError(f"Specialization level must be a positive integer, got {specialization_level}")
        
        if specialization_level > constants.PRIMARY_TRAIT_MAX:
            raise ValueError(f"Specialization level cannot exceed {constants.PRIMARY_TRAIT_MAX}, got {specialization_level}")
        
        # Create base animal
        animal = create_random_animal(animal_id, category)
        
        # Set specialization trait
        animal.traits[specialization_trait] = specialization_level
        
        # Distribute remaining points
        remaining_points = 30 - specialization_level
        other_traits = [t for t in constants.TRAIT_NAMES if t != specialization_trait]
        points_per_trait = remaining_points // len(other_traits)
        extra_points = remaining_points % len(other_traits)
        
        for i, trait in enumerate(other_traits):
            base_points = points_per_trait
            if i < extra_points:
                base_points += 1
            animal.traits[trait] = max(constants.STANDARD_TRAIT_MIN, base_points)
        
        # Recalculate health and energy
        max_health = constants.BASE_HEALTH + (animal.traits['END'] * constants.HEALTH_PER_ENDURANCE)
        max_energy = constants.BASE_ENERGY + (animal.traits['END'] * constants.ENERGY_PER_ENDURANCE)
        
        animal.status['Health'] = float(max_health)
        animal.status['Energy'] = float(max_energy)
        
        return animal


def create_animal_with_questions(animal_id: str, category: AnimalCategory) -> Tuple[Animal, List[TrainingQuestionData]]:
    """Interactive function to create an animal with training questions."""
    creator = AnimalCreator()
    questions = creator.get_training_questions()
    
    # For now, return random choices (in a real implementation, this would be interactive)
    training_choices = [random.randint(0, 3) for _ in range(len(TrainingQuestion))]
    animal = creator.create_animal_with_training(animal_id, category, training_choices)
    
    question_list = [questions[q] for q in TrainingQuestion]
    return animal, question_list


if __name__ == "__main__":
    # Test the animal creator
    print("🧪 Testing Animal Creator...")
    
    creator = AnimalCreator(seed=42)
    
    # Test basic creation
    animal = creator.create_animal_with_training("test_001", AnimalCategory.HERBIVORE, [0, 1, 2, 3, 4])
    print(f"Created {animal.category.value} with traits: {animal.traits}")
    
    # Test analysis
    analysis = creator.analyze_animal_traits(animal)
    print(f"Analysis: {analysis}")
    
    print("✅ Animal Creator test completed!")
