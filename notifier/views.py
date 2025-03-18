import requests
from django.shortcuts import render
from django.conf import settings
from datetime import datetime

# Your Etherscan API Key
ETHERSCAN_API_KEY = "5DFE258U1KA5397WP6YH8IB4YR3JAF3FCR"

def index(request):
    url = f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={ETHERSCAN_API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()

        if data["status"] == "1":  # Successful response
            gas_fee = data["result"]["SafeGasPrice"]  # Fetch Safe Gas Price
        else:
            gas_fee = "Unavailable"

    except Exception as e:
        gas_fee = "Error fetching data"

    context = {
        "gas_fee": gas_fee,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    return render(request, "index.html", context)