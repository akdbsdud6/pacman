from queue import PriorityQueue

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
    
def heuristic(current, dots):
    return min(manhattan(current, dot) for dot in dots)

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
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

def pacman_move(grid, current_pos, dots):
    #nearest_dot = heuristic(current_pos, dots)
    #min_dist = 999999
    #for dot in dots:
    #    current_dist = manhattan(current_pos, dot)
    #    if current_dist < min_dist:
    #        min_dist = current_dist
    #        nearest_dot = dot
    nearest_dot = min(dots, key=lambda dot: manhattan(current_pos, dot))
    path = astar(grid, current_pos, nearest_dot)

    if path:
        next_pos = path[1]
        if next_pos in dots:
            dots.remove(next_pos)
            grid[next_pos[0]][next_pos[1]] = 0
        return next_pos
    else:
        return None
    
def print_board(grid, current_pos):
    for i, row in enumerate(grid):
        for j, item in enumerate(row):
            if (i, j) == current_pos:
                print("P ", end="")
            elif (i, j) in dots:
                print("* ", end="")
            else:
                print(f"{item} ", end="")
        print()
    print("\n")

    
def main():

    current_pos = (0, 0)
    while dots:
        new_pos = pacman_move(grid, current_pos, dots)
        if new_pos:
            current_pos = new_pos
            print_board(grid, current_pos)
        else:
            break

    print("Game over! All dots collected")

    #for i, rows in enumerate(grid):
    #    for j, item in enumerate(rows):
    #        if (i, j) == current_pos:
    #            print("P ", end="")
    #        else:
    #            print(item, "", end="")
    #    print("\n")

if __name__ == "__main__":
    main()

