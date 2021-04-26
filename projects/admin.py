from django.contrib import admin
from .models import Project
from tickets.models import Ticket

class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0

class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        TicketInline #, EnrollmentsInline
    ]
    # The field we want to show in the admin
    list_display = ('title', 'description', 'created_by', 
                    'created_at', 'updated_at')
    search_fields = ('title',)



# Register your models here.
admin.site.register(Project, ProjectAdmin)
