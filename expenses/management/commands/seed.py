# expenses/management/commands/seed.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, timedelta

from expenses.models import Category, Expense

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with test data (user, categories, expenses)'

    def handle(self, *args, **options):
        # ------------------------------------------------------------
        # 1. Create a test user (with hashed password)
        # ------------------------------------------------------------
        test_user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'testuser@example.com',
                'first_name': 'Test',
                'last_name': 'User',
            }
        )
        if created:
            test_user.set_password('testpass123')
            test_user.save()
            self.stdout.write(self.style.SUCCESS('✅ Created user: testuser (password: testpass123)'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ User testuser already exists'))

        # ------------------------------------------------------------
        # 2. Create categories for this user (with monthly budget thresholds)
        # ------------------------------------------------------------
        categories_data = [
            {'name': 'Food', 'description': 'Groceries, restaurants, coffee', 'budget': Decimal('500.00')},
            {'name': 'Transport', 'description': 'Fuel, public transit, rideshares', 'budget': Decimal('300.00')},
            {'name': 'Entertainment', 'description': 'Movies, games, subscriptions', 'budget': Decimal('200.00')},
            {'name': 'Utilities', 'description': 'Electricity, water, internet', 'budget': Decimal('400.00')},
            {'name': 'Shopping', 'description': 'Clothes, electronics, gifts', 'budget': Decimal('350.00')},
            {'name': 'Health', 'description': 'Pharmacy, doctor, gym', 'budget': Decimal('250.00')},
        ]

        created_cats = []
        for cat_data in categories_data:
            cat, cat_created = Category.objects.get_or_create(
                user=test_user,
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'monthly_budget_threshold': cat_data['budget']
                }
            )
            created_cats.append(cat)
            if cat_created:
                self.stdout.write(self.style.SUCCESS(f'  ➕ Created category: {cat.name} (budget: ${cat.monthly_budget_threshold})'))
            else:
                self.stdout.write(self.style.WARNING(f'  ⚠️ Category {cat.name} already exists'))

        # ------------------------------------------------------------
        # 3. Create expenses for the current month (using fixed date for reproducibility)
        #    Include multi‑currency expenses to test conversion
        # ------------------------------------------------------------
        # Fixed "today" for reproducible seeding: June 13, 2026 (as in your example)
        today = date(2026, 6, 13)
        start_of_month = today.replace(day=1)

        expenses_raw = [
            # Food (USD)
            {'title': 'Grocery shopping', 'amount': Decimal('85.50'), 'category': 'Food', 'date': start_of_month + timedelta(days=2), 'currency': 'USD', 'notes': 'Weekly groceries'},
            {'title': 'Restaurant dinner', 'amount': Decimal('62.30'), 'category': 'Food', 'date': start_of_month + timedelta(days=5), 'currency': 'USD', 'notes': 'Italian place'},
            {'title': 'Coffee shop', 'amount': Decimal('12.75'), 'category': 'Food', 'date': start_of_month + timedelta(days=8), 'currency': 'USD', 'notes': 'Latte and pastry'},
            {'title': 'Pizza delivery', 'amount': Decimal('28.99'), 'category': 'Food', 'date': start_of_month + timedelta(days=10), 'currency': 'USD', 'notes': 'Weekend treat'},
            # Food (EUR, INR)
            {'title': 'Paris café', 'amount': Decimal('35.00'), 'category': 'Food', 'date': start_of_month + timedelta(days=4), 'currency': 'EUR', 'notes': 'Croissant and coffee'},
            {'title': 'Mumbai street food', 'amount': Decimal('500.00'), 'category': 'Food', 'date': start_of_month + timedelta(days=6), 'currency': 'INR', 'notes': 'Vada pav and chai'},
            
            # Transport
            {'title': 'Gas station', 'amount': Decimal('45.00'), 'category': 'Transport', 'date': start_of_month + timedelta(days=3), 'currency': 'USD', 'notes': 'Fill up'},
            {'title': 'Uber ride', 'amount': Decimal('18.50'), 'category': 'Transport', 'date': start_of_month + timedelta(days=7), 'currency': 'USD', 'notes': 'Airport'},
            {'title': 'Bus pass', 'amount': Decimal('60.00'), 'category': 'Transport', 'date': start_of_month + timedelta(days=1), 'currency': 'USD', 'notes': 'Monthly pass'},
            {'title': 'London underground', 'amount': Decimal('15.00'), 'category': 'Transport', 'date': start_of_month + timedelta(days=8), 'currency': 'GBP', 'notes': 'Oyster top-up'},
            
            # Entertainment
            {'title': 'Netflix', 'amount': Decimal('15.99'), 'category': 'Entertainment', 'date': start_of_month + timedelta(days=1), 'currency': 'USD', 'notes': 'Monthly sub'},
            {'title': 'Cinema tickets', 'amount': Decimal('24.00'), 'category': 'Entertainment', 'date': start_of_month + timedelta(days=6), 'currency': 'USD', 'notes': 'IMAX'},
            {'title': 'Video game', 'amount': Decimal('59.99'), 'category': 'Entertainment', 'date': start_of_month + timedelta(days=9), 'currency': 'USD', 'notes': 'Steam purchase'},
            
            # Utilities
            {'title': 'Electricity bill', 'amount': Decimal('95.00'), 'category': 'Utilities', 'date': start_of_month + timedelta(days=4), 'currency': 'USD', 'notes': 'June estimate'},
            {'title': 'Internet bill', 'amount': Decimal('79.99'), 'category': 'Utilities', 'date': start_of_month + timedelta(days=5), 'currency': 'USD', 'notes': 'Fiber'},
            
            # Shopping
            {'title': 'New shoes', 'amount': Decimal('120.00'), 'category': 'Shopping', 'date': start_of_month + timedelta(days=7), 'currency': 'USD', 'notes': 'Running shoes'},
            {'title': 'Book', 'amount': Decimal('22.50'), 'category': 'Shopping', 'date': start_of_month + timedelta(days=11), 'currency': 'USD', 'notes': 'Hardcover'},
            {'title': 'Kathmandu souvenir', 'amount': Decimal('2500.00'), 'category': 'Shopping', 'date': start_of_month + timedelta(days=10), 'currency': 'NPR', 'notes': 'Handicraft'},
            
            # Health
            {'title': 'Pharmacy', 'amount': Decimal('34.25'), 'category': 'Health', 'date': start_of_month + timedelta(days=2), 'currency': 'USD', 'notes': 'Allergy meds'},
            {'title': 'Doctor visit', 'amount': Decimal('150.00'), 'category': 'Health', 'date': start_of_month + timedelta(days=9), 'currency': 'USD', 'notes': 'Checkup'},
        ]

        category_map = {cat.name: cat for cat in created_cats}
        expenses_created = 0

        for exp in expenses_raw:
            cat_obj = category_map.get(exp['category'])
            if not cat_obj:
                self.stdout.write(self.style.ERROR(f'❌ Category {exp["category"]} not found – skipping expense'))
                continue

            # Use get_or_create to avoid duplicates (based on title + date + user)
            obj, created_flag = Expense.objects.get_or_create(
                user=test_user,
                title=exp['title'],
                date=exp['date'],
                defaults={
                    'amount': exp['amount'],
                    'currency': exp['currency'],
                    'category': cat_obj,
                    'notes': exp.get('notes', ''),
                }
            )
            if created_flag:
                expenses_created += 1

        self.stdout.write(self.style.SUCCESS(f'✅ Created {expenses_created} new expenses'))

        # ------------------------------------------------------------
        # 4. Summary
        # ------------------------------------------------------------
        self.stdout.write(self.style.SUCCESS('\n=== SEEDING COMPLETE ==='))
        self.stdout.write(f'👤 User: testuser / password: testpass123')
        self.stdout.write(f'📂 Categories: {Category.objects.filter(user=test_user).count()}')
        self.stdout.write(f'💰 Total expenses: {Expense.objects.filter(user=test_user).count()}')