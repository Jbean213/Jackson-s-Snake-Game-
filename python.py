import pygame
import random

# Initialize pygame
pygame.init()

# Set up the display
canvas_size = 400
screen = pygame.display.set_mode((canvas_size, canvas_size))
pygame.display.set_caption('Snake Game')

# Colors
WHITE = (255, 255, 255)
LIME = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game variables
snake_size = 10
snake = [(200, 200)]
food = (random.randint(0, canvas_size - snake_size) // snake_size * snake_size,
        random.randint(0, canvas_size - snake_size) // snake_size * snake_size)
dx, dy = snake_size, 0
score = 0
paused = False
game_over = False

# Fonts
font = pygame.font.Font(None, 36)

# Function to handle events
def handle_events():
    global dx, dy, paused, game_over

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif game_over and event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                restart_game()
            elif not paused:
                change_direction(event)

# Function to change direction based on key pressed
def change_direction(event):
    global dx, dy

    if event.key == pygame.K_LEFT and dx == 0:
        dx, dy = -snake_size, 0
    elif event.key == pygame.K_RIGHT and dx == 0:
        dx, dy = snake_size, 0
    elif event.key == pygame.K_UP and dy == 0:
        dx, dy = 0, -snake_size
    elif event.key == pygame.K_DOWN and dy == 0:
        dx, dy = 0, snake_size

# Function to draw snake
def draw_snake():
    for part in snake:
        pygame.draw.rect(screen, LIME, (part[0], part[1], snake_size, snake_size))

# Function to move snake
def move_snake():
    global score

    head = (snake[0][0] + dx, snake[0][1] + dy)
    snake.insert(0, head)

    if head == food:
        score += 1
        generate_food()
    else:
        snake.pop()

# Function to generate food
def generate_food():
    global food

    food = (random.randint(0, canvas_size - snake_size) // snake_size * snake_size,
            random.randint(0, canvas_size - snake_size) // snake_size * snake_size)

# Function to draw food
def draw_food():
    pygame.draw.rect(screen, RED, (food[0], food[1], snake_size, snake_size))

# Function to draw score
def draw_score():
    score_text = font.render('Score: ' + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

# Function to check if game over
def game_over_check():
    global game_over

    if (snake[0][0] < 0 or snake[0][0] >= canvas_size or
        snake[0][1] < 0 or snake[0][1] >= canvas_size or
        len(snake) != len(set(snake))):
        game_over = True

# Function to restart game
def restart_game():
    global snake, food, dx, dy, score, game_over

    snake = [(200, 200)]
    generate_food()
    dx, dy = snake_size, 0
    score = 0
    game_over = False

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BLUE)  # Set background color

    handle_events()

    if not paused and not game_over:
        move_snake()
        draw_food()
        draw_snake()
        draw_score()
        game_over_check()

    if game_over:
        game_over_text = font.render('Game Over', True, WHITE)
        screen.blit(game_over_text, ((canvas_size - game_over_text.get_width()) // 2, (canvas_size - game_over_text.get_height()) // 2))

    pygame.display.update()
    clock.tick(10)  # Adjust snake speed

pygame.quit()
