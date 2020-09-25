from pyfiglet import Figlet
from terminal.app import TradeTermial
from database.connect import session

if __name__ == '__main__':
    f = Figlet(font='slant')
    print(f.renderText('TradeTerminal'))
    app = TradeTermial(completekey='tab', stdin=None, stdout=None)
    app.cmdloop('''Welcome to the TradeTerminal. Enter a command into the prompt.\nIf a new user, enter the command newuser to get started''')
    