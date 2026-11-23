# 🏎️ Car Racing Game

A 2D car racing game built with **Python 3** and **Pygame**. Choose your car, steer left and right on a three-lane road, dodge the oncoming traffic and beat your own high score.

> **PS No. 49** · Concepts: Pygame, Collision Detection, Game Loop

<p align="center">
  <img src="screenshots/menu.png" width="230" alt="Car selection menu">
  <img src="screenshots/gameplay.png" width="230" alt="Gameplay">
  <img src="screenshots/gameover.png" width="230" alt="Game over with new record">
</p>

## Table of contents

- [Features](#features)
- [Quick start](#quick-start)
- [Controls](#controls)
- [How to play](#how-to-play)
- [Game specification](#game-specification)
- [Test cases](#test-cases)
- [Project structure](#project-structure)
- [How the code works](#how-the-code-works)
- [Troubleshooting](#troubleshooting)
- [Upload to GitHub](#upload-to-github)

## Features

- 🚗 **4 selectable cars:** Sports Car, Sedan, Taxi and Police Car, each drawn in code with windscreen, wheels, headlights, tail lights and style details
- 🚦 **Random traffic** in different colours and styles, appearing at random positions on the road
- 💥 **Collision detection** with `Rect.colliderect()`
- 🏆 **Saved high score** in `highscore.txt`, shown during the game and on the Game Over screen
- ✨ **Live record update:** the Best score turns gold the moment you beat the old record, and Game Over shows **NEW RECORD!**
- 🖱️ **Keyboard and mouse/touch support**
- 📦 **Single file, no setup:** installs pygame automatically if it is missing
- ✅ **27 built-in tests** covering every test case, with no extra test file needed

## Quick start

**Requirements:** Python 3.8 or newer. Works on Windows, macOS and Linux.

```bash
# 1. Download or clone the project, then go into the folder
cd car-racing-game

# 2. Play (pygame is installed automatically if missing)
python car_racing_game.py
```

On some macOS and Linux systems use `python3` instead of `python`.

To install pygame yourself instead:

```bash
pip install -r requirements.txt
```

## Controls

| Screen | Key | Action |
|---|---|---|
| Car menu | ← / → | Change car |
| Car menu | ENTER | Start the game |
| Game | ← | Move left 10 px (stops at the road edge, x = 50) |
| Game | → | Move right 10 px (stops at the road edge, x = 310) |
| Game | Any other key | Ignored |
| Game Over | R | Restart with the same car |
| Game Over | C | Back to the car menu |
| Any screen | ESC | Quit |

**Mouse / touch:** click the left or right side of the window to steer or change car, click the middle of the menu to start, and click anywhere after Game Over to restart.

## How to play

1. Pick your car on the menu and press **ENTER**.
2. Steer with the arrow keys and avoid the traffic coming down the road.
3. Every car you pass gives **+1 point**.
4. The game ends when you hit a car. Press **R** to try again or **C** to change car.
5. Your best score is saved automatically, so close the game and come back to beat it.

## Game specification

| Item | Value |
|---|---|
| Window | 400 × 600 px, 60 FPS |
| Road | x = 50 to x = 350 |
| Player car | 40 × 80 px at y = 500, starts at x = 180 |
| Player movement | 10 px per key press, kept inside the road |
| Obstacle cars | 40 × 80 px, random x on the road, move 5 px per frame |
| Spawn rate | One new obstacle every 60 frames (1 second) |
| Score | +1 for each obstacle that leaves the bottom of the screen |
| Game over | Player car collides with an obstacle |

## Test cases

Run all tests (no window opens, and your real high score is never changed):

```bash
python car_racing_game.py --test
```

| # | Test case | Input | Expected output | Status |
|---|---|---|---|---|
| 1 | Normal input | x = 180, key RIGHT | `Player car x = 190 \| Score: 0 \| Game running` | ✅ |
| 2a | Boundary | x = 50, key LEFT | No movement, stays on road (x = 50) | ✅ |
| 2b | Boundary | x = 310, key RIGHT | No movement, stays on road (x = 310) | ✅ |
| 3 | Invalid input | Key SPACE | `Key ignored. Player car x = 180 \| Game running` | ✅ |
| 4a | Valid scenario | Score 3, obstacle at (300, 600) leaves the screen | `Obstacle passed. Score: 4` | ✅ |
| 4b | Valid scenario | Obstacle at (200, 520), player car at (180, 500) | `Collision detected \| Game Over \| Final Score: 4` | ✅ |

The suite also tests the high score (save, load, new record, lower score, damaged file), the car menu, restart, obstacle spawning and a short run of the real game loop.

## Project structure

```
car-racing-game/
├── car_racing_game.py   # complete game + built-in tests (one file)
├── requirements.txt     # pygame
├── README.md
├── screenshots/         # images used in this README
└── .gitignore           # keeps highscore.txt out of GitHub
```

## How the code works

The game data lives in one dictionary called `game`, and the code is made of simple functions with no classes:

```python
game = {"player_x": 180, "score": 0, "obstacles": [[x, y, car], ...],
        "game_over": False, "high_score": 0, "new_record": False, "car": 0, ...}
```

| Function | Job |
|---|---|
| `new_game()` | Create a fresh game dictionary |
| `move_player()` | Move the car left or right inside the road |
| `handle_key()` | Handle one key press and return the console message |
| `handle_click()` | Mouse/touch steering and restart |
| `spawn_obstacle()` | Add a traffic car at the top of the screen |
| `update_game()` | Move obstacles, detect collisions, count score, update the record |
| `run_one_frame()` | Spawn timer plus one update |
| `load_high_score()` / `save_high_score()` | Read and write `highscore.txt` |
| `build_car()` | Draw a car (sports, sedan, taxi, police) with pygame shapes |
| `draw_menu()` / `draw_game()` | Draw the car menu, the road and the Game Over screen |
| `main()` | The game loop: events → update → draw → `clock.tick(60)` |

Game events are also printed to the console, for example `Obstacle passed. Score: 4`.

## Troubleshooting

| Problem | Fix |
|---|---|
| `No module named pygame` | Run `python -m pip install pygame`. On Python 3.13 or newer, if that fails, use `python -m pip install pygame-ce` |
| `python` not found | Use `python3` (macOS/Linux) or `py` (Windows) |
| VS Code shows an import warning | Press `Ctrl+Shift+P`, choose **Python: Select Interpreter** and pick the Python where pygame is installed |
| High score does not save | The game folder may be read-only; the score is then saved in your home folder instead |
| Reset the high score | Delete `highscore.txt` |

## License

Free to use for learning and study projects.
