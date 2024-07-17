from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from familybudget.budgets.api.views import BudgetViewSet
from familybudget.users.api.views import UserViewSet, FamilyViewSet, InvitationViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("families", FamilyViewSet)
router.register("invitations", InvitationViewSet)
router.register("budgets", BudgetViewSet)


app_name = "api"
urlpatterns = router.urls
