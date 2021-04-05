from django.contrib import admin
from .models import Ticket

class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'submitter',
                    'created_at', 'updated_at', 'developer', 'status', 'priority', 'type')

# Register your models here.
admin.site.register(Ticket, TicketAdmin)
