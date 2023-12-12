from django.contrib import admin

from apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone_number", "email")
    search_fields = ("full_name", "phone_number", "email")
