import pygame, random, sys

# --- Initialization ---
pygame.init()
WIDTH, HEIGHT = 800, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Run")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 40)

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_COLOR = (83, 83, 83)
DINO_COLOR = (0, 100, 200)
OBSTACLE_COLOR = (200, 50, 50)

# --- Dino ---
dino = pygame.Rect(50, HEIGHT - 80, 40, 40)
dino_y_vel = 0
gravity = 1
jump_strength = -15
on_ground = True

# --- Obstacles ---
obstacles = []
obstacle_timer = 0
spawn_interval = 1500  # milliseconds

# --- Score ---
score = 0
start_ticks = pygame.time.get_ticks()

# --- Game Loop ---
while True:
    screen.fill(WHITE)

    # Time and score
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    score = int(seconds * 10)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and on_ground:
        dino_y_vel = jump_strength
        on_ground = False

    # Dino physics
    dino_y_vel += gravity
    dino.y += dino_y_vel
    if dino.bottom >= HEIGHT - 40:
        dino.bottom = HEIGHT - 40
        dino_y_vel = 0
        on_ground = True

    # Obstacle spawning
    if pygame.time.get_ticks() - obstacle_timer > spawn_interval:
        obstacle_timer = pygame.time.get_ticks()
        obstacle = pygame.Rect(WIDTH, HEIGHT - 60, 20, 40)
        obstacles.append(obstacle)

    # Move & remove obstacles
    for obs in obstacles:
        obs.x -= 6
    obstacles = [obs for obs in obstacles if obs.x > -20]

    # Collision
    for obs in obstacles:
        if dino.colliderect(obs):
            print("Game Over! Final Score:", score)
            pygame.quit()
            sys.exit()

    # Drawing
    pygame.draw.rect(screen, GROUND_COLOR, (0, HEIGHT - 40, WIDTH, 40))
    pygame.draw.rect(screen, DINO_COLOR, dino)
    for obs in obstacles:
        pygame.draw.rect(screen, OBSTACLE_COLOR, obs)

    score_text = FONT.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update display and control FPS
    pygame.display.flip()
    clock.tick(60)
