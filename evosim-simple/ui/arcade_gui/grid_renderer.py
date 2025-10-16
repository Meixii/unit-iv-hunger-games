import arcade
import random
from .theme import Theme

class GridRenderer:
    def __init__(self, x, y, width, height, sprite_manager, animation_manager):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprite_manager = sprite_manager
        self.animation_manager = animation_manager
        self.selected_animal = None
        self.simulation = None  # Will be set when drawing

    def draw(self, simulation, generation, step, events, fps):
        if not simulation or not simulation.environment:
            return

        self.simulation = simulation
        env = simulation.environment
        
        # Draw border around grid
        arcade.draw_rectangle_outline(self.x + self.width/2, self.y + self.height/2,
                                      self.width, self.height, Theme.BORDER_COLOR, 2)
        
        self.draw_grid_background(env)
        self.draw_resources(env.food_positions, env.water_positions)
        self.draw_animals(env.animals)
        self.draw_event_effects(events)
        self.draw_overlays(generation, step, events, fps)

    def draw_grid_background(self, environment):
        # Draw base background (darker green)
        arcade.draw_rectangle_filled(self.x + self.width/2, self.y + self.height/2,
                                     self.width, self.height, (34, 139, 34))  # Forest green
        
        # Draw grass tiles
        texture = self.sprite_manager.get_grass_texture()
        for y in range(environment.height):
            for x in range(environment.width):
                world_x = self.x + x * self.sprite_manager.cell_size
                world_y = self.y + (environment.height - y - 1) * self.sprite_manager.cell_size
                arcade.draw_texture_rectangle(world_x + self.sprite_manager.cell_size // 2,
                                              world_y + self.sprite_manager.cell_size // 2,
                                              self.sprite_manager.cell_size, self.sprite_manager.cell_size,
                                              texture)
        
        # Draw grid lines for better visibility
        grid_color = (40, 100, 40, 100)  # Semi-transparent dark green
        # Vertical lines
        for x in range(environment.width + 1):
            line_x = self.x + x * self.sprite_manager.cell_size
            arcade.draw_line(line_x, self.y, line_x, self.y + self.height, grid_color, 1)
        # Horizontal lines
        for y in range(environment.height + 1):
            line_y = self.y + y * self.sprite_manager.cell_size
            arcade.draw_line(self.x, line_y, self.x + self.width, line_y, grid_color, 1)

    def draw_resources(self, food_positions, water_positions):
        # Create copies to avoid RuntimeError: Set changed size during iteration
        food_pos_copy = list(food_positions) if food_positions else []
        water_pos_copy = list(water_positions) if water_positions else []
        
        if not self.simulation or not self.simulation.environment:
            return
        
        env_height = self.simulation.environment.height
        
        # Draw food
        for pos in food_pos_copy:
            x, y = pos
            world_x = self.x + x * self.sprite_manager.cell_size + self.sprite_manager.cell_size // 2
            world_y = self.y + (env_height - y - 1) * self.sprite_manager.cell_size + self.sprite_manager.cell_size // 2
            sprite = self.sprite_manager.get_resource_sprite("food")
            sprite.center_x = world_x
            sprite.center_y = world_y
            sprite.draw()

        # Draw water
        for pos in water_pos_copy:
            x, y = pos
            world_x = self.x + x * self.sprite_manager.cell_size + self.sprite_manager.cell_size // 2
            world_y = self.y + (env_height - y - 1) * self.sprite_manager.cell_size + self.sprite_manager.cell_size // 2
            sprite = self.sprite_manager.get_resource_sprite("water")
            sprite.center_x = world_x
            sprite.center_y = world_y
            sprite.draw()

    def draw_animals(self, animals):
        # Create copy to avoid RuntimeError: Set changed size during iteration
        animals_copy = list(animals) if animals else []
        
        if not self.simulation or not self.simulation.environment:
            return
        
        env_height = self.simulation.environment.height
        
        for animal in animals_copy:
            if animal.alive:
                x, y = animal.position
                world_x = self.x + x * self.sprite_manager.cell_size + self.sprite_manager.cell_size // 2
                world_y = self.y + (env_height - y - 1) * self.sprite_manager.cell_size + self.sprite_manager.cell_size // 2
                sprite = self.sprite_manager.get_animal_sprite(animal)
                sprite.center_x = world_x
                sprite.center_y = world_y
                sprite.draw()

    def draw_overlays(self, generation, step, events, fps):
        # Compact info panel at top-left with generation, step, and legend
        info_width = self.width - 120  # Span most of the top
        info_height = 60
        info_x = self.x + 10
        info_y = self.y + self.height - 70
        
        # Draw info background
        arcade.draw_rectangle_filled(info_x + info_width/2, info_y + info_height/2,
                                     info_width, info_height, (46, 52, 64, 220))
        arcade.draw_rectangle_outline(info_x + info_width/2, info_y + info_height/2,
                                      info_width, info_height, Theme.BORDER_COLOR, 1)
        
        # Generation and step text (left side)
        arcade.draw_text(f"Gen: {generation}", info_x + 10, info_y + 35,
                         Theme.TEXT_PRIMARY, Theme.FONT_BODY, anchor_x="left", bold=True)
        arcade.draw_text(f"Step: {step}", info_x + 10, info_y + 10,
                         Theme.TEXT_SECONDARY, Theme.FONT_BODY, anchor_x="left")
        
        # Compact legend (right side of info panel)
        legend_x = info_x + 120
        legend_y = info_y + 23
        
        arcade.draw_text("Legend: ", legend_x, legend_y,
                         Theme.TEXT_PRIMARY, Theme.FONT_SMALL, anchor_x="left", bold=True)
        
        # Animal indicator
        legend_x += 55
        arcade.draw_circle_filled(legend_x, legend_y + 5, 5, (255, 85, 85))
        arcade.draw_text("Animal", legend_x + 10, legend_y,
                         Theme.TEXT_SECONDARY, Theme.FONT_SMALL, anchor_x="left")
        
        # Food indicator
        legend_x += 70
        arcade.draw_rectangle_filled(legend_x, legend_y + 5, 8, 8, (255, 165, 0))
        arcade.draw_text("Food", legend_x + 10, legend_y,
                         Theme.TEXT_SECONDARY, Theme.FONT_SMALL, anchor_x="left")
        
        # Water indicator
        legend_x += 60
        arcade.draw_rectangle_filled(legend_x, legend_y + 5, 8, 8, (0, 191, 255))
        arcade.draw_text("Water", legend_x + 10, legend_y,
                         Theme.TEXT_SECONDARY, Theme.FONT_SMALL, anchor_x="left")
        
        # Grass/Empty indicator
        legend_x += 65
        arcade.draw_rectangle_filled(legend_x, legend_y + 5, 8, 8, (34, 139, 34))
        arcade.draw_text("Grass/Empty", legend_x + 10, legend_y,
                         Theme.TEXT_SECONDARY, Theme.FONT_SMALL, anchor_x="left")
        
        # Active events (centered at top)
        if events:
            event_text = " | ".join([e.upper() for e in events])
            # Event banner
            arcade.draw_rectangle_filled(self.x + self.width/2, self.y + self.height - 20,
                                         len(event_text) * 10 + 40, 30, (208, 135, 112, 220))  # Orange with alpha
            arcade.draw_text(event_text, self.x + self.width // 2, self.y + self.height - 25,
                             Theme.TEXT_PRIMARY, Theme.FONT_BODY, anchor_x="center", bold=True)
        
        # FPS counter (bottom-right with background)
        fps_text = f"FPS: {fps:.1f}"
        arcade.draw_rectangle_filled(self.x + self.width - 50, self.y + 20,
                                     80, 30, (46, 52, 64, 200))
        arcade.draw_text(fps_text, self.x + self.width - 15, self.y + 15,
                         Theme.ACCENT_GREEN if fps > 30 else Theme.ACCENT_ORANGE, 
                         Theme.FONT_BODY, anchor_x="right", bold=True)

    def draw_legend_old(self):
        # Legend panel dimensions - positioned at top-left below gen info
        legend_width = 180
        legend_height = 140
        legend_x = self.x + 10
        legend_y = self.y + self.height - 180  # Below the gen/step info panel
        
        # Draw legend background
        arcade.draw_rectangle_filled(legend_x + legend_width/2, legend_y + legend_height/2,
                                     legend_width, legend_height, (46, 52, 64, 220))
        arcade.draw_rectangle_outline(legend_x + legend_width/2, legend_y + legend_height/2,
                                      legend_width, legend_height, Theme.BORDER_COLOR, 1)
        
        # Title
        arcade.draw_text("Legend", legend_x + 10, legend_y + legend_height - 20,
                         Theme.TEXT_PRIMARY, Theme.FONT_BODY, anchor_x="left", bold=True)
        
        # Legend items
        item_y = legend_y + legend_height - 45
        item_spacing = 25
        
        # Animals (show color variations)
        colors = [(255, 85, 85), (189, 147, 249), (241, 250, 140), (139, 233, 253), (255, 121, 198)]
        arcade.draw_circle_filled(legend_x + 20, item_y, 8, colors[0])
        arcade.draw_text("Animals (various colors)", legend_x + 35, item_y - 5,
                         Theme.TEXT_SECONDARY, Theme.FONT_SMALL, anchor_x="left")
        
        item_y -= item_spacing
        # Food
        arcade.draw_circle_filled(legend_x + 20, item_y, 8, (255, 184, 108))
        arcade.draw_text("Food", legend_x + 35, item_y - 5,
                         Theme.TEXT_SECONDARY, Theme.FONT_SMALL, anchor_x="left")
        
        item_y -= item_spacing
        # Water
        arcade.draw_circle_filled(legend_x + 20, item_y, 8, (139, 233, 253))
        arcade.draw_text("Water", legend_x + 35, item_y - 5,
                         Theme.TEXT_SECONDARY, Theme.FONT_SMALL, anchor_x="left")
        
        item_y -= item_spacing
        # Grass
        arcade.draw_rectangle_filled(legend_x + 20, item_y, 16, 16, (50, 168, 82))
        arcade.draw_text("Grass/Empty", legend_x + 35, item_y - 5,
                         Theme.TEXT_SECONDARY, Theme.FONT_SMALL, anchor_x="left")

    def draw_event_effects(self, active_events):
        # Visual effects for active events
        if 'drought' in active_events:
            # Brown tint overlay
            arcade.draw_rectangle_filled(self.x + self.width/2, self.y + self.height/2,
                                         self.width, self.height, (139, 69, 19, 100))  # Brown with alpha
        if 'storm' in active_events:
            # Rain effect - simple lines
            for _ in range(20):
                x = self.x + random.randint(0, int(self.width))
                y_start = self.y + self.height
                y_end = self.y
                arcade.draw_line(x, y_start, x, y_end, arcade.color.BLUE, 1)

    def update_animations(self, delta_time):
        # Update smooth animations
        pass

    def handle_click(self, x, y):
        # Handle animal selection
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            if not self.simulation or not self.simulation.environment:
                return None
            env = self.simulation.environment
            grid_x = int((x - self.x) / self.sprite_manager.cell_size)
            grid_y = env.height - 1 - int((y - self.y) / self.sprite_manager.cell_size)  # Flip y
            # Find animal at position
            for animal in env.animals:
                if animal.position == (grid_x, grid_y) and animal.alive:
                    self.selected_animal = animal
                    return animal
        self.selected_animal = None
        return None
