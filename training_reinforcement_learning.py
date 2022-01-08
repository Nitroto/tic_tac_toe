import random

from common import states_dict
from models import Board, AIPlayer
from tools import is_game_over, get_winner, save_state_values


# Training
def train(state_values_for_ai_x, state_values_for_ai_o, num_iterations=10000,
          learning_rate=0.2, epsilon=0.2):
    player_x = AIPlayer('X', state_values_for_ai_x, epsilon)
    player_o = AIPlayer('O', state_values_for_ai_o, epsilon)
    players = (player_x, player_o)
    for iteration in range(num_iterations):
        board = Board()

        print(f"Iteration {iteration}!")
        game_status_flag = True
        current_player_idx = random.choice([0, 1])

        while game_status_flag:
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

    save_state_values(state_values_for_ai_x, state_values_for_ai_o)
