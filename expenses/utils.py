from decimal import Decimal
import requests

def get_exchange_rates(currency: str) -> Decimal:

    CURRENCY_API_URL = "https://open.er-api.com/v6/latest/USD"
    
    response = requests.get(CURRENCY_API_URL, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch exchange rates: HTTP {response.status_code}")
    
    data = response.json()
    if data.get("result") != "success":
        raise Exception(f"API error: {data.get('error-type', 'unknown')}")
    
    rates = data.get("rates", {})
    if currency not in rates:
        raise Exception(f"Currency '{currency}' not found in exchange rates")
    return Decimal(str(rates[currency]))

def get_amount_in_usd(currency_type: str, amount: Decimal) -> Decimal:

    rate = get_exchange_rates(currency_type)
    return amount / rate