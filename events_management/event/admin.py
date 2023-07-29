from django.contrib import admin

from events_management.event.models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass
