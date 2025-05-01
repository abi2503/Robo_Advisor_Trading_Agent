from data_ingestion.api_client import fetch_fx_data
from agents.trend_following_agent import trend_following_signal
from agents.volatility_agent import volatility_breakout_signal

def coordinator(pair="EURUSD=X"):
    print(f"\n📡 Fetching FX data for: {pair}")
    data = fetch_fx_data(pair)

    if data.empty:
        print("⚠️ No data returned. Please check the currency pair symbol.")
        return

    print("✅ Data fetched. Running strategy agents...")

    # Get signals
    trend_signal = trend_following_signal(data)
    volatility_signal = volatility_breakout_signal(data)

    # Extract base and quote currency for context
    base_currency = pair[:3]
    quote_currency = pair[3:6]

    # Output Trend-Following Result
    print(f"\n📈 Trend-Following Agent Signal: {trend_signal}")
    print(f"🔍 Base Currency: {base_currency}")
    print(f"🔍 Quote Currency: {quote_currency}")
    if trend_signal == "BUY":
        print(f"🟢 Interpretation: {base_currency} is gaining strength over {quote_currency}.")
        print(f"✅ Action: Go LONG — Buy {base_currency}, Sell {quote_currency}.")
    elif trend_signal == "SELL":
        print(f"🔴 Interpretation: {base_currency} is weakening against {quote_currency}.")
        print(f"✅ Action: Go SHORT — Sell {base_currency}, Buy {quote_currency}.")
    else:
        print("⚪ HOLD — Trend is unclear. No position suggested.")

    # Output Volatility Result
    print(f"\n📊 Volatility Breakout Agent Signal: {volatility_signal}")
    if volatility_signal == "BUY":
        print(f"🟢 Market is breaking above recent highs with rising volatility.")
        print(f"✅ Action: Go LONG — Buy {base_currency}, Sell {quote_currency}.")
    elif volatility_signal == "SELL":
        print(f"🔴 Market is breaking below recent lows with rising volatility.")
        print(f"✅ Action: Go SHORT — Sell {base_currency}, Buy {quote_currency}.")
    else:
        print("⚪ HOLD — Market is calm or no breakout detected.")

    return {
        "trend_following": trend_signal,
        "volatility_breakout": volatility_signal
    }


if __name__ == "__main__":
    user_pair = input("Enter currency pair (e.g., EURUSD=X, USDJPY=X): ")
    coordinator(user_pair)
