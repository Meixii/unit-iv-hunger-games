"""
EvoSim GUI - Main Application

This is the main GUI application for the EvoSim animal evolution simulation.
It provides a comprehensive interface for running, monitoring, and visualizing
the simulation with real-time updates and controls.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import sys
import os
from typing import Optional, Dict, Any
import json

from simulation_controller import SimulationController, SimulationConfig
from world_generator import GenerationConfig
from data_structures import Animal, World, TerrainType, AnimalCategory
from config import AppConfig


class EvoSimGUI:
    """
    Main GUI application for EvoSim simulation.
    
    Features:
    - Real-time simulation control (start/stop/pause/resume)
    - Live visualization of the world grid
    - Animal statistics and monitoring
    - Configuration management
    - Event logging and display
    - Generation tracking and evolution progress
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("EvoSim - Animal Evolution Simulation")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2b2b2b')
        
        # Simulation state
        self.simulation_controller: Optional[SimulationController] = None
        self.simulation_thread: Optional[threading.Thread] = None
        self.is_running = False
        self.is_paused = False
        
        # GUI state
        self.config = AppConfig()
        self.current_generation = 0
        self.current_week = 0
        self.animal_stats = {}
        
        # Create GUI components
        self.setup_styles()
        self.create_widgets()
        self.setup_layout()
        self.setup_bindings()
        
        # Load default configuration
        self.load_default_config()
    
    def setup_styles(self):
        """Setup custom styles for the GUI."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors for dark theme
        style.configure('Title.TLabel', 
                       background='#2b2b2b', 
                       foreground='#ffffff',
                       font=('Arial', 16, 'bold'))
        
        style.configure('Header.TLabel',
                       background='#2b2b2b',
                       foreground='#ffffff',
                       font=('Arial', 12, 'bold'))
        
        style.configure('Info.TLabel',
                       background='#2b2b2b',
                       foreground='#cccccc',
                       font=('Arial', 10))
        
        style.configure('Control.TButton',
                       background='#4a4a4a',
                       foreground='#ffffff',
                       font=('Arial', 10, 'bold'))
        
        style.configure('Danger.TButton',
                       background='#8b0000',
                       foreground='#ffffff',
                       font=('Arial', 10, 'bold'))
        
        style.configure('Success.TButton',
                       background='#006400',
                       foreground='#ffffff',
                       font=('Arial', 10, 'bold'))
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main container
        self.main_frame = ttk.Frame(self.root)
        
        # Title
        self.title_label = ttk.Label(self.main_frame, 
                                   text="EvoSim - Animal Evolution Simulation",
                                   style='Title.TLabel')
        
        # Control panel
        self.control_frame = ttk.LabelFrame(self.main_frame, 
                                          text="Simulation Controls",
                                          padding=10)
        
        # Control buttons
        self.start_button = ttk.Button(self.control_frame, 
                                     text="Start Simulation",
                                     command=self.start_simulation,
                                     style='Success.TButton')
        
        self.pause_button = ttk.Button(self.control_frame,
                                     text="Pause",
                                     command=self.pause_simulation,
                                     state='disabled',
                                     style='Control.TButton')
        
        self.stop_button = ttk.Button(self.control_frame,
                                    text="Stop",
                                    command=self.stop_simulation,
                                    state='disabled',
                                    style='Danger.TButton')
        
        self.reset_button = ttk.Button(self.control_frame,
                                     text="Reset",
                                     command=self.reset_simulation,
                                     style='Control.TButton')
        
        self.analyze_button = ttk.Button(self.control_frame,
                                       text="Analyze",
                                       command=self.analyze_animal_population,
                                       style='Control.TButton')
        
        # Configuration panel
        self.config_frame = ttk.LabelFrame(self.main_frame,
                                         text="Configuration",
                                         padding=10)
        
        # Configuration controls
        self.population_label = ttk.Label(self.config_frame, text="Population Size:")
        self.population_var = tk.StringVar(value="20")
        self.population_entry = ttk.Entry(self.config_frame, 
                                        textvariable=self.population_var,
                                        width=10)
        
        self.generations_label = ttk.Label(self.config_frame, text="Max Generations:")
        self.generations_var = tk.StringVar(value="10")
        self.generations_entry = ttk.Entry(self.config_frame,
                                         textvariable=self.generations_var,
                                         width=10)
        
        self.weeks_label = ttk.Label(self.config_frame, text="Max Weeks:")
        self.weeks_var = tk.StringVar(value="20")
        self.weeks_entry = ttk.Entry(self.config_frame,
                                   textvariable=self.weeks_var,
                                   width=10)
        
        self.seed_label = ttk.Label(self.config_frame, text="Random Seed:")
        self.seed_var = tk.StringVar(value="42")
        self.seed_entry = ttk.Entry(self.config_frame,
                                  textvariable=self.seed_var,
                                  width=10)
        
        # Status panel
        self.status_frame = ttk.LabelFrame(self.main_frame,
                                        text="Simulation Status",
                                        padding=10)
        
        # Status labels
        self.generation_label = ttk.Label(self.status_frame, 
                                       text="Generation: 0",
                                       style='Header.TLabel')
        
        self.week_label = ttk.Label(self.status_frame,
                                  text="Week: 0",
                                  style='Header.TLabel')
        
        self.animals_label = ttk.Label(self.status_frame,
                                     text="Living Animals: 0",
                                     style='Info.TLabel')
        
        self.status_label = ttk.Label(self.status_frame,
                                   text="Status: Ready",
                                   style='Info.TLabel')
        
        # Visualization panel
        self.viz_frame = ttk.LabelFrame(self.main_frame,
                                      text="World Visualization",
                                      padding=10)
        
        # World grid canvas
        self.world_canvas = tk.Canvas(self.viz_frame,
                                    width=600,
                                    height=600,
                                    bg='#1a1a1a',
                                    highlightthickness=1,
                                    highlightbackground='#666666')
        
        # Scrollbars for world canvas
        self.v_scrollbar = ttk.Scrollbar(self.viz_frame, 
                                       orient="vertical", 
                                       command=self.world_canvas.yview)
        self.h_scrollbar = ttk.Scrollbar(self.viz_frame,
                                       orient="horizontal",
                                       command=self.world_canvas.xview)
        
        self.world_canvas.configure(yscrollcommand=self.v_scrollbar.set,
                                  xscrollcommand=self.h_scrollbar.set)
        
        # Statistics panel
        self.stats_frame = ttk.LabelFrame(self.main_frame,
                                       text="Animal Statistics",
                                       padding=10)
        
        # Statistics treeview
        self.stats_tree = ttk.Treeview(self.stats_frame,
                                    columns=('Category', 'Count', 'Avg Fitness', 'Avg Health'),
                                    show='headings',
                                    height=8)
        
        self.stats_tree.heading('Category', text='Category')
        self.stats_tree.heading('Count', text='Count')
        self.stats_tree.heading('Avg Fitness', text='Avg Fitness')
        self.stats_tree.heading('Avg Health', text='Avg Health')
        
        # Statistics scrollbar
        self.stats_scrollbar = ttk.Scrollbar(self.stats_frame,
                                           orient="vertical",
                                           command=self.stats_tree.yview)
        self.stats_tree.configure(yscrollcommand=self.stats_scrollbar.set)
        
        # Log panel
        self.log_frame = ttk.LabelFrame(self.main_frame,
                                      text="Event Log",
                                      padding=10)
        
        # Log text widget
        self.log_text = tk.Text(self.log_frame,
                              height=8,
                              width=50,
                              bg='#1a1a1a',
                              fg='#cccccc',
                              font=('Consolas', 9),
                              wrap=tk.WORD)
        
        # Log scrollbar
        self.log_scrollbar = ttk.Scrollbar(self.log_frame,
                                         orient="vertical",
                                         command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=self.log_scrollbar.set)
        
        # Menu bar
        self.create_menu()
    
    def create_menu(self):
        """Create the menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Load Configuration", command=self.load_config)
        file_menu.add_command(label="Save Configuration", command=self.save_config)
        file_menu.add_separator()
        file_menu.add_command(label="Export Data", command=self.export_data)
        file_menu.add_command(label="Export Animal Data", command=self.export_animal_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Simulation menu
        sim_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Simulation", menu=sim_menu)
        sim_menu.add_command(label="New Simulation", command=self.new_simulation)
        sim_menu.add_command(label="Load World", command=self.load_world)
        sim_menu.add_separator()
        sim_menu.add_command(label="Analyze Population", command=self.analyze_animal_population)
        sim_menu.add_command(label="Animal Creator", command=self.open_animal_creator)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Documentation", command=self.show_documentation)
    
    def setup_layout(self):
        """Setup the layout of all widgets."""
        # Main frame
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        self.title_label.pack(pady=(0, 10))
        
        # Top row - Controls and Configuration
        top_frame = ttk.Frame(self.main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Control panel
        self.control_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.pause_button.pack(side=tk.LEFT, padx=5)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        self.analyze_button.pack(side=tk.LEFT, padx=5)
        
        # Configuration panel
        self.config_frame.pack(side=tk.RIGHT, fill=tk.X, padx=(5, 0))
        
        # Configuration grid
        self.population_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.population_entry.grid(row=0, column=1, padx=(0, 10))
        
        self.generations_label.grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        self.generations_entry.grid(row=0, column=3, padx=(0, 10))
        
        self.weeks_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.weeks_entry.grid(row=1, column=1, padx=(0, 10))
        
        self.seed_label.grid(row=1, column=2, sticky=tk.W, padx=(0, 5))
        self.seed_entry.grid(row=1, column=3, padx=(0, 10))
        
        # Status panel
        self.status_frame.pack(fill=tk.X, pady=(0, 10))
        self.generation_label.pack(side=tk.LEFT, padx=10)
        self.week_label.pack(side=tk.LEFT, padx=10)
        self.animals_label.pack(side=tk.LEFT, padx=10)
        self.status_label.pack(side=tk.RIGHT, padx=10)
        
        # Middle row - Visualization and Statistics
        middle_frame = ttk.Frame(self.main_frame)
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Visualization
        self.viz_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.world_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Statistics panel
        self.stats_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))
        self.stats_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.stats_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bottom row - Log
        self.log_frame.pack(fill=tk.X)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_bindings(self):
        """Setup event bindings."""
        # Canvas bindings for world interaction
        self.world_canvas.bind("<Button-1>", self.on_canvas_click)
        self.world_canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.world_canvas.bind("<MouseWheel>", self.on_canvas_scroll)
        
        # Window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def load_default_config(self):
        """Load default configuration."""
        try:
            # Set default values from constants
            self.population_var.set("20")
            self.generations_var.set("10")
            self.weeks_var.set("20")
            self.seed_var.set("42")
            
            self.log_message("Default configuration loaded")
        except Exception as e:
            self.log_message(f"Error loading default config: {e}")
    
    def start_simulation(self):
        """Start the simulation."""
        try:
            # Validate configuration
            population_size = int(self.population_var.get())
            max_generations = int(self.generations_var.get())
            max_weeks = int(self.weeks_var.get())
            random_seed = int(self.seed_var.get()) if self.seed_var.get() else None
            
            # Create world generation configuration using GenerationConfig
            world_config = GenerationConfig(
                width=25,  # Default world size
                height=25,
                mountain_border=True
            )
            
            # Create simulation configuration
            config = SimulationConfig(
                max_weeks=max_weeks,
                max_generations=max_generations,
                population_size=population_size,
                enable_logging=True,
                log_level="INFO",
                random_seed=random_seed,
                world_config=world_config
            )
            
            # Create simulation controller
            self.simulation_controller = SimulationController(config)
            
            # Initialize world and population
            world = self.simulation_controller.initialize_world()
            animals = self.simulation_controller.initialize_population()
            
            # Log world and animal information
            self.log_world_info(world)
            self.log_animal_info(animals)
            
            # Update GUI state
            self.is_running = True
            self.is_paused = False
            self.current_generation = 0
            self.current_week = 0
            
            # Update buttons
            self.start_button.config(state='disabled')
            self.pause_button.config(state='normal')
            self.stop_button.config(state='normal')
            
            # Start simulation thread
            self.simulation_thread = threading.Thread(target=self.run_simulation, daemon=True)
            self.simulation_thread.start()
            
            # Update visualization
            self.update_world_visualization()
            self.update_statistics()
            
            self.log_message("Simulation started successfully")
            self.update_status("Running")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start simulation: {e}")
            self.log_message(f"Error starting simulation: {e}")
    
    def pause_simulation(self):
        """Pause the simulation."""
        if self.simulation_controller and self.is_running:
            if self.is_paused:
                self.simulation_controller.resume_simulation()
                self.is_paused = False
                self.pause_button.config(text="Pause")
                self.update_status("Running")
                self.log_message("Simulation resumed")
            else:
                self.simulation_controller.pause_simulation()
                self.is_paused = True
                self.pause_button.config(text="Resume")
                self.update_status("Paused")
                self.log_message("Simulation paused")
    
    def stop_simulation(self):
        """Stop the simulation."""
        if self.simulation_controller:
            self.simulation_controller.stop_simulation()
            self.is_running = False
            self.is_paused = False
            
            # Update buttons
            self.start_button.config(state='normal')
            self.pause_button.config(state='disabled')
            self.stop_button.config(state='disabled')
            
            self.update_status("Stopped")
            self.log_message("Simulation stopped")
    
    def reset_simulation(self):
        """Reset the simulation."""
        self.stop_simulation()
        self.simulation_controller = None
        self.current_generation = 0
        self.current_week = 0
        self.animal_stats = {}
        
        # Clear visualization
        self.world_canvas.delete("all")
        
        # Clear statistics
        for item in self.stats_tree.get_children():
            self.stats_tree.delete(item)
        
        # Clear log
        self.log_text.delete(1.0, tk.END)
        
        self.update_status("Ready")
        self.log_message("Simulation reset")
    
    def run_simulation(self):
        """Run the simulation in a separate thread."""
        try:
            # Start the simulation
            self.simulation_controller.start_simulation()
            
            while self.is_running and self.simulation_controller:
                if not self.is_paused:
                    # Run one generation of simulation
                    try:
                        result = self.simulation_controller.run_generation()
                        
                        # Update GUI in main thread
                        self.root.after(0, self.update_simulation_state)
                        
                        # Check if simulation should continue
                        status = self.simulation_controller.get_simulation_status()
                        if status.get('living_animals', 0) == 0:
                            self.is_running = False
                            self.root.after(0, self.simulation_complete)
                            break
                            
                    except Exception as e:
                        self.root.after(0, lambda: self.log_message(f"Generation error: {e}"))
                        self.is_running = False
                        break
                
                time.sleep(1.0)  # Small delay to prevent overwhelming the GUI
                
        except Exception as e:
            self.root.after(0, lambda: self.log_message(f"Simulation error: {e}"))
            self.is_running = False
    
    def update_simulation_state(self):
        """Update the simulation state display."""
        if self.simulation_controller:
            status = self.simulation_controller.get_simulation_status()
            
            self.current_generation = status.get('current_generation', 0)
            self.current_week = status.get('current_week', 0)
            
            self.generation_label.config(text=f"Generation: {self.current_generation}")
            self.week_label.config(text=f"Week: {self.current_week}")
            self.animals_label.config(text=f"Living Animals: {status.get('living_animals', 0)}")
            
            # Update visualization
            self.update_world_visualization()
            self.update_statistics()
    
    def update_world_visualization(self):
        """Update the world visualization."""
        if not self.simulation_controller:
            return
        
        try:
            world = self.simulation_controller.world
            if not world:
                return
            
            # Clear canvas
            self.world_canvas.delete("all")
            
            # Calculate tile size
            canvas_width = self.world_canvas.winfo_width()
            canvas_height = self.world_canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:
                return  # Canvas not ready
            
            width, height = world.dimensions
            tile_width = canvas_width // width
            tile_height = canvas_height // height
            
            # Draw world grid
            for y in range(height):
                for x in range(width):
                    tile = world.get_tile(x, y)
                    if not tile:
                        continue
                    
                    # Calculate position
                    x1 = x * tile_width
                    y1 = y * tile_height
                    x2 = x1 + tile_width
                    y2 = y1 + tile_height
                    
                    # Choose color based on terrain
                    color = self.get_terrain_color(tile.terrain_type)
                    
                    # Draw tile
                    self.world_canvas.create_rectangle(x1, y1, x2, y2, 
                                                    fill=color, 
                                                    outline='#333333',
                                                    width=1)
                    
                    # Draw animals
                    if tile.occupant:
                        self.draw_animal(x1, y1, x2, y2, tile.occupant)
            
            # Update scroll region
            self.world_canvas.configure(scrollregion=self.world_canvas.bbox("all"))
            
        except Exception as e:
            self.log_message(f"Error updating visualization: {e}")
    
    def get_terrain_color(self, terrain_type):
        """Get color for terrain type."""
        colors = {
            TerrainType.PLAINS: '#90EE90',      # Light green
            TerrainType.FOREST: '#228B22',      # Forest green
            TerrainType.JUNGLE: '#006400',      # Dark green
            TerrainType.WATER: '#4169E1',       # Royal blue
            TerrainType.SWAMP: '#8FBC8F',       # Dark sea green
            TerrainType.MOUNTAINS: '#696969'     # Dim gray
        }
        return colors.get(terrain_type, '#FFFFFF')
    
    def draw_animal(self, x1, y1, x2, y2, animal):
        """Draw an animal on the canvas."""
        # Calculate center
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        
        # Choose color based on category
        colors = {
            AnimalCategory.HERBIVORE: '#FFD700',    # Gold
            AnimalCategory.CARNIVORE: '#FF4500',    # Orange red
            AnimalCategory.OMNIVORE: '#9370DB'      # Medium purple
        }
        color = colors.get(animal.category, '#FFFFFF')
        
        # Draw animal as circle
        radius = min((x2 - x1), (y2 - y1)) // 4
        self.world_canvas.create_oval(center_x - radius, center_y - radius,
                                   center_x + radius, center_y + radius,
                                   fill=color, outline='#000000', width=2)
    
    def update_statistics(self):
        """Update animal statistics."""
        if not self.simulation_controller:
            return
        
        try:
            # Clear existing statistics
            for item in self.stats_tree.get_children():
                self.stats_tree.delete(item)
            
            # Get animals from world
            world = self.simulation_controller.world
            if not world:
                return
            
            width, height = world.dimensions
            animals = []
            for y in range(height):
                for x in range(width):
                    tile = world.get_tile(x, y)
                    if tile and tile.occupant:
                        animals.append(tile.occupant)
            
            # Group by category
            categories = {}
            for animal in animals:
                category = animal.category.value
                if category not in categories:
                    categories[category] = []
                categories[category].append(animal)
            
            # Add statistics to tree
            for category, animal_list in categories.items():
                count = len(animal_list)
                avg_fitness = sum(animal.get_fitness_score() for animal in animal_list) / count
                avg_health = sum(animal.status['Health'] for animal in animal_list) / count
                
                self.stats_tree.insert('', 'end', values=(
                    category,
                    count,
                    f"{avg_fitness:.2f}",
                    f"{avg_health:.2f}"
                ))
        
        except Exception as e:
            self.log_message(f"Error updating statistics: {e}")
    
    def update_status(self, status):
        """Update the status label."""
        self.status_label.config(text=f"Status: {status}")
    
    def log_message(self, message):
        """Add a message to the log."""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
    
    def simulation_complete(self):
        """Handle simulation completion."""
        self.is_running = False
        self.update_status("Complete")
        self.log_message("Simulation completed!")
        
        # Update buttons
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled')
        self.stop_button.config(state='disabled')
    
    def on_canvas_click(self, event):
        """Handle canvas click events."""
        # Get canvas coordinates
        canvas_x = self.world_canvas.canvasx(event.x)
        canvas_y = self.world_canvas.canvasy(event.y)
        
        # Convert to world coordinates
        if self.simulation_controller and self.simulation_controller.world:
            world = self.simulation_controller.world
            canvas_width = self.world_canvas.winfo_width()
            canvas_height = self.world_canvas.winfo_height()
            
            width, height = world.dimensions
            tile_width = canvas_width // width
            tile_height = canvas_height // height
            
            world_x = int(canvas_x // tile_width)
            world_y = int(canvas_y // tile_height)
            
            if 0 <= world_x < width and 0 <= world_y < height:
                tile = world.get_tile(world_x, world_y)
                if tile:
                    self.show_tile_info(tile, world_x, world_y)
    
    def on_canvas_drag(self, event):
        """Handle canvas drag events."""
        # Scroll the canvas
        self.world_canvas.scan_dragto(event.x, event.y, gain=1)
    
    def on_canvas_scroll(self, event):
        """Handle canvas scroll events."""
        # Zoom the canvas
        if event.delta > 0:
            self.world_canvas.scale("all", event.x, event.y, 1.1, 1.1)
        else:
            self.world_canvas.scale("all", event.x, event.y, 0.9, 0.9)
    
    def show_tile_info(self, tile, x, y):
        """Show information about a tile."""
        info = f"Tile ({x}, {y})\n"
        info += f"Terrain: {tile.terrain_type.value}\n"
        info += f"Resource: {'Yes' if tile.resource else 'No'}\n"
        info += f"Occupant: {'Yes' if tile.occupant else 'No'}\n"
        
        if tile.occupant:
            animal = tile.occupant
            info += f"\nAnimal:\n"
            info += f"  Category: {animal.category.value}\n"
            info += f"  Health: {animal.status['Health']:.1f}\n"
            info += f"  Energy: {animal.status['Energy']:.1f}\n"
            info += f"  Fitness: {animal.get_fitness_score():.2f}\n"
            info += f"  Alive: {animal.is_alive()}\n"
        
        messagebox.showinfo("Tile Information", info)
    
    def log_world_info(self, world: World):
        """Log information about the world using World class."""
        if world:
            width, height = world.dimensions
            self.log_message(f"World initialized: {width}x{height}")
            
            # Count terrain types
            terrain_counts = {}
            for y in range(height):
                for x in range(width):
                    tile = world.get_tile(x, y)
                    if tile:
                        terrain = tile.terrain_type.value
                        terrain_counts[terrain] = terrain_counts.get(terrain, 0) + 1
            
            for terrain, count in terrain_counts.items():
                self.log_message(f"  {terrain}: {count} tiles")
    
    def log_animal_info(self, animals):
        """Log information about animals using Animal class."""
        if animals:
            self.log_message(f"Population initialized: {len(animals)} animals")
            
            # Count by category
            category_counts = {}
            for animal in animals:
                category = animal.category.value
                category_counts[category] = category_counts.get(category, 0) + 1
            
            for category, count in category_counts.items():
                self.log_message(f"  {category}: {count} animals")
            
            # Log some animal details
            for i, animal in enumerate(animals[:3]):  # Show first 3 animals
                self.log_message(f"  Animal {i+1}: {animal.category.value}, "
                               f"Health: {animal.status['Health']:.1f}, "
                               f"Energy: {animal.status['Energy']:.1f}")
    
    def get_animal_details(self, animal: Animal) -> str:
        """Get detailed information about an animal using Animal class."""
        details = f"Category: {animal.category.value}\n"
        details += f"Health: {animal.status['Health']:.1f}\n"
        details += f"Energy: {animal.status['Energy']:.1f}\n"
        details += f"Hunger: {animal.status['Hunger']:.1f}\n"
        details += f"Thirst: {animal.status['Thirst']:.1f}\n"
        details += f"Fitness: {animal.get_fitness_score():.2f}\n"
        details += f"Traits: Strength={animal.traits['STR']}, "
        details += f"Agility={animal.traits['AGI']}, Endurance={animal.traits['END']}\n"
        details += f"Position: ({animal.location[0]}, {animal.location[1]})\n"
        details += f"Alive: {animal.is_alive()}\n"
        return details
    
    def analyze_animal_population(self):
        """Analyze the current animal population using Animal class methods."""
        if not self.simulation_controller or not self.simulation_controller.world:
            return
        
        world = self.simulation_controller.world
        width, height = world.dimensions
        animals = []
        
        # Collect all animals from the world
        for y in range(height):
            for x in range(width):
                tile = world.get_tile(x, y)
                if tile and tile.occupant:
                    animals.append(tile.occupant)
        
        if not animals:
            self.log_message("No animals found in the world")
            return
        
        # Analyze using Animal class methods
        living_animals = [animal for animal in animals if animal.is_alive()]
        dead_animals = [animal for animal in animals if not animal.is_alive()]
        
        self.log_message(f"Population Analysis:")
        self.log_message(f"  Total animals: {len(animals)}")
        self.log_message(f"  Living: {len(living_animals)}")
        self.log_message(f"  Dead: {len(dead_animals)}")
        
        if living_animals:
            # Calculate average fitness
            avg_fitness = sum(animal.get_fitness_score() for animal in living_animals) / len(living_animals)
            self.log_message(f"  Average fitness: {avg_fitness:.2f}")
            
            # Find best and worst animals
            best_animal = max(living_animals, key=lambda a: a.get_fitness_score())
            worst_animal = min(living_animals, key=lambda a: a.get_fitness_score())
            
            self.log_message(f"  Best fitness: {best_animal.get_fitness_score():.2f} "
                           f"({best_animal.category.value})")
            self.log_message(f"  Worst fitness: {worst_animal.get_fitness_score():.2f} "
                           f"({worst_animal.category.value})")
    
    def export_animal_data(self):
        """Export detailed animal data using Animal class."""
        if not self.simulation_controller or not self.simulation_controller.world:
            messagebox.showwarning("Warning", "No simulation data to export")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Animal Data",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                world = self.simulation_controller.world
                width, height = world.dimensions
                animals = []
                
                # Collect all animals from the world
                for y in range(height):
                    for x in range(width):
                        tile = world.get_tile(x, y)
                        if tile and tile.occupant:
                            animals.append(tile.occupant)
                
                # Export animal data
                with open(filename, 'w', newline='') as csvfile:
                    import csv
                    writer = csv.writer(csvfile)
                    
                    # Write header
                    writer.writerow([
                        'ID', 'Category', 'Health', 'Energy', 'Hunger', 'Thirst',
                        'Fitness', 'Strength', 'Agility', 'Endurance',
                        'X', 'Y', 'Alive'
                    ])
                    
                    # Write animal data
                    for i, animal in enumerate(animals):
                        writer.writerow([
                            i, animal.category.value, animal.status['Health'], animal.status['Energy'],
                            animal.status['Hunger'], animal.status['Thirst'], animal.get_fitness_score(),
                            animal.traits['STR'], animal.traits['AGI'], animal.traits['END'],
                            animal.location[0], animal.location[1], animal.is_alive()
                        ])
                
                self.log_message(f"Animal data exported to {filename}")
                messagebox.showinfo("Success", f"Animal data exported to {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export animal data: {e}")
                self.log_message(f"Error exporting animal data: {e}")
    
    def load_config(self):
        """Load configuration from file."""
        filename = filedialog.askopenfilename(
            title="Load Configuration",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.config = AppConfig.load(filename)
                self.log_message(f"Configuration loaded from {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load configuration: {e}")
    
    def save_config(self):
        """Save configuration to file."""
        filename = filedialog.asksaveasfilename(
            title="Save Configuration",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                self.config.save(filename)
                self.log_message(f"Configuration saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save configuration: {e}")
    
    def export_data(self):
        """Export simulation data."""
        # Use the same logic as export_animal_data
        self.export_animal_data()
    
    def new_simulation(self):
        """Create a new simulation."""
        self.reset_simulation()
    
    def load_world(self):
        """Load a world from file."""
        messagebox.showinfo("Info", "Load world functionality not yet implemented")
    
    def open_animal_creator(self):
        """Open the animal creator dialog."""
        messagebox.showinfo("Info", "Animal creator functionality not yet implemented")
    
    def show_about(self):
        """Show about dialog."""
        about_text = """
EvoSim - Animal Evolution Simulation

A Python implementation of an evolutionary simulation
where animals with neural networks compete for survival.

Features:
- Real-time simulation visualization
- Evolutionary algorithm with neural networks
- Dynamic world with events and disasters
- Comprehensive statistics and logging

Version: 1.0.0
        """
        messagebox.showinfo("About EvoSim", about_text)
    
    def show_documentation(self):
        """Show documentation."""
        messagebox.showinfo("Documentation", "Documentation is available in the README.md file")
    
    def on_closing(self):
        """Handle window closing."""
        if self.is_running:
            if messagebox.askokcancel("Quit", "Simulation is running. Do you want to quit?"):
                self.stop_simulation()
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """Run the GUI application."""
        self.root.mainloop()


def main():
    """Main entry point for the GUI application."""
    try:
        app = EvoSimGUI()
        app.run()
    except Exception as e:
        print(f"Error starting GUI: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
