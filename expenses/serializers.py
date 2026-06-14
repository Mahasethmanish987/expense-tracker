from rest_framework import serializers

from .models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]

class CategoryBudgetSerializer(CategorySerializer):
    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ["monthly_limit"]

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ["id", "title", "amount", "category", "date", "notes"]
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value        

class ExpenseWithCurrencySerializer(ExpenseSerializer):
    class Meta(ExpenseSerializer.Meta):
        fields = ExpenseSerializer.Meta.fields + ["currency"]

    def validate_currency(self, value):
        valid_currencies = [
            choice[0]
            for choice in Expense.CURRENCY_CHOICES
        ]

        if value not in valid_currencies:
            raise serializers.ValidationError(
                f"Currency must be one of: {', '.join(valid_currencies)}"
            )

        return value