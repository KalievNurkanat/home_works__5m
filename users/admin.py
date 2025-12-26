from django.contrib import admin
from .models import *
from django.contrib import admin
from users.models import CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.register(ConfirmCode)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "email", "is_active")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "phone_number", "password", "is_active")}),
        ("Important dates", {"fields": ("last_login",)}),
    )