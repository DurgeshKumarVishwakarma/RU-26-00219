# 🏎️ Car Racing Game (PS 49)

A 2D car racing game built with **Python 3** and **Pygame**. Steer your car left and right, dodge the traffic coming down the road, and earn a point for every obstacle you pass. One crash and it's Game Over!

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green)
![Tests](https://img.shields.io/badge/Tests-unittest-brightgreen)

**Concepts covered:** Pygame · Collision Detection (`Rect.colliderect`) · Game Loop

---

## 📑 Table of Contents

1. [Features](#-features)
2. [Specification](#-specification)
3. [Controls](#-controls)
4. [Installation and Run](#-installation-and-run)
5. [Running the Tests](#-running-the-tests)
6. [Project Structure](#-project-structure)
7. [How It Works](#-how-it-works)
8. [Troubleshooting](#-troubleshooting)

---

## ✨ Features

- Smooth 60 FPS gameplay in a 400 × 600 window
- Keyboard steering that stays inside the road boundaries
- Randomly placed obstacle cars that move down the road
- Score that goes up for every obstacle you pass
- Collision detection with `Rect.colliderect()`
- Game Over screen with your final score and quick restart
- Obstacles speed up slowly as your score grows (capped for fairness)
- Logic separated from drawing, so it can be tested without opening a window

---

## 📐 Specification

| Item | Value |
|---|---|
| Window | 400 × 600 pixels, 60 FPS |
| Road | x = 50 to 350 |
| Player car | 40 × 80, at y = 500, starts at x = 180, moves 10 px per key press |
| Obstacle cars | 40 × 80, random x on the road, move downwards |
| Score | +1 for each obstacle that passes the bottom of the screen |
| Game over | Collision with an obstacle. Shows "Game Over" and the final score |
| Restart | Press **R** after Game Over |

---

## 🎮 Controls

| Key | Action |
|---|---|
| ⬅️ LEFT arrow | Move left 10 px (stops at the road edge, x = 50) |
| ➡️ RIGHT arrow | Move right 10 px (stops at the road edge, x = 310) |
| **R** | Restart after Game Over |
| **ESC** | Quit |
| Any other key | Ignored |

---

## 🚀 Installation and Run

**Requirements:** Python 3.8 or newer.

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/car-racing-game.git
cd car-racing-game

# 2. (Optional) create a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS / Linux

# 3. Install the dependency
pip install -r requirements.txt

# 4. Start the game
python car_racing.py
```

---

## 🧪 Running the Tests

```bash
python -m unittest -v
```

The tests run **headless** (no window needed) and cover every test case:

| Test case | Input | Expected output |
|---|---|---|
| 1. Normal | x = 180, RIGHT | x = 190, Score 0, Game running |
| 2a. Boundary | x = 50, LEFT | x = 50, no movement |
| 2b. Boundary | x = 310, RIGHT | x = 310, no movement |
| 3. Invalid | SPACE | Key ignored, x = 180, Game running |
| 4a. Valid | Score 3, obstacle at (300, 600) leaves the screen | Obstacle passed, Score 4 |
| 4b. Valid | Obstacle at (200, 520), player at (180, 500) | Collision detected, Game Over, Final Score 4 |

---

## 📁 Project Structure

```
car-racing-game/
├── car_racing.py        # Game class, drawing and game loop
├── test_car_racing.py   # Unit tests for all test cases
├── requirements.txt     # pygame
├── README.md
└── .gitignore
```

---

## ⚙️ How It Works

- **`Game`** holds all the logic (player, obstacles, score, game over). It needs no window, so it can be tested directly.
- **`Game.handle_key()`** processes one key press and returns the console message.
- **`Game.update()`** moves obstacles, checks collisions with `colliderect()`, and scores obstacles that leave the screen.
- **`run()`** is the game loop: handle events → update → draw → `clock.tick(60)`.

```
Start → Handle events → Update (move, collide, score) → Draw → Repeat at 60 FPS
                                   │
                          Collision? ──► Game Over ──► R to restart
```

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'pygame'` | Run `pip install -r requirements.txt` and make sure your editor uses the same Python interpreter |
| `No module named car_racing` when testing | Run the tests from the project folder, where `car_racing.py` is located |
| No window appears on a remote or headless machine | The game needs a display. The tests do not |

---

## 📜 License

Made for the PS 49 Python project. Free to use for learning.
