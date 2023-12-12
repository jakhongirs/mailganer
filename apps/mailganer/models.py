from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.users.models import User


class EmailTemplate(BaseModel):
    name = models.CharField(_("Name"), max_length=255)
    template = models.TextField(_("Template"))

    class Meta:
        verbose_name = _("Email template")
        verbose_name_plural = _("Email templates")

    def __str__(self):
        return self.name


class EmailDistribution(BaseModel):
    template = models.ForeignKey("mailganer.EmailTemplate", on_delete=models.CASCADE)
    users = models.ManyToManyField(
        User, verbose_name=_("Users"), null=True, blank=True, related_name="email_distributions"
    )
    send_to_all = models.BooleanField(_("Send to all"), default=False)

    class Meta:
        verbose_name = _("Email distribution")
        verbose_name_plural = _("Email distributions")

    def __str__(self):
        return f"{self.id}"


class UserEmailDistribution(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_email_distributions")
    email_distribution = models.ForeignKey(
        EmailDistribution,
        on_delete=models.CASCADE,
        verbose_name=_("Email distribution"),
        related_name="user_email_distributions",
    )
    is_read = models.BooleanField(_("Is read"), default=False)

    class Meta:
        verbose_name = _("User email distribution")
        verbose_name_plural = _("User email distributions")

    def __str__(self):
        return f"{self.user}"
