from django.urls import path

from . import views

urlpatterns = [
    path("categories/", views.category_list, name="category-list"),
    path("expenses/", views.expense_list, name="expense-list"),
     path("expenses/summary/", views.expense_summary, name="expense-summary"),
    path("expenses/<int:pk>/", views.expense_detail, name="expense-detail"),
    path(
        "categories-with-budget/",
        views.create_category_with_budget,
        name="create-category-with-budget",
    ),
    path(
    "expenses-with-currency/",
    views.create_expense_with_currency,
    name="expense-with-currency",
    ),
   
]
