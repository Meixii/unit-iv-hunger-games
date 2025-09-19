"""
Event & Disaster Engine

This module implements the event and disaster system for EvoSim, providing:
- Triggered events based on specific conditions
- Random events with probability-based occurrence
- Disaster events with area-of-effect mechanics
- Comprehensive event scheduling and execution

The system integrates with the main simulation controller to provide dynamic
and engaging gameplay through environmental challenges and opportunities.
"""

from .event_data import Event, EventType, EventResult, EventCondition
from .triggered_events import TriggeredEvent, TriggeredEventEngine
from .random_events import RandomEvent, RandomEventEngine  
from .disaster_events import DisasterEvent, DisasterEventEngine
from .event_scheduler import EventScheduler
from .event_engine import EventEngine

__all__ = [
    'Event',
    'EventType', 
    'EventResult',
    'EventCondition',
    'TriggeredEvent',
    'TriggeredEventEngine',
    'RandomEvent',
    'RandomEventEngine',
    'DisasterEvent', 
    'DisasterEventEngine',
    'EventScheduler',
    'EventEngine'
]
