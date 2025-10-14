"""
Data Visualization for Evolutionary Simulation

This module implements data visualization using matplotlib,
including fitness progression charts, population graphs,
survival rate visualizations, and behavioral pattern displays.

Author: Zen Garden
University of Caloocan City
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for tkinter integration
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from typing import Dict, List, Any, Optional
import tkinter as tk
from tkinter import ttk


class SimulationVisualizer:
    """
    Visualizes simulation data using matplotlib charts and graphs.
    
    Provides:
    - Fitness progression charts
    - Population size graphs
    - Survival rate visualizations
    - Behavioral pattern displays
    - Comparative analysis tools
    """
    
    def __init__(self, parent_frame: Optional[tk.Frame] = None):
        """
        Initialize the visualizer.
        
        Args:
            parent_frame: Parent tkinter frame (optional)
        """
        self.parent_frame = parent_frame
        self.figures: Dict[str, Figure] = {}
        self.canvases: Dict[str, FigureCanvasTkAgg] = {}
    
    def create_fitness_chart(self, fitness_data: Dict[str, List[float]], 
                            title: str = "Fitness Progression") -> Figure:
        """
        Create fitness progression chart.
        
        Args:
            fitness_data: Dictionary with average, best, worst fitness trends
            title: Chart title
            
        Returns:
            Matplotlib figure
        """
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        generations = list(range(len(fitness_data['average'])))
        
        ax.plot(generations, fitness_data['average'], label='Average Fitness', linewidth=2)
        ax.plot(generations, fitness_data['best'], label='Best Fitness', linewidth=2, linestyle='--')
        ax.plot(generations, fitness_data['worst'], label='Worst Fitness', linewidth=2, linestyle=':')
        
        # Add confidence interval
        if 'std' in fitness_data and fitness_data['std']:
            avg = np.array(fitness_data['average'])
            std = np.array(fitness_data['std'])
            ax.fill_between(generations, avg - std, avg + std, alpha=0.2)
        
        ax.set_xlabel('Generation')
        ax.set_ylabel('Fitness')
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        fig.tight_layout()
        return fig
    
    def create_survival_rate_chart(self, survival_rates: List[float],
                                   title: str = "Survival Rate Over Generations") -> Figure:
        """
        Create survival rate chart.
        
        Args:
            survival_rates: List of survival rates per generation
            title: Chart title
            
        Returns:
            Matplotlib figure
        """
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        generations = list(range(len(survival_rates)))
        
        ax.plot(generations, survival_rates, linewidth=2, color='green', marker='o')
        mean_survival = np.mean(survival_rates) if len(survival_rates) > 0 else 0
        ax.axhline(y=mean_survival, color='r', linestyle='--', 
                  label=f'Average: {mean_survival:.2%}')
        
        ax.set_xlabel('Generation')
        ax.set_ylabel('Survival Rate')
        ax.set_title(title)
        ax.set_ylim(0, 1.05)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        fig.tight_layout()
        return fig
    
    def create_population_chart(self, population_data: Dict[str, List[int]],
                               title: str = "Population Over Generations") -> Figure:
        """
        Create population size chart.
        
        Args:
            population_data: Dictionary with alive and dead counts
            title: Chart title
            
        Returns:
            Matplotlib figure
        """
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        generations = list(range(len(population_data['alive'])))
        
        ax.plot(generations, population_data['alive'], label='Alive', 
               linewidth=2, color='green', marker='o')
        ax.plot(generations, population_data['dead'], label='Dead', 
               linewidth=2, color='red', marker='x')
        
        ax.set_xlabel('Generation')
        ax.set_ylabel('Count')
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        fig.tight_layout()
        return fig
    
    def create_resource_consumption_chart(self, resource_data: Dict[str, List[int]],
                                         title: str = "Resource Consumption") -> Figure:
        """
        Create resource consumption chart.
        
        Args:
            resource_data: Dictionary with food and water consumption
            title: Chart title
            
        Returns:
            Matplotlib figure
        """
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        generations = list(range(len(resource_data['food'])))
        
        ax.bar(generations, resource_data['food'], label='Food', alpha=0.7, color='orange')
        ax.bar(generations, resource_data['water'], label='Water', alpha=0.7, 
              color='blue', bottom=resource_data['food'])
        
        ax.set_xlabel('Generation')
        ax.set_ylabel('Resources Consumed')
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        fig.tight_layout()
        return fig
    
    def create_behavioral_pattern_chart(self, behavior_data: Dict[str, List[int]],
                                       title: str = "Behavioral Patterns") -> Figure:
        """
        Create behavioral pattern chart.
        
        Args:
            behavior_data: Dictionary with action frequencies
            title: Chart title
            
        Returns:
            Matplotlib figure
        """
        fig = Figure(figsize=(8, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        generations = list(range(len(behavior_data['move'])))
        
        ax.plot(generations, behavior_data['move'], label='Move', linewidth=2, marker='o')
        ax.plot(generations, behavior_data['eat'], label='Eat', linewidth=2, marker='s')
        ax.plot(generations, behavior_data['drink'], label='Drink', linewidth=2, marker='^')
        ax.plot(generations, behavior_data['rest'], label='Rest', linewidth=2, marker='d')
        
        ax.set_xlabel('Generation')
        ax.set_ylabel('Action Count')
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        fig.tight_layout()
        return fig
    
    def create_comparison_chart(self, gen1_data: Dict[str, Any], gen2_data: Dict[str, Any],
                               title: str = "Generation Comparison") -> Figure:
        """
        Create generation comparison chart.
        
        Args:
            gen1_data: First generation data
            gen2_data: Second generation data
            title: Chart title
            
        Returns:
            Matplotlib figure
        """
        fig = Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        metrics = ['Survival Rate', 'Avg Fitness', 'Best Fitness', 'Alive Count']
        gen1_values = [
            gen1_data.get('survival_rate', 0),
            gen1_data.get('average_fitness', 0),
            gen1_data.get('best_fitness', 0),
            gen1_data.get('alive_count', 0)
        ]
        gen2_values = [
            gen2_data.get('survival_rate', 0),
            gen2_data.get('average_fitness', 0),
            gen2_data.get('best_fitness', 0),
            gen2_data.get('alive_count', 0)
        ]
        
        x = np.arange(len(metrics))
        width = 0.35
        
        ax.bar(x - width/2, gen1_values, width, label=f"Gen {gen1_data.get('generation', 0)}")
        ax.bar(x + width/2, gen2_values, width, label=f"Gen {gen2_data.get('generation', 0)}")
        
        ax.set_ylabel('Value')
        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(metrics)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        fig.tight_layout()
        return fig
    
    def create_step_analysis_chart(self, step_data: List[Dict[str, Any]]) -> Figure:
        """
        Create step-by-step analysis chart.
        
        Args:
            step_data: List of step statistics
            
        Returns:
            Matplotlib figure
        """
        fig = Figure(figsize=(12, 8))
        
        if not step_data:
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, 'No step data available', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=16)
            ax.set_title('Step Analysis')
            return fig
        
        # Extract data
        steps = [d.get('step', 0) for d in step_data]
        alive_animals = [d.get('alive_animals', 0) for d in step_data]
        food_consumed = [d.get('total_food_consumed', 0) for d in step_data]
        water_consumed = [d.get('total_water_consumed', 0) for d in step_data]
        
        # Create subplots
        ax1 = fig.add_subplot(2, 2, 1)
        ax2 = fig.add_subplot(2, 2, 2)
        ax3 = fig.add_subplot(2, 2, 3)
        ax4 = fig.add_subplot(2, 2, 4)
        
        # Population over time
        ax1.plot(steps, alive_animals, 'b-', linewidth=2, label='Alive Animals')
        ax1.set_xlabel('Step')
        ax1.set_ylabel('Population')
        ax1.set_title('Population Over Time')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Resource consumption
        ax2.plot(steps, food_consumed, 'g-', linewidth=2, label='Food Consumed')
        ax2.plot(steps, water_consumed, 'b-', linewidth=2, label='Water Consumed')
        ax2.set_xlabel('Step')
        ax2.set_ylabel('Resources Consumed')
        ax2.set_title('Resource Consumption Over Time')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Survival rate
        if len(steps) > 1:
            survival_rates = [alive / max(1, alive_animals[0]) for alive in alive_animals]
            ax3.plot(steps, survival_rates, 'r-', linewidth=2, label='Survival Rate')
            ax3.set_xlabel('Step')
            ax3.set_ylabel('Survival Rate')
            ax3.set_title('Survival Rate Over Time')
            ax3.grid(True, alpha=0.3)
            ax3.legend()
        
        # Resource efficiency
        if len(steps) > 1:
            efficiency = [(f + w) / max(1, alive) for f, w, alive in zip(food_consumed, water_consumed, alive_animals)]
            ax4.plot(steps, efficiency, 'm-', linewidth=2, label='Resource Efficiency')
            ax4.set_xlabel('Step')
            ax4.set_ylabel('Efficiency (Resources/Population)')
            ax4.set_title('Resource Efficiency Over Time')
            ax4.grid(True, alpha=0.3)
            ax4.legend()
        
        fig.suptitle('Step-by-Step Analysis', fontsize=16, fontweight='bold')
        fig.tight_layout()
        
        return fig
    
    def create_generation_comparison_chart(self, gen_data: List[Dict[str, Any]]) -> Figure:
        """
        Create generation comparison chart.
        
        Args:
            gen_data: List of generation statistics
            
        Returns:
            Matplotlib figure
        """
        fig = Figure(figsize=(12, 8))
        
        if not gen_data:
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, 'No generation data available', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=16)
            ax.set_title('Generation Comparison')
            return fig
        
        # Extract data
        generations = [d.get('generation', 0) for d in gen_data]
        pop_stats = [d.get('population_stats', {}) for d in gen_data]
        
        # Extract metrics
        avg_fitness = [p.get('average_fitness', 0) for p in pop_stats]
        best_fitness = [p.get('best_fitness', 0) for p in pop_stats]
        survival_rates = [p.get('survival_rate', 0) for p in pop_stats]
        alive_counts = [p.get('alive_count', 0) for p in pop_stats]
        
        # Create subplots
        ax1 = fig.add_subplot(2, 2, 1)
        ax2 = fig.add_subplot(2, 2, 2)
        ax3 = fig.add_subplot(2, 2, 3)
        ax4 = fig.add_subplot(2, 2, 4)
        
        # Fitness progression
        ax1.plot(generations, avg_fitness, 'b-', linewidth=2, label='Average Fitness')
        ax1.plot(generations, best_fitness, 'r-', linewidth=2, label='Best Fitness')
        ax1.set_xlabel('Generation')
        ax1.set_ylabel('Fitness')
        ax1.set_title('Fitness Progression')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Survival rates
        ax2.plot(generations, survival_rates, 'g-', linewidth=2, label='Survival Rate')
        ax2.set_xlabel('Generation')
        ax2.set_ylabel('Survival Rate')
        ax2.set_title('Survival Rate by Generation')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Population sizes
        ax3.plot(generations, alive_counts, 'm-', linewidth=2, label='Alive Animals')
        ax3.set_xlabel('Generation')
        ax3.set_ylabel('Population Size')
        ax3.set_title('Population Size by Generation')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        # Fitness improvement
        if len(avg_fitness) > 1:
            improvement = [avg_fitness[i] - avg_fitness[0] for i in range(len(avg_fitness))]
            ax4.plot(generations, improvement, 'c-', linewidth=2, label='Fitness Improvement')
            ax4.set_xlabel('Generation')
            ax4.set_ylabel('Fitness Improvement')
            ax4.set_title('Fitness Improvement Over Generations')
            ax4.grid(True, alpha=0.3)
            ax4.legend()
        
        fig.suptitle('Generation Comparison Analysis', fontsize=16, fontweight='bold')
        fig.tight_layout()
        
        return fig
    
    def create_summary_dashboard(self, summary_stats: Dict[str, Any]) -> Figure:
        """
        Create summary dashboard with key metrics.
        
        Args:
            summary_stats: Summary statistics
            
        Returns:
            Matplotlib figure
        """
        fig = Figure(figsize=(10, 8), dpi=100)
        
        # Create text display
        ax = fig.add_subplot(111)
        ax.axis('off')
        
        # Format summary text - handle None values safely
        total_gens = summary_stats.get('total_generations', 0) or 0
        total_steps = summary_stats.get('total_steps', 0) or 0
        avg_survival = summary_stats.get('average_survival_rate', 0) or 0
        avg_fitness = summary_stats.get('average_fitness', 0) or 0
        best_fitness = summary_stats.get('best_fitness_ever', 0) or 0
        fitness_improvement = summary_stats.get('fitness_improvement', 0) or 0
        duration = summary_stats.get('duration_seconds', 0) or 0
        start_time = summary_stats.get('start_time', 'N/A')
        end_time = summary_stats.get('end_time', 'N/A')
        
        text = f"""
        SIMULATION SUMMARY
        {'='*50}
        
        Total Generations: {total_gens}
        Total Steps: {total_steps}
        
        Average Survival Rate: {avg_survival:.2%}
        Average Fitness: {avg_fitness:.2f}
        Best Fitness Ever: {best_fitness:.2f}
        Fitness Improvement: {fitness_improvement:.2f}
        
        Duration: {duration:.2f} seconds
        Start Time: {start_time}
        End Time: {end_time}
        """
        
        ax.text(0.1, 0.5, text, fontsize=12, family='monospace',
               verticalalignment='center')
        
        fig.tight_layout()
        return fig
    
    def embed_figure_in_frame(self, figure: Figure, frame: tk.Frame, 
                             figure_name: str) -> FigureCanvasTkAgg:
        """
        Embed a matplotlib figure in a tkinter frame.
        
        Args:
            figure: Matplotlib figure
            frame: Tkinter frame
            figure_name: Name for the figure
            
        Returns:
            Canvas widget
        """
        # Remove old canvas if exists
        if figure_name in self.canvases:
            self.canvases[figure_name].get_tk_widget().destroy()
        
        # Create new canvas
        canvas = FigureCanvasTkAgg(figure, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Store references
        self.figures[figure_name] = figure
        self.canvases[figure_name] = canvas
        
        return canvas
    
    def save_figure(self, figure: Figure, filename: str, dpi: int = 300):
        """
        Save a figure to file.
        
        Args:
            figure: Matplotlib figure
            filename: Output filename
            dpi: Resolution in dots per inch
        """
        figure.savefig(filename, dpi=dpi, bbox_inches='tight')
    
    def close_all(self):
        """Close all figures and canvases."""
        for canvas in self.canvases.values():
            canvas.get_tk_widget().destroy()
        
        for figure in self.figures.values():
            plt.close(figure)
        
        self.figures.clear()
        self.canvases.clear()


def create_visualization_window(statistics_data: Dict[str, Any], 
                                parent: Optional[tk.Tk] = None) -> tk.Toplevel:
    """
    Create a visualization window with multiple charts.
    
    Args:
        statistics_data: Statistics data to visualize
        parent: Parent window
        
    Returns:
        Toplevel window
    """
    window = tk.Toplevel(parent) if parent else tk.Tk()
    window.title("Simulation Data Visualization")
    window.geometry("1000x800")
    
    # Create notebook for tabs
    notebook = ttk.Notebook(window)
    notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    visualizer = SimulationVisualizer()
    
    # Fitness tab
    if 'fitness_scores' in statistics_data:
        fitness_frame = ttk.Frame(notebook)
        notebook.add(fitness_frame, text="Fitness")
        
        fitness_data = statistics_data['fitness_scores']
        fig = visualizer.create_fitness_chart(fitness_data)
        visualizer.embed_figure_in_frame(fig, fitness_frame, 'fitness')
    
    # Survival rate tab
    if 'survival_rates' in statistics_data:
        survival_frame = ttk.Frame(notebook)
        notebook.add(survival_frame, text="Survival Rate")
        
        survival_rates = statistics_data['survival_rates']
        fig = visualizer.create_survival_rate_chart(survival_rates)
        visualizer.embed_figure_in_frame(fig, survival_frame, 'survival')
    
    # Resource consumption tab
    if 'resource_consumption' in statistics_data:
        resource_frame = ttk.Frame(notebook)
        notebook.add(resource_frame, text="Resources")
        
        resource_data = statistics_data['resource_consumption']
        fig = visualizer.create_resource_consumption_chart(resource_data)
        visualizer.embed_figure_in_frame(fig, resource_frame, 'resources')
    
    # Behavioral patterns tab
    if 'behavioral_patterns' in statistics_data:
        behavior_frame = ttk.Frame(notebook)
        notebook.add(behavior_frame, text="Behavior")
        
        behavior_data = statistics_data['behavioral_patterns']
        fig = visualizer.create_behavioral_pattern_chart(behavior_data)
        visualizer.embed_figure_in_frame(fig, behavior_frame, 'behavior')
    
    # Step-by-step analysis tab
    if 'step_history' in statistics_data and statistics_data['step_history']:
        step_frame = ttk.Frame(notebook)
        notebook.add(step_frame, text="Step Analysis")
        
        step_data = statistics_data['step_history']
        fig = visualizer.create_step_analysis_chart(step_data)
        visualizer.embed_figure_in_frame(fig, step_frame, 'step_analysis')
    
    # Generation comparison tab
    if 'generation_history' in statistics_data and statistics_data['generation_history']:
        gen_frame = ttk.Frame(notebook)
        notebook.add(gen_frame, text="Generation Comparison")
        
        gen_data = statistics_data['generation_history']
        fig = visualizer.create_generation_comparison_chart(gen_data)
        visualizer.embed_figure_in_frame(fig, gen_frame, 'generation_comparison')
    
    # Summary tab
    if 'summary' in statistics_data:
        summary_frame = ttk.Frame(notebook)
        notebook.add(summary_frame, text="Summary")
        
        summary_stats = statistics_data['summary']
        fig = visualizer.create_summary_dashboard(summary_stats)
        visualizer.embed_figure_in_frame(fig, summary_frame, 'summary')
    
    return window

