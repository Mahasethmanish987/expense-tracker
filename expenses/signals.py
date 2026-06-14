from .models import Expense,Category 
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Sum
from .models import Expense, Category
from .utils import get_monthly_usd_spending,get_rates_and_as_of,send_slack_budget_alert

@receiver(post_save, sender=Expense)
def check_budget_threshold(sender, instance, created, **kwargs):

    category = instance.category
    budget = category.monthly_limit

    # No budget set or budget is zero → nothing to check
    if budget is None or budget <= Decimal('0'):
        return

    # Get total USD spending for the category in the expense's month
    total_usd = get_monthly_usd_spending(category, reference_date=instance.date)

    if total_usd > budget:
        month_year = instance.date.strftime("%B %Y")  # e.g., "June 2026"
        send_slack_budget_alert(
            category_name=category.name,
            spent=total_usd,
            limit=budget,
            month_year=month_year
        )