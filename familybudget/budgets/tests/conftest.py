import pytest

from familybudget.budgets.tests.factories import (
    BudgetFactory,
    ExpenseFactory,
    IncomeFactory,
)


@pytest.fixture()
def negative_budget():
    budget = BudgetFactory(allow_negative_saldo=True)
    budget.transactions.add(ExpenseFactory())
    return budget


@pytest.fixture()
def positive_budget():
    budget = BudgetFactory()
    budget.transactions.add(IncomeFactory())
    return budget
