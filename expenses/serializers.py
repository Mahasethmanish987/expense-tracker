from rest_framework import serializers

from .models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]

class CategoryBudgetSerializer(CategorySerializer):
    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ["monthly_budget_threshold"]

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