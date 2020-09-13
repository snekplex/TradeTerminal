from cmd import Cmd
from data.yahoo import get_ticker_current_price

class TradeTermial(Cmd):

    prompt = '> '

    def do_price(self, ticker: str) -> None:
        price = None
        try:
            price = get_ticker_current_price(ticker)
        except AssertionError:
            # Handle if ticker is not found or does not exist
            print(f'Ticker {ticker} not found')
    
        if price:
            print('{} => ${}'.format(ticker.upper(), price))

    def do_help(self, arg):
        print('Help here')

    def do_exit(self, args):
        raise SystemExit()
