"""
Action Resolution System

This module implements the 4-phase action resolution system as specified in Section IV.B:
1. Decision Phase: Collect actions from all animals
2. Status & Environmental Phase: Apply passive effects
3. Action Execution Phase: Execute actions by priority
4. Cleanup Phase: Apply new effects and remove expired ones

The system ensures fairness by preventing animals that act earlier from having an unfair advantage.
"""

from .action_data import AnimalAction, ActionPriority
from .action_resolver import ActionResolver
from .decision_engine import DecisionEngine
from .execution_engine import ExecutionEngine
from .status_engine import StatusEngine
from .cleanup_engine import CleanupEngine

# Import ActionType from parent directory
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


__all__ = [
    'AnimalAction',
    'ActionPriority', 
    'ActionResolver',
    'DecisionEngine',
    'ExecutionEngine',
    'StatusEngine',
    'CleanupEngine'
]
