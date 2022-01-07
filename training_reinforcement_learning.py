import random

import numpy as np

from common import states_dict
from models import Board, AIPlayer
from tools import is_game_over, get_winner


# Training
def train(state_values_for_ai_x, state_values_for_ai_o,
          learning_rate=0.2, epsilon=0.2, num_iterations=10000):
    player_x = AIPlayer('X', state_values_for_ai_x, epsilon)
    player_o = AIPlayer('O', state_values_for_ai_o, epsilon)
    players = (player_x, player_o)
    for iteration in range(num_iterations):
        board = Board()

        print(f"\nIteration {iteration}!")
        game_status_flag = True
        current_player_idx = random.choice([0, 1])

        while game_status_flag:
            curr_state_idx = list(states_dict.keys())[
                list(states_dict.values()).index(board.state)]
            current_player = players[current_player_idx]
            print(f"\nAI {current_player.symbol}'s turn!")

            block_choice = current_player.get_best_move(board.state)
            print(f'Agent decides to explore! Takes action = {block_choice}')
            board.play_move(current_player.symbol, block_choice)
            new_state_idx = list(states_dict.keys())[
                list(states_dict.values()).index(board.state)]

            board.print()
            player_x.update_state_value(curr_state_idx, new_state_idx,
                                        learning_rate)
            player_o.update_state_value(curr_state_idx, new_state_idx,
                                        learning_rate)

            game_status_flag = not is_game_over(board.state)
            if not game_status_flag:
                winner = get_winner(board.state)
                if winner:
                    print(f"{winner} won!")
                    continue
                print("Draw!")
                continue

            current_player_idx = (current_player_idx + 1) % 2
    print('Training Complete!')

    # Save state values for future use
    np.savetxt('trained_state_values_X.txt', state_values_for_ai_x, fmt='%.6f')
    np.savetxt('trained_state_values_O.txt', state_values_for_ai_o, fmt='%.6f')
