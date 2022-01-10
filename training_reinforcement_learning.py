import random

from common import states_dict, LEARNING_RATE, EPSILON
from models import Board, AIPlayer
from tools import is_game_over, get_winner


# Training
def train(state_values_x, state_values_o, num_iterations, epsilon=EPSILON,
          learning_rate=LEARNING_RATE):
    player_x = AIPlayer('X', state_values_x, epsilon, learning_rate)
    player_o = AIPlayer('O', state_values_o, epsilon, learning_rate)
    players = (player_x, player_o)
    for iteration in range(num_iterations):
        board = Board()

        print(f"Iteration {iteration}!")
        is_running = True
        current_player_idx = random.choice([0, 1])

        while is_running:
            curr_state_idx = list(states_dict.keys())[
                list(states_dict.values()).index(board.state)]
            current_player = players[current_player_idx]
            print(f"AI {current_player.symbol}'s turn!")

            cell_choice = current_player.get_best_move(board)
            print(f'Selected action = {cell_choice}')
            board.play_move(current_player.symbol, cell_choice)
            new_state_idx = list(states_dict.keys())[
                list(states_dict.values()).index(board.state)]

            board.print()
            player_x.update_state_value(curr_state_idx, new_state_idx)
            player_o.update_state_value(curr_state_idx, new_state_idx)

            is_running = not is_game_over(board.state)
            if not is_running:
                winner = get_winner(board.state)
                if winner:
                    print(f"{winner} won!")
                    continue
                print("Draw!")
                continue

            current_player_idx = (current_player_idx + 1) % 2
    print('Training Complete!')

    return player_x.trained_state_values, player_o.trained_state_values
