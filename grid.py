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

for i, rows in enumerate(grid):
    for j, item in enumerate(rows):
        if grid[i][j] == 2:
            print(f"({i}, {j}), ", end="")