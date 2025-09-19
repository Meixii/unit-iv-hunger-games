"""
Main Event Engine

This module provides the main EventEngine class that integrates all event systems
and provides a unified interface for the simulation controller.
"""

from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

# Import from parent directory
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures import Simulation
from .event_data import Event, EventType, EventResult
from .event_scheduler import EventScheduler


class EventEngine:
    """
    Main event engine that coordinates all event systems.
    
    This class provides a unified interface for the simulation controller
    to interact with the event system, handling scheduling, execution,
    and management of all event types.
    """
    
    def __init__(self, simulation: Simulation, logger: logging.Logger):
        """Initialize the event engine."""
        self.simulation = simulation
        self.logger = logger
        
        # Initialize event scheduler
        self.scheduler = EventScheduler(simulation, logger)
        
        # Engine state
        self.is_enabled = True
        self.current_week = 0
        
        # Statistics
        self.total_events_executed = 0
        self.total_casualties = 0
        self.total_resources_affected = 0
        
        self.logger.info("Event Engine initialized")
    
    def execute_weekly_events(self, week: int) -> Dict[str, Any]:
        """
        Execute all events for the given week.
        
        This is the main method called by the simulation controller
        to handle all event processing for a week.
        
        Args:
            week: Current week number
            
        Returns:
            Dictionary containing event execution results and statistics
        """
        if not self.is_enabled:
            return {
                "week": week,
                "events_executed": 0,
                "success": True,
                "message": "Event engine disabled",
                "results": [],
                "statistics": {}
            }
        
        self.current_week = week
        start_time = datetime.now()
        
        try:
            # Execute events through scheduler
            event_results = self.scheduler.execute_weekly_events(week)
            
            # Update statistics
            self._update_statistics(event_results)
            
            # Calculate execution time
            execution_time = datetime.now() - start_time
            
            # Prepare result summary
            successful_events = [r for r in event_results if r.success]
            failed_events = [r for r in event_results if not r.success]
            
            total_casualties = sum(r.casualties for r in event_results)
            total_resources_affected = sum(r.resources_changed for r in event_results)
            
            result = {
                "week": week,
                "events_executed": len(event_results),
                "successful_events": len(successful_events),
                "failed_events": len(failed_events),
                "success": len(failed_events) == 0,
                "message": self._generate_summary_message(event_results),
                "casualties": total_casualties,
                "resources_affected": total_resources_affected,
                "execution_time": execution_time.total_seconds(),
                "results": event_results,
                "statistics": self.get_statistics()
            }
            
            self.logger.debug(f"Week {week} event execution complete: {result['message']}")
            return result
            
        except Exception as e:
            self.logger.error(f"Event engine execution failed for week {week}: {e}")
            return {
                "week": week,
                "events_executed": 0,
                "success": False,
                "message": f"Event engine error: {str(e)}",
                "results": [],
                "statistics": {},
                "execution_time": (datetime.now() - start_time).total_seconds()
            }
    
    def _update_statistics(self, event_results: List[EventResult]):
        """Update internal statistics with event results."""
        self.total_events_executed += len(event_results)
        
        for result in event_results:
            self.total_casualties += result.casualties
            self.total_resources_affected += result.resources_changed
    
    def _generate_summary_message(self, event_results: List[EventResult]) -> str:
        """Generate a summary message for the week's events."""
        if not event_results:
            return "No events occurred this week"
        
        event_types = {}
        total_casualties = 0
        total_resources = 0
        
        for result in event_results:
            event_type = result.event_type.value
            event_types[event_type] = event_types.get(event_type, 0) + 1
            total_casualties += result.casualties
            total_resources += result.resources_changed
        
        # Build summary message
        parts = []
        for event_type, count in event_types.items():
            parts.append(f"{count} {event_type}")
        
        message = f"Events: {', '.join(parts)}"
        
        if total_casualties > 0:
            message += f", {total_casualties} casualties"
        
        if total_resources > 0:
            message += f", {total_resources} resources affected"
        
        return message
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive event system statistics."""
        scheduler_stats = self.scheduler.get_event_statistics()
        
        return {
            "total_events_executed": self.total_events_executed,
            "total_casualties": self.total_casualties,
            "total_resources_affected": self.total_resources_affected,
            "current_week": self.current_week,
            "is_enabled": self.is_enabled,
            "scheduler_statistics": scheduler_stats
        }
    
    def configure(self, **kwargs):
        """Configure the event engine."""
        # Handle engine-level configuration
        if "enabled" in kwargs:
            self.is_enabled = kwargs["enabled"]
            self.logger.info(f"Event engine {'enabled' if self.is_enabled else 'disabled'}")
        
        # Pass remaining configuration to scheduler
        scheduler_config = {k: v for k, v in kwargs.items() if k != "enabled"}
        if scheduler_config:
            self.scheduler.configure_events(**scheduler_config)
    
    def reset(self):
        """Reset the event engine for a new simulation."""
        self.scheduler.reset_events()
        self.current_week = 0
        self.total_events_executed = 0
        self.total_casualties = 0
        self.total_resources_affected = 0
        
        self.logger.info("Event engine reset for new simulation")
    
    def add_custom_event(self, event: Event):
        """Add a custom event to the system."""
        self.scheduler.add_custom_event(event)
        self.logger.info(f"Added custom event: {event.name} ({event.event_type.value})")
    
    def remove_event(self, event_id: str) -> bool:
        """Remove an event from the system."""
        return self.scheduler.remove_event(event_id)
    
    def get_active_events(self) -> Dict[str, List[str]]:
        """Get lists of all active events by type."""
        return {
            "triggered": [e.event_id for e in self.scheduler.triggered_engine.events if e.is_active],
            "random": [e.event_id for e in self.scheduler.random_engine.events if e.is_active],
            "disaster": [e.event_id for e in self.scheduler.disaster_engine.events if e.is_active]
        }
    
    def get_event_history(self, limit: Optional[int] = None) -> List[EventResult]:
        """Get event execution history."""
        history = self.scheduler.event_history
        if limit:
            return history[-limit:]
        return history.copy()
    
    def enable(self):
        """Enable the event engine."""
        self.is_enabled = True
        self.logger.info("Event engine enabled")
    
    def disable(self):
        """Disable the event engine."""
        self.is_enabled = False
        self.logger.info("Event engine disabled")
    
    def get_engine_status(self) -> Dict[str, Any]:
        """Get comprehensive status of the event engine."""
        active_events = self.get_active_events()
        
        return {
            "is_enabled": self.is_enabled,
            "current_week": self.current_week,
            "active_events": active_events,
            "total_active_events": sum(len(events) for events in active_events.values()),
            "configuration": self.scheduler.config,
            "statistics": self.get_statistics()
        }
