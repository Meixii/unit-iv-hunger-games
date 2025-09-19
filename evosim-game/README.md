# EvoSim Game

**Evolve or Perish: AI-Driven Animal Survival in a Neural Network Battle Royale**

A Python implementation of the EvoSim simulation project, featuring evolutionary algorithms training multi-layer perceptrons for animal survival behavior.

## Project Status

### Phase 1: Foundational Classes & Core Mechanics

#### ✅ Task 1.1: Setup Constants File
- **Status:** COMPLETED
- **File:** `constants.py`
- **Description:** Centralized all numeric and categorical constants for easy tuning and reference
- **Coverage:** All constants from Section IX of documentation.md

#### ✅ Task 1.2: Build Core Data Classes
- **Status:** COMPLETED
- **File:** `data_structures.py`
- **Description:** Implemented data containers for animals, world, resources, tiles, and effects
- **Coverage:** All classes from Section XI of documentation.md

#### ✅ Task 1.3: World & Map Generation
- **Status:** COMPLETED
- **File:** `world_generator.py`
- **Description:** Implemented world generation logic with terrain placement and resource distribution
- **Coverage:** All requirements from Section VI and VIII of documentation.md

#### ✅ Task 1.4: Animal Creation & Customization
- **Status:** COMPLETED
- **File:** `animal_creator.py`
- **Description:** Implemented animal creation and customization system with training questions
- **Coverage:** All requirements from Section V and VII of documentation.md

#### ✅ Task 1.5: Foundational Unit Tests
- **Status:** COMPLETED
- **Files:** `test/test_*.py`, `test/test_runner.py`, `test/test_edge_cases.py`
- **Description:** Comprehensive test suite ensuring 80%+ code coverage and reliability
- **Coverage:** All foundational classes with edge cases, integration, and performance tests

## Project Structure

```
evosim-game/
├── README.md                    # This file
├── constants.py                 # All game constants and parameters
├── data_structures.py           # Core data classes and structures
├── world_generator.py           # World generation logic and utilities
├── animal_creator.py            # Animal creation and customization system
├── demo/                        # Demonstration scripts
│   └── demo_mountain_borders.py # Mountain border feature demonstration
├── example/                     # Example usage scripts
│   ├── example_usage.py         # Constants usage examples
│   ├── example_data_usage.py    # Data structures usage examples
│   ├── example_world_generation.py # World generation usage examples
│   └── example_animal_creation.py # Animal creation usage examples
└── test/                        # Test scripts
    ├── test_constants.py        # Test script for constants validation
    ├── test_data_structures.py  # Test script for data structures validation
    ├── test_world_generator.py  # Test script for world generation validation
    ├── test_animal_creator.py   # Test script for animal creation validation
    ├── test_edge_cases.py       # Edge case and boundary condition tests
    └── test_runner.py           # Comprehensive test runner with coverage analysis
```

## Data Structures Features

The `data_structures.py` file includes:

### Core Classes
- **Effect**: Temporary buffs/debuffs with duration and modifiers
- **Resource**: Consumable items with quantity and uses
- **Tile**: World grid cells with terrain, resources, and occupants
- **World**: 2D grid container with coordinate validation
- **Animal**: Complete animal entity with traits, status, and effects
- **Simulation**: Main controller for the simulation state

### Enums and Types
- **AnimalCategory**: Herbivore, Carnivore, Omnivore
- **TerrainType**: Plains, Forest, Jungle, Water, Swamp, Mountains
- **ResourceType**: Plant, Prey, Water, Carcass
- **EffectType**: All buffs and debuffs
- **ActionType**: All possible animal actions

### Utility Functions
- **create_random_animal()**: Generate animals with proper trait distribution
- **create_effect()**: Create effects with default values
- **create_resource()**: Create resources with default values
- **validate_data_structures()**: Comprehensive validation

## World Generator Features

The `world_generator.py` file includes:

### Core Generation
- **WorldGenerator**: Main class for generating worlds and placing animals
- **GenerationConfig**: Configurable parameters for world generation
- **WorldValidator**: Validation and statistics for generated worlds

### Terrain Generation
- **Weighted Random Distribution**: Terrain types placed according to distribution percentages
- **Mountain Borders**: Optional mountain borders around world edges for containment
- **Deterministic Generation**: Same seed produces identical worlds
- **Terrain Effects**: Movement costs and resource spawn rates based on terrain

### Resource Placement
- **Water Resources**: Clustered around water tiles for realistic distribution
- **Food Resources**: Terrain-based spawn rates (jungles have more food)
- **Resource Types**: Plants, prey, carcasses, and water with appropriate values

### Animal Placement
- **Valid Spawn Locations**: Only on plains tiles without occupants
- **Category Distribution**: Even distribution across animal categories
- **Location Tracking**: Animals know their world coordinates

### Validation & Statistics
- **Terrain Distribution**: Validates against expected percentages
- **Resource Counting**: Tracks all placed resources
- **Spawn Location Counting**: Ensures adequate space for animals
- **Error Reporting**: Detailed validation error messages

## Animal Creator Features

The `animal_creator.py` file includes:

### Core Creation System
- **AnimalCreator**: Main class for creating and customizing animals
- **AnimalCustomizer**: Advanced customization and optimization tools
- **Training System**: 5-question system for trait bonuses

### Training Questions
- **Hunting Style**: Ambush, direct confrontation, patient observation, endurance
- **Survival Priority**: Food finding, predator avoidance, energy conservation, learning
- **Environment Preference**: Plains, forests, mountains, complex terrain
- **Combat Approach**: Strike first, dodge and counter, outsmart, outlast
- **Resource Strategy**: Gather much, find best sources, efficient collection, plan ahead

### Customization Options
- **Custom Traits**: Create animals with specific trait values
- **Training Bonuses**: Apply +1 bonuses based on training choices
- **Population Creation**: Generate groups of animals with varied training
- **Diverse Populations**: Create populations with trait variation
- **Category Optimization**: Optimize animals for their category strengths

### Analysis & Validation
- **Trait Analysis**: Comprehensive analysis of animal trait distribution
- **Specialization Detection**: Identify primary traits and specialization levels
- **Trait Validation**: Ensure all traits are within valid ranges
- **Health/Energy Calculation**: Automatic recalculation based on endurance

## Testing Features

The comprehensive test suite includes:

### Core Test Modules
- **`test_constants.py`** - Validates all constants are defined and accessible
- **`test_data_structures.py`** - Tests all classes instantiate and validate correctly
- **`test_world_generator.py`** - Tests terrain, resources, and animals placed correctly
- **`test_animal_creator.py`** - Tests training, customization, and analysis working

### Advanced Testing
- **`test_edge_cases.py`** - Edge cases, boundary conditions, and error handling
- **`test_runner.py`** - Comprehensive test runner with coverage analysis

### Test Coverage
- **100% Success Rate** - All tests pass consistently
- **80%+ Code Coverage** - Meets requirement for foundational classes
- **Edge Case Testing** - Boundary values, invalid inputs, extreme scenarios
- **Integration Testing** - Complete workflow from world creation to animal placement
- **Performance Testing** - Ensures reasonable execution times
- **Error Recovery** - Graceful handling of invalid inputs and edge cases

### Test Categories
- **Unit Tests** - Individual component testing
- **Integration Tests** - Component interaction testing
- **Edge Case Tests** - Boundary condition testing
- **Performance Tests** - Execution time validation
- **Error Handling Tests** - Invalid input validation

## Constants File Features

The `constants.py` file includes:

### World Generation
- Grid dimensions (25x25)
- Terrain distribution percentages
- Resource spawn probabilities
- Movement cost modifiers

### Animal Parameters
- Trait value ranges (4-6 standard, 7-9 primary)
- Health and energy calculations
- Initial training points

### Game Mechanics
- Status dynamics (hunger, thirst, energy)
- Action costs and gains
- Combat mechanics
- Passive abilities and effects

### Events & Disasters
- Triggered events parameters
- Random events configuration
- Disaster damage values
- Event difficulty checks

### Fitness System
- Fitness score weights
- Evolutionary algorithm parameters
- MLP architecture constants

### Validation
- Built-in validation function
- Type and range checking
- Data integrity verification

## Usage

```python
import constants

# Access world parameters
grid_size = constants.GRID_WIDTH * constants.GRID_HEIGHT

# Access animal parameters
trait_range = (constants.STANDARD_TRAIT_MIN, constants.STANDARD_TRAIT_MAX)

# Access fitness weights
time_weight = constants.FITNESS_WEIGHTS['Time']

# Validate all constants
constants.validate_constants()
```

## Testing

Run the test script to validate constants:

```bash
python test_constants.py
```

## Next Steps

- **Task 1.2:** Build Core Data Classes
- **Task 1.3:** World & Map Generation
- **Task 1.4:** Animal Creation & Customization
- **Task 1.5:** Foundational Unit Tests

## Reference

This implementation follows the detailed specifications in `documentation.md` Section IX: Code Implementation Constants.
