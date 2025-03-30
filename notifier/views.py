import requests
from django.shortcuts import render
from django.conf import settings
from datetime import datetime

# API Keys from settings.py
ETHERSCAN_API_KEY = settings.ETHERSCAN_API_KEY
BLOCKNATIVE_API_KEY = settings.BLOCKNATIVE_API_KEY

def fetch_gas_fee_from_blocknative():
    """Fetch gas fee from Blocknative API."""
    url = "https://api.blocknative.com/gasprices/blockprices"
    headers = {"Authorization": BLOCKNATIVE_API_KEY}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        # Extract highest confidence gas price
        estimated_prices = data.get("estimatedPrices", [])
        if estimated_prices:
            return estimated_prices[0]["price"]  # Gas fee in Gwei
    except Exception:
        return None  # Return None if Blocknative fails

def fetch_gas_fee_from_etherscan():
    """Fetch gas fee from Etherscan API (fallback)."""
    url = f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={ETHERSCAN_API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("status") == "1":  # Successful response
            return data["result"]["SafeGasPrice"]  # Gas fee in Gwei
    except Exception:
        return None  # Return None if Etherscan fails

def index(request):
    """Main view: Fetch gas fee from Blocknative (primary) or Etherscan (fallback)."""
    gas_fee = fetch_gas_fee_from_blocknative() or fetch_gas_fee_from_etherscan() or "Unavailable"

    context = {
        "gas_fee": gas_fee,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    return render(request, "index.html", context)