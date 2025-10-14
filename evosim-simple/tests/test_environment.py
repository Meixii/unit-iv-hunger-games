"""
Test module for the Environment system.
"""

import pytest
import numpy as np
from src.environment import GridWorld
from src.events import EventManager, EnvironmentalEvent
from src.animal import Animal
from src.neural_network import NeuralNetwork


class TestGridWorld:
    """Test cases for GridWorld class."""
    
    def test_gridworld_initialization(self):
        """Test grid world initialization."""
        world = GridWorld(20, 20)
        
        assert world.width == 20
        assert world.height == 20
        assert world.grid.shape == (20, 20)
        assert len(world.animals) == 0
        assert len(world.food_positions) == 0
        assert len(world.water_positions) == 0
        assert world.food_count == 0
        assert world.water_count == 0
    
    def test_place_resources(self):
        """Test resource placement."""
        world = GridWorld(10, 10)
        world.place_resources(food_density=0.1, water_density=0.1)
        
        # Check that resources were placed
        assert world.food_count > 0
        assert world.water_count > 0
        assert len(world.food_positions) == world.food_count
        assert len(world.water_positions) == world.water_count
        
        # Check grid state
        food_cells = np.sum(world.grid == 1)
        water_cells = np.sum(world.grid == 2)
        assert food_cells == world.food_count
        assert water_cells == world.water_count
    
    def test_add_animal(self):
        """Test adding animals to the grid."""
        world = GridWorld(10, 10)
        animal = Animal(5, 5)
        
        # Test successful placement
        success = world.add_animal(animal, 5, 5)
        assert success == True
        assert animal in world.animals
        assert world.animal_positions[(5, 5)] == animal
        assert world.grid[5, 5] == 3
        
        # Test invalid position
        animal2 = Animal(0, 0)
        success = world.add_animal(animal2, 15, 15)  # Out of bounds
        assert success == False
        
        # Test occupied position
        animal3 = Animal(0, 0)
        success = world.add_animal(animal3, 5, 5)  # Already occupied
        assert success == False
    
    def test_remove_animal(self):
        """Test removing animals from the grid."""
        world = GridWorld(10, 10)
        animal = Animal(5, 5)
        world.add_animal(animal, 5, 5)
        
        world.remove_animal(animal)
        
        assert animal not in world.animals
        assert (5, 5) not in world.animal_positions
        assert world.grid[5, 5] == 0
    
    def test_move_animal(self):
        """Test moving animals."""
        world = GridWorld(10, 10)
        animal = Animal(5, 5)
        world.add_animal(animal, 5, 5)
        
        # Test successful move
        success = world.move_animal(animal, 6, 6)
        assert success == True
        assert animal.get_position() == (6, 6)
        assert world.grid[5, 5] == 0
        assert world.grid[6, 6] == 3
        assert (6, 6) in world.animal_positions
        assert (5, 5) not in world.animal_positions
        
        # Test invalid move (out of bounds)
        success = world.move_animal(animal, 15, 15)
        assert success == False
        
        # Test move to occupied position
        animal2 = Animal(0, 0)
        world.add_animal(animal2, 7, 7)
        success = world.move_animal(animal, 7, 7)
        assert success == False
    
    def test_is_valid_position(self):
        """Test position validation."""
        world = GridWorld(10, 10)
        
        # Valid positions
        assert world.is_valid_position(0, 0) == True
        assert world.is_valid_position(9, 9) == True
        assert world.is_valid_position(5, 5) == True
        
        # Invalid positions
        assert world.is_valid_position(-1, 0) == False
        assert world.is_valid_position(0, -1) == False
        assert world.is_valid_position(10, 0) == False
        assert world.is_valid_position(0, 10) == False
        assert world.is_valid_position(15, 15) == False
    
    def test_get_cell_content(self):
        """Test getting cell content."""
        world = GridWorld(10, 10)
        world.place_resources(food_density=0.1, water_density=0.1)
        
        # Test empty cell (find an actual empty cell)
        empty_positions = world.get_empty_positions()
        if empty_positions:
            empty_pos = empty_positions[0]
            assert world.get_cell_content(empty_pos[0], empty_pos[1]) == 'empty'
        
        # Test food cell
        food_pos = list(world.food_positions)[0]
        assert world.get_cell_content(food_pos[0], food_pos[1]) == 'food'
        
        # Test water cell
        water_pos = list(world.water_positions)[0]
        assert world.get_cell_content(water_pos[0], water_pos[1]) == 'water'
        
        # Test animal cell
        animal = Animal(5, 5)
        world.add_animal(animal, 5, 5)
        assert world.get_cell_content(5, 5) == 'animal'
        
        # Test invalid position
        assert world.get_cell_content(15, 15) == 'invalid'
    
    def test_consume_resource(self):
        """Test resource consumption."""
        world = GridWorld(10, 10)
        world.place_resources(food_density=0.1, water_density=0.1)
        
        # Test consuming food
        food_pos = list(world.food_positions)[0]
        initial_food_count = world.food_count
        success = world.consume_resource(food_pos[0], food_pos[1], 'food')
        
        assert success == True
        assert world.food_count == initial_food_count - 1
        assert food_pos not in world.food_positions
        assert world.grid[food_pos[1], food_pos[0]] == 0
        
        # Test consuming water
        water_pos = list(world.water_positions)[0]
        initial_water_count = world.water_count
        success = world.consume_resource(water_pos[0], water_pos[1], 'water')
        
        assert success == True
        assert world.water_count == initial_water_count - 1
        assert water_pos not in world.water_positions
        assert world.grid[water_pos[1], water_pos[0]] == 0
        
        # Test consuming non-existent resource (find an empty cell)
        empty_positions = world.get_empty_positions()
        if empty_positions:
            empty_pos = empty_positions[0]
            success = world.consume_resource(empty_pos[0], empty_pos[1], 'food')
            assert success == False
    
    def test_get_available_actions(self):
        """Test getting available actions."""
        world = GridWorld(10, 10)
        world.place_resources(food_density=0.1, water_density=0.1)
        
        # Test empty cell
        actions = world.get_available_actions(0, 0)
        assert 'move' in actions
        assert 'rest' in actions
        assert 'eat' not in actions
        assert 'drink' not in actions
        
        # Test food cell
        food_pos = list(world.food_positions)[0]
        actions = world.get_available_actions(food_pos[0], food_pos[1])
        assert 'eat' in actions
        assert 'move' in actions
        assert 'rest' in actions
        
        # Test water cell
        water_pos = list(world.water_positions)[0]
        actions = world.get_available_actions(water_pos[0], water_pos[1])
        assert 'drink' in actions
        assert 'move' in actions
        assert 'rest' in actions
    
    def test_get_neighboring_positions(self):
        """Test getting neighboring positions."""
        world = GridWorld(10, 10)
        
        # Test center position
        neighbors = world.get_neighboring_positions(5, 5)
        assert len(neighbors) == 8
        assert (4, 4) in neighbors
        assert (4, 5) in neighbors
        assert (4, 6) in neighbors
        assert (5, 4) in neighbors
        assert (5, 6) in neighbors
        assert (6, 4) in neighbors
        assert (6, 5) in neighbors
        assert (6, 6) in neighbors
        
        # Test corner position
        neighbors = world.get_neighboring_positions(0, 0)
        assert len(neighbors) == 3
        assert (0, 1) in neighbors
        assert (1, 0) in neighbors
        assert (1, 1) in neighbors
    
    def test_get_empty_positions(self):
        """Test getting empty positions."""
        world = GridWorld(5, 5)
        world.place_resources(food_density=0.2, water_density=0.2)
        
        empty_positions = world.get_empty_positions()
        assert len(empty_positions) > 0
        
        # All empty positions should be empty
        for pos in empty_positions:
            assert world.get_cell_content(pos[0], pos[1]) == 'empty'
    
    def test_get_resource_positions(self):
        """Test getting resource positions."""
        world = GridWorld(10, 10)
        world.place_resources(food_density=0.1, water_density=0.1)
        
        food_positions = world.get_resource_positions('food')
        water_positions = world.get_resource_positions('water')
        
        assert len(food_positions) == world.food_count
        assert len(water_positions) == world.water_count
        assert set(food_positions) == world.food_positions
        assert set(water_positions) == world.water_positions
    
    def test_get_animal_at_position(self):
        """Test getting animal at position."""
        world = GridWorld(10, 10)
        animal = Animal(5, 5)
        world.add_animal(animal, 5, 5)
        
        # Test getting animal
        retrieved_animal = world.get_animal_at_position(5, 5)
        assert retrieved_animal == animal
        
        # Test empty position
        retrieved_animal = world.get_animal_at_position(0, 0)
        assert retrieved_animal is None
    
    def test_get_alive_animals(self):
        """Test getting alive animals."""
        world = GridWorld(10, 10)
        animal1 = Animal(5, 5)
        animal2 = Animal(6, 6)
        animal2.alive = False  # Make it dead
        
        world.add_animal(animal1, 5, 5)
        world.add_animal(animal2, 6, 6)
        
        alive_animals = world.get_alive_animals()
        assert len(alive_animals) == 1
        assert animal1 in alive_animals
        assert animal2 not in alive_animals
    
    def test_update_animals(self):
        """Test updating animals."""
        world = GridWorld(10, 10)
        animal = Animal(5, 5)
        world.add_animal(animal, 5, 5)
        
        # Make animal die
        animal.hunger = 0
        animal.thirst = 0
        
        world.update_animals()
        
        # Dead animal should be removed
        assert animal not in world.animals
        assert (5, 5) not in world.animal_positions
        assert world.grid[5, 5] == 0
    
    def test_get_statistics(self):
        """Test getting environment statistics."""
        world = GridWorld(10, 10)
        world.place_resources(food_density=0.1, water_density=0.1)
        
        animal = Animal(5, 5)
        world.add_animal(animal, 5, 5)
        
        stats = world.get_statistics()
        
        assert stats['grid_size'] == (10, 10)
        assert stats['total_animals'] == 1
        assert stats['alive_animals'] == 1
        assert stats['dead_animals'] == 0
        assert stats['food_count'] == world.food_count
        assert stats['water_count'] == world.water_count
        assert 'empty_cells' in stats
        assert 'active_events' in stats
    
    def test_reset(self):
        """Test resetting the environment."""
        world = GridWorld(10, 10)
        world.place_resources(food_density=0.1, water_density=0.1)
        animal = Animal(5, 5)
        world.add_animal(animal, 5, 5)
        
        world.reset()
        
        assert len(world.animals) == 0
        assert len(world.food_positions) == 0
        assert len(world.water_positions) == 0
        assert world.food_count == 0
        assert world.water_count == 0
        assert np.all(world.grid == 0)


class TestEventManager:
    """Test cases for EventManager class."""
    
    def test_event_manager_initialization(self):
        """Test event manager initialization."""
        manager = EventManager()
        
        assert len(manager.active_events) == 0
        assert len(manager.event_history) == 0
        assert manager.drought_probability == 0.2
        assert manager.storm_probability == 0.1
        assert manager.famine_probability == 0.15
        assert manager.bonus_probability == 0.05
    
    def test_environmental_event(self):
        """Test environmental event creation."""
        event = EnvironmentalEvent('test', 100, {'effect': 0.5})
        
        assert event.name == 'test'
        assert event.duration == 100
        assert event.remaining_duration == 100
        assert event.active == True
        assert event.effects == {'effect': 0.5}
    
    def test_event_update(self):
        """Test event update."""
        event = EnvironmentalEvent('test', 3, {'effect': 0.5})
        
        # Update once
        active = event.update()
        assert active == True
        assert event.remaining_duration == 2
        
        # Update until expired
        active = event.update()
        assert active == True
        assert event.remaining_duration == 1
        
        active = event.update()
        assert active == False
        assert event.remaining_duration == 0
    
    def test_force_event(self):
        """Test forcing events."""
        manager = EventManager()
        
        # Force drought
        success = manager.force_event('drought')
        assert success == True
        assert 'drought' in manager.active_events
        
        # Force storm
        success = manager.force_event('storm')
        assert success == True
        assert 'storm' in manager.active_events
        
        # Force invalid event
        success = manager.force_event('invalid')
        assert success == False
    
    def test_get_event_effects(self):
        """Test getting event effects."""
        manager = EventManager()
        
        # No events active
        effects = manager.get_event_effects()
        assert len(effects) == 0
        
        # Force drought
        manager.force_event('drought')
        effects = manager.get_event_effects()
        assert 'water_availability' in effects
        assert effects['water_availability'] == 0.3
    
    def test_is_event_active(self):
        """Test checking if event is active."""
        manager = EventManager()
        
        assert manager.is_event_active('drought') == False
        
        manager.force_event('drought')
        assert manager.is_event_active('drought') == True
    
    def test_get_event_progress(self):
        """Test getting event progress."""
        manager = EventManager()
        
        # No event
        progress = manager.get_event_progress('drought')
        assert progress == 0.0
        
        # Active event
        manager.force_event('drought')
        progress = manager.get_event_progress('drought')
        assert 0.0 <= progress <= 1.0
    
    def test_set_event_probabilities(self):
        """Test setting event probabilities."""
        manager = EventManager()
        
        manager.set_event_probabilities(drought=0.5, storm=0.3)
        
        assert manager.drought_probability == 0.5
        assert manager.storm_probability == 0.3
        assert manager.famine_probability == 0.15  # Unchanged
        assert manager.bonus_probability == 0.05  # Unchanged
    
    def test_get_statistics(self):
        """Test getting event manager statistics."""
        manager = EventManager()
        manager.force_event('drought')
        
        stats = manager.get_statistics()
        
        assert stats['active_events'] == 1
        assert 'drought' in stats['event_names']
        assert stats['total_events_triggered'] >= 1
        assert 'drought_probability' in stats
        assert 'cooldowns' in stats
    
    def test_reset(self):
        """Test resetting event manager."""
        manager = EventManager()
        manager.force_event('drought')
        manager.force_event('storm')
        
        manager.reset()
        
        assert len(manager.active_events) == 0
        assert len(manager.event_history) == 0
        for cooldown in manager.event_cooldowns.values():
            assert cooldown == 0
