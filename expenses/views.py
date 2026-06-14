from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from .utils import get_rates_and_as_of
from .models import Category, Expense
from .serializers import CategorySerializer, ExpenseSerializer
from collections import defaultdict
from decimal import Decimal
from rest_framework.decorators import  permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import CategoryBudgetSerializer,ExpenseWithCurrencySerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def category_list(request):
    if request.method == "GET":
        categories = Category.objects.filter(user=request.user)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    serializer = CategorySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_category_with_budget(request):
    serializer = CategoryBudgetSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user)

    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def expense_list(request):
    if request.method == "GET":
        expenses = Expense.objects.filter(user=request.user)

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        if start_date:
            expenses = expenses.filter(date__gte=start_date)
        if end_date:
            expenses = expenses.filter(date__lte=end_date)

        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    serializer = ExpenseSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_expense_with_currency(request):
    serializer = ExpenseWithCurrencySerializer(
        data=request.data
    )

    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user)

    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED,
    )

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def expense_detail(request, pk):
    try:
        expense = Expense.objects.get(pk=pk,user=request.user)
    except Expense.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)
    print("hellow world")
    if request.method == "PUT":
        serializer = ExpenseWithCurrencySerializer(expense, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    expense.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def expense_summary(request):
    rates, as_of = get_rates_and_as_of()
    categories = Category.objects.filter(user=request.user).prefetch_related("expenses")
    category_data = defaultdict(lambda: {
        'total_usd': Decimal('0'),
        'currencies': set()
    })
    for cat in categories:
        for expense in cat.expenses.all():
            currency = expense.currency
            rate = rates.get(currency)
            if rate is None:
                continue
            usd_amount = expense.amount / rate
            category_data[cat.name]['total_usd'] += usd_amount
            category_data[cat.name]['currencies'].add(currency)
    categories_output = []
    for cat_name, data in category_data.items():
        rate_dict = {curr: f"{rates[curr]:.2f}" for curr in data['currencies']}
        categories_output.append({
             "category": cat_name,
            "total": f"{data['total_usd']:.2f}",
            "rate": rate_dict,
            "as_of": as_of  
        })

    return Response({
        "base_currency": "USD",
        "categories": categories_output
    })