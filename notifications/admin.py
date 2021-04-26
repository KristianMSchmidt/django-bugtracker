from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('type', 'recipient', 'sender', 'created_at')

# Register your models here.
admin.site.register(Notification, NotificationAdmin)
