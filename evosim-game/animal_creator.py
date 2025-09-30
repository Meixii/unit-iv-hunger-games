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
    MOVEMENT_STYLE = "movement_style"
    SURVIVAL_PRIORITY = "survival_priority"
    ENVIRONMENT_PREFERENCE = "environment_preference"
    CONFLICT_RESOLUTION = "conflict_resolution"
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
        """Initialize the animal creator with optional seed for reproducible results.
        
        Args:
            seed: Optional random seed for reproducible animal generation
        """
        self.random = random.Random(seed)
        self.training_questions = self._create_training_questions()
    
    def _create_training_questions(self) -> Dict[TrainingQuestion, TrainingQuestionData]:
        """Create the training questions for animal customization.
        
        Generates a set of 5 general survival questions that work for any animal category.
        Each question has 4 options, each corresponding to a different trait bonus.
        
        Returns:
            Dictionary mapping question types to their data and options
        """
        questions = {}
        
        # Question 1: Movement Style
        questions[TrainingQuestion.MOVEMENT_STYLE] = TrainingQuestionData(
            question="How do you prefer to move through your environment?",
            options=[
                QuestionOption(
                    text="Quick bursts of speed",
                    trait_bonus="AGI",
                    description="Fast, agile movements"
                ),
                QuestionOption(
                    text="Steady, powerful strides",
                    trait_bonus="STR",
                    description="Strong, determined movement"
                ),
                QuestionOption(
                    text="Careful, calculated steps",
                    trait_bonus="PER",
                    description="Observant and cautious approach"
                ),
                QuestionOption(
                    text="Consistent, long-distance travel",
                    trait_bonus="END",
                    description="Enduring, persistent movement"
                )
            ]
        )
        
        # Question 2: Survival Priority
        questions[TrainingQuestion.SURVIVAL_PRIORITY] = TrainingQuestionData(
            question="What is your top survival priority?",
            options=[
                QuestionOption(
                    text="Finding resources quickly",
                    trait_bonus="AGI",
                    description="Speed in gathering food and water"
                ),
                QuestionOption(
                    text="Avoiding danger",
                    trait_bonus="PER",
                    description="Awareness of threats and hazards"
                ),
                QuestionOption(
                    text="Conserving energy",
                    trait_bonus="END",
                    description="Efficiency and endurance"
                ),
                QuestionOption(
                    text="Learning and adapting",
                    trait_bonus="INT",
                    description="Intelligence and problem-solving"
                )
            ]
        )
        
        # Question 3: Environment Preference
        questions[TrainingQuestion.ENVIRONMENT_PREFERENCE] = TrainingQuestionData(
            question="Which type of environment do you prefer?",
            options=[
                QuestionOption(
                    text="Open, wide spaces",
                    trait_bonus="AGI",
                    description="Speed and mobility"
                ),
                QuestionOption(
                    text="Dense, complex areas",
                    trait_bonus="PER",
                    description="Stealth and awareness"
                ),
                QuestionOption(
                    text="Challenging, harsh terrain",
                    trait_bonus="END",
                    description="Endurance and toughness"
                ),
                QuestionOption(
                    text="Varied, changing landscapes",
                    trait_bonus="INT",
                    description="Adaptability and problem-solving"
                )
            ]
        )
        
        # Question 4: Conflict Resolution
        questions[TrainingQuestion.CONFLICT_RESOLUTION] = TrainingQuestionData(
            question="How do you handle conflicts or threats?",
            options=[
                QuestionOption(
                    text="Face them head-on",
                    trait_bonus="STR",
                    description="Direct confrontation and strength"
                ),
                QuestionOption(
                    text="Escape quickly",
                    trait_bonus="AGI",
                    description="Speed and evasion"
                ),
                QuestionOption(
                    text="Outsmart the situation",
                    trait_bonus="INT",
                    description="Intelligence and strategy"
                ),
                QuestionOption(
                    text="Endure and persist",
                    trait_bonus="END",
                    description="Patience and resilience"
                )
            ]
        )
        
        # Question 5: Resource Strategy
        questions[TrainingQuestion.RESOURCE_STRATEGY] = TrainingQuestionData(
            question="What's your approach to finding resources?",
            options=[
                QuestionOption(
                    text="Gather large amounts",
                    trait_bonus="STR",
                    description="Strength and carrying capacity"
                ),
                QuestionOption(
                    text="Find the best quality sources",
                    trait_bonus="PER",
                    description="Awareness and detection"
                ),
                QuestionOption(
                    text="Collect efficiently and quickly",
                    trait_bonus="AGI",
                    description="Speed and efficiency"
                ),
                QuestionOption(
                    text="Plan and strategize",
                    trait_bonus="INT",
                    description="Intelligence and foresight"
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
        """Create an animal with custom training choices applied.
        
        Creates a base animal and applies trait bonuses based on training question answers.
        Each training choice corresponds to one of the 5 training questions.
        
        Args:
            animal_id: Unique identifier for the animal
            category: Animal category (Herbivore, Carnivore, Omnivore)
            training_choices: List of 5 integers (0-3) representing question answers
            
        Returns:
            Animal with training bonuses applied
            
        Raises:
            ValueError: If training_choices length doesn't match number of questions
        """
        if len(training_choices) != len(TrainingQuestion):
            raise ValueError(f"Expected {len(TrainingQuestion)} training choices, got {len(training_choices)}")
        
        # Create base animal
        animal = create_random_animal(animal_id, category)
        
        # Apply training bonuses
        trait_bonuses = self._calculate_training_bonuses(training_choices)
        self._apply_trait_bonuses(animal, trait_bonuses)
        
        return animal
    
    def _calculate_training_bonuses(self, training_choices: List[int]) -> Dict[str, int]:
        """Calculate trait bonuses from training choices.
        
        Maps each training choice to its corresponding trait bonus and sums them up.
        
        Args:
            training_choices: List of integers (0-3) representing question answers
            
        Returns:
            Dictionary mapping trait names to their total bonus values
        """
        bonuses = {trait: 0 for trait in constants.TRAIT_NAMES}
        
        for i, choice in enumerate(training_choices):
            question_type = list(TrainingQuestion)[i]
            question_data = self.training_questions[question_type]
            
            if 0 <= choice < len(question_data.options):
                trait = question_data.options[choice].trait_bonus
                bonuses[trait] += 1
        
        return bonuses
    
    def _apply_trait_bonuses(self, animal: Animal, bonuses: Dict[str, int]) -> None:
        """Apply trait bonuses to an animal and recalculate derived stats.
        
        Adds trait bonuses to the animal's traits, ensuring they don't exceed maximum values.
        Recalculates health and energy based on the new endurance value.
        
        Args:
            animal: Animal to apply bonuses to
            bonuses: Dictionary mapping trait names to bonus values
        """
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
        """Create an animal with completely custom trait values.
        
        Allows for precise control over all animal traits, useful for testing
        specific trait combinations or creating animals with exact specifications.
        
        Args:
            animal_id: Unique identifier for the animal
            category: Animal category (Herbivore, Carnivore, Omnivore)
            custom_traits: Dictionary mapping trait names to their desired values
            
        Returns:
            Animal with the specified custom traits
            
        Raises:
            ValueError: If custom_traits are invalid or incomplete
        """
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
        """Validate custom trait values for correctness and completeness.
        
        Ensures all required traits are present, have valid names, and are within
        acceptable value ranges.
        
        Args:
            traits: Dictionary of trait names to values to validate
            
        Raises:
            ValueError: If traits are invalid, missing, or out of range
        """
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
        """Create a population of animals with individual training choices.
        
        Creates multiple animals with different training configurations, cycling
        through animal categories to ensure diversity.
        
        Args:
            population_size: Number of animals to create
            training_choices: List of training choice lists, one per animal
            
        Returns:
            List of trained animals
            
        Raises:
            ValueError: If training_choices length doesn't match population_size
        """
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
        """Create a diverse population with varied traits.
        
        Generates a population with random trait variations to increase genetic
        diversity. Each animal has a chance to receive trait modifications.
        
        Args:
            population_size: Number of animals to create
            diversity_factor: Probability (0.0-1.0) that each animal gets trait variation
            
        Returns:
            List of diverse animals with varied traits
        """
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
        """Add random variation to an animal's traits.
        
        Randomly boosts one trait and reduces another to create trait diversity.
        Ensures traits stay within valid ranges and recalculates derived stats.
        
        Args:
            animal: Animal to add trait variation to
        """
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
        """Get the training questions for display or interactive use.
        
        Returns the complete set of training questions that can be used
        for user interfaces or programmatic animal creation.
        
        Returns:
            Dictionary mapping question types to their data and options
        """
        return self.training_questions
    
    def analyze_animal_traits(self, animal: Animal) -> Dict[str, any]:
        """Analyze an animal's trait distribution and characteristics.
        
        Provides comprehensive analysis of an animal's trait distribution,
        specialization level, and effective stats for evaluation purposes.
        
        Args:
            animal: Animal to analyze
            
        Returns:
            Dictionary containing trait analysis data including:
            - total_traits: Sum of all trait values
            - primary_trait: Highest trait name
            - primary_value: Value of highest trait
            - trait_balance: Difference between highest and lowest traits
            - specialization: Specialization level (High/Medium/Low)
            - effective_traits: Effective trait values after modifiers
            - max_health: Maximum health value
            - max_energy: Maximum energy value
        """
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
        """Initialize the animal customizer with optional seed for reproducible results.
        
        Args:
            seed: Optional random seed for reproducible animal generation
        """
        self.random = random.Random(seed)
    
    def optimize_animal_for_category(self, animal: Animal) -> Animal:
        """Optimize an animal's traits for its category's primary focus.
        
        Maximizes the animal's primary trait for its category and ensures all
        other traits are within standard ranges for optimal performance.
        
        Args:
            animal: Animal to optimize
            
        Returns:
            Optimized animal with traits adjusted for its category
        """
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
        """Create an animal with balanced traits across all categories.
        
        Creates an animal with the primary trait maximized and remaining points
        distributed evenly among other traits for a balanced build.
        
        Args:
            animal_id: Unique identifier for the animal
            category: Animal category (Herbivore, Carnivore, Omnivore)
            target_total: Total trait points to distribute (default: 30)
            
        Returns:
            Animal with balanced trait distribution
        """
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
        """Create an animal specialized in a specific trait.
        
        Creates an animal with one trait maximized and remaining points distributed
        among other traits. Useful for testing extreme trait combinations.
        
        Args:
            animal_id: Unique identifier for the animal
            category: Animal category (Herbivore, Carnivore, Omnivore)
            specialization_trait: Trait to specialize in (STR, AGI, INT, END, PER)
            specialization_level: Level of specialization (1-10, default: 9)
            
        Returns:
            Animal specialized in the specified trait
            
        Raises:
            ValueError: If specialization_trait is invalid or specialization_level is out of range
        """
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
    """Interactive function to create an animal with training questions.
    
    Creates an animal using random training choices and returns both the animal
    and the list of questions. In a real implementation, this would be interactive.
    
    Args:
        animal_id: Unique identifier for the animal
        category: Animal category (Herbivore, Carnivore, Omnivore)
        
    Returns:
        Tuple containing:
        - Animal: Created animal with training applied
        - List[TrainingQuestionData]: List of training questions for display
    """
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
