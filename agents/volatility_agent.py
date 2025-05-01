import pandas as pd

def calculate_atr(data, period=14):
    """
    Calculates the Average True Range (ATR) — a volatility indicator.
    ATR reflects how much price fluctuates on average over 'period' days.
    """
    data['H-L'] = data['High'] - data['Low']
    data['H-PC'] = abs(data['High'] - data['Close'].shift(1))
    data['L-PC'] = abs(data['Low'] - data['Close'].shift(1))
    data['TR'] = data[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    data['ATR'] = data['TR'].rolling(window=period).mean()
    return data['ATR']


def volatility_breakout_signal(data, atr_period=14):
    """
    Detects breakout signals based on price + volatility (ATR).
    Signal triggers when price breaks recent range with increasing ATR.
    Returns: 'BUY', 'SELL', or 'HOLD'
    """

    # Ensure required columns exist
    required_cols = {'Close', 'High', 'Low'}
    if not required_cols.issubset(data.columns):
        raise ValueError("Missing required columns in input data.")

    # Calculate ATR
    data['ATR'] = calculate_atr(data, period=atr_period)

    # Calculate breakout levels (exclude current day)
    data['rolling_high'] = data['High'].shift(1).rolling(window=atr_period).max()
    data['rolling_low'] = data['Low'].shift(1).rolling(window=atr_period).min()

    # Extract scalar values (to avoid ambiguous Series)
    latest_close = data['Close'].iloc[-1]
    rolling_high = data['rolling_high'].iloc[-1]
    rolling_low = data['rolling_low'].iloc[-1]
    current_atr = data['ATR'].iloc[-1]
    prev_atr = data['ATR'].iloc[-2]

    # Check if volatility is rising
    atr_increasing = current_atr > prev_atr

    # Decision logic
    if atr_increasing and latest_close > rolling_high:
        return "BUY"
    elif atr_increasing and latest_close < rolling_low:
        return "SELL"
    else:
        return "HOLD"


# Optional CLI entry point for testing
if __name__ == "__main__":
    from data_ingestion.api_client import fetch_fx_data

    pair = input("Enter currency pair (e.g., USDJPY=X): ")
    df = fetch_fx_data(pair)

    if df.empty:
        print("⚠️ No data fetched. Please enter a valid symbol.")
    else:
        signal = volatility_breakout_signal(df)

        # Extract base and quote for explanation
        base_currency = pair[:3]
        quote_currency = pair[3:6]

        print(f"\n📊 Volatility Breakout Signal for {pair}: {signal}")
        print(f"🔍 Base Currency: {base_currency}")
        print(f"🔍 Quote Currency: {quote_currency}")

        if signal == "BUY":
            print(f"🟢 Interpretation: Price is breaking out above recent highs with rising volatility.")
            print(f"✅ Suggested Action: Go LONG — Buy {base_currency} and sell {quote_currency}.")
            print("💼 You can execute this via: Spot FX, Currency Futures, or CFDs.")
        elif signal == "SELL":
            print(f"🔴 Interpretation: Price is breaking down below recent lows with rising volatility.")
            print(f"✅ Suggested Action: Go SHORT — Sell {base_currency} and buy {quote_currency}.")
            print("💼 You can execute this via: Spot FX, Currency Futures, or CFDs.")
        else:
            print("⚪ Interpretation: Market is calm or within normal range.")
            print("💡 Suggested Action: HOLD — Wait for stronger breakout confirmation.")
