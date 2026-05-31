import pygame
from explosion import *
from hud import Hud
from shot import SaucerShot, Shot
from player import Player
from constants import *
from logger import *
from asteroid import Asteroid
from asteroidfield import AsteroidField
from game_state import Game_State
import sys
from enemy_saucer import EnemySaucer
from saucer_manager import SaucerManager

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
    saucer_shots = pygame.sprite.Group()
    saucers = pygame.sprite.Group()
    AsteroidField.containers = (updatable)
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (updatable, drawable)
    ShipExplosion.containers = (updatable, drawable)
    EnemySaucer.containers = (updatable, drawable, saucers)
    SaucerManager.containers = (updatable)
    SaucerShot.containers = (saucer_shots, updatable, drawable)
    game_state = Game_State()
    player = Player(x, y)
    asteroid_field = AsteroidField(player)
    hud = Hud(game_state)
    saucer_manager = SaucerManager(game_state, saucers, player)
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
        for saucer in saucers:
            for shot in shots:
                if shot.collides_with(saucer):
                    log_event("saucer_shot")
                    game_state.add_saucer_score(saucer)
                    saucer.kill()
                    shot.kill()
                    ShipExplosion(saucer.position.x, saucer.position.y)
        if not game_state.waiting and game_state.invulnerability_timer <= 0 and game_state.game_over_timer <= 0:
            for saucer_shot in saucer_shots:
                if player.collides_with(saucer_shot):
                    game_state.lose_life()
                    log_event("player_hit_by_saucer")
                    ShipExplosion(player.position.x, player.position.y)
                    saucer_shot.kill()
                    if game_state.is_game_over():
                        game_state.game_over_timer = GAME_OVER_TIMER_SECONDS
                        drawable.remove(player)
                        updatable.remove(player)
                    else:
                        game_state.waiting = True
                        drawable.remove(player) 
                        updatable.remove(player)
        if not game_state.waiting and game_state.invulnerability_timer <= 0 and game_state.game_over_timer <= 0:
            for saucer in saucers:
                if player.collides_with(saucer):
                    game_state.lose_life()
                    log_event("player_hit_by_saucer")
                    ShipExplosion(player.position.x, player.position.y)
                    saucer.kill()
                    if game_state.is_game_over():
                        game_state.game_over_timer = GAME_OVER_TIMER_SECONDS
                        drawable.remove(player)
                        updatable.remove(player)
                    else:
                        game_state.waiting = True
                        drawable.remove(player) 
                        updatable.remove(player)
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
