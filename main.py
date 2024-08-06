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
    obstacle = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
    obstacle.fill(WHITE)
    obstacle_rect = obstacle.get_rect()
    obstacle_rect.x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
    obstacle_rect.y = -OBSTACLE_HEIGHT
    return obstacle, obstacle_rect

# Create an initial list of obstacles
obstacles = [create_obstacle() for _ in range(5)]

# Main game loop
clock = pygame.time.Clock()
running = True
start_time = pygame.time.get_ticks()
best_time = None

while running:
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

    # Move obstacles
    for obstacle, obstacle_rect in obstacles:
        obstacle_rect.y += 5
        if obstacle_rect.top > HEIGHT:
            obstacles.remove((obstacle, obstacle_rect))
            obstacles.append(create_obstacle())

    # Check for collisions
    for obstacle, obstacle_rect in obstacles:
        if car_rect.colliderect(obstacle_rect):
            running = False

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

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

# Display the final time
final_time = elapsed_time
if best_time is None or final_time < best_time:
    best_time = final_time
print(f"Your time: {final_time:.2f} seconds")
print(f"Best time: {best_time:.2f} seconds")

pygame.quit()
sys.exit()
