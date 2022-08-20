from django.contrib import admin

from .models import *


class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('event_name', 'contract', 'client', 'support_contact',
                       'status', 'attendees', 'event_date_time', 'notes')
        }),
    )

    readonly_fields = ['client', ]


admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event, EventAdmin)
