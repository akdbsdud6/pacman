import pygame
import numpy as np
import random
from tqdm import tqdm

# Initialize Pygame
pygame.init()


grid = [
    [0, 0, 0, 0, 2, 2, 2, 2, 2, 1],
    [2, 1, 1, 1, 2, 0, 1, 1, 1, 1],
    [2, 2, 2, 1, 2, 1, 0, 0, 0, 1],
    [1, 1, 2, 2, 2, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 2, 2, 2, 2, 2, 1],
    [2, 2, 2, 2, 2, 0, 0, 0, 2, 1],
    [2, 0, 0, 0, 0, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
    [2, 2, 2, 2, 2, 2, 2, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 2, 2, 1]
]

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Grid size
GRID_SIZE = len(grid)
CELL_SIZE = 30
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Q-Learning")


# Q-table
Q = np.zeros((GRID_SIZE, GRID_SIZE, 4))  # 4 actions: 0:up, 1:right, 2:down, 3:left

# Hyperparameters
EPISODES = 1000
EPSILON = 0.1
ALPHA = 0.1
GAMMA = 0.9

# Rewards
DOT_REWARD = 10
GHOST_PENALTY = -100
MOVE_PENALTY = -1

def reset_game():
    global pacman_pos, ghost_pos, grid
    pacman_pos = [1, 1]
    ghost_pos = [GRID_SIZE-1, GRID_SIZE-2]
    grid = [
    [0, 0, 0, 0, 2, 2, 2, 2, 2, 1],
    [2, 1, 1, 1, 2, 0, 1, 1, 1, 1],
    [2, 2, 2, 1, 2, 1, 0, 0, 0, 1],
    [1, 1, 2, 2, 2, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 2, 2, 2, 2, 2, 1],
    [2, 2, 2, 2, 2, 0, 0, 0, 2, 1],
    [2, 0, 0, 0, 0, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
    [2, 2, 2, 2, 2, 2, 2, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 2, 2, 1]
    ]
    
    # Place dots

def move_ghost():
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    dx, dy = random.choice(directions)
    new_x, new_y = ghost_pos[0] + dx, ghost_pos[1] + dy
    if 0 < new_x < GRID_SIZE-1 and 0 < new_y < GRID_SIZE-1 and grid[new_x][new_y] != 1:
        ghost_pos[0], ghost_pos[1] = new_x, new_y

def draw_grid():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            rect = pygame.Rect(j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[i][j] == 1:
                pygame.draw.rect(screen, BLUE, rect)
            elif grid[i][j] == 2:
                pygame.draw.circle(screen, WHITE, rect.center, CELL_SIZE//4)

def draw_pacman():
    rect = pygame.Rect(pacman_pos[1]*CELL_SIZE, pacman_pos[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.circle(screen, YELLOW, rect.center, CELL_SIZE//2)

def draw_ghost():
    rect = pygame.Rect(ghost_pos[1]*CELL_SIZE, ghost_pos[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.circle(screen, RED, rect.center, CELL_SIZE//2)

def get_state():
    return tuple(pacman_pos)

def choose_action(state):
    if random.random() < EPSILON:
        return random.randint(0, 3)
    return np.argmax(Q[state])

def take_action(action):
    global pacman_pos
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    dx, dy = directions[action]
    new_x, new_y = pacman_pos[0] + dx, pacman_pos[1] + dy
    
    if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and grid[new_x][new_y] != 1:
        pacman_pos = [new_x, new_y]
        
        if grid[new_x][new_y] == 2:  # Dot
            grid[new_x][new_y] = 0
            return DOT_REWARD
        elif grid[new_x][new_y] == ghost_pos:
            return GHOST_PENALTY
        else:
            return MOVE_PENALTY
    return MOVE_PENALTY

def update_q_table(state, action, reward, next_state):
    best_next_action = np.argmax(Q[next_state])
    td_target = reward + GAMMA * Q[next_state + (best_next_action,)]
    td_error = td_target - Q[state + (action,)]
    Q[state + (action,)] += ALPHA * td_error

# Training phase (without display)
print("Training Pac-Man...")
for episode in tqdm(range(EPISODES)):
    reset_game()
    state = get_state()
    total_reward = 0
    
    while True:
        action = choose_action(state)
        reward = take_action(action)
        next_state = get_state()
        update_q_table(state, action, reward, next_state)
        
        total_reward += reward
        state = next_state
        
        move_ghost()
        
        if reward == GHOST_PENALTY or not np.any(grid == 2):
            break

print("Training complete!")

# Gameplay demonstration
def play_game():
    reset_game()
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        state = get_state()
        action = np.argmax(Q[state])  # Always choose the best action
        reward = take_action(action)
        
        move_ghost()
        
        # Draw everything
        screen.fill(BLACK)
        draw_grid()
        draw_pacman()
        draw_ghost()
        pygame.display.flip()
        
        if reward == GHOST_PENALTY or not np.any(grid == 2):
            print("Game Over!")
            pygame.time.wait(1000)  # Wait for 1 second before resetting
            reset_game()
        
        clock.tick(10)  # Adjust for speed

# Run the gameplay demonstration
play_game()

pygame.quit()