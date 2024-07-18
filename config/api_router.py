from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from familybudget.budgets.api.views import BudgetCategoryViewSet
from familybudget.budgets.api.views import BudgetViewSet
from familybudget.budgets.api.views import TransactionViewSet
from familybudget.users.api.views import FamilyViewSet
from familybudget.users.api.views import InvitationViewSet
from familybudget.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet, basename="user")
router.register("families", FamilyViewSet)
router.register("invitations", InvitationViewSet)
router.register("budgets", BudgetViewSet)
router.register(
    "budget-categories", BudgetCategoryViewSet, basename="budget-categories",
)
router.register("transactions", TransactionViewSet)


app_name = "api"
urlpatterns = router.urls
