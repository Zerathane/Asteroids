import math
from constants import *
from circleshape import *
import random
from explosion import *
from logger import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.points = []
        for i in range(10):
            angle = (i / 10) * 360
            distance = random.uniform(self.radius * 0.35, self.radius * 1.2)
            x = distance * math.cos(math.radians(angle))
            y = distance * math.sin(math.radians(angle))
            self.points.append(pygame.Vector2(x, y))
            

    def draw(self, screen):
        offset_points = []
        for point in self.points:
            offset_points.append(self.position + point)
        pygame.draw.polygon(screen, "white", offset_points, width=LINE_WIDTH)

    def update(self, dt):
        self.position += (self.velocity * dt)

    def split(self):
        if self.radius <= ASTEROID_MIN_RADIUS:
            Explosion(self.position.x, self.position.y, self.radius)
            self.kill()
            return
        else:
            log_event("asteroid_split")
            angle = random.uniform(20, 50)
            self.velocity = self.velocity.rotate(angle)
            new_velocity = self.velocity.rotate(-2 * angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid1.velocity = (self.velocity * 1.5)
            asteroid2.velocity = (new_velocity * 1.5)
            Explosion(self.position.x, self.position.y, self.radius)
            self.kill()
            