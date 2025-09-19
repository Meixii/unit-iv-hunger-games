"""
Disaster Events System

This module handles large-scale disaster events that can significantly impact
the simulation world and animal populations. These events are more severe
than regular random events and often have area-of-effect mechanics.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set
import logging
import random
import math

# Import from parent directory
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures import Simulation, Animal, TerrainType, Resource, ResourceType
from .event_data import Event, EventType, EventResult


@dataclass
class DisasterEvent(Event):
    """Event representing a large-scale disaster."""
    severity: str = "moderate"  # "minor", "moderate", "major", "catastrophic"
    area_of_effect: int = 3  # Radius of effect in tiles
    epicenter: Optional[Tuple[int, int]] = None  # Will be randomly chosen if None
    
    def __post_init__(self):
        """Initialize disaster event."""
        self.event_type = EventType.DISASTER
    
    def calculate_affected_area(self, simulation: Simulation) -> Set[Tuple[int, int]]:
        """Calculate which tiles are affected by the disaster."""
        if not simulation.world:
            return set()
        
        # Choose epicenter if not specified
        if self.epicenter is None:
            world_width, world_height = simulation.world.dimensions
            self.epicenter = (
                random.randint(0, world_width - 1),
                random.randint(0, world_height - 1)
            )
        
        affected_tiles = set()
        epicenter_x, epicenter_y = self.epicenter
        
        # Calculate tiles within radius
        for x in range(simulation.world.dimensions[0]):
            for y in range(simulation.world.dimensions[1]):
                distance = math.sqrt((x - epicenter_x) ** 2 + (y - epicenter_y) ** 2)
                if distance <= self.area_of_effect:
                    affected_tiles.add((x, y))
        
        return affected_tiles
    
    def get_severity_multiplier(self) -> float:
        """Get damage multiplier based on severity."""
        multipliers = {
            "minor": 0.5,
            "moderate": 1.0,
            "major": 1.5,
            "catastrophic": 2.0
        }
        return multipliers.get(self.severity, 1.0)


class DisasterEventEngine:
    """Engine for managing and executing disaster events."""
    
    def __init__(self, simulation: Simulation, logger: logging.Logger):
        """Initialize the disaster event engine."""
        self.simulation = simulation
        self.logger = logger
        self.events: List[DisasterEvent] = []
        
        # Initialize default disaster events
        self._initialize_default_disasters()
    
    def _initialize_default_disasters(self):
        """Initialize default disaster events."""
        # Natural disasters
        self._add_natural_disasters()
        
        # Environmental disasters
        self._add_environmental_disasters()
        
        # Biological disasters
        self._add_biological_disasters()
    
    def _add_natural_disasters(self):
        """Add natural disaster events."""
        # Earthquake
        earthquake = EarthquakeEvent(
            event_id="earthquake",
            name="Earthquake",
            description="A powerful earthquake shakes the ground",
            probability=0.05,  # 5% chance per week
            severity="major",
            area_of_effect=4,
            cooldown_weeks=10,
            max_occurrences=3
        )
        self.events.append(earthquake)
        
        # Wildfire
        wildfire = WildfireEvent(
            event_id="wildfire",
            name="Wildfire",
            description="A devastating fire spreads across the land",
            probability=0.08,
            severity="major",
            area_of_effect=5,
            cooldown_weeks=8,
            max_occurrences=2
        )
        self.events.append(wildfire)
        
        # Flood
        flood = FloodEvent(
            event_id="flood",
            name="Flash Flood",
            description="Heavy rains cause severe flooding",
            probability=0.06,
            severity="moderate",
            area_of_effect=3,
            cooldown_weeks=6,
            max_occurrences=4
        )
        self.events.append(flood)
    
    def _add_environmental_disasters(self):
        """Add environmental disaster events."""
        # Drought
        drought = DroughtEvent(
            event_id="drought",
            name="Severe Drought",
            description="Extended drought devastates water and plant resources",
            probability=0.04,
            severity="major",
            area_of_effect=6,  # Large area effect
            cooldown_weeks=12,
            max_occurrences=2
        )
        self.events.append(drought)
        
        # Toxic spill
        toxic_spill = ToxicSpillEvent(
            event_id="toxic_spill",
            name="Toxic Contamination",
            description="Toxic materials contaminate the environment",
            probability=0.03,
            severity="catastrophic",
            area_of_effect=2,
            cooldown_weeks=15,
            max_occurrences=1
        )
        self.events.append(toxic_spill)
    
    def _add_biological_disasters(self):
        """Add biological disaster events."""
        # Plague
        plague = PlagueEvent(
            event_id="plague",
            name="Plague Outbreak",
            description="A deadly plague spreads among the animal population",
            probability=0.02,
            severity="catastrophic",
            area_of_effect=4,
            cooldown_weeks=20,
            max_occurrences=1
        )
        self.events.append(plague)
        
        # Predator invasion
        predator_invasion = PredatorInvasionEvent(
            event_id="predator_invasion",
            name="Predator Invasion",
            description="Dangerous predators invade the territory",
            probability=0.06,
            severity="moderate",
            area_of_effect=3,
            cooldown_weeks=8,
            max_occurrences=3
        )
        self.events.append(predator_invasion)
    
    def execute_disaster_events(self, week: int, max_disasters: int = 1) -> List[EventResult]:
        """Execute disaster events for the current week."""
        results = []
        disasters_executed = 0
        
        # Shuffle events to randomize execution order
        shuffled_events = self.events.copy()
        random.shuffle(shuffled_events)
        
        for event in shuffled_events:
            if disasters_executed >= max_disasters:
                break
            
            try:
                if event.can_occur(week) and random.random() <= event.probability:
                    self.logger.warning(f"DISASTER EVENT: {event.name}")
                    result = event.execute(self.simulation, week)
                    results.append(result)
                    disasters_executed += 1
                    
                    self.logger.warning(f"Disaster result: {result.message}")
                    
            except Exception as e:
                self.logger.error(f"Error executing disaster event {event.event_id}: {e}")
                # Create error result
                error_result = EventResult(
                    event_id=event.event_id,
                    event_type=EventType.DISASTER,
                    success=False,
                    message=f"Disaster event execution failed: {str(e)}"
                )
                results.append(error_result)
        
        return results
    
    def add_event(self, event: DisasterEvent):
        """Add a custom disaster event."""
        self.events.append(event)
    
    def remove_event(self, event_id: str) -> bool:
        """Remove an event by ID."""
        initial_count = len(self.events)
        self.events = [e for e in self.events if e.event_id != event_id]
        return len(self.events) < initial_count


# Specific disaster event implementations
class EarthquakeEvent(DisasterEvent):
    """Earthquake disaster that damages animals and destroys resources."""
    
    def execute(self, simulation: Simulation, week: int) -> EventResult:
        """Execute earthquake disaster."""
        super().execute(simulation, week)
        
        if not simulation.world:
            return EventResult(
                event_id=self.event_id,
                event_type=self.event_type,
                success=False,
                message="No world available for earthquake"
            )
        
        affected_area = self.calculate_affected_area(simulation)
        severity_multiplier = self.get_severity_multiplier()
        
        affected_animals = []
        casualties = 0
        resources_destroyed = 0
        effects_applied = 0
        
        # Find animals in affected area
        for animal in simulation.get_living_animals():
            if animal.location in affected_area:
                affected_animals.append(animal)
        
        # Apply earthquake effects to animals
        for animal in affected_animals:
            # Calculate distance from epicenter for damage scaling
            distance = math.sqrt(
                (animal.location[0] - self.epicenter[0]) ** 2 + 
                (animal.location[1] - self.epicenter[1]) ** 2
            )
            
            # Closer animals take more damage
            distance_factor = max(0.3, 1.0 - (distance / self.area_of_effect))
            
            # Apply damage
            base_damage = random.randint(20, 40)
            actual_damage = int(base_damage * severity_multiplier * distance_factor)
            
            current_health = animal.status.get('Health', 100)
            animal.status['Health'] = max(0, current_health - actual_damage)
            
            # Apply energy loss from trauma
            energy_loss = random.randint(15, 25)
            current_energy = animal.status.get('Energy', 100)
            animal.status['Energy'] = max(0, current_energy - energy_loss)
            
            effects_applied += 1
            
            # Check for death
            if animal.status['Health'] <= 0:
                simulation.remove_animal(animal)
                casualties += 1
        
        # Destroy resources in affected area
        for x, y in affected_area:
            tile = simulation.world.get_tile(x, y)
            if tile and tile.resource and tile.resource.uses_left > 0:
                # 70% chance to destroy or damage resource
                if random.random() < 0.7:
                    if random.random() < 0.5:
                        # Completely destroy resource
                        tile.resource = None
                    else:
                        # Partially damage resource
                        damage = random.randint(2, 5)
                        tile.resource.uses_left = max(0, tile.resource.uses_left - damage)
                    resources_destroyed += 1
        
        return EventResult(
            event_id=self.event_id,
            event_type=self.event_type,
            success=True,
            message=f"Earthquake devastated {len(affected_area)} tiles, {casualties} casualties, {resources_destroyed} resources destroyed",
            affected_animals=[a.animal_id for a in affected_animals],
            casualties=casualties,
            effects_applied=effects_applied,
            resources_changed=resources_destroyed,
            terrain_modified=True
        )


class WildfireEvent(DisasterEvent):
    """Wildfire disaster that spreads and destroys vegetation."""
    
    def execute(self, simulation: Simulation, week: int) -> EventResult:
        """Execute wildfire disaster."""
        super().execute(simulation, week)
        
        if not simulation.world:
            return EventResult(
                event_id=self.event_id,
                event_type=self.event_type,
                success=False,
                message="No world available for wildfire"
            )
        
        affected_area = self.calculate_affected_area(simulation)
        severity_multiplier = self.get_severity_multiplier()
        
        affected_animals = []
        casualties = 0
        resources_destroyed = 0
        effects_applied = 0
        
        # Find animals in affected area
        for animal in simulation.get_living_animals():
            if animal.location in affected_area:
                affected_animals.append(animal)
        
        # Apply fire effects to animals
        for animal in affected_animals:
            # Fire damage
            fire_damage = random.randint(25, 45)
            actual_damage = int(fire_damage * severity_multiplier)
            
            current_health = animal.status.get('Health', 100)
            animal.status['Health'] = max(0, current_health - actual_damage)
            
            # Smoke inhalation (energy loss)
            energy_loss = random.randint(20, 35)
            current_energy = animal.status.get('Energy', 100)
            animal.status['Energy'] = max(0, current_energy - energy_loss)
            
            effects_applied += 1
            
            # Check for death
            if animal.status['Health'] <= 0:
                simulation.remove_animal(animal)
                casualties += 1
        
        # Destroy vegetation and resources
        for x, y in affected_area:
            tile = simulation.world.get_tile(x, y)
            if tile:
                # Destroy plant resources completely
                if (tile.resource and 
                    tile.resource.resource_type in [ResourceType.PLANT]):
                    tile.resource = None
                    resources_destroyed += 1
                
                # Damage other resources
                elif tile.resource and tile.resource.uses_left > 0:
                    if random.random() < 0.4:  # 40% chance
                        damage = random.randint(3, 6)
                        tile.resource.uses_left = max(0, tile.resource.uses_left - damage)
                        resources_destroyed += 1
        
        return EventResult(
            event_id=self.event_id,
            event_type=self.event_type,
            success=True,
            message=f"Wildfire burned {len(affected_area)} tiles, {casualties} casualties, {resources_destroyed} resources destroyed",
            affected_animals=[a.animal_id for a in affected_animals],
            casualties=casualties,
            effects_applied=effects_applied,
            resources_changed=resources_destroyed,
            terrain_modified=True
        )


class FloodEvent(DisasterEvent):
    """Flood disaster that affects low-lying areas."""
    
    def execute(self, simulation: Simulation, week: int) -> EventResult:
        """Execute flood disaster."""
        super().execute(simulation, week)
        
        if not simulation.world:
            return EventResult(
                event_id=self.event_id,
                event_type=self.event_type,
                success=False,
                message="No world available for flood"
            )
        
        affected_area = self.calculate_affected_area(simulation)
        severity_multiplier = self.get_severity_multiplier()
        
        affected_animals = []
        casualties = 0
        resources_destroyed = 0
        effects_applied = 0
        
        # Find animals in affected area
        for animal in simulation.get_living_animals():
            if animal.location in affected_area:
                affected_animals.append(animal)
        
        # Apply flood effects to animals
        for animal in affected_animals:
            # Drowning/hypothermia damage
            flood_damage = random.randint(15, 30)
            actual_damage = int(flood_damage * severity_multiplier)
            
            current_health = animal.status.get('Health', 100)
            animal.status['Health'] = max(0, current_health - actual_damage)
            
            # Exhaustion from swimming/escaping
            energy_loss = random.randint(25, 40)
            current_energy = animal.status.get('Energy', 100)
            animal.status['Energy'] = max(0, current_energy - energy_loss)
            
            effects_applied += 1
            
            # Check for death
            if animal.status['Health'] <= 0:
                simulation.remove_animal(animal)
                casualties += 1
        
        # Destroy or damage resources
        for x, y in affected_area:
            tile = simulation.world.get_tile(x, y)
            if tile and tile.resource and tile.resource.uses_left > 0:
                # 60% chance to damage resource
                if random.random() < 0.6:
                    damage = random.randint(2, 4)
                    tile.resource.uses_left = max(0, tile.resource.uses_left - damage)
                    resources_destroyed += 1
        
        return EventResult(
            event_id=self.event_id,
            event_type=self.event_type,
            success=True,
            message=f"Flood inundated {len(affected_area)} tiles, {casualties} casualties, {resources_destroyed} resources damaged",
            affected_animals=[a.animal_id for a in affected_animals],
            casualties=casualties,
            effects_applied=effects_applied,
            resources_changed=resources_destroyed
        )


class DroughtEvent(DisasterEvent):
    """Drought disaster that affects water and plant resources."""
    
    def execute(self, simulation: Simulation, week: int) -> EventResult:
        """Execute drought disaster."""
        super().execute(simulation, week)
        
        if not simulation.world:
            return EventResult(
                event_id=self.event_id,
                event_type=self.event_type,
                success=False,
                message="No world available for drought"
            )
        
        affected_area = self.calculate_affected_area(simulation)
        severity_multiplier = self.get_severity_multiplier()
        
        affected_animals = []
        resources_destroyed = 0
        effects_applied = 0
        
        # Find animals in affected area
        for animal in simulation.get_living_animals():
            if animal.location in affected_area:
                affected_animals.append(animal)
        
        # Apply drought effects to animals (dehydration)
        for animal in affected_animals:
            # Increased thirst depletion
            thirst_loss = random.randint(10, 20)
            actual_loss = int(thirst_loss * severity_multiplier)
            
            current_thirst = animal.status.get('Thirst', 100)
            animal.status['Thirst'] = max(0, current_thirst - actual_loss)
            
            # Health loss from dehydration
            if animal.status['Thirst'] < 30:
                health_loss = random.randint(5, 15)
                current_health = animal.status.get('Health', 100)
                animal.status['Health'] = max(0, current_health - health_loss)
            
            effects_applied += 1
        
        # Destroy water and plant resources
        for x, y in affected_area:
            tile = simulation.world.get_tile(x, y)
            if tile and tile.resource:
                if tile.resource.resource_type == ResourceType.WATER:
                    # Severely reduce or eliminate water
                    reduction = int(tile.resource.uses_left * 0.7 * severity_multiplier)
                    tile.resource.uses_left = max(0, tile.resource.uses_left - reduction)
                    resources_destroyed += 1
                elif tile.resource.resource_type == ResourceType.PLANT:
                    # Wither plants
                    reduction = int(tile.resource.uses_left * 0.5 * severity_multiplier)
                    tile.resource.uses_left = max(0, tile.resource.uses_left - reduction)
                    resources_destroyed += 1
        
        return EventResult(
            event_id=self.event_id,
            event_type=self.event_type,
            success=True,
            message=f"Drought affected {len(affected_area)} tiles, {len(affected_animals)} animals dehydrated, {resources_destroyed} resources depleted",
            affected_animals=[a.animal_id for a in affected_animals],
            effects_applied=effects_applied,
            resources_changed=resources_destroyed
        )


class ToxicSpillEvent(DisasterEvent):
    """Toxic contamination disaster with long-lasting effects."""
    
    def execute(self, simulation: Simulation, week: int) -> EventResult:
        """Execute toxic spill disaster."""
        super().execute(simulation, week)
        
        if not simulation.world:
            return EventResult(
                event_id=self.event_id,
                event_type=self.event_type,
                success=False,
                message="No world available for toxic spill"
            )
        
        affected_area = self.calculate_affected_area(simulation)
        severity_multiplier = self.get_severity_multiplier()
        
        affected_animals = []
        casualties = 0
        resources_destroyed = 0
        effects_applied = 0
        
        # Find animals in affected area
        for animal in simulation.get_living_animals():
            if animal.location in affected_area:
                affected_animals.append(animal)
        
        # Apply toxic effects to animals
        for animal in affected_animals:
            # Severe poisoning damage
            poison_damage = random.randint(30, 50)
            actual_damage = int(poison_damage * severity_multiplier)
            
            current_health = animal.status.get('Health', 100)
            animal.status['Health'] = max(0, current_health - actual_damage)
            
            # Toxic shock (energy loss)
            energy_loss = random.randint(35, 50)
            current_energy = animal.status.get('Energy', 100)
            animal.status['Energy'] = max(0, current_energy - energy_loss)
            
            effects_applied += 1
            
            # High mortality rate
            if animal.status['Health'] <= 0:
                simulation.remove_animal(animal)
                casualties += 1
        
        # Contaminate all resources in area
        for x, y in affected_area:
            tile = simulation.world.get_tile(x, y)
            if tile and tile.resource:
                # Completely destroy contaminated resources
                tile.resource = None
                resources_destroyed += 1
        
        return EventResult(
            event_id=self.event_id,
            event_type=self.event_type,
            success=True,
            message=f"Toxic contamination devastated {len(affected_area)} tiles, {casualties} casualties, {resources_destroyed} resources contaminated",
            affected_animals=[a.animal_id for a in affected_animals],
            casualties=casualties,
            effects_applied=effects_applied,
            resources_changed=resources_destroyed,
            terrain_modified=True
        )


class PlagueEvent(DisasterEvent):
    """Plague disaster that spreads among animals."""
    
    def execute(self, simulation: Simulation, week: int) -> EventResult:
        """Execute plague disaster."""
        super().execute(simulation, week)
        
        living_animals = simulation.get_living_animals()
        if len(living_animals) < 2:
            return EventResult(
                event_id=self.event_id,
                event_type=self.event_type,
                success=True,
                message="Plague event occurred but insufficient population to spread"
            )
        
        severity_multiplier = self.get_severity_multiplier()
        
        # Plague spreads to 50-80% of population
        infection_rate = random.uniform(0.5, 0.8) * severity_multiplier
        num_infected = int(len(living_animals) * infection_rate)
        num_infected = min(num_infected, len(living_animals))
        
        infected_animals = random.sample(living_animals, num_infected)
        casualties = 0
        effects_applied = 0
        
        # Apply plague effects
        for animal in infected_animals:
            # Severe health loss
            plague_damage = random.randint(40, 70)
            actual_damage = int(plague_damage * severity_multiplier)
            
            current_health = animal.status.get('Health', 100)
            animal.status['Health'] = max(0, current_health - actual_damage)
            
            # Weakness (energy loss)
            energy_loss = random.randint(30, 50)
            current_energy = animal.status.get('Energy', 100)
            animal.status['Energy'] = max(0, current_energy - energy_loss)
            
            effects_applied += 1
            
            # High mortality rate
            if animal.status['Health'] <= 0:
                simulation.remove_animal(animal)
                casualties += 1
        
        return EventResult(
            event_id=self.event_id,
            event_type=self.event_type,
            success=True,
            message=f"Plague infected {num_infected} animals, {casualties} casualties",
            affected_animals=[a.animal_id for a in infected_animals],
            casualties=casualties,
            effects_applied=effects_applied
        )


class PredatorInvasionEvent(DisasterEvent):
    """Predator invasion disaster that threatens animals."""
    
    def execute(self, simulation: Simulation, week: int) -> EventResult:
        """Execute predator invasion disaster."""
        super().execute(simulation, week)
        
        if not simulation.world:
            return EventResult(
                event_id=self.event_id,
                event_type=self.event_type,
                success=False,
                message="No world available for predator invasion"
            )
        
        affected_area = self.calculate_affected_area(simulation)
        severity_multiplier = self.get_severity_multiplier()
        
        affected_animals = []
        casualties = 0
        effects_applied = 0
        
        # Find animals in affected area
        for animal in simulation.get_living_animals():
            if animal.location in affected_area:
                affected_animals.append(animal)
        
        if not affected_animals:
            return EventResult(
                event_id=self.event_id,
                event_type=self.event_type,
                success=True,
                message="Predator invasion occurred but no animals in affected area"
            )
        
        # Apply predator attack effects
        for animal in affected_animals:
            # Predator attack chance based on animal strength
            attack_chance = 0.4 * severity_multiplier
            strength = animal.traits.get('STR', 50)
            
            # Stronger animals have better survival chance
            if strength > 70:
                attack_chance *= 0.6
            elif strength < 40:
                attack_chance *= 1.4
            
            if random.random() < attack_chance:
                # Animal is attacked
                attack_damage = random.randint(20, 40)
                actual_damage = int(attack_damage * severity_multiplier)
                
                current_health = animal.status.get('Health', 100)
                animal.status['Health'] = max(0, current_health - actual_damage)
                
                # Stress and exhaustion from escape attempt
                energy_loss = random.randint(15, 30)
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
            message=f"Predator invasion in {len(affected_area)} tiles, {casualties} casualties from {len(affected_animals)} animals",
            affected_animals=[a.animal_id for a in affected_animals],
            casualties=casualties,
            effects_applied=effects_applied
        )
