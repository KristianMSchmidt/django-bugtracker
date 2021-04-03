from django.urls import path
from .views import DemoLoginView

urlpatterns = [
    path('', DemoLoginView.as_view(), name='demo_login')
]
