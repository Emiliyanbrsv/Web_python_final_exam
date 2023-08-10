from django.contrib import admin

from events_management.app_auth.models import AppUser


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'profile_type')
    list_filter = ('profile_type',)

    ordering = ['pk']