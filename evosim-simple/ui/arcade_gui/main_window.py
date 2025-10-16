import arcade
import time
from .theme import Theme
from .constants import get_layout, DEFAULT_CONFIG, RESOLUTIONS
from .sprite_manager import SpriteManager
from .grid_renderer import GridRenderer
from .tab_panel import TabPanel
from .animal_inspector import AnimalInspector
from .animation_effects import AnimationManager

# Import simulation classes
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.simulation import Simulation

class EvolutionSimulationWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.width = width
        self.height = height
        self.resolution_preset = "1366x768" if width == 1366 else "1024x768" if width == 1024 else "1920x1080"
        self.layout = get_layout(self.resolution_preset)
        self.cell_size = self.layout["cell_size"]

        # Components
        self.sprite_manager = None
        self.grid_renderer = None
        
        # End-of-simulation feedback
        self.show_end_dialog = False
        self.end_dialog_data = None
        
        # Right panel scrolling
        self.panel_scroll_offset = 0
        self.max_scroll_offset = 0
        
        self.tab_panel = None
        self.animal_inspector = None
        self.animation_manager = None

        # Simulation state
        self.simulation = None
        self.is_running = False
        self.is_paused = False
        self.speed = 1.0
        self.simulation_config = DEFAULT_CONFIG.copy()

        # UI state
        self.mouse_x = 0
        self.mouse_y = 0
        self.last_fps_time = time.time()
        self.frame_count = 0
        self.fps = 0

        # Stats data
        self.current_stats = {}

    def setup(self):
        arcade.set_background_color(Theme.BACKGROUND)
        self.sprite_manager = SpriteManager(self.cell_size)
        self.animation_manager = AnimationManager()

        # Initialize tabbed panel for right side
        panel_x = self.layout["panel"]["x"]
        panel_y = self.layout["panel"]["y"]
        panel_width = self.layout["panel"]["width"]
        panel_height = self.layout["panel"]["height"]

        self.tab_panel = TabPanel(panel_x, panel_y, panel_width, panel_height, self)

        # Grid renderer
        self.grid_renderer = GridRenderer(self.layout["grid"]["x"], self.layout["grid"]["y"],
                                          self.layout["grid"]["width"], self.layout["grid"]["height"],
                                          self.sprite_manager, self.animation_manager)

        # Animal inspector (overlay, initially hidden)
        self.animal_inspector = AnimalInspector(panel_x + 50, panel_y + 50, 300, 400, self)

        # Initialize simulation
        self.initialize_simulation()

    def initialize_simulation(self):
        self.simulation = Simulation(self.simulation_config)
        self.simulation.add_step_callback(self.on_simulation_step)
        self.simulation.add_generation_callback(self.on_simulation_generation)
        self.simulation.add_state_change_callback(self.on_simulation_state_change)
        self.simulation.initialize()

    def on_simulation_step(self, step_stats):
        self.current_stats.update(step_stats)
        # Update stats panel through tab panel
        if hasattr(self.tab_panel, 'stats_panel'):
            self.tab_panel.stats_panel.update_data(self.current_stats)
        # Trigger animations based on actions
        # Placeholder: could check for eating/drinking events

    def on_simulation_generation(self, gen_stats):
        self.current_stats.update(gen_stats)
        
        # Check if simulation has ended
        if self.simulation and self.simulation.current_generation >= self.simulation.config.get("max_generations", 10):
            self.show_end_of_simulation_feedback()

    def on_simulation_state_change(self, old_state, new_state):
        print(f"Simulation state changed: {old_state.value} -> {new_state.value}")
        
    def show_end_of_simulation_feedback(self):
        """Display end-of-simulation summary dialog"""
        if not self.simulation:
            return
            
        # Gather final statistics
        final_stats = {
            "total_generations": self.simulation.current_generation,
            "final_population": len([a for a in self.simulation.environment.animals if a.alive]),
            "initial_population": self.simulation_config.get("population_size", 50),
            "total_deaths": self.current_stats.get("total_deaths", 0),
            "total_births": self.current_stats.get("total_births", 0),
            "avg_fitness": self.current_stats.get("avg_fitness", 0),
            "best_fitness": self.current_stats.get("best_fitness", 0),
            "total_food_consumed": self.current_stats.get("total_food_consumed", 0),
            "total_water_consumed": self.current_stats.get("total_water_consumed", 0),
        }
        
        self.end_dialog_data = final_stats
        self.show_end_dialog = True
        print("[SIMULATION] End of simulation reached - showing feedback dialog")
    
    def draw_end_dialog(self):
        """Draw the end-of-simulation feedback dialog"""
        # Semi-transparent overlay
        arcade.draw_rectangle_filled(self.width/2, self.height/2,
                                     self.width, self.height, (0, 0, 0, 180))
        
        # Dialog box
        dialog_width = 600
        dialog_height = 500
        dialog_x = self.width/2
        dialog_y = self.height/2
        
        # Background
        arcade.draw_rectangle_filled(dialog_x, dialog_y, dialog_width, dialog_height,
                                     Theme.PANEL_BG)
        arcade.draw_rectangle_outline(dialog_x, dialog_y, dialog_width, dialog_height,
                                      Theme.ACCENT_BLUE, 3)
        
        # Title
        arcade.draw_text("Simulation Complete!", dialog_x, dialog_y + 220,
                         Theme.TEXT_PRIMARY, 24, anchor_x="center", bold=True)
        
        # Statistics
        stats = self.end_dialog_data
        y_offset = dialog_y + 160
        line_spacing = 35
        
        # Population survival rate
        survival_rate = (stats["final_population"] / stats["initial_population"] * 100) if stats["initial_population"] > 0 else 0
        
        arcade.draw_text(f"Generations Completed: {stats['total_generations']}", 
                         dialog_x, y_offset, Theme.TEXT_PRIMARY, 16, anchor_x="center")
        y_offset -= line_spacing
        
        arcade.draw_text(f"Population: {stats['initial_population']} → {stats['final_population']} ({survival_rate:.1f}% survival)",
                         dialog_x, y_offset, Theme.TEXT_PRIMARY, 16, anchor_x="center")
        y_offset -= line_spacing
        
        arcade.draw_text(f"Total Deaths: {stats['total_deaths']}  |  Total Births: {stats['total_births']}",
                         dialog_x, y_offset, Theme.TEXT_SECONDARY, 14, anchor_x="center")
        y_offset -= line_spacing * 1.5
        
        arcade.draw_text(f"Average Fitness: {stats['avg_fitness']:.2f}",
                         dialog_x, y_offset, Theme.ACCENT_GREEN, 16, anchor_x="center")
        y_offset -= line_spacing
        
        arcade.draw_text(f"Best Fitness: {stats['best_fitness']:.2f}",
                         dialog_x, y_offset, Theme.ACCENT_BLUE, 16, anchor_x="center")
        y_offset -= line_spacing * 1.5
        
        arcade.draw_text(f"Food Consumed: {stats['total_food_consumed']}",
                         dialog_x, y_offset, Theme.TEXT_SECONDARY, 14, anchor_x="center")
        y_offset -= line_spacing
        
        arcade.draw_text(f"Water Consumed: {stats['total_water_consumed']}",
                         dialog_x, y_offset, Theme.TEXT_SECONDARY, 14, anchor_x="center")
        
        # Close button
        button_width = 200
        button_height = 50
        button_y = dialog_y - 200
        
        arcade.draw_rectangle_filled(dialog_x, button_y, button_width, button_height,
                                     Theme.ACCENT_GREEN)
        arcade.draw_rectangle_outline(dialog_x, button_y, button_width, button_height,
                                      Theme.TEXT_PRIMARY, 2)
        arcade.draw_text("CLOSE", dialog_x, button_y - 8,
                         Theme.TEXT_PRIMARY, 18, anchor_x="center", bold=True)

    def on_draw(self):
        arcade.start_render()

        # Calculate FPS
        self.frame_count += 1
        current_time = time.time()
        if current_time - self.last_fps_time >= 1.0:
            self.fps = self.frame_count / (current_time - self.last_fps_time)
            self.frame_count = 0
            self.last_fps_time = current_time

        self.grid_renderer.draw(self.simulation, self.simulation.current_generation if self.simulation else 0,
                                self.simulation.current_step if self.simulation else 0,
                                self.current_stats.get('event_names', []), self.fps)
        self.tab_panel.draw(self.current_stats)
        if self.grid_renderer.selected_animal:
            self.animal_inspector.draw(self.grid_renderer.selected_animal)
        self.animation_manager.draw_all()
        
        # Draw end-of-simulation dialog if active
        if self.show_end_dialog and self.end_dialog_data:
            self.draw_end_dialog()

    def on_update(self, delta_time):
        if self.is_running and not self.is_paused and self.simulation:
            # Run simulation step
            pass  # Simulation runs in its own thread
        self.animation_manager.update_all(delta_time)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y
        self.tab_panel.check_hover(x, y)
        if self.grid_renderer.selected_animal:
            self.animal_inspector.export_button.check_hover(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Check if clicking on end dialog close button
            if self.show_end_dialog:
                dialog_x = self.width/2
                dialog_y = self.height/2
                button_y = dialog_y - 200
                button_width = 200
                button_height = 50
                
                if (dialog_x - button_width/2 <= x <= dialog_x + button_width/2 and
                    button_y - button_height/2 <= y <= button_y + button_height/2):
                    self.show_end_dialog = False
                    self.end_dialog_data = None
                    return
                # Block clicks to underlying UI when dialog is open
                return
            
            # Start slider drag in active tab
            self.tab_panel.start_slider_drag(x, y)
            
            # Check tab panel click
            if self.tab_panel.handle_click(x, y):
                return
            if self.grid_renderer.handle_click(x, y):
                if self.grid_renderer.selected_animal:
                    self.animal_inspector.set_selected_animal(self.grid_renderer.selected_animal)
                return
            if self.grid_renderer.selected_animal and self.animal_inspector.handle_click(x, y):
                return

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.tab_panel.handle_release()

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & arcade.MOUSE_BUTTON_LEFT:
            # Handle tab panel slider dragging
            self.tab_panel.handle_drag(x, y)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # Check if mouse is over right panel
        panel_x = self.layout["panel"]["x"]
        panel_width = self.layout["panel"]["width"]
        
        if panel_x <= x <= panel_x + panel_width:
            # Forward scroll to tab panel (for stats tab)
            self.tab_panel.handle_scroll(scroll_y)

    def on_key_press(self, key, modifiers):
        # Close end dialog with ESC
        if key == arcade.key.ESCAPE and self.show_end_dialog:
            self.show_end_dialog = False
            self.end_dialog_data = None
            return
        
        # First check if tab panel needs the key press (for numeric inputs in config tab)
        if self.tab_panel.handle_key_press(key, modifiers):
            return
        
        # Fullscreen toggle
        if key == arcade.key.F11:
            self.set_fullscreen(not self.fullscreen)
            return
            
        if key == arcade.key.SPACE:
            self.toggle_pause()
        elif key == arcade.key.R:
            self.reset_simulation()
        elif key == arcade.key.S:
            self.stop_simulation()
        elif key == arcade.key.NUM_1:
            self.change_resolution("1920x1080")
        elif key == arcade.key.NUM_2:
            self.change_resolution("1366x768")
        elif key == arcade.key.NUM_3:
            self.change_resolution("1024x768")
        elif key == arcade.key.PLUS or key == arcade.key.EQUAL:
            self.speed = min(10.0, self.speed + 0.1)
            if self.simulation:
                self.simulation.set_simulation_speed(self.speed)
        elif key == arcade.key.MINUS:
            self.speed = max(0.1, self.speed - 0.1)
            if self.simulation:
                self.simulation.set_simulation_speed(self.speed)

    def toggle_pause(self):
        if self.simulation:
            if self.simulation.is_running():
                self.simulation.pause()
                self.is_paused = True
            elif self.simulation.is_paused():
                self.simulation.resume()
                self.is_paused = False

    def reset_simulation(self):
        if self.simulation:
            self.simulation.reset()
            # Reset generation counter to 0 for display
            self.simulation.current_generation = 0
            # Reset step counter to 0 for display
            self.simulation.current_step = 0
            self.is_running = False
            self.is_paused = False
            self.current_stats = {}
            print("[RESET] Simulation reset - generation and step counters cleared")

    def stop_simulation(self):
        if self.simulation:
            self.simulation.stop()
            self.is_running = False
            self.is_paused = False

    def change_resolution(self, preset):
        if preset in RESOLUTIONS:
            width, height, cell_size = RESOLUTIONS[preset]
            self.set_size(width, height)
            self.width = width
            self.height = height
            self.resolution_preset = preset
            self.layout = get_layout(preset)
            self.cell_size = cell_size
            self.sprite_manager.scale_sprites(cell_size)
            # Reinitialize panels with new layout
            self.setup()
