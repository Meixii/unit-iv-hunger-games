"""
EvoSim Core Data Structures

This module contains all the core data classes for the EvoSim simulation.
These classes represent the fundamental entities in the game world.

Reference: Section XI - Conceptual Data Structure from documentation.md
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import random
import constants


# =============================================================================
# ENUMS AND CONSTANTS
# =============================================================================

class AnimalCategory(Enum):
    """Animal categories with their primary traits."""
    HERBIVORE = "Herbivore"
    CARNIVORE = "Carnivore"
    OMNIVORE = "Omnivore"


class TerrainType(Enum):
    """Terrain types available in the world."""
    PLAINS = "Plains"
    FOREST = "Forest"
    JUNGLE = "Jungle"
    WATER = "Water"
    SWAMP = "Swamp"
    MOUNTAINS = "Mountains"


class ResourceType(Enum):
    """Resource types available in the world."""
    PLANT = "Plant"
    PREY = "Prey"
    WATER = "Water"
    CARCASS = "Carcass"


class EffectType(Enum):
    """Effect types for buffs and debuffs."""
    WELL_FED = "Well-Fed"
    HYDRATED = "Hydrated"
    RESTED = "Rested"
    ADRENALINE_RUSH = "Adrenaline Rush"
    INJURED = "Injured"
    POISONED = "Poisoned"
    EXHAUSTED = "Exhausted"
    SICK = "Sick"


class ActionType(Enum):
    """Available actions for animals."""
    MOVE_NORTH = "Move North"
    MOVE_EAST = "Move East"
    MOVE_SOUTH = "Move South"
    MOVE_WEST = "Move West"
    REST = "Rest"
    EAT = "Eat"
    DRINK = "Drink"
    ATTACK = "Attack"


# =============================================================================
# CORE DATA CLASSES
# =============================================================================

@dataclass
class Effect:
    """Represents a temporary effect (buff or debuff) applied to an animal."""
    name: str
    duration: int
    modifiers: Dict[str, float] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate effect data after initialization."""
        if self.duration <= 0:
            raise ValueError(f"Effect duration must be positive, got {self.duration}")
        if not isinstance(self.modifiers, dict):
            raise ValueError("Effect modifiers must be a dictionary")
    
    def is_expired(self) -> bool:
        """Check if the effect has expired."""
        return self.duration <= 0
    
    def tick(self) -> None:
        """Reduce duration by 1 turn."""
        if self.duration > 0:
            self.duration -= 1


@dataclass
class Resource:
    """Represents a resource that can be consumed by animals."""
    resource_type: ResourceType
    quantity: int
    uses_left: int
    
    def __post_init__(self):
        """Validate resource data after initialization."""
        if self.quantity <= 0:
            raise ValueError(f"Resource quantity must be positive, got {self.quantity}")
        if self.uses_left <= 0:
            raise ValueError(f"Resource uses_left must be positive, got {self.uses_left}")
    
    def consume(self) -> int:
        """Consume one use of the resource and return the quantity gained."""
        if self.uses_left <= 0:
            return 0
        
        self.uses_left -= 1
        return self.quantity
    
    def is_depleted(self) -> bool:
        """Check if the resource is completely depleted."""
        return self.uses_left <= 0


@dataclass
class Tile:
    """Represents a single tile in the world grid."""
    coordinates: Tuple[int, int]
    terrain_type: TerrainType
    resource: Optional[Resource] = None
    occupant: Optional['Animal'] = None
    
    def __post_init__(self):
        """Validate tile data after initialization."""
        if len(self.coordinates) != 2:
            raise ValueError(f"Coordinates must be a tuple of 2 integers, got {self.coordinates}")
        if not all(isinstance(coord, int) and coord >= 0 for coord in self.coordinates):
            raise ValueError(f"Coordinates must be non-negative integers, got {self.coordinates}")
    
    def is_occupied(self) -> bool:
        """Check if the tile is occupied by an animal."""
        return self.occupant is not None
    
    def is_passable(self) -> bool:
        """Check if the tile can be moved onto."""
        return self.terrain_type != TerrainType.MOUNTAINS and not self.is_occupied()
    
    def get_movement_cost(self) -> float:
        """Get the movement cost multiplier for this terrain."""
        return constants.TERRAIN_MOVEMENT_MODIFIERS.get(self.terrain_type.value, 1.0)


@dataclass
class World:
    """Represents the game world containing all tiles."""
    grid: List[List[Tile]]
    dimensions: Tuple[int, int]
    
    def __post_init__(self):
        """Validate world data after initialization."""
        if len(self.grid) != self.dimensions[1]:
            raise ValueError(f"Grid height {len(self.grid)} doesn't match dimensions {self.dimensions}")
        if len(self.grid) > 0 and len(self.grid[0]) != self.dimensions[0]:
            raise ValueError(f"Grid width {len(self.grid[0])} doesn't match dimensions {self.dimensions}")
    
    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        """Get a tile at the specified coordinates."""
        if 0 <= x < self.dimensions[0] and 0 <= y < self.dimensions[1]:
            return self.grid[y][x]
        return None
    
    def is_valid_coordinate(self, x: int, y: int) -> bool:
        """Check if coordinates are within world bounds."""
        return 0 <= x < self.dimensions[0] and 0 <= y < self.dimensions[1]
    
    def get_adjacent_tiles(self, x: int, y: int) -> List[Tile]:
        """Get all valid adjacent tiles."""
        adjacent = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = x + dx, y + dy
            if self.is_valid_coordinate(new_x, new_y):
                adjacent.append(self.get_tile(new_x, new_y))
        return adjacent


@dataclass
class Animal:
    """Represents an animal in the simulation."""
    animal_id: str
    category: AnimalCategory
    traits: Dict[str, int]
    status: Dict[str, float]
    passive: Optional[str] = None
    active_effects: List[Effect] = field(default_factory=list)
    location: Tuple[int, int] = (0, 0)
    fitness_score_components: Dict[str, float] = field(default_factory=dict)
    mlp_network: Optional[Any] = None  # Will be set when MLP is implemented
    
    def __post_init__(self):
        """Validate animal data after initialization."""
        # Normalize and validate traits (accept long or short keys)
        long_to_short = {
            'Strength': 'STR',
            'Agility': 'AGI',
            'Intelligence': 'INT',
            'Endurance': 'END',
            'Perception': 'PER',
        }
        normalized_traits: Dict[str, int] = {}
        for key, value in list(self.traits.items()):
            short_key = long_to_short.get(key, key)
            normalized_traits[short_key] = value
        self.traits = normalized_traits

        required_traits = constants.TRAIT_NAMES
        for trait in required_traits:
            if trait not in self.traits:
                raise ValueError(f"Missing required trait: {trait}")
            if not isinstance(self.traits[trait], int) or self.traits[trait] < 1:
                raise ValueError(f"Trait {trait} must be a positive integer, got {self.traits[trait]}")
        
        # Ensure default Instinct if missing; then validate status
        if 'Instinct' not in self.status:
            self.status['Instinct'] = 0.0

        required_status = constants.STATUS_NAMES
        for status in required_status:
            if status not in self.status:
                raise ValueError(f"Missing required status: {status}")
            if not isinstance(self.status[status], (int, float)):
                raise ValueError(f"Status {status} must be a number, got {self.status[status]}")
        
        # Validate category
        if self.category not in AnimalCategory:
            raise ValueError(f"Invalid animal category: {self.category}")
        
        # Derive passive from category if not provided
        if not self.passive:
            category_to_passive = {
                AnimalCategory.HERBIVORE: "Efficient Grazer",
                AnimalCategory.CARNIVORE: "Ambush Predator",
                AnimalCategory.OMNIVORE: "Iron Stomach",
            }
            self.passive = category_to_passive.get(self.category, "")

        # Validate location
        if len(self.location) != 2:
            raise ValueError(f"Location must be a tuple of 2 integers, got {self.location}")
        if not all(isinstance(coord, int) for coord in self.location):
            raise ValueError(f"Location coordinates must be integers, got {self.location}")
    
    def get_max_health(self) -> int:
        """Calculate maximum health based on endurance."""
        return constants.BASE_HEALTH + (self.traits['END'] * constants.HEALTH_PER_ENDURANCE)
    
    def get_max_energy(self) -> int:
        """Calculate maximum energy based on endurance."""
        return constants.BASE_ENERGY + (self.traits['END'] * constants.ENERGY_PER_ENDURANCE)
    
    def get_effective_trait(self, trait_name: str) -> int:
        """Get effective trait value including all active effects."""
        base_value = self.traits[trait_name]
        
        # Apply effects
        for effect in self.active_effects:
            if trait_name in effect.modifiers:
                base_value += effect.modifiers[trait_name]
        
        return max(1, base_value)  # Ensure minimum value of 1
    
    def add_effect(self, effect: Effect) -> None:
        """Add an effect to the animal."""
        self.active_effects.append(effect)
    
    def remove_effect(self, effect_name: str) -> None:
        """Remove an effect by name."""
        self.active_effects = [e for e in self.active_effects if e.name != effect_name]
    
    def tick_effects(self) -> None:
        """Tick all active effects and remove expired ones."""
        for effect in self.active_effects:
            effect.tick()
        
        # Remove expired effects
        self.active_effects = [e for e in self.active_effects if not e.is_expired()]
    
    def is_alive(self) -> bool:
        """Check if the animal is still alive."""
        return self.status['Health'] > 0
    
    def get_fitness_score(self) -> float:
        """Calculate the animal's fitness score."""
        if not self.fitness_score_components:
            return 0.0
        
        score = 0.0
        for component, value in self.fitness_score_components.items():
            if component in constants.FITNESS_WEIGHTS:
                weight = constants.FITNESS_WEIGHTS[component]
                if component == 'Resource':
                    # Resources are measured in units, convert to count
                    score += (value / 40) * weight
                else:
                    score += value * weight
        
        return score


@dataclass
class Simulation:
    """Main simulation controller."""
    current_week: int = 0
    event_queue: List[str] = field(default_factory=list)
    world: Optional[World] = None
    population: List[Animal] = field(default_factory=list)
    graveyard: List[Animal] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate simulation data after initialization."""
        if self.current_week < 0:
            raise ValueError(f"Current week must be non-negative, got {self.current_week}")
    
    def add_animal(self, animal: Animal) -> None:
        """Add an animal to the population."""
        self.population.append(animal)
    
    def remove_animal(self, animal: Animal) -> None:
        """Remove an animal from the population and add to graveyard."""
        if animal in self.population:
            self.population.remove(animal)
            self.graveyard.append(animal)
    
    def get_living_animals(self) -> List[Animal]:
        """Get all living animals in the population."""
        return [animal for animal in self.population if animal.is_alive()]
    
    def get_dead_animals(self) -> List[Animal]:
        """Get all dead animals in the population."""
        return [animal for animal in self.population if not animal.is_alive()]
    
    def advance_week(self) -> None:
        """Advance the simulation by one week."""
        self.current_week += 1
    
    def reset(self) -> None:
        """Reset the simulation to initial state."""
        self.current_week = 0
        self.event_queue.clear()
        self.population.clear()
        self.graveyard.clear()


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def create_random_animal(animal_id: str, category: AnimalCategory) -> Animal:
    """Create a random animal with appropriate trait distribution."""
    # Get primary trait for category
    primary_trait = constants.CATEGORY_PRIMARY_TRAITS[category.value]
    
    # Generate traits
    traits = {}
    for trait in constants.TRAIT_NAMES:
        if trait == primary_trait:
            traits[trait] = random.randint(constants.PRIMARY_TRAIT_MIN, constants.PRIMARY_TRAIT_MAX)
        else:
            traits[trait] = random.randint(constants.STANDARD_TRAIT_MIN, constants.STANDARD_TRAIT_MAX)
    
    # Generate initial status
    max_health = constants.BASE_HEALTH + (traits['END'] * constants.HEALTH_PER_ENDURANCE)
    max_energy = constants.BASE_ENERGY + (traits['END'] * constants.ENERGY_PER_ENDURANCE)
    
    status = {
        'Health': float(max_health),
        'Hunger': 100.0,
        'Thirst': 100.0,
        'Energy': float(max_energy),
        'Instinct': 0.0  # 0 for Calm, 1 for Alert
    }
    
    # Get passive ability
    passive_abilities = {
        AnimalCategory.HERBIVORE: "Efficient Grazer",
        AnimalCategory.CARNIVORE: "Ambush Predator",
        AnimalCategory.OMNIVORE: "Iron Stomach"
    }
    
    return Animal(
        animal_id=animal_id,
        category=category,
        traits=traits,
        status=status,
        passive=passive_abilities[category],
        location=(0, 0)  # Will be set during world generation
    )


def create_effect(effect_type: EffectType, duration: int = None) -> Effect:
    """Create an effect with default duration and modifiers."""
    if duration is None:
        duration = constants.DEFAULT_BUFF_DURATION if effect_type.value in constants.BUFF_EFFECTS else constants.DEFAULT_DEBUFF_DURATION
    
    # Define effect modifiers
    modifiers = {
        EffectType.WELL_FED: {'STR': 1, 'END': 1},
        EffectType.HYDRATED: {'AGI': 1},
        EffectType.RESTED: {},  # Handled separately in energy regeneration
        EffectType.ADRENALINE_RUSH: {'STR': 2, 'AGI': 2},
        EffectType.INJURED: {'AGI': -2},
        EffectType.POISONED: {},  # Handled separately in damage calculation
        EffectType.EXHAUSTED: {},  # Handled separately in energy regeneration
        EffectType.SICK: {'STR': -1, 'AGI': -1, 'INT': -1, 'END': -1, 'PER': -1}
    }
    
    return Effect(
        name=effect_type.value,
        duration=duration,
        modifiers=modifiers.get(effect_type, {})
    )


def create_resource(resource_type: ResourceType, quantity: int = None, uses: int = 1) -> Resource:
    """Create a resource with default values."""
    if quantity is None:
        quantity = constants.PLANT_FOOD_GAIN if resource_type == ResourceType.PLANT else constants.PREY_FOOD_GAIN
    
    return Resource(
        resource_type=resource_type,
        quantity=quantity,
        uses_left=uses
    )


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_data_structures():
    """Validate that all data structures work correctly."""
    print("🔍 Validating data structures...")
    
    # Test Effect
    effect = create_effect(EffectType.WELL_FED)
    assert effect.name == "Well-Fed"
    assert effect.duration > 0
    assert not effect.is_expired()
    
    # Test Resource
    resource = create_resource(ResourceType.PLANT)
    assert resource.resource_type == ResourceType.PLANT
    assert resource.quantity > 0
    assert resource.uses_left > 0
    
    # Test Tile
    tile = Tile((0, 0), TerrainType.PLAINS)
    assert tile.coordinates == (0, 0)
    assert tile.terrain_type == TerrainType.PLAINS
    assert not tile.is_occupied()
    assert tile.is_passable()
    
    # Test Animal
    animal = create_random_animal("test_001", AnimalCategory.HERBIVORE)
    assert animal.category == AnimalCategory.HERBIVORE
    assert animal.is_alive()
    assert animal.get_max_health() > 0
    assert animal.get_max_energy() > 0
    
    # Test Simulation
    sim = Simulation()
    assert sim.current_week == 0
    assert len(sim.population) == 0
    
    print("✅ All data structure validation passed!")


if __name__ == "__main__":
    # Run validation when script is executed directly
    validate_data_structures()
