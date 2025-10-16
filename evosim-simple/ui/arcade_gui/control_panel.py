import arcade
import os
from .theme import Theme
from .ui_components import UIButton, UISlider, UICard

class ControlPanel:
    def __init__(self, x, y, width, height, window):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.window = window

        # Create buttons with proper spacing
        padding = 15
        button_width = 90
        button_height = 35
        button_spacing = 10
        button_y = self.y + self.height - 60

        self.start_button = UIButton(self.x + padding, button_y, button_width, button_height,
                                     "START", Theme.ACCENT_GREEN, self.start_simulation)
        self.pause_button = UIButton(self.x + padding + button_width + button_spacing, button_y, button_width, button_height,
                                     "PAUSE", Theme.ACCENT_ORANGE, self.pause_simulation)
        self.stop_button = UIButton(self.x + padding + 2*(button_width + button_spacing), button_y, button_width, button_height,
                                    "STOP", Theme.ACCENT_RED, self.stop_simulation)
        self.reset_button = UIButton(self.x + padding + 3*(button_width + button_spacing), button_y, button_width, button_height,
                                     "RESET", Theme.TEXT_SECONDARY, self.reset_simulation)

        # Speed slider with proper spacing and callback
        self.speed_slider = UISlider(self.x + padding, button_y - 70, self.width - 2*padding, 0.1, 10.0, 1.0, "Speed", self.on_speed_change)

        # Event trigger buttons with proper spacing
        event_y = button_y - 140
        event_button_width = 85
        event_spacing = 8
        self.drought_button = UIButton(self.x + padding, event_y, event_button_width, 28, "DROUGHT", Theme.ACCENT_ORANGE, self.trigger_drought)
        self.storm_button = UIButton(self.x + padding + event_button_width + event_spacing, event_y, event_button_width, 28, "STORM", Theme.ACCENT_BLUE, self.trigger_storm)
        self.famine_button = UIButton(self.x + padding + 2*(event_button_width + event_spacing), event_y, event_button_width, 28, "FAMINE", Theme.ACCENT_ORANGE, self.trigger_famine)
        self.bonus_button = UIButton(self.x + padding + 3*(event_button_width + event_spacing), event_y, event_button_width, 28, "BONUS", Theme.ACCENT_GREEN, self.trigger_bonus)

        self.buttons = [self.start_button, self.pause_button, self.stop_button, self.reset_button,
                        self.drought_button, self.storm_button, self.famine_button, self.bonus_button]

        # Bottom action buttons - positioned higher to ensure visibility
        bottom_y = self.y + 80  # Moved up from 40 to 80
        self.view_charts_button = UIButton(self.x + 10, bottom_y, 100, 25, "VIEW CHARTS", Theme.ACCENT_BLUE, self.view_charts)
        self.export_data_button = UIButton(self.x + 120, bottom_y, 100, 25, "EXPORT DATA", Theme.ACCENT_BLUE, self.export_data)
        self.export_animals_button = UIButton(self.x + 230, bottom_y, 110, 25, "EXPORT ANIMALS", Theme.ACCENT_BLUE, self.export_animals)
        self.screenshot_button = UIButton(self.x + 10, bottom_y - 35, 100, 25, "SCREENSHOT", Theme.ACCENT_BLUE, self.take_screenshot)
        self.settings_button = UIButton(self.x + 120, bottom_y - 35, 100, 25, "SETTINGS", Theme.ACCENT_BLUE, self.open_settings)

        self.bottom_buttons = [self.view_charts_button, self.export_data_button, self.export_animals_button,
                               self.screenshot_button, self.settings_button]

        self.buttons.extend(self.bottom_buttons)

    def draw(self):
        # Background
        arcade.draw_rectangle_filled(self.x + self.width/2, self.y + self.height/2,
                                     self.width, self.height, Theme.PANEL_BG)
        # Border
        arcade.draw_rectangle_outline(self.x + self.width/2, self.y + self.height/2,
                                      self.width, self.height, Theme.BORDER_COLOR, 1)
        
        # Header
        arcade.draw_text("Controls", self.x + 15, self.y + self.height - 30,
                         Theme.TEXT_PRIMARY, Theme.FONT_HEADER, anchor_x="left", bold=True)

        # Draw buttons
        for button in self.buttons:
            button.draw()

        # Draw speed slider
        self.speed_slider.draw()

    def check_hover(self, mouse_x, mouse_y):
        for button in self.buttons:
            button.check_hover(mouse_x, mouse_y)

    def handle_click(self, mouse_x, mouse_y):
        for button in self.buttons:
            if button.is_clicked(mouse_x, mouse_y):
                button.execute_callback()
                return True
        return False

    def handle_drag(self, mouse_x, mouse_y):
        # Handle speed slider drag
        pass

    # Button callbacks
    def start_simulation(self):
        if self.window.simulation and not self.window.is_running:
            self.window.simulation.start()
            self.window.is_running = True
            self.window.is_paused = False
            print("[GUI] Simulation started")

    def pause_simulation(self):
        self.window.toggle_pause()

    def stop_simulation(self):
        self.window.stop_simulation()

    def reset_simulation(self):
        self.window.reset_simulation()
    
    def on_speed_change(self, new_speed):
        """Callback when speed slider changes"""
        if self.window.simulation:
            self.window.simulation.set_simulation_speed(new_speed)
            self.window.speed = new_speed
            print(f"[SPEED] Simulation speed set to {new_speed:.2f}x")

    def trigger_drought(self):
        if self.window.simulation and self.window.simulation.event_manager:
            self.window.simulation.event_manager.trigger_event("drought")

    def trigger_storm(self):
        if self.window.simulation and self.window.simulation.event_manager:
            self.window.simulation.event_manager.trigger_event("storm")

    def trigger_famine(self):
        if self.window.simulation and self.window.simulation.event_manager:
            self.window.simulation.event_manager.trigger_event("famine")

    def trigger_bonus(self):
        if self.window.simulation and self.window.simulation.event_manager:
            self.window.simulation.event_manager.trigger_event("bonus")

    # Bottom action button callbacks
    def view_charts(self):
        # Open matplotlib charts window
        if self.window.simulation:
            # Import here to avoid circular import
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
            from analysis.visualization import SimulationVisualizer
            visualizer = SimulationVisualizer(self.window.simulation.get_generation_history())
            visualizer.show()  # Assuming it has a show method

    def export_data(self):
        if self.window.simulation:
            import json
            data = {
                'generation_history': self.window.simulation.get_generation_history(),
                'final_animal_stats': self.window.simulation.get_final_animal_statistics()
            }
            with open('simulation_data.json', 'w') as f:
                json.dump(data, f, indent=2)
            print("Data exported to simulation_data.json")

    def export_animals(self):
        if self.window.simulation:
            animal_ids = self.window.simulation.get_available_animal_ids()
            for animal_id in animal_ids:
                self.window.simulation.export_animal_history(animal_id)
            print("Animal histories exported")

    def take_screenshot(self):
        # Take screenshot of grid area
        # Arcade has arcade.get_image() but for simplicity, print message
        print("Screenshot functionality not implemented yet")

    def open_settings(self):
        # Toggle settings panel or something
        print("Settings: Use 1-3 for resolution")
