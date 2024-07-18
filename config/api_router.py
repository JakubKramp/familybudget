from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from familybudget.budgets.api.views import (
    BudgetCategoryViewSet,
    BudgetViewSet,
    TransactionViewSet,
)
from familybudget.users.api.views import (
    FamilyViewSet,
    InvitationViewSet,
    RegisterViewSet,
    UserViewSet,
)

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet, basename="user")
router.register("register", RegisterViewSet, basename="register")
router.register("families", FamilyViewSet)
router.register("invitations", InvitationViewSet)
router.register("budgets", BudgetViewSet)
router.register(
    "budget-categories", BudgetCategoryViewSet, basename="budget-categories",
)
router.register("transactions", TransactionViewSet)


app_name = "api"
urlpatterns = router.urls
