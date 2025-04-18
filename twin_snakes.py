import pygame
import sys
import random

# Initialize
pygame.init()

# --- Config ---
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Snake A
RED = (255, 0, 0)    # Snake B
YELLOW = (255, 255, 0)  # Food

# Direction Vectors
DIRECTIONS = {
    "UP": (0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0)
}

class Snake:
    def __init__(self, x, y, color, controls):
        self.body = [(x, y)]
        self.direction = (1, 0)
        self.color = color
        self.controls = controls
        self.grow = False

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_x = (head_x + dx) % GRID_WIDTH
        new_y = (head_y + dy) % GRID_HEIGHT
        new_head = (new_x, new_y)

        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, key):
        if key in self.controls:
            new_dir = self.controls[key]
            # prevent 180 turn
            if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
                self.direction = new_dir

    def draw(self, surface):
        for segment in self.body:
            rect = pygame.Rect(
                segment[0] * GRID_SIZE,
                segment[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE
            )
            pygame.draw.rect(surface, self.color, rect)

class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def respawn(self):
        self.position = self.random_position()

    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE
        )
        pygame.draw.rect(surface, YELLOW, rect)

# Player Controls
player1_controls = {
    pygame.K_w: DIRECTIONS["UP"],
    pygame.K_s: DIRECTIONS["DOWN"],
    pygame.K_a: DIRECTIONS["LEFT"],
    pygame.K_d: DIRECTIONS["RIGHT"]
}

player2_controls = {
    pygame.K_UP: DIRECTIONS["UP"],
    pygame.K_DOWN: DIRECTIONS["DOWN"],
    pygame.K_LEFT: DIRECTIONS["LEFT"],
    pygame.K_RIGHT: DIRECTIONS["RIGHT"]
}

snake1 = Snake(5, 5, GREEN, player1_controls)
snake2 = Snake(20, 20, RED, player2_controls)
food = Food()

# Setup screen and clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Twin Snakes")
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            snake1.change_direction(event.key)
            snake2.change_direction(event.key)

    # Move snakes (with wrap-around)
    snake1.move()
    snake2.move()

    # Check for eating food
    for snake in (snake1, snake2):
        if snake.body[0] == food.position:
            snake.grow = True
            food.respawn()

    # Draw
    screen.fill(BLACK)
    food.draw(screen)
    snake1.draw(screen)
    snake2.draw(screen)
    pygame.display.flip()
