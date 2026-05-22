import pygame
from explosion import *
from hud import Hud
from shot import Shot
from player import Player
from constants import *
from logger import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from game_state import Game_State
import sys

def main():
    version = pygame.version.ver
    print(f"Starting Asteroids with pygame version: {version}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    pygame.font.init()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    AsteroidField.containers = (updatable)
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (updatable, drawable)
    ShipExplosion.containers = (updatable, drawable)
    game_state = Game_State()
    player = Player(x, y)
    asteroid_field = AsteroidField(player)
    hud = Hud(game_state)
    asteroid_field.spawn_wave(4)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)
        hud.draw(screen)
        if len(asteroids) == 0:
            game_state.next_wave()
            asteroid_field.spawn_wave((game_state.wave_number + 3))
        if game_state.invulnerability_timer > 0:
            if game_state.invulnerability_timer % 0.2 > 0.1:
                drawable.remove(player)
            else:
                drawable.add(player)
            game_state.invulnerability_timer -= dt
        if game_state.game_over_timer > 0:
            game_state.game_over_timer -= dt
            hud.draw_game_over(screen)
            if game_state.game_over_timer <= 0:
                print("Game over!")
                sys.exit()
        if not game_state.waiting and game_state.invulnerability_timer <= 0 and game_state.game_over_timer <= 0:
            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    game_state.lose_life()
                    log_event("player_hit")
                    ShipExplosion(player.position.x, player.position.y)
                    if game_state.is_game_over():
                        game_state.game_over_timer = GAME_OVER_TIMER_SECONDS
                        drawable.remove(player)
                        updatable.remove(player)
                    else:
                        game_state.waiting = True
                        drawable.remove(player) 
                        updatable.remove(player)   
        for asteroid in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    game_state.add_score(asteroid)
                    asteroid.split()
                    shot.kill()
        if game_state.waiting:
            if not game_state.waiting_for_respawn(asteroids):
                player.reset(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                drawable.add(player) 
                updatable.add(player)   
                game_state.waiting = False
                game_state.invulnerability_timer = INVULNERABILITY_SECONDS
        for sprite in drawable:
            sprite.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000
        
if __name__ == "__main__":
    main()
