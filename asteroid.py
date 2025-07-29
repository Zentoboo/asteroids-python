import pygame
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    def draw(self,screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius,2)
    def update(self, dt):
        self.position += self.velocity * dt
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            rand_angle = random.uniform(20,50)
            new1st_velocity = self.velocity.rotate(rand_angle)
            new2nd_velocity = self.velocity.rotate(-rand_angle)
            new1st_radius = self.radius - ASTEROID_MIN_RADIUS
            new2nd_radius = self.radius - ASTEROID_MIN_RADIUS
            
            Asteroid(self.position.x, self.position.y, new1st_radius).velocity = new1st_velocity*1.2
            Asteroid(self.position.x, self.position.y, new2nd_radius).velocity = new2nd_velocity*1.2
            