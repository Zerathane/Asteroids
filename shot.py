from circleshape import *
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.lifetime = SHOT_LIFETIME_SECONDS
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius)

    def update(self, dt):
        self.position += (self.velocity * dt)
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
        self.wrap(SCREEN_WIDTH, SCREEN_HEIGHT)

    