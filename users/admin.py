from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    model = CustomUser

    fieldsets = (
        (None, {
            "fields": (
                "email",
                "phone_number",
                "first_name",
                "last_name",
            )
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
    )

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )

    ordering = ("email",)