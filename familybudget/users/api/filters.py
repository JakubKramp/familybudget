from django_filters import rest_framework as filters


class InvitationFilter(filters.FilterSet):
    status = filters.CharFilter(field_name="status", lookup_expr='iexact')

    class Meta:
        model = Invitation
        fields = ['status']