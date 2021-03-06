from django.contrib import admin
from .models import Ticket, TicketComment, TicketEvent

class TicketAdmin(admin.ModelAdmin):

    list_display = ('title', 'description','project', 'submitter',
                    'created_at', 'updated_at', 'developer', 'status', 'priority', 'type')
    list_filter = ("status", "priority", "type")
    search_fields = ("title",'description','project__title')

    class TicketCommentInline(admin.TabularInline):
        model = TicketComment
        extra = 0

    class TicketEventInline(admin.TabularInline):
        model = TicketEvent
        extra = 0

    inlines = [
        TicketCommentInline, TicketEventInline
    ]
    def save_model(self, request, obj, form, change):
        obj.save(request=request)
   
class TicketEventAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'property_changed', 'old_value', 'new_value', 'user', 'created_at')


class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'commenter','message', 'created_at',)
    search_fields =('ticket__title', 'message')

    def save_model(self, request, obj, form, change):
        obj.save()

# Register your models here.
admin.site.register(Ticket,TicketAdmin)
admin.site.register(TicketEvent, TicketEventAdmin)
admin.site.register(TicketComment, TicketCommentAdmin)



