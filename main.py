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


def print_board(board, scores, turn_result="", highlight_cells=[]):
    """Display the scoreboard and game board with colors."""
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


def check_winner(board, player):
    """Check if the given player has won."""
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


def is_full(board):
    """Check if the board is completely filled."""
    return all(board[i][j] in ["X", "O"] for i in range(3) for j in range(3))


def get_available_moves(board):
    """Return a list of available moves."""
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] not in ["X", "O"]]


def is_draw_situation(board, computer_symbol, player_symbol):
    """Check if all possible moves lead to a draw."""
    for row, col in get_available_moves(board):
        board[row][col] = computer_symbol
        if check_winner(board, computer_symbol):
            board[row][col] = str(row * 3 + col + 1)
            return False
        board[row][col] = player_symbol
        if check_winner(board, player_symbol):
            board[row][col] = str(row * 3 + col + 1)
            return False
        board[row][col] = str(row * 3 + col + 1)  # Reset to original value

    return True  # No winning move exists for either player


def minimax(board, depth, is_maximizing, computer_symbol, player_symbol):
    """Minimax algorithm to determine the best move for the computer."""
    if check_winner(board, computer_symbol):
        return 10 - depth
    if check_winner(board, player_symbol):
        return depth - 10
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for row, col in get_available_moves(board):
            board[row][col] = computer_symbol
            score = minimax(board, depth + 1, False,
                            computer_symbol, player_symbol)
            board[row][col] = str(row * 3 + col + 1)
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for row, col in get_available_moves(board):
            board[row][col] = player_symbol
            score = minimax(board, depth + 1, True,
                            computer_symbol, player_symbol)
            board[row][col] = str(row * 3 + col + 1)
            best_score = min(score, best_score)
        return best_score


def best_computer_move(board, computer_symbol, player_symbol, first_move=False):
    """Find the best move for the computer using Minimax algorithm."""
    available_moves = get_available_moves(board)

    if len(available_moves) == 9:
        return random.choice(available_moves)

    best_moves = []
    best_score = -float("inf")
    for row, col in available_moves:
        board[row][col] = computer_symbol
        score = minimax(board, 0, False, computer_symbol, player_symbol)
        board[row][col] = str(row * 3 + col + 1)

        if score > best_score:
            best_score = score
            best_moves = [(row, col)]
        elif score == best_score:
            best_moves.append((row, col))

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
        player1 (str): _description_
        player2 (str): _description_
        symbols (dict): _description_
        scores (dict): _description_
        single_player (bool, optional): _description_. Defaults to False.
        starting_player (str, optional): _description_. Defaults to None.

    Returns:
        str | None: _description_
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
            time.sleep(2)
            return current_player

        if moves_count >= 5 and is_draw_situation(board, symbols[player2], symbols[player1]):
            print_board(board, scores,
                        "It's a draw! No one can win this turn.")
            time.sleep(2)
            return None

        if is_full(board):
            print_board(board, scores, "It's a tie! No one wins this turn.")
            time.sleep(2)
            return None

        current_player = player1 if current_player == player2 else player2


def get_players(single_player: bool = False) -> list:
    """_summary_

    Args:
        single_player (bool, optional): _description_. Defaults to False.

    Returns:
        list: _description_
    """
    if single_player:
        player1 = input("Enter your name: ")
        player2 = "Computer"
    else:
        player1 = input("Enter name for Player 1: ")
        player2 = input("Enter name for Player 2: ")

    return list((player1, player2))


def get_turns(prompt: str = "Enter number of turns: ") -> int:
    """_summary_

    Args:
        prompt (_type_, optional): _description_. Defaults to "Enter number of turns: ".

    Returns:
        int: _description_
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
