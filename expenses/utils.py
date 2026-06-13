import requests 
from decimal import Decimal
import datetime 
from datetime import datetime
from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

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



def get_monthly_usd_spending(category, reference_date=None):
    """Return total USD spending for the category in the month of reference_date."""
    if reference_date is None:
        reference_date = timezone.now().date()
    start_of_month = reference_date.replace(day=1)
    next_month = start_of_month.replace(day=28) + timedelta(days=4)
    end_of_month = next_month - timedelta(days=next_month.day)

    expenses = category.expenses.filter(date__gte=start_of_month, date__lte=end_of_month)
    if not expenses.exists():
        return Decimal('0')

    rates, _ = get_rates_and_as_of()   # cached
    total_usd = Decimal('0')
    for exp in expenses:
        rate = rates.get(exp.currency)
        if rate:
            total_usd += exp.amount / rate
    return total_usd

def send_slack_budget_alert(category_name, spent, limit, month_year):
    """
    Send a formatted budget alert to a Slack channel.
    Requires SLACK_BOT_TOKEN and SLACK_CHANNEL in Django settings.
    """
    token = settings.SLACK_BOT_TOKEN
    channel = settings.SLACK_CHANNEL      # e.g., 'budget-alerts' (without '#')
    client = WebClient(token=token)

    message = (
        f"⚠️ Budget alert: \"{category_name}\" is over its monthly limit.\n"
        f"Spent {spent:.2f} / {limit:.2f} USD for {month_year}."
    )

    try:
        response = client.chat_postMessage(channel=channel, text=message)
     
    except SlackApiError as e:
      pass 