from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken

from apps.common.models import BaseModel
from apps.users.managers import UserManager


class User(AbstractUser, BaseModel):
    username = None
    first_name = models.CharField(_("first name"), max_length=255, null=True, blank=True)
    last_name = models.CharField(_("last name"), max_length=255, null=True, blank=True)
    full_name = models.CharField(_("full name"), max_length=255)
    email = models.EmailField(_("email"), null=True, blank=True)
    phone_number = PhoneNumberField(_("phone number"), max_length=32, unique=True)
    birth_date = models.DateField(_("birth date"), null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["full_name"]

    @property
    def tokens(self):
        token = RefreshToken.for_user(self)
        return {"access": str(token.access_token), "refresh": str(token)}

    def __str__(self):
        return f"{self.full_name} - {self.phone_number} - {self.email}"

    def save(self, *args, **kwargs):
        if self.phone_number:
            user = User.objects.filter(phone_number=self.phone_number).first()
            if user and user.id != self.id:
                raise ValidationError(_("User with this phone number already exists."))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ("-created_at",)
