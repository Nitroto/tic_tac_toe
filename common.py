import itertools

empty_board_state = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
players = ('X', 'O')
possible_symbols = (*players, ' ')

n_actions = 9
all_possible_states = [[list(i[0:3]), list(i[3:6]), list(i[6:10])] for i in
                       itertools.product(possible_symbols, repeat=n_actions)]
states_dict = {index: x for index, x in enumerate(all_possible_states)}
n_states = len(all_possible_states)
