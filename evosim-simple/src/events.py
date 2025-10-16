"""
Environmental Events System for Evolutionary Simulation

This module implements dynamic environmental events that affect the simulation,
including drought, storms, and other environmental challenges.

Author: Zen Garden
University of Caloocan City
"""

import random
import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class EnvironmentalEvent:
    """
    Base class for environmental events.
    """
    
    def __init__(self, name: str, duration: int, effects: Dict):
        """
        Initialize an environmental event.
        
        Args:
            name: Event name
            duration: Event duration in time steps
            effects: Dictionary of event effects
        """
        self.name = name
        self.duration = duration
        self.remaining_duration = duration
        self.effects = effects
        self.active = True
    
    def update(self) -> bool:
        """
        Update event duration.
        
        Returns:
            True if event is still active, False if expired
        """
        if self.active:
            self.remaining_duration -= 1
            if self.remaining_duration <= 0:
                self.active = False
        return self.active
    
    def get_effects(self) -> Dict:
        """
        Get current event effects.
        
        Returns:
            Dictionary of event effects
        """
        return self.effects.copy()
    
    def get_progress(self) -> float:
        """
        Get event progress (0.0 to 1.0).
        
        Returns:
            Event progress as a float
        """
        if self.duration <= 0:
            return 1.0
        return 1.0 - (self.remaining_duration / self.duration)


class EventManager:
    """
    Manages environmental events in the simulation.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize the event manager.
        
        Args:
            config_file: Path to event configuration file
        """
        self.active_events: Dict[str, EnvironmentalEvent] = {}
        self.event_history: List[Dict] = []
        self.event_config = self._load_event_config(config_file)
        
        # Event probabilities and settings
        self.drought_probability = 0.01
        self.storm_probability = 0.01
        self.famine_probability = 0.01
        self.bonus_probability = 0.01
        
        # Event cooldowns (prevent overlapping events)
        self.event_cooldowns: Dict[str, int] = {
            'drought': 0,
            'storm': 0,
            'famine': 0,
            'bonus': 0
        }
        
        # Cooldown duration (time steps)
        self.cooldown_duration = 100
    
    def _load_event_config(self, config_file: Optional[str]) -> Dict:
        """
        Load event configuration from file.
        
        Args:
            config_file: Path to configuration file
            
        Returns:
            Event configuration dictionary
        """
        if config_file is None:
            config_file = Path(__file__).parent.parent / "config" / "event_config.json"
        
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default configuration
            return {
                "drought": {
                    "name": "Drought",
                    "description": "Reduces water availability significantly",
                    "effects": {
                        "water_availability": 0.3,
                        "water_regeneration_rate": 0.1
                    },
                    "duration": 50,
                    "visual_effects": {
                        "color": "#8B4513",
                        "symbol": "D"
                    }
                },
                "storm": {
                    "name": "Storm",
                    "description": "Makes movement more difficult and costly",
                    "effects": {
                        "movement_cost_multiplier": 2.0,
                        "energy_decay_multiplier": 1.5,
                        "visibility_reduction": 0.5
                    },
                    "duration": 30,
                    "visual_effects": {
                        "color": "#4169E1",
                        "symbol": "S"
                    }
                }
            }
    
    def update(self) -> None:
        """
        Update all active events and check for new events.
        """
        # Update active events
        expired_events = []
        for event_name, event in self.active_events.items():
            if not event.update():
                expired_events.append(event_name)
                self._log_event_end(event)
        
        # Remove expired events
        for event_name in expired_events:
            del self.active_events[event_name]
        
        # Update cooldowns
        for event_type in self.event_cooldowns:
            if self.event_cooldowns[event_type] > 0:
                self.event_cooldowns[event_type] -= 1
        
        # Check for new events
        self._check_for_new_events()
    
    def _check_for_new_events(self) -> None:
        """
        Check if new events should be triggered.
        Prevents multiple events from occurring simultaneously.
        """
        # Only allow ONE event at a time to prevent overwhelming the animals
        if len(self.active_events) > 0:
            return  # No new events if any are already active
        
        # Check for events in order of severity (least severe first)
        if (self.bonus_probability > 0 and 
            random.random() < self.bonus_probability and 
            'bonus' not in self.active_events and 
            self.event_cooldowns['bonus'] == 0):
            self._trigger_bonus()
        elif (self.drought_probability > 0 and 
              random.random() < self.drought_probability and 
              'drought' not in self.active_events and 
              self.event_cooldowns['drought'] == 0):
            self._trigger_drought()
        elif (self.storm_probability > 0 and 
              random.random() < self.storm_probability and 
              'storm' not in self.active_events and 
              self.event_cooldowns['storm'] == 0):
            self._trigger_storm()
        elif (self.famine_probability > 0 and 
              random.random() < self.famine_probability and 
              'famine' not in self.active_events and 
              self.event_cooldowns['famine'] == 0):
            self._trigger_famine()
    
    def trigger_event(self, event_name: str) -> bool:
        """
        Manually trigger an event (used by GUI).
        
        Args:
            event_name: Name of the event to trigger ('drought', 'storm', 'famine', 'bonus')
            
        Returns:
            True if event was triggered, False if already active or on cooldown
        """
        if event_name in self.active_events:
            print(f"[EVENT] {event_name} is already active")
            return False
            
        if event_name == 'drought':
            self._trigger_drought()
        elif event_name == 'storm':
            self._trigger_storm()
        elif event_name == 'famine':
            self._trigger_famine()
        elif event_name == 'bonus':
            self._trigger_bonus()
        else:
            print(f"[EVENT] Unknown event type: {event_name}")
            return False
        
        print(f"[EVENT] Manually triggered: {event_name}")
        return True
    
    def _trigger_drought(self) -> None:
        """Trigger a drought event."""
        config = self.event_config.get('drought', {})
        effects = config.get('effects', {
            'water_availability': 0.7,
            'water_regeneration_rate': 0.5
        })
        duration = config.get('duration', 20)
        
        event = EnvironmentalEvent('drought', duration, effects)
        self.active_events['drought'] = event
        self.event_cooldowns['drought'] = self.cooldown_duration
        self._log_event_start('drought', effects, duration)
    
    def _trigger_storm(self) -> None:
        """Trigger a storm event."""
        config = self.event_config.get('storm', {})
        effects = config.get('effects', {
            'movement_cost_multiplier': 2.0,
            'energy_decay_multiplier': 1.5,
            'visibility_reduction': 0.5
        })
        duration = config.get('duration', 5)
        
        event = EnvironmentalEvent('storm', duration, effects)
        self.active_events['storm'] = event
        self.event_cooldowns['storm'] = self.cooldown_duration
        self._log_event_start('storm', effects, duration)
    
    def _trigger_famine(self) -> None:
        """Trigger a famine event."""
        config = self.event_config.get('famine', {})
        effects = config.get('effects', {
            'food_availability': 0.7,
            'food_regeneration_rate': 0.5
        })
        duration = config.get('duration', 10)
        
        event = EnvironmentalEvent('famine', duration, effects)
        self.active_events['famine'] = event
        self.event_cooldowns['famine'] = self.cooldown_duration
        self._log_event_start('famine', effects, duration)
    
    def _trigger_bonus(self) -> None:
        """Trigger a resource bonus event."""
        config = self.event_config.get('bonus', {})
        effects = config.get('effects', {
            'food_availability': 1.2,
            'water_availability': 1.2,
            'resource_regeneration_rate': 1.5
        })
        duration = config.get('duration', 50)
        
        event = EnvironmentalEvent('bonus', duration, effects)
        self.active_events['bonus'] = event
        self.event_cooldowns['bonus'] = self.cooldown_duration
        self._log_event_start('bonus', effects, duration)
    
    def _log_event_start(self, event_name: str, effects: Dict, duration: int) -> None:
        """Log the start of an event."""
        self.event_history.append({
            'type': 'start',
            'event': event_name,
            'effects': effects,
            'duration': duration,
            'timestamp': len(self.event_history)
        })
    
    def _log_event_end(self, event: EnvironmentalEvent) -> None:
        """Log the end of an event."""
        self.event_history.append({
            'type': 'end',
            'event': event.name,
            'duration_actual': event.duration - event.remaining_duration,
            'timestamp': len(self.event_history)
        })
    
    def get_active_events(self) -> Dict[str, EnvironmentalEvent]:
        """
        Get all currently active events.
        
        Returns:
            Dictionary of active events
        """
        return self.active_events.copy()
    
    def get_event_effects(self) -> Dict:
        """
        Get combined effects of all active events.
        
        Returns:
            Dictionary of combined event effects
        """
        combined_effects = {}
        
        for event in self.active_events.values():
            effects = event.get_effects()
            for key, value in effects.items():
                if key in combined_effects:
                    # Apply multiplicative effects
                    if 'multiplier' in key or 'rate' in key:
                        combined_effects[key] *= value
                    else:
                        combined_effects[key] = min(combined_effects[key], value)
                else:
                    combined_effects[key] = value
        
        return combined_effects
    
    def is_event_active(self, event_name: str) -> bool:
        """
        Check if a specific event is active.
        
        Args:
            event_name: Name of the event to check
            
        Returns:
            True if event is active
        """
        return event_name in self.active_events
    
    def get_event_progress(self, event_name: str) -> float:
        """
        Get progress of a specific event.
        
        Args:
            event_name: Name of the event
            
        Returns:
            Event progress (0.0 to 1.0)
        """
        if event_name in self.active_events:
            return self.active_events[event_name].get_progress()
        return 0.0
    
    def force_event(self, event_name: str) -> bool:
        """
        Force trigger a specific event.
        
        Args:
            event_name: Name of the event to trigger
            
        Returns:
            True if event was triggered successfully
        """
        if event_name == 'drought':
            self._trigger_drought()
            return True
        elif event_name == 'storm':
            self._trigger_storm()
            return True
        elif event_name == 'famine':
            self._trigger_famine()
            return True
        elif event_name == 'bonus':
            self._trigger_bonus()
            return True
        
        return False
    
    def set_event_probabilities(self, drought: float = None, storm: float = None, 
                               famine: float = None, bonus: float = None) -> None:
        """
        Set event probabilities.
        
        Args:
            drought: Drought probability (0-1)
            storm: Storm probability (0-1)
            famine: Famine probability (0-1)
            bonus: Bonus probability (0-1)
        """
        if drought is not None:
            self.drought_probability = max(0.0, min(1.0, drought))
        if storm is not None:
            self.storm_probability = max(0.0, min(1.0, storm))
        if famine is not None:
            self.famine_probability = max(0.0, min(1.0, famine))
        if bonus is not None:
            self.bonus_probability = max(0.0, min(1.0, bonus))
    
    def get_statistics(self) -> Dict:
        """
        Get event manager statistics.
        
        Returns:
            Dictionary with event statistics
        """
        return {
            'active_events': len(self.active_events),
            'event_names': list(self.active_events.keys()),
            'total_events_triggered': len([e for e in self.event_history if e['type'] == 'start']),
            'drought_probability': self.drought_probability,
            'storm_probability': self.storm_probability,
            'famine_probability': self.famine_probability,
            'bonus_probability': self.bonus_probability,
            'cooldowns': self.event_cooldowns.copy()
        }
    
    def reset(self) -> None:
        """
        Reset the event manager to initial state.
        """
        self.active_events.clear()
        self.event_history.clear()
        for event_type in self.event_cooldowns:
            self.event_cooldowns[event_type] = 0
