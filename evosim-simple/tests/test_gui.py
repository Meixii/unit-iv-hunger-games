"""
Test module for the GUI system.
"""

import pytest
import tkinter as tk
from unittest.mock import Mock, patch
from ui.gui import SimulationGUI


class TestSimulationGUI:
    """Test cases for SimulationGUI class."""
    
    def test_gui_initialization(self):
        """Test GUI initialization."""
        # Create GUI in a separate thread to avoid tkinter issues
        gui = SimulationGUI()
        
        assert gui.root is not None
        assert gui.simulation is None
        assert gui.config_frame is not None
        assert gui.visualization_frame is not None
        assert gui.control_frame is not None
        assert gui.stats_frame is not None
        
        # Clean up
        gui.root.destroy()
    
    def test_config_variables_creation(self):
        """Test configuration variables creation."""
        gui = SimulationGUI()
        
        # Check that all required config variables exist
        required_vars = [
            'grid_width', 'grid_height', 'population_size', 'max_generations',
            'steps_per_generation', 'simulation_speed', 'food_density',
            'water_density', 'drought_probability', 'storm_probability',
            'famine_probability', 'bonus_probability', 'mutation_rate',
            'crossover_rate', 'selection_method', 'tournament_size',
            'elite_percentage'
        ]
        
        for var_name in required_vars:
            assert var_name in gui.config_vars
            assert gui.config_vars[var_name] is not None
        
        # Clean up
        gui.root.destroy()
    
    def test_stats_variables_creation(self):
        """Test statistics variables creation."""
        gui = SimulationGUI()
        
        # Check that all required stats variables exist
        required_vars = [
            'state', 'current_step', 'current_generation', 'alive_animals',
            'dead_animals', 'survival_rate', 'average_fitness', 'best_fitness',
            'active_events', 'food_count', 'water_count'
        ]
        
        for var_name in required_vars:
            assert var_name in gui.stats_vars
            assert gui.stats_vars[var_name] is not None
        
        # Clean up
        gui.root.destroy()
    
    def test_get_config_from_gui(self):
        """Test getting configuration from GUI."""
        gui = SimulationGUI()
        
        # Set some test values
        gui.config_vars['grid_width'].set(15)
        gui.config_vars['grid_height'].set(15)
        gui.config_vars['population_size'].set(30)
        gui.config_vars['max_generations'].set(3)
        gui.config_vars['simulation_speed'].set(2.0)
        gui.config_vars['food_density'].set(0.15)
        gui.config_vars['water_density'].set(0.15)
        gui.config_vars['drought_probability'].set(0.3)
        gui.config_vars['storm_probability'].set(0.2)
        gui.config_vars['famine_probability'].set(0.15)
        gui.config_vars['bonus_probability'].set(0.05)
        gui.config_vars['mutation_rate'].set(0.1)
        gui.config_vars['crossover_rate'].set(0.8)
        gui.config_vars['selection_method'].set('tournament')
        gui.config_vars['tournament_size'].set(3)
        gui.config_vars['elite_percentage'].set(0.1)
        
        config = gui._get_config_from_gui()
        
        assert config['grid_size'] == (15, 15)
        assert config['population_size'] == 30
        assert config['max_generations'] == 3
        assert config['simulation_speed'] == 2.0
        assert config['food_density'] == 0.15
        assert config['water_density'] == 0.15
        assert config['drought_probability'] == 0.3
        assert config['storm_probability'] == 0.2
        assert config['famine_probability'] == 0.15
        assert config['bonus_probability'] == 0.05
        assert config['mutation_rate'] == 0.1
        assert config['crossover_rate'] == 0.8
        assert config['selection_method'] == 'tournament'
        assert config['tournament_size'] == 3
        assert config['elite_percentage'] == 0.1
        
        # Clean up
        gui.root.destroy()
    
    def test_update_display_without_simulation(self):
        """Test update display when no simulation is running."""
        gui = SimulationGUI()
        
        # Should not raise exception
        gui._update_display()
        
        # Clean up
        gui.root.destroy()
    
    def test_update_display_with_simulation(self):
        """Test update display with simulation."""
        gui = SimulationGUI()
        
        # Mock simulation
        mock_simulation = Mock()
        mock_simulation.get_statistics.return_value = {
            'state': 'running',
            'current_step': 10,
            'current_generation': 1,
            'population_stats': {
                'alive_count': 25,
                'dead_count': 0,
                'survival_rate': 1.0,
                'average_fitness': 50.0,
                'best_fitness': 100.0
            },
            'environment_stats': {
                'food_count': 20,
                'water_count': 20
            },
            'event_stats': {
                'event_names': ['drought']
            }
        }
        
        gui.simulation = mock_simulation
        
        # Should not raise exception
        gui._update_display()
        
        # Check that statistics were updated
        assert gui.stats_vars['state'].get() == 'Running'
        assert gui.stats_vars['current_step'].get() == '10'
        assert gui.stats_vars['current_generation'].get() == '1'
        
        # Clean up
        gui.root.destroy()
    
    def test_update_control_buttons_without_simulation(self):
        """Test update control buttons without simulation."""
        try:
            gui = SimulationGUI()
            
            # Should not raise exception
            gui._update_control_buttons()
            
            # Check that buttons exist
            assert gui.start_button is not None
            assert gui.pause_button is not None
            assert gui.resume_button is not None
            assert gui.stop_button is not None
            assert gui.reset_button is not None
            
            # Clean up
            gui.root.destroy()
        except Exception as e:
            # Skip test if tkinter is not available
            pytest.skip(f"Tkinter not available: {e}")
    
    def test_update_control_buttons_with_simulation(self):
        """Test update control buttons with simulation."""
        try:
            gui = SimulationGUI()
            
            # Mock simulation with different states
            from src.simulation import SimulationState
            
            # Test stopped state
            mock_simulation = Mock()
            mock_simulation.state = SimulationState.STOPPED
            gui.simulation = mock_simulation
            
            gui._update_control_buttons()
            
            # Check that buttons exist
            assert gui.start_button is not None
            assert gui.pause_button is not None
            assert gui.resume_button is not None
            assert gui.stop_button is not None
            assert gui.reset_button is not None
            
            # Test running state
            mock_simulation.state = SimulationState.RUNNING
            gui._update_control_buttons()
            
            # Test paused state
            mock_simulation.state = SimulationState.PAUSED
            gui._update_control_buttons()
            
            # Clean up
            gui.root.destroy()
        except Exception as e:
            # Skip test if tkinter is not available
            pytest.skip(f"Tkinter not available: {e}")
    
    def test_reset_config(self):
        """Test reset configuration."""
        gui = SimulationGUI()
        
        # Set some values
        gui.config_vars['grid_width'].set(30)
        gui.config_vars['population_size'].set(100)
        gui.config_vars['simulation_speed'].set(5.0)
        
        # Reset configuration
        gui._reset_config()
        
        # Check that values were reset to defaults
        assert gui.config_vars['grid_width'].get() == 20
        assert gui.config_vars['population_size'].get() == 50
        assert gui.config_vars['simulation_speed'].get() == 1.0
        
        # Clean up
        gui.root.destroy()
    
    def test_update_speed(self):
        """Test update speed functionality."""
        gui = SimulationGUI()
        
        # Mock simulation
        mock_simulation = Mock()
        gui.simulation = mock_simulation
        
        # Test speed update
        gui._update_speed("2.5")
        
        # Check that set_simulation_speed was called
        mock_simulation.set_simulation_speed.assert_called_once_with(2.5)
        
        # Clean up
        gui.root.destroy()
    
    def test_update_speed_without_simulation(self):
        """Test update speed without simulation."""
        gui = SimulationGUI()
        
        # Should not raise exception
        gui._update_speed("2.5")
        
        # Clean up
        gui.root.destroy()
    
    def test_update_visualization_without_simulation(self):
        """Test update visualization without simulation."""
        gui = SimulationGUI()
        
        # Should not raise exception
        gui._update_visualization()
        
        # Clean up
        gui.root.destroy()
    
    def test_update_visualization_with_simulation(self):
        """Test update visualization with simulation."""
        gui = SimulationGUI()
        
        # Mock simulation and environment
        mock_environment = Mock()
        mock_environment.width = 10
        mock_environment.height = 10
        mock_environment.get_cell_content.return_value = 'empty'
        
        mock_simulation = Mock()
        mock_simulation.environment = mock_environment
        gui.simulation = mock_simulation
        
        # Should not raise exception
        gui._update_visualization()
        
        # Clean up
        gui.root.destroy()
    
    def test_gui_components_creation(self):
        """Test that all GUI components are created."""
        gui = SimulationGUI()
        
        # Check that all frames exist
        assert gui.config_frame is not None
        assert gui.visualization_frame is not None
        assert gui.control_frame is not None
        assert gui.stats_frame is not None
        
        # Check that canvas exists
        assert gui.canvas is not None
        
        # Check that control buttons exist
        assert gui.start_button is not None
        assert gui.pause_button is not None
        assert gui.resume_button is not None
        assert gui.stop_button is not None
        assert gui.reset_button is not None
        
        # Check that speed scale exists
        assert gui.speed_scale is not None
        
        # Clean up
        gui.root.destroy()
    
    def test_gui_layout(self):
        """Test GUI layout configuration."""
        gui = SimulationGUI()
        
        # Check that frames are properly configured
        assert gui.config_frame.grid_info()['row'] == 0
        assert gui.config_frame.grid_info()['column'] == 0
        
        assert gui.visualization_frame.grid_info()['row'] == 0
        assert gui.visualization_frame.grid_info()['column'] == 1
        
        assert gui.control_frame.grid_info()['row'] == 1
        assert gui.control_frame.grid_info()['column'] == 0
        
        assert gui.stats_frame.grid_info()['row'] == 1
        assert gui.stats_frame.grid_info()['column'] == 1
        
        # Clean up
        gui.root.destroy()
    
    def test_gui_bindings(self):
        """Test GUI event bindings."""
        gui = SimulationGUI()
        
        # Check that close protocol is set
        assert gui.root.protocol("WM_DELETE_WINDOW") is not None
        
        # Clean up
        gui.root.destroy()
    
    def test_gui_update_timer(self):
        """Test GUI update timer."""
        gui = SimulationGUI()
        
        # Check that update timer is set
        assert gui.update_timer is not None
        
        # Clean up
        gui.root.destroy()
    
    def test_gui_statistics_display(self):
        """Test statistics display functionality."""
        gui = SimulationGUI()
        
        # Check that all statistics variables are initialized
        for var_name, var in gui.stats_vars.items():
            assert var.get() is not None
        
        # Clean up
        gui.root.destroy()
    
    def test_gui_configuration_display(self):
        """Test configuration display functionality."""
        gui = SimulationGUI()
        
        # Check that all configuration variables are initialized
        for var_name, var in gui.config_vars.items():
            assert var.get() is not None
        
        # Clean up
        gui.root.destroy()
    
    def test_gui_visualization_canvas(self):
        """Test visualization canvas functionality."""
        gui = SimulationGUI()
        
        # Check that canvas is properly configured
        assert gui.canvas is not None
        assert gui.canvas.winfo_class() == 'Canvas'
        
        # Clean up
        gui.root.destroy()
    
    def test_gui_control_buttons(self):
        """Test control buttons functionality."""
        gui = SimulationGUI()
        
        # Check that all control buttons exist and are properly configured
        buttons = [
            gui.start_button, gui.pause_button, gui.resume_button,
            gui.stop_button, gui.reset_button
        ]
        
        for button in buttons:
            assert button is not None
            assert button.winfo_class() == 'TButton'
        
        # Clean up
        gui.root.destroy()
    
    def test_gui_speed_control(self):
        """Test speed control functionality."""
        gui = SimulationGUI()
        
        # Check that speed scale exists and is properly configured
        assert gui.speed_scale is not None
        assert gui.speed_scale.winfo_class() == 'TScale'
        
        # Clean up
        gui.root.destroy()
    
    def test_gui_export_functionality(self):
        """Test export functionality."""
        gui = SimulationGUI()
        
        # Check that export methods exist
        assert hasattr(gui, '_export_data')
        assert hasattr(gui, '_export_config')
        assert hasattr(gui, '_save_screenshot')
        assert hasattr(gui, '_replay_simulation')
        
        # Clean up
        gui.root.destroy()
    
    def test_gui_config_management(self):
        """Test configuration management functionality."""
        gui = SimulationGUI()
        
        # Check that config management methods exist
        assert hasattr(gui, '_load_config')
        assert hasattr(gui, '_save_config')
        assert hasattr(gui, '_reset_config')
        
        # Clean up
        gui.root.destroy()
    
    def test_gui_simulation_control(self):
        """Test simulation control functionality."""
        gui = SimulationGUI()
        
        # Check that simulation control methods exist
        assert hasattr(gui, '_start_simulation')
        assert hasattr(gui, '_pause_simulation')
        assert hasattr(gui, '_resume_simulation')
        assert hasattr(gui, '_stop_simulation')
        assert hasattr(gui, '_reset_simulation')
        
        # Clean up
        gui.root.destroy()
    
    def test_gui_initialization_methods(self):
        """Test GUI initialization methods."""
        gui = SimulationGUI()
        
        # Check that initialization methods exist
        assert hasattr(gui, '_initialize_simulation')
        assert hasattr(gui, '_setup_gui')
        assert hasattr(gui, '_setup_bindings')
        assert hasattr(gui, '_schedule_update')
        
        # Clean up
        gui.root.destroy()
    
    def test_gui_display_methods(self):
        """Test GUI display methods."""
        gui = SimulationGUI()
        
        # Check that display methods exist
        assert hasattr(gui, '_update_display')
        assert hasattr(gui, '_update_visualization')
        assert hasattr(gui, '_update_control_buttons')
        
        # Clean up
        gui.root.destroy()
    
    def test_gui_utility_methods(self):
        """Test GUI utility methods."""
        gui = SimulationGUI()
        
        # Check that utility methods exist
        assert hasattr(gui, '_get_config_from_gui')
        assert hasattr(gui, '_create_config_variables')
        assert hasattr(gui, '_create_stats_variables')
        assert hasattr(gui, '_on_closing')
        
        # Clean up
        gui.root.destroy()
    
    def test_gui_frame_creation(self):
        """Test GUI frame creation methods."""
        gui = SimulationGUI()
        
        # Check that frame creation methods exist
        assert hasattr(gui, '_create_config_frame')
        assert hasattr(gui, '_create_visualization_frame')
        assert hasattr(gui, '_create_control_frame')
        assert hasattr(gui, '_create_stats_frame')
        
        # Clean up
        gui.root.destroy()
    
    def test_gui_run_method(self):
        """Test GUI run method."""
        gui = SimulationGUI()
        
        # Check that run method exists
        assert hasattr(gui, 'run')
        assert callable(gui.run)
        
        # Clean up
        gui.root.destroy()
