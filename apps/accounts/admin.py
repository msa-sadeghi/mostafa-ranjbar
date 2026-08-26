from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["username", "full_name", "email", "user_type", "is_active", "is_verified", "created_at"]
    list_filter = ["user_type", "is_active", "is_verified", "is_staff"]
    search_fields = ["username", "email", "first_name", "last_name", "national_code"]
    ordering = ["-created_at"]

    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "اطلاعات اضافی",
            {"fields": ("user_type", "phone_number", "national_code", "department", "avatar", "is_verified")},
        ),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("اطلاعات اضافی", {"fields": ("email", "user_type", "phone_number", "national_code")}),
    )
    list_editable = ["is_active", "is_verified"]
