import numpy as np

from generate_initial_data import generate_initial_data
from models import Board, AIPlayer
from training_reinforcement_learning import train

confirmation_answers = ('y', 'yes')


def main():
    # LOAD TRAINED STATE VALUES
    try:
        state_values_for_ai_x = np.loadtxt('trained_state_values_X.txt',
                                           dtype=np.float64)
        state_values_for_ai_o = np.loadtxt('trained_state_values_O.txt',
                                           dtype=np.float64)
    except FileNotFoundError:
        state_values_for_ai_x, state_values_for_ai_o = generate_initial_data()

    train_ai = input("Do you want to run AI train (y/n)? ")
    if train_ai.lower() in confirmation_answers:
        train(state_values_for_ai_x, state_values_for_ai_o, 10000)

    # Computer vs Human Games
    play_game = input("Do you want to play a game? ")
    while play_game in confirmation_answers:
        select_symbol = input("Select your symbol (X/O): ")
        board = Board()
        game_status_flag = True
        computer = AIPlayer('X', state_values_for_ai_x, 0.1)
        human_symbol = 'O'
        game_history = []

        print('\nLet the game begin\n')
        while game_status_flag:
            board.state = computer.choose_move(board.state, human_symbol)
            print("Computers\'s Turn:\n")
            board.print()
            game_history.append(board.state)
            game_status_flag = not is_game_over(board.state, computer.symbol)
            if not game_status_flag:
                break

            print("Human\'s Turn:\n")
            print('Enter X-coordinate(0-2):')
            x = int(input())
            print('Enter Y-coordinate(0-2):')
            y = int(input())

            board.state[y][x] = 'O'
            board.print()
            game_history.append(board.state)
            game_status_flag = not is_game_over(board.state, human_symbol)

        final_score = 0

        if final_score > 0:
            print(f"Computer wins")
        elif final_score < 0:
            print("Human wins")
        else:
            print("Draw")

        print("Do you want to play another game(y/n)?")
        ans = input()


if __name__ == '__main__':
    main()
