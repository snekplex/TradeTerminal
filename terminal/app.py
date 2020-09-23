import uuid
from cmd import Cmd
from data.yahoo import get_ticker_current_price
from database.account import Account
from database.connect import session

class TradeTermial(Cmd):

    prompt = '> '

    def __init__(self, completekey, stdin, stdout):
        super().__init__(completekey, stdin, stdout)

        self.current_account = None

    def do_account(self, args) -> None:
        try:
            command, param = args.rsplit(' ', 1)
            if command.lower() == 'switch':
                account_name = input('Enter account name: ')
                account = session.query(Account).filter_by(name=account_name).first()
                if not account:
                    print('Account not found. Please try another account.')
                    return
                
                self.current_account = account.serialize
                print('Account switched to => {}'.format(self.current_account['name']))
        except ValueError:
            print('Please enter valid command and/or necessary params')
            return

    def do_create(self, args) -> None:
        try:
            command, param = args.rsplit(' ', 1)
                
            if command.lower() == 'account':
                new_account = Account(uuid=str(uuid.uuid4()), name=param)
                session.add(new_account)
                session.commit()
                print('Account {} created'.format(param))

        except ValueError:
            print('Please enter valid command and/or necessary params')


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
            'account': 'Used to manage user accounts',
            'create': 'Used to create accounts',
            'price': 'Displays the current price of a ticker'
        }

        if not command:
            for key, val in commands.items():
                print('{} : {}'.format(key, val))

        if command.lower() in commands:
            print('{} : {}'.format(command, commands[command]))


    def do_exit(self, args) -> None:
        raise SystemExit()
