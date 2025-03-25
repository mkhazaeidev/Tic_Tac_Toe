
# Tic-Tac-Toe Game with Python

This is an educational project developed for introductory Python training, focusing on working with functions and structured programming. It features proper in-code documentation to help beginners learn both how the code works and how to document it effectively.



## Project scenario

#### Problem Statement:
Create a console-based Tic-Tac-Toe (Doze) game using a functional (structured) programming approach.

#### Scenario Overview:
 • When the program starts, it displays a menu.
 • The user can choose between:
 • Single-player mode (against the computer)
 • Two-player mode (against a friend)
 • In single-player mode:
 • The player enters their name and the number of rounds.
 • The program randomly selects who starts first (player or computer).
 • From the 5th move onward, the program can detect if the remaining moves are ineffective (i.e., game will result in a draw) and immediately move to the next round.
 • In two-player mode:
 • Both players enter their names.
 • The starting player is randomly chosen.
 • The game continues until one player reaches the specified number of wins.
 • At the end of each match, the program asks if the user wants to play again. If not, the program exits.

## How to Run the Code

#### 1.	Clone the Repository
Make sure you have Git installed. Then open your terminal, navigate to your desired directory, and run:

```bash
  git clone https://github.com/mkhazaeidev/Tic_Tac_Toe.git
```

#### 2.	Create and Activate a Virtual Environment
It’s recommended to use a virtual environment to avoid conflicts with system-wide packages.

For Linux and macOS:
```bash
  cd Tic_Tac_Toe/
  python3 -m venv .venv
  source .venv/bin/activate
```

For Windows:
```CMD
  cd Tic_Tac_Toe/
  py -m venv .venv
  .venv\Scripts\activate
```

#### 3.	Run the Game
With the virtual environment activated, run the game using:

For Linux and macOS:
```bash
  python main.py
```

For Windows:
```CMD
  py main.py
```

#### Enjoy the Game!

Feel free to explore the code, modify it, and learn from it. Whether you’re a beginner or just refreshing your Python skills, this project is a great starting point.

## License
This project is open-source and available under the MIT License (or whichever license you apply).
[MIT](https://choosealicense.com/licenses/mit/)
