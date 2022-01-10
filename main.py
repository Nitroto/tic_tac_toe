from common import players, PlayerChoices, states_dict
from models import Board, AIPlayer
from tools import is_game_over, get_winner, save_state_values, \
    input_board_print, load_trained_state_values
from training_reinforcement_learning import train
from user_input import select_symbol, select_first_player, select_next_cell

confirmation_answers = ('y', 'yes')


def main():
    state_values_x, state_values_o = load_trained_state_values()
    train_ai = input("Do you want to run AI train (y/n)? ")
    if train_ai.lower() in confirmation_answers:
        state_values_x, state_values_o = train(state_values_x, state_values_o,
                                               num_iterations=20000)
        save_state_values(state_values_x, state_values_o)

    # Computer vs Human
    play_game = input("Do you want to play a game (y/n)? ")
    while play_game in confirmation_answers:
        human_symbol = select_symbol()
        computer_symbol = list(
            filter(lambda s: (s != human_symbol), players))[0]
        state_values = state_values_x
        if computer_symbol == 'O':
            state_values = state_values_o
        board = Board()
        is_running = True
        computer = AIPlayer(computer_symbol, state_values, epsilon=0)
        current_player = select_first_player(human_symbol, computer_symbol)
        first_round = True
        print('Let the game begin')
        while is_running:
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
                computer.update_state_value(curr_state_idx, new_state_idx)
                current_player = PlayerChoices.HUMAN
            else:
                print("Wrong choice")
                break

            board.print()

            is_running = not is_game_over(board.state)

            if not is_running:
                winner = get_winner(board.state)
                if winner:
                    print(f"{winner} won!")
                    continue
                print("Draw!")
                continue

        play_game = input("Do you want to play one more game (y/n)? ")

    print('See you!')
    save_state_values(state_values_x, state_values_o)


if __name__ == '__main__':
    main()
