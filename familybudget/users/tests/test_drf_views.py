import pytest
from rest_framework.test import APIRequestFactory

from familybudget.users.api.views import UserViewSet
from familybudget.users.models import User


class TestUserViewSet:
    @pytest.fixture()
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)  # type: ignore[call-arg, arg-type, misc]

        assert response.data == {
            "name": user.name,
            "id": user.id,
            "url": f"http://testserver/api/users/{user.pk}/",
        }


class TestInvitationViewSet:
    def test_update_invitation(self):
        pass

    def test_update_invitation_wrong_status(self):
        pass

    def test_cancel_invitation(self):
        pass

    def test_cancel_invitation_wrong_user(self):
        pass
