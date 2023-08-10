from django.contrib import admin

from events_management.event.models import Event, EventRegistration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'start_date_time', 'end_date_time', 'location', 'slug')
    list_filter = ('location', 'start_date_time')

    ordering = ['pk']

    fieldsets = (
        (
            'Event info',
            {
                'fields': ('name', 'start_date_time', 'end_date_time', 'image')
            }
        ),
        (
            'Additional info',
            {
                'fields': ('location', 'organizer')
            }
        ),
    )


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'attendees', 'event')
    ordering = ['pk']

    fieldsets = (
        (
            'Event registration',
            {
                'fields': ('first_name', 'last_name', 'attendees', 'phone_number')
            }
        ),
        (
            'Additional info',
            {
                'fields': ('user', 'event')
            }
        )
    )
