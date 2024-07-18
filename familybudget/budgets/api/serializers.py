from django.core.exceptions import ValidationError
from rest_framework import serializers

from familybudget.budgets.models import Budget, BudgetCategory, Transaction


class ListTransactionsSerializer(serializers.ModelSerializer[Transaction]):
    class Meta:
        model = Transaction
        fields = ["amount", "transaction_type"]


class ListBudgetSerializer(serializers.ModelSerializer[Budget]):
    category = serializers.CharField(source="category.name")

    class Meta:
        model = Budget
        fields = ["id", "name", "saldo", "category"]


class BudgetSerializer(serializers.ModelSerializer[Budget]):
    transactions = ListTransactionsSerializer(read_only=True, many=True)

    class Meta:
        model = Budget
        fields = [
            "id",
            "name",
            "saldo",
            "category",
            "users",
            "families",
            "transactions",
        ]

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


class BudgetCategorySerializer(serializers.ModelSerializer[BudgetCategory]):
    class Meta:
        model = BudgetCategory
        fields = ["name"]


class TransactionSerializer(ListTransactionsSerializer):
    class Meta:
        model = Transaction
        fields = [*ListTransactionsSerializer.Meta.fields, "budget"]

    def create(self, validated_data):
        budget = validated_data["budget"]
        if self.context["request"].user not in budget.get_users_with_access():
            raise ValidationError(
                {
                    "budget": "Cant create a transaction for a budget you dont have access to",  # noqa: E501
                },
                code="Access denied",
            )
        if (
            not budget.allow_negative_saldo
            and validated_data.get("transaction_type", "EX") == "EX"
            and budget.saldo < validated_data.get("amount")
        ):
            raise ValidationError(
                {"amount": "This budget does not allow negative saldo"},
                code="Saldo exceeded",
            )
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)
