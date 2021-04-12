from django.contrib import admin
from .models import Ticket, TicketEvent


class TicketEventInline(admin.TabularInline):
    model = TicketEvent
    extra = 0

class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'project', 'submitter',
                    'created_at', 'updated_at', 'developer', 'status', 'priority', 'type')

    inlines = [
        TicketEventInline,
    ]
    list_filter = ("status","priority","type")
    search_fields = ("title",)


class TicketEventAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'property_changed', 'old_value', 'new_value', 'user', 'created_at')

# Register your models here.
admin.site.register(Ticket,TicketAdmin)
admin.site.register(TicketEvent, TicketEventAdmin)


