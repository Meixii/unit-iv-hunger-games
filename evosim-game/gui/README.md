# EvoSim GUI

A comprehensive graphical user interface for the EvoSim animal evolution simulation.

## Features

### 🎮 Simulation Control
- **Start/Stop/Pause/Resume** simulation with real-time controls
- **Configuration Management** with customizable parameters
- **Real-time Status Monitoring** showing generation, week, and population data

### 🗺️ World Visualization
- **Interactive World Grid** showing terrain types and animal positions
- **Zoom and Pan** capabilities for detailed exploration
- **Click-to-Inspect** tiles for detailed information
- **Color-coded Terrain** for easy identification

### 📊 Statistics & Monitoring
- **Live Animal Statistics** grouped by category
- **Fitness and Health Tracking** with average calculations
- **Event Logging** with timestamped messages
- **Population Dynamics** monitoring

### ⚙️ Configuration
- **Population Size** control
- **Generation Limits** setting
- **Week Limits** configuration
- **Random Seed** for reproducible results
- **Save/Load** configuration files

## Quick Start

### Windows Users
1. Double-click `run_gui.bat` to launch the GUI
2. Configure your simulation parameters
3. Click "Start Simulation" to begin

### All Platforms
1. Open a terminal/command prompt
2. Navigate to the gui directory
3. Run: `python run_gui.py`

## Requirements

### Required
- Python 3.7 or higher
- tkinter (usually included with Python)
- Access to the evosim-game simulation modules

### Optional (for enhanced features)
- matplotlib (for advanced visualizations)
- numpy (for data processing)
- pandas (for data export)

## Installation

1. **Install Python Dependencies** (optional):
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure evosim-game is available**:
   - The GUI expects the `evosim-game` directory to be in the parent directory
   - Make sure all simulation modules are properly installed

## Usage Guide

### Starting a Simulation

1. **Configure Parameters**:
   - Set population size (default: 20)
   - Set maximum generations (default: 10)
   - Set maximum weeks per generation (default: 20)
   - Optionally set a random seed for reproducible results

2. **Start Simulation**:
   - Click "Start Simulation" to begin
   - Watch the real-time visualization
   - Monitor statistics in the right panel

3. **Control Simulation**:
   - Use "Pause" to temporarily stop
   - Use "Resume" to continue
   - Use "Stop" to end the simulation
   - Use "Reset" to clear and start over

### Exploring the World

1. **World Grid**:
   - The main visualization shows the world grid
   - Different colors represent different terrain types
   - Animals appear as colored circles on the grid

2. **Terrain Types**:
   - 🟢 **Plains** (Light Green) - Basic terrain
   - 🌲 **Forest** (Dark Green) - Rich in resources
   - 🌿 **Jungle** (Very Dark Green) - Abundant resources
   - 💧 **Water** (Blue) - Water sources
   - 🐸 **Swamp** (Gray-Green) - Challenging terrain
   - ⛰️ **Mountains** (Gray) - Difficult to traverse

3. **Animal Categories**:
   - 🟡 **Herbivores** (Gold) - Plant eaters
   - 🔴 **Carnivores** (Red) - Meat eaters
   - 🟣 **Omnivores** (Purple) - Mixed diet

4. **Interacting with the World**:
   - **Click** on tiles to see detailed information
   - **Scroll** to zoom in/out
   - **Drag** to pan around the world

### Monitoring Progress

1. **Status Panel**:
   - Current generation number
   - Current week within generation
   - Number of living animals
   - Simulation status (Ready/Running/Paused/Stopped)

2. **Statistics Panel**:
   - Animal count by category
   - Average fitness scores
   - Average health levels

3. **Event Log**:
   - Timestamped messages about simulation events
   - Error messages and warnings
   - Status updates

### Configuration Management

1. **Load Configuration**:
   - Use File → Load Configuration
   - Select a JSON configuration file
   - Parameters will be loaded into the interface

2. **Save Configuration**:
   - Use File → Save Configuration
   - Choose a location and filename
   - Current parameters will be saved

3. **Export Data**:
   - Use File → Export Data
   - Export simulation data to CSV format
   - Useful for analysis and reporting

## Troubleshooting

### Common Issues

1. **"Module not found" errors**:
   - Ensure the `evosim-game` directory exists in the parent directory
   - Check that all simulation modules are properly installed

2. **GUI won't start**:
   - Verify Python 3.7+ is installed
   - Check that tkinter is available (usually included with Python)
   - Run `python run_gui.py` from the gui directory

3. **Simulation won't start**:
   - Check that all required modules are imported correctly
   - Verify configuration parameters are valid
   - Check the event log for error messages

4. **Visualization issues**:
   - Try resizing the window
   - Use the scroll bars to navigate
   - Reset the simulation if needed

### Getting Help

1. **Check the Event Log** for error messages
2. **Verify Dependencies** are properly installed
3. **Check File Paths** are correct
4. **Review Configuration** parameters

## Advanced Features

### Custom Configurations
- Modify simulation parameters through the GUI
- Save and load custom configurations
- Experiment with different parameter combinations

### Data Export
- Export population data for analysis
- Generate reports on simulation results
- Track evolution progress over time

### Real-time Monitoring
- Watch animals evolve in real-time
- Monitor population dynamics
- Track fitness improvements

## File Structure

```
gui/
├── main_gui.py          # Main GUI application
├── run_gui.py           # GUI launcher script
├── run_gui.bat          # Windows batch file
├── requirements.txt     # Optional dependencies
└── README.md           # This file
```

## Contributing

To contribute to the GUI:

1. **Report Issues**: Use the issue tracker for bugs and feature requests
2. **Submit Pull Requests**: For code improvements and new features
3. **Documentation**: Help improve this README and code comments
4. **Testing**: Test on different platforms and Python versions

## License

This GUI is part of the EvoSim project and follows the same license terms.
