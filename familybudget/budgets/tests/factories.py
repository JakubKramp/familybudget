from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from familybudget.budgets.models import Budget, BudgetCategory, Transaction
from familybudget.users.tests.factories import UserFactory


class BudgetCategoryFactory(DjangoModelFactory):
    name = Faker("name")

    class Meta:
        model = BudgetCategory


class BudgetFactory(DjangoModelFactory):
    name = Faker("name")
    category = SubFactory(BudgetCategoryFactory)
    owner = SubFactory(UserFactory)

    class Meta:
        model = Budget


class IncomeFactory(DjangoModelFactory):
    budget = SubFactory(BudgetFactory)
    amount = Faker("pyint")
    transaction_type = Transaction.TransactionType.INCOME
    author = SubFactory(UserFactory)

    class Meta:
        model = Transaction


class ExpenseFactory(DjangoModelFactory):
    budget = SubFactory(BudgetFactory)
    amount = Faker("number")
    transaction_type = Transaction.TransactionType.EXPENSE
    author = SubFactory(UserFactory)

    class Meta:
        model = Transaction
