import uuid

from django.conf import settings
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from apps.mailganer.models import EmailDistribution, UserEmailDistribution
from apps.mailganer.tasks import send_email_task
from apps.users.models import User


@receiver(post_save, sender=EmailDistribution)
def create_email_distribution_all(sender, instance, created, **kwargs):
    if created and instance.send_to_all:
        if settings.DEBUG:
            tracking_pixel_url = f"http://localhost:8000/api/v1/mailganer/tracking/{uuid.uuid4()}/"
        else:
            tracking_pixel_url = f"https://bizni-domain.com/track/{uuid.uuid4()}/"

        UserEmailDistribution.objects.bulk_create(
            [
                UserEmailDistribution(user=user, email_distribution=instance, tracking_pixel_url=tracking_pixel_url)
                for user in User.objects.all()
            ]
        )

        for user in User.objects.all():
            send_email_task.delay(
                email=settings.EMAIL_HOST_USER,
                subject=instance.template.name,
                message=instance.template.template,
                recipient_list=[user.email],
                user_fullname=user.full_name,
                user_birthdate=user.birth_date,
                tracking_pixel_url=tracking_pixel_url,
            )


@receiver(m2m_changed, sender=EmailDistribution.users.through)
def create_user_email_distribution(sender, instance, action, **kwargs):
    if action == "post_add":
        if instance.send_to_all:
            instance.users.clear()
        else:
            if settings.DEBUG:
                tracking_pixel_url = f"http://localhost:8000/api/v1/mailganer/tracking/{uuid.uuid4()}/"
            else:
                tracking_pixel_url = f"https://bizni-domain.com/track/{uuid.uuid4()}/"

            UserEmailDistribution.objects.bulk_create(
                [
                    UserEmailDistribution(user=user, email_distribution=instance, tracking_pixel_url=tracking_pixel_url)
                    for user in instance.users.all()
                ]
            )

            for user in instance.users.all():
                send_email_task.delay(
                    email=settings.EMAIL_HOST_USER,
                    subject=instance.template.name,
                    message=instance.template.template,
                    recipient_list=[user.email],
                    user_fullname=user.full_name,
                    user_birthdate=user.birth_date,
                    tracking_pixel_url=tracking_pixel_url,
                )
