from django.contrib import admin

from apps.mailganer.models import (EmailDistribution, EmailTemplate,
                                   UserEmailDistribution)


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "template")
    search_fields = ("name",)


@admin.register(EmailDistribution)
class EmailDistributionAdmin(admin.ModelAdmin):
    list_display = ("id", "template", "send_to_all")
    search_fields = ("users__email",)
    list_filter = ("send_to_all",)


@admin.register(UserEmailDistribution)
class UserEmailDistributionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "email_distribution", "is_read")
    search_fields = ("user__email",)
    list_filter = ("is_read",)
