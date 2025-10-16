import arcade
from .theme import Theme
from .ui_components import UIButton, UISlider, UICard, UINumericInput
from .constants import DEFAULT_CONFIG

class ConfigPanel:
    def __init__(self, x, y, width, height, window=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.window = window
        self.is_collapsed = False

        # Grid size presets (buttons instead of sliders)
        slider_y = self.y + self.height - 70
        slider_spacing = 50
        padding = 15
        input_width = 80
        input_height = 25
        
        # Grid size preset buttons
        grid_button_y = slider_y
        grid_button_width = 70
        grid_button_spacing = 10
        self.grid_size = DEFAULT_CONFIG["grid_size"]  # Store current grid size
        
        self.grid_10x10_button = UIButton(self.x + padding, grid_button_y, grid_button_width, 30, "10x10", Theme.ACCENT_BLUE, lambda: self.set_grid_size(10, 10))
        self.grid_15x15_button = UIButton(self.x + padding + grid_button_width + grid_button_spacing, grid_button_y, grid_button_width, 30, "15x15", Theme.ACCENT_BLUE, lambda: self.set_grid_size(15, 15))
        self.grid_20x20_button = UIButton(self.x + padding + 2*(grid_button_width + grid_button_spacing), grid_button_y, grid_button_width, 30, "20x20", Theme.ACCENT_BLUE, lambda: self.set_grid_size(20, 20))
        
        # Label for grid size
        arcade.draw_text("Grid Size:", self.x + padding, grid_button_y + 35, Theme.TEXT_SECONDARY, Theme.FONT_BODY, anchor_x="left")
        
        self.grid_buttons = [self.grid_10x10_button, self.grid_15x15_button, self.grid_20x20_button]
        
        self.population_slider = UISlider(self.x + padding, slider_y - 2*slider_spacing, self.width - 2*padding - input_width - 10, 10, 50, DEFAULT_CONFIG["population_size"], "Population")
        self.population_input = UINumericInput(self.x + self.width - padding - input_width, slider_y - 2*slider_spacing - 5, input_width, input_height, DEFAULT_CONFIG["population_size"], 10, 200, "", decimals=0)
        
        self.max_gen_slider = UISlider(self.x + padding, slider_y - 3*slider_spacing, self.width - 2*padding - input_width - 10, 5, 20, DEFAULT_CONFIG.get("max_generations", 10), "Max Generations")
        self.max_gen_input = UINumericInput(self.x + self.width - padding - input_width, slider_y - 3*slider_spacing - 5, input_width, input_height, DEFAULT_CONFIG.get("max_generations", 10), 5, 100, "", decimals=0)
        
        self.steps_per_gen_slider = UISlider(self.x + padding, slider_y - 4*slider_spacing, self.width - 2*padding - input_width - 10, 50, 200, DEFAULT_CONFIG.get("steps_per_generation", 100), "Steps per Gen")
        self.steps_per_gen_input = UINumericInput(self.x + self.width - padding - input_width, slider_y - 4*slider_spacing - 5, input_width, input_height, DEFAULT_CONFIG.get("steps_per_generation", 100), 50, 500, "", decimals=0)
        
        self.food_density_slider = UISlider(self.x + padding, slider_y - 5*slider_spacing, self.width - 2*padding - input_width - 10, 0.05, 0.5, DEFAULT_CONFIG["food_density"], "Food Density")
        self.food_density_input = UINumericInput(self.x + self.width - padding - input_width, slider_y - 5*slider_spacing - 5, input_width, input_height, DEFAULT_CONFIG["food_density"], 0.05, 0.5, "", decimals=2)
        
        self.water_density_slider = UISlider(self.x + padding, slider_y - 6*slider_spacing, self.width - 2*padding - input_width - 10, 0.05, 0.5, DEFAULT_CONFIG["water_density"], "Water Density")
        self.water_density_input = UINumericInput(self.x + self.width - padding - input_width, slider_y - 6*slider_spacing - 5, input_width, input_height, DEFAULT_CONFIG["water_density"], 0.05, 0.5, "", decimals=2)
        
        self.drought_prob_slider = UISlider(self.x + padding, slider_y - 7*slider_spacing, self.width - 2*padding - input_width - 10, 0, 0.5, DEFAULT_CONFIG["drought_probability"], "Drought Prob")
        self.drought_prob_input = UINumericInput(self.x + self.width - padding - input_width, slider_y - 7*slider_spacing - 5, input_width, input_height, DEFAULT_CONFIG["drought_probability"], 0, 0.5, "", decimals=2)
        
        self.storm_prob_slider = UISlider(self.x + padding, slider_y - 8*slider_spacing, self.width - 2*padding - input_width - 10, 0, 0.5, DEFAULT_CONFIG["storm_probability"], "Storm Prob")
        self.storm_prob_input = UINumericInput(self.x + self.width - padding - input_width, slider_y - 8*slider_spacing - 5, input_width, input_height, DEFAULT_CONFIG["storm_probability"], 0, 0.5, "", decimals=2)
        
        self.famine_prob_slider = UISlider(self.x + padding, slider_y - 9*slider_spacing, self.width - 2*padding - input_width - 10, 0, 0.5, DEFAULT_CONFIG["famine_probability"], "Famine Prob")
        self.famine_prob_input = UINumericInput(self.x + self.width - padding - input_width, slider_y - 9*slider_spacing - 5, input_width, input_height, DEFAULT_CONFIG["famine_probability"], 0, 0.5, "", decimals=2)
        
        self.bonus_prob_slider = UISlider(self.x + padding, slider_y - 10*slider_spacing, self.width - 2*padding - input_width - 10, 0, 0.5, DEFAULT_CONFIG["bonus_probability"], "Bonus Prob")
        self.bonus_prob_input = UINumericInput(self.x + self.width - padding - input_width, slider_y - 10*slider_spacing - 5, input_width, input_height, DEFAULT_CONFIG["bonus_probability"], 0, 0.5, "", decimals=2)

        self.sliders = [self.population_slider, self.max_gen_slider, self.steps_per_gen_slider,
                        self.food_density_slider, self.water_density_slider,
                        self.drought_prob_slider, self.storm_prob_slider,
                        self.famine_prob_slider, self.bonus_prob_slider]
        
        self.inputs = [self.population_input, self.max_gen_input, self.steps_per_gen_input,
                       self.food_density_input, self.water_density_input,
                       self.drought_prob_input, self.storm_prob_input,
                       self.famine_prob_input, self.bonus_prob_input]

        # Buttons
        button_y = self.y + 50
        self.apply_button = UIButton(self.x + 10, button_y, 80, 30, "APPLY", Theme.ACCENT_GREEN, self.apply_config)
        self.preset_optimal = UIButton(self.x + 110, button_y, 80, 30, "OPTIMAL", Theme.ACCENT_BLUE, lambda: self.load_preset("optimal"))
        self.preset_default = UIButton(self.x + 210, button_y, 80, 30, "DEFAULT", Theme.ACCENT_BLUE, lambda: self.load_preset("default"))
        self.preset_challenge = UIButton(self.x + 310, button_y, 80, 30, "CHALLENGE", Theme.ACCENT_BLUE, lambda: self.load_preset("challenge"))

        self.buttons = [self.apply_button, self.preset_optimal, self.preset_default, self.preset_challenge]
        self.buttons.extend(self.grid_buttons)  # Add grid size buttons

    def draw(self):
        if self.is_collapsed:
            # Draw collapsed header at the top of the original panel area
            collapsed_height = 40
            header_y = self.y + self.height - collapsed_height/2
            arcade.draw_rectangle_filled(self.x + self.width/2, header_y, self.width, collapsed_height, Theme.PANEL_BG)
            arcade.draw_rectangle_outline(self.x + self.width/2, header_y, self.width, collapsed_height, Theme.BORDER_COLOR, 1)
            arcade.draw_text("▼ Configuration (Click to Expand)", self.x + 15, header_y - 8, Theme.TEXT_PRIMARY, Theme.FONT_BODY, anchor_y="center")
            return

        # Background
        arcade.draw_rectangle_filled(self.x + self.width/2, self.y + self.height/2,
                                     self.width, self.height, Theme.PANEL_BG)
        # Border
        arcade.draw_rectangle_outline(self.x + self.width/2, self.y + self.height/2,
                                      self.width, self.height, Theme.BORDER_COLOR, 1)

        # Title with collapse indicator
        arcade.draw_text("▲ Configuration (Click to Collapse)", self.x + 15, self.y + self.height - 30,
                         Theme.TEXT_PRIMARY, Theme.FONT_HEADER, anchor_x="left", bold=True)

        # Draw grid size label and current selection
        padding = 15
        grid_label_y = self.y + self.height - 70 + 35
        arcade.draw_text(f"Grid Size: {self.grid_size[0]}x{self.grid_size[1]}", 
                         self.x + padding, grid_label_y,
                         Theme.TEXT_SECONDARY, Theme.FONT_BODY, anchor_x="left")

        # Draw sliders and inputs
        for slider, input_field in zip(self.sliders, self.inputs):
            slider.draw()
            input_field.draw()

        # Draw buttons
        for button in self.buttons:
            button.draw()

    def check_hover(self, mouse_x, mouse_y):
        if self.is_collapsed:
            return
        for button in self.buttons:
            button.check_hover(mouse_x, mouse_y)
        for input_field in self.inputs:
            input_field.check_hover(mouse_x, mouse_y)

    def handle_click(self, mouse_x, mouse_y):
        if self.is_collapsed:
            # Toggle expand if clicked on collapsed header (at top of panel area)
            collapsed_height = 40
            header_y_min = self.y + self.height - collapsed_height
            header_y_max = self.y + self.height
            if self.x <= mouse_x <= self.x + self.width and header_y_min <= mouse_y <= header_y_max:
                self.is_collapsed = False
                return True
            return False

        # Check if clicking on buttons first (higher priority)
        for button in self.buttons:
            if button.is_clicked(mouse_x, mouse_y):
                button.execute_callback()
                return True

        # Handle input field clicks
        for input_field in self.inputs:
            if input_field.handle_click(mouse_x, mouse_y):
                return True

        # Check if clicking on sliders (to start dragging)
        for slider in self.sliders:
            handle_x = slider.x + (slider.value - slider.min_val) / (slider.max_val - slider.min_val) * slider.width
            if abs(mouse_x - handle_x) < 15 and abs(mouse_y - slider.y) < 15:
                return True

        # Toggle collapse only if clicked on header area (top 40px)
        if self.x <= mouse_x <= self.x + self.width and self.y + self.height - 40 <= mouse_y <= self.y + self.height:
            self.is_collapsed = True
            return True

        # Check if click is within panel bounds
        if self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height:
            return True
            
        return False

    def handle_drag(self, mouse_x, mouse_y):
        # Handle slider dragging and sync with inputs
        for slider, input_field in zip(self.sliders, self.inputs):
            slider.handle_drag(mouse_x)
            if slider.is_dragging:
                input_field.value = slider.value
                input_field.text = f"{slider.value:.{input_field.decimals}f}"
                return True
        return False

    def handle_key_press(self, key, modifiers):
        # Handle input field key presses
        for input_field in self.inputs:
            if input_field.handle_key_press(key, modifiers):
                # Sync slider with input
                slider_index = self.inputs.index(input_field)
                self.sliders[slider_index].value = input_field.value
                return True
        return False

    def handle_release(self):
        for slider in self.sliders:
            slider.stop_drag()
    
    def set_grid_size(self, width, height):
        """Set grid size from preset buttons"""
        self.grid_size = (width, height)
        print(f"[CONFIG] Grid size set to {width}x{height}")
        # Highlight the selected button
        for button in self.grid_buttons:
            if f"{width}x{height}" in button.text:
                button.color = Theme.ACCENT_GREEN
            else:
                button.color = Theme.ACCENT_BLUE

    def apply_config(self):
        if not self.window:
            return
            
        # Build config dictionary from current values
        config = {
            "grid_size": self.grid_size,  # Use preset grid size
            "population_size": int(self.population_slider.value),
            "max_generations": int(self.max_gen_slider.value),
            "steps_per_generation": int(self.steps_per_gen_slider.value),
            "simulation_speed": self.window.simulation_config.get("simulation_speed", 1.0),
            "day_night_cycle": self.window.simulation_config.get("day_night_cycle", False),
            "seasonal_variations": self.window.simulation_config.get("seasonal_variations", False),
            "food_density": self.food_density_slider.value,
            "water_density": self.water_density_slider.value,
            "drought_probability": self.drought_prob_slider.value,
            "storm_probability": self.storm_prob_slider.value,
            "famine_probability": self.famine_prob_slider.value,
            "bonus_probability": self.bonus_prob_slider.value,
            "mutation_rate": self.window.simulation_config.get("mutation_rate", 0.1),
            "crossover_rate": self.window.simulation_config.get("crossover_rate", 0.8),
            "selection_method": self.window.simulation_config.get("selection_method", "tournament"),
            "tournament_size": self.window.simulation_config.get("tournament_size", 3),
            "elite_percentage": self.window.simulation_config.get("elite_percentage", 0.1)
        }
        
        # Update window config
        self.window.simulation_config = config.copy()
        
        # If simulation is running, show message that changes take effect on reset
        if self.window.simulation and self.window.simulation.is_running():
            print("[CONFIG] Configuration updated. Changes will take effect when simulation is reset.")
        else:
            print("[CONFIG] Configuration updated.")

    def load_preset(self, preset):
        if preset == "default":
            config = DEFAULT_CONFIG.copy()
        elif preset == "optimal":
            config = {
                "grid_size": (20, 20),  # Changed to allowed preset
                "population_size": 30,
                "max_generations": 5,
                "steps_per_generation": 100,
                "simulation_speed": 1.0,
                "day_night_cycle": True,
                "seasonal_variations": True,
                "food_density": 0.2,
                "water_density": 0.2,
                "drought_probability": 0.05,
                "storm_probability": 0.03,
                "famine_probability": 0.08,
                "bonus_probability": 0.1,
                "mutation_rate": 0.05,
                "crossover_rate": 0.9,
                "selection_method": "tournament",
                "tournament_size": 5,
                "elite_percentage": 0.2
            }
        elif preset == "challenge":
            config = {
                "grid_size": (15, 15),
                "population_size": 50,
                "max_generations": 10,
                "steps_per_generation": 100,
                "simulation_speed": 1.0,
                "day_night_cycle": True,
                "seasonal_variations": True,
                "food_density": 0.05,
                "water_density": 0.05,
                "drought_probability": 0.15,
                "storm_probability": 0.1,
                "famine_probability": 0.2,
                "bonus_probability": 0.02,
                "mutation_rate": 0.2,
                "crossover_rate": 0.6,
                "selection_method": "tournament",
                "tournament_size": 2,
                "elite_percentage": 0.05
            }
        else:
            return
            
        # Update grid size using preset method
        self.set_grid_size(config["grid_size"][0], config["grid_size"][1])
        
        # Update sliders and inputs
        self.population_slider.value = config["population_size"]
        self.population_input.value = config["population_size"]
        self.population_input.text = f"{config['population_size']:.0f}"
        
        self.max_gen_slider.value = config["max_generations"]
        self.max_gen_input.value = config["max_generations"]
        self.max_gen_input.text = f"{config['max_generations']:.0f}"
        
        self.steps_per_gen_slider.value = config["steps_per_generation"]
        self.steps_per_gen_input.value = config["steps_per_generation"]
        self.steps_per_gen_input.text = f"{config['steps_per_generation']:.0f}"
        
        self.food_density_slider.value = config["food_density"]
        self.food_density_input.value = config["food_density"]
        self.food_density_input.text = f"{config['food_density']:.2f}"
        
        self.water_density_slider.value = config["water_density"]
        self.water_density_input.value = config["water_density"]
        self.water_density_input.text = f"{config['water_density']:.2f}"
        
        self.drought_prob_slider.value = config["drought_probability"]
        self.drought_prob_input.value = config["drought_probability"]
        self.drought_prob_input.text = f"{config['drought_probability']:.2f}"
        
        self.storm_prob_slider.value = config["storm_probability"]
        self.storm_prob_input.value = config["storm_probability"]
        self.storm_prob_input.text = f"{config['storm_probability']:.2f}"
        
        self.famine_prob_slider.value = config["famine_probability"]
        self.famine_prob_input.value = config["famine_probability"]
        self.famine_prob_input.text = f"{config['famine_probability']:.2f}"
        
        self.bonus_prob_slider.value = config["bonus_probability"]
        self.bonus_prob_input.value = config["bonus_probability"]
        self.bonus_prob_input.text = f"{config['bonus_probability']:.2f}"
        
        # Update window config
        self.window.simulation_config = config.copy()
        print(f"[CONFIG] Loaded {preset} preset")

