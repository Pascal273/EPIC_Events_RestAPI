from django.contrib import admin

from .models import *

admin.site.register(Client)
admin.site.register(Contract)
admin.site.register(Event)
admin.site.register(Team)
admin.site.register(TeamMembers)
