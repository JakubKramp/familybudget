
from django.contrib import admin

from familybudget.budgets.models import Budget, Transaction


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'saldo', 'allow_negative_saldo']
    search_fields = ['name']

    list_filter = [
        'allow_negative_saldo'
    ]



@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['budget', 'amount', 'transaction_type']
    search_fields = ['budget']
    list_filter = [
        'transaction_type', 'budget'
    ]