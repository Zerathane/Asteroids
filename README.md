# 🚀 Asteroids

A recreation of the classic **Asteroids** arcade game, built with Python and Pygame as part of [Boot.dev's](https://www.boot.dev/about) backend developer path.

## About

This project is a hands-on learning exercise in Python game development. The goal was to recreate the core mechanics of the 1979 Atari classic — a spaceship navigating a field of drifting asteroids — while getting practical experience with game loops and object-oriented programming.

## Built With

- **Python**
- **Pygame**

## Features

- Player-controlled spaceship
- Asteroid field with moving objects
- Shooting mechanics to destroy asteroids

## What I Learned

This project was primarily a learning exercise, covering:

- **Game loop architecture** — managing update and render cycles each frame
- **Object-oriented design** — modelling game entities (ship, asteroids, bullets) as classes with their own state and behaviour
- **Collision detection** — identifying when game objects interact
- **Pygame fundamentals** — display setup, event handling, sprite groups, and frame timing

## Running the Game

1. Make sure you have Python and Pygame installed:
   ```
   pip install pygame
   ```

2. Clone the repository and run the main file:
   ```
   uv run main.py

Developed on WSL2 — if running in a similar environment, an X server (e.g. XLaunch) is required for the display.

## Controls

| Key | Action |
|-----|--------|
| `W` | Thrust forward |
| `A` | Rotate left |
| `S` | Thrust backwards |
| `D` | Rotate right |
| `Space` | Shoot |

## Acknowledgements

Built as part of [Boot.dev's](https://www.boot.dev/about) backend developer course. The original Asteroids game was developed by Atari and released in 1979.
Font: [Press Start 2P](https://fonts.google.com/specimen/Press+Start+2P) by CodeMan38, licensed under the SIL Open Font License


