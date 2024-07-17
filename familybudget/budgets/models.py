

from typing import ClassVar

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone

from familybudget.users.models import User


class BudgetCategory(models.Model):
    """
    Model for grouping budgets in categories.
    """
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'Budget category {self.name}'



class Budget(models.Model):
    """
    Model for tracking expenses. Can be shared with individual users and entire families.
    """
    name = models.CharField(max_length=50)
    category = models.ForeignKey(BudgetCategory, null=True, blank=True, on_delete=models.SET_NULL)
    owner = models.ManyToManyField('users.User', null=True, blank=True, related_name='managed_budgets')
    users = models.ManyToManyField('users.User', null=True, blank=True, related_name='budgets')
    families = models.ManyToManyField('users.Family', null=True, blank=True, related_name='budgets')
    allow_negative_saldo = models.BooleanField(default=True, help_text='If set to True user can create transactions that will reduce this budgets saldo below 0')

    @property
    def saldo(self) -> int:
        income_sum = \
        self.transactions.filter(transaction_type=Transaction.TransactionType.INCOME).aggregate(total=Sum('amount'))[
            'total'] or 0
        expense_sum = \
        self.transactions.filter(transaction_type=Transaction.TransactionType.EXPENSE).aggregate(total=Sum('amount'))[
            'total'] or 0
        return income_sum - expense_sum

    def get_users_with_access(self):
        owners_q = Q(managed_budgets=self)

        users_q = Q(budgets=self)

        families_q = Q(family__budgets=self)

        combined_q = owners_q | users_q | families_q


        return User.objects.filter(combined_q).distinct()

    def __str__(self) -> str:
        return f'Budget {self.name} with an id of {self.pk}'


class Transaction(models.Model):
    """
    Model for inviting users to families. Any member of a family can send an invitation.
    """
    class TransactionType(models.TextChoices):
        INCOME = 'IN', 'Income'
        EXPENSE = 'EX', 'Expense'

    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='transactions')
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='transactions')
    amount = models.PositiveIntegerField()
    transaction_type = models.CharField(max_length=2, choices=TransactionType.choices, default=TransactionType.INCOME)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f"{self.transaction_type} to {self.budget}. Amount:{self.amount}"
