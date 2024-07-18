from django.contrib import admin

from familybudget.budgets.models import Budget
from familybudget.budgets.models import BudgetCategory
from familybudget.budgets.models import Transaction


@admin.register(BudgetCategory)
class BudgetCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "budgets_count"]
    search_fields = ["name"]

    def budgets_count(self, obj):
        return obj.budgets.count()


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ["name", "saldo", "allow_negative_saldo", "category", "owner"]
    search_fields = ["name", "category", "owner"]
    list_filter = ["allow_negative_saldo", "category"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["budget", "amount", "transaction_type", "author"]
    search_fields = ["budget", "author"]
    list_filter = ["transaction_type", "budget"]
