import arcade

class Theme:
    # Modern color palette - Dark theme with vibrant accents
    BACKGROUND = (30, 33, 39)       # #1E2127 - Deep charcoal
    PANEL_BG = (40, 44, 52)         # #282C34 - Dark gray
    CARD_BG = (50, 55, 65)          # #323741 - Medium gray
    
    # Vibrant accent colors
    ACCENT_GREEN = (80, 250, 123)   # #50FA7B - Bright green
    ACCENT_ORANGE = (255, 184, 108) # #FFB86C - Warm orange
    ACCENT_BLUE = (139, 233, 253)   # #8BE9FD - Cyan blue
    ACCENT_PURPLE = (189, 147, 249) # #BD93F9 - Purple
    ACCENT_PINK = (255, 121, 198)   # #FF79C6 - Pink
    ACCENT_RED = (255, 85, 85)      # #FF5555 - Red
    ACCENT_YELLOW = (241, 250, 140) # #F1FA8C - Yellow
    
    # Text colors
    TEXT_PRIMARY = (248, 248, 242)  # #F8F8F2 - Almost white
    TEXT_SECONDARY = (189, 189, 189) # #BDBDBD - Light gray
    TEXT_DIM = (108, 113, 128)      # #6C7180 - Dim gray
    
    # UI element colors
    BUTTON_HOVER = (60, 65, 75)     # Lighter than CARD_BG
    SLIDER_TRACK = (70, 75, 85)     # Track color
    BORDER_COLOR = (80, 85, 95)     # Border color

    # Font sizes
    FONT_HEADER = 18
    FONT_BODY = 14
    FONT_COUNTER = 20
    FONT_SMALL = 12
