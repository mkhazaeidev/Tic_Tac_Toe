import os
import random
import time


# ANSI color codes
YELLOW = "\033[93m"
BLUE = "\033[94m"
GREEN = "\033[92m"
RESET = "\033[0m"


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_board(board: list, scores: dict, turn_result: str = "", highlight_cells: list = []) -> None:
    """Display the scoreboard and game board with colors.

    Args:
        board (list): The main board of the game.
        scores (dict): Scores earned by each user.
        turn_result (str, optional): A message to display the game result. Defaults to "".
        highlight_cells (list, optional): Highlighted cells. Defaults to [].
    """
    clear_screen()
    player1, player2 = list(scores.keys())

    score_text = f"🏆 Scoreboard: {YELLOW}{player1} : {scores[player1]}{RESET} | {BLUE}{player2} : {scores[player2]}{RESET} 🏆"

    print("\n" + score_text + "\n")

    if turn_result:
        print(f"🎉 {turn_result} 🎉\n")

    for i, row in enumerate(board):
        row_display = []
        for j, cell in enumerate(row):
            if (i, j) in highlight_cells:
                # Highlight winning moves in green
                row_display.append(GREEN + cell + RESET)
            elif cell == "X":
                row_display.append(YELLOW + cell + RESET)
            elif cell == "O":
                row_display.append(BLUE + cell + RESET)
            else:
                row_display.append(cell)
        print(" | ".join(row_display))
        print("-" * 9)


def check_winner(board: list, player: str) -> bool:
    """Check if the given player has won.

    Args:
        board (list): The main board of the game.
        player (str): Player's symbol.

    Returns:
        bool: Return True if the given player has won.
    """
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


def is_full(board: list) -> bool:
    """Check if the board is completely filled.

    Args:
        board (list): The main board of the game.

    Returns:
        bool: Return True if the board is completely filled.
    """
    return all(board[i][j] in ["X", "O"] for i in range(3) for j in range(3))


def get_available_moves(board: list) -> list:
    """Return a list of available moves.

    Args:
        board (list): The main board of the game.

    Returns:
        list: A list of available moves.
    """
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] not in ["X", "O"]]


def is_draw_situation(board: list, computer_symbol: str, player_symbol: str) -> bool:
    """Check if all possible moves lead to a draw.

    Args:
        board (list): The main board of the game.
        computer_symbol (str): Computer game symbol.
        player_symbol (str): Player game symbol.

    Returns:
        bool: Return True if all possible moves lead to a draw.
    """
    for row, column in get_available_moves(board):
        board[row][column] = computer_symbol
        if check_winner(board, computer_symbol):
            board[row][column] = str(row * 3 + column + 1)
            return False
        board[row][column] = player_symbol
        if check_winner(board, player_symbol):
            board[row][column] = str(row * 3 + column + 1)
            return False
        # Reset to original value
        board[row][column] = str(row * 3 + column + 1)

    return True  # No winning move exists for either player


def minimax(board: list, depth: int, is_maximizing: bool, computer_symbol: str, player_symbol: str) -> int:
    """Minimax algorithm to determine the best move for the computer.

    Args:
        board (list): The main board of the game.
        depth (int): Current level of return in the game tree.
        is_maximizing (bool): When is_maximizing is True, the algorithm is in a state where it is trying to find the best possible move for the maximizing player.
        computer_symbol (str): Computer game symbol.
        player_symbol (str): Player game symbol.

    Returns:
        int: return a value of a game state.
    """
    if check_winner(board, computer_symbol):
        return 10 - depth
    if check_winner(board, player_symbol):
        return depth - 10
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for row, column in get_available_moves(board):
            board[row][column] = computer_symbol
            score = minimax(board, depth + 1, False,
                            computer_symbol, player_symbol)
            board[row][column] = str(row * 3 + column + 1)
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for row, column in get_available_moves(board):
            board[row][column] = player_symbol
            score = minimax(board, depth + 1, True,
                            computer_symbol, player_symbol)
            board[row][column] = str(row * 3 + column + 1)
            best_score = min(score, best_score)
        return best_score


def best_computer_move(board: list, computer_symbol: list, player_symbol: list, first_move: bool = False) -> str:
    """Find the best move for the computer using Minimax algorithm.

    Args:
        board (list): The main board of the game.
        computer_symbol (list): Computer game symbol.
        player_symbol (list): Player game symbol.
        first_move (bool, optional): It should be True if it is the first move of the game. Defaults to False.

    Returns:
        str: Returns the computer's selected option.
    """
    available_moves = get_available_moves(board)

    if len(available_moves) == 9:
        return random.choice(available_moves)

    best_moves = []
    best_score = -float("inf")
    for row, column in available_moves:
        board[row][column] = computer_symbol
        score = minimax(board, 0, False, computer_symbol, player_symbol)
        board[row][column] = str(row * 3 + column + 1)

        if score > best_score:
            best_score = score
            best_moves = [(row, column)]
        elif score == best_score:
            best_moves.append((row, column))

    if first_move and len(best_moves) > 1:
        return random.choice(best_moves[:3])

    return best_moves[0]


def play_turn(
    player1: str,
    player2: str,
    symbols: dict,
    scores: dict,
    single_player: bool = False,
    starting_player: str = None
) -> str | None:
    """Play one turn of the game.

    Args:
        player1 (str): First player's name.
        player2 (str): Second player's name.
        symbols (dict): List of user symbols.
        scores (dict): Scores earned by each user.
        single_player (bool, optional): Game mode. Defaults to False.
        starting_player (str, optional): Name of the player who started the game. Defaults to None.

    Returns:
        str | None: If a user wins, it returns the user's name, and if there is a tie, it returns None.
    """
    board = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]

    if starting_player is None:
        current_player = player1
    else:
        current_player = starting_player

    print_board(board, scores)
    moves_count = 0

    while True:
        symbol = symbols[current_player]

        if single_player and current_player == "Computer":
            print("Computer is thinking...")
            time.sleep(1 if moves_count > 0 else 0.5)
            row, column = best_computer_move(
                board, symbols["Computer"],
                symbols[player1],
                first_move=(moves_count == 0)
            )
        else:
            while True:
                choice = input(
                    f"{current_player}, it's your turn. Choose a number (1-9): ")
                if not choice.isdigit() or choice not in "123456789":
                    print("Invalid input! Please enter a number between 1 and 9.")
                    continue

                row, column = divmod(int(choice) - 1, 3)
                if board[row][column] in ["X", "O"]:
                    print("This cell is already occupied. Try another.")
                    continue
                break

        board[row][column] = symbol
        print_board(board, scores)
        moves_count += 1

        if check_winner(board, symbol):
            scores[current_player] += 1
            print_board(board, scores, f"{current_player} wins this turn!")
            time.sleep(5)
            return current_player

        if moves_count >= 5 and is_draw_situation(board, symbols[player2], symbols[player1]):
            print_board(board, scores,
                        "It's a draw! No one can win this turn.")
            time.sleep(5)
            return None

        if is_full(board):
            print_board(board, scores, "It's a tie! No one wins this turn.")
            time.sleep(5)
            return None

        current_player = player1 if current_player == player2 else player2


def get_name(prompt: str = "Name: ", length: int = 3, empty: bool = False) -> str:
    """A function to get a name from standard input.

    Args:
        prompt (str, optional): The message displayed to the user. Defaults to "Name: ".
        length (int, optional): Minimum length of the entered name. Defaults to 4.
        empty (bool, optional): If True, the user can enter an empty value. Defaults to False.

    Returns:
        str: Validated name.
    """
    while True:
        name = input(prompt)
        if name:
            if name.isalpha() and len(name) >= length:
                return name
            else:
                print(
                    "ERROR: The name must be at least {length} characters and contain only alphabets.")
        else:
            print("ERROR: Name cannot be empty.")


def get_players(single_player: bool = False) -> list:
    """Depending on the game mode, it takes the names of one or two users from the input.

    Args:
        single_player (bool, optional): If true, it will only get one user.. Defaults to False.

    Returns:
        list: A list of user names.
    """
    if single_player:
        player1 = get_name("Enter your name: ")
        player2 = "Computer"
    else:
        player1 = get_name("Enter name for Player 1: ")
        player2 = get_name("Enter name for Player 2: ")

    return list((player1, player2))


def get_turns(prompt: str = "Enter number of turns: ") -> int:
    """This function takes the number of turns in the game from the user and returns the entered value as an integer if the user enters a valid integer.

    Args:
        prompt (str, optional): The message that is displayed to the user. Defaults to "Enter number of turns: ".

    Returns:
        int: Number of game turns.
    """
    while True:
        turns = input("Enter number of turns: ")
        try:
            return int(turns)
        except:
            print("ERROR: The number of turns in the game must be an integer.")


def game_loop(single_player: bool = False) -> None:
    """Main game loop that handles multiple turns.

    Args:
        single_player (bool, optional): _description_. Defaults to False.
    """
    players = get_players(single_player)
    random.shuffle(players)
    player1, player2 = players

    turns = get_turns()

    player_symbols = {player1: random.choice(["X", "O"])}
    player_symbols[player2] = "O" if player_symbols[player1] == "X" else "X"

    scores = {player1: 0, player2: 0}
    starting_player = player1

    while max(scores.values()) < turns:
        winner = play_turn(player1, player2, player_symbols,
                           scores, single_player, starting_player)

        if winner:
            starting_player = winner


def show_menu() -> None:
    """A function to display the main menu."""
    print("🎮 Welcome to Tic-Tac-Toe! 🎮")
    print("1. Single Player (vs Computer)")
    print("2. Two Players")
    print("3. Exit")


def main() -> None:
    """
    The program execution starts from this function.
    In this function, the main menu is called and, depending on the user's choice,
    the game enters one of two modes: single-player or two-player.
    """
    error = False
    while True:
        clear_screen()
        show_menu()

        if error:
            print("ERROR: Please select a correct option.")
        choice = input("Select an option (1/2/3): ")

        match choice:
            case "1":
                game_loop(single_player=True)
            case "2":
                game_loop(single_player=False)
            case "3":
                break
            case _:
                error = True


if __name__ == "__main__":
    main()
