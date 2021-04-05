from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

CustomUser = get_user_model()

#ADDITIONAL_USER_FIELDS = (
#    ('Role', {'fields': ('role',)}),
#)

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'role', 'email']

    # Fields to show when creating user in admin. Default is just the required fields: email and username
    #add_fieldsets = UserAdmin.add_fieldsets  
  
    # Fields shown in admin user details
    #fieldsets = UserAdmin.fieldsets + ADDITIONAL_USER_FIELDS
    fieldsets = ((None, {'fields': ('username', 'password')}), ('Role', {'fields': ('role',)}), ('Personal info', {'fields': ('first_name', 'last_name', 'email')}), ('Permissions', {'fields': (
        'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}), ('Important dates', {'fields': ('last_login', 'date_joined')}))

admin.site.register(CustomUser, CustomUserAdmin)
