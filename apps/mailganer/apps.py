from django.apps import AppConfig


class MailganerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.mailganer"

    def ready(self):
        import apps.mailganer.signals  # noqa: F401
