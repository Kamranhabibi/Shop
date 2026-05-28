# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):

    list_display = ['first_name','last_name','email', 'phone', 'is_admin', 'is_active']
    list_filter = ['is_admin', 'is_active']
    search_fields = ['email', 'phone']
    ordering = ['email']


    fieldsets = (
        (None, {"fields": ("first_name","last_name","email", "phone", "password")}),
        (_("Personal info"), {"fields": ()}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_admin",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    # این بخش برای صفحه "افزودن کاربر" هست
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "phone","first_name","last_name", "password1", "password2"),
            },
        ),
    )

# رجیستر کردن مدل و ادمین سفارشی در پنل
admin.site.register(CustomUser, CustomUserAdmin)