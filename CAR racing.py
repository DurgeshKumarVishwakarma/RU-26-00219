# Car Racing Game (PS No. 49) - single file, runs on Windows, Mac and Linux
# Just run:  python car_racing_all_devices.py
# If pygame is not installed, this file installs it automatically.
#
# Controls:  LEFT / RIGHT arrow keys   (or click / tap the left or right half
#            of the window), R or click after Game Over = restart, ESC = quit
#
# The game data is kept in one dictionary called "game":
#   game = {"player_x": 180, "score": 0, "obstacles": [[x, y], ...], ...}
# Each obstacle is stored as a small list:  [x, y]

import sys
import random
import subprocess

# ---------- Install pygame automatically if it is missing ----------

try:
    import pygame
except ImportError:
    print("pygame is not installed. Installing it now, please wait...")
    attempts = [
        ["pygame"],
        ["pygame", "--user"],
        ["pygame", "--break-system-packages"],
        ["pygame-ce"],
        ["pygame-ce", "--user"],
        ["pygame-ce", "--break-system-packages"],
    ]
    for attempt in attempts:
        command = [sys.executable, "-m", "pip", "install"] + attempt
        if subprocess.call(command) == 0:
            break
    try:
        import pygame
    except ImportError:
        print("Could not install pygame automatically.")
        print("Please run:  python -m pip install pygame")
        sys.exit(1)

# ---------- Settings ----------

WIDTH = 400            # window width
HEIGHT = 600           # window height
ROAD_LEFT = 50         # road starts at x = 50
ROAD_RIGHT = 350       # road ends at x = 350
CAR_WIDTH = 40         # every car is 40 x 80
CAR_HEIGHT = 80
PLAYER_Y = 500         # player car y position
START_X = 180          # player car starting x position
MOVE_STEP = 10         # player moves 10 px per key press
OBSTACLE_SPEED = 5     # obstacle moves down 5 px every frame
SPAWN_DELAY = 60       # new obstacle every 60 frames (1 second)
FPS = 60

GRASS_COLOR = (34, 139, 34)
ROAD_COLOR = (60, 60, 60)
LINE_COLOR = (240, 240, 240)
PLAYER_COLOR = (30, 144, 255)
OBSTACLE_COLOR = (220, 20, 60)
TEXT_COLOR = (255, 255, 255)


# ---------- Game data ----------

def new_game(score=0, player_x=START_X):
    """Create a fresh game dictionary."""
    game = {
        "player_x": player_x,
        "score": score,
        "obstacles": [],        # list of [x, y]
        "game_over": False,
        "spawn_timer": 0,
        "road_offset": 0,       # only used to scroll the road lines
    }
    return game


def get_status(game):
    if game["game_over"]:
        return "Game Over"
    return "Game running"


# ---------- Main functions ----------

def move_player(game, direction):
    """Move the player car 10 px LEFT or RIGHT, but keep it inside the road."""
    if direction == "LEFT":
        game["player_x"] = game["player_x"] - MOVE_STEP
        if game["player_x"] < ROAD_LEFT:
            game["player_x"] = ROAD_LEFT                  # left edge = 50
    elif direction == "RIGHT":
        game["player_x"] = game["player_x"] + MOVE_STEP
        if game["player_x"] > ROAD_RIGHT - CAR_WIDTH:
            game["player_x"] = ROAD_RIGHT - CAR_WIDTH     # right edge = 310


def handle_key(game, key):
    """Handle one key press and return the message to print."""
    # After Game Over only the R key works (restart)
    if game["game_over"]:
        if key == pygame.K_r:
            game.update(new_game())
            return "Game restarted | Score: 0 | Game running"
        return "Key ignored. Game Over | Final Score: " + str(game["score"])

    if key == pygame.K_LEFT:
        move_player(game, "LEFT")
    elif key == pygame.K_RIGHT:
        move_player(game, "RIGHT")
    else:
        # any other key (SPACE, A, ENTER ...) is ignored
        return ("Key ignored. Player car x = " + str(game["player_x"])
                + " | " + get_status(game))

    return ("Player car x = " + str(game["player_x"])
            + " | Score: " + str(game["score"])
            + " | " + get_status(game))


def handle_click(game, click_x):
    """Mouse click / screen tap: left half = LEFT, right half = RIGHT,
    and any click after Game Over restarts the game."""
    if game["game_over"]:
        return handle_key(game, pygame.K_r)
    if click_x < WIDTH // 2:
        return handle_key(game, pygame.K_LEFT)
    return handle_key(game, pygame.K_RIGHT)


def spawn_obstacle(game, x=None):
    """Add a new obstacle at the top of the screen (random x on the road)."""
    if x is None:
        x = random.randint(ROAD_LEFT, ROAD_RIGHT - CAR_WIDTH)
    game["obstacles"].append([x, -CAR_HEIGHT])


def update_game(game):
    """Move obstacles down, check collisions, count passed obstacles.
    Returns a list of messages to print."""
    messages = []
    if game["game_over"]:
        return messages

    game["road_offset"] = (game["road_offset"] + OBSTACLE_SPEED) % 40
    player_rect = pygame.Rect(game["player_x"], PLAYER_Y, CAR_WIDTH, CAR_HEIGHT)

    for obstacle in game["obstacles"][:]:
        obstacle[1] = obstacle[1] + OBSTACLE_SPEED       # move downwards
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], CAR_WIDTH, CAR_HEIGHT)

        # collision detection using Rect.colliderect()
        if player_rect.colliderect(obstacle_rect):
            game["game_over"] = True
            messages.append("Collision detected | Game Over | Final Score: "
                            + str(game["score"]))
            return messages

        # obstacle left the bottom of the screen = obstacle passed
        if obstacle[1] >= HEIGHT:
            game["obstacles"].remove(obstacle)
            game["score"] = game["score"] + 1
            messages.append("Obstacle passed. Score: " + str(game["score"]))

    return messages


def run_one_frame(game):
    """One frame of game logic: spawn an obstacle on a timer, then update."""
    if game["game_over"]:
        return []
    game["spawn_timer"] = game["spawn_timer"] + 1
    if game["spawn_timer"] >= SPAWN_DELAY:
        game["spawn_timer"] = 0
        spawn_obstacle(game)
    return update_game(game)


# ---------- Drawing ----------

def draw_game(screen, game, font, big_font):
    screen.fill(GRASS_COLOR)
    pygame.draw.rect(screen, ROAD_COLOR,
                     (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))

    # dashed line in the middle of the road
    line_x = (ROAD_LEFT + ROAD_RIGHT) // 2 - 2
    for y in range(-40, HEIGHT, 40):
        pygame.draw.rect(screen, LINE_COLOR, (line_x, y + game["road_offset"], 4, 20))

    # player car and obstacle cars
    pygame.draw.rect(screen, PLAYER_COLOR,
                     (game["player_x"], PLAYER_Y, CAR_WIDTH, CAR_HEIGHT))
    for obstacle in game["obstacles"]:
        pygame.draw.rect(screen, OBSTACLE_COLOR,
                         (obstacle[0], obstacle[1], CAR_WIDTH, CAR_HEIGHT))

    # score
    screen.blit(font.render("Score: " + str(game["score"]), True, TEXT_COLOR), (10, 10))

    # Game Over screen
    if game["game_over"]:
        cover = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        cover.fill((0, 0, 0, 160))
        screen.blit(cover, (0, 0))
        lines = [
            (big_font, "Game Over"),
            (font, "Final Score: " + str(game["score"])),
            (font, "Press R or click to restart"),
        ]
        y = HEIGHT // 2 - 60
        for line_font, text in lines:
            picture = line_font.render(text, True, TEXT_COLOR)
            screen.blit(picture, picture.get_rect(center=(WIDTH // 2, y)))
            y = y + 45


# ---------- Game loop ----------

def main(max_frames=None):
    """Start the game. max_frames is only used for automatic testing."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Car Racing Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)
    big_font = pygame.font.Font(None, 64)
    pygame.key.set_repeat(120, 40)       # hold a key to keep steering

    game = new_game()
    running = True
    frames = 0

    while running:
        # 1. events (keyboard / mouse / close button)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    print(handle_key(game, event.key))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(handle_click(game, event.pos[0]))

        # 2. update the game
        for message in run_one_frame(game):
            print(message)

        # 3. draw
        draw_game(screen, game, font, big_font)
        pygame.display.flip()
        clock.tick(FPS)

        frames = frames + 1
        if max_frames is not None and frames >= max_frames:
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()
    sys.exit(0)