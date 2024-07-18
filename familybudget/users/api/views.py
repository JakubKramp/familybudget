from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from django_filters import rest_framework as filters
from familybudget.users.models import User, Family, Invitation
from .filters import InvitationFilter

from .serializers import UserSerializer, FamilySerializer, ListInvitationsSerializer, InvitationSerializer


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class FamilyViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = FamilySerializer
    permission_classes = (IsAuthenticated,)
    queryset = Family.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(members=self.request.user)


class InvitationViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = ListInvitationsSerializer
    permission_classes = (IsAuthenticated,)
    serializer_classes = {'retrieve': InvitationSerializer,
                          'create': InvitationSerializer,
                          'update': InvitationSerializer,
                          'partial_update': InvitationSerializer,
    }
    queryset = Invitation.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = InvitationFilter
    lookup_field = "pk"

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(Q(user=self.request.user) | Q(sent_by=self.request.user))

