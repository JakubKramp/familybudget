from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from familybudget.users.models import User
from familybudget.users.tests.factories import InvitationFactory


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/api/users/{user.pk}/"


def test_invitation_is_expired():
    invitation = InvitationFactory(created_at=timezone.now() -
                                   timedelta(days=(settings.INVITATION_EXPIRE_DAYS +1)))
    assert invitation.is_expired()


def test_invitation_to_own_family():
    pass


def test_self_invitation():
    pass


def test_invite_to_alien_family():
    pass
