from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, 
         {'fields': ('phone_number','role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, 
         {'fields': ('role',)}),
    )
    list_display = UserAdmin.list_display + ('phone_number','role',)
    list_filter = UserAdmin.list_filter + ('role',)
    search_fields = UserAdmin.search_fields + ('role',)
    ordering = UserAdmin.ordering + ('role',)


