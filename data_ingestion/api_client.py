import yfinance as yf
import pandas as pd

def fetch_fx_data(pair, period="1mo", interval="1d"):
    """
    Fetches historical FX data from Yahoo Finance.

    Parameters:
    - pair (str): Currency pair ticker (e.g., "EURUSD=X")
    - period (str): Historical period to fetch (e.g., "1mo", "1y")
    - interval (str): Data frequency ("1d", "1h")

    Returns:
    - DataFrame: Historical OHLC data with dates reset as a column.
    """
    data = yf.download(pair, period=period, interval=interval)
    data.reset_index(inplace=True)
    return data

if __name__ == "__main__":
    user_pair = input("Enter currency pair (e.g., EURUSD=X, GBPUSD=X): ")
    df = fetch_fx_data(user_pair)
    print(df.head())
