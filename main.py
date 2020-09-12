from pyfiglet import Figlet
from terminal.app import TradeTermial

if __name__ == '__main__':
    f = Figlet(font='slant')
    print(f.renderText('TradeTerminal'))
    app = TradeTermial()
    app.cmdloop('Welcome to the TradeTerminal. Enter a command into the prompt.')
    