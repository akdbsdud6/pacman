from queue import PriorityQueue

grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 1, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0]
]

class Node:
    def __init__(self, position, g=0, h=0, parent=None):
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g+h
        self.position = position

    def __eq__(self, other):
        return self.position == other.position
    
    def __lt__(self, other):
        return self.f < other.f
    
def heuristic(a, b):
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

            next_node = Node(next_pos, current_node.g + 1, heuristic(next_pos, goal), current_node)

            if next_node not in [item[1] for item in open_list.queue]:
                open_list.put((next_node.f, next_node))
            else:
                for i, (f, node) in enumerate(open_list.queue):
                    if node == next_node and node.g > next_node.g:
                        del open_list.queue[i]
                        open_list.put((next_node.f, next_node))
                        break
    return None

    
def main():

    start = (0, 0)
    goal = (9, 8)
    path = astar(grid, start, goal)

    if path:
        print("Path found:", path)
    # Visualize the path on the grid
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if (i, j) == start:
                    print("S", end=" ")
                elif (i, j) == goal:
                    print("G", end=" ")
                elif (i, j) in path:
                    print("*", end=" ")
                else:
                    print(cell, end=" ")
            print("\n")
    else:
        print("No path found")





        # check neighbors of popped
        # assign popped as the parent of its neighbors
        # add those neighbors to the priority queue
        # repeat

if __name__ == "__main__":
    main()

