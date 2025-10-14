"""
Main GUI Application for Evolutionary Simulation

This module implements the main user interface using tkinter,
providing interactive controls and real-time visualization.

Author: Zen Garden
University of Caloocan City
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import json
from typing import Dict, Any, Optional

from src.simulation import Simulation, SimulationState
from src.environment import GridWorld
from src.events import EventManager
from src.evolution import Population, EvolutionManager
from analysis.statistics import StatisticsCollector
from analysis.visualization import SimulationVisualizer, create_visualization_window


class SimulationGUI:
    """
    Main GUI application for the evolutionary simulation.
    
    Provides:
    - Configuration interface
    - Real-time visualization
    - Control panel
    - Statistics display
    - Data export
    """
    
    def __init__(self):
        """Initialize the GUI application."""
        self.root = tk.Tk()
        self.root.title("Evolutionary Simulation - Educational AI Project")
        self.root.geometry("1600x800")
        self.root.configure(bg='#f0f0f0')
        
        # Simulation components
        self.simulation: Optional[Simulation] = None
        self.simulation_thread: Optional[threading.Thread] = None
        self.statistics_collector: StatisticsCollector = StatisticsCollector()
        self.visualizer: SimulationVisualizer = SimulationVisualizer()
        
        # GUI components
        self.config_frame = None
        self.visualization_frame = None
        self.control_frame = None
        self.stats_frame = None
        self.animals_frame = None
        
        # Configuration variables
        self.config_vars = self._create_config_variables()
        
        # Statistics variables
        self.stats_vars = self._create_stats_variables()
        
        # Visualization
        self.canvas = None
        self.grid_size = 20
        self.cell_size = 20
        
        # Setup GUI
        self._setup_gui()
        self._setup_bindings()
        
        # Update timer
        self.update_timer = None
        self._schedule_update()
    
    def _create_config_variables(self) -> Dict[str, tk.Variable]:
        """Create configuration variables."""
        return {
            'grid_width': tk.IntVar(value=20),
            'grid_height': tk.IntVar(value=20),
            'population_size': tk.IntVar(value=30),
            'max_generations': tk.IntVar(value=5),
            'steps_per_generation': tk.IntVar(value=100),
            'simulation_speed': tk.DoubleVar(value=1.0),
            'food_density': tk.DoubleVar(value=0.15),
            'water_density': tk.DoubleVar(value=0.15),
                'drought_probability': tk.DoubleVar(value=0.01),
                'storm_probability': tk.DoubleVar(value=0.01),
                'famine_probability': tk.DoubleVar(value=0.01),
                'bonus_probability': tk.DoubleVar(value=0.01),
            'mutation_rate': tk.DoubleVar(value=0.05),
            'crossover_rate': tk.DoubleVar(value=0.7),
            'selection_method': tk.StringVar(value='tournament'),
            'tournament_size': tk.IntVar(value=3),
            'elite_percentage': tk.DoubleVar(value=0.2)
        }
    
    def _create_stats_variables(self) -> Dict[str, tk.StringVar]:
        """Create statistics variables."""
        return {
            'state': tk.StringVar(value='Stopped'),
            'current_step': tk.StringVar(value='0'),
            'current_generation': tk.StringVar(value='0'),
            'alive_animals': tk.StringVar(value='0'),
            'dead_animals': tk.StringVar(value='0'),
            'survival_rate': tk.StringVar(value='0.0%'),
            'average_fitness': tk.StringVar(value='0.0'),
            'best_fitness': tk.StringVar(value='0.0'),
            'active_events': tk.StringVar(value='None'),
            'food_count': tk.StringVar(value='0'),
            'water_count': tk.StringVar(value='0')
        }
    
    def _setup_gui(self):
        """Setup the GUI layout."""
        # Create main frames
        self._create_config_frame()
        self._create_visualization_frame()
        self._create_control_frame()
        self._create_stats_frame()
        self._create_animals_frame()
        
        # Layout frames
        self.config_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.visualization_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        self.control_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        self.stats_frame.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        self.animals_frame.grid(row=0, column=2, rowspan=2, sticky='nsew', padx=5, pady=5)
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
    
    def _create_config_frame(self):
        """Create configuration frame."""
        self.config_frame = ttk.LabelFrame(self.root, text="Configuration", padding=10)
        
        # Grid configuration
        ttk.Label(self.config_frame, text="Grid Size:").grid(row=0, column=0, sticky='w')
        ttk.Entry(self.config_frame, textvariable=self.config_vars['grid_width'], width=5).grid(row=0, column=1, padx=5)
        ttk.Label(self.config_frame, text="x").grid(row=0, column=2)
        ttk.Entry(self.config_frame, textvariable=self.config_vars['grid_height'], width=5).grid(row=0, column=3, padx=5)
        
        # Population configuration
        ttk.Label(self.config_frame, text="Population Size:").grid(row=1, column=0, sticky='w')
        ttk.Entry(self.config_frame, textvariable=self.config_vars['population_size'], width=10).grid(row=1, column=1, columnspan=3, sticky='w', padx=5)
        
        # Simulation configuration
        ttk.Label(self.config_frame, text="Max Generations:").grid(row=2, column=0, sticky='w')
        ttk.Entry(self.config_frame, textvariable=self.config_vars['max_generations'], width=10).grid(row=2, column=1, columnspan=3, sticky='w', padx=5)
        
        ttk.Label(self.config_frame, text="Steps per Generation:").grid(row=3, column=0, sticky='w')
        ttk.Entry(self.config_frame, textvariable=self.config_vars['steps_per_generation'], width=10).grid(row=3, column=1, columnspan=3, sticky='w', padx=5)
        
        ttk.Label(self.config_frame, text="Simulation Speed:").grid(row=4, column=0, sticky='w')
        speed_frame = ttk.Frame(self.config_frame)
        speed_frame.grid(row=4, column=1, columnspan=3, sticky='w', padx=5)
        ttk.Scale(speed_frame, from_=0.1, to=10.0, variable=self.config_vars['simulation_speed'], 
                 orient='horizontal', length=120, command=lambda v: self._update_slider_label('simulation_speed', v)).grid(row=0, column=0)
        self.speed_entry = ttk.Entry(speed_frame, textvariable=self.config_vars['simulation_speed'], width=8)
        self.speed_entry.grid(row=0, column=1, padx=5)
        self.speed_entry.bind('<Return>', lambda e: self._update_slider_from_entry('simulation_speed'))
        
        # Resource configuration
        ttk.Label(self.config_frame, text="Food Density:").grid(row=5, column=0, sticky='w')
        food_frame = ttk.Frame(self.config_frame)
        food_frame.grid(row=5, column=1, columnspan=3, sticky='w', padx=5)
        ttk.Scale(food_frame, from_=0.0, to=0.5, variable=self.config_vars['food_density'], 
                 orient='horizontal', length=120, command=lambda v: self._update_slider_label('food_density', v)).grid(row=0, column=0)
        self.food_entry = ttk.Entry(food_frame, textvariable=self.config_vars['food_density'], width=8)
        self.food_entry.grid(row=0, column=1, padx=5)
        self.food_entry.bind('<Return>', lambda e: self._update_slider_from_entry('food_density'))
        
        ttk.Label(self.config_frame, text="Water Density:").grid(row=6, column=0, sticky='w')
        water_frame = ttk.Frame(self.config_frame)
        water_frame.grid(row=6, column=1, columnspan=3, sticky='w', padx=5)
        ttk.Scale(water_frame, from_=0.0, to=0.5, variable=self.config_vars['water_density'], 
                 orient='horizontal', length=120, command=lambda v: self._update_slider_label('water_density', v)).grid(row=0, column=0)
        self.water_entry = ttk.Entry(water_frame, textvariable=self.config_vars['water_density'], width=8)
        self.water_entry.grid(row=0, column=1, padx=5)
        self.water_entry.bind('<Return>', lambda e: self._update_slider_from_entry('water_density'))
        
        # Event configuration
        ttk.Label(self.config_frame, text="Drought Probability:").grid(row=7, column=0, sticky='w')
        drought_frame = ttk.Frame(self.config_frame)
        drought_frame.grid(row=7, column=1, columnspan=3, sticky='w', padx=5)
        ttk.Scale(drought_frame, from_=0.0, to=1.0, variable=self.config_vars['drought_probability'], 
                 orient='horizontal', length=120, command=lambda v: self._update_slider_label('drought_probability', v)).grid(row=0, column=0)
        self.drought_entry = ttk.Entry(drought_frame, textvariable=self.config_vars['drought_probability'], width=8)
        self.drought_entry.grid(row=0, column=1, padx=5)
        self.drought_entry.bind('<Return>', lambda e: self._update_slider_from_entry('drought_probability'))
        
        ttk.Label(self.config_frame, text="Storm Probability:").grid(row=8, column=0, sticky='w')
        storm_frame = ttk.Frame(self.config_frame)
        storm_frame.grid(row=8, column=1, columnspan=3, sticky='w', padx=5)
        ttk.Scale(storm_frame, from_=0.0, to=1.0, variable=self.config_vars['storm_probability'], 
                 orient='horizontal', length=120, command=lambda v: self._update_slider_label('storm_probability', v)).grid(row=0, column=0)
        self.storm_entry = ttk.Entry(storm_frame, textvariable=self.config_vars['storm_probability'], width=8)
        self.storm_entry.grid(row=0, column=1, padx=5)
        self.storm_entry.bind('<Return>', lambda e: self._update_slider_from_entry('storm_probability'))
        
        ttk.Label(self.config_frame, text="Famine Probability:").grid(row=9, column=0, sticky='w')
        famine_frame = ttk.Frame(self.config_frame)
        famine_frame.grid(row=9, column=1, columnspan=3, sticky='w', padx=5)
        ttk.Scale(famine_frame, from_=0.0, to=1.0, variable=self.config_vars['famine_probability'], 
                 orient='horizontal', length=120, command=lambda v: self._update_slider_label('famine_probability', v)).grid(row=0, column=0)
        self.famine_entry = ttk.Entry(famine_frame, textvariable=self.config_vars['famine_probability'], width=8)
        self.famine_entry.grid(row=0, column=1, padx=5)
        self.famine_entry.bind('<Return>', lambda e: self._update_slider_from_entry('famine_probability'))
        
        ttk.Label(self.config_frame, text="Bonus Probability:").grid(row=10, column=0, sticky='w')
        bonus_frame = ttk.Frame(self.config_frame)
        bonus_frame.grid(row=10, column=1, columnspan=3, sticky='w', padx=5)
        ttk.Scale(bonus_frame, from_=0.0, to=1.0, variable=self.config_vars['bonus_probability'], 
                 orient='horizontal', length=120, command=lambda v: self._update_slider_label('bonus_probability', v)).grid(row=0, column=0)
        self.bonus_entry = ttk.Entry(bonus_frame, textvariable=self.config_vars['bonus_probability'], width=8)
        self.bonus_entry.grid(row=0, column=1, padx=5)
        self.bonus_entry.bind('<Return>', lambda e: self._update_slider_from_entry('bonus_probability'))
        
        # Evolution configuration
        ttk.Label(self.config_frame, text="Mutation Rate:").grid(row=11, column=0, sticky='w')
        mutation_frame = ttk.Frame(self.config_frame)
        mutation_frame.grid(row=11, column=1, columnspan=3, sticky='w', padx=5)
        ttk.Scale(mutation_frame, from_=0.0, to=1.0, variable=self.config_vars['mutation_rate'], 
                 orient='horizontal', length=120, command=lambda v: self._update_slider_label('mutation_rate', v)).grid(row=0, column=0)
        self.mutation_entry = ttk.Entry(mutation_frame, textvariable=self.config_vars['mutation_rate'], width=8)
        self.mutation_entry.grid(row=0, column=1, padx=5)
        self.mutation_entry.bind('<Return>', lambda e: self._update_slider_from_entry('mutation_rate'))
        
        ttk.Label(self.config_frame, text="Crossover Rate:").grid(row=12, column=0, sticky='w')
        crossover_frame = ttk.Frame(self.config_frame)
        crossover_frame.grid(row=12, column=1, columnspan=3, sticky='w', padx=5)
        ttk.Scale(crossover_frame, from_=0.0, to=1.0, variable=self.config_vars['crossover_rate'], 
                 orient='horizontal', length=120, command=lambda v: self._update_slider_label('crossover_rate', v)).grid(row=0, column=0)
        self.crossover_entry = ttk.Entry(crossover_frame, textvariable=self.config_vars['crossover_rate'], width=8)
        self.crossover_entry.grid(row=0, column=1, padx=5)
        self.crossover_entry.bind('<Return>', lambda e: self._update_slider_from_entry('crossover_rate'))
        
        # Selection method
        ttk.Label(self.config_frame, text="Selection Method:").grid(row=13, column=0, sticky='w')
        selection_combo = ttk.Combobox(self.config_frame, textvariable=self.config_vars['selection_method'], 
                                     values=['tournament', 'roulette', 'rank'], state='readonly', width=15)
        selection_combo.grid(row=13, column=1, columnspan=3, sticky='w', padx=5)
        
        # Buttons
        ttk.Button(self.config_frame, text="Initialize", command=self._initialize_simulation).grid(row=14, column=0, pady=10)
        ttk.Button(self.config_frame, text="Load Config", command=self._load_config).grid(row=14, column=1, pady=10)
        ttk.Button(self.config_frame, text="Save Config", command=self._save_config).grid(row=14, column=2, pady=10)
        ttk.Button(self.config_frame, text="Reset", command=self._reset_config).grid(row=14, column=3, pady=10)
    
    def _create_visualization_frame(self):
        """Create visualization frame."""
        self.visualization_frame = ttk.LabelFrame(self.root, text="Simulation Visualization", padding=10)
        
        # Canvas for grid visualization
        self.canvas = tk.Canvas(self.visualization_frame, width=400, height=400, bg='white', relief='sunken', bd=2)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(self.visualization_frame, orient='vertical', command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(self.visualization_frame, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configure grid
        self.visualization_frame.grid_rowconfigure(0, weight=1)
        self.visualization_frame.grid_columnconfigure(0, weight=1)
        
        # Legend
        legend_frame = ttk.Frame(self.visualization_frame)
        legend_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=5)
        
        ttk.Label(legend_frame, text="Legend:").grid(row=0, column=0, sticky='w')
        ttk.Label(legend_frame, text="🟢 Animal", foreground='green').grid(row=0, column=1, sticky='w', padx=10)
        ttk.Label(legend_frame, text="🍎 Food", foreground='red').grid(row=0, column=2, sticky='w', padx=10)
        ttk.Label(legend_frame, text="💧 Water", foreground='blue').grid(row=0, column=3, sticky='w', padx=10)
        ttk.Label(legend_frame, text="⚡ Event", foreground='orange').grid(row=0, column=4, sticky='w', padx=10)
    
    def _create_control_frame(self):
        """Create control frame."""
        self.control_frame = ttk.LabelFrame(self.root, text="Simulation Control", padding=10)
        
        # Control buttons
        self.start_button = ttk.Button(self.control_frame, text="Start", command=self._start_simulation)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.pause_button = ttk.Button(self.control_frame, text="Pause", command=self._pause_simulation, state='disabled')
        self.pause_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.resume_button = ttk.Button(self.control_frame, text="Resume", command=self._resume_simulation, state='disabled')
        self.resume_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.stop_button = ttk.Button(self.control_frame, text="Stop", command=self._stop_simulation, state='disabled')
        self.stop_button.grid(row=0, column=3, padx=5, pady=5)
        
        self.reset_button = ttk.Button(self.control_frame, text="Reset", command=self._reset_simulation, state='disabled')
        self.reset_button.grid(row=0, column=4, padx=5, pady=5)
        
        # Speed control
        ttk.Label(self.control_frame, text="Speed:").grid(row=1, column=0, sticky='w', pady=5)
        self.speed_scale = ttk.Scale(self.control_frame, from_=0.1, to=10.0, orient='horizontal', length=200)
        self.speed_scale.grid(row=1, column=1, columnspan=3, sticky='w', padx=5)
        self.speed_scale.set(1.0)
        self.speed_scale.configure(command=self._update_speed)
        
        # Export buttons
        ttk.Button(self.control_frame, text="Export Data", command=self._export_data).grid(row=2, column=0, padx=5, pady=5)
        ttk.Button(self.control_frame, text="Export Config", command=self._export_config).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(self.control_frame, text="View Charts", command=self._view_charts).grid(row=2, column=2, padx=5, pady=5)
        ttk.Button(self.control_frame, text="Export Report", command=self._export_report).grid(row=2, column=3, padx=5, pady=5)
    
    def _create_stats_frame(self):
        """Create statistics frame."""
        self.stats_frame = ttk.LabelFrame(self.root, text="Statistics", padding=10)
        
        # Create statistics display
        stats_grid = ttk.Frame(self.stats_frame)
        stats_grid.grid(row=0, column=0, sticky='nsew')
        
        # Simulation state
        ttk.Label(stats_grid, text="State:").grid(row=0, column=0, sticky='w')
        ttk.Label(stats_grid, textvariable=self.stats_vars['state']).grid(row=0, column=1, sticky='w', padx=10)
        
        ttk.Label(stats_grid, text="Step:").grid(row=1, column=0, sticky='w')
        ttk.Label(stats_grid, textvariable=self.stats_vars['current_step']).grid(row=1, column=1, sticky='w', padx=10)
        
        ttk.Label(stats_grid, text="Generation:").grid(row=2, column=0, sticky='w')
        ttk.Label(stats_grid, textvariable=self.stats_vars['current_generation']).grid(row=2, column=1, sticky='w', padx=10)
        
        # Population statistics
        ttk.Label(stats_grid, text="Alive Animals:").grid(row=3, column=0, sticky='w')
        ttk.Label(stats_grid, textvariable=self.stats_vars['alive_animals']).grid(row=3, column=1, sticky='w', padx=10)
        
        ttk.Label(stats_grid, text="Dead Animals:").grid(row=4, column=0, sticky='w')
        ttk.Label(stats_grid, textvariable=self.stats_vars['dead_animals']).grid(row=4, column=1, sticky='w', padx=10)
        
        ttk.Label(stats_grid, text="Survival Rate:").grid(row=5, column=0, sticky='w')
        ttk.Label(stats_grid, textvariable=self.stats_vars['survival_rate']).grid(row=5, column=1, sticky='w', padx=10)
        
        # Fitness statistics
        ttk.Label(stats_grid, text="Average Fitness:").grid(row=6, column=0, sticky='w')
        ttk.Label(stats_grid, textvariable=self.stats_vars['average_fitness']).grid(row=6, column=1, sticky='w', padx=10)
        
        ttk.Label(stats_grid, text="Best Fitness:").grid(row=7, column=0, sticky='w')
        ttk.Label(stats_grid, textvariable=self.stats_vars['best_fitness']).grid(row=7, column=1, sticky='w', padx=10)
        
        # Environment statistics
        ttk.Label(stats_grid, text="Active Events:").grid(row=8, column=0, sticky='w')
        ttk.Label(stats_grid, textvariable=self.stats_vars['active_events']).grid(row=8, column=1, sticky='w', padx=10)
        
        ttk.Label(stats_grid, text="Food Count:").grid(row=9, column=0, sticky='w')
        ttk.Label(stats_grid, textvariable=self.stats_vars['food_count']).grid(row=9, column=1, sticky='w', padx=10)
        
        ttk.Label(stats_grid, text="Water Count:").grid(row=10, column=0, sticky='w')
        ttk.Label(stats_grid, textvariable=self.stats_vars['water_count']).grid(row=10, column=1, sticky='w', padx=10)
    
    def _create_animals_frame(self):
        """Create animals list frame."""
        self.animals_frame = ttk.LabelFrame(self.root, text="Animal Statistics", padding=10)
        
        # Create treeview for animal list with sortable columns
        columns = ('ID', 'Position', 'Status', 'Health', 'Age', 'Fitness', 'Actions', 'Resources')
        
        self.animals_tree = ttk.Treeview(self.animals_frame, columns=columns, show='headings', height=15)
        
        # Configure columns with sorting
        self.animals_tree.heading('ID', text='Animal ID', command=lambda: self._sort_animals('ID'))
        self.animals_tree.heading('Position', text='Position', command=lambda: self._sort_animals('Position'))
        self.animals_tree.heading('Status', text='Status', command=lambda: self._sort_animals('Status'))
        self.animals_tree.heading('Health', text='Health', command=lambda: self._sort_animals('Health'))
        self.animals_tree.heading('Age', text='Age', command=lambda: self._sort_animals('Age'))
        self.animals_tree.heading('Fitness', text='Fitness', command=lambda: self._sort_animals('Fitness'))
        self.animals_tree.heading('Actions', text='Actions', command=lambda: self._sort_animals('Actions'))
        self.animals_tree.heading('Resources', text='Resources', command=lambda: self._sort_animals('Resources'))
        
        # Set column widths
        self.animals_tree.column('ID', width=100)
        self.animals_tree.column('Position', width=80)
        self.animals_tree.column('Status', width=60)
        self.animals_tree.column('Health', width=120)
        self.animals_tree.column('Age', width=50)
        self.animals_tree.column('Fitness', width=80)
        self.animals_tree.column('Actions', width=120)
        self.animals_tree.column('Resources', width=100)
        
        # Add scrollbar
        animals_scrollbar = ttk.Scrollbar(self.animals_frame, orient='vertical', command=self.animals_tree.yview)
        self.animals_tree.configure(yscrollcommand=animals_scrollbar.set)
        
        # Grid layout
        self.animals_tree.grid(row=0, column=0, sticky='nsew')
        animals_scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Configure grid weights
        self.animals_frame.grid_rowconfigure(0, weight=1)
        self.animals_frame.grid_columnconfigure(0, weight=1)
        
        # Add control buttons
        buttons_frame = ttk.Frame(self.animals_frame)
        buttons_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=5)
        
        ttk.Button(buttons_frame, text="Refresh", command=self._refresh_animals_list).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Clear", command=self._clear_animals_list).grid(row=0, column=1, padx=5)
        ttk.Button(buttons_frame, text="Export", command=self._export_animals_data).grid(row=0, column=2, padx=5)
        ttk.Button(buttons_frame, text="Sort by Fitness", command=lambda: self._sort_animals('Fitness')).grid(row=0, column=3, padx=5)
        ttk.Button(buttons_frame, text="Sort by Age", command=lambda: self._sort_animals('Age')).grid(row=0, column=4, padx=5)
        
        # Track current sort order
        self.current_sort_column = 'Fitness'
        self.current_sort_reverse = True
        
        # Add search/filter frame
        search_frame = ttk.Frame(self.animals_frame)
        search_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=5)
        
        ttk.Label(search_frame, text="Search Animal ID:").grid(row=0, column=0, padx=5)
        self.animal_search_var = tk.StringVar()
        self.animal_search_entry = ttk.Entry(search_frame, textvariable=self.animal_search_var, width=20)
        self.animal_search_entry.grid(row=0, column=1, padx=5)
        self.animal_search_entry.bind('<KeyRelease>', self._filter_animals)
        
        ttk.Button(search_frame, text="Find", command=self._find_animal).grid(row=0, column=2, padx=5)
        ttk.Button(search_frame, text="Show Alive Only", command=self._filter_alive_only).grid(row=0, column=3, padx=5)
    
    def _setup_bindings(self):
        """Setup event bindings."""
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _update_slider_label(self, slider_name: str, value: str):
        """Update the slider label with its current value (now handled by entry fields)."""
        # This method is kept for compatibility but entry fields now handle the display
        pass
    
    def _update_slider_from_entry(self, slider_name: str):
        """Update slider position when user types in entry field."""
        try:
            var = self.config_vars[slider_name]
            value = float(var.get())
            
            # Clamp values to valid ranges
            if slider_name == 'simulation_speed':
                value = max(0.1, min(10.0, value))
            elif slider_name in ['food_density', 'water_density']:
                value = max(0.0, min(0.5, value))
            elif slider_name in ['drought_probability', 'storm_probability', 'famine_probability', 'bonus_probability', 'mutation_rate', 'crossover_rate']:
                value = max(0.0, min(1.0, value))
            
            # Update the variable
            var.set(value)
            
        except (ValueError, AttributeError):
            # Reset to current value if invalid input
            pass
    
    def _schedule_update(self):
        """Schedule periodic updates."""
        self._update_display()
        self.update_timer = self.root.after(100, self._schedule_update)  # Update every 100ms
    
    def _update_display(self):
        """Update the display with current simulation state."""
        if self.simulation is None:
            return
        
        # Update statistics
        stats = self.simulation.get_statistics()
        self.stats_vars['state'].set(stats['state'].title())
        self.stats_vars['current_step'].set(str(stats['current_step']))
        self.stats_vars['current_generation'].set(str(stats['current_generation']))
        
        # Update population statistics
        if 'population_stats' in stats:
            pop_stats = stats['population_stats']
            self.stats_vars['alive_animals'].set(str(pop_stats.get('alive_count', 0)))
            self.stats_vars['dead_animals'].set(str(pop_stats.get('dead_count', 0)))
            self.stats_vars['survival_rate'].set(f"{pop_stats.get('survival_rate', 0):.1%}")
            self.stats_vars['average_fitness'].set(f"{pop_stats.get('average_fitness', 0):.2f}")
            self.stats_vars['best_fitness'].set(f"{pop_stats.get('best_fitness', 0):.2f}")
        
        # Update environment statistics
        if 'environment_stats' in stats:
            env_stats = stats['environment_stats']
            self.stats_vars['food_count'].set(str(env_stats.get('food_count', 0)))
            self.stats_vars['water_count'].set(str(env_stats.get('water_count', 0)))
        
        # Update event statistics
        if 'event_stats' in stats:
            event_stats = stats['event_stats']
            active_events = event_stats.get('event_names', [])
            if active_events:
                self.stats_vars['active_events'].set(', '.join(active_events))
            else:
                self.stats_vars['active_events'].set('None')
        
        # Update visualization
        self._update_visualization()
        
        # Update animals list
        self._refresh_animals_list()
        
        # Update control buttons
        self._update_control_buttons()
    
    def _update_visualization(self):
        """Update the grid visualization."""
        if self.simulation is None or self.simulation.environment is None:
            return
        
        self.canvas.delete("all")
        
        # Get environment data
        env = self.simulation.environment
        width = env.width
        height = env.height
        
        # Calculate cell size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1 or canvas_height <= 1:
            return  # Canvas not ready
        
        cell_width = canvas_width // width
        cell_height = canvas_height // height
        self.cell_size = min(cell_width, cell_height, 20)
        
        # Get active events for visual indicators
        active_events = []
        if hasattr(self.simulation, 'environment') and hasattr(self.simulation.environment, 'event_manager'):
            active_events = self.simulation.environment.event_manager.get_active_events()
        
        # Draw grid
        for x in range(width):
            for y in range(height):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Get cell content
                content = env.get_cell_content(x, y)
                
                # Set cell color based on content
                if content == 'food':
                    color = 'red'
                elif content == 'water':
                    color = 'blue'
                elif content == 'animal':
                    color = 'green'
                else:
                    color = 'white'
                
                # Draw cell
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black', width=1)
                
                # Draw content indicator
                if content == 'food':
                    self.canvas.create_text(x1 + self.cell_size//2, y1 + self.cell_size//2, text='🍎', font=('Arial', 8))
                elif content == 'water':
                    self.canvas.create_text(x1 + self.cell_size//2, y1 + self.cell_size//2, text='💧', font=('Arial', 8))
                elif content == 'animal':
                    self.canvas.create_text(x1 + self.cell_size//2, y1 + self.cell_size//2, text='🟢', font=('Arial', 8))
                
                # Draw coordinates (every 5th cell to avoid clutter)
                if x % 5 == 0 and y % 5 == 0:
                    self.canvas.create_text(x1 + 2, y1 + 2, text=f"{x},{y}", font=('Arial', 6), fill='gray')
                
                # Draw event indicators
                if active_events:
                    for event in active_events:
                        if hasattr(event, 'name'):
                            if event.name == 'drought' and content == 'water':
                                # Drought reduces water availability
                                self.canvas.create_text(x1 + self.cell_size//2, y1 + self.cell_size//2, text='💧', font=('Arial', 6), fill='orange')
                            elif event.name == 'storm' and content == 'water':
                                # Storm increases water availability
                                self.canvas.create_text(x1 + self.cell_size//2, y1 + self.cell_size//2, text='💧', font=('Arial', 8), fill='lightblue')
                            elif event.name == 'famine' and content == 'food':
                                # Famine reduces food availability
                                self.canvas.create_text(x1 + self.cell_size//2, y1 + self.cell_size//2, text='🍎', font=('Arial', 6), fill='orange')
                            elif event.name == 'bonus' and (content == 'food' or content == 'water'):
                                # Bonus increases resource availability
                                self.canvas.create_text(x1 + self.cell_size//2, y1 + self.cell_size//2, text='✨', font=('Arial', 8), fill='yellow')
        
        # Update scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _update_control_buttons(self):
        """Update control button states."""
        if self.simulation is None:
            self.start_button.configure(state='disabled')
            self.pause_button.configure(state='disabled')
            self.resume_button.configure(state='disabled')
            self.stop_button.configure(state='disabled')
            self.reset_button.configure(state='disabled')
            return
        
        state = self.simulation.state
        
        if state == SimulationState.STOPPED:
            self.start_button.configure(state='normal')
            self.pause_button.configure(state='disabled')
            self.resume_button.configure(state='disabled')
            self.stop_button.configure(state='disabled')
            self.reset_button.configure(state='normal')
        elif state == SimulationState.RUNNING:
            self.start_button.configure(state='disabled')
            self.pause_button.configure(state='normal')
            self.resume_button.configure(state='disabled')
            self.stop_button.configure(state='normal')
            self.reset_button.configure(state='disabled')
        elif state == SimulationState.PAUSED:
            self.start_button.configure(state='disabled')
            self.pause_button.configure(state='disabled')
            self.resume_button.configure(state='normal')
            self.stop_button.configure(state='normal')
            self.reset_button.configure(state='disabled')
        else:  # EVOLVING or FINISHED
            self.start_button.configure(state='disabled')
            self.pause_button.configure(state='disabled')
            self.resume_button.configure(state='disabled')
            self.stop_button.configure(state='normal')
            self.reset_button.configure(state='normal')
    
    def _initialize_simulation(self):
        """Initialize the simulation with current configuration."""
        try:
            # Get configuration from GUI
            config = self._get_config_from_gui()
            
            # Create simulation
            self.simulation = Simulation(config)
            self.simulation.initialize()
            
            # Add callbacks for real-time updates
            self.simulation.add_step_callback(self._on_simulation_step)
            self.simulation.add_generation_callback(self._on_simulation_generation)
            self.simulation.add_state_change_callback(self._on_simulation_state_change)
            
            # Update grid size
            self.grid_size = max(config['grid_size'])
            
            messagebox.showinfo("Success", "Simulation initialized successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize simulation: {str(e)}")
    
    def _on_simulation_step(self, step_data):
        """Handle simulation step updates."""
        # Collect step data for statistics
        if self.statistics_collector.is_tracking():
            # Record step data (this will be used for trend analysis)
            pass
    
    def _on_simulation_generation(self, generation_data):
        """Handle simulation generation updates."""
        print(f"[DEBUG] GUI generation callback called with data: {generation_data}")
        # Record generation data for statistics
        if self.statistics_collector.is_tracking():
            print(f"[DEBUG] Statistics collector is tracking, recording generation data")
            # Extract data from generation_data
            generation = generation_data.get('generation', 0)
            population_stats = generation_data.get('population_stats', {})
            environment_stats = generation_data.get('environment_stats', {})
            event_stats = generation_data.get('event_stats', {})
            
            print(f"[DEBUG] Extracted data - gen:{generation}, pop:{len(population_stats)}, env:{len(environment_stats)}, events:{len(event_stats)}")
            
            self.statistics_collector.record_generation(
                generation, population_stats, environment_stats, event_stats
            )
        else:
            print(f"[DEBUG] Statistics collector is NOT tracking")
    
    def _on_simulation_state_change(self, old_state, new_state):
        """Handle simulation state changes."""
        # Update UI based on state changes
        pass
    
    def _get_config_from_gui(self) -> Dict[str, Any]:
        """Get configuration from GUI variables."""
        return {
            'grid_size': (self.config_vars['grid_width'].get(), self.config_vars['grid_height'].get()),
            'population_size': self.config_vars['population_size'].get(),
            'max_generations': self.config_vars['max_generations'].get(),
            'steps_per_generation': self.config_vars['steps_per_generation'].get(),
            'simulation_speed': self.config_vars['simulation_speed'].get(),
            'food_density': self.config_vars['food_density'].get(),
            'water_density': self.config_vars['water_density'].get(),
            'drought_probability': self.config_vars['drought_probability'].get(),
            'storm_probability': self.config_vars['storm_probability'].get(),
            'famine_probability': self.config_vars['famine_probability'].get(),
            'bonus_probability': self.config_vars['bonus_probability'].get(),
            'mutation_rate': self.config_vars['mutation_rate'].get(),
            'crossover_rate': self.config_vars['crossover_rate'].get(),
            'selection_method': self.config_vars['selection_method'].get(),
            'tournament_size': self.config_vars['tournament_size'].get(),
            'elite_percentage': self.config_vars['elite_percentage'].get()
        }
    
    def _start_simulation(self):
        """Start the simulation."""
        if self.simulation is None:
            messagebox.showerror("Error", "Please initialize simulation first!")
            return
        
        try:
            # Start statistics tracking
            self.statistics_collector.start_tracking()
            
            self.simulation.start()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start simulation: {str(e)}")
    
    def _pause_simulation(self):
        """Pause the simulation."""
        if self.simulation is None:
            return
        
        try:
            self.simulation.pause()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to pause simulation: {str(e)}")
    
    def _resume_simulation(self):
        """Resume the simulation."""
        if self.simulation is None:
            return
        
        try:
            self.simulation.resume()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to resume simulation: {str(e)}")
    
    def _stop_simulation(self):
        """Stop the simulation."""
        if self.simulation is None:
            return
        
        try:
            self.simulation.stop()
            # Stop statistics tracking
            self.statistics_collector.stop_tracking()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop simulation: {str(e)}")
    
    def _reset_simulation(self):
        """Reset the simulation."""
        if self.simulation is None:
            return
        
        try:
            self.simulation.reset()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset simulation: {str(e)}")
    
    def _update_speed(self, value):
        """Update simulation speed."""
        if self.simulation is None:
            return
        
        try:
            speed = float(value)
            self.simulation.set_simulation_speed(speed)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update speed: {str(e)}")
    
    def _load_config(self):
        """Load configuration from file."""
        filename = filedialog.askopenfilename(
            title="Load Configuration",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    config = json.load(f)
                
                # Update GUI variables
                for key, value in config.items():
                    if key in self.config_vars:
                        self.config_vars[key].set(value)
                
                messagebox.showinfo("Success", "Configuration loaded successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load configuration: {str(e)}")
    
    def _save_config(self):
        """Save configuration to file."""
        filename = filedialog.asksaveasfilename(
            title="Save Configuration",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                config = self._get_config_from_gui()
                
                with open(filename, 'w') as f:
                    json.dump(config, f, indent=2)
                
                messagebox.showinfo("Success", "Configuration saved successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
    
    def _reset_config(self):
        """Reset configuration to defaults."""
        # Reset to default values
        self.config_vars['grid_width'].set(20)
        self.config_vars['grid_height'].set(20)
        self.config_vars['population_size'].set(50)
        self.config_vars['max_generations'].set(5)
        self.config_vars['steps_per_generation'].set(1000)
        self.config_vars['simulation_speed'].set(1.0)
        self.config_vars['food_density'].set(0.1)
        self.config_vars['water_density'].set(0.1)
        self.config_vars['drought_probability'].set(0.2)
        self.config_vars['storm_probability'].set(0.1)
        self.config_vars['famine_probability'].set(0.15)
        self.config_vars['bonus_probability'].set(0.05)
        self.config_vars['mutation_rate'].set(0.1)
        self.config_vars['crossover_rate'].set(0.8)
        self.config_vars['selection_method'].set('tournament')
        self.config_vars['tournament_size'].set(3)
        self.config_vars['elite_percentage'].set(0.1)
    
    def _export_data(self):
        """Export simulation data."""
        if self.simulation is None:
            messagebox.showerror("Error", "No simulation to export!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Data",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                data = {
                    'statistics': self.simulation.get_statistics(),
                    'step_history': self.simulation.get_step_history(),
                    'generation_history': self.simulation.get_generation_history()
                }
                
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
                
                messagebox.showinfo("Success", "Data exported successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {str(e)}")
    
    def _export_config(self):
        """Export current configuration."""
        filename = filedialog.asksaveasfilename(
            title="Export Configuration",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                config = self._get_config_from_gui()
                
                with open(filename, 'w') as f:
                    json.dump(config, f, indent=2)
                
                messagebox.showinfo("Success", "Configuration exported successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export configuration: {str(e)}")
    
    def _save_screenshot(self):
        """Save visualization screenshot."""
        filename = filedialog.asksaveasfilename(
            title="Save Screenshot",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                # This would require PIL/Pillow for actual screenshot functionality
                messagebox.showinfo("Info", "Screenshot functionality requires PIL/Pillow library")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save screenshot: {str(e)}")
    
    def _view_charts(self):
        """View data visualization charts."""
        if self.simulation is None:
            messagebox.showerror("Error", "No simulation data to visualize!")
            return
        
        try:
            # Collect statistics data
            stats_data = {
                'fitness_scores': self.statistics_collector.get_fitness_trend(),
                'survival_rates': self.statistics_collector.get_survival_rate_trend(),
                'resource_consumption': self.statistics_collector.get_resource_consumption_trend(),
                'behavioral_patterns': self.statistics_collector.get_behavioral_pattern_trend(),
                'summary': self.statistics_collector.get_summary_statistics()
            }
            
            # Create visualization window
            create_visualization_window(stats_data, self.root)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create charts: {str(e)}")
    
    def _export_report(self):
        """Export simulation report."""
        if self.simulation is None:
            messagebox.showerror("Error", "No simulation data to export!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Report",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    self.statistics_collector.export_to_json(filename)
                elif filename.endswith('.csv'):
                    self.statistics_collector.export_to_csv(filename)
                else:
                    # Export as text report
                    summary = self.statistics_collector.get_summary_statistics()
                    
                    # Handle None values safely
                    total_gens = summary.get('total_generations', 0) or 0
                    total_steps = summary.get('total_steps', 0) or 0
                    avg_survival = summary.get('average_survival_rate', 0) or 0
                    avg_fitness = summary.get('average_fitness', 0) or 0
                    best_fitness = summary.get('best_fitness_ever', 0) or 0
                    fitness_improvement = summary.get('fitness_improvement', 0) or 0
                    duration = summary.get('duration_seconds', 0) or 0
                    
                    with open(filename, 'w') as f:
                        f.write("EVOLUTIONARY SIMULATION REPORT\n")
                        f.write("=" * 60 + "\n\n")
                        f.write(f"Total Generations: {total_gens}\n")
                        f.write(f"Total Steps: {total_steps}\n")
                        f.write(f"Average Survival Rate: {avg_survival:.2%}\n")
                        f.write(f"Average Fitness: {avg_fitness:.2f}\n")
                        f.write(f"Best Fitness Ever: {best_fitness:.2f}\n")
                        f.write(f"Fitness Improvement: {fitness_improvement:.2f}\n")
                        f.write(f"Duration: {duration:.2f} seconds\n")
                
                messagebox.showinfo("Success", "Report exported successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export report: {str(e)}")
    
    def _on_closing(self):
        """Handle application closing."""
        if self.simulation is not None:
            self.simulation.stop()
        
        if self.update_timer is not None:
            self.root.after_cancel(self.update_timer)
        
        self.root.destroy()
    
    def _refresh_animals_list(self):
        """Refresh the animals list with current data."""
        if not self.simulation or not self.simulation.environment:
            return
        
        # Clear existing items
        for item in self.animals_tree.get_children():
            self.animals_tree.delete(item)
        
        # Get all animals (alive and dead)
        all_animals = self.simulation.environment.animals + self.simulation.environment.dead_animals
        
        # Sort by current sort order
        if self.current_sort_column == 'Fitness':
            all_animals.sort(key=lambda a: a.fitness, reverse=self.current_sort_reverse)
        elif self.current_sort_column == 'Age':
            all_animals.sort(key=lambda a: a.age, reverse=self.current_sort_reverse)
        elif self.current_sort_column == 'ID':
            all_animals.sort(key=lambda a: a.animal_id, reverse=self.current_sort_reverse)
        elif self.current_sort_column == 'Status':
            all_animals.sort(key=lambda a: a.alive, reverse=self.current_sort_reverse)
        elif self.current_sort_column == 'Position':
            all_animals.sort(key=lambda a: (a.position[1], a.position[0]), reverse=self.current_sort_reverse)
        else:
            # Default sort by fitness
            all_animals.sort(key=lambda a: a.fitness, reverse=True)
        
        for animal in all_animals:
            # Get animal state
            state = animal.get_state()
            
            # Format health info with coordinates
            health = f"H:{state['hunger']:.0f} T:{state['thirst']:.0f} E:{state['energy']:.0f} HP:{state.get('health', 100):.0f}"
            coords = f"({state['coordinates']['x']},{state['coordinates']['y']})"
            
            # Format position (already done above)
            pos = coords
            
            # Format status
            status = "Alive" if state['alive'] else "Dead"
            
            # Format actions
            actions = f"M:{state['behavioral_counts']['move']} E:{state['behavioral_counts']['eat']} D:{state['behavioral_counts']['drink']} R:{state['behavioral_counts']['rest']}"
            
            # Format resources consumed
            resources = f"F:{state['resource_consumed']['food']} W:{state['resource_consumed']['water']}"
            
            # Insert into tree
            self.animals_tree.insert('', 'end', values=(
                state['animal_id'][:12],  # Show more of the ID
                pos,
                status,
                health,
                state['age'],
                f"{state['fitness']:.1f}",
                actions,
                resources
            ))
    
    def _clear_animals_list(self):
        """Clear the animals list."""
        for item in self.animals_tree.get_children():
            self.animals_tree.delete(item)
    
    def _sort_animals(self, column):
        """Sort animals by the specified column."""
        if not self.simulation or not self.simulation.environment:
            return
        
        # Update sort tracking
        if self.current_sort_column == column:
            self.current_sort_reverse = not self.current_sort_reverse
        else:
            self.current_sort_column = column
            self.current_sort_reverse = True
        
        # Get all animals
        all_animals = self.simulation.environment.animals + self.simulation.environment.dead_animals
        
        # Sort animals based on column
        if column == 'Fitness':
            all_animals.sort(key=lambda a: a.fitness, reverse=self.current_sort_reverse)
        elif column == 'Age':
            all_animals.sort(key=lambda a: a.age, reverse=self.current_sort_reverse)
        elif column == 'ID':
            all_animals.sort(key=lambda a: a.animal_id, reverse=self.current_sort_reverse)
        elif column == 'Status':
            all_animals.sort(key=lambda a: a.alive, reverse=self.current_sort_reverse)
        elif column == 'Position':
            all_animals.sort(key=lambda a: (a.position[1], a.position[0]), reverse=self.current_sort_reverse)
        
        # Clear and repopulate with sorted data
        for item in self.animals_tree.get_children():
            self.animals_tree.delete(item)
        
        for animal in all_animals:
            state = animal.get_state()
            health = f"H:{state['hunger']:.0f} T:{state['thirst']:.0f} E:{state['energy']:.0f} HP:{state.get('health', 100):.0f}"
            coords = f"({state['coordinates']['x']},{state['coordinates']['y']})"
            status = "Alive" if state['alive'] else "Dead"
            actions = f"M:{state['behavioral_counts']['move']} E:{state['behavioral_counts']['eat']} D:{state['behavioral_counts']['drink']} R:{state['behavioral_counts']['rest']}"
            resources = f"F:{state['resource_consumed']['food']} W:{state['resource_consumed']['water']}"
            
            self.animals_tree.insert('', 'end', values=(
                state['animal_id'][:12],
                coords,
                status,
                health,
                state['age'],
                f"{state['fitness']:.1f}",
                actions,
                resources
            ))
    
    def _filter_animals(self, event=None):
        """Filter animals based on search term."""
        search_term = self.animal_search_var.get().lower()
        if not search_term:
            self._refresh_animals_list()
            return
        
        # Clear existing items
        for item in self.animals_tree.get_children():
            self.animals_tree.delete(item)
        
        if not self.simulation or not self.simulation.environment:
            return
        
        # Get all animals and filter
        all_animals = self.simulation.environment.animals + self.simulation.environment.dead_animals
        filtered_animals = [a for a in all_animals if search_term in a.animal_id.lower()]
        
        for animal in filtered_animals:
            state = animal.get_state()
            health = f"H:{state['hunger']:.0f} T:{state['thirst']:.0f} E:{state['energy']:.0f} HP:{state.get('health', 100):.0f}"
            coords = f"({state['coordinates']['x']},{state['coordinates']['y']})"
            status = "Alive" if state['alive'] else "Dead"
            actions = f"M:{state['behavioral_counts']['move']} E:{state['behavioral_counts']['eat']} D:{state['behavioral_counts']['drink']} R:{state['behavioral_counts']['rest']}"
            resources = f"F:{state['resource_consumed']['food']} W:{state['resource_consumed']['water']}"
            
            self.animals_tree.insert('', 'end', values=(
                state['animal_id'][:12],
                coords,
                status,
                health,
                state['age'],
                f"{state['fitness']:.1f}",
                actions,
                resources
            ))
    
    def _find_animal(self):
        """Find and highlight a specific animal."""
        search_term = self.animal_search_var.get().lower()
        if not search_term:
            return
        
        # Clear selection and find matching item
        self.animals_tree.selection_remove(self.animals_tree.selection())
        
        for item in self.animals_tree.get_children():
            values = self.animals_tree.item(item, 'values')
            if search_term in values[0].lower():  # Check ID column
                self.animals_tree.selection_set(item)
                self.animals_tree.see(item)
                break
    
    def _filter_alive_only(self):
        """Show only alive animals."""
        # Clear existing items
        for item in self.animals_tree.get_children():
            self.animals_tree.delete(item)
        
        if not self.simulation or not self.simulation.environment:
            return
        
        # Get only alive animals
        alive_animals = self.simulation.environment.animals
        
        for animal in alive_animals:
            state = animal.get_state()
            health = f"H:{state['hunger']:.0f} T:{state['thirst']:.0f} E:{state['energy']:.0f} HP:{state.get('health', 100):.0f}"
            coords = f"({state['coordinates']['x']},{state['coordinates']['y']})"
            status = "Alive"
            actions = f"M:{state['behavioral_counts']['move']} E:{state['behavioral_counts']['eat']} D:{state['behavioral_counts']['drink']} R:{state['behavioral_counts']['rest']}"
            resources = f"F:{state['resource_consumed']['food']} W:{state['resource_consumed']['water']}"
            
            self.animals_tree.insert('', 'end', values=(
                state['animal_id'][:12],
                coords,
                status,
                health,
                state['age'],
                f"{state['fitness']:.1f}",
                actions,
                resources
            ))

    def _export_animals_data(self):
        """Export animals data to file."""
        if not self.simulation or not self.simulation.environment:
            messagebox.showwarning("Warning", "No simulation data to export!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Animals Data",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                # Collect all animal data
                all_animals = self.simulation.environment.animals + self.simulation.environment.dead_animals
                animals_data = []
                
                for animal in all_animals:
                    state = animal.get_state()
                    animals_data.append({
                        'animal_id': state['animal_id'],
                        'position': state['position'],
                        'coordinates': state['coordinates'],
                        'hunger': state['hunger'],
                        'thirst': state['thirst'],
                        'energy': state['energy'],
                        'age': state['age'],
                        'fitness': state['fitness'],
                        'alive': state['alive'],
                        'behavioral_counts': state['behavioral_counts'],
                        'resource_consumed': state['resource_consumed'],
                        'action_count': state['action_count'],
                        'movement_count': state['movement_count']
                    })
                
                if filename.endswith('.csv'):
                    # Export as CSV
                    import csv
                    with open(filename, 'w', newline='') as f:
                        if animals_data:
                            writer = csv.DictWriter(f, fieldnames=animals_data[0].keys())
                            writer.writeheader()
                            writer.writerows(animals_data)
                else:
                    # Export as JSON
                    import json
                    with open(filename, 'w') as f:
                        json.dump(animals_data, f, indent=2)
                
                messagebox.showinfo("Success", f"Animals data exported to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export animals data: {str(e)}")
    
    def run(self):
        """Run the GUI application."""
        self.root.mainloop()


def main():
    """Main entry point for the GUI application."""
    app = SimulationGUI()
    app.run()


if __name__ == "__main__":
    main()
