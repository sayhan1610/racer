import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
CAR_WIDTH, CAR_HEIGHT = 50, 90
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game")

# Load car image
car_image = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
car_image.fill(RED)
car_rect = car_image.get_rect()
car_rect.center = (WIDTH // 2, HEIGHT - CAR_HEIGHT // 2 - 10)

# Function to create obstacles
def create_obstacle():
    obstacle_color = random.choice([WHITE, GREEN, BLUE, YELLOW])
    obstacle = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
    obstacle.fill(obstacle_color)
    obstacle_rect = obstacle.get_rect()
    obstacle_rect.x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
    obstacle_rect.y = -OBSTACLE_HEIGHT
    return obstacle, obstacle_rect

# Create an initial list of obstacles
obstacles = [create_obstacle() for _ in range(5)]

# Function to display text
def display_text(text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Main game loop
clock = pygame.time.Clock()
running = True
game_active = False
start_time = 0
best_time = None
obstacle_speed = 5
increase_difficulty_interval = 5000  # milliseconds

# Start screen
def start_screen():
    screen.fill(BLACK)
    display_text("Racing Game", 72, WHITE, WIDTH // 2, HEIGHT // 2 - 50)
    display_text("Press any key to start", 36, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Game over screen
def game_over_screen(final_time, best_time):
    screen.fill(BLACK)
    display_text(f"Your time: {final_time:.2f} seconds", 48, WHITE, WIDTH // 2, HEIGHT // 2 - 50)
    display_text(f"Best time: {best_time:.2f} seconds", 48, WHITE, WIDTH // 2, HEIGHT // 2 + 10)
    display_text("Press any key to play again", 36, WHITE, WIDTH // 2, HEIGHT // 2 + 70)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Show start screen initially
start_screen()

while running:
    if not game_active:
        start_time = pygame.time.get_ticks()
        obstacles = [create_obstacle() for _ in range(5)]
        car_rect.center = (WIDTH // 2, HEIGHT - CAR_HEIGHT // 2 - 10)
        obstacle_speed = 5
        game_active = True

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle car movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_rect.left > 0:
        car_rect.x -= 5
    if keys[pygame.K_RIGHT] and car_rect.right < WIDTH:
        car_rect.x += 5
    if keys[pygame.K_UP] and car_rect.top > 0:
        car_rect.y -= 5
    if keys[pygame.K_DOWN] and car_rect.bottom < HEIGHT:
        car_rect.y += 5

    # Move obstacles
    for obstacle, obstacle_rect in obstacles:
        obstacle_rect.y += obstacle_speed
        if obstacle_rect.top > HEIGHT:
            obstacles.remove((obstacle, obstacle_rect))
            obstacles.append(create_obstacle())

    # Check for collisions
    for obstacle, obstacle_rect in obstacles:
        if car_rect.colliderect(obstacle_rect):
            game_active = False
            final_time = (pygame.time.get_ticks() - start_time) / 1000
            if best_time is None or final_time < best_time:
                best_time = final_time
            game_over_screen(final_time, best_time)
            start_screen()

    # Clear the screen
    screen.fill(BLACK)

    # Draw the car
    screen.blit(car_image, car_rect)

    # Draw obstacles
    for obstacle, obstacle_rect in obstacles:
        screen.blit(obstacle, obstacle_rect)

    # Draw the timer
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    timer_text = pygame.font.SysFont(None, 36).render(f'Time: {elapsed_time:.2f}', True, WHITE)
    screen.blit(timer_text, (10, 10))

    # Increase difficulty over time
    if pygame.time.get_ticks() % increase_difficulty_interval < FPS:
        obstacle_speed += 1

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
