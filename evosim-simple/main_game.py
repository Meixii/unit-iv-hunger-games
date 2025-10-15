"""
Main Gamified GUI for the Evolutionary Simulation using Arcade.

This module provides an interactive and visually engaging interface for the
simulation, designed to be more accessible for educational purposes.

Author: Zen Garden & Gemini
University of Caloocan City
"""

import arcade
import arcade.gui
import json
import time
from typing import Optional

# Import your existing simulation logic
from src.simulation import Simulation, SimulationState

# --- Constants for the GUI ---
# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Evolutionary Ecosystem Simulator"

# Grid visualization dimensions
GRID_START_X = 450
GRID_START_Y = 150
GRID_WIDTH_PIXELS = 1000
GRID_HEIGHT_PIXELS = 750

# UI Panel dimensions
LEFT_PANEL_WIDTH = 400
RIGHT_PANEL_WIDTH = 400
BOTTOM_PANEL_HEIGHT = 250
ANIMAL_DETAILS_PANEL_WIDTH = 350

# Colors - Modern color scheme
BACKGROUND_COLOR = (34, 40, 49)  # Dark blue-gray
PANEL_COLOR = (52, 58, 64)  # Darker gray
PANEL_BORDER_COLOR = (73, 80, 87)  # Light gray border
TEXT_COLOR = (248, 249, 250)  # Light gray text
ACCENT_COLOR = (0, 123, 255)  # Blue accent
SUCCESS_COLOR = (40, 167, 69)  # Green
WARNING_COLOR = (255, 193, 7)  # Yellow
DANGER_COLOR = (220, 53, 69)  # Red
INFO_COLOR = (23, 162, 184)  # Cyan


class SimGame(arcade.Window):
    """ Main Arcade application class for the simulation. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
        arcade.set_background_color(BACKGROUND_COLOR)

        # --- Simulation Logic ---
        self.simulation: Optional[Simulation] = None
        self.is_initialized = False

        # --- UI Manager & Widgets ---
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self._setup_ui()

        # --- Sprites and Drawing ---
        self.animal_sprites = arcade.SpriteList()
        self.food_sprites = arcade.SpriteList()
        self.water_sprites = arcade.SpriteList()
        self.grid_lines = []
        self.cell_size = 30 # Default value, will be calculated on init
        
        # Animal details tracking
        self.selected_animal = None
        self.animal_details_visible = False

    def _setup_ui(self):
        """ Create all the GUI widgets and anchor them to the screen. """
        # --- Left Panel for Controls & Stats ---
        left_panel_box = arcade.gui.UIBoxLayout(vertical=True)

        # Title for the panel
        left_panel_box.add(arcade.gui.UILabel(
            text="CONTROLS", 
            font_size=20, 
            font_name="Arial", 
            bold=True,
            text_color=ACCENT_COLOR
        ).with_space_around(bottom=10))

        # Control Buttons
        button_row = arcade.gui.UIBoxLayout(vertical=False)
        init_button = arcade.gui.UIFlatButton(
            text="Initialize", 
            width=110,
            style={"bg_color": SUCCESS_COLOR, "font_color": TEXT_COLOR, "border_width": 2, "border_color": PANEL_BORDER_COLOR}
        )
        self.start_button = arcade.gui.UIFlatButton(
            text="Start", 
            width=110,
            style={"bg_color": SUCCESS_COLOR, "font_color": TEXT_COLOR, "border_width": 2, "border_color": PANEL_BORDER_COLOR}
        )
        self.pause_button = arcade.gui.UIFlatButton(
            text="Pause", 
            width=110,
            style={"bg_color": WARNING_COLOR, "font_color": TEXT_COLOR, "border_width": 2, "border_color": PANEL_BORDER_COLOR}
        )
        stop_button = arcade.gui.UIFlatButton(
            text="Stop", 
            width=110,
            style={"bg_color": DANGER_COLOR, "font_color": TEXT_COLOR, "border_width": 2, "border_color": PANEL_BORDER_COLOR}
        )

        init_button.on_click = self.on_click_initialize
        self.start_button.on_click = self.on_click_start
        self.pause_button.on_click = self.on_click_pause
        stop_button.on_click = self.on_click_stop

        button_row.add(init_button.with_space_around(right=5))
        button_row.add(self.start_button.with_space_around(right=5))
        button_row.add(self.pause_button.with_space_around(right=5))
        button_row.add(stop_button)
        left_panel_box.add(button_row.with_space_around(bottom=20))
        
        # --- Speed Control ---
        speed_section = arcade.gui.UIBoxLayout(vertical=True)
        speed_section.add(arcade.gui.UILabel(
            text="Simulation Speed", 
            text_color=TEXT_COLOR,
            font_size=14
        ).with_space_around(bottom=5))
        
        # Speed input with buttons
        speed_control_row = arcade.gui.UIBoxLayout(vertical=False)
        
        # Speed down button
        speed_down_button = arcade.gui.UIFlatButton(
            text="-", 
            width=40,
            style={"bg_color": WARNING_COLOR, "font_color": TEXT_COLOR, "border_width": 2, "border_color": PANEL_BORDER_COLOR}
        )
        speed_down_button.on_click = lambda e: self.adjust_speed(-0.1)
        speed_control_row.add(speed_down_button.with_space_around(right=5))
        
        # Speed display
        self.speed_display = arcade.gui.UILabel(
            text="1.0x", 
            width=80,
            text_color=TEXT_COLOR,
            font_size=14
        )
        speed_control_row.add(self.speed_display.with_space_around(right=5))
        
        # Speed up button
        speed_up_button = arcade.gui.UIFlatButton(
            text="+", 
            width=40,
            style={"bg_color": SUCCESS_COLOR, "font_color": TEXT_COLOR, "border_width": 2, "border_color": PANEL_BORDER_COLOR}
        )
        speed_up_button.on_click = lambda e: self.adjust_speed(0.1)
        speed_control_row.add(speed_up_button)
        
        speed_section.add(speed_control_row)
        left_panel_box.add(speed_section.with_space_around(bottom=20))
        
        # Store current speed
        self.current_speed = 1.0

        # --- Configuration Buttons ---
        config_row = arcade.gui.UIBoxLayout(vertical=False)
        
        load_config_button = arcade.gui.UIFlatButton(
            text="Load Config", 
            width=90,
            style={"bg_color": INFO_COLOR, "font_color": TEXT_COLOR, "border_width": 2, "border_color": PANEL_BORDER_COLOR}
        )
        load_config_button.on_click = self.on_click_load_config
        config_row.add(load_config_button.with_space_around(right=5))
        
        save_config_button = arcade.gui.UIFlatButton(
            text="Save Config", 
            width=90,
            style={"bg_color": INFO_COLOR, "font_color": TEXT_COLOR, "border_width": 2, "border_color": PANEL_BORDER_COLOR}
        )
        save_config_button.on_click = self.on_click_save_config
        config_row.add(save_config_button.with_space_around(right=5))
        
        export_button = arcade.gui.UIFlatButton(
            text="Export", 
            width=90,
            style={"bg_color": ACCENT_COLOR, "font_color": TEXT_COLOR, "border_width": 2, "border_color": PANEL_BORDER_COLOR}
        )
        export_button.on_click = self.on_click_export_data
        config_row.add(export_button.with_space_around(right=5))
        
        config_button = arcade.gui.UIFlatButton(
            text="Configure", 
            width=90,
            style={"bg_color": (255, 165, 0), "font_color": TEXT_COLOR, "border_width": 2, "border_color": PANEL_BORDER_COLOR}
        )
        config_button.on_click = self.on_click_configure
        config_row.add(config_button)

        left_panel_box.add(config_row.with_space_around(bottom=20))

        # --- Live Statistics Section ---
        left_panel_box.add(arcade.gui.UILabel(
            text="LIVE STATISTICS", 
            font_size=18, 
            font_name="Arial", 
            bold=True,
            text_color=ACCENT_COLOR
        ).with_space_around(bottom=10, top=20))

        # Instructions
        left_panel_box.add(arcade.gui.UILabel(
            text="Click animals to inspect them!",
            text_color=WARNING_COLOR,
            font_size=12,
            italic=True
        ).with_space_around(bottom=10))

        # Anchor the entire left panel to the bottom-left corner
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                align_x=20,
                align_y=20,
                child=left_panel_box)
        )

        # --- Right Panel for Selected Animal Info ---
        right_panel_box = arcade.gui.UIBoxLayout(vertical=True)
        right_panel_box.add(arcade.gui.UILabel(
            text="SELECTED ANIMAL", 
            font_size=20, 
            font_name="Arial", 
            bold=True,
            text_color=ACCENT_COLOR
        ).with_space_around(bottom=10))
        
        # Animal info text area
        self.selected_animal_info = arcade.gui.UITextArea(
            text="Click an animal in the grid to see its detailed statistics and behavior patterns.", 
            width=350, 
            height=200, 
            font_size=12,
            text_color=TEXT_COLOR
        )
        right_panel_box.add(self.selected_animal_info.with_space_around(top=10))
        
        # Live Graph placeholder
        right_panel_box.add(arcade.gui.UILabel(
            text="LIVE GRAPH", 
            font_size=18, 
            font_name="Arial", 
            bold=True,
            text_color=ACCENT_COLOR
        ).with_space_around(top=20, bottom=10))
        
        graph_placeholder = arcade.gui.UITextArea(
            text="Population and fitness trends will be displayed here in real-time as the simulation progresses.",
            width=350,
            height=150,
            font_size=12,
            text_color=TEXT_COLOR
        )
        right_panel_box.add(graph_placeholder)
        
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="right",
                anchor_y="top",
                align_x=-20,
                align_y=-20,
                child=right_panel_box)
        )

    def on_click_initialize(self, event):
        """ Initialize the simulation with default or loaded config. """
        if self.is_initialized:
            print("Simulation is already initialized.")
            return

        try:
            # --- Using the provided config file for consistency ---
            with open("config_1760461028.8971348.json", 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            print("Config file not found. Using default simulation settings.")
            config = None # Let the simulation use its defaults

        self.simulation = Simulation(config)
        self.simulation.initialize()
        self.is_initialized = True
        
        # Calculate cell size based on grid and screen space
        grid_config = self.simulation.config['grid_size']
        self.cell_size = min(GRID_WIDTH_PIXELS // grid_config[0], GRID_HEIGHT_PIXELS // grid_config[1])
        
        # Create grid lines for drawing
        self._create_grid_lines()
        
        print("Simulation Initialized!")

    def _create_grid_lines(self):
        """ Pre-calculate the lines for the grid for faster drawing. """
        self.grid_lines = []
        grid_rows = self.simulation.config['grid_size'][1]
        grid_cols = self.simulation.config['grid_size'][0]

        # Calculate adjusted grid position
        grid_bottom = max(GRID_START_Y, BOTTOM_PANEL_HEIGHT + 20)
        
        for row in range(grid_rows + 1):
            y = grid_bottom + row * self.cell_size
            start_point = (GRID_START_X, y)
            end_point = (GRID_START_X + grid_cols * self.cell_size, y)
            self.grid_lines.append((start_point, end_point))

        for col in range(grid_cols + 1):
            x = GRID_START_X + col * self.cell_size
            start_point = (x, grid_bottom)
            end_point = (x, grid_bottom + grid_rows * self.cell_size)
            self.grid_lines.append((start_point, end_point))

    def on_click_start(self, event):
        """ Start the simulation. """
        if self.is_initialized and self.simulation.state == SimulationState.STOPPED:
            self.simulation.start()
            print("Simulation Started!")
        else:
            print("Initialize the simulation before starting.")

    def on_click_pause(self, event):
        """ Pause/Resume the simulation. """
        if not self.simulation:
            return
            
        if self.simulation.state == SimulationState.RUNNING:
            self.simulation.pause()
            self.pause_button.text = "Resume"
            print("Simulation Paused.")
        elif self.simulation.state == SimulationState.PAUSED:
            self.simulation.resume()
            self.pause_button.text = "Pause"
            print("Simulation Resumed.")

    def on_click_stop(self, event):
        """ Stop the simulation. """
        if self.simulation and self.simulation.state != SimulationState.STOPPED:
            self.simulation.stop()
            self.pause_button.text = "Pause"  # Reset button text
            print("Simulation Stopped.")

    def adjust_speed(self, delta):
        """ Adjust simulation speed by the given delta. """
        self.current_speed = max(0.1, min(5.0, self.current_speed + delta))
        self.current_speed = round(self.current_speed, 1)
        
        # Update display
        self.speed_display.text = f"{self.current_speed}x"
        
        # Apply to simulation if it exists
        if self.simulation:
            self.simulation.set_simulation_speed(self.current_speed)
            print(f"Simulation speed set to: {self.current_speed}")

    def on_click_load_config(self, event):
        """ Load configuration from file. """
        # For now, just use default config
        print("Load config functionality - using default config")

    def on_click_save_config(self, event):
        """ Save current configuration. """
        if self.simulation:
            config = self.simulation.config
            filename = f"config_{time.time()}.json"
            with open(filename, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"Configuration saved to {filename}")

    def on_click_export_data(self, event):
        """ Export simulation data. """
        if self.simulation:
            # Export generation history
            gen_history = self.simulation.get_generation_history()
            filename = f"simulation_data_{time.time()}.json"
            with open(filename, 'w') as f:
                json.dump(gen_history, f, indent=2)
            print(f"Simulation data exported to {filename}")
    
    def on_click_configure(self, event):
        """ Open configuration screen. """
        self.show_config_screen()
    
    def show_config_screen(self):
        """ Show configuration screen with editable parameters. """
        # Create a modal configuration window
        config_window = arcade.gui.UIBoxLayout(vertical=True)
        
        # Title
        title = arcade.gui.UILabel(
            text="SIMULATION CONFIGURATION",
            width=600,
            text_color=ACCENT_COLOR,
            font_size=20,
            bold=True
        )
        config_window.add(title.with_space_around(bottom=20))
        
        # Grid Size Configuration
        grid_section = arcade.gui.UIBoxLayout(vertical=True)
        grid_title = arcade.gui.UILabel(text="Grid Settings", width=600, text_color=INFO_COLOR, font_size=16, bold=True)
        grid_section.add(grid_title.with_space_around(bottom=10))
        
        grid_row = arcade.gui.UIBoxLayout(vertical=False)
        grid_row.add(arcade.gui.UILabel(text="Width:", width=100, text_color=TEXT_COLOR))
        width_input = arcade.gui.UIInputText(text="20", width=80)
        grid_row.add(width_input.with_space_around(right=20))
        
        grid_row.add(arcade.gui.UILabel(text="Height:", width=100, text_color=TEXT_COLOR))
        height_input = arcade.gui.UIInputText(text="20", width=80)
        grid_row.add(height_input)
        
        grid_section.add(grid_row)
        config_window.add(grid_section.with_space_around(bottom=20))
        
        # Population Configuration
        pop_section = arcade.gui.UIBoxLayout(vertical=True)
        pop_title = arcade.gui.UILabel(text="Population Settings", width=600, text_color=INFO_COLOR, font_size=16, bold=True)
        pop_section.add(pop_title.with_space_around(bottom=10))
        
        pop_row = arcade.gui.UIBoxLayout(vertical=False)
        pop_row.add(arcade.gui.UILabel(text="Population Size:", width=150, text_color=TEXT_COLOR))
        pop_input = arcade.gui.UIInputText(text="50", width=80)
        pop_row.add(pop_input.with_space_around(right=20))
        
        pop_row.add(arcade.gui.UILabel(text="Max Generations:", width=150, text_color=TEXT_COLOR))
        gen_input = arcade.gui.UIInputText(text="5", width=80)
        pop_row.add(gen_input)
        
        pop_section.add(pop_row)
        config_window.add(pop_section.with_space_around(bottom=20))
        
        # Resource Configuration
        resource_section = arcade.gui.UIBoxLayout(vertical=True)
        resource_title = arcade.gui.UILabel(text="Resource Settings", width=600, text_color=INFO_COLOR, font_size=16, bold=True)
        resource_section.add(resource_title.with_space_around(bottom=10))
        
        resource_row = arcade.gui.UIBoxLayout(vertical=False)
        resource_row.add(arcade.gui.UILabel(text="Food Density:", width=120, text_color=TEXT_COLOR))
        food_input = arcade.gui.UIInputText(text="0.15", width=80)
        resource_row.add(food_input.with_space_around(right=20))
        
        resource_row.add(arcade.gui.UILabel(text="Water Density:", width=120, text_color=TEXT_COLOR))
        water_input = arcade.gui.UIInputText(text="0.15", width=80)
        resource_row.add(water_input)
        
        resource_section.add(resource_row)
        config_window.add(resource_section.with_space_around(bottom=20))
        
        # Buttons
        button_row = arcade.gui.UIBoxLayout(vertical=False)
        
        apply_button = arcade.gui.UIFlatButton(
            text="Apply & Initialize",
            width=150,
            style={"bg_color": SUCCESS_COLOR, "font_color": TEXT_COLOR, "border_width": 2, "border_color": PANEL_BORDER_COLOR}
        )
        apply_button.on_click = lambda e: self.apply_config(width_input.text, height_input.text, pop_input.text, gen_input.text, food_input.text, water_input.text)
        button_row.add(apply_button.with_space_around(right=20))
        
        cancel_button = arcade.gui.UIFlatButton(
            text="Cancel",
            width=100,
            style={"bg_color": DANGER_COLOR, "font_color": TEXT_COLOR, "border_width": 2, "border_color": PANEL_BORDER_COLOR}
        )
        cancel_button.on_click = lambda e: self.hide_config_screen()
        button_row.add(cancel_button)
        
        config_window.add(button_row)
        
        # Add to manager
        self.config_widget = arcade.gui.UIAnchorWidget(
            anchor_x="center",
            anchor_y="center",
            align_x=0,
            align_y=0,
            child=config_window
        )
        self.manager.add(self.config_widget)
    
    def apply_config(self, width, height, population, generations, food_density, water_density):
        """ Apply configuration and initialize simulation. """
        try:
            # Parse inputs
            grid_width = int(width)
            grid_height = int(height)
            pop_size = int(population)
            max_gens = int(generations)
            food_dens = float(food_density)
            water_dens = float(water_density)
            
            # Create new config
            config = {
                'grid_size': (grid_width, grid_height),
                'population_size': pop_size,
                'max_generations': max_gens,
                'steps_per_generation': 50,
                'simulation_speed': 1.0,
                'food_density': food_dens,
                'water_density': water_dens,
                'drought_probability': 0.02,
                'storm_probability': 0.01,
                'famine_probability': 0.05,
                'bonus_probability': 0.05,
                'mutation_rate': 0.1,
                'crossover_rate': 0.8,
                'selection_method': 'tournament',
                'tournament_size': 3,
                'elite_percentage': 0.1
            }
            
            # Initialize with new config
            self.simulation = Simulation(config)
            self.simulation.initialize()
            self.is_initialized = True
            
            # Recalculate cell size and grid lines
            self.cell_size = min(GRID_WIDTH_PIXELS // grid_width, GRID_HEIGHT_PIXELS // grid_height)
            self._create_grid_lines()
            
            # Hide config screen
            self.hide_config_screen()
            
            print(f"Simulation initialized with custom config: {grid_width}x{grid_height} grid, {pop_size} animals")
            
        except ValueError as e:
            print(f"Invalid configuration values: {e}")
    
    def hide_config_screen(self):
        """ Hide the configuration screen. """
        if hasattr(self, 'config_widget'):
            self.manager.remove(self.config_widget)
            self.config_widget = None

    def on_update(self, delta_time: float):
        """ Main update loop. """
        if not self.is_initialized or not self.simulation:
            return

        # Update sprite lists based on the simulation state (throttled to avoid excessive updates)
        if not hasattr(self, '_last_sprite_update'):
            self._last_sprite_update = 0
        
        current_time = time.time()
        if current_time - self._last_sprite_update > 0.1:  # Update sprites every 100ms
            self.update_sprites()
            self._last_sprite_update = current_time

    def update_sprites(self):
        """ Syncs the sprites with the simulation environment. """
        env = self.simulation.environment
        
        # Calculate adjusted grid position
        grid_bottom = 50
        
        # --- Update Animals ---
        self.animal_sprites.clear()
        for animal in env.get_alive_animals():
            sprite = arcade.Sprite("assets/animal.png", scale=self.cell_size/32)
            sprite.center_x = GRID_START_X + animal.position[0] * self.cell_size + self.cell_size / 2
            sprite.center_y = grid_bottom + animal.position[1] * self.cell_size + self.cell_size / 2
            self.animal_sprites.append(sprite)
            
        # --- Update Food (FIX: Create copy to avoid iteration error) ---
        self.food_sprites.clear()
        try:
            # Create a copy of the set to avoid "Set changed size during iteration" error
            food_positions_copy = list(env.food_positions)
            for pos in food_positions_copy:
                sprite = arcade.Sprite("assets/food.png", scale=self.cell_size/32)
                sprite.center_x = GRID_START_X + pos[0] * self.cell_size + self.cell_size / 2
                sprite.center_y = grid_bottom + pos[1] * self.cell_size + self.cell_size / 2
                self.food_sprites.append(sprite)
        except RuntimeError:
            # If we still get an error, skip this update
            pass
            
        # --- Update Water (FIX: Create copy to avoid iteration error) ---
        self.water_sprites.clear()
        try:
            # Create a copy of the set to avoid "Set changed size during iteration" error
            water_positions_copy = list(env.water_positions)
            for pos in water_positions_copy:
                sprite = arcade.Sprite("assets/water.png", scale=self.cell_size/32)
                sprite.center_x = GRID_START_X + pos[0] * self.cell_size + self.cell_size / 2
                sprite.center_y = grid_bottom + pos[1] * self.cell_size + self.cell_size / 2
                self.water_sprites.append(sprite)
        except RuntimeError:
            # If we still get an error, skip this update
            pass

    def on_draw(self):
        """ Render the screen with modern styling. """
        self.clear()
        
        # --- Draw Background with gradient effect ---
        arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, BACKGROUND_COLOR)
        
        # --- Draw UI Panels with modern styling ---
        # Left panel with border
        arcade.draw_lrtb_rectangle_filled(0, LEFT_PANEL_WIDTH, SCREEN_HEIGHT, 0, PANEL_COLOR)
        arcade.draw_lrtb_rectangle_outline(0, LEFT_PANEL_WIDTH, SCREEN_HEIGHT, 0, PANEL_BORDER_COLOR, 3)
        
        # Right panel with border
        arcade.draw_lrtb_rectangle_filled(
            SCREEN_WIDTH - RIGHT_PANEL_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT, 0, PANEL_COLOR
        )
        arcade.draw_lrtb_rectangle_outline(
            SCREEN_WIDTH - RIGHT_PANEL_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT, 0, PANEL_BORDER_COLOR, 3
        )
        
        # --- Draw Grid Area with modern styling ---
        if self.is_initialized:
            # Position grid in center, avoiding panels
            grid_bottom = 50
            grid_height = min(GRID_HEIGHT_PIXELS, SCREEN_HEIGHT - grid_bottom - 50)
            
            # Grid background with subtle pattern
            arcade.draw_lrtb_rectangle_filled(
                GRID_START_X - 10, GRID_START_X + GRID_WIDTH_PIXELS + 10,
                grid_bottom + grid_height + 10, grid_bottom - 10,
                (45, 52, 61)  # Slightly lighter than background
            )
            
            # Grid border
            arcade.draw_lrtb_rectangle_outline(
                GRID_START_X - 10, GRID_START_X + GRID_WIDTH_PIXELS + 10,
                grid_bottom + grid_height + 10, grid_bottom - 10,
                ACCENT_COLOR, 4
            )
            
            # Grid title
            arcade.draw_text(
                "ECOSYSTEM GRID",
                GRID_START_X + GRID_WIDTH_PIXELS // 2,
                grid_bottom + grid_height + 30,
                ACCENT_COLOR, font_size=20, bold=True,
                anchor_x="center"
            )
            
            # Draw grid lines with subtle styling
            for start, end in self.grid_lines:
                arcade.draw_line(start[0], start[1], end[0], end[1], (100, 100, 100), 1)

            # Draw sprites with enhanced effects
            self.food_sprites.draw()
            self.water_sprites.draw()
            self.animal_sprites.draw()
            
            # --- Draw Statistics with modern styling ---
            stats = self.simulation.get_statistics()
            self.draw_stats_panel(stats)
            
            # Draw right panel content
            self.draw_right_panel()
            
            # Draw animal details panel if visible
            self.draw_animal_details_panel()
        
        # Draw UI manager last
        self.manager.draw()

    def draw_stats_panel(self, stats):
        """ Draw the live statistics on the left panel with modern styling. """
        y_pos = self.height - BOTTOM_PANEL_HEIGHT - 50  # Account for bottom panel
        x_pos = 25
        
        def draw_stat(label, value, y, color=TEXT_COLOR, font_size=13):
            arcade.draw_text(f"{label}: {value}", x_pos, y, color, font_size=font_size, font_name="Arial")

        def draw_section_header(title, y, color):
            # Section background
            arcade.draw_lrtb_rectangle_filled(x_pos - 5, x_pos + 350, y + 20, y - 5, (60, 67, 76))
            arcade.draw_lrtb_rectangle_outline(x_pos - 5, x_pos + 350, y + 20, y - 5, PANEL_BORDER_COLOR, 2)
            # Section title
            arcade.draw_text(title, x_pos, y + 5, color, font_size=16, font_name="Arial", bold=True)

        # Main title with icon
        arcade.draw_text("SIMULATION STATISTICS", x_pos, y_pos + 30, ACCENT_COLOR, font_size=20, font_name="Arial", bold=True)
        
        # Basic Info Section
        draw_section_header("SIMULATION STATUS", y_pos - 20, INFO_COLOR)
        state = stats.get('state', 'N/A').title()
        state_color = SUCCESS_COLOR if state == 'Running' else WARNING_COLOR if state == 'Paused' else DANGER_COLOR
        draw_stat("State", state, y_pos - 45, state_color, 14)
        draw_stat("Generation", stats.get('current_generation', 'N/A'), y_pos - 70)
        draw_stat("Step", stats.get('current_step', 'N/A'), y_pos - 95)
        
        env_stats = stats.get('environment_stats', {})
        pop_stats = stats.get('population_stats', {})
        event_stats = stats.get('event_stats', {})
        
        # Population Section
        draw_section_header("POPULATION", y_pos - 140, SUCCESS_COLOR)
        alive_count = env_stats.get('alive_animals', 0)
        dead_count = env_stats.get('dead_animals', 0)
        draw_stat("Alive Animals", alive_count, y_pos - 165, SUCCESS_COLOR if alive_count > 0 else DANGER_COLOR, 14)
        draw_stat("Dead Animals", dead_count, y_pos - 190, DANGER_COLOR if dead_count > 0 else TEXT_COLOR)
        
        # Resources Section
        draw_section_header("RESOURCES", y_pos - 240, WARNING_COLOR)
        draw_stat("Food Count", env_stats.get('food_count', 'N/A'), y_pos - 265)
        draw_stat("Water Count", env_stats.get('water_count', 'N/A'), y_pos - 290)
        draw_stat("Food Consumed", env_stats.get('total_food_consumed', 'N/A'), y_pos - 315)
        draw_stat("Water Consumed", env_stats.get('total_water_consumed', 'N/A'), y_pos - 340)
        
        # Fitness Section
        draw_section_header("FITNESS", y_pos - 380, (138, 43, 226))  # Purple
        survival_rate = pop_stats.get('survival_rate', 0)
        survival_color = SUCCESS_COLOR if survival_rate > 0.8 else WARNING_COLOR if survival_rate > 0.5 else DANGER_COLOR
        draw_stat("Survival Rate", f"{survival_rate:.1%}", y_pos - 405, survival_color, 14)
        draw_stat("Avg Fitness", f"{pop_stats.get('average_fitness', 0):.2f}", y_pos - 430)
        draw_stat("Best Fitness", f"{pop_stats.get('best_fitness', 0):.2f}", y_pos - 455)
        draw_stat("Worst Fitness", f"{pop_stats.get('worst_fitness', 0):.2f}", y_pos - 480)
        
        # Events Section
        if event_stats.get('active_events', 0) > 0:
            draw_section_header("ACTIVE EVENTS", y_pos - 520, DANGER_COLOR)
            event_names = event_stats.get('event_names', [])
            for i, event_name in enumerate(event_names):
                draw_stat(f"Event {i+1}", event_name.title(), y_pos - 545 - (i * 25), DANGER_COLOR)

    def draw_right_panel(self):
        """ Draw additional information on the right panel with modern styling. """
        x_pos = SCREEN_WIDTH - RIGHT_PANEL_WIDTH + 25
        y_pos = self.height - BOTTOM_PANEL_HEIGHT - 50  # Account for bottom panel
        
        def draw_stat(label, value, y, color=TEXT_COLOR, font_size=13):
            arcade.draw_text(f"{label}: {value}", x_pos, y, color, font_size=font_size, font_name="Arial")

        def draw_section_header(title, y, color):
            # Section background
            arcade.draw_lrtb_rectangle_filled(x_pos - 5, x_pos + 350, y + 20, y - 5, (60, 67, 76))
            arcade.draw_lrtb_rectangle_outline(x_pos - 5, x_pos + 350, y + 20, y - 5, PANEL_BORDER_COLOR, 2)
            # Section title
            arcade.draw_text(title, x_pos, y + 5, color, font_size=16, font_name="Arial", bold=True)

        # Main title with icon
        arcade.draw_text("SIMULATION INFO", x_pos, y_pos + 30, ACCENT_COLOR, font_size=20, font_name="Arial", bold=True)
        
        if self.simulation:
            stats = self.simulation.get_statistics()
            env_stats = stats.get('environment_stats', {})
            
            # Environment Section
            draw_section_header("ENVIRONMENT", y_pos - 20, SUCCESS_COLOR)
            draw_stat("Grid Size", f"{env_stats.get('grid_size', 'N/A')}", y_pos - 45)
            draw_stat("Empty Cells", env_stats.get('empty_cells', 'N/A'), y_pos - 70)
            
            # Performance Section
            draw_section_header("PERFORMANCE", y_pos - 120, WARNING_COLOR)
            draw_stat("Total Steps", stats.get('total_steps', 'N/A'), y_pos - 145)
            draw_stat("Total Generations", stats.get('total_generations', 'N/A'), y_pos - 170)
            speed = stats.get('simulation_speed', 0)
            speed_color = SUCCESS_COLOR if speed > 1.0 else WARNING_COLOR if speed > 0.5 else DANGER_COLOR
            draw_stat("Simulation Speed", f"{speed:.1f}x", y_pos - 195, speed_color, 14)
            
            # Generation History Section
            gen_history = self.simulation.get_generation_history()
            if gen_history:
                draw_section_header("GENERATION HISTORY", y_pos - 250, (138, 43, 226))  # Purple
                recent_gens = gen_history[-3:]  # Show last 3 generations
                for i, gen in enumerate(recent_gens):
                    gen_num = gen.get('generation', 'N/A')
                    pop_stats = gen.get('population_stats', {})
                    survival = pop_stats.get('survival_rate', 0)
                    survival_color = SUCCESS_COLOR if survival > 0.8 else WARNING_COLOR if survival > 0.5 else DANGER_COLOR
                    draw_stat(f"Gen {gen_num}", f"{survival:.1%} survival", y_pos - 275 - (i * 25), survival_color)
            
            # Tips Section
            draw_section_header("TIPS", y_pos - 400, INFO_COLOR)
            arcade.draw_text("• Click animals to inspect", x_pos, y_pos - 425, TEXT_COLOR, font_size=12)
            arcade.draw_text("• Adjust speed for better control", x_pos, y_pos - 445, TEXT_COLOR, font_size=12)
            arcade.draw_text("• Export data for analysis", x_pos, y_pos - 465, TEXT_COLOR, font_size=12)
    
    def draw_animal_details_panel(self):
        """ Draw the animal details panel when an animal is selected. """
        if not self.animal_details_visible or not self.selected_animal:
            return
            
        animal = self.selected_animal
        x_pos = SCREEN_WIDTH - RIGHT_PANEL_WIDTH - ANIMAL_DETAILS_PANEL_WIDTH + 25
        y_pos = self.height - BOTTOM_PANEL_HEIGHT - 50
        
        def draw_detail(label, value, y, color=TEXT_COLOR, font_size=12):
            arcade.draw_text(f"{label}: {value}", x_pos, y, color, font_size=font_size, font_name="Arial")
        
        def draw_section_header(title, y, color):
            # Section background
            arcade.draw_lrtb_rectangle_filled(x_pos - 5, x_pos + 300, y + 20, y - 5, (60, 67, 76))
            arcade.draw_lrtb_rectangle_outline(x_pos - 5, x_pos + 300, y + 20, y - 5, PANEL_BORDER_COLOR, 2)
            # Section title
            arcade.draw_text(title, x_pos, y + 5, color, font_size=14, font_name="Arial", bold=True)
        
        # Main title
        arcade.draw_text("ANIMAL DETAILS", x_pos, y_pos + 30, ACCENT_COLOR, font_size=18, font_name="Arial", bold=True)
        
        # Basic Info Section
        draw_section_header("BASIC INFO", y_pos - 20, INFO_COLOR)
        draw_detail("ID", animal.animal_id[:12] + "...", y_pos - 45)
        draw_detail("Position", f"({animal.position[0]}, {animal.position[1]})", y_pos - 70)
        draw_detail("Generation", animal.generation, y_pos - 95)
        draw_detail("Age", animal.age, y_pos - 120)
        
        # Health Section
        draw_section_header("HEALTH STATUS", y_pos - 160, SUCCESS_COLOR)
        health_color = SUCCESS_COLOR if animal.health > 70 else WARNING_COLOR if animal.health > 30 else DANGER_COLOR
        draw_detail("Health", f"{animal.health:.1f}", y_pos - 185, health_color, 13)
        draw_detail("Hunger", f"{animal.hunger:.1f}", y_pos - 210)
        draw_detail("Thirst", f"{animal.thirst:.1f}", y_pos - 235)
        draw_detail("Energy", f"{animal.energy:.1f}", y_pos - 260)
        
        # Performance Section
        draw_section_header("PERFORMANCE", y_pos - 300, WARNING_COLOR)
        draw_detail("Fitness", f"{animal.fitness:.2f}", y_pos - 325)
        draw_detail("Actions Taken", len(animal.action_history), y_pos - 350)
        draw_detail("Movement Count", animal.movement_count, y_pos - 375)
        
        # Resources Section
        draw_section_header("RESOURCES", y_pos - 420, (138, 43, 226))
        draw_detail("Food Consumed", animal.resource_consumed['food'], y_pos - 445)
        draw_detail("Water Consumed", animal.resource_consumed['water'], y_pos - 470)
        
        # Behavior Section
        draw_section_header("BEHAVIOR", y_pos - 520, INFO_COLOR)
        draw_detail("Move Actions", animal.behavioral_counts['move'], y_pos - 545)
        draw_detail("Eat Actions", animal.behavioral_counts['eat'], y_pos - 570)
        draw_detail("Drink Actions", animal.behavioral_counts['drink'], y_pos - 595)
        draw_detail("Rest Actions", animal.behavioral_counts['rest'], y_pos - 620)

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called when the user presses a mouse button. """
        if not self.is_initialized or not self.simulation:
            return

        # Check if the click was on any animal sprite
        clicked_sprites = arcade.get_sprites_at_point((x, y), self.animal_sprites)
        if clicked_sprites:
            # Find the corresponding animal object in the simulation
            clicked_animal_sprite = clicked_sprites[0]
            # Find the index of the clicked sprite in the sprite list
            try:
                index = self.animal_sprites.sprite_list.index(clicked_animal_sprite)
                alive_animals = self.simulation.environment.get_alive_animals()
                if index < len(alive_animals):
                    animal = alive_animals[index]
                    
                    # Update the info panel with the animal's stats
                    self.selected_animal = animal
                    self.animal_details_visible = True
                    
                    # Create detailed info text
                    info_text = (
                        f"ANIMAL ID: {animal.animal_id[:12]}...\n"
                        f"GENERATION: {animal.generation}\n"
                        f"AGE: {animal.age} steps\n"
                        f"POSITION: ({animal.position[0]}, {animal.position[1]})\n\n"
                        f"HEALTH: {animal.health:.1f} / {animal.max_health}\n"
                        f"HUNGER: {animal.hunger:.1f} / {animal.max_hunger}\n"
                        f"THIRST: {animal.thirst:.1f} / {animal.max_thirst}\n"
                        f"ENERGY: {animal.energy:.1f} / {animal.max_energy}\n\n"
                        f"FITNESS: {animal.fitness:.2f}\n"
                        f"ACTIONS TAKEN: {len(animal.action_history)}\n"
                        f"MOVEMENTS: {animal.movement_count}\n\n"
                        f"RESOURCES CONSUMED:\n"
                        f"  Food: {animal.resource_consumed['food']}\n"
                        f"  Water: {animal.resource_consumed['water']}\n\n"
                        f"BEHAVIOR COUNTS:\n"
                        f"  Move: {animal.behavioral_counts['move']}\n"
                        f"  Eat: {animal.behavioral_counts['eat']}\n"
                        f"  Drink: {animal.behavioral_counts['drink']}\n"
                        f"  Rest: {animal.behavioral_counts['rest']}"
                    )
                    self.selected_animal_info.text = info_text
                    print(f"Selected animal: {animal.animal_id}")
            except (ValueError, IndexError):
                print("Error finding animal for clicked sprite")
        else:
            # Check if click was in grid area but no animal
            grid_bottom = 50
            grid_height = min(GRID_HEIGHT_PIXELS, SCREEN_HEIGHT - grid_bottom - 50)
            
            if (GRID_START_X <= x <= GRID_START_X + GRID_WIDTH_PIXELS and 
                grid_bottom <= y <= grid_bottom + grid_height):
                
                # Convert screen coordinates to grid coordinates
                grid_x = int((x - GRID_START_X) // self.cell_size)
                grid_y = int((y - grid_bottom) // self.cell_size)
                
                # Clear selection
                self.animal_details_visible = False
                self.selected_animal = None
                self.selected_animal_info.text = "Click an animal in the grid to see its detailed statistics and behavior patterns."
                print(f"Clicked at grid position ({grid_x}, {grid_y}) - no animal found")

    def show_animal_details(self, animal):
        """ Show detailed information about a clicked animal. """
        print("\n" + "="*50)
        print(f"ANIMAL DETAILS: {animal.animal_id}")
        print("="*50)
        print(f"Position: {animal.position}")
        print(f"Health: {animal.health:.1f}")
        print(f"Hunger: {animal.hunger:.1f}")
        print(f"Thirst: {animal.thirst:.1f}")
        print(f"Energy: {animal.energy:.1f}")
        print(f"Age: {animal.age}")
        print(f"Fitness: {animal.fitness:.1f}")
        print(f"Alive: {animal.alive}")
        print(f"Generation: {animal.generation}")
        print(f"Actions Taken: {len(animal.action_history)}")
        print(f"Movement Count: {animal.movement_count}")
        print(f"Resources Consumed: {animal.resource_consumed}")
        print(f"Behavioral Counts: {animal.behavioral_counts}")
        
        # Show recent actions
        if animal.recent_actions:
            print(f"Recent Actions: {animal.recent_actions[-5:]}")  # Last 5 actions
        
        # Show learning progress
        learning = animal.get_learning_progress()
        print(f"Learning Progress:")
        print(f"  Survival Rate: {learning['survival_rate']:.1%}")
        print(f"  Resource Efficiency: {learning['resource_efficiency']:.1%}")
        print(f"  Exploration Rate: {learning['exploration_rate']:.1%}")
        print(f"  Adaptation Score: {learning['adaptation_score']:.1%}")
        print("="*50)

    def on_close(self):
        """ Safely close the simulation when the window is closed. """
        if self.simulation:
            self.simulation.stop()
        super().on_close()


def main():
    """ Main method """
    window = SimGame()
    arcade.run()

if __name__ == "__main__":
    main()