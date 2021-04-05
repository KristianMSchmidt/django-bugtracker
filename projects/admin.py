from django.contrib import admin
from .models import Project
from tickets.models import Ticket

class TicketInline(admin.TabularInline):
    model = Ticket

# The field we want to show in the admin
class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        TicketInline,
    ]
    list_display= ('title', 'description', 'created_by', 'created_at', 'updated_at')


# Register your models here.
admin.site.register(Project, ProjectAdmin)
