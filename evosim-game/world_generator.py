"""
EvoSim World Generator

This module handles the generation of the game world, including terrain placement,
resource distribution, and initial world setup.

Reference: Section VI - Map and Objectives, Section VIII - World Generation Parameters
"""

import random
import math
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, field

import constants
from data_structures import (
    World, Tile, Resource, Animal, TerrainType, ResourceType,
    create_resource, create_random_animal, AnimalCategory
)


@dataclass
class GenerationConfig:
    """Configuration for world generation."""
    width: int = constants.GRID_WIDTH
    height: int = constants.GRID_HEIGHT
    terrain_distribution: Dict[str, float] = field(default_factory=lambda: constants.TERRAIN_DISTRIBUTION.copy())
    food_spawn_chance: float = constants.FOOD_SPAWN_CHANCE
    water_spawn_chance: float = constants.WATER_SPAWN_CHANCE
    population_size: int = constants.POPULATION_SIZE
    animal_categories: List[AnimalCategory] = field(default_factory=list)
    mountain_border: bool = True  # Whether to create mountain borders
    
    def __post_init__(self):
        """Validate generation configuration."""
        if not self.animal_categories:  # Empty list
            self.animal_categories = list(AnimalCategory)
        
        # Validate terrain distribution sums to 1.0
        total_distribution = sum(self.terrain_distribution.values())
        if abs(total_distribution - 1.0) > 0.001:
            raise ValueError(f"Terrain distribution must sum to 1.0, got {total_distribution}")
        
        # Validate probabilities
        if not 0 <= self.food_spawn_chance <= 1:
            raise ValueError(f"Food spawn chance must be between 0 and 1, got {self.food_spawn_chance}")
        if not 0 <= self.water_spawn_chance <= 1:
            raise ValueError(f"Water spawn chance must be between 0 and 1, got {self.water_spawn_chance}")


class WorldGenerator:
    """Handles world generation logic."""
    
    def __init__(self, config: GenerationConfig = None):
        """Initialize the world generator with configuration."""
        self.config = config or GenerationConfig()
        self.random = random.Random()
    
    def generate_world(self, seed: Optional[int] = None) -> World:
        """Generate a complete world with terrain and resources."""
        if seed is not None:
            self.random.seed(seed)
        
        # Generate terrain grid
        terrain_grid = self._generate_terrain_grid()
        
        # Create tiles
        tiles = self._create_tiles(terrain_grid)
        
        # Place resources
        self._place_resources(tiles)
        
        # Create world
        world = World(tiles, (self.config.width, self.config.height))
        
        return world
    
    def _generate_terrain_grid(self) -> List[List[TerrainType]]:
        """Generate a 2D grid of terrain types with clustered biomes.

        Strategy:
        - Place mountain borders if enabled.
        - Compute interior target counts from distribution.
        - For each non-plains terrain (Water, Forest, Jungle, Swamp), grow
          several clusters by random BFS until the target count is reached.
        - Fill remaining cells with Plains.
        """
        width, height = self.config.width, self.config.height
        grid: List[List[Optional[TerrainType]]] = [[None for _ in range(width)] for _ in range(height)]

        # 1) Mountains along the border (if enabled)
        interior_cells = 0
        for y in range(height):
            for x in range(width):
                if self.config.mountain_border and self._is_border_tile(x, y):
                    grid[y][x] = TerrainType.MOUNTAINS
                else:
                    interior_cells += 1

        # 2) Determine target counts for interior terrains (excluding Mountains)
        #    We will assign Forest/Jungle/Swamp/Water first; Plains fills the rest.
        distribution = self.config.terrain_distribution
        def count_for(name: str) -> int:
            return max(0, int(round(distribution.get(name, 0.0) * (width * height))))

        target_water   = min(interior_cells, count_for('Water'))
        target_forest  = min(interior_cells, count_for('Forest'))
        target_jungle  = min(interior_cells, count_for('Jungle'))
        target_swamp   = min(interior_cells, count_for('Swamp'))
        # Plains are the remainder implicitly

        # Helper to list free interior cells
        def free_cells() -> List[tuple]:
            cells = []
            for yy in range(height):
                for xx in range(width):
                    if grid[yy][xx] is None:
                        cells.append((xx, yy))
            return cells

        # Helper to get 4-neighbors
        def neighbors4(x: int, y: int) -> List[tuple]:
            out = []
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and grid[ny][nx] is None:
                    out.append((nx, ny))
            return out

        # Generic cluster grower
        def grow_terrain(terrain: TerrainType, remaining: int, seed_attempts: int, continue_prob: float) -> None:
            nonlocal grid
            if remaining <= 0:
                return
            attempts = 0
            while remaining > 0 and attempts < seed_attempts * 100:
                attempts += 1
                cells = free_cells()
                if not cells:
                    break
                sx, sy = self.random.choice(cells)
                # Start a cluster
                queue = [(sx, sy)]
                while queue and remaining > 0:
                    x, y = queue.pop(0)
                    if grid[y][x] is not None:
                        continue
                    grid[y][x] = terrain
                    remaining -= 1
                    # Probabilistically continue to neighbors to keep compact blobs
                    for nx, ny in neighbors4(x, y):
                        if self.random.random() < continue_prob:
                            queue.append((nx, ny))
                # Move to a new seed if we still have remaining tiles
                if remaining <= 0:
                    break

        # Tune per-terrain clustering behavior
        grow_terrain(TerrainType.WATER,   target_water,  seed_attempts=8,  continue_prob=0.7)
        grow_terrain(TerrainType.FOREST,  target_forest, seed_attempts=12, continue_prob=0.6)
        grow_terrain(TerrainType.JUNGLE,  target_jungle, seed_attempts=6,  continue_prob=0.65)
        grow_terrain(TerrainType.SWAMP,   target_swamp,  seed_attempts=6,  continue_prob=0.55)

        # 3) Fill any remaining interior cells with Plains
        for y in range(height):
            for x in range(width):
                if grid[y][x] is None:
                    grid[y][x] = TerrainType.PLAINS

        return grid
    
    def _is_border_tile(self, x: int, y: int) -> bool:
        """Check if a tile is on the border of the world."""
        return (x == 0 or x == self.config.width - 1 or 
                y == 0 or y == self.config.height - 1)
    
    def _create_tiles(self, terrain_grid: List[List[TerrainType]]) -> List[List[Tile]]:
        """Create tile objects from terrain grid."""
        tiles = []
        
        for y in range(self.config.height):
            row = []
            for x in range(self.config.width):
                tile = Tile(
                    coordinates=(x, y),
                    terrain_type=terrain_grid[y][x]
                )
                row.append(tile)
            tiles.append(row)
        
        return tiles
    
    def _place_resources(self, tiles: List[List[Tile]]) -> None:
        """Place resources on appropriate tiles."""
        # Place water resources
        self._place_water_resources(tiles)
        
        # Place food resources
        self._place_food_resources(tiles)
    
    def _place_water_resources(self, tiles: List[List[Tile]]) -> None:
        """Place water resources, clustering them to form lakes and rivers."""
        # Find all water terrain tiles
        water_tiles = []
        for y in range(self.config.height):
            for x in range(self.config.width):
                if tiles[y][x].terrain_type == TerrainType.WATER:
                    water_tiles.append((x, y))
        
        # Place water resources on water tiles
        for x, y in water_tiles:
            if self.random.random() < self.config.water_spawn_chance:
                water_resource = create_resource(ResourceType.WATER, 30, 3)
                tiles[y][x].resource = water_resource
        
        # Also place water resources near water tiles (for drinking)
        for x, y in water_tiles:
            adjacent_tiles = self._get_adjacent_coordinates(x, y)
            for adj_x, adj_y in adjacent_tiles:
                if (0 <= adj_x < self.config.width and 
                    0 <= adj_y < self.config.height and
                    tiles[adj_y][adj_x].terrain_type != TerrainType.WATER and
                    tiles[adj_y][adj_x].resource is None):
                    
                    if self.random.random() < self.config.water_spawn_chance * 0.5:
                        water_resource = create_resource(ResourceType.WATER, 20, 2)
                        tiles[adj_y][adj_x].resource = water_resource
    
    def _place_food_resources(self, tiles: List[List[Tile]]) -> None:
        """Place food resources based on terrain type."""
        for y in range(self.config.height):
            for x in range(self.config.width):
                tile = tiles[y][x]
                
                # Skip if tile already has a resource
                if tile.resource is not None:
                    continue
                
                # Skip water and mountain tiles
                if tile.terrain_type in [TerrainType.WATER, TerrainType.MOUNTAINS]:
                    continue
                
                # Determine spawn chance based on terrain
                spawn_chance = self._get_food_spawn_chance(tile.terrain_type)
                
                if self.random.random() < spawn_chance:
                    resource_type = self._get_food_type_for_terrain(tile.terrain_type)
                    resource = self._create_food_resource(resource_type)
                    tile.resource = resource
    
    def _get_food_spawn_chance(self, terrain: TerrainType) -> float:
        """Get food spawn chance based on terrain type."""
        base_chance = self.config.food_spawn_chance
        
        # Adjust chance based on terrain
        terrain_multipliers = {
            TerrainType.PLAINS: 1.0,
            TerrainType.FOREST: 1.5,  # Higher food density in forests
            TerrainType.JUNGLE: 2.0,  # Even higher in jungles
            TerrainType.SWAMP: 0.8,   # Lower in swamps
        }
        
        multiplier = terrain_multipliers.get(terrain, 1.0)
        return min(1.0, base_chance * multiplier)
    
    def _get_food_type_for_terrain(self, terrain: TerrainType) -> ResourceType:
        """Get appropriate food type for terrain."""
        if terrain == TerrainType.SWAMP:
            # Swamps have more carcasses
            return self.random.choices(
                [ResourceType.PLANT, ResourceType.CARCASS],
                weights=[0.3, 0.7]
            )[0]
        else:
            # Other terrains have mostly plants
            return self.random.choices(
                [ResourceType.PLANT, ResourceType.PREY],
                weights=[0.8, 0.2]
            )[0]
    
    def _create_food_resource(self, resource_type: ResourceType) -> Resource:
        """Create a food resource with appropriate values."""
        if resource_type == ResourceType.PLANT:
            quantity = constants.PLANT_FOOD_GAIN
            uses = self.random.randint(1, 3)
        elif resource_type == ResourceType.PREY:
            quantity = constants.PREY_FOOD_GAIN
            uses = 1
        elif resource_type == ResourceType.CARCASS:
            quantity = self.random.randint(30, 60)
            uses = self.random.randint(1, 2)
        else:
            quantity = constants.PLANT_FOOD_GAIN
            uses = 1
        
        return create_resource(resource_type, quantity, uses)
    
    def _get_adjacent_coordinates(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Get adjacent coordinates (including diagonals)."""
        adjacent = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                adjacent.append((x + dx, y + dy))
        return adjacent
    
    def place_animals(self, world: World, animals: List[Animal]) -> None:
        """Place animals on valid tiles in the world."""
        # Find all valid spawn locations (plains tiles without occupants)
        valid_locations = []
        for y in range(world.dimensions[1]):
            for x in range(world.dimensions[0]):
                tile = world.get_tile(x, y)
                if (tile.terrain_type == TerrainType.PLAINS and 
                    not tile.is_occupied()):
                    valid_locations.append((x, y))
        
        if len(valid_locations) < len(animals):
            raise ValueError(f"Not enough valid spawn locations. Need {len(animals)}, have {len(valid_locations)}")
        
        # Shuffle locations and place animals
        self.random.shuffle(valid_locations)
        
        for i, animal in enumerate(animals):
            x, y = valid_locations[i]
            animal.location = (x, y)
            world.get_tile(x, y).occupant = animal
    
    def generate_initial_population(self, world: World, seed: Optional[int] = None) -> List[Animal]:
        """Generate initial population of animals."""
        if seed is not None:
            self.random.seed(seed)
        
        animals = []
        
        # Distribute animals across categories
        category_counts = self._distribute_animals_by_category()
        
        animal_id = 0
        for category, count in category_counts.items():
            for _ in range(count):
                animal = create_random_animal(f"gen0_{animal_id:03d}", category)
                animals.append(animal)
                animal_id += 1
        
        # Place animals in the world
        self.place_animals(world, animals)
        
        return animals
    
    def _distribute_animals_by_category(self) -> Dict[AnimalCategory, int]:
        """Distribute animals evenly across categories."""
        total_animals = self.config.population_size
        num_categories = len(self.config.animal_categories)
        
        base_count = total_animals // num_categories
        remainder = total_animals % num_categories
        
        distribution = {}
        for i, category in enumerate(self.config.animal_categories):
            count = base_count + (1 if i < remainder else 0)
            distribution[category] = count
        
        return distribution


class WorldValidator:
    """Validates generated worlds for correctness."""
    
    @staticmethod
    def validate_world(world: World) -> Dict[str, any]:
        """Validate a generated world and return statistics."""
        stats = {
            'total_tiles': world.dimensions[0] * world.dimensions[1],
            'terrain_counts': {},
            'resource_counts': {},
            'occupied_tiles': 0,
            'valid_spawn_locations': 0,
            'errors': []
        }
        
        # Count terrain types
        for y in range(world.dimensions[1]):
            for x in range(world.dimensions[0]):
                tile = world.get_tile(x, y)
                terrain = tile.terrain_type.value
                stats['terrain_counts'][terrain] = stats['terrain_counts'].get(terrain, 0) + 1
                
                # Count resources
                if tile.resource is not None:
                    resource_type = tile.resource.resource_type.value
                    stats['resource_counts'][resource_type] = stats['resource_counts'].get(resource_type, 0) + 1
                
                # Count occupied tiles
                if tile.is_occupied():
                    stats['occupied_tiles'] += 1
                
                # Count valid spawn locations
                if (tile.terrain_type == TerrainType.PLAINS and 
                    not tile.is_occupied()):
                    stats['valid_spawn_locations'] += 1
        
        # Validate terrain distribution
        total_tiles = stats['total_tiles']
        for terrain, count in stats['terrain_counts'].items():
            actual_percentage = count / total_tiles
            expected_percentage = constants.TERRAIN_DISTRIBUTION.get(terrain, 0)
            
            # For mountains, check if they're mostly on borders (if mountain_border is enabled)
            if terrain == 'Mountains':
                # Count border tiles
                border_tiles = 2 * (world.dimensions[0] + world.dimensions[1]) - 4
                if count > border_tiles * 0.8:  # At least 80% of mountains should be on borders
                    # This is expected with mountain borders
                    continue
            
            # Allow 10% tolerance for other terrains
            if abs(actual_percentage - expected_percentage) > 0.1:
                stats['errors'].append(
                    f"Terrain {terrain}: expected {expected_percentage:.1%}, got {actual_percentage:.1%}"
                )
        
        return stats
    
    @staticmethod
    def print_world_stats(stats: Dict[str, any]) -> None:
        """Print world statistics in a readable format."""
        print("🌍 World Generation Statistics")
        print("=" * 40)
        print(f"Total tiles: {stats['total_tiles']}")
        print(f"Occupied tiles: {stats['occupied_tiles']}")
        print(f"Valid spawn locations: {stats['valid_spawn_locations']}")
        
        print("\nTerrain distribution:")
        for terrain, count in stats['terrain_counts'].items():
            percentage = (count / stats['total_tiles']) * 100
            print(f"  {terrain}: {count} tiles ({percentage:.1f}%)")
        
        print("\nResource distribution:")
        for resource, count in stats['resource_counts'].items():
            print(f"  {resource}: {count} tiles")
        
        if stats['errors']:
            print("\n⚠️  Validation errors:")
            for error in stats['errors']:
                print(f"  - {error}")
        else:
            print("\n✅ World validation passed!")
    
    @staticmethod
    def visualize_world(world: World, show_resources: bool = True, show_animals: bool = True) -> None:
        """Print a visual representation of the world."""
        print("🗺️  World Visualization")
        print("=" * (world.dimensions[0] * 2 + 3))
        
        # Terrain symbols
        terrain_symbols = {
            TerrainType.PLAINS: '·',
            TerrainType.FOREST: '🌲',
            TerrainType.JUNGLE: '🌴',
            TerrainType.WATER: '💧',
            TerrainType.SWAMP: '🌿',
            TerrainType.MOUNTAINS: '⛰️'
        }
        
        # Resource symbols
        resource_symbols = {
            ResourceType.PLANT: '🌱',
            ResourceType.PREY: '🐭',
            ResourceType.WATER: '💧',
            ResourceType.CARCASS: '🦴'
        }
        
        # Animal symbols
        animal_symbols = {
            AnimalCategory.HERBIVORE: '🦌',
            AnimalCategory.CARNIVORE: '🐺',
            AnimalCategory.OMNIVORE: '🐻'
        }
        
        for y in range(world.dimensions[1]):
            row = ""
            for x in range(world.dimensions[0]):
                tile = world.get_tile(x, y)
                symbol = terrain_symbols.get(tile.terrain_type, '?')
                
                # Overlay resource or animal if present
                if show_animals and tile.is_occupied():
                    symbol = animal_symbols.get(tile.occupant.category, '🐾')
                elif show_resources and tile.resource is not None:
                    symbol = resource_symbols.get(tile.resource.resource_type, '📦')
                
                row += symbol + " "
            print(f"{y:2d}| {row}")
        
        print("   " + "".join([f"{x:2d}" for x in range(world.dimensions[0])]))
        print()


def generate_world_with_population(
    config: GenerationConfig = None,
    world_seed: Optional[int] = None,
    population_seed: Optional[int] = None
) -> Tuple[World, List[Animal]]:
    """Generate a complete world with initial population."""
    generator = WorldGenerator(config)
    
    # Generate world
    world = generator.generate_world(world_seed)
    
    # Generate population
    population = generator.generate_initial_population(world, population_seed)
    
    return world, population


def create_test_world(size: int = 10) -> World:
    """Create a small test world for debugging."""
    config = GenerationConfig(
        width=size,
        height=size,
        population_size=5
    )
    
    generator = WorldGenerator(config)
    return generator.generate_world(seed=42)


if __name__ == "__main__":
    # Test world generation
    print("🧪 Testing world generation...")
    
    # Create a test world
    world = create_test_world(10)
    
    # Validate the world
    stats = WorldValidator.validate_world(world)
    WorldValidator.print_world_stats(stats)
    
    print("\n🎉 World generation test completed!")
