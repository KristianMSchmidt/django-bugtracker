from django.contrib import admin
from .models import Project

# The field we want to show in the admin
class ProjectAdmin(admin.ModelAdmin):
    list_display= ('title', 'description')

# Register your models here.
admin.site.register(Project, ProjectAdmin)

