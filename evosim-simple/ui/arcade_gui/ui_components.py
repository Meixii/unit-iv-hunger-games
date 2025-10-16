import arcade
from .theme import Theme

class UICard:
    def __init__(self, x, y, width, height, title="", bg_color=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.bg_color = bg_color or Theme.CARD_BG

    def draw(self):
        # Draw background with rounded corners effect
        arcade.draw_rectangle_filled(self.x + self.width/2, self.y - self.height/2,
                                     self.width, self.height, self.bg_color)
        # Draw border
        arcade.draw_rectangle_outline(self.x + self.width/2, self.y - self.height/2,
                                      self.width, self.height, Theme.BORDER_COLOR, 1)
        # Draw title if provided with proper padding
        if self.title:
            arcade.draw_text(self.title, self.x + 15, self.y - 25,
                             Theme.TEXT_PRIMARY, Theme.FONT_HEADER, anchor_x="left", bold=True)

class UIButton:
    def __init__(self, x, y, width, height, text, color=None, callback=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color or Theme.ACCENT_GREEN
        self.hover_color = self.lighten_color(self.color, 1.1)
        self.callback = callback
        self.is_hovered = False

    def draw(self):
        color = self.hover_color if self.is_hovered else self.color
        arcade.draw_rectangle_filled(self.x + self.width/2, self.y - self.height/2,
                                     self.width, self.height, color)
        arcade.draw_rectangle_outline(self.x + self.width/2, self.y - self.height/2,
                                      self.width, self.height, Theme.TEXT_SECONDARY, 1)
        arcade.draw_text(self.text, self.x + self.width/2, self.y - self.height/2,
                         Theme.TEXT_PRIMARY, Theme.FONT_BODY, anchor_x="center", anchor_y="center")

    def check_hover(self, mouse_x, mouse_y):
        self.is_hovered = (self.x <= mouse_x <= self.x + self.width and
                           self.y - self.height <= mouse_y <= self.y)

    def is_clicked(self, mouse_x, mouse_y):
        return (self.x <= mouse_x <= self.x + self.width and
                self.y - self.height <= mouse_y <= self.y)

    def execute_callback(self):
        if self.callback:
            self.callback()

    @staticmethod
    def lighten_color(color, factor):
        if len(color) == 3:
            # RGB tuple
            return (min(255, int(color[0] * factor)),
                    min(255, int(color[1] * factor)),
                    min(255, int(color[2] * factor)))
        elif len(color) == 4:
            # RGBA tuple
            return (min(255, int(color[0] * factor)),
                    min(255, int(color[1] * factor)),
                    min(255, int(color[2] * factor)),
                    color[3])
        else:
            # Fallback
            return color

class UISlider:
    def __init__(self, x, y, width, min_val, max_val, initial_val, label="", callback=None):
        self.x = x
        self.y = y
        self.width = width
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.is_dragging = False
        self.callback = callback  # Callback function when value changes

    def draw(self):
        # Draw label and value above slider
        if self.label:
            # Format value based on label type
            if "Prob" in self.label or "Density" in self.label:
                # Show as percentage
                display_value = f"{self.value * 100:.0f}%"
            elif ("Width" in self.label or "Height" in self.label or "Population" in self.label or 
                  "Generation" in self.label or "Steps" in self.label):
                # Show as whole number
                display_value = f"{int(self.value)}"
            else:
                # Default: 2 decimal places
                display_value = f"{self.value:.2f}"
            
            arcade.draw_text(f"{self.label}: {display_value}", self.x, self.y + 15,
                             Theme.TEXT_SECONDARY, Theme.FONT_BODY, anchor_x="left")
        # Draw track
        arcade.draw_rectangle_filled(self.x + self.width/2, self.y,
                                     self.width, 6, Theme.SLIDER_TRACK)
        # Draw filled portion
        filled_width = ((self.value - self.min_val) / (self.max_val - self.min_val)) * self.width
        if filled_width > 0:
            arcade.draw_rectangle_filled(self.x + filled_width/2, self.y,
                                         filled_width, 6, Theme.ACCENT_BLUE)
        # Draw handle
        handle_x = self.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.width
        arcade.draw_circle_filled(handle_x, self.y, 10, Theme.ACCENT_BLUE)
        arcade.draw_circle_outline(handle_x, self.y, 10, Theme.TEXT_PRIMARY, 1)

    def handle_drag(self, mouse_x):
        if self.is_dragging:
            relative_x = mouse_x - self.x
            ratio = max(0, min(1, relative_x / self.width))
            old_value = self.value
            self.value = self.min_val + ratio * (self.max_val - self.min_val)
            # Call callback if value changed
            if self.callback and abs(old_value - self.value) > 0.01:
                self.callback(self.value)

    def start_drag(self, mouse_x, mouse_y):
        # Check if clicking anywhere on the slider track or label area
        if (self.x <= mouse_x <= self.x + self.width and 
            self.y - 20 <= mouse_y <= self.y + 25):  # Expanded to include label area
            self.is_dragging = True
            # Immediately update value to clicked position
            relative_x = mouse_x - self.x
            ratio = max(0, min(1, relative_x / self.width))
            old_value = self.value
            self.value = self.min_val + ratio * (self.max_val - self.min_val)
            # Call callback immediately
            if self.callback and abs(old_value - self.value) > 0.01:
                self.callback(self.value)

    def stop_drag(self):
        self.is_dragging = False

    def get_value(self):
        return self.value

class ProgressBar:
    @staticmethod
    def draw(x, y, width, height, value, max_value, color):
        ratio = value / max_value if max_value > 0 else 0
        fill_width = width * ratio
        # Background
        arcade.draw_rectangle_filled(x + width/2, y - height/2, width, height, Theme.PANEL_BG)
        # Fill
        arcade.draw_rectangle_filled(x + fill_width/2, y - height/2, fill_width, height, color)
        # Border
        arcade.draw_rectangle_outline(x + width/2, y - height/2, width, height, Theme.TEXT_SECONDARY, 1)

class MiniLineChart:
    def __init__(self, x, y, width, height, data_points, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.data_points = data_points
        self.color = color

    def draw(self):
        if not self.data_points or len(self.data_points) < 2:
            return
        max_val = max(self.data_points) if self.data_points else 1
        if max_val == 0:
            max_val = 1
        points = []
        step_x = self.width / (len(self.data_points) - 1) if len(self.data_points) > 1 else 0
        for i, val in enumerate(self.data_points):
            px = self.x + i * step_x
            py = self.y - (val / max_val) * self.height
            points.append((px, py))  # Append as tuple, not extend
        if len(points) >= 2:
            arcade.draw_line_strip(points, self.color, 2)

class PieChart:
    def __init__(self, x, y, radius, percentages, colors, labels=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.percentages = percentages
        self.colors = colors
        self.labels = labels or []

    def draw(self):
        start_angle = 0
        for i, percentage in enumerate(self.percentages):
            angle = percentage * 360
            arcade.draw_arc_filled(self.x, self.y, self.radius * 2, self.radius * 2,
                                   self.colors[i % len(self.colors)], start_angle, start_angle + angle)
            start_angle += angle
        # Border
        arcade.draw_circle_outline(self.x, self.y, self.radius, Theme.TEXT_SECONDARY, 2)

class UINumericInput:
    def __init__(self, x, y, width, height, value, min_val, max_val, label="", decimals=2):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.value = value
        self.min_val = min_val
        self.max_val = max_val
        self.label = label
        self.decimals = decimals
        self.is_selected = False
        self.text = f"{value:.{decimals}f}"
        self.cursor_pos = len(self.text)
        self.last_click_time = 0

    def draw(self):
        # Draw label
        if self.label:
            arcade.draw_text(self.label, self.x, self.y + self.height + 5,
                             Theme.TEXT_SECONDARY, Theme.FONT_BODY, anchor_x="left")
        
        # Draw background
        bg_color = Theme.BUTTON_HOVER if self.is_selected else Theme.CARD_BG
        arcade.draw_rectangle_filled(self.x + self.width/2, self.y + self.height/2,
                                     self.width, self.height, bg_color)
        
        # Draw border
        border_color = Theme.ACCENT_BLUE if self.is_selected else Theme.BORDER_COLOR
        arcade.draw_rectangle_outline(self.x + self.width/2, self.y + self.height/2,
                                      self.width, self.height, border_color, 2)
        
        # Draw text
        text_color = Theme.TEXT_PRIMARY
        arcade.draw_text(self.text, self.x + 10, self.y + self.height//2,
                         text_color, Theme.FONT_BODY, anchor_y="center", anchor_x="left")
        
        # Draw cursor if selected
        if self.is_selected:
            # Estimate text width (8 pixels per character for size 14 font)
            char_width = 8
            text_width = len(self.text[:self.cursor_pos]) * char_width
            cursor_x = self.x + 10 + text_width
            arcade.draw_line(cursor_x, self.y + 5, cursor_x, self.y + self.height - 5,
                             Theme.TEXT_PRIMARY, 2)

    def check_hover(self, mouse_x, mouse_y):
        return (self.x <= mouse_x <= self.x + self.width and
                self.y <= mouse_y <= self.y + self.height)

    def handle_click(self, mouse_x, mouse_y):
        if self.check_hover(mouse_x, mouse_y):
            self.is_selected = True
            # Calculate cursor position based on click location
            char_width = 8  # Approximate character width
            if len(self.text) > 0:
                relative_x = mouse_x - (self.x + 10)
                self.cursor_pos = min(len(self.text), max(0, int(relative_x / char_width)))
            else:
                self.cursor_pos = 0
            return True
        else:
            self.is_selected = False
            return False

    def handle_key_press(self, key, modifiers):
        if not self.is_selected:
            return False
            
        if key == arcade.key.BACKSPACE:
            if self.cursor_pos > 0:
                self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
                self.cursor_pos -= 1
        elif key == arcade.key.DELETE:
            if self.cursor_pos < len(self.text):
                self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos+1:]
        elif key == arcade.key.LEFT:
            self.cursor_pos = max(0, self.cursor_pos - 1)
        elif key == arcade.key.RIGHT:
            self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
        elif key == arcade.key.HOME:
            self.cursor_pos = 0
        elif key == arcade.key.END:
            self.cursor_pos = len(self.text)
        else:
            # Handle numeric input
            char = None
            if key >= arcade.key.NUM_0 and key <= arcade.key.NUM_9:
                char = str(key - arcade.key.NUM_0)
            elif key == arcade.key.PERIOD and '.' not in self.text:
                char = '.'
            elif key == arcade.key.MINUS and self.cursor_pos == 0:
                char = '-'
            
            if char:
                self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
                self.cursor_pos += 1
        
        # Try to parse and validate the value
        try:
            new_value = float(self.text)
            if self.min_val <= new_value <= self.max_val:
                self.value = new_value
            else:
                # Revert text if out of bounds
                self.text = f"{self.value:.{self.decimals}f}"
        except ValueError:
            # Revert text if invalid
            self.text = f"{self.value:.{self.decimals}f}"
        
        return True

class ScrollableContainer:
    def __init__(self, x, y, width, height, content_height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.content_height = content_height
        self.scroll_y = 0
        self.max_scroll = max(0, content_height - height)

    def draw(self, draw_content_callback):
        # Draw scrollbar if needed
        if self.content_height > self.height:
            scrollbar_height = self.height * (self.height / self.content_height)
            scrollbar_y = self.y - (self.scroll_y / self.max_scroll) * (self.height - scrollbar_height)
            arcade.draw_rectangle_filled(self.x + self.width - 10, scrollbar_y - scrollbar_height/2,
                                         8, scrollbar_height, Theme.TEXT_SECONDARY)

        # Clip drawing to container area (simplified, arcade doesn't have built-in clipping)
        draw_content_callback(self.scroll_y)

    def handle_scroll(self, delta):
        self.scroll_y = max(0, min(self.max_scroll, self.scroll_y + delta * 20))
