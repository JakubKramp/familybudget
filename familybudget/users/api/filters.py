from django_filters import rest_framework as filters

from familybudget.users.models import Invitation


class InvitationFilter(filters.FilterSet):
    status = filters.CharFilter(field_name="status", lookup_expr='iexact')

    class Meta:
        model = Invitation
        fields = ['status']