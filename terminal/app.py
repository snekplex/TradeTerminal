from cmd import Cmd
from data.yahoo import get_ticker_current_price

class TradeTermial(Cmd):

    prompt = '> '

    # Prints the current price of the inputted ticker
    def do_price(self, ticker: str) -> None:
        price = None
        try:
            price = get_ticker_current_price(ticker)
        except AssertionError:
            # Handle if ticker is not found or does not exist
            print('Ticker {} not found'.format(ticker))
    
        if price:
            print('{} => ${}'.format(ticker.upper(), price))

    # Used to find all available commands and their functions
    def do_help(self, command: str) -> None:
        commands = {
            'exit': 'Exits the terminal and closes the application',
            'price': 'Displays the current price of a ticker'
        }

        if not command:
            for key, val in commands.items():
                print('{} : {}'.format(key, val))

        if command.lower() in commands:
            print('{} : {}'.format(command, commands[command]))


    def do_exit(self, args) -> None:
        raise SystemExit()
