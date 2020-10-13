import uuid
import sqlalchemy
from cmd import Cmd
from PyInquirer import prompt, Separator
from getpass import getpass
from data.yahoo import get_ticker_current_price
from database.account import Account
from database.user import User
from database.position import Position
from database.connect import session

class TradeTermial(Cmd):

    def __init__(self, completekey, stdin, stdout):
        super().__init__(completekey, stdin, stdout)

        # Overridng inherited self.prompt variable
        self.prompt = '> '
        
        self.user = None
        self.current_account = None

    # Creates new users for the terminal
    def do_newuser(self, args) -> None:

        def create_user_loop() -> bool:
            username = input('Enter username: ')
            if username.strip() == 'exit':
                return False
            
            user_exists = session.query(User).filter_by(username=username).first()
            
            if user_exists:
                print('Username => {} taken. Please select another.'.format(username))
                create_user_loop()
            
            password = getpass('Enter password: ')
            password_confirm = getpass('Confirm password: ')
            
            if password != password_confirm:
                print('Passwords did not match. Restarting newuser process')
                create_user_loop()

            user = User(uuid=str(uuid.uuid4()), username=username, password=password)
            session.add(user)
            session.commit()
            
            
            account = Account(uuid=str(uuid.uuid4()), name='default', user_id=user.id)
            session.add(account)
            session.commit()

            user.active_account_id = account.id
            session.commit()
            

            print('User {} created'.format(username))

            self.user = user.serialize
            self.current_account = account.serialize

            self.prompt = '{}@{} > '.format(user.username, account.name)

            return True

        try:
            created_user = False
            print('Creating new user')
            while not created_user:
                created = create_user_loop()
                if created:
                    created_user = True
                    break
                if created == False:
                    return
                
        except ValueError:
            print('Please enter valid command and/or necessary params')
            return

    # Logs in existing user
    def do_login(self, args):

        def login_loop() -> bool:
            username = input('Enter username: ')
            
            if username.strip() == 'exit':
                return False
            
            user = session.query(User).filter_by(username=username).first()

            if user:
                password = getpass('Enter password: ')
                password_match = user.verify_password(password)
                if password_match:
                    self.user = user.serialize
                    active_account = session.query(Account).filter_by(user_id=user.id, id=user.active_account_id).first()
                    self.current_account = active_account.serialize
                    print('Logged in as {}'.format(user.username))
                    self.prompt = '{}@{} > '.format(user.username, active_account.name)
                else:
                    print('Password failed. Retry login.')
                    login_loop()
            else:
                print('User with username, {} not found. Please try agin.'.format(username))
                login_loop()

        try:
            logged_in_user = False
            while not logged_in_user:
                logged_in = login_loop()

                if logged_in:
                    logged_in_user = True
                    break
                if logged_in_user == False:
                    return

        except ValueError:
            print('Please enter valid command and/or necessary params')
            return

    # Logs out currently logged in user
    def do_logout(self, args) -> None:
        try:

            if not self.user:
                print('No user logged in.')
                return

            print('Logging out')
            self.user = None
            self.current_account = None
            self.prompt = '> '
        except ValueError:
            print('Please enter valid command and/or necessary params')
            return

    
    # Used to manage and create accounts
    def do_account(self, args) -> None:
        try:

            command = args
            
            if not self.user:
                print('Please login to a user to connect account to')
                return
            
            if command.lower() == 'create':
                account_name = input('Enter new account name: ')
                new_account = Account(uuid=str(uuid.uuid4()), name=account_name, user_id=self.user['id'])
                session.add(new_account)
                session.commit()

                current_user = session.query(User).filter_by(id=self.user['id']).first()
                current_user.active_account_id = new_account.id
                session.commit()

                self.user = current_user.serialize
                self.current_account = new_account.serialize
                print('Account {} created'.format(account_name))
                self.prompt = '{}@{} > '.format(self.user['username'], self.current_account['name'])

            elif command.lower() == 'switch':
                account_name = input('Enter account name: ')
                account = session.query(Account).filter_by(name=account_name, user_id=self.user['id']).first()
                if not account:
                    print('Account not found. Please try another account.')
                    return
                
                user = session.query(User).filter_by(id=self.user['id']).first()
                user.active_account_id = account.id
                self.user = user.serialize
                self.current_account = account.serialize
                session.commit()

                print('Account switched to => {}'.format(self.current_account['name']))
                self.prompt = '{}@{} > '.format(self.user['username'], self.current_account['name'])

            elif command.lower() == 'showall':
                accounts = session.query(Account).filter_by(user_id=self.user['id']).all()
                print(accounts)
            
            elif command.lower() == 'current':
                print(self.current_account)

            else:
                print('Please enter a valid command input.')
            
        except ValueError:
            print('Please enter valid command and/or necessary params')
            return

    # Used to display info on user positions
    def do_positions(self, command: str) -> None:
        try:
            if command.strip() == 'current':
                print('========== {} =========='.format(self.current_account['name']))
                current_acct_positions = session.query(Position).filter_by(account_id=self.current_account['id']).all()
                print(current_acct_positions)
            
            else:
                print('Please enter a valid command input.')
            

        except ValueError:
            print('Please enter valid command and/or necessary params')
            return

    # Prints the current price of the inputted ticker
    def do_price(self, ticker: str) -> None:

        if not self.user:
            print('Please login/create a user')
            return

        price = None

        if ticker == '' or ticker == None:
            print('Please provide a valid ticker')
            return

        try:
            price = get_ticker_current_price(ticker)
        except AssertionError:
            # Handle if ticker is not found or does not exist
            print('Ticker {} not found'.format(ticker))
    
        if price:
            print('{} => ${}'.format(ticker.upper(), price))

    # Used to buy stock and create positions
    def do_buy(self, args) -> None:
        try:

            if not self.user:
                print('Please login/create a user')
                return

            ticker = input('Enter ticker: ').strip()
            current_price = get_ticker_current_price(ticker)
            shares = input('Enter how many shares at ${} per share: '.format(current_price))
            transaction_total = float('{:2f}'.format(current_price * int(shares)))
            
            order = {'ticker': ticker, 'shares': shares, 'total': transaction_total}
            if self.current_account['balance'] < transaction_total:
                print('Insufficent funds in acccount for order.')
                print('Order: ', order)
                return
            
            if self.current_account['balance'] >= transaction_total:
                print('Current order => ', order)
                confirm_order = input(r'Confirm order(y/n): ').strip().lower()
                if confirm_order == 'y':
                    current_account = session.query(Account).filter_by(name=self.current_account['name'],
                                                                       user_id=self.user['id']).first()
                    allowed_trade = current_account.remove_from_balance(transaction_total)
                    if not allowed_trade:
                        print('Insufficent funds in acccount for order.')
                        print('Order: ', order)
                        return

                    new_balance = float('{:2f}'.format(current_account.balance - transaction_total))
                    current_account.balance = new_balance

                    new_position = Position(account_id=self.current_account['id'], buy_price=current_price,
                                            ticker=ticker.upper(), shares=int(shares))
                    
                    session.add(new_position)
                    session.commit()

                    self.current_account = current_account.serialize
                    print('Order confirmed. Stock bought.')
                    print('New account balance => ${}'.format(new_balance))

                elif confirm_order == 'n':
                    print('Order cancelled. Returning to terminal.')
                else:
                    print('Invalid input. Cancelling order and returning to terminal.')
                    return


        except AssertionError:
            # Handle if ticker is not found or does not exist
            print('Ticker {} not found'.format(ticker))

        except ValueError:
            print('Please enter valid command and/or necessary params')
            return

    # Used to sell any currently help positions in account
    def do_sell(self, args) -> None:
        try:
            if not self.user:
                print('Please login/create a user')
                return

            open_positions = session.query(Position).filter_by(account_id=self.current_account['id']).all()

            if not open_positions:
                print('No positions currently in account. To use, buy shares of a stock.')
                return

            formatted_positions = [position.serialize for position in open_positions]
            position_dict = {}

            # Potential collision with positions with the same 'name'
            # Causes bug to select both, thus duplicate number is added.
            duplicate_num = 0
            position_tickers = set()

            for position in formatted_positions:
                if position['ticker'] in position_tickers:
                    duplicate_num += 1
                else:
                    position_tickers.add(position['ticker'])

                # Added duplicate_num is arbitrary. No meaning other then to prevent choice bug.
                position['name'] = '{} | {} shares held @ ${} |'.format(position['ticker'] + '-' + str(duplicate_num), position['shares'],
                                                                        position['buy_price'])
                position_dict[position['ticker'] + '-' + str(duplicate_num)] = position

            formatted_positions.insert(0, Separator('===== Positions ====='))
            formatted_positions.append({ 'name': 'CANCEL' })

            questions = [
                {
                    'type': 'checkbox',
                    'message': 'Select positons to sell',
                    'name': 'positions',
                    'choices': formatted_positions
                }
            ]

            choices = prompt(questions)

            choices = [choice.split()[0] for choice in choices['positions']]

            if choices.count('CANCEL') > 0:
                print('Cancelling sell process')
                return

            setting_sell_amount = True
            while setting_sell_amount:
                
                try:
                    for idx in range(len(choices)):
                        sell_share_amount = int(input('Sell how many of {} shares bought @ ${} of {}: '
                                                .format(position_dict[choices[idx]]['shares'], position_dict[choices[idx]]['buy_price'],
                                                        position_dict[choices[idx]]['ticker'])).strip())

                        position_dict[choices[idx]]['sell_share_amount'] = sell_share_amount
                        if idx == len(choices) - 1:
                            setting_sell_amount =  False
                except:
                    print('Please input valid integer to sell.')

            current_account = session.query(Account).filter_by(id=self.current_account['id']).first()

            # Be carful of potential request limit/denials due to requesting latest price
            for db_position in open_positions:
                for choice in choices:
                    if position_dict[choice]['id'] == db_position.id and position_dict[choice]['sell_share_amount'] > 0:
                        shares_left = db_position.shares - position_dict[choice]['sell_share_amount']
                        if shares_left < 0:
                            print('Unable to sell more shares than owned')
                        else:
                            current_price = get_ticker_current_price(position_dict[choice]['ticker'])
                            gain = (db_position.buy_price * db_position.shares) + (current_price * db_position.shares)
                            current_account.balance = float('{:2f}'.format(current_account.balance + gain))
                            if shares_left >= 1:
                                db_position.shares = shares_left
                            elif shares_left == 0:
                                session.delete(db_position)
            
            self.current_account = current_account.serialize
            session.commit()

            print('New account balance => ${}'.format(self.current_account['balance']))
            return

        except ValueError:
            print('Please enter valid command and/or necessary params')
            return

    # Used to find all available commands and their functions
    def do_help(self, command: str) -> None:
        commands = {
            'exit': {
                'description': 'Exits the terminal and closes the application'
            },
            'newuser': {
                'description': 'Creates a new user'
            },
            'login': {
                'description': 'Login as an existing user'
            },
            'logout': {
                'description': 'When logged in, logs out user'
            },
            'account': {
                'description': 'Used to create and manage user accounts'
            },
            'positions': {
                'description': 'Displays the current positions in an account'
            },
            'price': {
                'description': 'Displays the current price of a ticker'
            },
            'buy': {
                'description': 'Used to buy and create a position for a stock'
            },
            'sell': {
                'description': 'Used to sell current positions'
            }
        }

        if not command:
            for key, val in commands.items():
                print('\t{} : {}'.format(key, val['description']))

        if command.lower() in commands:
            print('{} : {}'.format(command, commands[command]))
        


    def do_exit(self, args) -> None:
        raise SystemExit()
