"""
Event Data Structures

This module contains the base data structures used by the event system.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable, Tuple
from enum import Enum
from datetime import datetime

# Import from parent directory
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures import Animal, Simulation


class EventType(Enum):
    """Types of events that can occur in the simulation."""
    TRIGGERED = "triggered"
    RANDOM = "random"
    DISASTER = "disaster"
    MOVEMENT = "movement"  # Already handled by action resolution
    CUSTOM = "custom"


@dataclass
class EventCondition:
    """Represents a condition that must be met for an event to trigger."""
    name: str
    description: str
    check_function: Callable[[Simulation], bool]
    parameters: Dict[str, Any] = field(default_factory=dict)
    
    def is_met(self, simulation: Simulation) -> bool:
        """Check if the condition is currently met."""
        try:
            return self.check_function(simulation, **self.parameters)
        except Exception as e:
            # If condition check fails, assume condition is not met
            return False


@dataclass
class EventResult:
    """Represents the result of an event execution."""
    event_id: str
    event_type: EventType
    success: bool
    message: str
    affected_animals: List[str] = field(default_factory=list)
    casualties: int = 0
    effects_applied: int = 0
    resources_changed: int = 0
    terrain_modified: bool = False
    duration: Optional[float] = None
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class Event:
    """Base class for all events in the simulation."""
    event_id: str
    name: str
    description: str
    event_type: EventType = EventType.CUSTOM  # Default to CUSTOM, subclasses override
    probability: float = 1.0  # 1.0 = always occurs when triggered
    cooldown_weeks: int = 0  # Minimum weeks between occurrences
    max_occurrences: Optional[int] = None  # Maximum times this event can occur
    
    # State tracking
    last_occurrence_week: int = -1
    occurrence_count: int = 0
    is_active: bool = True
    
    def can_occur(self, current_week: int) -> bool:
        """Check if this event can occur in the current week."""
        if not self.is_active:
            return False
        
        # Check maximum occurrences
        if self.max_occurrences is not None and self.occurrence_count >= self.max_occurrences:
            return False
        
        # Check cooldown
        if current_week - self.last_occurrence_week < self.cooldown_weeks:
            return False
        
        return True
    
    def execute(self, simulation: Simulation, week: int) -> EventResult:
        """Execute the event. Override in subclasses."""
        # Update occurrence tracking
        self.last_occurrence_week = week
        self.occurrence_count += 1
        
        # Base implementation returns a simple success result
        return EventResult(
            event_id=self.event_id,
            event_type=self.event_type,
            success=True,
            message=f"Base event {self.name} executed successfully"
        )
    
    def reset(self):
        """Reset the event state for a new simulation run."""
        self.last_occurrence_week = -1
        self.occurrence_count = 0
        self.is_active = True
