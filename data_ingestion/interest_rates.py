import requests

API_KEY = "c9SGBDBvuZQ1HTrFDvhXkFTCWclpOQmN"

INDICATOR_MAP = {
    "USD": "FEDFUNDS",
    "EUR": "ECBDEPO",
    "GBP": "BOERATE",
    "JPY": "JPNINT",
    "AUD": "RBACASH",
    "CAD": "BOCRATE",
    "CHF": "SNBRATE",
    "NZD": "RBNZRATE"
}

def get_interest_rate(currency_code):
    indicator = INDICATOR_MAP.get(currency_code.upper())
    if not indicator:
        print(f"⚠️ No indicator mapped for {currency_code}")
        return None

    url = f"https://api.polygon.io/v1/indicators/{indicator}?apiKey={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        # Look at the most recent value
        latest = data.get("results", {}).get("values", [])[0]
        return float(latest.get("value"))
    except Exception as e:
        print(f"⚠️ Error fetching rate for {currency_code}: {e}")
        return None
