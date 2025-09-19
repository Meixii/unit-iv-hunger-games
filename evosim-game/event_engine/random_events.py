"""
Random Events System

This module handles events that occur randomly with specific probabilities.
Examples: weather changes, resource discoveries, beneficial mutations, etc.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import logging
import random

# Import from parent directory
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures import Simulation, Animal, Resource, ResourceType, TerrainType
from .event_data import Event, EventType, EventResult


@dataclass
class RandomEvent(Event):
    """Event that occurs randomly with a specific probability."""
    base_probability: float = 0.1  # Base chance per week
    probability_modifiers: Dict[str, float] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize random event."""
        self.event_type = EventType.RANDOM
        self.probability = self.base_probability
    
    def calculate_probability(self, simulation: Simulation) -> float:
        """Calculate the actual probability based on current conditions."""
        prob = self.base_probability
        
        # Apply modifiers based on simulation state
        for modifier_name, modifier_value in self.probability_modifiers.items():
            if modifier_name == "population_size":
                living_count = len(simulation.get_living_animals())
                if living_count > 10:
                    prob *= modifier_value
            elif modifier_name == "week_number":
                if simulation.current_week > 5:
                    prob *= modifier_value
            # Add more modifiers as needed
        
        return min(1.0, max(0.0, prob))  # Clamp between 0 and 1
    
    def should_occur(self, simulation: Simulation) -> bool:
        """Check if this random event should occur."""
        if not self.can_occur(simulation.current_week):
            return False
        
        current_probability = self.calculate_probability(simulation)
        return random.random() <= current_probability


class RandomEventEngine:
    """Engine for managing and executing random events."""
    
    def __init__(self, simulation: Simulation, logger: logging.Logger):
        """Initialize the random event engine."""
        self.simulation = simulation
        self.logger = logger
        self.events: List[RandomEvent] = []
        
        # Initialize default random events
        self._initialize_default_events()
    
    def _initialize_default_events(self):
        """Initialize default random events."""
        # Beneficial events
        self._add_beneficial_events()
        
        # Neutral events
        self._add_neutral_events()
        
        # Minor negative events
        self._add_minor_negative_events()
    
    def _add_beneficial_events(self):
        """Add beneficial random events."""
        # Resource discovery
        resource_discovery = ResourceDiscoveryEvent(
            event_id="resource_discovery",
            name="Resource Discovery",
            description="New resources are discovered in the world",
            base_probability=0.15,
            cooldown_weeks=3
        )
        self.events.append(resource_discovery)
        
        # Healing springs
        healing_springs = HealingEvent(
            event_id="healing_springs",
            name="Healing Springs",
            description="Natural healing springs restore animal health",
            base_probability=0.08,
            cooldown_weeks=4
        )
        self.events.append(healing_springs)
        
        # Abundant harvest
        abundant_harvest = AbundantHarvestEvent(
            event_id="abundant_harvest",
            name="Abundant Harvest",
            description="Plants and prey become more abundant",
            base_probability=0.12,
            cooldown_weeks=5
        )
        self.events.append(abundant_harvest)
    
    def _add_neutral_events(self):
        """Add neutral random events."""
        # Migration
        migration = MigrationEvent(
            event_id="migration",
            name="Animal Migration",
            description="Animals are compelled to move to new locations",
            base_probability=0.1,
            cooldown_weeks=3
        )
        self.events.append(migration)
        
        # Weather change
        weather_change = WeatherChangeEvent(
            event_id="weather_change",
            name="Weather Change",
            description="Weather patterns shift, affecting animal behavior",
            base_probability=0.2,
            cooldown_weeks=2
        )
        self.events.append(weather_change)
    
    def _add_minor_negative_events(self):
        """Add minor negative random events."""
        # Pest infestation
        pest_infestation = PestInfestationEvent(
            event_id="pest_infestation",
            name="Pest Infestation",
            description="Pests reduce available plant resources",
            base_probability=0.1,
            cooldown_weeks=4
        )
        self.events.append(pest_infestation)
        
        # Territorial dispute
        territorial_dispute = TerritorialDisputeEvent(
            event_id="territorial_dispute",
            name="Territorial Dispute",
            description="Animals become more aggressive over territory",
            base_probability=0.08,
            cooldown_weeks=3
        )
        self.events.append(territorial_dispute)
    
    def execute_random_events(self, week: int, max_events: int = 2) -> List[EventResult]:
        """Execute random events for the current week."""
        results = []
        events_executed = 0
        
        # Shuffle events to randomize execution order
        shuffled_events = self.events.copy()
        random.shuffle(shuffled_events)
        
        for event in shuffled_events:
            if events_executed >= max_events:
                break
            
            try:
                if event.should_occur(self.simulation):
                    self.logger.info(f"Random event occurring: {event.name}")
                    result = event.execute(self.simulation, week)
                    results.append(result)
                    events_executed += 1
                    
                    self.logger.info(f"Random event result: {result.message}")
                    
            except Exception as e:
                self.logger.error(f"Error executing random event {event.event_id}: {e}")
                # Create error result
                error_result = EventResult(
                    event_id=event.event_id,
                    event_type=EventType.RANDOM,
                    success=False,
                    message=f"Random event execution failed: {str(e)}"
                )
                results.append(error_result)
        
        return results
    
    def add_event(self, event: RandomEvent):
        """Add a custom random event."""
        self.events.append(event)
    
    def remove_event(self, event_id: str) -> bool:
        """Remove an event by ID."""
        initial_count = len(self.events)
        self.events = [e for e in self.events if e.event_id != event_id]
        return len(self.events) < initial_count


# Specific random event implementations
class ResourceDiscoveryEvent(RandomEvent):
    """Random event that adds new resources to the world."""
    
    def execute(self, simulation: Simulation, week: int) -> EventResult:
        """Execute resource discovery event."""
        super().execute(simulation, week)
        
        if not simulation.world:
            return EventResult(
                event_id=self.event_id,
                event_type=self.event_type,
                success=False,
                message="No world available for resource discovery"
            )
        
        # Find empty tiles to add resources to
        empty_tiles = []
        for x in range(simulation.world.dimensions[0]):
            for y in range(simulation.world.dimensions[1]):
                tile = simulation.world.get_tile(x, y)
                if (tile and 
                    tile.terrain_type in [TerrainType.PLAINS, TerrainType.FOREST] and
                    (not tile.resource or tile.resource.uses_left == 0)):
                    empty_tiles.append(tile)
        
        if not empty_tiles:
            return EventResult(
                event_id=self.event_id,
                event_type=self.event_type,
                success=True,
                message="Resource discovery event occurred but no suitable locations found"
            )
        
        # Add resources to 2-5 random empty tiles
        num_resources = min(random.randint(2, 5), len(empty_tiles))
        selected_tiles = random.sample(empty_tiles, num_resources)
        
        resources_added = 0
        for tile in selected_tiles:
            # Choose resource type based on terrain
            if tile.terrain_type == TerrainType.FOREST:
                resource_type = random.choice([ResourceType.PLANT, ResourceType.PREY])
            else:
                resource_type = ResourceType.PLANT
            
            # Create new resource
            uses = random.randint(3, 8)
            new_resource = Resource(
                resource_type=resource_type,
                quantity=uses,
                uses_left=uses
            )
            tile.resource = new_resource
            resources_added += 1
        
        return EventResult(
            event_id=self.event_id,
            event_type=self.event_type,
            success=True,
            message=f"Discovered {resources_added} new resource locations",
            resources_changed=resources_added
        )


class HealingEvent(RandomEvent):
    """Random event that heals animals."""
    
    def execute(self, simulation: Simulation, week: int) -> EventResult:
        """Execute healing event."""
        super().execute(simulation, week)
        
        living_animals = simulation.get_living_animals()
        if not living_animals:
            return EventResult(
                event_id=self.event_id,
                event_type=self.event_type,
                success=True,
                message="Healing springs appeared but no animals to heal"
            )
        
        # Heal 30-70% of animals
        heal_rate = random.uniform(0.3, 0.7)
        num_to_heal = int(len(living_animals) * heal_rate)
        num_to_heal = max(1, min(num_to_heal, len(living_animals)))
        
        healed_animals = random.sample(living_animals, num_to_heal)
        effects_applied = 0
        
        for animal in healed_animals:
            # Heal health
            current_health = animal.status.get('Health', 100)
            if current_health < 100:
                healing = random.randint(15, 35)
                animal.status['Health'] = min(100, current_health + healing)
                effects_applied += 1
            
            # Restore some energy
            current_energy = animal.status.get('Energy', 100)
            if current_energy < 100:
                energy_boost = random.randint(10, 20)
                animal.status['Energy'] = min(100, current_energy + energy_boost)
        
        return EventResult(
            event_id=self.event_id,
            event_type=self.event_type,
            success=True,
            message=f"Healing springs restored health to {num_to_heal} animals",
            affected_animals=[a.animal_id for a in healed_animals],
            effects_applied=effects_applied
        )


class AbundantHarvestEvent(RandomEvent):
    """Random event that increases resource abundance."""
    
    def execute(self, simulation: Simulation, week: int) -> EventResult:
        """Execute abundant harvest event."""
        super().execute(simulation, week)
        
        if not simulation.world:
            return EventResult(
                event_id=self.event_id,
                event_type=self.event_type,
                success=False,
                message="No world available for abundant harvest"
            )
        
        # Increase all existing resources
        resources_enhanced = 0
        for x in range(simulation.world.dimensions[0]):
            for y in range(simulation.world.dimensions[1]):
                tile = simulation.world.get_tile(x, y)
                if tile and tile.resource and tile.resource.uses_left > 0:
                    # Increase resource uses by 2-5
                    bonus_uses = random.randint(2, 5)
                    tile.resource.uses_left += bonus_uses
                    tile.resource.quantity += bonus_uses
                    resources_enhanced += 1
        
        return EventResult(
            event_id=self.event_id,
            event_type=self.event_type,
            success=True,
            message=f"Abundant harvest enhanced {resources_enhanced} resource locations",
            resources_changed=resources_enhanced
        )


class MigrationEvent(RandomEvent):
    """Random event that moves animals to new locations."""
    
    def execute(self, simulation: Simulation, week: int) -> EventResult:
        """Execute migration event."""
        super().execute(simulation, week)
        
        living_animals = simulation.get_living_animals()
        if not living_animals or not simulation.world:
            return EventResult(
                event_id=self.event_id,
                event_type=self.event_type,
                success=True,
                message="Migration event occurred but no animals to migrate"
            )
        
        # Migrate 20-50% of animals
        migration_rate = random.uniform(0.2, 0.5)
        num_to_migrate = int(len(living_animals) * migration_rate)
        num_to_migrate = max(1, min(num_to_migrate, len(living_animals)))
        
        migrating_animals = random.sample(living_animals, num_to_migrate)
        
        # Find valid migration locations
        valid_locations = []
        for x in range(simulation.world.dimensions[0]):
            for y in range(simulation.world.dimensions[1]):
                tile = simulation.world.get_tile(x, y)
                if (tile and 
                    tile.terrain_type != TerrainType.MOUNTAINS and 
                    tile.occupant is None):
                    valid_locations.append((x, y))
        
        if not valid_locations:
            return EventResult(
                event_id=self.event_id,
                event_type=self.event_type,
                success=True,
                message="Migration event occurred but no valid destinations found"
            )
        
        migrated_count = 0
        for animal in migrating_animals:
            if valid_locations:
                # Remove from current location
                old_x, old_y = animal.location
                old_tile = simulation.world.get_tile(old_x, old_y)
                if old_tile:
                    old_tile.occupant = None
                
                # Move to new location
                new_location = random.choice(valid_locations)
                valid_locations.remove(new_location)  # Prevent multiple animals in same spot
                
                new_x, new_y = new_location
                new_tile = simulation.world.get_tile(new_x, new_y)
                if new_tile:
                    animal.location = new_location
                    new_tile.occupant = animal
                    migrated_count += 1
        
        return EventResult(
            event_id=self.event_id,
            event_type=self.event_type,
            success=True,
            message=f"Migration event moved {migrated_count} animals to new locations",
            affected_animals=[a.animal_id for a in migrating_animals[:migrated_count]]
        )


class WeatherChangeEvent(RandomEvent):
    """Random event that affects animal energy and behavior."""
    
    def execute(self, simulation: Simulation, week: int) -> EventResult:
        """Execute weather change event."""
        super().execute(simulation, week)
        
        living_animals = simulation.get_living_animals()
        if not living_animals:
            return EventResult(
                event_id=self.event_id,
                event_type=self.event_type,
                success=True,
                message="Weather change occurred but no animals to affect"
            )
        
        # Weather can be beneficial or detrimental
        weather_types = [
            ("mild_weather", "Mild weather boosts animal energy", 1),
            ("harsh_weather", "Harsh weather drains animal energy", -1),
            ("perfect_weather", "Perfect weather greatly boosts animals", 2)
        ]
        
        weather_type, weather_desc, effect_multiplier = random.choice(weather_types)
        
        effects_applied = 0
        for animal in living_animals:
            if effect_multiplier > 0:
                # Beneficial weather
                energy_change = random.randint(5, 15) * effect_multiplier
                current_energy = animal.status.get('Energy', 100)
                animal.status['Energy'] = min(100, current_energy + energy_change)
            else:
                # Harsh weather
                energy_change = random.randint(5, 15) * abs(effect_multiplier)
                current_energy = animal.status.get('Energy', 100)
                animal.status['Energy'] = max(10, current_energy - energy_change)
            
            effects_applied += 1
        
        return EventResult(
            event_id=self.event_id,
            event_type=self.event_type,
            success=True,
            message=f"{weather_desc} affecting {len(living_animals)} animals",
            affected_animals=[a.animal_id for a in living_animals],
            effects_applied=effects_applied
        )


class PestInfestationEvent(RandomEvent):
    """Random event that reduces plant resources."""
    
    def execute(self, simulation: Simulation, week: int) -> EventResult:
        """Execute pest infestation event."""
        super().execute(simulation, week)
        
        if not simulation.world:
            return EventResult(
                event_id=self.event_id,
                event_type=self.event_type,
                success=False,
                message="No world available for pest infestation"
            )
        
        # Reduce plant resources
        plants_affected = 0
        for x in range(simulation.world.dimensions[0]):
            for y in range(simulation.world.dimensions[1]):
                tile = simulation.world.get_tile(x, y)
                if (tile and 
                    tile.resource and 
                    tile.resource.resource_type == ResourceType.PLANT and
                    tile.resource.uses_left > 0):
                    
                    # 60% chance to affect each plant
                    if random.random() < 0.6:
                        reduction = random.randint(1, 3)
                        tile.resource.uses_left = max(0, tile.resource.uses_left - reduction)
                        plants_affected += 1
        
        return EventResult(
            event_id=self.event_id,
            event_type=self.event_type,
            success=True,
            message=f"Pest infestation reduced {plants_affected} plant resources",
            resources_changed=plants_affected
        )


class TerritorialDisputeEvent(RandomEvent):
    """Random event that increases animal aggression."""
    
    def execute(self, simulation: Simulation, week: int) -> EventResult:
        """Execute territorial dispute event."""
        super().execute(simulation, week)
        
        living_animals = simulation.get_living_animals()
        if len(living_animals) < 2:
            return EventResult(
                event_id=self.event_id,
                event_type=self.event_type,
                success=True,
                message="Territorial dispute event occurred but insufficient animals for disputes"
            )
        
        # Affect 30-60% of animals with increased aggression/stress
        dispute_rate = random.uniform(0.3, 0.6)
        num_affected = int(len(living_animals) * dispute_rate)
        num_affected = max(2, min(num_affected, len(living_animals)))
        
        affected_animals = random.sample(living_animals, num_affected)
        effects_applied = 0
        
        for animal in affected_animals:
            # Increase stress (reduce health slightly)
            current_health = animal.status.get('Health', 100)
            stress_damage = random.randint(3, 8)
            animal.status['Health'] = max(20, current_health - stress_damage)
            
            # Increase energy expenditure
            current_energy = animal.status.get('Energy', 100)
            energy_loss = random.randint(5, 12)
            animal.status['Energy'] = max(10, current_energy - energy_loss)
            
            effects_applied += 1
        
        return EventResult(
            event_id=self.event_id,
            event_type=self.event_type,
            success=True,
            message=f"Territorial disputes stressed {num_affected} animals",
            affected_animals=[a.animal_id for a in affected_animals],
            effects_applied=effects_applied
        )
