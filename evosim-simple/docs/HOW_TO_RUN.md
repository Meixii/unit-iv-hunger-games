# How to Run the Evolutionary Simulation GUI

This guide will walk you through setting up and running the evolutionary simulation with the graphical user interface.

## Prerequisites

- Python 3.8 or higher
- Git (for cloning the repository)

## Step 1: Clone the Repository

```bash
git clone <repository-url>
cd evosim
```

## Step 2: Create and Activate Virtual Environment

### On Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

### On macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt
```

## Step 4: Run the GUI

### Method 1: Using the provided script
```bash
python run_gui.py
```

### Method 2: Direct execution
```bash
python -m ui.gui
```

### Method 3: Using the main module
```bash
python -m src.main
```

## Step 5: Using the GUI

### Initial Setup:
1. **Configure Parameters**: Use the Configuration panel to set:
   - Grid Size: 20x20 (recommended)
   - Population Size: 20-50 animals
   - Max Generations: 5-10
   - Steps per Generation: 50-100
   - Food/Water Density: 0.1-0.2 (10-20%)

2. **Event Settings**: Adjust event probabilities:
   - Drought Probability: 0.01 (1%)
   - Storm Probability: 0.01 (1%)
   - Famine Probability: 0.01 (1%)
   - Bonus Probability: 0.01 (1%)

3. **Evolution Settings**:
   - Mutation Rate: 0.05 (5%)
   - Crossover Rate: 0.7 (70%)
   - Selection Method: Tournament

### Running the Simulation:
1. Click **"Initialize"** to set up the environment
2. Click **"Start"** to begin the simulation
3. Use **"Pause"** and **"Resume"** to control execution
4. Click **"Stop"** to end the simulation

### Monitoring Progress:
- **Simulation Visualization**: Watch animals move on the grid
- **Animal Statistics**: Track individual animal behavior and learning
- **Statistics Panel**: Monitor overall simulation metrics
- **Export Data**: Save results for analysis

## Step 6: Understanding the Results

### Learning Indicators:
- **L:X.XX**: Adaptation score showing how well animals are learning
- **Actions**: M (Move), E (Eat), D (Drink), R (Rest) counts
- **Resources**: F (Food), W (Water) consumed
- **Health**: H (Hunger), T (Thirst), E (Energy), HP (Health Points)

### Educational Value:
- Watch how animals adapt to environmental challenges
- Observe evolutionary pressure through survival rates
- See neural networks learning optimal strategies
- Track fitness improvement over generations

## Troubleshooting

### Common Issues:

1. **Import Errors**:
   ```bash
   # Make sure you're in the project directory
   cd evosim
   
   # Ensure virtual environment is activated
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

2. **Missing Dependencies**:
   ```bash
   # Reinstall requirements
   pip install -r requirements.txt
   ```

3. **GUI Not Starting**:
   ```bash
   # Check Python version
   python --version
   
   # Try alternative execution
   python -c "import tkinter; print('Tkinter available')"
   ```

4. **Performance Issues**:
   - Reduce population size
   - Decrease steps per generation
   - Lower simulation speed

### System Requirements:
- **RAM**: 4GB minimum, 8GB recommended
- **CPU**: Multi-core processor recommended
- **Display**: 1024x768 minimum resolution

## Advanced Usage

### Custom Configurations:
1. Modify parameters in the GUI
2. Click **"Save Config"** to save settings
3. Click **"Load Config"** to restore settings

### Data Export:
- **Export Data**: Save simulation data as JSON
- **Export Report**: Generate text summary
- **View Charts**: Visualize fitness trends

### Batch Runs:
```bash
# Run multiple simulations programmatically
python -c "
from src.simulation import Simulation
from src.config import Config

config = Config()
sim = Simulation(config)
sim.run()
"
```

## Educational Features

### For Students:
1. **Observe Learning**: Watch animals develop survival strategies
2. **Track Evolution**: See how populations improve over generations
3. **Analyze Behavior**: Study decision-making patterns
4. **Compare Strategies**: Different animals may develop different approaches

### For Instructors:
1. **Demonstrate Concepts**: Show evolutionary algorithms in action
2. **Adjust Parameters**: Modify difficulty and learning speed
3. **Export Data**: Use results for analysis and discussion
4. **Visual Learning**: Students can see AI learning process