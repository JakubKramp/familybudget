from django.core.exceptions import ValidationError
from rest_framework import serializers

from familybudget.budgets.models import Budget, BudgetCategory, Transaction


class ListTransactionsSerializer(serializers.ModelSerializer[Transaction]):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type']

class ListBudgetSerializer(serializers.ModelSerializer[Budget]):
    class Meta:
        model = Budget
        fields = ["name", 'saldo', 'category']

class BudgetSerializer(ListBudgetSerializer):
    transactions = ListTransactionsSerializer
    class Meta:
        model = Budget
        fields = ListBudgetSerializer.Meta.fields + ["users", "families", "transactions"]

    def create(self, validated_data):
        budget = super().create(validated_data)
        budget.owner = self.context['request'].user
        budget.save()
        return budget


class BudgetCategorySerializer(serializers.ModelSerializer[BudgetCategory]):
    class Meta:
        model = BudgetCategory
        fields = ["name"]

class TransactionSerializer(ListTransactionsSerializer):
    class Meta:
        model = Transaction
        fields = ListTransactionsSerializer.Meta.fields + ['budget']

    def create(self, validated_data):
        budget = Budget.objects.get(id=validated_data.get('budget'))
        if self.context['request'].user not in budget.get_users_with_access():
            raise ValidationError(
                {'budget': 'Cant create a transaction for a budget you dont have access to'},
                code='Access denied',
            )
        if budget.allow_negative_saldo and validated_data.get('transaction_type', 'EX') == 'EX' and budget.saldo < validated_data.get('amount'):
            raise ValidationError(
                {'amount': 'This budget does not allow negative saldo'},
                code='Saldo exceeded',
            )
        return super().create(validated_data)