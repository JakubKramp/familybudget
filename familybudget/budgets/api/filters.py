from django_filters import RangeFilter
from django_filters import rest_framework as filters

from familybudget.budgets.models import Budget, BudgetCategory, Transaction


class BudgetFilter(filters.FilterSet):
    category = filters.CharFilter(field_name="category__name", lookup_expr="icontains")

    class Meta:
        model = Budget
        fields = ["category"]


class BudgetCategoryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = BudgetCategory
        fields = ["name"]


class TransactionFilter(filters.FilterSet):
    transaction_type = filters.CharFilter(
        field_name="transaction_type", lookup_expr="iexact"
    )
    amount = RangeFilter()

    class Meta:
        model = Transaction
        fields = ["transaction_type", "amount"]
