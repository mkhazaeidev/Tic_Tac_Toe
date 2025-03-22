
# Tic-Tac-Toe Game with Python

This is an educational project for introductory Python training and working with functions. The main coding approach in this mini-project is the structured or functional approach.

Proper documentation has been added to the code so that firstly you can learn how to write documentation in the code, and secondly, use it to better understand the written code.




## Project scenario

Problem Statement:
Write a program that implements the game of Doze using a structured approach.

Scenario:
The program starts by displaying a menu to the user(s). The user can play as a single-player against the computer or as a two-player game with a friend.

The user enters the game by selecting the appropriate option. If it is in single-player mode, the program asks for his name and then asks for the number of turns in the game, and then a user is randomly selected as the first user (user or computer). During the game, in each turn, the results obtained are displayed to the users. And from the 5th choice onwards, the program, based on the users' choices, can determine that the next choices are ineffective and the game is going to be a draw. As a result, it immediately enters the next round of the game.

The difference between two-player mode and single-player is that after entering two-player mode, the names of the two users are asked, and the choice is random between the two players.

The game ends when a user's number of wins reaches the number specified as the number of turns. After the winner is announced, the program asks the user if they want to continue. If the user selects yes, the program restarts by displaying the menu, otherwise the program ends.
## Running the code

To run the code, you must first clone the project to your computer. To do this, you must have git version control installed on your computer.

#### Clone project
To clone, first open your terminal, navigate to the desired path, and then enter the following command.

```bash
  git clone https://github.com/mkhazaeidev/Tic_Tac_Toe.git
```

#### Creating a virtual environment
It is better to create a virtual environment in the project path so that your project does not use your system resources to run. To do this, first enter the project folder with the change directory command and enter the command to create the virtual environment and activate it.

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

#### Running main.py
After the virtual environment is activated, simply run the following command to start the game.

For Linux and macOS:
```bash
  python main.py
```

For Windows:
```CMD
  py main.py
```

I hope you enjoy it.

## License

[MIT](https://choosealicense.com/licenses/mit/)
