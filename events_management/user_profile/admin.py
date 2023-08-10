from django.contrib import admin

from events_management.user_profile.models import Profile, Organizer


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'gender')
    list_filter = ('user',)

    ordering = ['pk']

    fieldsets = (
        (
            'Personal info',
            {
                'fields': ('first_name', 'last_name', 'date_of_birth',)
            }
        ),
        (
            'Additional info',
            {
                'fields': ('phone_number', 'gender', 'profile_image',)
            }
        ),
        (
            'App_auth user',
            {
                'fields': ('user',)
            }
        )
    )


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'user', 'website', 'phone_number')
    search_fields = ('name', 'user__email', 'website', 'phone_number')
    list_filter = ('user',)

    ordering = ['pk']

    fieldsets = (
        (
            'Organizer info',
            {
                'fields': ('name', 'description', 'website', 'phone_number', 'logo')
            }
        ),
        (
            'App_auth user',
            {
                'fields': ('user',)
            }
        ),
    )
