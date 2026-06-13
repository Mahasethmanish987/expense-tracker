import requests 
from decimal import Decimal
import datetime 
from datetime import datetime



def get_rates_and_as_of():

    url = "https://open.er-api.com/v6/latest/USD"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    rates = {curr: Decimal(str(rate)) for curr, rate in data["rates"].items()}

    last_update = data.get("time_last_update_utc", "")
    try:
        as_of = datetime.strptime(last_update, "%a, %d %b %Y %H:%M:%S %z").date().isoformat()
    except Exception:
        as_of = datetime.now().date().isoformat()
    return rates, as_of