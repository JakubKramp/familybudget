from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from familybudget.budgets.api.filters import BudgetCategoryFilter
from familybudget.budgets.api.filters import BudgetFilter
from familybudget.budgets.api.filters import TransactionFilter
from familybudget.budgets.api.permissions import IsOwnerOrReadOnly
from familybudget.budgets.api.serializers import BudgetCategorySerializer
from familybudget.budgets.api.serializers import BudgetSerializer
from familybudget.budgets.api.serializers import ListBudgetSerializer
from familybudget.budgets.api.serializers import ListTransactionsSerializer
from familybudget.budgets.api.serializers import TransactionSerializer
from familybudget.budgets.models import Budget
from familybudget.budgets.models import BudgetCategory
from familybudget.budgets.models import Transaction


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
            | Q(owner=self.request.user),
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
    RetrieveModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet,
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
