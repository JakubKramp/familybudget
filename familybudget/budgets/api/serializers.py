from django.core.exceptions import ValidationError
from rest_framework import serializers

from familybudget.budgets.models import Budget
from familybudget.users.models import User, Family, Invitation


class BudgetSerializer(serializers.ModelSerializer[Budget]):
    class Meta:
        model = Budget
        fields = ["name", 'saldo']