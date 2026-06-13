from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)
    monthly_budget_threshold = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Expense(models.Model):
    CURRENCY_CHOICES = [
        ("USD", "US Dollar"),
        ("EUR", "Euro"),
        ("GBP", "British Pound"),
        ("INR", "Indian Rupee"),
        ("NPR", "Nepalese Rupee"),
    ]

    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default="USD",
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="expenses"
    )
    date = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} ({self.amount} {self.currency})"
