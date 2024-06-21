from django.contrib import admin
import django.contrib.auth.admin as ad
from .models import CustomUser


class CustomUserAdmin(ad.UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'phone',
                    'first_name', 'last_name',]


admin.site.register(CustomUser, CustomUserAdmin)
