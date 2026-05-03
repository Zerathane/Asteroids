from constants import *
from circleshape import *
import random
from logger import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, width=LINE_WIDTH)

    def update(self, dt):
        self.position += (self.velocity * dt)

    def split(self):
        if self.radius <= ASTEROID_MIN_RADIUS:
            self.kill()
            return
        else:
            log_event("asteroid_split")
            angle = random.uniform(20, 50)
            self.velocity = self.velocity.rotate(angle)
            new_velocity = self.velocity.rotate(-2 * angle) # should rotate opposite direction, check this
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid1.velocity = (self.velocity * 1.2)
            asteroid2.velocity = (new_velocity * 1.2)
            self.kill()