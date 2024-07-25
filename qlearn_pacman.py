import pygame
import numpy as np
import random

pygame.init()

grid = [
    [0, 0, 0, 0, 2, 2, 2, 2, 2],
    [2, 1, 1, 1, 2, 0, 1, 1, 1],
    [2, 2, 2, 1, 2, 1, 0, 0, 0],
    [1, 1, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 2, 1, 1, 1],
    [2, 2, 2, 2, 2, 2, 2, 1, 1],
    [1, 1, 1, 1, 1, 1, 2, 2, 2]
]

dots = [(0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (1, 0), (1, 4), (2, 0), (2, 1), 
(2, 2), (2, 4), (3, 2), (3, 3), (3, 4), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), 
(5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 8), (6, 0), (6, 5), (6, 6), (6, 7), 
(6, 8), (7, 5), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (9, 6), 
(9, 7), (9, 8)]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

CELL_SIZE = 40
WIDTH = len(grid[0]) * CELL_SIZE
HEIGHT = len(grid) * CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Pathfinding")

def draw_grid(grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if cell == 1:
                pygame.draw.rect(screen, BLUE, rect)
            elif cell == 2:
                pygame.draw.circle(screen, WHITE, rect.center, CELL_SIZE//8)

def draw_pacman(pos):
    center = (pos[1] * CELL_SIZE + CELL_SIZE//2, pos[0] * CELL_SIZE + CELL_SIZE//2)
    pygame.draw.circle(screen, YELLOW, center, CELL_SIZE // 2)

# Q-learning parameters
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.95
EPSILON = 1.0
EPSILON_DECAY = 0.9995
EPSILON_MIN = 0.01
EPISODES = 1000  # Number of training episodes

# Initialize Q-table
state_space = len(grid) * len(grid[0])
action_space = 4  # Up, Down, Left, Right
q_table = np.zeros((state_space, action_space))

def get_state(pos):
    return pos[0] * len(grid[0]) + pos[1]

def get_action(state, epsilon):
    if random.uniform(0, 1) < epsilon:
        return random.randint(0, 3)
    else:
        return np.argmax(q_table[state])

def get_next_position(current_pos, action):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right


    next_pos = (current_pos[0] + directions[action][0], current_pos[1] + directions[action][1])
    
    if (0 <= next_pos[0] < len(grid) and 0 <= next_pos[1] < len(grid[0]) and
        grid[next_pos[0]][next_pos[1]] != 1):
        return next_pos
    else:
        return current_pos

def update_q_table(state, action, reward, next_state):
    current_q = q_table[state][action]
    max_future_q = np.max(q_table[next_state])
    new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT_FACTOR * max_future_q)
    q_table[state][action] = new_q

def train():
    global q_table
    epsilon = 0.9
    discount_factor = 0.9
    learning_rate = 0.9

    for episode in range(EPISODES):
        current_pos = (0, 0)
        dots_copy = dots.copy()
        grid_copy = [row[:] for row in grid]
        score = 0
        pellets_collected = 0
        
        while pellets_collected < len(dots):
            state = get_state(current_pos)
            action = get_action(state, epsilon)
            new_pos = get_next_position(current_pos, action)

            if new_pos in dots_copy:
                reward = 200  # Reward for collecting a pellet
                dots_copy.remove(new_pos)
                grid_copy[new_pos[0]][new_pos[1]] = 0
                pellets_collected += 1
            else:
                reward = -3000  # Time penalty

            old_q = q_table[state, action]
            temporal_diff = reward + (discount_factor * np.max(q_table[state]) - old_q)

            

            new_q = (temporal_diff * learning_rate) + old_q
            q_table[state][action] = new_q
            
            #next_state = get_state(new_pos)
            #update_q_table(state, action, reward, next_state)

            current_pos = new_pos
            score += reward

        #epsilon = max(epsilon * epsilon_decay, epsilon_min)

        if episode % 100 == 0:
            print(f"Episode {episode}, Score: {score}, Epsilon: {epsilon:.4f}")

    print("Training complete.")

def display_score(screen, score, pellets_collected, total_pellets):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    pellets_text = font.render(f"Pellets: {pellets_collected}/{total_pellets}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(pellets_text, (10, 50))

def main():
    print("Training Pac-Man...")
    train()
    print("Training complete. Starting game...")

    current_pos = (0, 0)
    clock = pygame.time.Clock()
    score = 0
    pellets_collected = 0
    total_pellets = len(dots)
    dots_copy = dots.copy()
    grid_copy = [row[:] for row in grid]

    running = True
    while pellets_collected < len(dots) and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        state = get_state(current_pos)
        action = get_action(state, 1)
        new_pos = get_next_position(current_pos, action)

        if new_pos in dots_copy:
            reward = 200  # Reward for collecting a pellet
            dots_copy.remove(new_pos)
            grid_copy[new_pos[0]][new_pos[1]] = 0
            pellets_collected += 1
        else:
            reward = -3000  # Time penalty


        current_pos = new_pos
        score += reward

        screen.fill(BLACK)
        draw_grid(grid_copy)
        draw_pacman(current_pos)
        display_score(screen, score, pellets_collected, total_pellets)
        pygame.display.flip()

        clock.tick(5)

    print(f"Game over! Score: {score}, Pellets collected: {pellets_collected}/{total_pellets}")
    pygame.quit()

if __name__ == "__main__":
    main()