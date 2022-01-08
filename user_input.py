from common import players, PlayerChoices


def select_symbol():
    selected_symbol = input("Select your symbol (X or O): ").upper()
    if selected_symbol not in players:
        print("Selected symbol is not correct ")
        return select_symbol()
    return selected_symbol


def select_first_player(human_symbol, computer_symbol):
    player_choice = input(f"Choose which player goes first\n"
                          f"{human_symbol} - You\n"
                          f"{computer_symbol} - Computer").upper()

    if player_choice == human_symbol:
        return PlayerChoices.HUMAN

    if player_choice == computer_symbol:
        return PlayerChoices.COMPUTER

    print("Wrong choice!")
    return select_first_player(human_symbol, computer_symbol)


def select_next_cell(board):
    empty_cells = board.get_empty_cells()
    cell_choice = int(input(f"Choose where to place {empty_cells}: "))

    if cell_choice not in empty_cells:
        print("Wrong selection!")
        return select_next_cell(board)

    return cell_choice
