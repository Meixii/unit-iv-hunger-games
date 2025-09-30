# EvoSim: Evolve or Perish

**AI-Driven Animal Survival in a Neural Network Battle Royale**

A computational science project implementing an evolutionary simulation where AI-controlled animals compete for survival in a dynamic world, using neural networks and genetic algorithms to drive evolution.

## 🎯 Project Overview

EvoSim is a sophisticated simulation system that combines artificial intelligence, evolutionary algorithms, and game mechanics to create a "Hunger Games" style survival scenario. Animals controlled by Multi-Layer Perceptrons (MLPs) compete for resources, adapt to environmental challenges, and evolve over generations to become more successful survivors.

### Key Features

- **🧠 Neural Network AI**: Each animal is controlled by a trained MLP that makes survival decisions
- **🧬 Evolutionary Algorithm**: Genetic algorithms drive population evolution across generations
- **🌍 Dynamic World**: Procedurally generated worlds with terrain, resources, and environmental challenges
- **⚔️ Survival Mechanics**: Combat, resource management, and environmental adaptation
- **📊 Data Analysis**: Comprehensive tracking and analysis of evolutionary progress
- **🎮 Interactive Demos**: Hands-on exploration of the simulation system

## 📁 Project Structure

```
unit-iv-hunger-games/
├── README.md                    # This file
├── documentation.md             # Complete project documentation
├── proposal.md                  # Academic research proposal
├── evosim-docs/                 # Interactive web documentation
│   ├── src/                     # Next.js documentation website
│   └── README.md                # Documentation site details
└── evosim-game/                 # Core simulation implementation
    ├── README.md                # Implementation details
    ├── constants.py             # Game constants and parameters
    ├── data_structures.py       # Core data classes
    ├── world_generator.py       # World generation system
    ├── animal_creator.py        # Animal creation and customization
    ├── demo/                    # Demonstration applications
    ├── example/                 # Usage examples
    └── test/                    # Comprehensive test suite
```

## 🧬 Core Concepts

### Neural Network AI
Each animal is controlled by a Multi-Layer Perceptron (MLP) with:
- **41 Input Nodes**: Internal status + 3x3 sensory grid
- **2 Hidden Layers**: 16 and 12 neurons with ReLU activation
- **8 Output Actions**: Movement, rest, eat, drink, attack

### Evolutionary Algorithm
The system uses genetic algorithms to evolve populations:
- **Selection**: Tournament selection with elitism
- **Crossover**: Single-point crossover of MLP weights
- **Mutation**: Gaussian noise applied to weights
- **Fitness**: Multi-component fitness function

### World Generation
Dynamic worlds with:
- **Terrain Types**: Plains, Forest, Jungle, Water, Swamp, Mountains
- **Resources**: Plants, Prey, Water, Carcasses
- **Environmental Effects**: Movement costs, resource spawn rates
- **Mountain Borders**: Configurable containment barriers

### Animal Categories
Three distinct animal types with unique traits:
- **Herbivores**: Agility-focused, efficient grazers
- **Carnivores**: Strength-focused, ambush predators
- **Omnivores**: Endurance-focused, adaptable survivors

## 📊 Current Status

### ✅ Phase 1: Foundational Classes & Core Mechanics (COMPLETED)
- **Constants & Configuration**: All game parameters centralized
- **Data Structures**: Complete class hierarchy for all game entities
- **World Generation**: Procedural terrain and resource placement
- **Animal Creation**: Training system and trait customization
- **Testing Suite**: 100% test coverage with edge case validation

### 🔄 Phase 2: Simulation Engine & Event Handling (COMPLETED)
- **Main Simulation Controller**: Core simulation orchestration
- **Game Loop Implementation**: Week-based generational cycles
- **Action Resolution System**: Turn-based action processing
- **Event & Disaster Engine**: Environmental challenges and events
- **Simulation Engine Testing**: Integration and performance validation

### 📋 Phase 3: Artificial Intelligence & Evolution (COMPLETED)
- **MLP Implementation**: Neural network decision system (implemented)
- **Sensory Input System**: Environmental perception (implemented)
- **Fitness Function**: Evolutionary success measurement (implemented)
- **Evolutionary Algorithm**: Population evolution mechanics (implemented)
- **AI/Evolution Testing**: Multi-generation demos and CSV logging (added)

### 🎨 Phase 4: UI, Visualization & Reports (IN PROGRESS)
- **Training CLI Interface**: Interactive animal customization
- **Simulation Visualization**: Real-time world rendering
- **Generational Reporting**: Evolution progress analysis
- **Documentation**: Complete system documentation

## 📚 Documentation

### Web Documentation
- **Interactive Site**: Modern, responsive documentation website
- **Navigation**: Sidebar with active page highlighting
- **Content**: Complete project documentation with code examples
- **Design**: shadcn/ui inspired layout with dark mode

### Technical Documentation
- **`documentation.md`**: Complete technical specification
- **`proposal.md`**: Academic research proposal
- **Code Comments**: Comprehensive inline documentation
- **README Files**: Detailed implementation guides

## 🔬 Research Context

This project is part of a computational science curriculum exploring:
- **Artificial Intelligence**: Neural network implementation and training
- **Evolutionary Algorithms**: Genetic programming and population dynamics
- **Simulation Science**: Complex system modeling and analysis
- **Game Theory**: Strategic decision-making in competitive environments

## 🛠️ Technology Stack

### Core Implementation
- **Python 3.x**: Primary programming language
- **NumPy**: Numerical computations (planned)
- **Dataclasses**: Modern Python data structures
- **Type Hints**: Static type checking

### Documentation
- **Next.js**: React-based documentation website
- **TypeScript**: Type-safe documentation code
- **Tailwind CSS**: Utility-first styling
- **shadcn/ui**: Modern UI component library

### Testing
- **Custom Test Framework**: Comprehensive testing suite
- **Edge Case Testing**: Boundary condition validation
- **Performance Testing**: Execution time optimization
- **Integration Testing**: Component interaction validation

## 📄 License

This project is part of an academic curriculum and is intended for educational purposes.

## 🎯 Future Enhancements

- **Advanced AI**: More sophisticated neural network architectures
- **Complex Environments**: Multi-biome worlds with seasonal changes
- **Social Dynamics**: Animal interactions and group behaviors
- **Visualization**: Real-time 3D world rendering
- **Data Analysis**: Advanced evolutionary progress tracking