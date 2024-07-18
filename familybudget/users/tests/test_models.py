from familybudget.users.models import User


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/api/users/{user.pk}/"

def test_invitation_is_expired(user):
    pass

def test_invitation_to_own_family():
    pass

def test_self_invitation():
    pass

def test_invite_to_alien_family():
    pass