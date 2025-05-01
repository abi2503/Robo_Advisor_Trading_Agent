from data_ingestion.interest_rates import get_interest_rate

def fx_carry_trade_signal(pair):
    """
    Determines FX carry trade signal based on real interest rate spread.
    - BUY: if base rate > quote rate by >1%
    - SELL: if base rate < quote rate by >1%
    - HOLD: otherwise
    """
    base = pair[:3]
    quote = pair[3:6]

    base_rate = get_interest_rate(base)
    quote_rate = get_interest_rate(quote)

    print(f"\n🔍 Live Interest Rates:")
    print(f"{base}: {base_rate}%")
    print(f"{quote}: {quote_rate}%")

    if base_rate is None or quote_rate is None:
        return "HOLD"

    spread = base_rate - quote_rate

    if spread > 1.0:
        return "BUY"
    elif spread < -1.0:
        return "SELL"
    else:
        return "HOLD"


# CLI entry point for testing
if __name__ == "__main__":
    pair = input("Enter currency pair (e.g., USDJPY=X): ")
    signal = fx_carry_trade_signal(pair)
    base = pair[:3]
    quote = pair[3:6]

    print(f"\n💰 FX Carry Trade Signal for {pair}: {signal}")
    if signal == "BUY":
        print(f"🟢 Suggested Action: Go LONG — Buy {base} (high yield), Sell {quote} (low yield)")
    elif signal == "SELL":
        print(f"🔴 Suggested Action: Go SHORT — Sell {base} (low yield), Buy {quote} (high yield)")
    else:
        print("⚪ Suggested Action: HOLD — No strong rate advantage detected")
