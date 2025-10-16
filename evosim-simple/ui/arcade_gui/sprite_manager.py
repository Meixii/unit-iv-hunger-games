import arcade
import random
import os

class SpriteManager:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.animal_sprites = {}
        self.food_sprite = None
        self.water_sprite = None
        self.grass_texture = None
        self.asset_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "assets")
        self.load_or_create_sprites()

    def load_or_create_sprites(self):
        # Create grass tile texture (darker, more natural green)
        grass_color = (50, 168, 82)  # Medium forest green
        self.grass_texture = arcade.make_soft_square_texture(self.cell_size, grass_color, outer_alpha=255)

        # Try to load asset images, fallback to colored shapes
        try:
            # Find closest matching asset size
            asset_size = min([16, 20, 24, 28, 32], key=lambda x: abs(x - self.cell_size))
            asset_file = os.path.join(self.asset_path, f"{asset_size}x{asset_size}.png")
            
            if os.path.exists(asset_file):
                # Load the asset as texture for animals
                self.animal_texture = arcade.load_texture(asset_file)
                print(f"[SPRITES] Loaded asset: {asset_file}")
            else:
                self.animal_texture = None
        except Exception as e:
            print(f"[SPRITES] Could not load assets: {e}")
            self.animal_texture = None

        # Create food sprite (orange circle with glow)
        self.food_sprite = arcade.SpriteSolidColor(self.cell_size // 2, self.cell_size // 2, (255, 184, 108))

        # Create water sprite (cyan circle with glow)
        self.water_sprite = arcade.SpriteSolidColor(self.cell_size // 2, self.cell_size // 2, (139, 233, 253))

    def create_animal_sprite(self, animal_id):
        # Use loaded texture if available, otherwise create colored circle
        if self.animal_texture:
            sprite = arcade.Sprite()
            sprite.texture = self.animal_texture
            sprite.width = self.cell_size - 4
            sprite.height = self.cell_size - 4
            # Add color tint variation
            colors = [(255, 85, 85), (189, 147, 249), (241, 250, 140), (139, 233, 253), (255, 121, 198)]
            sprite.color = colors[animal_id % len(colors)]
        else:
            # Fallback to colored circles with modern palette
            colors = [(255, 85, 85), (189, 147, 249), (241, 250, 140), (139, 233, 253), (255, 121, 198)]
            color = colors[animal_id % len(colors)]
            sprite = arcade.SpriteSolidColor(self.cell_size - 4, self.cell_size - 4, color)
        self.animal_sprites[animal_id] = sprite
        return sprite

    def get_animal_sprite(self, animal):
        animal_id = id(animal)  # Use object id as unique identifier
        if animal_id not in self.animal_sprites:
            self.create_animal_sprite(animal_id)
        return self.animal_sprites[animal_id]

    def get_resource_sprite(self, resource_type):
        if resource_type == "food":
            return self.food_sprite
        elif resource_type == "water":
            return self.water_sprite
        return None

    def get_grass_texture(self):
        return self.grass_texture

    def scale_sprites(self, new_cell_size):
        self.cell_size = new_cell_size
        self.load_or_create_sprites()
        # Rescale animal sprites
        for sprite in self.animal_sprites.values():
            sprite.width = new_cell_size - 4
            sprite.height = new_cell_size - 4
