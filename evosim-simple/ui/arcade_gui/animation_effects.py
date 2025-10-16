import arcade
import random
from .theme import Theme

class ParticleEffect:
    def __init__(self, x, y, particle_type, count=5):
        self.x = x
        self.y = y
        self.particle_type = particle_type
        self.particles = []
        self.finished = False

        for _ in range(count):
            self.particles.append({
                'x': x + random.uniform(-10, 10),
                'y': y + random.uniform(-10, 10),
                'vx': random.uniform(-50, 50),
                'vy': random.uniform(-50, 50),
                'life': 1.0,
                'decay': random.uniform(0.5, 1.0)
            })

    def update(self, delta_time):
        for particle in self.particles:
            particle['x'] += particle['vx'] * delta_time
            particle['y'] += particle['vy'] * delta_time
            particle['life'] -= particle['decay'] * delta_time
            particle['vy'] -= 100 * delta_time  # Gravity

        self.particles = [p for p in self.particles if p['life'] > 0]
        if not self.particles:
            self.finished = True

    def draw(self):
        for particle in self.particles:
            alpha = int(particle['life'] * 255)
            color = Theme.ACCENT_ORANGE if self.particle_type == "eating" else Theme.ACCENT_BLUE
            color = (color[0], color[1], color[2], alpha)
            arcade.draw_circle_filled(particle['x'], particle['y'], 3, color)

    def is_finished(self):
        return self.finished

class AnimationManager:
    def __init__(self):
        self.effects = []

    def add_eating_effect(self, x, y):
        self.effects.append(ParticleEffect(x, y, "eating"))

    def add_drinking_effect(self, x, y):
        self.effects.append(ParticleEffect(x, y, "drinking"))

    def add_death_effect(self, x, y):
        # Larger effect for death
        self.effects.append(ParticleEffect(x, y, "death", 10))

    def add_movement_trail(self, from_pos, to_pos):
        # Simple line trail
        pass

    def update_all(self, delta_time):
        for effect in self.effects:
            effect.update(delta_time)
        self.effects = [e for e in self.effects if not e.is_finished()]

    def draw_all(self):
        for effect in self.effects:
            effect.draw()

    def clear_finished(self):
        self.effects = [e for e in self.effects if not e.is_finished()]
