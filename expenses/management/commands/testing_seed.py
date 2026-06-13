# expenses/management/commands/seed2.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date

from expenses.models import Category, Expense
from expenses.utils import get_rates_and_as_of

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed user, low-budget category, and multi-currency expenses that exceed threshold (triggers Slack alert)'

    def handle(self, *args, **options):
        # ------------------------------------------------------------
        # 1. Create/get test user
        # ------------------------------------------------------------
        user, created = User.objects.get_or_create(
            username='alert_test_user',
            defaults={
                'email': 'alert_test@example.com',
                'first_name': 'Alert',
                'last_name': 'Tester',
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS('✅ Created user: alert_test_user (pw: testpass123)'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ User alert_test_user exists'))

        # ------------------------------------------------------------
        # 2. Category with a low USD budget (now $40 to easily exceed)
        # ------------------------------------------------------------
        category_name = "Global Snacks"
        threshold_usd = Decimal('40.00')   # <<< lowered to $40

        category, cat_created = Category.objects.get_or_create(
            user=user,
            name=category_name,
            defaults={
                'description': 'Multi-currency test category – low USD budget',
                'monthly_budget_threshold': threshold_usd
            }
        )
        if cat_created:
            self.stdout.write(self.style.SUCCESS(f'✅ Created category: {category_name} (budget: ${threshold_usd})'))
        else:
            category.monthly_budget_threshold = threshold_usd
            category.save()
            self.stdout.write(self.style.WARNING(f'⚠️ Updated category {category_name} to budget ${threshold_usd}'))

        # ------------------------------------------------------------
        # 3. Delete all existing expenses for this user & category
        #    to ensure a clean test run
        # ------------------------------------------------------------
        deleted_count, _ = Expense.objects.filter(user=user, category=category).delete()
        if deleted_count:
            self.stdout.write(f'🗑️ Deleted {deleted_count} existing expenses for {category_name}')

        # ------------------------------------------------------------
        # 4. Fetch current exchange rates (to compute USD equivalents)
        # ------------------------------------------------------------
        rates, as_of = get_rates_and_as_of()
        self.stdout.write(f'📅 Using exchange rates from {as_of}')

        # ------------------------------------------------------------
        # 5. Multi-currency expenses that exceed $40 USD
        #    (using the same amounts as before, which totalled ~$49)
        # ------------------------------------------------------------
        expense_date = date(2026, 6, 15)
        expenses_raw = [
            {'title': 'Burger meal', 'amount': Decimal('25.00'), 'currency': 'USD'},
            {'title': 'Soda', 'amount': Decimal('5.50'), 'currency': 'USD'},
            {'title': 'Croissant in Paris', 'amount': Decimal('8.00'), 'currency': 'EUR'},
            {'title': 'Espresso', 'amount': Decimal('3.50'), 'currency': 'EUR'},
            {'title': 'Samosa', 'amount': Decimal('120.00'), 'currency': 'INR'},
            {'title': 'Chai', 'amount': Decimal('50.00'), 'currency': 'INR'},
            {'title': 'Momo', 'amount': Decimal('400.00'), 'currency': 'NPR'},
            {'title': 'Tea', 'amount': Decimal('150.00'), 'currency': 'NPR'},
        ]

        # Calculate USD equivalent total BEFORE adding to DB (for info)
        total_usd = Decimal('0')
        for exp in expenses_raw:
            currency = exp['currency']
            amount = exp['amount']
            if currency == 'USD':
                usd_val = amount
            else:
                rate = rates.get(currency)
                if rate:
                    usd_val = amount / rate
                else:
                    self.stdout.write(self.style.ERROR(f'⚠️ No rate for {currency} – skipping USD calc'))
                    usd_val = Decimal('0')
            total_usd += usd_val
            exp['usd_equivalent'] = usd_val

        self.stdout.write(f'📊 Total USD equivalent of all expenses: ${total_usd:.2f}')
        self.stdout.write(f'🎯 Category budget: ${threshold_usd:.2f}')
        if total_usd > threshold_usd:
            self.stdout.write(self.style.SUCCESS('✅ Total exceeds budget – alert should trigger!'))
        else:
            self.stdout.write(self.style.ERROR('❌ Total does NOT exceed budget – adjust amounts/rates'))

        # ------------------------------------------------------------
        # 6. Create expenses (fresh because we deleted existing ones)
        # ------------------------------------------------------------
        created_count = 0
        for exp in expenses_raw:
            expense = Expense.objects.create(
                user=user,
                title=exp['title'],
                date=expense_date,
                amount=exp['amount'],
                currency=exp['currency'],
                category=category,
                notes=f'Multi-currency test – USD equivalent ≈ {exp["usd_equivalent"]:.2f}'
            )
            created_count += 1
            self.stdout.write(f'  ➕ Added: {exp["title"]} ({exp["amount"]} {exp["currency"]}) = ~${exp["usd_equivalent"]:.2f}')

        # ------------------------------------------------------------
        # 7. Summary
        # ------------------------------------------------------------
        self.stdout.write(self.style.SUCCESS('\n=== SEEDING COMPLETE ==='))
        self.stdout.write(f'👤 User: alert_test_user / testpass123')
        self.stdout.write(f'📂 Category: {category.name} (budget ${category.monthly_budget_threshold})')
        self.stdout.write(f'💰 Expenses created: {created_count}')
        self.stdout.write(f'💵 Month-to-date USD spending (from seed): ${total_usd:.2f}')
        self.stdout.write('🔔 If Slack is configured and total > budget, you should receive an alert now.')

        # Optional: recompute via helper function to verify
        from expenses.utils import get_monthly_usd_spending
        verified_total = get_monthly_usd_spending(category, reference_date=expense_date)
        self.stdout.write(f'✅ Verified by get_monthly_usd_spending(): ${verified_total:.2f}')