from django.urls import path
from .views import DemoLoginView, AboutView

urlpatterns = [
    path('about', AboutView.as_view(), name='about'),
    path('', DemoLoginView.as_view(), name='demo_login')
]
