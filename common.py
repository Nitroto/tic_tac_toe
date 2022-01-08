import itertools
from enum import Enum

empty_board_state = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
input_board_state = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
players = ('X', 'O')
possible_symbols = (*players, ' ')

n_actions = 9
all_possible_states = [[list(i[0:3]), list(i[3:6]), list(i[6:10])] for i in
                       itertools.product(possible_symbols, repeat=n_actions)]
states_dict = {index: x for index, x in enumerate(all_possible_states)}
n_states = len(all_possible_states)


class PlayerChoices(Enum):
    HUMAN = 0
    COMPUTER = 1
