import pytest

from familybudget.users.models import User
from familybudget.users.tests.factories import UserFactory


@pytest.fixture()
def user(db) -> User:
    return UserFactory()
