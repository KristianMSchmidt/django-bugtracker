from django.contrib import admin
from .models import Project
from tickets.models import Ticket

class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0


class EnrollmentsInline(admin.TabularInline):
    model = Project.users.through
    extra = 0   
    verbose_name = "Enrolled user"
    verbose_name_plural = "Enrolled users"

class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        TicketInline, EnrollmentsInline
    ]
    # The field we want to show in the admin
    list_display = ('title', 'description', 'created_by', 
                    'created_at', 'updated_at')
    exclude = ('users',)


# Register your models here.
admin.site.register(Project, ProjectAdmin)
