# EvoSim GUI - Quick Start Guide

## 🚀 Getting Started

### Windows Users (Easiest)
1. **Double-click** `run_evosim_gui.bat` in the project root
2. The GUI will launch automatically

### All Platforms
1. **Open terminal/command prompt**
2. **Navigate to project root** (where you see the `evosim-game` folder)
3. **Run**: `python run_evosim_gui.py`

### From GUI Directory
1. **Navigate to the `gui` folder**
2. **Run**: `python run_gui.py`

## 🎮 Using the GUI

### 1. Configure Your Simulation
- **Population Size**: Number of animals (default: 20)
- **Max Generations**: How many generations to run (default: 10)
- **Max Weeks**: Weeks per generation (default: 20)
- **Random Seed**: For reproducible results (optional)

### 2. Start the Simulation
- Click **"Start Simulation"**
- Watch the world grid populate with animals
- Monitor statistics in real-time

### 3. Control the Simulation
- **Pause/Resume**: Temporarily stop and continue
- **Stop**: End the current simulation
- **Reset**: Clear everything and start over

### 4. Explore the World
- **Click tiles** to see detailed information
- **Scroll** to zoom in/out
- **Drag** to pan around the world

## 🗺️ Understanding the Visualization

### Terrain Colors
- 🟢 **Plains** (Light Green) - Basic terrain
- 🌲 **Forest** (Dark Green) - Rich in resources  
- 🌿 **Jungle** (Very Dark Green) - Abundant resources
- 💧 **Water** (Blue) - Water sources
- 🐸 **Swamp** (Gray-Green) - Challenging terrain
- ⛰️ **Mountains** (Gray) - Difficult to traverse

### Animal Colors
- 🟡 **Herbivores** (Gold) - Plant eaters
- 🔴 **Carnivores** (Red) - Meat eaters  
- 🟣 **Omnivores** (Purple) - Mixed diet

## 📊 Monitoring Progress

### Status Panel
- **Generation**: Current generation number
- **Week**: Current week within generation
- **Living Animals**: Number of surviving animals
- **Status**: Simulation state (Ready/Running/Paused/Stopped)

### Statistics Panel
- **Animal counts** by category
- **Average fitness** scores
- **Average health** levels

### Event Log
- **Timestamped messages** about simulation events
- **Error messages** and warnings
- **Status updates**

## ⚙️ Advanced Features

### Configuration Management
- **File → Load Configuration**: Load saved settings
- **File → Save Configuration**: Save current settings
- **File → Export Data**: Export simulation data to CSV

### Menu Options
- **File**: Configuration and data management
- **Simulation**: New simulation and world loading
- **Help**: About and documentation

## 🔧 Troubleshooting

### Common Issues

1. **"Module not found" errors**
   - Make sure you're in the project root directory
   - Check that `evosim-game` folder exists
   - Verify all simulation modules are present

2. **GUI won't start**
   - Ensure Python 3.7+ is installed
   - Check that tkinter is available
   - Try running from the `gui` directory: `python run_gui.py`

3. **Simulation won't start**
   - Check configuration parameters are valid
   - Look at the event log for error messages
   - Try with smaller population size

4. **Visualization issues**
   - Try resizing the window
   - Use scroll bars to navigate
   - Reset the simulation if needed

### Getting Help

1. **Check the Event Log** for error messages
2. **Verify Dependencies** are properly installed
3. **Check File Paths** are correct
4. **Review Configuration** parameters

## 📁 File Structure

```
project-root/
├── evosim-game/           # Simulation engine
├── gui/                    # GUI application
│   ├── main_gui.py        # Main GUI code
│   ├── run_gui.py         # GUI launcher
│   ├── test_gui.py        # Test suite
│   └── README.md          # Detailed documentation
├── run_evosim_gui.py      # Project root launcher
└── run_evosim_gui.bat     # Windows batch file
```

## 🎯 Tips for Best Experience

1. **Start Small**: Begin with small population sizes (10-20 animals)
2. **Short Runs**: Try shorter generations (5-10 weeks) initially
3. **Watch Closely**: Monitor the first few generations to understand the behavior
4. **Experiment**: Try different parameter combinations
5. **Save Configs**: Save interesting configurations for later use

## 🚀 Ready to Go!

The EvoSim GUI is now ready to use! Start with the default settings and explore the fascinating world of animal evolution simulation.

For detailed documentation, see `gui/README.md`.
