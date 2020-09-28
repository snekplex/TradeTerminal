import uuid
import sqlalchemy
from cmd import Cmd
from getpass import getpass
from data.yahoo import get_ticker_current_price
from database.account import Account
from database.user import User
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
                    active_account = session.query(Account).filter_by(user_id=user.active_account_id).first()
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
            print('Logging out')
            self.user = None
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
                
                self.current_account = new_account.serialize
                print('Account {} created'.format(account_name))
                self.prompt = '{}@{} > '.format(self.user['username'], self.current_account['name'])

            elif command.lower() == 'switch':
                account_name = input('Enter account name: ')
                account = session.query(Account).filter_by(name=account_name).first()
                if not account:
                    print('Account not found. Please try another account.')
                    return
                
                user = session.query(User).filter_by(id=self.user['id']).first()
                user.active_account_id = account.id
                self.user = user
                self.current_account = account.serialize
                
                print('Account switched to => {}'.format(self.current_account['name']))
                self.prompt = '{}@{} > '.format(self.user['username'], self.current_account['name'])

            elif command.lower() == 'showall':
                accounts = session.query(Account).filter_by(user_id=self.user['id']).all()
                print(accounts)
            
            elif command.lower() == 'current':
                print(self.current_account)
            
        except ValueError:
            print('Please enter valid command and/or necessary params')
            return


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
            'price': {
                'description': 'Displays the current price of a ticker'
            }
        }

        if not command:
            for key, val in commands.items():
                print('\t{} : {}'.format(key, val['description']))

        if command.lower() in commands:
            print('{} : {}'.format(command, commands[command]))
        


    def do_exit(self, args) -> None:
        raise SystemExit()
