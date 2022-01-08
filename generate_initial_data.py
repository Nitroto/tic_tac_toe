import numpy as np

from common import n_states, states_dict
from tools import get_winner


def generate_initial_data():
    # Initialize state values
    state_values_for_ai_o = np.full(n_states, 0.0)
    state_values_for_ai_x = np.full(n_states, 0.0)
    for i in range(n_states):
        winner = get_winner(states_dict[i])
        if winner == 'O':  # AI won
            state_values_for_ai_o[i] = 1
            state_values_for_ai_x[i] = -1
        elif winner == 'X':  # AI lost
            state_values_for_ai_o[i] = -1
            state_values_for_ai_x[i] = 1

    # Save state values for future use
    np.savetxt('trained_state_values_X.txt', state_values_for_ai_x, fmt='%.6f')
    np.savetxt('trained_state_values_O.txt', state_values_for_ai_o, fmt='%.6f')

    return state_values_for_ai_x, state_values_for_ai_o
