"""
Configuration Screen for Modern GUI

This module implements an interactive configuration screen
for setting up simulation parameters with sliders and input fields.

Author: Zen Garden
University of Caloocan City
"""

import arcade
import arcade.gui
from typing import Dict, Callable, Optional


class ConfigScreen:
    """Interactive configuration screen for simulation parameters."""
    
    def __init__(self, width: int, height: int, on_config_save: Optional[Callable] = None):
        self.width = width
        self.height = height
        self.on_config_save = on_config_save
        
        # Configuration values
        self.config = {
            'population_size': 30,
            'max_generations': 5,
            'steps_per_generation': 50,
            'food_density': 0.15,
            'water_density': 0.15,
            'simulation_speed': 1.0,
            'grid_width': 20,
            'grid_height': 20
        }
        
        # UI Manager
        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()
        
        # Create UI elements
        self._create_ui()
    
    def _create_ui(self):
        """Create the configuration UI elements."""
        # Title
        title = arcade.gui.UILabel(
            text="Simulation Configuration",
            center_x=self.width // 2,
            center_y=self.height - 50,
            style={"font_size": 32, "font_color": arcade.color.WHITE}
        )
        
        # Population size slider
        self.population_label = arcade.gui.UILabel(
            text=f"Population Size: {self.config['population_size']}",
            center_x=self.width // 2 - 200,
            center_y=self.height - 120,
            style={"font_size": 16, "font_color": arcade.color.WHITE}
        )
        
        self.population_slider = arcade.gui.UIInputText(
            center_x=self.width // 2 - 50,
            center_y=self.height - 120,
            width=100,
            height=30,
            text=str(self.config['population_size'])
        )
        self.population_slider.on_change = self._on_population_change
        
        # Max generations slider
        self.generations_label = arcade.gui.UILabel(
            text=f"Max Generations: {self.config['max_generations']}",
            center_x=self.width // 2 - 200,
            center_y=self.height - 160,
            style={"font_size": 16, "font_color": arcade.color.WHITE}
        )
        
        self.generations_slider = arcade.gui.UIInputText(
            center_x=self.width // 2 - 50,
            center_y=self.height - 160,
            width=100,
            height=30,
            text=str(self.config['max_generations'])
        )
        self.generations_slider.on_change = self._on_generations_change
        
        # Steps per generation
        self.steps_label = arcade.gui.UILabel(
            text=f"Steps per Generation: {self.config['steps_per_generation']}",
            center_x=self.width // 2 - 200,
            center_y=self.height - 200,
            style={"font_size": 16, "font_color": arcade.color.WHITE}
        )
        
        self.steps_slider = arcade.gui.UIInputText(
            center_x=self.width // 2 - 50,
            center_y=self.height - 200,
            width=100,
            height=30,
            text=str(self.config['steps_per_generation'])
        )
        self.steps_slider.on_change = self._on_steps_change
        
        # Food density
        self.food_label = arcade.gui.UILabel(
            text=f"Food Density: {self.config['food_density']:.2f}",
            center_x=self.width // 2 - 200,
            center_y=self.height - 240,
            style={"font_size": 16, "font_color": arcade.color.WHITE}
        )
        
        self.food_slider = arcade.gui.UIInputText(
            center_x=self.width // 2 - 50,
            center_y=self.height - 240,
            width=100,
            height=30,
            text=str(self.config['food_density'])
        )
        self.food_slider.on_change = self._on_food_change
        
        # Water density
        self.water_label = arcade.gui.UILabel(
            text=f"Water Density: {self.config['water_density']:.2f}",
            center_x=self.width // 2 - 200,
            center_y=self.height - 280,
            style={"font_size": 16, "font_color": arcade.color.WHITE}
        )
        
        self.water_slider = arcade.gui.UIInputText(
            center_x=self.width // 2 - 50,
            center_y=self.height - 280,
            width=100,
            height=30,
            text=str(self.config['water_density'])
        )
        self.water_slider.on_change = self._on_water_change
        
        # Grid size
        self.grid_label = arcade.gui.UILabel(
            text=f"Grid Size: {self.config['grid_width']}x{self.config['grid_height']}",
            center_x=self.width // 2 - 200,
            center_y=self.height - 320,
            style={"font_size": 16, "font_color": arcade.color.WHITE}
        )
        
        self.grid_width_input = arcade.gui.UIInputText(
            center_x=self.width // 2 - 100,
            center_y=self.height - 320,
            width=60,
            height=30,
            text=str(self.config['grid_width'])
        )
        self.grid_width_input.on_change = self._on_grid_width_change
        
        self.grid_height_input = arcade.gui.UIInputText(
            center_x=self.width // 2 - 20,
            center_y=self.height - 320,
            width=60,
            height=30,
            text=str(self.config['grid_height'])
        )
        self.grid_height_input.on_change = self._on_grid_height_change
        
        # Buttons
        save_button = arcade.gui.UIFlatButton(
            text="Save & Start",
            center_x=self.width // 2 - 100,
            center_y=100,
            width=150,
            height=50
        )
        save_button.on_click = self._on_save_click
        
        cancel_button = arcade.gui.UIFlatButton(
            text="Cancel",
            center_x=self.width // 2 + 100,
            center_y=100,
            width=150,
            height=50
        )
        cancel_button.on_click = self._on_cancel_click
        
        # Add all elements to UI manager
        self.ui_manager.add(title)
        self.ui_manager.add(self.population_label)
        self.ui_manager.add(self.population_slider)
        self.ui_manager.add(self.generations_label)
        self.ui_manager.add(self.generations_slider)
        self.ui_manager.add(self.steps_label)
        self.ui_manager.add(self.steps_slider)
        self.ui_manager.add(self.food_label)
        self.ui_manager.add(self.food_slider)
        self.ui_manager.add(self.water_label)
        self.ui_manager.add(self.water_slider)
        self.ui_manager.add(self.grid_label)
        self.ui_manager.add(self.grid_width_input)
        self.ui_manager.add(self.grid_height_input)
        self.ui_manager.add(save_button)
        self.ui_manager.add(cancel_button)
    
    def _on_population_change(self, event):
        """Handle population size change."""
        try:
            value = int(self.population_slider.text)
            self.config['population_size'] = max(1, min(100, value))
            self.population_label.text = f"Population Size: {self.config['population_size']}"
        except ValueError:
            pass
    
    def _on_generations_change(self, event):
        """Handle max generations change."""
        try:
            value = int(self.generations_slider.text)
            self.config['max_generations'] = max(1, min(20, value))
            self.generations_label.text = f"Max Generations: {self.config['max_generations']}"
        except ValueError:
            pass
    
    def _on_steps_change(self, event):
        """Handle steps per generation change."""
        try:
            value = int(self.steps_slider.text)
            self.config['steps_per_generation'] = max(10, min(1000, value))
            self.steps_label.text = f"Steps per Generation: {self.config['steps_per_generation']}"
        except ValueError:
            pass
    
    def _on_food_change(self, event):
        """Handle food density change."""
        try:
            value = float(self.food_slider.text)
            self.config['food_density'] = max(0.01, min(0.5, value))
            self.food_label.text = f"Food Density: {self.config['food_density']:.2f}"
        except ValueError:
            pass
    
    def _on_water_change(self, event):
        """Handle water density change."""
        try:
            value = float(self.water_slider.text)
            self.config['water_density'] = max(0.01, min(0.5, value))
            self.water_label.text = f"Water Density: {self.config['water_density']:.2f}"
        except ValueError:
            pass
    
    def _on_grid_width_change(self, event):
        """Handle grid width change."""
        try:
            value = int(self.grid_width_input.text)
            self.config['grid_width'] = max(10, min(50, value))
            self.grid_label.text = f"Grid Size: {self.config['grid_width']}x{self.config['grid_height']}"
        except ValueError:
            pass
    
    def _on_grid_height_change(self, event):
        """Handle grid height change."""
        try:
            value = int(self.grid_height_input.text)
            self.config['grid_height'] = max(10, min(50, value))
            self.grid_label.text = f"Grid Size: {self.config['grid_width']}x{self.config['grid_height']}"
        except ValueError:
            pass
    
    def _on_save_click(self, event):
        """Handle save button click."""
        if self.on_config_save:
            self.on_config_save(self.config)
    
    def _on_cancel_click(self, event):
        """Handle cancel button click."""
        # Return to main menu
        pass
    
    def draw(self):
        """Draw the configuration screen."""
        # Background
        arcade.draw_rectangle_filled(
            self.width // 2, self.height // 2,
            self.width, self.height,
            arcade.color.DARK_BLUE_GRAY
        )
        
        # Draw UI elements
        self.ui_manager.draw()
    
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """Handle mouse clicks."""
        pass
    
    def on_key_press(self, key: int, modifiers: int):
        """Handle key presses."""
        pass
