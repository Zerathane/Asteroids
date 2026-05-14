from constants import *
from circleshape import *
from shot import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0

    def draw(self, screen):
        keys = pygame.key.get_pressed()
        draw_ship(screen, self.position, self.radius, self.rotation, "white", thrusting=keys[pygame.K_w])
        
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
            
        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_SPACE]:
            self.shoot()

        self.shot_cooldown -= dt
        self.position += self.velocity * dt
        self.velocity *= PLAYER_DRAG
        self.wrap(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed = rotated_vector * PLAYER_ACCELERATION * dt
        self.velocity += rotated_with_speed
        self.velocity = self.velocity.clamp_magnitude(PLAYER_MAX_SPEED)
        
    def shoot(self):
        if self.shot_cooldown > 0:
            return
        else:
            self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED + self.velocity

    def reset(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.shot_cooldown = 0

def draw_ship(screen, position, radius, rotation, colour, thrusting=False):
    forward = pygame.Vector2(0, 1).rotate(rotation)
    right = pygame.Vector2(0, 1).rotate(rotation + 90) * radius / 1.5
    a = position + forward * radius
    b = position - forward * radius - right
    notch = position - forward * (radius / 2)
    c = position - forward * radius + right
    pygame.draw.polygon(screen, colour, [a, b, notch, c], width=LINE_WIDTH)
    line_start = notch - forward * 5
    line_end = notch - forward * 15
    keys = pygame.key.get_pressed()
    if thrusting:
        pygame.draw.line(screen, "white", line_start, line_end, width=LINE_WIDTH)

    
    
    