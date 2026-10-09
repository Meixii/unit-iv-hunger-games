"""
Generate High-Quality Simulation Screenshots and Scientific Charts for EvoSim Documentation.
Executes real simulation runs using the EvoSim engine and renders publication-quality figures.
"""

import sys
import os
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, RegularPolygon, FancyBboxPatch
import numpy as np

# Ensure evosim-game is on sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
GAME_DIR = os.path.join(PROJECT_ROOT, "evosim-game")
DOCS_IMAGES_DIR = os.path.join(PROJECT_ROOT, "evosim-docs", "public", "images")
os.makedirs(DOCS_IMAGES_DIR, exist_ok=True)

sys.path.insert(0, GAME_DIR)

from simulation_controller import SimulationController
from config import SimulationConfig
from data_structures import TerrainType, AnimalCategory, ResourceType
from sensory import build_input_vector
from mlp import MLPNetwork


def set_custom_dark_theme():
    """Apply modern dark-theme styling inspired by the Astro documentation design system."""
    plt.rcParams.update({
        'figure.facecolor': '#090d16',
        'axes.facecolor': '#0d1322',
        'axes.edgecolor': '#1e293b',
        'axes.labelcolor': '#94a3b8',
        'text.color': '#f8fafc',
        'xtick.color': '#64748b',
        'ytick.color': '#64748b',
        'grid.color': '#1e293b',
        'grid.linestyle': '--',
        'grid.alpha': 0.6,
        'font.sans-serif': ['DejaVu Sans', 'Liberation Sans', 'Arial'],
        'font.family': 'sans-serif',
        'axes.titlecolor': '#38bdf8',
        'axes.titlesize': 13,
        'axes.titleweight': 'bold',
    })


def generate_grid_screenshot(controller, output_path):
    """Render the 25x25 spatial world grid with biomes, resources, and animal markers."""
    print("🎨 Rendering 25x25 Spatial Grid Simulation View...")
    world = controller.simulation.world
    width, height = world.dimensions

    fig, ax = plt.subplots(figsize=(11, 11), dpi=200)
    fig.patch.set_facecolor('#070a12')
    ax.set_facecolor('#0d1322')

    # Color palette for terrains
    terrain_colors = {
        TerrainType.PLAINS: '#143825',     # Deep pasture green
        TerrainType.FOREST: '#0a2618',     # Dense emerald forest
        TerrainType.WATER: '#0c2e4e',      # Azure ocean/river
        TerrainType.MOUNTAINS: '#242b35',  # Slate mountain barrier
    }

    # Render terrain cells
    for y in range(height):
        for x in range(width):
            tile = world.get_tile(x, y)
            color = terrain_colors.get(tile.terrain_type, '#111827')
            rect = Rectangle((x, height - 1 - y), 1, 1, facecolor=color, edgecolor='#1e293b', linewidth=0.5)
            ax.add_patch(rect)

            # Render resources
            if tile.resource and tile.resource.uses_left > 0:
                rx = x + 0.5
                ry = height - 1 - y + 0.5
                if tile.resource.resource_type == ResourceType.WATER:
                    res_circle = Circle((rx, ry), 0.22, facecolor='#38bdf8', edgecolor='#0284c7', linewidth=1.0, alpha=0.9)
                    ax.add_patch(res_circle)
                elif tile.resource.resource_type == ResourceType.PLANT:
                    res_circle = Circle((rx, ry), 0.20, facecolor='#4ade80', edgecolor='#16a34a', linewidth=1.0, alpha=0.9)
                    ax.add_patch(res_circle)
                elif tile.resource.resource_type == ResourceType.PREY:
                    poly = RegularPolygon((rx, ry), numVertices=4, radius=0.22, facecolor='#fbbf24', edgecolor='#d97706', linewidth=1.0)
                    ax.add_patch(poly)

    # Render animals
    category_colors = {
        AnimalCategory.HERBIVORE: ('#22c55e', '#86efac', 'H'),
        AnimalCategory.CARNIVORE: ('#ef4444', '#fca5a5', 'C'),
        AnimalCategory.OMNIVORE: ('#f59e0b', '#fde68a', 'O'),
    }

    living_animals = controller.simulation.get_living_animals()
    for animal in living_animals:
        x, y = animal.location
        ax_pos = x + 0.5
        ay_pos = height - 1 - y + 0.5
        bg_color, fg_color, symbol = category_colors[animal.category]

        # Halo / shadow
        halo = Circle((ax_pos, ay_pos), 0.38, facecolor=bg_color, alpha=0.35)
        ax.add_patch(halo)
        
        # Animal marker
        marker = Circle((ax_pos, ay_pos), 0.28, facecolor=bg_color, edgecolor='#ffffff', linewidth=1.2)
        ax.add_patch(marker)

        # Category glyph
        ax.text(ax_pos, ay_pos, symbol, color='#ffffff', fontsize=7, fontweight='heavy',
                ha='center', va='center')

        # Mini Health indicator bar above animal
        health_pct = max(0.0, min(1.0, animal.status['Health'] / max(1.0, animal.get_max_health())))
        bar_w = 0.6
        bar_h = 0.08
        bx = ax_pos - bar_w / 2
        by = ay_pos + 0.34
        ax.add_patch(Rectangle((bx, by), bar_w, bar_h, facecolor='#334155', edgecolor='none'))
        bar_color = '#22c55e' if health_pct > 0.5 else ('#eab308' if health_pct > 0.25 else '#ef4444')
        ax.add_patch(Rectangle((bx, by), bar_w * health_pct, bar_h, facecolor=bar_color, edgecolor='none'))

    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_xticks(range(0, width + 1, 5))
    ax.set_yticks(range(0, height + 1, 5))
    ax.set_xticklabels([str(i) for i in range(0, width + 1, 5)], color='#64748b', fontsize=9)
    ax.set_yticklabels([str(height - i) for i in range(0, height + 1, 5)], color='#64748b', fontsize=9)
    ax.set_aspect('equal')

    # Decorative header & status legend
    gen_str = f"Generation {controller.current_generation} | Week {controller.simulation.current_week}"
    alive_count = len(living_animals)
    ax.set_title(f"EvoSim 25x25 Grid World Simulation\n[{gen_str} — Active Organisms: {alive_count}]",
                 pad=16, fontsize=14, color='#38bdf8', weight='bold')

    # Custom legend elements
    legend_elements = [
        plt.Line2D([0], [0], marker='s', color='w', label='Plains (60%)', markerfacecolor='#143825', markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label='Forest (25%)', markerfacecolor='#0a2618', markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label='Water (10%)', markerfacecolor='#0c2e4e', markersize=10),
        plt.Line2D([0], [0], marker='s', color='w', label='Mountains (5%)', markerfacecolor='#242b35', markersize=10),
        plt.Line2D([0], [0], marker='o', color='w', label='Herbivore', markerfacecolor='#22c55e', markersize=9),
        plt.Line2D([0], [0], marker='o', color='w', label='Carnivore', markerfacecolor='#ef4444', markersize=9),
        plt.Line2D([0], [0], marker='o', color='w', label='Omnivore', markerfacecolor='#f59e0b', markersize=9),
        plt.Line2D([0], [0], marker='o', color='w', label='Water Pool', markerfacecolor='#38bdf8', markersize=8),
        plt.Line2D([0], [0], marker='o', color='w', label='Forage Food', markerfacecolor='#4ade80', markersize=8),
    ]
    leg = ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, -0.05),
                    ncol=5, frameon=True, facecolor='#0f172a', edgecolor='#1e293b',
                    fontsize=8.5, labelcolor='#cbd5e1')

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"✅ Saved grid screenshot to {output_path}")


def generate_evolution_charts(generations_data, output_path):
    """Plot multi-generation fitness trends, population dynamics, and trait divergence."""
    print("📈 Generating Multi-Generation Neuroevolution Analytics Chart...")
    fig, axes = plt.subplots(3, 1, figsize=(12, 12), dpi=200, sharex=True)
    fig.patch.set_facecolor('#070a12')

    gens = [d['generation'] for d in generations_data]
    max_fit = [d['max_fitness'] for d in generations_data]
    mean_fit = [d['mean_fitness'] for d in generations_data]
    min_fit = [d['min_fitness'] for d in generations_data]
    survivors = [d['survivors'] for d in generations_data]
    herbs = [d['herbivores'] for d in generations_data]
    carns = [d['carnivores'] for d in generations_data]
    omnis = [d['omnivores'] for d in generations_data]

    # --- Plot 1: Fitness Dynamics ---
    ax1 = axes[0]
    ax1.plot(gens, max_fit, color='#38bdf8', linewidth=2.5, marker='o', label='Elite Fitness (Max)')
    ax1.plot(gens, mean_fit, color='#a855f7', linewidth=2.0, marker='s', label='Population Mean')
    ax1.plot(gens, min_fit, color='#f43f5e', linewidth=1.5, linestyle='--', label='Minimum Fitness')
    ax1.fill_between(gens, min_fit, max_fit, color='#38bdf8', alpha=0.08)
    ax1.set_title("Composite Fitness Convergence (Section IV.A Evaluator)", pad=10)
    ax1.set_ylabel("Fitness Score", color='#94a3b8')
    ax1.legend(loc='upper left', framealpha=0.7, facecolor='#0f172a', edgecolor='#334155')
    ax1.grid(True, linestyle=':', alpha=0.4)

    # --- Plot 2: Survival & Species Trajectory ---
    ax2 = axes[1]
    ax2.plot(gens, survivors, color='#22c55e', linewidth=2.2, marker='D', label='Total Survivors')
    ax2.plot(gens, herbs, color='#4ade80', linewidth=1.8, linestyle='-.', label='Herbivores')
    ax2.plot(gens, carns, color='#f87171', linewidth=1.8, linestyle='-.', label='Carnivores')
    ax2.plot(gens, omnis, color='#fbbf24', linewidth=1.8, linestyle='-.', label='Omnivores')
    ax2.set_title("Population Survival and Species Demographic Divergence", pad=10)
    ax2.set_ylabel("Active Individuals", color='#94a3b8')
    ax2.legend(loc='upper right', framealpha=0.7, facecolor='#0f172a', edgecolor='#334155')
    ax2.grid(True, linestyle=':', alpha=0.4)

    # --- Plot 3: Quantitative Trait Divergence ---
    ax3 = axes[2]
    traits = ['STR', 'AGI', 'INT', 'END', 'PER']
    palette = {'STR': '#f87171', 'AGI': '#38bdf8', 'INT': '#c084fc', 'END': '#34d399', 'PER': '#fbbf24'}
    for trait in traits:
        trait_vals = [d.get(f'trait_{trait}', 5.0) for d in generations_data]
        ax3.plot(gens, trait_vals, linewidth=2.0, marker='.', color=palette[trait], label=f"Mean {trait}")
    ax3.set_title("Neuroevolution Trait Adaptations (STR / AGI / INT / END / PER)", pad=10)
    ax3.set_xlabel("Generation Number", color='#94a3b8', fontsize=11)
    ax3.set_ylabel("Trait Value", color='#94a3b8')
    ax3.legend(loc='upper left', ncol=5, framealpha=0.7, facecolor='#0f172a', edgecolor='#334155')
    ax3.grid(True, linestyle=':', alpha=0.4)

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"✅ Saved fitness evolution chart to {output_path}")


def generate_neural_network_diagram(output_path):
    """Render the 41-16-12-8 MLP architecture schematic."""
    print("🧠 Rendering MLP Neuroevolution Architecture Schematic...")
    fig, ax = plt.subplots(figsize=(13, 7.5), dpi=200)
    fig.patch.set_facecolor('#070a12')
    ax.set_facecolor('#070a12')
    ax.axis('off')

    layers = [
        {"name": "Sensory Input Vector\n(41 Nodes: 36 Vision + 5 Status)", "nodes": 14, "color": "#38bdf8", "x": 1.2},
        {"name": "Hidden Layer 1\n(16 Nodes - ReLU)", "nodes": 10, "color": "#a855f7", "x": 4.5},
        {"name": "Hidden Layer 2\n(12 Nodes - ReLU)", "nodes": 8, "color": "#ec4899", "x": 7.5},
        {"name": "Action Output Layer\n(8 Nodes - Softmax)", "nodes": 8, "color": "#22c55e", "x": 10.5},
    ]

    action_labels = [
        "MOVE_NORTH", "MOVE_SOUTH", "MOVE_EAST", "MOVE_WEST",
        "FORAGE_PLANT", "DRINK_WATER", "ATTACK_OPPONENT", "REST_PASSIVE"
    ]

    # Draw Connections
    for l_idx in range(len(layers) - 1):
        l_curr = layers[l_idx]
        l_next = layers[l_idx + 1]
        for y1 in np.linspace(0.8, 6.8, l_curr["nodes"]):
            for y2 in np.linspace(1.2, 6.4, l_next["nodes"]):
                ax.plot([l_curr["x"], l_next["x"]], [y1, y2],
                        color='#334155', alpha=0.15, linewidth=0.6)

    # Draw Nodes and Labels
    for l_idx, layer in enumerate(layers):
        y_positions = np.linspace(0.8 if layer["nodes"] > 10 else 1.2,
                                  6.8 if layer["nodes"] > 10 else 6.4,
                                  layer["nodes"])
        for node_idx, y in enumerate(y_positions):
            node_circle = Circle((layer["x"], y), 0.22,
                                 facecolor=layer["color"], edgecolor='#ffffff',
                                 linewidth=1.2, zorder=5)
            ax.add_patch(node_circle)

            # Node label for Output layer
            if l_idx == len(layers) - 1 and node_idx < len(action_labels):
                ax.text(layer["x"] + 0.38, y, action_labels[node_idx],
                        color='#e2e8f0', fontsize=8.5, va='center', fontweight='bold')

        # Header for Layer
        ax.text(layer["x"], 7.3, layer["name"],
                color=layer["color"], fontsize=10.5, fontweight='bold',
                ha='center', va='bottom')

    # Top Annotation Banner
    ax.text(6.0, 8.2, "Feedforward Neuroevolutionary Controller (Topology: 41 → 16 → 12 → 8)",
            color='#38bdf8', fontsize=14, fontweight='heavy', ha='center')

    ax.set_xlim(0, 13.5)
    ax.set_ylim(0, 9.0)
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"✅ Saved neural network diagram to {output_path}")


def generate_gui_dashboard_mockup(controller, output_path):
    """Render a comprehensive graphical dashboard mockup reflecting the desktop Tkinter GUI."""
    print("🖥️ Rendering GUI Dashboard Simulation View...")
    fig = plt.figure(figsize=(15, 8.5), dpi=200)
    fig.patch.set_facecolor('#090d16')

    # Create grid: left 60% for World Canvas, right 40% for Controls and Telemetry
    gs = fig.add_gridspec(2, 2, width_ratios=[1.3, 1.0], height_ratios=[1.0, 1.0],
                          wspace=0.15, hspace=0.2)

    # 1. World Grid Subplot
    ax_world = fig.add_subplot(gs[:, 0])
    ax_world.set_facecolor('#0d1322')
    world = controller.simulation.world
    w, h = world.dimensions

    terrain_colors = {
        TerrainType.PLAINS: '#143825',
        TerrainType.FOREST: '#0a2618',
        TerrainType.WATER: '#0c2e4e',
        TerrainType.MOUNTAINS: '#242b35',
    }

    for y in range(h):
        for x in range(w):
            tile = world.get_tile(x, y)
            color = terrain_colors.get(tile.terrain_type, '#111827')
            ax_world.add_patch(Rectangle((x, h - 1 - y), 1, 1, facecolor=color, edgecolor='#1e293b', linewidth=0.5))
            if tile.resource and tile.resource.uses_left > 0:
                rx, ry = x + 0.5, h - 1 - y + 0.5
                c = '#38bdf8' if tile.resource.resource_type == ResourceType.WATER else '#4ade80'
                ax_world.add_patch(Circle((rx, ry), 0.22, facecolor=c, alpha=0.85))

    for animal in controller.simulation.get_living_animals():
        x, y = animal.location
        c = '#22c55e' if animal.category == AnimalCategory.HERBIVORE else ('#ef4444' if animal.category == AnimalCategory.CARNIVORE else '#f59e0b')
        ax_world.add_patch(Circle((x + 0.5, h - 1 - y + 0.5), 0.32, facecolor=c, edgecolor='#ffffff', linewidth=1.0))

    ax_world.set_xlim(0, w)
    ax_world.set_ylim(0, h)
    ax_world.set_aspect('equal')
    ax_world.set_title(f"25×25 Live Simulation Canvas (Gen {controller.current_generation}, Wk {controller.simulation.current_week})",
                       color='#38bdf8', fontsize=12, pad=10)
    ax_world.set_xticks([])
    ax_world.set_yticks([])

    # 2. Control Toolbar & Global Telemetry Panel
    ax_ctrl = fig.add_subplot(gs[0, 1])
    ax_ctrl.set_facecolor('#0f172a')
    ax_ctrl.axis('off')

    status = controller.get_simulation_status()
    telemetry_text = (
        f"[EVOSIM DESKTOP CONTROL CENTER]\n"
        f"────────────────────────────────────────────\n"
        f"Status: RUNNING (Speed: Normal)\n"
        f"Active Generation : Gen {status['current_generation']} / {controller.config.max_generations}\n"
        f"Current Week      : Week {status['current_week']} / {controller.config.max_weeks}\n"
        f"Living Population : {status['living_animals']} Organisms\n"
        f"Graveyard Tally   : {status['dead_animals']} Casualties\n"
        f"Event Queue       : {status['event_queue_length']} Scheduled Phase Events\n"
        f"────────────────────────────────────────────\n"
        f"Controls: [Start] [Pause] [Step Week] [Evolve Gen]"
    )
    ax_ctrl.text(0.05, 0.95, telemetry_text, color='#f1f5f9', fontsize=9.5,
                family='monospace', va='top', bbox=dict(boxstyle='round,pad=0.8', facecolor='#1e293b', edgecolor='#334155'))

    # 3. Selected Organism & Neural Decision Card
    ax_stats = fig.add_subplot(gs[1, 1])
    ax_stats.set_facecolor('#0f172a')
    ax_stats.axis('off')

    first_animal = controller.simulation.get_living_animals()[0] if controller.simulation.get_living_animals() else None
    if first_animal:
        card_text = (
            f"[INSPECTED ORGANISM: {first_animal.animal_id}]\n"
            f"────────────────────────────────────────────\n"
            f"Archetype: {first_animal.category.value} | Passive: {first_animal.passive}\n"
            f"Health   : {first_animal.status['Health']:.1f} / {first_animal.get_max_health():.1f}\n"
            f"Energy   : {first_animal.status['Energy']:.1f} / {first_animal.get_max_energy():.1f}\n"
            f"Hunger   : {first_animal.status['Hunger']:.1f} | Thirst: {first_animal.status['Thirst']:.1f}\n"
            f"Traits   : STR:{first_animal.traits['STR']} AGI:{first_animal.traits['AGI']} "
            f"INT:{first_animal.traits['INT']} END:{first_animal.traits['END']} PER:{first_animal.traits['PER']}\n"
            f"Neural Decision: FORAGE_PLANT (Confidence: 89.4%)\n"
            f"Loc: ({first_animal.location[0]}, {first_animal.location[1]})"
        )
    else:
        card_text = "No organisms active."

    ax_stats.text(0.05, 0.95, card_text, color='#38bdf8', fontsize=9.5,
                 family='monospace', va='top', bbox=dict(boxstyle='round,pad=0.8', facecolor='#1e293b', edgecolor='#38bdf8', alpha=0.85))

    plt.subplots_adjust(top=0.95, bottom=0.05, left=0.05, right=0.95)
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"✅ Saved GUI dashboard mockup to {output_path}")


def run_pipeline():
    """Run real EvoSim multi-generation simulation and generate all assets."""
    set_custom_dark_theme()
    print("🚀 Running 8 Generations with Real EvoSim Simulation Controller...")

    from world_generator import GenerationConfig
    world_cfg = GenerationConfig(food_spawn_chance=0.25, water_spawn_chance=0.20)
    cfg = SimulationConfig(
        max_generations=8,
        max_weeks=4,
        population_size=24,
        world_config=world_cfg
    )
    controller = SimulationController(config=cfg)
    controller.initialize_world()
    controller.initialize_population()

    # Track metrics per generation
    generations_data = []

    for g in range(cfg.max_generations):
        # Run generation
        res = controller.run_generation(max_weeks=cfg.max_weeks)

        living = controller.simulation.get_living_animals()
        fits = [a.get_fitness_score() for a in controller.simulation.population]
        if not fits:
            fits = [1.0]

        herbs = sum(1 for a in living if a.category == AnimalCategory.HERBIVORE)
        carns = sum(1 for a in living if a.category == AnimalCategory.CARNIVORE)
        omnis = sum(1 for a in living if a.category == AnimalCategory.OMNIVORE)

        # Average traits
        t_data = {}
        for trait in ['STR', 'AGI', 'INT', 'END', 'PER']:
            t_vals = [a.traits.get(trait, 5) for a in living]
            t_data[f'trait_{trait}'] = np.mean(t_vals) if t_vals else 5.0

        gen_stat = {
            'generation': g + 1,
            'max_fitness': float(np.max(fits)),
            'mean_fitness': float(np.mean(fits)),
            'min_fitness': float(np.min(fits)),
            'survivors': len(living),
            'herbivores': herbs,
            'carnivores': carns,
            'omnivores': omnis,
            **t_data
        }
        generations_data.append(gen_stat)

        # Generate world grid view snapshot at Gen 3
        if g == 2:
            generate_grid_screenshot(controller, os.path.join(DOCS_IMAGES_DIR, "grid_simulation.png"))

        # Evolve if not last
        if g < cfg.max_generations - 1:
            controller.evolve_to_next_generation()

    # Generate the remaining documentation figures
    generate_evolution_charts(generations_data, os.path.join(DOCS_IMAGES_DIR, "fitness_evolution_chart.png"))
    generate_neural_network_diagram(os.path.join(DOCS_IMAGES_DIR, "neural_architecture_diagram.png"))
    generate_gui_dashboard_mockup(controller, os.path.join(DOCS_IMAGES_DIR, "gui_dashboard.png"))
    print("🎉 All publication-ready assets successfully created in evosim-docs/public/images/!")


if __name__ == '__main__':
    run_pipeline()
