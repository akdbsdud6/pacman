import random
import numpy as np

q_table = [
    {0:0, 1:0, -1:0}, #0 : stay, 1 : move right, -1: move left
    {0:0, 1:0, -1:0},
    {0:0, 1:0, -1:0},
    {0:0, 1:0, -1:0},
    {0:0, 1:0, -1:0}
]

# [| a | b | c | d | G |]

reward_board = [0, 0, 0, 0, 100]

epsilon = 0.9
learning_rate = 0.9
discount_factor = 0.9
episodes = 100

def choose_next_action(epsilon, current_pos):
    if np.random.random() > epsilon:
        if current_pos == 0:
            return random.choice([0, 1])
        return random.choice([0, 1, -1])
    else:
        return max(q_table[current_pos], key=q_table[current_pos].get)

for i in range(episodes):
    score = 0
    current_pos = 0
    while current_pos != 4:
        next_action = choose_next_action(epsilon, current_pos)
        score -= 1

        new_pos = current_pos + next_action

        reward = reward_board[new_pos]
        score += reward
        
        old_q = q_table[current_pos][next_action]
        temp_diff = reward + (discount_factor * max(q_table[new_pos], key=q_table[new_pos].get)) - old_q
        new_q = old_q + (learning_rate * temp_diff)

        q_table[current_pos][next_action] = new_q

        current_pos = new_pos
    if i % 10 == 0:
        print(f"{i}th train. Score: {score}")



while current_pos != 4:
    next_action = max(q_table[current_pos], key=q_table[current_pos].get)
    score -= 1

    new_pos = current_pos + next_action

    reward = reward_board[new_pos]
    score += reward

    current_pos = new_pos

print("final score:", score, "\n max possible score: 96")

    

#temporal_difference = reward + (discount_factor * np.max(q_values[row_index, column_index])) - old_q_value

    #update the Q-value for the previous state and action pair
#new_q_value = old_q_value + (learning_rate * temporal_difference)

