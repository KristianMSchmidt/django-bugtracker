from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from projects.models import Project
from tickets.models import Ticket
CustomUser = get_user_model()

#ADDITIONAL_USER_FIELDS = (
#    ('Role', {'fields': ('role',)}),
#)


class TicketDeveloperInline(admin.TabularInline):
    model = Ticket
    fk_name = 'developer'
    extra = 0
    verbose_name = "Ticket assignment"
    verbose_name_plural = "Ticket assignments"


class TicketSubmitterInline(admin.TabularInline):
    model = Ticket
    fk_name = 'submitter'
    extra = 0
    verbose_name = "Ticket submission"
    verbose_name_plural = "Ticket submissions"

class EnrollmentsInline(admin.TabularInline):
    model = Project.users.through
    extra = 0
    verbose_name = "Project enrollment"
    verbose_name_plural = "Project enrollments"

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'role', 'email']
    list_filter = ("role",)

    inlines = [EnrollmentsInline, TicketDeveloperInline, TicketSubmitterInline]
    # Fields to show when creating user in admin. Default is just the required fields: email and username
    #add_fieldsets = UserAdmin.add_fieldsets  
  
    # Fields shown in admin user details
    #fieldsets = UserAdmin.fieldsets + ADDITIONAL_USER_FIELDS
    fieldsets = ((None, {'fields': ('username', 'password')}), ('Role', {'fields': ('role',)}), ('Personal info', {'fields': ('first_name', 'last_name', 'email')}), ('Permissions', {'fields': (
        'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}), ('Important dates', {'fields': ('last_login', 'date_joined')}))

admin.site.register(CustomUser, CustomUserAdmin)
