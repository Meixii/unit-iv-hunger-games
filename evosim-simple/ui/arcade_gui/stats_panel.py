import arcade
from .theme import Theme
from .ui_components import UICard, ProgressBar, MiniLineChart, PieChart

class StatsPanel:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.scroll_y = 0

        # Card positions with proper spacing
        padding = 15
        card_width = self.width - 2*padding
        card_height = 90
        card_spacing = 12
        current_y = self.y + self.height - card_height - 40

        self.population_card = UICard(self.x + padding, current_y, card_width, card_height, "Population")
        current_y -= card_height + card_spacing
        self.fitness_card = UICard(self.x + padding, current_y, card_width, card_height, "Fitness")
        current_y -= card_height + card_spacing
        self.resources_card = UICard(self.x + padding, current_y, card_width, card_height, "Resources")
        current_y -= card_height + card_spacing
        self.behavior_card = UICard(self.x + padding, current_y, card_width, card_height, "Behavior")
        current_y -= card_height + card_spacing
        self.environment_card = UICard(self.x + padding, current_y, card_width, card_height, "Environment")

        # Sample data for charts
        self.fitness_history = [0.5, 0.6, 0.7, 0.8, 0.9]
        self.behavior_data = [30, 20, 15, 10]  # move, eat, drink, rest

    def draw(self, stats_data=None):
        # Background
        arcade.draw_rectangle_filled(self.x + self.width/2, self.y + self.height/2,
                                     self.width, self.height, Theme.PANEL_BG)
        # Border
        arcade.draw_rectangle_outline(self.x + self.width/2, self.y + self.height/2,
                                      self.width, self.height, Theme.BORDER_COLOR, 1)

        # Title
        arcade.draw_text("Live Statistics", self.x + 15, self.y + self.height - 30,
                         Theme.TEXT_PRIMARY, Theme.FONT_HEADER, anchor_x="left", bold=True)

        # Draw cards
        self.draw_population_card(stats_data)
        self.draw_fitness_card(stats_data)
        self.draw_resources_card(stats_data)
        self.draw_behavior_card(stats_data)
        self.draw_environment_card(stats_data)

    def draw_population_card(self, stats_data):
        self.population_card.draw()
        if not stats_data:
            return
        alive = stats_data.get('alive_count', 0)
        dead = stats_data.get('dead_count', 0)
        total = alive + dead
        survival_rate = alive / total if total > 0 else 0

        padding = 15
        arcade.draw_text(f"Alive: {alive}", self.population_card.x + padding, self.population_card.y - 35,
                         Theme.ACCENT_GREEN, Theme.FONT_BODY)
        arcade.draw_text(f"Dead: {dead}", self.population_card.x + padding, self.population_card.y - 55,
                         Theme.ACCENT_ORANGE, Theme.FONT_BODY)
        ProgressBar.draw(self.population_card.x + padding, self.population_card.y - 75,
                         self.population_card.width - 2*padding, 10, survival_rate, 1.0, Theme.ACCENT_GREEN)

    def draw_fitness_card(self, stats_data):
        self.fitness_card.draw()
        if not stats_data:
            return
        avg_fitness = stats_data.get('average_fitness', 0)
        best_fitness = stats_data.get('best_fitness', 0)
        worst_fitness = stats_data.get('worst_fitness', 0)

        padding = 15
        arcade.draw_text(f"Avg: {avg_fitness:.2f}", self.fitness_card.x + padding, self.fitness_card.y - 35,
                         Theme.TEXT_PRIMARY, Theme.FONT_BODY)
        arcade.draw_text(f"Best: {best_fitness:.2f}", self.fitness_card.x + padding, self.fitness_card.y - 55,
                         Theme.ACCENT_GREEN, Theme.FONT_BODY)
        arcade.draw_text(f"Worst: {worst_fitness:.2f}", self.fitness_card.x + padding, self.fitness_card.y - 75,
                         Theme.ACCENT_ORANGE, Theme.FONT_BODY)

        # Mini chart
        chart = MiniLineChart(self.fitness_card.x + self.fitness_card.width - 90, self.fitness_card.y - 45,
                             70, 30, self.fitness_history, Theme.ACCENT_BLUE)
        chart.draw()

    def draw_resources_card(self, stats_data):
        self.resources_card.draw()
        if not stats_data:
            return
        food_remaining = stats_data.get('food_remaining', 0)
        water_remaining = stats_data.get('water_remaining', 0)
        total_consumed = stats_data.get('total_consumed', 0)

        padding = 15
        arcade.draw_text(f"Food: {food_remaining}", self.resources_card.x + padding, self.resources_card.y - 35,
                         Theme.ACCENT_ORANGE, Theme.FONT_BODY)
        arcade.draw_text(f"Water: {water_remaining}", self.resources_card.x + padding, self.resources_card.y - 55,
                         Theme.ACCENT_BLUE, Theme.FONT_BODY)
        arcade.draw_text(f"Consumed: {total_consumed}", self.resources_card.x + padding, self.resources_card.y - 75,
                         Theme.TEXT_SECONDARY, Theme.FONT_BODY)

    def draw_behavior_card(self, stats_data):
        self.behavior_card.draw()
        if not stats_data:
            return
        move_count = stats_data.get('move_count', 0)
        eat_count = stats_data.get('eat_count', 0)
        drink_count = stats_data.get('drink_count', 0)
        rest_count = stats_data.get('rest_count', 0)

        padding = 15
        arcade.draw_text(f"Move: {move_count}", self.behavior_card.x + padding, self.behavior_card.y - 35,
                         Theme.TEXT_PRIMARY, Theme.FONT_BODY)
        arcade.draw_text(f"Eat: {eat_count}", self.behavior_card.x + padding, self.behavior_card.y - 55,
                         Theme.ACCENT_ORANGE, Theme.FONT_BODY)
        arcade.draw_text(f"Drink: {drink_count}", self.behavior_card.x + padding, self.behavior_card.y - 75,
                         Theme.ACCENT_BLUE, Theme.FONT_BODY)

        # Pie chart
        total = move_count + eat_count + drink_count + rest_count
        if total > 0:
            chart = PieChart(self.behavior_card.x + self.behavior_card.width - 70, self.behavior_card.y - 45,
                             40, [move_count/total, eat_count/total, drink_count/total, rest_count/total],
                             [Theme.TEXT_PRIMARY, Theme.ACCENT_ORANGE, Theme.ACCENT_BLUE, Theme.TEXT_SECONDARY])
            chart.draw()

    def draw_environment_card(self, stats_data):
        self.environment_card.draw()
        if not stats_data:
            return
        active_events = stats_data.get('active_events', [])
        # Ensure active_events is a list
        if not isinstance(active_events, list):
            active_events = []
        grid_utilization = stats_data.get('grid_utilization', 0)

        padding = 15
        event_text = ', '.join(active_events) if active_events else "None"
        arcade.draw_text(f"Events: {event_text}", self.environment_card.x + padding, self.environment_card.y - 35,
                         Theme.TEXT_PRIMARY, Theme.FONT_BODY)
        arcade.draw_text(f"Grid Use: {grid_utilization:.1%}", self.environment_card.x + padding, self.environment_card.y - 55,
                         Theme.TEXT_SECONDARY, Theme.FONT_BODY)

    def handle_scroll(self, delta):
        self.scroll_y += delta * 10
        # Clamp scroll
        max_scroll = 200  # Adjust based on content height
        self.scroll_y = max(0, min(max_scroll, self.scroll_y))

    def update_data(self, new_stats):
        # Update chart data
        if 'average_fitness' in new_stats:
            self.fitness_history.append(new_stats['average_fitness'])
            if len(self.fitness_history) > 10:
                self.fitness_history.pop(0)
