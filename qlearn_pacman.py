import numpy as np


grid = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2],
        [1, 2, 1, 2, 2, 2, 2, 2, 2, 1, 2],
        [1, 1, 2, 2, 0, 2, 0, 0, 2, 2, 2],
        [1, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0],
        [1, 1, 2, 1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
rows = cols = 11
actions = ["up", "right", "down", "left"]
q_values = np.zeros((rows, cols, 4)) # 4 as in four actions can be taken at each cell

rewards = np.full((rows, cols), -999)

path = {}
path[1] = [1, 2, 3, 8, 9, 10]
path[2] = [1, 3, 4, 5, 6, 7, 8, 10]
path[3] = [i for i in range(2, 11)]
path[4] = [1, 2]
path[5] = [i for i in range(2, 11)]
path[6] = [1, 2]
path[7] = [i for i in range(1, 11)]
path[8] = [i for i in range(1, 11)]
path[9] = [2, 4, 5, 6]

dots = {}
dots[1] = [1, 2, 3, 8, 9, 10]
dots[2] = [1, 3, 4, 5, 6, 7, 8, 10]
dots[3] = [2, 3, 5, 8, 9, 10]
dots[4] = [2]
dots[5] = [i for i in range(2, 11)]
dots[6] = [1, 2]
dots[7] = [1, 9, 10]
dots[8] = [i for i in range(1, 10)]
dots[9] = [2]


for row_index in range(1, 10):
    for cell in path[row_index]:
        if cell in dots[row_index]:
            rewards[row_index, cell] = 5
        else:
            rewards[row_index, cell] = 0

for row in rewards:
    print(row)

def 

        



