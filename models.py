import copy
import random

import numpy as np

from common import empty_board_state, states_dict


class Board:
    def __init__(self):
        self.state = copy.deepcopy(empty_board_state)

    def play_move(self, player_symbol, block_num):
        x_coordinate = (block_num - 1) % 3
        y_coordinate = int((block_num - 1) / 3)

        if self.state[y_coordinate][x_coordinate] == ' ':
            self.state[y_coordinate][x_coordinate] = player_symbol
            return

        block_num = int(input("Block is not empty! Choose again: "))
        self.play_move(player_symbol, block_num)

    def print(self):
        """ Displays board in proper format"""

        from tools import board_print
        board_print(self.state)


class AIPlayer:
    """ Provides all the methods that a AIPlayer must execute. """

    def __init__(self, symbol, state_values_for_ai, epsilon=0.2):
        self.symbol = symbol
        self.state_values_for_ai = state_values_for_ai
        self.epsilon = epsilon

    def get_empty_cells(self, board_state):
        flat_array = np.array(board_state).flatten()
        empty_cells = []
        for i in range(len(flat_array)):
            if flat_array[i] == ' ':
                empty_cells.append(i + 1)
        return empty_cells

    def get_best_move(self, board_state):
        """ Reinforcement Learning Algorithm """

        moves = []
        curr_state_values = []
        empty_cells = self.get_empty_cells(board_state)

        for empty_cell in empty_cells:
            moves.append(empty_cell)
            new_state = copy.deepcopy(board_state)
            self._play_move(new_state, empty_cell)
            next_state_idx = list(states_dict.keys())[
                list(states_dict.values()).index(new_state)]

            curr_state_values.append(self.state_values_for_ai[next_state_idx])

        best_move_idx = np.argmax(curr_state_values)

        best_move = moves[best_move_idx]
        if np.random.uniform(0, 1) <= self.epsilon:
            self.epsilon *= 0.99
            return random.choice(empty_cells)

        return best_move

    def update_state_value(self, curr_state_idx, next_state_idx,
                           learning_rate):
        new_value = self.state_values_for_ai[curr_state_idx] + \
                    learning_rate * (self.state_values_for_ai[next_state_idx] -
                                     self.state_values_for_ai[curr_state_idx])
        self.state_values_for_ai[curr_state_idx] = new_value

    def _play_move(self, board_state, block_num):
        x_coordinate = (block_num - 1) % 3
        y_coordinate = int((block_num - 1) / 3)
        if board_state[y_coordinate][x_coordinate] == ' ':
            board_state[y_coordinate][x_coordinate] = self.symbol
