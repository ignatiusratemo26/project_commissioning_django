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


    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        fieldsets = tuple(
            (name, {'fields': [field for field in data['fields'] if field != 'email']})
            for name, data in fieldsets
        )
        return fieldsets

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        return tuple(field for field in list_display if field != 'email')