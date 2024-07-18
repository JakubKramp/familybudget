from django.core.exceptions import ValidationError
from rest_framework import serializers

from familybudget.users.models import Family, Invitation, User


class LightUserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["name", "id"]


class RegisterUserSerializer(serializers.ModelSerializer[User]):
    password = serializers.CharField(write_only=True)
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = User
        fields = ["id", "email", "name", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(LightUserSerializer):
    class Meta:
        model = User
        fields = [*LightUserSerializer.Meta.fields, "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class FamilySerializer(serializers.ModelSerializer[Family]):
    class Meta:
        model = Family
        fields = ("family_name", "members")

    def create(self, validated_data):
        family = super().create(validated_data)
        family.members.add(self.context["request"].user)
        family.save()
        return family


class ListInvitationsSerializer(serializers.ModelSerializer[Invitation]):
    family = serializers.CharField(source="family.family_name")

    class Meta:
        model = Invitation
        fields = ["id", "user", "sent_by", "family", "status"]


class InvitationSerializer(serializers.ModelSerializer[Invitation]):
    sent_by = serializers.PrimaryKeyRelatedField(read_only=True, required=False)

    class Meta:
        model = Invitation
        fields = ["id", "user", "sent_by", "family", "status", "created_at"]

    def validate(self, data):
        if self.instance:
            if self.instance.status != Invitation.Status.PENDING:
                raise ValidationError(
                    {"status": "You can only update invitations with `Pending status`"},
                    code="Invitation already responded",
                )
            status = data.get("status")
            if status == Invitation.Status.EXPIRED:
                raise ValidationError(
                    {"status": "Expired status can only be set automatically"},
                    code="Invalid status",
                )
            if (
                self.context["request"].user != self.instance.sent_by
                and status == Invitation.Status.CANCELED
            ):
                raise ValidationError(
                    {"status": "Only User that sent the invitation can cancel it"},
                    code="Invalid user",
                )
        return super().validate(data)

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if instance.status == Invitation.Status.ACCEPTED:
            instance.family.members.add(instance.user)
            instance.family.save()
        return instance

    def create(self, validated_data):
        if validated_data.get("user") == self.context["request"].user:
            raise ValidationError(
                {"user": "Cant send invitation to yourself"},
                code="Invalid user",
            )
        validated_data["sent_by"] = self.context["request"].user
        return super().create(validated_data)
