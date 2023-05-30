from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'online')
    list_filter = ('online', )


admin.site.register(User, CustomUserAdmin)
