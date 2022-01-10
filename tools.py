import numpy as np

from common import players, input_board_state, n_states, states_dict


def is_player_winner(board, player_symbol):
    return ((board[0][0] == board[0][1] == board[0][2] == player_symbol) or
            (board[1][0] == board[1][1] == board[1][2] == player_symbol) or
            (board[2][0] == board[2][1] == board[2][2] == player_symbol) or
            (board[0][0] == board[1][0] == board[2][0] == player_symbol) or
            (board[0][1] == board[1][1] == board[2][1] == player_symbol) or
            (board[0][2] == board[1][2] == board[2][2] == player_symbol) or
            (board[0][0] == board[1][1] == board[2][2] == player_symbol) or
            (board[0][2] == board[1][1] == board[2][0] == player_symbol))


def get_winner(board_state):
    for player in players:
        if is_player_winner(board_state, player):
            return player

    return None


def is_game_over(board_state):
    """ Returns True if game is over else returns false """

    winner = get_winner(board_state)
    # Game won by either player
    if winner:
        return True
    # Board full game is Draw
    if ' ' not in np.array(board_state).flatten():
        return True
    return False


def board_print(board):
    print(f"\n{'|'.join(board[0])}\n{'+'.join('-' * 3)}\n"
          f"{'|'.join(board[1])}\n{'+'.join('-' * 3)}\n{'|'.join(board[2])}\n")


def input_board_print():
    board_print(input_board_state)


def save_state_values(state_values_for_ai_x, state_values_for_ai_o):
    # Save state values for future use
    np.savetxt('trained_state_values_x.txt', state_values_for_ai_x, fmt='%.6f')
    np.savetxt('trained_state_values_o.txt', state_values_for_ai_o, fmt='%.6f')


def generate_initial_data():
    # Initialize state values
    state_values_x = np.full(n_states, 0.0)
    state_values_o = np.full(n_states, 0.0)
    for i in range(n_states):
        winner = get_winner(states_dict[i])
        if winner == 'X':
            state_values_x[i] = 1
            state_values_o[i] = -1
        elif winner == 'O':
            state_values_x[i] = -1
            state_values_o[i] = 1

    save_state_values(state_values_x, state_values_o)

    return state_values_x, state_values_o


def load_trained_state_values():
    # Load trained state values
    try:
        state_values_x = np.loadtxt('trained_state_values_x.txt',
                                    dtype=np.float64)
        state_values_o = np.loadtxt('trained_state_values_o.txt',
                                    dtype=np.float64)
    except FileNotFoundError:
        # If files are missing generate new initial ones
        return generate_initial_data()

    return state_values_x, state_values_o
