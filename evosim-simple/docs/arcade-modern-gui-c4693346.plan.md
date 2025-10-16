
# Modern Arcade GUI for Evolutionary Simulation

## Overview

Create `evosim-simple/ui/main_gui.py` - a modern, game-like interface using Arcade library with split-screen layout, nature-themed visuals, and comprehensive controls for presentations.

## Architecture

### Core Components

**1. Main Window Class (`EvolutionSimulationWindow`)**

- Extends `arcade.Window`
- Resolution presets: 1920x1080, 1366x768, 1024x768
- Split-screen layout with responsive scaling

**2. Left Side: Grid Visualization (60% width)**

- Live simulation grid with sprite rendering
- Grid cell size: 32px (scalable based on resolution)
- Visual elements:
                                - Animals: Colored circles/shapes (placeholder sprites)
                                - Food: Orange/yellow shapes
                                - Water: Blue shapes
                                - Background: Green grass pattern
- Animations:
                                - Smooth movement transitions
                                - Eating/drinking particle effects
                                - Death fade-out effect
                                - Environmental event overlays (drought = brown tint, storm = rain effect)
- Grid info overlay:
                                - Generation counter (top-left)
                                - Step counter (top-left)
                                - Active events banner (top-center)
                                - FPS counter (bottom-right)

**3. Right Side: Control & Stats Panel (40% width)**

**3a. Configuration Section (top, collapsible)**

- Grid size sliders (width/height: 10-50)
- Population size slider (10-200)
- Resource density sliders (food/water: 0.05-0.50)
- Event probability sliders (drought/storm/famine/bonus)
- Max generations input (1-100)
- Steps per generation input (10-500)
- "Apply Config" button
- "Load Preset" dropdown (Optimal, Default, Challenge modes)

**3b. Control Buttons (middle)**

- START (green, large) - Initialize and start simulation
- PAUSE/RESUME (yellow) - Toggle pause state
- STOP (red) - Stop simulation
- RESET (orange) - Reset to initial state
- Speed slider (0.1x to 10x)
- "Trigger Event" dropdown (manually trigger drought/storm/etc)

**3c. Live Statistics Cards (scrollable)**

- **Population Card**
                                - Alive count (green number)
                                - Dead count (red number)
                                - Survival rate progress bar
                                - Icon indicators

- **Fitness Card**
                                - Average fitness (with trend arrow)
                                - Best fitness (gold medal icon)
                                - Worst fitness
                                - Fitness graph mini-preview

- **Resources Card**
                                - Food remaining (orange icon + count)
                                - Water remaining (blue icon + count)
                                - Total consumed (stacked bar)

- **Behavior Card**
                                - Move count (foot icon)
                                - Eat count (fork icon)
                                - Drink count (water drop icon)
                                - Rest count (bed icon)
                                - Pie chart preview

- **Environment Card**
                                - Active events list
                                - Grid utilization
                                - Environmental conditions

**3d. Bottom Action Buttons**

- "View Charts" - Opens detailed matplotlib charts window (reuses existing visualization.py)
- "Export Data" - Save statistics to JSON/CSV
- "Export Animals" - Export individual animal history
- "Screenshot" - Save current grid view
- "Settings" - Resolution/theme options

## Implementation Details

### File Structure (Modular Architecture)

```
evosim-simple/ui/
├── arcade_gui/                    # New Arcade GUI package
│   ├── __init__.py               # Package initialization
│   ├── main_window.py            # Main window class (~250 lines)
│   ├── grid_renderer.py          # Grid visualization (~300 lines)
│   ├── control_panel.py          # Control panel UI (~350 lines)
│   ├── stats_panel.py            # Statistics display (~300 lines)
│   ├── config_panel.py           # Configuration UI (~250 lines)
│   ├── animal_inspector.py       # Animal details view (~200 lines)
│   ├── ui_components.py          # Reusable UI elements (~350 lines)
│   ├── sprite_manager.py         # Sprite management (~200 lines)
│   ├── animation_effects.py      # Particle & animations (~250 lines)
│   ├── theme.py                  # Color palette & styling (~100 lines)
│   └── constants.py              # Constants & presets (~100 lines)
├── gui.py                        # Keep existing tkinter GUI
└── run_arcade_gui.py             # Entry point script (~50 lines)
```

### Key Classes (Modular Design)

**main_window.py:**

```python
class EvolutionSimulationWindow(arcade.Window):
 - __init__(width, height, title)
 - setup() - Initialize all components
 - on_draw() - Orchestrate rendering of all panels
 - on_update(delta_time) - Update simulation & animations
 - on_mouse_press/release/motion() - Delegate to panels
 - on_key_press/release() - Handle keyboard shortcuts
 - _initialize_panels() - Create panel instances
 - _handle_simulation_callbacks() - Process sim events
 - change_resolution(preset) - Switch resolution
```

**grid_renderer.py:**

```python
class GridRenderer:
 - __init__(x, y, width, height, theme)
 - draw(environment, generation, step, events) - Main render
 - draw_grid_background() - Grass/terrain tiles
 - draw_resources(food_positions, water_positions)
 - draw_animals(animals_list) - With smooth movement
 - draw_overlays(generation, step, events, fps)
 - draw_event_effects(active_events) - Drought/storm effects
 - update_animations(delta_time) - Smooth transitions
 - handle_click(x, y) - Animal selection for inspector
```

**control_panel.py:**

```python
class ControlPanel:
 - __init__(x, y, width, height, theme)
 - draw() - Render all controls
 - draw_simulation_buttons() - Start/Pause/Stop/Reset
 - draw_speed_control() - Speed slider
 - draw_event_triggers() - Manual event buttons
 - handle_click(x, y) - Process button clicks
 - get_callbacks() - Return dict of button callbacks
```

**stats_panel.py:**

```python
class StatsPanel:
 - __init__(x, y, width, height, theme)
 - draw(stats_data) - Render all stat cards
 - draw_population_card(alive, dead, survival_rate)
 - draw_fitness_card(avg, best, worst, trend)
 - draw_resources_card(food, water, consumed)
 - draw_behavior_card(move, eat, drink, rest)
 - draw_environment_card(events, grid_util)
 - draw_mini_chart(data, chart_type) - Small graphs
 - update_data(new_stats) - Refresh statistics
```

**config_panel.py:**

```python
class ConfigPanel:
 - __init__(x, y, width, height, theme)
 - draw() - Render configuration UI
 - draw_sliders() - All config sliders
 - draw_preset_dropdown() - Load preset configs
 - draw_apply_button() - Apply configuration
 - handle_click(x, y) - Slider/button interaction
 - handle_drag(x, y) - Slider dragging
 - get_config() - Return current config dict
 - set_config(config_dict) - Load config values
 - is_collapsed - Collapsible state management
```

**animal_inspector.py:**

```python
class AnimalInspector:
 - __init__(x, y, width, height, theme)
 - draw(animal) - Render animal details
 - draw_stats(hunger, thirst, energy, health)
 - draw_action_history(actions) - Timeline view
 - draw_neural_network_preview() - Simplified visualization
 - draw_export_button() - Export animal data
 - set_selected_animal(animal) - Update displayed animal
 - handle_click(x, y) - Export button handler
```

**ui_components.py:**

```python
class UICard:
 - draw(x, y, width, height, title, bg_color)
    
class UIButton:
 - __init__(x, y, width, height, text, color, callback)
 - draw() - Render with hover effect
 - is_hovered(mouse_x, mouse_y)
 - is_clicked(mouse_x, mouse_y)
 - execute_callback()
    
class UISlider:
 - __init__(x, y, width, min_val, max_val, initial, label)
 - draw() - Render slider with label
 - handle_drag(mouse_x) - Update value
 - get_value() - Current slider value
    
class ProgressBar:
 - draw(x, y, width, height, value, max_value, color)
    
class MiniLineChart:
 - draw(x, y, width, height, data_points, color)
    
class PieChart:
 - draw(x, y, radius, percentages, colors, labels)
    
class ScrollableContainer:
 - __init__(x, y, width, height, content_height)
 - draw(draw_content_callback)
 - handle_scroll(delta) - Mouse wheel scrolling
```

**sprite_manager.py:**

```python
class SpriteManager:
 - __init__(cell_size)
 - load_or_create_sprites() - Initialize all sprites
 - create_animal_sprite(animal_id) - Unique color per animal
 - create_food_sprite() - 20x20 orange/yellow shape
 - create_water_sprite() - 20x20 blue droplet
 - create_grass_tile() - 32x32 green texture
 - get_animal_sprite(animal) - Retrieve cached sprite
 - get_resource_sprite(type) - food or water
 - scale_sprites(new_cell_size) - For resolution change
```

**animation_effects.py:**

```python
class ParticleEffect:
 - __init__(x, y, particle_type, count)
 - update(delta_time) - Update particle positions
 - draw() - Render particles
 - is_finished() - Check if animation done

class AnimationManager:
 - __init__()
 - add_eating_effect(x, y)
 - add_drinking_effect(x, y)
 - add_death_effect(x, y)
 - add_movement_trail(from_pos, to_pos)
 - update_all(delta_time) - Update all active effects
 - draw_all() - Render all active effects
 - clear_finished() - Remove completed animations
```

**theme.py:**

```python
class Theme:
  # Color constants
  BACKGROUND = arcade.color.from_hex_string("#2E3440")
  PANEL_BG = arcade.color.from_hex_string("#3B4252")
  CARD_BG = arcade.color.from_hex_string("#434C5E")
  ACCENT_GREEN = arcade.color.from_hex_string("#A3BE8C")
  ACCENT_ORANGE = arcade.color.from_hex_string("#D08770")
  ACCENT_BLUE = arcade.color.from_hex_string("#88C0D0")
  TEXT_PRIMARY = arcade.color.from_hex_string("#ECEFF4")
  TEXT_SECONDARY = arcade.color.from_hex_string("#D8DEE9")
  
  # Font sizes
  FONT_HEADER = 18
  FONT_BODY = 14
  FONT_COUNTER = 20
```

**constants.py:**

```python
# Resolution presets
RESOLUTIONS = {
  "1920x1080": (1920, 1080, 40),  # (width, height, cell_size)
  "1366x768": (1366, 768, 32),
  "1024x768": (1024, 768, 25)
}

# Default configuration
DEFAULT_CONFIG = {
  "grid_size": (20, 20),
  "population_size": 50,
  "food_density": 0.15,
  # ... etc
}

# Layout constants (calculated per resolution)
def get_layout(resolution_preset):
  # Returns dict with panel positions/sizes
```

### Integration with Existing Code

**Leverage existing modules:**

- `src.simulation.Simulation` - Core simulation engine
- `src.environment.GridWorld` - Grid state and animal positions
- `src.events.EventManager` - Environmental events
- `src.evolution.Population` - Population management
- `analysis.statistics.StatisticsCollector` - Stats tracking
- `analysis.visualization.SimulationVisualizer` - Charts (opened in separate window)

**Data Flow:**

1. GUI creates `Simulation` instance with config
2. GUI registers callbacks for step/generation updates
3. Arcade's `on_update()` calls simulation step (if running)
4. Simulation callbacks update GUI state variables
5. `on_draw()` renders current state

### Visual Styling (Nature Theme)

**Color Palette:**

- Background: `#2E3440` (dark gray)
- Panel background: `#3B4252` (lighter gray)
- Card background: `#434C5E` (card gray)
- Accent green: `#A3BE8C` (nature green)
- Accent orange: `#D08770` (food)
- Accent blue: `#88C0D0` (water)
- Text primary: `#ECEFF4` (white)
- Text secondary: `#D8DEE9` (light gray)

**Typography:**

- Headers: 16-20px bold
- Body: 12-14px regular
- Counters: 18-24px bold

**Effects:**

- Cards: Subtle shadow/border
- Buttons: Hover effect (brighten 10%)
- Animations: Smooth easing (0.2s transition)
- Particle effects for eating/drinking (3-5 particles, fade out)

### Resolution Scaling

**1920x1080:**

- Grid: 800x800 (40px cells for 20x20 grid)
- Control panel: 1120px wide
- Cell size: 40px

**1366x768:**

- Grid: 640x640 (32px cells)
- Control panel: 726px wide
- Cell size: 32px

**1024x768:**

- Grid: 512x512 (25px cells)
- Control panel: 512px wide
- Cell size: 25px

### Keyboard Shortcuts

- `SPACE` - Pause/Resume
- `R` - Reset
- `S` - Stop
- `1-3` - Change resolution preset
- `+/-` - Adjust speed
- `E` - Export data
- `C` - View charts
- `ESC` - Quit

### Entry Point

Create `evosim-simple/ui/run_arcade_gui.py`:

```python
"""Entry point for Arcade GUI version of Evolution Simulation"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import arcade
from arcade_gui.main_window import EvolutionSimulationWindow

def main():
    # Default to 1366x768
    window = EvolutionSimulationWindow(1366, 768, "Evolution Simulation")
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
```

## Implementation Steps (Modular Approach)

### Phase 1: Foundation

1. Create `arcade_gui` package directory and `__init__.py`
2. Create `theme.py` with color palette and style constants
3. Create `constants.py` with resolution presets and default configs
4. Create `sprite_manager.py` with placeholder sprite generation (circles/shapes)

### Phase 2: Core UI Components  

5. Create `ui_components.py` with:

      - UICard class
      - UIButton class with hover effects
      - UISlider class with drag support
      - ProgressBar class
      - MiniLineChart class
      - PieChart class
      - ScrollableContainer class

### Phase 3: Main Window & Grid

6. Create `main_window.py` with basic Arcade window setup
7. Create `grid_renderer.py` for left-side visualization:

      - Grid background rendering
      - Resource sprite placement
      - Animal sprite rendering
      - Overlay information display

### Phase 4: Control Panels

8. Create `control_panel.py` with simulation control buttons
9. Create `config_panel.py` with configuration sliders and presets
10. Create `stats_panel.py` with live statistics cards
11. Create `animal_inspector.py` for animal detail view

### Phase 5: Animation & Effects

12. Create `animation_effects.py` with:

        - ParticleEffect class for eating/drinking
        - Death fade-out animations
        - Movement interpolation
        - Environmental effect overlays

### Phase 6: Integration

13. Connect all panels to `main_window.py`
14. Implement simulation callbacks (step/generation updates)
15. Add button click handlers and event routing
16. Implement mouse interaction (click animals, drag sliders)
17. Add keyboard shortcuts

### Phase 7: Advanced Features

18. Implement resolution switching functionality
19. Add animal inspector click-to-select feature
20. Integrate export functionality (data/charts/screenshots)
21. Add scrolling for stats panel if content overflows

### Phase 8: Polish & Testing

22. Add smooth transitions and animations
23. Implement environmental event visual effects
24. Create entry point script `run_arcade_gui.py`
25. Test all resolutions and features
26. Performance optimization (sprite batching, dirty regions)

## Testing Checklist

- [ ] All resolutions display correctly without overlapping
- [ ] Simulation starts/pauses/stops/resets properly
- [ ] Statistics update in real-time
- [ ] Animal sprites move smoothly across grid
- [ ] Resource sprites appear/disappear correctly
- [ ] Event effects display properly (drought tint, storm particles)
- [ ] Configuration changes apply correctly
- [ ] Export functions work (data, charts, screenshots)
- [ ] Keyboard shortcuts function as expected
- [ ] UI remains responsive during simulation
- [ ] No performance issues with 50 animals + 200 steps