import arcade
from .theme import Theme
from .config_panel import ConfigPanel
from .control_panel import ControlPanel
from .stats_panel import StatsPanel

class TabPanel:
    """Tabbed interface for right panel to avoid overflow"""
    def __init__(self, x, y, width, height, window):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.window = window
        
        # Tab configuration
        self.tabs = ["Config", "Controls", "Stats"]
        self.active_tab = 1  # Start with Controls tab
        self.tab_height = 40
        self.tab_width = self.width // len(self.tabs)
        
        # Create panels (they will be drawn based on active tab)
        panel_y = self.y
        panel_height = self.height - self.tab_height
        
        self.config_panel = ConfigPanel(self.x, panel_y, self.width, panel_height, window)
        self.control_panel = ControlPanel(self.x, panel_y, self.width, panel_height, window)
        self.stats_panel = StatsPanel(self.x, panel_y, self.width, panel_height)
        
        # Adjust config panel to not be collapsible in tabbed mode
        self.config_panel.is_collapsed = False
    
    def draw(self, current_stats=None):
        # Draw tab bar at top
        tab_y = self.y + self.height - self.tab_height
        
        for i, tab_name in enumerate(self.tabs):
            tab_x = self.x + i * self.tab_width
            is_active = (i == self.active_tab)
            
            # Tab background
            color = Theme.ACCENT_BLUE if is_active else Theme.PANEL_BG
            arcade.draw_rectangle_filled(tab_x + self.tab_width/2, tab_y + self.tab_height/2,
                                         self.tab_width, self.tab_height, color)
            
            # Tab border
            arcade.draw_rectangle_outline(tab_x + self.tab_width/2, tab_y + self.tab_height/2,
                                          self.tab_width, self.tab_height, Theme.BORDER_COLOR, 1)
            
            # Tab text
            text_color = Theme.TEXT_PRIMARY if is_active else Theme.TEXT_SECONDARY
            arcade.draw_text(tab_name, tab_x + self.tab_width/2, tab_y + self.tab_height/2 - 6,
                             text_color, Theme.FONT_BODY, anchor_x="center", bold=is_active)
        
        # Draw active panel
        if self.active_tab == 0:  # Config
            self.config_panel.draw()
        elif self.active_tab == 1:  # Controls
            self.control_panel.draw()
        elif self.active_tab == 2:  # Stats
            if current_stats:
                self.stats_panel.draw(current_stats)
    
    def handle_click(self, mouse_x, mouse_y):
        # Check if clicking on tabs
        tab_y = self.y + self.height - self.tab_height
        if tab_y <= mouse_y <= tab_y + self.tab_height:
            for i in range(len(self.tabs)):
                tab_x = self.x + i * self.tab_width
                if tab_x <= mouse_x <= tab_x + self.tab_width:
                    self.active_tab = i
                    print(f"[TAB] Switched to {self.tabs[i]} tab")
                    return True
        
        # Forward click to active panel
        if self.active_tab == 0:
            return self.config_panel.handle_click(mouse_x, mouse_y)
        elif self.active_tab == 1:
            return self.control_panel.handle_click(mouse_x, mouse_y)
        elif self.active_tab == 2:
            return False  # Stats panel doesn't handle clicks
        return False
    
    def check_hover(self, mouse_x, mouse_y):
        if self.active_tab == 0:
            self.config_panel.check_hover(mouse_x, mouse_y)
        elif self.active_tab == 1:
            self.control_panel.check_hover(mouse_x, mouse_y)
    
    def handle_drag(self, mouse_x, mouse_y):
        if self.active_tab == 0:
            self.config_panel.handle_drag(mouse_x, mouse_y)
        elif self.active_tab == 1:
            self.control_panel.speed_slider.handle_drag(mouse_x)
    
    def handle_release(self):
        if self.active_tab == 0:
            self.config_panel.handle_release()
        elif self.active_tab == 1:
            self.control_panel.speed_slider.stop_drag()
    
    def handle_key_press(self, key, modifiers):
        if self.active_tab == 0:
            return self.config_panel.handle_key_press(key, modifiers)
        return False
    
    def handle_scroll(self, scroll_y):
        if self.active_tab == 2:
            self.stats_panel.handle_scroll(scroll_y)
    
    def start_slider_drag(self, mouse_x, mouse_y):
        """Start dragging sliders in active panel"""
        if self.active_tab == 0:
            for slider in self.config_panel.sliders:
                slider.start_drag(mouse_x, mouse_y)
        elif self.active_tab == 1:
            self.control_panel.speed_slider.start_drag(mouse_x, mouse_y)
