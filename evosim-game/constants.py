"""
EvoSim Game Constants

This module centralizes all numeric and categorical constants for the EvoSim simulation.
All magic numbers and configuration values are defined here for easy tuning and reference.

Reference: Section IX - Code Implementation Constants from documentation.md
"""

# =============================================================================
# WORLD GENERATION PARAMETERS
# =============================================================================

# Grid dimensions
GRID_WIDTH = 25
GRID_HEIGHT = 25

# Terrain distribution percentages
TERRAIN_DISTRIBUTION = {
    'Plains': 0.60,
    'Forest': 0.25,
    'Water': 0.10,
    'Mountains': 0.05
}

# Resource spawn probabilities
FOOD_SPAWN_CHANCE = 0.15
WATER_SPAWN_CHANCE = 0.05

# Terrain movement cost multipliers
TERRAIN_MOVEMENT_MODIFIERS = {
    'Plains': 1.0,
    'Forest': 1.5,
    'Jungle': 2.0,
    'Swamp': 1.8
}

# Swamp-specific effects
SWAMP_SICKNESS_CHANCE = 0.10

# =============================================================================
# ANIMAL PARAMETERS
# =============================================================================

# Trait value ranges
STANDARD_TRAIT_MIN = 4
STANDARD_TRAIT_MAX = 6
PRIMARY_TRAIT_MIN = 7
PRIMARY_TRAIT_MAX = 9

# Base health and energy calculations
BASE_HEALTH = 100
HEALTH_PER_ENDURANCE = 10
BASE_ENERGY = 100
ENERGY_PER_ENDURANCE = 5

# Initial training points for player customization
INITIAL_TRAINING_POINTS = 5

# =============================================================================
# STATUS DYNAMICS
# =============================================================================

# Depletion rates per movement event
HUNGER_DEPLETION_RATE = 5
THIRST_DEPLETION_RATE = 8

# Energy regeneration
PASSIVE_ENERGY_REGEN = 10

# Damage from starvation and dehydration
STARVATION_DAMAGE = 5
DEHYDRATION_DAMAGE = 10

# =============================================================================
# ACTION COSTS & GAINS
# =============================================================================

# Movement energy costs
MOVEMENT_BASE_COST = 10
MOVEMENT_AGILITY_MULTIPLIER = 0.5

# Rest action
REST_ENERGY_GAIN = 40

# Food consumption gains
PLANT_FOOD_GAIN = 40
PREY_FOOD_GAIN = 50

# Water consumption
DRINKING_THIRST_GAIN = 40

# =============================================================================
# COMBAT MECHANICS
# =============================================================================

# Combat damage calculations
STRENGTH_DAMAGE_MULTIPLIER = 2
AGILITY_EVASION_MULTIPLIER = 5

# =============================================================================
# PASSIVES & EFFECTS
# =============================================================================

# Passive ability multipliers
AMBUSH_PREDATOR_MULTIPLIER = 1.5
EFFICIENT_GRAZER_MULTIPLIER = 1.25
IRON_STOMACH_RESISTANCE_CHANCE = 0.50

# Effect durations (in turns)
DEFAULT_BUFF_DURATION = 3
DEFAULT_DEBUFF_DURATION = 5

# Poison damage per turn
POISON_DAMAGE_PER_TURN = 5

# =============================================================================
# EVENTS & DISASTERS
# =============================================================================

# Resource scarcity event
RESOURCE_SCARCITY_GAIN = 10

# Rockslide event parameters
ROCKSLIDE_ESCAPE_DC = 14
ROCKSLIDE_HIDE_DC = 12
ROCKSLIDE_DAMAGE = 15

# Curious object event
CURIOUS_OBJECT_DC = 13

# Migration event
MIGRATION_ENERGY_BONUS = 15

# Resource bloom event
RESOURCE_BLOOM_MULTIPLIER = 1.5

# Drought event
DROUGHT_WATER_REDUCTION = 0.50

# Disaster damage values
WILDFIRE_DAMAGE = 20
FLOOD_DAMAGE = 15

# Contamination event
CONTAMINATION_SAVE_DC = 10

# Earthquake event
EARTHQUAKE_INJURY_CHANCE = 0.25

# Harsh winter event
WINTER_DEPLETION_MULTIPLIER = 2

# =============================================================================
# FITNESS SCORE WEIGHTS
# =============================================================================

# Weights for fitness score calculation
FITNESS_WEIGHTS = {
    'Time': 1,
    'Resource': 5,
    'Kill': 50,
    'Distance': 0.2,
    'Event': 10
}

# =============================================================================
# ANIMAL CATEGORIES
# =============================================================================

# Available animal categories
ANIMAL_CATEGORIES = ['Herbivore', 'Carnivore', 'Omnivore']

# Primary traits for each category
CATEGORY_PRIMARY_TRAITS = {
    'Herbivore': 'AGI',
    'Carnivore': 'STR',
    'Omnivore': 'END'
}

# =============================================================================
# TRAIT NAMES
# =============================================================================

# Core trait names
TRAIT_NAMES = ['STR', 'AGI', 'INT', 'END', 'PER']

# =============================================================================
# STATUS NAMES
# =============================================================================

# Core status names
STATUS_NAMES = ['Health', 'Hunger', 'Thirst', 'Energy', 'Instinct']

# =============================================================================
# TERRAIN TYPES
# =============================================================================

# Available terrain types
TERRAIN_TYPES = ['Plains', 'Forest', 'Jungle', 'Water', 'Swamp', 'Mountains']

# =============================================================================
# RESOURCE TYPES
# =============================================================================

# Available resource types
RESOURCE_TYPES = ['Plant', 'Prey', 'Water', 'Carcass']

# =============================================================================
# EFFECT NAMES
# =============================================================================

# Buff effects
BUFF_EFFECTS = ['Well-Fed', 'Hydrated', 'Rested', 'Adrenaline Rush']

# Debuff effects
DEBUFF_EFFECTS = ['Injured', 'Poisoned', 'Exhausted', 'Sick']

# =============================================================================
# EVENT TYPES
# =============================================================================

# Triggered events
TRIGGERED_EVENTS = [
    'Animal Encounter',
    'Resource Scarcity',
    'Sudden Threat',
    'Curious Object'
]

# Random events
RANDOM_EVENTS = [
    'Migration',
    'Resource Bloom',
    'Drought',
    'Predator Frenzy',
    'Grazing Season'
]

# Disasters
DISASTERS = [
    'Wildfire',
    'Contamination',
    'Flood',
    'Earthquake',
    'Harsh Winter'
]

# =============================================================================
# SIMULATION PARAMETERS
# =============================================================================

# Maximum simulation weeks per generation
MAX_WEEKS_PER_GENERATION = 50

# Population size
POPULATION_SIZE = 100

# Elite percentage for evolutionary algorithm
ELITE_PERCENTAGE = 0.10

# Tournament size for selection
TOURNAMENT_SIZE = 5

# Mutation rate
MUTATION_RATE = 0.02

# =============================================================================
# MLP ARCHITECTURE
# =============================================================================

# Neural network architecture
INPUT_NODES = 41  # 5 internal + 9 tiles * 4 data points
HIDDEN_LAYER_1_NODES = 16
HIDDEN_LAYER_2_NODES = 12
OUTPUT_NODES = 8  # 8 possible actions

# Activation functions
HIDDEN_ACTIVATION = 'relu'
OUTPUT_ACTIVATION = 'softmax'

# =============================================================================
# ACTION TYPES
# =============================================================================

# Available actions for animals
ACTIONS = [
    'Move North',
    'Move East', 
    'Move South',
    'Move West',
    'Rest',
    'Eat',
    'Drink',
    'Attack'
]

# =============================================================================
# DEBUGGING AND LOGGING
# =============================================================================

# Enable debug mode
DEBUG_MODE = False

# Log level
LOG_LEVEL = 'INFO'

# Save simulation data
SAVE_SIMULATION_DATA = True

# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_constants():
    """
    Validate that all constants are within expected ranges and types.
    This function can be called during initialization to ensure data integrity.
    """
    # Validate terrain distribution sums to 1.0
    terrain_sum = sum(TERRAIN_DISTRIBUTION.values())
    assert abs(terrain_sum - 1.0) < 0.001, f"Terrain distribution must sum to 1.0, got {terrain_sum}"
    
    # Validate trait ranges
    assert STANDARD_TRAIT_MIN < STANDARD_TRAIT_MAX, "Standard trait min must be less than max"
    assert PRIMARY_TRAIT_MIN < PRIMARY_TRAIT_MAX, "Primary trait min must be less than max"
    assert PRIMARY_TRAIT_MIN > STANDARD_TRAIT_MAX, "Primary traits should be higher than standard traits"
    
    # Validate fitness weights are positive
    for weight_name, weight_value in FITNESS_WEIGHTS.items():
        assert weight_value > 0, f"Fitness weight {weight_name} must be positive, got {weight_value}"
    
    # Validate probabilities are between 0 and 1
    assert 0 <= FOOD_SPAWN_CHANCE <= 1, f"Food spawn chance must be between 0 and 1, got {FOOD_SPAWN_CHANCE}"
    assert 0 <= WATER_SPAWN_CHANCE <= 1, f"Water spawn chance must be between 0 and 1, got {WATER_SPAWN_CHANCE}"
    assert 0 <= SWAMP_SICKNESS_CHANCE <= 1, f"Swamp sickness chance must be between 0 and 1, got {SWAMP_SICKNESS_CHANCE}"
    
    print("✅ All constants validation passed!")

if __name__ == "__main__":
    # Run validation when script is executed directly
    validate_constants()
