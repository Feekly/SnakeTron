import pygame
import sys
import random
import math

# Initialize
pygame.init()
pygame.font.init()
pygame.mixer.init()

# --- Config ---
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
TOP_BG = (10, 10, 50)
BOTTOM_BG = (60, 60, 120)

# Directions
DIRECTIONS = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}

# Background gradient
background = pygame.Surface((WIDTH, HEIGHT))
for y in range(HEIGHT):
    t = y / (HEIGHT - 1)
    r = int(TOP_BG[0] * (1 - t) + BOTTOM_BG[0] * t)
    g = int(TOP_BG[1] * (1 - t) + BOTTOM_BG[1] * t)
    b = int(TOP_BG[2] * (1 - t) + BOTTOM_BG[2] * t)
    pygame.draw.line(background, (r, g, b), (0, y), (WIDTH, y))

# Button for the menu
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False

    def draw(self, surface):
        # Button glows when the mouse hovers over it
        color = (30, 200, 250) if self.is_hovered else (20, 100, 150)
        glow = 3 if self.is_hovered else 0

        if glow > 0:
            glow_rect = self.rect.inflate(glow * 2, glow * 2)
            pygame.draw.rect(surface, (60, 220, 255), glow_rect, border_radius=8)

        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (100, 200, 255), self.rect, 2, border_radius=5)

        menuFont = pygame.font.SysFont(None, 36)
        text_surf = menuFont.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos, click):
        return click and self.check_hover(pos)

class Snake:
    def __init__(self, x, y, head_color, controls):
        self.start_pos = (x, y)
        self.head_color = head_color
        self.tail_color = tuple(c // 4 for c in head_color)
        self.controls = controls
        self.reset()

    def reset(self):
        self.body = [self.start_pos]
        self.direction = (1, 0)
        self.grow = False

    def move(self):
        head = self.body[0]
        dx, dy = self.direction
        new_head = ((head[0] + dx) % GRID_WIDTH, (head[1] + dy) % GRID_HEIGHT)
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, key):
        if key in self.controls:
            nd = self.controls[key]
            if nd != (-self.direction[0], -self.direction[1]):
                self.direction = nd

    def draw(self, surf):
        glow = GRID_SIZE + 8
        glow_surf = pygame.Surface((glow, glow), pygame.SRCALPHA)
        glow_surf.fill((*self.head_color, 80))
        for i, seg in enumerate(self.body):
            x, y = seg[0] * GRID_SIZE - 4, seg[1] * GRID_SIZE - 4
            surf.blit(glow_surf, (x, y))
            t = i / (len(self.body) - 1) if len(self.body) > 1 else 0
            c1, c2 = self.head_color, self.tail_color
            color = (int(c1[0]*(1-t) + c2[0]*t), int(c1[1]*(1-t) + c2[1]*t), int(c1[2]*(1-t) + c2[2]*t))
            pygame.draw.rect(surf, color, (seg[0]*GRID_SIZE, seg[1]*GRID_SIZE, GRID_SIZE, GRID_SIZE))

class Particle:
    def __init__(self, pos):
        self.x, self.y = pos
        ang, spd = random.uniform(0, 2*math.pi), random.uniform(1,3)
        self.vx, self.vy = math.cos(ang)*spd, math.sin(ang)*spd
        self.life = random.randint(20,40)
    def update(self): self.x += self.vx; self.y += self.vy; self.life -= 1
    def draw(self, surf):
        if self.life>0:
            alpha = int(255*(self.life/40))
            s = pygame.Surface((4,4), pygame.SRCALPHA)
            s.fill((255,255,255,alpha)); surf.blit(s,(self.x,self.y))

class Food:
    def __init__(self):
        self.pos = None; self.phase = 0; self.respawn()
    def respawn(self):
        self.pos = (random.randrange(GRID_WIDTH), random.randrange(GRID_HEIGHT))
        for _ in range(20): particles.append(Particle((self.pos[0]*GRID_SIZE+GRID_SIZE/2, self.pos[1]*GRID_SIZE+GRID_SIZE/2)))
    def draw(self, surf):
        self.phase += 0.2; dy = math.sin(self.phase)*5
        x, y = self.pos[0]*GRID_SIZE, self.pos[1]*GRID_SIZE + dy
        pygame.draw.rect(surf, YELLOW, (x,y,GRID_SIZE,GRID_SIZE))

# Sound loading (using WAV for best compatibility)
eat_sound = pygame.mixer.Sound('eat.wav')  # convert your SFX to WAV
print('Loaded eat.wav')
die_sound = pygame.mixer.Sound('die.wav')  # convert your SFX to WAV
print('Loaded die.wav')

# Background music (MP3 is fine for music channel)
pygame.mixer.music.load('background.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Display setup
screen = pygame.display.set_mode((WIDTH,HEIGHT)); pygame.display.set_caption('Tron Snakes')
clock = pygame.time.Clock(); font = pygame.font.SysFont(None,48)
controls1 = {pygame.K_w:DIRECTIONS['UP'],pygame.K_s:DIRECTIONS['DOWN'],pygame.K_a:DIRECTIONS['LEFT'],pygame.K_d:DIRECTIONS['RIGHT']}
controls2 = {pygame.K_UP:DIRECTIONS['UP'],pygame.K_DOWN:DIRECTIONS['DOWN'],pygame.K_LEFT:DIRECTIONS['LEFT'],pygame.K_RIGHT:DIRECTIONS['RIGHT']}
particles=[]; s1=Snake(5,5,GREEN,controls1); s2=Snake(20,20,RED,controls2); food=Food()

def draw_game_over(msg):
    screen.blit(background,(0,0))
    t=font.render(msg,True,WHITE); screen.blit(t,t.get_rect(center=(WIDTH//2,HEIGHT//2)))
    i=font.render('R:Restart Q:Quit',True,WHITE); screen.blit(i,i.get_rect(center=(WIDTH//2,HEIGHT//2+50)))
    pygame.display.flip()


def draw_start_menu():
    screen.blit(background, (0, 0))

    # Draw title with glow effect
    title_font = pygame.font.SysFont(None, 80)
    title = title_font.render("TRON SNAKES", True, (0, 200, 255))
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))

    # Glow effect
    glow_surf = pygame.Surface((title.get_width() + 20, title.get_height() + 20), pygame.SRCALPHA)
    pygame.draw.rect(glow_surf, (0, 150, 255, 100), glow_surf.get_rect(), border_radius=10)
    screen.blit(glow_surf, glow_surf.get_rect(center=title_rect.center))
    screen.blit(title, title_rect)

    # Draw animated particles in background
    for i in range(len(particles) - 1, -1, -1):
        particles[i].update()
        particles[i].draw(screen)
        if particles[i].life <= 0:
            particles.pop(i)

    # Randomly add new particles
    if random.random() < 0.2:
        particles.append(Particle((random.randint(0, WIDTH), random.randint(0, HEIGHT))))

    # Draw player controls
    p1_font = pygame.font.SysFont(None, 24)
    p1_text = p1_font.render("Player 1: WASD to move", True, GREEN)
    p1_rect = p1_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 140))

    p2_font = pygame.font.SysFont(None, 24)
    p2_text = p2_font.render("Player 2: Arrow Keys to move", True, RED)
    p2_rect = p2_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 170))

    screen.blit(p1_text, p1_rect)
    screen.blit(p2_text, p2_rect)

    # Draw buttons
    start_button.draw(screen)
    quit_button.draw(screen)

    pygame.display.flip()


# Create menu buttons
start_button = Button(WIDTH // 2 - 100, HEIGHT // 2, 200, 50, "START GAME")
quit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50, "QUIT")

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
game_state = MENU

# Main loop
over = False
winner = ''
while True:
    # Handle common events
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif e.type == pygame.KEYDOWN:
            if game_state == PLAYING:
                s1.change_direction(e.key)
                s2.change_direction(e.key)
            elif game_state == GAME_OVER:
                if e.key == pygame.K_r:
                    s1.reset()
                    s2.reset()
                    food.respawn()
                    particles.clear()
                    over = False
                    game_state = PLAYING
                elif e.key == pygame.K_q:
                    game_state = MENU
            elif game_state == MENU:
                if e.key == pygame.K_RETURN:  # Enter key also starts game
                    game_state = PLAYING
        elif e.type == pygame.MOUSEBUTTONDOWN:
            mouse_clicked = True

    # Update and render based on game state
    if game_state == MENU:
        # Update button hover states
        start_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)

        # Handle button clicks
        if start_button.is_clicked(mouse_pos, mouse_clicked):
            s1.reset()
            s2.reset()
            food.respawn()
            particles.clear()
            game_state = PLAYING
        elif quit_button.is_clicked(mouse_pos, mouse_clicked):
            pygame.quit()
            sys.exit()

        # Draw menu
        draw_start_menu()

    elif game_state == PLAYING:
        # Game logic (from original code)
        clock.tick(FPS)
        s1.move()
        s2.move()
        for sn in (s1, s2):
            if sn.body[0] == food.pos:
                if eat_sound: eat_sound.play()
                sn.grow = True
                food.respawn()
        particles[:] = [p for p in particles if p.life > 0]
        for p in particles: p.update()
        p1, p2 = s1.body[0], s2.body[0]
        dead1 = p1 in s1.body[1:] or p1 in s2.body
        dead2 = p2 in s2.body[1:] or p2 in s1.body
        if dead1 or dead2:
            if die_sound: die_sound.play()
            over = True
            winner = 'Tie!' if dead1 and dead2 else 'P2 Wins!' if dead1 else 'P1 Wins!'
            game_state = GAME_OVER

        # Draw game screen (from original code)
        screen.blit(background, (0, 0))
        food.draw(screen)
        s1.draw(screen)
        s2.draw(screen)
        for p in particles: p.draw(screen)
        pygame.display.flip()

    elif game_state == GAME_OVER:
        # Draw game over screen (from original code)
        draw_game_over(winner)