import json
from http import HTTPStatus

from rest_framework.reverse import reverse

from familybudget.budgets.models import Budget
from familybudget.budgets.tests.factories import BudgetFactory


class TestBudgetViewSet:
    def test_create_budget(self, user, api_client):
        api_client.force_authenticate(user=user)
        budget_data = {"name": "Savings"}
        api_client.post(
            reverse("api:budget-list"),
            data=json.dumps(budget_data),
            content_type="application/json",
        )
        assert Budget.objects.first().owner == user


class TestTransactionViewSet:
    def test_transaction_exceeds_saldo(self, user, api_client):
        budget = BudgetFactory(owner=user, allow_negative_saldo=False)
        transaction_data = {"budget": budget.id,
                            "transaction_type": "EX",
                            "amount": 1000}
        api_client.force_authenticate(user=user)
        response = api_client.post(
            reverse("api:transaction-list"),
            data=json.dumps(transaction_data),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
