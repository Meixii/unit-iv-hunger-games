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

### Phase 2: Simulation Engine & Event Handling

#### ✅ Task 2.1: Main Simulation Controller
- **Status:** COMPLETED
- **File:** `simulation_controller.py`
- **Description:** Implemented main simulation controller that orchestrates the entire simulation

#### ✅ Task 2.2: Game Loop Implementation
- **Status:** COMPLETED
- **File:** `simulation_controller.py`
- **Description:** Implemented week-based generational simulation with event scheduling and win/loss detection
- **Features:** Generation execution, weekly cycles, event ordering, win/loss detection, comprehensive logging
- **Tests:** `test/test_game_loop.py` - 19 comprehensive tests covering all game loop functionality
- **Demo:** `demo/demo_game_loop.py` - Interactive demonstration of game loop features
- **Coverage:** All requirements from Section IV.A (Simulation Flow) of documentation.md

#### ✅ Task 2.3: Action Resolution System
- **Status:** COMPLETED
- **File:** `action_resolution/` (modular implementation)
- **Description:** Implemented 4-phase action resolution system with conflict handling and priority-based execution
- **Features:**
  - Decision Phase: Collect actions from all animals using simple rule-based logic
  - Status & Environmental Phase: Apply passive changes (hunger, thirst, health loss from debuffs)
  - Action Execution Phase: Execute actions by priority (stationary first, then movement)
  - Cleanup Phase: Apply new effects and remove expired ones
  - Conflict Resolution: Agility-based movement conflict resolution
  - Animal Encounters: Basic combat mechanics when animals move into occupied tiles
  - Resource Consumption: Animals can eat and drink from available resources
- **Architecture:** Modular design with separate engines for each phase
- **Tests:** `test/test_action_resolution.py`
- **Demo:** `demo/demo_action_resolution.py`

#### ✅ Task 2.4: Event & Disaster Engine
- **Status:** COMPLETED
- **File:** `event_engine/` (modular implementation)
- **Description:** Comprehensive event system providing dynamic gameplay elements
- **Features:**
  - Triggered Events: Condition-based events (overpopulation, resource scarcity, disease outbreaks, extinction threats)
  - Random Events: Probability-based events (resource discovery, healing springs, weather changes, predator migration)
  - Disaster Events: Large-scale area-effect events (earthquakes, wildfires, floods, volcanic eruptions, blizzards, meteors, tsunamis)
  - Event Scheduling: Coordinated event timing and frequency management
  - Event Configuration: Flexible system for adjusting probabilities and enabling/disabling event types
  - Comprehensive Tracking: Detailed event statistics and logging
  - Modular Architecture: Easy to extend with new event types
- **Architecture:** Modular design with separate engines for each event type
- **Tests:** Integrated with game loop tests
- **Demo:** `demo/demo_event_engine.py`

## Project Structure

```
evosim-game/
├── README.md                    # This file
├── constants.py                 # All game constants and parameters
├── data_structures.py           # Core data classes and structures
├── world_generator.py           # World generation logic and utilities
├── animal_creator.py            # Animal creation and customization system
├── simulation_controller.py     # Main simulation controller and orchestration
├── action_resolution/           # Modular action resolution system
│   ├── __init__.py             # Package initialization
│   ├── action_data.py          # Action data structures and enums
│   ├── action_resolver.py      # Main action resolution orchestrator
│   ├── decision_engine.py      # Phase 1: Decision collection
│   ├── status_engine.py        # Phase 2: Status & environmental effects
│   ├── execution_engine.py     # Phase 3: Action execution with conflicts
│   └── cleanup_engine.py       # Phase 4: Effect management
├── event_engine/                # Modular event & disaster system
│   ├── __init__.py             # Package initialization
│   ├── event_data.py           # Event data structures and base classes
│   ├── event_engine.py         # Main event engine interface
│   ├── event_scheduler.py      # Event scheduling and coordination
│   ├── triggered_events.py     # Condition-based events
│   ├── random_events.py        # Probability-based events
│   └── disaster_events.py      # Large-scale disaster events
├── demo/                        # Demonstration scripts
│   ├── demo_mountain_borders.py # Mountain border feature demonstration
│   ├── demo_phase1_complete.py  # Complete Phase 1 demonstration
│   ├── demo_interactive.py      # Interactive hands-on demo
│   ├── demo_simulation_controller.py # Simulation controller demonstration
│   ├── demo_game_loop.py        # Game loop implementation demonstration
│   ├── demo_action_resolution.py # Action resolution system demonstration
│   └── demo_event_engine.py     # Event & disaster engine demonstration
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
    ├── test_simulation_controller.py # Test script for simulation controller validation
    ├── test_game_loop.py        # Test script for game loop functionality validation
    ├── test_action_resolution.py # Test script for action resolution system validation
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

## Simulation Controller Features

The `simulation_controller.py` file includes:

### Core Controller System
- **SimulationController**: Main class for orchestrating the entire simulation
- **SimulationConfig**: Configurable parameters for simulation behavior
- **State Management**: Complete simulation state tracking and validation

### World and Population Management
- **World Initialization**: Generate and validate simulation worlds
- **Population Initialization**: Create and place animals in the world
- **Location Management**: Ensure proper animal placement and tile occupancy
- **Statistics Tracking**: Monitor terrain and category distributions

### Simulation Control
- **Start/Stop/Pause/Resume**: Complete simulation lifecycle management
- **State Validation**: Comprehensive simulation state validation
- **Error Handling**: Robust error handling and recovery
- **Status Monitoring**: Real-time simulation status and statistics

### Logging and Debugging
- **Configurable Logging**: Adjustable log levels and output
- **State Logging**: Detailed simulation state information
- **Performance Tracking**: Simulation timing and duration tracking
- **Debug Information**: Comprehensive debugging capabilities

### Configuration and Customization
- **Flexible Configuration**: Customizable simulation parameters
- **Random Seed Support**: Reproducible simulation results
- **World Configuration**: Integration with world generation settings
- **Population Customization**: Configurable population sizes and distributions

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

## Demo Applications

The project includes comprehensive demonstration applications:

### Complete Phase 1 Demo
- **`demo/demo_phase1_complete.py`** - Comprehensive showcase of all Phase 1 components
- **Features**: Constants, data structures, world generation, animal creation, testing
- **Usage**: `python demo/demo_phase1_complete.py`
- **Output**: Full demonstration with visualizations and performance metrics

### Interactive Demo
- **`demo/demo_interactive.py`** - Hands-on interactive exploration
- **Features**: Custom world creation, animal customization, training system testing
- **Usage**: `python demo/demo_interactive.py`
- **Output**: Menu-driven interface for exploring all features

### Mountain Borders Demo
- **`demo/demo_mountain_borders.py`** - Specific feature demonstration
- **Features**: Mountain border generation and effects
- **Usage**: `python demo/demo_mountain_borders.py`
- **Output**: Visual comparison of worlds with and without borders

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

### Basic Simulation Controller Usage

```python
from simulation_controller import create_simulation_controller

# Create a simulation controller
controller = create_simulation_controller(
    max_weeks=20,
    max_generations=10,
    population_size=20,
    random_seed=42,
    enable_logging=True
)

# Initialize world and population
world = controller.initialize_world()
animals = controller.initialize_population()

# Start simulation
controller.start_simulation()

# Monitor status
status = controller.get_simulation_status()
print(f"Living animals: {status['living_animals']}")

# Stop simulation
controller.stop_simulation()
```

### Advanced Configuration

```python
from simulation_controller import SimulationController, SimulationConfig
from world_generator import GenerationConfig

# Create custom configuration
config = SimulationConfig(
    max_weeks=50,
    max_generations=5,
    population_size=100,
    enable_logging=True,
    log_level="DEBUG",
    random_seed=123
)

# Create controller with custom config
controller = SimulationController(config)

# Initialize with custom world settings
world_config = GenerationConfig(width=30, height=30, enable_mountain_borders=True)
world = controller.initialize_world(world_config)

# Initialize population
animals = controller.initialize_population(50)

# Validate simulation state
if controller.validate_simulation_state():
    controller.start_simulation()
    print("Simulation started successfully!")
else:
    print("Simulation state validation failed!")
```

### Constants Usage

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
