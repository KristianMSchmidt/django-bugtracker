from django.urls import path
from .views import NotificationsSeen

urlpatterns = [
    path('seen', NotificationsSeen.as_view(), name='notifications_seen'),
]
