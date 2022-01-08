import numpy as np

from common import players, PlayerChoices, states_dict
from generate_initial_data import generate_initial_data
from models import Board, AIPlayer
from tools import is_game_over, get_winner, save_state_values, \
    input_board_print
from training_reinforcement_learning import train
from user_input import select_symbol, select_first_player, select_next_cell

confirmation_answers = ('y', 'yes')


def main():
    # Load trained state values
    try:
        state_values_for_ai_x = np.loadtxt('trained_state_values_X.txt',
                                           dtype=np.float64)
        state_values_for_ai_o = np.loadtxt('trained_state_values_O.txt',
                                           dtype=np.float64)
    except FileNotFoundError:
        state_values_for_ai_x, state_values_for_ai_o = generate_initial_data()

    train_ai = input("Do you want to run AI train (y/n)? ")
    if train_ai.lower() in confirmation_answers:
        train(state_values_for_ai_x, state_values_for_ai_o)

    # Computer vs Human Games
    play_game = input("Do you want to play a game? ")
    while play_game in confirmation_answers:
        human_symbol = select_symbol()
        computer_symbol = list(
            filter(lambda s: (s != human_symbol), players))[0]
        state_values_for_ai = state_values_for_ai_x
        if computer_symbol != 'O':
            state_values_for_ai = state_values_for_ai_o
        board = Board()
        game_status_flag = True
        computer = AIPlayer(computer_symbol, state_values_for_ai, 0)
        current_player = select_first_player(human_symbol, computer_symbol)
        first_round = True
        print('Let the game begin')
        while game_status_flag:
            if current_player == PlayerChoices.HUMAN:  # Human input
                print("Human\'s Turn")
                if first_round:
                    first_round = False
                    input_board_print()
                cell_choice = select_next_cell(board)
                board.play_move(human_symbol, cell_choice)
                current_player = PlayerChoices.COMPUTER
            elif current_player == PlayerChoices.COMPUTER:
                curr_state_idx = list(states_dict.keys())[
                    list(states_dict.values()).index(board.state)]
                # AI turn
                print("Computers\'s Turn")
                ai_move = computer.get_best_move(board)
                board.play_move(computer.symbol, ai_move)
                new_state_idx = list(states_dict.keys())[
                    list(states_dict.values()).index(board.state)]
                computer.update_state_value(curr_state_idx, new_state_idx,
                                            learning_rate=0.2)
                current_player = PlayerChoices.HUMAN
            else:
                print("Wrong choice")
                break

            board.print()

            game_status_flag = not is_game_over(board.state)

            if not game_status_flag:
                winner = get_winner(board.state)
                if winner:
                    print(f"{winner} won!")
                    continue
                print("Draw!")
                continue

        play_game = input("Do you want to play another game(y/n)?")

    print('See you!')
    save_state_values(state_values_for_ai_x, state_values_for_ai_o)


if __name__ == '__main__':
    main()
