"""
Triggered Events System

This module handles events that are triggered by specific conditions in the simulation.
Examples: resource depletion, population thresholds, animal interactions, etc.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import logging
import random

# Import from parent directory
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures import Simulation, Animal, Effect, EffectType
from .event_data import Event, EventType, EventResult, EventCondition


@dataclass
class TriggeredEvent(Event):
    """Event that occurs when specific conditions are met."""
    conditions: List[EventCondition] = field(default_factory=list)
    require_all_conditions: bool = True  # If False, only one condition needs to be met
    
    def __post_init__(self):
        """Initialize triggered event."""
        self.event_type = EventType.TRIGGERED
    
    def should_trigger(self, simulation: Simulation) -> bool:
        """Check if this event should trigger based on its conditions."""
        if not self.can_occur(simulation.current_week):
            return False
        
        if not self.conditions:
            return False
        
        # Check conditions
        if self.require_all_conditions:
            # All conditions must be met
            return all(condition.is_met(simulation) for condition in self.conditions)
        else:
            # At least one condition must be met
            return any(condition.is_met(simulation) for condition in self.conditions)
    
    def execute(self, simulation: Simulation, week: int) -> EventResult:
        """Execute the triggered event."""
        # Update occurrence tracking
        self.last_occurrence_week = week
        self.occurrence_count += 1
        
        # Base triggered event implementation
        return EventResult(
            event_id=self.event_id,
            event_type=self.event_type,
            success=True,
            message=f"Triggered event {self.name} executed"
        )


class TriggeredEventEngine:
    """Engine for managing and executing triggered events."""
    
    def __init__(self, simulation: Simulation, logger: logging.Logger):
        """Initialize the triggered event engine."""
        self.simulation = simulation
        self.logger = logger
        self.events: List[TriggeredEvent] = []
        
        # Initialize default triggered events
        self._initialize_default_events()
    
    def _initialize_default_events(self):
        """Initialize default triggered events."""
        # Population threshold events
        self._add_population_events()
        
        # Resource depletion events
        self._add_resource_events()
        
        # Health crisis events
        self._add_health_events()
    
    def _add_population_events(self):
        """Add population-related triggered events."""
        # Overpopulation event
        overpopulation_condition = EventCondition(
            name="overpopulation",
            description="Too many animals in a small area",
            check_function=self._check_overpopulation,
            parameters={"threshold": 15, "area_size": 25}
        )
        
        overpopulation_event = OverpopulationEvent(
            event_id="overpopulation",
            name="Overpopulation Crisis",
            description="Too many animals competing for limited resources",
            conditions=[overpopulation_condition],
            probability=0.8,
            cooldown_weeks=5
        )
        self.events.append(overpopulation_event)
        
        # Extinction threat event
        extinction_condition = EventCondition(
            name="near_extinction",
            description="Very few animals remaining",
            check_function=self._check_near_extinction,
            parameters={"threshold": 3}
        )
        
        extinction_event = ExtinctionThreatEvent(
            event_id="extinction_threat",
            name="Extinction Threat",
            description="Population has dropped to critically low levels",
            conditions=[extinction_condition],
            probability=1.0,
            cooldown_weeks=3
        )
        self.events.append(extinction_event)
    
    def _add_resource_events(self):
        """Add resource-related triggered events."""
        # Resource scarcity event
        scarcity_condition = EventCondition(
            name="resource_scarcity",
            description="Limited resources available",
            check_function=self._check_resource_scarcity,
            parameters={"threshold": 0.3}  # Less than 30% of tiles have resources
        )
        
        scarcity_event = ResourceScarcityEvent(
            event_id="resource_scarcity",
            name="Resource Scarcity",
            description="Resources are becoming scarce across the world",
            conditions=[scarcity_condition],
            probability=0.9,
            cooldown_weeks=4
        )
        self.events.append(scarcity_event)
    
    def _add_health_events(self):
        """Add health-related triggered events."""
        # Disease outbreak event
        disease_condition = EventCondition(
            name="disease_outbreak",
            description="Many animals have low health",
            check_function=self._check_disease_conditions,
            parameters={"health_threshold": 50, "affected_percentage": 0.4}
        )
        
        disease_event = DiseaseOutbreakEvent(
            event_id="disease_outbreak",
            name="Disease Outbreak",
            description="A disease spreads through the animal population",
            conditions=[disease_condition],
            probability=0.7,
            cooldown_weeks=8
        )
        self.events.append(disease_event)
    
    def check_and_execute_events(self, week: int) -> List[EventResult]:
        """Check all triggered events and execute those that should trigger."""
        results = []
        
        for event in self.events:
            try:
                if event.should_trigger(self.simulation):
                    # Apply probability check
                    if random.random() <= event.probability:
                        self.logger.info(f"Triggering event: {event.name}")
                        result = event.execute(self.simulation, week)
                        results.append(result)
                        
                        self.logger.info(f"Event result: {result.message}")
                    else:
                        self.logger.debug(f"Event {event.name} conditions met but failed probability check")
                        
            except Exception as e:
                self.logger.error(f"Error executing triggered event {event.event_id}: {e}")
                # Create error result
                error_result = EventResult(
                    event_id=event.event_id,
                    event_type=EventType.TRIGGERED,
                    success=False,
                    message=f"Event execution failed: {str(e)}"
                )
                results.append(error_result)
        
        return results
    
    def add_event(self, event: TriggeredEvent):
        """Add a custom triggered event."""
        self.events.append(event)
    
    def remove_event(self, event_id: str) -> bool:
        """Remove an event by ID."""
        initial_count = len(self.events)
        self.events = [e for e in self.events if e.event_id != event_id]
        return len(self.events) < initial_count
    
    # Condition check functions
    def _check_overpopulation(self, simulation: Simulation, threshold: int, area_size: int) -> bool:
        """Check if there are too many animals in a small area."""
        if not simulation.world:
            return False
        
        living_animals = simulation.get_living_animals()
        if len(living_animals) < threshold:
            return False
        
        # Check if most animals are clustered in a small area
        world_area = simulation.world.dimensions[0] * simulation.world.dimensions[1]
        density_threshold = threshold / area_size
        current_density = len(living_animals) / world_area
        
        return current_density > density_threshold
    
    def _check_near_extinction(self, simulation: Simulation, threshold: int) -> bool:
        """Check if population is near extinction."""
        living_animals = simulation.get_living_animals()
        return len(living_animals) <= threshold
    
    def _check_resource_scarcity(self, simulation: Simulation, threshold: float) -> bool:
        """Check if resources are becoming scarce."""
        if not simulation.world:
            return False
        
        total_tiles = 0
        tiles_with_resources = 0
        
        for x in range(simulation.world.dimensions[0]):
            for y in range(simulation.world.dimensions[1]):
                tile = simulation.world.get_tile(x, y)
                if tile:
                    total_tiles += 1
                    if tile.resource and tile.resource.uses_left > 0:
                        tiles_with_resources += 1
        
        if total_tiles == 0:
            return False
        
        resource_ratio = tiles_with_resources / total_tiles
        return resource_ratio < threshold
    
    def _check_disease_conditions(self, simulation: Simulation, health_threshold: int, affected_percentage: float) -> bool:
        """Check if conditions are right for a disease outbreak."""
        living_animals = simulation.get_living_animals()
        if len(living_animals) < 3:  # Need minimum population for disease
            return False
        
        unhealthy_animals = [
            animal for animal in living_animals 
            if animal.status.get('Health', 100) < health_threshold
        ]
        
        affected_ratio = len(unhealthy_animals) / len(living_animals)
        return affected_ratio >= affected_percentage


# Specific triggered event implementations
class OverpopulationEvent(TriggeredEvent):
    """Event triggered by overpopulation."""
    
    def execute(self, simulation: Simulation, week: int) -> EventResult:
        """Execute overpopulation event."""
        super().execute(simulation, week)
        
        living_animals = simulation.get_living_animals()
        affected_count = min(len(living_animals) // 3, 5)  # Affect up to 1/3 of population, max 5
        
        if affected_count == 0:
            return EventResult(
                event_id=self.event_id,
                event_type=self.event_type,
                success=True,
                message="Overpopulation event occurred but no animals were affected"
            )
        
        # Apply stress effects to random animals
        affected_animals = random.sample(living_animals, affected_count)
        effects_applied = 0
        
        for animal in affected_animals:
            # Reduce health due to competition stress
            current_health = animal.status.get('Health', 100)
            health_loss = random.randint(5, 15)
            animal.status['Health'] = max(10, current_health - health_loss)
            
            # Reduce energy due to competition
            current_energy = animal.status.get('Energy', 100)
            energy_loss = random.randint(10, 20)
            animal.status['Energy'] = max(5, current_energy - energy_loss)
            
            effects_applied += 1
        
        return EventResult(
            event_id=self.event_id,
            event_type=self.event_type,
            success=True,
            message=f"Overpopulation stress affected {affected_count} animals",
            affected_animals=[a.animal_id for a in affected_animals],
            effects_applied=effects_applied
        )


class ExtinctionThreatEvent(TriggeredEvent):
    """Event triggered when population is near extinction."""
    
    def execute(self, simulation: Simulation, week: int) -> EventResult:
        """Execute extinction threat event."""
        super().execute(simulation, week)
        
        living_animals = simulation.get_living_animals()
        
        # Boost remaining animals to give them a fighting chance
        effects_applied = 0
        for animal in living_animals:
            # Boost health
            current_health = animal.status.get('Health', 100)
            health_boost = random.randint(10, 25)
            animal.status['Health'] = min(100, current_health + health_boost)
            
            # Boost energy
            current_energy = animal.status.get('Energy', 100)
            energy_boost = random.randint(15, 30)
            animal.status['Energy'] = min(100, current_energy + energy_boost)
            
            effects_applied += 1
        
        return EventResult(
            event_id=self.event_id,
            event_type=self.event_type,
            success=True,
            message=f"Extinction threat event boosted {len(living_animals)} remaining animals",
            affected_animals=[a.animal_id for a in living_animals],
            effects_applied=effects_applied
        )


class ResourceScarcityEvent(TriggeredEvent):
    """Event triggered by resource scarcity."""
    
    def execute(self, simulation: Simulation, week: int) -> EventResult:
        """Execute resource scarcity event."""
        super().execute(simulation, week)
        
        if not simulation.world:
            return EventResult(
                event_id=self.event_id,
                event_type=self.event_type,
                success=False,
                message="No world available for resource scarcity event"
            )
        
        # Reduce all remaining resources
        resources_changed = 0
        for x in range(simulation.world.dimensions[0]):
            for y in range(simulation.world.dimensions[1]):
                tile = simulation.world.get_tile(x, y)
                if tile and tile.resource and tile.resource.uses_left > 0:
                    # Reduce resource by 1-3 uses
                    reduction = random.randint(1, 3)
                    tile.resource.uses_left = max(0, tile.resource.uses_left - reduction)
                    resources_changed += 1
        
        return EventResult(
            event_id=self.event_id,
            event_type=self.event_type,
            success=True,
            message=f"Resource scarcity reduced resources in {resources_changed} locations",
            resources_changed=resources_changed
        )


class DiseaseOutbreakEvent(TriggeredEvent):
    """Event triggered by disease outbreak conditions."""
    
    def execute(self, simulation: Simulation, week: int) -> EventResult:
        """Execute disease outbreak event."""
        super().execute(simulation, week)
        
        living_animals = simulation.get_living_animals()
        if len(living_animals) < 2:
            return EventResult(
                event_id=self.event_id,
                event_type=self.event_type,
                success=True,
                message="Disease outbreak event occurred but insufficient population to spread"
            )
        
        # Affect 30-60% of population
        infection_rate = random.uniform(0.3, 0.6)
        affected_count = int(len(living_animals) * infection_rate)
        affected_count = max(1, min(affected_count, len(living_animals)))
        
        affected_animals = random.sample(living_animals, affected_count)
        casualties = 0
        effects_applied = 0
        
        for animal in affected_animals:
            # Apply disease effects
            health_loss = random.randint(15, 35)
            current_health = animal.status.get('Health', 100)
            animal.status['Health'] = max(0, current_health - health_loss)
            
            # Apply energy drain
            energy_loss = random.randint(20, 40)
            current_energy = animal.status.get('Energy', 100)
            animal.status['Energy'] = max(0, current_energy - energy_loss)
            
            effects_applied += 1
            
            # Check for death
            if animal.status['Health'] <= 0:
                simulation.remove_animal(animal)
                casualties += 1
        
        return EventResult(
            event_id=self.event_id,
            event_type=self.event_type,
            success=True,
            message=f"Disease outbreak affected {affected_count} animals, {casualties} casualties",
            affected_animals=[a.animal_id for a in affected_animals],
            casualties=casualties,
            effects_applied=effects_applied
        )
