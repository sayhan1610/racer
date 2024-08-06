import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
FPS = 60
CAR_WIDTH, CAR_HEIGHT = 50, 50
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 50
POWERUP_WIDTH, POWERUP_HEIGHT = 30, 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ROAD_COLOR = (50, 50, 50)
LINE_COLOR = (255, 255, 255)
BORDER_COLOR = (255, 0, 0)
MAX_OBSTACLES = 3  # Maximum number of obstacles per row
INITIAL_SPEED = 5  # Initial speed of the obstacles
BRAKE_COOLDOWN = 15000  # 15 seconds in milliseconds
POWERUP_INTERVAL = 30000  # 30 seconds in milliseconds
INVINCIBILITY_DURATION = 10000  # 10 seconds in milliseconds

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game")

# Function to scale images while maintaining aspect ratio
def scale_image(image, target_width, target_height):
    original_width, original_height = image.get_size()
    aspect_ratio = original_width / original_height

    if target_width / target_height > aspect_ratio:
        new_height = target_height
        new_width = int(target_height * aspect_ratio)
    else:
        new_width = target_width
        new_height = int(target_width / aspect_ratio)

    return pygame.transform.smoothscale(image, (new_width, new_height))

# Load car image
car_image = pygame.image.load('images/racer.png').convert_alpha()
car_image = scale_image(car_image, CAR_WIDTH, CAR_HEIGHT)
car_rect = car_image.get_rect()
car_rect.center = (WIDTH // 2, HEIGHT - CAR_HEIGHT // 2 - 10)

# Load obstacle images
obstacle_images = [
    pygame.image.load('images/car_red.png').convert_alpha(),
    pygame.image.load('images/car_blue.png').convert_alpha(),
    pygame.image.load('images/car_green.png').convert_alpha()
]
obstacle_images = [scale_image(img, OBSTACLE_WIDTH, OBSTACLE_HEIGHT) for img in obstacle_images]

# Load power-up image
powerup_image = pygame.image.load('images/power.png').convert_alpha()
powerup_image = scale_image(powerup_image, POWERUP_WIDTH, POWERUP_HEIGHT)
powerup_rect = powerup_image.get_rect()

# Function to create obstacles
def create_obstacle(existing_obstacles):
    while True:
        obstacle_image = random.choice(obstacle_images)
        obstacle_rect = obstacle_image.get_rect()
        obstacle_rect.x = random.randint(50, WIDTH - OBSTACLE_WIDTH - 50)
        obstacle_rect.y = -OBSTACLE_HEIGHT
        
        # Check for overlap
        if not any(obstacle_rect.colliderect(o[1]) for o in existing_obstacles):
            return obstacle_image, obstacle_rect

# Function to create power-up
def create_powerup():
    powerup_rect.x = random.randint(60, WIDTH - powerup_rect.width - 60)  # Ensuring it drops within the road
    powerup_rect.y = -powerup_rect.height
    return powerup_rect

# Function to display text
def display_text(text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

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
def game_over_screen(final_time):
    screen.fill(BLACK)
    display_text(f"Your time: {final_time:.2f} seconds", 48, WHITE, WIDTH // 2, HEIGHT // 2 - 50)
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

# Main game loop
clock = pygame.time.Clock()
running = True
game_active = False
start_time = 0
obstacle_speed = INITIAL_SPEED
increase_difficulty_interval = 5000  # milliseconds

# Variables for brake functionality
brake_last_used = -BRAKE_COOLDOWN  # Initialize to allow immediate use

# Variables for power-up functionality
powerup_active = False
powerup_last_drop = 0
invincibility_end_time = 0

# Show start screen initially
start_screen()

while running:
    if not game_active:
        start_time = pygame.time.get_ticks()
        obstacles = []
        for _ in range(MAX_OBSTACLES):
            obstacle = create_obstacle(obstacles)
            obstacles.append(obstacle)
        car_rect.center = (WIDTH // 2, HEIGHT - CAR_HEIGHT // 2 - 10)
        obstacle_speed = INITIAL_SPEED
        brake_last_used = -BRAKE_COOLDOWN  # Reset brake cooldown timer
        powerup_active = False
        invincibility_end_time = 0
        powerup_last_drop = start_time
        powerup_rect.y = -powerup_rect.height  # Hide power-up initially
        game_active = True

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle car movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_rect.left > 50:
        car_rect.x -= 5
    if keys[pygame.K_RIGHT] and car_rect.right < WIDTH - 50:
        car_rect.x += 5
    if keys[pygame.K_UP] and car_rect.top > 0:
        car_rect.y -= 5
    if keys[pygame.K_DOWN] and car_rect.bottom < HEIGHT:
        car_rect.y += 5
    if keys[pygame.K_SPACE]:
        current_time = pygame.time.get_ticks()
        if current_time - brake_last_used >= BRAKE_COOLDOWN:
            obstacle_speed = INITIAL_SPEED
            brake_last_used = current_time

    # Move obstacles
    for obstacle, obstacle_rect in obstacles:
        obstacle_rect.y += obstacle_speed
        if obstacle_rect.top > HEIGHT:
            obstacles.remove((obstacle, obstacle_rect))
            new_obstacle = create_obstacle(obstacles)
            obstacles.append(new_obstacle)

    # Move power-up
    if pygame.time.get_ticks() - powerup_last_drop >= POWERUP_INTERVAL:
        powerup_last_drop = pygame.time.get_ticks()
        create_powerup()

    if powerup_rect.y < HEIGHT:
        powerup_rect.y += obstacle_speed

    # Check for collisions
    if car_rect.colliderect(powerup_rect):
        powerup_active = True
        invincibility_end_time = pygame.time.get_ticks() + INVINCIBILITY_DURATION
        powerup_rect.y = -powerup_rect.height  # Hide power-up after collecting

    if powerup_active and pygame.time.get_ticks() >= invincibility_end_time:
        powerup_active = False

    if not powerup_active:
        for obstacle, obstacle_rect in obstacles:
            if car_rect.colliderect(obstacle_rect):
                game_active = False
                final_time = (pygame.time.get_ticks() - start_time) / 1000
                game_over_screen(final_time)
                start_screen()

    # Clear the screen
    screen.fill(ROAD_COLOR)

    # Draw road lines
    pygame.draw.rect(screen, LINE_COLOR, (WIDTH // 2 - 5, 0, 10, HEIGHT))

    # Draw borders
    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, 50, HEIGHT))
    pygame.draw.rect(screen, BORDER_COLOR, (WIDTH - 50, 0, 50, HEIGHT))

    # Draw the car
    screen.blit(car_image, car_rect)

    # Draw obstacles
    for obstacle, obstacle_rect in obstacles:
        screen.blit(obstacle, obstacle_rect)

    # Draw power-up
    if powerup_rect.y < HEIGHT:
        screen.blit(powerup_image, powerup_rect)

    # Draw the timer
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    timer_text = pygame.font.SysFont(None, 36).render(f'Time: {elapsed_time:.2f}', True, WHITE)
    screen.blit(timer_text, (10, 10))

    # Draw brake cooldown timer
    cooldown_remaining = max(0, (BRAKE_COOLDOWN - (pygame.time.get_ticks() - brake_last_used)) / 1000)
    brake_text = pygame.font.SysFont(None, 36).render(f'Brake CD: {cooldown_remaining:.2f}s', True, WHITE)
    screen.blit(brake_text, (10, 50))

    # Increase difficulty over time
    if pygame.time.get_ticks() % increase_difficulty_interval < FPS:
        obstacle_speed += 1

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
