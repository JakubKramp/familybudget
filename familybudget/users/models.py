from typing import ClassVar

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for family-budget.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = models.CharField(blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = models.EmailField(unique=True)
    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


class Family(models.Model):
    """
    Model for simpler sharing budgets with many people.
    One user can be member of many families (ex. through marriage)
    """
    family_name = models.CharField(max_length=50)
    members = models.ManyToManyField(User, related_name='families')

    def __str__(self) -> str:
        return f'Family {self.family_name} with an id of {self.pk}'


class Invitation(models.Model):
    """
    Model for inviting users to families. Any member of a family can send an invitation.
    """
    class Status(models.TextChoices):
        PENDING = 'PE', 'Pending'
        REFUSED = 'RF', 'Refused'
        CANCELED = 'CA', 'Canceled'
        ACCEPTED = 'AC', 'Accepted'
        EXPIRED = 'EX', 'Expired'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations')
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='invitations')
    sent_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('status', 'user', 'family')

    @property
    def is_expired(self) -> bool:
        return self.status == self.Status.PENDING and (timezone.now()-self.created_at).days > settings.INVITATION_EXPIRE_DAYS

    def expire(self):
        if self.status == self.Status.PENDING and (timezone.now()-self.created_at).days > settings.INVITATION_EXPIRE_DAYS:
            self.status = self.Status.EXPIRED
            self.save()

    def __str__(self) -> str:
        return f"Invitation to family {self.family.family_name} for {self.user} sent_ by {self.sent_by}"

    def clean(self):
        super().clean()
        if self.user in self.family.members.all():
            raise ValidationError('User cant be invited to family he is already a part of')
        if self.sent_by not in self.family.members.all():
            raise ValidationError('User can be invited to a family only by its members')
        if self.sent_by == self.user:
            raise ValidationError('User cant send an invitation to himself')