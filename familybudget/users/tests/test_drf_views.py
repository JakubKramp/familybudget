import json
from http import HTTPStatus

import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory

from familybudget.users.api.views import UserViewSet
from familybudget.users.models import User
from familybudget.users.tests.factories import InvitationFactory


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

    def test_update_invitation(self, user, api_client):
        invitation = InvitationFactory(user=user)
        api_client.force_authenticate(user=user)
        invitation_data = {"status": "AC"}
        api_client.patch(
            reverse("api:invitation-detail", args=[invitation.id]),
            data=json.dumps(invitation_data),
            content_type="application/json",
        )
        assert user in invitation.family.members.all()

    def test_invitation_to_self(self, user, api_client):
        api_client.force_authenticate(user=user)
        invitation_data = {"user": user.id}
        response = api_client.post(
            reverse("api:invitation-list"),
            data=json.dumps(invitation_data),
            content_type="application/json",
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_update_invitation_wrong_status(self, user, api_client):
        invitation = InvitationFactory(user=user)
        api_client.force_authenticate(user=user)
        invitation_data = {"status": "EX"}
        response = api_client.patch(
            reverse("api:invitation-detail", args=[invitation.id]),
            data=json.dumps(invitation_data),
            content_type="application/json",
        )
        assert (response.data["status"][0] ==
                "Expired status can only be set automatically")
        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_cancel_invitation(self, user, api_client):
        invitation = InvitationFactory(user=user)
        api_client.force_authenticate(user=user)
        invitation_data = {"status": "CA"}
        response = api_client.patch(
            reverse("api:invitation-detail", args=[invitation.id]),
            data=json.dumps(invitation_data),
            content_type="application/json",
        )
        assert (response.data["status"][0] ==
                "Only User that sent the invitation can cancel it")
        assert response.status_code == HTTPStatus.BAD_REQUEST

