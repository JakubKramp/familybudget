from django.db.models import Q
from rest_framework.mixins import (
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from familybudget.budgets.api.filters import (
    BudgetFilter,
    BudgetCategoryFilter,
    TransactionFilter,
)
from familybudget.budgets.api.permissions import IsOwnerOrReadOnly
from familybudget.budgets.api.serializers import (
    BudgetSerializer,
    BudgetCategorySerializer,
    ListBudgetSerializer,
    TransactionSerializer,
    ListTransactionsSerializer,
)
from familybudget.budgets.models import Budget, Transaction, BudgetCategory

from django_filters import rest_framework as filters


class BudgetViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    serializer_class = BudgetSerializer
    serializer_classes = {
        "retrieve": BudgetSerializer,
        "list": ListBudgetSerializer,
    }
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Budget.objects.all()
    lookup_field = "pk"
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BudgetFilter

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(
            Q(users=self.request.user)
            | Q(families__in=self.request.user.families.all())
            | Q(owner=self.request.user)
        ).distinct()

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)


class BudgetCategoryViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    serializer_class = BudgetCategorySerializer
    permission_classes = (IsAuthenticated,)
    queryset = BudgetCategory.objects.all()
    lookup_field = "pk"
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BudgetCategoryFilter


class TransactionViewSet(
    RetrieveModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet
):
    serializer_class = TransactionSerializer
    serializer_classes = {
        "retrieve": TransactionSerializer,
        "list": ListTransactionsSerializer,
    }
    permission_classes = (IsAuthenticated,)
    queryset = Transaction.objects.all()
    lookup_field = "pk"
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TransactionFilter

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.serializer_class)

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(author=self.request.user)
