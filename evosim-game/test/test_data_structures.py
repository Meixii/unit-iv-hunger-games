#!/usr/bin/env python3
"""
Test script for data_structures.py

This script validates that all data structures work correctly and can be instantiated.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import data_structures
from data_structures import *
import constants

def test_effect_creation():
    """Test Effect class creation and methods."""
    print("Testing Effect class...")
    
    # Test basic effect creation
    effect = Effect("Test Effect", 5, {"STR": 2, "AGI": 1})
    assert effect.name == "Test Effect"
    assert effect.duration == 5
    assert effect.modifiers == {"STR": 2, "AGI": 1}
    assert not effect.is_expired()
    
    # Test effect ticking
    effect.tick()
    assert effect.duration == 4
    assert not effect.is_expired()
    
    # Test effect expiration
    effect.duration = 1
    effect.tick()
    assert effect.is_expired()
    
    # Test effect creation function
    well_fed = create_effect(EffectType.WELL_FED)
    assert well_fed.name == "Well-Fed"
    assert well_fed.duration == constants.DEFAULT_BUFF_DURATION
    assert "STR" in well_fed.modifiers
    
    print("✅ Effect tests passed!")

def test_resource_creation():
    """Test Resource class creation and methods."""
    print("Testing Resource class...")
    
    # Test basic resource creation
    resource = Resource(ResourceType.PLANT, 40, 2)
    assert resource.resource_type == ResourceType.PLANT
    assert resource.quantity == 40
    assert resource.uses_left == 2
    assert not resource.is_depleted()
    
    # Test resource consumption
    gained = resource.consume()
    assert gained == 40
    assert resource.uses_left == 1
    assert not resource.is_depleted()
    
    # Test resource depletion
    gained = resource.consume()
    assert gained == 40
    assert resource.uses_left == 0
    assert resource.is_depleted()
    
    # Test consumption when depleted
    gained = resource.consume()
    assert gained == 0
    
    # Test resource creation function
    plant_resource = create_resource(ResourceType.PLANT)
    assert plant_resource.resource_type == ResourceType.PLANT
    assert plant_resource.quantity == constants.PLANT_FOOD_GAIN
    
    print("✅ Resource tests passed!")

def test_tile_creation():
    """Test Tile class creation and methods."""
    print("Testing Tile class...")
    
    # Test basic tile creation
    tile = Tile((5, 10), TerrainType.FOREST)
    assert tile.coordinates == (5, 10)
    assert tile.terrain_type == TerrainType.FOREST
    assert tile.resource is None
    assert tile.occupant is None
    assert not tile.is_occupied()
    assert tile.is_passable()
    
    # Test tile with resource
    resource = create_resource(ResourceType.PLANT)
    tile_with_resource = Tile((0, 0), TerrainType.PLAINS, resource)
    assert tile_with_resource.resource is not None
    assert tile_with_resource.is_passable()
    
    # Test tile with occupant
    animal = create_random_animal("test_001", AnimalCategory.HERBIVORE)
    tile_with_occupant = Tile((1, 1), TerrainType.PLAINS, occupant=animal)
    assert tile_with_occupant.occupant is not None
    assert tile_with_occupant.is_occupied()
    assert not tile_with_occupant.is_passable()
    
    # Test movement costs
    plains_tile = Tile((0, 0), TerrainType.PLAINS)
    forest_tile = Tile((0, 0), TerrainType.FOREST)
    assert plains_tile.get_movement_cost() == 1.0
    assert forest_tile.get_movement_cost() == 1.5
    
    print("✅ Tile tests passed!")

def test_world_creation():
    """Test World class creation and methods."""
    print("Testing World class...")
    
    # Create a small test world
    grid = []
    for y in range(3):
        row = []
        for x in range(3):
            tile = Tile((x, y), TerrainType.PLAINS)
            row.append(tile)
        grid.append(row)
    
    world = World(grid, (3, 3))
    assert world.dimensions == (3, 3)
    assert len(world.grid) == 3
    assert len(world.grid[0]) == 3
    
    # Test coordinate validation
    assert world.is_valid_coordinate(0, 0)
    assert world.is_valid_coordinate(2, 2)
    assert not world.is_valid_coordinate(3, 0)
    assert not world.is_valid_coordinate(0, 3)
    assert not world.is_valid_coordinate(-1, 0)
    
    # Test tile retrieval
    tile = world.get_tile(1, 1)
    assert tile is not None
    assert tile.coordinates == (1, 1)
    
    # Test invalid tile retrieval
    invalid_tile = world.get_tile(5, 5)
    assert invalid_tile is None
    
    # Test adjacent tiles
    adjacent = world.get_adjacent_tiles(1, 1)
    assert len(adjacent) == 4  # Should have 4 adjacent tiles
    
    print("✅ World tests passed!")

def test_animal_creation():
    """Test Animal class creation and methods."""
    print("Testing Animal class...")
    
    # Test random animal creation
    animal = create_random_animal("test_001", AnimalCategory.HERBIVORE)
    assert animal.animal_id == "test_001"
    assert animal.category == AnimalCategory.HERBIVORE
    assert animal.passive == "Efficient Grazer"
    assert animal.is_alive()
    
    # Test trait validation
    for trait in constants.TRAIT_NAMES:
        assert trait in animal.traits
        assert isinstance(animal.traits[trait], int)
        assert animal.traits[trait] >= 1
    
    # Test status validation
    for status in constants.STATUS_NAMES:
        assert status in animal.status
        assert isinstance(animal.status[status], (int, float))
    
    # Test health and energy calculations
    max_health = animal.get_max_health()
    max_energy = animal.get_max_energy()
    assert max_health > 0
    assert max_energy > 0
    assert max_health == constants.BASE_HEALTH + (animal.traits['END'] * constants.HEALTH_PER_ENDURANCE)
    assert max_energy == constants.BASE_ENERGY + (animal.traits['END'] * constants.ENERGY_PER_ENDURANCE)
    
    # Test effective trait calculation
    base_str = animal.traits['STR']
    effective_str = animal.get_effective_trait('STR')
    assert effective_str == base_str  # No effects yet
    
    # Test effect management
    effect = create_effect(EffectType.WELL_FED)
    animal.add_effect(effect)
    assert len(animal.active_effects) == 1
    
    effective_str_with_effect = animal.get_effective_trait('STR')
    assert effective_str_with_effect > base_str
    
    # Test effect ticking
    animal.tick_effects()
    assert len(animal.active_effects) == 1  # Effect still active
    
    # Test animal death
    animal.status['Health'] = 0
    assert not animal.is_alive()
    
    print("✅ Animal tests passed!")

def test_simulation_creation():
    """Test Simulation class creation and methods."""
    print("Testing Simulation class...")
    
    # Test basic simulation creation
    sim = Simulation()
    assert sim.current_week == 0
    assert len(sim.population) == 0
    assert len(sim.graveyard) == 0
    assert len(sim.event_queue) == 0
    
    # Test animal management
    animal1 = create_random_animal("test_001", AnimalCategory.HERBIVORE)
    animal2 = create_random_animal("test_002", AnimalCategory.CARNIVORE)
    
    sim.add_animal(animal1)
    sim.add_animal(animal2)
    assert len(sim.population) == 2
    
    # Test living/dead animal queries
    living = sim.get_living_animals()
    dead = sim.get_dead_animals()
    assert len(living) == 2
    assert len(dead) == 0
    
    # Test animal removal
    sim.remove_animal(animal1)
    assert len(sim.population) == 1
    assert len(sim.graveyard) == 1
    
    # Test week advancement
    sim.advance_week()
    assert sim.current_week == 1
    
    # Test simulation reset
    sim.reset()
    assert sim.current_week == 0
    assert len(sim.population) == 0
    assert len(sim.graveyard) == 0
    
    print("✅ Simulation tests passed!")

def test_utility_functions():
    """Test utility functions."""
    print("Testing utility functions...")
    
    # Test create_random_animal
    herbivore = create_random_animal("herb_001", AnimalCategory.HERBIVORE)
    carnivore = create_random_animal("carn_001", AnimalCategory.CARNIVORE)
    omnivore = create_random_animal("omni_001", AnimalCategory.OMNIVORE)
    
    assert herbivore.category == AnimalCategory.HERBIVORE
    assert carnivore.category == AnimalCategory.CARNIVORE
    assert omnivore.category == AnimalCategory.OMNIVORE
    
    # Test primary trait distribution
    assert herbivore.traits['AGI'] >= constants.PRIMARY_TRAIT_MIN  # Herbivore primary trait
    assert carnivore.traits['STR'] >= constants.PRIMARY_TRAIT_MIN  # Carnivore primary trait
    assert omnivore.traits['END'] >= constants.PRIMARY_TRAIT_MIN   # Omnivore primary trait
    
    # Test create_effect
    effect = create_effect(EffectType.POISONED)
    assert effect.name == "Poisoned"
    assert effect.duration == constants.DEFAULT_DEBUFF_DURATION
    
    # Test create_resource
    resource = create_resource(ResourceType.WATER)
    assert resource.resource_type == ResourceType.WATER
    assert resource.quantity > 0
    
    print("✅ Utility function tests passed!")

def test_data_integrity():
    """Test data integrity and edge cases."""
    print("Testing data integrity...")
    
    # Test invalid coordinates
    try:
        Tile((1, 2, 3), TerrainType.PLAINS)  # Too many coordinates
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    try:
        Tile((-1, 0), TerrainType.PLAINS)  # Negative coordinates
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    # Test invalid resource quantities
    try:
        Resource(ResourceType.PLANT, 0, 1)  # Zero quantity
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    try:
        Resource(ResourceType.PLANT, 10, 0)  # Zero uses
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    # Test invalid effect duration
    try:
        Effect("Test", 0)  # Zero duration
        assert False, "Should have raised ValueError"
    except ValueError:
        pass
    
    print("✅ Data integrity tests passed!")

def main():
    """Run all tests."""
    print("🧪 Running data_structures.py tests...\n")
    
    try:
        test_effect_creation()
        test_resource_creation()
        test_tile_creation()
        test_world_creation()
        test_animal_creation()
        test_simulation_creation()
        test_utility_functions()
        test_data_integrity()
        
        print("\n🎉 All tests passed! Data structures are working correctly.")
        
    except Exception as e:
        print(f"\n❌ Tests failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
