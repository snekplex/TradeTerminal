from typing import List, Dict
import yfinance as yf
from yahoo_fin.stock_info import get_live_price

def get_ticker_current_price(ticker: str) -> float:
    live_price = get_live_price(ticker)

    # formatted like this to avoid prices in the thousandths place
    price = float('{:.2f}'.format(live_price))
    return price 