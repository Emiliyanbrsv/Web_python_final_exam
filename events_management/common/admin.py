from django.contrib import admin

from events_management.common.models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'city_name', 'country')
    list_filter = ('country',)

    ordering = ['pk']

    fieldsets = (description
        (
            'Location info',
            {
                'fields': ('city_name', 'country', 'description', 'image')
            }
        ),
    )
