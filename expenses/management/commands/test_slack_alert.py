# expenses/management/commands/test_slack_alert.py

from django.core.management.base import BaseCommand

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from django.conf import settings 
class Command(BaseCommand):
    help = 'Send a dummy budget alert to Slack'

    def handle(self, *args, **options):

        token = settings.SLACK_BOT_TOKEN
        channel = settings.SLACK_CHANNEL 
        client = WebClient(token=token)
        category_name = "Dining"
        spent = 215.00
        limit = 200.00
        month_year = "June 2026"

        message = (
            f"⚠️ Budget alert: \"{category_name}\" is over its monthly limit.\n"
            f"Spent {spent:.2f} / {limit:.2f} USD for {month_year}."
        )

        try:
            response = client.chat_postMessage(channel=channel, text=message)
            self.stdout.write(self.style.SUCCESS(f'✅ Alert sent! Timestamp: {response["ts"]}'))
        except SlackApiError as e:
            self.stdout.write(self.style.ERROR(f'❌ Slack error: {e.response["error"]}'))