import pygame
import random
import time
from queue import PriorityQueue

pygame.init()

grid = [
    [0, 0, 0, 0, 2, 2, 2, 2, 2, 0],
    [2, 1, 1, 1, 2, 0, 1, 1, 0, 2],
    [2, 2, 2, 1, 2, 1, 0, 0, 0, 2],
    [1, 1, 2, 2, 2, 0, 0, 0, 0, 2],
    [0, 0, 0, 0, 2, 2, 2, 2, 2, 1],
    [2, 2, 2, 2, 2, 0, 0, 0, 2, 2],
    [2, 0, 0, 0, 0, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 2, 1, 1, 1, 2],
    [2, 2, 2, 2, 2, 2, 2, 1, 1, 2],
    [1, 1, 1, 1, 1, 1, 2, 2, 2, 2]
]

dots = []

for i, rows in enumerate(grid):
    for j, item in enumerate(rows):
        if grid[i][j] == 2:
            dots.append((i, j))
            #print(f"({i}, {j}), ", end="")




class Node:
    def __init__(self, position, g=0, h=0, parent=None):
        self.position = position
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

    def __eq__(self, other):
        return self.position == other.position
    
    def __lt__(self, other):
        return self.f < other.f

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal, ghost_pos):
    rows, cols = len(grid), len(grid[0])
    start_node = Node(start)
    goal_node = Node(goal)

    open_list = PriorityQueue()
    open_list.put((0, start_node))

    closed_set = set()

    while not open_list.empty():
        current_node = open_list.get()[1]

        if current_node == goal_node:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]
        
        closed_set.add(current_node.position)

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_pos = (current_node.position[0] + dx, current_node.position[1] + dy)

            if next_pos[0] >= rows or next_pos[0] < 0:
                continue
            elif next_pos[1] >= cols or next_pos[1] < 0:
                continue
            elif grid[next_pos[0]][next_pos[1]] == 1:
                continue
            elif next_pos == ghost_pos:
                continue
            elif next_pos in closed_set:
                continue

            next_node = Node(next_pos, g=current_node.g + 1, h=manhattan(next_pos, goal), parent=current_node)

            if next_node not in [item[1] for item in open_list.queue]:
                open_list.put((next_node.f, next_node))
            else:
                for i, (f, node) in enumerate(open_list.queue):
                    if node == next_node and node.g > next_node.g:
                        del open_list.queue[i]
                        open_list.put((next_node.f, next_node))
                        break
    return None

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

CELL_SIZE = 40
WIDTH = len(grid[0]) * CELL_SIZE
HEIGHT = len(grid) * CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Pathfinding")

class Ghost:
    def __init__(self, position, color):
        self.position = position
        self.color = color

    def draw(self):
        center = (self.position[1] * CELL_SIZE + CELL_SIZE//2, self.position[0] * CELL_SIZE + CELL_SIZE//2)
        pygame.draw.circle(screen, self.color, center, CELL_SIZE//2 - 2)

    #def move(self, grid, pacman_pos):
    #    path_to_pacman = astar(grid, self.position, pacman_pos, self.position)
    #    if path_to_pacman and len(path_to_pacman) > 1:
    #        self.position = path_to_pacman[1]
    #    return self.position

    def move(self, grid, pacman_pos):
        rows, cols = len(grid), len(grid[0])
        move_list = []

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_pos = (self.position[0] + dx, self.position[1] + dy)

            if next_pos[0] >= rows or next_pos[0] < 0:
                continue
            elif next_pos[1] >= cols or next_pos[1] < 0:
                continue
            elif grid[next_pos[0]][next_pos[1]] == 1:
                continue

            #if next_pos == pacman_pos:
            #    self.position = next_pos
            #    return next_pos
            
            move_list.append(next_pos)

        self.position = random.choice(move_list)
        return self.position

def draw_grid():
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

def pacman_move(grid, current_pos, dots, ghost_pos):
    sorted_dots = sorted(dots, key=lambda dot: manhattan(current_pos, dot))

    for dot in sorted_dots:
        path = astar(grid, current_pos, dot, ghost_pos)
        if path and len(path) > 1:
            return path[1]  # Return the next position in the path

    #nearest_dot = min(dots, key=lambda dot: manhattan(current_pos, dot))
    #path = astar(grid, current_pos, nearest_dot, ghost_pos)

    #if path:
    #    return path[1]
    #else:
    return None
    

def main():
    ghost_pos = (6, 7)
    ghost = Ghost(ghost_pos, RED)
    #cleared = True

    current_pos = (0, 0)
    clock = pygame.time.Clock()

    running = True
    while running and dots:
        screen.fill(BLACK)
        draw_grid()
        draw_pacman(current_pos)
        ghost.draw()
        pygame.display.flip()

        if ghost_pos == current_pos:
            #cleared = False
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        new_pos = pacman_move(grid, current_pos, dots, ghost_pos)
        ghost_pos = ghost.move(grid, current_pos)
        if new_pos:
            current_pos = new_pos
            if new_pos in dots:
                dots.remove(new_pos)
                grid[new_pos[0]][new_pos[1]] = 0
        else:
            screen.fill(BLACK)
            draw_grid()
            draw_pacman(current_pos)
            ghost.draw()
            pygame.display.flip()
            break

        
        
        pygame.display.flip()


        clock.tick(5)

    if len(dots) == 0:
        print("Game over! All dots collected")
    elif ghost_pos == current_pos:
        print("Game over! Pac-Man caught by ghost")
    else:
        print("Error occured")
    pygame.quit()


if __name__ == "__main__":
    main()
