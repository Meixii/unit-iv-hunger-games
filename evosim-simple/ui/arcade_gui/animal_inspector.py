import arcade
from .theme import Theme
from .ui_components import UIButton

class AnimalInspector:
    def __init__(self, x, y, width, height, window):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.window = window
        self.selected_animal = None

        # Export button
        self.export_button = UIButton(self.x + self.width - 90, self.y + self.height - 40,
                                      80, 30, "EXPORT", Theme.ACCENT_BLUE, self.export_animal_data)

    def draw(self, animal):
        if not animal:
            # Draw placeholder
            arcade.draw_rectangle_filled(self.x + self.width/2, self.y + self.height/2,
                                         self.width, self.height, Theme.CARD_BG)
            arcade.draw_text("Click an animal to inspect", self.x + self.width/2, self.y + self.height/2,
                             Theme.TEXT_SECONDARY, Theme.FONT_BODY, anchor_x="center", anchor_y="center")
            return

        # Background
        arcade.draw_rectangle_filled(self.x + self.width/2, self.y + self.height/2,
                                     self.width, self.height, Theme.CARD_BG)

        # Title
        arcade.draw_text(f"Animal {animal.animal_id}", self.x + 10, self.y + self.height - 20,
                         Theme.TEXT_PRIMARY, Theme.FONT_HEADER)

        # Stats
        stat_y = self.y + self.height - 50
        arcade.draw_text(f"Hunger: {animal.hunger:.2f}", self.x + 10, stat_y, Theme.TEXT_PRIMARY, Theme.FONT_BODY)
        arcade.draw_text(f"Thirst: {animal.thirst:.2f}", self.x + 10, stat_y - 20, Theme.TEXT_PRIMARY, Theme.FONT_BODY)
        arcade.draw_text(f"Energy: {animal.energy:.2f}", self.x + 10, stat_y - 40, Theme.TEXT_PRIMARY, Theme.FONT_BODY)
        arcade.draw_text(f"Health: {animal.health:.2f}", self.x + 10, stat_y - 60, Theme.TEXT_PRIMARY, Theme.FONT_BODY)
        arcade.draw_text(f"Age: {animal.age}", self.x + 10, stat_y - 80, Theme.TEXT_PRIMARY, Theme.FONT_BODY)
        arcade.draw_text(f"Fitness: {animal.fitness:.2f}", self.x + 10, stat_y - 100, Theme.TEXT_PRIMARY, Theme.FONT_BODY)
        arcade.draw_text(f"Alive: {animal.alive}", self.x + 10, stat_y - 120,
                         Theme.ACCENT_GREEN if animal.alive else Theme.ACCENT_ORANGE, Theme.FONT_BODY)

        # Action history (simplified)
        arcade.draw_text("Recent Actions:", self.x + 10, stat_y - 150, Theme.TEXT_SECONDARY, Theme.FONT_BODY)
        if hasattr(animal, 'action_history') and animal.action_history:
            for i, action in enumerate(animal.action_history[-5:]):
                arcade.draw_text(str(action), self.x + 10, stat_y - 170 - i*15, Theme.TEXT_SECONDARY, 12)

        # Neural network preview (placeholder)
        arcade.draw_text("Neural Network:", self.x + 10, stat_y - 250, Theme.TEXT_SECONDARY, Theme.FONT_BODY)
        # Draw simple representation
        arcade.draw_circle_outline(self.x + 50, stat_y - 280, 20, Theme.TEXT_PRIMARY, 2)
        arcade.draw_circle_outline(self.x + 100, stat_y - 280, 20, Theme.TEXT_PRIMARY, 2)
        arcade.draw_circle_outline(self.x + 150, stat_y - 280, 20, Theme.TEXT_PRIMARY, 2)
        arcade.draw_line(self.x + 50, stat_y - 280, self.x + 100, stat_y - 280, Theme.TEXT_SECONDARY, 1)
        arcade.draw_line(self.x + 100, stat_y - 280, self.x + 150, stat_y - 280, Theme.TEXT_SECONDARY, 1)

        # Export button
        self.export_button.draw()

    def set_selected_animal(self, animal):
        self.selected_animal = animal

    def export_animal_data(self):
        if self.selected_animal and hasattr(self, 'window') and self.window.simulation:
            animal_id = self.selected_animal.animal_id
            filename = self.window.simulation.export_animal_history(animal_id)
            print(f"Exported animal {animal_id} data to {filename}")
        else:
            print("No animal selected or simulation not available")

    def handle_click(self, mouse_x, mouse_y):
        if self.export_button.is_clicked(mouse_x, mouse_y):
            self.export_button.execute_callback()
            return True
        return False
