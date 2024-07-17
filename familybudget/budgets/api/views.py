from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from familybudget.budgets.api.serializers import BudgetSerializer
from familybudget.budgets.models import Budget


class BudgetViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = BudgetSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Budget.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(shared_with_users=self.request.user)