from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('type', 'sender', 'receiver')


# Register your models here.
admin.site.register(Notification, NotificationAdmin)
