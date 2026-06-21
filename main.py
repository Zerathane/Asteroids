import pygame
from explosion import *
from hud import *
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
from menu import Menu

def reset_game(asteroids, shots, saucers, saucer_shots, updatable, drawable, game_state, player, asteroid_field):
    asteroids.empty()
    shots.empty()
    saucers.empty()
    saucer_shots.empty()
    updatable.empty()
    drawable.empty()
    game_state.reset()
    player.reset(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    updatable.add(player)
    drawable.add(player)
    asteroid_field.spawn_wave(4)

def handle_player_death(game_state, player, drawable, updatable):
    game_state.lose_life()
    log_event("player_hit")
    ShipExplosion(player.position.x, player.position.y)
    drawable.remove(player)
    updatable.remove(player)
    if game_state.is_game_over():
        game_state.game_over_timer = GAME_OVER_TIMER_SECONDS 
    else:
        game_state.waiting = True

def handle_collisions(game_state, player, asteroids, shots, saucers, saucer_shots, updatable, drawable):
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
    if game_state.player_is_vulnerable():
        for asteroid in asteroids:
                if player.collides_with(asteroid):
                    handle_player_death(game_state, player, drawable, updatable)
                    break
        for saucer_shot in saucer_shots:
                if player.collides_with(saucer_shot):
                    handle_player_death(game_state, player, drawable, updatable)
                    saucer_shot.kill()
                    break
        for saucer in saucers:
                if player.collides_with(saucer):
                    handle_player_death(game_state, player, drawable, updatable)
                    saucer.kill()
                    break
        
def handle_events(events):
    for event in events:
        if event.type == pygame.QUIT:
            return False
    return True

def handle_game_state(game_state, updatable, drawable, player, hud, asteroids, dt, screen):
    if game_state.waiting:
        if not game_state.waiting_for_respawn(asteroids):
            player.reset(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            drawable.add(player) 
            updatable.add(player)   
            game_state.waiting = False
            game_state.invulnerability_timer = INVULNERABILITY_SECONDS
    if game_state.invulnerability_timer > 0:
        if game_state.invulnerability_timer % 0.2 > 0.1:
            drawable.remove(player)
        else:
            drawable.add(player)
        game_state.invulnerability_timer -= dt
    if game_state.game_over_timer > 0:
        game_state.game_over_timer -= dt
        if game_state.game_over_timer <= 0:
            print("Game over!")
            return AppState.MAIN_MENU

def draw(screen, drawable, hud, game_state):
    screen.fill("black")
    hud.draw(screen)
    if game_state.game_over_timer > 0:
        hud.draw_game_over(screen)
    for sprite in drawable:
        sprite.draw(screen)
    pygame.display.flip()

def manage_wave(asteroids, game_state, asteroid_field):
    if len(asteroids) == 0:
        game_state.next_wave()
        asteroid_field.spawn_wave(min((game_state.wave_number + 3), 11))

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
    current_state = AppState.MAIN_MENU
    menu = Menu()

    while True:
        events = pygame.event.get()
        log_state()
        if not handle_events(events):
            break 

        if current_state == AppState.MAIN_MENU:
            selection = menu.update(events, dt)
            if selection == "play":
                current_state = AppState.PLAYING
                reset_game(asteroids, shots, saucers, saucer_shots, updatable, drawable, game_state, player, asteroid_field)
            elif selection == "leaderboard":
                current_state = AppState.LEADERBOARD
            elif selection == "help":
                current_state = AppState.HELP
            elif selection == "quit":
                break
            screen.fill("black")
            menu.draw(screen)
            pygame.display.flip()

        elif current_state == AppState.PLAYING:
            updatable.update(dt)
            manage_wave(asteroids, game_state, asteroid_field)
            handle_collisions(game_state, player, asteroids, shots, saucers, saucer_shots, updatable, drawable)
            new_state = handle_game_state(game_state, updatable, drawable, player, hud, asteroids, dt, screen)
            if new_state is not None:
                current_state = new_state
            draw(screen, drawable, hud, game_state)  
        dt = clock.tick(60) / 1000
        
if __name__ == "__main__":
    main()
