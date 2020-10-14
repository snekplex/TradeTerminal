# TradeTerminal
A python3 based CLI that lets users buy and sell stocks at current market prices.

## Installation
1. Have python3 installed on your system. Tested using python 3.8.
2. Run the command `git clone https://github.com/snekplex/TradeTerminal.git` in location of choice
3. Project is downloaded and enjoy.

## Getting Started
To get the app running simply cd into the TradeTerminal directory where cloned and run 
the `main.py` file. Then it is recommended to run the `newuser` commmand as in order
to use most commands a user is required.

## Command Manual
Commands look as follows `<command> <args>`

The format for the manual is as follows:
- *command*
    - *Argument after*

- *help* : Used to display the other commands available in the program.
- *exit* : Used to exit the application safetly and return to the command line.
- *newuser* : Used to create a new user and be logged in as them
- *login* : Used to login an already existing user into the terminal.
- *logout* : Logs out the currently logged in user from the terminal
- *account* : Used to create and manage user accounts
    - *create* : Enters the process of creating a new user
    - *switch* : Swaps user's current account with the one of the name inputted
    - *showall* : Shows all accounts currently owned by the currently logged in user
    - *current* : Displays the current account being used with basic stats
- *positions* : Used to see info on positions in current account
    - *current* : Displays all of the current positions held in the account
- *price*: Displays the current price of the inputted ticker
- *buy* : Used to buy shares of a stock
- *sell* : Used to sell shares of a stock currently held in a position
