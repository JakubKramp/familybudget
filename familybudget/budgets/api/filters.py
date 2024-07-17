import django_filters
from django_filters import rest_framework as filters

class BudgetFilter(filters.FilterSet):
    status = filters.CharFilter(field_name="category", lookup_expr='iexact')

    class Meta:
        model = Budget
        fields = ['status']

class TransactionFilter(filters.FilterSet):
    author = filters.CharFilter(field_name="author__name", lookup_expr='icontains')
    transaction_type = filters.CharFilter(field_name="transaction_type", lookup_expr='iexact')
    amount = RangeFilter()

    class Meta:
        model = Transaction
        fields = ['author', 'transaction_type', 'amount']