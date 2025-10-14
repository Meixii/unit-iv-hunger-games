"""
Statistics Collection for Evolutionary Simulation

This module implements comprehensive statistics collection and tracking
for the evolutionary simulation, including survival rates, fitness scores,
resource consumption, and behavioral patterns.

Author: Zen Garden
University of Caloocan City
"""

from typing import Dict, List, Any, Optional
import json
import csv
from datetime import datetime


class StatisticsCollector:
    """
    Collects and tracks simulation statistics over time.
    
    Tracks:
    - Survival rates per generation
    - Fitness scores (average, best, worst)
    - Resource consumption patterns
    - Behavioral patterns (action frequencies)
    - Generation comparisons
    """
    
    def __init__(self):
        """Initialize the statistics collector."""
        # Generation data
        self.generation_data: List[Dict[str, Any]] = []
        self.survival_rates: List[float] = []
        self.fitness_scores: List[Dict[str, float]] = []
        
        # Resource consumption
        self.resource_consumption: List[Dict[str, int]] = []
        
        # Behavioral patterns
        self.behavioral_patterns: List[Dict[str, int]] = []
        
        # Time tracking
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        
        # Current statistics
        self.current_generation = 0
        self.total_steps = 0
    
    def start_tracking(self):
        """Start tracking statistics."""
        self.start_time = datetime.now()
        self._is_tracking = True
    
    def stop_tracking(self):
        """Stop tracking statistics."""
        self.end_time = datetime.now()
        self._is_tracking = False
    
    def is_tracking(self) -> bool:
        """Check if statistics tracking is active."""
        return getattr(self, '_is_tracking', False)
    
    def record_generation(self, generation: int, population_stats: Dict[str, Any],
                         environment_stats: Dict[str, Any], event_stats: Dict[str, Any]):
        """
        Record statistics for a generation.
        
        Args:
            generation: Generation number
            population_stats: Population statistics
            environment_stats: Environment statistics
            event_stats: Event statistics
        """
        print(f"[DEBUG] StatisticsCollector.record_generation called with generation={generation}")
        self.current_generation = generation
        
        # Record generation data
        gen_data = {
            'generation': generation,
            'timestamp': datetime.now().isoformat(),
            'population': population_stats,
            'environment': environment_stats,
            'events': event_stats
        }
        self.generation_data.append(gen_data)
        
        # Record survival rate
        survival_rate = population_stats.get('survival_rate', 0.0)
        self.survival_rates.append(survival_rate)
        
        # Record fitness scores
        fitness_data = {
            'generation': generation,
            'average': population_stats.get('average_fitness', 0.0),
            'best': population_stats.get('best_fitness', 0.0),
            'worst': population_stats.get('worst_fitness', 0.0),
            'std': population_stats.get('fitness_std', 0.0)
        }
        self.fitness_scores.append(fitness_data)
        
        # Record resource consumption
        resource_data = {
            'generation': generation,
            'food_consumed': environment_stats.get('total_food_consumed', 0),
            'water_consumed': environment_stats.get('total_water_consumed', 0)
        }
        self.resource_consumption.append(resource_data)
        
        # Record behavioral patterns
        behavior_data = {
            'generation': generation,
            'move_count': population_stats.get('total_moves', 0),
            'eat_count': population_stats.get('total_eats', 0),
            'drink_count': population_stats.get('total_drinks', 0),
            'rest_count': population_stats.get('total_rests', 0)
        }
        self.behavioral_patterns.append(behavior_data)
    
    def record_step(self, step: int, step_stats: Dict[str, Any]):
        """
        Record statistics for a simulation step.
        
        Args:
            step: Step number
            step_stats: Step statistics
        """
        self.total_steps = step
    
    def get_survival_rate_trend(self) -> List[float]:
        """
        Get survival rate trend over generations.
        
        Returns:
            List of survival rates
        """
        return self.survival_rates.copy()
    
    def get_fitness_trend(self) -> Dict[str, List[float]]:
        """
        Get fitness trend over generations.
        
        Returns:
            Dictionary with average, best, and worst fitness trends
        """
        return {
            'average': [f['average'] for f in self.fitness_scores],
            'best': [f['best'] for f in self.fitness_scores],
            'worst': [f['worst'] for f in self.fitness_scores],
            'std': [f['std'] for f in self.fitness_scores]
        }
    
    def get_resource_consumption_trend(self) -> Dict[str, List[int]]:
        """
        Get resource consumption trend over generations.
        
        Returns:
            Dictionary with food and water consumption trends
        """
        return {
            'food': [r['food_consumed'] for r in self.resource_consumption],
            'water': [r['water_consumed'] for r in self.resource_consumption]
        }
    
    def get_behavioral_pattern_trend(self) -> Dict[str, List[int]]:
        """
        Get behavioral pattern trend over generations.
        
        Returns:
            Dictionary with action frequency trends
        """
        return {
            'move': [b['move_count'] for b in self.behavioral_patterns],
            'eat': [b['eat_count'] for b in self.behavioral_patterns],
            'drink': [b['drink_count'] for b in self.behavioral_patterns],
            'rest': [b['rest_count'] for b in self.behavioral_patterns]
        }
    
    def get_generation_comparison(self, gen1: int, gen2: int) -> Dict[str, Any]:
        """
        Compare two generations.
        
        Args:
            gen1: First generation number
            gen2: Second generation number
            
        Returns:
            Dictionary with comparison data
        """
        if gen1 >= len(self.generation_data) or gen2 >= len(self.generation_data):
            return {}
        
        data1 = self.generation_data[gen1]
        data2 = self.generation_data[gen2]
        
        return {
            'generation_1': gen1,
            'generation_2': gen2,
            'survival_rate_change': data2['population']['survival_rate'] - data1['population']['survival_rate'],
            'fitness_change': data2['population']['average_fitness'] - data1['population']['average_fitness'],
            'best_fitness_change': data2['population']['best_fitness'] - data1['population']['best_fitness'],
            'population_size_change': data2['population']['alive_count'] - data1['population']['alive_count']
        }
    
    def get_summary_statistics(self) -> Dict[str, Any]:
        """
        Get summary statistics for the entire simulation.
        
        Returns:
            Dictionary with summary statistics
        """
        if not self.generation_data:
            return {}
        
        # Calculate overall statistics
        avg_survival_rate = sum(self.survival_rates) / len(self.survival_rates) if self.survival_rates else 0.0
        
        fitness_averages = [f['average'] for f in self.fitness_scores]
        avg_fitness = sum(fitness_averages) / len(fitness_averages) if fitness_averages else 0.0
        
        best_fitnesses = [f['best'] for f in self.fitness_scores]
        best_fitness_ever = max(best_fitnesses) if best_fitnesses else 0.0
        
        # Calculate improvement
        fitness_improvement = 0.0
        if len(fitness_averages) >= 2:
            fitness_improvement = fitness_averages[-1] - fitness_averages[0]
        
        # Calculate duration
        duration = None
        if self.start_time and self.end_time:
            duration = (self.end_time - self.start_time).total_seconds()
        
        return {
            'total_generations': len(self.generation_data),
            'total_steps': self.total_steps,
            'average_survival_rate': avg_survival_rate,
            'average_fitness': avg_fitness,
            'best_fitness_ever': best_fitness_ever,
            'fitness_improvement': fitness_improvement,
            'duration_seconds': duration,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None
        }
    
    def export_to_json(self, filename: str):
        """
        Export statistics to JSON file.
        
        Args:
            filename: Output filename
        """
        data = {
            'summary': self.get_summary_statistics(),
            'generation_data': self.generation_data,
            'survival_rates': self.survival_rates,
            'fitness_scores': self.fitness_scores,
            'resource_consumption': self.resource_consumption,
            'behavioral_patterns': self.behavioral_patterns
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def export_to_csv(self, filename: str):
        """
        Export statistics to CSV file.
        
        Args:
            filename: Output filename
        """
        if not self.generation_data:
            return
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow([
                'Generation', 'Survival Rate', 'Average Fitness', 'Best Fitness',
                'Worst Fitness', 'Alive Count', 'Dead Count', 'Food Consumed',
                'Water Consumed', 'Move Count', 'Eat Count', 'Drink Count', 'Rest Count'
            ])
            
            # Write data
            for i, gen_data in enumerate(self.generation_data):
                pop_stats = gen_data['population']
                resource_data = self.resource_consumption[i] if i < len(self.resource_consumption) else {}
                behavior_data = self.behavioral_patterns[i] if i < len(self.behavioral_patterns) else {}
                
                writer.writerow([
                    gen_data['generation'],
                    pop_stats.get('survival_rate', 0.0),
                    pop_stats.get('average_fitness', 0.0),
                    pop_stats.get('best_fitness', 0.0),
                    pop_stats.get('worst_fitness', 0.0),
                    pop_stats.get('alive_count', 0),
                    pop_stats.get('dead_count', 0),
                    resource_data.get('food_consumed', 0),
                    resource_data.get('water_consumed', 0),
                    behavior_data.get('move_count', 0),
                    behavior_data.get('eat_count', 0),
                    behavior_data.get('drink_count', 0),
                    behavior_data.get('rest_count', 0)
                ])
    
    def reset(self):
        """Reset all statistics."""
        self.generation_data.clear()
        self.survival_rates.clear()
        self.fitness_scores.clear()
        self.resource_consumption.clear()
        self.behavioral_patterns.clear()
        self.start_time = None
        self.end_time = None
        self.current_generation = 0
        self.total_steps = 0
    
    def __str__(self) -> str:
        """String representation."""
        return f"StatisticsCollector(generations={len(self.generation_data)}, steps={self.total_steps})"

