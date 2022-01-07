import numpy as np

from common import players


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
