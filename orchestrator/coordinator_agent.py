from data_ingestion.api_client import fetch_fx_data

def coordinator(pair="EURUSD=X"):
    """
    Coordinates data flow to strategy agents for the given currency pair.
    """
    print(f"📡 Fetching FX data for: {pair}")
    data = fetch_fx_data(pair=pair)

    if data.empty:
        print("⚠️ No data returned. Please check the currency pair symbol.")
        return None

    print("✅ Data fetched. Preview:")
    print(data.head())

    # Placeholder for future routing to strategy agents
    return data


if __name__ == "__main__":
    user_pair = input("Enter currency pair (e.g., EURUSD=X, GBPUSD=X): ")
    coordinator(user_pair)
