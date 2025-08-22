import pygame
import random

class Particle:
    def __init__(self, x, y, particle_type):
        self.x = x
        self.y = y
        self.particle_type = particle_type
        self.size = random.randint(3, 7)
        self.color = self.get_color()
        self.velocity_x = random.uniform(-5, 5)
        self.velocity_y = random.uniform(-5, 5)
        self.decay = 0.99  # Slows down particle over time

    def get_color(self):
        # Assign colors based on particle type (1-8)
        if self.particle_type == 1:
            return (255, 0, 0)  # Red
        elif self.particle_type == 2:
            return (0, 255, 0)  # Green
        elif self.particle_type == 3:
            return (0, 0, 255)  # Blue
        elif self.particle_type == 4:
            return (255, 255, 0)  # Yellow
        elif self.particle_type == 5:
            return (0, 255, 255)  # Cyan
        elif self.particle_type == 6:
            return (255, 0, 255)  # Magenta
        elif self.particle_type == 7:
            return (128, 0, 128) # Purple
        elif self.particle_type == 8:
            return (255, 165, 0) # Orange
        return (255, 255, 255) # Default white

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_x *= self.decay
        self.velocity_y *= self.decay

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

