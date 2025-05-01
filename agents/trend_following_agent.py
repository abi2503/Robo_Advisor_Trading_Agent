import pandas as pd

def calculate_ema(series, period):
    """
    Calculate Exponential Moving Average (EMA) for a given price series.

    EMA gives more weight to recent prices and reacts faster to changes.
    Think of it like a momentum tracker that cares more about recent moves.
    """
    return series.ewm(span=period, adjust=False).mean()


def trend_following_signal(data):
    """
    Uses EMA crossover logic to generate a trading signal.

    Strategy:
    - BUY  if EMA_50 > EMA_200 (short-term trend stronger)
    - SELL if EMA_50 < EMA_200 (long-term trend dominates)
    - HOLD otherwise
    """

    # Ensure 'Close' price column exists
    if 'Close' not in data.columns:
        raise ValueError("Missing 'Close' column in input data.")

    # Calculate 50-period and 200-period EMAs
    data['EMA_50'] = calculate_ema(data['Close'], 50)
    data['EMA_200'] = calculate_ema(data['Close'], 200)

    # Extract most recent EMA values (float, not Series)
    ema_50 = data['EMA_50'].iloc[-1]
    ema_200 = data['EMA_200'].iloc[-1]

    # Decision logic based on crossover
    if ema_50 > ema_200:
        return "BUY"
    elif ema_50 < ema_200:
        return "SELL"
    else:
        return "HOLD"


# Optional CLI usage for standalone testing
if __name__ == "__main__":
    from data_ingestion.api_client import fetch_fx_data

    pair = input("Enter currency pair (e.g., EURUSD=X): ")
    df = fetch_fx_data(pair)

    if df.empty:
        print("⚠️ No data fetched. Please enter a valid currency pair.")
    else:
        signal = trend_following_signal(df)
        # Parse base and quote currencies
        base_currency = pair[:3]
        quote_currency = pair[3:6]

        print(f"\n📈 Trend Following Signal for {pair}: {signal}")
        print(f"🔍 Base Currency: {base_currency}")
        print(f"🔍 Quote Currency: {quote_currency}")

        if signal == "BUY":
            print(f"🟢 Interpretation: The market is in an uptrend. Recent momentum favors {base_currency}.")
            print(f"✅ Suggested Action: Go LONG — Buy {base_currency} and sell {quote_currency}.")
            print("💼 You can execute this via: Spot FX, Currency Futures, or CFDs.")
        elif signal == "SELL":
            print(f"🔴 Interpretation: The market is in a downtrend. Momentum favors {quote_currency}.")
            print(f"✅ Suggested Action: Go SHORT — Sell {base_currency} and buy {quote_currency}.")
            print("💼 You can execute this via: Spot FX, Currency Futures, or CFDs.")
        else:
            print("⚪ Interpretation: No strong trend detected.")
            print("💡 Suggested Action: HOLD — Do not initiate new trades based on this strategy right now.")
