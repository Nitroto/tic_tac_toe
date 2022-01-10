import copy
import random

import numpy as np

from common import empty_board_state, states_dict, EPSILON, LEARNING_RATE


class Board:
    def __init__(self):
        self.state = copy.deepcopy(empty_board_state)

    def play_move(self, player_symbol, cell_num):
        row = int((cell_num - 1) / 3)
        col = (cell_num - 1) % 3

        if self.state[row][col] == ' ':
            self.state[row][col] = player_symbol
            return

        cell_num = int(input("Cell is not empty! Choose again: "))
        self.play_move(player_symbol, cell_num)

    def get_empty_cells(self):
        flat_array = np.array(self.state).flatten()
        empty_cells = []
        for i in range(len(flat_array)):
            if flat_array[i] == ' ':
                empty_cells.append(i + 1)
        return empty_cells

    def print(self):
        """ Displays board in proper format"""

        from tools import board_print
        board_print(self.state)


class AIPlayer:
    """ Provides all the methods that a AIPlayer must execute. """

    def __init__(self, symbol, trained_state_values, epsilon=EPSILON,
                 learning_rate=LEARNING_RATE):
        self.symbol = symbol
        self.trained_state_values = trained_state_values
        self.epsilon = epsilon
        self.current_epsilon = epsilon
        self.learning_rate = learning_rate

    def get_best_move(self, board):
        """ Reinforcement Learning Algorithm """

        moves = []
        curr_state_values = []
        empty_cells = board.get_empty_cells()

        for empty_cell in empty_cells:
            moves.append(empty_cell)
            new_state = copy.deepcopy(board.state)
            self._generate_possible_move(new_state, empty_cell)
            next_state_idx = list(states_dict.keys())[
                list(states_dict.values()).index(new_state)]

            curr_state_values.append(self.trained_state_values[next_state_idx])

        print(f'Possible moves: {moves}')
        print(f'Move values {curr_state_values}')
        best_move_idx = np.argmax(curr_state_values)

        best_move = moves[best_move_idx]
        if self.epsilon:
            if np.random.uniform(0, 1) <= self.current_epsilon:
                self.current_epsilon *= 0.99
                return random.choice(empty_cells)
            self.current_epsilon = self.epsilon

        return best_move

    def update_state_value(self, curr_state_idx, next_state_idx):
        new_value = self.trained_state_values[curr_state_idx] + \
                    self.learning_rate * \
                    (self.trained_state_values[next_state_idx] -
                     self.trained_state_values[curr_state_idx])
        self.trained_state_values[curr_state_idx] = new_value

    def _generate_possible_move(self, board_state, cell_num):
        row = int((cell_num - 1) / 3)
        col = (cell_num - 1) % 3

        if board_state[row][col] == ' ':
            board_state[row][col] = self.symbol
