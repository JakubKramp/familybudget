import pytest
from familybudget.users.tests.factories import UserFactory, FamilyFactory


@pytest.mark.django_db()
def test_users_with_access(positive_budget):
    user = UserFactory()
    family = FamilyFactory()
    family_member = UserFactory()
    family.members.add(family_member)
    family.save()
    positive_budget.users.add(user)
    assert user in positive_budget.get_users_with_access()
    positive_budget.families.add(family)
    assert family_member in positive_budget.get_users_with_access()
    assert len(positive_budget.get_users_with_access()) == 3
