import random
import pygame
from circleshape import CircleShape
from constants import *
from shot import SaucerShot

class EnemySaucer(CircleShape):
    def __init__(self, x, y, radius, size, side, player):
        super().__init__(x, y, radius)
        self.shot_cooldown = SAUCER_SHOT_COOLDOWN_SECONDS
        self.size = size
        self.side = side
        self.player = player
        if self.side == "left":
            self.velocity = pygame.Vector2(ENEMY_SAUCER_SPEED, 0)
        else:
            self.velocity = pygame.Vector2(-ENEMY_SAUCER_SPEED, 0)       
        self.direction_change_timer = ENEMY_SAUCER_DIRECT_CHANGE_INTERVAL_SECONDS
        if self.size == "small":
            self.velocity = self.velocity.normalize() * ENEMY_SAUCER_SMALL_SPEED
        else:
            self.velocity = self.velocity.normalize() * ENEMY_SAUCER_SPEED
        self.lower_points = [
            pygame.Vector2(-1.5 * self.radius, 0),
            pygame.Vector2(1.5 * self.radius, 0),
            pygame.Vector2(1 * self.radius, (0.5 * self.radius)),
            pygame.Vector2(-1 * self.radius, (0.5 * self.radius)),
        ]
        self.middle_points = [
            pygame.Vector2(-1.55 * self.radius, (self.radius * -0.2)),
            pygame.Vector2(1.55 * self.radius, (self.radius * -0.2)),
            pygame.Vector2(1.55 * self.radius, 0),
            pygame.Vector2(-1.55 * self.radius, 0),
        ]
        self.upper_points = [
            pygame.Vector2(-1 * self.radius, (self.radius * -0.7)),
            pygame.Vector2(1 * self.radius, (self.radius * -0.7)),
            pygame.Vector2(1.5 * self.radius, (self.radius * -0.2)),
            pygame.Vector2(-1.5 * self.radius, (self.radius * -0.2)),
        ]
        self.dome_points = [
            pygame.Vector2(-0.25 * self.radius, (self.radius * -0.95)),
            pygame.Vector2(0.25 * self.radius, (self.radius * -0.95)),
            pygame.Vector2(0.80 * self.radius, (self.radius * -0.70)),
            pygame.Vector2(-0.80 * self.radius, (self.radius * -0.70)),
        ]
        

    def move(self, dt):
        self.position += self.velocity * dt
        self.direction_change_timer -= dt
        if self.direction_change_timer <= 0:
            self.direction_change_timer = ENEMY_SAUCER_DIRECT_CHANGE_INTERVAL_SECONDS
            self.velocity.y = random.uniform(-ENEMY_SAUCER_SPEED, ENEMY_SAUCER_SPEED)



    def update(self, dt):
        self.move(dt)
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0
        if self.position.x < -ENEMY_SAUCER_LARGE_RADIUS * 2:
            self.kill()
        elif self.position.x > SCREEN_WIDTH + ENEMY_SAUCER_LARGE_RADIUS * 2:
            self.kill()
        self.shot_cooldown -= dt
        if self.shot_cooldown <= 0:
            if self.size == "large":
                self.shoot_random()
                self.shot_cooldown = SAUCER_SHOT_COOLDOWN_SECONDS
            else:
                self.shoot_at_player(self.player)
                self.shot_cooldown = SAUCER_SHOT_COOLDOWN_SECONDS

        

    def draw(self, screen):
        lower_offset_points = []
        for point in self.lower_points:
            lower_offset_points.append(self.position + point)
        pygame.draw.polygon(screen, "white", lower_offset_points, width=LINE_WIDTH)
        middle_offset_points = []
        for point in self.middle_points:
            middle_offset_points.append(self.position + point)
        pygame.draw.polygon(screen, "white", middle_offset_points, width=LINE_WIDTH)
        upper_offset_points = []
        for point in self.upper_points:
            upper_offset_points.append(self.position + point)
        pygame.draw.polygon(screen, "white", upper_offset_points, width=LINE_WIDTH)
        dome_offset_points = []
        for point in self.dome_points:
            dome_offset_points.append(self.position + point)
        pygame.draw.polygon(screen, "white", dome_offset_points, width=LINE_WIDTH)

    def shoot_random(self):
        velocity = pygame.Vector2(1, 0).rotate(random.uniform(0, 360)).normalize() * SAUCER_SHOOT_SPEED
        SaucerShot(self.position.x, self.position.y, SHOT_RADIUS).velocity = velocity
        
    def shoot_at_player(self, player):
        direction = (player.position - self.position).normalize()
        velocity = direction * SAUCER_SHOOT_SPEED
        SaucerShot(self.position.x, self.position.y, SHOT_RADIUS).velocity = velocity


