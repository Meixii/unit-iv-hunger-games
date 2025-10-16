# Resolution presets
RESOLUTIONS = {
    "1920x1080": (1920, 1080, 40),  # (width, height, cell_size)
    "1366x768": (1366, 768, 32),
    "1024x768": (1024, 768, 25)
}

# Default configuration - matches simulation.py _get_default_config structure
DEFAULT_CONFIG = {
    "grid_size": (20, 20),
    "population_size": 50,
    "max_generations": 10,
    "steps_per_generation": 100,
    "simulation_speed": 1.0,
    "day_night_cycle": False,
    "seasonal_variations": False,
    "food_density": 0.15,
    "water_density": 0.15,
    "drought_probability": 0.02,
    "storm_probability": 0.01,
    "famine_probability": 0.05,
    "bonus_probability": 0.05,
    "mutation_rate": 0.1,
    "crossover_rate": 0.8,
    "selection_method": "tournament",
    "tournament_size": 3,
    "elite_percentage": 0.1
}

# Layout constants (calculated per resolution)
def get_layout(resolution_preset):
    width, height, cell_size = RESOLUTIONS[resolution_preset]
    grid_width = int(width * 0.6)
    panel_width = width - grid_width

    return {
        "grid": {"x": 0, "y": 0, "width": grid_width, "height": height},
        "panel": {"x": grid_width, "y": 0, "width": panel_width, "height": height},
        "cell_size": cell_size
    }
