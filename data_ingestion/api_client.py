import yfinance as yf
import pandas as pd

def fetch_fx_data(pair, period="1mo", interval="1d"):
    data = yf.download(pair, period=period, interval=interval)
    data.reset_index(inplace=True)

    # Step 1: Flatten multi-index columns if needed
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]

    # Step 2: Rename any symbol-suffixed columns
    new_columns = {}
    for col in data.columns:
        # Handle cases like 'Close USDJPY=X'
        if pair in col:
            new_col = col.replace(f' {pair}', '')  # Remove the symbol
            new_columns[col] = new_col
    data.rename(columns=new_columns, inplace=True)

    # Step 3: Check required columns
    required_cols = ['Open', 'High', 'Low', 'Close']
    if not all(col in data.columns for col in required_cols):
        print("⚠️ Columns fetched:", data.columns.tolist())
        raise ValueError("Missing required columns: Open, High, Low, Close")

    return data
if __name__ == "__main__":
    user_pair = input("Enter currency pair (e.g., EURUSD=X, GBPUSD=X): ")
    df = fetch_fx_data(user_pair)
    print("📋 Columns in fetched data:", df.columns.tolist())

    print(df.head())
