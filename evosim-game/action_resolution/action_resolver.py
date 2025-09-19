"""
Main Action Resolution System

This class orchestrates the 4-phase action resolution process.
"""

from typing import Dict, List, Any
from datetime import datetime
import logging

# Import from parent directory
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures import Animal, Simulation
from .action_data import AnimalAction
from .decision_engine import DecisionEngine
from .status_engine import StatusEngine
from .execution_engine import ExecutionEngine
from .cleanup_engine import CleanupEngine


class ActionResolver:
    """
    Main Action Resolution System that orchestrates the 4-phase process.
    """
    
    def __init__(self, simulation: Simulation, logger: logging.Logger):
        """
        Initialize the action resolver.
        
        Args:
            simulation: The simulation instance containing world and population data.
            logger: Logger for debugging and information output.
        """
        self.simulation = simulation
        self.logger = logger
        
        # Initialize the phase engines
        self.decision_engine = DecisionEngine(simulation, logger)
        self.status_engine = StatusEngine(simulation, logger)
        self.execution_engine = ExecutionEngine(simulation, logger)
        self.cleanup_engine = CleanupEngine(simulation, logger)
    
    def execute_action_resolution_system(self, week: int) -> Dict[str, Any]:
        """
        Execute the complete 4-phase action resolution system.
        
        This implements the turn-based action processing as specified in Section IV.B:
        1. Decision Phase: Collect actions from all animals
        2. Status & Environmental Phase: Apply passive effects
        3. Action Execution Phase: Execute actions by priority
        4. Cleanup Phase: Apply new effects and remove expired ones
        
        Args:
            week: Current week number for logging.
            
        Returns:
            Dictionary containing detailed results of the action resolution.
        """
        self.logger.info("🎯 Starting Action Resolution System")
        
        start_time = datetime.now()
        living_animals = self.simulation.get_living_animals()
        
        if not living_animals:
            return {
                'phase': 'action_resolution',
                'week': week,
                'success': True,
                'message': 'No living animals to process',
                'phases_completed': 0,
                'actions_processed': 0,
                'casualties': 0,
                'duration': datetime.now() - start_time
            }
        
        try:
            # Phase 1: Decision Phase
            self.logger.info("📋 Phase 1: Decision Phase")
            planned_actions = self.decision_engine.execute_decision_phase(living_animals)
            self.logger.info(f"   Collected {len(planned_actions)} actions from {len(living_animals)} animals")
            
            # Phase 2: Status & Environmental Phase
            self.logger.info("🌡️ Phase 2: Status & Environmental Phase")
            status_results = self.status_engine.execute_status_environmental_phase(living_animals)
            self.logger.info(f"   Applied passive effects to {len(living_animals)} animals")
            
            # Phase 3: Action Execution Phase
            self.logger.info("⚡ Phase 3: Action Execution Phase")
            execution_results = self.execution_engine.execute_action_execution_phase(planned_actions)
            self.logger.info(f"   Executed {len(planned_actions)} actions with {execution_results['conflicts']} conflicts")
            
            # Phase 4: Cleanup Phase
            self.logger.info("🧹 Phase 4: Cleanup Phase")
            cleanup_results = self.cleanup_engine.execute_cleanup_phase(living_animals)
            self.logger.info(f"   Applied {cleanup_results['effects_added']} new effects, removed {cleanup_results['effects_removed']} expired effects")
            
            # Calculate final results
            final_living = self.simulation.get_living_animals()
            casualties = len(living_animals) - len(final_living)
            
            # Extract affected animals from status results (casualties)
            affected_animals = []
            if 'casualties' in status_results and isinstance(status_results['casualties'], list):
                affected_animals = [casualty['animal_id'] for casualty in status_results['casualties']]
            
            result = {
                'phase': 'action_resolution',
                'week': week,
                'success': True,
                'message': f'Action resolution completed successfully. {casualties} casualties.',
                'phases_completed': 4,
                'actions_processed': len(planned_actions),
                'casualties': casualties,
                'affected_animals': affected_animals,
                'conflicts_resolved': execution_results['conflicts'],
                'duration': datetime.now() - start_time,
                'phase_results': {
                    'decision': {'actions_collected': len(planned_actions)},
                    'status_environmental': status_results,
                    'action_execution': execution_results,
                    'cleanup': cleanup_results
                }
            }
            
            self.logger.info(f"✅ Action Resolution Complete: {len(planned_actions)} actions, {casualties} casualties")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ Action resolution failed: {e}")
            return {
                'phase': 'action_resolution',
                'week': week,
                'success': False,
                'message': f'Action resolution failed: {str(e)}',
                'phases_completed': 0,
                'actions_processed': 0,
                'casualties': 0,
                'duration': datetime.now() - start_time
            }
