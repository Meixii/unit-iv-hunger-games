# Implementation Guide

## Technical Architecture Overview

### System Components

The evolutionary simulation system consists of several interconnected components:

1. **Neural Network Engine** - Core MLP implementation
2. **Animal System** - Individual animal behavior and decision-making
3. **Environment System** - Grid world and resource management
4. **Evolution Engine** - Genetic algorithms and population management
5. **Simulation Controller** - Main simulation loop and coordination
6. **User Interface** - Interactive controls and visualization
7. **Data Analysis** - Statistics collection and visualization

## Core Implementation Details

### 1. Neural Network Implementation

#### MLP Architecture
```python
class NeuralNetwork:
    def __init__(self, input_size=2, hidden_size=4, output_size=4):
        # Network structure: 2 inputs → 4 hidden → 4 outputs
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        # Weight matrices
        self.weights_input_hidden = np.random.randn(input_size, hidden_size)
        self.weights_hidden_output = np.random.randn(hidden_size, output_size)
        
        # Bias vectors
        self.bias_hidden = np.zeros(hidden_size)
        self.bias_output = np.zeros(output_size)
```

#### Key Methods
- `forward_propagation(inputs)` - Process inputs through network
- `get_decision(inputs)` - Return action decision based on outputs
- `mutate(mutation_rate)` - Apply random mutations to weights
- `crossover(other_network)` - Create offspring with genetic crossover
- `copy()` - Create identical copy of network

### 2. Animal System

#### Animal Class Structure
```python
class Animal:
    def __init__(self, x, y, neural_network):
        self.position = (x, y)
        self.neural_network = neural_network
        self.hunger = 100.0
        self.thirst = 100.0
        self.energy = 100.0
        self.age = 0
        self.fitness = 0.0
        self.alive = True
```

#### Decision Making Process
1. **Input Processing**: Normalize hunger and thirst values (0-1)
2. **Neural Network Forward Pass**: Process inputs through MLP
3. **Action Selection**: Choose action with highest output value
4. **Action Execution**: Perform selected action and update state

#### Action Types
- **Move**: Change position (costs energy, may find resources)
- **Eat**: Consume food if available (reduces hunger)
- **Drink**: Consume water if available (reduces thirst)
- **Rest**: Recover energy (reduces hunger/thirst slowly)

### 3. Environment System

#### Grid World Implementation
```python
class GridWorld:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)
        self.food_positions = []
        self.water_positions = []
        self.animals = []
```

#### Resource Management
- **Food Placement**: Random distribution with configurable density
- **Water Placement**: Separate water sources with configurable density
- **Resource Consumption**: Animals consume resources when performing eat/drink actions
- **Resource Regeneration**: Optional resource respawning system

#### Environmental Events
- **Drought**: Reduces water availability by 50-80%
- **Storm**: Reduces movement efficiency and increases energy consumption
- **Event Duration**: Configurable event length and impact

### 4. Evolutionary Algorithm

#### Population Management
```python
class Population:
    def __init__(self, size=50):
        self.animals = []
        self.generation = 0
        self.fitness_history = []
        self.survival_rate = 0.0
```

#### Selection Methods
1. **Fitness-Based Selection**: Select parents based on survival fitness
2. **Tournament Selection**: Random tournaments with fitness comparison
3. **Roulette Wheel Selection**: Probability-based selection

#### Genetic Operations
- **Mutation**: Random weight changes with configurable rate
- **Crossover**: Weight averaging between parent networks
- **Elitism**: Preserve best individuals across generations

#### Fitness Calculation
```python
def calculate_fitness(animal):
    # Base fitness from survival time
    survival_bonus = animal.age * 10
    
    # Resource consumption efficiency
    resource_efficiency = (animal.hunger + animal.thirst) / 200
    
    # Energy management
    energy_bonus = animal.energy / 100
    
    return survival_bonus + resource_efficiency + energy_bonus
```

### 5. Simulation Controller

#### Main Simulation Loop
```python
class Simulation:
    def run_simulation(self, generations=5, steps_per_generation=1000):
        for generation in range(generations):
            # Run simulation steps
            for step in range(steps_per_generation):
                self.update_environment()
                self.update_animals()
                self.check_events()
            
            # Evolution phase
            self.evolve_population()
            self.reset_environment()
```

#### State Management
- **Simulation State**: Running, paused, stopped
- **Generation Tracking**: Current generation and progress
- **Statistics Collection**: Real-time data gathering
- **Event Scheduling**: Dynamic event management

### 6. User Interface Implementation

#### Configuration System
```python
class SimulationConfig:
    def __init__(self):
        self.population_size = 50
        self.grid_size = (20, 20)
        self.food_density = 0.1
        self.water_density = 0.1
        self.mutation_rate = 0.1
        self.generations = 5
        self.steps_per_generation = 1000
```

#### Visualization Components
- **Grid Display**: Real-time grid visualization
- **Animal Tracking**: Position and state visualization
- **Resource Display**: Food and water location indicators
- **Statistics Panel**: Live data display
- **Control Panel**: Simulation controls and parameter adjustment

### 7. Data Analysis System

#### Statistics Collection
```python
class StatisticsCollector:
    def __init__(self):
        self.generation_data = []
        self.survival_rates = []
        self.fitness_scores = []
        self.resource_consumption = []
        self.behavioral_patterns = []
```

#### Key Metrics
- **Survival Rate**: Percentage of animals surviving each generation
- **Average Fitness**: Mean fitness score per generation
- **Resource Efficiency**: Resource consumption patterns
- **Behavioral Analysis**: Action selection patterns
- **Evolution Progress**: Fitness improvement over generations

## File Structure

```
evosim/
├── src/
│   ├── neural_network.py      # MLP implementation
│   ├── animal.py             # Animal class and behavior
│   ├── environment.py        # Grid world and resources
│   ├── evolution.py          # Genetic algorithms
│   ├── simulation.py         # Main simulation controller
│   ├── events.py             # Environmental events
│   └── utils.py              # Utility functions
├── ui/
│   ├── gui.py                # Main user interface
│   ├── visualization.py      # Grid and data visualization
│   └── controls.py           # Control panel
├── analysis/
│   ├── statistics.py         # Data collection
│   ├── visualization.py      # Charts and graphs
│   └── export.py             # Data export
├── tests/
│   ├── test_neural_network.py
│   ├── test_animal.py
│   ├── test_environment.py
│   └── test_evolution.py
├── config/
│   ├── default_config.json   # Default parameters
│   └── event_config.json     # Event definitions
└── docs/
    ├── README.md
    ├── tasks.md
    ├── implementation.md
    └── design.md
```

## Dependencies

### Core Dependencies
- **numpy**: Numerical computations and array operations
- **matplotlib**: Data visualization and charting
- **tkinter**: GUI framework (built-in with Python)
- **json**: Configuration file handling
- **random**: Random number generation
- **math**: Mathematical operations

### Optional Dependencies
- **pandas**: Advanced data analysis
- **seaborn**: Enhanced visualization
- **pygame**: Alternative GUI framework
- **scipy**: Scientific computing

## Configuration System

### Default Parameters
```json
{
    "simulation": {
        "generations": 5,
        "steps_per_generation": 1000,
        "population_size": 50
    },
    "environment": {
        "grid_width": 20,
        "grid_height": 20,
        "food_density": 0.1,
        "water_density": 0.1
    },
    "neural_network": {
        "input_size": 2,
        "hidden_size": 4,
        "output_size": 4,
        "mutation_rate": 0.1
    },
    "animals": {
        "initial_hunger": 100,
        "initial_thirst": 100,
        "initial_energy": 100,
        "hunger_decay": 0.1,
        "thirst_decay": 0.1,
        "energy_decay": 0.05
    }
}
```

## Performance Considerations

### Optimization Strategies
1. **Vectorized Operations**: Use NumPy for efficient array operations
2. **Batch Processing**: Process multiple animals simultaneously
3. **Memory Management**: Efficient data structures and garbage collection
4. **Caching**: Cache frequently computed values
5. **Parallel Processing**: Multi-threading for independent operations

### Scalability Limits
- **Population Size**: Recommended max 200 animals
- **Grid Size**: Recommended max 50x50
- **Generations**: Recommended max 20 generations
- **Simulation Steps**: Recommended max 5000 per generation

## Error Handling

### Common Error Scenarios
1. **Invalid Parameters**: Configuration validation
2. **Resource Exhaustion**: Memory and CPU limits
3. **Simulation Errors**: Invalid states and transitions
4. **File I/O Errors**: Configuration and data file handling
5. **User Input Errors**: Invalid user inputs

### Error Recovery
- **Graceful Degradation**: Continue simulation with reduced functionality
- **State Recovery**: Restore from last valid state
- **User Notification**: Clear error messages and suggestions
- **Logging**: Comprehensive error logging for debugging

## Testing Strategy

### Unit Testing
- **Neural Network**: Test forward propagation and mutation
- **Animal Behavior**: Test decision-making and state updates
- **Environment**: Test resource management and events
- **Evolution**: Test selection and genetic operations

### Integration Testing
- **Simulation Flow**: Test complete simulation runs
- **User Interface**: Test GUI interactions and controls
- **Data Collection**: Test statistics and visualization
- **Configuration**: Test parameter loading and validation

### Performance Testing
- **Load Testing**: Test with maximum recommended parameters
- **Memory Testing**: Monitor memory usage and leaks
- **Speed Testing**: Measure simulation performance
- **Stress Testing**: Test with extreme parameter values
