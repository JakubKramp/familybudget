from datetime import timedelta

import pytest
from django.conf import settings
from django.utils import timezone

from familybudget.users.models import User
from familybudget.users.tests.factories import InvitationFactory


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/api/users/{user.pk}/"

@pytest.mark.django_db()
def test_invitation_is_expired():
    invitation = InvitationFactory()
    invitation.created_at = (timezone.now() -
                             timedelta(days=(settings.INVITATION_EXPIRE_DAYS + 1)))
    invitation.save()
    assert invitation.is_expired
