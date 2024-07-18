import pytest
from rest_framework.test import APIClient

from familybudget.users.models import User
from familybudget.users.tests.factories import UserFactory


@pytest.fixture()
def user(db) -> User:
    return UserFactory()

@pytest.fixture()
def api_client():
    return APIClient()
