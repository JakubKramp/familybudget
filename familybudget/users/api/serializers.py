from django.core.exceptions import ValidationError
from rest_framework import serializers

from familybudget.users.models import User, Family, Invitation


class LightUserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["name", 'id']

class UserSerializer(LightUserSerializer):
    class Meta:
        model = User
        fields = LightUserSerializer.Meta.fields + ["url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }

class FamilySerializer(serializers.ModelSerializer[Family]):
    class Meta:
        model = Family
        fields = ('family_name', 'members')

    def create(self, validated_data):
        family = super().create(validated_data)
        family.members.add(self.context['request'].user)
        family.save()
        return family


class ListInvitationsSerializer(serializers.ModelSerializer[Invitation]):
    family = serializers.CharField(source='family.family_name')
    class Meta:
        model = Invitation
        fields = ['id', 'user', 'sent_by', 'family', 'status']


class InvitationSerializer(ListInvitationsSerializer):
    class Meta:
        model = Invitation
        fields = ListInvitationsSerializer.Meta.fields + ['created_at']

    def validate(self, data):
        if self.instance.status != Invitation.Status.PENDING:
            raise ValidationError(
                {'status': 'You can only update invitations with `Pending status`'},
                code='Invitation already responded',
            )
        status = data.get('status')
        if status == Invitation.Status.EXPIRED:
            raise ValidationError(
                {'status': 'Expired status can only be set automatically'},
                code='Invalid status',
            )
        if self.context['request'].user != self.instance.sent_by and status == Invitation.Status.CANCELED:
            raise ValidationError(
                {'status': 'Only User that sent the invitation cna cancel it'},
                code='Invalid user',
            )

        return data

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if instance.status == Invitation.Status.ACCEPTED:
            instance.family.members.add(instance.user)
            instance.family.save()
        return instance


