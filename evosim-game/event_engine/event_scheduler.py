"""
Event Scheduler

This module handles the scheduling and coordination of different types of events
throughout the simulation. It determines when events should occur and manages
their execution order and frequency.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import logging
import random

# Import from parent directory
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures import Simulation
from .event_data import Event, EventType, EventResult
from .triggered_events import TriggeredEventEngine
from .random_events import RandomEventEngine
from .disaster_events import DisasterEventEngine


@dataclass
class EventSchedule:
    """Represents the event schedule for a given week."""
    week: int
    triggered_events: List[str] = field(default_factory=list)
    random_events: List[str] = field(default_factory=list)
    disaster_events: List[str] = field(default_factory=list)
    max_events_per_type: Dict[str, int] = field(default_factory=lambda: {
        "triggered": 3,
        "random": 2,
        "disaster": 1
    })


class EventScheduler:
    """Manages the scheduling and execution of events."""
    
    def __init__(self, simulation: Simulation, logger: logging.Logger):
        """Initialize the event scheduler."""
        self.simulation = simulation
        self.logger = logger
        
        # Initialize event engines
        self.triggered_engine = TriggeredEventEngine(simulation, logger)
        self.random_engine = RandomEventEngine(simulation, logger)
        self.disaster_engine = DisasterEventEngine(simulation, logger)
        
        # Event execution history
        self.event_history: List[EventResult] = []
        
        # Configuration
        self.config = {
            "triggered_events_enabled": True,
            "random_events_enabled": True,
            "disaster_events_enabled": True,
            "max_events_per_week": 5,
            "disaster_probability_modifier": 1.0,
            "event_intensity_modifier": 1.0
        }
    
    def generate_weekly_schedule(self, week: int) -> EventSchedule:
        """Generate the event schedule for a given week."""
        schedule = EventSchedule(week=week)
        
        # Adjust event probabilities based on week number and population
        self._adjust_event_probabilities(week)
        
        # Determine which types of events can occur this week
        if week == 1:
            # First week: minimal events to let simulation establish
            schedule.max_events_per_type = {
                "triggered": 1,
                "random": 1,
                "disaster": 0  # No disasters in first week
            }
        elif week <= 3:
            # Early weeks: limited events
            schedule.max_events_per_type = {
                "triggered": 2,
                "random": 1,
                "disaster": 0 if week <= 2 else 1
            }
        else:
            # Normal event scheduling
            schedule.max_events_per_type = {
                "triggered": 3,
                "random": 2,
                "disaster": 1
            }
        
        return schedule
    
    def execute_weekly_events(self, week: int) -> List[EventResult]:
        """Execute all events for the given week."""
        self.logger.info(f"Executing events for week {week}")
        
        schedule = self.generate_weekly_schedule(week)
        all_results = []
        
        try:
            # Execute triggered events
            if self.config["triggered_events_enabled"]:
                triggered_results = self._execute_triggered_events(schedule)
                all_results.extend(triggered_results)
            
            # Execute random events
            if self.config["random_events_enabled"]:
                random_results = self._execute_random_events(schedule)
                all_results.extend(random_results)
            
            # Execute disaster events
            if self.config["disaster_events_enabled"]:
                disaster_results = self._execute_disaster_events(schedule)
                all_results.extend(disaster_results)
            
            # Store results in history
            self.event_history.extend(all_results)
            
            # Log summary
            if all_results:
                self.logger.info(f"Week {week} events: {len(all_results)} events executed")
                for result in all_results:
                    if result.success:
                        self.logger.info(f"  - {result.event_type.value}: {result.message}")
                    else:
                        self.logger.warning(f"  - FAILED {result.event_type.value}: {result.message}")
            else:
                self.logger.debug(f"Week {week}: No events occurred")
                
        except Exception as e:
            self.logger.error(f"Error executing weekly events for week {week}: {e}")
            # Create error result
            error_result = EventResult(
                event_id="scheduler_error",
                event_type=EventType.CUSTOM,
                success=False,
                message=f"Event scheduler error: {str(e)}"
            )
            all_results.append(error_result)
        
        return all_results
    
    def _execute_triggered_events(self, schedule: EventSchedule) -> List[EventResult]:
        """Execute triggered events according to schedule."""
        max_events = schedule.max_events_per_type.get("triggered", 3)
        results = self.triggered_engine.check_and_execute_events(schedule.week)
        
        # Limit number of triggered events
        return results[:max_events]
    
    def _execute_random_events(self, schedule: EventSchedule) -> List[EventResult]:
        """Execute random events according to schedule."""
        max_events = schedule.max_events_per_type.get("random", 2)
        results = self.random_engine.execute_random_events(schedule.week, max_events)
        
        return results
    
    def _execute_disaster_events(self, schedule: EventSchedule) -> List[EventResult]:
        """Execute disaster events according to schedule."""
        max_events = schedule.max_events_per_type.get("disaster", 1)
        
        # Apply disaster probability modifier
        original_probabilities = {}
        for event in self.disaster_engine.events:
            original_probabilities[event.event_id] = event.probability
            event.probability *= self.config["disaster_probability_modifier"]
        
        try:
            results = self.disaster_engine.execute_disaster_events(schedule.week, max_events)
        finally:
            # Restore original probabilities
            for event in self.disaster_engine.events:
                event.probability = original_probabilities.get(event.event_id, event.probability)
        
        return results
    
    def _adjust_event_probabilities(self, week: int):
        """Adjust event probabilities based on current simulation state."""
        living_count = len(self.simulation.get_living_animals())
        
        # Adjust disaster probability based on population and week
        if living_count <= 3:
            # Reduce disasters when population is low
            self.config["disaster_probability_modifier"] = 0.3
        elif living_count > 15:
            # Increase disasters when population is high
            self.config["disaster_probability_modifier"] = 1.5
        else:
            self.config["disaster_probability_modifier"] = 1.0
        
        # Increase disaster probability in later weeks
        if week > 10:
            self.config["disaster_probability_modifier"] *= 1.2
        elif week > 5:
            self.config["disaster_probability_modifier"] *= 1.1
    
    def get_event_statistics(self) -> Dict[str, Any]:
        """Get statistics about executed events."""
        if not self.event_history:
            return {
                "total_events": 0,
                "by_type": {},
                "success_rate": 0.0,
                "casualties": 0,
                "resources_affected": 0
            }
        
        total_events = len(self.event_history)
        successful_events = sum(1 for e in self.event_history if e.success)
        total_casualties = sum(e.casualties for e in self.event_history)
        total_resources_affected = sum(e.resources_changed for e in self.event_history)
        
        # Count by type
        by_type = {}
        for event in self.event_history:
            event_type = event.event_type.value
            if event_type not in by_type:
                by_type[event_type] = {"count": 0, "successful": 0}
            by_type[event_type]["count"] += 1
            if event.success:
                by_type[event_type]["successful"] += 1
        
        return {
            "total_events": total_events,
            "successful_events": successful_events,
            "success_rate": successful_events / total_events if total_events > 0 else 0.0,
            "casualties": total_casualties,
            "resources_affected": total_resources_affected,
            "by_type": by_type
        }
    
    def configure_events(self, **kwargs):
        """Configure event system parameters."""
        for key, value in kwargs.items():
            if key in self.config:
                self.config[key] = value
                self.logger.info(f"Event configuration updated: {key} = {value}")
    
    def reset_events(self):
        """Reset all event states for a new simulation."""
        # Reset event engines
        for event in self.triggered_engine.events:
            event.reset()
        for event in self.random_engine.events:
            event.reset()
        for event in self.disaster_engine.events:
            event.reset()
        
        # Clear history
        self.event_history.clear()
        
        self.logger.info("Event system reset for new simulation")
    
    def add_custom_event(self, event: Event):
        """Add a custom event to the appropriate engine."""
        if event.event_type == EventType.TRIGGERED:
            self.triggered_engine.add_event(event)
        elif event.event_type == EventType.RANDOM:
            self.random_engine.add_event(event)
        elif event.event_type == EventType.DISASTER:
            self.disaster_engine.add_event(event)
        else:
            self.logger.warning(f"Unknown event type for custom event: {event.event_type}")
    
    def remove_event(self, event_id: str) -> bool:
        """Remove an event from all engines."""
        removed = False
        removed |= self.triggered_engine.remove_event(event_id)
        removed |= self.random_engine.remove_event(event_id)
        removed |= self.disaster_engine.remove_event(event_id)
        
        if removed:
            self.logger.info(f"Removed event: {event_id}")
        
        return removed
